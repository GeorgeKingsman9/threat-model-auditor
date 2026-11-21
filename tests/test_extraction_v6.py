"""V6 coverage, sampled-data provenance and historical-engine compatibility.

Synthetic review votes exercise deterministic gates, not model accuracy.
"""

import copy
import json
from pathlib import Path
import tempfile
import unittest

import extraction_v4 as v4
import extraction_v6 as v6
from evidence_expansion import DATA_POLICY
from source_bundle import load_repository
import test_extraction_v5 as toy


class ExtractionV6Tests(unittest.TestCase):
    def fixtures(self):
        paper, repository, _, extraction, review = toy.ExtractionV5Tests().fixtures()
        document = v6.combine_inputs(paper, repository)
        extraction["schema_version"] = review["schema_version"] = 6
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        extraction.update(channel_assessments=[], deployment_findings=[])
        review.update(channel_reviews=[], deployment_reviews=[])
        for item in document["model_repository"]["input_channels"]["candidates"]:
            extraction["channel_assessments"].append({"candidate_id": item["id"],
                "channel_kind": item["channel_kind"], "status": "unresolved", "flow_index": None,
                "citations": [], "reason": "The additional channel is not yet mapped."})
            review["channel_reviews"].append({"candidate_id": item["id"], "mapping_supported": False,
                "exclusion_supported": False, "reason": "Do not assume coverage from another argument."})
        return paper, repository, document, extraction, review

    def test_confirmed_local_violation_survives_other_uncovered_inputs(self):
        _, _, document, extraction, review = self.fixtures()
        result = v6.decide_extraction(extraction, review, document)
        self.assertEqual(result["schema_version"], 6)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertGreater(result["channel_coverage"]["candidate_count"], 0)
        self.assertFalse(result["channel_coverage"]["complete"])
        self.assertFalse(result["deployment_assessment"]["general_clean_blocked"])

    def test_explicit_permission_does_not_hide_other_unexamined_channels(self):
        _, _, document, extraction, review = self.fixtures()
        flow = extraction["flows"][0]
        flow["permission"] = "allow"
        flow["refutation"]["basis"] = "explicit_permission"
        flow["refutation"]["citation"] = copy.deepcopy(flow["declaration"])
        review["flow_reviews"][0]["refutation"] = "explicit_permission"
        result = v6.decide_extraction(extraction, review, document)
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["reason"], "unresolved_input_or_deployment_obligations")

    def test_changed_inventory_or_its_binding_cannot_be_replayed(self):
        _, _, document, extraction, review = self.fixtures()
        altered = copy.deepcopy(document)
        altered["model_repository"]["input_channels"]["candidates"] = []
        with self.assertRaisesRegex(ValueError, "input binding"):
            v6.decide_extraction(extraction, review, altered)
        altered["model_content_sha256"] = v4._hash_json(v4._unbound_model_content(altered))
        altered["sha256"] = v4._hash_json(v4._binding_material(altered))
        with self.assertRaisesRegex(ValueError, "channel inventory"):
            v6.validate_input_binding(altered)

    def test_unknown_channel_ids_are_visible_without_erasing_valid_positive(self):
        _, _, document, extraction, review = self.fixtures()
        extraction["channel_assessments"].append({"candidate_id": "invented", "channel_kind": "question",
            "status": "out_of_scope", "flow_index": None, "citations": [], "reason": "Untrusted claim."})
        result = v6.decide_extraction(extraction, review, document)
        self.assertEqual(result["verdict"], "inconsistent")
        self.assertIn("unknown_or_duplicate_channel_id", result["channel_coverage"]["validation_errors"])

    def test_data_witness_is_exact_locatable_sample_not_raw_model_dump(self):
        paper, repository, _, _, _ = self.fixtures()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for part in repository["segments"]:
                path = root / part["path"]; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(part["text"])
            with (root / "generator.py").open("a") as stream:
                stream.write('\nDATA_PATH = "data/tasks.json"\n')
            raw = json.dumps([{"question": f"Which city {index}?", "text": "中文 evidence"}
                              for index in range(10)], ensure_ascii=False, indent=2).encode()
            (root / "data").mkdir(); (root / "data/tasks.json").write_bytes(raw)
            snapshot = load_repository(str(root), evidence_policy=DATA_POLICY)
            document = v6.combine_inputs(paper, snapshot)
            witness = snapshot["data_witnesses"][0]
            quote = '"question": "Which city 0?"'
            locator = v4._locate({"segment_id": witness["id"], "quote": quote}, document, "code")
            bounds = locator["data_witness"]
            self.assertEqual(raw[bounds["byte_start"]:bounds["byte_end"]].decode(), quote)
            self.assertEqual(locator["file_sha256"], snapshot["data_blobs"][0]["sha256"])
            payload = json.dumps(v6.model_content(document), ensure_ascii=False)
            self.assertNotIn("raw_base64", payload)
            visible_records = sum(f"Which city {index}?" in payload for index in range(10))
            self.assertEqual(visible_records, len(snapshot["data_witnesses"]))
            self.assertLess(visible_records, 10)
            self.assertFalse(document["coverage"]["complete"])
            v6.validate_input_binding(document)
            mutations = [
                lambda d: next(p for p in d["segments"] if "data_witness_origin" in p).update(text="changed author data"),
                lambda d: next(p for p in d["segments"] if "data_witness_origin" in p)["data_witness_origin"].update(byte_start=0),
                lambda d: d["model_repository"]["data_evidence"]["files"][0]["coverage"].update(complete=True),
                lambda d: d["coverage"].update(complete=True),
            ]
            for mutate in mutations:
                altered = copy.deepcopy(document); mutate(altered)
                with self.assertRaisesRegex(ValueError, "data|sampled"):
                    v6._refresh_binding(altered)
            altered = copy.deepcopy(document)
            clone = copy.deepcopy(next(p for p in altered["segments"] if "data_witness_origin" in p))
            clone.pop("data_witness_origin"); clone["text"] = "unverified duplicate"
            altered["segments"].insert(0, clone)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                v6._refresh_binding(altered)


if __name__ == "__main__":
    unittest.main()
