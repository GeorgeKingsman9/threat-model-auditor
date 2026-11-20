"""Audit a PDF or paper URL, retaining each processing stage and its artifacts."""

import argparse
import hashlib
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

from documents import load_document
from extraction_v3 import (EXTRACTION_SCHEMA, REVIEW_SCHEMA, EXTRACT_PROMPT, REVIEW_PROMPT,
                        decide_extraction, prompt_hash, validate_shape)
from providers import ModelClient
from reports import write_reports
from source_discovery import discover_repository
from findings import project_result


def now():
    return datetime.now(timezone.utc).isoformat()


def default_output_directory(source):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    identity = hashlib.sha256(source.encode()).hexdigest()[:8]
    return Path(__file__).resolve().parent / "outputs" / f"auto-{stamp}-{identity}"


def save_json(path, data):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def checked_payload_size(content, limit):
    """Bound JSON data, including source inventories and review proposals."""
    size = len(json.dumps(content, ensure_ascii=False, sort_keys=True))
    if size > limit:
        raise ValueError("model data payload exceeds the configured input limit; not silently truncated")
    return size


def scan_source(source, output_dir, client=None, prepare_only=False, paper_id="uploaded_paper",
                prepared=None, extraction=None, review=None, max_input_chars=600000,
                repository=None, repo_revision=None, max_code_chars=320000, repair_citations=True,
                auto_repository=True, source_fetch="auto", require_source=False, engine_version=4):
    """One document produces one result, including failures and pending stages."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    row = {"id": paper_id, "title": paper_id, "source": source if "://" in source else Path(source).name,
           "status": "running", "has_confirmed_inconsistency": None, "stages": [], "evidence": []}
    stage = "ingestion"
    started = time.monotonic()

    def generate_model(prompt, content, schema):
        # A later paper/transport failure must not erase completed model calls.
        # Persist the provider's safe ledger even when this particular call fails.
        try:
            return client.generate(prompt, content, schema)
        finally:
            ledger = client.ledger() if callable(getattr(client, "ledger", None)) else None
            if isinstance(ledger, dict):
                save_json(output_dir / f"inference.{stage}.json", ledger)
    try:
        # Fixed historical outputs must never trigger a fresh source search or
        # acquire new evidence behind a saved model proposal's back.
        explicit_repository = repository is not None
        if repo_revision and not explicit_repository:
            raise ValueError("repo_revision requires an explicit repository")
        if explicit_repository and extraction is not None and extraction.get("schema_version") not in {4, 5}:
            raise ValueError("paper-plus-source replay requires V4/V5 outputs from the same source snapshot")
        if not explicit_repository and extraction is not None and extraction.get("schema_version") in {4, 5}:
            raise ValueError("V4 replay requires the repository snapshot as well as the paper")
        if isinstance(prepared, (str, Path)):
            prepared = json.loads(Path(prepared).read_text(encoding="utf-8"))
        document = dict(prepared) if prepared is not None else load_document(source)
        requested_source = source if "://" in source else Path(source).name
        canonical_source = source if "://" in source else str(Path(source).resolve())
        binding = hashlib.sha256(canonical_source.encode()).hexdigest()
        if prepared is not None and "source_binding" in document and document["source_binding"] != binding:
            raise ValueError("prepared document source binding does not match the requested paper")
        if prepared is not None and "://" not in source and "source_binding" not in document:
            raise ValueError("legacy local prepared input has no source binding; prepare it again")
        if prepared is not None and document.get("requested_source", document.get("source")) != requested_source:
            raise ValueError("prepared document source does not match the requested paper")
        document["requested_source"] = requested_source
        document["source_binding"] = binding
        # Prepared inputs come only from a local file or the ingestion step;
        # never include gold labels or a bundled case selected by paper ID.
        if not document.get("segments") or not document.get("sha256"):
            raise ValueError("prepared document lacks segments or content hash")
        save_json(output_dir / "prepared.json", document)
        row.update(source=document["source"], document_sha256=document["sha256"])
        row["stages"].append({"stage": stage, "status": "completed",
            "segments": len(document["segments"]), "characters": len(document["text"]),
            "coverage": document["coverage"], "source_links": document["links"],
            "sha256": document["sha256"]})
        if len(document["text"]) > max_input_chars:
            raise ValueError("document exceeds the configured model input limit; not silently truncated")
        row["requested_workflow"] = (
            "fixed_output_replay" if extraction is not None else
            "explicit_paper_and_source" if explicit_repository else
            "automatic_from_paper" if auto_repository else "paper_only"
        )
        row["source_audit"] = {"status": "not_requested"}
        if not explicit_repository and auto_repository and extraction is None:
            stage = "source_discovery"
            discovery = discover_repository(document, source)
            save_json(output_dir / "source_discovery.json", discovery)
            row["source_discovery"] = discovery
            row["stages"].append({"stage": stage, "status": "completed",
                                  "discovery_status": discovery["status"],
                                  "reason": discovery.get("reason", "")})
            if discovery["status"] == "selected":
                repository, repo_revision = discovery["repository"], discovery["revision"]
            else:
                row["source_audit"] = {"status": "unavailable", "reason": discovery.get("reason", discovery["status"])}
                row.setdefault("notes", []).append(
                    "Official source was not resolved automatically. This result uses only the paper text; "
                    "missing source is not evidence of absent information flow or an out-of-scope paper."
                )
        source_snapshot = None
        if repository is not None:
            from source_bundle import load_repository
            stage = "repository_ingestion"
            try:
                source_options = {"revision": repo_revision, "max_chars": max_code_chars}
                if source_fetch != "auto":
                    source_options["fetch_mode"] = source_fetch
                source_snapshot = load_repository(str(repository), **source_options)
            except (OSError, ValueError) as error:
                acquisition = getattr(error, "acquisition", None)
                if isinstance(acquisition, dict):
                    save_json(output_dir / "source_acquisition.json", acquisition)
                if explicit_repository:
                    raise
                # Retain the failed source stage separately from any successful
                # paper-only audit. Never pass unverified source bytes to V4.
                row["source_audit"] = {"status": "unavailable", "repository": repository,
                                       "revision": repo_revision, "reason": str(error)}
                if isinstance(acquisition, dict):
                    row["source_audit"]["acquisition"] = acquisition
                row["stages"].append({"stage": stage, "status": "failed", "error": str(error)})
                row.setdefault("notes", []).append(
                    "An associated source revision was discovered but could not be read. "
                    "The remaining audit covers paper text only; source verification did not complete."
                )
                repository = None
        if require_source and source_snapshot is None:
            raise ValueError("A verified source snapshot is required; model inference was not started")
        if source_snapshot is not None:
            selected_version = extraction.get("schema_version") if extraction is not None else engine_version
            if selected_version == 5:
                import extraction_v5 as engine
            else:
                import extraction_v4 as engine
        elif extraction is not None and extraction.get("schema_version", 2) == 2:
            import extraction as engine
        else:
            import extraction_v3 as engine
        evidence_document = document
        if source_snapshot is not None:
            save_json(output_dir / "repository.json", source_snapshot)
            evidence_document = engine.combine_inputs(document, source_snapshot)
            save_json(output_dir / "combined_input.json", evidence_document)
            row["repository"] = evidence_document["repository"]
            row["source_audit"] = {"status": "loaded", "repository": str(repository),
                                   "revision": source_snapshot["revision"], "coverage": source_snapshot["coverage"]}
            acquisition = source_snapshot.get("source_acquisition")
            if isinstance(acquisition, dict):
                save_json(output_dir / "source_acquisition.json", acquisition)
                row["source_audit"]["acquisition"] = acquisition
            row["stages"].append({"stage": stage, "status": "completed",
                "revision": source_snapshot["revision"], "manifest_sha256": source_snapshot["manifest_sha256"],
                "source_segments": len(source_snapshot["segments"]), "coverage": source_snapshot["coverage"]})
        if len(evidence_document["text"]) > max_input_chars:
            raise ValueError("document exceeds the configured model input limit; not silently truncated")
        row["input_mode"] = "paper_and_source" if source_snapshot is not None else "document_only"
        stage = "model_input_preparation"
        model_segments = [{"id": part["id"], "text": part.get("reading_order_text", part["text"])}
                          for part in evidence_document["segments"]]
        content = {"source_type": evidence_document["media_type"], "segments": model_segments}
        if source_snapshot is not None:
            content = engine.model_content(evidence_document)
        payload_size = checked_payload_size(content, max_input_chars)
        save_json(output_dir / "request.json", {
            "prompt_sha256": engine.prompt_hash(), "input_sha256": evidence_document["sha256"],
            "input_binding_version": evidence_document.get("input_binding_version"),
            "model_content_sha256": evidence_document.get("model_content_sha256"),
            "max_input_chars": max_input_chars,
            "model_data_characters": payload_size,
            "source_fetch": source_fetch, "require_source": require_source,
            "evidence_scope": "supplied_paper_and_source" if repository is not None else "supplied_document_only",
            "engine": type(client).__name__ if client else "no_model_or_replay",
        })
        if prepare_only:
            row.update(status="pending", verdict="not_run", reason="document_prepared_inference_not_run")
            row["stages"].append({"stage": "extraction", "status": "not_run"})
        else:
            stage = "extraction"
            supplied_extraction = extraction is not None
            # Only paper/source text and provenance enter the checked payload;
            # curated permissions, gold labels and historical reports are not read.
            if extraction is None:
                if client is None:
                    raise ValueError("choose an inference engine, or supply extraction and review JSON for replay")
                extraction = generate_model(engine.EXTRACT_PROMPT, content, engine.EXTRACTION_SCHEMA)
            save_json(output_dir / "extraction.json", extraction)
            validate_shape(extraction, engine.EXTRACTION_SCHEMA)
            row["title"] = extraction["title"]
            row["stages"].append({"stage": stage, "status": "completed",
                                  "applicability": extraction["applicability"],
                                  "flow_count": len(extraction["flows"]),
                                  "execution": "supplied_automatic_proposal" if supplied_extraction else "fresh_model_call"})
            row["effective_extraction_file"] = "extraction.json"
            if repository is not None:
                if extraction["input_binding"] != evidence_document["sha256"]:
                    raise ValueError("supplied proposal is bound to different paper/source bytes")
                from citation_repair import citation_issues, choice_request, apply_choices, REPAIR_PROMPT, CHOICE_SCHEMA
                issues = citation_issues(extraction, evidence_document)
                max_calls = getattr(client, "max_calls", None)
                calls = getattr(client, "calls", [])
                remaining = max_calls - len(calls) if type(max_calls) is int and isinstance(calls, list) else 0
                if issues and len(issues) <= 24 and repair_citations and review is None and client is not None and remaining >= 2:
                    stage = "citation_repair"
                    repair_input = choice_request(extraction, evidence_document, issues)
                    checked_payload_size(repair_input, max_input_chars)
                    save_json(output_dir / "citation_repair.request.json", repair_input)
                    response = generate_model(REPAIR_PROMPT, repair_input, CHOICE_SCHEMA)
                    save_json(output_dir / "citation_repair.response.json", response)
                    extraction, accepted = apply_choices(extraction, response, evidence_document, issues, repair_input)
                    save_json(output_dir / "extraction.repaired.json", extraction)
                    row["effective_extraction_file"] = "extraction.repaired.json"
                    row["stages"].append({"stage": stage, "status": "completed", "issues_before": len(issues),
                        "accepted_replacements": len(accepted), "remaining_issues": len(citation_issues(extraction, evidence_document)),
                        "classification_fields_modified": False, "accepted": accepted})
                elif issues:
                    row["stages"].append({"stage": "citation_repair", "status": "not_run", "issues": len(issues),
                        "reason": "disabled_or_fixed_review_or_insufficient_call_budget"})
            stage = "semantic_review"
            if review is None:
                if client is None:
                    raise ValueError("replay requires a separate review JSON")
                review_input = {**content, "proposal": extraction}
                checked_payload_size(review_input, max_input_chars)
                review = generate_model(engine.REVIEW_PROMPT, review_input, engine.REVIEW_SCHEMA)
            save_json(output_dir / "review.json", review)
            validate_shape(review, engine.REVIEW_SCHEMA)
            row["stages"].append({"stage": stage, "status": "completed",
                                  "applicability": review["applicability"]})
            stage = "citation_validation_and_decision"
            source_notes = list(row.get("notes", []))
            row.update(engine.decide_extraction(extraction, review, evidence_document, paper_id))
            if source_notes:
                row["notes"] = source_notes + [note for note in row.get("notes", []) if note not in source_notes]
            row.update(status="completed", input_mode="paper_and_source" if repository is not None else "document_only",
                       prompt_sha256=engine.prompt_hash())
            row["stages"].append({"stage": stage, "status": "completed",
                                  "verdict": row["verdict"], "reason": row["reason"]})
    except Exception as error:
        # This is the per-paper boundary. Preserve programming/transport errors
        # as failed rows so one paper cannot discard the rest of a batch.
        # BaseException (including user interruption) still propagates.
        row.update(status="failed", verdict="technical_failure", error=str(error),
                   error_type=type(error).__name__, has_confirmed_inconsistency=None)
        row["stages"].append({"stage": stage, "status": "failed", "error": str(error)})
    row["duration_seconds"] = round(time.monotonic() - started, 3)
    if client is not None and callable(getattr(client, "ledger", None)):
        ledger = client.ledger()
        if isinstance(ledger, dict):
            save_json(output_dir / "inference.json", ledger)
    project_result(row)
    save_json(output_dir / "result.json", row)
    return row


def make_report(rows, run_type):
    return {"run_type": run_type, "created_at": now(),
            "summary": {"paper_count": len(rows), "statuses": dict(Counter(r.get("status") for r in rows)),
                        "verdicts": dict(Counter(r.get("verdict") for r in rows))}, "papers": rows}


def add_engine_arguments(parser):
    parser.add_argument("--provider", choices=["codex", "openai", "anthropic"], help="Default: existing Codex ChatGPT login")
    parser.add_argument("--model", help="Explicit model ID; no automatic model substitution")
    parser.add_argument("--allow-api", action="store_true", help="Authorize this command's API calls")
    parser.add_argument("--max-cost-usd", type=float)
    parser.add_argument("--input-price", type=float, help="USD per million input tokens")
    parser.add_argument("--output-price", type=float, help="USD per million output tokens")
    parser.add_argument("--max-output-tokens", type=int, default=4000)
    parser.add_argument("--max-calls", type=int, default=28)
    parser.add_argument("--model-timeout", type=int, default=300,
                        help="Per Codex extraction/review call timeout in seconds; no automatic retry")


def get_client(args):
    if args.provider in {None, "codex"}:
        from codex_provider import CodexClient
        return CodexClient(model=args.model, max_calls=args.max_calls, timeout=getattr(args, "model_timeout", 300))
    if not all(value is not None for value in (args.model, args.max_cost_usd, args.input_price, args.output_price)):
        raise ValueError("API backend requires --model, --max-cost-usd, --input-price and --output-price")
    return ModelClient(args.provider, args.model, args.max_cost_usd, args.input_price, args.output_price,
                       args.max_output_tokens, args.max_calls, args.allow_api)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Local PDF/HTML/TXT path or HTTP(S) paper URL")
    parser.add_argument("--output", type=Path, help="Optional new output directory; generated automatically when omitted")
    parser.add_argument("--engine-version", type=int, choices=[4, 5], default=5,
                        help="Default: recipient/instance-aware V5; V4 retained for historical comparisons")
    parser.add_argument("--prepare-only", action="store_true", help="Read document without model calls")
    parser.add_argument("--paper-only", action="store_true",
                        help="Disable automatic associated-source discovery; audit the supplied paper text only")
    parser.add_argument("--source-fetch", choices=["auto", "files"], default="auto",
                        help="Fetch a pinned archive with fallback, or directly fetch verified eligible GitHub source files")
    parser.add_argument("--require-source", action="store_true",
                        help="Stop before model inference if verified source cannot be loaded")
    parser.add_argument("--max-input-chars", type=int, default=600000,
                        help="Combined paper/source text limit; oversized inputs fail without truncation")
    parser.add_argument("--repo", help="Optional override: local source directory/Git checkout or public GitHub repository URL")
    parser.add_argument("--repo-revision", help="Pinned Git commit (required for GitHub URLs)")
    parser.add_argument("--max-code-chars", type=int, default=320000,
                        help="Selected source text budget; any omitted files remain explicit in coverage")
    parser.add_argument("--no-citation-repair", action="store_true", help="Disable the optional single citation-only recovery call")
    parser.add_argument("--proposal", type=Path,
                        help="Resume a stored V4 automatic proposal with citation recovery and a fresh review")
    parser.add_argument("--extraction", type=Path, help="Replay a stored extraction JSON")
    parser.add_argument("--review", type=Path, help="Replay a stored semantic-review JSON")
    add_engine_arguments(parser)
    args = parser.parse_args(argv)
    try:
        if args.output is None:
            args.output = default_output_directory(args.source)
        if bool(args.extraction) != bool(args.review):
            raise ValueError("replay requires both --extraction and --review")
        if args.proposal and (args.extraction or args.review or not args.repo):
            raise ValueError("--proposal requires --repo and cannot be combined with fixed-output replay")
        if args.extraction and args.provider:
            raise ValueError("choose replay or model inference, not both")
        if args.repo_revision and not args.repo:
            raise ValueError("--repo-revision requires --repo")
        if args.paper_only and args.repo:
            raise ValueError("--paper-only cannot be combined with --repo")
        if args.paper_only and (args.require_source or args.source_fetch != "auto"):
            raise ValueError("--paper-only cannot require or fetch source")
        client = get_client(args) if not args.prepare_only and not args.extraction else None
        proposal_path = args.proposal or args.extraction
        extraction = json.loads(proposal_path.read_text()) if proposal_path else None
        review = json.loads(args.review.read_text()) if args.review else None
        row = scan_source(args.source, args.output, client, args.prepare_only,
                          extraction=extraction, review=review, max_input_chars=args.max_input_chars,
                          repository=args.repo, repo_revision=args.repo_revision, max_code_chars=args.max_code_chars,
                          repair_citations=not args.no_citation_repair, auto_repository=not args.paper_only,
                          source_fetch=args.source_fetch, require_source=args.require_source,
                          engine_version=args.engine_version)
        mode = "paper_source_audit" if args.repo else "document_audit" if args.paper_only else "automatic_paper_audit"
        report = make_report([row], "document_preparation" if args.prepare_only else mode)
        if client:
            report["inference"] = client.ledger()
        save_json(args.output / "report.json", report)
        paths = write_reports(report, args.output)
        print(json.dumps({"inconsistency": row["inconsistency"], "verdict": row["verdict"],
                          "status": row["status"], "findings": row["findings"],
                          "unresolved": row["unresolved_findings"],
                          "report": str(paths["html"])}, ensure_ascii=False))
        return int(row["status"] == "failed")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
