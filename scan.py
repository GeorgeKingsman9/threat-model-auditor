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
                prepared=None, extraction=None, review=None, max_input_chars=180000):
    """One document produces one result, including failures and pending stages."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    row = {"id": paper_id, "title": paper_id, "source": source if "://" in source else Path(source).name,
           "status": "running", "has_confirmed_inconsistency": None, "stages": [], "evidence": []}
    stage = "ingestion"
    started = time.monotonic()
    try:
        # V2 outputs remain replayable as historical evidence; live inference
        # always requests V3 and may not silently fall back to the old contract.
        if extraction is not None and extraction.get("schema_version", 2) == 2:
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
        if len(document["text"]) > max_input_chars:
            raise ValueError("document exceeds the configured model input limit; not silently truncated")
        save_json(output_dir / "request.json", {
            "prompt_sha256": engine.prompt_hash(), "input_sha256": document["sha256"],
            "max_input_chars": max_input_chars, "evidence_scope": "supplied_document_only",
            "engine": type(client).__name__ if client else "no_model_or_replay",
        })
        if prepare_only:
            row.update(status="pending", verdict="not_run", reason="document_prepared_inference_not_run")
            row["stages"].append({"stage": "extraction", "status": "not_run"})
        else:
            stage = "extraction"
            # Use a logical reading-order view for model input when the PDF
            # reader can supply one. Keep both source views for exact locators.
            model_segments = [{"id": part["id"], "text": part.get("reading_order_text", part["text"])}
                              for part in document["segments"]]
            content = {"source_type": document["media_type"], "segments": model_segments}
            if extraction is None:
                if client is None:
                    raise ValueError("choose an inference engine, or supply extraction and review JSON for replay")
                extraction = client.generate(engine.EXTRACT_PROMPT, content, engine.EXTRACTION_SCHEMA)
            save_json(output_dir / "extraction.json", extraction)
            validate_shape(extraction, engine.EXTRACTION_SCHEMA)
            row["title"] = extraction["title"]
            row["stages"].append({"stage": stage, "status": "completed",
                                  "applicability": extraction["applicability"],
                                  "flow_count": len(extraction["flows"])})
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
            row.update(engine.decide_extraction(extraction, review, document, paper_id))
            row.update(status="completed", input_mode="document_only", prompt_sha256=engine.prompt_hash())
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


def get_client(args):
    if args.provider in {None, "codex"}:
        from codex_provider import CodexClient
        return CodexClient(model=args.model, max_calls=args.max_calls)
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
                        help="Explicit text limit; oversized inputs fail without truncation")
    parser.add_argument("--extraction", type=Path, help="Replay a stored extraction JSON")
    parser.add_argument("--review", type=Path, help="Replay a stored semantic-review JSON")
    add_engine_arguments(parser)
    args = parser.parse_args(argv)
    try:
        if bool(args.extraction) != bool(args.review):
            raise ValueError("replay requires both --extraction and --review")
        if args.extraction and args.provider:
            raise ValueError("choose replay or model inference, not both")
        client = get_client(args) if not args.prepare_only and not args.extraction else None
        extraction = json.loads(args.extraction.read_text()) if args.extraction else None
        review = json.loads(args.review.read_text()) if args.review else None
        row = scan_source(args.source, args.output, client, args.prepare_only,
                          extraction=extraction, review=review, max_input_chars=args.max_input_chars)
        report = make_report([row], "document_preparation" if args.prepare_only else "document_audit")
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
