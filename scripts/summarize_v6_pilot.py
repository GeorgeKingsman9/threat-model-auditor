#!/usr/bin/env python3
"""Summarize finished V6 pilot artifacts offline without copying source payloads.

    python3 -B scripts/summarize_v6_pilot.py outputs/RUN \
      --preflight-dir outputs/PREFLIGHT --preflight-dir outputs/DISCOVERY_RETRY \
      --public-dir docs/results/2026-11-21-v6-pilot

No inference, network access, repository execution, or evaluation-label lookup.
All fresh attempts must have final result/report artifacts. Preparation-only
preflights remain a separate zero-inference cohort, never paper verdicts.
Existing output directories are refused. Only the standard library is used.
"""

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re


TERMINAL = {"completed", "failed", "technical_failure", "error", "invalid", "blocked"}
PAPERS = {"aspi": "ASPI", "muzzle": "MUZZLE", "obliinjection": "ObliInjection",
          "topicattack": "TopicAttack"}
TOKEN_KEYS = {"input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"}
CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:+/-]{0,199}$")
HEX = re.compile(r"^[a-fA-F0-9]{40,64}$")
PRIVATE = re.compile(r"(?:/(?:Users|home|private|tmp|var)/[^\s\"<>`]*|[A-Za-z]:\\[^\s\"<>`]*)")
SECRET = re.compile(r"(?i)(?:bearer\s+\S+|\b(?:sk|ghp|github_pat)[-_][A-Za-z0-9_-]{12,}|"
                    r"(?:api[_-]?key|access[_-]?token|authorization|password)\s*[:=]\s*\S+)")
EVAL_FIELDS = {"gold", "gold_label", "gold_labels", "expected", "expected_label",
               "expected_labels", "expected_verdict", "matches_gold", "curated_cases",
               "previous_proposal", "reproduction_evidence"}
FORBIDDEN_PUBLIC = {"quote", "text", "raw_base64", "prompt", "context", "reading_order_text"}
DERIVATIVES = {"combined", "public", "derivatives", "generated", "revalidated", "deterministic_revalidation"}
LOCATOR_FIELDS = {"segment_id", "start", "end", "line_start", "line_end", "char_start", "char_end",
                  "byte_start", "byte_end", "record_index", "record_pointer", "document_sha256",
                  "paper_sha256", "file_sha256", "source_kind", "path", "original_path",
                  "repository_revision", "repository_manifest_sha256", "object_id", "sha256"}
COVERAGE_FIELDS = {"complete", "inventory_complete", "raw_complete", "eligible_files", "included_files",
                   "omitted_files", "excluded_entries", "characters", "max_characters", "total_records",
                   "sampled_records", "omitted_records", "oversized_records", "oversized_pointers",
                   "output_bytes", "max_output_bytes"}
STAGE_FIELDS = {"stage", "name", "status", "segments", "characters", "sha256", "revision",
                "manifest_sha256", "source_segments", "discovery_status", "applicability", "flow_count",
                "execution", "issues_before", "accepted_replacements", "remaining_issues",
                "classification_fields_modified", "verdict", "previous_verdict", "model_calls", "evidence_edited"}


def read_json(path, optional=False):
    if optional and not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path.name}")
    return value


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def code(value):
    return value if isinstance(value, str) and CODE.fullmatch(value) and not PRIVATE.search(value) else None


def numbers(value, keys=None):
    return {key: item for key, item in (value or {}).items()
            if (keys is None or key in keys) and isinstance(item, (bool, int, float))}


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    path = PurePosixPath(value)
    return value if not path.is_absolute() and ".." not in path.parts and not PRIVATE.search(value) else None


def public_url(value):
    from urllib.parse import urlsplit, urlunsplit
    if not isinstance(value, str):
        return None
    parts = urlsplit(value)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        return None
    return urlunsplit((parts.scheme, parts.hostname, parts.path, "", ""))


def collect_quotes(value):
    found = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"quote", "raw_base64"} and isinstance(item, str) and len(item) >= 12:
                found.add(item)
            elif isinstance(item, (dict, list)):
                found.update(collect_quotes(item))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_quotes(item))
    return found


class Projector:
    def __init__(self, *inputs):
        self.omitted_spans = set().union(*(collect_quotes(value) for value in inputs))

    def prose(self, value):
        if not isinstance(value, str):
            return None
        value = SECRET.sub("[redacted]", PRIVATE.sub("[local path omitted]", value))
        for span in sorted(self.omitted_spans, key=len, reverse=True):
            value = value.replace(span, "[citation content omitted]")
        value = re.sub(r"```[\s\S]*?```", "[code omitted]", value)
        # Long literal expressions belong in the original evidence, not the report.
        return re.sub(r"`[^`\n]{80,}`", "[code omitted]", value)

    def metadata(self, value):
        if isinstance(value, dict):
            return {key: self.metadata(item) for key, item in value.items()
                    if key.lower() not in FORBIDDEN_PUBLIC and not key.lower().endswith("_quote")}
        if isinstance(value, list):
            return [self.metadata(item) for item in value]
        return self.prose(value) if isinstance(value, str) else value

    def locators(self, value):
        result = []
        if isinstance(value, dict):
            if "segment_id" in value or "path" in value and "line_start" in value:
                row = {}
                for key in LOCATOR_FIELDS & value.keys():
                    item = value[key]
                    if key in {"path", "original_path"}:
                        row[key] = relative_path(item)
                    elif isinstance(item, (bool, int, float, type(None))):
                        row[key] = item
                    elif isinstance(item, str):
                        row[key] = self.prose(item)
                if value.get("repository_source"):
                    row["repository_source"] = public_url(value["repository_source"])
                if isinstance(value.get("data_witness"), dict):
                    row["data_witness"] = self.metadata({key: item for key, item in value["data_witness"].items()
                        if key in LOCATOR_FIELDS | {"coverage"}})
                result.append(row)
            for key, item in value.items():
                if key not in FORBIDDEN_PUBLIC and isinstance(item, (dict, list)):
                    result.extend(self.locators(item))
        elif isinstance(value, list):
            for item in value:
                result.extend(self.locators(item))
        return list({json.dumps(row, sort_keys=True): row for row in result}.values())


def error_code(value, stage=None):
    if code(value):
        return value
    message = str(value).lower()
    if "timeout" in message or "timed out" in message:
        return "timeout"
    if "source" in message and ("resolved" in message or "required" in message):
        return "required_source_unavailable"
    if "exceeds" in message and "limit" in message:
        return "configured_input_limit_exceeded"
    if "schema" in message:
        return "schema_validation_error"
    return (code(stage) + "_error") if code(stage) else "technical_error"


def coverage(value, projector):
    result = numbers(value, COVERAGE_FIELDS)
    for key in ("scope", "reason", "sampling"):
        if key in value:
            result[key] = projector.prose(value[key])
    result["omission_reasons"] = [projector.prose(x) for x in value.get("omission_reasons", [])]
    return result


def stages(value, projector):
    rows = []
    for item in value:
        row = {key: projector.prose(v) if isinstance(v, str) else v for key, v in item.items()
               if key in STAGE_FIELDS and isinstance(v, (str, bool, int, float, type(None)))}
        if item.get("reason"):
            row["reason_code"] = code(item["reason"])
            if row["reason_code"] is None:
                row["reason"] = projector.prose(item["reason"])
        if item.get("error"):
            row["error_code"] = error_code(item["error"], item.get("stage"))
        if isinstance(item.get("coverage"), dict):
            row["coverage"] = coverage(item["coverage"], projector)
        rows.append(row)
    return rows


def inference(directory, preflight=False):
    path = directory / "inference.json"
    if preflight:
        if path.exists() or list(directory.glob("inference.*.json")):
            raise ValueError("preflight contains inference artifacts; it must be a separate inference cohort")
        return {"invocation_count": 0, "calls": [], "usage": {}, "usage_reporting_complete": True,
                "recording_status": "preparation_only_no_inference_artifacts", "actual_model_unknown_invocations": 0}
    if not path.exists():
        return {"invocation_count": None, "calls": [], "usage": {}, "usage_reporting_complete": False,
                "recording_status": "final_cumulative_ledger_missing", "actual_model_unknown_invocations": None}
    ledger = read_json(path)
    stage_by_request = {}
    for snapshot in sorted(directory.glob("inference.*.json")):
        for call in read_json(snapshot).get("calls", []):
            stage_by_request.setdefault(call.get("request_sha256"), snapshot.name[10:-5])
    calls = []
    for index, call in enumerate(ledger.get("calls", []), 1):
        calls.append({"invocation": index, "stage": stage_by_request.get(call.get("request_sha256")),
                      "status": code(call.get("status")), "requested_model": code(call.get("requested_model")),
                      "actual_model": code(call.get("actual_model")),
                      "actual_models": [code(x) for x in call.get("actual_models", [])],
                      "request_sha256": code(call.get("request_sha256")), "usage": numbers(call.get("usage"), TOKEN_KEYS),
                      "diagnostic_codes": [code(x.get("category")) for x in call.get("diagnostics", []) if isinstance(x, dict)],
                      "execution": numbers(call.get("execution"), {"returncode", "turn_completed", "fatal_error_count", "error_notification_count"})})
    return {"provider": code(ledger.get("provider")), "requested_model": code(ledger.get("model")),
            "max_calls": ledger.get("max_calls"), "invocation_count": len(calls), "calls": calls,
            "usage": numbers(ledger.get("usage"), TOKEN_KEYS), "usage_reporting_complete": ledger.get("usage_reporting_complete") is True,
            "actual_model_unknown_invocations": sum(not x["actual_model"] and not x["actual_models"] for x in calls),
            "preflight_failure_count": len(ledger.get("preflight_failures", [])),
            "preflight_failure_codes": [error_code(x) for x in ledger.get("preflight_failures", [])],
            "recording_status": "final_cumulative_ledger"}


def label_fields(value, prefix=""):
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = prefix + "/" + key
            if key.lower() in EVAL_FIELDS:
                found.append(path)
            if isinstance(item, (dict, list)):
                found.extend(label_fields(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(label_fields(item, prefix + "/" + str(index)))
    return found


def input_audit(directory, request, combined):
    checked = [name for name in ("prepared.json", "combined_input.json", "request.json") if (directory / name).exists()]
    for name in checked:
        if label_fields(read_json(directory / name)):
            raise ValueError(f"evaluation-label fields found in input artifact: {directory.name}/{name}")
    for key, corresponding in (("input_sha256", "sha256"), ("model_content_sha256", "model_content_sha256")):
        if request.get(key) and request.get(key) != combined.get(corresponding):
            raise ValueError(f"input/request binding mismatch: {directory.name}/{key}")
    return {"status": "passed", "checked_artifacts": checked, "evaluation_label_fields_found": 0,
            "scope": "Structured evaluation-label sidecar fields in supplied input artifacts; author data label channels and words inside original source are not evaluation labels. No gold files were opened.",
            "binding_metadata_matches": bool(request and combined),
            "request_hashes": {key: value for key, value in request.items() if key in
                {"prompt_sha256", "input_sha256", "model_content_sha256"} and isinstance(value, str) and HEX.fullmatch(value)},
            "limits": numbers(request, {"max_input_chars", "max_code_chars", "model_data_characters", "input_binding_version"}),
            "source_fetch": code(request.get("source_fetch")), "require_source": request.get("require_source")}


def repository_summary(repo, projector):
    data = []
    witnesses = repo.get("data_witnesses", [])
    for blob in repo.get("data_blobs", []):
        selected = [item for item in witnesses if item.get("path") == blob.get("path")]
        data.append({"path": relative_path(blob.get("path")), "bytes": blob.get("bytes"),
                     "sha256": code(blob.get("sha256")), "object_id": code(blob.get("object_id")),
                     "status": code(blob.get("status")), "coverage": coverage(blob.get("coverage", {}), projector),
                     "witness_count": len(selected),
                     "sampled_record_indices": sorted({x["record_index"] for x in selected if type(x.get("record_index")) is int}),
                     "sampled_record_pointers": sorted({x["record_pointer"] for x in selected if isinstance(x.get("record_pointer"), str)}),
                     "witnesses": [{**{key: item[key] for key in LOCATOR_FIELDS | {"id", "coverage"} if key in item},
                                    "content_sha256": item.get("text_sha256")} for item in selected]})
    expansion = repo.get("evidence_expansion", {})
    return {"url": public_url(repo.get("source")), "revision": code(repo.get("revision")),
            "manifest_sha256": code(repo.get("manifest_sha256")), "coverage": coverage(repo.get("coverage", {}), projector),
            "dependency_snapshot_count": len(repo.get("dependency_snapshots", [])),
            "expansion": {**numbers(expansion, {"added_files", "added_bytes", "data_files", "data_bytes", "data_output_bytes", "data_coverage_complete"}),
                          **{key + "_count": len(expansion.get(key, [])) for key in ("needed", "unresolved", "over_limit", "inspected_paths")}},
            "data_files": projector.metadata(data), "data_file_count": len(data), "data_witness_count": len(witnesses),
            "sampled_file_count": sum(x.get("coverage", {}).get("complete") is False for x in data)}


def channel_summary(result, combined, extraction, projector):
    inventory = combined.get("model_repository", {}).get("input_channels", {})
    final = result.get("channel_coverage", {})
    candidates = inventory.get("candidates", [])
    channels = []
    for row in final.get("channels", []):
        candidate = row.get("candidate", {})
        channels.append({"candidate_id": row.get("candidate_id"), "channel_kind": row.get("channel_kind"),
                         "status": row.get("status"), "reason": row.get("reason"), "flow_index": row.get("flow_index"),
                         "path": relative_path(row.get("path")), "role_hint": code(candidate.get("role_hint")),
                         "phase_hint": code(candidate.get("phase_hint")),
                         "locators": projector.locators([candidate.get("call_anchor", {}), candidate.get("source_anchor", {})])})
    return {"assessment_status": "reviewed" if final else "not_assessed",
            "candidate_count": final.get("candidate_count", len(candidates)), "complete": final.get("complete"),
            "truncated": final.get("truncated", inventory.get("truncated")),
            "discovery_complete": inventory.get("discovery_complete"), "statistics": numbers(inventory.get("statistics")),
            "limits": numbers(inventory.get("limits")), "limitations": [projector.prose(x) for x in inventory.get("limitations", [])],
            "candidate_kind_counts": dict(Counter(x.get("channel_kind", "unknown") for x in candidates)),
            "status_counts": dict(Counter(x.get("status", "unknown") for x in channels)),
            "kind_status_counts": dict(Counter(x.get("channel_kind", "unknown") + ":" + x.get("status", "unknown") for x in channels)),
            "validation_error_codes": [error_code(x) for x in final.get("validation_errors", [])],
            "candidates": [{"candidate_id": x.get("id"), "channel_kind": x.get("channel_kind"),
                            "path": relative_path(x.get("path")), "role_hint": code(x.get("role_hint")),
                            "phase_hint": code(x.get("phase_hint")),
                            "locators": projector.locators([x.get("call_anchor", {}), x.get("source_anchor", {})])} for x in candidates],
            "proposed_assessment_counts": dict(Counter(x.get("status", "unknown") for x in extraction.get("channel_assessments", []))),
            "channels": channels}


def safe_claim(row, projector):
    claim = {key: projector.prose(row[key]) for key in ("id", "claim", "description", "reason", "information_level",
               "claim_result", "verdict", "issue_type", "validation_mode", "explanation") if isinstance(row.get(key), str)}
    assessment = row.get("assessment", {})
    claim["information_level"] = code(row.get("information_level", assessment.get("information_level")))
    claim["assessment"] = {key: {name: projector.prose(value) for name, value in axis.items()
                                if name in {"policy_kind", "status", "evidence_kind", "task_relation", "basis"}}
                           for key, axis in assessment.items() if isinstance(axis, dict)}
    claim["scope"] = projector.metadata(row.get("scope", {}))
    claim["target"] = projector.metadata(row.get("target", {}))
    claim["flow_binding"] = projector.metadata({key: item for key, item in row.get("flow_binding", {}).items()
        if isinstance(item, (bool, int)) or code(item)})
    claim["locators"] = projector.locators({key: row.get(key, {}) for key in ("locators", "binding_validation", "source_validation")})
    for key in ("binding_validation", "source_validation"):
        claim[key] = {**numbers(row.get(key, {})), "error_codes": [error_code(x) for x in row.get(key, {}).get("validation_errors", [])]}
    claim["missing_obligations"] = [{"kind": code(x.get("kind")), "conditional_on_policy_scope": x.get("conditional_on_policy_scope")}
                                     for x in row.get("missing_obligations", [])]
    claim["citation_error_codes"] = [error_code(x) for x in row.get("citation_errors", [])]
    return claim


def deployment_summary(result, extraction, projector):
    assessment = result.get("deployment_assessment", {})
    rows = []
    for finding in assessment.get("findings", []):
        row = {key: projector.metadata(finding[key]) for key in ("index", "claim", "issue_type", "assessment", "proposed_assessment",
                 "materiality", "scope", "scope_supported", "blocks_general_clean", "evidence_scope",
                 "historical_execution_established", "observed_effect") if key in finding}
        row["positive_facts"] = {}
        for name, fact in finding.get("positive_facts", {}).items():
            row["positive_facts"][name] = {"description": projector.prose(fact.get("description")),
                                            "supported": fact.get("supported"), "locators": projector.locators(fact.get("locators", []))}
        fact = finding.get("knowledge_provenance", {})
        row["knowledge_provenance"] = {"description": projector.prose(fact.get("description")), "supported": fact.get("supported"),
            "status": fact.get("status"), "proposed_status": fact.get("proposed_status"),
            "acquisition_path_established": fact.get("acquisition_path_established"), "locators": projector.locators(fact.get("locators", []))}
        row["unresolved_questions"] = [projector.prose(x) for x in finding.get("unresolved_questions", [])]
        row["evidence_error_codes"] = [error_code(x) for x in finding.get("evidence_errors", [])]
        rows.append(row)
    return {"status": "reviewed_named_findings" if rows else "reviewed_no_named_findings" if assessment else "not_assessed",
            "findings": rows, "finding_count": len(rows), "assessment_counts": dict(Counter(x.get("assessment", "unknown") for x in rows)),
            "proposed_finding_count": len(extraction.get("deployment_findings", [])),
            **{key: assessment.get(key) for key in ("in_audit_scope", "general_clean_blocked", "general_clean_established",
                                                   "coverage", "information_boundary_verdict_unchanged")},
            "scope_note": "Auxiliary deployment assumptions are separate from information-boundary inconsistencies; static evidence does not establish historical execution or numerical effects."}


def attempt(directory, run, paper_id, selected, preflight=False):
    result = read_json(directory / "result.json")
    for name in ("report.json", "report.md", "report.html"):
        if not (directory / name).is_file():
            raise ValueError(f"final output missing: {run.name}/{directory.name}/{name}")
    prepared_preflight = preflight and result.get("status") == "pending" and result.get("verdict") == "not_run" \
        and result.get("reason") == "document_prepared_inference_not_run"
    if result.get("status") not in TERMINAL and not prepared_preflight:
        raise ValueError(f"attempt is not final: {run.name}/{directory.name}")
    request = read_json(directory / "request.json", optional=True)
    combined = read_json(directory / "combined_input.json", optional=True)
    repo = read_json(directory / "repository.json", optional=True)
    extraction_name = result.get("effective_extraction_file", "extraction.json")
    if relative_path(extraction_name) != extraction_name or "/" in extraction_name:
        raise ValueError("invalid effective extraction artifact name")
    extraction = read_json(directory / extraction_name, optional=True)
    discovery = read_json(directory / "source_discovery.json", optional=True)
    projector = Projector(result, extraction, combined)
    ledger = inference(directory, preflight)
    row = {"paper_id": paper_id, "paper_name": PAPERS[paper_id], "attempt_id": directory.relative_to(run).as_posix() if directory != run else ".",
           "run_id": run.name, "selected_final": selected, "cohort_type": "material_preflight" if preflight else "fresh_model_audit",
           "status": result.get("status"), "phase_outcome": "prepared_without_inference" if prepared_preflight else result.get("status"),
           "source": public_url(result.get("source")), "paper_verdict": None if preflight else result.get("verdict"),
           "preflight_internal_verdict": result.get("verdict") if preflight else None,
           "inconsistency": None if preflight else result.get("inconsistency"),
           "has_confirmed_inconsistency": None if preflight else result.get("has_confirmed_inconsistency"),
           "reason": projector.prose(result.get("reason")), "error_type": code(result.get("error_type")),
           "error_code": error_code(result["error"], next((x.get("stage") for x in reversed(result.get("stages", [])) if x.get("status") == "failed"), None)) if result.get("error") else None,
           "stages": stages(result.get("stages", []), projector), "coverage_complete": result.get("coverage_complete"),
           "claim_result_counts": numbers(result.get("claim_result_counts")), "input_audit": input_audit(directory, request, combined),
           "inference": ledger, "duration_seconds": result.get("duration_seconds"), "document_sha256": result.get("document_sha256"),
           "repository": repository_summary(repo, projector), "input_channels": channel_summary(result, combined, extraction, projector),
           "claims": [safe_claim(x, projector) for x in result.get("evidence", [])],
           "deployment": deployment_summary(result, extraction, projector),
           "unresolved_questions": [projector.prose(x) for x in result.get("unresolved_questions", [])],
           "limitations": [projector.prose(x) for x in result.get("limitations", [])],
           "source_discovery": {"status": code(discovery.get("status")), "reason": projector.prose(discovery.get("reason")),
                                "repository_url": public_url(discovery.get("repository")), "candidate_count": len(discovery.get("candidates", []))},
           "source_artifacts": {name: (directory / name).relative_to(run).as_posix() for name in
               ("result.json", "report.json", "inference.json", "prepared.json", "combined_input.json", "request.json", "source_discovery.json", "source_acquisition.json", "repository.json")
               if (directory / name).exists()}}
    assert_public_safe(row, projector.omitted_spans)
    return row


def assert_public_safe(value, omitted_spans=()):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in FORBIDDEN_PUBLIC or key.lower().endswith("_quote"):
                raise ValueError(f"forbidden public payload field: {key}")
            assert_public_safe(item, omitted_spans)
    elif isinstance(value, list):
        for item in value:
            assert_public_safe(item, omitted_spans)
    elif isinstance(value, str):
        if PRIVATE.search(value) or SECRET.search(value):
            raise ValueError("private path or credential-shaped value in public projection")
        if any(span in value for span in omitted_spans):
            raise ValueError("citation/source payload leaked into public projection")


def manifest_files(runs, public_dir):
    rows = []
    for run in runs:
        for path in sorted(run.rglob("*")):
            relative = path.relative_to(run)
            if set(relative.parts) & DERIVATIVES or path.is_relative_to(public_dir):
                continue
            if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".log"}:
                if not path.resolve().is_relative_to(run):
                    raise ValueError("input artifact symlink escapes its run directory")
                if any(part.lower().startswith("gold") for part in relative.parts):
                    raise ValueError("evaluation-label sidecar found in raw run artifacts")
                rows.append({"run_id": run.name, "path": relative.as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)})
    return rows


def counts(rows):
    return {"count": len(rows), "statuses": dict(Counter(x["status"] for x in rows)),
            "verdicts": dict(Counter(x["paper_verdict"] for x in rows if x["paper_verdict"] is not None)),
            "inconsistency_flags": {str(key).lower(): sum(x["inconsistency"] is key for x in rows) for key in (True, False, None)},
            "technical_failure_count": sum(x["status"] != "completed" for x in rows),
            "insufficient_evidence_count": sum(x["paper_verdict"] == "insufficient_evidence" for x in rows)}


def retry_provenance(value):
    """Keep retry lineage and limits without copying commands or captured output."""
    projector = Projector(value)
    fields = {"created_at", "paper_id", "kind", "status", "reason", "scope", "code_commit", "retry_code_commit",
              "original_code_commit", "frozen_code_commit", "original_attempt", "original_attempt_id", "retry_attempt",
              "retry_attempt_id", "source", "requested_model", "provider", "max_calls_per_paper", "max_total_cli_calls",
              "max_input_chars", "max_code_chars", "model_timeout_seconds", "source_fetch", "require_source",
              "model_calls", "inference_started", "input_contract", "classification_changed", "source_only_fix"}
    output = {key: projector.metadata(item) for key, item in value.items() if key in fields and
              isinstance(item, (str, bool, int, float, type(None)))}
    for key, item in value.items():
        if key.endswith("sha256") and isinstance(item, str) and HEX.fullmatch(item):
            output[key] = item
        elif key in {"code_files", "code_files_sha256", "reference_artifacts_sha256"} and isinstance(item, dict):
            output[key] = {name: sha for name, sha in item.items() if relative_path(name) and isinstance(sha, str) and HEX.fullmatch(sha)}
    return output


def build(run, preflights, public_dir, selections):
    combined_dir = run / "combined"
    runs = [*preflights, run]
    if len({x.name for x in runs}) != len(runs):
        raise ValueError("input run names must be distinct")
    if public_dir.exists() or combined_dir.exists():
        raise FileExistsError("refusing to overwrite existing public or combined directory")
    if any(public_dir.is_relative_to(x) or x.is_relative_to(public_dir) for x in runs):
        raise ValueError("public output must be separate from input run directories")
    before = manifest_files(runs, public_dir)
    config = read_json(run / "frozen_config.json")
    frozen = config.get("papers", [])
    if {x.get("id") for x in frozen} != set(PAPERS) or len(frozen) != len(PAPERS):
        raise ValueError("V6 pilot must freeze exactly the four named papers")
    by_source = {x["source"]: x["id"] for x in frozen}
    selected = {key: key for key in PAPERS}
    if (run / "audits/muzzle-source-retry").is_dir():
        selected["muzzle"] = "muzzle-source-retry"
    for selection in selections:
        paper_id, separator, attempt_id = selection.partition("=")
        if not separator or paper_id not in PAPERS or relative_path(attempt_id) != attempt_id or "/" in attempt_id:
            raise ValueError("--select-final must be PAPER_ID=ATTEMPT_DIRECTORY")
        selected[paper_id] = attempt_id
    attempts, preflight_rows = [], []
    directories = sorted(x for x in (run / "audits").iterdir() if x.is_dir())
    for directory in directories:
        result = read_json(directory / "result.json")
        paper_id = by_source.get(result.get("source"))
        if paper_id is None:
            raise ValueError("fresh attempt source is not one of the frozen papers")
        attempts.append(attempt(directory, run, paper_id, selected[paper_id] == directory.name))
    finals = [x for x in attempts if x["selected_final"]]
    if len(finals) != len(PAPERS) or {x["paper_id"] for x in finals} != set(PAPERS):
        raise ValueError("exactly one terminal selected final is required for every frozen paper")
    for preflight in preflights:
        for result_path in sorted(preflight.rglob("result.json")):
            if set(result_path.relative_to(preflight).parts) & DERIVATIVES:
                continue
            result = read_json(result_path)
            paper_id = by_source.get(result.get("source"))
            if paper_id is None:
                raise ValueError("preflight source is not one of the frozen papers")
            preflight_rows.append(attempt(result_path.parent, preflight, paper_id, False, True))
    total_calls = sum(x["inference"]["invocation_count"] or 0 for x in attempts)
    for row in attempts:
        settings = {**row["input_audit"]["limits"], **{key: row["input_audit"].get(key) for key in ("source_fetch", "require_source")}}
        for key in ("max_input_chars", "max_code_chars", "source_fetch", "require_source"):
            if settings.get(key) is not None and settings[key] != config.get(key):
                raise ValueError(f"attempt settings differ from frozen limits: {row['attempt_id']}/{key}")
        for call in row["inference"]["calls"]:
            if call["requested_model"] is not None and call["requested_model"] != config.get("requested_model"):
                raise ValueError("attempt requested model differs from frozen requested model")
    if total_calls > config.get("max_total_cli_calls", total_calls):
        raise ValueError("recorded invocation count exceeds frozen total call limit")
    for paper_id in PAPERS:
        if sum(x["inference"]["invocation_count"] or 0 for x in attempts if x["paper_id"] == paper_id) > config.get("max_calls_per_paper", 3):
            raise ValueError(f"recorded invocation count exceeds paper call limit: {paper_id}")
    retry_metadata = []
    for path in sorted(run.rglob("source_retry.json")):
        if not set(path.relative_to(run).parts) & DERIVATIVES:
            retry_metadata.append({"path": path.relative_to(run).as_posix(), "sha256": digest(path),
                                   "metadata": retry_provenance(read_json(path))})
    report = {"schema_version": "v6-pilot-summary-v1", "run_id": run.name, "created_at": config.get("created_at"),
              "code_commit": code(config.get("code_commit")), "frozen_config_sha256": digest(run / "frozen_config.json"),
              "code_files_sha256": {key: sha for key, sha in config.get("code_files", {}).items() if relative_path(key) and isinstance(sha, str) and HEX.fullmatch(sha)},
              "frozen_limits": {key: config.get(key) for key in ("provider", "requested_model", "max_calls_per_paper", "max_total_cli_calls", "model_timeout_seconds", "max_input_chars", "max_code_chars", "source_fetch", "require_source")},
              "selected_final_attempts": selected, "source_retries": retry_metadata,
              "summary": {"papers": counts(finals), "fresh_attempts": counts(attempts), "preflight_attempt_count": len(preflight_rows),
                          "preflight_failure_count": sum(x["status"] == "failed" for x in preflight_rows),
                          "model_invocation_count": total_calls, "invocation_count_complete": all(x["inference"]["invocation_count"] is not None for x in attempts),
                          "actual_model_unknown_invocations": sum(x["inference"]["actual_model_unknown_invocations"] or 0 for x in attempts),
                          "usage": {key: sum(x["inference"]["usage"].get(key, 0) for x in attempts) for key in sorted(TOKEN_KEYS)},
                          "usage_reporting_complete": all(x["inference"]["usage_reporting_complete"] for x in attempts if x["inference"]["invocation_count"] != 0),
                          "error_code_counts": dict(Counter(x["error_code"] for x in attempts if x["error_code"])),
                          "denominator_note": "Four selected paper results. Earlier failures and zero-inference material preflights are separate attempts, not extra papers or negative findings.",
                          "usage_note": "Counts are recorded wrapper invocations; final cumulative ledgers are counted once. Null actual model IDs remain unknown. Missing usage or ledgers do not prove zero use.",
                          "scope_note": "Development-case pilot, not an independent accuracy estimate. Static/sampled evidence is bounded to named claims and inspected source; no historical execution or numerical effect is established."},
              "paper_results": finals, "attempts": attempts, "preflights": preflight_rows,
              "builder": {"script": "scripts/summarize_v6_pilot.py", "script_sha256": digest(Path(__file__))},
              "public_evidence_policy": "Allowlisted verdicts, model-written claim/scope summaries, stage metadata, counts, hashes and locators. Citation contents, source payloads and prompts are omitted."}
    assert_public_safe(report)
    if manifest_files(runs, public_dir) != before:
        raise ValueError("input artifacts changed while building; wait for all writers to finish")
    manifest = {"schema_version": "v6-pilot-process-manifest-v1", "hash_algorithm": "sha256",
                "path_base": "relative to run_id directory", "exclusions": sorted(DERIVATIVES),
                "files": before, "builder_sha256": report["builder"]["script_sha256"]}
    assert_public_safe(manifest)
    return report, manifest, combined_dir


def render_markdown(report):
    summary = report["summary"]
    lines = ["# V6 pilot results", "", summary["denominator_note"], "", summary["scope_note"], "",
             f"Frozen commit: `{report['code_commit']}`. Recorded model invocations: {summary['model_invocation_count']}.", "",
             "| Paper | Status | Verdict | Inconsistency | Calls |", "| --- | --- | --- | --- | --- |"]
    for row in report["paper_results"]:
        lines.append(f"| {row['paper_name']} | {row['status']} | {row['paper_verdict']} | {json.dumps(row['inconsistency'])} | {row['inference']['invocation_count']} |")
    lines += ["", summary["usage_note"], "", "Complete structured metadata is in report.json; original artifact hashes are in process_manifest.json.", ""]
    for heading, rows in (("Selected final papers", report["paper_results"]),
                          ("Earlier fresh attempts", [x for x in report["attempts"] if not x["selected_final"]]),
                          ("Material preflights: no paper verdicts", report["preflights"])):
        lines += ["## " + heading, ""]
        for row in rows:
            lines += [f"### {row['paper_name']} · {row['run_id']}/{row['attempt_id']}", "",
                      f"Status: {row['status']}; phase outcome: {row['phase_outcome']}; error code: {row['error_code'] or 'none'}.", "",
                      f"Reason: {row['reason'] or 'not recorded'}. Model calls: {row['inference']['invocation_count']}.", "",
                      "Stages: " + "; ".join(str(x.get("stage")) + "=" + str(x.get("status")) +
                                                (" (" + x["error_code"] + ")" if x.get("error_code") else "") for x in row["stages"]) + ".", "",
                      f"Repository: {row['repository']['url'] or 'unavailable'}; revision: {row['repository']['revision'] or 'unknown'}.", "",
                      f"Data files: {row['repository']['data_file_count']}; sampled files: {row['repository']['sampled_file_count']}; witnesses: {row['repository']['data_witness_count']}.", ""]
            for data in row["repository"]["data_files"]:
                lines += [f"- Data `{data['path']}`: coverage {json.dumps(data['coverage'], ensure_ascii=False)}; sampled indices {json.dumps(data['sampled_record_indices'])}."]
            if row["repository"]["data_files"]:
                lines += [""]
            channels = row["input_channels"]
            lines += [f"Input channels: {channels['assessment_status']}; {channels['candidate_count']} candidates; statuses {json.dumps(channels['status_counts'])}; complete={json.dumps(channels['complete'])}; truncated={json.dumps(channels['truncated'])}.", ""]
            for claim in row["claims"]:
                lines += [f"- Claim: {claim.get('claim', claim.get('description', claim.get('id')))}",
                          f"  Result: {claim.get('claim_result')}; reason: {claim.get('reason')}; information level: {claim.get('information_level')}.",
                          "  Scope: " + json.dumps(claim["scope"], ensure_ascii=False),
                          "  Locators: " + json.dumps(claim["locators"], ensure_ascii=False)]
            if row["claims"]:
                lines += [""]
            deployment = row["deployment"]
            lines += [f"Deployment auxiliary assessment: {deployment['status']}; {deployment['finding_count']} named findings.", ""]
            for finding in deployment["findings"]:
                lines += [f"- {finding.get('claim')}: {finding.get('assessment')}; materiality={finding.get('materiality')}; scope={finding.get('scope')}",
                          "  Facts and locators: " + json.dumps({key: finding[key] for key in ("positive_facts", "knowledge_provenance")}, ensure_ascii=False)]
            if deployment["findings"]:
                lines += [""]
            for call in row["inference"]["calls"]:
                lines += [f"- Call {call['invocation']} ({call['stage']}): {call['status']}; requested={call['requested_model']}; actual={json.dumps(call['actual_model'])}; actual IDs={json.dumps(call['actual_models'])}; usage={json.dumps(call['usage'])}."]
            lines += [""]
    return "\n".join(lines)


def render_html(report):
    rows = "".join("<tr>" + "".join("<td>" + html.escape(str(v)) + "</td>" for v in
        (r["paper_name"], r["status"], r["paper_verdict"], json.dumps(r["inconsistency"]), r["inference"]["invocation_count"])) + "</tr>"
        for r in report["paper_results"])
    sections = []
    for heading, attempts in (("Selected final papers", report["paper_results"]),
                              ("Earlier fresh attempts", [x for x in report["attempts"] if not x["selected_final"]]),
                              ("Material preflights: no paper verdicts", report["preflights"])):
        sections.append("<h2>" + html.escape(heading) + "</h2>")
        for attempt_row in attempts:
            title = attempt_row["paper_name"] + " · " + attempt_row["run_id"] + "/" + attempt_row["attempt_id"]
            brief = {key: attempt_row[key] for key in ("status", "phase_outcome", "paper_verdict", "inconsistency", "reason", "error_code")}
            sections.append("<article><h3>" + html.escape(title) + "</h3><pre>" + html.escape(json.dumps(brief, ensure_ascii=False, indent=2)) + "</pre>")
            for label, value in (("Stages", attempt_row["stages"]), ("Named claims and locators", attempt_row["claims"]),
                                 ("Data coverage and sampling", attempt_row["repository"]), ("Input channels", attempt_row["input_channels"]),
                                 ("Deployment auxiliary findings", attempt_row["deployment"]), ("Model calls and usage", attempt_row["inference"]),
                                 ("Input audit and bindings", attempt_row["input_audit"])):
                sections.append("<details" + (" open" if label in {"Stages", "Named claims and locators"} else "") + "><summary>" + html.escape(label)
                                + "</summary><pre>" + html.escape(json.dumps(value, ensure_ascii=False, indent=2)) + "</pre></details>")
            sections.append("</article>")
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">' \
        '<title>V6 pilot results</title><style>body{font:15px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#182331}' \
        'table{border-collapse:collapse;width:100%}td,th{padding:.6rem;border:1px solid #ccd2dc;text-align:left}' \
        'article{border:1px solid #ccd2dc;padding:1rem;margin:1rem 0}summary{cursor:pointer;padding:.4rem 0}' \
        'pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f8;padding:1rem;font-size:12px}</style><h1>V6 pilot results</h1><p>' \
        + html.escape(report["summary"]["denominator_note"]) + '</p><p>' + html.escape(report["summary"]["scope_note"]) \
        + '</p><table><thead><tr><th>Paper</th><th>Status</th><th>Verdict</th><th>Inconsistency</th><th>Calls</th></tr></thead><tbody>' \
        + rows + '</tbody></table><p>' + html.escape(report["summary"]["usage_note"]) \
        + '</p><p>Complete structured metadata: <a href="report.json">report.json</a>. Original artifact hashes: ' \
        + '<a href="process_manifest.json">process_manifest.json</a>.</p>' + "".join(sections) + '</html>\n'


def write_outputs(report, manifest, combined_dir, public_dir):
    payloads = {"report.json": json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                "report.md": render_markdown(report), "report.html": render_html(report),
                "process_manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"}
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
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink(missing_ok=True)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--preflight-dir", action="append", default=[], type=Path,
                        help="Preparation-only run directory; repeat in chronological order")
    parser.add_argument("--select-final", action="append", default=[], help="Override PAPER_ID=ATTEMPT_DIRECTORY")
    parser.add_argument("--public-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        run = args.run_dir.resolve(strict=True)
        preflights = [x.resolve(strict=True) for x in args.preflight_dir]
        public_dir = args.public_dir.resolve()
        report, manifest, combined_dir = build(run, preflights, public_dir, args.select_final)
        write_outputs(report, manifest, combined_dir, public_dir)
        print(json.dumps({"run_id": run.name, "public_directory": public_dir.name,
                          "paper_count": len(report["paper_results"]), "fresh_attempt_count": len(report["attempts"]),
                          "preflight_count": len(report["preflights"]), "model_invocations": report["summary"]["model_invocation_count"],
                          "manifest_artifact_count": len(manifest["files"])}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
