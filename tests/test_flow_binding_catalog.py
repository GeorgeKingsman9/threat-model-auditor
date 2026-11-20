"""Keep the separately counted binding rules tied to their implementation."""

import ast
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import rule_catalog
import scope_review


class FlowBindingCatalogTests(unittest.TestCase):
    def test_binding_rules_cover_every_branch_in_order(self):
        data = rule_catalog.catalog()
        rules = data["flow_binding_rules"]
        self.assertEqual(data["counts"]["business_rules"], 30)
        self.assertEqual(data["counts"]["flow_binding_rules"], len(rules))
        tree = ast.parse((ROOT / "scope_review.py").read_text(encoding="utf-8"))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_assess_bound_claim")
        returns = sorted((node for node in ast.walk(function)
                          if isinstance(node, ast.Return) and isinstance(node.value, ast.Call)
                          and isinstance(node.value.func, ast.Name) and node.value.func.id == "result"),
                         key=lambda node: node.lineno)
        positions = {}
        for rule in rules:
            self.assertEqual(rule["functions"], ["scope_review._assess_bound_claim"])
            for field in ("condition", "result", "positive_example", "negative_example"):
                self.assertTrue(rule[field].strip())
            for position in rule["priority"]["flow_binding"]:
                self.assertNotIn(position, positions)
                positions[position] = rule["reason_codes"]
        self.assertEqual(sorted(positions), list(range(1, len(returns) + 1)))
        for position, node in enumerate(returns, 1):
            self.assertIn(node.value.args[1].value, positions[position])
        actual = {node.value.args[1].value for node in returns}
        self.assertEqual(actual, {code for rule in rules for code in rule["reason_codes"]})

    def test_binding_enums_and_exports_match_source(self):
        data = rule_catalog.catalog()
        for field, expected in (("recipient_role", scope_review.RECIPIENT_ROLES),
                                ("attacker_delivery", scope_review.ATTACKER_DELIVERY_STATES),
                                ("instance_requirement", scope_review.INSTANCE_REQUIREMENTS),
                                ("instance_relation", scope_review.INSTANCE_RELATIONS)):
            self.assertEqual(set(data["value_options"]["flow_binding." + field]), expected)
        self.assertIn("flow_binding_v1", data["value_options"]["validation_mode"])
        self.assertEqual(json.loads((ROOT / "docs" / "RULES.json").read_text(encoding="utf-8")), data)
        self.assertEqual((ROOT / "docs" / "RULES_ZH.md").read_text(encoding="utf-8"), rule_catalog.markdown())


if __name__ == "__main__":
    unittest.main()
