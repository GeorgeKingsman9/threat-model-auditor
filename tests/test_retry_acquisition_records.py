"""Freeze real discovery/reader retry results through the URL-only entrypoint.

Only paper loading and the HTTP/DNS boundary are fixtures. Discovery, archive
ingestion, source validation, V4 binding and scan persistence run unchanged. No
author source, network endpoint, model, curated repository hint or gold is used.
"""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import socket
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v3
import extraction_v4
import extraction_v6
import scan
import source_bundle
import source_discovery


COMMIT = "3" * 40
REPOSITORY = "https://github.com/fixture/constructor"
COMMIT_API = "https://api.github.com/repos/fixture/constructor/commits?per_page=1"
ARCHIVE_URL = f"https://codeload.github.com/fixture/constructor/tar.gz/{COMMIT}"
SOURCE_COMMIT_API = f"https://api.github.com/repos/fixture/constructor/git/commits/{COMMIT}"
CODE = b"def construct(record):\n    return {'task': record['request']}\n"
EXCLUDED_MARKER = b"EXCLUDED_RESEARCH_LABEL_MUST_NOT_ENTER_SOURCE"


def git_object_id(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


class FixtureResponse(io.BytesIO):
    def __init__(self, data, url, *, interrupt_after=None):
        super().__init__(data)
        self.url = url
        self.headers = {"Content-Length": str(len(data))}
        self.status = 200
        self.interrupt_after = interrupt_after

    def geturl(self):
        return self.url

    def read(self, size=-1):
        if self.interrupt_after is not None:
            remaining = self.interrupt_after - self.tell()
            if remaining <= 0:
                raise TimeoutError("Offline partial-response fixture")
            size = min(size, remaining) if size >= 0 else remaining
        return super().read(size)


class RetryAcquisitionRecordTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="retry acquisition integration ")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.source = "https://example.org/synthetic-paper.pdf"
        text = ("This synthetic paper studies indirect prompt injection. "
                f"Our code is available at {REPOSITORY}.")
        self.paper = {
            "source": self.source,
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text": text,
            "segments": [{"id": "p1", "text": text}],
            "coverage": {"complete": True, "reason": "Entire synthetic text supplied"},
            "links": [REPOSITORY],
            "media_type": "application/pdf",
        }
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode="w:gz") as stream:
            for path, data in [("generator.py", CODE), ("labels.py", EXCLUDED_MARKER)]:
                member = tarfile.TarInfo(f"constructor-{COMMIT}/{path}")
                member.size = len(data)
                stream.addfile(member, io.BytesIO(data))
        self.archive = archive.getvalue()
        self.blob = git_object_id("blob", CODE)
        label_blob = git_object_id("blob", EXCLUDED_MARKER)
        tree_data = b"100644 generator.py\0" + bytes.fromhex(self.blob)
        tree_data += b"100644 labels.py\0" + bytes.fromhex(label_blob)
        self.tree = git_object_id("tree", tree_data)
        self.tree_url = f"https://api.github.com/repos/fixture/constructor/git/trees/{self.tree}?recursive=1"
        self.raw_url = f"https://raw.githubusercontent.com/fixture/constructor/{COMMIT}/generator.py"
        self.source_commit_data = json.dumps({"sha": COMMIT, "tree": {"sha": self.tree}}).encode()
        self.tree_data = json.dumps({"sha": self.tree, "truncated": False, "tree": [
            {"path": "generator.py", "type": "blob", "mode": "100644", "sha": self.blob, "size": len(CODE)},
            {"path": "labels.py", "type": "blob", "mode": "100644", "sha": label_blob, "size": len(EXCLUDED_MARKER)},
        ]}).encode()
        self.api_data = json.dumps([{
            "sha": COMMIT, "html_url": f"{REPOSITORY}/commit/{COMMIT}",
        }]).encode()
        self.discovery_urls = []
        self.archive_urls = []
        self.archive_timeouts = []
        self.fallback_urls = []

    def load_json(self, output, name):
        return json.loads((output / name).read_text(encoding="utf-8"))

    def run_preparation(self, name, responses, fallback_responses=None):
        output = self.directory / name
        responses = iter(responses)
        fallback_responses = {url: iter(values) for url, values in (fallback_responses or {}).items()}

        def discover_open(request, timeout):
            self.discovery_urls.append(request.full_url)
            if request.full_url != COMMIT_API:
                raise AssertionError("Unexpected discovery request: " + request.full_url)
            return FixtureResponse(self.api_data, request.full_url)

        def archive_open(request, timeout):
            if request.full_url == ARCHIVE_URL:
                self.archive_urls.append(request.full_url)
                self.archive_timeouts.append(timeout)
                response = next(responses)
            elif request.full_url in fallback_responses:
                self.fallback_urls.append(request.full_url)
                response = next(fallback_responses[request.full_url])
            else:
                raise AssertionError("Unexpected source request: " + request.full_url)
            if isinstance(response, Exception):
                raise response
            return response

        with ExitStack() as stack:
            stack.enter_context(patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)))
            engine = stack.enter_context(patch.object(scan, "get_client", side_effect=AssertionError("No model may be selected")))
            stack.enter_context(patch.object(source_discovery, "build_opener", return_value=Mock(open=discover_open)))
            stack.enter_context(patch.object(source_bundle, "build_opener", return_value=Mock(open=archive_open)))
            # Keep the actual public-address guard, with deterministic offline DNS.
            stack.enter_context(patch("documents.socket.getaddrinfo", return_value=[
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
            ]))
            stack.enter_context(redirect_stdout(io.StringIO()))
            stack.enter_context(redirect_stderr(io.StringIO()))
            code = scan.main([self.source, "--output", str(output), "--prepare-only"])
        self.assertEqual(code, 0)
        engine.assert_not_called()
        self.assertEqual(self.discovery_urls, [COMMIT_API])
        discovery = self.load_json(output, "source_discovery.json")
        self.assertEqual(discovery["status"], "selected")
        self.assertEqual(discovery["repository"], REPOSITORY)
        self.assertEqual(discovery["revision"], COMMIT)
        self.assertEqual(discovery["requests"][0]["sha256"], hashlib.sha256(self.api_data).hexdigest())
        row = self.load_json(output, "result.json")
        self.assertEqual(row["requested_workflow"], "automatic_from_paper")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["verdict"], "not_run")
        self.assertIsNone(row["has_confirmed_inconsistency"])
        for name in ("extraction.json", "review.json", "inference.json"):
            self.assertFalse((output / name).exists(), name)
        self.assertEqual(self.load_json(output, "report.json")["papers"][0], row)
        return output, row

    def test_complete_archive_preserves_acquisition_and_the_actual_source_binding(self):
        output, row = self.run_preparation("recovered archive", [
            FixtureResponse(self.archive, ARCHIVE_URL),
        ])
        self.assertEqual(self.archive_urls, [ARCHIVE_URL])
        self.assertEqual(self.archive_timeouts, [source_bundle.DOWNLOAD_TIMEOUT_SECONDS])
        self.assertFalse(self.fallback_urls)
        acquisition = self.load_json(output, "source_acquisition.json")
        self.assertEqual(row["source_audit"]["acquisition"], acquisition)
        self.assertEqual([entry["status"] for entry in acquisition["attempts"]], ["succeeded"])
        self.assertEqual(acquisition["attempts"][0]["bytes_received"], len(self.archive))
        self.assertEqual(acquisition["attempts"][0]["sha256"], hashlib.sha256(self.archive).hexdigest())

        repository = self.load_json(output, "repository.json")
        source_bundle.validate_repository(repository)
        self.assertEqual(repository["source_acquisition"], acquisition)
        self.assertEqual(repository["source"], REPOSITORY)
        self.assertEqual(repository["source_binding"], hashlib.sha256(REPOSITORY.encode()).hexdigest())
        self.assertEqual(repository["revision"], COMMIT)
        self.assertEqual(repository["commit_binding"], "github_codeload_full_commit_url")
        self.assertEqual(repository["archive_sha256"], hashlib.sha256(self.archive).hexdigest())
        self.assertEqual(repository["execution"], "none")
        self.assertTrue(repository["coverage"]["inventory_complete"])
        self.assertTrue(repository["coverage"]["complete"])
        self.assertEqual([item["path"] for item in repository["inventory"]], ["generator.py"])
        self.assertEqual(repository["segments"][0]["text"].encode(), CODE)
        self.assertEqual(repository["segments"][0]["sha256"], hashlib.sha256(CODE).hexdigest())
        self.assertNotIn(EXCLUDED_MARKER.decode(), json.dumps(repository))

        combined = self.load_json(output, "combined_input.json")
        request = self.load_json(output, "request.json")
        content = extraction_v4.model_content(combined)
        self.assertEqual(row["input_mode"], "paper_and_source")
        self.assertEqual(row["source_audit"]["status"], "loaded")
        self.assertEqual(combined["input_binding"]["repository_manifest_sha256"], repository["manifest_sha256"])
        self.assertEqual(combined["input_binding"]["repository_revision"], COMMIT)
        self.assertEqual(content["input_binding"], request["input_sha256"])
        self.assertEqual(combined["sha256"], request["input_sha256"])
        self.assertEqual(request["model_content_sha256"], combined["model_content_sha256"])
        self.assertEqual(request["prompt_sha256"], extraction_v6.prompt_hash())
        self.assertEqual(request["evidence_scope"], "supplied_paper_and_source")
        self.assertEqual(request["model_data_characters"], len(json.dumps(content, ensure_ascii=False, sort_keys=True)))
        self.assertEqual(combined["repository"]["source_acquisition"], acquisition)
        self.assertEqual([part["text"] for part in content["segments"] if part["id"].startswith("repo:")], [CODE.decode()])
        for forbidden in ("gold", "expected", "matches_gold", "curated_cases"):
            self.assertNotIn(forbidden, content)

    def test_partial_archive_and_transient_commit_failure_recover_a_tree_bound_source_snapshot(self):
        partial = 19
        output, row = self.run_preparation("recovered source only", [
            FixtureResponse(self.archive, ARCHIVE_URL, interrupt_after=partial),
        ], {
            SOURCE_COMMIT_API: [TimeoutError("Offline commit request fixture"),
                                FixtureResponse(self.source_commit_data, SOURCE_COMMIT_API)],
            self.tree_url: [FixtureResponse(self.tree_data, self.tree_url)],
            self.raw_url: [FixtureResponse(CODE, self.raw_url)],
        })
        self.assertEqual(self.archive_urls, [ARCHIVE_URL])
        self.assertEqual(self.fallback_urls, [SOURCE_COMMIT_API, SOURCE_COMMIT_API, self.tree_url, self.raw_url])
        acquisition = self.load_json(output, "source_acquisition.json")
        self.assertEqual(row["source_audit"]["acquisition"], acquisition)
        self.assertEqual(len(acquisition["attempts"]), 1)
        self.assertEqual(acquisition["attempts"][0]["bytes_received"], partial)
        self.assertEqual(acquisition["attempts"][0]["status"], "failed")
        self.assertNotIn("sha256", acquisition["attempts"][0])
        fallback = acquisition["fallback"]
        self.assertEqual(fallback["status"], "succeeded")
        self.assertEqual([attempt["resource_kind"] for attempt in fallback["attempts"]], ["commit", "commit", "tree", "blob"])
        self.assertEqual([attempt["status"] for attempt in fallback["attempts"]], ["failed", "succeeded", "succeeded", "succeeded"])
        self.assertEqual(fallback["attempts"][0]["failure_kind"], "timeout")
        self.assertEqual(fallback["attempts"][-1]["path"], "generator.py")
        self.assertEqual(fallback["fetched_files"], 1)

        repository = self.load_json(output, "repository.json")
        source_bundle.validate_repository(repository)
        self.assertEqual(repository["source_acquisition"], acquisition)
        self.assertEqual(repository["commit_binding"], "github_commit_tree_raw_blobs")
        self.assertEqual(repository["commit"], COMMIT)
        self.assertEqual(repository["tree_sha"], self.tree)
        self.assertNotIn("archive_sha256", repository)
        self.assertEqual(repository["inventory"][0]["object_id"], self.blob)
        self.assertTrue(repository["coverage"]["inventory_complete"])
        self.assertTrue(repository["coverage"]["complete"])
        self.assertEqual(repository["coverage"]["eligible_files"], 1)
        self.assertEqual(repository["segments"][0]["text"].encode(), CODE)
        self.assertNotIn(EXCLUDED_MARKER.decode(), json.dumps(repository))
        self.assertEqual(row["input_mode"], "paper_and_source")
        self.assertEqual(row["source_audit"]["status"], "loaded")
        combined = self.load_json(output, "combined_input.json")
        content = extraction_v4.model_content(combined)
        request = self.load_json(output, "request.json")
        self.assertEqual(content["input_binding"], request["input_sha256"])
        self.assertEqual(combined["repository"]["source_acquisition"], acquisition)
        self.assertEqual(request["model_content_sha256"], combined["model_content_sha256"])
        self.assertEqual(request["prompt_sha256"], extraction_v6.prompt_hash())
        self.assertEqual([part["text"] for part in content["segments"] if part["id"].startswith("repo:")], [CODE.decode()])

    def test_exhausted_partial_archive_and_fallback_preserve_failure_records_without_a_source_snapshot(self):
        partial = 23
        output, row = self.run_preparation("exhausted archive", [
            FixtureResponse(self.archive, ARCHIVE_URL, interrupt_after=partial),
        ], {
            SOURCE_COMMIT_API: [TimeoutError("Offline source fallback timeout")
                                for _ in range(source_bundle.DOWNLOAD_ATTEMPTS)],
        })
        self.assertEqual(self.archive_urls, [ARCHIVE_URL])
        self.assertEqual(self.fallback_urls, [SOURCE_COMMIT_API] * source_bundle.DOWNLOAD_ATTEMPTS)
        acquisition = self.load_json(output, "source_acquisition.json")
        self.assertEqual(row["source_audit"]["acquisition"], acquisition)
        self.assertEqual(len(acquisition["attempts"]), 1)
        for entry in acquisition["attempts"]:
            self.assertEqual(entry["status"], "failed")
            self.assertEqual(entry["failure_kind"], "timeout")
            self.assertEqual(entry["bytes_received"], partial)
            self.assertNotIn("sha256", entry)
        self.assertEqual(acquisition["fallback"]["status"], "failed")
        self.assertEqual(len(acquisition["fallback"]["attempts"]), source_bundle.DOWNLOAD_ATTEMPTS)
        for entry in acquisition["fallback"]["attempts"]:
            self.assertEqual(entry["status"], "failed")
            self.assertEqual(entry["resource_kind"], "commit")
            self.assertEqual(entry["failure_kind"], "timeout")
            self.assertEqual(entry["bytes_received"], 0)
        self.assertIn("timed out", row["source_audit"]["reason"])
        self.assertEqual(row["source_audit"]["status"], "unavailable")
        self.assertEqual(row["input_mode"], "document_only")
        self.assertTrue(any(stage["stage"] == "repository_ingestion" and stage["status"] == "failed"
                            for stage in row["stages"]))
        self.assertTrue(any("source verification did not complete" in note for note in row["notes"]))
        self.assertNotIn("repository", row)
        for name in ("repository.json", "combined_input.json"):
            self.assertFalse((output / name).exists(), name)
        request = self.load_json(output, "request.json")
        self.assertEqual(request["input_sha256"], self.paper["sha256"])
        self.assertEqual(request["prompt_sha256"], extraction_v3.prompt_hash())
        self.assertIsNone(request["model_content_sha256"])
        self.assertEqual(request["evidence_scope"], "supplied_document_only")


if __name__ == "__main__":
    unittest.main()
