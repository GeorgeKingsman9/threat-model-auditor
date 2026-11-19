"""Exercise the public commands without network access or third-party packages."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="auditor CLI ")
        self.addCleanup(self.temp.cleanup)
        self.workdir = Path(self.temp.name)

    def run_cli(self, *args):
        # Running elsewhere catches accidental dependencies on the caller's cwd.
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "audit.py"), *map(str, args)],
            cwd=self.workdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def get_report(self, *args, expected_code=0):
        result = self.run_cli(*args, "--json")
        self.assertEqual(result.returncode, expected_code, result.stderr)
        return json.loads(result.stdout)

    def write_json(self, name, data):
        path = self.workdir / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def custom_inputs(self):
        edge = {
            "role": "constructor",
            "phase": "construction",
            "source": "evaluated user query",
            "representation": "query text",
            "operation": "receive as input",
            "query_form": "partial_query",
        }
        case = {
            "id": "forbidden_query",
            "description": "A declared forbidden input is confirmed at the boundary.",
            "source_group": "archived",
            "scope": {
                "paper_version": "test version",
                "experiment_arm": "test arm",
                "artifact_revision": "test revision",
                "configuration": "test configuration",
            },
            "target": copy.deepcopy(edge),
            "rules": [{
                "edge": copy.deepcopy(edge),
                "permission": "deny",
                "reference": "test declaration",
            }],
            "observations": [{
                "edge": copy.deepcopy(edge),
                "status": "present",
                "reference": "test boundary evidence",
            }],
        }
        paper = {
            "id": "example",
            "title": "Test fixture, not a research finding",
            "version": "test version",
            "audit_scope": "test arm only",
            "coverage_complete": False,
            "required_checks": [case["id"], "missing_boundary"],
        }
        return [case], [paper]

    def custom_args(self, cases, papers):
        return [
            "--cases", self.write_json("cases.json", cases),
            "--papers", self.write_json("papers.json", papers),
        ]

    def test_list_from_another_working_directory(self):
        result = self.run_cli("list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        papers = json.loads(result.stdout)
        ids = [paper["id"] for paper in papers]
        self.assertEqual(len(ids), 11)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("aspi", ids)
        self.assertIn("muzzle", ids)

    def test_one_paper_one_verdict_and_uncertainty_preserved(self):
        for paper_id, confirmed, verdict in (
            ("aspi", True, "inconsistent"),
            ("muzzle", False, "insufficient_evidence"),
        ):
            with self.subTest(paper=paper_id):
                report = self.get_report("audit", paper_id)
                self.assertEqual(report["paper_count"], 1)
                self.assertEqual(len(report["papers"]), 1)
                row = report["papers"][0]
                self.assertEqual(row["id"], paper_id)
                self.assertIs(row["has_confirmed_inconsistency"], confirmed)
                self.assertEqual(row["verdict"], verdict)
                self.assertNotIn("evidence", row)
                self.assertNotIn("expected", row)
                self.assertNotIn("comparison", report)

    def test_default_output_is_one_row_per_paper(self):
        result = self.run_cli("audit", "all")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(lines[0], "paper\tconfirmed_inconsistency\tstatus")
        self.assertEqual(len(lines[1:]), 11)
        ids = [line.split("\t")[0] for line in lines[1:]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_details_keep_evidence_under_the_same_paper(self):
        report = self.get_report("audit", "aspi", "--details")
        self.assertEqual(report["paper_count"], 1)
        self.assertEqual(len(report["papers"]), 1)
        self.assertEqual(len(report["papers"][0]["evidence"]), 2)

    def test_unknown_paper_returns_a_clear_error(self):
        result = self.run_cli("audit", "not_a_paper")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown paper", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_audit_does_not_accept_gold(self):
        result = self.run_cli("audit", "aspi", "--gold", "nonexistent.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)

    def test_output_is_json_and_never_overwrites_an_existing_file(self):
        output = self.workdir / "results" / "aspi.json"
        result = self.run_cli("audit", "aspi", "--json", "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(output.read_text()), json.loads(result.stdout))
        original = output.read_bytes()
        result = self.run_cli("audit", "muzzle", "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_bytes(), original)

    def test_bash_wrapper_runs_outside_the_repository(self):
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / "audit.sh"), "aspi", "--json"],
            cwd=self.workdir,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["paper_count"], 1)
        self.assertEqual(report["papers"][0]["id"], "aspi")

    def test_custom_inputs_must_be_supplied_together(self):
        cases, _ = self.custom_inputs()
        result = self.run_cli("audit", "all", "--cases", self.write_json("cases.json", cases))
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be supplied together", result.stderr)

    def test_one_confirmed_finding_wins_despite_another_missing_check(self):
        cases, papers = self.custom_inputs()
        report = self.get_report("audit", "example", *self.custom_args(cases, papers), "--details")
        row = report["papers"][0]
        self.assertEqual(report["paper_count"], 1)
        self.assertIs(row["has_confirmed_inconsistency"], True)
        self.assertEqual(row["verdict"], "inconsistent")
        self.assertEqual(row["unresolved_checks"], ["missing_boundary"])

    def test_missing_check_prevents_a_consistency_claim(self):
        cases, papers = self.custom_inputs()
        cases[0]["rules"][0]["permission"] = "allow"
        papers[0]["coverage_complete"] = True
        report = self.get_report("audit", "example", *self.custom_args(cases, papers))
        row = report["papers"][0]
        self.assertIs(row["has_confirmed_inconsistency"], False)
        self.assertEqual(row["verdict"], "insufficient_evidence")

    def test_partial_and_full_query_do_not_match(self):
        cases, papers = self.custom_inputs()
        cases[0]["observations"][0]["edge"]["query_form"] = "full_query"
        papers[0]["required_checks"] = [cases[0]["id"]]
        report = self.get_report("audit", "example", *self.custom_args(cases, papers))
        self.assertEqual(report["papers"][0]["verdict"], "insufficient_evidence")

    def test_gold_changes_comparison_but_not_the_verdict(self):
        cases, papers = self.custom_inputs()
        args = self.custom_args(cases, papers)
        audit = self.get_report("audit", "example", *args)
        gold = self.write_json("wrong_gold.json", {"example": "consistent_within_scope"})
        evaluated = self.get_report(
            "evaluate", "example", *args, "--gold", gold, expected_code=1,
        )
        self.assertEqual(evaluated["comparison"], {"matched": 0, "total": 1})
        self.assertEqual(evaluated["papers"][0]["verdict"], audit["papers"][0]["verdict"])
        self.assertIs(evaluated["papers"][0]["has_confirmed_inconsistency"], True)

    def test_bundled_evaluation_matches_the_curated_regression_labels(self):
        report = self.get_report("evaluate", "all")
        self.assertEqual(report["comparison"], {"matched": 11, "total": 11})
        self.assertEqual(report["verdict_counts"], {
            "inconsistent": 7,
            "consistent_within_scope": 1,
            "insufficient_evidence": 3,
        })


if __name__ == "__main__":
    unittest.main()
