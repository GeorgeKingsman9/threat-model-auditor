"""Audit a bounded task-acquisition/deployment contract, independently of deny.

V6's positive construction/provenance facts are retained. V7 can classify a
material, independently reviewed deployment-contract gap as its own issue type.
It does not turn unestablished acquisition into absent knowledge, a prohibition,
impossible acquisition, historical execution, or an ASR claim.
"""

import copy

from extraction import STRING, obj, validate_shape
import extraction_v3 as v3
import extraction_v4 as v4
import deployment_findings as legacy
from construction_contracts import _verify_path_locator


_CITATIONS = {"type": "array", "items": v3.CITATION, "maxItems": 6}
_FACT_FIELDS = {"description": STRING, "citations": _CITATIONS}
_EXTRA_FIELDS = {
    "dependency_flow_index": {"type": "integer"},
    "source_boundary": obj({"basis": v3.enum(
        "allowed_observations", "explicit_knowledge_constraint",
        "black_box_label_only", "unresolved"), **copy.deepcopy(_FACT_FIELDS)}),
    "actual_source": obj({"origin": v3.enum(
        "operator_provided", "configuration_provided", "observed_trace",
        "public_observation", "explicit_assumption", "other", "unknown"),
        **copy.deepcopy(_FACT_FIELDS)}),
    "timing": obj({"status": v3.enum("pre_observation", "post_observation", "unresolved"),
                   **copy.deepcopy(_FACT_FIELDS)}),
    "task_relation": obj({"status": v3.enum(
        "same_task_conditioning", "future_task_transfer", "different_task", "unknown"),
        **copy.deepcopy(_FACT_FIELDS)}),
    "deployment_scope": obj({"status": v3.enum(
        "offline_only", "online", "offline_to_online", "uncertain"),
        **copy.deepcopy(_FACT_FIELDS)}),
}
_EXTRA_REVIEWS = {name + "_supported": {"type": "boolean"} for name in (
    "source_boundary", "actual_source", "timing", "task_relation", "deployment_scope")}
DEPLOYMENT_SCHEMA = obj({**copy.deepcopy(legacy.FINDING_SCHEMA["properties"]),
                         **copy.deepcopy(_EXTRA_FIELDS)})
DEPLOYMENT_REVIEW_SCHEMA = obj({**copy.deepcopy(legacy.FINDING_REVIEW_SCHEMA["properties"]),
                                **copy.deepcopy(_EXTRA_REVIEWS)})


def _check_bounds(findings):
    if len(findings) > 4:
        raise ValueError("at most four V7 deployment findings are supported")
    for finding in findings:
        for name in ("conditional_construction", "required_knowledge", "knowledge_provenance",
                     "source_boundary", "actual_source", "timing", "task_relation", "deployment_scope"):
            if len(finding[name]["citations"]) > 6:
                raise ValueError("V7 deployment evidence exceeds the six-citation limit")


def _fact(item, document, supported, kind, errors, name):
    # All submitted quotes must validate; a valid subset cannot silently replace
    # a proposed fact with an unsupported extra pointer.
    return legacy._fact(item["description"], item["citations"], document,
                        supported, kind, errors, name)


def _same_span(left, right):
    """Require actual same-domain overlap, never merely the same source file."""
    keys = ("segment_id", "document_sha256", "source_kind", "path", "file_sha256")
    if any(left.get(key) != right.get(key) for key in keys):
        return False
    if left.get("text_view", "primary") != right.get("text_view", "primary"):
        return False
    bounds = (left.get("start"), left.get("end"), right.get("start"), right.get("end"))
    return (all(type(value) is int for value in bounds)
            and left["start"] < right["end"] and right["start"] < left["end"])


def _dependency(finding, flow_rows, document, actual_source, construction, knowledge, errors):
    index = finding["dependency_flow_index"]
    if not isinstance(flow_rows, list) or type(index) is not int or not 0 <= index < len(flow_rows):
        errors.append("dependency_flow_index: no matching grounded flow")
        return {"supported": False, "flow_index": index, "path_locators": []}
    flow = flow_rows[index]
    validation = flow.get("source_validation", {})
    binding = flow.get("flow_binding", {})
    diagnostics = flow.get("binding_validation", {})
    proposed_path = validation.get("code_path_locators", [])
    path, path_valid = [], isinstance(proposed_path, list) and bool(proposed_path)
    for loc in proposed_path if isinstance(proposed_path, list) else []:
        try:
            path.append(_verify_path_locator(loc, document))
        except ValueError as error:
            path_valid = False
            errors.append("dependency_flow: " + str(error))
    receipt = (validation.get("delivery_supported") is True
               and validation.get("binding_supported") is True
               and binding.get("attacker_delivery") == "confirmed"
               and binding.get("alignment_verified") is True
               and diagnostics.get("recipient_supported") is True
               and binding.get("recipient_role") in {"attacker_constructor", "attacker_optimizer"})
    linked = path_valid and all(any(_same_span(loc, step) for loc in fact["locators"] for step in path)
                                for fact in (actual_source, construction, knowledge))
    if not receipt:
        errors.append("dependency_flow: attacker receipt is not independently established")
    if not linked:
        errors.append("dependency_flow: source/construction/knowledge citations do not match its grounded path")
    return {"supported": bool(receipt and linked), "flow_index": index,
            "path_locators": copy.deepcopy(path)}


def project_deployment_findings_v7(findings, reviews, document, flow_rows, *,
                                   input_binding, review_input_binding, in_audit_scope=True):
    """Return typed findings without inventing a strict permission value.

    A confirmed gap needs positive cited deployment/boundary/dependency facts,
    exact connected attacker receipt, temporal and task-instance alignment,
    materiality and an independent vote on every axis. The source/route enums
    describe the proposal's semantics, not a keyword classifier; the independent
    review must reject a ``black-box`` label mislabeled as a knowledge boundary.

    ``unresolved`` provenance means the reviewed claimed deployment has not
    established acquisition. It never means the task cannot be acquired. A
    resolved named route or an affirmative, explicitly offline scope can refute
    this particular gap; neither certifies the whole paper.
    """
    v4.validate_input_binding(document)
    if input_binding != document["sha256"] or review_input_binding != document["sha256"]:
        raise ValueError("V7 deployment finding input binding does not match supplied input")
    if type(in_audit_scope) is not bool:
        raise ValueError("deployment audit scope must be boolean")
    validate_shape(findings, {"type": "array", "items": DEPLOYMENT_SCHEMA})
    validate_shape(reviews, {"type": "array", "items": DEPLOYMENT_REVIEW_SCHEMA})
    _check_bounds(findings)
    if sorted(item["index"] for item in reviews) != list(range(len(findings))):
        raise ValueError("V7 deployment review must cover every finding exactly once")
    old_findings = [{key: copy.deepcopy(item[key]) for key in legacy.FINDING_SCHEMA["properties"]}
                    for item in findings]
    old_reviews = [{key: copy.deepcopy(item[key]) for key in legacy.FINDING_REVIEW_SCHEMA["properties"]}
                   for item in reviews]
    prior = legacy.project_deployment_findings(old_findings, old_reviews, document,
        input_binding=input_binding, review_input_binding=review_input_binding,
        in_audit_scope=in_audit_scope)
    review_by_index = {item["index"]: item for item in reviews}
    rows = []
    for index, finding in enumerate(findings):
        vote = review_by_index[index]
        row = copy.deepcopy(prior["findings"][index])
        errors = row["evidence_errors"]
        kinds = {"source_boundary": "paper", "actual_source": "code", "timing": "code",
                 "task_relation": None, "deployment_scope": "paper"}
        axes = {name: _fact(finding[name], document, vote[name + "_supported"], kind, errors, name)
                for name, kind in kinds.items()}
        # Same-task conditioning is an implementation relation. Its code proof
        # and independent review need no duplicate paper quote: paper_claim and
        # deployment_scope already ground the advertised scenario separately.
        # A future-task transfer relation additionally needs the paper's specific
        # transfer claim; neither relation follows from paper wording alone.
        relation_domains = {loc["source_kind"] for loc in axes["task_relation"]["locators"]}
        needed_domains = ({"paper", "code"} if finding["task_relation"]["status"] == "future_task_transfer"
                          else {"code"})
        if not relation_domains >= needed_domains:
            axes["task_relation"]["supported"] = False
            errors.append("task_relation: code identity evidence is required; future-task transfer also needs a paper claim")
        dependency = _dependency(finding, flow_rows, document, axes["actual_source"],
            row["positive_facts"]["conditional_construction"],
            row["positive_facts"]["required_knowledge"], errors)
        new_axes_supported = all(fact["supported"] for fact in axes.values())
        source_class = finding["source_boundary"]["basis"] in {
            "allowed_observations", "explicit_knowledge_constraint"}
        origin_class = finding["actual_source"]["origin"] in {
            "operator_provided", "configuration_provided"}
        # Observing the very task that conditions construction can legitimately
        # disclose it. A post-observation gap needs the separate future-task
        # transfer claim; it cannot be inferred from same-task conditioning.
        timing_supported = (finding["timing"]["status"] == "pre_observation"
            or (finding["timing"]["status"] == "post_observation"
                and finding["task_relation"]["status"] == "future_task_transfer"
                and finding["deployment_scope"]["status"] == "offline_to_online"))
        relation = finding["task_relation"]["status"] in {
            "same_task_conditioning", "future_task_transfer"}
        online_scope = finding["deployment_scope"]["status"] in {"online", "offline_to_online"}
        result, reason = "unresolved", "deployment_contract_obligations_unresolved"
        if in_audit_scope:
            if (row["assessment"] == "supported_gap" and row["materiality"] == "material"
                    and new_axes_supported and dependency["supported"]
                    and source_class and origin_class and timing_supported and relation and online_scope):
                result, reason = "confirmed", "material_task_acquisition_deployment_gap_confirmed"
            elif (finding["assessment"] == vote["assessment"] == "resolved"
                  and row["scope_supported"]
                  and row["positive_facts"]["paper_claim"]["supported"]
                  and axes["deployment_scope"]["supported"]
                  and finding["deployment_scope"]["status"] == "offline_only"):
                result, reason = "refuted", "deployment_gap_refuted_explicit_offline_scope"
            elif row["assessment"] == "resolved" and new_axes_supported and dependency["supported"]:
                # Require the demonstrated acquisition/non-use evidence to be
                # linked to this exact path, not a hypothetical other branch.
                route_linked = any(_same_span(loc, step)
                    for loc in row["knowledge_provenance"]["locators"]
                    for step in dependency["path_locators"])
                if route_linked:
                    result, reason = "refuted", "deployment_gap_refuted_grounded_acquisition_or_non_requirement"
                else:
                    errors.append("knowledge_provenance: resolution is not linked to the matching flow path")
        else:
            reason = "deployment_finding_outside_audit_scope"
        if not source_class:
            errors.append("source_boundary: a black-box label or unresolved rule is not a knowledge boundary")
        row.update({
            "issue_type": "task_acquisition_deployment_gap", "proposed_issue_type": finding["issue_type"],
            "claim_result": result, "reason": reason,
            "axes": {name: {**fact, **{key: value for key, value in finding[name].items()
                                              if key not in {"description", "citations"}}}
                     for name, fact in axes.items()},
            "dependency": dependency,
            "semantic_review": copy.deepcopy(vote),
            "locators": {**{name: fact["locators"] for name, fact in row["positive_facts"].items()},
                         "knowledge_provenance": row["knowledge_provenance"]["locators"],
                         **{name: fact["locators"] for name, fact in axes.items()},
                         "dependency_path": dependency["path_locators"]},
            "blocks_general_clean": bool(in_audit_scope and result != "refuted"),
            "finding_strength": "bounded_deployment_contract_gap" if result == "confirmed" else result,
            "acquisition_impossible_established": False,
            "knowledge_prohibition_inferred": False,
        })
        rows.append(row)
    blocked = any(row["blocks_general_clean"] for row in rows)
    return {"schema_version": 7, "input_binding": document["sha256"], "findings": rows,
            "has_confirmed_gap": any(row["claim_result"] == "confirmed" for row in rows),
            "blocks_negative": blocked, "general_clean_blocked": blocked,
            "general_clean_established": False, "in_audit_scope": in_audit_scope,
            "coverage": "named_findings_only", "information_boundary_verdict_unchanged": True}
