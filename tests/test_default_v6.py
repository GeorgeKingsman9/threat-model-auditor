"""One paper argument selects V6 and never reads curated expected labels."""

from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scan
import test_extraction_v6 as fixtures


def paper_contract(paper_hash):
    def missing():
        return {"status": "unspecified", "text": "Not established in this synthetic first pass.", "citations": []}
    return {"schema_version": 1, "paper_sha256": paper_hash, "knowledge_rules": [],
        "task_input_definition": {"definition": missing(), "components": [], "relationships": []},
        "construction_recipe": {"procedure": missing(), "metadata_budget": missing(),
            "inputs": [], "generated_artifacts": [], "scope": missing()},
        "unresolved_questions": ["Synthetic proposal remains untrusted."], "limitations": []}


class DefaultV6Tests(unittest.TestCase):
    def test_one_url_defaults_to_v6_with_channel_and_deployment_outputs(self):
        paper, repository, _, extraction, review = fixtures.ExtractionV6Tests().fixtures()
        source = "https://example.org/new-paper.pdf"; paper["source"] = source
        class Client:
            max_calls = 3
            def __init__(self): self.calls = []
            def generate(self, prompt, content, schema):
                self.calls.append(copy.deepcopy(content))
                if "input_binding" not in content:
                    return paper_contract(content["paper_sha256"])
                result = copy.deepcopy(review if "proposal" in content else extraction)
                result["input_binding"] = content["input_binding"]
                return result
            def ledger(self): return {"calls": len(self.calls), "provider": "test-only"}
        client = Client()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "auto"
            with patch.object(scan, "default_output_directory", return_value=output), \
                 patch.object(scan, "load_document", return_value=paper), \
                 patch.object(scan, "discover_repository", return_value={"status": "selected", "repository": "https://github.com/toy/source", "revision": repository["revision"]}), \
                 patch("source_bundle.load_repository", return_value=repository) as loader, \
                 patch.object(scan, "get_client", return_value=client), redirect_stdout(io.StringIO()) as console:
                self.assertEqual(scan.main([source]), 0)
            row = json.loads((output / "result.json").read_text())
            self.assertEqual(row["schema_version"], 6)
            self.assertIs(row["inconsistency"], True)
            self.assertIn("channel_coverage", row)
            self.assertIn("deployment_assessment", row)
            self.assertIn("evidence_policy", loader.call_args.kwargs)
            self.assertIn("deployment_findings", json.loads(console.getvalue()))
            self.assertEqual(len(client.calls), 3)
            self.assertEqual(set(client.calls[0]), {"source_type", "segments", "paper_sha256"})
            self.assertNotIn("repository", client.calls[0])
            self.assertTrue(all(not p["id"].startswith("paper:") for p in client.calls[0]["segments"]))
            contract = json.loads((output / "declared_contract.json").read_text())
            self.assertEqual(contract["trust"], "untrusted_declared_contract_proposal")
            self.assertTrue(contract["semantic_review_required"])
            self.assertIn("declared_contract_proposal", client.calls[1]["repository"])
            self.assertNotIn('"expected"', json.dumps(client.calls))


if __name__ == "__main__":
    unittest.main()
