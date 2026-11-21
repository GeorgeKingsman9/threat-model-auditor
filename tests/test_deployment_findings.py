"""Synthetic offline tests for separate deployment/provenance findings.

Review votes test deterministic projection gates, not independent model accuracy.
No known paper, curated case, expected label, model, network or attack is used.
"""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import deployment_findings as deployment
import extraction_v4 as v4
from test_extraction_v4 import code_segment, digest, source_bundle


def cite(segment, quote):
    return {"segment_id": segment, "quote": quote}


class DeploymentFindingsTests(unittest.TestCase):
    def fixtures(self):
        text = (
            "The generated artifact transfers to a future victim task. "
            "The experimental constructor is conditioned on the supplied task record. "
            "The constructor is permitted to read public context."
        )
        paper = {
            "source": "synthetic-paper.txt", "sha256": digest(text),
            "media_type": "text/plain", "text": text,
            "segments": [{"id": "p1", "text": text}],
            "coverage": {"complete": True, "reason": "Entire synthetic paper."}, "links": [],
        }
        source = code_segment("builder.py", (
            "def construct(record, model):\n"
            '    task = record["future_task"]\n'
            '    prompt = {"task": task}\n'
            "    return model.generate(prompt)\n"
            "def supplied_tasks(dataset):\n"
            "    return [construct(row, model) for row in dataset]\n"
            "def public_task_route(public_tool):\n"
            "    return public_tool.read_task()\n"
            "def deploy(public_tool, model):\n"
            '    return construct({"future_task": public_task_route(public_tool)}, model)\n'
            "def task_independent(model):\n"
            '    return model.generate({"goal": "generic"})\n'
        ))
        document = v4.combine_inputs(paper, source_bundle([source]))
        receipt = cite(source["id"], "return model.generate(prompt)")
        dependency = cite(source["id"], 'task = record["future_task"]\n    prompt = {"task": task}')
        origin = cite(source["id"], "return [construct(row, model) for row in dataset]")
        finding = {
            "claim": "Transfer deployment requires a future task acquisition route.",
            "issue_type": "deployment_provenance",
            "paper_claim": {
                "description": "A future victim deployment is claimed.",
                "citation": cite("paper:p1", "transfers to a future victim task"),
            },
            "conditional_construction": {
                "description": "The released constructor sends the task-bound prompt.",
                "citations": [receipt],
            },
            "required_knowledge": {
                "description": "The constructor conditions the artifact on a supplied task.",
                "citations": [dependency],
            },
            "knowledge_provenance": {
                "status": "unresolved",
                "description": "The shown input comes from a dataset; its acquisition for a future victim is unestablished.",
                "citations": [origin],
            },
            "assessment": "supported_gap", "materiality": "material",
            "scope": "Static future-task-conditioned constructor and its advertised deployment.",
            "unresolved_questions": ["How does the deployer acquire the future task record?"],
        }
        review = {
            "index": 0, "paper_claim_supported": True,
            "construction_supported": True, "required_knowledge_supported": True,
            "provenance_supported": True, "scope_supported": True,
            "materiality_supported": True, "assessment": "supported_gap",
            "reason": "The conditional construction is grounded; deployment acquisition remains unresolved.",
        }
        return document, finding, review

    def project(self, document, finding, review, **kwargs):
        return deployment.project_deployment_findings(
            [finding], [review], document, input_binding=document["sha256"],
            review_input_binding=document["sha256"], **kwargs)

    def test_reviewed_deployment_gap_preserves_positive_construction(self):
        document, finding, review = self.fixtures()
        before = copy.deepcopy((document, finding, review))
        result = self.project(document, finding, review)
        row = result["findings"][0]
        self.assertEqual(row["assessment"], "supported_gap")
        self.assertTrue(row["positive_facts"]["conditional_construction"]["supported"])
        self.assertTrue(row["positive_facts"]["required_knowledge"]["supported"])
        self.assertEqual(row["knowledge_provenance"]["status"], "unresolved")
        self.assertFalse(row["knowledge_provenance"]["acquisition_path_established"])
        self.assertTrue(result["general_clean_blocked"])
        self.assertTrue(result["information_boundary_verdict_unchanged"])
        self.assertFalse(row["historical_execution_established"])
        self.assertEqual(row["observed_effect"], "not_assessed")
        self.assertEqual((document, finding, review), before)
        # The auxiliary vocabulary has no permission or strict truth value.
        self.assertNotIn("verdict", result)
        self.assertNotIn("has_confirmed_inconsistency", result)
        self.assertNotIn("permission", row)

    def test_exact_locators_are_bound_to_domains_and_revision(self):
        document, finding, review = self.fixtures()
        row = self.project(document, finding, review)["findings"][0]
        locator = row["positive_facts"]["conditional_construction"]["locators"][0]
        self.assertEqual(locator["source_kind"], "code")
        self.assertEqual(locator["path"], "builder.py")
        self.assertEqual(locator["line_start"], 4)
        self.assertEqual(locator["line_end"], 4)
        self.assertEqual(locator["document_sha256"], document["sha256"])
        self.assertEqual(locator["repository_revision"], document["repository"]["revision"])
        paper = row["positive_facts"]["paper_claim"]["locators"][0]
        self.assertEqual(paper["source_kind"], "paper")
        self.assertEqual(paper["paper_sha256"], document["paper_sha256"])

    def test_every_independent_review_axis_is_required_for_supported_gap(self):
        document, finding, review = self.fixtures()
        for key in ("paper_claim_supported", "construction_supported",
                    "required_knowledge_supported", "provenance_supported", "scope_supported"):
            with self.subTest(axis=key):
                changed = {**review, key: False}
                row = self.project(document, finding, changed)["findings"][0]
                self.assertEqual(row["assessment"], "uncertain")
        review["assessment"] = "resolved"
        self.assertEqual(self.project(document, finding, review)["findings"][0]["assessment"], "uncertain")

    def test_unestablished_route_is_never_resolved_by_a_missing_path(self):
        document, finding, review = self.fixtures()
        finding["assessment"] = review["assessment"] = "resolved"
        result = self.project(document, finding, review)
        self.assertEqual(result["findings"][0]["assessment"], "uncertain")
        self.assertTrue(result["general_clean_blocked"])
        self.assertEqual(result["findings"][0]["knowledge_provenance"]["status"], "unresolved")

    def test_missing_anchors_leave_uncertainty_and_preserve_grounded_receipt(self):
        document, finding, review = self.fixtures()
        finding["paper_claim"]["citation"] = None
        finding["knowledge_provenance"]["citations"] = []
        result = self.project(document, finding, review)
        row = result["findings"][0]
        self.assertEqual(row["assessment"], "uncertain")
        self.assertEqual(row["knowledge_provenance"]["status"], "uncertain")
        self.assertTrue(row["positive_facts"]["conditional_construction"]["supported"])
        self.assertTrue(result["general_clean_blocked"])

    def test_code_cannot_be_a_paper_deployment_claim(self):
        document, finding, review = self.fixtures()
        finding["paper_claim"]["citation"] = finding["required_knowledge"]["citations"][0]
        row = self.project(document, finding, review)["findings"][0]
        self.assertFalse(row["positive_facts"]["paper_claim"]["supported"])
        self.assertEqual(row["assessment"], "uncertain")
        self.assertTrue(any("must reference paper" in error for error in row["evidence_errors"]))

    def test_paper_disclosure_is_neither_source_proof_nor_acquisition_resolution(self):
        document, finding, review = self.fixtures()
        disclosure = cite("paper:p1", "constructor is conditioned on the supplied task record")
        finding["conditional_construction"]["citations"] = [disclosure]
        row = self.project(document, finding, review)["findings"][0]
        self.assertFalse(row["positive_facts"]["conditional_construction"]["supported"])
        self.assertEqual(row["assessment"], "uncertain")
        document, finding, review = self.fixtures()
        finding["assessment"] = review["assessment"] = "resolved"
        finding["knowledge_provenance"].update(status="established", citations=[disclosure])
        row = self.project(document, finding, review)["findings"][0]
        self.assertEqual(row["assessment"], "uncertain")
        self.assertFalse(row["knowledge_provenance"]["acquisition_path_established"])

    def test_paper_permission_does_not_establish_implemented_acquisition(self):
        document, finding, review = self.fixtures()
        finding["assessment"] = review["assessment"] = "resolved"
        finding["knowledge_provenance"].update(
            status="established", citations=[cite("paper:p1", "permitted to read public context")])
        row = self.project(document, finding, review)["findings"][0]
        self.assertEqual(row["assessment"], "uncertain")
        self.assertIn("positive resolution requires code evidence", " ".join(row["evidence_errors"]))

    def test_positive_route_or_non_requirement_can_resolve_precise_scope(self):
        for status, quote in (("established", "return public_tool.read_task()"),
                              ("not_required", 'return model.generate({"goal": "generic"})')):
            with self.subTest(status=status):
                document, finding, review = self.fixtures()
                finding["assessment"] = review["assessment"] = "resolved"
                source_id = finding["required_knowledge"]["citations"][0]["segment_id"]
                finding["knowledge_provenance"].update(status=status,
                    description="Positive route or non-use evidence for the reviewed exact branch.",
                    citations=[cite(source_id, quote)])
                if status == "established":
                    finding["knowledge_provenance"]["citations"].append(cite(source_id,
                        'return construct({"future_task": public_task_route(public_tool)}, model)'))
                else:
                    # This alternative deployment branch positively establishes
                    # non-use; the dependent constructor remains a separate fact.
                    independent = cite(source_id, quote)
                    finding["scope"] = "The explicitly task-independent deployment branch only."
                    finding["conditional_construction"] = {
                        "description": "The named branch sends a fixed generic goal.",
                        "citations": [independent],
                    }
                    finding["required_knowledge"] = {
                        "description": "The candidate task prerequisite is excluded on this branch.",
                        "citations": [copy.deepcopy(independent)],
                    }
                result = self.project(document, finding, review)
                row = result["findings"][0]
                self.assertEqual(row["assessment"], "resolved")
                self.assertEqual(row["knowledge_provenance"]["status"], status)
                self.assertFalse(result["general_clean_blocked"])
                self.assertFalse(result["general_clean_established"])
                self.assertFalse(row["historical_execution_established"])

    def test_invalid_extra_citation_cannot_be_dropped_to_resolve_finding(self):
        document, finding, review = self.fixtures()
        finding["conditional_construction"]["citations"].append(cite("missing", "invented"))
        row = self.project(document, finding, review)["findings"][0]
        self.assertFalse(row["positive_facts"]["conditional_construction"]["supported"])
        self.assertEqual(row["assessment"], "uncertain")
        self.assertEqual(len(row["positive_facts"]["conditional_construction"]["locators"]), 1)

    def test_auxiliary_gap_requires_unresolved_provenance_not_positive_acquisition(self):
        document, finding, review = self.fixtures()
        finding["knowledge_provenance"]["status"] = "established"
        row = self.project(document, finding, review)["findings"][0]
        self.assertEqual(row["assessment"], "uncertain")

    def test_material_issue_blocks_general_clean_only_when_in_audit_scope(self):
        document, finding, review = self.fixtures()
        result = self.project(document, finding, review, in_audit_scope=False)
        self.assertEqual(result["findings"][0]["assessment"], "supported_gap")
        self.assertFalse(result["general_clean_blocked"])
        finding["materiality"] = "limited"
        self.assertFalse(self.project(document, finding, review)["general_clean_blocked"])
        finding["materiality"] = "material"
        review["materiality_supported"] = False
        result = self.project(document, finding, review)
        self.assertEqual(result["findings"][0]["materiality"], "uncertain")
        self.assertFalse(result["general_clean_established"])

    def test_no_auxiliary_findings_never_establishes_general_paper_cleanliness(self):
        document, _, _ = self.fixtures()
        result = deployment.project_deployment_findings([], [], document,
            input_binding=document["sha256"], review_input_binding=document["sha256"])
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["coverage"], "named_findings_only")
        self.assertFalse(result["general_clean_established"])

    def test_review_coverage_binding_and_evidence_limits_fail_closed(self):
        document, finding, review = self.fixtures()
        for reviews in ([], [review, review], [{**review, "index": -1}]):
            with self.subTest(reviews=reviews), self.assertRaisesRegex(ValueError, "cover each"):
                deployment.project_deployment_findings([finding], reviews, document,
                    input_binding=document["sha256"], review_input_binding=document["sha256"])
        for bindings in (("wrong", document["sha256"]), (document["sha256"], "wrong")):
            with self.subTest(bindings=bindings), self.assertRaisesRegex(ValueError, "input binding"):
                deployment.project_deployment_findings([finding], [review], document,
                    input_binding=bindings[0], review_input_binding=bindings[1])
        changed = copy.deepcopy(document)
        changed["segments"][0]["text"] += " unbound edit"
        with self.assertRaisesRegex(ValueError, "input binding"):
            self.project(changed, finding, review)
        finding["required_knowledge"]["citations"] *= 9
        with self.assertRaisesRegex(ValueError, "eight-citation"):
            self.project(document, finding, review)

    def test_schema_rejects_hidden_verdicts_and_temporal_overclaims(self):
        document, finding, review = self.fixtures()
        for field, value in (("permission", "deny"), ("historical_execution_established", True),
                             ("observed_effect", "proven")):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "extra fields"):
                self.project(document, {**finding, field: value}, review)


if __name__ == "__main__":
    unittest.main()
