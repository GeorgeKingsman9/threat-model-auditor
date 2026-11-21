"""Discover self-associated public code from paper data, without knowing labels.

Only author-style code-availability contexts and explicitly linked project pages
can nominate a repository. A GitHub URL among references or dependencies is not
an official-code declaration. Selection remains unresolved when more than one
repository has such support. The chosen public repository is resolved once to a
full commit using GitHub's read-only API; HEAD is never passed to the source
reader as an immutable revision. No repository content is executed.
"""

from __future__ import annotations

import hashlib
from http.client import HTTPException
from html.parser import HTMLParser
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from documents import DocumentError, _http_link, _validate_url


MAX_REQUESTS = 6
MAX_PAGE_BYTES = 2 * 1024 * 1024
TIMEOUT_SECONDS = 12
TOTAL_SECONDS = 65
MAX_PROJECT_PAGES = 2
MAX_CANDIDATES = 40
MAX_CONTEXT = 420
URL = re.compile(r"https?://[^\s<>\"']+")
SHA = re.compile(r"[0-9a-fA-F]{40}")
# Generic availability language, never paper names, repository names or labels.
AVAILABILITY = re.compile(
    r"(?:\b(?:our|the|this)\s+(?:(?:source|official|research)\s+)?"
    r"(?:code|implementation|software|artifacts?|data\s+and\s+(?:source\s+)?code|code\s+and\s+data)\b"
    r"[^.!?]{0,95}?\b(?:available|released|public|provided|found|hosted|accessed|open[- ]sourced|at)\b"
    r"|\b(?:source\s+code|code\s+and\s+data|data\s+and\s+(?:source\s+)?code)\b"
    r"[^.!?]{0,60}?\b(?:available|released|provided|found|hosted|at)\b"
    r"|\b(?:code|implementation)\s+(?:is\s+)?(?:publicly\s+)?(?:available|released|provided|hosted)\b"
    r"|(?:^|[\n.;])\s*(?:source\s+code|code|official\s+implementation)\s*[:：])", re.I
)
PROJECT = re.compile(r"\b(?:our\s+)?(?:project\s+(?:page|website|site)|paper\s+website)\s*(?::|is|at|available)?", re.I)
ANCHOR_CODE = re.compile(r"^(?:source\s+code|code|official\s+(?:code|implementation)|github|implementation|code\s*&\s*data)$", re.I)


class DiscoveryError(ValueError):
    """Discovery could not safely complete its bounded read-only requests."""


def _trim_url(url):
    return url.rstrip(".,;:!?)］】]}")


def _github_repository(url):
    """Normalize only real GitHub repository paths; retain an explicit commit."""
    try:
        parts = urlsplit(_trim_url(url))
        if (parts.scheme not in {"http", "https"} or parts.hostname not in {"github.com", "www.github.com"}
                or parts.username is not None or parts.password is not None or parts.port not in {None, 443, 80}):
            return None
        path = parts.path.strip("/").split("/")
        if len(path) < 2 or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", item) or item in {".", ".."} for item in path[:2]):
            return None
        owner, name = path[:2]
        if name.endswith(".git"):
            name = name[:-4]
        if not name or owner.lower() in {"features", "topics", "collections", "marketplace", "sponsors", "settings", "login", "search", "orgs", "users", "site"}:
            return None
        revision = path[3].lower() if len(path) >= 4 and path[2] in {"tree", "blob", "commit"} and SHA.fullmatch(path[3]) else None
        return {"repository": f"https://github.com/{owner}/{name}", "revision": revision}
    except (ValueError, AttributeError):
        return None


def _context_support(text, before_url=None, anchor=False, source_kind="paper"):
    # A single line break may be PDF/HTML layout wrapping. Blank lines still
    # delimit paragraphs, including before the availability phrase itself.
    # Slice the original text so recorded URL offsets keep their meaning.
    left = text if before_url is None else text[:before_url]
    left = re.split(r"\r?\n[^\S\r\n]*\r?\n", left)[-1]
    if anchor and ANCHOR_CODE.fullmatch(" ".join(text.split())):
        return "code_anchor" if source_kind in {"landing_page", "project_page", "html_anchor"} else None
    matches = list(AVAILABILITY.finditer(left))
    if matches:
        match = matches[-1]
        # Named dependency/baseline availability does not become an author-code
        # statement merely because the surrounding paragraph discusses our work.
        nearby = left[max(0, match.start() - 120):match.end()]
        own = re.search(r"\bour\s+(?:(?:source|official)\s+)?(?:code|implementation|data\s+and|software|artifacts?)", nearby, re.I)
        if not own and re.search(r"\b(?:baseline|dependency|dependencies|third[- ]party|prior\s+work|related\s+work|library|we\s+(?:use|adopt))\b", nearby, re.I):
            return None
        suffix = left[match.end():]
        # A declaration attaches to the next URL/anchor, not an unrelated URL
        # later in the same paragraph. Footnote markers and short phrases fit.
        if len(suffix) <= 100 and not URL.search(suffix) and not re.search(r"[!?]|\n\s*\n", suffix):
            return "self_described_code_availability"
    return None


class _Page(HTMLParser):
    """Extract readable page text plus exact anchor-adjacent contexts."""
    EXCLUDED = {"script", "style", "noscript", "template", "svg"}
    BREAKS = {"p", "div", "section", "article", "li", "br", "h1", "h2", "h3", "footer", "header"}

    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url, self.parts, self.anchors, self.hidden, self.active = url, [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.hidden:
            if tag in self.EXCLUDED:
                self.hidden.append(tag)
            return
        if tag in self.EXCLUDED:
            self.hidden.append(tag)
            return
        if tag in self.BREAKS:
            self.parts.append("\n")
        if tag == "a" and attrs.get("href"):
            href = _http_link(attrs["href"], self.url)
            if href:
                self.active.append((href, sum(map(len, self.parts))))

    def handle_endtag(self, tag):
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
            return
        if tag == "a" and self.active:
            href, start = self.active.pop()
            self.anchors.append((href, start, sum(map(len, self.parts))))
        if tag in self.BREAKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def record(self, kind, sha256):
        text = "".join(self.parts)
        contexts = []
        for href, start, end in self.anchors:
            # Keep the nearest block; boilerplate code/footer links must not
            # acquire an unrelated availability declaration from another block.
            left = max(text.rfind("\n", 0, start), start - 230)
            right = text.find("\n", end)
            right = min(right if right >= 0 else len(text), end + 150)
            contexts.append({"url": href, "text": text[left + 1:right],
                             "anchor_text": text[start:end], "source": kind,
                             "start": left + 1, "end": right})
        return {"source": self.url, "text": text, "sha256": sha256,
                "links": [context["url"] for context in contexts], "link_contexts": contexts}


class _Redirect(HTTPRedirectHandler):
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def redirect_request(self, request, response, code, message, headers, newurl):
        self.fetcher.reserve(newurl, redirect=True)
        return super().redirect_request(request, response, code, message, headers, newurl)


class _Fetcher:
    def __init__(self):
        self.requests = []
        self.started = time.monotonic()

    def reserve(self, url, redirect=False):
        if len(self.requests) >= MAX_REQUESTS or time.monotonic() - self.started > TOTAL_SECONDS:
            raise DiscoveryError("automatic source-discovery request budget exhausted")
        _validate_url(url)
        self.requests.append({"url": url, "status": "redirect" if redirect else "requested"})

    def fetch(self, url, accept="text/html,application/json;q=0.9"):
        self.reserve(url)
        entry = self.requests[-1]
        request = Request(url, headers={"User-Agent": "ThreatModelAuditor/0.3 source discovery", "Accept": accept, "Accept-Encoding": "identity"})
        try:
            with build_opener(_Redirect(self)).open(request, timeout=TIMEOUT_SECONDS) as response:
                final = response.geturl()
                _validate_url(final)
                length = response.headers.get("Content-Length", "")
                if length.isdigit() and int(length) > MAX_PAGE_BYTES:
                    raise DiscoveryError("discovery response exceeds the byte limit")
                chunks, size = [], 0
                while True:
                    if time.monotonic() - self.started > TOTAL_SECONDS:
                        raise DiscoveryError("automatic source-discovery time budget exhausted")
                    chunk = response.read(min(65536, MAX_PAGE_BYTES + 1 - size))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    size += len(chunk)
                    if size > MAX_PAGE_BYTES:
                        raise DiscoveryError("discovery response exceeds the byte limit")
                data = b"".join(chunks)
                entry.update(status="completed", final_url=final, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
                return data, final
        except (HTTPError, URLError, OSError, TimeoutError, HTTPException, DocumentError) as error:
            entry.update(status="unavailable", error=type(error).__name__)
            raise DiscoveryError("public source-discovery endpoint unavailable") from None
        except DiscoveryError:
            entry.update(status="unavailable", error="bounded_request_rejected")
            raise


def _page_record(data, source, kind):
    try:
        decoded = data.decode("utf-8")
    except UnicodeDecodeError:
        raise DiscoveryError("discovery page is not exact UTF-8 text") from None
    if not re.search(r"<(?:!doctype\s+html|html|body|a|p|div|section)\b", decoded, re.I):
        raise DiscoveryError("discovery endpoint did not return an HTML page")
    parser = _Page(source)
    parser.feed(decoded)
    return parser.record(kind, hashlib.sha256(data).hexdigest())


def _texts(document):
    seen = set()
    for segment in document.get("segments", []):
        for view in ("reading_order_text", "text"):
            text = segment.get(view)
            if isinstance(text, str) and text not in seen:
                seen.add(text)
                yield segment.get("id"), view, text
    text = document.get("text")
    if isinstance(text, str) and text not in seen:
        yield None, "text", text


def _paper_html_url(source):
    try:
        parts = urlsplit(source)
        if parts.scheme in {"http", "https"} and parts.hostname in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
            match = re.fullmatch(r"/(?:pdf|abs)/([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?)(?:\.pdf)?", parts.path)
            if match:
                return "https://arxiv.org/html/" + match.group(1)
    except (ValueError, TypeError):
        pass
    return None


def _github_link_prefix(url):
    try:
        parts = urlsplit(_trim_url(url))
        if parts.hostname not in {"github.com", "www.github.com"} or parts.username is not None or parts.password is not None:
            return None
        return "https://github.com" + parts.path.rstrip("/").lower()
    except (ValueError, AttributeError):
        return None


def _host_wrapped_github_annotation(text, match, segment_id, annotations):
    """Verify one visible host/path hard wrap against a same-page PDF URI.

    A bare host never identifies a repository. Unlike partial-path recovery,
    this path requires the complete owner/repository on the immediately next
    line and an equal annotation URI, not an arbitrary annotation completion.
    The returned offsets refer to original text; no joined string is evidence.
    """
    if segment_id is None:
        return []
    url = _trim_url(match.group())
    try:
        parts = urlsplit(url)
        if (parts.scheme not in {"http", "https"} or parts.hostname not in {"github.com", "www.github.com"}
                or parts.path != "/" or parts.query or parts.fragment
                or parts.username is not None or parts.password is not None or parts.port not in {None, 80, 443}):
            return []
    except ValueError:
        return []
    continuation = re.match(r"[\t ]*\r?\n[\t ]*(?P<path>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?=$|[\s,;:!?)\]】}])",
                            text[match.end():])
    if continuation is None:
        return []
    end = match.end() + continuation.end("path")
    visible = url + continuation.group("path")
    parsed = _github_repository(visible)
    if parsed is None:
        return []
    prefix = _github_link_prefix(visible)
    matching = {annotation["url"] for annotation in annotations
                if annotation.get("segment_id") == segment_id
                and _github_repository(annotation["url"]) is not None
                and _github_link_prefix(annotation["url"]) == prefix}
    return [{"url": url, "start": match.start(), "end": end} for url in sorted(matching)]


def _host_wrap_context_supported(text, before_url):
    """Apply extra ambiguity guards only to the new host-only recovery path.

    Legacy full-URL and partial-prefix association retain their own context
    contract. A named framework's possessive is not third-party evidence.
    """
    left = re.split(r"\r?\n[^\S\r\n]*\r?\n", text[:before_url])[-1]
    matches = list(AVAILABILITY.finditer(left))
    if not matches:
        return False
    match = matches[-1]
    nearby = left[max(0, match.start() - 120):match.end()]
    own = re.search(r"\bour\s+(?:(?:source|official)\s+)?(?:code|implementation|data\s+and|software|artifacts?)", match.group(), re.I)
    return bool(own or not re.search(
        r"\b(?:baseline|dependency|dependencies|third[- ]party|prior\s+work|related\s+work|references?|authors?|library|we\s+(?:use|adopt)|et\s+al)\b",
        nearby, re.I))


def discover_repository(document, source):
    """Discover one explicitly associated GitHub repository and pin its commit.

    Return selected/not_found/ambiguous/unavailable with evidence and candidate
    rejection reasons. No model call, curated case, expected label or code
    execution participates in discovery.
    """
    if not isinstance(document, dict):
        raise ValueError("source discovery requires a loaded paper document")
    fetcher = _Fetcher()
    candidates, projects, notes = {}, [], []

    def add(url, context, origin, supported=None, segment_id=None, view=None, start=None, anchor_text=None):
        parsed = _github_repository(url)
        if parsed is not None:
            key = parsed["repository"].lower()
            candidate = candidates.setdefault(key, {"repository": parsed["repository"], "revision": None, "evidence": [], "accepted": False,
                                                    "reason": "no_self_associated_code_context"})
            evidence = {"source": origin, "url": url, "context": context[:MAX_CONTEXT],
                        "association": supported or "unassociated_link"}
            if segment_id is not None:
                evidence.update(segment_id=segment_id, text_view=view, context_start=start)
            if evidence not in candidate["evidence"]:
                candidate["evidence"].append(evidence)
            if supported:
                candidate.update(accepted=True, reason="paper_or_linked_project_explicitly_associates_code")
                if parsed["revision"]:
                    existing = candidate.get("revision")
                    if existing and existing != parsed["revision"]:
                        candidate["revision_conflict"] = True
                    candidate["revision"] = parsed["revision"]
            return
        if supported and _http_link(url) and len(projects) < MAX_PROJECT_PAGES:
            parts = urlsplit(url)
            if parts.hostname not in {"github.com", "www.github.com", "api.github.com"} and not parts.path.lower().endswith(".pdf"):
                if url not in [item["url"] for item in projects]:
                    projects.append({"url": url, "association": supported, "parent_source": origin, "context": context[:MAX_CONTEXT]})

    def inspect(record, kind="paper"):
        origin = record.get("source", document.get("source", "supplied_paper"))
        annotations = [item for item in record.get("link_contexts", []) if isinstance(item, dict)
                       and item.get("source") == "pdf_annotation" and isinstance(item.get("url"), str)]
        for segment_id, view, text in _texts(record):
            for match in URL.finditer(text):
                url = _trim_url(match.group())
                left = max(text.rfind("\n\n", 0, match.start()), match.start() - 230, 0)
                context = text[left:min(len(text), match.end() + 120)]
                support = _context_support(context, match.start() - left, source_kind=kind)
                before = text[max(0, match.start() - 80):match.start()]
                if support is None and PROJECT.search(before):
                    support = "explicitly_linked_project_page"
                wrapped = (_host_wrapped_github_annotation(text, match, segment_id, annotations)
                           if support == "self_described_code_availability"
                           and _host_wrap_context_supported(context, match.start() - left) else [])
                if wrapped:
                    for item in sorted(wrapped, key=lambda entry: entry["url"]):
                        full = item["url"]
                        # Include the complete literal fragment even when its
                        # line extends beyond the ordinary URL context window.
                        raw_context = text[left:min(len(text), max(match.end() + 120, item["end"]))]
                        add(full, raw_context, origin, "code_availability_with_same_page_annotation", segment_id, view, left)
                        key = _github_repository(full)["repository"].lower()
                        evidence = candidates[key]["evidence"][-1]
                        evidence.update(visible_url_fragment=text[item["start"]:item["end"]],
                                        visible_url_start=item["start"], visible_url_end=item["end"],
                                        annotation_url=full, annotation_source="pdf_annotation")
                    continue
                # Some two-column PDFs visibly truncate a URL while the actual
                # hyperlink annotation retains it. Combine only the same-page
                # URI with an explicitly associated visible prefix. The URI
                # alone is never an ownership declaration. Multiple continuations
                # remain separate supported candidates and therefore ambiguous.
                prefix = _github_link_prefix(url)
                recovered = []
                if support and segment_id is not None and prefix and len(prefix) > len("https://github.com/") + 2:
                    for annotation in annotations:
                        full = _github_link_prefix(annotation["url"])
                        if (annotation.get("segment_id") == segment_id and full and full != prefix
                                and full.startswith(prefix) and _github_repository(annotation["url"])):
                            recovered.append(annotation["url"])
                if recovered:
                    for full in sorted(set(recovered)):
                        add(full, context, origin, "code_availability_with_same_page_annotation", segment_id, view, left)
                        key = _github_repository(full)["repository"].lower()
                        evidence = candidates[key]["evidence"][-1]
                        evidence.update(visible_url_fragment=url, annotation_url=full,
                                        annotation_source="pdf_annotation")
                    add(url, context, origin, None, segment_id, view, left)
                    partial = _github_repository(url)
                    if partial:
                        candidate = candidates[partial["repository"].lower()]
                        if not candidate["accepted"]:
                            candidate["reason"] = "visible_url_fragment_recovered_by_same_page_annotation"
                    continue
                add(url, context, origin, support, segment_id, view, left)
        for record_context in record.get("link_contexts", []):
            if not isinstance(record_context, dict) or not isinstance(record_context.get("url"), str):
                continue
            url = record_context["url"]
            context = record_context.get("text", "")
            if not isinstance(context, str):
                continue
            context_kind = record_context.get("source", kind)
            # An annotation URI by itself supplies no ownership evidence.
            position = context.find(url)
            support = _context_support(context, position if position >= 0 else None, anchor=True, source_kind=context_kind)
            label = record_context.get("anchor_text", "")
            if support is None and isinstance(label, str):
                support = _context_support(label, anchor=True, source_kind=context_kind)
            if support is None and PROJECT.search(context):
                support = "explicitly_linked_project_page"
            add(url, context, origin, support, record_context.get("segment_id"), "link_context",
                record_context.get("start"), label)
        for url in record.get("links", []):
            if isinstance(url, str):
                add(url, "", origin)

    inspect(document)
    for record in document.get("discovery_documents", []):
        if isinstance(record, dict):
            inspect(record, "landing_page")
    # A source landing page or the matching arXiv HTML rendition is tied to this
    # paper, unlike an arbitrary search result. Follow it only when paper text did
    # not already establish code. Never crawl references for more candidates.
    related = []
    if not any(item["accepted"] for item in candidates.values()):
        html = _paper_html_url(source)
        if html:
            related.append(html)
        elif isinstance(source, str) and source.startswith(("http://", "https://")) and not urlsplit(source).path.lower().endswith(".pdf"):
            related.append(source)
    for url in related[:1]:
        try:
            data, final = fetcher.fetch(url)
            inspect(_page_record(data, final, "landing_page"), "landing_page")
        except (DiscoveryError, DocumentError, ValueError) as error:
            notes.append({"source": url, "reason": str(error)})
    for project in projects[:MAX_PROJECT_PAGES]:
        try:
            data, final = fetcher.fetch(project["url"])
            record = _page_record(data, final, "project_page")
            inspect(record, "project_page")
            notes.append({**project, "status": "read", "sha256": record["sha256"]})
        except (DiscoveryError, DocumentError, ValueError) as error:
            notes.append({**project, "status": "unavailable", "reason": str(error)})
    rows = sorted(candidates.values(), key=lambda item: item["repository"].lower())[:MAX_CANDIDATES]
    accepted = [item for item in rows if item["accepted"]]
    base = {"repository": None, "revision": None, "evidence": [], "candidates": rows,
            "requests": fetcher.requests, "discovery_notes": notes}
    if len(candidates) > MAX_CANDIDATES:
        return {**base, "status": "ambiguous", "reason": "too_many_repository_candidates"}
    if len(accepted) > 1 or any(item.get("revision_conflict") for item in accepted):
        return {**base, "status": "ambiguous", "reason": "multiple_self_associated_repositories_or_commit_versions"}
    if not accepted:
        return {**base, "status": "unavailable" if notes and all(note.get("status") != "read" for note in notes) else "not_found",
                "reason": "no_unambiguous_self_associated_code_repository"}
    selected = accepted[0]
    try:
        owner, name = urlsplit(selected["repository"]).path.strip("/").split("/")
        # The one-item list returns the same immutable identity without the
        # potentially large file patches included by the single-commit API.
        query = [("per_page", "1")]
        if selected.get("revision"):
            query.append(("sha", selected["revision"]))
        api = f"https://api.github.com/repos/{quote(owner, safe='')}/{quote(name, safe='')}/commits?{urlencode(query)}"
        data, final_api = fetcher.fetch(api, "application/vnd.github+json")
        final_parts = urlsplit(final_api)
        if (final_parts.hostname != "api.github.com" or final_parts.scheme != "https"
                or final_parts.username is not None or final_parts.password is not None
                or final_parts.port not in {None, 443} or final_parts.fragment):
            raise DiscoveryError("GitHub commit resolution left the authoritative API host")
        if sorted(parse_qsl(final_parts.query, keep_blank_values=True, strict_parsing=True)) != sorted(query):
            raise DiscoveryError("GitHub commit resolution changed the bounded revision query")
        commits = json.loads(data.decode("utf-8"))
        if not isinstance(commits, list) or len(commits) != 1 or not isinstance(commits[0], dict):
            raise DiscoveryError("GitHub did not return exactly one commit identity")
        metadata = commits[0]
        revision = metadata.get("sha")
        if not isinstance(revision, str) or SHA.fullmatch(revision) is None:
            raise DiscoveryError("GitHub did not return a full commit identity")
        if selected.get("revision") and revision.lower() != selected["revision"]:
            raise DiscoveryError("GitHub commit identity differs from the paper-linked commit")
        canonical = _github_repository(metadata.get("html_url", ""))
        if canonical is None or canonical["revision"] != revision.lower():
            raise DiscoveryError("GitHub metadata lacks the verified commit URL")
        api_match = re.fullmatch(r"/repos/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/commits", final_parts.path)
        if api_match is None:
            raise DiscoveryError("GitHub commit response has an unverified repository path")
        api_repository = f"https://github.com/{api_match.group(1)}/{api_match.group(2)}"
        if canonical["repository"].lower() != api_repository.lower():
            raise DiscoveryError("GitHub commit metadata belongs to another repository")
        if canonical["repository"].lower() != selected["repository"].lower() and not any(
            request.get("url") == final_api and request.get("status") == "redirect" for request in fetcher.requests
        ):
            raise DiscoveryError("Repository rename was not verified by an authoritative API redirect")
        repository = canonical["repository"]
        evidence = selected["evidence"] + [{"source": api, "association": "public_github_commit_resolution",
                    "revision": revision.lower(), "response_sha256": hashlib.sha256(data).hexdigest(),
                    "scope": "Selected current public revision; historical paper execution revision is not established"}]
        return {**base, "status": "selected", "repository": repository, "revision": revision.lower(),
                "evidence": evidence, "reason": "unique_self_associated_code_link_resolved_to_full_commit"}
    except (DiscoveryError, DocumentError, ValueError, TypeError, AttributeError):
        return {**base, "status": "unavailable", "evidence": selected["evidence"],
                "reason": "self_associated_repository_found_but_immutable_revision_unavailable"}
