"""Offline integration checks for document preparation and stored-output replay."""

from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scan


def fixture():
    text = ("This paper evaluates indirect prompt injection. "
            "The online attacker cannot see the full user query. "
            "Its online construction input contains the full user query.")
    document = {
        "source": "paper.txt", "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "text": text, "segments": [{"id": "s1", "text": text}],
        "coverage": {"complete": True, "reason": "Test text decoded in full"},
        "links": [], "media_type": "text/plain",
    }
    extraction = {
        "title": "Offline pipeline fixture", "applicability": "in_scope",
        "applicability_reason": "The text describes indirect prompt injection.",
        "applicability_citation": {"segment_id": "s1", "quote": "evaluates indirect prompt injection"},
        "scope_summary": "This online construction condition only", "limitations": ["No runtime artifact"],
        "flows": [{
            "edge": {"role": "online attacker", "phase": "online construction",
                     "source": "current user request", "representation": "query text",
                     "operation": "receive as input", "query_form": "full_query"},
            "permission": "deny", "observation": "present",
            "declaration": {"segment_id": "s1", "quote": "online attacker cannot see the full user query"},
            "implementation": {"segment_id": "s1", "quote": "online construction input contains the full user query"},
            "explanation": "The described input contradicts the stated boundary for the same online role.",
        }],
    }
    review = {
        "applicability": "in_scope", "applicability_supported": True,
        "flow_reviews": [{"index": 0, "supported": True, "reason": "Both quotes specify the same online role."}],
        "limitations": ["Fixture review, not real model verification"],
    }
    return document, extraction, review


class ScanIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="audit scan integration ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.document, self.extraction, self.review = fixture()
        self.source = self.directory / "paper.txt"
        self.source.write_text(self.document["text"], encoding="utf-8")
        network = patch("providers.urllib.request.urlopen", side_effect=AssertionError("Network is forbidden in tests"))
        self.network = network.start()
        self.addCleanup(network.stop)

    def write_json(self, name, data):
        path = self.directory / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def run_main(self, args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return scan.main(list(map(str, args)))

    def test_prepare_only_creates_one_pending_result_without_selecting_a_model(self):
        output = self.directory / "prepared run"
        with patch.object(scan, "get_client", side_effect=AssertionError("No model should be selected")) as engine:
            code = self.run_main([self.source, "--output", output, "--prepare-only"])
        self.assertEqual(code, 0)
        engine.assert_not_called()
        self.network.assert_not_called()
        for name in ("prepared.json", "request.json", "result.json", "report.json", "report.html", "report.md"):
            self.assertTrue((output / name).is_file(), name)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(report["summary"]["paper_count"], 1)
        row = report["papers"][0]
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["verdict"], "not_run")
        self.assertIsNone(row["has_confirmed_inconsistency"])
        self.assertEqual(row["stages"][-1], {"stage": "extraction", "status": "not_run"})
        self.assertFalse((output / "extraction.json").exists())

    def test_missing_file_keeps_a_failed_result_stage_and_report(self):
        output = self.directory / "missing run"
        code = self.run_main([self.directory / "missing.txt", "--output", output, "--prepare-only"])
        self.assertEqual(code, 1)
        row = json.loads((output / "result.json").read_text())
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIsNone(row["has_confirmed_inconsistency"])
        self.assertEqual(row["stages"][-1]["stage"], "ingestion")
        self.assertEqual(row["stages"][-1]["status"], "failed")
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(len(report["papers"]), 1)
        self.assertTrue((output / "report.html").is_file())

    def test_replay_produces_one_paper_and_preserves_each_processing_stage(self):
        output = self.directory / "replay run"
        extraction = self.write_json("extraction.json", self.extraction)
        review = self.write_json("review.json", self.review)
        with patch.object(scan, "get_client", side_effect=AssertionError("Replay must not select a model")):
            code = self.run_main([self.source, "--output", output, "--extraction", extraction, "--review", review])
        self.assertEqual(code, 0)
        self.network.assert_not_called()
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(report["summary"]["paper_count"], 1)
        row = report["papers"][0]
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "inconsistent")
        self.assertIs(row["has_confirmed_inconsistency"], True)
        self.assertEqual(row["review_status"], "model_reviewed_not_human_verified")
        self.assertEqual([stage["stage"] for stage in row["stages"]], [
            "ingestion", "extraction", "semantic_review", "citation_validation_and_decision",
        ])
        self.assertEqual(set(row["evidence"][0]["locators"]), {"declaration", "implementation"})
        self.assertNotIn("expected", row)
        self.assertNotIn("matches_gold", row)

    def test_fabricated_replay_quote_is_insufficient_not_a_confirmed_finding(self):
        output = self.directory / "fabricated run"
        extraction = copy.deepcopy(self.extraction)
        extraction["flows"][0]["implementation"]["quote"] = "An invented quote absent from the paper."
        row = scan.scan_source(str(self.source), output, extraction=extraction, review=self.review)
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "insufficient_evidence")
        self.assertIs(row["has_confirmed_inconsistency"], False)
        self.assertTrue(row["evidence"][0]["citation_errors"])
        self.assertEqual(json.loads((output / "result.json").read_text())["verdict"], "insufficient_evidence")

    def test_prepared_document_from_another_url_is_rejected_before_inference(self):
        output = self.directory / "wrong prepared"
        prepared = {**self.document, "requested_source": "https://example.org/other.pdf"}
        client = Mock()
        with patch.object(scan, "load_document", side_effect=AssertionError("Must not fetch on replay")):
            row = scan.scan_source("https://example.org/target.pdf", output, client=client, prepared=prepared)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("source does not match", row["error"])
        client.generate.assert_not_called()
        self.assertFalse((output / "extraction.json").exists())
        self.assertTrue((output / "result.json").is_file())

    def test_model_input_limit_fails_without_silent_truncation_or_inference(self):
        output = self.directory / "too large"
        client = Mock()
        row = scan.scan_source(str(self.source), output, client=client, max_input_chars=10)
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("not silently truncated", row["error"])
        client.generate.assert_not_called()
        prepared = json.loads((output / "prepared.json").read_text())
        self.assertEqual(prepared["text"], self.document["text"])

    def test_same_filename_in_different_directories_cannot_reuse_prepared_text(self):
        other = self.directory / "another directory" / "paper.txt"
        other.parent.mkdir()
        other.write_text("A different paper with the same filename.", encoding="utf-8")
        first_output = self.directory / "first preparation"
        scan.scan_source(str(self.source), first_output, prepare_only=True)
        prepared = json.loads((first_output / "prepared.json").read_text())
        self.assertIn("source_binding", prepared)
        self.assertNotIn(str(self.source), json.dumps(prepared))
        output = self.directory / "wrong same filename"
        client = Mock()
        row = scan.scan_source(str(other), output, client=client, prepared=prepared)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("source binding does not match", row["error"])
        client.generate.assert_not_called()
        self.assertFalse((output / "prepared.json").exists())

    def test_corrupt_prepared_json_is_a_recorded_ingestion_failure(self):
        corrupt = self.directory / "corrupt prepared.json"
        corrupt.write_text("{not valid JSON", encoding="utf-8")
        output = self.directory / "corrupt prepared run"
        client = Mock()
        row = scan.scan_source(str(self.source), output, client=client, prepared=corrupt)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertEqual(row["stages"][-1]["stage"], "ingestion")
        self.assertTrue((output / "result.json").is_file())
        client.generate.assert_not_called()

    def test_api_backend_without_explicit_allow_never_reads_or_sends_the_document(self):
        for provider in ("openai", "anthropic"):
            with self.subTest(provider=provider):
                output = self.directory / provider
                with patch.object(scan, "load_document") as ingest:
                    with self.assertRaises(SystemExit) as raised:
                        self.run_main([
                            self.source, "--output", output, "--provider", provider,
                            "--model", "fixture", "--max-cost-usd", "1", "--input-price", "1", "--output-price", "1",
                        ])
                self.assertEqual(raised.exception.code, 2)
                ingest.assert_not_called()
                self.assertFalse(output.exists())
        self.network.assert_not_called()

    def test_existing_output_directory_is_preserved(self):
        output = self.directory / "existing"
        self.assertEqual(self.run_main([self.source, "--output", output, "--prepare-only"]), 0)
        original = {path.name: path.read_bytes() for path in output.iterdir()}
        with self.assertRaises(SystemExit) as raised:
            self.run_main([self.source, "--output", output, "--prepare-only"])
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, original)


if __name__ == "__main__":
    unittest.main()
