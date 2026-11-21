"""Offline integration of auxiliary deployment findings with the V5 core.

Synthetic evidence and review votes verify gates and projection plumbing. They
do not measure model accuracy and use no real papers, expected labels or network.
"""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v5 as v5
import extraction_v6 as v6
from findings import project_result
import test_extraction_v4 as source_fixtures
import test_extraction_v6 as v6_fixtures


def cite(segment, quote):
    return {"segment_id": segment, "quote": quote}


class V6DeploymentIntegrationTests(unittest.TestCase):
    def fixtures(self, permission="allow", with_gap=True):
        paper, repository, _, extraction, review = v6_fixtures.ExtractionV6Tests().fixtures()
        grant = "The direct constructor is expressly allowed to receive the target request text."
        deployment = "The task-conditioned artifact transfers to a future victim task."
        paper["segments"] += [{"id": "p3", "text": grant}, {"id": "p4", "text": deployment}]
        paper["text"] = "\n".join(part["text"] for part in paper["segments"])
        paper["sha256"] = source_fixtures.digest(paper["text"])
        document = v6.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        extraction["channel_assessments"], review["channel_reviews"] = [], []
        for candidate in document["model_repository"]["input_channels"]["candidates"]:
            extraction["channel_assessments"].append({
                "candidate_id": candidate["id"], "channel_kind": candidate["channel_kind"],
                "status": "represented", "flow_index": 0,
                "citations": [copy.deepcopy(candidate["source_citation"]), copy.deepcopy(candidate["citation"])],
                "reason": "The direct constructor flow covers this exact task argument.",
            })
            review["channel_reviews"].append({
                "candidate_id": candidate["id"], "mapping_supported": True,
                "exclusion_supported": False, "reason": "The same origin and generation boundary are bound.",
            })
        flow = extraction["flows"][0]
        if permission == "allow":
            declaration = cite("paper:p3", "direct constructor is expressly allowed to receive the target request text")
            flow["permission"] = "allow"
            flow["declaration"] = copy.deepcopy(declaration)
            flow["refutation"].update(basis="explicit_permission", citation=copy.deepcopy(declaration),
                                      reason="A positive grant covers this direct constructor.")
            flow["scope_resolution"].update(basis="specific_rule", specific_rule=copy.deepcopy(declaration),
                                            override_dimension="knowledge", reason="The specific direct-constructor grant applies.")
            review["flow_reviews"][0]["refutation"] = "explicit_permission"
        if with_gap:
            construction = copy.deepcopy(flow["delivery"]["citation"])
            dependency = copy.deepcopy(flow["code_path"][0]["citation"])
            extraction["deployment_findings"] = [{
                "claim": "The released conditional constructor leaves future task acquisition unestablished.",
                "issue_type": "deployment_provenance",
                "paper_claim": {"description": "Deployment to a future victim task is advertised.",
                                "citation": cite("paper:p4", "artifact transfers to a future victim task")},
                "conditional_construction": {"description": "The constructor receives a task-bound generation prompt.",
                                             "citations": [construction]},
                "required_knowledge": {"description": "Construction uses the supplied case's exact request.",
                                       "citations": [dependency]},
                "knowledge_provenance": {"status": "unresolved",
                    "description": "The task comes from a supplied case; future victim acquisition is unestablished.",
                    "citations": [copy.deepcopy(dependency)]},
                "assessment": "supported_gap", "materiality": "material",
                "scope": "The advertised future deployment of this task-conditioned constructor.",
                "unresolved_questions": ["How is the future victim task acquired?"],
            }]
            review["deployment_reviews"] = [{
                "index": 0, "paper_claim_supported": True, "construction_supported": True,
                "required_knowledge_supported": True, "provenance_supported": True,
                "scope_supported": True, "materiality_supported": True,
                "assessment": "supported_gap", "reason": "Conditional receipt is proved; deployment acquisition is unresolved.",
            }]
        return document, extraction, review

    def test_material_gap_blocks_scoped_negative_without_changing_refuted_boundary(self):
        document, extraction, review = self.fixtures(with_gap=False)
        baseline = project_result(v6.decide_extraction(extraction, review, document))
        self.assertTrue(baseline["channel_coverage"]["complete"])
        self.assertEqual(baseline["verdict"], "consistent_within_scope")
        self.assertIs(baseline["inconsistency"], False)
        self.assertEqual(baseline["evidence"][0]["claim_result"], "refuted")
        document, extraction, review = self.fixtures()
        result = project_result(v6.decide_extraction(extraction, review, document))
        self.assertTrue(result["channel_coverage"]["complete"])
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIsNone(result["inconsistency"])
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["claim_result_counts"], baseline["claim_result_counts"])
        self.assertEqual(result["findings"], [])
        auxiliary = result["deployment_assessment"]
        self.assertTrue(auxiliary["general_clean_blocked"])
        self.assertEqual(auxiliary["findings"][0]["assessment"], "supported_gap")
        self.assertEqual(auxiliary["findings"][0]["knowledge_provenance"]["status"], "unresolved")

    def test_independent_boundary_violation_survives_unresolved_deployment(self):
        document, extraction, review = self.fixtures(permission="deny")
        result = project_result(v6.decide_extraction(extraction, review, document))
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertIs(result["inconsistency"], True)
        self.assertEqual(result["evidence"][0]["claim_result"], "confirmed")
        self.assertEqual(len(result["findings"]), 1)
        self.assertTrue(result["deployment_assessment"]["general_clean_blocked"])
        self.assertEqual(result["deployment_assessment"]["findings"][0]["assessment"], "supported_gap")

    def test_provenance_unknown_does_not_create_a_knowledge_prohibition(self):
        document, extraction, review = self.fixtures()
        flow, vote = extraction["flows"][0], review["flow_reviews"][0]
        flow["permission"], flow["declaration"] = "unspecified", None
        flow["refutation"].update(basis="none", citation=None, reason="No permission conclusion is claimed.")
        flow["policy_application"]["status"] = "uncertain"
        vote.update(refutation="none", policy_application="uncertain")
        result = project_result(v6.decide_extraction(extraction, review, document))
        self.assertEqual(extraction["flows"][0]["permission"], "unspecified")
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIsNone(result["inconsistency"])
        self.assertEqual(result["evidence"][0]["claim_result"], "unresolved")
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["deployment_assessment"]["findings"][0]["assessment"], "supported_gap")
        self.assertTrue(result["deployment_assessment"]["findings"][0]["positive_facts"]["conditional_construction"]["supported"])

    def test_auxiliary_review_cannot_be_omitted_or_reused(self):
        document, extraction, review = self.fixtures()
        for votes in ([], review["deployment_reviews"] * 2):
            with self.subTest(votes=len(votes)), self.assertRaisesRegex(ValueError, "cover each"):
                v6.decide_extraction(extraction, {**review, "deployment_reviews": votes}, document)
        altered = copy.deepcopy(review)
        altered["deployment_reviews"][0]["provenance_supported"] = False
        result = v6.decide_extraction(extraction, altered, document)
        self.assertEqual(result["deployment_assessment"]["findings"][0]["assessment"], "uncertain")
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["verdict"], "insufficient_evidence")

    def test_v5_delegation_does_not_mutate_inputs_or_shared_schemas(self):
        document, extraction, review = self.fixtures()
        before = copy.deepcopy((document, extraction, review, v5.EXTRACTION_SCHEMA, v5.REVIEW_SCHEMA))
        v6.decide_extraction(extraction, review, document)
        self.assertEqual((document, extraction, review, v5.EXTRACTION_SCHEMA, v5.REVIEW_SCHEMA), before)
        self.assertEqual(v5.EXTRACTION_SCHEMA["properties"]["schema_version"]["enum"], [5])
        self.assertNotIn("deployment_findings", v5.EXTRACTION_SCHEMA["properties"])
        self.assertNotIn("deployment_reviews", v5.REVIEW_SCHEMA["properties"])
        payload = v6.model_content(document)
        self.assertEqual(payload["input_binding"], document["sha256"])
        self.assertNotIn("proposal", payload)
        self.assertNotIn("deployment_findings", payload)


if __name__ == "__main__":
    unittest.main()
