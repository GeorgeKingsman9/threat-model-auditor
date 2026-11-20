"""Preserve discovery links without mixing landing-page text into paper evidence."""

from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import documents


class DocumentDiscoveryLinkTests(unittest.TestCase):
    def test_pdf_annotations_preserve_page_and_uri_without_fetching(self):
        def inspect(command, **kwargs):
            self.assertEqual(command, ["pdfinfo", "-url", "-"])
            self.assertEqual(kwargs["input"], b"%PDF-fixture")
            self.assertNotIn("shell", kwargs)
            kwargs["stdout"].write(
                b"Page  Type          URL\n"
                b"  3   Annotation    https://github.com/example/full-repository\n"
                b"  4   Annotation    javascript:alert(1)\n"
            )
            return SimpleNamespace(returncode=0)

        with patch.object(documents.subprocess, "run", side_effect=inspect), \
                patch.object(documents, "_fetch_url", side_effect=AssertionError("Do not visit annotations")):
            links, status = documents._pdf_annotation_links(b"%PDF-fixture")
        self.assertEqual(status["status"], "completed")
        self.assertEqual(links, [{"url": "https://github.com/example/full-repository",
                                  "source": "pdf_annotation", "segment_id": "p3", "text": ""}])

    def test_landing_code_anchor_survives_pdf_follow_without_becoming_paper_text(self):
        page = (
            b'<html><p>Our implementation: <a href="https://github.com/author/project">Code</a>.</p>'
            b'<meta name="citation_pdf_url" content="/paper.pdf"></html>'
        )
        responses = [(page, "https://example.org/project", "text/html"),
                     (b"%PDF-fixture", "https://example.org/paper.pdf", "application/pdf")]
        with patch.object(documents, "_validate_url"), \
                patch.object(documents, "_fetch_url", side_effect=responses), \
                patch.object(documents, "pdf_text_views", return_value=[{"id": "p1", "text": "Actual paper body"}]), \
                patch.object(documents, "_pdf_annotation_links", return_value=([], {"status": "completed"})):
            document = documents.load_document("https://example.org/project")
        self.assertEqual(document["text"], "Actual paper body")
        self.assertEqual(document["segments"], [{"id": "p1", "text": "Actual paper body"}])
        context = next(c for c in document["link_contexts"] if c["url"] == "https://github.com/author/project")
        self.assertIn("Our implementation", context["text"])
        self.assertEqual(context["anchor_text"], "Code")
        self.assertEqual(context["source"], "landing_page")

    def test_annotation_tool_missing_does_not_destroy_readable_pdf_body(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.pdf"
            path.write_bytes(b"%PDF-fixture")
            with patch.object(documents.subprocess, "run", side_effect=FileNotFoundError), \
                    patch.object(documents, "pdf_text_views", return_value=[{"id": "p1", "text": "Readable body"}]):
                document = documents.load_document(str(path))
        self.assertEqual(document["text"], "Readable body")
        self.assertEqual(document["pdf_link_extraction"]["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
