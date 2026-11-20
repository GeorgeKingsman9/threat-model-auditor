"""Truncated HTTP bodies and failed reviews remain durable per-paper failures."""

from http.client import IncompleteRead
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import documents
import scan
import source_bundle
import test_benchmark as benchmark_fixtures


class BrokenResponse:
    headers = {}

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def geturl(self):
        return self.url

    def read(self, amount):
        raise IncompleteRead(b"partial-body", 200)


class Opener:
    def open(self, request, **kwargs):
        return BrokenResponse(request.full_url)


class TransportFailureTests(unittest.TestCase):
    def test_truncated_paper_is_a_document_error_without_accepting_partial_bytes(self):
        with patch.object(documents, "_validate_url"), patch.object(documents, "build_opener", return_value=Opener()):
            with self.assertRaisesRegex(documents.DocumentError, "Could not download"):
                documents._fetch_url("https://example.org/paper.pdf")

    def test_truncated_source_is_a_repository_error_without_accepting_partial_archive(self):
        with patch.object(source_bundle, "build_opener", return_value=Opener()):
            with self.assertRaisesRegex(source_bundle.RepositoryError, "Could not download"):
                source_bundle._download_archive("https://codeload.github.com/owner/repo/tar.gz/" + "a" * 40)

    def document(self):
        return benchmark_fixtures.BenchmarkIntegrationTests().document("https://example.org/paper.pdf")

    def test_unexpected_discovery_error_still_writes_one_failed_paper(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            with patch.object(scan, "load_document", return_value=self.document()), \
                    patch.object(scan, "discover_repository", side_effect=RuntimeError("discovery failed")):
                row = scan.scan_source("https://example.org/paper.pdf", output, client=benchmark_fixtures.FakeClient())
            self.assertEqual(row["verdict"], "technical_failure")
            self.assertEqual(row["error_type"], "RuntimeError")
            self.assertEqual(row["stages"][-1]["stage"], "source_discovery")
            self.assertTrue((output / "result.json").is_file())
            self.assertTrue((output / "inference.json").is_file())

    def test_completed_extraction_ledger_survives_a_later_review_failure(self):
        class ReviewFailureClient(benchmark_fixtures.FakeClient):
            def generate(self, system, content, schema):
                if self.calls:
                    self.calls.append({"failed_review": True})
                    raise ValueError("review unavailable")
                return super().generate(system, content, schema)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            with patch.object(scan, "load_document", return_value=self.document()), \
                    patch.object(scan, "discover_repository", return_value={"status": "not_found", "reason": "fixture"}):
                row = scan.scan_source("https://example.org/paper.pdf", output, client=ReviewFailureClient())
            self.assertEqual(row["verdict"], "technical_failure")
            self.assertTrue((output / "extraction.json").is_file())
            self.assertEqual(json.loads((output / "inference.extraction.json").read_text())["calls"], 1)
            self.assertEqual(json.loads((output / "inference.semantic_review.json").read_text())["calls"], 2)
            self.assertEqual(json.loads((output / "inference.json").read_text())["calls"], 2)


if __name__ == "__main__":
    unittest.main()
