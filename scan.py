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


def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, data):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def scan_source(source, output_dir, client=None, prepare_only=False, paper_id="uploaded_paper",
                prepared=None, extraction=None, review=None, max_input_chars=180000,
                repository=None, repo_revision=None, max_code_chars=240000, repair_citations=True):
    """One document produces one result, including failures and pending stages."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    row = {"id": paper_id, "title": paper_id, "source": source if "://" in source else Path(source).name,
           "status": "running", "has_confirmed_inconsistency": None, "stages": [], "evidence": []}
    stage = "ingestion"
    started = time.monotonic()
    try:
        # Historical V2/V3 outputs remain replayable. Live paper/source inference
        # requests V4 and cannot fall back to curated records or a PDF-only claim.
        if repository is not None:
            import extraction_v4 as engine
            if extraction is not None and extraction.get("schema_version") != 4:
                raise ValueError("paper-plus-source replay requires V4 outputs from the same source snapshot")
        elif extraction is not None and extraction.get("schema_version") == 4:
            raise ValueError("V4 replay requires the repository snapshot as well as the paper")
        elif extraction is not None and extraction.get("schema_version", 2) == 2:
            import extraction as engine
        else:
            import extraction_v3 as engine
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
        evidence_document = document
        if repository is not None:
            from source_bundle import load_repository
            stage = "repository_ingestion"
            source_snapshot = load_repository(str(repository), revision=repo_revision, max_chars=max_code_chars)
            save_json(output_dir / "repository.json", source_snapshot)
            evidence_document = engine.combine_inputs(document, source_snapshot)
            save_json(output_dir / "combined_input.json", evidence_document)
            row["repository"] = evidence_document["repository"]
            row["stages"].append({"stage": stage, "status": "completed",
                "revision": source_snapshot["revision"], "manifest_sha256": source_snapshot["manifest_sha256"],
                "source_segments": len(source_snapshot["segments"]), "coverage": source_snapshot["coverage"]})
        if len(evidence_document["text"]) > max_input_chars:
            raise ValueError("document exceeds the configured model input limit; not silently truncated")
        save_json(output_dir / "request.json", {
            "prompt_sha256": engine.prompt_hash(), "input_sha256": evidence_document["sha256"],
            "max_input_chars": max_input_chars,
            "evidence_scope": "supplied_paper_and_source" if repository is not None else "supplied_document_only",
            "engine": type(client).__name__ if client else "no_model_or_replay",
        })
        if prepare_only:
            row.update(status="pending", verdict="not_run", reason="document_prepared_inference_not_run")
            row["stages"].append({"stage": "extraction", "status": "not_run"})
        else:
            stage = "extraction"
            supplied_extraction = extraction is not None
            # Use a logical reading-order view for model input when the PDF
            # reader can supply one. Keep both source views for exact locators.
            model_segments = [{"id": part["id"], "text": part.get("reading_order_text", part["text"])}
                              for part in evidence_document["segments"]]
            content = {"source_type": evidence_document["media_type"], "segments": model_segments}
            if repository is not None:
                # Only raw paper/source text and provenance are supplied. Curated
                # permissions, gold labels and historical reports are not read.
                content.update(input_binding=evidence_document["sha256"],
                               repository=evidence_document["repository"],
                               paper_sha256=document["sha256"])
            if extraction is None:
                if client is None:
                    raise ValueError("choose an inference engine, or supply extraction and review JSON for replay")
                extraction = client.generate(engine.EXTRACT_PROMPT, content, engine.EXTRACTION_SCHEMA)
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
                if issues and repair_citations and review is None and client is not None and remaining >= 2:
                    stage = "citation_repair"
                    repair_input = choice_request(extraction, evidence_document, issues)
                    save_json(output_dir / "citation_repair.request.json", repair_input)
                    response = client.generate(REPAIR_PROMPT, repair_input, CHOICE_SCHEMA)
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
                review = client.generate(engine.REVIEW_PROMPT, {**content, "proposal": extraction}, engine.REVIEW_SCHEMA)
            save_json(output_dir / "review.json", review)
            validate_shape(review, engine.REVIEW_SCHEMA)
            row["stages"].append({"stage": stage, "status": "completed",
                                  "applicability": review["applicability"]})
            stage = "citation_validation_and_decision"
            row.update(engine.decide_extraction(extraction, review, evidence_document, paper_id))
            row.update(status="completed", input_mode="paper_and_source" if repository is not None else "document_only",
                       prompt_sha256=engine.prompt_hash())
            row["stages"].append({"stage": stage, "status": "completed",
                                  "verdict": row["verdict"], "reason": row["reason"]})
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        row.update(status="failed", verdict="technical_failure", error=str(error),
                   has_confirmed_inconsistency=None)
        row["stages"].append({"stage": stage, "status": "failed", "error": str(error)})
    row["duration_seconds"] = round(time.monotonic() - started, 3)
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
    parser.add_argument("--output", type=Path, required=True, help="New output directory")
    parser.add_argument("--prepare-only", action="store_true", help="Read document without model calls")
    parser.add_argument("--max-input-chars", type=int, default=180000,
                        help="Combined paper/source text limit; oversized inputs fail without truncation")
    parser.add_argument("--repo", help="Local source directory/Git checkout or public GitHub repository URL")
    parser.add_argument("--repo-revision", help="Pinned Git commit (required for GitHub URLs)")
    parser.add_argument("--max-code-chars", type=int, default=240000,
                        help="Selected source text budget; any omitted files remain explicit in coverage")
    parser.add_argument("--no-citation-repair", action="store_true", help="Disable the optional single citation-only recovery call")
    parser.add_argument("--proposal", type=Path,
                        help="Resume a stored V4 automatic proposal with citation recovery and a fresh review")
    parser.add_argument("--extraction", type=Path, help="Replay a stored extraction JSON")
    parser.add_argument("--review", type=Path, help="Replay a stored semantic-review JSON")
    add_engine_arguments(parser)
    args = parser.parse_args(argv)
    try:
        if bool(args.extraction) != bool(args.review):
            raise ValueError("replay requires both --extraction and --review")
        if args.proposal and (args.extraction or args.review or not args.repo):
            raise ValueError("--proposal requires --repo and cannot be combined with fixed-output replay")
        if args.extraction and args.provider:
            raise ValueError("choose replay or model inference, not both")
        if args.repo_revision and not args.repo:
            raise ValueError("--repo-revision requires --repo")
        client = get_client(args) if not args.prepare_only and not args.extraction else None
        proposal_path = args.proposal or args.extraction
        extraction = json.loads(proposal_path.read_text()) if proposal_path else None
        review = json.loads(args.review.read_text()) if args.review else None
        row = scan_source(args.source, args.output, client, args.prepare_only,
                          extraction=extraction, review=review, max_input_chars=args.max_input_chars,
                          repository=args.repo, repo_revision=args.repo_revision, max_code_chars=args.max_code_chars,
                          repair_citations=not args.no_citation_repair)
        mode = "paper_source_audit" if args.repo else "document_audit"
        report = make_report([row], "document_preparation" if args.prepare_only else mode)
        if client:
            report["inference"] = client.ledger()
        save_json(args.output / "report.json", report)
        paths = write_reports(report, args.output)
        print(json.dumps({"verdict": row["verdict"], "status": row["status"],
                          "report": str(paths["html"])}, ensure_ascii=False))
        return int(row["status"] == "failed")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
