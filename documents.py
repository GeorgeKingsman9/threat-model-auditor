"""Read paper documents as data; never execute document or repository content.

The standard library handles HTML and text. PDFs require the ``pdftotext``
executable or the optional ``pypdf`` package. This module performs no OCR.
"""

from __future__ import annotations

import hashlib
import importlib
import io
import ipaddress
import re
import socket
import subprocess
import tempfile
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_BYTES = 20 * 1024 * 1024
TIMEOUT_SECONDS = 30
MAX_REDIRECTS = 5
_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")
_CODE_SUFFIXES = {".py", ".js", ".ts", ".sh", ".bash", ".zip", ".gz", ".tar", ".exe"}


class DocumentError(ValueError):
    """A document could not be safely loaded or its text extracted."""


def _http_link(value: str, base: str = "") -> str | None:
    """Resolve an HTTP link without fetching or performing DNS requests."""
    try:
        link = urljoin(base, value)
        parts = urlsplit(link)
        if (
            parts.scheme.lower() not in {"http", "https"}
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
            or any(ord(char) < 32 or ord(char) == 127 for char in link)
        ):
            return None
        return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
    except ValueError:
        return None


def _unique_links(values: list[str]) -> list[str]:
    return list(dict.fromkeys(link for value in values if (link := _http_link(value))))


def _validate_url(url: str) -> None:
    """Reject credentials and nonpublic addresses, including DNS resolutions.

    This is an accidental-request guard, not a DNS-rebinding-proof network
    sandbox. Every redirect and followed PDF link is checked separately.
    """
    if not _http_link(url):
        raise DocumentError("Document URLs must use HTTP(S), without credentials or control characters")
    try:
        parts = urlsplit(url)
        host = parts.hostname.rstrip(".")
        port = parts.port or (443 if parts.scheme.lower() == "https" else 80)
    except (AttributeError, ValueError) as error:
        raise DocumentError("Invalid document URL") from error
    if host.lower() == "localhost" or host.lower().endswith((".localhost", ".local", ".internal")):
        raise DocumentError("Local or internal document URLs are not allowed")
    if Path(parts.path).suffix.lower() in _CODE_SUFFIXES:
        raise DocumentError("Provide a paper PDF, HTML, or text document, not source code or an archive")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        try:
            addresses = {
                entry[4][0]
                for entry in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
            }
        except OSError as error:
            raise DocumentError("Could not resolve the document host") from error
    else:
        addresses = {str(address)}
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise DocumentError("Local, private, or otherwise nonpublic document addresses are not allowed")


class _SafeRedirectHandler(HTTPRedirectHandler):
    max_redirections = MAX_REDIRECTS

    def redirect_request(self, request, response, code, message, headers, newurl):
        _validate_url(newurl)
        return super().redirect_request(request, response, code, message, headers, newurl)


def _fetch_url(url: str) -> tuple[bytes, str, str]:
    _validate_url(url)
    opener = build_opener(_SafeRedirectHandler())
    request = Request(url, headers={
        "User-Agent": "ThreatModelAuditor/0.1 (paper text reader)",
        "Accept": "application/pdf,text/html,text/plain;q=0.9",
        "Accept-Encoding": "identity",
    })
    started = time.monotonic()
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            final_url = response.geturl()
            _validate_url(final_url)
            length = response.headers.get("Content-Length")
            if length and length.isdigit() and int(length) > MAX_BYTES:
                raise DocumentError("Document exceeds the 20 MiB size limit")
            chunks = []
            size = 0
            while True:
                if time.monotonic() - started > TIMEOUT_SECONDS:
                    raise DocumentError("Document download timed out")
                chunk = response.read(min(65536, MAX_BYTES + 1 - size))
                if not chunk:
                    break
                chunks.append(chunk)
                size += len(chunk)
                if size > MAX_BYTES:
                    raise DocumentError("Document exceeds the 20 MiB size limit")
            media_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            return b"".join(chunks), final_url, media_type
    except (HTTPError, URLError, OSError, TimeoutError) as error:
        raise DocumentError("Could not download the paper document") from error


def _arxiv_pdf_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.hostname in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"} and parts.path.startswith("/abs/"):
        return urlunsplit((parts.scheme, parts.netloc, "/pdf/" + parts.path[5:], "", ""))
    return url


class _PaperHTML(HTMLParser):
    _EXCLUDED = {"script", "style", "noscript", "template", "svg"}
    _BREAKS = {"p", "div", "section", "article", "main", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.parts: list[str] = []
        self.links: list[str] = []
        self.pdf_meta: list[str] = []
        self.pdf_anchors: list[str] = []
        self._excluded: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self._excluded:
            if tag in self._EXCLUDED:
                self._excluded.append(tag)
            return
        if tag in self._EXCLUDED:
            self._excluded.append(tag)
            return
        if tag in self._BREAKS:
            self.parts.append("\n")
        if tag == "a" and attrs.get("href"):
            link = _http_link(attrs["href"], self.base)
            if link:
                self.links.append(link)
                classes = (attrs.get("class") or "").split()
                if (
                    "pdf_link" in classes
                    or attrs.get("id") == "pdf_link"
                    or urlsplit(link).path.lower().endswith(".pdf")
                ):
                    self.pdf_anchors.append(link)
        if tag == "meta" and (attrs.get("name") or attrs.get("property") or "").lower() == "citation_pdf_url":
            link = _http_link(attrs.get("content") or "", self.base)
            if link:
                self.pdf_meta.append(link)
                self.links.append(link)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self._EXCLUDED:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self._excluded:
            if tag == self._excluded[-1]:
                self._excluded.pop()
            return
        if tag in self._BREAKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._excluded:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line).strip()


def _pdftotext_pages(data: bytes, *, layout: bool) -> list[str] | None:
    """Return one Poppler extraction, or None when it is unavailable."""
    try:
        with tempfile.TemporaryDirectory(prefix="paper-text-") as directory:
            output = Path(directory) / "extracted.txt"
            command = ["pdftotext"]
            if layout:
                command.append("-layout")
            command.extend(["-enc", "UTF-8", "-", str(output)])
            result = subprocess.run(
                command,
                input=data, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                timeout=TIMEOUT_SECONDS, check=False,
            )
            if result.returncode == 0:
                with output.open("rb") as stream:
                    extracted = stream.read(MAX_BYTES + 1)
                if len(extracted) > MAX_BYTES:
                    raise DocumentError("Extracted text exceeds the 20 MiB size limit")
                pages = extracted.decode("utf-8", errors="replace").split("\f")
                # pdftotext emits one terminal form feed; preserve real blank pages.
                if pages and not pages[-1].strip():
                    pages.pop()
                return [page.strip() for page in pages]
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired as error:
        raise DocumentError("PDF text extraction timed out") from error
    except OSError as error:
        raise DocumentError("Could not run PDF text extraction") from error
    return None


def _pypdf_pages(data: bytes) -> list[str]:
    try:
        pypdf = importlib.import_module("pypdf")
    except ImportError as error:
        raise DocumentError("PDF extraction requires pdftotext (Poppler) or optional pypdf") from error
    try:
        reader = pypdf.PdfReader(io.BytesIO(data))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except Exception as error:
        raise DocumentError("Could not extract text from this PDF") from error
    if sum(len(page.encode("utf-8")) for page in pages) > MAX_BYTES:
        raise DocumentError("Extracted text exceeds the 20 MiB size limit")
    return pages


def _pdf_pages(data: bytes) -> list[str]:
    """Preserve the original layout-first extraction for existing callers."""
    pages = _pdftotext_pages(data, layout=True)
    return pages if pages is not None else _pypdf_pages(data)


def pdf_text_views(data: bytes) -> list[dict[str, str]]:
    """Extract page-aligned layout and reading-order views from the same bytes.

    With both Poppler views available, ``text`` is its default reading order
    and ``layout_text`` preserves the original layout extraction. Otherwise
    only the original page text is returned. Alternate extraction failures
    and page-count differences leave that original view intact.
    """
    pages = _pdftotext_pages(data, layout=True)
    if pages is None:
        return [
            {"id": f"p{index}", "text": text}
            for index, text in enumerate(_pypdf_pages(data), 1)
        ]
    original = [
        {"id": f"p{index}", "text": text}
        for index, text in enumerate(pages, 1)
    ]
    try:
        reading_pages = _pdftotext_pages(data, layout=False)
    except DocumentError:
        return original
    if reading_pages is None or len(reading_pages) != len(pages):
        return original
    return [
        {
            "id": f"p{index}",
            "text": reading,
            "layout_text": layout,
            "source_extraction_version": "pdftotext-reading-order-v1",
        }
        for index, (layout, reading) in enumerate(zip(pages, reading_pages), 1)
    ]


def _decode_text(data: bytes) -> tuple[str, bool]:
    """Use BOM or declared HTML charset when present, otherwise UTF-8."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        encoding = "utf-16"
    else:
        match = re.search(br"charset\s*=\s*[\"']?([A-Za-z0-9_.-]+)", data[:4096], re.I)
        encoding = match.group(1).decode("ascii") if match else "utf-8-sig"
    try:
        return data.decode(encoding), True
    except (UnicodeError, LookupError):
        return data.decode("utf-8", errors="replace"), False


def _read_local(path: Path) -> bytes:
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
    except OSError as error:
        raise DocumentError(f"Could not read local document: {path.name}") from error
    if len(data) > MAX_BYTES:
        raise DocumentError("Document exceeds the 20 MiB size limit")
    return data


def _classify(data: bytes, hint: str, source: str) -> str:
    if data.lstrip().startswith(b"%PDF-"):
        return "application/pdf"
    if hint == "application/pdf" or Path(urlsplit(source).path).suffix.lower() == ".pdf":
        raise DocumentError("The document is labelled PDF but does not contain a PDF header")
    start = data[:1024].lstrip().lower()
    if hint in {"text/html", "application/xhtml+xml"} or start.startswith((b"<!doctype html", b"<html", b"<head", b"<body")):
        return "text/html"
    suffix = Path(urlsplit(source).path).suffix.lower()
    if hint == "text/plain" or suffix in {".txt", ".md", ".rst"}:
        if b"\x00" in data[:4096] and not data.startswith((b"\xff\xfe", b"\xfe\xff")):
            raise DocumentError("The text document appears to contain binary data")
        return "text/plain"
    if suffix in {".html", ".htm"}:
        return "text/html"
    raise DocumentError("Unsupported document format; provide PDF, HTML, or TXT")


def _reject_access_challenge(source: str, text: str) -> None:
    """Keep a recognisable access gate out of the paper-text audit input.

    Only explicit challenge routes or short pages headed by challenge wording
    are rejected. Ordinary HTML abstracts remain valid partial documents, and
    a paper discussing CAPTCHA or quoting verification text is not itself a
    challenge page.
    """
    parts = urlsplit(source)
    path = parts.path.lower().rstrip("/")
    challenge_route = parts.scheme.lower() in {"http", "https"} and (
        path == "/challenge"
        or path.startswith("/cdn-cgi/challenge-platform/")
        or path == "/cdn-cgi/l/chk_captcha"
    )
    compact = " ".join(text.lower().split())
    challenge_headings = (
        "verify you are human", "verify that you are human",
        "please verify you are human", "please verify that you are human",
        "checking your browser", "checking if the site connection is secure",
        "enable javascript and cookies to continue",
        "please complete the security check", "access denied",
    )
    challenge_message = len(compact) <= 4000 and compact.startswith(challenge_headings)
    if not challenge_message and len(compact) <= 4000 and compact.startswith(
        ("just a moment", "one more step", "security verification", "security check", "cloudflare")
    ):
        challenge_message = any(marker in compact for marker in challenge_headings)
    if challenge_route or challenge_message:
        raise DocumentError(
            "Received an access/security challenge page, not paper body text; "
            "provide an accessible PDF or a local document"
        )


def load_document(source: str) -> dict:
    """Load one local paper or public HTTP(S) paper URL.

    A landing page may lead to one PDF via citation_pdf_url or a PDF anchor.
    Returned SHA-256 hashes the actual document bytes, before text extraction.
    ``coverage.complete`` describes extraction coverage, not audit completeness
    or verification of the paper's claims. HTML cannot establish full-paper
    coverage and therefore has ``complete=False``.
    """
    if not isinstance(source, str) or not source.strip():
        raise DocumentError("Provide a nonempty local document path or HTTP(S) URL")
    source = source.strip()
    parts = urlsplit(source)
    is_url = parts.scheme.lower() in {"http", "https"}
    if parts.scheme and not is_url:
        raise DocumentError("Only HTTP(S) document URLs are supported")
    if is_url:
        # Validate before transforming, so credentials or invalid paths cannot
        # be hidden by conversion of an arXiv abstract URL.
        _validate_url(source)
        data, label, hint = _fetch_url(_arxiv_pdf_url(source))
    else:
        path = Path(source).expanduser()
        label = path.name
        data = _read_local(path)
        hint = ""
    if not data:
        raise DocumentError("The document is empty")
    if len(data) > MAX_BYTES:
        raise DocumentError("Document exceeds the 20 MiB size limit")
    media_type = _classify(data, hint, label)
    links: list[str] = []
    parser = None
    decoded = None
    decoded_cleanly = True
    if media_type == "text/html":
        decoded, decoded_cleanly = _decode_text(data)
        parser = _PaperHTML(label if is_url else "")
        parser.feed(decoded)
        _reject_access_challenge(label, parser.text())
        links.extend(parser.links)
        candidates = parser.pdf_meta + parser.pdf_anchors
        if is_url and candidates:
            # Exactly one landing-page-to-document hop; no recursive crawling.
            data, label, hint = _fetch_url(candidates[0])
            media_type = _classify(data, hint, label)
            if media_type != "application/pdf":
                if media_type == "text/html":
                    linked_parser = _PaperHTML(label)
                    linked_parser.feed(_decode_text(data)[0])
                    _reject_access_challenge(label, linked_parser.text())
                raise DocumentError("The landing-page PDF link did not return a PDF")
            links.append(label)

    if media_type == "application/pdf":
        views = pdf_text_views(data)
        segments = []
        for view in views:
            segment = {"id": view["id"], "text": view.get("layout_text", view["text"])}
            if "layout_text" in view:
                segment["reading_order_text"] = view["text"]
                segment["source_extraction_version"] = view["source_extraction_version"]
            segments.append(segment)
        pages = [segment["text"] for segment in segments]
        if not pages or not any(page.strip() for page in pages):
            raise DocumentError("PDF has no extractable text; OCR is not provided")
        complete = all(page.strip() for page in pages)
        reason = "Text extracted from every PDF page; OCR and visual content are not inspected" if complete else "Some PDF pages have no extractable text; OCR is not provided"
        text = "\n\n".join(pages)
    elif media_type == "text/html":
        text = parser.text()
        if not text:
            raise DocumentError("HTML has no readable text after removing script/style content")
        segments = [{"id": "s1", "text": text}]
        complete = False
        reason = "HTML text extracted; full-paper coverage is not established"
        if not decoded_cleanly:
            reason += "; some text could not be decoded exactly"
    else:
        decoded, decoded_cleanly = _decode_text(data)
        text = decoded.strip()
        if not text:
            raise DocumentError("The document has no readable text")
        segments = [{"id": "s1", "text": text}]
        complete = decoded_cleanly
        reason = "The supplied text document was decoded in full" if complete else "Some text could not be decoded exactly"

    links.extend(match.rstrip(".,;:!?)］】") for match in _URL_PATTERN.findall(text))
    return {
        "source": label,
        "sha256": hashlib.sha256(data).hexdigest(),
        "media_type": media_type,
        "text": text,
        "segments": segments,
        "coverage": {"complete": bool(complete), "reason": reason},
        "links": _unique_links(links),
    }
