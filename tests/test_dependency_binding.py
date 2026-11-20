"""Offline dependency flattening and compact-model/full-provenance bindings.

The parent is a real temporary Git repository with a committed gitlink and
.gitmodules. Its child is ingested through the remote Git-tree/raw-blob reader
using an offline HTTP fixture with independently computed Git object hashes.
No repository code, real network, model or manually adjudicated labels are used.
"""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v4 as v4
import extraction_v5 as v5
import source_bundle as source
import test_extraction_v4 as toy
import test_source_only as remote_toy


MOUNT = "third_party/Engine"
CHILD_MARKER = "DEPENDENCY_UNIQUE_MARKER"


class DependencyBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="dependency binding parent ")
        cls.addClassCleanup(cls.directory.cleanup)
        root = Path(cls.directory.name)

        def git(*args):
            return subprocess.run(
                ["git", "-c", "commit.gpgsign=false", "-C", str(root), *args],
                capture_output=True, check=True, text=True,
            ).stdout.strip()

        git("init", "-q")
        git("config", "user.name", "Offline Fixture")
        git("config", "user.email", "fixture@example.test")
        # Missing imports generate a genuine unresolved evidence ledger large
        # enough to exercise projection truncation; these imports never execute.
        main = ('import os\n'
                'engine = os.path.join(os.path.dirname(__file__), "third_party/Engine")\n')
        main += "".join(f"from missing_{index:03d} import value_{index:03d}\n" for index in range(45))
        (root / "main.py").write_text(main, encoding="utf-8")
        (root / ".gitmodules").write_text(
            '[submodule "engine"]\n'
            ' path = third_party/Engine\n'
            ' url = https://github.com/owner/repo\n', encoding="utf-8")
        git("add", ".")
        git("update-index", "--add", "--cacheinfo", f"160000,{remote_toy.COMMIT},{MOUNT}")
        git("commit", "-qm", "Commit the pinned dependency fixture")
        parent_commit = git("rev-parse", "HEAD")
        raw_files = {
            "common.py": ("def serialize(value):\n"
                          "    # " + CHILD_MARKER + "\n"
                          "    return {\"payload\": value}\n").encode(),
            "formatting.py": b"def format_input(value):\n    return str(value)\n",
        }
        mocked_http, requested = remote_toy.SourceOnlyTests().fixture(raw_files)
        with mocked_http:
            repository = source.load_repository(str(root))
        source.validate_repository(repository)
        wrapper = repository["dependency_snapshots"][0]
        child = wrapper["snapshot"]
        source.validate_repository(child)
        if (repository["revision"] != parent_commit or child["revision"] != remote_toy.COMMIT
                or child.get("eligibility_policy") is not None):
            raise AssertionError("Fixture did not ingest independently pinned parent and child")
        paper, _, _, _, _ = toy.ExtractionV4Tests().fixtures()
        cls.paper = paper
        cls.repository = repository
        cls.child = child
        cls.requested = requested
        cls.document = v5.combine_inputs(paper, repository)

    def test_parent_gitlink_and_child_are_independently_validated_source_bundles(self):
        self.assertEqual(len(self.repository["dependency_snapshots"]), 1)
        self.assertEqual(self.repository["dependency_acquisition"][0]["status"], "resolved")
        self.assertEqual(self.repository["dependency_snapshots"][0]["source"], remote_toy.REPOSITORY)
        self.assertEqual(self.child["commit_binding"], "github_commit_tree_raw_blobs")
        self.assertNotEqual(self.repository["revision"], self.child["revision"])
        self.assertFalse(any("codeload.github.com" in url for url in self.requested))
        self.assertEqual(sum("raw.githubusercontent.com" in url for url in self.requested), 2)
        before = copy.deepcopy(self.repository)
        v5.combine_inputs(self.paper, self.repository)
        self.assertEqual(before, self.repository)

    def test_flattened_segments_keep_mount_and_child_origin_without_nested_payloads(self):
        document = self.document
        flattened = {part["path"]: part for part in document["segments"] if part.get("dependency_origin")}
        self.assertEqual(set(flattened), {MOUNT + "/" + part["path"] for part in self.child["segments"]})
        for original in self.child["segments"]:
            mounted = flattened[MOUNT + "/" + original["path"]]
            self.assertEqual(mounted["id"], f"repo:{mounted['path']}:L1-L{original['line_end']}")
            self.assertEqual(mounted["text"], original["text"])
            self.assertEqual(mounted["sha256"], original["sha256"])
            self.assertEqual(mounted["dependency_origin"], {
                "mount_path": MOUNT, "source": self.child["source"], "revision": self.child["revision"],
                "manifest_sha256": self.child["manifest_sha256"], "original_path": original["path"],
            })
        self.assertNotIn("dependency_snapshots", document["repository"])
        metadata = document["repository"]["dependencies"][0]
        self.assertEqual(metadata["mount_path"], MOUNT)
        for omitted in ("files", "segments", "dependency_snapshots"):
            self.assertNotIn(omitted, metadata)
        self.assertIn("inventory", metadata)
        v5.validate_input_binding(document)

    def test_dependency_citation_uses_child_commit_and_manifest(self):
        part = next(part for part in self.document["segments"] if part.get("path") == MOUNT + "/common.py")
        citation = {"segment_id": part["id"], "quote": 'return {"payload": value}'}
        located = v4._locate(citation, self.document, "code")
        self.assertEqual(located["path"], MOUNT + "/common.py")
        self.assertEqual(located["original_path"], "common.py")
        self.assertEqual(located["repository_source"], remote_toy.REPOSITORY)
        self.assertEqual(located["repository_revision"], self.child["revision"])
        self.assertEqual(located["repository_manifest_sha256"], self.child["manifest_sha256"])
        self.assertNotEqual(located["repository_revision"], self.document["repository"]["revision"])
        self.assertEqual(located["file_sha256"], part["sha256"])
        self.assertEqual((located["line_start"], located["line_end"]), (3, 3))
        altered = copy.deepcopy(self.document)
        altered["repository"]["dependencies"][0]["revision"] = "b" * 40
        with self.assertRaisesRegex(ValueError, "validated source identity"):
            v4._locate(citation, altered, "code")

    def test_child_revision_manifest_and_source_bytes_cannot_change_before_merge(self):
        mutations = (
            lambda wrapper: wrapper.update(revision="b" * 40),
            lambda wrapper: wrapper["snapshot"].update(manifest_sha256="0" * 64),
            lambda wrapper: wrapper["snapshot"].update(commit="b" * 40),
            lambda wrapper: wrapper["snapshot"]["segments"][0].update(text="changed child bytes\n"),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                repository = copy.deepcopy(self.repository)
                mutation(repository["dependency_snapshots"][0])
                with self.assertRaises(ValueError):
                    v5.combine_inputs(self.paper, repository)

    def test_compact_model_projection_omits_snapshots_and_duplicate_child_text(self):
        payload = v5.model_content(self.document)
        view = payload["repository"]
        self.assertEqual(view, self.document["model_repository"])
        self.assertNotIn("inventory", view)
        self.assertNotIn("dependency_snapshots", view)
        self.assertNotIn("tree_manifest", view["dependencies"][0])
        self.assertNotIn("source_acquisition", view["dependencies"][0])
        self.assertEqual(view["dependencies"][0]["revision"], self.child["revision"])
        self.assertNotIn("needed", view["evidence_expansion"])
        self.assertEqual(len(view["evidence_expansion"]["unresolved"]), 40)
        self.assertGreater(view["evidence_expansion"]["unresolved_total"], 40)
        self.assertEqual(json.dumps(payload).count(CHILD_MARKER), 1)
        self.assertNotIn(CHILD_MARKER, json.dumps(view))
        # Callers receive a copy of the projection, not a writable binding view.
        payload["repository"]["dependencies"][0]["revision"] = "changed caller copy"
        v5.validate_input_binding(self.document)

    def test_changed_projected_metadata_or_segments_fail_binding_checks(self):
        mutations = (
            lambda doc: doc["model_repository"].update(source="another-source"),
            lambda doc: doc["model_repository"]["dependencies"][0]["coverage"].update(reason="changed projected reason"),
            lambda doc: doc["segments"][-1].update(text="changed selected model source"),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                altered = copy.deepcopy(self.document)
                mutation(altered)
                with self.assertRaisesRegex(ValueError, "input binding"):
                    v5.model_content(altered)

    def test_full_provenance_remains_bound_when_the_model_projection_does_not_change(self):
        mutations = (
            lambda doc: doc["repository"]["dependencies"][0]["inventory"][0].update(bytes=999),
            lambda doc: doc["repository"]["dependency_metadata"].update(text="changed gitmodules metadata"),
            lambda doc: doc["repository"].update(source_binding="0" * 64),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                altered = copy.deepcopy(self.document)
                mutation(altered)
                self.assertEqual(v4._unbound_model_content(altered), v4._unbound_model_content(self.document))
                with self.assertRaisesRegex(ValueError, "input binding"):
                    v5.validate_input_binding(altered)

    def test_legacy_v4_document_without_a_model_projection_keeps_its_contract(self):
        _, _, legacy, extraction, review = toy.ExtractionV4Tests().fixtures()
        self.assertNotIn("model_repository", legacy)
        expected = {
            "source_type": legacy["media_type"],
            "segments": [{"id": part["id"], "text": part.get("reading_order_text", part["text"])}
                         for part in legacy["segments"]],
            "input_binding": legacy["sha256"], "repository": legacy["repository"],
            "paper_sha256": legacy["paper_sha256"],
        }
        self.assertEqual(v4.model_content(legacy), expected)
        self.assertEqual(v5.model_content(legacy), expected)
        self.assertEqual(v4.decide_extraction(extraction, review, legacy)["schema_version"], 4)


if __name__ == "__main__":
    unittest.main()
