"""Fresh one-URL routing and bounded review failure recovery, with synthetic data."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
import io

import scan
import extraction_v7 as v7
from test_default_v6 import paper_contract
import test_extraction_v6 as v6_fixtures


def fixtures():
    paper, repository, _, extraction, review = v6_fixtures.ExtractionV6Tests().fixtures()
    source = "https://example.org/new-unknown-paper.pdf"
    paper["source"] = source
    extraction.update(schema_version=7, construction_findings=[], category_assessments=[])
    review.update(schema_version=7, construction_reviews=[], category_reviews=[])
    for category in v7.CATEGORIES:
        extraction["category_assessments"].append({"category": category, "status": "unresolved",
            "finding_indices": [], "citations": [], "reason": "Synthetic coverage remains open."})
        review["category_reviews"].append({"category": category, "assessment_supported": False,
                                            "reason": "No global negative claim."})
    return source, paper, repository, extraction, review


class Client:
    def __init__(self, extraction, review, failure=None, max_calls=5):
        self.extraction, self.review = extraction, review
        self.failure, self.max_calls = failure, max_calls
        self.calls, self.payloads, self.review_calls = [], [], 0

    def generate(self, prompt, content, schema):
        self.payloads.append(copy.deepcopy(content))
        entry = {"status": "completed", "request_sha256": hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()}
        self.calls.append(entry)
        if "input_binding" not in content:
            return paper_contract(content["paper_sha256"])
        if "dependency_audits" in schema.get("properties", {}):
            return {"input_binding": content["input_binding"], "dependency_audits": []}
        if "proposal" in content:
            self.review_calls += 1
            if self.failure and self.review_calls == 1:
                entry["status"] = self.failure
                raise ValueError("Codex CLI failed (" + self.failure + "); safe synthetic failure")
            result = copy.deepcopy(self.review)
        else:
            result = copy.deepcopy(self.extraction)
        result["input_binding"] = content["input_binding"]
        return result

    def ledger(self):
        return {"provider": "test-only", "calls": copy.deepcopy(self.calls), "max_calls": self.max_calls}


class DefaultV7Tests(unittest.TestCase):
    def run_fixture(self, output, failure=None, max_calls=5, retries=1, use_cli=False):
        source, paper, repository, extraction, review = fixtures()
        client = Client(extraction, review, failure, max_calls)
        with patch.object(scan, "load_document", return_value=paper), \
             patch.object(scan, "discover_repository", return_value={"status": "selected", "repository": "https://github.com/synthetic/source", "revision": repository["revision"]}), \
             patch("source_bundle.load_repository", return_value=repository), \
             patch.object(scan, "get_client", return_value=client), redirect_stdout(io.StringIO()):
            if use_cli:
                code = scan.main([source, "--output", str(output)])
                row = json.loads((output / "result.json").read_text())
                self.assertEqual(code, 0)
            else:
                row = scan.scan_source(source, output, client=client, engine_version=7, review_retries=retries)
        return row, client

    def test_one_url_defaults_to_three_categories_and_paper_only_first_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            row, client = self.run_fixture(Path(temp) / "fresh", use_cli=True)
            self.assertEqual(row["schema_version"], 7)
            self.assertIs(row["inconsistency"], True)
            self.assertEqual(row["confirmed_issue_types"], ["knowledge_boundary_violation"])
            self.assertEqual(len(client.calls), 4)
            self.assertEqual(set(client.payloads[0]), {"source_type", "segments", "paper_sha256"})
            self.assertNotIn("repository", client.payloads[0])
            self.assertNotIn('"expected"', json.dumps(client.payloads))
            self.assertIn("issue_type", row["findings"][0])
            self.assertIn("acquisition_pass", [stage["stage"] for stage in row["stages"]])

    def test_failed_review_retries_once_with_identical_automatic_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "recovered"
            row, client = self.run_fixture(output, failure="cli_failed")
            self.assertEqual(row["status"], "completed")
            self.assertEqual(client.review_calls, 2)
            self.assertEqual(client.payloads[-2], client.payloads[-1])
            self.assertTrue((output / "semantic_review.attempt1.failure.json").is_file())
            self.assertTrue((output / "inference.semantic_review.json").is_file())
            self.assertTrue((output / "inference.semantic_review_retry1.json").is_file())
            stages = {s["stage"]: s["status"] for s in row["stages"]}
            self.assertEqual(stages["semantic_review"], "failed")
            self.assertEqual(stages["semantic_review_retry1"], "completed")
            self.assertEqual(len(client.calls), 4)

    def test_exhausted_call_cap_preserves_failure_without_retry(self):
        with tempfile.TemporaryDirectory() as temp:
            row, client = self.run_fixture(Path(temp) / "limited", failure="cli_failed", max_calls=3)
            self.assertEqual(row["status"], "failed")
            self.assertEqual(client.review_calls, 1)
            self.assertIsNone(row["inconsistency"])

    def test_account_limit_does_not_trigger_useless_retry_or_model_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            row, client = self.run_fixture(Path(temp) / "quota", failure="account_limit_or_quota")
            self.assertEqual(row["status"], "failed")
            self.assertEqual(client.review_calls, 1)


if __name__ == "__main__":
    unittest.main()
