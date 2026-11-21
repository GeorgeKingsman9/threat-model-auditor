"""Offline projection controls; all paper/model/run artifacts are synthetic."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("summarize_v7_pilot", ROOT / "scripts/summarize_v7_pilot.py")
builder = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = builder
spec.loader.exec_module(builder)


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


class V7ReportBuilderTests(unittest.TestCase):
    def fixtures(self, root):
        run = root / "synthetic-v7-run"
        run.mkdir(); (run / "audits").mkdir()
        (run / "driver.py").write_text("# synthetic driver, never executed\n")
        config = {"engine_version": 7, "review_retries": 1, "max_calls_per_paper": 5, "max_total_cli_calls": 10,
            "requested_model": "synthetic-model", "provider": "test-only", "max_input_chars": 1200000,
            "max_code_chars": 500000, "source_fetch": "files", "require_source": True,
            "created_at": "synthetic-fixture", "code_commit": "a" * 40, "code_files": {},
            "papers": [{"id": paper, "source": "https://example.org/" + paper + ".pdf"} for paper in builder.PAPER_IDS]}
        save(run / "frozen_config.json", config)
        for item in config["papers"]:
            directory = run / "audits" / item["id"]; directory.mkdir()
            original = "AUTHOR_PAYLOAD_DO_NOT_PUBLISH"
            paper_sha = sha(original)
            prepared = {"source": item["source"], "requested_source": item["source"],
                "sha256": paper_sha, "media_type": "application/pdf", "segments": [{"id": "p1", "text": original}]}
            save(directory / "prepared.json", prepared)
            declaration_input = {"source_type": "application/pdf", "segments": [{"id": "p1", "text": original}], "paper_sha256": paper_sha}
            save(directory / "declared_contract.request.json", declaration_input)
            proposal = {"schema_version": 1, "paper_sha256": paper_sha, "knowledge_rules": [],
                "task_input_definition": {"definition": {"status": "unspecified", "text": "Private interpretation omitted.", "citations": []},
                                          "components": [], "relationships": []},
                "construction_recipe": {"inputs": [], "generated_artifacts": []}, "unresolved_questions": [], "limitations": []}
            declaration = {"paper_sha256": paper_sha, "trust": "untrusted_declared_contract_proposal",
                "proposal": proposal, "locators": {}, "citation_errors": [], "citations_grounded": True,
                "semantic_review_required": True}
            save(directory / "declared_contract.response.json", proposal)
            save(directory / "declared_contract.json", declaration)
            repository = {"source": "https://github.com/example/fixture", "revision": "b" * 40,
                "manifest_sha256": "c" * 64, "coverage": {"complete": True, "eligible_files": 1, "included_files": 1},
                "segments": [{"id": "repo:builder.py", "text": original}]}
            save(directory / "repository.json", repository)
            combined = {"media_type": "paper+source", "segments": [{"id": "paper:p1", "text": original},
                {"id": "repo:builder.py", "text": original}], "repository": repository,
                "model_repository": {"input_channels": {"candidates": []}}, "paper_sha256": paper_sha,
                "sha256": "d" * 64}
            content = {"source_type": combined["media_type"], "segments": combined["segments"],
                "repository": combined["model_repository"], "paper_sha256": paper_sha}
            combined["model_content_sha256"] = builder.json_hash(content)
            save(directory / "combined_input.json", combined)
            extraction = {"schema_version": 7, "input_binding": combined["sha256"], "flows": [],
                "construction_findings": [{"contract": {"citations": [{"segment_id": "paper:p1", "quote": original}]}}],
                "deployment_findings": []}
            save(directory / "extraction.json", extraction)
            save(directory / "request.json", {"input_sha256": combined["sha256"],
                "model_content_sha256": combined["model_content_sha256"], "prompt_sha256": "e" * 64,
                "max_input_chars": 1200000, "max_code_chars": 500000, "source_fetch": "files", "require_source": True})
            review_input = {**content, "input_binding": combined["sha256"], "proposal": extraction}
            save(directory / "review.request.json", review_input)
            review_prompt, schema = "Review synthetic artifact only.", {"type": "object"}
            save(directory / "review.contract.json", {"engine_version": 7, "input_binding": combined["sha256"],
                "prompt": review_prompt, "schema": schema, "prompt_sha256": sha(review_prompt),
                "schema_sha256": builder.json_hash(schema), "review_input_sha256": builder.json_hash(review_input)})
            stages = [{"stage": "declared_contract", "status": "completed", "execution": "fresh_paper_only_call"},
                {"stage": "extraction", "status": "completed", "execution": "fresh_model_call"},
                {"stage": "semantic_review", "status": "failed", "error": "Codex CLI failed (cli_failed)"},
                {"stage": "semantic_review_retry1", "status": "completed"},
                {"stage": "citation_validation_and_decision", "status": "completed"}]
            finding = {"claim": "A supplied record is used rather than a declared generated proxy.",
                "issue_type": "construction_contract_mismatch", "claim_result": "confirmed", "reason": "construction_contract_mismatch_confirmed",
                "scope": "Only the synthetic constructor branch.",
                "positive_facts": {"contract": {"description": "Declared proxy differs from provided record. " + original,
                    "supported": True, "locators": [{"segment_id": "paper:p1", "source_kind": "paper", "paper_sha256": paper_sha}]}},
                "evidence_errors": [], "semantic_review": {"reason": "Synthetic independent review supports this bounded comparison.", "scope_supported": True}}
            result = {"source": item["source"], "requested_workflow": "automatic_from_paper", "schema_version": 7,
                "status": "completed", "verdict": "inconsistent", "inconsistency": True,
                "knowledge_boundary_verdict": "insufficient_evidence", "confirmed_issue_types": ["construction_contract_mismatch"],
                "reason": "confirmed_typed_inconsistency_in_scope", "evidence": [finding], "stages": stages,
                "construction_assessment": {"findings": [finding]}, "deployment_assessment": {"findings": []}}
            save(directory / "result.json", result)
            save(directory / "report.json", {"fixture": True})
            (directory / "report.html").write_text("synthetic terminal placeholder")
            (directory / "report.md").write_text("synthetic terminal placeholder")
            calls = []
            for index, phase in enumerate(("declared_contract", "extraction", "semantic_review", "semantic_review_retry1"), 1):
                calls.append({"requested_model": "synthetic-model", "actual_model": None, "actual_models": [],
                    "request_sha256": sha("review" if index >= 3 else phase),
                    "status": "cli_failed" if index == 3 else "completed",
                    "usage": {} if index == 3 else {"input_tokens": 12, "output_tokens": 3}})
                save(directory / ("inference." + phase + ".json"), {"calls": copy.deepcopy(calls)})
            save(directory / "inference.json", {"calls": calls, "model": "synthetic-model", "max_calls": 5,
                "provider": "test-only", "usage": {"input_tokens": 36, "output_tokens": 9}, "usage_reporting_complete": False})
        return run, root / "public"

    def acquisition_fixture(self, root):
        run, public = self.fixtures(root)
        config = json.loads((run / "frozen_config.json").read_text())
        config["papers"] = [row for row in config["papers"] if row["id"] == "muzzle"]
        config.update(acquisition_passes=1, max_calls_per_paper=6, max_total_cli_calls=6)
        save(run / "frozen_config.json", config)
        shutil.rmtree(run / "audits/obliinjection")
        directory = run / "audits/muzzle"
        combined = json.loads((directory / "combined_input.json").read_text())
        original = json.loads((directory / "extraction.json").read_text())
        old_step = {"kind": "source", "input_symbol": "record.value", "output_symbol": "constructor.argument",
            "citation": {"segment_id": "repo:builder.py", "quote": "AUTHOR_PAYLOAD_DO_NOT_PUBLISH"}, "explanation": "Original step."}
        original["flows"] = [{"claim": "Original claim unchanged.", "permission": "unspecified",
                              "code_path": [old_step], "binding": {"recipient_role": "attacker_optimizer"}}]
        save(directory / "extraction.json", original)
        prefix = {**copy.deepcopy(old_step), "input_symbol": "configuration.value", "output_symbol": "record.value",
                  "explanation": "A new proposed upstream source."}
        candidate = {"claim": "A task-acquisition candidate.", "dependency_flow_index": 0}
        refined = copy.deepcopy(original)
        refined["flows"][0]["code_path"] = [prefix, old_step]
        refined["deployment_findings"] = [candidate]
        response = {"input_binding": combined["sha256"], "dependency_audits": [{
            "flow_index": 0, "source_prefix": [prefix], "deployment_finding": candidate,
            "evaluation_location": {"status": "sandbox", "description": "The measurement is sandboxed."},
            "first_knowledge": {"status": "pre_observation", "description": "A configured task precedes observation."},
            "observation_relation": {"status": "unestablished", "description": "A source-matched observation route is not demonstrated."},
            "reason": "The upstream search found a supplied task input."}]}
        notes = [{"flow_index": 0, "status": "proposed_unreviewed", "reason": "source_prefix_prepended",
                  "prefix_steps": 1, "original_steps_preserved": True},
                 {"flow_index": 0, "status": "proposed_unreviewed", "reason": "deployment_candidate_appended",
                  "finding_index": 0, "quotation_issues": 0, "independent_review_required": True}]
        save(directory / "acquisition_pass.request.json", {**builder.bound_content(combined), "proposal": original})
        save(directory / "acquisition_pass.response.json", response)
        save(directory / "acquisition_pass.checks.json", notes)
        save(directory / "extraction.acquisition.json", refined)
        result = json.loads((directory / "result.json").read_text())
        result["effective_extraction_file"] = "extraction.acquisition.json"
        result["stages"].insert(2, {"stage": "acquisition_pass", "status": "completed", "classification_fields_modified": False})
        save(directory / "result.json", result)
        self.rebind_review(directory, refined)
        calls = []
        phases = ("declared_contract", "extraction", "acquisition_pass", "semantic_review", "semantic_review_retry1")
        for index, phase in enumerate(phases, 1):
            calls.append({"requested_model": "synthetic-model", "actual_model": None, "actual_models": [],
                "request_sha256": sha("review" if index >= 4 else phase),
                "status": "cli_failed" if index == 4 else "completed",
                "usage": {} if index == 4 else {"input_tokens": 12, "output_tokens": 3}})
            save(directory / ("inference." + phase + ".json"), {"calls": copy.deepcopy(calls)})
        save(directory / "inference.json", {"calls": calls, "model": "synthetic-model", "max_calls": 6,
            "provider": "test-only", "usage": {"input_tokens": 48, "output_tokens": 12}, "usage_reporting_complete": False})
        return run, public

    def rebind_review(self, directory, proposal):
        review = json.loads((directory / "review.request.json").read_text())
        review["proposal"] = proposal
        save(directory / "review.request.json", review)
        contract = json.loads((directory / "review.contract.json").read_text())
        contract["review_input_sha256"] = builder.json_hash(review)
        save(directory / "review.contract.json", contract)

    def test_finished_report_keeps_three_types_boundary_and_failed_retry(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            report, manifest, combined = builder.build(run, public)
            self.assertEqual(report["summary"]["model_invocation_count"], 8)
            self.assertEqual(report["summary"]["failed_invocation_count"], 2)
            self.assertEqual(report["summary"]["review_retry_count"], 2)
            self.assertEqual(report["paper_results"][0]["knowledge_boundary_verdict"], "insufficient_evidence")
            self.assertEqual(report["paper_results"][0]["paper_verdict"], "inconsistent")
            self.assertEqual(set(report["summary"]["claim_category_counts"]), set(builder.CATEGORIES))
            serialized = json.dumps(report, ensure_ascii=False)
            self.assertNotIn("AUTHOR_PAYLOAD_DO_NOT_PUBLISH", serialized)
            self.assertNotIn('"quote"', serialized)
            self.assertGreater(len(manifest["files"]), 20)
            self.assertIn("driver.py", {item["path"] for item in manifest["files"]})
            self.assertIn("audits/muzzle/report.html", {item["path"] for item in manifest["files"]})
            builder.write_outputs(report, manifest, combined, public)
            self.assertIn("Findings and unresolved checks", (public / "report.html").read_text())
            self.assertIn("semantic_review_retry1", (public / "report.md").read_text())
            with self.assertRaises(FileExistsError): builder.build(run, public)

    def test_paper_only_stage_cannot_receive_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            path = run / "audits/muzzle/declared_contract.request.json"
            value = json.loads(path.read_text()); value["repository"] = {"source": "injected"}; save(path, value)
            with self.assertRaisesRegex(ValueError, "paper-only"): builder.build(run, public)
            self.assertFalse(public.exists())

    def test_review_payload_proposal_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            path = run / "audits/muzzle/review.request.json"
            value = json.loads(path.read_text()); value["proposal"]["flows"] = ["changed"]; save(path, value)
            with self.assertRaisesRegex(ValueError, "exact model input"): builder.build(run, public)

    def test_retry_must_reuse_exact_failed_request(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            directory = run / "audits/muzzle"
            for name in ("inference.json", "inference.semantic_review_retry1.json"):
                path = directory / name; value = json.loads(path.read_text())
                value["calls"][-1]["request_sha256"] = sha("changed retry"); save(path, value)
            with self.assertRaisesRegex(ValueError, "exact request/model"): builder.build(run, public)

    def test_cumulative_snapshot_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            path = run / "audits/muzzle/inference.semantic_review.json"
            value = json.loads(path.read_text()); value["calls"][0]["usage"] = {}; save(path, value)
            with self.assertRaisesRegex(ValueError, "unchanged prefix"): builder.build(run, public)

    def test_existing_proposals_and_label_sidecars_are_rejected(self):
        for damage in ("proposal", "label"):
            with self.subTest(damage=damage), tempfile.TemporaryDirectory() as temporary:
                run, public = self.fixtures(Path(temporary))
                path = run / "audits/muzzle/result.json" if damage == "proposal" else run / "audits/muzzle/request.json"
                value = json.loads(path.read_text())
                if damage == "proposal": value["stages"][1]["execution"] = "supplied_automatic_proposal"
                else: value["expected_verdict"] = "inconsistent"
                save(path, value)
                with self.assertRaises(ValueError): builder.build(run, public)

    def test_technical_failure_is_kept_separate_from_paper_uncertainty(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.fixtures(Path(temporary))
            path = run / "audits/muzzle/result.json"
            result = json.loads(path.read_text()); result.update(status="failed", verdict="technical_failure", inconsistency=None,
                error="Synthetic review failure", evidence=[], confirmed_issue_types=[]); save(path, result)
            report, _, _ = builder.build(run, public)
            self.assertEqual(report["summary"]["papers"]["technical_failure_count"], 1)
            self.assertEqual(report["summary"]["papers"]["insufficient_evidence_count"], 0)
            self.assertIsNone(report["paper_results"][0]["inconsistency"])

    def test_separate_subset_acquisition_preserves_automatic_classifications(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.acquisition_fixture(Path(temporary))
            with self.assertRaisesRegex(ValueError, "selected paper IDs"): builder.build(run, public)
            report, manifest, combined = builder.build(run, public, ["muzzle"])
            self.assertEqual(report["summary"]["papers"]["count"], 1)
            self.assertEqual(report["summary"]["model_invocation_count"], 5)
            acquisition = report["paper_results"][0]["acquisition_pass"]
            self.assertTrue(acquisition["classification_fields_preserved"])
            self.assertEqual(acquisition["appended_candidate_count"], 1)
            self.assertEqual(acquisition["source_prefixes"][0]["steps"], 1)
            builder.write_outputs(report, manifest, combined, public)
            self.assertIn("Acquisition evidence pass", (public / "report.html").read_text())
            self.assertNotIn("AUTHOR_PAYLOAD_DO_NOT_PUBLISH", json.dumps(report))

    def test_acquisition_pass_cannot_relabel_original_flow_even_with_rebound_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.acquisition_fixture(Path(temporary))
            directory = run / "audits/muzzle"
            proposal = json.loads((directory / "extraction.acquisition.json").read_text())
            proposal["flows"][0]["permission"] = "deny"
            save(directory / "extraction.acquisition.json", proposal)
            self.rebind_review(directory, proposal)
            with self.assertRaisesRegex(ValueError, "original flow classification"):
                builder.build(run, public, ["muzzle"])

    def test_acquisition_pass_cannot_replace_an_old_path_step(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.acquisition_fixture(Path(temporary))
            directory = run / "audits/muzzle"
            proposal = json.loads((directory / "extraction.acquisition.json").read_text())
            proposal["flows"][0]["code_path"][-1]["explanation"] = "Changed original path."
            save(directory / "extraction.acquisition.json", proposal)
            self.rebind_review(directory, proposal)
            with self.assertRaisesRegex(ValueError, "every original path step"):
                builder.build(run, public, ["muzzle"])

    def test_acquisition_input_cannot_load_a_previous_proposal(self):
        with tempfile.TemporaryDirectory() as temporary:
            run, public = self.acquisition_fixture(Path(temporary))
            path = run / "audits/muzzle/acquisition_pass.request.json"
            request = json.loads(path.read_text())
            request["proposal"]["flows"][0]["claim"] = "An older proposal from somewhere else."
            save(path, request)
            with self.assertRaisesRegex(ValueError, "current-run automatic proposal"):
                builder.build(run, public, ["muzzle"])


if __name__ == "__main__":
    unittest.main()
