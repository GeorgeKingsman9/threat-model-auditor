"""Offline v3 extraction checks using explicit proposals and review fixtures.

These tests check grounding and decision plumbing, not real model accuracy.
No known-paper labels, model generation, or provider calls are used.
"""

import copy
import hashlib
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction as v2
import extraction_v3 as v3


class ExtractionV3Tests(unittest.TestCase):
    def fixtures(self):
        text = (
            "This paper evaluates indirect prompt injection. "
            "External attackers may not read the exact evaluation query. "
            "In the evaluated construction arm, the payload generator receives that exact evaluation query. "
            "The input boundary excludes the future test query and accepts only public task topics. "
            "The benchmark discloses a stronger baseline without settling its knowledge budget. "
            "The user security goal is no secret disclosure without consent. "
            "The attack trace shows successful secret disclosure to a remote attacker. "
            "The utility metric concerns task outcomes, not private-query delivery. "
            "An ablation found no clear ASR effect."
        )
        document = {
            "source": "synthetic fixture.txt", "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "segments": [{"id": "s1", "text": text}], "coverage": {"complete": True},
        }
        cite = lambda quote: {"segment_id": "s1", "quote": quote}
        declaration = cite("External attackers may not read the exact evaluation query")
        implementation = cite("the payload generator receives that exact evaluation query")
        extraction = {
            "schema_version": 3, "title": "Synthetic scope fixture", "applicability": "in_scope",
            "applicability_reason": "The document discusses an IPI evaluation.",
            "applicability_citation": cite("evaluates indirect prompt injection"),
            "scope_summary": "Only the explicitly named query-delivery suspicion",
            "flows": [{
                "claim": "The scoped constructor receives query information explicitly excluded from its knowledge budget.",
                "issue_type": "information_boundary", "information_level": "exact_query",
                "edge": {"role": "attacker-side constructor", "phase": "offline construction",
                         "source": "evaluated query", "representation": "exact query text",
                         "operation": "receive as construction input", "query_form": "full_query"},
                "permission": "deny", "observation": "present",
                "declaration": declaration, "implementation": implementation,
                "policy_application": {"policy_kind": "attacker_knowledge_constraint", "status": "applicable",
                                       "citation": copy.deepcopy(declaration), "reason": "The quoted prohibition applies to the named constructor and condition."},
                "delivery": {"status": "confirmed", "evidence_kind": "paper_procedure", "task_relation": "same_evaluated_instance",
                             "citation": copy.deepcopy(implementation), "reason": "The procedure identifies the recipient and its exact construction input."},
                "refutation": {"basis": "none", "citation": None, "reason": "No positive counterevidence refutes this claim."},
                "explanation": "Compare the scoped knowledge constraint with the stated construction input.",
            }],
            "unresolved_questions": [], "limitations": ["Paper-text fixture, not a runtime verification."],
        }
        review = {
            "schema_version": 3, "applicability": "in_scope", "applicability_supported": True,
            "scope_review_complete": True,
            "flow_reviews": [{"index": 0, "supported": True, "policy_kind": "attacker_knowledge_constraint",
                              "policy_application": "applicable", "delivery": "confirmed", "refutation": "none",
                              "reason": "The fixture's quotes support the same scoped input."}],
            "limitations": ["This review is a fixture, not a claim of model or human semantic accuracy."],
        }
        return extraction, review, document

    def decide(self, extraction, review, document):
        return v3.decide_extraction(extraction, review, document, "fixture")

    def excluded_claim(self):
        extraction, review, document = self.fixtures()
        boundary = {"segment_id": "s1", "quote": "The input boundary excludes the future test query and accepts only public task topics"}
        flow = extraction["flows"][0]
        flow.update(observation="absent", implementation=copy.deepcopy(boundary))
        flow["delivery"].update(status="excluded", citation=copy.deepcopy(boundary), reason="The described receiving boundary affirmatively excludes the target query.")
        flow["refutation"].update(basis="excluded_delivery", citation=copy.deepcopy(boundary), reason="This boundary is positive counterevidence to the named query-delivery suspicion.")
        review["flow_reviews"][0].update(delivery="excluded", refutation="excluded_delivery")
        return extraction, review, document

    def test_scoped_forbidden_delivery_still_produces_a_confirmed_finding(self):
        result = self.decide(*self.fixtures())
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertIs(result["has_confirmed_inconsistency"], True)
        self.assertEqual(result["evidence"][0]["claim_result"], "confirmed")
        self.assertEqual(result["review_status"], "model_reviewed_not_human_verified")

    def test_successful_exfiltration_does_not_make_a_security_goal_an_attacker_knowledge_constraint(self):
        extraction, review, document = self.fixtures()
        flow = extraction["flows"][0]
        goal = {"segment_id": "s1", "quote": "The user security goal is no secret disclosure without consent"}
        trace = {"segment_id": "s1", "quote": "The attack trace shows successful secret disclosure to a remote attacker"}
        flow.update(information_level="other", declaration=goal, implementation=trace)
        flow["edge"].update(source="victim secret", representation="secret content", operation="receive as attack output", query_form="unspecified")
        flow["policy_application"]["citation"] = copy.deepcopy(goal)
        flow["delivery"]["citation"] = copy.deepcopy(trace)
        self.assertEqual(self.decide(extraction, review, document)["verdict"], "inconsistent")
        # Isolate the real category error: keep deny, present, all quotes and the
        # supporting-review flags, changing only the normative policy type.
        flow["policy_application"]["policy_kind"] = "victim_security_goal"
        review["flow_reviews"][0]["policy_kind"] = "victim_security_goal"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        self.assertEqual(result["evidence"][0]["reason"], "policy_is_not_attacker_knowledge_constraint")

    def test_disclosed_stronger_baseline_with_unsettled_applicability_abstains(self):
        extraction, review, document = self.fixtures()
        flow = extraction["flows"][0]
        flow["policy_application"].update(status="uncertain", citation={"segment_id": "s1", "quote": "The benchmark discloses a stronger baseline without settling its knowledge budget"})
        review["flow_reviews"][0]["policy_application"] = "uncertain"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_whitespace_and_nfkc_quote_offsets_point_back_into_original_text(self):
        raw = "🙂 Background.\nThe ﬂow  includes\n\tＦＵＬＬ query.\nEnd."
        quote = "The flow includes FULL query."
        document = {"sha256": "fixture-hash", "segments": [{"id": "p1", "text": raw}]}
        locator = v3.locate({"segment_id": "p1", "quote": quote}, document)
        original = raw[locator["start"]:locator["end"]]
        self.assertEqual(locator["start"], raw.index("The"))
        self.assertEqual(locator["end"], raw.index("query.") + len("query."))
        self.assertIn("ﬂ", original)
        self.assertIn("ＦＵＬＬ", original)
        self.assertEqual(v3.normalized_with_offsets(original)[0], v3.normalized_with_offsets(quote)[0])
        self.assertEqual(locator["document_sha256"], "fixture-hash")

    def test_nfkc_canonical_composition_is_supported_with_original_offsets(self):
        raw = "Prefix. The cafe\u0301 uses canonical decomposition. Tail."
        quote = "The café uses canonical decomposition."
        document = {"sha256": "fixture-hash", "segments": [{"id": "p1", "text": raw}]}
        locator = v3.locate({"segment_id": "p1", "quote": quote}, document)
        self.assertEqual(raw[locator["start"]:locator["end"]], "The cafe\u0301 uses canonical decomposition.")

    def test_forged_and_normalization_ambiguous_quotes_are_rejected(self):
        document = {"sha256": "fixture-hash", "segments": [{"id": "p1", "text": "Do  not read. Do\nnot read."}]}
        for quote in ("A fabricated claim", "Do not read."):
            with self.subTest(quote=quote):
                with self.assertRaises(ValueError):
                    v3.locate({"segment_id": "p1", "quote": quote}, document)

    def test_reading_order_locator_has_its_own_view_hash_and_original_document_hash(self):
        primary = "The generator receives\nUNRELATED COLUMN\nonly public topics."
        reading = "The generator receives only public topics."
        document = {"sha256": hashlib.sha256(b"%PDF-original-bytes").hexdigest(), "segments": [
            {"id": "p1", "text": primary, "reading_order_text": reading},
        ]}
        quote = "generator receives only public topics"
        locator = v3.locate({"segment_id": "p1", "quote": quote}, document)
        self.assertEqual(locator["text_view"], "reading_order")
        self.assertEqual(locator["document_sha256"], document["sha256"])
        self.assertEqual(locator["text_view_sha256"], hashlib.sha256(reading.encode()).hexdigest())
        self.assertEqual(reading[locator["start"]:locator["end"]], quote)

    def test_overlapping_normalized_occurrences_are_ambiguous(self):
        document = {"sha256": "fixture-hash", "segments": [{"id": "p1", "text": "aaaa"}]}
        with self.assertRaises(ValueError):
            v3.locate({"segment_id": "p1", "quote": "aaa"}, document)

    def test_fake_quote_does_not_become_a_finding_even_when_review_says_supported(self):
        for field in ("declaration", "implementation"):
            with self.subTest(field=field):
                extraction, review, document = self.fixtures()
                extraction["flows"][0][field]["quote"] = "This forged quotation is not in the document."
                result = self.decide(extraction, review, document)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)
                self.assertTrue(result["evidence"][0]["citation_errors"])

    def test_every_review_field_must_agree_before_confirmation(self):
        for field, different in (("policy_kind", "victim_security_goal"), ("policy_application", "uncertain"), ("delivery", "evaluator_only"), ("refutation", "excluded_delivery"), ("supported", False)):
            with self.subTest(field=field):
                extraction, review, document = self.fixtures()
                review["flow_reviews"][0][field] = different
                result = self.decide(extraction, review, document)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)
                self.assertIn("semantic_review_disagrees", result["evidence"][0]["citation_errors"][0])

    def test_positive_counterevidence_can_clear_only_the_named_claim(self):
        result = self.decide(*self.excluded_claim())
        self.assertEqual(result["verdict"], "consistent_within_scope")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        self.assertTrue(result["coverage_complete"])
        self.assertEqual(result["evidence_scope"], "listed_claims_document_only")
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")

    def test_no_flows_unresolved_questions_or_incomplete_documents_cannot_clear_a_paper(self):
        for gap in ("empty_flows", "questions", "incomplete_document", "incomplete_review"):
            with self.subTest(gap=gap):
                extraction, review, document = self.excluded_claim()
                if gap == "empty_flows":
                    extraction["flows"] = []
                    review["flow_reviews"] = []
                elif gap == "questions":
                    extraction["unresolved_questions"] = ["Does a separate configuration expose the future query?"]
                elif gap == "incomplete_document":
                    document["coverage"]["complete"] = False
                else:
                    review["scope_review_complete"] = False
                result = self.decide(extraction, review, document)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertFalse(result["coverage_complete"])

    def test_only_permitted_flow_without_a_supported_refutation_is_not_a_negative(self):
        extraction, review, document = self.fixtures()
        extraction["flows"][0]["permission"] = "allow"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")

    def test_policy_sentence_alone_cannot_prove_implementation_absence(self):
        extraction, review, document = self.excluded_claim()
        flow = extraction["flows"][0]
        policy_sentence = copy.deepcopy(flow["declaration"])
        flow["implementation"] = policy_sentence
        flow["delivery"]["citation"] = copy.deepcopy(policy_sentence)
        flow["refutation"]["citation"] = copy.deepcopy(policy_sentence)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")

    def test_overlapping_policy_excerpt_does_not_become_independent_boundary_evidence(self):
        extraction, review, document = self.excluded_claim()
        flow = extraction["flows"][0]
        overlap = {"segment_id": "s1", "quote": "attackers may not read the exact evaluation query"}
        flow["implementation"] = copy.deepcopy(overlap)
        flow["delivery"]["citation"] = copy.deepcopy(overlap)
        flow["refutation"]["citation"] = copy.deepcopy(overlap)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")

    def test_changing_text_views_cannot_make_one_policy_sentence_two_independent_sources(self):
        extraction, review, document = self.excluded_claim()
        policy = "External attackers may not read the exact evaluation query."
        document["segments"] = [{
            "id": "s1", "text": "External attackers may not read the exact\nUNRELATED COLUMN\nevaluation query.",
            "reading_order_text": policy,
        }]
        flow = extraction["flows"][0]
        flow["declaration"] = {"segment_id": "s1", "quote": "External attackers may not read the exact"}
        flow["policy_application"]["citation"] = copy.deepcopy(flow["declaration"])
        overlap = {"segment_id": "s1", "quote": "may not read the exact evaluation query"}
        flow["implementation"] = copy.deepcopy(overlap)
        flow["delivery"]["citation"] = copy.deepcopy(overlap)
        flow["refutation"]["citation"] = copy.deepcopy(overlap)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")

    def test_unlocated_out_of_scope_citation_abstains_instead_of_throwing(self):
        extraction, review, document = self.fixtures()
        extraction.update(applicability="out_of_scope", flows=[], applicability_citation={"segment_id": "s1", "quote": "An absent optimization title"})
        review.update(applicability="out_of_scope", flow_reviews=[])
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["reason"], "applicability_citation_unverified")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        self.assertTrue(result["citation_errors"])

    def test_refutation_without_its_own_grounded_citation_cannot_clear_the_claim(self):
        extraction, review, document = self.excluded_claim()
        extraction["flows"][0]["refutation"]["citation"] = None
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")

    def test_incomplete_document_does_not_erase_a_grounded_positive(self):
        extraction, review, document = self.fixtures()
        document["coverage"]["complete"] = False
        self.assertEqual(self.decide(extraction, review, document)["verdict"], "inconsistent")

    def test_behavioral_effect_does_not_gate_a_grounded_construction_finding(self):
        for effect in ("No clear ASR effect", "An effect was observed", "Behavioral effect has not been tested"):
            with self.subTest(effect=effect):
                extraction, review, document = self.fixtures()
                extraction["limitations"].append(effect)
                review["limitations"].append(effect)
                self.assertEqual(self.decide(extraction, review, document)["verdict"], "inconsistent")

    def test_query_form_conflicting_with_information_level_cannot_confirm(self):
        extraction, review, document = self.fixtures()
        extraction["flows"][0]["edge"]["query_form"] = "partial_query"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["reason"], "query_form_information_level_conflict")

    def test_legacy_v2_remains_explicitly_replayable_but_is_not_v3(self):
        extraction, review, document = self.fixtures()
        flow = extraction["flows"][0]
        legacy = {key: value for key, value in extraction.items() if key not in {"schema_version", "unresolved_questions"}}
        legacy["flows"] = [{key: flow[key] for key in ("edge", "permission", "observation", "declaration", "implementation", "explanation")}]
        legacy_review = {key: review[key] for key in ("applicability", "applicability_supported", "limitations")}
        legacy_review["flow_reviews"] = [{"index": 0, "supported": True, "reason": "Legacy fixture review"}]
        result = v2.decide_extraction(legacy, legacy_review, document, "legacy_fixture")
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["evidence"][0]["validation_mode"], "legacy_v2")
        with self.assertRaises(ValueError):
            self.decide(legacy, legacy_review, document)


if __name__ == "__main__":
    unittest.main()
