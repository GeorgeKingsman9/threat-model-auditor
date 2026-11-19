"""Ground source-aware decisions in a toy paper and immutable toy code bundle.

No curated paper cases, expected-label files, network, or model calls are used.
The review values are fixtures checking axis plumbing, not model accuracy.
"""

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v4 as v4
from source_bundle import load_repository


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def code_segment(path, text):
    return {
        "id": f"repo:{path}:L1-L{max(1, len(text.splitlines()))}", "path": path, "text": text,
        "sha256": digest(text), "line_start": 1, "line_end": len(text.splitlines()),
    }


def source_bundle(segments, max_chars=240000):
    # Exercise the real reader/validator; do not fabricate Git identity or a
    # partially populated provenance dict. The returned content-manifest snapshot
    # remains version-bound after the temporary input directory is removed.
    with tempfile.TemporaryDirectory(prefix="toy source snapshot ") as temporary:
        root = Path(temporary)
        for part in segments:
            path = root / part["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(part["text"], encoding="utf-8")
        return load_repository(str(root), max_chars=max_chars)


class ExtractionV4Tests(unittest.TestCase):
    def fixtures(self):
        budget = (
            "All evaluated attacker channels share the same knowledge budget. "
            "For direct payload construction, the adversary cannot receive the target request text. "
            "A stronger delivery channel does not change access to request information."
        )
        exception = "Only the diagnostic oracle constructor is expressly allowed to receive the target request text."
        paper = {
            "source": "toy-paper.txt", "sha256": digest(budget + "\n" + exception),
            "media_type": "text/plain", "text": budget + "\n" + exception,
            "segments": [{"id": "p1", "text": budget}, {"id": "p2", "text": exception}],
            "coverage": {"complete": True, "reason": "Entire toy paper supplied."}, "links": [],
        }
        generator = code_segment("generator.py", (
            "def build(case, backend):\n"
            "    record = case[\"user_request\"]\n"
            "    prompt = {\"task\": record}\n"
            "    reply = backend.generate(prompt)\n"
            "    save_artifact(case[\"id\"], reply)\n"
            "    return reply\n"
        ))
        evaluator = code_segment("evaluator.py", (
            "def evaluate(case, channel):\n"
            "    reply = read_artifact(case[\"id\"])\n"
            "    if channel == \"direct\":\n"
            "        return victim.inject(reply)\n"
        ))
        repository = source_bundle([generator, evaluator])
        merged = v4.combine_inputs(paper, repository)
        cite = lambda segment_id, quote: {"segment_id": segment_id, "quote": quote}
        declaration = cite("paper:p1", "the adversary cannot receive the target request text")
        common = cite("paper:p1", "All evaluated attacker channels share the same knowledge budget")
        request = cite(generator["id"], "reply = backend.generate(prompt)")
        delivery = cite(evaluator["id"], 'if channel == "direct":\n        return victim.inject(reply)')
        path = [
            {"kind": "source", "input_symbol": "case.user_request", "output_symbol": "build.record",
             "citation": cite(generator["id"], 'record = case["user_request"]'), "explanation": "Read this case's request."},
            {"kind": "transform", "input_symbol": "build.record", "output_symbol": "build.prompt",
             "citation": cite(generator["id"], 'prompt = {"task": record}'), "explanation": "Bind the request as construction input."},
            {"kind": "request", "input_symbol": "build.prompt", "output_symbol": "build.reply",
             "citation": copy.deepcopy(request), "explanation": "Send that prompt to the construction backend."},
            {"kind": "artifact_write", "input_symbol": "build.reply", "output_symbol": "artifact(case.id)",
             "citation": cite(generator["id"], 'save_artifact(case["id"], reply)'), "explanation": "Save by the same case ID."},
            {"kind": "artifact_read", "input_symbol": "artifact(case.id)", "output_symbol": "evaluate.reply",
             "citation": cite(evaluator["id"], 'reply = read_artifact(case["id"])'), "explanation": "Load the matching case's artifact."},
            {"kind": "delivery", "input_symbol": "evaluate.reply", "output_symbol": "victim.direct.input",
             "citation": copy.deepcopy(delivery), "explanation": "Use that artifact in the named direct channel."},
        ]
        extraction = {
            "schema_version": 4, "input_binding": merged["sha256"], "title": "Toy construction audit",
            "applicability": "in_scope", "applicability_reason": "A synthetic attacker-channel study.",
            "applicability_citation": copy.deepcopy(common),
            "scope_summary": "Only the direct source branch at the supplied revision",
            "unresolved_questions": [], "limitations": ["Static toy code only; no historical execution claim."],
            "flows": [{
                "claim": "The direct constructor uses target request text excluded by its shared knowledge budget.",
                "issue_type": "information_boundary", "information_level": "exact_query",
                "edge": {"role": "attacker-side constructor", "phase": "direct payload construction",
                         "source": "target evaluation case", "representation": "exact request text",
                         "operation": "receive as construction input", "query_form": "full_query"},
                "permission": "deny", "observation": "present",
                "declaration": declaration, "implementation": request,
                "policy_application": {"policy_kind": "attacker_knowledge_constraint", "status": "applicable",
                                       "citation": copy.deepcopy(common), "reason": "The paper states a shared budget for the named channel."},
                "delivery": {"status": "confirmed", "evidence_kind": "static_bound_path",
                             "task_relation": "same_evaluated_instance", "citation": delivery,
                             "reason": "The connected request, storage and evaluation path uses the same case ID."},
                "refutation": {"basis": "none", "citation": None, "reason": "No direct-channel knowledge grant is established."},
                "explanation": "A bounded source-level comparison, without executing repository code.",
                "scope_resolution": {"basis": "common_contract", "common_rule": common,
                                     "specific_rule": None, "override_dimension": "none",
                                     "reason": "The direct channel is within the explicit common knowledge contract."},
                "code_path": path, "experiment_arm": "direct",
            }],
        }
        review = {
            "schema_version": 4, "input_binding": merged["sha256"], "applicability": "in_scope",
            "applicability_supported": True, "scope_review_complete": True,
            "limitations": ["Fixture votes exercise validation, not independent semantic proof."],
            "flow_reviews": [{"index": 0, "supported": True, "policy_kind": "attacker_knowledge_constraint",
                              "policy_application": "applicable", "delivery": "confirmed", "refutation": "none",
                              "declaration_supported": True, "implementation_supported": True,
                              "scope_resolution_supported": True, "code_path_supported": True,
                              "reason": "The supplied declarations and each connected source step support the precise toy branch."}],
        }
        return paper, repository, merged, extraction, review

    def decide(self, extraction, review, merged):
        return v4.decide_extraction(extraction, review, merged, "toy")

    def assert_no_positive(self, result):
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_connected_cross_file_path_produces_a_bounded_static_finding(self):
        paper, repository, merged, extraction, review = self.fixtures()
        result = self.decide(extraction, review, merged)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertIs(result["has_confirmed_inconsistency"], True)
        self.assertEqual(result["schema_version"], 4)
        self.assertEqual(result["input_mode"], "paper_and_source")
        self.assertEqual(result["document_sha256"], paper["sha256"])
        self.assertEqual(result["input_binding"], merged["sha256"])
        row = result["evidence"][0]
        self.assertEqual(row["source_group"], "archived")
        self.assertEqual(row["scope"]["artifact_revision"], repository["revision"])
        self.assertEqual(row["scope"]["experiment_arm"], "direct")
        path = row["source_validation"]["code_path_locators"]
        self.assertEqual(len(path), 6)
        self.assertEqual(path[2]["path"], "generator.py")
        self.assertEqual((path[2]["line_start"], path[2]["line_end"]), (4, 4))
        self.assertEqual((path[-1]["line_start"], path[-1]["line_end"]), (3, 4))
        for locator in path:
            self.assertEqual(locator["source_kind"], "code")
            self.assertEqual(locator["repository_revision"], repository["revision"])
            self.assertEqual(locator["repository_manifest_sha256"], repository["manifest_sha256"])
            segment = next(p for p in repository["segments"] if p["path"] == locator["path"])
            self.assertEqual(locator["file_sha256"], segment["sha256"])

    def test_paper_and_source_namespaces_and_binding_are_distinct(self):
        paper, repository, merged, _, _ = self.fixtures()
        self.assertEqual(merged["paper_sha256"], paper["sha256"])
        self.assertEqual({part["source_kind"] for part in merged["segments"]}, {"paper", "code"})
        self.assertTrue(all(part["id"].startswith("paper:") for part in merged["segments"] if part["source_kind"] == "paper"))
        for field in ("revision", "manifest_sha256"):
            altered = copy.deepcopy(repository)
            altered[field] += "changed"
            with self.assertRaises(ValueError):
                v4.combine_inputs(paper, altered)
        changed = copy.deepcopy(repository["segments"])
        changed[0]["text"] += "# a different source version\n"
        different_version = source_bundle(changed)
        self.assertNotEqual(v4.combine_inputs(paper, different_version)["sha256"], merged["sha256"])

    def test_fixed_outputs_cannot_be_reused_after_input_binding_changes(self):
        paper, repository, merged, extraction, review = self.fixtures()
        changed_files = copy.deepcopy(repository["segments"])
        changed_files[0]["text"] += "# a different source version\n"
        changed_repo = source_bundle(changed_files)
        changed = v4.combine_inputs(paper, changed_repo)
        with self.assertRaisesRegex(ValueError, "input binding"):
            self.decide(extraction, review, changed)
        for which in ("extraction", "review"):
            with self.subTest(which=which):
                ext, rev = copy.deepcopy((extraction, review))
                (ext if which == "extraction" else rev)["input_binding"] = "wrong-input-binding"
                with self.assertRaises(ValueError):
                    self.decide(ext, rev, merged)

    def test_declaration_cannot_be_substituted_with_a_code_comment(self):
        paper, repository, _, extraction, review = self.fixtures()
        code = code_segment("comment.py", "# The adversary cannot receive the target request text.\n")
        repository = source_bundle(repository["segments"] + [code])
        merged = v4.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = merged["sha256"]
        extraction["flows"][0]["declaration"] = {"segment_id": code["id"], "quote": "The adversary cannot receive the target request text"}
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        row = result["evidence"][0]
        self.assertFalse(row["source_validation"]["policy_supported"])
        self.assertTrue(row["source_validation"]["delivery_supported"])

    def test_scope_resolution_must_be_grounded_in_the_paper_not_source_code(self):
        _, _, merged, extraction, review = self.fixtures()
        extraction["flows"][0]["scope_resolution"]["common_rule"] = copy.deepcopy(extraction["flows"][0]["implementation"])
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        self.assertTrue(result["evidence"][0]["source_validation"]["delivery_supported"])

    def test_code_receipt_cannot_be_proved_by_a_paper_only_citation(self):
        for destination in ("implementation", "delivery", "path_step"):
            with self.subTest(destination=destination):
                _, _, merged, extraction, review = self.fixtures()
                flow = extraction["flows"][0]
                paper_citation = copy.deepcopy(flow["declaration"])
                if destination == "implementation":
                    flow["implementation"] = paper_citation
                elif destination == "delivery":
                    flow["delivery"]["citation"] = paper_citation
                else:
                    flow["code_path"][2]["citation"] = paper_citation
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                self.assertFalse(result["evidence"][0]["source_validation"]["delivery_supported"])

    def test_each_source_step_needs_an_existing_exact_quote(self):
        _, _, merged, extraction, review = self.fixtures()
        extraction["flows"][0]["code_path"][3]["citation"]["quote"] = "write_other_artifact(the_future_query)"
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        self.assertTrue(any("source_path_citation" in error for error in result["evidence"][0]["source_validation"]["validation_errors"]))

    def test_disconnected_symbols_and_delivery_before_request_are_rejected(self):
        for damage in ("disconnect", "wrong_order"):
            with self.subTest(damage=damage):
                _, _, merged, extraction, review = self.fixtures()
                path = extraction["flows"][0]["code_path"]
                if damage == "disconnect":
                    path[4]["input_symbol"] = "artifact(other.case.id)"
                else:
                    path[2]["kind"], path[5]["kind"] = "delivery", "request"
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                self.assertFalse(result["evidence"][0]["source_validation"]["delivery_supported"])

    def test_dataset_presence_without_request_and_delivery_cannot_confirm_receipt(self):
        for kinds in (("source", "transform"), ("source", "request"), ("source", "delivery")):
            with self.subTest(kinds=kinds):
                _, _, merged, extraction, review = self.fixtures()
                path = extraction["flows"][0]["code_path"][:2]
                path[0]["kind"], path[1]["kind"] = kinds
                extraction["flows"][0]["code_path"] = path
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                self.assertTrue(any("request_and_delivery" in error for error in result["evidence"][0]["source_validation"]["validation_errors"]))

    def test_review_of_a_path_is_required_in_addition_to_real_code_quotes(self):
        _, _, merged, extraction, review = self.fixtures()
        review["flow_reviews"][0]["code_path_supported"] = False
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        self.assertFalse(result["evidence"][0]["source_validation"]["delivery_supported"])

    def test_policy_dispute_preserves_independently_supported_code_delivery(self):
        for axis in ("declaration_supported", "scope_resolution_supported"):
            with self.subTest(axis=axis):
                _, _, merged, extraction, review = self.fixtures()
                vote = review["flow_reviews"][0]
                vote.update(supported=False)
                vote[axis] = False
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                row = result["evidence"][0]
                self.assertEqual(row["assessment"]["policy_application"]["status"], "uncertain")
                self.assertEqual(row["assessment"]["delivery"]["status"], "confirmed")
                self.assertEqual({record["status"] for record in row["matching_observations"]}, {"present"})
                self.assertEqual(row["matching_rules"], [])
                self.assertFalse(row["source_validation"]["policy_supported"])
                self.assertTrue(row["source_validation"]["delivery_supported"])

    def test_bad_implementation_axis_does_not_erase_the_applicable_policy(self):
        _, _, merged, extraction, review = self.fixtures()
        review["flow_reviews"][0].update(supported=False, implementation_supported=False)
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        row = result["evidence"][0]
        self.assertEqual({rule["permission"] for rule in row["matching_rules"]}, {"deny"})
        self.assertNotIn("present", {observation["status"] for observation in row["matching_observations"]})
        self.assertTrue(row["source_validation"]["policy_supported"])
        self.assertFalse(row["source_validation"]["delivery_supported"])

    def test_common_contract_cannot_override_an_explicit_knowledge_or_diagnostic_exception(self):
        for dimension in ("knowledge", "diagnostic", "unknown"):
            with self.subTest(dimension=dimension):
                _, _, merged, extraction, review = self.fixtures()
                flow = extraction["flows"][0]
                flow["scope_resolution"].update(
                    specific_rule={"segment_id": "paper:p2", "quote": "Only the diagnostic oracle constructor is expressly allowed to receive the target request text"},
                    override_dimension=dimension,
                )
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                self.assertTrue(result["evidence"][0]["source_validation"]["delivery_supported"])
                self.assertIn("common_contract_conflicts_with_specific_scope", result["evidence"][0]["source_validation"]["validation_errors"])

    def test_delivery_only_change_does_not_automatically_grant_more_knowledge(self):
        _, _, merged, extraction, review = self.fixtures()
        extraction["flows"][0]["scope_resolution"].update(
            specific_rule={"segment_id": "paper:p1", "quote": "A stronger delivery channel does not change access to request information"},
            override_dimension="delivery",
        )
        self.assertEqual(self.decide(extraction, review, merged)["verdict"], "inconsistent")

    def test_unknown_experiment_arm_cannot_be_treated_as_a_bound_branch(self):
        for arm in ("", "unknown", "unspecified"):
            with self.subTest(arm=arm):
                _, _, merged, extraction, review = self.fixtures()
                extraction["flows"][0]["experiment_arm"] = arm
                self.assert_no_positive(self.decide(extraction, review, merged))

    def test_specific_rule_can_support_a_precise_local_request_to_delivery_chain(self):
        paper, _, _, extraction, review = self.fixtures()
        local = code_segment("direct.py", (
            "def direct(case, model, victim):\n"
            "    payload = model.generate({\"task\": case[\"user_request\"]})\n"
            "    return victim.inject(payload, channel=\"direct\")\n"
        ))
        repository = source_bundle([local])
        merged = v4.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = merged["sha256"]
        flow = extraction["flows"][0]
        request = {"segment_id": local["id"], "quote": 'payload = model.generate({"task": case["user_request"]})'}
        delivery = {"segment_id": local["id"], "quote": 'return victim.inject(payload, channel="direct")'}
        flow["implementation"] = copy.deepcopy(request)
        flow["delivery"]["citation"] = copy.deepcopy(delivery)
        flow["scope_resolution"].update(basis="specific_rule", common_rule=None, specific_rule=copy.deepcopy(flow["declaration"]))
        flow["code_path"] = [
            {"kind": "request", "input_symbol": "case.user_request", "output_symbol": "direct.payload", "citation": request, "explanation": "Directly bound request input in this local arm."},
            {"kind": "delivery", "input_symbol": "direct.payload", "output_symbol": "victim.direct.input", "citation": delivery, "explanation": "That payload enters the direct branch."},
        ]
        result = self.decide(extraction, review, merged)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertEqual(result["evidence_scope"], "listed_claims_paper_and_pinned_source")
        self.assertNotEqual(result["review_status"], "human_verified")

    def test_source_snapshot_is_not_runtime_or_a_saved_request(self):
        for kind in ("runtime", "saved_request"):
            with self.subTest(kind=kind):
                _, _, merged, extraction, review = self.fixtures()
                extraction["flows"][0]["delivery"]["evidence_kind"] = kind
                result = self.decide(extraction, review, merged)
                self.assert_no_positive(result)
                self.assertIn("source_snapshot_cannot_establish_runtime", result["evidence"][0]["source_validation"]["validation_errors"])

    def test_empty_claims_do_not_become_a_source_audit_negative(self):
        _, _, merged, extraction, review = self.fixtures()
        extraction["flows"] = []
        review["flow_reviews"] = []
        result = self.decide(extraction, review, merged)
        self.assert_no_positive(result)
        self.assertEqual(result["evidence"], [])

    def test_partial_repository_can_support_only_a_bounded_positive(self):
        paper, repository, _, extraction, review = self.fixtures()
        relevant = repository["segments"]
        source_limit = sum(len(part["text"]) for part in relevant) + 20
        repository = source_bundle(relevant + [code_segment("unrelated.py", "# Unrelated source\n" * 500)], max_chars=source_limit)
        self.assertFalse(repository["coverage"]["complete"])
        merged = v4.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = merged["sha256"]
        result = self.decide(extraction, review, merged)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertFalse(result["coverage_complete"])

    def test_modified_source_text_or_line_metadata_cannot_bypass_repository_validation(self):
        paper, repository, _, _, _ = self.fixtures()
        for field in ("text", "line_start", "line_end", "id"):
            with self.subTest(field=field):
                altered = copy.deepcopy(repository)
                part = altered["segments"][0]
                part[field] = part[field] + (" changed" if isinstance(part[field], str) else 1)
                with self.assertRaises(ValueError):
                    v4.combine_inputs(paper, altered)

    def test_binding_changes_with_selected_files_even_when_repository_manifest_is_identical(self):
        paper, _, _, _, _ = self.fixtures()
        with tempfile.TemporaryDirectory(prefix="binding budget ") as temporary:
            root = Path(temporary)
            (root / "pipeline.py").write_text("def construct(x):\n    return x\n", encoding="utf-8")
            (root / "unrelated.py").write_text("# extra source\n" * 100, encoding="utf-8")
            small = load_repository(str(root), max_chars=50)
            large = load_repository(str(root), max_chars=5000)
        self.assertEqual(small["manifest_sha256"], large["manifest_sha256"])
        self.assertNotEqual(len(small["segments"]), len(large["segments"]))
        self.assertNotEqual(v4.combine_inputs(paper, small)["sha256"],
                            v4.combine_inputs(paper, large)["sha256"])

    def test_binding_covers_reading_order_and_primary_citation_views_independently(self):
        paper, repository, merged, _, _ = self.fixtures()
        reading = copy.deepcopy(paper)
        reading["segments"][0]["reading_order_text"] = "Another reading-order representation."
        first = v4.combine_inputs(reading, repository)
        self.assertEqual(first["paper_sha256"], merged["paper_sha256"])
        self.assertNotEqual(first["sha256"], merged["sha256"])
        primary = copy.deepcopy(reading)
        primary["segments"][0]["text"] += " Different primary-layout citation view."
        second = v4.combine_inputs(primary, repository)
        self.assertEqual(v4.model_content(first)["segments"], v4.model_content(second)["segments"])
        self.assertNotEqual(first["sha256"], second["sha256"])

    def test_binding_covers_ordered_source_segments_and_all_model_repository_metadata(self):
        paper, repository, merged, _, _ = self.fixtures()
        reordered = copy.deepcopy(repository)
        reordered["segments"].reverse()
        self.assertEqual(reordered["manifest_sha256"], repository["manifest_sha256"])
        self.assertNotEqual(v4.combine_inputs(paper, reordered)["sha256"], merged["sha256"])
        metadata = copy.deepcopy(repository)
        metadata["coverage"]["max_characters"] += 1
        changed = v4.combine_inputs(paper, metadata)
        self.assertEqual(changed["segments"], merged["segments"])
        self.assertNotEqual(changed["sha256"], merged["sha256"])

    def test_model_content_preserves_original_payload_contract_without_exposing_labels(self):
        _, _, merged, _, _ = self.fixtures()
        actual = v4.model_content(merged)
        old_caller = {
            "source_type": merged["media_type"],
            "segments": [{"id": p["id"], "text": p.get("reading_order_text", p["text"])}
                         for p in merged["segments"]],
            "input_binding": merged["sha256"], "repository": merged["repository"],
            "paper_sha256": merged["paper_sha256"],
        }
        self.assertEqual(actual, old_caller)
        self.assertNotIn("expected", actual)
        self.assertNotIn("gold", actual)
        actual["repository"]["coverage"]["max_characters"] = 1
        actual["segments"][0]["text"] = "A caller mutation cannot rewrite prepared evidence."
        v4.validate_input_binding(merged)

    def test_changed_combined_views_or_metadata_are_rejected_before_replay_decision(self):
        _, _, merged, extraction, review = self.fixtures()
        changes = [
            lambda d: d["segments"][0].update(text=d["segments"][0]["text"] + " extra citation text"),
            lambda d: d["segments"][0].update(reading_order_text="changed input view"),
            lambda d: d["repository"]["coverage"].update(max_characters=999999),
            lambda d: d["coverage"].update(complete=False),
            lambda d: d["paper_coverage"].update(reason="different coverage statement"),
            lambda d: d["segments"].reverse(),
            lambda d: d.update(text="silently truncated bookkeeping text"),
        ]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                changed = copy.deepcopy(merged)
                change(changed)
                with self.assertRaisesRegex(ValueError, "input binding"):
                    v4.model_content(changed)
                with self.assertRaisesRegex(ValueError, "input binding"):
                    self.decide(extraction, review, changed)

    def test_legacy_three_identity_binding_does_not_masquerade_as_current_full_payload_binding(self):
        _, _, merged, extraction, review = self.fixtures()
        old = copy.deepcopy(merged)
        old.pop("input_binding_version")
        old.pop("model_content_sha256")
        old["sha256"] = hashlib.sha256(json.dumps(old["input_binding"], sort_keys=True).encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, "obsolete"):
            v4.model_content(old)
        with self.assertRaisesRegex(ValueError, "obsolete"):
            self.decide(extraction, review, old)


if __name__ == "__main__":
    unittest.main()
