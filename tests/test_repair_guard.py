"""Offline selection isolation; source/request guards remain strict."""

import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import citation_repair as repair
import repair_guard as guard
import test_extraction_v4 as toy
import test_extraction_v6 as channels
import test_v6_deployment_integration as deployment


class BoundedCitationChoiceTests(unittest.TestCase):
    def fixtures(self):
        _, _, document, extraction, _ = toy.ExtractionV4Tests().fixtures()
        extraction["flows"][0]["implementation"]["quote"] = "missing implementation pointer"
        extraction["flows"][0]["declaration"]["quote"] = "missing declaration pointer"
        issues = repair.citation_issues(extraction, document)
        request = repair.choice_request(extraction, document, issues)
        self.assertTrue(all(task["choices"] for task in request["tasks"]))
        return document, extraction, issues, request

    def selection(self, request, target, candidate_id="first"):
        task = next(task for task in request["tasks"] if task["target"] == target)
        return {"target": target,
                "candidate_id": task["choices"][0]["candidate_id"] if candidate_id == "first" else candidate_id,
                "reason": "Use only the mechanically offered exact pointer."}

    def pointer(self, value, path):
        for key in path.split("."):
            value = value[int(key)] if isinstance(value, list) else value[key]
        return value

    def test_mixed_valid_and_unknown_ids_preserve_invalid_pointer_and_classification(self):
        document, extraction, issues, request = self.fixtures()
        before = copy.deepcopy(extraction)
        response = {"choices": [self.selection(request, "flows.0.declaration"),
                                self.selection(request, "flows.0.implementation", "c12 debugger")]}
        response_before = copy.deepcopy(response)
        with patch.object(guard, "apply_choices", wraps=repair.apply_choices) as strict:
            fixed, accepted, rejected = guard.apply_bounded_choices(extraction, response, document, issues, request)
        strict.assert_called_once()
        self.assertEqual(strict.call_args.args[1], {"choices": [response["choices"][0]]})
        self.assertEqual([item["target"] for item in accepted], ["flows.0.declaration"])
        self.assertEqual(rejected, [{"index": 1, "target": "flows.0.implementation", "candidate_id": "c12 debugger",
                                   "reason": "unknown_candidate_id", "selection_reason": response["choices"][1]["reason"]}])
        expected = copy.deepcopy(before)
        expected["flows"][0]["declaration"] = accepted[0]["after"]
        self.assertEqual(fixed, expected)
        self.assertEqual(extraction, before)
        self.assertEqual(response, response_before)

    def test_unknown_target_cannot_modify_classification_or_prevent_valid_repair(self):
        document, extraction, issues, request = self.fixtures()
        valid = self.selection(request, "flows.0.implementation")
        for unknown_target in ("flows.0.permission", "flows.0.implementation debugger", "unknown.pointer"):
            with self.subTest(target=unknown_target):
                unknown = {**valid, "target": unknown_target}
                fixed, accepted, rejected = guard.apply_bounded_choices(
                    extraction, {"choices": [unknown, valid]}, document, issues, request)
                self.assertEqual(len(accepted), 1)
                self.assertEqual(rejected[0]["reason"], "unknown_target")
                expected = copy.deepcopy(extraction)
                expected["flows"][0]["implementation"] = accepted[0]["after"]
                self.assertEqual(fixed, expected)

    def test_candidate_ids_are_exact_and_never_trimmed_or_guessed(self):
        document, extraction, issues, request = self.fixtures()
        valid = self.selection(request, "flows.0.implementation")
        for bad_id in (valid["candidate_id"] + " debugger", " " + valid["candidate_id"],
                       valid["candidate_id"] + " ", valid["candidate_id"].upper(), "c999"):
            with self.subTest(candidate_id=bad_id):
                fixed, accepted, rejected = guard.apply_bounded_choices(
                    extraction, {"choices": [{**valid, "candidate_id": bad_id}]}, document, issues, request)
                self.assertEqual(fixed, extraction)
                self.assertEqual(accepted, [])
                self.assertEqual(rejected[0]["candidate_id"], bad_id)
                self.assertEqual(rejected[0]["reason"], "unknown_candidate_id")

    def test_every_duplicate_target_choice_is_rejected_before_applying_any_occurrence(self):
        document, extraction, issues, request = self.fixtures()
        unique = self.selection(request, "flows.0.declaration")
        first = self.selection(request, "flows.0.implementation")
        for second_id in (first["candidate_id"], "c12 debugger", None):
            with self.subTest(second_id=second_id):
                choices = [first, unique, {**first, "candidate_id": second_id}]
                fixed, accepted, rejected = guard.apply_bounded_choices(
                    extraction, {"choices": choices}, document, issues, request)
                self.assertEqual([item["target"] for item in accepted], [unique["target"]])
                self.assertEqual([item["index"] for item in rejected], [0, 2])
                self.assertEqual([item["reason"] for item in rejected], ["duplicate_target"] * 2)
                self.assertEqual(fixed["flows"][0]["implementation"], extraction["flows"][0]["implementation"])

    def test_unique_null_abstains_without_rejection_and_without_changing_pointer(self):
        document, extraction, issues, request = self.fixtures()
        choice = self.selection(request, "flows.0.implementation", None)
        fixed, accepted, rejected = guard.apply_bounded_choices(
            extraction, {"choices": [choice]}, document, issues, request)
        self.assertEqual(fixed, extraction)
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, [])

    def test_malformed_response_is_a_strict_failure_before_partial_application(self):
        document, extraction, issues, request = self.fixtures()
        before = copy.deepcopy(extraction)
        valid = self.selection(request, "flows.0.implementation")
        for response in ({"choices": [valid], "permission": "allow"},
                         {"choices": [{**valid, "candidate_id": 1}]},
                         {"choices": [{**valid, "replacement": {"quote": "invented"}}]},
                         {"choices": [valid, {"target": "unknown"}]},
                         {"choices": None}):
            with self.subTest(response=response):
                with self.assertRaises(ValueError):
                    guard.apply_bounded_choices(extraction, response, document, issues, request)
                self.assertEqual(extraction, before)

    def test_request_tampering_is_fatal_even_when_all_selections_would_be_filtered(self):
        document, extraction, issues, request = self.fixtures()
        for damage in ("id", "quote", "context", "binding", "target"):
            with self.subTest(damage=damage):
                altered = copy.deepcopy(request)
                choice = altered["tasks"][0]["choices"][0]
                if damage == "id":
                    choice["candidate_id"] += " debugger"
                elif damage == "quote":
                    choice["citation"]["quote"] = "invented exact-looking quote"
                elif damage == "context":
                    choice["context"] += " altered"
                elif damage == "target":
                    altered["tasks"][0]["target"] = "flows.0.permission"
                else:
                    altered["input_binding"] = "different-document"
                with self.assertRaisesRegex(ValueError, "candidates changed"):
                    guard.apply_bounded_choices(extraction, {"choices": []}, document, issues, altered)

    def test_forged_issue_is_a_strict_failure_and_legacy_applicator_is_unchanged(self):
        document, extraction, issues, request = self.fixtures()
        forged = [{**issues[0], "target": "flows.0.permission"}]
        with self.assertRaisesRegex(ValueError, "currently failed citation"):
            guard.apply_bounded_choices(extraction, {"choices": []}, document, forged, request)
        invalid = self.selection(request, "flows.0.implementation", "c12 debugger")
        with self.assertRaisesRegex(ValueError, "unknown citation candidate ID"):
            repair.apply_choices(extraction, {"choices": [invalid]}, document, issues, request)

    def test_strict_apply_failure_propagates_instead_of_becoming_a_rejected_selection(self):
        document, extraction, issues, request = self.fixtures()
        response = {"choices": [self.selection(request, "flows.0.implementation")]}
        with patch.object(guard, "apply_choices", side_effect=ValueError("strict boundary failed")):
            with self.assertRaisesRegex(ValueError, "strict boundary failed"):
                guard.apply_bounded_choices(extraction, response, document, issues, request)

    def test_v6_channel_list_pointer_is_repaired_without_changing_channel_assessment(self):
        _, _, document, extraction, _ = channels.ExtractionV6Tests().fixtures()
        original = copy.deepcopy(document["model_repository"]["input_channels"]["candidates"][0]["citation"])
        extraction["channel_assessments"][0]["citations"] = [{**original, "quote": "missing channel quote"}]
        self.check_v6_pointer(document, extraction, "channel_assessments.0.citations.0")

    def test_v6_deployment_list_pointer_is_repaired_without_changing_deployment_assessment(self):
        document, extraction, _ = deployment.V6DeploymentIntegrationTests().fixtures()
        extraction["deployment_findings"][0]["conditional_construction"]["citations"][0]["quote"] = "missing construction quote"
        self.check_v6_pointer(document, extraction, "deployment_findings.0.conditional_construction.citations.0")

    def check_v6_pointer(self, document, extraction, target):
        before = copy.deepcopy(extraction)
        issues = repair.citation_issues(extraction, document)
        request = repair.choice_request(extraction, document, issues)
        selected = self.selection(request, target)
        fixed, accepted, rejected = guard.apply_bounded_choices(
            extraction, {"choices": [selected]}, document, issues, request)
        self.assertEqual([item["target"] for item in accepted], [target])
        self.assertEqual(rejected, [])
        expected = copy.deepcopy(before)
        parent_path, _, last = target.rpartition(".")
        self.pointer(expected, parent_path)[int(last)] = accepted[0]["after"]
        self.assertEqual(fixed, expected)
        self.assertEqual(extraction, before)
        self.assertNotIn(target, [issue["target"] for issue in repair.citation_issues(fixed, document)])


if __name__ == "__main__":
    unittest.main()
