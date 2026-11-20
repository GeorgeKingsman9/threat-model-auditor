"""Offline source discovery: self-association and immutable resolution are distinct."""

import io
import json
import unittest
from unittest.mock import patch

import source_discovery as discovery


COMMIT = "1" * 40
OLDER = "2" * 40


def paper(text, links=None, **extra):
    return {"source": "paper.pdf", "sha256": "a" * 64, "text": text,
            "segments": [{"id": "p1", "text": text}], "links": links or [], **extra}


def api_bytes(repo="owner/study", sha=COMMIT):
    return json.dumps({"sha": sha, "html_url": f"https://github.com/{repo}/commit/{sha}"}).encode()


class SourceDiscoveryTests(unittest.TestCase):
    def resolve(self, document, source="paper.pdf", responses=None):
        calls = []

        def fetch(fetcher, url, accept=None):
            calls.append(url)
            value = (responses or {}).get(url)
            if isinstance(value, Exception):
                raise value
            if value is not None:
                return value, url
            if url.startswith("https://api.github.com/repos/"):
                repository = url.split("/repos/", 1)[1].split("/commits/", 1)[0]
                return api_bytes(repository), url
            raise discovery.DiscoveryError("fixture endpoint unavailable")

        with patch.object(discovery._Fetcher, "fetch", new=fetch):
            result = discovery.discover_repository(document, source)
        return result, calls

    def test_explicit_paper_code_statement_selects_and_freezes_only_the_associated_repo(self):
        text = ("We compare the baseline https://github.com/other/baseline. "
                "For reproducibility, our data and source code are available at https://github.com/owner/study.")
        result, calls = self.resolve(paper(text))
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["repository"], "https://github.com/owner/study")
        self.assertEqual(result["revision"], COMMIT)
        self.assertEqual(calls, ["https://api.github.com/repos/owner/study/commits/HEAD"])
        self.assertEqual(len(result["candidates"]), 2)
        self.assertFalse(next(c for c in result["candidates"] if c["repository"].endswith("baseline"))["accepted"])
        self.assertIn("our data and source code", result["evidence"][0]["context"])

    def test_reference_or_dependency_links_do_not_imply_our_official_code(self):
        for text in ["References: https://github.com/other/baseline",
                     "We use a baseline whose source code is available at https://github.com/other/baseline.",
                     "Our paper improves the library. Its source code is available at https://github.com/other/baseline."]:
            with self.subTest(text=text):
                result, calls = self.resolve(paper(text, ["https://github.com/other/baseline"]))
                self.assertEqual(result["status"], "not_found")
                self.assertFalse(calls)
                self.assertFalse(result["candidates"][0]["accepted"])

    def test_two_self_associated_repositories_are_ambiguous_without_trying_to_pick_a_label(self):
        text = ("Our code is available at https://github.com/owner/attack.\n\n"
                "Our implementation is released at https://github.com/owner/framework.")
        result, calls = self.resolve(paper(text))
        self.assertEqual(result["status"], "ambiguous")
        self.assertIsNone(result["repository"])
        self.assertFalse(calls)

    def test_unassociated_pinned_reference_does_not_override_associated_head(self):
        text = (f"References https://github.com/owner/study/tree/{OLDER}.\n\n"
                "Our source code is available at https://github.com/owner/study.")
        result, calls = self.resolve(paper(text))
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["revision"], COMMIT)
        self.assertEqual(calls[-1], "https://api.github.com/repos/owner/study/commits/HEAD")

    def test_explicit_full_commit_is_verified_and_conflicting_versions_stay_ambiguous(self):
        text = f"Our code is available at https://github.com/owner/study/tree/{COMMIT}."
        result, calls = self.resolve(paper(text))
        self.assertEqual(result["revision"], COMMIT)
        self.assertTrue(calls[0].endswith(COMMIT))
        text += f"\n\nOur code is available at https://github.com/owner/study/tree/{OLDER}."
        result, calls = self.resolve(paper(text))
        self.assertEqual(result["status"], "ambiguous")
        self.assertFalse(calls)

    def test_original_landing_page_code_anchor_can_nominate_a_repository(self):
        document = paper("Paper body", link_contexts=[{
            "url": "https://github.com/owner/study", "text": "Title Code PDF", "anchor_text": "Code", "source": "landing_page",
        }])
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["evidence"][0]["association"], "code_anchor")

    def test_unlabelled_pdf_annotation_uri_is_not_ownership_evidence(self):
        document = paper("We discuss prior work.", links=["https://github.com/owner/study"], link_contexts=[{
            "url": "https://github.com/owner/study", "text": "", "source": "pdf_annotation", "segment_id": "p1",
        }])
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "not_found")
        self.assertFalse(calls)

    def test_same_page_annotation_can_complete_a_code_associated_visible_url_fragment(self):
        document = paper("Our source code is available at https://github.com/own\nA following line.", link_contexts=[{
            "url": "https://github.com/owner/study", "text": "", "source": "pdf_annotation", "segment_id": "p1",
        }])
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["repository"], "https://github.com/owner/study")
        evidence = result["evidence"][0]
        self.assertEqual(evidence["association"], "code_availability_with_same_page_annotation")
        self.assertEqual(evidence["visible_url_fragment"], "https://github.com/own")
        self.assertEqual(evidence["annotation_url"], "https://github.com/owner/study")
        document["link_contexts"][0]["segment_id"] = "p2"
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "not_found")
        self.assertFalse(calls)

    def test_multiple_annotation_completions_stay_ambiguous(self):
        document = paper("Code is available at https://github.com/owner/stu\n", link_contexts=[
            {"url": f"https://github.com/owner/{repo}", "source": "pdf_annotation", "segment_id": "p1", "text": ""}
            for repo in ("study", "student")
        ])
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "ambiguous")
        self.assertFalse(calls)

    def test_metadata_cannot_switch_the_paper_associated_repository_or_hide_commit_url(self):
        document = paper("Code: https://github.com/owner/study.")
        endpoint = "https://api.github.com/repos/owner/study/commits/HEAD"
        for response in [api_bytes("other/unrelated"), json.dumps({"sha": COMMIT}).encode(),
                         json.dumps({"sha": COMMIT, "html_url": "https://example.org/commit/" + COMMIT}).encode()]:
            with self.subTest(response=response):
                result, _ = self.resolve(document, responses={endpoint: response})
                self.assertEqual(result["status"], "unavailable")
                self.assertIsNone(result["repository"])

    def test_named_baseline_code_availability_is_not_self_association(self):
        result, calls = self.resolve(paper("Baseline X code is available at https://github.com/other/baseline."))
        self.assertEqual(result["status"], "not_found")
        self.assertFalse(calls)

    def test_reading_order_recovers_a_url_split_by_the_layout_view(self):
        document = paper("Our source code is available at https://github.com/owner/\nstudy")
        document["segments"][0]["reading_order_text"] = "Our source code is available at https://github.com/owner/study."
        result, calls = self.resolve(document)
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["evidence"][0]["text_view"], "reading_order_text")

    def test_linked_project_page_is_followed_but_its_reference_link_is_not_chosen(self):
        text = "Our project page is at https://research.example/study."
        html = (b"<html><p>Study project</p><a href='https://github.com/owner/study'>Code</a>"
                b"<p>Related work <a href='https://github.com/other/baseline'>Reference</a></p></html>")
        result, calls = self.resolve(paper(text), responses={"https://research.example/study": html})
        self.assertEqual(result["status"], "selected")
        self.assertEqual(result["repository"], "https://github.com/owner/study")
        self.assertEqual(calls[0], "https://research.example/study")
        self.assertFalse(any("other/baseline/commits" in call for call in calls))

    def test_arxiv_html_is_a_bounded_same_paper_fallback_for_missing_pdf_link_text(self):
        url = "https://arxiv.org/html/1234.56789v2"
        html = b"<html><p>Our code is available at <a href='https://github.com/owner/study'>this repository</a>.</p></html>"
        result, calls = self.resolve(paper("Paper body without visible URL"), "https://arxiv.org/pdf/1234.56789v2", {url: html})
        self.assertEqual(result["status"], "selected")
        self.assertEqual(calls[0], url)
        self.assertEqual(len(calls), 2)

    def test_repository_resolution_failure_is_unavailable_not_a_guessed_revision(self):
        document = paper("Code: https://github.com/owner/study.")
        for response in [discovery.DiscoveryError("rate limit"), b'{}', api_bytes(sha="short")]:
            with self.subTest(response=response):
                result, _ = self.resolve(document, responses={"https://api.github.com/repos/owner/study/commits/HEAD": response})
                self.assertEqual(result["status"], "unavailable")
                self.assertIsNone(result["revision"])
                self.assertTrue(result["evidence"])

    def test_fetcher_rejects_private_urls_and_over_budget_without_reading_any_response(self):
        fetcher = discovery._Fetcher()
        with patch.object(discovery, "_validate_url", side_effect=discovery.DocumentError("private")), patch.object(discovery, "build_opener") as opener:
            with self.assertRaises(discovery.DocumentError):
                fetcher.fetch("https://localhost/internal")
            opener.assert_not_called()
        fetcher.requests = [{}] * discovery.MAX_REQUESTS
        with patch.object(discovery, "build_opener") as opener:
            with self.assertRaisesRegex(discovery.DiscoveryError, "budget"):
                fetcher.fetch("https://example.org")
            opener.assert_not_called()

    def test_redirect_safety_and_response_byte_limit_are_checked(self):
        class Response(io.BytesIO):
            headers = {"Content-Length": str(discovery.MAX_PAGE_BYTES + 1)}
            def geturl(self):
                return "https://example.org/project"
        class Opener:
            def open(self, *args, **kwargs):
                return Response(b"html")
        with patch.object(discovery, "_validate_url"), patch.object(discovery, "build_opener", return_value=Opener()):
            with self.assertRaisesRegex(discovery.DiscoveryError, "byte limit"):
                discovery._Fetcher().fetch("https://example.org/project")
        fetcher = discovery._Fetcher()
        handler = discovery._Redirect(fetcher)
        with patch.object(discovery, "_validate_url", side_effect=discovery.DocumentError("private redirect")):
            with self.assertRaises(discovery.DocumentError):
                handler.redirect_request(None, None, 302, "", {}, "http://127.0.0.1/secret")


if __name__ == "__main__":
    unittest.main()
