"""A candidate can discharge coverage only through its represented source path.

Synthetic reviewer votes deliberately approve an unrelated mapping in the
negative case. Exact candidate citations must not let that mapping reuse a
different, explicitly permitted flow to report a clean audit.
"""

import copy
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extraction_v6 as v6
from source_bundle import load_repository
import test_v6_deployment_integration as fixtures


class V6ChannelCoverageLinkTests(unittest.TestCase):
    def inputs(self, *, extra_source=None, question_source=False):
        original, extraction, review = fixtures.V6DeploymentIntegrationTests().fixtures(with_gap=False)
        paper_parts = [{"id": part["id"].removeprefix("paper:"), "text": part["text"]}
                       for part in original["segments"] if part["source_kind"] == "paper"]
        paper = {
            "source": original["source"], "media_type": original["media_type"],
            "sha256": original["paper_sha256"], "coverage": original["paper_coverage"],
            "links": original["links"], "segments": paper_parts,
            "text": "\n".join(part["text"] for part in paper_parts),
        }
        with tempfile.TemporaryDirectory(prefix="v6 candidate path link ") as temporary:
            root = Path(temporary)
            for part in original["segments"]:
                if part["source_kind"] != "code":
                    continue
                text = part["text"]
                if question_source and part["path"] == "generator.py":
                    text = text.replace("record", "question")
                (root / part["path"]).write_text(text, encoding="utf-8")
            if extra_source is not None:
                (root / "optimizer.py").write_text(extra_source, encoding="utf-8")
            repository = load_repository(str(root))
        if question_source:
            for step in extraction["flows"][0]["code_path"]:
                for key in ("input_symbol", "output_symbol"):
                    step[key] = step[key].replace("record", "question")
                step["citation"]["quote"] = step["citation"]["quote"].replace("record", "question")
        document = v6.combine_inputs(paper, repository)
        extraction["input_binding"] = review["input_binding"] = document["sha256"]
        extraction["channel_assessments"], review["channel_reviews"] = [], []
        for candidate in document["model_repository"]["input_channels"]["candidates"]:
            extraction["channel_assessments"].append({
                "candidate_id": candidate["id"], "channel_kind": candidate["channel_kind"],
                "status": "represented", "flow_index": 0,
                "citations": [copy.deepcopy(candidate["source_citation"]), copy.deepcopy(candidate["citation"])],
                "reason": "Propose that the direct constructor flow covers this input.",
            })
            review["channel_reviews"].append({
                "candidate_id": candidate["id"], "mapping_supported": True,
                "exclusion_supported": False,
                "reason": "Synthetic approval cannot replace source-path linkage.",
            })
        return document, extraction, review

    def test_unrelated_optimizer_question_cannot_reuse_permitted_constructor_flow(self):
        document, extraction, review = self.inputs(extra_source=(
            "def optimize(question, optimizer):\n"
            "    return optimizer.run(question=question)\n"
        ))
        result = v6.decide_extraction(extraction, review, document)
        self.assertEqual(result["evidence"][0]["claim_result"], "refuted")
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertFalse(result["channel_coverage"]["complete"])
        channels = result["channel_coverage"]["channels"]
        optimizer = next(item for item in channels if item["path"] == "optimizer.py")
        self.assertEqual(optimizer["channel_kind"], "question")
        self.assertEqual(optimizer["status"], "unresolved")
        constructor = next(item for item in channels if item["path"] == "generator.py")
        self.assertEqual(constructor["status"], "represented")

    def test_question_present_in_the_mapped_flow_path_can_complete_coverage(self):
        document, extraction, review = self.inputs(question_source=True)
        result = v6.decide_extraction(extraction, review, document)
        channels = result["channel_coverage"]["channels"]
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]["channel_kind"], "question")
        self.assertEqual(channels[0]["status"], "represented")
        self.assertTrue(result["channel_coverage"]["complete"])
        self.assertEqual(result["verdict"], "consistent_within_scope")


if __name__ == "__main__":
    unittest.main()
