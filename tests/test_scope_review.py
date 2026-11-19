"""Adjudicate scoped allegations with fixtures; no paper gold or model calls."""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scope_review import assess_claim


class ScopeReviewTests(unittest.TestCase):
    def case(self):
        return {
            "schema_version": 3,
            "claim": "The construction input receives the exact evaluated query despite a matching prohibition.",
            "issue_type": "information_boundary",
            "assessment": {
                "information_level": "exact_query",
                "policy_application": {"policy_kind": "attacker_knowledge_constraint", "status": "applicable", "reference": "policy scope locator", "reason": "This prohibition covers the construction role and arm."},
                "delivery": {"status": "confirmed", "evidence_kind": "saved_request", "task_relation": "same_evaluated_instance", "reference": "input boundary locator", "reason": "The saved request contains the evaluated query."},
                "refutation": {"basis": "none", "reference": "", "reason": "No supported exclusion is proposed."},
            },
        }

    def assess(self, case=None, verdict="inconsistent", reason="forbidden_flow_confirmed", permissions=None, observations=None):
        return assess_claim(
            self.case() if case is None else case, verdict, reason,
            {"deny"} if permissions is None else permissions,
            {"present"} if observations is None else observations,
        )

    def assert_unresolved(self, result):
        self.assertEqual(result["claim_result"], "unresolved")
        self.assertEqual(result["verdict"], "insufficient_evidence")

    def refutation(self, basis):
        case = self.case()
        case["assessment"]["refutation"] = {"basis": basis, "reference": "refutation locator", "reason": "Evidence rules out the enumerated allegation."}
        return case

    def test_v2_replay_preserves_the_original_verdict_and_reason(self):
        for version in (None, 2):
            for verdict, claim_result in (("inconsistent", "confirmed"), ("consistent_within_scope", "refuted"), ("insufficient_evidence", "unresolved")):
                with self.subTest(version=version, verdict=verdict):
                    case = {} if version is None else {"schema_version": version}
                    result = self.assess(case, verdict=verdict, reason="legacy reason")
                    self.assertEqual(result["verdict"], verdict)
                    self.assertEqual(result["reason"], "legacy reason")
                    self.assertEqual(result["claim_result"], claim_result)
                    self.assertEqual(result["validation_mode"], "legacy_v2")

    def test_same_scope_prohibition_and_boundary_delivery_confirm_the_claim(self):
        result = self.assess()
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["claim_result"], "confirmed")
        self.assertEqual(result["validation_mode"], "scope_review_v3")

    def test_shape_errors_raise_instead_of_becoming_results(self):
        for missing in ("claim", "issue_type", "assessment"):
            with self.subTest(missing=missing):
                case = self.case()
                del case[missing]
                with self.assertRaises(ValueError):
                    self.assess(case)
        for invalid_version in (True, 1, 4, "3"):
            with self.subTest(version=invalid_version):
                case = self.case()
                case["schema_version"] = invalid_version
                with self.assertRaises(ValueError):
                    self.assess(case)
        for section, key, invalid in (("policy_application", "status", "probably"), ("policy_application", "policy_kind", "normative"), ("delivery", "task_relation", "whatever"), ("delivery", "evidence_kind", "filename"), ("refutation", "basis", "not_found")):
            with self.subTest(section=section, field=key):
                case = self.case()
                case["assessment"][section][key] = invalid
                with self.assertRaises(ValueError):
                    self.assess(case)
        for field, invalid in (("issue_type", "evaluation_confound"),):
            case = self.case()
            case[field] = invalid
            with self.assertRaises(ValueError):
                self.assess(case)
        case = self.case()
        case["assessment"]["information_level"] = "future_query"
        with self.assertRaises(ValueError):
            self.assess(case)

    def test_missing_scope_or_delivery_reference_abstains(self):
        for section in ("policy_application", "delivery"):
            with self.subTest(section=section):
                case = self.case()
                case["assessment"][section]["reference"] = "  "
                self.assert_unresolved(self.assess(case))

    def test_generic_external_deny_does_not_automatically_apply_to_a_disclosed_stronger_baseline(self):
        for status in ("uncertain", "not_applicable"):
            with self.subTest(status=status):
                case = self.case()
                case["assessment"]["policy_application"].update(status=status, reason="The evaluated arm is a disclosed offline stronger baseline, not the generic external role.")
                self.assert_unresolved(self.assess(case))

    def test_document_or_unbound_path_presence_is_not_generator_delivery(self):
        for kind in ("document_presence", "possible_path", "not_applicable"):
            with self.subTest(kind=kind):
                case = self.case()
                case["assessment"]["delivery"]["evidence_kind"] = kind
                self.assert_unresolved(self.assess(case))
        for status in ("excluded", "unresolved"):
            with self.subTest(status=status):
                case = self.case()
                case["assessment"]["delivery"]["status"] = status
                self.assert_unresolved(self.assess(case))

    def test_topic_or_unaligned_information_does_not_prove_exact_query_access(self):
        for relation in ("topic_only", "different_instance", "unknown"):
            with self.subTest(relation=relation):
                case = self.case()
                case["assessment"]["delivery"]["task_relation"] = relation
                self.assert_unresolved(self.assess(case))

    def test_training_is_not_globally_permitted_when_a_prohibition_explicitly_applies(self):
        case = self.case()
        case["claim"] = "The training constructor receives query information explicitly forbidden in this training condition."
        case["assessment"]["delivery"]["task_relation"] = "training_instance"
        self.assertEqual(self.assess(case)["claim_result"], "confirmed")
        case["claim"] = "The constructor knows an exact future test query."
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        self.assert_unresolved(self.assess(case))

    def test_categorical_information_can_violate_a_rule_that_really_prohibits_categories(self):
        case = self.case()
        case["assessment"]["information_level"] = "task_category"
        case["assessment"]["delivery"]["task_relation"] = "topic_only"
        self.assertEqual(self.assess(case)["claim_result"], "confirmed")

    def test_confirming_a_claim_requires_actual_matching_deny_and_present(self):
        for permissions, observations in ((set(), {"present"}), ({"allow"}, {"present"}), ({"deny"}, set()), ({"deny"}, {"possible"}), ({"allow", "deny"}, {"present"}), ({"deny"}, {"present", "absent"})):
            with self.subTest(permissions=permissions, observations=observations):
                self.assert_unresolved(self.assess(permissions=permissions, observations=observations))
        self.assert_unresolved(self.assess(verdict="insufficient_evidence", reason="no matching observation"))

    def test_explicit_permission_refutes_only_with_confirmed_matching_delivery(self):
        case = self.refutation("explicit_permission")
        result = self.assess(case, verdict="consistent_within_scope", permissions={"allow"})
        self.assertEqual(result["claim_result"], "refuted")
        self.assertEqual(result["verdict"], "consistent_within_scope")
        for permissions, observations in (({"deny"}, {"present"}), ({"allow", "deny"}, {"present"}), ({"allow"}, set()), ({"allow"}, {"possible"})):
            with self.subTest(permissions=permissions, observations=observations):
                self.assert_unresolved(self.assess(case, verdict="consistent_within_scope", permissions=permissions, observations=observations))
        case["assessment"]["delivery"]["reference"] = ""
        self.assert_unresolved(self.assess(case, verdict="consistent_within_scope", permissions={"allow"}))

    def test_confirmed_source_training_authorization_refutes_a_generic_prohibition_claim(self):
        case = self.refutation("explicit_permission")
        case["assessment"]["delivery"].update(task_relation="training_instance", reason="An explicitly authorized source-training subset reaches construction.")
        result = self.assess(case, verdict="consistent_within_scope", permissions={"allow"})
        self.assertEqual(result["claim_result"], "refuted")
        self.assertEqual(result["reason"], "claim_refuted_explicit_permission")

    def test_different_instance_refutation_requires_positive_disambiguation_evidence(self):
        case = self.refutation("different_instance")
        case["assessment"]["policy_application"]["status"] = "not_applicable"
        case["assessment"]["delivery"]["task_relation"] = "training_instance"
        result = self.assess(case, verdict="insufficient_evidence", observations={"possible"})
        self.assertEqual(result["claim_result"], "refuted")
        self.assert_unresolved(self.assess(case))
        case["assessment"]["delivery"]["task_relation"] = "unknown"
        self.assert_unresolved(self.assess(case, observations={"possible"}))

    def test_explicit_boundary_exclusion_can_refute_without_whole_paper_coverage(self):
        case = self.refutation("excluded_delivery")
        case["assessment"]["delivery"].update(status="excluded", evidence_kind="static_bound_path")
        result = self.assess(case, verdict="consistent_within_scope", observations={"absent"})
        self.assertEqual(result["claim_result"], "refuted")
        self.assert_unresolved(self.assess(case))
        case["assessment"]["delivery"]["evidence_kind"] = "document_presence"
        self.assert_unresolved(self.assess(case, observations={"absent"}))

    def test_other_experimental_problem_needs_supported_type_refutation(self):
        case = self.refutation("different_issue_type")
        case["issue_type"] = "task_integrity"
        case["assessment"]["policy_application"].update(policy_kind="protocol_requirement", status="not_applicable")
        result = self.assess(case, verdict="insufficient_evidence", observations=set())
        self.assertEqual(result["claim_result"], "refuted")
        case["issue_type"] = "information_boundary"
        self.assert_unresolved(self.assess(case, observations=set()))

    def test_protocol_or_metric_definition_can_refute_the_limited_inference_with_uncertain_policy_scope(self):
        for issue_type in ("task_integrity", "experimental_protocol"):
            with self.subTest(issue_type=issue_type):
                case = self.refutation("different_issue_type")
                case["claim"] = "Does a utility metric change or harness-forced action alone establish delivery of a forbidden private query?"
                case["issue_type"] = issue_type
                case["assessment"]["policy_application"].update(policy_kind="protocol_requirement", status="uncertain", reference="")
                case["assessment"]["delivery"].update(status="unresolved", evidence_kind="not_applicable", reference="")
                case["assessment"]["refutation"].update(reference="Positive metric/protocol definition showing it concerns task outcomes or action scheduling.", reason="The definition does not assert a source-to-recipient private-query flow; this refutes only that limited logical inference.")
                result = self.assess(case, verdict="insufficient_evidence", permissions=set(), observations=set())
                self.assertEqual(result["claim_result"], "refuted")
                self.assertEqual(result["reason"], "claim_refuted_different_issue_type")
                # The program adjudicates this named inference; it certifies
                # neither the claimed quantitative bug nor the whole paper.
                self.assertNotIn("coverage_complete", result)
                case["assessment"]["policy_application"]["policy_kind"] = "attacker_knowledge_constraint"
                self.assert_unresolved(self.assess(case, verdict="insufficient_evidence", permissions=set(), observations=set()))

    def test_successful_security_goal_violation_is_not_a_paper_knowledge_boundary_violation(self):
        case = self.case()
        self.assertEqual(self.assess(case)["claim_result"], "confirmed")
        # Only the policy's normative type changes; identical deny/present and
        # input evidence must not turn attack success into a paper inconsistency.
        case["assessment"]["policy_application"]["policy_kind"] = "victim_security_goal"
        result = self.assess(case)
        self.assert_unresolved(result)
        self.assertEqual(result["reason"], "policy_is_not_attacker_knowledge_constraint")
        case["assessment"]["policy_application"]["policy_kind"] = "protocol_requirement"
        self.assert_unresolved(self.assess(case))

    def test_security_outcome_can_refute_the_wrong_information_boundary_allegation(self):
        case = self.refutation("different_issue_type")
        case["issue_type"] = "security_outcome"
        case["assessment"]["policy_application"].update(policy_kind="victim_security_goal", status="not_applicable")
        result = self.assess(case)
        self.assertEqual(result["claim_result"], "refuted")
        self.assertEqual(result["reason"], "claim_refuted_different_issue_type")

    def test_evaluator_only_delivery_refutes_the_generator_claim_with_boundary_evidence(self):
        case = self.refutation("excluded_delivery")
        case["assessment"]["delivery"]["status"] = "evaluator_only"
        result = self.assess(case, verdict="insufficient_evidence", observations=set())
        self.assertEqual(result["claim_result"], "refuted")
        self.assert_unresolved(self.assess(case))

    def test_an_asserted_refutation_without_evidence_never_overrides_a_claim(self):
        case = self.refutation("explicit_permission")
        case["assessment"]["refutation"]["reference"] = ""
        self.assert_unresolved(self.assess(case, verdict="consistent_within_scope", permissions={"allow"}))

    def test_any_affirmative_judgment_with_missing_evidence_keeps_a_refutation_unresolved(self):
        for section in ("policy_application", "delivery"):
            with self.subTest(section=section):
                case = self.refutation("different_issue_type")
                case["issue_type"] = "security_outcome"
                case["assessment"]["policy_application"].update(policy_kind="victim_security_goal", status="not_applicable")
                case["assessment"][section]["reference"] = ""
                self.assert_unresolved(self.assess(case))

    def test_no_flows_or_only_permitted_flows_do_not_automatically_refute_a_claim(self):
        case = self.case()
        self.assert_unresolved(self.assess(case, verdict="consistent_within_scope", permissions={"allow"}))
        case["assessment"]["policy_application"].update(status="uncertain", reference="")
        case["assessment"]["delivery"].update(status="unresolved", evidence_kind="not_applicable", task_relation="unknown", reference="")
        self.assert_unresolved(self.assess(case, verdict="insufficient_evidence", permissions=set(), observations=set()))

    def test_causal_impact_fields_do_not_change_boundary_verdicts(self):
        for impact in ("not_tested", "no_clear_effect", "effect_supported"):
            with self.subTest(impact=impact):
                case = self.case()
                case["behavioral_impact"] = impact
                self.assertEqual(self.assess(case)["claim_result"], "confirmed")

    def test_query_form_and_information_level_must_agree(self):
        for form, level in (("full_query", "partial_query"), ("partial_query", "exact_query"), ("full_query", "task_category")):
            with self.subTest(query_form=form, information_level=level):
                case = self.case()
                case["target"] = {"query_form": form}
                case["assessment"]["information_level"] = level
                result = self.assess(case)
                self.assert_unresolved(result)
                self.assertEqual(result["reason"], "query_form_information_level_conflict")
        for form, level in (("full_query", "exact_query"), ("partial_query", "partial_query")):
            case = self.case()
            case["target"] = {"query_form": form}
            case["assessment"]["information_level"] = level
            self.assertEqual(self.assess(case)["claim_result"], "confirmed")

    def test_query_type_conflict_cannot_be_used_as_a_refutation(self):
        case = self.refutation("explicit_permission")
        case["target"] = {"query_form": "partial_query"}
        result = self.assess(case, verdict="consistent_within_scope", permissions={"allow"})
        self.assert_unresolved(result)
        self.assertEqual(result["reason"], "query_form_information_level_conflict")

    def test_assessment_does_not_mutate_input(self):
        case = self.case()
        before = copy.deepcopy(case)
        self.assess(case)
        self.assertEqual(case, before)


if __name__ == "__main__":
    unittest.main()
