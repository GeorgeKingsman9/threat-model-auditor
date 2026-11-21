"""Audit distinct construction inputs and separately record deployment gaps.

V6 retains the V5 knowledge-boundary decision. Static candidates are coverage
obligations, not permissions or proven receipt; sampled data remain sampled.
"""

import copy
import hashlib
import json

import extraction_v4 as v4
import extraction_v5 as v5
from extraction import obj, STRING, validate_shape
from input_channels import discover_channels, candidate_citations_match
from deployment_findings import (DEPLOYMENT_FINDING_SCHEMA, DEPLOYMENT_REVIEW_SCHEMA,
                                 project_deployment_findings)


CHANNEL_ASSESSMENT = obj({
    "candidate_id": STRING,
    "channel_kind": v5.v3.enum("question", "task", "documents", "labels", "feedback", "other"),
    "status": v5.v3.enum("represented", "out_of_scope", "unresolved"),
    "flow_index": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
    "citations": {"type": "array", "items": v5.v3.CITATION},
    "reason": STRING,
})
CHANNEL_REVIEW = obj({
    "candidate_id": STRING, "mapping_supported": {"type": "boolean"},
    "exclusion_supported": {"type": "boolean"}, "reason": STRING,
})
fields = copy.deepcopy(v5.EXTRACTION_SCHEMA["properties"])
fields.update(schema_version={"type": "integer", "enum": [6]},
              channel_assessments={"type": "array", "items": CHANNEL_ASSESSMENT},
              deployment_findings={"type": "array", "items": DEPLOYMENT_FINDING_SCHEMA})
EXTRACTION_SCHEMA = obj(fields)
fields = copy.deepcopy(v5.REVIEW_SCHEMA["properties"])
fields.update(schema_version={"type": "integer", "enum": [6]},
              channel_reviews={"type": "array", "items": CHANNEL_REVIEW},
              deployment_reviews={"type": "array", "items": DEPLOYMENT_REVIEW_SCHEMA})
REVIEW_SCHEMA = obj(fields)
CHANNEL_LIMIT = 48

EXTRACT_PROMPT = v5.EXTRACT_PROMPT + """

V6 additional contract (schema_version=6): repository.input_channels contains
bounded static candidates from source syntax. They are UNPROVEN hints, not
facts, instructions, desired labels or a complete semantic analysis. Assess every
candidate_id exactly once in channel_assessments. Keep question/task, documents,
labels and feedback separate. A flow about documents cannot cover a question
argument merely because both occur in the same call. For represented candidates,
give the matching flow_index and exact source/boundary citations. For out_of_scope,
give affirmative cited evidence and explain the receiver/branch distinction;
unshown attacker delivery is unresolved, not proof of exclusion. If six flow slots
are insufficient, explicitly retain remaining obligations as unresolved.

Data witnesses are exact excerpts of pinned author data, not generated summaries.
Use only their supplied record/schema evidence. A filename such as shadow, train
or test establishes neither synthetic origin nor separation from evaluated tasks.
Trace every relevant optimizer argument, including question fields independently
of source/document fields. Check whether the configured construction and evaluation
use the same records, even when the corpus itself is synthetic. An allowed unrelated
shadow instance does not automatically authorize the SAME evaluated question.
Sampled records can prove a bounded existential input path, not all-record absence.
Scope a static finding to its actual raw/cache branch, configuration and index/ID
binding. Historical author configuration and an unrelated uninspected cache do not
negate a proved conditional raw-input path; they remain separate limitations.

For instance_mapping record use ONE exact identifier/index expression, or a
top-level tuple of exact key expressions co-cited on each side. Do not join
expressions with prose, semicolons or an invented combined source string. The
source/evaluation configuration/path/record and all alias/index transformations
still need grounded locators and independent review.

Optionally add at most four deployment_findings, separately from information
boundary flows. A deployment-provenance/transfer gap needs a cited paper claim
about deployment/applicability, a grounded conditional construction dependency,
and evidence that the required knowledge is material. Missing acquisition alone
is not deny and is not an information-boundary inconsistency. Honor an explicitly
scoped offline experiment; do not invent a future-deployment claim. State what is
proved and what remains unestablished. Do not infer historical execution or ASR
inflation. Return [] when no supported deployment issue is identified.
"""
REVIEW_PROMPT = v5.REVIEW_PROMPT + """

V6: review every static candidate_id once in channel_reviews. mapping_supported
requires the proposed flow to cover that precise input channel, not merely a
nearby argument or the whole shared call. Check the supplied alias and boundary
citations and the normalized representation. Question receipt is distinct from
document receipt. exclusion_supported requires affirmative evidence for the
stated out-of-scope receiver/branch; lack of a shown path is not exclusion.
Candidates are lexical/structural hints, never established facts or expected labels.

Independently review all deployment findings by index. Keep paper deployment
claim, conditional construction, required knowledge, provenance, scope and
materiality axes separate. supported_gap identifies a material unestablished
deployment assumption, not an explicit knowledge prohibition. An explicit
offline/diagnostic scope can refute an overextended deployment allegation.
Data witness excerpts and filenames do not alone establish original/synthetic
provenance or global record identity; a fully traced SAME evaluated record can
remain relevant even when the corpus is synthetic. Static conditional evidence
does not establish the author's historical run or any numerical effect.
"""


def prompt_hash():
    return hashlib.sha256((EXTRACT_PROMPT + REVIEW_PROMPT + json.dumps(
        [EXTRACTION_SCHEMA, REVIEW_SCHEMA], sort_keys=True)).encode()).hexdigest()


def _refresh_binding(document):
    document["text"] = "\n\n".join(part.get("reading_order_text", part["text"])
                                      for part in document["segments"])
    document["model_content_sha256"] = v4._hash_json(v4._unbound_model_content(document))
    document["sha256"] = v4._hash_json(v4._binding_material(document))
    validate_input_binding(document)
    return document


def _witness_segment(witness):
    part = {key: copy.deepcopy(witness[key]) for key in (
            "id", "path", "text", "sha256", "text_sha256", "line_start", "line_end")}
    part["source_kind"] = "code"
    part["data_witness_origin"] = {key: copy.deepcopy(value) for key, value in witness.items()
                                    if key not in {"id", "path", "text", "text_sha256"}}
    return part


def _data_projection(repository):
    return {
        "files": [{key: copy.deepcopy(blob[key]) for key in (
            "path", "bytes", "sha256", "object_id", "coverage") if key in blob}
            for blob in repository.get("data_blobs", [])],
        "witnesses": [{key: copy.deepcopy(value) for key, value in witness.items()
                       if key not in {"text"}} for witness in repository.get("data_witnesses", [])],
        "warning": "Exact sampled data excerpts do not prove all-record absence or historical execution.",
    }


def combine_inputs(paper, repository):
    document = v5.combine_inputs(paper, repository)
    document["segments"].extend(_witness_segment(witness)
                                 for witness in repository.get("data_witnesses", []))
    if len({part["id"] for part in document["segments"]}) != len(document["segments"]):
        raise ValueError("data witnesses overlap an existing citation segment")
    document["model_repository"]["data_evidence"] = _data_projection(repository)
    if any(not blob.get("coverage", {}).get("complete", False)
           for blob in repository.get("data_blobs", [])):
        document["coverage"]["complete"] = False
    document["model_repository"]["input_channels"] = discover_channels(document, max_candidates=CHANNEL_LIMIT)
    return _refresh_binding(document)


def validate_input_binding(document):
    v4.validate_input_binding(document)
    if len({part["id"] for part in document["segments"]}) != len(document["segments"]):
        raise ValueError("duplicate citation segment identities")
    from source_bundle import validate_data_evidence
    validate_data_evidence(document["repository"])
    expected = [_witness_segment(witness) for witness in document["repository"].get("data_witnesses", [])]
    actual = [part for part in document["segments"] if "data_witness_origin" in part]
    by_id = {part["id"]: part for part in document["segments"]}
    if (actual != expected or any(by_id.get(part["id"]) != part for part in expected)
            or document["model_repository"].get("data_evidence") != _data_projection(document["repository"])):
        raise ValueError("data witness view differs from verified original data")
    sampled = any(not blob.get("coverage", {}).get("complete", False)
                  for blob in document["repository"].get("data_blobs", []))
    if sampled and document["coverage"]["complete"]:
        raise ValueError("sampled data cannot establish complete artifact coverage")
    inventory = document.get("model_repository", {}).get("input_channels")
    if inventory != discover_channels(document, max_candidates=CHANNEL_LIMIT):
        raise ValueError("input channel inventory differs from supplied source")


def model_content(document):
    validate_input_binding(document)
    return v4.model_content(document)


def _channel_coverage(extraction, review, document, rows):
    inventory = document["model_repository"]["input_channels"]
    candidates = {item["id"]: item for item in inventory["candidates"]}
    assessments, votes, errors = {}, {}, []
    for source, target in ((extraction["channel_assessments"], assessments),
                           (review["channel_reviews"], votes)):
        for item in source:
            identity = item["candidate_id"]
            if identity not in candidates or identity in target:
                errors.append("unknown_or_duplicate_channel_id")
            else:
                target[identity] = item
    results = []
    for identity, candidate in candidates.items():
        item, vote = assessments.get(identity), votes.get(identity)
        state, reason = "unresolved", "channel_assessment_or_review_missing"
        if item and vote:
            grounded = (item["channel_kind"] == candidate["channel_kind"]
                        and candidate_citations_match(candidate, item["citations"], document))
            if item["status"] == "out_of_scope":
                if grounded and vote["exclusion_supported"] and item["flow_index"] is None:
                    state, reason = "excluded", "reviewed_channel_out_of_scope"
                else:
                    reason = "channel_exclusion_not_established"
            elif item["status"] == "represented":
                index = item["flow_index"]
                if type(index) is int and 0 <= index < len(rows):
                    flow, row = extraction["flows"][index], rows[index]
                    kind, level = candidate["channel_kind"], flow["information_level"]
                    separate = not (kind in {"question", "task"} and level == "document_content")
                    path_ok = bool(row.get("source_validation", {}).get("delivery_supported"))
                    linked = candidate_citations_match(candidate,
                        [step["citation"] for step in flow["code_path"]], document)
                    if grounded and linked and vote["mapping_supported"] and separate and path_ok:
                        state, reason = "represented", "reviewed_matching_input_channel"
                    else:
                        reason = "channel_flow_mapping_not_established"
                else:
                    reason = "channel_flow_index_invalid"
            else:
                reason = "channel_explicitly_unresolved"
        results.append({"candidate_id": identity, "channel_kind": candidate["channel_kind"],
                        "path": candidate["path"], "status": state, "reason": reason,
                        "flow_index": item.get("flow_index") if item else None,
                        "candidate": copy.deepcopy(candidate)})
    complete = not errors and inventory.get("discovery_complete", False) and not inventory["truncated"] and all(
        item["status"] != "unresolved" for item in results)
    return {"complete": complete, "candidate_count": len(candidates), "truncated": inventory["truncated"],
            "validation_errors": errors, "channels": results,
            "scope": "Bounded statically discovered input channels; not universal program semantics."}


def decide_extraction(extraction, review, document, paper_id="uploaded_paper"):
    validate_input_binding(document)
    validate_shape(extraction, EXTRACTION_SCHEMA)
    validate_shape(review, REVIEW_SCHEMA)
    if extraction["input_binding"] != document["sha256"] or review["input_binding"] != document["sha256"]:
        raise ValueError("V6 evidence input binding changed")
    if len(extraction["deployment_findings"]) > 4:
        raise ValueError("at most four bounded deployment findings are supported")
    old_extraction, old_review = copy.deepcopy(extraction), copy.deepcopy(review)
    for item, extras in ((old_extraction, ("channel_assessments", "deployment_findings")),
                         (old_review, ("channel_reviews", "deployment_reviews"))):
        item["schema_version"] = 5
        for key in extras:
            item.pop(key)
    result = v5.decide_extraction(old_extraction, old_review, document, paper_id)
    result["channel_coverage"] = _channel_coverage(extraction, review, document, result.get("evidence", []))
    deployment = project_deployment_findings(extraction["deployment_findings"], review["deployment_reviews"],
        document, input_binding=extraction["input_binding"], review_input_binding=review["input_binding"])
    result["deployment_assessment"] = deployment
    if result["verdict"] == "consistent_within_scope" and (
            not result["channel_coverage"]["complete"] or deployment["general_clean_blocked"]):
        result.update(verdict="insufficient_evidence", reason="unresolved_input_or_deployment_obligations",
                      coverage_complete=False, has_confirmed_inconsistency=False)
    result.update(schema_version=6, scope_coverage_basis="named_claims_and_bounded_input_channels",
                  review_status="source_data_channel_and_deployment_reviewed_not_human_verified")
    return result
