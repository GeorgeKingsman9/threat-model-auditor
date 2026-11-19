"""Gate information-flow verdicts on policy scope and delivery evidence.

Version 2 records remain reproducible legacy replays. Version 3 records explicitly
adjudicate an enumerated claim; a refuted claim is not a whole-paper clean bill.
References are grounded upstream (for model extraction) or curated by an auditor.
This module checks their presence and the consistency of the structured evidence;
it does not pretend that a nonempty reference independently proves its semantics.
"""


VERDICTS = {"inconsistent", "consistent_within_scope", "insufficient_evidence"}
ISSUE_TYPES = {"information_boundary", "experimental_protocol", "task_integrity", "acquisition_gap", "security_outcome"}
INFORMATION_LEVELS = {"exact_query", "partial_query", "task_category", "document_content", "runtime_trace", "user_identity", "resource_metadata", "other"}
POLICY_KINDS = {"attacker_knowledge_constraint", "victim_security_goal", "protocol_requirement", "unspecified"}
POLICY_STATES = {"applicable", "not_applicable", "uncertain"}
DELIVERY_STATES = {"confirmed", "excluded", "evaluator_only", "unresolved"}
EVIDENCE_KINDS = {
    "paper_procedure", "static_bound_path", "saved_request", "runtime",
    "document_presence", "possible_path", "not_applicable",
}
BOUNDARY_EVIDENCE = {"paper_procedure", "static_bound_path", "saved_request", "runtime"}
TASK_RELATIONS = {
    "same_evaluated_instance", "training_instance", "topic_only", "different_instance", "unknown",
}
REFUTATION_BASES = {"none", "explicit_permission", "different_instance", "excluded_delivery", "different_issue_type"}


def _object(value, fields, name):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(f"{name} must contain exactly {', '.join(fields)}")
    return value


def _text(record, field, name, allow_empty=False):
    value = record[field]
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        qualifier = "a string" if allow_empty else "a nonempty string"
        raise ValueError(f"{name}.{field} must be {qualifier}")
    return value


def _enum(record, field, allowed, name):
    value = _text(record, field, name)
    if value not in allowed:
        raise ValueError(f"{name}.{field} is invalid: {value}")
    return value


def _validate_assessment(case):
    for field in ("claim", "issue_type"):
        if field not in case:
            raise ValueError(f"v3 case requires {field}")
        _text(case, field, "case")
    _enum(case, "issue_type", ISSUE_TYPES, "case")
    assessment = _object(case.get("assessment"), ("information_level", "policy_application", "delivery", "refutation"), "assessment")
    _enum(assessment, "information_level", INFORMATION_LEVELS, "assessment")
    policy = _object(assessment["policy_application"], ("policy_kind", "status", "reference", "reason"), "policy_application")
    delivery = _object(assessment["delivery"], ("status", "evidence_kind", "task_relation", "reference", "reason"), "delivery")
    refutation = _object(assessment["refutation"], ("basis", "reference", "reason"), "refutation")
    _enum(policy, "policy_kind", POLICY_KINDS, "policy_application")
    _enum(policy, "status", POLICY_STATES, "policy_application")
    _enum(delivery, "status", DELIVERY_STATES, "delivery")
    _enum(delivery, "evidence_kind", EVIDENCE_KINDS, "delivery")
    _enum(delivery, "task_relation", TASK_RELATIONS, "delivery")
    _enum(refutation, "basis", REFUTATION_BASES, "refutation")
    for name, record in (("policy_application", policy), ("delivery", delivery), ("refutation", refutation)):
        _text(record, "reference", name, allow_empty=True)
        _text(record, "reason", name)
    return assessment, policy, delivery, refutation


def assess_claim(case, verdict, reason, permissions, observations):
    """Return a compatible verdict plus confirmed/refuted/unresolved claim status.

    Required v3 input fields are ``schema_version=3``, ``claim``, ``issue_type``
    and ``assessment`` (see ``_validate_assessment``). Missing/invalid structure
    raises ValueError. Well-formed but absent, conflicting or inapplicable
    evidence produces insufficient_evidence rather than a confirmation.

    A different-instance refutation requires that no matching present observation
    contradict it. An explicit-permission refutation requires an actual matching
    present observation and evidence at the receiving input boundary.
    """
    if not isinstance(case, dict):
        raise ValueError("case must be an object")
    version = case.get("schema_version", 2)
    if type(version) is not int or version not in {2, 3}:
        raise ValueError("schema_version must be 2 or 3")
    if verdict not in VERDICTS or not isinstance(reason, str) or not reason.strip():
        raise ValueError("a valid base verdict and nonempty reason are required")
    if version == 2:
        return {
            "verdict": verdict,
            "reason": reason,
            "claim_result": {"inconsistent": "confirmed", "consistent_within_scope": "refuted", "insufficient_evidence": "unresolved"}[verdict],
            "validation_mode": "legacy_v2",
        }

    assessment, policy, delivery, refutation = _validate_assessment(case)
    if not isinstance(permissions, (set, frozenset)) or not permissions <= {"allow", "deny"}:
        raise ValueError("permissions must be a set of allow/deny values")
    if not isinstance(observations, (set, frozenset)) or not observations <= {"present", "absent", "possible"}:
        raise ValueError("observations must be a set of present/absent/possible values")
    base = {
        "validation_mode": "scope_review_v3", "claim": case["claim"],
        "issue_type": case["issue_type"], "assessment": assessment,
    }

    def result(state, why):
        return {
            **base, "claim_result": state,
            "verdict": {"confirmed": "inconsistent", "refuted": "consistent_within_scope", "unresolved": "insufficient_evidence"}[state],
            "reason": why,
        }

    target = case.get("target")
    if isinstance(target, dict) and "query_form" in target:
        expected_level = {"full_query": "exact_query", "partial_query": "partial_query"}.get(target["query_form"])
        if expected_level is None:
            raise ValueError("target.query_form must be full_query or partial_query when specified")
        if assessment["information_level"] != expected_level:
            return result("unresolved", "query_form_information_level_conflict")

    if len(permissions) > 1:
        return result("unresolved", "conflicting_policy")
    if {"present", "absent"} <= observations:
        return result("unresolved", "conflicting_observations")
    if delivery["status"] in {"excluded", "evaluator_only"} and "present" in observations:
        return result("unresolved", "delivery_exclusion_conflicts_with_present")
    if delivery["status"] == "confirmed" and "absent" in observations:
        return result("unresolved", "delivery_confirmation_conflicts_with_absent")

    policy_cited = bool(policy["reference"].strip())
    delivery_cited = bool(delivery["reference"].strip())
    boundary_evidence = delivery["evidence_kind"] in BOUNDARY_EVIDENCE
    confirmed_delivery = delivery["status"] == "confirmed" and delivery_cited and boundary_evidence
    if policy["status"] != "uncertain" and not policy_cited:
        return result("unresolved", "policy_scope_evidence_missing")
    if delivery["status"] != "unresolved" and not delivery_cited:
        return result("unresolved", "delivery_boundary_evidence_missing")
    if delivery["status"] != "unresolved" and not boundary_evidence:
        return result("unresolved", "delivery_to_input_boundary_not_established")
    basis = refutation["basis"]
    if basis != "none":
        if not refutation["reference"].strip():
            return result("unresolved", "refutation_evidence_missing")
        if basis == "explicit_permission":
            if (permissions == {"allow"} and "present" in observations
                    and policy["policy_kind"] == "attacker_knowledge_constraint"
                    and policy["status"] == "applicable" and policy_cited and confirmed_delivery):
                return result("refuted", "claim_refuted_explicit_permission")
        elif basis == "different_instance":
            if (delivery["task_relation"] in {"training_instance", "topic_only", "different_instance"}
                    and delivery["status"] in {"confirmed", "excluded", "evaluator_only"}
                    and delivery_cited and boundary_evidence and "present" not in observations
                    and policy["status"] == "not_applicable" and policy_cited):
                return result("refuted", "claim_refuted_different_instance")
        elif basis == "excluded_delivery":
            if (delivery["status"] in {"excluded", "evaluator_only"} and delivery_cited and boundary_evidence
                    and "present" not in observations):
                return result("refuted", "claim_refuted_excluded_delivery")
        elif basis == "different_issue_type":
            if (case["issue_type"] != "information_boundary"
                    and policy["policy_kind"] in {"victim_security_goal", "protocol_requirement"}):
                return result("refuted", "claim_refuted_different_issue_type")
        return result("unresolved", "refutation_not_supported_by_scoped_evidence")

    if case["issue_type"] != "information_boundary":
        return result("unresolved", "information_boundary_issue_not_established")
    if policy["policy_kind"] != "attacker_knowledge_constraint":
        return result("unresolved", "policy_is_not_attacker_knowledge_constraint")
    if policy["status"] != "applicable":
        return result("unresolved", "policy_scope_not_established")
    if not policy_cited:
        return result("unresolved", "policy_scope_evidence_missing")
    if delivery["task_relation"] in {"different_instance", "unknown"}:
        return result("unresolved", "evaluated_instance_alignment_not_established")
    if (delivery["task_relation"] == "topic_only"
            and assessment["information_level"] in {"exact_query", "partial_query"}):
        return result("unresolved", "topic_information_is_not_instance_query")
    if not confirmed_delivery:
        return result("unresolved", "delivery_to_input_boundary_not_established")
    if verdict == "inconsistent" and permissions == {"deny"} and "present" in observations:
        return result("confirmed", "scoped_forbidden_delivery_confirmed")
    return result("unresolved", "base_rule_does_not_confirm_forbidden_delivery")
