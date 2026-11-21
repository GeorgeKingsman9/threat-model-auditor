"""Offline declared-model boundaries; these tests do not assess model accuracy."""

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import declared_contract as contract


def citation(quote, segment="p1"):
    return {"segment_id": segment, "quote": quote}


def field(text="", *quotes, status=None):
    return {"status": status or ("explicit" if quotes else "unspecified"),
            "text": text, "citations": [citation(quote) for quote in quotes]}


def knowledge(text="", *quotes, status=None, granularity="unspecified"):
    return {**field(text, *quotes, status=status), "granularity": granularity}


class DeclaredContractTests(unittest.TestCase):
    def fixtures(self):
        text = (
            "The victim input concatenates a user instruction and external data. "
            "The user instruction contains the evaluated task question. "
            "An external attacker does not know this user instruction. "
            "The constructor receives a resource title and a resource description. "
            "It produces a candidate data document. "
            "This setting evaluates one shared attacker model."
        )
        paper = {"sha256": hashlib.sha256(text.encode()).hexdigest(),
                 "media_type": "application/pdf", "segments": [{"id": "p1", "text": text}]}
        proposal = {
            "schema_version": 1, "paper_sha256": paper["sha256"],
            "knowledge_rules": [{
                "role": field("External attacker", "An external attacker does not know"),
                "phase": field(),
                "source": field("User instruction", "does not know this user instruction"),
                "allowed_knowledge": knowledge(),
                "forbidden_knowledge": knowledge(
                    "The stated user instruction is unknown to this attacker.",
                    "An external attacker does not know this user instruction",
                    granularity="paper-defined user instruction"),
                "scope": field("Shared model", "one shared attacker model"),
                "exceptions": field(),
            }],
            "task_input_definition": {
                "definition": field("Concatenated victim input", "concatenates a user instruction and external data"),
                "components": [
                    {"concept": "user instruction", "definition": field(
                        "Contains the evaluated task question.",
                        "user instruction contains the evaluated task question")},
                    {"concept": "external data", "definition": field(
                        "External component of the concatenated input.",
                        "a user instruction and external data")},
                ],
                "relationships": [{"component_concepts": ["user instruction", "external data"],
                                   "relationship": field("Concatenation.",
                                       "victim input concatenates a user instruction and external data")}],
            },
            "construction_recipe": {
                "procedure": field("Generate a candidate document.", "It produces a candidate data document"),
                "metadata_budget": field("Resource title and description.",
                                         "receives a resource title and a resource description"),
                "inputs": [{"concept": "resource metadata", "description": field(
                    "Resource title and description.", "a resource title and a resource description")}],
                "generated_artifacts": [{"concept": "candidate data document", "description": field(
                    "Constructed candidate.", "produces a candidate data document")}],
                "scope": field(),
            },
            "unresolved_questions": ["Does the stated model apply during offline construction?"],
            "limitations": ["Declared paper model only; implementation has not been supplied."],
        }
        return paper, proposal

    def test_prepare_strips_all_nonpaper_metadata_and_preserves_ids(self):
        paper, _ = self.fixtures()
        paper.update(repository={"private_source": "constructor(secret_question)"},
                     previous_verdict="inconsistent", expected_label="secret label",
                     source="private/local/path", title="unneeded paper identifier")
        paper["segments"][0].update(path="implementation.py", expected_label="secret label")
        before = copy.deepcopy(paper)
        payload = contract.prepare_contract_input(paper)
        self.assertEqual(set(payload), {"source_type", "segments", "paper_sha256"})
        self.assertEqual(payload["segments"], [{"id": "p1", "text": paper["segments"][0]["text"]}])
        encoded = json.dumps(payload)
        for value in ("private_source", "constructor(secret_question)", "previous_verdict",
                      "expected_label", "implementation.py", "private/local/path"):
            self.assertNotIn(value, encoded)
        self.assertEqual(paper, before)
        payload["segments"][0]["text"] = "changed returned copy"
        self.assertEqual(paper, before)

    def test_reconstructed_domain_needs_no_source_title_or_coverage(self):
        paper, proposal = self.fixtures()
        result = contract.validate_contract(proposal, paper)
        self.assertTrue(result["citations_grounded"])
        self.assertEqual(result["citation_errors"], [])
        locator = result["locators"]["knowledge_rules[0].forbidden_knowledge"][0]
        self.assertEqual(locator["segment_id"], "p1")
        self.assertEqual(locator["source_kind"], "paper")
        self.assertEqual(locator["paper_sha256"], paper["sha256"])
        self.assertEqual(locator["document_sha256"], paper["sha256"])
        self.assertEqual(locator["text_view"], "primary")

    def test_combined_documents_and_explicit_code_segments_are_rejected(self):
        paper, _ = self.fixtures()
        combined = {**paper, "media_type": "paper+source"}
        with self.assertRaisesRegex(ValueError, "paper-only"):
            contract.prepare_contract_input(combined)
        paper["segments"].append({"id": "repo:builder", "text": "secret", "source_kind": "code"})
        with self.assertRaisesRegex(ValueError, "paper only"):
            contract.prepare_contract_input(paper)

    def test_only_selected_reading_order_view_is_a_citation_domain(self):
        paper, proposal = self.fixtures()
        primary_only = "Hidden layout view has an unrelated authoring allowance."
        paper["segments"][0]["reading_order_text"] = paper["segments"][0]["text"]
        paper["segments"][0]["text"] = primary_only
        result = contract.validate_contract(proposal, paper)
        self.assertTrue(result["citations_grounded"])
        locator = result["locators"]["construction_recipe.metadata_budget"][0]
        self.assertEqual(locator["text_view"], "reading_order")
        selected = paper["segments"][0]["reading_order_text"]
        self.assertEqual(selected[locator["start"]:locator["end"]],
                         "receives a resource title and a resource description")
        self.assertEqual(contract.prepare_contract_input(paper)["segments"][0]["text"], selected)
        proposal["knowledge_rules"][0]["allowed_knowledge"] = knowledge(
            "Unshown allowance", "unrelated authoring allowance", granularity="unknown")
        result = contract.validate_contract(proposal, paper)
        self.assertFalse(result["citations_grounded"])
        self.assertEqual(result["locators"]["knowledge_rules[0].allowed_knowledge"], [])
        self.assertTrue(any("absent" in error for error in result["citation_errors"]))

    def test_normalized_exact_locators_use_original_offsets(self):
        paper, proposal = self.fixtures()
        paper["segments"][0]["text"] = paper["segments"][0]["text"].replace(
            "resource title and a resource description", "resource\n title and a resource\t description")
        result = contract.validate_contract(proposal, paper)
        self.assertTrue(result["citations_grounded"])
        locator = result["locators"]["construction_recipe.metadata_budget"][0]
        raw = paper["segments"][0]["text"][locator["start"]:locator["end"]]
        self.assertIn("\n", raw)
        self.assertIn("\t", raw)
        self.assertEqual(locator["match"], "normalized_exact")

    def test_bad_extra_citation_is_reported_without_erasing_valid_citations(self):
        paper, proposal = self.fixtures()
        citations = proposal["knowledge_rules"][0]["forbidden_knowledge"]["citations"]
        citations.extend([citation("not in the supplied paper"),
                          citation("does not know this user instruction", segment="paper:p1")])
        result = contract.validate_contract(proposal, paper)
        self.assertFalse(result["citations_grounded"])
        self.assertEqual(len(result["citation_errors"]), 2)
        self.assertEqual(len(result["locators"]["knowledge_rules[0].forbidden_knowledge"]), 1)
        self.assertTrue(result["locators"]["construction_recipe.metadata_budget"])
        self.assertEqual(result["proposal"], proposal)
        self.assertTrue(any("citations[2]" in error for error in result["citation_errors"]))

    def test_ambiguous_quote_is_rejected_and_ids_must_be_unique(self):
        paper, proposal = self.fixtures()
        quote = "produces a candidate data document"
        paper["segments"][0]["text"] += " " + quote
        result = contract.validate_contract(proposal, paper)
        self.assertFalse(result["citations_grounded"])
        self.assertTrue(any("ambiguous" in error for error in result["citation_errors"]))
        paper["segments"].append(copy.deepcopy(paper["segments"][0]))
        with self.assertRaisesRegex(ValueError, "unique"):
            contract.validate_contract(proposal, paper)

    def test_metadata_recipe_does_not_create_a_question_permission_or_ban(self):
        paper, proposal = self.fixtures()
        paper["segments"][0]["text"] = (
            "The constructor receives a resource title and a resource description. "
            "It produces a candidate data document."
        )
        proposal["knowledge_rules"] = []
        proposal["task_input_definition"] = {"definition": field(), "components": [], "relationships": []}
        result = contract.validate_contract(proposal, paper)
        self.assertTrue(result["citations_grounded"])
        self.assertEqual(result["proposal"]["knowledge_rules"], [])
        self.assertTrue(result["locators"]["construction_recipe.metadata_budget"])
        self.assertTrue(result["semantic_review_required"])
        self.assertEqual(result["trust"], "untrusted_declared_contract_proposal")
        for key in ("verdict", "permission", "has_confirmed_inconsistency", "semantic_supported"):
            self.assertNotIn(key, result)

    def test_literal_definitions_and_honest_uncertainty_are_preserved(self):
        paper, proposal = self.fixtures()
        statement = proposal["knowledge_rules"][0]["forbidden_knowledge"]
        statement["status"] = "uncertain"
        statement["text"] = "The scope during construction is unresolved."
        result = contract.validate_contract(proposal, paper)
        self.assertEqual(result["proposal"]["knowledge_rules"][0]["forbidden_knowledge"], statement)
        self.assertEqual(result["proposal"]["task_input_definition"], proposal["task_input_definition"])
        self.assertTrue(result["semantic_review_required"])
        # Successful location cannot decide whether an instruction denotes the
        # full question, a shared generic string or a different paper concept.
        self.assertNotIn("policy_application", json.dumps(result))
        result["proposal"]["knowledge_rules"][0]["forbidden_knowledge"]["status"] = "explicit"
        self.assertEqual(proposal["knowledge_rules"][0]["forbidden_knowledge"]["status"], "uncertain")

    def test_explicit_declarations_need_text_and_citations(self):
        paper, proposal = self.fixtures()
        proposal["knowledge_rules"][0]["allowed_knowledge"] = knowledge(
            "Unsubstantiated grant", status="explicit", granularity="full question")
        proposal["knowledge_rules"][0]["phase"] = field("", "external attacker", status="explicit")
        result = contract.validate_contract(proposal, paper)
        self.assertEqual(len(result["citation_errors"]), 2)
        self.assertFalse(result["citations_grounded"])
        self.assertTrue(result["semantic_review_required"])
        self.assertEqual(result["locators"]["knowledge_rules[0].allowed_knowledge"], [])

    def test_unspecified_knowledge_stays_unspecified(self):
        paper, proposal = self.fixtures()
        statement = proposal["knowledge_rules"][0]["allowed_knowledge"]
        statement["granularity"] = "exact question"
        statement["citations"] = [citation("a resource title and a resource description")]
        result = contract.validate_contract(proposal, paper)
        self.assertFalse(result["citations_grounded"])
        self.assertEqual(len(result["citation_errors"]), 2)
        self.assertEqual(result["proposal"]["knowledge_rules"][0]["allowed_knowledge"]["status"], "unspecified")

    def test_shape_hash_and_all_array_limits_fail_closed(self):
        paper, proposal = self.fixtures()
        bad = copy.deepcopy(proposal)
        bad["paper_sha256"] = "different paper"
        with self.assertRaisesRegex(ValueError, "paper hash"):
            contract.validate_contract(bad, paper)
        bad = copy.deepcopy(proposal)
        bad["verdict"] = "inconsistent"
        with self.assertRaisesRegex(ValueError, "extra fields"):
            contract.validate_contract(bad, paper)
        cases = [
            ("rules", lambda item: item.update(knowledge_rules=item["knowledge_rules"] * 7)),
            ("citations", lambda item: item["knowledge_rules"][0]["role"].update(
                citations=item["knowledge_rules"][0]["role"]["citations"] * 7)),
            ("components", lambda item: item["task_input_definition"].update(
                components=item["task_input_definition"]["components"] * 5)),
            ("artifacts", lambda item: item["construction_recipe"].update(
                generated_artifacts=item["construction_recipe"]["generated_artifacts"] * 9)),
        ]
        for name, change in cases:
            with self.subTest(array=name):
                bad = copy.deepcopy(proposal)
                change(bad)
                with self.assertRaisesRegex(ValueError, "item limit"):
                    contract.validate_contract(bad, paper)

    def test_component_relationships_cannot_name_unlisted_or_duplicate_concepts(self):
        paper, proposal = self.fixtures()
        proposal["task_input_definition"]["relationships"][0]["component_concepts"].append("guessed question field")
        with self.assertRaisesRegex(ValueError, "listed component"):
            contract.validate_contract(proposal, paper)
        paper, proposal = self.fixtures()
        proposal["task_input_definition"]["components"][1]["concept"] = "user instruction"
        with self.assertRaisesRegex(ValueError, "unique"):
            contract.validate_contract(proposal, paper)

    def test_validation_does_not_mutate_either_input(self):
        paper, proposal = self.fixtures()
        original_paper, original_proposal = copy.deepcopy(paper), copy.deepcopy(proposal)
        result = contract.validate_contract(proposal, paper)
        self.assertEqual(paper, original_paper)
        self.assertEqual(proposal, original_proposal)
        result["proposal"]["task_input_definition"]["definition"]["text"] = "mutated result"
        self.assertEqual(proposal, original_proposal)

    def test_prompt_and_schema_hash_are_reproducible(self):
        expected = hashlib.sha256((contract.PROMPT + json.dumps(contract.SCHEMA, sort_keys=True)).encode()).hexdigest()
        self.assertEqual(contract.prompt_hash(), expected)
        self.assertEqual(len(expected), 64)


if __name__ == "__main__":
    unittest.main()
