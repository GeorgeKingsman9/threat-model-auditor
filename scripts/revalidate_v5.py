"""Revalidate frozen automatic V5 evidence; no inference or evidence edits."""

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v5
from findings import project_result
from reports import write_reports


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revalidate(source, output, paper_id=None):
    source, output = Path(source), Path(output)
    original = json.loads((source / "result.json").read_text())
    if original.get("status") != "completed" or original.get("schema_version") != 5:
        raise ValueError("revalidation requires a completed automatic V5 audit")
    effective = original.get("effective_extraction_file", "extraction.json")
    if effective not in {"extraction.json", "extraction.repaired.json"}:
        raise ValueError("unsupported stored extraction file")
    names = ["result.json", effective, "review.json", "combined_input.json", "request.json"]
    files = {name: source / name for name in names}
    extraction = json.loads(files[effective].read_text())
    review = json.loads(files["review.json"].read_text())
    document = json.loads(files["combined_input.json"].read_text())
    # Input binding, exact citations, shape, roles and identity are all checked
    # again. Stored model proposals and the original review are never rewritten.
    decision = extraction_v5.decide_extraction(extraction, review, document,
                                               paper_id or original["id"])
    row = copy.deepcopy(original)
    row.update(decision)
    row["execution_kind"] = "deterministic_revalidation"
    row["inference_reused_from"] = str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else source.name
    row["revalidation"] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_calls": 0,
        "original_verdict": original["verdict"],
        "evidence_edited": False,
        "reference_artifacts_sha256": {name: digest(path) for name, path in files.items()},
        "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "code_files_sha256": {name: digest(ROOT / name) for name in (
            "extraction_v5.py", "extraction_v4.py", "extraction_v3.py", "checker.py",
            "scope_review.py", "call_boundaries.py", "findings.py")},
    }
    row["stages"] = copy.deepcopy(original["stages"]) + [{
        "stage": "deterministic_revalidation", "status": "completed",
        "previous_verdict": original["verdict"], "verdict": row["verdict"],
        "model_calls": 0, "evidence_edited": False,
    }]
    row.setdefault("notes", []).append(
        "Deterministic revalidation of the same automatic extraction and independent review; "
        "not a fresh independent inference trial. No evidence or gold was edited.")
    project_result(row)
    output.mkdir(parents=True, exist_ok=False)
    with (output / "result.json").open("x") as stream:
        json.dump(row, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    with (output / "report.json").open("x") as stream:
        json.dump({"papers": [row]}, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    write_reports({"papers": [row]}, output)
    return row


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--id")
    args = parser.parse_args()
    row = revalidate(args.source.resolve(), args.output.resolve(), args.id)
    print(json.dumps({key: row[key] for key in ("id", "verdict", "inconsistency")}, ensure_ascii=False))
