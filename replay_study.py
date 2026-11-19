"""Recheck stored model outputs without inference; optionally repair PDF text views."""

import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from documents import load_document
from extraction_v3 import decide_extraction
from reports import write_reports
from scan import make_report, save_json


def enrich_document(original):
    refreshed = load_document(original.get("requested_source", original["source"]))
    if refreshed["sha256"] != original["sha256"]:
        raise ValueError("source PDF bytes changed; refusing to mix evidence versions")
    if len(refreshed["segments"]) != len(original["segments"]):
        raise ValueError("source page count changed; refusing to remap citations")
    document = dict(original)
    segments = []
    for before, after in zip(original["segments"], refreshed["segments"]):
        if before["id"] != after["id"] or before["text"] != after["text"]:
            raise ValueError("primary extraction changed; refusing to replace the model's input text")
        segment = dict(before)
        if "reading_order_text" in after:
            segment["reading_order_text"] = after["reading_order_text"]
            segment["source_extraction_version"] = after["source_extraction_version"]
        segments.append(segment)
    document["segments"] = segments
    document["citation_views_enriched"] = True
    return document


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True, help="Completed document-study run")
    parser.add_argument("--output", type=Path, required=True, help="New output directory")
    parser.add_argument("--refresh-pdf-views", action="store_true")
    parser.add_argument("--workers", type=int, choices=[1, 2, 3], default=2)
    args = parser.parse_args(argv)
    try:
        report = json.loads((args.run / "report.json").read_text())
        args.output.mkdir(parents=True, exist_ok=False)

        def process(previous):
            ident = previous["id"]
            root = args.run / ident
            destination = args.output / ident
            destination.mkdir()
            row = dict(previous)
            row["previous_verdict"] = previous.get("verdict")
            has_outputs = all((root / name).is_file() for name in ("prepared.json", "extraction.json", "review.json"))
            if has_outputs:
                try:
                    document = json.loads((root / "prepared.json").read_text())
                    if args.refresh_pdf_views:
                        document = enrich_document(document)
                    extraction = json.loads((root / "extraction.json").read_text())
                    review = json.loads((root / "review.json").read_text())
                    result = decide_extraction(extraction, review, document, ident)
                    row.update(result, status="completed")
                    row.pop("error", None)
                    save_json(destination / "prepared.json", document)
                    save_json(destination / "extraction.json", extraction)
                    save_json(destination / "review.json", review)
                    row["model_output_hashes"] = {
                        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                        for name in ("extraction.json", "review.json")
                    }
                    row["stages"] = list(previous.get("stages", [])) + [{
                        "stage": "decision_replay", "status": "completed", "inference_calls": 0,
                        "same_pdf_bytes": True, "same_primary_model_input": True,
                        "additional_reading_order_view": args.refresh_pdf_views,
                        "previous_verdict": previous.get("verdict"), "verdict": row["verdict"],
                    }]
                except (OSError, ValueError, KeyError, TypeError) as error:
                    row.update(status="failed", verdict="technical_failure", error=str(error),
                               has_confirmed_inconsistency=None)
                    row["stages"] = list(previous.get("stages", [])) + [
                        {"stage": "decision_replay", "status": "failed", "error": str(error)}]
            if "expected" in row:
                row["matches_gold"] = (row.get("verdict") == row["expected"]) if (
                    row.get("status") == "completed" and row["expected"] is not None) else None
            save_json(destination / "result.json", row)
            print(ident, row.get("status"), row.get("verdict"), flush=True)
            return row

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            rows = list(pool.map(process, report["papers"]))
        updated = make_report(rows, "fixed_model_outputs_citation_and_decision_replay")
        updated["original_inference"] = report.get("inference")
        updated["replay"] = {"model_calls": 0, "same_pdf_hash_required": True,
                             "same_primary_input_required": True, "refresh_pdf_views": args.refresh_pdf_views}
        save_json(args.output / "report.json", updated)
        write_reports(updated, args.output)
        print(json.dumps(updated["summary"], ensure_ascii=False, indent=2))
        return int(any(row.get("status") == "failed" for row in rows))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
