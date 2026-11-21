"""Synthetic tests for construction contracts; no paper labels or model calls.

Review votes exercise deterministic gates only. The implementation flow is
grounded by the existing V5 engine, independently of this new issue family.
"""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import construction_contracts as contracts
import extraction_v4 as v4
import extraction_v5 as v5
import extraction_v6 as v6
from test_extraction_v4 import digest
import test_extraction_v5 as toy


def cite(identity, quote):
    return {"segment_id": identity, "quote": quote}


class ConstructionContractsTests(unittest.TestCase):
    def fixtures(self, engine=v5):
        paper, repository, _, extraction, review = toy.ExtractionV5Tests().fixtures()
        recipe = "For ordinary construction, generate a proxy request from category metadata."
        exception = "Only the diagnostic arm may instead reuse the evaluated request verbatim."
        paper["segments"] += [{"id": "p3", "text": recipe}, {"id": "p4", "text": exception}]
        paper["text"] = "\n".join(part["text"] for part in paper["segments"])
        paper["sha256"] = digest(paper["text"])
        document = engine.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        if engine is v6:
            extraction.update(schema_version=6, channel_assessments=[], deployment_findings=[])
            review.update(schema_version=6, channel_reviews=[], deployment_reviews=[])
        flow_rows = engine.decide_extraction(extraction, review, document)["evidence"]
        source = next(part for part in repository["segments"] if part["path"] == "generator.py")
        source_cite = cite(source["id"], 'record = case["user_request"]')
        mapping_cite = cite(source["id"], 'prompt = {"task": record}')
        finding = {
            "claim": "Ordinary construction uses an evaluated request rather than the specified proxy source.",
            "flow_index": 0,
            "instance_requirement": "same_evaluated_instance",
            "contract": {"description": "The ordinary arm specifies a proxy request generated from metadata.",
                         "citations": [cite("paper:p3", recipe)]},
            "implemented_source": {"description": "The evaluated case request enters the constructor's prompt.",
                                   "citations": [source_cite]},
            "semantic_mapping": {
                "description": "The conceptual request is the task component serialized from the case record.",
                "paper_citations": [cite("paper:p3", "generate a proxy request from category metadata")],
                "code_citations": [mapping_cite],
            },
            "comparison": {"kind": "incompatible_source",
                           "description": "Direct evaluated-record reuse differs from the specified metadata proxy source."},
            "exceptions": {"status": "none_applicable",
                           "description": "The explicit reuse exception is restricted to the diagnostic arm, not ordinary construction.",
                           "citations": [cite("paper:p4", exception)]},
            "scope": "Released ordinary construction branch and its cited task input.",
            "assessment": "mismatch",
        }
        vote = {"index": 0, "contract_supported": True, "implementation_supported": True,
                "semantic_mapping_supported": True, "comparison_supported": True,
                "scope_supported": True, "exceptions_supported": True, "assessment": "mismatch",
                "reason": "The declared source differs from the source received on this independently grounded path."}
        return document, finding, vote, flow_rows, extraction, review

    def project(self, document, finding, review, rows, **kwargs):
        return contracts.project_construction_findings(
            [finding], [review], document, rows, input_binding=document["sha256"],
            review_input_binding=document["sha256"], **kwargs)

    def test_reviewed_mismatch_is_separate_from_permission_or_effect(self):
        document, finding, review, rows, _, _ = self.fixtures()
        before = copy.deepcopy((document, finding, review, rows))
        result = self.project(document, finding, review, rows)
        row = result["findings"][0]
        self.assertEqual(row["claim_result"], "confirmed")
        self.assertEqual(row["issue_type"], "construction_contract_mismatch")
        self.assertTrue(row["delivery_linked"])
        self.assertTrue(result["has_confirmed_mismatch"])
        self.assertFalse(row["historical_execution_established"])
        self.assertEqual(row["observed_effect"], "not_assessed")
        self.assertNotIn("permission", row)
        self.assertNotIn("verdict", result)
        self.assertEqual((document, finding, review, rows), before)

    def test_policy_uncertainty_does_not_erase_independently_established_delivery(self):
        document, finding, review, _, extraction, policy_review = self.fixtures()
        flow = extraction["flows"][0]
        flow["permission"] = "unspecified"
        flow["policy_application"]["status"] = "uncertain"
        policy_review["flow_reviews"][0]["policy_application"] = "uncertain"
        result = v5.decide_extraction(extraction, policy_review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertTrue(result["evidence"][0]["source_validation"]["delivery_supported"])
        self.assertTrue(self.project(document, finding, review, result["evidence"])["has_confirmed_mismatch"])

    def test_v6_grounded_flow_rows_support_the_separate_contract_track(self):
        document, finding, review, rows, _, _ = self.fixtures(engine=v6)
        result = self.project(document, finding, review, rows)
        self.assertTrue(result["has_confirmed_mismatch"])
        self.assertTrue(result["findings"][0]["instance_alignment_supported"])
        self.assertEqual(len(result["findings"][0]["locators"]["instances"]), 2)

    def test_all_review_axes_required(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for field in ("contract_supported", "implementation_supported", "semantic_mapping_supported",
                      "comparison_supported", "scope_supported", "exceptions_supported"):
            with self.subTest(field=field):
                changed = {**review, field: False}
                result = self.project(document, finding, changed, rows)
                self.assertEqual(result["findings"][0]["claim_result"], "unresolved")
                self.assertFalse(result["has_confirmed_mismatch"])
                self.assertTrue(result["blocks_negative"])

    def test_positive_grounding_needs_all_axes_and_all_extra_quotes(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for field in ("contract", "implemented_source", "exceptions"):
            with self.subTest(field=field):
                changed = copy.deepcopy(finding)
                changed[field]["citations"].append({**changed[field]["citations"][0], "quote": "invented absent passage"})
                row = self.project(document, changed, review, rows)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertTrue(row["evidence_errors"])
                self.assertEqual(len(row["locators"][field]), 1)

    def test_both_paper_and_code_semantic_mapping_are_required(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for field in ("paper_citations", "code_citations"):
            with self.subTest(field=field):
                changed = copy.deepcopy(finding)
                changed["semantic_mapping"][field] = []
                row = self.project(document, changed, review, rows)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertEqual(row["reason"], "construction_semantic_mapping_not_established")

    def test_citation_domains_cannot_be_swapped(self):
        document, finding, review, rows, _, _ = self.fixtures()
        changed = copy.deepcopy(finding)
        changed["contract"]["citations"] = copy.deepcopy(finding["implemented_source"]["citations"])
        row = self.project(document, changed, review, rows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertTrue(any("must reference paper" in error for error in row["evidence_errors"]))

    def test_missing_or_unconfirmed_receipt_is_unresolved(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for value in (False, "true", None):
            changed = copy.deepcopy(rows)
            changed[0]["source_validation"]["delivery_supported"] = value
            row = self.project(document, finding, review, changed)["findings"][0]
            self.assertEqual(row["claim_result"], "unresolved")
            self.assertEqual(row["reason"], "construction_delivery_not_linked")
        self.assertEqual(self.project(document, finding, review, [])["findings"][0]["claim_result"], "unresolved")

    def test_another_flow_path_cannot_cover_the_implemented_source(self):
        document, finding, review, rows, _, _ = self.fixtures()
        evaluator = next(part for part in document["segments"] if part.get("path") == "evaluator.py")
        other = v4._locate(cite(evaluator["id"], 'reply = read_artifact(case["id"])'), document, "code")
        changed = copy.deepcopy(rows)
        changed[0]["source_validation"]["code_path_locators"] = [other]
        row = self.project(document, finding, review, changed)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertIn("construction_source_not_linked_to_delivery_path", row["evidence_errors"])

    def test_evaluator_receipt_or_unsupported_attacker_binding_cannot_confirm(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for group, field, value in (("flow_binding", "recipient_role", "evaluator"),
                                    ("flow_binding", "recipient_role", "simulator"),
                                    ("flow_binding", "attacker_delivery", "unresolved"),
                                    ("flow_binding", "alignment_verified", False),
                                    ("binding_validation", "recipient_supported", False),
                                    ("source_validation", "binding_supported", False)):
            with self.subTest(group=group, field=field, value=value):
                changed = copy.deepcopy(rows)
                changed[0][group][field] = value
                row = self.project(document, finding, review, changed)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertIn("construction_attacker_recipient_not_established", row["evidence_errors"])

    def test_same_instance_claim_needs_the_checked_instance_mapping(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for group, field, value in (("flow_binding", "instance_relation", "unknown"),
                                    ("flow_binding", "instance_relation", "different"),
                                    ("binding_validation", "instance_alignment_supported", False),
                                    ("source_validation", "instance_alignment_supported", False)):
            with self.subTest(group=group, field=field, value=value):
                changed = copy.deepcopy(rows)
                changed[0][group][field] = value
                row = self.project(document, finding, review, changed)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertIn("construction_same_instance_not_established", row["evidence_errors"])
        changed = copy.deepcopy(rows)
        changed[0]["binding_validation"]["locators"]["instances"] = []
        row = self.project(document, finding, review, changed)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertIn("construction_instance_evidence_requires_independent_bindings", row["evidence_errors"])

    def test_category_contract_can_be_independent_of_an_evaluation_instance(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["instance_requirement"] = "any_instance"
        rows[0]["flow_binding"]["instance_relation"] = "unknown"
        rows[0]["binding_validation"]["instance_alignment_supported"] = False
        rows[0]["source_validation"]["instance_alignment_supported"] = False
        self.assertTrue(self.project(document, finding, review, rows)["has_confirmed_mismatch"])
        finding["instance_requirement"] = "unspecified"
        row = self.project(document, finding, review, rows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertEqual(row["reason"], "construction_instance_scope_not_established")

    def test_changed_path_metadata_and_stale_input_are_rejected(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for field, value in (("document_sha256", "stale"), ("file_sha256", "tampered"),
                             ("start", -1), ("source_kind", "paper")):
            with self.subTest(field=field):
                changed = copy.deepcopy(rows)
                changed[0]["source_validation"]["code_path_locators"][0][field] = value
                row = self.project(document, finding, review, changed)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertTrue(any("construction_delivery_path:" in error for error in row["evidence_errors"]))

    def test_input_hash_changes_and_cross_snapshot_bindings_fail_closed(self):
        document, finding, review, rows, _, _ = self.fixtures()
        with self.assertRaisesRegex(ValueError, "input binding"):
            contracts.project_construction_findings([finding], [review], document, rows,
                input_binding="old", review_input_binding=document["sha256"])
        changed = copy.deepcopy(document)
        changed["segments"][0]["text"] += "tampered"
        with self.assertRaisesRegex(ValueError, "input binding"):
            self.project(changed, finding, review, rows)

    def test_applicable_exception_can_refute_a_sourced_difference(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["exceptions"]["status"] = "applicable"
        finding["exceptions"]["description"] = "The named diagnostic scope explicitly permits this record reuse."
        finding["scope"] = "The explicitly named diagnostic arm."
        finding["assessment"] = review["assessment"] = "aligned"
        result = self.project(document, finding, review, rows)
        self.assertEqual(result["findings"][0]["claim_result"], "refuted")
        self.assertEqual(result["findings"][0]["reason"], "construction_contract_exception_applies")
        self.assertFalse(result["blocks_negative"])

    def test_unresolved_exception_is_not_a_confirmed_mismatch(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["exceptions"]["status"] = "unresolved"
        row = self.project(document, finding, review, rows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertEqual(row["reason"], "construction_exception_scope_unresolved")

    def test_explicit_alignment_is_a_scoped_refutation(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["comparison"] = {"kind": "aligned", "description": "A supplied specific contract explicitly permits this branch's record source."}
        finding["assessment"] = review["assessment"] = "aligned"
        row = self.project(document, finding, review, rows)["findings"][0]
        self.assertEqual(row["claim_result"], "refuted")
        self.assertEqual(row["reason"], "construction_contract_alignment_confirmed")

    def test_missing_recipe_is_not_deny_or_mismatch(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["contract"] = {"description": "No generator was found in the repository.", "citations": []}
        result = self.project(document, finding, review, rows)
        self.assertFalse(result["has_confirmed_mismatch"])
        self.assertEqual(result["findings"][0]["claim_result"], "unresolved")

    def test_disagreement_or_unresolved_comparison_does_not_force_positive(self):
        document, finding, review, rows, _, _ = self.fixtures()
        changed = {**review, "assessment": "uncertain"}
        self.assertEqual(self.project(document, finding, changed, rows)["findings"][0]["reason"], "construction_review_disagrees")
        finding["comparison"]["kind"] = "unresolved"
        self.assertFalse(self.project(document, finding, review, rows)["has_confirmed_mismatch"])

    def test_named_scope_is_required_and_outside_scope_does_not_block_clean(self):
        document, finding, review, rows, _, _ = self.fixtures()
        finding["scope"] = ""
        row = self.project(document, finding, review, rows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertEqual(row["reason"], "construction_scope_not_established")
        finding["scope"] = "A scoped conditional construction."
        result = self.project(document, finding, review, rows, in_audit_scope=False)
        self.assertFalse(result["has_confirmed_mismatch"])
        self.assertFalse(result["blocks_general_clean"])
        self.assertEqual(result["findings"][0]["reason"], "construction_outside_audit_scope")

    def test_limits_and_complete_independent_review_coverage_are_enforced(self):
        document, finding, review, rows, _, _ = self.fixtures()
        def project(findings, reviews):
            return contracts.project_construction_findings(findings, reviews, document, rows,
                input_binding=document["sha256"], review_input_binding=document["sha256"])
        for votes in ([], [review, review], [{**review, "index": -1}]):
            with self.assertRaisesRegex(ValueError, "review must cover"):
                project([finding], votes)
        with self.assertRaisesRegex(ValueError, "at most four"):
            project([finding] * 5, [{**review, "index": i} for i in range(5)])
        finding["implemented_source"]["citations"] *= 7
        with self.assertRaisesRegex(ValueError, "six-citation"):
            project([finding], [review])

    def test_empty_findings_make_no_general_clean_claim(self):
        document, _, _, rows, _, _ = self.fixtures()
        result = contracts.project_construction_findings([], [], document, rows,
            input_binding=document["sha256"], review_input_binding=document["sha256"])
        self.assertFalse(result["general_clean_established"])
        self.assertFalse(result["has_confirmed_mismatch"])

    def test_empty_claim_or_review_reason_is_not_confirmation(self):
        document, finding, review, rows, _, _ = self.fixtures()
        for target, field in ((finding, "claim"), (review, "reason")):
            before = target[field]
            target[field] = " "
            self.assertFalse(self.project(document, finding, review, rows)["has_confirmed_mismatch"])
            target[field] = before


if __name__ == "__main__":
    unittest.main()
