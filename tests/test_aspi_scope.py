"""Regress the adjudicated ASPI construction scope, not a whole-paper label.

These are local rule-engine tests over the reviewed evidence. They do not rerun
ASPI, measure ASR, or establish a finding about the separate official W channel.
"""

from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import audit
from checker import audit_case, run_paper_pilot, summarize_paper


STAGE1 = "aspi_stage1_designer_task"
STAGE2 = "aspi_released_stage2_partial_query"


class AspiScopeRegressionTests(unittest.TestCase):
    def inputs(self, legacy=False):
        argv = ["audit", "aspi"] + (["--legacy"] if legacy else [])
        args = audit.make_parser().parse_args(argv)
        cases, papers = audit.load_inputs(args)
        paper = copy.deepcopy(audit.select_papers(papers, ["aspi"])[0])
        wanted = set(paper["required_checks"])
        return [copy.deepcopy(case) for case in cases if case["id"] in wanted], paper

    def paper_report(self, cases, paper):
        report = run_paper_pilot(cases, [paper])
        self.assertEqual(report["paper_count"], 1)
        self.assertEqual(len(report["papers"]), 1)
        return report["papers"][0]

    def test_default_v3_audit_has_one_positive_paper_from_the_limited_stage2_claim(self):
        original_reader = audit.read_json

        def no_gold(path):
            if "gold" in Path(path).name:
                raise AssertionError("Audit must decide without expected labels")
            return original_reader(path)

        stdout = io.StringIO()
        with patch.object(audit, "read_json", side_effect=no_gold), redirect_stdout(stdout), redirect_stderr(io.StringIO()):
            code = audit.main(["audit", "aspi", "--details", "--json"])
        self.assertEqual(code, 0)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["paper_count"], 1)
        paper = report["papers"][0]
        self.assertEqual(paper["id"], "aspi")
        self.assertEqual(paper["verdict"], "inconsistent")
        self.assertIs(paper["has_confirmed_inconsistency"], True)
        self.assertEqual(paper["confirmed_findings"], [STAGE2])
        self.assertEqual(paper["validation_modes"], ["scope_review_v3"])
        self.assertNotIn("comparison", report)
        by_id = {row["id"]: row for row in paper["evidence"]}
        self.assertEqual(by_id[STAGE1]["claim_result"], "refuted")
        self.assertEqual(by_id[STAGE1]["reason"], "claim_refuted_explicit_permission")
        self.assertEqual(by_id[STAGE2]["claim_result"], "confirmed")

    def test_stage1_designer_read_cannot_be_the_source_of_the_paper_positive(self):
        cases, paper = self.inputs()
        stage1 = next(case for case in cases if case["id"] == STAGE1)
        # Bound this test to the designer-access allegation alone. A designer's
        # full task input is not evidence about a different attacker's privilege.
        paper.update(audit_scope="Only the Stage 1 designer's original-task read", required_checks=[STAGE1], coverage_complete=True)
        row = self.paper_report([stage1], paper)
        self.assertEqual(row["verdict"], "consistent_within_scope")
        self.assertEqual(row["confirmed_findings"], [])
        self.assertEqual(row["claim_result_counts"], {"refuted": 1})
        self.assertEqual({rule["permission"] for rule in row["evidence"][0]["matching_rules"]}, {"allow"})

    def test_stage2_confirmation_uses_an_applicable_deny_and_the_same_partial_query_input(self):
        cases, _ = self.inputs()
        stage2 = next(case for case in cases if case["id"] == STAGE2)
        row = audit_case(stage2)
        self.assertEqual(row["claim_result"], "confirmed")
        self.assertEqual(row["target"]["query_form"], "partial_query")
        self.assertEqual(row["assessment"]["information_level"], "partial_query")
        self.assertEqual(row["assessment"]["policy_application"]["status"], "applicable")
        self.assertEqual(row["assessment"]["delivery"]["status"], "confirmed")
        self.assertEqual(row["assessment"]["delivery"]["task_relation"], "same_evaluated_instance")
        self.assertEqual({rule["permission"] for rule in row["matching_rules"]}, {"deny"})
        self.assertEqual({obs["status"] for obs in row["matching_observations"]}, {"present"})
        # Confirmation depends on the applicability decision, not simply finding
        # a task string in code or assigning this paper an expected label.
        uncertain = copy.deepcopy(stage2)
        uncertain["assessment"]["policy_application"]["status"] = "uncertain"
        self.assertEqual(audit_case(uncertain)["claim_result"], "unresolved")

    def test_partial_task_evidence_cannot_be_promoted_to_full_query_access(self):
        cases, _ = self.inputs()
        stage2 = next(case for case in cases if case["id"] == STAGE2)
        stage2["target"]["query_form"] = "full_query"
        result = audit_case(stage2)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["reason"], "query_form_information_level_conflict")
        self.assertEqual(result["matching_observations"], [])

    def test_behavioral_impact_metadata_does_not_erase_the_construction_finding(self):
        for status in ("not_tested", "inconclusive", "no_clear_effect", "effect_supported"):
            with self.subTest(behavioral_impact=status):
                cases, paper = self.inputs()
                stage2 = next(case for case in cases if case["id"] == STAGE2)
                stage2["behavioral_impact"] = {
                    "status": status, "reference": "test metadata only",
                    "description": "Changing causal-impact metadata must not change the scoped access decision.",
                }
                result = self.paper_report(cases, paper)
                self.assertEqual(result["verdict"], "inconsistent")
                self.assertEqual(result["confirmed_findings"], [STAGE2])
                metadata = next(item for item in result["behavioral_impact"] if item["case_id"] == STAGE2)
                self.assertEqual(metadata["status"], status)

    def test_an_unreviewed_w_channel_does_not_inherit_clarif_user_findings(self):
        cases, paper = self.inputs()
        original = self.paper_report(cases, paper)
        self.assertEqual(original["confirmed_findings"], [STAGE2])
        rows = {row["id"]: row for row in original["evidence"]}
        # This is an unreviewed-scope probe, not a new claim of what W contains.
        # No W policy, observation, or authorization is fabricated for the test.
        w_check = "unreviewed_official_clarif_ask_user_W_boundary"
        w_paper = {
            **paper, "audit_scope": "Probe only: the separate official W channel has not been audited here",
            "required_checks": [w_check], "coverage_complete": False,
        }
        other = summarize_paper(w_paper, rows)
        self.assertEqual(other["verdict"], "insufficient_evidence")
        self.assertEqual(other["confirmed_findings"], [])
        self.assertEqual(other["unresolved_checks"], [w_check])
        self.assertIs(other["has_confirmed_inconsistency"], False)

    def test_legacy_aspi_can_be_replayed_without_relabeling_it_as_v3_validation(self):
        cases, paper = self.inputs(legacy=True)
        result = self.paper_report(cases, paper)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["validation_modes"], ["legacy_v2"])
        self.assertEqual(result["confirmed_findings"], [STAGE2])


if __name__ == "__main__":
    unittest.main()
