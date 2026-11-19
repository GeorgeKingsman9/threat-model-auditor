"""Keep the exported inventory aligned with real branches, enums and manual.

These tests inspect local source and export documentation. They do not run a
research repository, ingest a document, download code, or call a model.
"""

import ast
from collections import Counter
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import checker
import extraction_v3
import extraction_v4
import rule_catalog
import scope_review


def function_node(module, name):
    tree = ast.parse((ROOT / (module + ".py")).read_text(encoding="utf-8"))
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)


def branch_reasons(module, name):
    """Return literal reason outcomes in source order, including repeated gates."""
    function = function_node(module, name)
    if name == "decide":
        returns = sorted((node for node in ast.walk(function) if isinstance(node, ast.Return)), key=lambda node: node.lineno)
        return [node.value.elts[1].value for node in returns]
    if name == "assess_claim":
        returns = sorted((node for node in ast.walk(function)
                          if isinstance(node, ast.Return) and isinstance(node.value, ast.Call)
                          and isinstance(node.value.func, ast.Name) and node.value.func.id == "result"),
                         key=lambda node: node.lineno)
        return [node.value.args[1].value for node in returns]
    assignments = sorted((node for node in ast.walk(function) if isinstance(node, ast.Assign)
                          and any(isinstance(target, ast.Name) and target.id == "reason" for target in node.targets)),
                         key=lambda node: node.lineno)
    values = []
    for node in assignments:
        if isinstance(node.value, ast.Constant):
            values.append(node.value.value)
        else:
            values.extend((node.value.body.value, node.value.orelse.value))
    return values


class RuleCatalogTests(unittest.TestCase):
    def test_counts_come_from_entries_with_an_explicit_separate_denominator(self):
        data = rule_catalog.catalog()
        self.assertEqual(data["counts"]["business_rules"], len(data["rules"]))
        self.assertEqual(data["counts"]["business_by_group"], dict(Counter(rule["group"] for rule in data["rules"])))
        self.assertEqual(data["counts"]["business_by_group"], {"base": 8, "scope": 19, "paper": 3})
        self.assertEqual(data["counts"]["source_validation_rules"], len(data["source_validation_rules"]))
        self.assertEqual(data["counts"]["source_validation_rules"], 15)
        self.assertEqual(data["counts"]["extraction_v3_gate_groups"], len(data["validation_summary"]["extraction_v3_gates"]))
        self.assertEqual(data["counts"]["structural_validation_groups"], len(data["validation_summary"]["structure_checks"]))
        self.assertEqual(data["counts"]["value_option_groups"], len(data["value_options"]))
        self.assertTrue(data["counts"]["v4_included"])

    def test_every_core_reason_and_its_priority_match_the_owning_function(self):
        rules = rule_catalog.catalog()["rules"]
        for group, module, function in (("base", "checker", "decide"),
                                         ("scope", "scope_review", "assess_claim"),
                                         ("paper", "checker", "summarize_paper")):
            with self.subTest(group=group):
                positioned = sorted((position, rule["reason_codes"])
                                    for rule in rules for position in rule["priority"].get(group, []))
                self.assertEqual([position for position, _ in positioned], list(range(1, len(positioned) + 1)))
                listed = [code for _, codes in positioned for code in codes]
                self.assertEqual(listed, branch_reasons(module, function))

    def test_reused_core_checks_are_not_counted_twice(self):
        rules = rule_catalog.catalog()["rules"]
        by_code = {}
        for rule in rules:
            for code in rule["reason_codes"]:
                self.assertNotIn(code, by_code)
                by_code[code] = rule["id"]
        self.assertEqual(by_code["conflicting_policy"], "B02")
        self.assertEqual(by_code["conflicting_observations"], "B03")
        self.assertEqual(by_code["policy_scope_evidence_missing"], "S04")
        self.assertEqual(by_code["delivery_to_input_boundary_not_established"], "S06")
        self.assertEqual(by_code["unresolved_checks"], by_code["audit_scope_not_fully_covered"])

    def test_entries_have_examples_and_real_code_function_mappings(self):
        data = rule_catalog.catalog()
        entries = data["rules"] + data["source_validation_rules"] + data["validation_summary"]["extraction_v3_gates"]
        self.assertEqual(len(entries), len({entry["id"] for entry in entries}))
        for entry in entries:
            with self.subTest(rule=entry["id"]):
                for field in ("condition", "result", "positive_example", "negative_example"):
                    self.assertTrue(entry[field].strip())
                self.assertIsInstance(entry["reason_codes"], list)
                self.assertTrue(entry["priority"])
                self.assertTrue(entry["functions"])
                for reference in entry["functions"]:
                    module, name = reference.rsplit(".", 1)
                    self.assertIsInstance(function_node(module, name), ast.FunctionDef)
        for group in data["validation_summary"]["structure_checks"]:
            for reference in group["functions"]:
                module, name = reference.rsplit(".", 1)
                self.assertIsInstance(function_node(module, name), ast.FunctionDef)

    def test_v3_extraction_outcome_and_error_codes_are_in_the_gate_inventory(self):
        function = function_node("extraction_v3", "decide_extraction")
        codes = set()
        for node in ast.walk(function):
            if isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if isinstance(key, ast.Constant) and key.value == "reason" and isinstance(value, ast.Constant):
                        codes.add(value.value)
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "append" and node.args and isinstance(node.args[0], ast.Constant)):
                codes.add(node.args[0].value)
        entries = rule_catalog.catalog()["validation_summary"]["extraction_v3_gates"]
        self.assertEqual(codes, {code for entry in entries for code in entry["reason_codes"]})

    def test_v4_path_and_scope_failures_are_not_hidden_from_the_source_inventory(self):
        actual = set()
        prefixes = ("source_path_", "source_boundary_", "source_snapshot_", "scope_resolution_", "common_contract_", "declaration_source:")
        for name in ("_scope_check", "_path_check", "decide_extraction"):
            for node in ast.walk(function_node("extraction_v4", name)):
                error_expression = None
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr == "append" and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "errors"):
                    error_expression = node.args[0]
                elif (isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple)
                      and isinstance(node.value.elts[-1], ast.List)):
                    error_expression = node.value.elts[-1]
                if error_expression is not None:
                    for value in ast.walk(error_expression):
                        if isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value.startswith(prefixes):
                            actual.add(value.value.split(":", 1)[0])
        listed = {code for rule in rule_catalog.catalog()["source_validation_rules"] for code in rule["reason_codes"]}
        self.assertEqual(actual, listed)

    def test_value_options_match_core_and_extraction_schemas(self):
        values = rule_catalog.catalog()["value_options"]
        constants = {
            "permission": checker.PERMISSIONS, "observation": checker.OBSERVATION_STATES,
            "verdict": checker.VERDICTS, "query_form": checker.QUERY_FORMS,
            "issue_type": scope_review.ISSUE_TYPES, "information_level": scope_review.INFORMATION_LEVELS,
            "policy_kind": scope_review.POLICY_KINDS, "policy_application.status": scope_review.POLICY_STATES,
            "delivery.status": scope_review.DELIVERY_STATES, "delivery.evidence_kind": scope_review.EVIDENCE_KINDS,
            "delivery.task_relation": scope_review.TASK_RELATIONS, "refutation.basis": scope_review.REFUTATION_BASES,
        }
        for key, expected in constants.items():
            with self.subTest(field=key):
                self.assertEqual(set(values[key]), expected)
        self.assertEqual(set(rule_catalog.catalog()["validation_summary"]["boundary_evidence_kinds"]), scope_review.BOUNDARY_EVIDENCE)
        for name, key in (("permission", "permission"), ("observation", "observation")):
            self.assertEqual(values["extraction_v3." + name], extraction_v3.FLOW_SCHEMA["properties"][key]["enum"])
        for name in ("basis", "override_dimension"):
            self.assertEqual(values["extraction_v4.scope_resolution." + name], extraction_v4.SCOPE_RESOLUTION["properties"][name]["enum"])
        self.assertEqual(values["extraction_v4.code_path.kind"], extraction_v4.PATH_STEP["properties"]["kind"]["enum"])

    def test_manual_is_generated_from_this_inventory_and_its_counts(self):
        self.assertEqual((ROOT / "docs" / "RULES_ZH.md").read_text(encoding="utf-8"), rule_catalog.markdown())

    def test_citation_recovery_is_a_bounded_workflow_under_the_existing_rules(self):
        data = rule_catalog.catalog()
        recovery = data["validation_summary"]["citation_recovery"]
        self.assertFalse(recovery["counts_as_new_rule"])
        self.assertEqual(data["counts"]["business_rules"], 30)
        self.assertEqual(data["counts"]["source_validation_rules"], 15)
        self.assertEqual(recovery["max_repair_calls"], 1)
        self.assertEqual(recovery["max_issues_per_request"], 24)
        self.assertTrue(recovery["budget_required"])
        self.assertEqual(recovery["mutable_fields"], ["failed_citation_pointers_only"])
        self.assertIn("code_path_structure", recovery["immutable_fields"])
        self.assertIn("fresh independent review", recovery["final_acceptance"])
        self.assertIn("never evidence", recovery["candidate_status"])
        source_rules = {rule["id"]: rule for rule in data["source_validation_rules"]}
        for reference in recovery["functions"]:
            module, name = reference.rsplit(".", 1)
            self.assertIsInstance(function_node(module, name), ast.FunctionDef)
            self.assertIn(reference, source_rules["SRC06"]["functions"])
            self.assertIn(reference, source_rules["SRC08"]["functions"])

    def test_export_is_json_and_callers_cannot_mutate_future_exports(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(rule_catalog.main([]), 0)
        expected = rule_catalog.catalog()
        self.assertEqual(json.loads(output.getvalue()), expected)
        changed = rule_catalog.catalog()
        changed["rules"][0]["reason_codes"].clear()
        changed["source_validation_rules"].clear()
        changed["validation_summary"]["extraction_v3_gates"].clear()
        changed["value_options"]["permission"].append("invented")
        self.assertEqual(rule_catalog.catalog(), expected)


if __name__ == "__main__":
    unittest.main()
