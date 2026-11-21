"""Compare a stated construction contract with a grounded implementation source.

This is a separate issue type from a forbidden information flow. It neither
creates ``deny`` from a recipe nor treats an omitted argument, filename or
missing generator as a mismatch. Model-proposed semantic comparisons must be
independently reviewed, grounded in original paper/code, and linked to an
already checked delivery path. A static finding establishes neither a historical
author run nor an effect on attack success.
"""

import copy

from extraction import STRING, obj, validate_shape
import extraction_v3 as v3
import extraction_v4 as v4


SCHEMA_VERSION = 1
MAX_FINDINGS = 4
MAX_CITATIONS = 6
CITATIONS = {"type": "array", "items": v3.CITATION, "maxItems": MAX_CITATIONS}
CITED_FACT = obj({"description": STRING, "citations": CITATIONS})
ASSESSMENT = v3.enum("mismatch", "aligned", "uncertain")
INCOMPATIBILITIES = frozenset({"incompatible_source", "incompatible_generation",
                             "incompatible_input_granularity"})

CONSTRUCTION_SCHEMA = obj({
    "claim": STRING,
    "flow_index": {"type": "integer"},
    "instance_requirement": v3.enum("same_evaluated_instance", "any_instance", "unspecified"),
    "contract": CITED_FACT,
    "implemented_source": CITED_FACT,
    "semantic_mapping": obj({"description": STRING,
                             "paper_citations": CITATIONS,
                             "code_citations": CITATIONS}),
    "comparison": obj({
        "kind": v3.enum("incompatible_source", "incompatible_generation",
                        "incompatible_input_granularity", "aligned", "unresolved"),
        "description": STRING,
    }),
    "exceptions": obj({"status": v3.enum("none_applicable", "applicable", "unresolved"),
                       "description": STRING, "citations": CITATIONS}),
    "scope": STRING,
    "assessment": ASSESSMENT,
})
CONSTRUCTION_REVIEW_SCHEMA = obj({
    "index": {"type": "integer"},
    **{key: {"type": "boolean"} for key in (
        "contract_supported", "implementation_supported", "semantic_mapping_supported",
        "comparison_supported", "scope_supported", "exceptions_supported")},
    "assessment": ASSESSMENT,
    "reason": STRING,
})


def _fact(description, citations, document, vote, kind, name, errors):
    """All proposed pointers must locate; a valid subset cannot hide a bad one."""
    if len(citations) > MAX_CITATIONS:
        raise ValueError("construction evidence exceeds the six-citation limit")
    valid = bool(description.strip() and citations)
    if not valid:
        errors.append(name + ": missing affirmative description or citation")
    locators = []
    for citation in citations:
        try:
            locators.append(v4._locate(citation, document, kind))
        except ValueError as error:
            errors.append(name + ": " + str(error))
            valid = False
    return {"description": description, "supported": bool(valid and vote),
            "locators": locators}


def _overlaps(left, right):
    return (left.get("segment_id") == right.get("segment_id")
            and left.get("text_view", "primary") == right.get("text_view", "primary")
            and left["start"] < right["end"] and right["start"] < left["end"])


def _verify_path_locator(locator, document):
    """Reject stale/tampered flow locations before using their overlap as a link."""
    if not isinstance(locator, dict) or locator.get("source_kind") != "code":
        raise ValueError("linked construction path must contain code locators")
    if locator.get("document_sha256") != document["sha256"]:
        raise ValueError("linked construction path belongs to a different input")
    segment = next((part for part in document["segments"]
                    if part["id"] == locator.get("segment_id")), None)
    if segment is None:
        raise ValueError("linked construction path segment is missing")
    view = locator.get("text_view", "primary")
    if view not in {"primary", "reading_order"}:
        raise ValueError("linked construction path text view is unknown")
    text = segment.get("reading_order_text") if view == "reading_order" else segment.get("text")
    start, end = locator.get("start"), locator.get("end")
    if (not isinstance(text, str) or type(start) is not int or type(end) is not int
            or not 0 <= start < end <= len(text)):
        raise ValueError("linked construction path offsets are invalid")
    located = v4._locate({"segment_id": segment["id"], "quote": text[start:end]}, document, "code")
    if located != locator:
        raise ValueError("linked construction path locator differs from original source")
    return located


def _flow_link(index, flow_rows, implemented_locators, document, errors):
    if type(index) is not int or not 0 <= index < len(flow_rows):
        errors.append("construction_flow_index_invalid")
        return False, []
    row = flow_rows[index]
    validation = row.get("source_validation", {}) if isinstance(row, dict) else {}
    if not isinstance(validation, dict) or validation.get("delivery_supported") is not True:
        errors.append("construction_delivery_not_established")
        return False, []
    binding, diagnostics = row.get("flow_binding", {}), row.get("binding_validation", {})
    if (not isinstance(binding, dict) or not isinstance(diagnostics, dict)
            or binding.get("recipient_role") not in {"attacker_constructor", "attacker_optimizer"}
            or binding.get("attacker_delivery") != "confirmed"
            or binding.get("alignment_verified") is not True
            or diagnostics.get("recipient_supported") is not True
            or validation.get("binding_supported") is not True):
        errors.append("construction_attacker_recipient_not_established")
        return False, []
    path = validation.get("code_path_locators", [])
    if not isinstance(path, list) or not path:
        errors.append("construction_delivery_path_missing")
        return False, []
    checked, valid = [], True
    for locator in path:
        try:
            checked.append(_verify_path_locator(locator, document))
        except ValueError as error:
            errors.append("construction_delivery_path: " + str(error))
            valid = False
    linked = valid and any(_overlaps(source, step)
                           for source in implemented_locators for step in checked)
    if not linked:
        errors.append("construction_source_not_linked_to_delivery_path")
    return bool(linked), checked


def _instance_link(requirement, index, flow_rows, document, errors):
    """A construction-specific instance requirement is separate from deny scope."""
    if requirement == "any_instance":
        return True, []
    if requirement != "same_evaluated_instance":
        errors.append("construction_instance_requirement_unspecified")
        return False, []
    if type(index) is not int or not 0 <= index < len(flow_rows):
        return False, []
    row = flow_rows[index]
    if not isinstance(row, dict):
        return False, []
    binding, diagnostics = row.get("flow_binding", {}), row.get("binding_validation", {})
    validation = row.get("source_validation", {})
    if (not isinstance(binding, dict) or not isinstance(diagnostics, dict)
            or not isinstance(validation, dict)
            or binding.get("instance_relation") != "same"
            or diagnostics.get("instance_alignment_supported") is not True
            or validation.get("instance_alignment_supported") is not True):
        errors.append("construction_same_instance_not_established")
        return False, []
    locators = diagnostics.get("locators", {})
    instances = locators.get("instances", []) if isinstance(locators, dict) else []
    if not isinstance(instances, list):
        errors.append("construction_instance_evidence_missing")
        return False, []
    checked, valid = [], True
    for locator in instances:
        try:
            checked.append(_verify_path_locator(locator, document))
        except ValueError as error:
            errors.append("construction_instance_evidence: " + str(error))
            valid = False
    identities = {(part["segment_id"], part["text_view"], part["start"], part["end"]) for part in checked}
    if len(identities) < 2:
        errors.append("construction_instance_evidence_requires_independent_bindings")
        valid = False
    return valid, checked


def project_construction_findings(findings, reviews, document, flow_rows, *,
                                  input_binding, review_input_binding,
                                  in_audit_scope=True):
    """Project independently reviewed construction differences without permissions.

    ``flow_rows`` must be the evidence rows just produced by the existing
    source-aware decision engine for these same bytes. Its delivery gate remains
    required even if its policy conclusion is unresolved. Citation location does
    not prove a semantic incompatibility: every comparison axis has a separate
    independent review vote. A mismatch also needs a positively supported scope
    and exception assessment; paper silence cannot supply either.
    ``scope_supported`` also reviews the construction-specific instance
    requirement. It cannot turn a same-evaluated-record claim into a category
    claim merely because a matching configuration/record proof is unavailable.
    """
    v4.validate_input_binding(document)
    if input_binding != document["sha256"] or review_input_binding != document["sha256"]:
        raise ValueError("construction finding input binding does not match supplied input")
    if type(in_audit_scope) is not bool:
        raise ValueError("construction audit scope must be boolean")
    if not isinstance(flow_rows, list):
        raise ValueError("construction delivery evidence must be a flow-row list")
    validate_shape(findings, {"type": "array", "items": CONSTRUCTION_SCHEMA})
    validate_shape(reviews, {"type": "array", "items": CONSTRUCTION_REVIEW_SCHEMA})
    if (len(findings) > MAX_FINDINGS
            or sorted(review["index"] for review in reviews) != list(range(len(findings)))):
        raise ValueError("review must cover each of at most four construction findings once")
    by_index = {review["index"]: review for review in reviews}
    projected = []
    for index, finding in enumerate(findings):
        review, errors = by_index[index], []
        named_claim = bool(finding["claim"].strip())
        reviewed_reason = bool(review["reason"].strip())
        if not named_claim:
            errors.append("construction_claim_missing")
        if not reviewed_reason:
            errors.append("construction_review_reason_missing")
        facts = {}
        for name, vote, kind in (("contract", "contract_supported", "paper"),
                                 ("implemented_source", "implementation_supported", "code"),
                                 ("exceptions", "exceptions_supported", "paper")):
            field = finding[name]
            facts[name] = _fact(field["description"], field["citations"], document,
                                review[vote], kind, name, errors)
        mapping = finding["semantic_mapping"]
        mapped_paper = _fact(mapping["description"], mapping["paper_citations"], document,
                             review["semantic_mapping_supported"], "paper", "semantic_mapping.paper", errors)
        mapped_code = _fact(mapping["description"], mapping["code_citations"], document,
                            review["semantic_mapping_supported"], "code", "semantic_mapping.code", errors)
        mapping_supported = mapped_paper["supported"] and mapped_code["supported"]
        linked, path = _flow_link(finding["flow_index"], flow_rows,
                                  facts["implemented_source"]["locators"], document, errors)
        instance_supported, instance_locators = _instance_link(finding["instance_requirement"],
            finding["flow_index"], flow_rows, document, errors)
        comparison = finding["comparison"]
        comparison_supported = bool(comparison["description"].strip()
                                    and review["comparison_supported"])
        scope_supported = bool(finding["scope"].strip() and review["scope_supported"])
        all_supported = (facts["contract"]["supported"]
                         and facts["implemented_source"]["supported"] and mapping_supported
                         and facts["exceptions"]["supported"] and linked
                         and instance_supported and comparison_supported and scope_supported
                         and named_claim and reviewed_reason)
        agreement = finding["assessment"] == review["assessment"]
        exception_status = finding["exceptions"]["status"]
        result, reason = "unresolved", "construction_contract_not_established"
        if not in_audit_scope:
            reason = "construction_outside_audit_scope"
        elif all_supported and agreement:
            if (finding["assessment"] == "mismatch"
                    and comparison["kind"] in INCOMPATIBILITIES
                    and exception_status == "none_applicable"):
                result, reason = "confirmed", "construction_contract_mismatch_confirmed"
            elif finding["assessment"] == "aligned" and exception_status == "applicable":
                result, reason = "refuted", "construction_contract_exception_applies"
            elif (finding["assessment"] == "aligned" and comparison["kind"] == "aligned"
                    and exception_status == "none_applicable"):
                result, reason = "refuted", "construction_contract_alignment_confirmed"
            elif exception_status == "unresolved":
                reason = "construction_exception_scope_unresolved"
        elif not linked:
            reason = "construction_delivery_not_linked"
        elif not instance_supported:
            reason = "construction_instance_scope_not_established"
        elif not mapping_supported:
            reason = "construction_semantic_mapping_not_established"
        elif not scope_supported:
            reason = "construction_scope_not_established"
        elif not agreement:
            reason = "construction_review_disagrees"
        blocks_clean = bool(in_audit_scope and result == "unresolved")
        projected.append({
            "index": index, "claim": finding["claim"],
            "issue_type": "construction_contract_mismatch", "claim_result": result,
            "reason": reason, "scope": finding["scope"],
            "linked_flow_index": finding["flow_index"], "delivery_linked": linked,
            "instance_requirement": finding["instance_requirement"],
            "instance_alignment_supported": instance_supported,
            "comparison": copy.deepcopy(comparison), "proposed_assessment": finding["assessment"],
            "exception_status": exception_status, "positive_facts": facts,
            "semantic_mapping": {"description": mapping["description"],
                                 "supported": bool(mapping_supported)},
            "locators": {"contract": facts["contract"]["locators"],
                         "implemented_source": facts["implemented_source"]["locators"],
                         "semantic_mapping": {"paper": mapped_paper["locators"],
                                              "code": mapped_code["locators"]},
                         "exceptions": facts["exceptions"]["locators"],
                         "instances": instance_locators,
                         "linked_delivery_path": path},
            "evidence_errors": errors, "semantic_review": copy.deepcopy(review),
            "blocks_general_clean": blocks_clean,
            "evidence_scope": "static_conditional", "historical_execution_established": False,
            "observed_effect": "not_assessed",
        })
    blocked = any(row["blocks_general_clean"] for row in projected)
    return {"schema_version": SCHEMA_VERSION, "input_binding": document["sha256"],
            "findings": projected, "has_confirmed_mismatch": any(
                row["claim_result"] == "confirmed" for row in projected),
            "blocks_general_clean": blocked, "blocks_negative": blocked,
            "in_audit_scope": in_audit_scope, "coverage": "named_findings_only",
            "general_clean_established": False}
