"""Known open-source audits can refuse paper-only inference after source failure."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scan
import test_automatic_entrypoint as entry
import test_extraction_v4 as toy


class RequiredSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = "https://example.org/paper.pdf"
        self.paper, self.repository, _, extraction, review = toy.ExtractionV4Tests().fixtures()
        self.paper["source"] = self.source
        self.client = entry.DynamicFakeClient(extraction, review)
        self.selected = {"status": "selected", "repository": "https://github.com/toy/source",
                         "revision": self.repository["revision"], "reason": "Offline selection fixture"}

    def test_missing_source_stops_before_any_model_call(self):
        with patch.object(scan, "load_document", return_value=self.paper), \
                patch.object(scan, "discover_repository", return_value={"status": "not_found", "reason": "Fixture"}):
            row = scan.scan_source(self.source, self.root / "missing", client=self.client, require_source=True)
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("inference was not started", row["error"])
        self.assertEqual(self.client.calls, [])

    def test_failed_source_stops_before_paper_only_model_fallback(self):
        with patch.object(scan, "load_document", return_value=self.paper), \
                patch.object(scan, "discover_repository", return_value=self.selected), \
                patch("source_bundle.load_repository", side_effect=ValueError("retrieval exhausted")):
            row = scan.scan_source(self.source, self.root / "failed", client=self.client, require_source=True)
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertEqual(row["source_audit"]["status"], "unavailable")
        self.assertEqual(self.client.calls, [])

    def test_url_only_cli_can_require_source_and_choose_files_without_manual_repository(self):
        output = self.root / "files"
        with patch.object(scan, "load_document", return_value=self.paper), \
                patch.object(scan, "discover_repository", return_value=self.selected), \
                patch("source_bundle.load_repository", return_value=self.repository) as load, \
                patch.object(scan, "get_client", side_effect=AssertionError("Prepare selects no model")), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = scan.main([self.source, "--source-fetch", "files", "--require-source", "--prepare-only", "--output", str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(load.call_args.kwargs["fetch_mode"], "files")
        self.assertEqual(json.loads((output / "request.json").read_text())["require_source"], True)
        self.assertEqual(json.loads((output / "result.json").read_text())["input_mode"], "paper_and_source")

    def test_paper_only_rejects_source_requirements_before_reading(self):
        for flags in [["--require-source"], ["--source-fetch", "files"]]:
            with self.subTest(flags=flags), patch.object(scan, "load_document") as read, \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    scan.main([self.source, "--paper-only", *flags, "--output", str(self.root / "invalid")])
                read.assert_not_called()


if __name__ == "__main__":
    unittest.main()
