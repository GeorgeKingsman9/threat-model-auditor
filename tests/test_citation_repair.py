"""Check citation-only repair against real toy source snapshots, without inference."""

import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import citation_repair as repair
import extraction_v4 as v4
import test_extraction_v4 as toy


class CitationRepairTests(unittest.TestCase):
    def setUp(self):
        _, _, self.document, self.extraction, self.review = toy.ExtractionV4Tests().fixtures()

    def broken_code(self):
        broken = copy.deepcopy(self.extraction)
        replacement = copy.deepcopy(broken["flows"][0]["implementation"])
        # This token occurs in the request, artifact write and return statement.
        broken["flows"][0]["implementation"]["quote"] = "reply"
        issues = repair.citation_issues(broken, self.document)
        self.assertEqual([issue["target"] for issue in issues], ["flows.0.implementation"])
        return broken, replacement, issues

    def response(self, target, replacement):
        return {"repairs": [{"target": target, "replacement": replacement, "reason": "Use a unique original substring at the same claimed boundary."}]}

    def test_valid_proposal_has_no_citation_issue(self):
        self.assertEqual(repair.citation_issues(self.extraction, self.document), [])

    def test_absent_paper_quote_and_duplicate_code_quote_are_detected(self):
        broken, _, _ = self.broken_code()
        broken["flows"][0]["declaration"]["quote"] = "An invented paper sentence absent from the snapshot."
        targets = {issue["target"] for issue in repair.citation_issues(broken, self.document)}
        self.assertEqual(targets, {"flows.0.declaration", "flows.0.implementation"})

    def test_repair_changes_only_the_failed_citation_and_can_be_exactly_located(self):
        broken, replacement, issues = self.broken_code()
        before = copy.deepcopy(broken)
        fixed, accepted = repair.apply_repairs(broken, self.response("flows.0.implementation", replacement), self.document, issues)
        expected = copy.deepcopy(before)
        expected["flows"][0]["implementation"] = replacement
        self.assertEqual(fixed, expected)
        self.assertEqual(broken, before)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0]["before"], before["flows"][0]["implementation"])
        self.assertEqual(accepted[0]["after"], replacement)
        self.assertEqual(repair.citation_issues(fixed, self.document), [])
        locator = v4._locate(replacement, self.document, "code")
        self.assertEqual(locator["path"], "generator.py")
        self.assertEqual((locator["line_start"], locator["line_end"]), (4, 4))
        self.assertEqual(locator["repository_revision"], self.document["repository"]["revision"])
        self.assertEqual(fixed["input_binding"], broken["input_binding"])

    def test_missing_paper_citation_can_be_replaced_without_changing_its_permission(self):
        broken = copy.deepcopy(self.extraction)
        replacement = copy.deepcopy(broken["flows"][0]["declaration"])
        broken["flows"][0]["declaration"] = None
        issues = repair.citation_issues(broken, self.document)
        fixed, accepted = repair.apply_repairs(broken, self.response("flows.0.declaration", replacement), self.document, issues)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(fixed["flows"][0]["permission"], "deny")
        self.assertEqual(fixed["flows"][0]["policy_application"], broken["flows"][0]["policy_application"])
        self.assertEqual(repair.citation_issues(fixed, self.document), [])

    def test_null_replacement_keeps_the_original_failure_and_does_not_invent_evidence(self):
        broken, _, issues = self.broken_code()
        fixed, accepted = repair.apply_repairs(broken, self.response("flows.0.implementation", None), self.document, issues)
        self.assertEqual(fixed, broken)
        self.assertEqual(accepted, [])
        self.assertEqual(repair.citation_issues(fixed, self.document), issues)
        result = v4.decide_extraction(fixed, self.review, self.document, "toy")
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_lexical_candidates_do_not_change_the_proposal_or_establish_a_verdict(self):
        broken, _, issues = self.broken_code()
        before = copy.deepcopy(broken)
        request = repair.repair_request(broken, self.document, issues)
        self.assertEqual(request["input_binding"], self.document["sha256"])
        self.assertEqual(len(request["tasks"]), 1)
        task = request["tasks"][0]
        by_id = {part["id"]: part for part in self.document["segments"]}
        self.assertTrue(task["candidates"])
        self.assertLessEqual(len(task["candidates"]), 7)
        for candidate in task["candidates"]:
            self.assertEqual(by_id[candidate["segment_id"]]["path"], "generator.py")
        for related in task["related_valid_citations"]:
            self.assertEqual(v4._locate(related, self.document, "code")["path"], "generator.py")
        self.assertEqual(broken, before)
        self.assertNotIn("verdict", request)
        self.assertEqual(v4.decide_extraction(broken, self.review, self.document, "toy")["verdict"], "insufficient_evidence")

    def test_locatable_repair_still_requires_the_separate_semantic_review(self):
        broken, replacement, issues = self.broken_code()
        fixed, _ = repair.apply_repairs(broken, self.response("flows.0.implementation", replacement), self.document, issues)
        review = copy.deepcopy(self.review)
        review["flow_reviews"][0].update(supported=False, implementation_supported=False)
        self.assertEqual(repair.citation_issues(fixed, self.document), [])
        result = v4.decide_extraction(fixed, review, self.document, "toy")
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["evidence"][0]["source_validation"]["delivery_supported"])

    def test_repair_cannot_switch_the_original_code_file(self):
        broken, _, issues = self.broken_code()
        other_file = copy.deepcopy(broken["flows"][0]["delivery"]["citation"])
        self.assertEqual(v4._locate(other_file, self.document, "code")["path"], "evaluator.py")
        with self.assertRaisesRegex(ValueError, "source file"):
            repair.apply_repairs(broken, self.response("flows.0.implementation", other_file), self.document, issues)

    def test_repair_cannot_replace_a_code_boundary_with_paper_text(self):
        broken, _, issues = self.broken_code()
        paper_quote = copy.deepcopy(broken["flows"][0]["declaration"])
        with self.assertRaises(ValueError):
            repair.apply_repairs(broken, self.response("flows.0.implementation", paper_quote), self.document, issues)

    def test_unknown_targets_nonfailed_targets_and_non_citation_fields_are_rejected(self):
        broken, replacement, issues = self.broken_code()
        before = copy.deepcopy(broken)
        for target in ("flows.0.permission", "flows.0.policy_application.status", "flows.0.experiment_arm", "flows.0.declaration", "flows.-1.implementation", "flows.0.code_path.999.citation", "__class__"):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    repair.apply_repairs(broken, self.response(target, replacement), self.document, issues)
                self.assertEqual(broken, before)

    def test_extra_classification_fields_are_rejected_at_every_response_level(self):
        broken, replacement, issues = self.broken_code()
        for level in ("top", "repair", "citation"):
            with self.subTest(level=level):
                response = self.response("flows.0.implementation", copy.deepcopy(replacement))
                if level == "top":
                    response["permission"] = "allow"
                elif level == "repair":
                    response["repairs"][0]["policy_application"] = "applicable"
                else:
                    response["repairs"][0]["replacement"]["experiment_arm"] = "another channel"
                with self.assertRaises(ValueError):
                    repair.apply_repairs(broken, response, self.document, issues)

    def test_duplicate_repair_targets_are_rejected_without_mutating_original(self):
        broken, replacement, issues = self.broken_code()
        before = copy.deepcopy(broken)
        response = self.response("flows.0.implementation", replacement)
        response["repairs"].append(copy.deepcopy(response["repairs"][0]))
        with self.assertRaises(ValueError):
            repair.apply_repairs(broken, response, self.document, issues)
        self.assertEqual(broken, before)

    def test_false_ambiguous_and_unknown_segment_replacements_are_rejected(self):
        broken, replacement, issues = self.broken_code()
        for damage in ("false_quote", "ambiguous_quote", "unknown_segment"):
            with self.subTest(damage=damage):
                bad = copy.deepcopy(replacement)
                if damage == "false_quote":
                    bad["quote"] = "reply = nonexistent_function(private_task)"
                elif damage == "ambiguous_quote":
                    bad["quote"] = "reply"
                else:
                    bad["segment_id"] = "repo:unknown.py:L1-L3"
                with self.assertRaises(ValueError):
                    repair.apply_repairs(broken, self.response("flows.0.implementation", bad), self.document, issues)

    def test_empty_repairs_and_bounded_request_limit_keep_the_proposal_unchanged(self):
        broken, _, issues = self.broken_code()
        fixed, accepted = repair.apply_repairs(broken, {"repairs": []}, self.document, issues)
        self.assertEqual(fixed, broken)
        self.assertEqual(accepted, [])
        with self.assertRaises(ValueError):
            repair.repair_request(broken, self.document, issues * 25)

    def test_forged_issue_paths_cannot_turn_classification_fields_into_repair_targets(self):
        broken, replacement, issues = self.broken_code()
        before = copy.deepcopy(broken)
        forged = {**issues[0], "target": "flows.0.permission"}
        with self.assertRaisesRegex(ValueError, "currently failed citation"):
            repair.repair_request(broken, self.document, [forged])
        with self.assertRaisesRegex(ValueError, "currently failed citation"):
            repair.apply_repairs(broken, self.response(forged["target"], replacement), self.document, [forged])
        self.assertEqual(broken, before)

    def test_unknown_original_code_file_has_no_candidates_and_cannot_be_guessed(self):
        broken = copy.deepcopy(self.extraction)
        known_quote = copy.deepcopy(broken["flows"][0]["implementation"])
        broken["flows"][0]["implementation"]["segment_id"] = "repo:unverified-file.py:L1-L6"
        issues = repair.citation_issues(broken, self.document)
        self.assertEqual([issue["target"] for issue in issues], ["flows.0.implementation"])
        request = repair.repair_request(broken, self.document, issues)
        self.assertEqual(request["tasks"][0]["candidates"], [])
        self.assertEqual(request["tasks"][0]["related_valid_citations"], [])
        with self.assertRaisesRegex(ValueError, "guess an unverified source file"):
            repair.apply_repairs(broken, self.response("flows.0.implementation", known_quote), self.document, issues)
        fixed, accepted = repair.apply_repairs(broken, self.response("flows.0.implementation", None), self.document, issues)
        self.assertEqual(fixed, broken)
        self.assertEqual(accepted, [])

    def test_every_offered_choice_is_exact_unique_and_in_the_correct_source_domain(self):
        broken, _, _ = self.broken_code()
        broken["flows"][0]["declaration"]["quote"] = "An absent paper sentence."
        issues = repair.citation_issues(broken, self.document)
        request = repair.choice_request(broken, self.document, issues)
        by_target = {issue["target"]: issue for issue in issues}
        self.assertEqual(len(request["tasks"]), 2)
        for task in request["tasks"]:
            with self.subTest(target=task["target"]):
                self.assertTrue(task["choices"])
                self.assertLessEqual(len(task["choices"]), 14)
                ids = [choice["candidate_id"] for choice in task["choices"]]
                self.assertEqual(len(ids), len(set(ids)))
                kind = by_target[task["target"]]["source_kind"]
                for choice in task["choices"]:
                    locator = v4._locate(choice["citation"], self.document, kind)
                    self.assertEqual(locator["source_kind"], kind)
                    if kind == "code":
                        self.assertEqual(locator["path"], "generator.py")

    def test_candidate_id_selection_changes_only_its_failed_citation(self):
        broken, replacement, issues = self.broken_code()
        before = copy.deepcopy(broken)
        request = repair.choice_request(broken, self.document, issues)
        choice = next(option for option in request["tasks"][0]["choices"] if option["citation"] == replacement)
        response = {"choices": [{"target": "flows.0.implementation", "candidate_id": choice["candidate_id"], "reason": "This exact candidate cites the same request boundary."}]}
        fixed, accepted = repair.apply_choices(broken, response, self.document, issues, request)
        expected = copy.deepcopy(before)
        expected["flows"][0]["implementation"] = replacement
        self.assertEqual(fixed, expected)
        self.assertEqual(broken, before)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0]["after"], replacement)
        # Mechanical uniqueness is not a semantic vote. An independent reviewer
        # can still reject this input-boundary interpretation after selection.
        review = copy.deepcopy(self.review)
        review["flow_reviews"][0]["implementation_supported"] = False
        self.assertEqual(v4.decide_extraction(fixed, review, self.document, "toy")["verdict"], "insufficient_evidence")

    def test_unknown_candidate_ids_and_duplicate_choice_targets_are_rejected(self):
        broken, _, issues = self.broken_code()
        request = repair.choice_request(broken, self.document, issues)
        choice = {"target": "flows.0.implementation", "candidate_id": "candidate-not-offered", "reason": "Invalid ID"}
        with self.assertRaisesRegex(ValueError, "unknown citation candidate ID"):
            repair.apply_choices(broken, {"choices": [choice]}, self.document, issues, request)
        choice["candidate_id"] = request["tasks"][0]["choices"][0]["candidate_id"]
        with self.assertRaisesRegex(ValueError, "repeated citation choice target"):
            repair.apply_choices(broken, {"choices": [choice, copy.deepcopy(choice)]}, self.document, issues, request)

    def test_prepared_candidate_ids_quotes_context_or_binding_cannot_be_tampered_with(self):
        broken, _, issues = self.broken_code()
        original = repair.choice_request(broken, self.document, issues)
        for field in ("id", "quote", "context", "binding"):
            with self.subTest(field=field):
                request = copy.deepcopy(original)
                option = request["tasks"][0]["choices"][0]
                if field == "id":
                    option["candidate_id"] = "forged-candidate"
                elif field == "quote":
                    option["citation"]["quote"] = "A fabricated source quote."
                elif field == "context":
                    option["context"] += " Forged supporting prose."
                else:
                    request["input_binding"] = "another-source-version"
                with self.assertRaisesRegex(ValueError, "candidates changed"):
                    repair.apply_choices(broken, {"choices": []}, self.document, issues, request)

    def test_null_candidate_id_preserves_the_original_unverifiable_citation(self):
        broken, _, issues = self.broken_code()
        request = repair.choice_request(broken, self.document, issues)
        response = {"choices": [{"target": "flows.0.implementation", "candidate_id": None, "reason": "No offered context supports the claimed request input."}]}
        fixed, accepted = repair.apply_choices(broken, response, self.document, issues, request)
        self.assertEqual(fixed, broken)
        self.assertEqual(accepted, [])
        self.assertEqual(repair.citation_issues(fixed, self.document), issues)

    def test_repetitive_file_with_no_unique_pointer_offers_no_choices_instead_of_guessing(self):
        paper, repository, _, extraction, _ = toy.ExtractionV4Tests().fixtures()
        repeated = toy.code_segment("repeated.py", "consume(shared_value)\n" * 160)
        repository = toy.source_bundle(repository["segments"] + [repeated])
        document = v4.combine_inputs(paper, repository)
        extraction["input_binding"] = document["sha256"]
        extraction["flows"][0]["implementation"] = {"segment_id": repeated["id"], "quote": "consume(shared_value)"}
        issues = repair.citation_issues(extraction, document)
        self.assertEqual([issue["target"] for issue in issues], ["flows.0.implementation"])
        request = repair.choice_request(extraction, document, issues)
        self.assertEqual(request["tasks"][0]["choices"], [])
        response = {"choices": [{"target": "flows.0.implementation", "candidate_id": "c1", "reason": "Guessing is prohibited."}]}
        with self.assertRaisesRegex(ValueError, "unknown citation candidate ID"):
            repair.apply_choices(extraction, response, document, issues, request)


if __name__ == "__main__":
    unittest.main()
