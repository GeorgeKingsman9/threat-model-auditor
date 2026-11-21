#!/usr/bin/env python3
"""Publish safe, offline projections of the finished two-paper V7 URL pilot.

python3 -B scripts/summarize_v7_pilot.py outputs/2026-11-21-v7-url-pilot \
    --public-dir docs/results/2026-11-21-v7-url-pilot

This script performs no inference, network requests, author-code execution or
label lookup. Wait for all run writers to finish first. Existing output
directories are refused, and source payloads/quotes/private paths are omitted.
"""

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import sys
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summarize_v6_pilot as base
import summarize_v6_followup as prior


PAPER_IDS = ("muzzle", "obliinjection")
CATEGORIES = ("knowledge_boundary_violation", "construction_contract_mismatch", "task_acquisition_deployment_gap")
SUCCESS = {"completed", "completed_with_warnings"}


def json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def raw_manifest(run, public_dir):
    """Hash every raw run file, including driver and raw per-paper reports."""
    rows = []
    for path in sorted(run.rglob("*")):
        relative = path.relative_to(run)
        if set(relative.parts) & base.DERIVATIVES or path.is_relative_to(public_dir):
            continue
        if path.is_file():
            if not path.resolve().is_relative_to(run):
                raise ValueError("input artifact symlink escapes its run directory")
            if any(part.lower().startswith("gold") for part in relative.parts):
                raise ValueError("evaluation-label sidecar found in raw run artifacts")
            rows.append({"run_id": run.name, "path": relative.as_posix(),
                         "bytes": path.stat().st_size, "sha256": base.digest(path)})
    return rows


def safe_fact(fact, projector):
    if not isinstance(fact, dict):
        return {}
    result = {key: projector.prose(value) if isinstance(value, str) else value
              for key, value in fact.items() if key in {
                  "supported", "status", "proposed_status", "basis", "origin", "acquisition_path_established"}
              and isinstance(value, (str, bool, int, type(None)))}
    if isinstance(fact.get("description"), str):
        result["summary"] = projector.prose(fact["description"])
    result["locators"] = projector.locators(fact.get("locators", []))
    return result


def safe_claim(claim, projector):
    result = {key: projector.prose(claim[key]) for key in (
        "claim", "claim_result", "reason", "issue_type", "evidence_scope", "observed_effect",
        "instance_requirement", "exception_status", "finding_strength") if isinstance(claim.get(key), str)}
    result["scope"] = projector.metadata(claim.get("scope"))
    for key in ("linked_flow_index", "delivery_linked", "instance_alignment_supported",
                "historical_execution_established", "acquisition_impossible_established", "knowledge_prohibition_inferred"):
        if isinstance(claim.get(key), (bool, int)):
            result[key] = claim[key]
    assessment = claim.get("assessment", {})
    if isinstance(assessment, dict):
        result["assessment"] = {key: {name: projector.prose(value) for name, value in field.items()
            if name in {"policy_kind", "status", "evidence_kind", "task_relation", "basis", "reason"} and isinstance(value, str)}
            for key, field in assessment.items() if isinstance(field, dict)}
    elif isinstance(assessment, str):
        result["assessment"] = base.code(assessment)
    result["flow_binding"] = projector.metadata(claim.get("flow_binding", {}))
    result["locators"] = projector.locators({key: claim.get(key, {}) for key in (
        "locators", "source_validation", "binding_validation", "positive_facts", "axes", "dependency")})
    result["positive_facts"] = {key: safe_fact(value, projector)
        for key, value in claim.get("positive_facts", {}).items()}
    result["axes"] = {key: safe_fact(value, projector) for key, value in claim.get("axes", {}).items()}
    if isinstance(claim.get("semantic_mapping"), dict):
        result["semantic_mapping"] = safe_fact(claim["semantic_mapping"], projector)
    if isinstance(claim.get("knowledge_provenance"), dict):
        result["knowledge_provenance"] = safe_fact(claim["knowledge_provenance"], projector)
    comparison = claim.get("comparison", {})
    if isinstance(comparison, dict) and comparison:
        result["comparison"] = {"kind": base.code(comparison.get("kind")),
                                "summary": projector.prose(comparison.get("description"))}
    vote = claim.get("semantic_review", {})
    result["independent_review"] = {key: projector.prose(value) if isinstance(value, str) else value
        for key, value in vote.items() if isinstance(value, bool) or key in {"index", "assessment", "reason"}}
    for key in ("source_validation", "binding_validation"):
        validation = claim.get(key, {})
        result[key] = {**base.numbers(validation), "error_codes": [base.error_code(value)
                       for value in validation.get("validation_errors", [])]}
    result["evidence_error_codes"] = [base.error_code(value) for value in claim.get("evidence_errors", [])]
    result["citation_error_codes"] = [base.error_code(value) for value in claim.get("citation_errors", [])]
    return result


def inference_summary(directory):
    """Count each wrapper invocation once and keep the failed first review."""
    result = base.inference(directory)
    raw = base.read_json(directory / "inference.json", optional=True)
    for public, call in zip(result["calls"], raw.get("calls", [])):
        for key in ("elapsed_seconds",):
            if isinstance(call.get(key), (int, float)):
                public[key] = call[key]
        public["cli_version"] = base.code(call.get("cli_version"))
        public["event_shapes"] = {base.code(key): value for key, value in call.get("event_shapes", {}).items()
                                  if base.code(key) and type(value) is int}
        public["diagnostics"] = [{
            "event_type": base.code(item.get("event_type")), "category": base.code(item.get("category")),
            "fatal": item.get("fatal") is True,
            "codes": [value for value in item.get("codes", []) if type(value) is int or base.code(value)],
            "http_statuses": [value for value in item.get("http_statuses", []) if type(value) is int and 100 <= value <= 599],
            "message_sha256": item.get("message_sha256") if base.HEX.fullmatch(str(item.get("message_sha256"))) else None,
            "message_characters": item.get("message_characters") if type(item.get("message_characters")) is int else None,
            "structure": base.numbers(item.get("structure")),
        } for item in call.get("diagnostics", []) if isinstance(item, dict)]
        for key in ("stdout_summary", "stderr_summary", "transport_diagnostics"):
            if isinstance(call.get(key), dict):
                # These are schema-owned opaque hashes/counts, never captured CLI prose.
                safe = {name: value for name, value in call[key].items() if name in {
                    "bytes", "timeout_seconds", "errno"} and isinstance(value, (int, float))}
                for name in ("sha256", "category", "kind"):
                    if base.code(call[key].get(name)):
                        safe[name] = call[key][name]
                public[key] = safe
    calls = result["calls"]
    phases = [call["stage"] for call in calls]
    permitted = [tuple(["declared_contract", "extraction"]
        + (["acquisition_pass"] if acquisition else []) + (["citation_repair"] if repair else [])
        + ["semantic_review", "semantic_review_retry1"])
        for acquisition in (False, True) for repair in (False, True)]
    if any(phase is None for phase in phases) or not any(tuple(phases) == sequence[:len(phases)] for sequence in permitted):
        raise ValueError("V7 invocation phases are not an exact allowed frozen prefix")
    retries = [index for index, call in enumerate(calls) if call["stage"] == "semantic_review_retry1"]
    if len(retries) > 1:
        raise ValueError("more than one V7 review retry was recorded")
    if retries:
        retry = retries[0]
        if (retry == 0 or calls[retry - 1]["stage"] != "semantic_review"
                or calls[retry - 1]["status"] in SUCCESS
                or calls[retry - 1]["request_sha256"] != calls[retry]["request_sha256"]
                or calls[retry - 1]["requested_model"] != calls[retry]["requested_model"]):
            raise ValueError("V7 retry did not preserve the failed review's exact request/model")
    result.update(review_retry_count=len(retries), observed_model_phases=phases,
                  model_phase_sequence_verified=True,
                  failed_invocation_count=sum(call["status"] not in SUCCESS for call in calls))
    return result


def bound_content(combined):
    content = {"source_type": combined["media_type"],
        "segments": [{"id": item["id"], "text": item.get("reading_order_text", item["text"])}
                     for item in combined["segments"]],
        "repository": combined.get("model_repository", combined["repository"]),
        "paper_sha256": combined["paper_sha256"]}
    if json_hash(content) != combined["model_content_sha256"]:
        raise ValueError("combined model view hash differs from its original payload")
    return {**content, "input_binding": combined["sha256"]}


def acquisition_summary(directory, combined, result, projector):
    names = ("acquisition_pass.request.json", "acquisition_pass.response.json", "acquisition_pass.checks.json",
             "extraction.acquisition.json", "acquisition_pass.failure.json")
    present = {name: (directory / name).is_file() for name in names}
    if not any(present.values()):
        return {"status": "not_requested_or_not_reached", "artifact_presence": present}, {"status": "not_reached"}
    request = base.read_json(directory / names[0], optional=True)
    if not request or not combined:
        raise ValueError("acquisition pass lacks the bound original source-aware request")
    original = base.read_json(directory / "extraction.json")
    if (base.label_fields(request) or original.get("input_binding") != combined["sha256"]
            or request != {**bound_content(combined), "proposal": original}):
        raise ValueError("acquisition input is not the same snapshot and current-run automatic proposal")
    response = base.read_json(directory / names[1], optional=True)
    refined = base.read_json(directory / names[3], optional=True)
    notes = json.loads((directory / names[2]).read_text()) if present[names[2]] else []
    if not isinstance(notes, list):
        raise ValueError("acquisition checks are not a note array")
    if any(not isinstance(note, dict) for note in notes):
        raise ValueError("acquisition check note must be an object")
    prefixes, candidates = [], []
    if refined:
        if not response or not present[names[2]] or response.get("input_binding") != combined["sha256"]:
            raise ValueError("refined acquisition proposal lacks its same-input response and checks")
        if set(refined) != set(original):
            raise ValueError("acquisition pass changed proposal fields")
        if any(refined[key] != original[key] for key in original if key not in {"flows", "deployment_findings"}):
            raise ValueError("acquisition pass changed original classification/category fields")
        if len(refined["flows"]) != len(original["flows"]):
            raise ValueError("acquisition pass changed original flow count")
        audits = response.get("dependency_audits", [])
        if not isinstance(audits, list) or any(not isinstance(audit, dict) for audit in audits):
            raise ValueError("refined acquisition proposal lacks a valid dependency-audit array")
        for index, (before, after) in enumerate(zip(original["flows"], refined["flows"])):
            if set(before) != set(after) or any(before[key] != after[key] for key in before if key != "code_path"):
                raise ValueError("acquisition pass changed original flow classification, role, binding or claim")
            old, new = before.get("code_path", []), after.get("code_path", [])
            if len(new) < len(old) or (old and new[-len(old):] != old) or (not old and new):
                raise ValueError("acquisition pass did not preserve every original path step")
            prefix = new[:len(new) - len(old)]
            if prefix:
                choices = [audit for audit in audits if audit.get("flow_index") == index]
                if len(choices) != 1 or choices[0].get("source_prefix") != prefix:
                    raise ValueError("acquisition prefix was not proposed by its unique current-run response")
                prefixes.append({"flow_index": index, "steps": len(prefix), "original_steps_preserved": True})
        previous_candidates = original.get("deployment_findings", [])
        refined_candidates = refined.get("deployment_findings", [])
        if refined_candidates[:len(previous_candidates)] != previous_candidates or len(refined_candidates) < len(previous_candidates):
            raise ValueError("acquisition pass modified original deployment findings")
        proposed = [audit.get("deployment_finding") for audit in audits if audit.get("deployment_finding") is not None]
        candidates = refined_candidates[len(previous_candidates):]
        if len(refined_candidates) > 4:
            raise ValueError("acquisition pass appended too many deployment candidates")
        for candidate in candidates:
            if candidate not in proposed:
                raise ValueError("acquisition pass appended an unproposed deployment candidate")
            proposed.remove(candidate)
        prepended_notes = [note for note in notes if note.get("reason") == "source_prefix_prepended"]
        appended_notes = [note for note in notes if note.get("reason") == "deployment_candidate_appended"]
        if len(prepended_notes) != len(prefixes) or len(appended_notes) != len(candidates):
            raise ValueError("acquisition check counts differ from actual unreviewed changes")
        if sorted((note.get("flow_index"), note.get("prefix_steps"), note.get("original_steps_preserved"))
                  for note in prepended_notes) != sorted((row["flow_index"], row["steps"], True) for row in prefixes):
            raise ValueError("acquisition prefix notes differ from the actual preserved paths")
    elif any(stage.get("stage") == "acquisition_pass" and stage.get("status") == "completed"
             for stage in result.get("stages", [])):
        raise ValueError("completed acquisition stage lacks its refined automatic proposal")
    safe_notes = []
    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("acquisition check note must be an object")
        safe = {key: value for key, value in note.items() if key in {
            "flow_index", "finding_index", "citation_index", "prefix_steps", "quotation_issues",
            "original_steps_preserved", "independent_review_required"} and isinstance(value, (int, bool))}
        safe.update({key: base.code(note.get(key)) for key in ("status", "reason")})
        if note.get("error"):
            safe["error_code"] = base.error_code(note["error"])
        if isinstance(note.get("errors"), list):
            safe["error_codes"] = [base.error_code(value) for value in note["errors"]]
        safe_notes.append(safe)
    audits = response.get("dependency_audits", [])
    audits = audits if isinstance(audits, list) else []
    audit_summaries = []
    for audit in audits:
        if not isinstance(audit, dict):
            continue
        audit_summaries.append({"flow_index": audit.get("flow_index"),
            "evaluation_location": {"status": base.code(audit.get("evaluation_location", {}).get("status")),
                "summary": projector.prose(audit.get("evaluation_location", {}).get("description"))},
            "first_knowledge": {"status": base.code(audit.get("first_knowledge", {}).get("status")),
                "summary": projector.prose(audit.get("first_knowledge", {}).get("description"))},
            "observation_relation": {"status": base.code(audit.get("observation_relation", {}).get("status")),
                "summary": projector.prose(audit.get("observation_relation", {}).get("description"))},
            "candidate_proposed": audit.get("deployment_finding") is not None,
            "reason": projector.prose(audit.get("reason"))})
    summary = {"status": "applied_unreviewed_proposal" if refined else "attempt_failed_or_unapplied",
        "artifact_presence": present, "source_prefixes": prefixes, "appended_candidate_count": len(candidates),
        "classification_fields_preserved": True if refined else None, "checks": safe_notes,
        "dependency_audits": audit_summaries,
        "trust": "untrusted_supplemental_proposal_independent_review_required"}
    audit = {"status": "passed", "same_current_run_model_input_verified": True,
        "original_automatic_proposal_verified": True, "evaluation_label_fields_found": 0,
        "request_sha256": base.digest(directory / names[0]),
        "original_proposal_sha256": base.digest(directory / "extraction.json"),
        "response_sha256": base.digest(directory / names[1]) if present[names[1]] else None,
        "refined_proposal_sha256": base.digest(directory / names[3]) if refined else None,
        "only_prefix_and_appended_candidate_changes_verified": True if refined else None}
    return summary, audit


def review_payload_audit(directory, combined, extraction):
    request = base.read_json(directory / "review.request.json", optional=True)
    contract = base.read_json(directory / "review.contract.json", optional=True)
    if not request and not contract:
        return {"status": "not_reached"}
    if not request or not contract:
        raise ValueError("review request and frozen review contract must both exist")
    if base.label_fields(request):
        raise ValueError("evaluation-label fields found in frozen review request")
    if not combined or contract.get("engine_version") != 7:
        raise ValueError("review request lacks its V7 combined snapshot")
    content = bound_content(combined)
    if request != {**content, "proposal": extraction}:
        raise ValueError("review request is not the exact model input and effective automatic proposal")
    if (contract.get("input_binding") != combined["sha256"]
            or contract.get("review_input_sha256") != json_hash(request)
            or contract.get("prompt_sha256") != hashlib.sha256(contract["prompt"].encode()).hexdigest()
            or contract.get("schema_sha256") != json_hash(contract["schema"])):
        raise ValueError("frozen review prompt/schema/payload binding is invalid")
    return {"status": "passed", "input_binding": combined["sha256"],
            "proposal_matches_effective_automatic_extraction": True, "evaluation_label_fields_found": 0,
            **{key: contract[key] for key in ("prompt_sha256", "schema_sha256", "review_input_sha256")}}


def attempt(directory, run, paper_id, source):
    result = base.read_json(directory / "result.json")
    if result.get("status") not in {"completed", "failed"}:
        raise ValueError("V7 attempt is not terminal")
    for name in ("report.json", "report.html", "report.md"):
        if not (directory / name).is_file():
            raise ValueError("V7 attempt lacks terminal reports")
    if result.get("source") != source or result.get("requested_workflow") != "automatic_from_paper":
        raise ValueError("V7 attempt is not a fresh audit of the original frozen paper URL")
    if result["status"] == "completed" and result.get("schema_version") != 7:
        raise ValueError("completed V7 attempt has another decision schema")
    if result["status"] == "failed" and (result.get("verdict") != "technical_failure" or result.get("inconsistency") is not None):
        raise ValueError("technical failure was incorrectly used as a paper judgment")
    for stage in result.get("stages", []):
        if stage.get("stage") == "extraction" and stage.get("status") == "completed" and stage.get("execution") != "fresh_model_call":
            raise ValueError("V7 pilot loaded an existing proposal instead of fresh extraction")
        if stage.get("stage") == "declared_contract" and stage.get("status") == "completed" and stage.get("execution") != "fresh_paper_only_call":
            raise ValueError("V7 pilot loaded an existing declaration instead of fresh paper input")
    request = base.read_json(directory / "request.json", optional=True)
    combined = base.read_json(directory / "combined_input.json", optional=True)
    repo = base.read_json(directory / "repository.json", optional=True)
    filename = result.get("effective_extraction_file", "extraction.json")
    if base.relative_path(filename) != filename or "/" in filename:
        raise ValueError("invalid effective extraction artifact name")
    extraction = base.read_json(directory / filename, optional=True)
    discovery = base.read_json(directory / "source_discovery.json", optional=True)
    acquisition_response = base.read_json(directory / "acquisition_pass.response.json", optional=True)
    projector = base.Projector(result, extraction, combined, acquisition_response)
    inference = inference_summary(directory)
    declared, declared_audit, declared_spans = prior.contract_summary(directory, result, inference)
    if result["status"] == "completed" and (not inference["calls"] or inference["calls"][-1]["stage"] not in {
            "semantic_review", "semantic_review_retry1"} or inference["calls"][-1]["status"] not in SUCCESS):
        raise ValueError("completed V7 result lacks a completed independent review")
    input_audit = base.input_audit(directory, request, combined)
    input_audit["paper_only_declaration"] = declared_audit
    input_audit["frozen_review"] = review_payload_audit(directory, combined, extraction)
    acquisition, acquisition_audit = acquisition_summary(directory, combined, result, projector)
    input_audit["acquisition_pass"] = acquisition_audit
    row = {"paper_id": paper_id, "paper_name": base.PAPERS[paper_id], "run_id": run.name,
        "attempt_id": directory.relative_to(run).as_posix(), "selected_final": True,
        "cohort_type": "fresh_v7_url_only_three_category_audit",
        "status": result["status"], "paper_verdict": result.get("verdict"),
        "knowledge_boundary_verdict": result.get("knowledge_boundary_verdict"),
        "inconsistency": result.get("inconsistency"), "source": base.public_url(source),
        "reason": projector.prose(result.get("reason")), "duration_seconds": result.get("duration_seconds"),
        "error_code": base.error_code(result["error"]) if result.get("error") else None,
        "document_sha256": base.code(result.get("document_sha256")),
        "confirmed_issue_types": [value for value in result.get("confirmed_issue_types", []) if value in CATEGORIES],
        "stages": prior.safe_stages(result.get("stages", [])), "input_audit": input_audit,
        "inference": inference, "declared_contract": declared,
        "acquisition_pass": acquisition,
        "repository": base.repository_summary(repo, projector),
        "input_channels": base.channel_summary(result, combined, extraction, projector),
        "claims": [safe_claim(claim, projector) for claim in result.get("evidence", [])],
        "category_coverage": {"complete": result.get("category_coverage", {}).get("complete"),
            "categories": [{"category": value.get("category"), "complete": value.get("complete"),
                "proposed_status": value.get("proposed_status"), "locators": projector.locators(value.get("locators", []))}
                for value in result.get("category_coverage", {}).get("categories", [])]},
        "source_discovery": {"status": base.code(discovery.get("status")), "reason": projector.prose(discovery.get("reason")),
                             "repository_url": base.public_url(discovery.get("repository"))},
        "source_artifacts": {path.name: path.relative_to(run).as_posix() for path in directory.glob("*.json")},
    }
    for target, assessment_name in (("construction", "construction_assessment"), ("deployment", "deployment_assessment")):
        assessment = result.get(assessment_name, {})
        row[target] = {"finding_count": len(assessment.get("findings", [])),
            "blocks_negative": assessment.get("blocks_negative"),
            "coverage": assessment.get("coverage"), "general_clean_established": assessment.get("general_clean_established"),
            "proposed_finding_count": len(extraction.get(target + "_findings", []))}
    row = prior.redact_contract_prose(row, declared_spans)
    base.assert_public_safe(row, projector.omitted_spans | declared_spans)
    return row


def build(run, public_dir, paper_ids=None):
    run, public_dir = Path(run).resolve(strict=True), Path(public_dir).resolve()
    paper_ids = tuple(paper_ids) if paper_ids is not None else PAPER_IDS
    if (not paper_ids or len(paper_ids) != len(set(paper_ids))
            or not set(paper_ids) <= set(PAPER_IDS)):
        raise ValueError("paper IDs must be a nonempty unique subset of muzzle/obliinjection")
    combined_dir = run / "combined"
    if combined_dir.exists() or public_dir.exists():
        raise FileExistsError("refusing to overwrite existing V7 report outputs")
    if public_dir.is_relative_to(run) or run.is_relative_to(public_dir):
        raise ValueError("public report output must be separate from the source run")
    before = raw_manifest(run, public_dir)
    config = base.read_json(run / "frozen_config.json")
    if (config.get("engine_version") != 7 or {paper.get("id") for paper in config.get("papers", [])} != set(paper_ids)
            or len(config.get("papers", [])) != len(paper_ids)):
        raise ValueError("V7 run must freeze exactly the selected paper IDs with engine version 7")
    acquisition_passes = config.get("acquisition_passes", 0)
    if acquisition_passes not in (0, 1):
        raise ValueError("V7 allows at most one acquisition follow-up pass")
    per_paper_cap = 5 + acquisition_passes
    total_cap = per_paper_cap * len(paper_ids)
    if config.get("max_calls_per_paper") != per_paper_cap or config.get("max_total_cli_calls") != total_cap:
        raise ValueError("V7 call caps do not match the selected cohort and acquisition-pass setting")
    retries = config.get("review_retries", config.get("review_retry_limit"))
    if retries != 1:
        raise ValueError("V7 pilot must freeze one possible independent-review retry")
    if {path.name for path in (run / "audits").iterdir() if path.is_dir()} != set(paper_ids):
        raise ValueError("V7 run has unexpected audit attempts or papers")
    sources = {paper["id"]: paper["source"] for paper in config["papers"]}
    if any(base.public_url(source) != source for source in sources.values()):
        raise ValueError("V7 pilot inputs must be original plain paper URLs")
    rows = [attempt(run / "audits" / paper_id, run, paper_id, sources[paper_id]) for paper_id in paper_ids]
    for row in rows:
        if row["inference"]["invocation_count"] is None or row["inference"]["invocation_count"] > per_paper_cap:
            raise ValueError("V7 attempt is missing a final ledger or exceeds its call cap")
        if row["inference"]["observed_model_phases"].count("acquisition_pass") > acquisition_passes:
            raise ValueError("recorded acquisition calls exceed the frozen pipeline setting")
        for call in row["inference"]["calls"]:
            if call["requested_model"] != config.get("requested_model"):
                raise ValueError("requested model differs from frozen V7 configuration")
        settings = {**row["input_audit"]["limits"], **row["input_audit"]}
        for key in ("max_input_chars", "max_code_chars", "source_fetch", "require_source"):
            if settings.get(key) is not None and settings[key] != config.get(key):
                raise ValueError("V7 input limits differ from frozen settings")
    calls = sum(row["inference"]["invocation_count"] for row in rows)
    if calls > total_cap:
        raise ValueError("V7 total call cap exceeded")
    counts = base.counts(rows)
    counts["inconsistency_flags"]["null"] = counts["inconsistency_flags"].pop("none")
    summary = {"papers": counts, "fresh_attempts": counts, "model_invocation_count": calls,
        "failed_invocation_count": sum(row["inference"]["failed_invocation_count"] for row in rows),
        "review_retry_count": sum(row["inference"]["review_retry_count"] for row in rows),
        "claim_category_counts": {category: dict(Counter(claim.get("claim_result", "unresolved")
            for row in rows for claim in row["claims"] if claim.get("issue_type") == category)) for category in CATEGORIES},
        "usage": {key: sum(row["inference"]["usage"].get(key, 0) for row in rows) for key in sorted(base.TOKEN_KEYS)},
        "usage_reporting_complete": all(row["inference"]["usage_reporting_complete"] for row in rows),
        "actual_model_unknown_invocations": sum(row["inference"]["actual_model_unknown_invocations"] or 0 for row in rows),
        "denominator_note": str(len(paper_ids)) + " fresh original-URL audit(s) only: " + ", ".join(base.PAPERS[key] for key in paper_ids)
            + ". This cohort is separate from earlier runs; older outcomes, curated findings and expected labels do not enter its denominator or model input.",
        "scope_note": "A typed paper result combines knowledge-boundary violations, explicit construction-contract mismatches and bounded task-acquisition/deployment gaps. These types are retained separately. A deployment gap does not prove forbidden or impossible knowledge, historical execution, or an ASR effect.",
        "usage_note": "At most " + str(per_paper_cap) + " wrapper calls per paper, " + str(total_cap)
            + " total; at most one identical-payload review retry and " + str(acquisition_passes)
            + " acquisition pass. Failed calls remain counted. Cumulative ledgers are counted once. Unknown actual model IDs remain null; unreported usage does not prove zero use."}
    report = {"schema_version": "v7-url-pilot-summary-v1", "run_id": run.name, "created_at": config.get("created_at"),
        "code_commit": base.code(config.get("code_commit")), "frozen_config_sha256": base.digest(run / "frozen_config.json"),
        "frozen_limits": {key: config.get(key) for key in ("provider", "requested_model", "engine_version",
            "max_calls_per_paper", "max_total_cli_calls", "model_timeout_seconds", "max_input_chars", "max_code_chars", "source_fetch", "require_source")},
        "review_retry_limit": retries,
        "acquisition_passes": acquisition_passes, "paper_ids": list(paper_ids),
        "code_files_sha256": {name: sha for name, sha in config.get("code_files", {}).items()
                              if base.relative_path(name) and base.HEX.fullmatch(str(sha))},
        "summary": summary, "paper_results": rows, "attempts": rows,
        "builder": {"script": "scripts/summarize_v7_pilot.py", "script_sha256": base.digest(Path(__file__)),
            "helpers": {path.name: base.digest(path) for path in (Path(base.__file__), Path(prior.__file__))}},
        "public_evidence_policy": "Semantic findings, grounded metadata/offsets/hashes, process stages, diagnostic correlation data and usage only. No source payloads, original quotations, prompts, raw data, credentials, private paths or declaration narrative."}
    base.assert_public_safe(report)
    if raw_manifest(run, public_dir) != before:
        raise ValueError("run artifacts changed during report construction; wait for all writers")
    manifest = {"schema_version": "v7-url-pilot-process-manifest-v1", "hash_algorithm": "sha256",
        "path_base": "relative to run_id directory", "scope": "every raw run file, including driver and original per-paper reports",
        "exclusions": sorted(base.DERIVATIVES), "files": before,
        "builder_sha256": report["builder"]["script_sha256"], "helper_sha256": report["builder"]["helpers"]}
    base.assert_public_safe(manifest)
    return report, manifest, combined_dir


def markdown_text(value):
    return str(value if value is not None else "unknown").replace("|", "\\|").replace("\n", " ")


def location_label(locator):
    if locator.get("source_kind") == "paper":
        return "paper " + str(locator.get("segment_id"))
    label = str(locator.get("path", locator.get("segment_id", "unlocated")))
    if locator.get("line_start") is not None:
        label += ":" + str(locator["line_start"])
        if locator.get("line_end") != locator.get("line_start"):
            label += "–" + str(locator.get("line_end"))
    return label


def location_url(locator):
    source = locator.get("repository_source", "") or ""
    revision = locator.get("repository_revision")
    if source.startswith("https://github.com/") and revision and locator.get("path"):
        url = source + "/blob/" + quote(revision, safe="") + "/" + quote(locator.get("original_path", locator["path"]), safe="/")
        return url + "#L" + str(locator["line_start"]) if locator.get("line_start") else url
    return None


def render_markdown(report):
    summary = report["summary"]
    lines = ["# V7: original-URL audit results", "", summary["denominator_note"], "", summary["scope_note"], "",
        "| Paper | Audit status | Paper result | Knowledge-boundary result | Confirmed types | Calls / review retries |",
        "| --- | --- | --- | --- | --- | --- |"]
    for row in report["paper_results"]:
        values = (row["paper_name"], row["status"], row["paper_verdict"], row["knowledge_boundary_verdict"],
                  ", ".join(row["confirmed_issue_types"]) or "none", str(row["inference"]["invocation_count"]) + " / " + str(row["inference"]["review_retry_count"]))
        lines.append("| " + " | ".join(markdown_text(value) for value in values) + " |")
    lines += ["", summary["usage_note"], "", "Full structured metadata: [report.json](report.json). Original artifact hashes: [process_manifest.json](process_manifest.json).", ""]
    for row in report["paper_results"]:
        lines += ["## " + row["paper_name"], "", "Original input: " + row["source"], "",
            "Result: **" + row["paper_verdict"] + "**; reason: " + str(row["reason"]) + ". Audit error: " + str(row["error_code"] or "none") + ".", "",
            "### Process", "", "| Stage | Status | Details |", "| --- | --- | --- |"]
        for stage in row["stages"]:
            details = stage.get("reason", stage.get("reason_code", stage.get("error_code", stage.get("execution", ""))))
            lines.append("| " + " | ".join(markdown_text(value) for value in (stage.get("stage"), stage.get("status"), details)) + " |")
        acquisition = row["acquisition_pass"]
        if acquisition["status"] != "not_requested_or_not_reached":
            lines += ["", "### Acquisition evidence pass", "", "Status: " + acquisition["status"] + ". This is a current-run supplemental proposal, subsequently subject to full independent review.", "",
                "Original classification fields preserved: " + str(acquisition["classification_fields_preserved"]) + "; source prefixes proposed: "
                + str(len(acquisition["source_prefixes"])) + "; new deployment candidates proposed: " + str(acquisition["appended_candidate_count"]) + ".", ""]
            for audit in acquisition["dependency_audits"]:
                lines += ["- Flow " + str(audit["flow_index"]) + ": " + str(audit["reason"]),
                    "- First knowledge (" + str(audit["first_knowledge"]["status"]) + "): " + str(audit["first_knowledge"]["summary"]),
                    "- Observation relation (" + str(audit["observation_relation"]["status"]) + "): " + str(audit["observation_relation"]["summary"])]
            lines += ["", "| Flow | Check status | Mechanical check |", "| --- | --- | --- |"]
            for note in acquisition["checks"]:
                lines.append("| " + " | ".join(markdown_text(value) for value in (note.get("flow_index"), note.get("status"), note.get("reason"))) + " |")
        repo = row["repository"]
        lines += ["", "Repository: " + str(repo["url"]) + " at `" + str(repo["revision"]) + "`. Data files: " + str(repo["data_file_count"]) + "; exact excerpts: " + str(repo["data_witness_count"]) + ".", "",
            "### Findings and unresolved checks", ""]
        for index, claim in enumerate(row["claims"], 1):
            lines += ["#### " + str(index) + ". " + str(claim.get("claim", "Unnamed claim")), "",
                "Type: `" + str(claim.get("issue_type")) + "`; result: **" + str(claim.get("claim_result")) + "**; reason: `" + str(claim.get("reason")) + "`.", "",
                "Scope: " + (json.dumps(claim["scope"], ensure_ascii=False) if isinstance(claim["scope"], dict) else str(claim["scope"])) + ".", ""]
            for label, fact in {**claim["positive_facts"], **claim["axes"]}.items():
                lines.append("- " + label + ": " + str(fact.get("summary", "")) + " (supported=" + str(fact.get("supported")) + ").")
            if claim.get("comparison"):
                lines.append("- Comparison: " + str(claim["comparison"].get("summary")))
            if claim.get("semantic_mapping"):
                lines.append("- Mapping: " + str(claim["semantic_mapping"].get("summary")))
            if claim.get("knowledge_provenance"):
                fact = claim["knowledge_provenance"]
                lines.append("- Acquisition: " + str(fact.get("status")) + "; " + str(fact.get("summary")))
            if claim.get("independent_review", {}).get("reason"):
                lines.append("- Independent review: " + claim["independent_review"]["reason"])
            lines += ["", "Locations:", ""]
            for loc in claim["locators"]:
                label, url = location_label(loc), location_url(loc)
                lines.append("- " + ("[" + label + "](" + url + ")" if url else label))
            lines += [""]
        lines += ["### Invocation ledger", "", "| Call | Stage | Status | Input / output tokens | Requested / actual model |", "| --- | --- | --- | --- | --- |"]
        for call in row["inference"]["calls"]:
            values = (call["invocation"], call["stage"], call["status"],
                str(call["usage"].get("input_tokens", "unreported")) + " / " + str(call["usage"].get("output_tokens", "unreported")),
                str(call["requested_model"]) + " / " + str(call["actual_model"] or "unknown"))
            lines.append("| " + " | ".join(markdown_text(value) for value in values) + " |")
        declared = row["declared_contract"]
        lines += ["", "Paper-only declaration: " + str(declared["trust"]) + "; " + str(declared["counts"]["located_citations"]) + "/" + str(declared["counts"]["proposed_citations"]) + " citations mechanically located. The proposal is not permission evidence.", "",
            "Input-channel closure: " + str(row["input_channels"]["complete"]) + "; category closure: " + str(row["category_coverage"]["complete"]) + ". A confirmed bounded issue does not require all other candidates to be resolved.", ""]
    return "\n".join(lines)


def render_html(report):
    escape = lambda value: html.escape(str(value if value is not None else "unknown"))
    summary_rows = "".join("<tr>" + "".join("<td>" + escape(value) + "</td>" for value in (
        row["paper_name"], row["status"], row["paper_verdict"], row["knowledge_boundary_verdict"],
        ", ".join(row["confirmed_issue_types"]) or "none", row["inference"]["invocation_count"], row["inference"]["review_retry_count"])) + "</tr>" for row in report["paper_results"])
    sections = []
    for row in report["paper_results"]:
        sections += ["<article><h2>" + escape(row["paper_name"]) + "</h2><p>Original paper: <a href=\"" + escape(row["source"]) + "\">" + escape(row["source"]) + "</a></p>",
            "<p><strong>" + escape(row["paper_verdict"]) + "</strong> · " + escape(row["reason"]) + "</p><h3>Process</h3><ol>"]
        for stage in row["stages"]:
            detail = stage.get("reason", stage.get("reason_code", stage.get("error_code", "")))
            sections.append("<li><strong>" + escape(stage.get("stage")) + "</strong>: " + escape(stage.get("status")) + (" — " + escape(detail) if detail else "") + "</li>")
        acquisition = row["acquisition_pass"]
        sections.append("</ol>")
        if acquisition["status"] != "not_requested_or_not_reached":
            sections.append("<h3>Acquisition evidence pass</h3><p>" + escape(acquisition["status"]) + "; original classification fields preserved="
                + escape(acquisition["classification_fields_preserved"]) + "; proposed source prefixes=" + escape(len(acquisition["source_prefixes"]))
                + "; proposed deployment candidates=" + escape(acquisition["appended_candidate_count"]) + ". Supplemental proposals require the subsequent independent review.</p>")
            for audit in acquisition["dependency_audits"]:
                sections.append("<p><strong>Flow " + escape(audit["flow_index"]) + "</strong>: " + escape(audit["reason"]) + "</p><ul><li>First knowledge ("
                    + escape(audit["first_knowledge"]["status"]) + "): " + escape(audit["first_knowledge"]["summary"]) + "</li><li>Observation relation ("
                    + escape(audit["observation_relation"]["status"]) + "): " + escape(audit["observation_relation"]["summary"]) + "</li></ul>")
            sections.append("<table><thead><tr><th>Flow</th><th>Check status</th><th>Mechanical check</th></tr></thead><tbody>")
            for note in acquisition["checks"]:
                sections.append("<tr>" + "".join("<td>" + escape(value) + "</td>" for value in (note.get("flow_index"), note.get("status"), note.get("reason"))) + "</tr>")
            sections.append("</tbody></table>")
        repo = row["repository"]
        sections += ["<p>Source: " + escape(repo["url"]) + " @ <code>" + escape(repo["revision"]) + "</code>; selected files " + escape(repo["coverage"].get("included_files")) + "; data excerpts " + escape(repo["data_witness_count"]) + ".</p><h3>Findings and unresolved checks</h3>"]
        for claim in row["claims"]:
            sections.append("<section class=\"claim " + escape(claim.get("claim_result")) + "\"><h4>" + escape(claim.get("claim")) + "</h4><p><code>" + escape(claim.get("issue_type")) + "</code> · <strong>" + escape(claim.get("claim_result")) + "</strong></p><p>" + escape(claim.get("reason")) + "</p><p>Scope: " + escape(json.dumps(claim["scope"], ensure_ascii=False) if isinstance(claim["scope"], dict) else claim["scope"]) + "</p><ul>")
            for label, fact in {**claim["positive_facts"], **claim["axes"]}.items():
                sections.append("<li><strong>" + escape(label) + "</strong>: " + escape(fact.get("summary")) + " <small>(supported=" + escape(fact.get("supported")) + ")</small></li>")
            for label in ("comparison", "semantic_mapping", "knowledge_provenance"):
                if claim.get(label):
                    sections.append("<li><strong>" + escape(label) + "</strong>: " + escape(claim[label].get("summary")) + "</li>")
            if claim["independent_review"].get("reason"):
                sections.append("<li><strong>Independent review</strong>: " + escape(claim["independent_review"]["reason"]) + "</li>")
            sections.append("</ul><details><summary>Exact paper/code locations and provenance hashes</summary><ul>")
            for loc in claim["locators"]:
                label, url = location_label(loc), location_url(loc)
                sections.append("<li>" + ("<a href=\"" + escape(url) + "\">" + escape(label) + "</a>" if url else escape(label)) + " <small>" + escape((loc.get("file_sha256") or loc.get("paper_sha256") or "")[:12]) + "</small></li>")
            sections.append("</ul></details></section>")
        sections.append("<h3>Invocation ledger</h3><table><thead><tr><th>Call</th><th>Stage</th><th>Status</th><th>Input/output tokens</th><th>Requested/actual</th></tr></thead><tbody>")
        for call in row["inference"]["calls"]:
            sections.append("<tr>" + "".join("<td>" + escape(value) + "</td>" for value in (
                call["invocation"], call["stage"], call["status"],
                str(call["usage"].get("input_tokens", "unreported")) + "/" + str(call["usage"].get("output_tokens", "unreported")),
                str(call["requested_model"]) + "/" + str(call["actual_model"] or "unknown"))) + "</tr>")
        sections.append("</tbody></table><details><summary>Input isolation, declaration, coverage and diagnostic metadata</summary><pre>" + escape(json.dumps({key: row[key] for key in ("input_audit", "declared_contract", "category_coverage", "input_channels", "repository", "inference")}, ensure_ascii=False, indent=2)) + "</pre></details></article>")
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>V7 URL pilot</title>'
        '<style>body{font:15px system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#172331;line-height:1.5}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:.55rem;border:1px solid #ccd3dd;text-align:left}article{margin:2rem 0;border-top:2px solid #8795a8;padding-top:1rem}.claim{padding:.8rem 1rem;margin:1rem 0;border-left:4px solid #a6afba;background:#f5f7f9}.confirmed{border-color:#356eb5}.unresolved{border-color:#be8c25}.refuted{border-color:#419367}summary{cursor:pointer;padding:.5rem 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;background:#f4f6f8;padding:1rem}code{overflow-wrap:anywhere}small{color:#566476}</style>'
        '<h1>V7: original-URL audit results</h1><p>' + escape(report["summary"]["denominator_note"]) + '</p><p>' + escape(report["summary"]["scope_note"]) + '</p><table><thead><tr><th>Paper</th><th>Audit</th><th>Paper result</th><th>Knowledge boundary</th><th>Confirmed types</th><th>Calls</th><th>Review retries</th></tr></thead><tbody>' + summary_rows + '</tbody></table><p>' + escape(report["summary"]["usage_note"]) + '</p><p><a href="report.json">Structured report</a> · <a href="process_manifest.json">Original artifact hashes</a>.</p>' + ''.join(sections) + '</html>\n')


def write_outputs(report, manifest, combined_dir, public_dir):
    payloads = {"report.json": json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        "process_manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        "report.md": render_markdown(report), "report.html": render_html(report)}
    created = []
    try:
        for directory in (combined_dir, public_dir):
            directory.mkdir(parents=True, exist_ok=False)
            created.append(directory)
            for name, payload in payloads.items():
                with (directory / name).open("x", encoding="utf-8") as stream:
                    created.append(directory / name)
                    stream.write(payload)
    except BaseException:
        for path in reversed(created):
            path.rmdir() if path.is_dir() else path.unlink(missing_ok=True)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--public-dir", required=True, type=Path)
    parser.add_argument("--paper-ids", nargs="+", choices=PAPER_IDS,
                        help="Explicit separate cohort subset; default freezes both original pilot papers")
    args = parser.parse_args(argv)
    try:
        report, manifest, combined = build(args.run_dir.resolve(strict=True), args.public_dir.resolve(), args.paper_ids)
        write_outputs(report, manifest, combined, args.public_dir.resolve())
        print(json.dumps({"run_id": report["run_id"], "papers": len(report["paper_results"]),
            "calls": report["summary"]["model_invocation_count"], "review_retries": report["summary"]["review_retry_count"],
            "raw_artifacts": len(manifest["files"])}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
