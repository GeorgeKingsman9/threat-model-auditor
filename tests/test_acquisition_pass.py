"""Synthetic proposal mechanics, not verdict labels or model-accuracy tests."""

import copy
import unittest

import acquisition_pass as acquisition
import extraction_v7 as v7
import test_extraction_v7 as toy


class AcquisitionPassTests(unittest.TestCase):
    def fixtures(self):
        document, extraction, _ = toy.ExtractionV7Tests().fixtures()
        source = next(p for p in document["segments"] if p.get("path") == "generator.py")
        paper = next(p for p in document["segments"] if p.get("source_kind") == "paper")
        code_cite = {"segment_id": source["id"], "quote": 'record = case["user_request"]'}
        paper_cite = {"segment_id": paper["id"], "quote": "All evaluated attacker channels share the same knowledge budget"}
        prefix = [{"kind": "source", "input_symbol": "supplied.case",
                   "output_symbol": extraction["flows"][0]["code_path"][0]["input_symbol"],
                   "citation": {"segment_id": source["id"], "quote": "def build(case, backend)"},
                   "explanation": "Candidate argument-origin prefix, awaiting semantic review."}]
        audit = {"flow_index": 0,
            "evaluation_location": {"status": "unspecified", "description": "No evaluation venue established.", "citations": []},
            "first_knowledge": {"status": "unresolved", "description": "The first upstream acquisition is not established.",
                                "citations": [copy.deepcopy(code_cite)]},
            "observation_relation": {"status": "unestablished", "description": "No observed-task acquisition route is established.",
                                     "citations": [copy.deepcopy(paper_cite), copy.deepcopy(code_cite)]},
            "source_prefix": prefix, "deployment_finding": None,
            "reason": "Candidate provenance completion; no permission or verdict changes."}
        response = {"input_binding": document["sha256"], "dependency_audits": [audit]}
        return document, extraction, response, code_cite, paper_cite

    def candidate(self, code, paper, flow_index=0):
        # This deliberately unresolved candidate exercises shape, linkage and
        # citation plumbing. It is not a claim of deployment confirmed by paper.
        def fact(citation):
            return {"description": "An untrusted candidate axis requiring independent semantic review.",
                    "citations": [copy.deepcopy(citation)]}
        return {"claim": "Candidate task-acquisition applicability question.",
            "issue_type": "deployment_provenance", "paper_claim": {"description": "Unreviewed scenario proposal.", "citation": copy.deepcopy(paper)},
            "conditional_construction": fact(code), "required_knowledge": fact(code),
            "knowledge_provenance": {"status": "unresolved", **fact(code)},
            "assessment": "uncertain", "materiality": "uncertain", "scope": "Named synthetic task-conditioning flow only.",
            "unresolved_questions": ["Deployment claim and acquisition route need independent review."],
            "dependency_flow_index": flow_index,
            "source_boundary": {"basis": "unresolved", **fact(paper)},
            "actual_source": {"origin": "unknown", **fact(code)},
            "timing": {"status": "unresolved", **fact(code)},
            "task_relation": {"status": "unknown", "description": "The task/scenario relation remains unresolved.",
                              "citations": [copy.deepcopy(paper), copy.deepcopy(code)]},
            "deployment_scope": {"status": "uncertain", **fact(paper)}}

    def test_payload_has_only_original_bound_content_and_automatic_proposal(self):
        document, extraction, _, _, _ = self.fixtures()
        content = v7.model_content(document)
        before = copy.deepcopy((content, extraction))
        result = acquisition.prepare_acquisition_input(content, extraction)
        self.assertEqual(set(result), set(content) | {"proposal"})
        self.assertEqual(result["proposal"], extraction)
        self.assertEqual((content, extraction), before)
        result["proposal"]["flows"][0]["permission"] = "allow"
        self.assertEqual((content, extraction), before)

    def test_classification_sidecars_and_top_level_extra_payload_are_rejected(self):
        document, extraction, _, _, _ = self.fixtures()
        content = v7.model_content(document)
        with self.assertRaisesRegex(ValueError, "original source-aware"):
            acquisition.prepare_acquisition_input({**content, "gold": "desired"}, extraction)
        content["repository"]["historical_results"] = {"prior_verdict": "desired"}
        with self.assertRaisesRegex(ValueError, "sidecar"):
            acquisition.prepare_acquisition_input(content, extraction)

    def test_author_prose_mentioning_label_words_is_still_untrusted_text(self):
        document, extraction, _, _, _ = self.fixtures()
        content = v7.model_content(document)
        content["segments"][0]["text"] += '\nAn author field example says {"gold": "answer"}.'
        result = acquisition.prepare_acquisition_input(content, extraction)
        self.assertIn('"gold"', result["segments"][0]["text"])

    def test_valid_prefix_preserves_old_path_and_every_classification_field(self):
        document, extraction, response, _, _ = self.fixtures()
        before = copy.deepcopy((document, extraction, response))
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined["flows"][0]["code_path"][1:], extraction["flows"][0]["code_path"])
        expected = copy.deepcopy(extraction)
        expected["flows"][0]["code_path"] = response["dependency_audits"][0]["source_prefix"] + expected["flows"][0]["code_path"]
        self.assertEqual(refined, expected)
        self.assertEqual((document, extraction, response), before)
        self.assertIn("source_prefix_prepended", [n["reason"] for n in notes])
        self.assertTrue(all(n["status"] != "confirmed" for n in notes))

    def test_invalid_prefix_extra_quote_rejects_entire_prefix(self):
        document, extraction, response, _, _ = self.fixtures()
        prefix = response["dependency_audits"][0]["source_prefix"]
        prefix.append({**copy.deepcopy(prefix[0]), "input_symbol": prefix[0]["output_symbol"],
                       "output_symbol": prefix[0]["output_symbol"],
                       "citation": {**prefix[0]["citation"], "quote": "an absent extra code quote"}})
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined, extraction)
        self.assertIn("source_prefix_rejected", [n["reason"] for n in notes])

    def test_paper_or_foreign_segment_cannot_be_prepended_as_code(self):
        document, extraction, response, _, paper = self.fixtures()
        for citation in (paper, {"segment_id": "foreign-paper:p1", "quote": "foreign text"}):
            with self.subTest(citation=citation):
                changed = copy.deepcopy(response)
                changed["dependency_audits"][0]["source_prefix"][0]["citation"] = citation
                refined, notes = acquisition.apply_acquisition_pass(extraction, changed, document)
                self.assertEqual(refined, extraction)
                self.assertIn("source_prefix_rejected", [n["reason"] for n in notes])

    def test_prefix_must_connect_internally_and_to_original_first_input(self):
        document, extraction, response, _, _ = self.fixtures()
        for mode in ("join", "internal", "empty"):
            with self.subTest(mode=mode):
                changed = copy.deepcopy(response)
                prefix = changed["dependency_audits"][0]["source_prefix"]
                if mode == "join":
                    prefix[-1]["output_symbol"] = "different-original-symbol"
                elif mode == "internal":
                    prefix.append({**copy.deepcopy(prefix[0]), "input_symbol": "disconnected"})
                else:
                    prefix[0]["input_symbol"] = " "
                refined, notes = acquisition.apply_acquisition_pass(extraction, changed, document)
                self.assertEqual(refined, extraction)
                self.assertIn("source_prefix_rejected", [n["reason"] for n in notes])

    def test_candidate_append_keeps_original_paths_and_unknown_axes_unreviewed(self):
        document, extraction, response, code, paper = self.fixtures()
        response["dependency_audits"][0]["source_prefix"] = []
        candidate = self.candidate(code, paper)
        response["dependency_audits"][0]["deployment_finding"] = candidate
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        expected = copy.deepcopy(extraction)
        expected["deployment_findings"].append(candidate)
        self.assertEqual(refined, expected)
        appended = next(n for n in notes if n["reason"] == "deployment_candidate_appended")
        self.assertTrue(appended["independent_review_required"])
        self.assertEqual(appended["status"], "proposed_unreviewed")

    def test_invalid_candidate_quotes_stay_untrusted_for_later_repair_not_validated(self):
        document, extraction, response, code, paper = self.fixtures()
        candidate = self.candidate(code, paper)
        candidate["actual_source"]["citations"].append({**code, "quote": "an absent candidate code quote"})
        candidate["deployment_scope"]["citations"] = [{"segment_id": "foreign-paper:p1", "quote": "foreign scope"}]
        response["dependency_audits"][0]["deployment_finding"] = candidate
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined["deployment_findings"], [candidate])
        self.assertTrue(any(n["reason"] == "unverified_candidate_actual_source_citation" for n in notes))
        self.assertTrue(any(n["reason"] == "unverified_candidate_deployment_scope_citation" for n in notes))
        self.assertTrue(all(n["status"] != "confirmed" for n in notes))

    def test_candidate_cannot_borrow_other_flow_or_unknown_index(self):
        document, extraction, response, code, paper = self.fixtures()
        response["dependency_audits"][0]["deployment_finding"] = self.candidate(code, paper, 2)
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined["deployment_findings"], [])
        self.assertIn("candidate_dependency_flow_mismatch", [n["reason"] for n in notes])
        response["dependency_audits"][0]["flow_index"] = 20
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined, extraction)
        self.assertIn("unknown_or_nonattacker_flow_index", [n["reason"] for n in notes])

    def test_duplicate_indices_reject_all_changes_and_missing_audit_is_visible(self):
        document, extraction, response, code, paper = self.fixtures()
        response["dependency_audits"][0]["deployment_finding"] = self.candidate(code, paper)
        response["dependency_audits"] *= 2
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined, extraction)
        self.assertEqual([n["reason"] for n in notes], ["duplicate_dependency_audit"] * 2)
        response["dependency_audits"] = []
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(refined, extraction)
        self.assertIn("dependency_audit_missing", [n["reason"] for n in notes])

    def test_binding_change_or_injected_classification_fields_fail_shape_validation(self):
        document, extraction, response, _, _ = self.fixtures()
        response["input_binding"] = "different-evidence"
        with self.assertRaisesRegex(ValueError, "different paper/source"):
            acquisition.apply_acquisition_pass(extraction, response, document)
        response["input_binding"] = document["sha256"]
        response["dependency_audits"][0]["permission"] = "allow"
        with self.assertRaisesRegex(ValueError, "extra fields"):
            acquisition.apply_acquisition_pass(extraction, response, document)

    def test_bounded_audits_citations_and_combined_path(self):
        document, extraction, response, code, paper = self.fixtures()
        oversized = copy.deepcopy(response)
        oversized["dependency_audits"] *= 7
        with self.assertRaisesRegex(ValueError, "six-audit"):
            acquisition.apply_acquisition_pass(extraction, oversized, document)
        oversized = copy.deepcopy(response)
        oversized["dependency_audits"][0]["first_knowledge"]["citations"] = [code] * 7
        with self.assertRaisesRegex(ValueError, "six-citation"):
            acquisition.apply_acquisition_pass(extraction, oversized, document)
        oversized = copy.deepcopy(response)
        prefix = oversized["dependency_audits"][0]["source_prefix"]
        prefix *= 16
        refined, notes = acquisition.apply_acquisition_pass(extraction, oversized, document)
        self.assertEqual(refined, extraction)
        self.assertIn("source_prefix_rejected", [n["reason"] for n in notes])
        extraction["deployment_findings"] = [self.candidate(code, paper)] * 4
        response["dependency_audits"][0]["deployment_finding"] = self.candidate(code, paper)
        refined, notes = acquisition.apply_acquisition_pass(extraction, response, document)
        self.assertEqual(len(refined["deployment_findings"]), 4)
        self.assertIn("deployment_candidate_limit_reached", [n["reason"] for n in notes])


if __name__ == "__main__":
    unittest.main()
