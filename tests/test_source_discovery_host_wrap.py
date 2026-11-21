"""Offline generic PDF host/path hard-wrap recovery, with exact provenance."""

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import source_discovery as discovery


def paper(text, annotations=(), *, reading_order=False):
    segment = {"id": "p1", "text": text if not reading_order else "Layout text has no complete visible URL."}
    if reading_order:
        segment["reading_order_text"] = text
    return {"source": "paper.pdf", "text": segment["text"], "segments": [segment], "links": list(annotations),
            "link_contexts": [{"url": url, "source": "pdf_annotation", "text": "", "segment_id": "p1"}
                              for url in annotations]}


class HostWrappedSourceDiscoveryTests(unittest.TestCase):
    def resolve(self, document):
        calls = []

        def fetch(fetcher, url, accept=None):
            calls.append(url)
            if not url.startswith("https://api.github.com/repos/"):
                raise AssertionError("unexpected network request")
            repo = url.split("/repos/")[1].split("/commits?")[0]
            commit = "1" * 40
            return json.dumps([{"sha": commit, "html_url": f"https://github.com/{repo}/commit/{commit}"}]).encode(), url

        with patch.object(discovery._Fetcher, "fetch", new=fetch):
            return discovery.discover_repository(document, "paper.pdf"), calls

    def test_publicly_available_host_wrap_requires_exact_annotation_and_keeps_raw_offsets(self):
        for newline in ("\n", "\r\n"):
            for punctuation in (".", ")", ";", ""):
                with self.subTest(newline=newline, punctuation=punctuation):
                    text = "Prior paragraph.\n\nCode is publicly available at https://github.com/" + newline + "Owner-Name/research-code" + punctuation + "\n"
                    document = paper(text, ["https://github.com/Owner-Name/research-code"], reading_order=True)
                    before = copy.deepcopy(document)
                    result, calls = self.resolve(document)
                    self.assertEqual(result["status"], "selected")
                    self.assertEqual(result["repository"], "https://github.com/Owner-Name/research-code")
                    self.assertEqual(len(calls), 1)
                    evidence = result["evidence"][0]
                    self.assertEqual(evidence["text_view"], "reading_order_text")
                    self.assertEqual(evidence["segment_id"], "p1")
                    self.assertEqual(evidence["association"], "code_availability_with_same_page_annotation")
                    start = evidence["context_start"]
                    self.assertEqual(text[start:start + len(evidence["context"])], evidence["context"])
                    self.assertEqual(text[evidence["visible_url_start"]:evidence["visible_url_end"]], evidence["visible_url_fragment"])
                    self.assertIn("https://github.com/" + newline + "Owner-Name/research-code", evidence["visible_url_fragment"])
                    self.assertEqual(evidence["annotation_url"], "https://github.com/Owner-Name/research-code")
                    self.assertEqual(document, before)

    def test_host_alone_missing_mismatched_or_other_page_annotation_does_not_associate(self):
        full = "https://github.com/owner/study"
        for text, annotations, page in [
                ("Our code is available at https://github.com/", [full], "p1"),
                ("Our code is available at https://github.com/\nA following sentence.", [full], "p1"),
                ("Our code is available at https://github.com/\nowner/study.", [], "p1"),
                ("Our code is available at https://github.com/\nowner/study.", ["https://github.com/other/study"], "p1"),
                ("Our code is available at https://github.com/\nowner/study.", [full], "p2"),
        ]:
            with self.subTest(text=text, annotations=annotations, page=page):
                document = paper(text, annotations)
                for annotation in document["link_contexts"]:
                    annotation["segment_id"] = page
                result, calls = self.resolve(document)
                self.assertEqual(result["status"], "not_found")
                self.assertFalse(calls)
                self.assertFalse(any(candidate["accepted"] for candidate in result["candidates"]))

    def test_baseline_author_and_reference_contexts_stay_unassociated(self):
        for statement in ("Baseline X code is publicly available at ",
                          "We use the author's code, which is publicly available at ",
                          "Smith et al.'s code is publicly available at ",
                          "Our code extends the method. Baseline code is publicly available at ",
                          "References:\nCode is publicly available at ",
                          "We adopt a library whose code is publicly available at "):
            with self.subTest(statement=statement):
                result, calls = self.resolve(paper(statement + "https://github.com/\nowner/study.",
                                                  ["https://github.com/owner/study"]))
                self.assertEqual(result["status"], "not_found")
                self.assertFalse(calls)

    def test_duplicate_annotations_preserve_one_supported_raw_context(self):
        full = "https://github.com/owner/study"
        result, calls = self.resolve(paper("Code is publicly available at https://github.com/\nowner/study.", [full, full]))
        self.assertEqual(result["status"], "selected")
        self.assertEqual(len(calls), 1)
        supported = [item for item in result["evidence"] if item["association"] == "code_availability_with_same_page_annotation"]
        self.assertEqual(len(supported), 1)

    def test_blank_paragraphs_cannot_join_host_or_availability(self):
        for text in ("Our code is available at https://github.com/\n\nowner/study.",
                     "Our code is available at https://github.com/\n \nowner/study.",
                     "Our code is available at https://github.com/\r\n\r\nowner/study.",
                     "Our code is available at\n\nhttps://github.com/\nowner/study."):
            with self.subTest(text=text):
                result, calls = self.resolve(paper(text, ["https://github.com/owner/study"]))
                self.assertEqual(result["status"], "not_found")
                self.assertFalse(calls)

    def test_ambiguous_annotation_completions_do_not_fill_a_partial_next_line(self):
        for text in ("Code is publicly available at https://github.com/\nowner/",
                     "Code is publicly available at https://github.com/\nowner/stu"):
            with self.subTest(text=text):
                result, calls = self.resolve(paper(text, ["https://github.com/owner/study", "https://github.com/owner/student"]))
                self.assertEqual(result["status"], "not_found")
                self.assertFalse(calls)

    def test_two_explicit_host_wrapped_links_stay_ambiguous(self):
        text = ("Our code is publicly available at https://github.com/\nowner/study.\n\n"
                "Our implementation is publicly available at https://github.com/\nowner/other.")
        result, calls = self.resolve(paper(text, ["https://github.com/owner/study", "https://github.com/owner/other"]))
        self.assertEqual(result["status"], "ambiguous")
        self.assertFalse(calls)


if __name__ == "__main__":
    unittest.main()
