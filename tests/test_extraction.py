"""Check grounding and conservative decisions using fixtures, never model/API calls."""

import copy
import hashlib
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extraction import (
    decide_extraction, EXTRACT_PROMPT, EXTRACTION_SCHEMA, locate,
    REVIEW_PROMPT, prompt_hash, validate_shape,
)


class ExtractionTests(unittest.TestCase):
    def fixtures(self):
        text = (
            "This research evaluates indirect prompt injection. "
            "The online attacker cannot read the full user query. "
            "In the online evaluation, its construction input contains the full user query. "
            "Benchmark designers may read full queries during offline setup. "
            "A separate topic phrase is stellar evolution in red giants."
        )
        document = {
            "source": "fixture.txt", "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "segments": [{"id": "s1", "text": text}], "coverage": {"complete": True},
        }
        extraction = {
            "title": "Test fixture, not a research finding",
            "applicability": "in_scope",
            "applicability_reason": "Evaluates indirect prompt injection.",
            "applicability_citation": {"segment_id": "s1", "quote": "evaluates indirect prompt injection"},
            "scope_summary": "The online evaluation only",
            "flows": [{
                "edge": {
                    "role": "online attacker", "phase": "online construction",
                    "source": "current user request", "representation": "exact query text",
                    "operation": "receive as input", "query_form": "full_query",
                },
                "permission": "deny", "observation": "present",
                "declaration": {"segment_id": "s1", "quote": "online attacker cannot read the full user query"},
                "implementation": {"segment_id": "s1", "quote": "construction input contains the full user query"},
                "explanation": "The specified online access boundary is contradicted by its described input.",
            }],
            "limitations": ["Paper-text fixture only; no execution artifact."],
        }
        review = {
            "applicability": "in_scope", "applicability_supported": True,
            "flow_reviews": [{"index": 0, "supported": True, "reason": "The same online role and query are specified."}],
            "limitations": ["This test simulates a review, not a model or human verification."],
        }
        return extraction, review, document

    def decide(self, extraction=None, review=None, document=None):
        default_extraction, default_review, default_document = self.fixtures()
        return decide_extraction(
            default_extraction if extraction is None else extraction,
            default_review if review is None else review,
            default_document if document is None else document,
            paper_id="fixture_paper",
        )

    def test_inconsistency_has_two_grounded_locators_and_model_review_label(self):
        extraction, review, document = self.fixtures()
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertIs(result["has_confirmed_inconsistency"], True)
        self.assertEqual(result["review_status"], "model_reviewed_not_human_verified")
        self.assertEqual(len(result["evidence"]), 1)
        evidence = result["evidence"][0]
        self.assertIs(evidence["semantic_review"]["supported"], True)
        self.assertEqual(set(evidence["locators"]), {"declaration", "implementation"})
        text = document["segments"][0]["text"]
        for field, locator in evidence["locators"].items():
            self.assertEqual(locator["document_sha256"], document["sha256"])
            self.assertEqual(text[locator["start"]:locator["end"]], extraction["flows"][0][field]["quote"])

    def test_no_extracted_flows_is_not_a_clean_paper(self):
        extraction, review, document = self.fixtures()
        extraction["flows"] = []
        review["flow_reviews"] = []
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_permitted_or_absent_flow_never_clears_the_entire_paper(self):
        for permission, observation in (("allow", "present"), ("deny", "absent")):
            with self.subTest(permission=permission, observation=observation):
                extraction, review, document = self.fixtures()
                extraction["flows"][0]["permission"] = permission
                extraction["flows"][0]["observation"] = observation
                result = self.decide(extraction, review, document)
                self.assertEqual(result["evidence"][0]["verdict"], "consistent_within_scope")
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_forged_quote_cannot_confirm_inconsistency(self):
        for field in ("declaration", "implementation"):
            with self.subTest(field=field):
                extraction, review, document = self.fixtures()
                extraction["flows"][0][field]["quote"] = "This is a fabricated sentence absent from the supplied document."
                result = self.decide(extraction, review, document)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)
                self.assertTrue(result["evidence"][0]["citation_errors"])
                self.assertNotIn(field, result["evidence"][0]["locators"])

    def test_missing_citation_or_wrong_segment_cannot_confirm_inconsistency(self):
        for invalid_citation in (None, {"segment_id": "nonexistent", "quote": "online attacker"}):
            with self.subTest(citation=invalid_citation):
                extraction, review, document = self.fixtures()
                extraction["flows"][0]["implementation"] = invalid_citation
                result = self.decide(extraction, review, document)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_semantic_review_can_reject_real_quotes(self):
        extraction, review, document = self.fixtures()
        review["flow_reviews"][0].update(supported=False, reason="The quotations do not establish the claimed causal access.")
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        row = result["evidence"][0]
        self.assertEqual(set(row["locators"]), {"declaration", "implementation"})
        self.assertEqual(row["matching_rules"], [])
        self.assertEqual(row["matching_observations"], [])
        self.assertIn("semantic_review_unsupported", row["citation_errors"][0])

    def test_partial_query_inference_rejected_by_review_does_not_become_a_finding(self):
        extraction, review, document = self.fixtures()
        extraction["flows"][0]["edge"]["query_form"] = "partial_query"
        review["flow_reviews"][0].update(
            supported=False,
            reason="A full-query restriction does not by itself prohibit partial-query access.",
        )
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        self.assertEqual(result["evidence"][0]["target"]["query_form"], "partial_query")

    def test_offline_designer_quote_cannot_override_a_rejected_online_claim(self):
        extraction, review, document = self.fixtures()
        extraction["flows"][0]["implementation"]["quote"] = "Benchmark designers may read full queries during offline setup"
        review["flow_reviews"][0].update(
            supported=False,
            reason="Offline benchmark designers and the online attacker are different roles and phases.",
        )
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def unrelated(self):
        extraction, review, document = self.fixtures()
        extraction.update(
            applicability="out_of_scope", applicability_reason="This is an astrophysics paper.",
            applicability_citation={"segment_id": "s1", "quote": "stellar evolution in red giants"},
            flows=[],
        )
        review.update(applicability="out_of_scope", flow_reviews=[])
        return extraction, review, document

    def test_unrelated_needs_agreement_exact_citation_and_complete_document(self):
        extraction, review, document = self.unrelated()
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "not_applicable")
        self.assertIs(result["has_confirmed_inconsistency"], False)
        self.assertIn("applicability_locator", result)
        for missing_requirement in ("complete", "review", "classification"):
            with self.subTest(missing=missing_requirement):
                ext, rev, doc = copy.deepcopy((extraction, review, document))
                if missing_requirement == "complete":
                    doc["coverage"]["complete"] = False
                elif missing_requirement == "review":
                    rev["applicability_supported"] = False
                else:
                    rev["applicability"] = "uncertain"
                result = self.decide(ext, rev, doc)
                self.assertEqual(result["verdict"], "insufficient_evidence")
                self.assertIs(result["has_confirmed_inconsistency"], False)
        extraction["applicability_citation"]["quote"] = "A fabricated astrophysics title"
        with self.assertRaises(ValueError):
            self.decide(extraction, review, document)

    def test_each_proposed_flow_must_be_reviewed_exactly_once(self):
        for indexes in ([], [0, 0], [-1], [1]):
            with self.subTest(indexes=indexes):
                extraction, review, document = self.fixtures()
                review["flow_reviews"] = [{"index": index, "supported": True, "reason": "test"} for index in indexes]
                with self.assertRaises(ValueError):
                    self.decide(extraction, review, document)

    def test_ambiguous_quote_is_rejected_instead_of_pointing_at_the_first_occurrence(self):
        extraction, review, document = self.fixtures()
        quote = extraction["flows"][0]["declaration"]["quote"]
        document["segments"][0]["text"] += " " + quote
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            locate(extraction["flows"][0]["declaration"], document)
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_out_of_scope_with_proposed_flows_is_not_accepted_as_unrelated(self):
        extraction, review, document = self.fixtures()
        extraction.update(
            applicability="out_of_scope", applicability_reason="Conflicting proposal",
            applicability_citation={"segment_id": "s1", "quote": "stellar evolution in red giants"},
        )
        review["applicability"] = "out_of_scope"
        result = self.decide(extraction, review, document)
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertIs(result["has_confirmed_inconsistency"], False)

    def test_review_schema_changes_the_recorded_prompt_hash(self):
        original = prompt_hash()
        with patch("extraction.REVIEW_SCHEMA", {"changed": True}):
            self.assertNotEqual(prompt_hash(), original)

    def test_unsupported_enum_and_extra_fields_fail_closed(self):
        for field, value in (("permission", "required"), ("observation", "not_found")):
            with self.subTest(field=field):
                extraction, _, _ = self.fixtures()
                extraction["flows"][0][field] = value
                with self.assertRaises(ValueError):
                    validate_shape(extraction, EXTRACTION_SCHEMA)
        extraction, _, _ = self.fixtures()
        extraction["hidden_override"] = "consistent"
        with self.assertRaises(ValueError):
            validate_shape(extraction, EXTRACTION_SCHEMA)

    def test_prompts_explicitly_distinguish_query_forms_and_roles(self):
        self.assertIn("full_query and partial_query differ", EXTRACT_PROMPT)
        for role in ("designer", "offline construction", "online attacker", "evaluator"):
            self.assertIn(role, EXTRACT_PROMPT)
        self.assertIn("offline and online roles differ", REVIEW_PROMPT)
        self.assertIn("untrusted", EXTRACT_PROMPT)
        self.assertIn("untrusted", REVIEW_PROMPT)


if __name__ == "__main__":
    unittest.main()
