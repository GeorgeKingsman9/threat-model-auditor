"""Integrate all-paper reports with local inputs and fake inference only."""

from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import benchmark
import scan


class FakeClient:
    def __init__(self):
        self.calls = []

    def generate(self, system, content, schema):
        self.calls.append(copy.deepcopy({"system": system, "content": content, "schema": schema}))
        if len(self.calls) % 2:
            return {
                "title": "Title from supplied document", "applicability": "in_scope",
                "applicability_reason": "The supplied fixture is an IPI paper.",
                "applicability_citation": {"segment_id": "s1", "quote": "indirect prompt injection"},
                "scope_summary": "Supplied document only", "flows": [], "limitations": ["Fixture, not a real model"],
            }
        return {
            "applicability": "in_scope", "applicability_supported": True,
            "flow_reviews": [], "limitations": ["Fixture semantic review"],
        }

    def ledger(self):
        return {"provider": "fixture", "calls": len(self.calls), "charged_or_reserved_usd": 0}


class BenchmarkIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="audit benchmark integration ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        network = patch("providers.urllib.request.urlopen", side_effect=AssertionError("No network in tests"))
        self.network = network.start()
        self.addCleanup(network.stop)

    def run_main(self, args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return benchmark.main(list(map(str, args)))

    def spec(self, paper_id, source, expected="insufficient_evidence"):
        return {
            "id": paper_id, "title": "Metadata title excluded from inference",
            "source": str(source), "cohort": "METADATA_COHORT_SENTINEL",
            "expected": expected, "expected_basis": "METADATA_EXPECTED_BASIS_SENTINEL",
            "comparison_note": "METADATA_COMPARISON_SENTINEL",
        }

    def manifest(self, specs):
        path = self.directory / "manifest.json"
        path.write_text(json.dumps({"papers": specs}), encoding="utf-8")
        return path

    def document(self, source):
        text = "This fixture evaluates indirect prompt injection."
        return {
            "source": str(source), "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text": text, "segments": [{"id": "s1", "text": text}], "links": [],
            "coverage": {"complete": True, "reason": "Fixture text only"}, "media_type": "text/plain",
        }

    def test_regression_retains_all_fourteen_papers_and_three_unrun_controls(self):
        output = self.directory / "regression"
        with patch.object(benchmark, "get_client", side_effect=AssertionError("Regression selects no model")):
            self.assertEqual(self.run_main(["--mode", "regression", "--output", output]), 0)
        report = json.loads((output / "report.json").read_text())
        rows = report["papers"]
        manifest = json.loads((ROOT / "benchmarks" / "papers.json").read_text())["papers"]
        self.assertEqual([row["id"] for row in rows], [spec["id"] for spec in manifest])
        self.assertEqual(len(rows), 14)
        controls = [row for row in rows if row["cohort"] == "out_of_domain"]
        self.assertEqual(len(controls), 3)
        for row in controls:
            self.assertEqual(row["status"], "not_run")
            self.assertEqual(row["verdict"], "not_run")
            self.assertIsNone(row["has_confirmed_inconsistency"])
            self.assertIsNone(row["matches_gold"])
            self.assertEqual(row["expected"], "not_applicable")
            self.assertEqual(row["stages"][0]["status"], "not_run")
        self.assertEqual(report["summary"]["statuses"], {"completed": 11, "not_run": 3})
        comparison = report["summary"]["reference_label_comparison"]
        self.assertEqual((comparison["matched"], comparison["completed"], comparison["total"]), (11, 11, 14))
        self.assertTrue((output / "report.html").is_file())
        self.assertTrue((output / "report.md").is_file())
        self.network.assert_not_called()

    def test_prepare_keeps_both_prepared_and_failed_papers_without_model_calls(self):
        source = self.directory / "readable.txt"
        source.write_text("A complete text fixture for preparation.", encoding="utf-8")
        specs = [self.spec("readable", source), self.spec("missing", self.directory / "missing.txt")]
        output = self.directory / "prepare"
        with patch.object(benchmark, "get_client", side_effect=AssertionError("Prepare selects no model")):
            code = self.run_main(["--mode", "prepare", "--manifest", self.manifest(specs), "--output", output])
        self.assertEqual(code, 1)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(len(report["papers"]), 2)
        self.assertEqual([row["status"] for row in report["papers"]], ["pending", "failed"])
        self.assertEqual(report["papers"][1]["verdict"], "technical_failure")
        self.assertTrue((output / "readable" / "prepared.json").is_file())
        self.assertTrue((output / "missing" / "result.json").is_file())
        self.assertTrue((output / "report.html").is_file())
        for row in report["papers"]:
            self.assertIsNone(row["matches_gold"])

    def test_scan_never_passes_gold_or_manifest_metadata_to_inference(self):
        source = "https://example.org/fixture.pdf"
        specs = [self.spec("fixture", source, expected="inconsistent")]
        output = self.directory / "fake inference"
        client = FakeClient()
        with patch.object(benchmark, "get_client", return_value=client), patch.object(scan, "load_document", return_value=self.document(source)):
            code = self.run_main(["--mode", "scan", "--manifest", self.manifest(specs), "--output", output])
        self.assertEqual(code, 0)
        self.assertEqual(len(client.calls), 2)
        payloads = json.dumps(client.calls)
        for sentinel in ("METADATA_COHORT_SENTINEL", "METADATA_EXPECTED_BASIS_SENTINEL", "METADATA_COMPARISON_SENTINEL", "Metadata title excluded from inference"):
            self.assertNotIn(sentinel, payloads)
        for call in client.calls:
            self.assertNotIn("expected", call["content"])
            self.assertNotIn("matches_gold", call["content"])
            self.assertNotIn("cohort", call["content"])
        standalone = json.loads((output / "fixture" / "result.json").read_text())
        self.assertNotIn("expected", standalone)
        self.assertNotIn("matches_gold", standalone)
        report = json.loads((output / "report.json").read_text())
        row = report["papers"][0]
        self.assertEqual(row["verdict"], "insufficient_evidence")
        self.assertEqual(row["expected"], "inconsistent")
        self.assertIs(row["matches_gold"], False)
        self.assertIs(row["has_confirmed_inconsistency"], False)
        self.network.assert_not_called()

    def test_wrong_prepared_source_is_retained_as_failure_without_fetch_or_model(self):
        source = "https://example.org/target.pdf"
        specs = [self.spec("fixture", source)]
        prepared_root = self.directory / "previous"
        (prepared_root / "fixture").mkdir(parents=True)
        prepared = self.document("https://example.org/wrong.pdf")
        prepared["requested_source"] = "https://example.org/wrong.pdf"
        (prepared_root / "fixture" / "prepared.json").write_text(json.dumps(prepared))
        output = self.directory / "wrong input"
        client = FakeClient()
        with patch.object(benchmark, "get_client", return_value=client), patch.object(scan, "load_document", side_effect=AssertionError("Must not fetch")):
            code = self.run_main([
                "--mode", "scan", "--manifest", self.manifest(specs),
                "--prepared-dir", prepared_root, "--output", output,
            ])
        self.assertEqual(code, 1)
        self.assertEqual(client.calls, [])
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(len(report["papers"]), 1)
        self.assertEqual(report["papers"][0]["verdict"], "technical_failure")
        self.assertIsNone(report["papers"][0]["matches_gold"])

    def test_openai_without_explicit_api_allow_is_rejected_before_output_or_requests(self):
        output = self.directory / "unauthorized"
        with self.assertRaises(SystemExit) as raised:
            self.run_main([
                "--mode", "scan", "--output", output, "--provider", "openai",
                "--model", "fixture", "--max-cost-usd", "1", "--input-price", "1", "--output-price", "1",
            ])
        self.assertEqual(raised.exception.code, 2)
        self.assertFalse(output.exists())
        self.network.assert_not_called()

    def test_corrupt_prepared_json_keeps_failed_paper_and_continues_with_next_paper(self):
        broken_source = "https://example.org/broken.pdf"
        good_source = "https://example.org/good.pdf"
        specs = [self.spec("broken", broken_source), self.spec("good", good_source)]
        prepared_root = self.directory / "previous"
        (prepared_root / "broken").mkdir(parents=True)
        (prepared_root / "broken" / "prepared.json").write_text("{invalid JSON", encoding="utf-8")
        output = self.directory / "continue after failure"
        client = FakeClient()
        with patch.object(benchmark, "get_client", return_value=client), patch.object(scan, "load_document", return_value=self.document(good_source)) as ingest:
            code = self.run_main([
                "--mode", "scan", "--manifest", self.manifest(specs),
                "--prepared-dir", prepared_root, "--output", output,
            ])
        self.assertEqual(code, 1)
        ingest.assert_called_once_with(good_source)
        self.assertEqual(len(client.calls), 2)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual([row["id"] for row in report["papers"]], ["broken", "good"])
        self.assertEqual([row["status"] for row in report["papers"]], ["failed", "completed"])
        self.assertEqual(report["papers"][0]["verdict"], "technical_failure")
        self.assertIsNone(report["papers"][0]["matches_gold"])
        self.assertTrue((output / "broken" / "result.json").is_file())
        self.assertTrue((output / "good" / "result.json").is_file())
        self.assertTrue((output / "report.html").is_file())

    def test_subset_includes_an_unrun_control_instead_of_dropping_it(self):
        output = self.directory / "subset"
        self.assertEqual(self.run_main([
            "--mode", "regression", "--output", output, "--only", "aspi", "attention",
        ]), 0)
        rows = json.loads((output / "report.json").read_text())["papers"]
        self.assertEqual([row["id"] for row in rows], ["aspi", "attention"])
        self.assertEqual(rows[0]["verdict"], "inconsistent")
        self.assertEqual(rows[1]["verdict"], "not_run")

    def test_output_directory_cannot_be_overwritten(self):
        output = self.directory / "preserved"
        output.mkdir()
        sentinel = output / "research artifact.txt"
        sentinel.write_text("preserve exact bytes", encoding="utf-8")
        with self.assertRaises(SystemExit) as raised:
            self.run_main(["--mode", "regression", "--output", output])
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(sentinel.read_text(), "preserve exact bytes")
        self.assertEqual(list(output.iterdir()), [sentinel])


if __name__ == "__main__":
    unittest.main()
