"""Compare knowledge boundaries, construction contracts and deployment assumptions.

Each track uses original paper/source evidence and an independent semantic review.
Broad paper findings retain their type; a deployment gap never manufactures deny.
"""

import copy
import hashlib
import json
from collections import Counter

from extraction import obj, STRING, validate_shape
import extraction_v6 as v6
from construction_contracts import (CONSTRUCTION_SCHEMA, CONSTRUCTION_REVIEW_SCHEMA,
                                    project_construction_findings)
from deployment_v7 import (DEPLOYMENT_SCHEMA, DEPLOYMENT_REVIEW_SCHEMA,
                           project_deployment_findings_v7)


CATEGORIES = ("knowledge_boundary_violation", "construction_contract_mismatch",
              "task_acquisition_deployment_gap")
CATEGORY_SCHEMA = obj({
    "category": v6.v5.v3.enum(*CATEGORIES),
    "status": v6.v5.v3.enum("candidates", "none_identified", "unresolved"),
    "finding_indices": {"type": "array", "items": {"type": "integer"}},
    "citations": {"type": "array", "items": v6.v5.v3.CITATION},
    "reason": STRING,
})
CATEGORY_REVIEW = obj({
    "category": v6.v5.v3.enum(*CATEGORIES),
    "assessment_supported": {"type": "boolean"}, "reason": STRING,
})
fields = copy.deepcopy(v6.EXTRACTION_SCHEMA["properties"])
fields.update(schema_version={"type": "integer", "enum": [7]},
              construction_findings={"type": "array", "items": CONSTRUCTION_SCHEMA},
              deployment_findings={"type": "array", "items": DEPLOYMENT_SCHEMA},
              category_assessments={"type": "array", "items": CATEGORY_SCHEMA})
EXTRACTION_SCHEMA = obj(fields)
fields = copy.deepcopy(v6.REVIEW_SCHEMA["properties"])
fields.update(schema_version={"type": "integer", "enum": [7]},
              construction_reviews={"type": "array", "items": CONSTRUCTION_REVIEW_SCHEMA},
              deployment_reviews={"type": "array", "items": DEPLOYMENT_REVIEW_SCHEMA},
              category_reviews={"type": "array", "items": CATEGORY_REVIEW})
REVIEW_SCHEMA = obj(fields)

EXTRACT_PROMPT = v6.EXTRACT_PROMPT + """

V7 supersedes the V6 optional-auxiliary-only decision contract. Set schema_version=7.
The audit now has THREE separate confirmation tracks. Examine all three on every
paper and record each category once in category_assessments, even when no candidate
is found. finding_indices refer respectively to flows, construction_findings and
deployment_findings. Cite affirmative evidence for a none_identified assessment;
an empty list or failure to search is not a clean result. Never use paper identity,
remembered findings, desired verdicts or labels to fill any track.

1. knowledge_boundary_violation: keep the existing SAME-edge applicable deny +
verified recipient receipt rule. A procedure saying the operator supplies input
is NOT itself a knowledge grant or a common-rule override. Identify an applicable
knowledge permission separately, or keep that permission unresolved.

2. construction_contract_mismatch: at most four construction_findings compare an
EXPLICIT paper claim about construction inputs, generation procedure, source or
information granularity against a source-supported incompatible implementation
within the SAME released branch/configuration. Link flow_index to the actual
constructor/optimizer receipt. Use exact paper citations for contract and scope
exceptions; source citations for implemented_source; and both domains for the
semantic_mapping. A semantic task component may map to a COMPOSITION of source
arguments (e.g. a generic instruction plus its task-specific question). Use the
paper's whole-input definition, component partition, and complete source formatter
to establish that mapping, not variable-name equality or a presumed prohibition.
Incompatible source provenance can establish a construction finding even when the
stronger knowledge-boundary policy remains uncertain. This is not an invented deny.
Compare stated metadata-to-generated-proxy construction with actual task-record
reuse when the pinned configuration/record chain supports that distinction. Do
not infer original/synthetic origin merely from field names or filenames. A direct
input omitted in prose, an unlocated generator, or a disclosed example alone is
not an incompatible contract. Honor explicit implementation variants, exceptions,
and genuinely separate training proxies. Unknown provenance remains uncertain.
Set instance_requirement from this construction contract: same_evaluated_instance
when incompatibility depends on reuse of that evaluated record, any_instance for
a category-wide construction rule, unspecified if unresolved. A same-instance
claim must use a linked flow with verified same-record mapping; do not switch to
any_instance to bypass missing identity evidence.
No proof of an ASR increase or author historical execution is required for a
bounded released-implementation mismatch; do not claim either from static evidence.

3. task_acquisition_deployment_gap: deployment_findings are now potentially
confirmatory for this distinct category, never for knowledge prohibition. Inspect
each task-conditioned constructor's input SOURCE, TIMING and INSTANCE against
the paper's claimed online/offline-to-online scenario. Link dependency_flow_index
to actual constructor/optimizer receipt. Keep source_boundary, actual_source,
timing, task_relation and deployment_scope separately cited. An operator-provided
precise task is an experimental dependency, not evidence that a real attacker can
acquire a future victim's task. Trace observation channels explicitly: local trace
visibility need not establish future-instance knowledge. Conversely, black-box
alone does not forbid queries; a demonstrated permitted observation or an explicit
offline-only scope may resolve/refute the gap. A confirmed gap needs a material,
paper-grounded claimed scenario, a verified task-conditioning dependency, a
reviewed timing/instance mismatch and unestablished acquisition within that named
scope. It asserts an unestablished deployment assumption, NOT impossible knowledge,
an absent acquisition route, ASR inflation, or a hidden explicit deny. Mere silence,
missing source, an unexplained argument or a speculative future-deployment claim
is not sufficient. State every established fact and remaining assumption precisely.
Separate the location of an experiment (sandbox versus live) from its claimed
deployment scope (offline versus online). A sandbox-only ethics statement is
not an offline-only threat-model exception to a separate online claim. A future
unseen-task success/transfer theorem is not needed to PROPOSE a structured
acquisition obligation; its absence alone also cannot CONFIRM a gap. Trace the
original task source upstream of wrapper arguments, and distinguish first task
knowledge from the later constructor-receipt time. Where online applicability
and a task-conditioned path are both cited, record a possibly uncertain structured
deployment candidate rather than replacing the source/timing analysis with prose.
source_boundary.basis distinguishes affirmative allowed_observations or an
explicit_knowledge_constraint from black_box_label_only or unresolved. actual_source.origin
names the proved operator/configuration, observed/public channel or explicit known
assumption. Do not label an operator field observed_trace without tracing that route.

Use concise summaries, at most six knowledge flows and four findings per new
track. Use short unique exact quotations rather than long reconstructed passages.
Return all required fields, but keep unsupported findings uncertain. The schema's
assessment enums do not waive exact citations, linked paths or independent review.
"""

REVIEW_PROMPT = v6.REVIEW_PROMPT + """

V7 supersedes the V6 auxiliary-only restriction. Set schema_version=7. Independently
review each construction/deployment index once and all three categories once.
Check the actual author's paper and pinned source, not the proposal's confidence.
The declared contract remains untrusted. Do not inherit permission from procedural
disclosure or equate source variable names with paper concepts. For compound task
input, check the full formatter and paper component partition before deciding
whether a separately stored question is part of the intended task information.

Construction comparison_supported requires an explicit applicable paper
construction/source claim and positively incompatible implemented source or
generation/granularity, not a missing prose argument or absent generator. Check
semantic_mapping, released branch scope and positive exception evidence separately.
construction scope_supported must verify instance_requirement against the
construction contract itself, not a guessed knowledge prohibition. Require a
verified same-record mapping when the alleged incompatibility depends on the
evaluated instance; category-wide contracts may genuinely use any_instance.
The linked flow must establish receipt by the actual constructor/optimizer even
when its knowledge permission is uncertain. A policy-uncertain flow does not
automatically invalidate an independently proved construction mismatch.

For deployment, review source boundary, actual supplied source, timing, task
relation and claimed deployment scope independently. Operator supplies a task
does not establish future-victim acquisition, nor does a procedure disclosure
create a knowledge exception. A material supported_gap may confirm only the typed
task_acquisition_deployment_gap. Preserve explicit offline-only cases, permitted
observation paths and stated known-task assumptions as possible refutations.
Missing paths/black-box wording alone cannot establish a gap. Do not claim that
acquisition is impossible, the attack ineffective, or a historical run differed.
Sandbox evaluation location does not by itself retract an online threat-model
claim. Check first acquisition and later receipt separately. Do not require an
unseen-task success theorem to recognize a missing acquisition assumption; still
require the positive scenario/dependency/temporal/materiality evidence for a gap.

Review category assessments even if a corresponding findings list is empty; flag
unexamined task-conditioning/proxy-generation obligations rather than accepting
none_identified by default. No expected answer or paper-specific exception exists.
"""


def prompt_hash():
    return hashlib.sha256((EXTRACT_PROMPT + REVIEW_PROMPT + json.dumps(
        [EXTRACTION_SCHEMA, REVIEW_SCHEMA], sort_keys=True)).encode()).hexdigest()


combine_inputs = v6.combine_inputs
model_content = v6.model_content
validate_input_binding = v6.validate_input_binding
attach_declared_contract = v6.attach_declared_contract


def _category_coverage(extraction, review, document, tracks):
    proposed, votes, errors = {}, {}, []
    for source, target in ((extraction["category_assessments"], proposed),
                           (review["category_reviews"], votes)):
        for item in source:
            category = item["category"]
            if category in target:
                errors.append("duplicate_category:" + category)
            target[category] = item
    rows = []
    for category in CATEGORIES:
        item, vote, valid = proposed.get(category), votes.get(category), True
        locators = []
        if item is None or vote is None:
            valid = False
        else:
            try:
                if not item["reason"].strip() or not item["citations"] or len(item["citations"]) > 6:
                    raise ValueError("category evidence missing or exceeds limit")
                locators = [v6.v4._locate(cite, document) for cite in item["citations"]]
            except ValueError:
                valid = False
            indices = item["finding_indices"]
            if (len(set(indices)) != len(indices)
                    or any(type(index) is not int or not 0 <= index < len(tracks[category]) for index in indices)):
                valid = False
            if item["status"] == "candidates" and not indices:
                valid = False
            if item["status"] == "none_identified" and (indices or tracks[category]):
                valid = False
            valid = bool(valid and vote["assessment_supported"] and item["status"] != "unresolved")
        rows.append({"category": category, "complete": valid,
                     "proposed_status": item["status"] if item else "missing", "locators": locators})
    return {"categories": rows, "validation_errors": errors,
            "complete": not errors and all(row["complete"] for row in rows)}


def decide_extraction(extraction, review, document, paper_id="uploaded_paper"):
    validate_input_binding(document)
    validate_shape(extraction, EXTRACTION_SCHEMA)
    validate_shape(review, REVIEW_SCHEMA)
    if extraction["input_binding"] != document["sha256"] or review["input_binding"] != document["sha256"]:
        raise ValueError("V7 evidence input binding changed")
    old_extraction, old_review = copy.deepcopy(extraction), copy.deepcopy(review)
    old_extraction["schema_version"] = old_review["schema_version"] = 6
    for item, extras in ((old_extraction, ("construction_findings", "category_assessments")),
                         (old_review, ("construction_reviews", "category_reviews"))):
        for field in extras:
            item.pop(field)
    # V6 receives no new deployment rows: its frozen semantics remain auxiliary.
    old_extraction["deployment_findings"], old_review["deployment_reviews"] = [], []
    result = v6.decide_extraction(old_extraction, old_review, document, paper_id)
    strict_rows = result.get("evidence", [])
    for row in strict_rows:
        row["issue_type"] = "knowledge_boundary_violation"
    boundary_verdict = result["verdict"]
    in_scope = bool(extraction["applicability"] == "in_scope"
                    and review["applicability"] == "in_scope" and review["applicability_supported"])
    options = {"input_binding": extraction["input_binding"], "review_input_binding": review["input_binding"],
               "in_audit_scope": in_scope}
    construction = project_construction_findings(extraction["construction_findings"],
        review["construction_reviews"], document, strict_rows, **options)
    deployment = project_deployment_findings_v7(extraction["deployment_findings"],
        review["deployment_reviews"], document, strict_rows, **options)
    crows, drows = construction["findings"], deployment["findings"]
    tracks = {CATEGORIES[0]: strict_rows, CATEGORIES[1]: crows, CATEGORIES[2]: drows}
    category_coverage = _category_coverage(extraction, review, document, tracks)
    result["evidence"] = strict_rows + crows + drows
    confirmed = [row for row in result["evidence"] if row.get("claim_result") == "confirmed"]
    if confirmed:
        result.update(verdict="inconsistent", reason="confirmed_typed_inconsistency_in_scope",
                      has_confirmed_inconsistency=True)
    elif result["verdict"] == "consistent_within_scope" and (
            construction["blocks_negative"] or deployment["blocks_negative"] or not category_coverage["complete"]):
        result.update(verdict="insufficient_evidence", reason="unresolved_three_category_obligations",
                      coverage_complete=False, has_confirmed_inconsistency=False)
    result.update(schema_version=7, knowledge_boundary_verdict=boundary_verdict,
        construction_assessment=construction, deployment_assessment=deployment,
        category_coverage=category_coverage,
        confirmed_issue_types=sorted({row["issue_type"] for row in confirmed}),
        claim_result_counts=dict(Counter(row.get("claim_result", "unresolved") for row in result["evidence"])),
        review_status="three_category_source_reviewed_not_human_verified",
        scope_coverage_basis="three_categories_named_claims_and_bounded_input_channels")
    return result
