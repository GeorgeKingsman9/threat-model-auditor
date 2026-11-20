"""Recipient and instance boundaries for opt-in V5 bindings; no model calls."""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scope_review import assess_claim


class FlowBindingTests(unittest.TestCase):
    def case(self, role="attacker_constructor"):
        return {
            "schema_version": 3,
            "claim": "The named receiving edge violates an attacker information prohibition.",
            "issue_type": "information_boundary",
            "target": {"role": role, "query_form": "full_query"},
            "assessment": {
                "information_level": "exact_query",
                "policy_application": {"policy_kind": "attacker_knowledge_constraint", "status": "applicable", "reference": "policy locator", "reason": "The specified prohibition applies to the named edge."},
                "delivery": {"status": "confirmed", "evidence_kind": "static_bound_path", "task_relation": "same_evaluated_instance", "reference": "boundary locator", "reason": "A verified receiving boundary."},
                "refutation": {"basis": "none", "reference": "", "reason": "No separate refutation proposed."},
            },
            "flow_binding": {
                "semantics_version": 1, "recipient_role": role,
                "observation_target": "matched_edge", "attacker_delivery": "confirmed",
                "instance_requirement": "same_evaluated_instance", "instance_relation": "same",
                "alignment_verified": True, "exclusion_verified": False,
            },
        }

    def assess(self, case=None, permissions=None, observations=None):
        return assess_claim(self.case() if case is None else case,
                            "inconsistent", "forbidden_flow_confirmed",
                            {"deny"} if permissions is None else permissions,
                            {"present"} if observations is None else observations)

    def assert_state(self, case, state, reason=None, **kwargs):
        row = self.assess(case, **kwargs)
        self.assertEqual(row["claim_result"], state)
        if reason:
            self.assertEqual(row["reason"], reason)
        return row

    def test_evaluator_present_is_neither_attacker_present_nor_attacker_absent(self):
        case = self.case("evaluator")
        case["assessment"]["delivery"]["status"] = "evaluator_only"
        case["flow_binding"]["attacker_delivery"] = "unresolved"
        row = self.assert_state(case, "unresolved", "bound_attacker_delivery_not_established")
        self.assertEqual(row["flow_binding"]["attacker_delivery"], "unresolved")
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        row = self.assert_state(case, "refuted", "bound_claim_refuted_evaluator_policy_inapplicable")
        self.assertEqual(row["flow_binding"]["attacker_delivery"], "unresolved")

    def test_present_evaluator_does_not_conflict_with_independent_attacker_exclusion(self):
        case = self.case("evaluator")
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        case["assessment"]["delivery"]["status"] = "evaluator_only"
        case["flow_binding"].update(attacker_delivery="excluded", exclusion_verified=True)
        self.assert_state(case, "refuted", "bound_claim_refuted_evaluator_policy_inapplicable")

    def test_fixed_attacker_target_is_not_refuted_by_an_evaluator_observation(self):
        case = self.case()
        case["flow_binding"].update(recipient_role="evaluator", attacker_delivery="unresolved")
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        case["assessment"]["delivery"]["status"] = "evaluator_only"
        self.assert_state(case, "unresolved", "flow_recipient_target_not_aligned")

    def test_attacker_present_and_attacker_excluded_still_conflict(self):
        for role in ("attacker_constructor", "attacker_optimizer"):
            case = self.case(role)
            case["flow_binding"].update(attacker_delivery="excluded", exclusion_verified=True)
            self.assert_state(case, "unresolved", "bound_attacker_exclusion_conflicts_with_present")
        case = self.case()
        self.assert_state(case, "unresolved", "bound_attacker_confirmation_conflicts_with_absent", observations={"absent"})
        case["flow_binding"].update(attacker_delivery="excluded", exclusion_verified=True)
        self.assert_state(case, "unresolved", "bound_attacker_delivery_states_conflict", observations={"possible"})

    def test_unknown_recipient_or_unverified_alignment_cannot_produce_a_negative(self):
        for role in ("unknown", "attacker_constructor"):
            case = self.case(role)
            case["flow_binding"].update(attacker_delivery="excluded", exclusion_verified=True)
            case["assessment"]["delivery"]["status"] = "excluded"
            if role != "unknown":
                case["flow_binding"]["alignment_verified"] = False
            self.assert_state(case, "unresolved", observations={"absent"})

    def test_explicit_applicable_permission_refutes_without_actual_delivery(self):
        for observations in ({"possible"}, set(), {"absent"}):
            case = self.case()
            case["assessment"]["delivery"].update(status="unresolved", evidence_kind="possible_path", reference="")
            case["flow_binding"].update(attacker_delivery="unresolved", instance_relation="unknown")
            self.assert_state(case, "refuted", "bound_claim_refuted_explicit_permission",
                              permissions={"allow"}, observations=observations)
        for status in ("uncertain", "not_applicable"):
            case["assessment"]["policy_application"]["status"] = status
            self.assert_state(case, "unresolved", permissions={"allow"}, observations={"possible"})

    def test_same_instance_requirement_needs_independent_identity_evidence(self):
        for relation in ("unknown", "different"):
            case = self.case()
            case["flow_binding"]["instance_relation"] = relation
            self.assert_state(case, "unresolved", "bound_evaluated_instance_alignment_not_established")
        self.assert_state(self.case(), "confirmed", "bound_scoped_forbidden_delivery_confirmed")

    def test_training_label_does_not_prove_different_instance_or_authorization(self):
        case = self.case()
        case["assessment"]["delivery"]["task_relation"] = "training_instance"
        case["flow_binding"]["instance_relation"] = "unknown"
        self.assert_state(case, "unresolved")
        case["flow_binding"].update(instance_requirement="any_instance")
        self.assert_state(case, "confirmed")

    def test_broad_prohibition_covers_training_and_other_instances(self):
        for level in ("task_category", "exact_query"):
            for relation in ("same", "different", "unknown"):
                with self.subTest(level=level, relation=relation):
                    case = self.case()
                    if level == "task_category":
                        del case["target"]["query_form"]
                    case["assessment"]["information_level"] = level
                    case["assessment"]["delivery"]["task_relation"] = "training_instance"
                    case["flow_binding"].update(instance_requirement="any_instance", instance_relation=relation)
                    self.assert_state(case, "confirmed")

    def test_different_instance_refutation_requires_verified_identity_and_narrow_policy(self):
        case = self.case()
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        case["assessment"]["refutation"].update(basis="different_instance", reference="instance mapping")
        case["flow_binding"]["instance_relation"] = "different"
        self.assert_state(case, "refuted", "bound_claim_refuted_different_instance")
        case["flow_binding"]["instance_relation"] = "unknown"
        self.assert_state(case, "unresolved")
        case["flow_binding"].update(instance_requirement="any_instance", instance_relation="different")
        self.assert_state(case, "unresolved")

    def test_exclusion_requires_positive_verified_boundary_evidence(self):
        case = self.case()
        case["flow_binding"].update(attacker_delivery="excluded", exclusion_verified=True)
        case["assessment"]["delivery"]["status"] = "excluded"
        self.assert_state(case, "refuted", "bound_claim_refuted_verified_exclusion", observations={"absent"})
        case["flow_binding"]["exclusion_verified"] = False
        self.assert_state(case, "unresolved", observations={"absent"})
        case["flow_binding"]["exclusion_verified"] = True
        case["assessment"]["delivery"]["evidence_kind"] = "document_presence"
        self.assert_state(case, "unresolved", observations={"absent"})

    def test_conflicts_remain_local_to_the_verified_edge(self):
        self.assert_state(self.case(), "unresolved", "bound_conflicting_policy", permissions={"allow", "deny"})
        self.assert_state(self.case(), "unresolved", "bound_conflicting_observations", observations={"present", "absent"})

    def test_binding_shape_errors_are_rejected(self):
        for field, value in (("semantics_version", True), ("semantics_version", 2),
                             ("recipient_role", "generator"), ("observation_target", "evaluator"),
                             ("attacker_delivery", "evaluator_only"), ("instance_requirement", "train"),
                             ("instance_relation", "training"), ("alignment_verified", 1), ("exclusion_verified", "true")):
            with self.subTest(field=field, value=value):
                case = self.case()
                case["flow_binding"][field] = value
                with self.assertRaises(ValueError):
                    self.assess(case)
        case = self.case()
        case["flow_binding"]["binding_verified"] = True
        with self.assertRaises(ValueError):
            self.assess(case)

    def test_legacy_v3_record_keeps_exact_output_without_binding(self):
        case = self.case()
        del case["flow_binding"]
        expected = {
            "validation_mode": "scope_review_v3", "claim": case["claim"],
            "issue_type": case["issue_type"], "assessment": case["assessment"],
            "claim_result": "confirmed", "verdict": "inconsistent",
            "reason": "scoped_forbidden_delivery_confirmed",
        }
        self.assertEqual(self.assess(case), expected)
        case["assessment"]["delivery"]["status"] = "evaluator_only"
        expected.update(claim_result="unresolved", verdict="insufficient_evidence",
                        reason="delivery_exclusion_conflicts_with_present")
        self.assertEqual(self.assess(case), expected)
        case["assessment"]["delivery"].update(status="unresolved", evidence_kind="possible_path", reference="")
        case["assessment"]["refutation"].update(basis="explicit_permission", reference="authorization locator")
        expected.update(reason="refutation_not_supported_by_scoped_evidence")
        self.assertEqual(self.assess(case, permissions={"allow"}, observations={"possible"}), expected)

    def test_binding_output_is_opt_in_and_does_not_mutate_input(self):
        case = self.case()
        before = copy.deepcopy(case)
        row = self.assess(case)
        self.assertEqual(case, before)
        self.assertEqual(row["validation_mode"], "flow_binding_v1")
        self.assertEqual(row["flow_binding"], case["flow_binding"])
        self.assertEqual(assess_claim({"schema_version": 2}, "inconsistent", "original", {"deny"}, {"present"}),
                         {"verdict": "inconsistent", "reason": "original", "claim_result": "confirmed", "validation_mode": "legacy_v2"})


if __name__ == "__main__":
    unittest.main()
