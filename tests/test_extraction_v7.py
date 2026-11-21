"""Three-category aggregation over real offline engine-generated evidence rows.

Synthetic papers and review votes check rule plumbing, not detection accuracy.
No labels, known papers, network, inference or author code execution are used.
"""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v6 as v6
import extraction_v7 as v7
from test_extraction_v4 import digest, source_bundle
import test_construction_contracts as construction_toy


class ExtractionV7Tests(unittest.TestCase):
    def fixtures(self, uncertain_policy=True):
        document, finding, vote, _, extraction, review = construction_toy.ConstructionContractsTests().fixtures(engine=v6)
        if uncertain_policy:
            extraction["flows"][0]["permission"] = "unspecified"
            extraction["flows"][0]["policy_application"]["status"] = "uncertain"
            review["flow_reviews"][0]["policy_application"] = "uncertain"
        extraction["schema_version"] = review["schema_version"] = 7
        extraction["construction_findings"] = [finding]
        review["construction_reviews"] = [vote]
        citation = copy.deepcopy(finding["contract"]["citations"][0])
        extraction["category_assessments"] = [
            {"category": category, "status": "candidates" if index < 2 else "none_identified",
             "finding_indices": [0] if index < 2 else [], "citations": [citation],
             "reason": "Synthetic category coverage evidence, not a real-paper completeness claim."}
            for index, category in enumerate(v7.CATEGORIES)
        ]
        review["category_reviews"] = [{"category": category, "assessment_supported": True,
                                       "reason": "The fixture reviews the named candidate family."}
                                      for category in v7.CATEGORIES]
        return document, extraction, review

    def legacy_projection(self, extraction, review):
        x, r = copy.deepcopy(extraction), copy.deepcopy(review)
        x["schema_version"] = r["schema_version"] = 6
        for item, keys in ((x, ("construction_findings", "category_assessments")),
                           (r, ("construction_reviews", "category_reviews"))):
            for key in keys:
                item.pop(key)
        x["deployment_findings"] = []
        r["deployment_reviews"] = []
        return x, r

    def test_policy_uncertain_construction_mismatch_confirms_typed_paper_finding(self):
        document, extraction, review = self.fixtures()
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["schema_version"], 7)
        self.assertEqual(result["knowledge_boundary_verdict"], "insufficient_evidence")
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["confirmed_issue_types"], ["construction_contract_mismatch"])
        self.assertTrue(result["has_confirmed_inconsistency"])
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")
        self.assertEqual(result["evidence"][1]["claim_result"], "confirmed")

    def test_v6_output_and_input_records_do_not_change_when_v7_adds_a_track(self):
        document, extraction, review = self.fixtures()
        x, r = self.legacy_projection(extraction, review)
        before = copy.deepcopy((document, extraction, review, x, r))
        old_result = v6.decide_extraction(x, r, document)
        v7.decide_extraction(extraction, review, document)
        self.assertEqual(v6.decide_extraction(x, r, document), old_result)
        self.assertEqual((document, extraction, review, x, r), before)
        self.assertEqual(old_result["schema_version"], 6)

    def test_strict_positive_remains_its_own_issue_type(self):
        document, extraction, review = self.fixtures(uncertain_policy=False)
        extraction["construction_findings"] = []
        review["construction_reviews"] = []
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["knowledge_boundary_verdict"], "inconsistent")
        self.assertEqual(result["confirmed_issue_types"], ["knowledge_boundary_violation"])
        self.assertEqual(result["verdict"], "inconsistent")

    def test_local_mismatch_survives_missing_unrelated_category_and_channel_coverage(self):
        document, extraction, review = self.fixtures()
        extraction["category_assessments"] = extraction["category_assessments"][:1]
        review["category_reviews"] = []
        result = v7.decide_extraction(extraction, review, document)
        self.assertFalse(result["category_coverage"]["complete"])
        self.assertFalse(result["channel_coverage"]["complete"])
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["confirmed_issue_types"], ["construction_contract_mismatch"])

    def test_empty_new_tracks_and_unclosed_obligations_are_not_negative(self):
        document, extraction, review = self.fixtures()
        extraction["construction_findings"] = []
        review["construction_reviews"] = []
        extraction["category_assessments"] = []
        review["category_reviews"] = []
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["confirmed_issue_types"])
        self.assertFalse(result["category_coverage"]["complete"])

    def test_uncertain_domain_never_promotes_a_new_track(self):
        document, extraction, review = self.fixtures()
        extraction["applicability"] = review["applicability"] = "uncertain"
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["confirmed_issue_types"])
        self.assertFalse(result["construction_assessment"]["in_audit_scope"])
        self.assertEqual(result["construction_assessment"]["findings"][0]["claim_result"], "unresolved")

    def test_no_mismatch_is_inferred_from_a_missing_or_disputed_contract(self):
        document, extraction, review = self.fixtures()
        review["construction_reviews"][0]["contract_supported"] = False
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["construction_assessment"]["has_confirmed_mismatch"])

    def test_evaluator_cannot_borrow_a_construction_positive(self):
        document, extraction, review = self.fixtures()
        binding = extraction["flows"][0]["binding"]
        binding["recipient_role"] = extraction["flows"][0]["edge"]["role"] = "evaluator"
        binding["attacker_delivery"] = "unresolved"
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["construction_assessment"]["has_confirmed_mismatch"])

    def test_deployment_gap_confirms_its_own_type_without_inventing_deny(self):
        document, extraction, review = self.fixtures()
        text = ("The artifact is deployed online to a future victim executing this recorded task. "
                "Construction knowledge is restricted to observed public interaction messages. "
                "The operator supplies that recorded task before observation begins.")
        parts = [{**part, "id": part["id"].removeprefix("paper:")}
                 for part in document["segments"] if part["source_kind"] == "paper"]
        for part in parts:
            part.pop("source_kind")
        parts.append({"id": "p5", "text": text})
        paper_text = "\n".join(part["text"] for part in parts)
        paper = {"source": document["source"], "sha256": digest(paper_text), "media_type": "text/plain",
                 "text": paper_text, "segments": parts, "coverage": document["paper_coverage"], "links": []}
        repository = source_bundle([part for part in document["segments"] if part["source_kind"] == "code"])
        document = v6.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        extraction["construction_findings"] = []
        review["construction_reviews"] = []
        sid = next(part["id"] for part in document["segments"] if part.get("path") == "generator.py")
        def paper_cite(quote): return {"segment_id": "paper:p5", "quote": quote}
        def code_cite(quote): return {"segment_id": sid, "quote": quote}
        scenario = paper_cite("deployed online to a future victim executing this recorded task")
        source = code_cite('record = case["user_request"]')
        receipt = code_cite("reply = backend.generate(prompt)")
        prompt = code_cite('prompt = {"task": record}')
        finding = {
            "claim": "The online scenario relies on a task supplied before the allowed observation.",
            "issue_type": "deployment_provenance", "dependency_flow_index": 0,
            "paper_claim": {"description": "The artifact is claimed to deploy to a future recorded-task victim.", "citation": scenario},
            "conditional_construction": {"description": "The generator receives the task-bearing prompt.", "citations": [receipt]},
            "required_knowledge": {"description": "The recorded task is inserted into that prompt.", "citations": [prompt]},
            "knowledge_provenance": {"status": "unresolved", "description": "The task is supplied in the case record; the online acquisition is unestablished.", "citations": [source]},
            "assessment": "supported_gap", "materiality": "material", "scope": "Recorded-task construction and its stated future online deployment.",
            "unresolved_questions": ["How does the deploying actor acquire the future task?"],
            "source_boundary": {"basis": "allowed_observations", "description": "Construction knowledge is restricted to observed messages.", "citations": [paper_cite("restricted to observed public interaction messages")]},
            "actual_source": {"origin": "operator_provided", "description": "The constructor reads the externally supplied task record.", "citations": [source]},
            "timing": {"status": "pre_observation", "description": "The supplied task is consumed before the observation phase stated by the scenario.", "citations": [source, prompt]},
            "task_relation": {"status": "same_task_conditioning", "description": "The claimed future victim executes the same recorded task used to construct the artifact.", "citations": [scenario, source]},
            "deployment_scope": {"status": "offline_to_online", "description": "The claim connects supplied-record construction to online deployment.", "citations": [scenario]},
        }
        vote = {"index": 0, "assessment": "supported_gap", "reason": "The material task dependency is grounded, but acquisition for the specified online victim is unestablished.",
                **{key: True for key in ("paper_claim_supported", "construction_supported", "required_knowledge_supported",
                    "provenance_supported", "scope_supported", "materiality_supported", "source_boundary_supported",
                    "actual_source_supported", "timing_supported", "task_relation_supported", "deployment_scope_supported")}}
        extraction["deployment_findings"] = [finding]
        review["deployment_reviews"] = [vote]
        extraction["category_assessments"][1].update(status="none_identified", finding_indices=[])
        extraction["category_assessments"][2].update(status="candidates", finding_indices=[0], citations=[scenario])
        result = v7.decide_extraction(extraction, review, document)
        self.assertEqual(result["knowledge_boundary_verdict"], "insufficient_evidence")
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["confirmed_issue_types"], ["task_acquisition_deployment_gap"])
        self.assertEqual(extraction["flows"][0]["permission"], "unspecified")
        self.assertFalse(result["deployment_assessment"]["findings"][0]["knowledge_prohibition_inferred"])


if __name__ == "__main__":
    unittest.main()
