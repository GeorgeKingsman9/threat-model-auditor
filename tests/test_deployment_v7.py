"""Synthetic controls for the bounded V7 deployment-contract issue class.

Review votes test rule gates, not model accuracy. No remembered paper, author
artifact, adjudication label, network, inference or source execution is used.
"""

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import deployment_v7 as deployment
import extraction_v4 as v4
from test_extraction_v4 import code_segment, digest, source_bundle


def cite(segment, quote):
    return {"segment_id": segment, "quote": quote}


class DeploymentV7Tests(unittest.TestCase):
    def fixtures(self):
        text = (
            "A crafted artifact can be deployed to a future victim executing the same task. "
            "The adversary knows only publicly observed interaction messages. "
            "The operator supplies the benign task in a configuration. "
            "A separate diagnostic is explicitly limited to offline tasks supplied by the operator. "
            "We call the model interface black-box."
        )
        paper = {"source": "synthetic-paper.txt", "sha256": digest(text),
            "media_type": "text/plain", "text": text, "segments": [{"id": "p1", "text": text}],
            "coverage": {"complete": True, "reason": "Entire synthetic paper"}, "links": []}
        source = code_segment("constructor.py", (
            "def configured_attack(config, attacker, proxy):\n"
            '    task = config["victim_task"]\n'
            '    prompt = {"original_task": task}\n'
            "    payload = attacker.generate(prompt)\n"
            "    proxy.observe()\n"
            "    return payload\n"
            "def public_attack(public_tool, attacker):\n"
            "    task = public_tool.current_task()\n"
            '    return attacker.generate({"observed_task": task})\n'
            "def independent_attack(attacker):\n"
            '    return attacker.generate({"goal": "generic"})\n'
        ))
        document = v4.combine_inputs(paper, source_bundle([source]))
        src = source["id"]
        source_cite = cite(src, 'task = config["victim_task"]')
        requirement = cite(src, 'prompt = {"original_task": task}')
        receipt = cite(src, "payload = attacker.generate(prompt)")
        scenario = cite("paper:p1", "deployed to a future victim executing the same task")
        finding = {
            "claim": "Deployment depends on an operator-supplied future task.",
            "issue_type": "deployment_provenance",
            "paper_claim": {"description": "Deployment to a future same-task victim is claimed.", "citation": scenario},
            "conditional_construction": {"description": "The task-bound prompt is sent to the attacker generator.",
                                         "citations": [receipt]},
            "required_knowledge": {"description": "The task text forms the construction prompt.",
                                   "citations": [requirement]},
            "knowledge_provenance": {"status": "unresolved",
                "description": "The supplied operator task is used; acquisition for the claimed victim is unestablished.",
                "citations": [source_cite]},
            "assessment": "supported_gap", "materiality": "material",
            "scope": "Configured constructor and the claimed future same-task deployment.",
            "unresolved_questions": ["How is the corresponding future victim task acquired?"],
            "dependency_flow_index": 0,
            "source_boundary": {"basis": "allowed_observations",
                "description": "Knowledge is limited to publicly observed interactions.",
                "citations": [cite("paper:p1", "knows only publicly observed interaction messages")]},
            "actual_source": {"origin": "configuration_provided",
                "description": "The task comes directly from the operator configuration.", "citations": [source_cite]},
            "timing": {"status": "pre_observation",
                "description": "The configured task is consumed before the observation call.",
                "citations": [cite(src, "payload = attacker.generate(prompt)\n    proxy.observe()")]},
            "task_relation": {"status": "same_task_conditioning",
                "description": "The claimed deployment concerns the same task used to condition construction.",
                "citations": [scenario, source_cite]},
            "deployment_scope": {"status": "offline_to_online",
                "description": "The claim extends the constructed artifact to a future victim.", "citations": [scenario]},
        }
        review = {"index": 0, "paper_claim_supported": True, "construction_supported": True,
            "required_knowledge_supported": True, "provenance_supported": True,
            "scope_supported": True, "materiality_supported": True,
            "assessment": "supported_gap", "reason": "All positive facts are grounded; deployment acquisition is unestablished.",
            "source_boundary_supported": True, "actual_source_supported": True,
            "timing_supported": True, "task_relation_supported": True, "deployment_scope_supported": True}
        locators = [v4._locate(pointer, document, "code") for pointer in (source_cite, requirement, receipt)]
        flows = [{"source_validation": {"delivery_supported": True, "binding_supported": True,
                                         "code_path_locators": locators},
                  "flow_binding": {"recipient_role": "attacker_constructor", "attacker_delivery": "confirmed",
                                   "alignment_verified": True},
                  "binding_validation": {"recipient_supported": True}}]
        return document, finding, review, flows

    def project(self, document, finding, review, flows, **kwargs):
        return deployment.project_deployment_findings_v7([finding], [review], document, flows,
            input_binding=document["sha256"], review_input_binding=document["sha256"], **kwargs)

    def test_positive_is_typed_deployment_gap_without_deny_or_impossibility(self):
        args = self.fixtures()
        before = copy.deepcopy(args)
        result = self.project(*args)
        row = result["findings"][0]
        self.assertTrue(result["has_confirmed_gap"])
        self.assertEqual(row["claim_result"], "confirmed")
        self.assertEqual(row["issue_type"], "task_acquisition_deployment_gap")
        self.assertEqual(row["knowledge_provenance"]["status"], "unresolved")
        self.assertFalse(row["acquisition_impossible_established"])
        self.assertFalse(row["knowledge_prohibition_inferred"])
        self.assertFalse(row["historical_execution_established"])
        self.assertEqual(row["observed_effect"], "not_assessed")
        self.assertNotIn("permission", row)
        self.assertEqual(args, before)

    def test_real_v6_recipient_projection_supports_gap_without_deny(self):
        # Use the real V6 decision pipeline to produce its recipient/path proof,
        # rather than only a hand-assembled source_validation dictionary.
        import extraction_v6 as v6
        from test_extraction_v6 import ExtractionV6Tests
        paper, repository, _, extraction, independent_review = ExtractionV6Tests().fixtures()
        synthetic_document, finding, review, _ = self.fixtures()
        extra = next(part["text"] for part in synthetic_document["segments"] if part["source_kind"] == "paper")
        paper["segments"].append({"id": "p3", "text": extra})
        paper["text"] += "\n" + extra
        paper["sha256"] = digest(paper["text"])
        document = v6.combine_inputs(paper, repository)
        extraction["input_binding"] = independent_review["input_binding"] = document["sha256"]
        extraction["flows"][0]["permission"] = "unspecified"
        extraction["flows"][0]["policy_application"]["status"] = "uncertain"
        independent_review["flow_reviews"][0]["policy_application"] = "uncertain"
        strict = v6.decide_extraction(extraction, independent_review, document)
        self.assertEqual(strict["verdict"], "insufficient_evidence")
        mapping = {
            'task = config["victim_task"]': 'record = case["user_request"]',
            'prompt = {"original_task": task}': 'prompt = {"task": record}',
            'payload = attacker.generate(prompt)': 'reply = backend.generate(prompt)',
            'payload = attacker.generate(prompt)\n    proxy.observe()':
                'record = case["user_request"]\n    prompt = {"task": record}',
        }
        def remap(value):
            if isinstance(value, dict):
                if set(value) == {"segment_id", "quote"}:
                    value["segment_id"] = "paper:p3" if value["segment_id"].startswith("paper:") else "repo:generator.py:L1-L6"
                    value["quote"] = mapping.get(value["quote"], value["quote"])
                else:
                    for child in value.values(): remap(child)
            elif isinstance(value, list):
                for child in value: remap(child)
        remap(finding)
        finding["timing"]["description"] = "The supplied record enters the constructor before its model request."
        result = self.project(document, finding, review, strict["evidence"])
        self.assertTrue(result["has_confirmed_gap"])
        self.assertEqual(strict["evidence"][0]["claim_result"], "unresolved")

    def test_every_legacy_and_new_review_axis_is_required(self):
        for key in ("paper_claim_supported", "construction_supported", "required_knowledge_supported",
                    "provenance_supported", "scope_supported", "materiality_supported", "source_boundary_supported",
                    "actual_source_supported", "timing_supported", "task_relation_supported", "deployment_scope_supported"):
            with self.subTest(axis=key):
                document, finding, review, flows = self.fixtures()
                review[key] = False
                result = self.project(document, finding, review, flows)
                self.assertFalse(result["has_confirmed_gap"])
                self.assertEqual(result["findings"][0]["claim_result"], "unresolved")

    def test_black_box_label_alone_is_not_a_knowledge_boundary(self):
        document, finding, review, flows = self.fixtures()
        finding["source_boundary"].update(basis="black_box_label_only",
            citations=[cite("paper:p1", "model interface black-box")])
        row = self.project(document, finding, review, flows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertIn("black-box label", " ".join(row["evidence_errors"]))

    def test_unresolved_or_explicitly_assumed_origin_cannot_create_gap(self):
        for origin in ("unknown", "other", "explicit_assumption", "observed_trace", "public_observation"):
            with self.subTest(origin=origin):
                document, finding, review, flows = self.fixtures()
                finding["actual_source"]["origin"] = origin
                self.assertFalse(self.project(document, finding, review, flows)["has_confirmed_gap"])

    def test_unknown_timing_task_relation_or_online_scope_remains_unresolved(self):
        for field, value in (("timing", "unresolved"), ("task_relation", "unknown"),
                             ("task_relation", "different_task"), ("deployment_scope", "uncertain"),
                             ("deployment_scope", "offline_only")):
            with self.subTest(field=field, value=value):
                document, finding, review, flows = self.fixtures()
                finding[field]["status"] = value
                row = self.project(document, finding, review, flows)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")

    def test_post_observation_same_task_is_not_a_deployment_violation(self):
        document, finding, review, flows = self.fixtures()
        finding["timing"]["status"] = "post_observation"
        self.assertEqual(self.project(document, finding, review, flows)["findings"][0]["claim_result"], "unresolved")
        # The distinct claim concerning a future task is separately reviewed.
        finding["task_relation"]["status"] = "future_task_transfer"
        self.assertTrue(self.project(document, finding, review, flows)["has_confirmed_gap"])
        finding["deployment_scope"]["status"] = "online"
        self.assertFalse(self.project(document, finding, review, flows)["has_confirmed_gap"])

    def test_explicit_offline_control_refutes_only_the_named_deployment_gap(self):
        document, finding, review, flows = self.fixtures()
        finding["assessment"] = review["assessment"] = "resolved"
        finding["deployment_scope"].update(status="offline_only",
            description="The examined diagnostic is explicitly limited to supplied offline tasks.",
            citations=[cite("paper:p1", "diagnostic is explicitly limited to offline tasks supplied by the operator")])
        finding["paper_claim"]["citation"] = finding["deployment_scope"]["citations"][0]
        result = self.project(document, finding, review, flows)
        self.assertEqual(result["findings"][0]["claim_result"], "refuted")
        self.assertFalse(result["has_confirmed_gap"])
        self.assertFalse(result["blocks_negative"])
        self.assertFalse(result["general_clean_established"])
        # A scope refutation does not fabricate an implemented acquisition route.
        self.assertEqual(result["findings"][0]["knowledge_provenance"]["status"], "unresolved")

    def test_positive_observation_route_resolves_matching_online_branch(self):
        document, finding, review, flows = self.fixtures()
        sid = finding["actual_source"]["citations"][0]["segment_id"]
        origin = cite(sid, "task = public_tool.current_task()")
        receipt = cite(sid, 'return attacker.generate({"observed_task": task})')
        finding["assessment"] = review["assessment"] = "resolved"
        finding["actual_source"].update(origin="public_observation", citations=[origin])
        finding["conditional_construction"]["citations"] = [receipt]
        finding["required_knowledge"]["citations"] = [receipt]
        finding["knowledge_provenance"].update(status="established", citations=[origin, receipt])
        finding["timing"].update(status="post_observation", citations=[origin, receipt])
        finding["task_relation"]["citations"][1] = origin
        flows[0]["source_validation"]["code_path_locators"] = [v4._locate(c, document, "code") for c in (origin, receipt)]
        result = self.project(document, finding, review, flows)
        row = result["findings"][0]
        self.assertEqual(row["claim_result"], "refuted")
        self.assertTrue(row["knowledge_provenance"]["acquisition_path_established"])
        self.assertFalse(result["blocks_negative"])

    def test_resolution_on_an_unrelated_route_cannot_refute_dependency(self):
        document, finding, review, flows = self.fixtures()
        finding["assessment"] = review["assessment"] = "resolved"
        sid = finding["actual_source"]["citations"][0]["segment_id"]
        finding["knowledge_provenance"].update(status="established",
            citations=[cite(sid, "task = public_tool.current_task()")])
        row = self.project(document, finding, review, flows)["findings"][0]
        self.assertEqual(row["claim_result"], "unresolved")
        self.assertIn("resolution is not linked", " ".join(row["evidence_errors"]))

    def test_missing_or_invalid_extra_quote_preserves_other_positive_facts(self):
        for field in ("conditional_construction", "required_knowledge", "knowledge_provenance",
                      "source_boundary", "actual_source", "timing", "task_relation", "deployment_scope"):
            with self.subTest(field=field):
                document, finding, review, flows = self.fixtures()
                finding[field]["citations"].append(cite("missing", "invented quotation"))
                row = self.project(document, finding, review, flows)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")
                self.assertTrue(row["evidence_errors"])
                if field != "conditional_construction":
                    self.assertTrue(row["positive_facts"]["conditional_construction"]["supported"])

    def test_all_source_domains_are_enforced(self):
        for field, pointer in (("source_boundary", "code"), ("actual_source", "paper"),
                               ("timing", "paper"), ("deployment_scope", "code")):
            with self.subTest(field=field):
                document, finding, review, flows = self.fixtures()
                replacement = (finding["actual_source"]["citations"][0] if pointer == "code"
                               else finding["deployment_scope"]["citations"][0])
                finding[field]["citations"] = [copy.deepcopy(replacement)]
                row = self.project(document, finding, review, flows)["findings"][0]
                self.assertEqual(row["claim_result"], "unresolved")

    def test_paper_only_task_relation_is_not_instance_mapping(self):
        document, finding, review, flows = self.fixtures()
        finding["task_relation"]["citations"] = finding["task_relation"]["citations"][:1]
        self.assertFalse(self.project(document, finding, review, flows)["has_confirmed_gap"])

    def test_dependency_needs_matching_grounded_attacker_receipt(self):
        for damage in ("missing", "wrong_index", "delivery", "binding", "evaluator", "other_span", "other_document",
                       "alignment_unverified", "recipient_unverified", "binding_unverified", "tampered_locator"):
            with self.subTest(damage=damage):
                document, finding, review, flows = self.fixtures()
                if damage == "missing": flows = []
                elif damage == "wrong_index": finding["dependency_flow_index"] = 1
                elif damage == "delivery": flows[0]["source_validation"]["delivery_supported"] = False
                elif damage == "binding": flows[0]["flow_binding"]["attacker_delivery"] = "unresolved"
                elif damage == "evaluator": flows[0]["flow_binding"]["recipient_role"] = "evaluator"
                elif damage == "alignment_unverified": flows[0]["flow_binding"]["alignment_verified"] = False
                elif damage == "recipient_unverified": flows[0]["binding_validation"]["recipient_supported"] = False
                elif damage == "binding_unverified": flows[0]["source_validation"]["binding_supported"] = False
                elif damage == "tampered_locator":
                    flows[0]["source_validation"]["code_path_locators"][0]["file_sha256"] = "changed"
                elif damage == "other_span":
                    sid = finding["actual_source"]["citations"][0]["segment_id"]
                    flows[0]["source_validation"]["code_path_locators"] = [v4._locate(
                        cite(sid, 'return attacker.generate({"goal": "generic"})'), document, "code")]
                else:
                    for loc in flows[0]["source_validation"]["code_path_locators"]:
                        loc["document_sha256"] = "different"
                self.assertFalse(self.project(document, finding, review, flows)["has_confirmed_gap"])

    def test_limited_materiality_and_conflicting_assessment_cannot_confirm(self):
        for field in ("materiality", "assessment"):
            document, finding, review, flows = self.fixtures()
            if field == "materiality": finding[field] = "limited"
            else: review[field] = "resolved"
            self.assertFalse(self.project(document, finding, review, flows)["has_confirmed_gap"])

    def test_empty_findings_never_certify_a_clean_paper(self):
        document, _, _, _ = self.fixtures()
        result = deployment.project_deployment_findings_v7([], [], document, [],
            input_binding=document["sha256"], review_input_binding=document["sha256"])
        self.assertFalse(result["has_confirmed_gap"])
        self.assertFalse(result["blocks_negative"])
        self.assertFalse(result["general_clean_established"])

    def test_outside_scope_preserves_facts_without_confirming(self):
        result = self.project(*self.fixtures(), in_audit_scope=False)
        self.assertFalse(result["has_confirmed_gap"])
        self.assertFalse(result["blocks_negative"])
        self.assertTrue(result["findings"][0]["positive_facts"]["conditional_construction"]["supported"])

    def test_binding_shape_review_and_limits_fail_closed(self):
        document, finding, review, flows = self.fixtures()
        for reviews in ([], [review, review], [{**review, "index": -1}]):
            with self.subTest(reviews=reviews), self.assertRaisesRegex(ValueError, "cover every"):
                deployment.project_deployment_findings_v7([finding], reviews, document, flows,
                    input_binding=document["sha256"], review_input_binding=document["sha256"])
        with self.assertRaisesRegex(ValueError, "input binding"):
            deployment.project_deployment_findings_v7([finding], [review], document, flows,
                input_binding="changed", review_input_binding=document["sha256"])
        with self.assertRaisesRegex(ValueError, "four"):
            deployment.project_deployment_findings_v7([finding] * 5, [{**review, "index": i} for i in range(5)],
                document, flows, input_binding=document["sha256"], review_input_binding=document["sha256"])
        finding["actual_source"]["citations"] *= 7
        with self.assertRaisesRegex(ValueError, "six-citation"):
            self.project(document, finding, review, flows)


if __name__ == "__main__":
    unittest.main()
