"""Replay fixed outputs and enrich citation views without any model or network."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
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
import replay_study


class ReplayStudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixed outputs replay ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.api = stack.enter_context(patch("providers.ModelClient.generate", side_effect=AssertionError("No API inference in replay")))
        self.codex = stack.enter_context(patch("codex_provider.CodexClient.generate", side_effect=AssertionError("No Codex inference in replay")))
        self.network = stack.enter_context(patch("urllib.request.urlopen", side_effect=AssertionError("No live network in tests")))

    def fixtures(self, quote="gradient-based training"):
        source = "https://example.org/fixed-paper.pdf"
        primary = "An optimization paper. The gradient-based\nOTHER COLUMN\ntraining objective is analyzed."
        reading = "An optimization paper. The gradient-based training objective is analyzed."
        document = {
            "source": source, "requested_source": source,
            "sha256": hashlib.sha256(b"%PDF-fixed-source-bytes").hexdigest(),
            "text": primary, "segments": [{"id": "p1", "text": primary}],
            "media_type": "application/pdf", "coverage": {"complete": True}, "links": [],
        }
        refreshed = copy.deepcopy(document)
        refreshed["segments"][0].update(reading_order_text=reading, source_extraction_version="fixture-reading-order-v1")
        extraction = {
            "schema_version": 3, "title": "An optimization method", "applicability": "out_of_scope",
            "applicability_reason": "Optimization topic only.",
            "applicability_citation": {"segment_id": "p1", "quote": quote},
            "scope_summary": "Applicability screening", "flows": [],
            "unresolved_questions": [], "limitations": ["Stored synthetic model output"],
        }
        review = {
            "schema_version": 3, "applicability": "out_of_scope", "applicability_supported": True,
            "scope_review_complete": True, "flow_reviews": [], "limitations": [],
        }
        previous = {
            "id": "fixture", "title": "An optimization method", "source": source,
            "status": "failed", "verdict": "technical_failure", "has_confirmed_inconsistency": None,
            "error": "A previous decision step failed to ground the citation.",
            "stages": [{"stage": "citation_validation_and_decision", "status": "failed"}],
            "evidence": [],
        }
        return document, refreshed, extraction, review, previous

    def write_run(self, document, extraction, review, previous, include_review=True):
        run = self.directory / "original run"
        (run / previous["id"]).mkdir(parents=True)
        (run / "report.json").write_text(json.dumps({"papers": [previous], "inference": {"provider": "historical", "calls": 2}}))
        for name, data in (("prepared.json", document), ("extraction.json", extraction), ("review.json", review)):
            if name == "review.json" and not include_review:
                continue
            (run / previous["id"] / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return run

    def run_main(self, run, output, refresh=False):
        args = ["--run", str(run), "--output", str(output), "--workers", "2"]
        if refresh:
            args.append("--refresh-pdf-views")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return replay_study.main(args)

    def test_same_pdf_and_primary_input_can_gain_only_an_additional_citation_view(self):
        document, refreshed, _, _, _ = self.fixtures()
        original = copy.deepcopy(document)
        with patch.object(replay_study, "load_document", return_value=refreshed) as load:
            enriched = replay_study.enrich_document(document)
        load.assert_called_once_with(document["requested_source"])
        self.assertEqual(document, original)
        self.assertEqual(enriched["sha256"], original["sha256"])
        self.assertEqual(enriched["text"], original["text"])
        self.assertEqual(enriched["segments"][0]["text"], original["segments"][0]["text"])
        self.assertEqual(enriched["segments"][0]["reading_order_text"], refreshed["segments"][0]["reading_order_text"])
        self.assertTrue(enriched["citation_views_enriched"])

    def test_changed_pdf_hash_pages_primary_text_or_page_identity_are_rejected(self):
        for changed in ("hash", "page_count", "primary_text", "segment_id"):
            with self.subTest(changed=changed):
                document, refreshed, _, _, _ = self.fixtures()
                if changed == "hash":
                    refreshed["sha256"] = hashlib.sha256(b"different PDF bytes").hexdigest()
                elif changed == "page_count":
                    refreshed["segments"].append({"id": "p2", "text": "Another page"})
                elif changed == "primary_text":
                    refreshed["segments"][0]["text"] += " changed"
                else:
                    refreshed["segments"][0]["id"] = "p2"
                with patch.object(replay_study, "load_document", return_value=refreshed):
                    with self.assertRaises(ValueError):
                        replay_study.enrich_document(document)

    def test_existing_model_outputs_recover_a_decision_failure_as_insufficient_without_inference(self):
        document, _, extraction, review, previous = self.fixtures(quote="This invented topic quote is absent.")
        run = self.write_run(document, extraction, review, previous)
        before = {path.name: path.read_bytes() for path in (run / "fixture").iterdir()}
        output = self.directory / "replayed"
        with patch.object(replay_study, "load_document", side_effect=AssertionError("No refresh requested")):
            code = self.run_main(run, output)
        self.assertEqual(code, 0)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(len(report["papers"]), 1)
        row = report["papers"][0]
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "insufficient_evidence")
        self.assertEqual(row["reason"], "applicability_citation_unverified")
        self.assertEqual(row["previous_verdict"], "technical_failure")
        self.assertNotIn("error", row)
        self.assertEqual(row["stages"][-1]["stage"], "decision_replay")
        self.assertEqual(row["stages"][-1]["inference_calls"], 0)
        self.assertEqual(report["replay"]["model_calls"], 0)
        for name in ("extraction.json", "review.json"):
            self.assertEqual(row["model_output_hashes"][name], hashlib.sha256(before[name]).hexdigest())
            self.assertEqual(json.loads((output / "fixture" / name).read_text()), json.loads(before[name]))
        self.assertEqual({path.name: path.read_bytes() for path in (run / "fixture").iterdir()}, before)
        self.api.assert_not_called()
        self.codex.assert_not_called()
        self.network.assert_not_called()

    def test_missing_model_output_remains_a_failed_case(self):
        document, _, extraction, review, previous = self.fixtures()
        previous.update(expected="not_applicable", matches_gold=True)
        run = self.write_run(document, extraction, review, previous, include_review=False)
        output = self.directory / "not recoverable"
        code = self.run_main(run, output)
        self.assertEqual(code, 1)
        row = json.loads((output / "report.json").read_text())["papers"][0]
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIsNone(row["matches_gold"])
        self.assertTrue((output / "fixture" / "result.json").is_file())
        self.assertFalse((output / "fixture" / "review.json").exists())
        self.api.assert_not_called()
        self.codex.assert_not_called()

    def test_replay_recomputes_label_comparison_when_a_previous_verdict_changes(self):
        document, _, extraction, review, previous = self.fixtures(quote="A fabricated topic quote")
        previous.update(status="completed", verdict="inconsistent", expected="inconsistent", matches_gold=True)
        previous.pop("error", None)
        run = self.write_run(document, extraction, review, previous)
        output = self.directory / "comparison changed"
        self.assertEqual(self.run_main(run, output), 0)
        row = json.loads((output / "report.json").read_text())["papers"][0]
        self.assertEqual(row["previous_verdict"], "inconsistent")
        self.assertEqual(row["verdict"], "insufficient_evidence")
        self.assertIs(row["matches_gold"], False)

    def test_refreshed_view_locator_binds_to_the_view_text_and_the_original_pdf_hash(self):
        document, refreshed, extraction, review, previous = self.fixtures()
        run = self.write_run(document, extraction, review, previous)
        output = self.directory / "view replay"
        with patch.object(replay_study, "load_document", return_value=refreshed) as load:
            code = self.run_main(run, output, refresh=True)
        self.assertEqual(code, 0)
        load.assert_called_once_with(document["requested_source"])
        row = json.loads((output / "report.json").read_text())["papers"][0]
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "not_applicable")
        locator = row["applicability_locator"]
        reading = refreshed["segments"][0]["reading_order_text"]
        self.assertEqual(locator["text_view"], "reading_order")
        self.assertEqual(locator["document_sha256"], document["sha256"])
        self.assertEqual(locator["text_view_sha256"], hashlib.sha256(reading.encode()).hexdigest())
        self.assertEqual(reading[locator["start"]:locator["end"]], extraction["applicability_citation"]["quote"])
        saved = json.loads((output / "fixture" / "prepared.json").read_text())
        self.assertEqual(saved["segments"][0]["text"], document["segments"][0]["text"])
        self.assertEqual(saved["sha256"], document["sha256"])
        self.api.assert_not_called()
        self.codex.assert_not_called()
        self.network.assert_not_called()

    def test_refreshing_changed_pdf_keeps_failure_instead_of_mixing_versions(self):
        document, refreshed, extraction, review, previous = self.fixtures()
        refreshed["sha256"] = "changed-source-pdf"
        run = self.write_run(document, extraction, review, previous)
        output = self.directory / "rejected refresh"
        with patch.object(replay_study, "load_document", return_value=refreshed):
            code = self.run_main(run, output, refresh=True)
        self.assertEqual(code, 1)
        row = json.loads((output / "report.json").read_text())["papers"][0]
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("source PDF bytes changed", row["error"])
        self.assertFalse((output / "fixture" / "prepared.json").exists())

    def test_existing_output_is_never_overwritten(self):
        document, _, extraction, review, previous = self.fixtures()
        run = self.write_run(document, extraction, review, previous)
        output = self.directory / "existing"
        output.mkdir()
        sentinel = output / "preserve.txt"
        sentinel.write_text("original artifact")
        with self.assertRaises(SystemExit) as raised:
            self.run_main(run, output)
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(sentinel.read_text(), "original artifact")
        self.assertEqual(list(output.iterdir()), [sentinel])


if __name__ == "__main__":
    unittest.main()
