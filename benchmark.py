"""Show every paper's process and result, including failures and pending work."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from audit import CASE_FILES, ROOT
from checker import run_paper_pilot
from extraction import prompt_hash
from reports import write_reports
from scan import add_engine_arguments, get_client, make_report, save_json, scan_source


def regression_rows():
    cases = [case for name in CASE_FILES for case in json.loads((ROOT / name).read_text())]
    papers = json.loads((ROOT / "paper_pilot.json").read_text())
    gold = json.loads((ROOT / "paper_pilot_gold.json").read_text())
    rows = run_paper_pilot(cases, papers, gold)["papers"]
    for row in rows:
        row["status"] = "completed"
        row["stages"] = [
            {"stage": "load_curated_records", "status": "completed", "required_checks": row["required_checks"]},
            {"stage": "field_matching_and_rule_decision", "status": "completed", "evidence": row["evidence"]},
            {"stage": "paper_aggregation", "status": "completed", "verdict": row["verdict"], "reason": row["reason"]},
            {"stage": "compare_after_decision", "status": "completed", "expected": row["expected"], "matches_gold": row["matches_gold"]},
        ]
        row["notes"] = ["Curated regression: no fresh paper reading, code verification or model extraction in this run."]
    return rows


def add_comparisons(rows, specs):
    by_id = {spec["id"]: spec for spec in specs}
    for row in rows:
        spec = by_id[row["id"]]
        row.update(cohort=spec["cohort"], expected=spec["expected"],
                   expected_basis=spec["expected_basis"], comparison_note=spec["comparison_note"])
        # These fields are attached AFTER scan_source has finished.
        row["matches_gold"] = (row["verdict"] == spec["expected"]) if row["status"] == "completed" else None
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["regression", "prepare", "scan"], required=True)
    parser.add_argument("--manifest", type=Path, default=ROOT / "benchmarks/papers.json")
    parser.add_argument("--output", type=Path, required=True, help="New run directory")
    parser.add_argument("--prepared-dir", type=Path, help="Prior preparation run directory, read-only")
    parser.add_argument("--only", nargs="+", help="Optional subset of paper IDs")
    add_engine_arguments(parser)
    args = parser.parse_args(argv)
    try:
        specs = json.loads(args.manifest.read_text())["papers"]
        ids = [spec["id"] for spec in specs]
        if len(set(ids)) != len(ids) or any(not name.replace("_", "").isalnum() for name in ids):
            raise ValueError("manifest requires unique simple paper IDs")
        if args.only:
            if set(args.only) - set(ids):
                raise ValueError("unknown --only paper ID")
            specs = [spec for spec in specs if spec["id"] in args.only]
        client = get_client(args) if args.mode == "scan" else None
        if args.mode == "scan" and client is None:
            raise ValueError("scan mode requires an explicitly selected inference engine")
        args.output.mkdir(parents=True, exist_ok=False)
        save_json(args.output / "run_config.json", {
            "mode": args.mode, "prompt_sha256": prompt_hash(),
            "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
            "paper_ids": [spec["id"] for spec in specs], "input_mode": "document_only",
            "provider": args.provider, "model": args.model,
            "max_cost_usd": args.max_cost_usd, "max_calls": args.max_calls,
            "input_price_per_million": args.input_price, "output_price_per_million": args.output_price,
            "max_output_tokens": args.max_output_tokens,
        })
        if args.mode == "regression":
            available = {row["id"]: row for row in regression_rows()}
            rows = [available.get(spec["id"], {
                "id": spec["id"], "title": spec["title"], "source": spec["source"],
                "status": "not_run", "verdict": "not_run", "has_confirmed_inconsistency": None,
                "stages": [{"stage": "load_curated_records", "status": "not_run",
                            "reason": "no curated records; needs document-input audit"}],
                "evidence": [],
            }) for spec in specs]
        else:
            rows = []
            for index, spec in enumerate(specs, 1):
                print(f"[{index}/{len(specs)}] {spec['id']}", file=sys.stderr, flush=True)
                prepared = None
                if args.prepared_dir:
                    path = args.prepared_dir / spec["id"] / "prepared.json"
                    if path.exists():
                        prepared = path
                row = scan_source(spec["source"], args.output / spec["id"], client,
                                  args.mode == "prepare", spec["id"], prepared=prepared)
                rows.append(row)
        add_comparisons(rows, specs)
        report = make_report(rows, "curated_regression" if args.mode == "regression" else "document_" + args.mode)
        report["summary"]["reference_label_comparison"] = {
            "matched": sum(row["matches_gold"] is True for row in rows),
            "completed": sum(row["status"] == "completed" for row in rows),
            "total": len(rows), "interpretation": "historical labels may use evidence outside the PDF; not accuracy",
        }
        if client:
            report["inference"] = client.ledger()
        save_json(args.output / "report.json", report)
        paths = write_reports(report, args.output)
        print(json.dumps({"report": str(paths["html"]), "summary": report["summary"]}, ensure_ascii=False, indent=2))
        return int(any(row["status"] == "failed" for row in rows))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
