"""Offline document-reader checks; no live HTTP or model requests."""

import hashlib
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import documents


class DocumentTests(unittest.TestCase):
    def local_document(self, name, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / name
        path.write_bytes(data)
        return path

    def test_local_text_hides_directory_and_hashes_original_bytes(self):
        data = "论文正文\nhttps://example.org/paper\n".encode()
        path = self.local_document("paper.txt", data)
        result = documents.load_document(str(path))
        self.assertEqual(result["source"], "paper.txt")
        self.assertNotIn(str(path.parent), str(result))
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(result["segments"], [{"id": "s1", "text": data.decode().strip()}])
        self.assertTrue(result["coverage"]["complete"])
        self.assertEqual(result["links"], ["https://example.org/paper"])

    def test_html_removes_code_and_does_not_claim_complete_paper(self):
        data = b'<html><head><style>secret style</style></head><body><h1>Paper</h1><script>secret script</script><p>Threat <b>model</b>.</p><a href="https://example.org/source">Source</a></body></html>'
        path = self.local_document("paper.html", data)
        result = documents.load_document(str(path))
        self.assertEqual(result["media_type"], "text/html")
        self.assertIn("Threat model.", result["text"])
        self.assertNotIn("secret", result["text"])
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["links"], ["https://example.org/source"])

    def test_arxiv_abstract_converts_to_pdf_and_keeps_pages(self):
        views = [{"id": "p1", "text": "First page"}, {"id": "p2", "text": "Second page"}]
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", return_value=(b"%PDF-test", "https://arxiv.org/pdf/1234.56789v2", "application/pdf")) as fetch, patch.object(documents, "pdf_text_views", return_value=views):
            result = documents.load_document("https://arxiv.org/abs/1234.56789v2")
        fetch.assert_called_once_with("https://arxiv.org/pdf/1234.56789v2")
        self.assertEqual([part["id"] for part in result["segments"]], ["p1", "p2"])
        self.assertTrue(result["coverage"]["complete"])

    def test_landing_page_follows_one_citation_pdf_url(self):
        page = b'<html><head><meta name="citation_pdf_url" content="/paper.pdf"></head><body>Abstract</body></html>'
        responses = [(page, "https://example.org/landing", "text/html"), (b"%PDF-test", "https://example.org/paper.pdf", "application/pdf")]
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", side_effect=responses) as fetch, patch.object(documents, "pdf_text_views", return_value=[{"id": "p1", "text": "Full paper"}]):
            result = documents.load_document("https://example.org/landing")
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(fetch.call_args.args, ("https://example.org/paper.pdf",))
        self.assertEqual(result["sha256"], hashlib.sha256(b"%PDF-test").hexdigest())
        self.assertEqual(result["source"], "https://example.org/paper.pdf")

    def test_landing_page_accepts_pdf_link_class(self):
        page = b'<html><a class="download pdf_link" href="/download/123">Download</a></html>'
        responses = [(page, "https://example.org/landing", "text/html"), (b"%PDF-test", "https://example.org/download/123", "application/pdf")]
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", side_effect=responses) as fetch, patch.object(documents, "pdf_text_views", return_value=[{"id": "p1", "text": "Full paper"}]):
            documents.load_document("https://example.org/landing")
        self.assertEqual(fetch.call_args.args, ("https://example.org/download/123",))

    def test_does_not_recursively_follow_landing_pages(self):
        page = b'<html><a class="pdf_link" href="/next">PDF</a></html>'
        responses = [(page, "https://example.org/landing", "text/html"), (page, "https://example.org/next", "text/html")]
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", side_effect=responses) as fetch:
            with self.assertRaisesRegex(documents.DocumentError, "did not return a PDF"):
                documents.load_document("https://example.org/landing")
        self.assertEqual(fetch.call_count, 2)

    def test_openreview_challenge_redirect_is_not_paper_text(self):
        page = b'<html><h1>OpenReview</h1><p>Please continue to the requested resource.</p></html>'
        response = (page, "https://openreview.net/challenge?redirect=%2Fpdf%3Fid%3Dtest", "text/html")
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", return_value=response):
            with self.assertRaisesRegex(documents.DocumentError, "challenge page, not paper body text"):
                documents.load_document("https://openreview.net/pdf?id=test")

    def test_short_browser_verification_page_is_rejected_without_special_route(self):
        page = b'<html><title>Just a moment...</title><p>Checking your browser before accessing the paper.</p></html>'
        response = (page, "https://example.org/paper", "text/html")
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", return_value=response):
            with self.assertRaisesRegex(documents.DocumentError, "challenge page"):
                documents.load_document("https://example.org/paper")

    def test_linked_pdf_returning_challenge_gives_specific_diagnostic(self):
        page = b'<html><meta name="citation_pdf_url" content="/paper.pdf"><p>Abstract</p></html>'
        challenge = b'<html><p>Verify you are human to continue.</p></html>'
        responses = [(page, "https://example.org/landing", "text/html"), (challenge, "https://example.org/challenge", "text/html")]
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", side_effect=responses):
            with self.assertRaisesRegex(documents.DocumentError, "challenge page"):
                documents.load_document("https://example.org/landing")

    def test_normal_html_abstract_discussing_human_verification_remains_partial(self):
        page = b'<html><h1>Research on CAPTCHA challenges</h1><p>Abstract: We study prompts saying verify you are human.</p></html>'
        response = (page, "https://example.org/papers/challenges", "text/html")
        with patch.object(documents, "_validate_url"), patch.object(documents, "_fetch_url", return_value=response):
            result = documents.load_document("https://example.org/papers/challenges")
        self.assertIn("Abstract:", result["text"])
        self.assertFalse(result["coverage"]["complete"])

    def test_saved_local_access_gate_is_rejected_by_its_heading(self):
        path = self.local_document("saved.html", b'<html><h1>Access denied</h1><p>Please complete the security check.</p></html>')
        with self.assertRaisesRegex(documents.DocumentError, "not paper body text"):
            documents.load_document(str(path))

    def test_textless_pdf_requires_ocr_instead_of_succeeding(self):
        path = self.local_document("scan.pdf", b"%PDF-test")
        views = [{"id": "p1", "text": ""}, {"id": "p2", "text": ""}]
        with patch.object(documents, "pdf_text_views", return_value=views):
            with self.assertRaisesRegex(documents.DocumentError, "OCR is not provided"):
                documents.load_document(str(path))

    def test_partial_pdf_preserves_empty_page_and_marks_incomplete(self):
        path = self.local_document("mixed.pdf", b"%PDF-test")
        views = [{"id": "p1", "text": "Text"}, {"id": "p2", "text": ""}, {"id": "p3", "text": "More text"}]
        with patch.object(documents, "pdf_text_views", return_value=views):
            result = documents.load_document(str(path))
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["segments"][1], {"id": "p2", "text": ""})

    def test_pdftotext_uses_layout_without_shell_and_preserves_blank_page(self):
        def extract(command, **kwargs):
            self.assertEqual(command[:5], ["pdftotext", "-layout", "-enc", "UTF-8", "-"])
            self.assertEqual(kwargs["input"], b"%PDF-test")
            self.assertEqual(kwargs["timeout"], documents.TIMEOUT_SECONDS)
            self.assertNotIn("shell", kwargs)
            Path(command[-1]).write_bytes(b"First page\f\f")
            return SimpleNamespace(returncode=0)
        with patch.object(documents.subprocess, "run", side_effect=extract):
            self.assertEqual(documents._pdf_pages(b"%PDF-test"), ["First page", ""])

    def test_two_column_reading_order_preserves_primary_text_and_original_hash(self):
        data = b"%PDF-two-column-test"
        path = self.local_document("columns.pdf", data)
        layout_pages = [
            "The attacker cannot access   Right column begins.\nthe exact document.          Other research.",
            "Second page layout.",
        ]
        reading_pages = [
            "The attacker cannot access the exact document.\nRight column begins. Other research.",
            "Second page reading order.",
        ]
        calls = []

        def extract(command, **kwargs):
            self.assertEqual(kwargs["input"], data)
            self.assertNotIn("shell", kwargs)
            self.assertEqual(kwargs["timeout"], documents.TIMEOUT_SECONDS)
            calls.append(command[:-1])
            pages = layout_pages if "-layout" in command else reading_pages
            Path(command[-1]).write_text("\f".join(pages) + "\f", encoding="utf-8")
            return SimpleNamespace(returncode=0)

        with patch.object(documents.subprocess, "run", side_effect=extract):
            result = documents.load_document(str(path))
        self.assertEqual(calls, [
            ["pdftotext", "-layout", "-enc", "UTF-8", "-"],
            ["pdftotext", "-enc", "UTF-8", "-"],
        ])
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(result["text"], "\n\n".join(layout_pages))
        self.assertEqual([segment["text"] for segment in result["segments"]], layout_pages)
        self.assertEqual([segment["reading_order_text"] for segment in result["segments"]], reading_pages)
        self.assertEqual([segment["id"] for segment in result["segments"]], ["p1", "p2"])
        self.assertTrue(result["coverage"]["complete"])
        for segment in result["segments"]:
            self.assertEqual(segment["source_extraction_version"], "pdftotext-reading-order-v1")
        quote = "The attacker cannot access the exact document."
        self.assertIn(quote, result["segments"][0]["reading_order_text"])
        self.assertNotIn(quote, result["segments"][0]["text"])

    def test_page_count_mismatch_discards_alternate_view_for_every_page(self):
        path = self.local_document("mismatch.pdf", b"%PDF-test")
        for reading_text in ("Only one page\f", "One\fTwo\fThree\f"):
            with self.subTest(reading_text=reading_text):
                def extract(command, **kwargs):
                    text = "First layout\fSecond layout\f" if "-layout" in command else reading_text
                    Path(command[-1]).write_text(text, encoding="utf-8")
                    return SimpleNamespace(returncode=0)

                with patch.object(documents.subprocess, "run", side_effect=extract):
                    result = documents.load_document(str(path))
                self.assertEqual(result["text"], "First layout\n\nSecond layout")
                self.assertEqual(result["segments"], [
                    {"id": "p1", "text": "First layout"},
                    {"id": "p2", "text": "Second layout"},
                ])

    def test_pdf_views_keep_blank_page_alignment(self):
        def extract(command, **kwargs):
            text = "First layout\f\fLast layout\f" if "-layout" in command else "First reading\f\fLast reading\f"
            Path(command[-1]).write_text(text, encoding="utf-8")
            return SimpleNamespace(returncode=0)

        with patch.object(documents.subprocess, "run", side_effect=extract):
            views = documents.pdf_text_views(b"%PDF-test")
        self.assertEqual([view["id"] for view in views], ["p1", "p2", "p3"])
        self.assertEqual(views[1]["text"], "")
        self.assertEqual(views[1]["layout_text"], "")
        self.assertEqual(views[2]["text"], "Last reading")

    def test_missing_poppler_returns_only_the_existing_fallback_text(self):
        fake = SimpleNamespace(PdfReader=lambda stream: SimpleNamespace(pages=[SimpleNamespace(extract_text=lambda: "Fallback page")]))
        with patch.object(documents.subprocess, "run", side_effect=FileNotFoundError) as run, patch.object(documents.importlib, "import_module", return_value=fake):
            views = documents.pdf_text_views(b"%PDF-test")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(views, [{"id": "p1", "text": "Fallback page"}])

    def test_alternate_extraction_failure_preserves_valid_layout_text(self):
        for failure in ("nonzero", "timeout"):
            with self.subTest(failure=failure):
                def extract(command, **kwargs):
                    if "-layout" in command:
                        Path(command[-1]).write_text("Original layout\f", encoding="utf-8")
                        return SimpleNamespace(returncode=0)
                    if failure == "timeout":
                        raise subprocess.TimeoutExpired("pdftotext", 30)
                    return SimpleNamespace(returncode=1)

                with patch.object(documents.subprocess, "run", side_effect=extract):
                    views = documents.pdf_text_views(b"%PDF-test")
                self.assertEqual(views, [{"id": "p1", "text": "Original layout"}])

    def test_reading_view_does_not_override_the_primary_ocr_requirement(self):
        path = self.local_document("empty-layout.pdf", b"%PDF-test")
        views = [{
            "id": "p1", "text": "Alternate extraction text", "layout_text": "",
            "source_extraction_version": "pdftotext-reading-order-v1",
        }]
        with patch.object(documents, "pdf_text_views", return_value=views):
            with self.assertRaisesRegex(documents.DocumentError, "OCR is not provided"):
                documents.load_document(str(path))

    def test_pdf_falls_back_to_optional_pypdf(self):
        fake = SimpleNamespace(PdfReader=lambda stream: SimpleNamespace(pages=[SimpleNamespace(extract_text=lambda: "Fallback page")]))
        with patch.object(documents.subprocess, "run", side_effect=FileNotFoundError), patch.object(documents.importlib, "import_module", return_value=fake):
            self.assertEqual(documents._pdf_pages(b"%PDF-test"), ["Fallback page"])

    def test_missing_pdf_tools_gives_actionable_error(self):
        with patch.object(documents.subprocess, "run", side_effect=FileNotFoundError), patch.object(documents.importlib, "import_module", side_effect=ImportError):
            with self.assertRaisesRegex(documents.DocumentError, "requires pdftotext"):
                documents._pdf_pages(b"%PDF-test")

    def test_pdf_extraction_timeout_is_reported(self):
        with patch.object(documents.subprocess, "run", side_effect=subprocess.TimeoutExpired("pdftotext", 30)):
            with self.assertRaisesRegex(documents.DocumentError, "timed out"):
                documents._pdf_pages(b"%PDF-test")

    def test_oversized_local_input_is_rejected(self):
        path = self.local_document("large.txt", b"123456")
        with patch.object(documents, "MAX_BYTES", 5):
            with self.assertRaisesRegex(documents.DocumentError, "size limit"):
                documents.load_document(str(path))

    def test_empty_binary_and_false_pdf_inputs_are_rejected(self):
        for name, data in [("empty.txt", b""), ("binary.txt", b"a\x00b"), ("false.pdf", b"not a PDF")]:
            with self.subTest(name=name):
                path = self.local_document(name, data)
                with self.assertRaises(documents.DocumentError):
                    documents.load_document(str(path))

    def test_invalid_utf8_does_not_claim_full_coverage(self):
        path = self.local_document("broken.txt", b"Text \xff")
        self.assertFalse(documents.load_document(str(path))["coverage"]["complete"])

    def test_rejects_internal_urls_credentials_and_other_protocols(self):
        for url in ["http://127.0.0.1/a.pdf", "http://[::1]/a.pdf", "http://169.254.169.254/a", "http://10.0.0.1/a", "http://localhost/a", "http://host.local/a", "https://user:secret@example.org/a", "file:///etc/passwd", "ftp://example.org/paper.pdf"]:
            with self.subTest(url=url):
                with self.assertRaises(documents.DocumentError):
                    documents.load_document(url)

    def test_dns_private_or_mixed_answer_is_rejected(self):
        public = (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        private = (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.168.1.1", 443))
        for records in [[private], [public, private]]:
            with patch.object(documents.socket, "getaddrinfo", return_value=records):
                with self.assertRaisesRegex(documents.DocumentError, "nonpublic"):
                    documents._validate_url("https://example.org/paper.pdf")

    def test_public_dns_is_accepted(self):
        record = (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        with patch.object(documents.socket, "getaddrinfo", return_value=[record]):
            documents._validate_url("https://example.org/paper.pdf")

    def test_redirect_to_internal_url_is_rejected_before_following(self):
        handler = documents._SafeRedirectHandler()
        with self.assertRaisesRegex(documents.DocumentError, "nonpublic"):
            handler.redirect_request(None, None, 302, "Found", {}, "http://127.0.0.1/private.pdf")

    def test_fetch_enforces_response_size_without_content_length(self):
        class Response:
            headers = {"Content-Type": "text/plain"}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def geturl(self): return "https://example.org/paper.txt"
            def read(self, length): return b"x" * length
        opener = SimpleNamespace(open=lambda *args, **kwargs: Response())
        with patch.object(documents, "_validate_url"), patch.object(documents, "build_opener", return_value=opener), patch.object(documents, "MAX_BYTES", 8):
            with self.assertRaisesRegex(documents.DocumentError, "size limit"):
                documents._fetch_url("https://example.org/paper.txt")


if __name__ == "__main__":
    unittest.main()
