"""Offline recovery preserves frozen evidence and performs one review only."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import extraction_v4 as v4
import extraction_v6 as v6
from review_recovery import resume_review
import test_extraction_v6 as toy


class Client:
    max_calls = 1
    def __init__(self, answer, failure=False, during_call=None):
        self.calls, self.answer, self.failure, self.during_call = [], answer, failure, during_call
        self.prompts = []

    def generate(self, prompt, content, schema):
        self.prompts.append((prompt, copy.deepcopy(content), copy.deepcopy(schema)))
        self.calls.append({"status": "cli_failed" if self.failure else "completed", "usage": {}})
        if self.during_call:
            self.during_call()
        if self.failure:
            raise ValueError("Codex CLI failed (cli_failed); no retry or fallback attempted")
        return copy.deepcopy(self.answer)

    def ledger(self):
        return {"provider": "test-only", "max_calls": self.max_calls, "calls": copy.deepcopy(self.calls)}


class ReviewRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.parent = self.root / "failed-automatic-attempt"
        self.parent.mkdir()
        self.paper, self.repo, self.document, self.extraction, self.review = toy.ExtractionV6Tests().fixtures()
        self.write("prepared.json", self.paper)
        self.write("repository.json", self.repo)
        self.write("source_discovery.json", {"status": "selected", "repository": self.repo["source"], "revision": self.repo["revision"]})
        self.write("combined_input.json", self.document)
        self.write("request.json", {"input_sha256": self.document["sha256"], "prompt_sha256": "original-combined-prompt-hash"})
        self.write("extraction.json", self.extraction)
        result = {"id": "toy", "title": "Toy audit", "source": self.paper["source"],
                  "status": "failed", "verdict": "technical_failure", "requested_workflow": "automatic_from_paper",
                  "source_audit": {"status": "loaded", "revision": self.repo["revision"]},
                  "stages": [{"stage": "semantic_review", "status": "failed"}], "effective_extraction_file": "extraction.json"}
        self.write("result.json", result)
        self.ledger = {"calls": [{"status": "completed", "usage": {}}, {"status": "cli_failed", "usage": {}}]}
        self.write("inference.json", self.ledger)
        self.write("inference.semantic_review.json", self.ledger)
        network = patch("source_bundle.load_repository", side_effect=AssertionError("Recovery cannot acquire source"))
        self.network = network.start()
        self.addCleanup(network.stop)

    def write(self, filename, value):
        (self.parent / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2))

    def hashes(self):
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.parent.iterdir()}

    def run_recovery(self, client=None, name="recovery"):
        client = client or Client(self.review)
        row = resume_review(self.parent, self.root / name, client)
        return row, client

    def test_legacy_parent_uses_one_amended_review_and_keeps_parent_immutable(self):
        before = self.hashes()
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "inconsistent")
        self.assertEqual(row["recovery"]["mode"], "amended_current_review_legacy_parent")
        self.assertEqual(len(client.calls), 1)
        self.assertEqual(client.prompts[0][1]["proposal"], self.extraction)
        self.assertEqual(self.hashes(), before)
        self.assertFalse((self.parent / "review.json").exists())
        self.network.assert_not_called()
        for filename in ("recovery.json", "review.request.json", "review.contract.json", "review.json",
                         "result.json", "report.json", "report.html", "report.md", "inference.json", "parent_integrity.json"):
            self.assertTrue((self.root / "recovery" / filename).is_file(), filename)

    def add_saved_contract(self, prompt="Saved exact review prompt"):
        payload = {**v6.model_content(self.document), "proposal": self.extraction}
        contract = {"prompt": prompt, "schema": v6.REVIEW_SCHEMA,
                    "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "schema_sha256": v4._hash_json(v6.REVIEW_SCHEMA),
                    "review_input_sha256": v4._hash_json(payload),
                    "input_binding": self.document["sha256"], "engine_version": 6}
        self.write("review.request.json", payload)
        self.write("review.contract.json", contract)
        return contract

    def test_saved_contract_keeps_exact_prompt_not_current_prompt(self):
        self.add_saved_contract()
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["recovery"]["mode"], "saved_exact_review_contract")
        self.assertEqual(client.prompts[0][0], "Saved exact review prompt")

    def test_changed_saved_prompt_hash_or_review_input_is_rejected_before_call(self):
        contract = self.add_saved_contract()
        contract["prompt"] = "Tampered prompt"
        self.write("review.contract.json", contract)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertIn("saved review contract", row["error"])
        self.assertEqual(client.calls, [])

    def test_saved_review_payload_cannot_inject_different_proposal(self):
        self.add_saved_contract()
        payload = json.loads((self.parent / "review.request.json").read_text())
        payload["proposal"]["flows"][0]["permission"] = "allow"
        self.write("review.request.json", payload)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertIn("saved review contract", row["error"])
        self.assertEqual(client.calls, [])

    def test_saved_untrusted_declared_contract_is_preserved_in_same_binding(self):
        from declared_contract import validate_contract
        from test_default_v6 import paper_contract
        envelope = validate_contract(paper_contract(self.paper["sha256"]), self.paper)
        self.document = v6.attach_declared_contract(self.document, envelope)
        self.extraction["input_binding"] = self.review["input_binding"] = self.document["sha256"]
        self.write("declared_contract.json", envelope)
        self.write("combined_input.json", self.document)
        self.write("extraction.json", self.extraction)
        self.write("request.json", {"input_sha256": self.document["sha256"], "prompt_sha256": "old"})
        self.add_saved_contract()
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "completed")
        self.assertEqual(client.prompts[0][1]["input_binding"], self.document["sha256"])
        self.assertEqual(json.loads((self.root / "recovery/declared_contract.json").read_text()), envelope)

    def test_changed_parent_proposal_binding_is_rejected_without_call(self):
        self.extraction["input_binding"] = "other"
        self.write("extraction.json", self.extraction)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertIn("binding", row["error"])
        self.assertEqual(client.calls, [])

    def test_changed_frozen_source_is_rejected_without_call(self):
        self.repo["segments"][0]["text"] += "\n# changed"
        self.write("repository.json", self.repo)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertEqual(client.calls, [])

    def test_manual_repository_parent_is_not_accepted_as_automatic(self):
        result = json.loads((self.parent / "result.json").read_text())
        result["requested_workflow"] = "explicit_paper_and_source"
        self.write("result.json", result)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertIn("automatic", row["error"])
        self.assertEqual(client.calls, [])

    def test_completed_or_wrong_stage_parent_cannot_be_rereviewed(self):
        result = json.loads((self.parent / "result.json").read_text())
        result["stages"] = [{"stage": "extraction", "status": "failed"}]
        self.write("result.json", result)
        row, client = self.run_recovery()
        self.assertIn("unfinished semantic review", row["error"])
        self.assertEqual(client.calls, [])

    def test_existing_parent_review_is_not_replaced(self):
        self.write("review.json", self.review)
        row, client = self.run_recovery()
        self.assertEqual(row["status"], "failed")
        self.assertIn("already contains a review", row["error"])
        self.assertEqual(client.calls, [])

    def test_failed_review_is_preserved_without_retry_or_new_verdict(self):
        before = self.hashes()
        row, client = self.run_recovery(Client(self.review, failure=True))
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIsNone(row["inconsistency"])
        self.assertEqual(len(client.calls), 1)
        self.assertEqual(self.hashes(), before)
        self.assertTrue((self.root / "recovery/inference.semantic_review.json").is_file())
        self.assertFalse((self.root / "recovery/review.json").exists())

    def test_parent_change_while_model_runs_prevents_decision(self):
        client = Client(self.review, during_call=lambda: self.write("prepared.json", {**self.paper, "sha256": "changed"}))
        row, client = self.run_recovery(client)
        self.assertEqual(row["status"], "failed")
        self.assertIn("parent artifacts changed", row["error"])
        self.assertFalse((self.root / "recovery/review.json").exists())
        integrity = json.loads((self.root / "recovery/parent_integrity.json").read_text())
        self.assertFalse(integrity["unchanged"])

    def test_input_and_budget_limits_stop_before_model(self):
        client = Client(self.review)
        row = resume_review(self.parent, self.root / "small", client, max_input_chars=10)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(client.calls, [])
        client.max_calls = 0
        row, _ = self.run_recovery(client, name="budget")
        self.assertEqual(row["status"], "failed")
        self.assertEqual(client.calls, [])

    def test_output_cannot_be_parent_or_replace_existing_attempt(self):
        with self.assertRaisesRegex(ValueError, "separate"):
            resume_review(self.parent, self.parent / "nested", Client(self.review))
        self.run_recovery()
        with self.assertRaises(FileExistsError):
            self.run_recovery()


if __name__ == "__main__":
    unittest.main()
