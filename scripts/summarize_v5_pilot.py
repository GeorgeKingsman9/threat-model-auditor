#!/usr/bin/env python3
"""Build offline local and quote-free public reports from finished V5 pilots.

Example (run directories are ordered oldest to newest)::

    python3 -B scripts/summarize_v5_pilot.py outputs/RUN1 outputs/RUN2 \
        --public-dir docs/results/v5-pilot

No model, network, repository-code execution, gold-label lookup, or raw-file writes.
Existing generated files are never overwritten. ``papers`` is a renderer alias for
all attempts; ``paper_results`` and per-run summaries contain only selected finals.
"""

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reports import write_reports  # noqa: E402


TERMINAL = {"completed", "success", "passed", "failed", "failure", "error",
            "technical_failure", "invalid", "blocked"}
PAPER_NAMES = {"aspi": "ASPI", "muzzle": "MUZZLE", "obliinjection": "ObliInjection"}
TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
LOCATOR_KEYS = {"segment_id", "start", "end", "document_sha256", "match", "text_view",
                "text_view_sha256", "source_kind", "paper_sha256", "path", "file_sha256",
                "repository_source", "repository_revision", "repository_manifest_sha256",
                "line_start", "line_end"}
COVERAGE_KEYS = {"complete", "inventory_complete", "eligible_files", "included_files",
                 "omitted_files", "excluded_entries", "characters", "max_characters"}
STAGE_KEYS = {"stage", "name", "status", "segments", "characters", "sha256", "revision",
              "manifest_sha256", "source_segments", "discovery_status", "applicability",
              "flow_count", "execution", "issues_before", "accepted_replacements",
              "remaining_issues", "classification_fields_modified", "verdict",
              "previous_verdict", "model_calls", "evidence_edited"}
SECRET = re.compile(r"(?i)(?:bearer\s+\S+|\b(?:sk|ghp|github_pat)[-_][A-Za-z0-9_-]{12,}|"
                    r"(?:api[_-]?key|access[_-]?token|authorization|password)\s*[:=]\s*\S+)")
CODE = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,160}$")
HEX = re.compile(r"^[a-fA-F0-9]{40,64}$")


def read_json(path, optional=False):
    if optional and not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prose(value):
    """Only explicitly selected human-readable fields pass through this helper."""
    value = SECRET.sub("[redacted]", str(value))
    return re.sub(r"/(?:Users|home)/[^\s\"<>]+", "[local-path]", value)


def url(value):
    if not isinstance(value, str):
        return None
    parts = urlsplit(value)
    if parts.scheme not in {"https", "http"} or not parts.hostname:
        return None
    # Drop user information, queries and fragments: these can carry credentials.
    return urlunsplit((parts.scheme, parts.hostname, parts.path, "", ""))


def codes(values):
    return [item for item in values if isinstance(item, str) and CODE.fullmatch(item)]


def numeric_fields(value, keys):
    return {key: item for key, item in value.items()
            if key in keys and isinstance(item, (int, float, bool))}


def coverage(value):
    return numeric_fields(value or {}, COVERAGE_KEYS)


def error_code(value):
    text = str(value).lower()
    if "download" in text and ("timed out" in text or "timeout" in text):
        return "document_download_timeout"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    return value if isinstance(value, str) and CODE.fullmatch(value) else "technical_error"


def safe_stages(stages):
    rows = []
    for stage in stages:
        row = {key: value for key, value in stage.items() if key in STAGE_KEYS
               and isinstance(value, (str, int, float, bool, type(None)))}
        if stage.get("reason") in codes([stage.get("reason")]):
            row["reason_code"] = stage["reason"]
        if stage.get("error"):
            row["error_code"] = error_code(stage["error"])
        if isinstance(stage.get("coverage"), dict):
            row["coverage"] = coverage(stage["coverage"])
        rows.append(row)
    return rows


def locators(value):
    """Return exact location/hash metadata, never citation quote or source text."""
    found = []
    if isinstance(value, dict):
        if "segment_id" in value:
            row = {key: item for key, item in value.items() if key in LOCATOR_KEYS
                   and isinstance(item, (str, int, float, bool, type(None)))}
            if "repository_source" in row:
                row["repository_source"] = url(row["repository_source"])
            found.append(row)
        else:
            for item in value.values():
                found.extend(locators(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(locators(item))
    unique = {json.dumps(row, sort_keys=True): row for row in found}
    return list(unique.values())


def gate(value):
    return {**{key: item for key, item in value.items() if isinstance(item, bool)},
            "validation_errors": codes(value.get("validation_errors", []))}


def safe_claim(claim):
    result = {key: claim[key] for key in
              ("id", "verdict", "reason", "claim_result", "validation_mode", "issue_type")
              if key in claim and isinstance(claim[key], str) and CODE.fullmatch(claim[key])}
    for key in ("flow_binding",):
        result[key] = {name: item for name, item in claim.get(key, {}).items()
                       if isinstance(item, (bool, int)) or
                       isinstance(item, str) and CODE.fullmatch(item)}
    for key in ("binding_validation", "source_validation"):
        result[key] = gate(claim.get(key, {}))
    result["citation_errors"] = codes(claim.get("citation_errors", []))
    result["safe_locator_metadata"] = locators({
        key: claim.get(key, {}) for key in ("locators", "binding_validation", "source_validation")})
    result["missing_obligations"] = [
        {key: row[key] for key in ("kind", "conditional_on_policy_scope") if key in row}
        for row in claim.get("missing_obligations", [])]
    return result


def repository_summary(repo):
    result = {"url": url(repo.get("source")), "revision": repo.get("revision"),
              "manifest_sha256": repo.get("manifest_sha256"),
              "coverage": coverage(repo.get("coverage", {})),
              "dependency_snapshot_count": len(repo.get("dependency_snapshots", []))}
    expansion = repo.get("evidence_expansion", {})
    result["dependency_reference_counts"] = {
        key: len(expansion.get(key, [])) for key in ("needed", "unresolved", "over_limit")}
    result["evidence_expansion_counts"] = {
        **numeric_fields(expansion, {"added_files", "added_bytes"}),
        "inspected_paths": len(expansion.get("inspected_paths", []))}
    result["dependencies"] = [
        {"mount_path": dep.get("mount_path"), "url": url(dep.get("source")),
         "revision": dep.get("revision"), "coverage": coverage(dep.get("snapshot", {}).get("coverage", {}))}
        for dep in repo.get("dependency_snapshots", [])]
    return result


def inference_summary(ledger, directory):
    # inference.json is the cumulative ledger. Stage ledgers are snapshots, not
    # additional calls; summing them would count the same invocation repeatedly.
    if not ledger:
        return {"invocation_count": None, "calls": [], "usage": {},
                "usage_reporting_complete": False, "recording_status": "cumulative_ledger_missing"}
    calls = []
    stage_by_request = {}
    for path in sorted(directory.glob("inference.*.json")):
        for call in read_json(path).get("calls", []):
            stage_by_request.setdefault(call.get("request_sha256"), path.name[10:-5])
    for index, call in enumerate(ledger.get("calls", []), 1):
        calls.append({
            "invocation": index, "stage": stage_by_request.get(call.get("request_sha256")),
            "status": call.get("status"), "requested_model": call.get("requested_model"),
            "actual_model": call.get("actual_model"), "actual_models": call.get("actual_models", []),
            "request_sha256": call.get("request_sha256"),
            "usage": numeric_fields(call.get("usage") or {}, set(TOKEN_KEYS)),
            "execution": numeric_fields(call.get("execution") or {},
                                         {"returncode", "turn_completed", "fatal_error_count", "error_notification_count"})})
    return {"provider": ledger.get("provider"), "requested_model": ledger.get("model"),
            "max_calls": ledger.get("max_calls"), "invocation_count": len(calls), "calls": calls,
            "usage": numeric_fields(ledger.get("usage") or {}, set(TOKEN_KEYS)),
            "usage_reporting_complete": ledger.get("usage_reporting_complete", False),
            "actual_model_unknown_invocations": sum(not row["actual_model"] and not row["actual_models"] for row in calls),
            "preflight_failure_count": len(ledger.get("preflight_failures", []))}


def raw_manifest(run_dirs, excluded):
    files = []
    for run in run_dirs:
        for path in sorted(run.rglob("*")):
            relative = path.relative_to(run)
            if "combined" in relative.parts or any(path.is_relative_to(p) for p in excluded):
                continue
            if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".log"}:
                if not path.resolve().is_relative_to(run):
                    raise ValueError(f"raw input symlink escapes run directory: {relative}")
                files.append({"run_id": run.name, "path": relative.as_posix(),
                              "bytes": path.stat().st_size, "sha256": digest(path)})
    return files


def count_rows(rows):
    return {"count": len(rows), "statuses": dict(Counter(row.get("status", "unknown") for row in rows)),
            "verdicts": dict(Counter(row.get("verdict", "unknown") for row in rows)),
            "confirmed_inconsistencies": sum(row.get("has_confirmed_inconsistency") is True for row in rows)}


def revalidation_cohort(directory, run, finals, label):
    """Re-run deterministic decisions on existing proposals; never new inference."""
    if not directory.is_relative_to(run) or directory == run:
        raise ValueError("revalidation directory must be inside the last input run")
    metadata_path = directory / "revalidation_metadata.json"
    metadata = read_json(metadata_path, optional=True)
    public_rows, local_rows = [], []
    code_versions = []
    for original in [row for row in finals if row["run_id"] == run.name]:
        paper_id = original["paper_id"]
        result_path = directory / paper_id / "result.json"
        result = read_json(result_path)
        if result.get("status") not in TERMINAL or result.get("source") != original["source"]:
            raise ValueError(f"revalidation must have a terminal result for the same source: {paper_id}")
        provenance = result.get("revalidation", {})
        if provenance.get("model_calls") != 0 or provenance.get("evidence_edited") is not False:
            raise ValueError(f"revalidation must explicitly record zero model calls and unedited evidence: {paper_id}")
        references = provenance.get("reference_artifacts_sha256", {})
        if not references:
            raise ValueError(f"revalidation is missing source artifact hashes: {paper_id}")
        source_dir = run / "audits" / original["attempt_id"]
        for name, sha in references.items():
            source_file = (source_dir / name).resolve()
            if not source_file.is_relative_to(source_dir) or digest(source_file) != sha:
                raise ValueError(f"revalidation source artifact hash mismatch: {paper_id}/{name}")
        code_version = {"code_commit": provenance.get("code_commit"),
                        "code_files_sha256": {key: value for key, value in provenance.get("code_files_sha256", {}).items()
                                              if isinstance(value, str) and HEX.fullmatch(value)}}
        code_versions.append(code_version)
        row = deepcopy(original)
        row.update({key: result.get(key) for key in
                    ("status", "verdict", "has_confirmed_inconsistency", "coverage_complete",
                     "document_sha256", "input_binding", "prompt_sha256", "duration_seconds")})
        row.update({"id": f"{run.name}/deterministic_revalidation/{paper_id}",
                    "title": f"{label} · deterministic revalidation · {PAPER_NAMES.get(paper_id, paper_id)}",
                    "cohort_type": "deterministic_revalidation", "selected_final": False,
                    "attempt_id": f"deterministic_revalidation/{paper_id}",
                    "reason_code": next(iter(codes([result.get("reason")])), None),
                    "stages": safe_stages(result.get("stages", [])),
                    "claim_result_counts": result.get("claim_result_counts", {}),
                    "evidence": [safe_claim(c) for c in result.get("evidence", [])],
                    "unresolved_questions": [prose(q) for q in result.get("unresolved_questions", [])],
                    "source_result_path": result_path.relative_to(run).as_posix(),
                    "reused_inference_from": original["id"],
                    "revalidation": {**code_version, "reference_artifacts_sha256": references,
                                     "original_verdict": original["verdict"],
                                     "model_calls": 0, "evidence_edited": False},
                    "inference": {"invocation_count": 0, "calls": [],
                                  "usage": dict.fromkeys(TOKEN_KEYS, 0), "usage_reporting_complete": True,
                                  "execution": "deterministic_revalidation_no_model_call"},
                    "notes": ["Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."]})
        for stage in row["stages"]:
            if stage.get("stage") != "deterministic_revalidation":
                stage["inherited_from_source_attempt"] = True
                if stage.get("execution") == "fresh_model_call":
                    stage["execution"] = "reused_prior_model_result"
        public_rows.append(row)
        local_rows.append({**deepcopy(result), **{key: row[key] for key in
                           ("id", "title", "run_id", "run_label", "paper_id", "attempt_id", "selected_final", "cohort_type")},
                           "raw_result": deepcopy(result), "public_summary": row,
                           "source_result_path": row["source_result_path"],
                           "revalidation_metadata": metadata})
    if any(version != code_versions[0] for version in code_versions):
        raise ValueError("revalidation results use different code versions; report separate cohorts")
    cohort = {"cohort_type": "deterministic_revalidation", "based_on_run": run.name,
              "model_invocation_count": 0, "independent_inference": False,
              "paper_summary": count_rows(public_rows),
              "created_at": metadata.get("created_at"), **code_versions[0],
              "metadata_path": metadata_path.relative_to(run).as_posix() if metadata_path.exists() else None,
              "metadata_sha256": digest(metadata_path) if metadata_path.exists() else None,
              "results": public_rows}
    return cohort, public_rows, local_rows


def build(run_dirs, labels, public_dir, revalidation_dir=None):
    combined_dir = run_dirs[-1] / "combined"
    if (public_dir.is_relative_to(combined_dir) or combined_dir.is_relative_to(public_dir)
            or any(p.is_relative_to(public_dir) or public_dir.is_relative_to(p / "audits") for p in run_dirs)
            or revalidation_dir and (public_dir.is_relative_to(revalidation_dir) or revalidation_dir.is_relative_to(public_dir))):
        raise ValueError("public directory must be separate from raw audits and local combined output")
    raw_before = raw_manifest(run_dirs, [public_dir])
    attempts, local_attempts, finals, runs = [], [], [], []
    for run, label in zip(run_dirs, labels):
        config = read_json(run / "frozen_config.json")
        papers = config.get("papers", [])
        if not papers or len({p["id"] for p in papers}) != len(papers):
            raise ValueError(f"missing or duplicate frozen paper IDs: {run.name}")
        paper_by_url = {p["source"]: p["id"] for p in papers}
        directories = sorted(p for p in (run / "audits").iterdir() if p.is_dir())
        selected = {p["id"]: p["id"] for p in papers}
        if (run / "audits" / "aspi-download-retry").is_dir():
            selected["aspi"] = "aspi-download-retry"
        for paper_id, attempt_id in selected.items():
            if not (run / "audits" / attempt_id / "result.json").is_file():
                raise ValueError(f"selected final is incomplete: {run.name}/{paper_id}/{attempt_id}")
        run_rows, final_rows = [], []
        for directory in directories:
            result = read_json(directory / "result.json")
            if result.get("status") not in TERMINAL:
                raise ValueError(f"attempt is not terminal: {run.name}/{directory.name}")
            paper_id = paper_by_url.get(result.get("source"))
            if paper_id is None:
                raise ValueError(f"attempt source is not a frozen paper: {run.name}/{directory.name}")
            chosen = selected[paper_id] == directory.name
            ledger = read_json(directory / "inference.json", optional=True)
            inference = inference_summary(ledger, directory)
            request = read_json(directory / "request.json", optional=True)
            repo = read_json(directory / "repository.json", optional=True)
            discovery = read_json(directory / "source_discovery.json", optional=True)
            row_id = f"{run.name}/{paper_id}/{directory.name}"
            row = {"id": row_id, "title": f"{label} · {PAPER_NAMES.get(paper_id, paper_id)} · {directory.name}",
                   "run_id": run.name, "run_label": label, "paper_id": paper_id,
                   "attempt_id": directory.name, "selected_final": chosen,
                   "cohort_type": "fresh_model_audit",
                   "source_result_path": f"audits/{directory.name}/result.json",
                   "source": url(result.get("source")), "status": result.get("status"),
                   "verdict": result.get("verdict"),
                   "has_confirmed_inconsistency": result.get("has_confirmed_inconsistency"),
                   "reason_code": next(iter(codes([result.get("reason")])), None),
                   "stages": safe_stages(result.get("stages", [])),
                   "coverage_complete": result.get("coverage_complete"),
                   "claim_result_counts": result.get("claim_result_counts", {}),
                   "document_sha256": result.get("document_sha256"),
                   "input_binding": result.get("input_binding"),
                   "prompt_sha256": result.get("prompt_sha256"),
                   "request_hashes": {key: request[key] for key in
                                      ("input_sha256", "model_content_sha256", "prompt_sha256") if key in request},
                   "repository": repository_summary(repo),
                   "source_discovery": {"status": discovery.get("status"),
                                        "reason_code": next(iter(codes([discovery.get("reason")])), None),
                                        "repository_url": url(discovery.get("repository"))},
                   "inference": inference, "duration_seconds": result.get("duration_seconds"),
                   "evidence": [safe_claim(c) for c in result.get("evidence", [])],
                   "unresolved_questions": [prose(q) for q in result.get("unresolved_questions", [])],
                   "notes": ["Selected final paper result." if chosen else
                             "Earlier attempt retained; excluded from the paper denominator."]}
            if result.get("error"):
                row["error_code"] = error_code(result["error"])
                row["error_type"] = next(iter(codes([result.get("error_type")])), None)
            local = {**deepcopy(result), **{key: row[key] for key in
                     ("id", "title", "run_id", "run_label", "paper_id", "attempt_id", "selected_final")},
                     "original_id": result.get("id"), "original_title": result.get("title"),
                     "raw_result": deepcopy(result), "inference_ledger": ledger,
                     "public_summary": row, "source_result_path": f"audits/{directory.name}/result.json"}
            attempts.append(row)
            local_attempts.append(local)
            run_rows.append(row)
            if chosen:
                finals.append(row)
                final_rows.append(row)
        if len(final_rows) != len(papers):
            raise ValueError(f"selected final count does not match frozen paper denominator: {run.name}")
        frozen_hashes = {name: sha for name, sha in config.get("code_files", {}).items()
                         if isinstance(sha, str) and HEX.fullmatch(sha)}
        runs.append({"run_id": run.name, "label": label, "created_at": config.get("created_at"),
                     "code_commit": config.get("code_commit"), "code_files_sha256": frozen_hashes,
                     "frozen_config_sha256": digest(run / "frozen_config.json"),
                     "paper_summary": count_rows(final_rows), "attempt_summary": count_rows(run_rows),
                     "selected_final_attempts": selected,
                     "paper_results": [{key: row[key] for key in
                                        ("paper_id", "attempt_id", "status", "verdict", "has_confirmed_inconsistency")}
                                       for row in final_rows],
                     "attempt_results": [{"attempt_id": row["attempt_id"], "paper_id": row["paper_id"],
                                          "status": row["status"], "verdict": row["verdict"],
                                          "invocation_count": row["inference"]["invocation_count"],
                                          "selected_final": row["selected_final"]} for row in run_rows],
                     "frozen_limits": {key: config[key] for key in
                                       ("requested_model", "max_calls_per_paper", "max_total_cli_calls",
                                        "max_input_chars", "max_code_chars", "source_fetch", "require_source") if key in config}})
    usage = {key: sum(row["inference"]["usage"].get(key, 0) for row in attempts) for key in TOKEN_KEYS}
    summary = {"paper_results": count_rows(finals), "attempts": count_rows(attempts),
               "denominator_note": "Each run has one selected final per frozen paper; earlier failed attempts do not add papers. Displayed rows are attempts.",
               "model_invocation_count": sum(row["inference"]["invocation_count"] or 0 for row in attempts),
               "invocation_count_complete": all(row["inference"]["invocation_count"] is not None for row in attempts),
               "usage": usage,
               "usage_reporting_complete": all(row["inference"]["usage_reporting_complete"] for row in attempts
                                               if row["inference"]["invocation_count"] != 0),
               "scope_note": "Known development-case pilot; no independent accuracy estimate. Static source receipt does not establish historical execution or whole-repository correctness.",
               "usage_note": "Counts are wrapper CLI invocations. Stage ledgers are cumulative snapshots and are not added again. Unknown actual model IDs remain null. Missing usage does not prove zero use.",
               "runs": runs}
    report = {"schema_version": "v5-pilot-summary-v1", "run_type": "V5 pilot: all execution attempts",
              "created_at": runs[-1]["created_at"], "summary": summary, "runs": runs,
              "paper_results": finals, "attempts": attempts, "papers": attempts,
              "builder": {"script_sha256": digest(Path(__file__)), "renderer_sha256": digest(ROOT / "reports.py")},
              "public_evidence_policy": "Allowlisted stage, gate, hash and locator metadata only. Paper/source text, citation quotes, acquisition payloads and prompts are retained locally, not copied here."}
    local = {**report, "run_type": "V5 pilot: full local execution attempts",
             "papers": local_attempts, "attempts": local_attempts,
             "paper_results": [row for row in local_attempts if row["selected_final"]]}
    if revalidation_dir:
        cohort, public_revalidated, local_revalidated = revalidation_cohort(
            revalidation_dir, run_dirs[-1], finals, labels[-1])
        summary["deterministic_revalidation"] = {key: value for key, value in cohort.items() if key != "results"}
        report["deterministic_revalidation"] = cohort
        report["papers"] = attempts + public_revalidated
        local["deterministic_revalidation"] = {**cohort, "results": local_revalidated}
        local["papers"] = local_attempts + local_revalidated
    manifest = {"schema_version": "v5-pilot-process-manifest-v1",
                "hash_algorithm": "sha256", "path_base": "relative to each run directory",
                "exclusions": ["generated combined directories", "public report directory"],
                "files": raw_before}
    if raw_manifest(run_dirs, [public_dir]) != raw_before:
        raise ValueError("raw inputs changed during report construction; retry after all processes finish")
    return local, report, manifest, combined_dir


def write_outputs(local, public, manifest, combined_dir, public_dir):
    outputs = {combined_dir: local, public_dir: public}
    planned = [directory / name for directory in outputs for name in ("report.json", "report.html", "report.md")]
    planned.append(public_dir / "process_manifest.json")
    if any(path.exists() or path.is_symlink() for path in planned):
        raise FileExistsError("refusing to overwrite existing generated reports; choose a new public directory and preserve or relocate the previous combined directory")
    created = []
    try:
        for directory, report in outputs.items():
            paths = write_reports(report, directory)
            created.extend(paths.values())
            target = directory / "report.json"
            with target.open("x", encoding="utf-8") as stream:
                created.append(target)
                json.dump(report, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        target = public_dir / "process_manifest.json"
        with target.open("x", encoding="utf-8") as stream:
            created.append(target)
            json.dump(manifest, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except BaseException:
        for target in reversed(created):
            target.unlink(missing_ok=True)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dirs", nargs="+", type=Path, help="Finished run directories, oldest first")
    parser.add_argument("--public-dir", required=True, type=Path, help="Destination for safe public artifacts")
    parser.add_argument("--run-label", action="append", help="Optional label per run, in the same order")
    parser.add_argument("--revalidation-dir", type=Path,
                        help="Optional last-run revalidated/PAPER/result.json cohort; no new inference")
    args = parser.parse_args(argv)
    try:
        run_dirs = [p.resolve(strict=True) for p in args.run_dirs]
        if len(set(p.name for p in run_dirs)) != len(run_dirs):
            raise ValueError("run directory names must be unique")
        labels = args.run_label or ["V5.1 pilot" if "v5-1" in p.name else "V5 pilot" for p in run_dirs]
        if len(labels) != len(run_dirs):
            raise ValueError("supply one --run-label per run directory")
        public_dir = args.public_dir.resolve()
        revalidation_dir = args.revalidation_dir.resolve(strict=True) if args.revalidation_dir else None
        local, public, manifest, combined_dir = build(run_dirs, labels, public_dir, revalidation_dir)
        write_outputs(local, public, manifest, combined_dir, public_dir)
        print(json.dumps({"local": str(combined_dir), "public": str(public_dir),
                          "selected_paper_results": len(public["paper_results"]),
                          "attempts": len(public["attempts"]),
                          "model_invocations": public["summary"]["model_invocation_count"],
                          "manifest_files": len(manifest["files"])}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
