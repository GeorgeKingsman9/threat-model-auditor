"""Project independently reviewed deployment questions beside information flows.

These findings concern whether an advertised deployment/transfer scenario has a
grounded route to an input used by a conditional construction. They never decide
an attacker permission or change an information-boundary verdict. In particular,
an unestablished acquisition route is not a denial, an absent route, or a proven
inconsistency. A disclosed construction dependency is not a knowledge grant.

Only supplied paper/source snapshots and independent review votes enter this
module. Exact locators establish where evidence occurs; the separate review must
establish its meaning. Static code establishes a conditional construction, never
historical execution, numerical effects, or author intent. This projection makes
no whole-paper completeness claim, including when its findings array is empty.
"""

import copy

from extraction import NULLABLE_CITATION, STRING, STRINGS, obj, validate_shape
import extraction_v3 as v3
import extraction_v4 as v4


SCHEMA_VERSION = 1
ASSESSMENT = v3.enum("supported_gap", "resolved", "uncertain")
CITATIONS = {"type": "array", "items": v3.CITATION}
CITED_FACT = obj({"description": STRING, "citations": CITATIONS})

FINDING_SCHEMA = obj({
    "claim": STRING,
    "issue_type": v3.enum("deployment_provenance", "transfer_applicability"),
    "paper_claim": obj({"description": STRING, "citation": NULLABLE_CITATION}),
    "conditional_construction": CITED_FACT,
    # The candidate prerequisite under examination. A positive not_required
    # resolution may show that it is unnecessary in the precisely named scope.
    "required_knowledge": CITED_FACT,
    "knowledge_provenance": obj({
        "status": v3.enum("established", "unresolved", "not_required"),
        "description": STRING, "citations": CITATIONS,
    }),
    "assessment": ASSESSMENT,
    "materiality": v3.enum("material", "limited", "uncertain"),
    "scope": STRING,
    "unresolved_questions": STRINGS,
})

FINDING_REVIEW_SCHEMA = obj({
    "index": {"type": "integer"},
    **{name: {"type": "boolean"} for name in (
        "paper_claim_supported", "construction_supported",
        "required_knowledge_supported", "provenance_supported",
        "scope_supported", "materiality_supported")},
    "assessment": ASSESSMENT,
    "reason": STRING,
})

# Explicit aliases make the embedded schema's purpose clear to callers.
DEPLOYMENT_FINDING_SCHEMA = FINDING_SCHEMA
DEPLOYMENT_REVIEW_SCHEMA = FINDING_REVIEW_SCHEMA


def _fact(description, citations, document, vote, kind, errors, name):
    """Locate all proposed citations; a bad extra citation cannot be ignored."""
    locators = []
    valid = bool(description.strip() and citations)
    if not valid:
        errors.append(name + ": missing description or citation")
    if len(citations) > 8:
        raise ValueError("deployment evidence exceeds the eight-citation limit")
    for citation in citations:
        try:
            locators.append(v4._locate(citation, document, kind))
        except ValueError as error:
            errors.append(name + ": " + str(error))
            valid = False
    return {"description": description,
            "supported": bool(valid and vote), "locators": locators}


def project_deployment_findings(findings, reviews, document, *, input_binding,
                                review_input_binding, in_audit_scope=True):
    """Validate and project auxiliary findings without consuming a strict verdict.

    ``findings`` and ``reviews`` are arrays embedded in the model extraction and
    its independent review. Both binding strings must identify the unchanged
    combined V4/V5 snapshot. Every finding needs exactly one review. Semantic
    review votes are necessary, but never bypass citation/domain validation.

    supported_gap requires grounded paper deployment/transfer claim, conditional
    construction and candidate prerequisite, plus reviewed unresolved acquisition.
    resolved requires positive acquisition/non-requirement evidence from code;
    disclosure or a paper permission alone cannot resolve an acquisition route.
    Neither status is an information-boundary inconsistency or permission value.

    ``general_clean_blocked`` flags material unresolved issues within the named
    audit scope. Its absence does not establish general paper cleanliness; this
    helper reviews named findings only. Independent positive facts survive a
    failed or uncertain assessment of another axis. Inputs are never mutated.
    """
    v4.validate_input_binding(document)
    if input_binding != document["sha256"] or review_input_binding != document["sha256"]:
        raise ValueError("deployment finding input binding does not match supplied input")
    if type(in_audit_scope) is not bool:
        raise ValueError("deployment audit scope must be boolean")
    validate_shape(findings, {"type": "array", "items": FINDING_SCHEMA})
    validate_shape(reviews, {"type": "array", "items": FINDING_REVIEW_SCHEMA})
    if len(findings) > 6 or sorted(r["index"] for r in reviews) != list(range(len(findings))):
        raise ValueError("review must cover each of at most six deployment findings once")
    by_index = {review["index"]: review for review in reviews}
    projected = []
    for index, finding in enumerate(findings):
        review, errors = by_index[index], []
        claim = finding["paper_claim"]
        paper_fact = _fact(claim["description"],
                           [claim["citation"]] if claim["citation"] is not None else [],
                           document, review["paper_claim_supported"], "paper", errors,
                           "paper_claim")
        construction = finding["conditional_construction"]
        construction_fact = _fact(construction["description"], construction["citations"],
                                  document, review["construction_supported"], "code", errors,
                                  "conditional_construction")
        knowledge = finding["required_knowledge"]
        knowledge_fact = _fact(knowledge["description"], knowledge["citations"],
                               document, review["required_knowledge_supported"], "code", errors,
                               "required_knowledge")
        provenance = finding["knowledge_provenance"]
        provenance_fact = _fact(provenance["description"], provenance["citations"],
                                document, review["provenance_supported"], None, errors,
                                "knowledge_provenance")
        # A paper's disclosure/grant describes an assumption or policy. It does
        # not by itself demonstrate the implemented acquisition or non-use path.
        if provenance["status"] != "unresolved" and not any(
                loc["source_kind"] == "code" for loc in provenance_fact["locators"]):
            provenance_fact["supported"] = False
            errors.append("knowledge_provenance: positive resolution requires code evidence")
        scope_supported = bool(finding["scope"].strip() and review["scope_supported"])
        materiality = (finding["materiality"] if review["materiality_supported"]
                       else "uncertain")
        anchors_supported = all((paper_fact["supported"], construction_fact["supported"],
                                 knowledge_fact["supported"], scope_supported))
        assessment = "uncertain"
        if (anchors_supported and provenance_fact["supported"]
                and finding["assessment"] == review["assessment"]):
            if finding["assessment"] == "supported_gap" and provenance["status"] == "unresolved":
                assessment = "supported_gap"
            elif finding["assessment"] == "resolved" and provenance["status"] != "unresolved":
                assessment = "resolved"
        blocks_clean = bool(in_audit_scope and scope_supported
                            and materiality == "material" and assessment != "resolved")
        projected.append({
            "index": index, "claim": finding["claim"], "issue_type": finding["issue_type"],
            "assessment": assessment, "proposed_assessment": finding["assessment"],
            "materiality": materiality, "scope": finding["scope"],
            "scope_supported": scope_supported,
            "positive_facts": {"paper_claim": paper_fact,
                               "conditional_construction": construction_fact,
                               "required_knowledge": knowledge_fact},
            "knowledge_provenance": {
                **provenance_fact, "proposed_status": provenance["status"],
                "status": provenance["status"] if provenance_fact["supported"] else "uncertain",
                "acquisition_path_established": bool(provenance_fact["supported"]
                                                     and provenance["status"] == "established"),
            },
            "unresolved_questions": copy.deepcopy(finding["unresolved_questions"]),
            "evidence_errors": errors, "semantic_review": copy.deepcopy(review),
            "blocks_general_clean": blocks_clean,
            "evidence_scope": "static_conditional",
            "historical_execution_established": False, "observed_effect": "not_assessed",
        })
    return {
        "schema_version": SCHEMA_VERSION, "input_binding": document["sha256"],
        "findings": projected, "in_audit_scope": in_audit_scope,
        "general_clean_blocked": any(row["blocks_general_clean"] for row in projected),
        "general_clean_established": False, "coverage": "named_findings_only",
        "information_boundary_verdict_unchanged": True,
    }
