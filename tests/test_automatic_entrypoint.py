"""Exercise PDF/URL-only routing with mocked discovery and fake model outputs.

Source payloads are real toy snapshots from load_repository. Discovery selection
is mocked: these tests do not verify GitHub ownership, resolve a remote ref, call
a model, or make a network request.
"""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scan
import benchmark
import extraction_v3
import extraction_v4
import test_extraction_v4 as toy


class DynamicFakeClient:
    def __init__(self, extraction, review, out_of_scope=False):
        self.extraction = extraction
        self.review = review
        self.out_of_scope = out_of_scope
        self.calls = []
        self.max_calls = 4

    def generate(self, system, content, schema):
        self.calls.append(copy.deepcopy({"system": system, "content": content, "schema": schema}))
        version = schema["properties"]["schema_version"]["enum"][0]
        is_review = "proposal" in content
        if version == 4:
            output = copy.deepcopy(self.review if is_review else self.extraction)
            # Binding comes from what the entrypoint actually supplied, not a
            # guessed hash or a previously curated paper identifier.
            output["input_binding"] = content["input_binding"]
            return output
        if version != 3:
            raise AssertionError("Unexpected inference schema or repair call")
        applicability = "out_of_scope" if self.out_of_scope else "in_scope"
        if is_review:
            return {"schema_version": 3, "applicability": applicability, "applicability_supported": True,
                    "scope_review_complete": True, "flow_reviews": [], "limitations": ["Offline fixture review"]}
        segment = content["segments"][0]
        return {
            "schema_version": 3, "title": "Paper-only fixture", "applicability": applicability,
            "applicability_reason": "Synthetic applicability screening from the supplied text.",
            "applicability_citation": {"segment_id": segment["id"], "quote": segment["text"][:100]},
            "scope_summary": "Only the supplied document; no source-level absence conclusion",
            "flows": [], "unresolved_questions": [], "limitations": ["Offline fixture, not actual model inference"],
        }

    def ledger(self):
        return {"provider": "offline-fixture", "calls": len(self.calls), "charged_or_reserved_usd": 0}


class AutomaticEntrypointTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="automatic paper entrypoint ")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        paper, repository, _, extraction, review = toy.ExtractionV4Tests().fixtures()
        self.paper = copy.deepcopy(paper)
        self.source = "https://example.org/paper.pdf"
        self.paper["source"] = self.source
        self.paper["media_type"] = "application/pdf"
        self.repository = repository
        self.client = DynamicFakeClient(extraction, review)
        self.selected = {
            "status": "selected", "repository": "https://github.com/toy/constructor",
            # This unit test consumes a real content-manifest toy snapshot. It
            # does not claim this placeholder URL was resolved to that snapshot.
            "revision": repository["revision"],
            "evidence": [{"source": "toy-paper", "reason": "Mock selection of the paper's own code."}],
            "candidates": [{"repository": "https://github.com/toy/constructor"}],
            "reason": "Mocked resolver result; remote identity is outside this integration test.",
        }
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.real_network = stack.enter_context(patch("providers.urllib.request.urlopen", side_effect=AssertionError("Live network forbidden")))
        self.real_codex = stack.enter_context(patch("codex_provider.CodexClient.generate", side_effect=AssertionError("Real model invocation forbidden")))

    def discovery(self, row):
        # The public result must retain the structured discovery outcome, not
        # hide source absence behind an ordinary successful source-audit label.
        value = row.get("source_discovery", row.get("repository_discovery"))
        self.assertIsInstance(value, dict, "Result lacks its source-discovery record")
        return value

    def run_main(self, arguments):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return scan.main(list(map(str, arguments)))

    def test_url_alone_selects_source_aware_audit_without_curated_cases_or_labels(self):
        output = self.directory / "automatic source run"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selected)) as discover, \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)) as load, \
                patch.object(scan, "get_client", return_value=self.client):
            code = self.run_main([self.source, "--output", output])
        self.assertEqual(code, 0)
        row = json.loads((output / "result.json").read_text())
        discover.assert_called_once()
        load.assert_called_once()
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["schema_version"], 4)
        self.assertEqual(row["input_mode"], "paper_and_source")
        self.assertEqual(row["verdict"], "inconsistent")
        self.assertEqual(row["requested_workflow"], "automatic_from_paper")
        self.assertEqual(self.discovery(row)["status"], "selected")
        self.assertEqual(row["source_audit"]["status"], "loaded")
        self.assertEqual(row["repository"]["manifest_sha256"], self.repository["manifest_sha256"])
        self.assertEqual(len(self.client.calls), 2)
        self.assertTrue((output / "repository.json").is_file())
        self.assertTrue((output / "combined_input.json").is_file())
        for call in self.client.calls:
            content = call["content"]
            self.assertEqual(content["source_type"], "paper+source")
            self.assertIn("input_binding", content)
            self.assertTrue(any(part["id"].startswith("repo:") for part in content["segments"]))
            for metadata in ("expected", "matches_gold", "gold", "cohort", "curated_cases"):
                self.assertNotIn(metadata, content)
        self.real_network.assert_not_called()
        self.real_codex.assert_not_called()

    def test_missing_ambiguous_or_unavailable_source_does_not_become_a_negative(self):
        for status in ("not_found", "ambiguous", "unavailable"):
            with self.subTest(status=status):
                discovery = {"status": status, "repository": None, "revision": None,
                             "evidence": [], "candidates": [], "reason": "Source selection was not established."}
                client = DynamicFakeClient(self.client.extraction, self.client.review)
                output = self.directory / status
                with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                        patch.object(scan, "discover_repository", return_value=discovery), \
                        patch("source_bundle.load_repository") as load:
                    row = scan.scan_source(self.source, output, client=client)
                load.assert_not_called()
                self.assertEqual(row["status"], "completed")
                self.assertEqual(row["verdict"], "insufficient_evidence")
                self.assertIs(row["has_confirmed_inconsistency"], False)
                self.assertEqual(row["input_mode"], "document_only")
                self.assertEqual(self.discovery(row)["status"], status)
                self.assertEqual(row["source_audit"]["status"], "unavailable")
                limitations = " ".join(row.get("notes", [])).lower()
                self.assertIn("source", limitations)
                self.assertIn("paper", limitations)
                self.assertFalse((output / "repository.json").exists())
                self.assertEqual(len(client.calls), 2)
                self.assertTrue(all("repository" not in call["content"] for call in client.calls))

    def test_selected_but_unreadable_source_has_an_explicit_document_only_fallback(self):
        output = self.directory / "failed source download"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selected)), \
                patch("source_bundle.load_repository", side_effect=ValueError("Pinned source archive unavailable")):
            row = scan.scan_source(self.source, output, client=self.client)
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "insufficient_evidence")
        self.assertEqual(row["input_mode"], "document_only")
        discovery = self.discovery(row)
        self.assertEqual(discovery["status"], "selected")
        self.assertEqual(row["source_audit"]["status"], "unavailable")
        self.assertIn("Pinned source archive unavailable", row["source_audit"]["reason"])
        failed_source_stages = [stage for stage in row["stages"] if stage["stage"] == "repository_ingestion"]
        self.assertTrue(any(stage["status"] == "failed" for stage in failed_source_stages))
        self.assertTrue(any("source verification did not complete" in note for note in row.get("notes", [])))
        self.assertFalse((output / "repository.json").exists())
        self.assertTrue(all("repository" not in call["content"] for call in self.client.calls))

    def test_prepare_only_can_freeze_discovered_source_without_selecting_any_model(self):
        output = self.directory / "prepared automatically"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selected)) as discover, \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)) as load, \
                patch.object(scan, "get_client", side_effect=AssertionError("Preparation must not select a model")) as engine:
            code = self.run_main([self.source, "--output", output, "--prepare-only"])
        self.assertEqual(code, 0)
        engine.assert_not_called()
        discover.assert_called_once()
        load.assert_called_once()
        row = json.loads((output / "result.json").read_text())
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["verdict"], "not_run")
        self.assertEqual(self.discovery(row)["status"], "selected")
        self.assertTrue((output / "prepared.json").is_file())
        self.assertTrue((output / "repository.json").is_file())
        self.assertTrue((output / "combined_input.json").is_file())
        self.assertFalse((output / "extraction.json").exists())
        self.assertFalse((output / "review.json").exists())
        combined = json.loads((output / "combined_input.json").read_text())
        request = json.loads((output / "request.json").read_text())
        measured = len(json.dumps(extraction_v4.model_content(combined), ensure_ascii=False, sort_keys=True))
        self.assertEqual(request["model_data_characters"], measured)
        self.real_codex.assert_not_called()

    def test_paper_only_explicitly_disables_discovery(self):
        output = self.directory / "paper only"
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", side_effect=AssertionError("Paper-only must not discover source")) as discover, \
                patch("source_bundle.load_repository") as load, \
                patch.object(scan, "get_client", return_value=self.client):
            code = self.run_main([self.source, "--output", output, "--paper-only"])
        self.assertEqual(code, 0)
        discover.assert_not_called()
        load.assert_not_called()
        row = json.loads((output / "result.json").read_text())
        self.assertEqual(row["input_mode"], "document_only")
        self.assertEqual(row["verdict"], "insufficient_evidence")

    def test_paper_only_cannot_be_combined_with_an_explicit_repository(self):
        for flags in (["--repo", "https://github.com/toy/constructor"], ["--repo-revision", "a" * 40]):
            with self.subTest(flags=flags):
                with patch.object(scan, "load_document") as ingest, \
                        patch.object(scan, "get_client") as engine:
                    with self.assertRaises(SystemExit) as raised:
                        self.run_main([self.source, "--output", self.directory / "invalid flags", "--paper-only", *flags])
                self.assertEqual(raised.exception.code, 2)
                ingest.assert_not_called()
                engine.assert_not_called()

    def test_fixed_v2_and_v3_replays_do_not_discover_new_source_or_select_a_model(self):
        for version in (2, 3):
            with self.subTest(version=version):
                extraction = {
                    "title": "Historical fixture", "applicability": "in_scope", "applicability_reason": "Stored domain assessment",
                    "applicability_citation": {"segment_id": "p1", "quote": self.paper["segments"][0]["text"][:80]},
                    "scope_summary": "Historical paper-only input", "flows": [], "limitations": [],
                }
                review = {"applicability": "in_scope", "applicability_supported": True, "flow_reviews": [], "limitations": []}
                if version == 3:
                    extraction.update(schema_version=3, unresolved_questions=[])
                    review.update(schema_version=3, scope_review_complete=False)
                with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                        patch.object(scan, "discover_repository", side_effect=AssertionError("Replay must not discover source")) as discover, \
                        patch("source_bundle.load_repository") as load:
                    row = scan.scan_source(self.source, self.directory / f"replay v{version}", extraction=extraction, review=review)
                self.assertEqual(row["status"], "completed")
                self.assertEqual(row["input_mode"], "document_only")
                self.assertEqual(row["verdict"], "insufficient_evidence")
                discover.assert_not_called()
                load.assert_not_called()

    def test_fixed_v4_without_repository_is_rejected_without_new_discovery(self):
        with patch.object(scan, "discover_repository", side_effect=AssertionError("Do not guess replay source")) as discover, \
                patch("source_bundle.load_repository") as load:
            row = scan.scan_source(self.source, self.directory / "missing replay source", extraction=self.client.extraction, review=self.client.review)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["verdict"], "technical_failure")
        self.assertIn("replay requires", row["error"])
        discover.assert_not_called()
        load.assert_not_called()

    def test_explicit_repository_bypasses_discovery(self):
        with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                patch.object(scan, "discover_repository", side_effect=AssertionError("Explicit source must take precedence")) as discover, \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)) as load:
            row = scan.scan_source(self.source, self.directory / "explicit source", client=self.client,
                                   repository=self.selected["repository"], repo_revision=self.selected["revision"])
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["schema_version"], 4)
        self.assertEqual(row["verdict"], "inconsistent")
        discover.assert_not_called()
        load.assert_called_once()

    def test_source_absence_does_not_prevent_a_supported_out_of_domain_result(self):
        paper = copy.deepcopy(self.paper)
        text = "This paper derives adaptive moment optimization for differentiable objectives."
        paper.update(text=text, sha256=hashlib.sha256(text.encode()).hexdigest(), segments=[{"id": "p1", "text": text}])
        discovery = {"status": "not_found", "repository": None, "revision": None,
                     "evidence": [], "candidates": [], "reason": "No code source selected."}
        client = DynamicFakeClient(self.client.extraction, self.client.review, out_of_scope=True)
        with patch.object(scan, "load_document", return_value=paper), \
                patch.object(scan, "discover_repository", return_value=discovery), \
                patch("source_bundle.load_repository") as load:
            row = scan.scan_source(self.source, self.directory / "unrelated paper", client=client)
        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["verdict"], "not_applicable")
        self.assertEqual(self.discovery(row)["status"], "not_found")
        load.assert_not_called()

    def test_landing_page_and_pdf_uri_contexts_are_discovery_metadata_not_model_body(self):
        paper = copy.deepcopy(self.paper)
        markers = ("LANDING_CONTEXT_METADATA_ONLY", "PDF_URI_CONTEXT_METADATA_ONLY", "LINKED_PAGE_METADATA_ONLY")
        paper["link_contexts"] = [
            {"source": "landing_page", "url": "https://github.com/toy/constructor", "text": markers[0], "anchor_text": "Code"},
            {"source": "pdf_annotation", "url": "https://github.com/toy/constructor", "segment_id": "p1", "text": markers[1]},
        ]
        paper["discovery_documents"] = [{"source": "https://example.org/project", "text": markers[2]}]
        with patch.object(scan, "load_document", return_value=paper), \
                patch.object(scan, "discover_repository", return_value=copy.deepcopy(self.selected)) as discover, \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)):
            row = scan.scan_source(self.source, self.directory / "metadata isolation", client=self.client)
        self.assertEqual(row["verdict"], "inconsistent")
        supplied_for_discovery = discover.call_args.args[0]
        self.assertEqual(supplied_for_discovery["link_contexts"], paper["link_contexts"])
        for call in self.client.calls:
            content = json.dumps(call["content"])
            for marker in markers:
                self.assertNotIn(marker, content)
            model_paper = [part["text"] for part in call["content"]["segments"] if part["id"].startswith("paper:")]
            self.assertEqual(model_paper, [part["text"] for part in self.paper["segments"]])

    def test_serialized_source_inventory_over_budget_stops_before_any_model_call(self):
        # Tiny valid source bodies with long filenames make inventory provenance
        # dominate the payload. All hashes, line IDs and coverage come from the
        # actual source reader; no manifest or binding is fabricated.
        files = [toy.code_segment(f"module_{index:02d}_{'x' * 80}.py", f"value = {index}\n") for index in range(24)]
        repository = toy.source_bundle(files)
        self.assertTrue(repository["coverage"]["complete"])
        combined = extraction_v4.combine_inputs(self.paper, repository)
        payload = extraction_v4.model_content(combined)
        body_size = len(combined["text"])
        inventory_size = len(json.dumps(payload["repository"]["inventory"], ensure_ascii=False, sort_keys=True))
        payload_size = len(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        limit = body_size + 100
        self.assertLess(body_size, limit)
        self.assertGreater(inventory_size, body_size)
        self.assertGreater(payload_size, limit)
        selected = {**copy.deepcopy(self.selected), "revision": repository["revision"]}
        for prepare_only in (True, False):
            with self.subTest(prepare_only=prepare_only):
                output = self.directory / f"inventory over budget {prepare_only}"
                with patch.object(scan, "load_document", return_value=copy.deepcopy(self.paper)), \
                        patch.object(scan, "discover_repository", return_value=copy.deepcopy(selected)), \
                        patch("source_bundle.load_repository", return_value=copy.deepcopy(repository)):
                    row = scan.scan_source(self.source, output, client=self.client, prepare_only=prepare_only, max_input_chars=limit)
                self.assertEqual(row["status"], "failed")
                self.assertEqual(row["verdict"], "technical_failure")
                self.assertIn("model data payload exceeds", row["error"])
                self.assertIn("not silently truncated", row["error"])
                self.assertEqual(row["stages"][-1]["stage"], "model_input_preparation")
                self.assertEqual(row["source_audit"]["status"], "loaded")
                self.assertEqual(self.client.calls, [])
                self.assertFalse((output / "extraction.json").exists())
                self.assertFalse((output / "review.json").exists())
                retained = json.loads((output / "combined_input.json").read_text())
                self.assertEqual(retained["text"], combined["text"])
                self.assertEqual(len(json.dumps(extraction_v4.model_content(retained), ensure_ascii=False, sort_keys=True)), payload_size)
        self.real_network.assert_not_called()
        self.real_codex.assert_not_called()

    def test_benchmark_keeps_effective_prompt_and_posthoc_labels_separate_for_both_auto_routes(self):
        second_source = "https://example.org/paper-without-source.pdf"
        markers = ["REFERENCE_TITLE_ONLY", "REFERENCE_COHORT_ONLY", "REFERENCE_BASIS_ONLY", "REFERENCE_NOTE_ONLY", "UNTRUSTED_MANIFEST_REPO_HINT"]
        specs = [{
            "id": ident, "source": source, "title": markers[0], "cohort": markers[1],
            "expected": expected, "expected_basis": markers[2], "comparison_note": markers[3],
            "repository": markers[4], "repo_revision": "must-not-override-discovery",
        } for ident, source, expected in (
            ("with_code", self.source, "consistent_within_scope"),
            ("without_code", second_source, "inconsistent"),
        )]
        manifest = self.directory / "manifest.json"
        manifest.write_text(json.dumps({"papers": specs}), encoding="utf-8")
        missing = {"status": "not_found", "repository": None, "revision": None,
                   "evidence": [], "candidates": [], "reason": "No associated source in this fixture."}

        def load_paper(source):
            return {**copy.deepcopy(self.paper), "source": source}

        def choose_source(document, source):
            self.assertEqual(document["source"], source)
            return copy.deepcopy(self.selected if source == self.source else missing)

        output = self.directory / "mixed automatic benchmark"
        with patch.object(benchmark, "get_client", return_value=self.client), \
                patch.object(scan, "load_document", side_effect=load_paper), \
                patch.object(scan, "discover_repository", side_effect=choose_source), \
                patch("source_bundle.load_repository", return_value=copy.deepcopy(self.repository)) as load:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = benchmark.main(["--mode", "scan", "--manifest", str(manifest), "--output", str(output)])
        self.assertEqual(code, 0)
        load.assert_called_once()
        self.assertEqual(len(self.client.calls), 4)
        config = json.loads((output / "run_config.json").read_text())
        self.assertEqual(config["input_mode"], "automatic_from_paper")
        self.assertIsNone(config["prompt_sha256"])
        self.assertEqual(config["max_input_chars"], 600000)
        self.assertEqual(config["max_code_chars"], 320000)
        report = json.loads((output / "report.json").read_text())
        by_id = {row["id"]: row for row in report["papers"]}
        self.assertEqual(by_id["with_code"]["verdict"], "inconsistent")
        self.assertEqual(by_id["without_code"]["verdict"], "insufficient_evidence")
        self.assertEqual(by_id["with_code"]["prompt_sha256"], extraction_v4.prompt_hash())
        self.assertEqual(by_id["without_code"]["prompt_sha256"], extraction_v3.prompt_hash())
        self.assertEqual(by_id["with_code"]["input_mode"], "paper_and_source")
        self.assertEqual(by_id["without_code"]["input_mode"], "document_only")
        for ident in by_id:
            self.assertIs(by_id[ident]["matches_gold"], False)
            standalone = json.loads((output / ident / "result.json").read_text())
            for key in ("expected", "matches_gold", "expected_basis", "cohort", "comparison_note"):
                self.assertNotIn(key, standalone)
        for call in self.client.calls:
            content = json.dumps(call["content"])
            for marker in markers:
                self.assertNotIn(marker, content)


if __name__ == "__main__":
    unittest.main()
