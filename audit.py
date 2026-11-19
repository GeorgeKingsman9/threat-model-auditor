"""Paper-level command line interface for the normalized evidence checker."""

import argparse
import json
import sys
from pathlib import Path

from checker import run_paper_pilot


ROOT = Path(__file__).resolve().parent
CASE_FILES = (
    "pilot_cases_v2.json",
    "paper_muzzle_cases.json",
    "paper_text_cases.json",
    "paper_text_cases_more.json",
)
REVIEWED_CASE_FILES = ("adjudication/reviewed_cases.json",)
REVIEWED_PAPERS_FILE = "adjudication/reviewed_papers.json"
REVIEWED_GOLD_FILE = "adjudication/reviewed_gold.json"
LABELS = {
    "inconsistent": "有已确认的不一致",
    "consistent_within_scope": "审计范围内一致",
    "insufficient_evidence": "证据不足",
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_inputs(args):
    # 自定义输入必须同时给声明/证据文件和论文清单，避免混入内置数据。
    if bool(args.cases) != bool(args.papers):
        raise ValueError("--cases and --papers must be supplied together")
    bundled_cases = CASE_FILES if args.legacy else REVIEWED_CASE_FILES
    bundled_papers = "paper_pilot.json" if args.legacy else REVIEWED_PAPERS_FILE
    paths = args.cases or [ROOT / name for name in bundled_cases]
    papers = read_json(args.papers or ROOT / bundled_papers)
    if not isinstance(papers, list) or not papers:
        raise ValueError("papers must be a nonempty JSON array")
    ids = [paper["id"] for paper in papers]
    if any(not isinstance(pid, str) or not pid.strip() for pid in ids):
        raise ValueError("paper IDs must be nonempty strings")
    if len(set(ids)) != len(ids):
        raise ValueError("paper IDs must be unique")
    cases = []
    for path in paths:
        entries = read_json(path)
        if not isinstance(entries, list):
            raise ValueError(f"{path}: cases must be a JSON array")
        cases.extend(entries)
    case_ids = [case["id"] for case in cases]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("case IDs must be unique across input files")
    return cases, papers


def select_papers(papers, requested):
    # 接受论文 ID；连字符可以替代 ID 中的下划线。多个名字按输入顺序输出。
    if requested == ["all"]:
        return papers
    if "all" in requested:
        raise ValueError("use 'all' alone, or specify paper IDs")
    by_id = {paper["id"].casefold(): paper for paper in papers}
    selected = []
    for name in requested:
        key = name.casefold().replace("-", "_")
        if key not in by_id:
            raise ValueError(f"unknown paper: {name}; use 'python3 audit.py list'")
        paper = by_id[key]
        if paper not in selected:
            selected.append(paper)
    return selected


def compact_report(report, details):
    # 详细证据仍归属于同一篇论文；默认报告不展开内部信息流。
    if details:
        return report
    fields = (
        "id", "title", "version", "audit_scope", "has_confirmed_inconsistency",
        "verdict", "reason", "coverage_complete", "expected", "matches_gold",
        "claim_result_counts", "validation_modes",
    )
    return {
        **report,
        "papers": [
            {key: row[key] for key in fields if key in row}
            for row in report["papers"]
        ],
    }


def render_table(report):
    rows = ["paper\tconfirmed_inconsistency\tstatus"]
    for row in report["papers"]:
        confirmed = "yes" if row["has_confirmed_inconsistency"] else "no"
        rows.append(f"{row['id']}\t{confirmed}\t{LABELS[row['verdict']]}")
    if "comparison" in report:
        comparison = report["comparison"]
        rows.append(
            f"Regression label agreement: {comparison['matched']}/{comparison['total']}"
        )
    return "\n".join(rows)


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    listing = subparsers.add_parser("list", help="List the bundled paper IDs")
    listing.add_argument("--json", action="store_true", help="Print the paper catalog as JSON")
    listing.add_argument("--legacy", action="store_true", help="Use the legacy V2 paper catalog")
    for command in ("audit", "evaluate"):
        sub = subparsers.add_parser(
            command,
            help="Audit papers" if command == "audit" else "Compare results with curated labels",
        )
        sub.add_argument("paper_ids", nargs="+", metavar="PAPER", help="One or more IDs, or all")
        sub.add_argument("--cases", nargs="+", type=Path, help="Custom normalized case JSON files")
        sub.add_argument("--papers", type=Path, help="Custom paper catalog JSON")
        sub.add_argument("--legacy", action="store_true", help="Use the bundled legacy V2 inputs")
        sub.add_argument("--json", action="store_true", help="Print JSON instead of a table")
        sub.add_argument("--details", action="store_true", help="Include evidence in JSON output")
        sub.add_argument("--output", type=Path, help="Also save the report as JSON; refuse overwrite")
        if command == "evaluate":
            sub.add_argument("--gold", type=Path, help="Expected paper verdicts JSON")
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            catalog = "paper_pilot.json" if args.legacy else REVIEWED_PAPERS_FILE
            papers = read_json(ROOT / catalog)
            if args.json:
                print(json.dumps(papers, ensure_ascii=False, indent=2))
            else:
                print("paper\ttitle")
                for paper in papers:
                    print(f"{paper['id']}\t{paper['title']}")
            return 0

        if args.details and not (args.json or args.output):
            raise ValueError("--details requires --json or --output")
        cases, papers = load_inputs(args)
        selected = select_papers(papers, args.paper_ids)
        # 只审选中论文的内部记录；缺失记录由核心规则报告证据不足。
        required_ids = {check for paper in selected for check in paper["required_checks"]}
        selected_cases = [case for case in cases if case["id"] in required_ids]
        if not selected_cases:
            raise ValueError("no normalized cases available for the selected papers")

        gold = None
        if args.command == "evaluate":
            if args.cases and args.gold is None:
                raise ValueError("custom evaluation requires an explicit --gold file")
            bundled_gold = "paper_pilot_gold.json" if args.legacy else REVIEWED_GOLD_FILE
            all_gold = read_json(args.gold or ROOT / bundled_gold)
            if not isinstance(all_gold, dict) or set(all_gold) != {p["id"] for p in papers}:
                raise ValueError("gold must contain exactly the IDs in the paper catalog")
            gold = {paper["id"]: all_gold[paper["id"]] for paper in selected}

        # 人工 gold 仅供比较；核心判定函数不读取标签来生成结论。
        report = compact_report(run_paper_pilot(selected_cases, selected, gold), args.details)
        serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(serialized)
            print(f"Saved JSON: {args.output}", file=sys.stderr)
        print(serialized, end="") if args.json else print(render_table(report))
        if gold is not None:
            return int(report["comparison"]["matched"] != report["comparison"]["total"])
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
