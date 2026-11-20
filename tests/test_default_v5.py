"""The one-argument CLI defaults to automatic V5 and reports grounded locations."""
from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import scan
from findings import project_result
import test_extraction_v5 as fixtures


class DefaultV5Tests(unittest.TestCase):
    def test_single_paper_url_produces_v5_verdict_and_locations_without_other_inputs(self):
        paper, repository, _, extraction, review = fixtures.ExtractionV5Tests().fixtures()
        source = "https://example.org/uploaded.pdf"
        paper["source"] = source
        class Client:
            max_calls = 3
            def __init__(self): self.calls = []
            def generate(self, prompt, content, schema):
                self.calls.append(copy.deepcopy(content))
                result = copy.deepcopy(review if "proposal" in content else extraction)
                result["input_binding"] = content["input_binding"]
                return result
            def ledger(self): return {"calls": len(self.calls), "provider": "test-only"}
        client = Client()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "auto-output"
            with patch.object(scan, "default_output_directory", return_value=output), \
                 patch.object(scan, "load_document", return_value=paper), \
                 patch.object(scan, "discover_repository", return_value={"status": "selected", "repository": "https://github.com/toy/source", "revision": repository["revision"]}), \
                 patch("source_bundle.load_repository", return_value=repository), \
                 patch.object(scan, "get_client", return_value=client), redirect_stdout(io.StringIO()) as console:
                code = scan.main([source])
            self.assertEqual(code, 0)
            row = json.loads((output / "result.json").read_text())
            self.assertEqual(row["schema_version"], 5)
            self.assertIs(row["inconsistency"], True)
            self.assertTrue(row["findings"][0]["paper_locations"])
            self.assertTrue(row["findings"][0]["code_locations"])
            self.assertIn("findings", json.loads(console.getvalue()))
            self.assertEqual(len(client.calls), 2)
            self.assertNotIn("expected", json.dumps(client.calls))
            request = json.loads((output / "request.json").read_text())
            self.assertEqual(request["max_input_chars"], 1200000)
            self.assertEqual(request["max_code_chars"], 500000)

    def test_uncertainty_and_failure_are_not_false_negative_answers(self):
        for verdict in ["insufficient_evidence", "technical_failure", "not_run", "not_applicable"]:
            self.assertIsNone(project_result({"verdict": verdict})["inconsistency"])
        self.assertIs(project_result({"verdict": "consistent_within_scope"})["inconsistency"], False)

    def test_repeated_grounded_code_location_is_reported_once(self):
        locator = {"source_kind": "code", "path": "attack.py", "line_start": 7,
                   "line_end": 9, "repository_source": "https://github.com/owner/source",
                   "repository_revision": "a" * 40}
        row = project_result({"verdict": "inconsistent", "evidence": [{
            "claim_result": "confirmed", "locators": {"implementation": locator},
            "source_validation": {"code_path_locators": [copy.deepcopy(locator)]}}]})
        locations = row["findings"][0]["code_locations"]
        self.assertEqual(len(locations), 1)
        self.assertTrue(locations[0]["url"].endswith("/attack.py#L7"))


if __name__ == "__main__": unittest.main()
