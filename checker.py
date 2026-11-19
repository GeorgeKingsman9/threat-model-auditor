"""Check normalized information-flow evidence against a scoped policy."""

import argparse
import json
from collections import Counter
from pathlib import Path

from scope_review import assess_claim


EDGE_FIELDS = ("role", "phase", "source", "representation", "operation")
QUERY_FORMS = {"full_query", "partial_query"}
SCOPE_FIELDS = ("paper_version", "experiment_arm", "artifact_revision", "configuration")
PERMISSIONS = {"allow", "deny"}
OBSERVATION_STATES = {"present", "absent", "possible"}
VERDICTS = {"inconsistent", "consistent_within_scope", "insufficient_evidence"}


def required_text(record, field):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def match_edge(edge):
    """Match a normalized edge, including its query form when specified."""
    if not isinstance(edge, dict) or set(edge) - {"query_form"} != set(EDGE_FIELDS):
        raise ValueError(f"edge must contain {', '.join(EDGE_FIELDS)} and optional query_form")

    # 未标注的旧记录沿用原有匹配方式。两种 query_form 均要求显式对齐。
    query_form = None
    if "query_form" in edge:
        query_form = required_text(edge, "query_form")
        if query_form not in QUERY_FORMS:
            raise ValueError(f"invalid query_form: {query_form}")

    values = tuple(required_text(edge, field) for field in EDGE_FIELDS)
    return (*values, query_form)


def matching_records(records, target, state_field, allowed_states):
    matches = []
    for record in records:
        state = required_text(record, state_field)
        if state not in allowed_states:
            raise ValueError(f"invalid {state_field}: {state}")
        required_text(record, "reference")
        if match_edge(record["edge"]) == target:
            matches.append(record)
    return matches


def decide(permissions, observations):
    """Return an edge-scoped verdict and the reason that determines it."""
    if not permissions:
        return "insufficient_evidence", "policy_unspecified"
    if len(permissions) > 1:
        return "insufficient_evidence", "conflicting_policy"
    if {"present", "absent"} <= observations:
        return "insufficient_evidence", "conflicting_observations"
    if "present" in observations:
        if "deny" in permissions:
            return "inconsistent", "forbidden_flow_confirmed"
        return "consistent_within_scope", "permitted_flow_confirmed"
    if "absent" in observations:
        return "consistent_within_scope", "absence_confirmed_at_boundary"
    if "possible" in observations:
        return "insufficient_evidence", "path_or_configuration_unconfirmed"
    return "insufficient_evidence", "no_matching_observation"


def audit_case(case):
    """Check one target edge against rules and evidence for one fixed scope."""
    case_id = required_text(case, "id")
    description = required_text(case, "description")
    source_group = required_text(case, "source_group")
    if source_group not in {"archived", "paper_text", "synthetic"}:
        raise ValueError(f"invalid source_group: {source_group}")
    for field in SCOPE_FIELDS:
        required_text(case["scope"], field)

    target = match_edge(case["target"])
    rules = matching_records(case["rules"], target, "permission", PERMISSIONS)
    observations = matching_records(
        case["observations"], target, "status", OBSERVATION_STATES
    )
    permissions = {rule["permission"] for rule in rules}
    states = {observation["status"] for observation in observations}
    verdict, reason = decide(permissions, states)
    assessment = assess_claim(case, verdict, reason, permissions, states)
    verdict, reason = assessment["verdict"], assessment["reason"]
    result = {
        "id": case_id,
        "source_group": source_group,
        "description": description,
        "scope": case["scope"],
        "target": case["target"],
        "verdict": verdict,
        "reason": reason,
        "matching_rules": rules,
        "matching_observations": observations,
        "other_observation_count": len(case["observations"]) - len(observations),
        **assessment,
    }
    if "note" in case:
        result["note"] = case["note"]
    if "behavioral_impact" in case:
        result["behavioral_impact"] = case["behavioral_impact"]
    if "input_provenance_gap" in case:
        gap = case["input_provenance_gap"]
        result["input_provenance_gap"] = {
            field: required_text(gap, field) for field in ("description", "reference")
        }
    return result


def run_pilot(cases, gold=None):
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty JSON array")
    rows = [audit_case(case) for case in cases]
    ids = {row["id"] for row in rows}
    if len(ids) != len(rows):
        raise ValueError("case IDs must be unique")

    report = {
        "case_count": len(rows),
        "verdict_counts": dict(Counter(row["verdict"] for row in rows)),
        "cases": rows,
    }
    if gold is not None:
        if not isinstance(gold, dict) or set(gold) != ids:
            raise ValueError("gold must contain exactly the IDs in the cases file")
        if any(label not in VERDICTS for label in gold.values()):
            raise ValueError("gold contains an invalid verdict")
        groups = {}
        for row in rows:
            row["expected"] = gold[row["id"]]
            row["matches_gold"] = row["verdict"] == row["expected"]
            group = groups.setdefault(row["source_group"], {"matched": 0, "total": 0})
            group["matched"] += int(row["matches_gold"])
            group["total"] += 1
        report["comparison"] = {
            "matched": sum(row["matches_gold"] for row in rows),
            "total": len(rows),
            "by_source_group": groups,
        }
    return report


def summarize_paper(paper, rows_by_id):
    """Return one verdict from the required checks in the stated scope."""
    paper_id = required_text(paper, "id")
    title = required_text(paper, "title")
    version = required_text(paper, "version")
    scope = required_text(paper, "audit_scope")
    coverage_complete = paper["coverage_complete"]
    if not isinstance(coverage_complete, bool):
        raise ValueError(f"{paper_id}: coverage_complete must be a boolean")

    checks = paper["required_checks"]
    if not isinstance(checks, list) or any(
        not isinstance(check_id, str) or not check_id.strip() for check_id in checks
    ):
        raise ValueError(f"{paper_id}: required_checks must be a list of case IDs")
    if len(set(checks)) != len(checks):
        raise ValueError(f"{paper_id}: required case IDs must be unique")

    examined = [rows_by_id[check_id] for check_id in checks if check_id in rows_by_id]
    if any(row["source_group"] == "synthetic" for row in examined):
        raise ValueError(f"{paper_id}: synthetic cases cannot determine a paper verdict")
    findings = [row["id"] for row in examined if row["verdict"] == "inconsistent"]
    unresolved = [
        check_id for check_id in checks
        if check_id not in rows_by_id
        or rows_by_id[check_id]["verdict"] == "insufficient_evidence"
    ]

    # 一条已确认的不一致就足以记录发现。其他尚未核实的检查仍单独列出。
    if findings:
        verdict = "inconsistent"
        reason = "confirmed_inconsistency_in_scope"
    elif checks and coverage_complete and not unresolved:
        verdict = "consistent_within_scope"
        reason = "all_required_checks_consistent"
    else:
        verdict = "insufficient_evidence"
        reason = "unresolved_checks" if unresolved else "audit_scope_not_fully_covered"

    return {
        "id": paper_id,
        "title": title,
        "version": version,
        "audit_scope": scope,
        "verdict": verdict,
        "has_confirmed_inconsistency": bool(findings),
        "reason": reason,
        "coverage_complete": coverage_complete,
        "required_checks": len(checks),
        "resolved_checks": len(checks) - len(unresolved),
        "confirmed_findings": findings,
        "unresolved_checks": unresolved,
        "claim_result_counts": dict(Counter(row["claim_result"] for row in examined)),
        "validation_modes": sorted({row["validation_mode"] for row in examined}),
        "behavioral_impact": [
            {"case_id": row["id"], **row["behavioral_impact"]}
            for row in examined if isinstance(row.get("behavioral_impact"), dict)
        ],
        "input_provenance_gaps": [
            {"case_id": row["id"], **row["input_provenance_gap"]}
            for row in examined if "input_provenance_gap" in row
        ],
        "evidence": examined,
    }


def run_paper_pilot(cases, papers, gold=None):
    if not isinstance(papers, list) or not papers:
        raise ValueError("papers must be a nonempty JSON array")
    rows_by_id = {row["id"]: row for row in run_pilot(cases)["cases"]}
    rows = []
    assigned_checks = set()
    for paper in papers:
        row = summarize_paper(paper, rows_by_id)
        shared = assigned_checks.intersection(paper["required_checks"])
        if shared:
            raise ValueError(f"checks assigned to multiple papers: {sorted(shared)}")
        assigned_checks.update(paper["required_checks"])
        rows.append(row)

    ids = {row["id"] for row in rows}
    if len(ids) != len(rows):
        raise ValueError("select exactly one audit scope and version per paper ID")

    report = {
        "paper_count": len(rows),
        "verdict_counts": dict(Counter(row["verdict"] for row in rows)),
        "papers": rows,
    }
    if gold is not None:
        if not isinstance(gold, dict) or set(gold) != ids:
            raise ValueError("paper gold must contain exactly the IDs in the papers file")
        if any(label not in VERDICTS for label in gold.values()):
            raise ValueError("paper gold contains an invalid verdict")
        for row in rows:
            row["expected"] = gold[row["id"]]
            row["matches_gold"] = row["verdict"] == row["expected"]
        report["comparison"] = {
            "matched": sum(row["matches_gold"] for row in rows),
            "total": len(rows),
        }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path, nargs="+", help="JSON files with normalized audit cases")
    parser.add_argument("--papers", type=Path, help="Optional JSON file of paper audit scopes")
    parser.add_argument("--gold", type=Path, help="Optional file of expected verdicts")
    args = parser.parse_args()
    try:
        cases = []
        for input_file in args.cases:
            entries = json.loads(input_file.read_text(encoding="utf-8"))
            if not isinstance(entries, list):
                raise ValueError(f"{input_file}: cases must be a JSON array")
            cases.extend(entries)
        gold = json.loads(args.gold.read_text(encoding="utf-8")) if args.gold else None
        if args.gold and gold is None:
            raise ValueError("gold must be a JSON object")
        if args.papers:
            papers = json.loads(args.papers.read_text(encoding="utf-8"))
            report = run_paper_pilot(cases, papers, gold)
        else:
            report = run_pilot(cases, gold)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(
        gold is not None and report["comparison"]["matched"] != report["comparison"]["total"]
    )


if __name__ == "__main__":
    raise SystemExit(main())
