"""Offline integration checks for the provisional paper-only V6 contract.

Synthetic extraction/review responses exercise routing and deterministic gates;
they are not model accuracy or historical execution evidence.
"""

from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import declared_contract
import extraction_v4 as v4
import extraction_v6 as v6
import scan
from test_default_v6 import paper_contract
import test_extraction_v6 as fixtures


def cited_contract(paper):
    proposal = paper_contract(paper["sha256"])
    proposal["task_input_definition"]["definition"] = {
        "status": "explicit", "text": "The paper states a common knowledge budget.",
        "citations": [{"segment_id": "p1",
                       "quote": "All evaluated attacker channels share the same knowledge budget"}],
    }
    return proposal


class FakeContractClient:
    def __init__(self, paper, extraction, review, *, max_calls=3, prior_calls=0):
        self.paper = paper
        self.extraction = extraction
        self.review = review
        self.max_calls = max_calls
        self.calls = [{"prior_completed_call": True} for _ in range(prior_calls)]

    def generate(self, prompt, content, schema):
        self.calls.append(copy.deepcopy(content))
        if "input_binding" not in content:
            return cited_contract(self.paper)
        result = copy.deepcopy(self.review if "proposal" in content else self.extraction)
        result["input_binding"] = content["input_binding"]
        return result

    def ledger(self):
        return {"provider": "offline-integration-fixture", "calls": len(self.calls)}


class V6ContractBindingTests(unittest.TestCase):
    def setUp(self):
        self.paper, self.repository, self.document, self.extraction, self.review = \
            fixtures.ExtractionV6Tests().fixtures()
        self.source = "https://example.org/synthetic-contract-paper.pdf"
        self.paper["source"] = self.source
        self.document = v6.combine_inputs(self.paper, self.repository)
        self.envelope = declared_contract.validate_contract(cited_contract(self.paper), self.paper)
        self.selection = {"status": "selected", "repository": "https://github.com/toy/contract-source",
                          "revision": self.repository["revision"], "reason": "Mock paper source selection."}
        temporary = tempfile.TemporaryDirectory(prefix="v6 contract binding ")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        # Fail loudly if these offline tests ever select a real inference path.
        real_api = patch("providers.ModelClient.generate", side_effect=AssertionError("Live model forbidden"))
        real_codex = patch("codex_provider.CodexClient.generate", side_effect=AssertionError("Live model forbidden"))
        self.real_api = real_api.start()
        self.real_codex = real_codex.start()
        self.addCleanup(real_api.stop)
        self.addCleanup(real_codex.stop)

    def test_attachment_binds_untrusted_proposal_and_changes_model_input(self):
        original_hash = self.document["sha256"]
        original_content_hash = self.document["model_content_sha256"]
        document = v6.attach_declared_contract(self.document, self.envelope)
        self.assertNotEqual(document["sha256"], original_hash)
        self.assertNotEqual(document["model_content_sha256"], original_content_hash)
        content = v6.model_content(document)
        attached = content["repository"]["declared_contract_proposal"]
        self.assertEqual(attached, self.envelope)
        self.assertEqual(content["input_binding"], document["sha256"])
        self.assertEqual(attached["trust"], "untrusted_declared_contract_proposal")
        self.assertTrue(attached["semantic_review_required"])
        self.assertTrue(attached["citations_grounded"])
        self.assertFalse(any(part["id"].startswith("contract:") for part in content["segments"]))
        self.assertNotIn("declared_contract_proposal", document["repository"])
        attached["trust"] = "changed returned metadata"
        self.assertEqual(document["model_repository"]["declared_contract_proposal"], self.envelope)
        self.envelope["proposal"]["limitations"].append("changed caller copy")
        self.assertNotEqual(document["model_repository"]["declared_contract_proposal"], self.envelope)
        v6.validate_input_binding(document)

    def test_rehashed_quote_or_locator_tampering_still_fails_v6_validation(self):
        document = v6.attach_declared_contract(self.document, self.envelope)
        for axis in ("citation", "locator", "trust"):
            with self.subTest(axis=axis):
                altered = copy.deepcopy(document)
                envelope = altered["model_repository"]["declared_contract_proposal"]
                if axis == "citation":
                    envelope["proposal"]["task_input_definition"]["definition"]["citations"][0]["quote"] = \
                        "A stronger delivery channel does not change access to request information"
                elif axis == "locator":
                    envelope["locators"]["task_input_definition.definition"][0]["start"] += 1
                else:
                    envelope["semantic_review_required"] = False
                # Rehash the ordinary payload and input binding, as a caller
                # could. Independent paper-only envelope validation must remain.
                altered["model_content_sha256"] = v4._hash_json(v4._unbound_model_content(altered))
                altered["sha256"] = v4._hash_json(v4._binding_material(altered))
                v4.validate_input_binding(altered)
                with self.assertRaisesRegex(ValueError, "declared contract"):
                    v6.validate_input_binding(altered)
                with self.assertRaisesRegex(ValueError, "declared contract"):
                    v6.model_content(altered)

    def test_attachment_rejects_a_modified_saved_envelope_before_binding(self):
        changed = copy.deepcopy(self.envelope)
        changed["locators"]["task_input_definition.definition"][0]["end"] += 1
        original = copy.deepcopy(self.document)
        with self.assertRaisesRegex(ValueError, "declared contract"):
            v6.attach_declared_contract(self.document, changed)
        self.assertEqual(self.document, original)

    def test_saved_automatic_envelope_replays_with_no_fresh_model_calls(self):
        automatic = self.directory / "automatic"
        client = FakeContractClient(self.paper, self.extraction, self.review)
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selection)), \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)):
            row = scan.scan_source(self.source, automatic, client=client, engine_version=6)
        self.assertEqual(row["status"], "completed", row.get("error"))
        self.assertEqual(len(client.calls), 3)
        saved = json.loads((automatic / "declared_contract.json").read_text())
        self.assertEqual(saved, self.envelope)
        source_binding = json.loads((automatic / "combined_input.json").read_text())["sha256"]
        replay = self.directory / "replay"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", side_effect=AssertionError("Replay must not rediscover source")) as discover, \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)), \
                patch.object(scan, "get_client", side_effect=AssertionError("Replay must not choose a model")) as get_client, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = scan.main([
                self.source, "--engine-version", "6", "--output", str(replay),
                "--repo", self.selection["repository"], "--repo-revision", self.selection["revision"],
                "--extraction", str(automatic / "extraction.json"),
                "--review", str(automatic / "review.json"),
                "--declared-contract", str(automatic / "declared_contract.json"),
            ])
        self.assertEqual(code, 0)
        replayed = json.loads((replay / "result.json").read_text())
        self.assertEqual(replayed["status"], "completed", replayed.get("error"))
        self.assertEqual(replayed["verdict"], row["verdict"])
        self.assertEqual(replayed["evidence"], row["evidence"])
        self.assertEqual(json.loads((replay / "combined_input.json").read_text())["sha256"], source_binding)
        self.assertEqual(json.loads((replay / "declared_contract.json").read_text()), saved)
        stage = next(item for item in replayed["stages"] if item["stage"] == "declared_contract")
        self.assertEqual(stage["execution"], "saved_automatic_proposal")
        self.assertFalse((replay / "inference.json").exists())
        self.assertEqual(len(client.calls), 3)
        discover.assert_not_called()
        get_client.assert_not_called()
        self.real_api.assert_not_called()
        self.real_codex.assert_not_called()

    def test_v6_prepare_only_never_selects_or_calls_a_contract_model(self):
        output = self.directory / "prepare only"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selection)), \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)), \
                patch.object(scan, "get_client", side_effect=AssertionError("Preparation must not choose a model")) as get_client, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = scan.main([self.source, "--engine-version", "6", "--prepare-only", "--output", str(output)])
        self.assertEqual(code, 0)
        row = json.loads((output / "result.json").read_text())
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["verdict"], "not_run")
        document = json.loads((output / "combined_input.json").read_text())
        v6.validate_input_binding(document)
        self.assertNotIn("declared_contract_proposal", v6.model_content(document)["repository"])
        self.assertFalse(any(item["stage"] == "declared_contract" for item in row["stages"]))
        for name in ("declared_contract.request.json", "declared_contract.response.json", "declared_contract.json",
                     "extraction.json", "review.json", "inference.json"):
            self.assertFalse((output / name).exists(), name)
        get_client.assert_not_called()
        self.real_api.assert_not_called()
        self.real_codex.assert_not_called()

    def test_two_calls_remaining_fails_before_any_inference(self):
        for maximum, prior in ((2, 0), (3, 1)):
            with self.subTest(maximum=maximum, prior_calls=prior):
                output = self.directory / f"budget {maximum} prior {prior}"
                client = FakeContractClient(self.paper, self.extraction, self.review,
                                            max_calls=maximum, prior_calls=prior)
                before = copy.deepcopy(client.calls)
                with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                        patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selection)), \
                        patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)):
                    row = scan.scan_source(self.source, output, client=client, engine_version=6)
                self.assertEqual(row["status"], "failed")
                self.assertEqual(row["verdict"], "technical_failure")
                self.assertIn("three calls", row["error"])
                self.assertEqual(row["stages"][-1]["stage"], "declared_contract")
                self.assertEqual(client.calls, before)
                self.assertEqual(json.loads((output / "inference.json").read_text())["calls"], prior)
                self.assertTrue((output / "declared_contract.request.json").exists())
                for name in ("declared_contract.response.json", "declared_contract.json", "extraction.json", "review.json"):
                    self.assertFalse((output / name).exists(), name)
        self.real_api.assert_not_called()
        self.real_codex.assert_not_called()


if __name__ == "__main__":
    unittest.main()
