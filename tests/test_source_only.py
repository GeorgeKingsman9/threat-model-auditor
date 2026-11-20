"""Offline checks for complete-tree, immutable-blob source-only fallback."""

import copy
import hashlib
import io
import json
import unittest
from unittest.mock import patch
from urllib.parse import unquote

import source_bundle as s


COMMIT = "a" * 40
REPOSITORY = "https://github.com/owner/repo"


def object_hash(kind, raw):
    return hashlib.sha1(f"{kind} {len(raw)}\0".encode() + raw).hexdigest()


def tree_fixture(files):
    entries = []

    def directory(prefix):
        children = {}
        for path, raw in files.items():
            if not path.startswith(prefix):
                continue
            remainder = path[len(prefix):]
            name, slash, _ = remainder.partition("/")
            if slash:
                children[name + "/"] = None
            else:
                children[name] = raw
        raw_tree = b""
        for name, raw in sorted(children.items()):
            path = prefix + name.rstrip("/")
            if raw is None:
                oid = directory(path + "/")
                mode, kind = "040000", "tree"
                entry = {"path": path, "mode": mode, "type": kind, "sha": oid}
            else:
                oid = object_hash("blob", raw)
                mode, kind = "100644", "blob"
                entry = {"path": path, "mode": mode, "type": kind, "sha": oid, "size": len(raw)}
            entries.append(entry)
            raw_tree += (mode.lstrip("0") + " " + name.rstrip("/")).encode() + b"\0" + bytes.fromhex(oid)
        return object_hash("tree", raw_tree)

    root = directory("")
    return {"sha": root, "truncated": False, "tree": entries}


class SourceOnlyTests(unittest.TestCase):
    def fixture(self, files, *, mutate_tree=None, mutate_commit=None, raw_files=None):
        tree = tree_fixture(files)
        commit = {"sha": COMMIT, "tree": {"sha": tree["sha"]}}
        if mutate_tree:
            mutate_tree(tree)
        if mutate_commit:
            mutate_commit(commit)
        requested = []
        raw_files = files if raw_files is None else raw_files

        class Response(io.BytesIO):
            headers = {}

            def __init__(self, url, raw):
                super().__init__(raw)
                self.url = url

            def geturl(self):
                return self.url

        def open_request(request, **kwargs):
            url = request.full_url
            requested.append(url)
            if url.startswith("https://codeload.github.com/"):
                raise TimeoutError("fixture archive timeout")
            if url == "https://api.github.com/repos/owner/repo/git/commits/" + COMMIT:
                return Response(url, json.dumps(commit).encode())
            if url.startswith("https://api.github.com/repos/owner/repo/git/trees/"):
                return Response(url, json.dumps(tree).encode())
            prefix = "https://raw.githubusercontent.com/owner/repo/" + COMMIT + "/"
            if url.startswith(prefix):
                path = unquote(url[len(prefix):])
                raw = raw_files[path]
                if isinstance(raw, Exception):
                    raise raw
                return Response(url, raw)
            raise AssertionError("Unexpected network target in offline fixture")

        return patch.object(s, "build_opener", return_value=type("Opener", (), {"open": staticmethod(open_request)})()), requested

    def test_archive_timeout_reads_all_source_and_excludes_labels_data_and_credentials(self):
        files = {"src/pipeline.py": b"pass\n", "src/runner.py": b"x = 1\n", "data/sample.py": b"PRIVATE_DATA",
                 "labels.py": b"PRIVATE_LABEL", "src/client.py": ("key = 'ghp_" + "A" * 36 + "'\n").encode()}
        mock, requested = self.fixture(files)
        with mock:
            snapshot = s.load_repository(REPOSITORY, revision=COMMIT)
        self.assertEqual(snapshot["commit_binding"], "github_commit_tree_raw_blobs")
        self.assertTrue(snapshot["coverage"]["inventory_complete"])
        self.assertFalse(snapshot["coverage"]["complete"])
        self.assertEqual(snapshot["omitted"][0]["reason"], "credential_like_content")
        self.assertEqual(snapshot["source_acquisition"]["attempts"][0]["failure_kind"], "timeout")
        self.assertEqual(snapshot["source_acquisition"]["fallback"]["status"], "succeeded")
        self.assertFalse(any("data/sample.py" in url or "labels.py" in url for url in requested))
        self.assertNotIn("PRIVATE_DATA", str(snapshot))
        self.assertNotIn("PRIVATE_LABEL", str(snapshot))
        s.validate_repository(snapshot)

    def test_full_source_is_hashed_before_original_character_budget_selection(self):
        mock, requested = self.fixture({"pipeline.py": b"pass\n", "runner.py": b"x = 1\n"})
        with mock:
            snapshot = s.load_repository(REPOSITORY, revision=COMMIT, max_chars=5)
        self.assertEqual(snapshot["coverage"]["eligible_files"], 2)
        self.assertFalse(snapshot["coverage"]["complete"])
        self.assertEqual(snapshot["omitted"][0]["reason"], "character_budget")
        self.assertTrue(snapshot["omitted"][0]["sha256"])
        self.assertEqual(sum("raw.githubusercontent.com" in url for url in requested), 2)
        s.validate_repository(snapshot)

    def test_one_failed_or_hash_mismatched_blob_never_returns_a_partial_snapshot(self):
        for raw in [b"evil\n", TimeoutError("fixture raw timeout")]:
            with self.subTest(raw=type(raw).__name__):
                mock, requested = self.fixture({"pipeline.py": b"pass\n"}, raw_files={"pipeline.py": raw})
                with mock, self.assertRaises(s.RepositoryError) as caught:
                    s.load_repository(REPOSITORY, revision=COMMIT)
                self.assertEqual(caught.exception.acquisition["fallback"]["status"], "failed")
                self.assertEqual(len(caught.exception.acquisition["attempts"]), 1)
                self.assertLessEqual(sum("raw.githubusercontent.com" in url for url in requested), 2)

    def test_truncated_wrong_commit_and_incomplete_or_forged_tree_fail_before_blob_reads(self):
        mutations = [
            {"mutate_tree": lambda d: d.update(truncated=True)},
            {"mutate_commit": lambda d: d.update(sha="b" * 40)},
            {"mutate_tree": lambda d: d["tree"].pop()},
            {"mutate_tree": lambda d: d["tree"][0].update(sha="b" * 40)},
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                mock, requested = self.fixture({"src/pipeline.py": b"pass\n"}, **mutation)
                with mock, self.assertRaises(s.RepositoryError):
                    s.load_repository(REPOSITORY, revision=COMMIT)
                self.assertFalse(any("raw.githubusercontent.com" in url for url in requested))

    def test_original_file_limit_is_explicit_without_fetching_oversized_blob(self):
        mock, requested = self.fixture({"pipeline.py": b"pass\n", "huge.py": b"x" * 30})
        with mock, patch.object(s, "MAX_FILE_BYTES", 20):
            snapshot = s.load_repository(REPOSITORY, revision=COMMIT)
        self.assertEqual(snapshot["omitted"][0]["reason"], "file_byte_limit")
        self.assertIsNone(snapshot["omitted"][0]["sha256"])
        self.assertFalse(any("huge.py" in url for url in requested))
        s.validate_repository(snapshot)

    def test_source_request_count_and_read_budgets_fail_before_blob_reads(self):
        for setting in [{"SOURCE_ONLY_MAX_FILES": 1}, {"MAX_READ_BYTES": 1}]:
            mock, requested = self.fixture({"pipeline.py": b"pass\n", "runner.py": b"pass\n"})
            with self.subTest(setting=setting), mock, patch.multiple(s, **setting), self.assertRaises(s.RepositoryError):
                s.load_repository(REPOSITORY, revision=COMMIT)
            self.assertFalse(any("raw.githubusercontent.com" in url for url in requested))

    def test_replay_rejects_tree_identity_inventory_and_blob_hash_tampering(self):
        mock, _ = self.fixture({"pipeline.py": b"pass\n"})
        with mock:
            snapshot = s.load_repository(REPOSITORY, revision=COMMIT)
        for mutate in [lambda d: d.update(tree_sha="b" * 40),
                       lambda d: d["tree_manifest"][0].update(size=99),
                       lambda d: d["inventory"][0].update(object_id="b" * 40)]:
            changed = copy.deepcopy(snapshot)
            mutate(changed)
            with self.assertRaises(s.RepositoryError):
                s.validate_repository(changed)


if __name__ == "__main__":
    unittest.main()
