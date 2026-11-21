#!/usr/bin/env python3
"""Build the separate two-paper V6 declared-contract follow-up report offline.

python3 -B scripts/summarize_v6_followup.py outputs/2026-11-21-v6-contract-followup \
    --public-dir docs/results/2026-11-21-v6-contract-followup

Only finished ASPI/ObliInjection audit artifacts are accepted. No inference,
network, audit-code execution, evaluation-label lookup, or existing-file writes.
Declared-contract prose and quotations are never copied to the public record.
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summarize_v6_pilot as base  # noqa: E402


PAPER_IDS = ("aspi", "obliinjection")
CONTRACT_FILES = ("declared_contract.request.json", "declared_contract.response.json", "declared_contract.json")
QUALIFICATIONS = {"explicit", "uncertain", "unspecified"}
REJECTION_CODES = {"duplicate_target", "unknown_target", "unknown_candidate_id"}


def object_value(value):
    return value if isinstance(value, dict) else {}


def array_value(value):
    return value if isinstance(value, list) else []


def declared_fields(proposal):
    """Yield schema-owned structural paths; never expose model-written concepts."""
    for index, rule in enumerate(array_value(proposal.get("knowledge_rules"))):
        if isinstance(rule, dict):
            for name in ("role", "phase", "source", "allowed_knowledge", "forbidden_knowledge", "scope", "exceptions"):
                yield f"knowledge_rules[{index}].{name}", rule.get(name, {})
    definition = proposal.get("task_input_definition", {})
    if isinstance(definition, dict):
        if "definition" in definition:
            yield "task_input_definition.definition", definition["definition"]
        for index, item in enumerate(array_value(definition.get("components"))):
            if isinstance(item, dict):
                yield f"task_input_definition.components[{index}].definition", item.get("definition", {})
        for index, item in enumerate(array_value(definition.get("relationships"))):
            if isinstance(item, dict):
                yield f"task_input_definition.relationships[{index}].relationship", item.get("relationship", {})
    recipe = proposal.get("construction_recipe", {})
    if isinstance(recipe, dict):
        for name in ("procedure", "metadata_budget", "scope"):
            if name in recipe:
                yield "construction_recipe." + name, recipe[name]
        for name in ("inputs", "generated_artifacts"):
            for index, item in enumerate(array_value(recipe.get(name))):
                if isinstance(item, dict):
                    yield f"construction_recipe.{name}[{index}].description", item.get("description", {})


def citation_error_code(message):
    message = str(message).lower()
    for terms, code in ((["unspecified", "citation"], "unspecified_field_asserts_citation"),
                        (["granularity", "unspecified"], "unspecified_granularity_invalid"),
                        (["explicit", "requires"], "explicit_field_missing_support"),
                        (["ambiguous"], "ambiguous_citation"),
                        (["not unique"], "ambiguous_citation"),
                        (["not found"], "citation_not_found"),
                        (["segment"], "citation_segment_error")):
        if all(term in message for term in terms):
            return code
    return "citation_validation_error"


def contract_prose(value):
    """Find raw contract narrative only to redact accidental later repetition."""
    found = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"text", "concept", "granularity", "quote"} and isinstance(item, str) and len(item) >= 12:
                found.add(item)
            if key in {"component_concepts", "unresolved_questions", "limitations"} and isinstance(item, list):
                found.update(x for x in item if isinstance(x, str) and len(x) >= 12)
            if isinstance(item, (dict, list)):
                found.update(contract_prose(item))
    elif isinstance(value, list):
        for item in value:
            found.update(contract_prose(item))
    return found


def redact_contract_prose(value, spans):
    if isinstance(value, dict):
        return {key: redact_contract_prose(item, spans) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_contract_prose(item, spans) for item in value]
    if isinstance(value, str):
        for span in sorted(spans, key=len, reverse=True):
            value = value.replace(span, "[declared-contract prose omitted]")
    return value


def paper_only_input_audit(directory, request):
    if not request:
        return {"status": "not_available", "paper_only_payload_verified": None, "segment_count": None}
    if set(request) != {"source_type", "segments", "paper_sha256"} or request["source_type"] == "paper+source":
        raise ValueError("declared-contract request is not a paper-only payload")
    prepared = base.read_json(directory / "prepared.json")
    if request["source_type"] != prepared.get("media_type"):
        raise ValueError("declared-contract source type differs from prepared paper")
    if request["paper_sha256"] != prepared.get("sha256"):
        raise ValueError("declared-contract paper hash differs from prepared paper")
    parts = prepared.get("segments", [])
    expected = [{"id": item.get("id"), "text": item.get("reading_order_text", item.get("text"))} for item in parts]
    if any(item.get("source_kind", "paper") != "paper" for item in parts) or request.get("segments") != expected:
        raise ValueError("declared-contract input differs from prepared paper-only segments")
    if base.label_fields(request):
        raise ValueError("evaluation-label fields found in paper-only declaration input")
    return {"status": "passed", "paper_only_payload_verified": True, "segment_count": len(expected),
            "source_type": base.code(request.get("source_type")), "paper_sha256": base.code(request.get("paper_sha256")),
            "payload_sha256": base.digest(directory / CONTRACT_FILES[0]), "evaluation_label_fields_found": 0}


def safe_stages(stages):
    result = base.stages(stages, base.Projector())
    for row, source in zip(result, stages):
        for key in ("citations_grounded", "semantic_review_required", "citation_error_count", "issues"):
            if isinstance(source.get(key), (bool, int)):
                row[key] = source[key]
        if source.get("trust") == "untrusted_declared_contract_proposal":
            row["trust"] = source["trust"]
        if isinstance(source.get("prompt_sha256"), str) and base.HEX.fullmatch(source["prompt_sha256"]):
            row["prompt_sha256"] = source["prompt_sha256"]
        if "rejected_choices" in source:
            rejected = source["rejected_choices"]
            row["rejected_choice_count"] = len(rejected)
            row["rejection_code_counts"] = dict(Counter(item.get("reason") if item.get("reason") in REJECTION_CODES
                                                       else "invalid_selection" for item in rejected))
    return result


def contract_summary(directory, result, inference):
    request, response, envelope = [base.read_json(directory / name, optional=True) for name in CONTRACT_FILES]
    if (response or envelope) and not request:
        raise ValueError("declaration output exists without its paper-only request")
    proposal = envelope.get("proposal", response)
    if not isinstance(proposal, dict):
        raise ValueError("declared-contract proposal must be a JSON object")
    audit = paper_only_input_audit(directory, request)
    if envelope and envelope.get("paper_sha256") != request.get("paper_sha256"):
        raise ValueError("declared-contract envelope does not identify its paper-only request")
    if proposal and proposal.get("paper_sha256") != request.get("paper_sha256"):
        raise ValueError("declared-contract response does not identify its paper-only request")
    attempted = any(row.get("stage") == "declared_contract" for row in result.get("stages", [])) or bool(request)
    attempted |= any(row.get("stage") == "declared_contract" for row in inference["calls"])
    if result.get("status") == "completed" and not envelope:
        raise ValueError("completed follow-up result lacks its declared-contract envelope")
    later_phases = {"model_input_preparation", "extraction", "citation_repair", "semantic_review", "citation_validation_and_decision"}
    if not envelope and (any(row.get("stage") in later_phases for row in result.get("stages", []))
                         or any(row.get("stage") in later_phases for row in inference["calls"])):
        raise ValueError("follow-up reached source mapping without its declared-contract envelope")
    if not request and inference.get("invocation_count", 0):
        raise ValueError("follow-up records model calls without a paper-only declaration request")
    fields = []
    locators = envelope.get("locators", {})
    for path, field in declared_fields(proposal):
        if not isinstance(field, dict):
            field = {}
        qualification = field.get("status") if field.get("status") in QUALIFICATIONS else "invalid_or_missing"
        fields.append({"field": path, "qualification": qualification,
                       "proposed_citation_count": len(array_value(field.get("citations"))),
                       "located_citation_count": len(array_value(locators.get(path)))})
    definition = object_value(proposal.get("task_input_definition"))
    recipe = object_value(proposal.get("construction_recipe"))
    errors = array_value(envelope.get("citation_errors"))
    summary = {"status": "validated_untrusted_proposal" if envelope else "attempted_without_validated_proposal" if attempted else "not_reached",
               "artifact_presence": {name: (directory / name).is_file() for name in CONTRACT_FILES},
               "paper_sha256": base.code(envelope.get("paper_sha256", request.get("paper_sha256"))),
               "trust": "untrusted_declared_contract_proposal" if envelope.get("trust") == "untrusted_declared_contract_proposal" else None,
               "semantic_review_required": envelope.get("semantic_review_required") if isinstance(envelope.get("semantic_review_required"), bool) else None,
               "citations_grounded": envelope.get("citations_grounded") if isinstance(envelope.get("citations_grounded"), bool) else None,
               "counts": {"knowledge_rules": len(array_value(proposal.get("knowledge_rules"))), "qualified_fields": len(fields),
                          "task_input_components": len(array_value(definition.get("components"))), "task_input_relationships": len(array_value(definition.get("relationships"))),
                          "recipe_inputs": len(array_value(recipe.get("inputs"))), "generated_artifacts": len(array_value(recipe.get("generated_artifacts"))),
                          "unresolved_questions": len(array_value(proposal.get("unresolved_questions"))), "limitations": len(array_value(proposal.get("limitations"))),
                          "proposed_citations": sum(x["proposed_citation_count"] for x in fields),
                          "located_citations": sum(x["located_citation_count"] for x in fields), "citation_errors": len(errors)},
               "qualification_counts": dict(Counter(x["qualification"] for x in fields)), "field_qualifications": fields,
               "citation_error_code_counts": dict(Counter(citation_error_code(x) for x in errors)),
               "stages": [row for row in safe_stages(result.get("stages", [])) if row.get("stage") == "declared_contract"]}
    return summary, audit, contract_prose(proposal)


def phase_sequence_audit(inference):
    sequence = [row.get("stage") for row in inference["calls"]]
    sequences = (("declared_contract", "extraction", "semantic_review"),
                 ("declared_contract", "extraction", "citation_repair", "semantic_review"))
    known = [phase for phase in sequence if phase is not None]
    if all(phase is not None for phase in sequence) and not any(tuple(sequence) == allowed[:len(sequence)] for allowed in sequences):
        raise ValueError("recorded model phases violate the frozen follow-up order")
    if any(phase not in set().union(*[set(item) for item in sequences]) for phase in known):
        raise ValueError("unrecognized model phase in follow-up")
    return {"observed_model_phases": sequence,
            "model_phase_sequence_verified": None if inference["invocation_count"] is None or None in sequence else True}


def inference_summary(directory):
    """Attribute each invocation to its own cumulative snapshot's final entry.

    A later cumulative snapshot contains earlier calls too. Filename order does
    not establish which stage created those earlier calls. Verify every snapshot
    against the final ledger and use its prefix length as the invocation index.
    """
    summary = base.inference(directory)
    final = base.read_json(directory / "inference.json", optional=True)
    calls = final.get("calls", [])
    stage_by_invocation, verified = {}, 0
    for path in sorted(directory.glob("inference.*.json")):
        snapshot = base.read_json(path).get("calls", [])
        if not isinstance(snapshot, list) or snapshot != calls[:len(snapshot)]:
            raise ValueError("stage inference snapshot is not an unchanged prefix of final ledger")
        if not snapshot:
            continue
        stage = base.code(path.name[10:-5])
        index = len(snapshot)
        if index in stage_by_invocation and stage_by_invocation[index] != stage:
            raise ValueError("multiple stage snapshots claim the same invocation")
        stage_by_invocation[index] = stage
        verified += 1
    for index, call in enumerate(summary["calls"], 1):
        call["stage"] = stage_by_invocation.get(index)
    for key, total in summary["usage"].items():
        if total != sum(call["usage"].get(key, 0) for call in summary["calls"]):
            raise ValueError("final ledger usage differs from its invocation usage sum")
    summary["stage_attribution"] = "verified_cumulative_snapshot_prefix_lengths"
    summary["verified_stage_snapshot_count"] = verified
    return summary


def build(run, public_dir):
    combined_dir = run / "combined"
    if combined_dir.exists() or public_dir.exists():
        raise FileExistsError("refusing to overwrite existing combined or public output directory")
    if public_dir.is_relative_to(run) or run.is_relative_to(public_dir):
        raise ValueError("public output must be separate from the input run directory")
    before = base.manifest_files([run], public_dir)
    config = base.read_json(run / "frozen_config.json")
    papers = config.get("papers", [])
    if len(papers) != 2 or {row.get("id") for row in papers} != set(PAPER_IDS):
        raise ValueError("follow-up must freeze exactly ASPI and ObliInjection")
    if config.get("max_calls_per_paper") != 4 or config.get("max_total_cli_calls") != 8:
        raise ValueError("follow-up must freeze four calls per paper and eight total")
    directories = {path.name for path in (run / "audits").iterdir() if path.is_dir()}
    if directories != set(PAPER_IDS):
        raise ValueError("follow-up audit directories must be exactly aspi and obliinjection")
    sources = {row["id"]: row["source"] for row in papers}
    attempts = []
    for paper_id in PAPER_IDS:
        directory = run / "audits" / paper_id
        raw_result = base.read_json(directory / "result.json")
        if raw_result.get("source") != sources[paper_id]:
            raise ValueError("follow-up result source differs from its frozen paper URL")
        if raw_result.get("requested_workflow") not in {None, "automatic_from_paper"}:
            raise ValueError("follow-up result is not a fresh automatic paper-URL audit")
        row = base.attempt(directory, run, paper_id, True)
        row["inference"] = inference_summary(directory)
        row["stages"] = safe_stages(raw_result.get("stages", []))
        contract, contract_audit, contract_spans = contract_summary(directory, raw_result, row["inference"])
        row["declared_contract"] = contract
        row["input_audit"]["declared_contract"] = contract_audit
        row["input_audit"]["phase_sequence"] = phase_sequence_audit(row["inference"])
        row["cohort_type"] = "fresh_declared_contract_followup"
        for name in CONTRACT_FILES:
            if (directory / name).exists():
                row["source_artifacts"][name] = (directory / name).relative_to(run).as_posix()
        settings = {**row["input_audit"]["limits"], **{key: row["input_audit"].get(key) for key in ("source_fetch", "require_source")}}
        for key in ("max_input_chars", "max_code_chars", "source_fetch", "require_source"):
            if settings.get(key) is not None and settings[key] != config.get(key):
                raise ValueError("attempt settings differ from frozen follow-up limits")
        if row["inference"]["invocation_count"] is not None and row["inference"]["invocation_count"] > 4:
            raise ValueError("recorded calls exceed four-call paper limit")
        for call in row["inference"]["calls"]:
            if call["requested_model"] is not None and call["requested_model"] != config.get("requested_model"):
                raise ValueError("attempt requested model differs from frozen follow-up model")
        row = redact_contract_prose(row, contract_spans)
        base.assert_public_safe(row, contract_spans)
        attempts.append(row)
    total_calls = sum(x["inference"]["invocation_count"] or 0 for x in attempts)
    if total_calls > 8:
        raise ValueError("recorded follow-up calls exceed eight-call total limit")
    summary_counts = base.counts(attempts)
    summary_counts["inconsistency_flags"]["null"] = summary_counts["inconsistency_flags"].pop("none")
    report = {"schema_version": "v6-contract-followup-summary-v1", "run_id": run.name,
              "created_at": config.get("created_at"), "code_commit": base.code(config.get("code_commit")),
              "frozen_config_sha256": base.digest(run / "frozen_config.json"),
              "code_files_sha256": {name: sha for name, sha in config.get("code_files", {}).items()
                  if base.relative_path(name) and isinstance(sha, str) and base.HEX.fullmatch(sha)},
              "frozen_limits": {key: config.get(key) for key in ("provider", "requested_model", "max_calls_per_paper", "max_total_cli_calls",
                  "model_timeout_seconds", "max_input_chars", "max_code_chars", "source_fetch", "require_source")},
              "selected_final_attempts": {key: key for key in PAPER_IDS},
              "summary": {"papers": summary_counts, "fresh_attempts": summary_counts, "model_invocation_count": total_calls,
                          "invocation_count_complete": all(x["inference"]["invocation_count"] is not None for x in attempts),
                          "actual_model_unknown_invocations": sum(x["inference"]["actual_model_unknown_invocations"] or 0 for x in attempts),
                          "usage": {key: sum(x["inference"]["usage"].get(key, 0) for x in attempts) for key in sorted(base.TOKEN_KEYS)},
                          "usage_reporting_complete": all(x["inference"]["usage_reporting_complete"] for x in attempts if x["inference"]["invocation_count"] != 0),
                          "error_code_counts": dict(Counter(x["error_code"] for x in attempts if x["error_code"])),
                          "denominator_note": "Separate two-paper follow-up: ASPI and ObliInjection only. No original pilot attempts or verdicts enter this cohort or denominator.",
                          "scope_note": "Fresh URL-only follow-up adds an untrusted paper-only declaration phase and guarded citation recovery. Exact declaration locations do not validate policy meaning; independent source review and existing evidence gates still decide named claims. Static or sampled evidence establishes neither historical execution nor numerical effects.",
                          "usage_note": "At most four recorded wrapper calls per paper: paper declaration, extraction, optional citation recovery, independent review. Cumulative ledgers are counted once; unknown actual model IDs stay null and missing usage never proves zero use."},
              "paper_results": attempts, "attempts": attempts, "preflights": [],
              "builder": {"script": "scripts/summarize_v6_followup.py", "script_sha256": base.digest(Path(__file__)),
                          "projection_helpers": "scripts/summarize_v6_pilot.py", "projection_helpers_sha256": base.digest(Path(base.__file__))},
              "public_evidence_policy": "Declared-contract narrative, concepts and quotations are omitted; only structural counts, field qualifications, trust, citation-check counts/codes, paper hash and stage records are public. Final evidence uses the existing safe semantic-summary projection. Source payloads, prompts and private absolute paths are omitted."}
    base.assert_public_safe(report)
    if base.manifest_files([run], public_dir) != before:
        raise ValueError("input artifacts changed while building; wait for all writers to finish")
    manifest = {"schema_version": "v6-contract-followup-process-manifest-v1", "hash_algorithm": "sha256",
                "path_base": "relative to run_id directory", "exclusions": sorted(base.DERIVATIVES), "files": before,
                "builder_sha256": report["builder"]["script_sha256"],
                "projection_helpers_sha256": report["builder"]["projection_helpers_sha256"]}
    base.assert_public_safe(manifest)
    return report, manifest, combined_dir


def write_outputs(report, manifest, combined_dir, public_dir):
    markdown = base.render_markdown(report).replace("# V6 pilot results", "# V6 declared-contract follow-up", 1)
    page = base.render_html(report).replace("V6 pilot results", "V6 declared-contract follow-up")
    sections = ["<h2>Paper-only declaration metadata</h2>"]
    markdown += "\n## Paper-only declaration metadata\n\n"
    for row in report["paper_results"]:
        record = json.dumps(row["declared_contract"], ensure_ascii=False, indent=2)
        sections.append("<h3>" + html.escape(row["paper_name"]) + "</h3><pre>" + html.escape(record) + "</pre>")
        markdown += "### " + row["paper_name"] + "\n\n```json\n" + record + "\n```\n\n"
    page = page.replace("</html>", "".join(sections) + "</html>")
    payloads = {"report.json": json.dumps(report, ensure_ascii=False, indent=2) + "\n", "report.md": markdown,
                "report.html": page, "process_manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"}
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
    parser.add_argument("--public-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        run, public_dir = args.run_dir.resolve(strict=True), args.public_dir.resolve()
        report, manifest, combined_dir = build(run, public_dir)
        write_outputs(report, manifest, combined_dir, public_dir)
        print(json.dumps({"run_id": run.name, "paper_count": len(report["paper_results"]),
                          "model_invocations": report["summary"]["model_invocation_count"], "manifest_artifact_count": len(manifest["files"])}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
