"""Citation-only recovery can update new array-valued evidence pointers."""

import copy
import unittest

from citation_repair import apply_repairs, citation_issues
import test_extraction_v6 as channels
import test_v6_deployment_integration as deployment


class V6CitationRepairTests(unittest.TestCase):
    def repair(self, extraction, document, target, original):
        issues = citation_issues(extraction, document)
        selected = [item for item in issues if item["target"] == target]
        self.assertEqual(len(selected), 1)
        before = copy.deepcopy(extraction)
        fixed, accepted = apply_repairs(extraction, {"repairs": [{"target": target,
            "replacement": original, "reason": "Restore the exact existing source pointer."}]}, document, selected)
        self.assertEqual(extraction, before)
        self.assertEqual(len(accepted), 1)
        self.assertNotIn(target, [item["target"] for item in citation_issues(fixed, document)])
        self.assertEqual(fixed["flows"], extraction["flows"])
        return fixed

    def test_channel_citation_list_final_index(self):
        _, _, document, extraction, _ = channels.ExtractionV6Tests().fixtures()
        candidate = document["model_repository"]["input_channels"]["candidates"][0]
        original = copy.deepcopy(candidate["citation"])
        extraction["channel_assessments"][0]["citations"] = [{**original, "quote": "missing code quote"}]
        fixed = self.repair(extraction, document, "channel_assessments.0.citations.0", original)
        self.assertEqual(fixed["channel_assessments"][0]["citations"][0], original)

    def test_deployment_construction_citation_list_final_index(self):
        document, extraction, _ = deployment.V6DeploymentIntegrationTests().fixtures()
        fact = extraction["deployment_findings"][0]["conditional_construction"]
        original = copy.deepcopy(fact["citations"][0])
        fact["citations"][0]["quote"] = "missing construction quote"
        fixed = self.repair(extraction, document, "deployment_findings.0.conditional_construction.citations.0", original)
        self.assertEqual(fixed["deployment_findings"][0]["conditional_construction"]["citations"][0], original)


if __name__ == "__main__":
    unittest.main()
