"""Read a version-bound source snapshot as untrusted data, never as executable code.

Git inputs are read from resolved commit objects, not the working tree. GitHub
inputs use a full commit SHA and a bounded codeload archive kept in memory. An
archive transport/size failure can fall back to a complete hash-checked Git tree
and bounded reads of eligible blobs at that commit. Every download attempt is
recorded; incomplete blob acquisition fails the snapshot. A plain directory has
a content-manifest revision; a supplied Git revision cannot be attached to it
without verification. No hooks, filters, submodules, package installation,
repository tests, or source instructions are executed.

``coverage.complete`` means every eligible source file was supplied, not that
all repository content or runtime behavior was inspected. Exclusions are explicit.
The character budget covers source text; callers should also bound inventory
metadata when constructing a model request.
"""

from __future__ import annotations

import hashlib
import configparser

import evidence_expansion
import data_witnesses
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import HTTPException, IncompleteRead
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tarfile
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_DOWNLOAD_BYTES = 40 * 1024 * 1024
MAX_EXPANDED_BYTES = 128 * 1024 * 1024
MAX_READ_BYTES = 64 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_ENTRIES = 12000
TIMEOUT_SECONDS = 40
DOWNLOAD_TIMEOUT_SECONDS = 90
DOWNLOAD_ATTEMPTS = 2
SOURCE_ONLY_MAX_FILES = 128
SOURCE_ONLY_WORKERS = 4
SOURCE_ONLY_TIMEOUT_SECONDS = 160
SOURCE_REQUEST_TIMEOUT_SECONDS = 20
MAX_METADATA_BYTES = 4 * 1024 * 1024
CODE_SUFFIXES = {
    ".py", ".pyi", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".go", ".rs", ".java", ".kt", ".kts", ".c", ".h", ".cc", ".cpp",
    ".cxx", ".hpp", ".cs", ".swift", ".rb", ".php", ".scala", ".r",
    ".sh", ".bash", ".zsh", ".lua", ".jl", ".m", ".mm",
}
CONFIG_NAMES = {"pyproject.toml", "cargo.toml", "package.json", "tsconfig.json", "setup.cfg"}
EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "vendor",
    "third_party", "third-party", "__pycache__", "dist", "build", "target",
    "data", "datasets", "dataset_cache", "test", "tests", "fixtures",
    "research", "adjudication", "reports", "results", "outputs", "artifacts",
    "benchmarks", "docs", "documentation", "notebooks", ".aws", ".ssh", ".codex",
}
SENSITIVE_NAME = re.compile(
    r"(?:^|[._-])(?:credentials?|secrets?|tokens?|passwords?|private[_-]?keys?|"
    r"api[_-]?keys?|gold|labels?|verdicts?|adjudicat\w*|pilot[_-]?results?)(?:[._-]|$)", re.I
)
CREDENTIAL_CONTENT = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{40,}|"
    r"sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,})\b"
)
_FULL_SHA = re.compile(r"[0-9a-fA-F]{40}")
_LOCAL_REVISION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,199}")


class RepositoryError(ValueError):
    """A source snapshot could not be loaded without guessing its provenance."""

    def __init__(self, message, *, acquisition=None, failure_kind=None, retryable=False):
        super().__init__(message)
        self.acquisition = acquisition
        self.failure_kind = failure_kind
        self.retryable = retryable


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _canonical_hash(value):
    return _digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def _safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise RepositoryError("Unsafe repository path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", ".."} for p in value.split("/")):
        raise RepositoryError("Repository path escapes its snapshot")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise RepositoryError("Repository path contains control characters")
    return value


def _excluded_reason(path):
    parts = PurePosixPath(path).parts
    lower = [part.lower() for part in parts]
    if any(part in EXCLUDED_DIRS for part in lower[:-1]):
        return "excluded_directory"
    if any(part.startswith(".") or SENSITIVE_NAME.search(part) for part in lower[:-1]):
        return "sensitive_or_label_directory"
    name = lower[-1]
    if name.startswith(".") or SENSITIVE_NAME.search(name):
        return "sensitive_or_label_filename"
    if "lock" in name.split(".") or name.endswith((".lock", "-lock.json")):
        return "lockfile"
    if PurePosixPath(path).suffix.lower() not in CODE_SUFFIXES and name not in CONFIG_NAMES:
        return "not_source_code"
    return None


def _eligible_reason(path, *, expand_evidence=False):
    reason = _excluded_reason(path)
    if expand_evidence and evidence_expansion.blocked(path):
        return reason or "hard_excluded_evidence_path"
    return reason


def _priority(path):
    """Generic construction/evaluation priority; never a paper-specific allowlist."""
    parts = PurePosixPath(path.lower()).parts
    name = PurePosixPath(path.lower()).stem
    if name in {"pipeline", "generator", "generate", "construction", "construct", "attack", "attacks", "prompts", "prompt"}:
        rank = 0
    elif any(part in {"prompts", "attacks", "generation", "construction", "dataset"} for part in parts[:-1]):
        rank = 1
    elif name in {"runner", "simulator", "eval", "evaluate", "evaluation", "inference", "client", "model", "models"}:
        rank = 2
    elif name in {"config", "configuration", "main", "utils", "schema", "schemas"}:
        rank = 3
    else:
        rank = 4
    return rank, path


def _git_environment():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0", "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_CONFIG_COUNT": "4", "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": os.devnull,
        "GIT_CONFIG_KEY_1": "core.fsmonitor", "GIT_CONFIG_VALUE_1": "false",
        "GIT_CONFIG_KEY_2": "protocol.ext.allow", "GIT_CONFIG_VALUE_2": "never",
        "GIT_CONFIG_KEY_3": "protocol.file.allow", "GIT_CONFIG_VALUE_3": "never",
    })
    return env


def _git(directory, arguments, max_bytes=4 * 1024 * 1024):
    executable = shutil.which("git")
    if not executable:
        raise RepositoryError("Git is required to read a local Git snapshot")
    try:
        process = subprocess.Popen(
            [executable, "--no-pager", "--literal-pathspecs", "-C", str(directory), *arguments],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=_git_environment(),
        )
    except OSError as error:
        raise RepositoryError("Could not start the Git object reader") from error
    chunks, failures = [], []

    def read():
        size = 0
        try:
            while True:
                chunk = process.stdout.read(65536)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    failures.append("Git object output exceeds its size bound")
                    process.kill()
                    return
                chunks.append(chunk)
        except (OSError, ValueError):
            failures.append("Could not read the Git object stream")

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    try:
        process.wait(timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        failures.append("Git object reading timed out")
    finally:
        reader.join(timeout=5)
        process.stdout.close()
    if failures or reader.is_alive() or process.returncode:
        raise RepositoryError(failures[0] if failures else "Could not resolve or read the requested Git revision")
    return b"".join(chunks)


def _expansion_text(item):
    if "data" not in item or item.get("omission_reason"):
        return None
    try:
        text = item["data"].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return None if "\x00" in text or CREDENTIAL_CONTENT.search(text) else text


MAX_PINNED_DEPENDENCIES = 2
MAX_DEPENDENCY_CHARS = 150000
MAX_GITMODULES_BYTES = 65536


def _submodule_urls(text):
    """Parse Git's declarative map, without invoking Git config or a shell."""
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    try:
        parser.read_string(text)
    except configparser.Error:
        return {}
    result = {}
    for section in parser.sections():
        if not re.fullmatch(r'submodule "[^"\n]+"', section):
            continue
        path, url = parser.get(section, "path", fallback=""), parser.get(section, "url", fallback="")
        # GitHub SCP notation declares a repository identity; normalize it
        # to public HTTPS without SSH, credentials, or branch resolution.
        if url.startswith("git@github.com:"):
            url = "https://github.com/" + url[len("git@github.com:"):]
        try:
            path = _safe_path(path)
            label, _, _, _ = _github_url(url, "0" * 40)
        except RepositoryError:
            continue
        if path not in result:
            result[path] = label
    return result


def _pinned_dependencies(candidates, ledger, read):
    by_path = {entry["path"]: entry for entry in candidates}
    targets = sorted({edge["target"] for edge in ledger["needed"]
                      if edge.get("reason") == "submodule_or_nonregular_boundary"
                      and by_path.get(edge.get("target"), {}).get("mode") == "160000"})
    if not targets:
        return {"dependency_snapshots": [], "dependency_acquisition": []}
    metadata, urls, records, children = None, {}, [], []
    entry = by_path.get(".gitmodules")
    if entry and entry["mode"] in {"100644", "100755"} and entry["bytes"] <= MAX_GITMODULES_BYTES:
        try:
            raw = read(entry)
            text = raw.decode("utf-8")
            if len(raw) != entry["bytes"] or CREDENTIAL_CONTENT.search(text):
                raise RepositoryError("Invalid dependency metadata")
            oid = entry.get("object_id")
            if oid is not None and oid != hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest():
                raise RepositoryError("Dependency metadata differs from its Git blob identity")
            metadata = {"path": ".gitmodules", "bytes": len(raw), "sha256": _digest(raw),
                        "text": text, "line_start": 1, "line_end": max(1, len(text.splitlines())),
                        "id": f"repo:.gitmodules:L1-L{max(1, len(text.splitlines()))}",
                        **({"object_id": oid} if oid else {})}
            urls = _submodule_urls(text)
        except (RepositoryError, UnicodeError):
            pass
    for index, target in enumerate(targets):
        entry = by_path[target]
        record = {"mount_path": target, "revision": entry.get("object_id"),
                  "resolution_scope": "separate_pinned_dependency_snapshot"}
        if index >= MAX_PINNED_DEPENDENCIES:
            record.update(status="unresolved", reason="dependency_count_limit")
        elif target not in urls:
            record.update(status="unresolved", reason="missing_public_github_gitmodules_binding")
        elif not isinstance(entry.get("object_id"), str) or not _FULL_SHA.fullmatch(entry["object_id"]):
            record.update(status="unresolved", reason="dependency_revision_not_fixed")
        else:
            record["source"] = urls[target]
            try:
                child = load_repository(urls[target], revision=entry["object_id"],
                    max_chars=MAX_DEPENDENCY_CHARS, fetch_mode="files", expand_evidence=False)
            except RepositoryError as error:
                record.update(status="unresolved", reason="pinned_dependency_acquisition_failed",
                              failure_kind=error.failure_kind or "repository_error")
                if error.acquisition is not None:
                    record["source_acquisition"] = error.acquisition
            else:
                children.append({"mount_path": target, "source": urls[target],
                                 "revision": entry["object_id"], "snapshot": child})
                record.update(status="resolved", manifest_sha256=child["manifest_sha256"],
                              coverage_complete=child["coverage"]["complete"])
        records.append(record)
    return {"dependency_snapshots": children, "dependency_acquisition": records,
            **({"dependency_metadata": metadata} if metadata else {})}


def _expand_items(items, excluded, candidates, read, max_chars, evidence_policy=evidence_expansion.POLICY):
    """Extend eligibility with the same pure static policy on every transport."""
    data_result = {} if evidence_policy == evidence_expansion.DATA_POLICY else None
    def acquire_data(entry, budget):
        raw = read(entry)
        if len(raw) != entry["bytes"]:
            raise RepositoryError("Data byte size differs from repository inventory")
        if entry.get("object_id") is not None and data_witnesses.git_blob(raw, entry["object_id"]) != entry["object_id"]:
            raise RepositoryError("Data bytes differ from their pinned Git blob identity")
        if CREDENTIAL_CONTENT.search(raw.decode("utf-8", errors="replace")):
            return {"path": entry["path"], "bytes": len(raw), "sha256": _digest(raw),
                    "policy": data_witnesses.POLICY, "output_budget": budget,
                    "status": "unresolved", "reason": "credential_like_content",
                    **({"object_id": entry["object_id"]} if "object_id" in entry else {})}, []
        return data_witnesses.build(entry, raw, output_budget=budget)
    added, ledger = evidence_expansion.expand(candidates, items, read,
        text_for_item=_expansion_text, priority=_priority, max_chars=max_chars,
        policy=evidence_policy, data_handler=acquire_data, data_result=data_result)
    if sum(item["bytes"] for item in items + added if "data" in item) + ledger.get("data_bytes", 0) > MAX_READ_BYTES:
        raise RepositoryError("Expanded source content exceeds its total byte limit")
    paths = {item["path"] for item in added}
    excluded = [item for item in excluded if item["path"] not in paths]
    dependencies = _pinned_dependencies(candidates, ledger, read)
    return items + added, excluded, {**dependencies, "eligibility_policy": evidence_policy,
        **(data_result or {}),
        "evidence_manifest": sorted(candidates, key=lambda item: item["path"]),
        "evidence_expansion": ledger}


def _git_snapshot(directory, revision, *, max_chars=240000, expand_evidence=True, evidence_policy=evidence_expansion.POLICY):
    if revision is not None and (
        not isinstance(revision, str) or not _LOCAL_REVISION.fullmatch(revision) or ".." in revision
    ):
        raise RepositoryError("Invalid Git revision")
    commit = _git(directory, ["rev-parse", "--verify", "--end-of-options", (revision or "HEAD") + "^{commit}"], 256).decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise RepositoryError("Git did not return a full commit identity")
    tree = _git(directory, ["rev-parse", commit + "^{tree}"], 256).decode().strip()
    raw = _git(directory, ["ls-tree", "-r", "-z", "-l", commit])
    entries = raw.rstrip(b"\0").split(b"\0") if raw else []
    if len(entries) > MAX_ENTRIES:
        raise RepositoryError("Repository has too many entries")
    items, excluded, candidates = [], [], []
    total_read = 0
    for entry in entries:
        try:
            header, encoded = entry.split(b"\t", 1)
            mode, kind, oid, size = header.decode("ascii").split()
            path = _safe_path(encoded.decode("utf-8"))
        except (ValueError, UnicodeError) as error:
            raise RepositoryError("Malformed or unsupported Git tree path") from error
        candidates.append({"path": path, "bytes": int(size) if size.isdigit() else 0, "object_id": oid, "mode": mode, "type": kind})
        reason = _eligible_reason(path, expand_evidence=expand_evidence)
        if mode not in {"100644", "100755"} or kind != "blob":
            reason = "symlink_or_submodule"
        if reason:
            excluded.append({"path": path, "reason": reason})
            continue
        count = int(size)
        item = {"path": path, "bytes": count, "object_id": oid, "sha256": None}
        if count > MAX_FILE_BYTES:
            item["omission_reason"] = "file_byte_limit"
        else:
            total_read += count
            if total_read > MAX_READ_BYTES:
                raise RepositoryError("Eligible source content exceeds its total byte limit")
            data = _git(directory, ["cat-file", "blob", oid], MAX_FILE_BYTES)
            if len(data) != count:
                raise RepositoryError("Git blob size changed during snapshot reading")
            item.update(data=data, sha256=_digest(data))
        items.append(item)
    def read(entry):
        data = _git(directory, ["cat-file", "blob", entry["object_id"]], max(MAX_FILE_BYTES, data_witnesses.LIMITS["max_file_bytes"]))
        if len(data) != entry["bytes"]:
            raise RepositoryError("Git blob size changed during evidence expansion")
        return data
    items, excluded, expansion = _expand_items(items, excluded, candidates, read, max_chars, evidence_policy) if expand_evidence else (items, excluded, {})
    return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit, "tree_sha": tree, **expansion}


def _directory_snapshot(directory, *, max_chars=240000, expand_evidence=True, evidence_policy=evidence_expansion.POLICY):
    items, excluded, candidates = [], [], []
    total_read, entries = 0, 0

    def walk_error(error):
        raise RepositoryError("Could not inventory the complete source directory") from error

    def read(entry):
        current = directory / entry["path"]
        try:
            # Parent symlinks are excluded during inventory and rechecked before
            # targeted reads, preventing traversal into a replaced directory.
            for parent in current.parents:
                if parent == directory: break
                if parent.is_symlink(): raise RepositoryError("Evidence parent became a symbolic link")
            descriptor = os.open(current, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
            with os.fdopen(descriptor, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_size != entry["bytes"]:
                    raise RepositoryError("Evidence file changed or is not regular")
                data = stream.read(max(MAX_FILE_BYTES, data_witnesses.LIMITS["max_file_bytes"]) + 1)
                if len(data) != info.st_size:
                    raise RepositoryError("Source file changed while its snapshot was read")
                return data
        except OSError as error:
            raise RepositoryError("Could not safely read a regular source file") from error

    for base, dirs, names in os.walk(directory, followlinks=False, onerror=walk_error):
        dirs.sort(); names.sort()
        entries += len(dirs) + len(names)
        if entries > MAX_ENTRIES:
            raise RepositoryError("Repository has too many entries")
        kept = []
        for name in dirs:
            current = Path(base) / name
            path = _safe_path(current.relative_to(directory).as_posix())
            # Inventory vendor/data paths, but never inspect hard-excluded trees.
            if current.is_symlink() or evidence_expansion.blocked(path + "/placeholder"):
                excluded.append({"path": path + "/", "reason": "symlink_or_excluded_directory"})
                candidates.append({"path": path, "bytes": 0, "mode": "directory", "type": "excluded_directory"})
            else:
                kept.append(name)
        dirs[:] = kept
        for name in names:
            current = Path(base) / name
            path = _safe_path(current.relative_to(directory).as_posix())
            info = current.lstat()
            mode = "100644" if stat.S_ISREG(info.st_mode) else "120000" if stat.S_ISLNK(info.st_mode) else "special"
            entry = {"path": path, "bytes": info.st_size, "mode": mode, "type": "blob"}
            candidates.append(entry)
            reason = _eligible_reason(path, expand_evidence=expand_evidence)
            if mode != "100644": reason = "symlink" if mode == "120000" else "not_regular_file"
            if evidence_expansion.blocked(path): reason = reason or "sensitive_or_label_directory"
            if reason:
                excluded.append({"path": path, "reason": reason})
                continue
            item = {"path": path, "bytes": info.st_size, "sha256": None}
            if info.st_size > MAX_FILE_BYTES:
                item["omission_reason"] = "file_byte_limit"
            else:
                total_read += info.st_size
                if total_read > MAX_READ_BYTES:
                    raise RepositoryError("Eligible source content exceeds its total byte limit")
                data = read(entry)
                item.update(data=data, sha256=_digest(data))
            items.append(item)
    items, excluded, expansion = _expand_items(items, excluded, candidates, read, max_chars, evidence_policy) if expand_evidence else (items, excluded, {})
    return items, excluded, {"revision_kind": "content_manifest", "commit": None, "tree_sha": None, **expansion}


def _github_url(source, revision):
    try:
        parts = urlsplit(source)
        path = parts.path.strip("/")
        if path.endswith(".git"):
            path = path[:-4]
        components = path.split("/")
        if (parts.scheme != "https" or parts.hostname != "github.com" or parts.netloc != "github.com"
                or parts.username or parts.password or parts.query or parts.fragment or len(components) != 2
                or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", part) or part in {".", ".."} for part in components)):
            raise RepositoryError("Provide an HTTPS github.com/owner/repository URL without credentials")
    except ValueError as error:
        raise RepositoryError("Invalid GitHub repository URL") from error
    if not isinstance(revision, str) or not _FULL_SHA.fullmatch(revision):
        raise RepositoryError("GitHub source requires a full 40-character commit SHA")
    owner, name = components
    commit = revision.lower()
    return f"https://github.com/{owner}/{name}", f"https://codeload.github.com/{owner}/{name}/tar.gz/{commit}", name, commit


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise RepositoryError("Unexpected source archive redirect", failure_kind="unexpected_redirect")


def _download_archive_once(url, attempt, *, byte_limit=None, timeout_seconds=None, consume=None):
    byte_limit = MAX_DOWNLOAD_BYTES if byte_limit is None else byte_limit
    timeout_seconds = DOWNLOAD_TIMEOUT_SECONDS if timeout_seconds is None else timeout_seconds
    opener = build_opener(_NoRedirect())
    request = Request(url, headers={"User-Agent": "ThreatModelAuditor/0.2 source reader", "Accept-Encoding": "identity"})
    started = time.monotonic()
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            if response.geturl() != url:
                raise RepositoryError("Source archive URL changed", failure_kind="unexpected_redirect")
            attempt["http_status"] = getattr(response, "status", None)
            length = response.headers.get("Content-Length", "")
            attempt["content_length"] = int(length) if length.isdigit() else None
            if length.isdigit() and int(length) > byte_limit:
                raise RepositoryError("Source archive exceeds its download limit", failure_kind="download_limit")
            chunks, size = [], 0
            while True:
                if time.monotonic() - started > timeout_seconds:
                    raise RepositoryError("Source archive download timed out", failure_kind="timeout", retryable=True)
                chunk = response.read(min(65536, byte_limit + 1 - size))
                if not chunk:
                    break
                chunks.append(chunk)
                size += len(chunk)
                attempt["bytes_received"] = size
                if consume is not None:
                    consume(len(chunk))
                if size > byte_limit:
                    raise RepositoryError("Source archive exceeds its download limit", failure_kind="download_limit")
            if time.monotonic() - started > timeout_seconds:
                raise RepositoryError("Source archive download timed out", failure_kind="timeout", retryable=True)
            if length.isdigit() and size != int(length):
                raise RepositoryError("Could not download the complete pinned GitHub source archive",
                                      failure_kind="truncated_response", retryable=True)
            return b"".join(chunks)
    except HTTPError as error:
        attempt["http_status"] = error.code
        raise RepositoryError("Could not download the pinned GitHub source archive (HTTP " + str(error.code) + ")",
                              failure_kind="http_error", retryable=error.code in {408, 425, 429, 500, 502, 503, 504}) from error
    except (URLError, OSError, TimeoutError, HTTPException) as error:
        reason = error.reason if isinstance(error, URLError) else error
        if isinstance(reason, TimeoutError):
            message, kind = "Source archive download timed out", "timeout"
        elif isinstance(error, IncompleteRead):
            attempt["bytes_received"] += len(error.partial)
            if consume is not None:
                consume(len(error.partial))
            message, kind = "Could not download the complete pinned GitHub source archive", "truncated_response"
        else:
            message, kind = "Could not download the pinned GitHub source archive", "transport_error"
        raise RepositoryError(message, failure_kind=kind, retryable=True) from error


def _download_archive(url, *, acquisition=None, max_attempts=DOWNLOAD_ATTEMPTS):
    """Retry only transient transport failures, without accepting partial bytes.

    Each attempt has the same size and time bounds. Its safe metadata survives
    both success and failure; response bodies, credentials and raw error text do
    not enter the ledger. Limits and invalid provenance are never retried.
    """
    if acquisition is None:
        acquisition = {}
    acquisition.update(method="github_codeload_full_commit_url", download_byte_limit=MAX_DOWNLOAD_BYTES,
                       attempt_timeout_seconds=DOWNLOAD_TIMEOUT_SECONDS, max_attempts=max_attempts, attempts=[])
    for number in range(1, max_attempts + 1):
        attempt = {"attempt": number, "bytes_received": 0}
        acquisition["attempts"].append(attempt)
        started = time.monotonic()
        try:
            data = _download_archive_once(url, attempt)
        except RepositoryError as error:
            attempt.update(status="failed", failure_kind=error.failure_kind or "invalid_download", retryable=error.retryable,
                           elapsed_seconds=round(time.monotonic() - started, 3))
            error.acquisition = acquisition
            if not error.retryable or number == max_attempts:
                raise
        else:
            attempt.update(status="succeeded", elapsed_seconds=round(time.monotonic() - started, 3), sha256=_digest(data))
            return data


def _archive_snapshot(data, repository_name, commit, *, max_chars=240000, expand_evidence=True, evidence_policy=evidence_expansion.POLICY):
    if len(data) > MAX_DOWNLOAD_BYTES:
        raise RepositoryError("Source archive exceeds its download limit")
    items, excluded, seen, candidates, members = [], [], set(), [], {}
    total_expanded, total_read = 0, 0
    prefix = repository_name + "-" + commit
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            for index, member in enumerate(archive):
                if index >= MAX_ENTRIES:
                    raise RepositoryError("Source archive has too many entries")
                name = member.name.rstrip("/")
                _safe_path(name)
                parts = name.split("/")
                if parts[0] != prefix:
                    raise RepositoryError("Archive root does not match the requested commit")
                if len(parts) == 1:
                    if not member.isdir() or member.size:
                        raise RepositoryError("Malformed source archive root")
                    continue
                path = _safe_path("/".join(parts[1:]))
                if path in seen:
                    raise RepositoryError("Duplicate source archive path")
                seen.add(path)
                total_expanded += max(0, member.size)
                if member.size < 0 or total_expanded > MAX_EXPANDED_BYTES:
                    raise RepositoryError("Source archive exceeds its expanded byte limit")
                if member.isdir():
                    if member.size:
                        raise RepositoryError("Malformed source archive directory")
                    continue
                mode = "100644" if member.isfile() else "special"
                candidates.append({"path": path, "bytes": member.size, "mode": mode, "type": "blob"})
                members[path] = member
                reason = _eligible_reason(path, expand_evidence=expand_evidence)
                if not member.isfile():
                    reason = "symlink_hardlink_or_special_file"
                if reason:
                    excluded.append({"path": path, "reason": reason})
                    continue
                item = {"path": path, "bytes": member.size, "sha256": None}
                if member.size > MAX_FILE_BYTES:
                    item["omission_reason"] = "file_byte_limit"
                else:
                    total_read += member.size
                    if total_read > MAX_READ_BYTES:
                        raise RepositoryError("Eligible source content exceeds its total byte limit")
                    stream = archive.extractfile(member)
                    if stream is None:
                        raise RepositoryError("Missing source archive content")
                    raw = stream.read(MAX_FILE_BYTES + 1)
                    if len(raw) != member.size:
                        raise RepositoryError("Source archive member size mismatch")
                    item.update(data=raw, sha256=_digest(raw))
                items.append(item)
            def read(entry):
                stream = archive.extractfile(members[entry["path"]])
                if stream is None:
                    raise RepositoryError("Missing referenced archive content")
                raw = stream.read(max(MAX_FILE_BYTES, data_witnesses.LIMITS["max_file_bytes"]) + 1)
                if len(raw) != entry["bytes"]:
                    raise RepositoryError("Referenced archive member size mismatch")
                return raw
            items, excluded, expansion = _expand_items(items, excluded, candidates, read, max_chars, evidence_policy) if expand_evidence else (items, excluded, {})
    except (tarfile.TarError, OSError, EOFError) as error:
        raise RepositoryError("Invalid or truncated source archive") from error
    if not items:
        raise RepositoryError("Source archive has no eligible source files")
    return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit,
                             "tree_sha": None, "commit_binding": "github_codeload_full_commit_url",
                             "archive_sha256": _digest(data), **expansion}


def _remote_tree(entries, tree_sha, *, expand_evidence=False):
    """Check the complete flat API tree, including its Git tree object hashes."""
    if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
        raise RepositoryError("GitHub source tree exceeds its entry limit")
    by_path, children = {}, {"": []}
    for entry in entries:
        if not isinstance(entry, dict):
            raise RepositoryError("Malformed GitHub source tree entry")
        path = _safe_path(entry.get("path"))
        if path in by_path or not isinstance(entry.get("sha"), str) or not _FULL_SHA.fullmatch(entry["sha"]):
            raise RepositoryError("Duplicate path or invalid GitHub object identity")
        mode, kind = entry.get("mode"), entry.get("type")
        if (mode, kind) not in {("040000", "tree"), ("100644", "blob"), ("100755", "blob"),
                                ("120000", "blob"), ("160000", "commit")}:
            raise RepositoryError("Unsupported GitHub source tree entry")
        if kind == "blob" and (type(entry.get("size")) is not int or entry["size"] < 0):
            raise RepositoryError("Invalid GitHub blob size")
        by_path[path] = entry
        parent = str(PurePosixPath(path).parent)
        parent = "" if parent == "." else parent
        children.setdefault(parent, []).append(entry)
        if kind == "tree":
            children.setdefault(path, [])
    for path, entry in by_path.items():
        parent = str(PurePosixPath(path).parent)
        if parent != "." and (parent not in by_path or by_path[parent]["type"] != "tree"):
            raise RepositoryError("Incomplete GitHub source tree inventory")
    for path, values in children.items():
        def tree_order(entry):
            name = PurePosixPath(entry["path"]).name
            return (name + ("/" if entry["type"] == "tree" else "")).encode("utf-8")

        raw = b"".join((entry["mode"].lstrip("0") + " " + PurePosixPath(entry["path"]).name).encode("utf-8")
                       + b"\0" + bytes.fromhex(entry["sha"]) for entry in sorted(values, key=tree_order))
        digest = hashlib.sha1(f"tree {len(raw)}\0".encode() + raw).hexdigest()
        expected = tree_sha if path == "" else by_path[path]["sha"]
        if digest != expected:
            raise RepositoryError("GitHub tree inventory does not match its Git object hash")
    items, excluded = [], []
    for path, entry in sorted(by_path.items()):
        if entry["type"] == "tree":
            continue
        reason = _eligible_reason(path, expand_evidence=expand_evidence)
        if entry["mode"] not in {"100644", "100755"} or entry["type"] != "blob":
            reason = "symlink_or_submodule"
        if reason:
            excluded.append({"path": path, "reason": reason})
        else:
            items.append({"path": path, "bytes": entry["size"], "object_id": entry["sha"], "sha256": None})
    return items, excluded


def _github_source_snapshot(label, commit, acquisition, *, max_chars=240000, expand_evidence=True, evidence_policy=evidence_expansion.POLICY):
    """Read only eligible blobs after an archive transport/size failure.

    The recursive tree must be complete and hash-correct. Every eligible blob
    within the original per-file bound must be read and hash-checked, or the
    entire acquisition fails. Character-budget selection still happens later.
    """
    fallback = {"method": "github_commit_tree_raw_blobs", "max_base_source_files": SOURCE_ONLY_MAX_FILES,
                "max_source_files": SOURCE_ONLY_MAX_FILES + (evidence_expansion.LIMITS["max_added_files"] if expand_evidence else 0),
                "max_workers": SOURCE_ONLY_WORKERS, "timeout_seconds": SOURCE_ONLY_TIMEOUT_SECONDS,
                "request_timeout_seconds": SOURCE_REQUEST_TIMEOUT_SECONDS,
                "download_byte_limit": MAX_DOWNLOAD_BYTES, "attempts": [], "bytes_received": 0}
    acquisition["fallback"] = fallback
    deadline, lock, abort = time.monotonic() + SOURCE_ONLY_TIMEOUT_SECONDS, threading.Lock(), threading.Event()
    owner_repo = urlsplit(label).path.strip("/")
    api = "https://api.github.com/repos/" + owner_repo + "/git/"

    def consume(count):
        with lock:
            fallback["bytes_received"] += count
            if fallback["bytes_received"] > MAX_DOWNLOAD_BYTES:
                raise RepositoryError("Source-only acquisition exceeds its total download limit", failure_kind="download_limit")

    def read(url, kind, limit, path=None):
        for number in range(1, DOWNLOAD_ATTEMPTS + 1):
            remaining = deadline - time.monotonic()
            if abort.is_set() or remaining <= 0:
                raise RepositoryError("Source-only acquisition timed out or stopped", failure_kind="source_acquisition_stopped")
            attempt = {"resource_kind": kind, "attempt": number, "bytes_received": 0}
            if path is not None:
                attempt["path"] = path
            with lock:
                fallback["attempts"].append(attempt)
            started = time.monotonic()
            try:
                data = _download_archive_once(url, attempt, byte_limit=limit,
                    timeout_seconds=min(SOURCE_REQUEST_TIMEOUT_SECONDS, remaining), consume=consume)
            except RepositoryError as error:
                attempt.update(status="failed", failure_kind=error.failure_kind or "invalid_download",
                               retryable=error.retryable, elapsed_seconds=round(time.monotonic() - started, 3))
                if not error.retryable or number == DOWNLOAD_ATTEMPTS:
                    raise
            else:
                attempt.update(status="succeeded", elapsed_seconds=round(time.monotonic() - started, 3), sha256=_digest(data))
                return data

    def metadata(suffix, kind):
        raw = read(api + suffix, kind, MAX_METADATA_BYTES)
        try:
            result = json.loads(raw)
        except (UnicodeError, ValueError) as error:
            raise RepositoryError("Malformed GitHub source metadata") from error
        if not isinstance(result, dict):
            raise RepositoryError("Malformed GitHub source metadata")
        return result

    try:
        commit_data = metadata("commits/" + commit, "commit")
        tree_sha = commit_data.get("tree", {}).get("sha") if isinstance(commit_data.get("tree"), dict) else None
        if commit_data.get("sha") != commit or not isinstance(tree_sha, str) or not _FULL_SHA.fullmatch(tree_sha):
            raise RepositoryError("GitHub commit metadata does not match the pinned commit")
        tree_data = metadata("trees/" + tree_sha + "?recursive=1", "tree")
        if tree_data.get("sha") != tree_sha or tree_data.get("truncated") is not False:
            raise RepositoryError("GitHub source tree is truncated or has the wrong identity")
        raw_entries = tree_data.get("tree")
        if not isinstance(raw_entries, list) or any(not isinstance(entry, dict) for entry in raw_entries):
            raise RepositoryError("Malformed GitHub source tree metadata")
        entries = [{key: entry[key] for key in ("path", "mode", "type", "sha", "size") if key in entry}
                   for entry in raw_entries]
        items, excluded = _remote_tree(entries, tree_sha, expand_evidence=expand_evidence)
        readable = [item for item in items if item["bytes"] <= MAX_FILE_BYTES]
        if not items or len(readable) > SOURCE_ONLY_MAX_FILES:
            raise RepositoryError("Source-only acquisition exceeds its eligible file limit or has no source")
        if sum(item["bytes"] for item in readable) > min(MAX_READ_BYTES, MAX_DOWNLOAD_BYTES):
            raise RepositoryError("Eligible source content exceeds its total byte limit")
        for item in items:
            if item["bytes"] > MAX_FILE_BYTES:
                item["omission_reason"] = "file_byte_limit"

        def blob(item, limit=MAX_FILE_BYTES):
            url = "https://raw.githubusercontent.com/" + owner_repo + "/" + commit + "/" + quote(item["path"], safe="/")
            raw = read(url, "blob", min(limit, item["bytes"]), item["path"])
            oid = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            if len(raw) != item["bytes"] or oid != item["object_id"]:
                raise RepositoryError("Source blob differs from its pinned Git tree identity")
            item.update(data=raw, sha256=_digest(raw))

        with ThreadPoolExecutor(max_workers=SOURCE_ONLY_WORKERS) as pool:
            futures = [pool.submit(blob, item) for item in readable]
            try:
                for future in as_completed(futures):
                    future.result()
            except Exception:
                abort.set()
                for future in futures:
                    future.cancel()
                raise
        if time.monotonic() > deadline:
            raise RepositoryError("Source-only acquisition timed out", failure_kind="timeout")
        candidates = [{"path": entry["path"], "bytes": entry.get("size", 0),
                       "mode": entry["mode"], "type": entry["type"], "object_id": entry["sha"]}
                      for entry in entries if entry["type"] != "tree"]
        def referenced_blob(entry):
            item = dict(entry)
            blob(item, max(MAX_FILE_BYTES, data_witnesses.LIMITS["max_file_bytes"]))
            return item["data"]
        items, excluded, expansion = _expand_items(items, excluded, candidates, referenced_blob, max_chars, evidence_policy) if expand_evidence else (items, excluded, {})
        fallback.update(status="succeeded", eligible_files=len(items), fetched_files=sum("data" in item for item in items), tree_sha=tree_sha)
        return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit,
            "tree_sha": tree_sha, "commit_binding": "github_commit_tree_raw_blobs",
            "tree_manifest": entries, "tree_manifest_sha256": _canonical_hash(entries), **expansion}
    except (RepositoryError, TypeError, KeyError, ValueError) as error:
        fallback["status"] = "failed"
        if not isinstance(error, RepositoryError):
            error = RepositoryError("Malformed GitHub source tree metadata")
        error.acquisition = acquisition
        raise error


def _manifest_hash(manifest, excluded, provenance):
    value = {"eligible_source": manifest, "excluded": excluded}
    if provenance.get("eligibility_policy") in evidence_expansion.SUPPORTED_POLICIES:
        for key in ("eligibility_policy", "evidence_manifest", "dependency_metadata"):
            value[key] = provenance.get(key)
        value["dependencies"] = [{key: child[key] for key in ("mount_path", "source", "revision")} | {"manifest_sha256": child["snapshot"]["manifest_sha256"]} for child in provenance.get("dependency_snapshots", [])]
    if provenance.get("eligibility_policy") == evidence_expansion.DATA_POLICY:
        for key in ("data_blobs", "data_witnesses"):
            value[key] = provenance.get(key)
    return _canonical_hash(value)


def _validate_dependencies(snapshot, fail):
    children, records = snapshot.get("dependency_snapshots"), snapshot.get("dependency_acquisition")
    if (not isinstance(children, list) or not isinstance(records, list) or len(children) > MAX_PINNED_DEPENDENCIES
            or any(not isinstance(record, dict) for record in records)):
        fail("invalid pinned dependency lists")
    entries = {entry["path"]: entry for entry in snapshot["evidence_manifest"]}
    metadata, urls = snapshot.get("dependency_metadata"), {}
    if metadata is not None:
        entry = entries.get(".gitmodules")
        if not isinstance(metadata, dict) or not isinstance(metadata.get("text"), str) or entry is None:
            fail("invalid gitmodules metadata")
        raw = metadata["text"].encode("utf-8")
        lines = max(1, len(metadata["text"].splitlines()))
        if (len(raw) > MAX_GITMODULES_BYTES or len(raw) != entry["bytes"] or metadata.get("bytes") != len(raw)
                or metadata.get("sha256") != _digest(raw) or metadata.get("path") != ".gitmodules"
                or metadata.get("line_start") != 1 or metadata.get("line_end") != lines
                or metadata.get("id") != f"repo:.gitmodules:L1-L{lines}" or CREDENTIAL_CONTENT.search(metadata["text"])):
            fail("gitmodules raw-byte or line binding changed")
        if entry.get("object_id") is not None:
            if metadata.get("object_id") != entry["object_id"] or entry["object_id"] != hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest():
                fail("gitmodules Git blob binding changed")
        urls = _submodule_urls(metadata["text"])
    targets = sorted({edge["target"] for edge in snapshot["evidence_expansion"]["needed"]
                      if edge.get("reason") == "submodule_or_nonregular_boundary"
                      and entries.get(edge.get("target"), {}).get("mode") == "160000"})
    for record in records:
        entry = entries.get(record.get("mount_path"), {})
        if (record.get("revision") != entry.get("object_id") or record.get("status") not in {"resolved", "unresolved"}
                or record.get("resolution_scope") != "separate_pinned_dependency_snapshot"
                or (record.get("source") is not None and record["source"] != urls.get(record.get("mount_path")))):
            fail("dependency acquisition identity changed")
    if [record.get("mount_path") for record in records] != targets:
        fail("dependency acquisition records differ from needed gitlinks")
    child_paths = []
    for wrapper in children:
        if not isinstance(wrapper, dict): fail("malformed dependency wrapper")
        mount = _safe_path(wrapper.get("mount_path"))
        entry = entries.get(mount, {})
        source, revision = wrapper.get("source"), wrapper.get("revision")
        if entry.get("mode") != "160000" or entry.get("object_id") != revision or urls.get(mount) != source:
            fail("dependency source or revision differs from pinned gitlink")
        child = wrapper.get("snapshot")
        if not isinstance(child, dict) or child.get("dependency_snapshots") or child.get("eligibility_policy") is not None:
            fail("recursive dependency expansion is prohibited")
        validate_repository(child)
        if child["source"] != source or child["revision"] != revision:
            fail("dependency snapshot identity changed")
        record = next((record for record in records if record["mount_path"] == mount), {})
        if record.get("status") != "resolved" or record.get("manifest_sha256") != child["manifest_sha256"]:
            fail("resolved dependency record differs from child snapshot")
        child_paths.append(mount)
    if len(set(child_paths)) != len(child_paths): fail("duplicate dependency snapshot")
    if {record["mount_path"] for record in records if record.get("status") == "resolved"} != set(child_paths):
        fail("resolved dependency has no validated snapshot")


def _validate_data_git_manifest(snapshot, entries, fail):
    """Bind flat pinned leaf identities back to their saved Git tree root."""
    tree_sha = snapshot.get("tree_sha")
    if snapshot.get("revision_kind") != "git_commit" or tree_sha is None:
        return
    if not isinstance(tree_sha, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", tree_sha):
        fail("invalid data repository Git tree identity")
    if snapshot.get("tree_manifest") is not None:
        # The GitHub transport also preserves explicit tree objects (including
        # empty trees), which the existing checker authenticates recursively.
        _remote_tree(snapshot["tree_manifest"], tree_sha, expand_evidence=True)
        expected = [{"path": entry["path"], "bytes": entry.get("size", 0),
                     "mode": entry["mode"], "type": entry["type"], "object_id": entry["sha"]}
                    for entry in snapshot["tree_manifest"] if entry["type"] != "tree"]
        if sorted(expected, key=lambda item: item["path"]) != entries:
            fail("data manifest differs from pinned Git tree")
        return
    root = {}
    for entry in entries:
        mode, oid = entry["mode"], entry.get("object_id")
        if (mode not in {"100644", "100755", "120000", "160000"}
                or not isinstance(oid, str) or len(oid) != len(tree_sha)
                or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid)):
            fail("data manifest has an invalid pinned leaf identity")
        parts, node = entry["path"].split("/"), root
        for parent in parts[:-1]:
            node = node.setdefault(parent, {})
            if not isinstance(node, dict): fail("Git data manifest path conflict")
        if parts[-1] in node: fail("Git data manifest path conflict")
        node[parts[-1]] = (mode, oid)

    def tree_identity(node, depth=0):
        if depth > 128: fail("Git data manifest nesting limit")
        values = []
        for name, child in sorted(node.items(), key=lambda pair: (
                pair[0] + ("/" if isinstance(pair[1], dict) else "")).encode("utf-8")):
            mode, oid = ("40000", tree_identity(child, depth + 1)) if isinstance(child, dict) else child
            values.append((mode + " " + name).encode("utf-8") + b"\0" + bytes.fromhex(oid))
        raw = b"".join(values)
        encoded = f"tree {len(raw)}\0".encode() + raw
        return hashlib.sha1(encoded).hexdigest() if len(tree_sha) == 40 else _digest(encoded)
    if tree_identity(root) != tree_sha:
        fail("data manifest leaf identities differ from pinned Git tree")


def _validated_data_state(snapshot, fail):
    entries = snapshot.get("evidence_manifest")
    if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
        fail("invalid data repository manifest")
    by_path = {}
    for entry in entries:
        if (not isinstance(entry, dict) or type(entry.get("bytes")) is not int
                or entry["bytes"] < 0 or not isinstance(entry.get("mode"), str)):
            fail("malformed data repository entry")
        path = _safe_path(entry.get("path"))
        if path in by_path: fail("duplicate data repository entry")
        by_path[path] = entry
    _validate_data_git_manifest(snapshot, entries, fail)
    raw_data, blobs_by_path = {}, {}
    if snapshot.get("eligibility_policy") == evidence_expansion.DATA_POLICY:
        blobs, witnesses = snapshot.get("data_blobs"), snapshot.get("data_witnesses")
        if (not isinstance(blobs, list) or len(blobs) > data_witnesses.LIMITS["max_files"]
                or not isinstance(witnesses, list)
                or len(witnesses) > data_witnesses.LIMITS["max_files"] * data_witnesses.LIMITS["max_records"]):
            fail("invalid bounded data collections")
        total = 0
        for blob in blobs:
            if not isinstance(blob, dict): fail("malformed data blob")
            path = _safe_path(blob.get("path"))
            entry = by_path.get(path)
            if (entry is None or path in blobs_by_path or evidence_expansion.blocked(path)
                    or entry.get("mode") not in {"100644", "100755"}
                    or PurePosixPath(path).suffix.lower() != ".json"
                    or blob.get("bytes") != entry["bytes"]
                    or type(blob.get("bytes")) is not int
                    or blob["bytes"] > data_witnesses.LIMITS["max_file_bytes"]
                    or blob.get("object_id") != entry.get("object_id")
                    or not isinstance(blob.get("sha256"), str)
                    or not re.fullmatch(r"[0-9a-f]{64}", blob["sha256"])
                    or type(blob.get("output_budget")) is not int
                    or not 0 < blob["output_budget"] <= data_witnesses.LIMITS["max_file_output_bytes"]):
                fail("data blob differs from bounded repository inventory")
            total += blob["bytes"]
            if total > data_witnesses.LIMITS["max_total_bytes"]:
                fail("bounded data total byte limit exceeded")
            blobs_by_path[path] = blob
            if blob.get("reason") == "credential_like_content":
                allowed = {"path", "bytes", "sha256", "policy", "output_budget", "status", "reason"}
                if "object_id" in entry: allowed.add("object_id")
                if set(blob) != allowed or blob.get("status") != "unresolved" or blob.get("policy") != data_witnesses.POLICY:
                    fail("invalid credential data omission")
            else:
                try:
                    raw = data_witnesses.decode_blob(blob)
                    if (len(raw) != entry["bytes"] or _digest(raw) != blob["sha256"]
                            or CREDENTIAL_CONTENT.search(raw.decode("utf-8", errors="replace"))):
                        fail("data raw bytes differ from their safe full-file hash")
                    if "object_id" in entry and data_witnesses.git_blob(raw, entry["object_id"]) != entry["object_id"]:
                        fail("data raw bytes differ from their Git blob identity")
                    raw_data[path] = raw
                except (ValueError, TypeError, UnicodeError) as error:
                    fail("invalid bounded raw data encoding: " + str(error))
        output_bytes = 0
        for witness in witnesses:
            if not isinstance(witness, dict) or not isinstance(witness.get("text"), str):
                fail("malformed bounded record witness")
            count = len(witness["text"].encode("utf-8"))
            if count > data_witnesses.LIMITS["max_record_bytes"]:
                fail("record witness byte limit exceeded")
            output_bytes += count
        if output_bytes > data_witnesses.LIMITS["max_output_bytes"]:
            fail("bounded record output byte limit exceeded")

    return raw_data, blobs_by_path


def validate_data_evidence(metadata):
    """Validate saved bounded data using provenance alone, without file segments.

    Combined V6 inputs retain these exact metadata and complete capped raw blobs.
    Validate their hashes, pinned Git object identities and deterministic record
    selection independently of any recomputed combined/model input binding.
    This checks internal provenance; callers still bind the repository identity
    to their recorded ingestion run, as with validate_repository.
    """
    def fail(message):
        raise RepositoryError("Invalid bounded data evidence: " + message)
    if not isinstance(metadata, dict): fail("expected repository metadata")
    if metadata.get("eligibility_policy") != evidence_expansion.DATA_POLICY:
        if any(key in metadata for key in ("data_blobs", "data_witnesses")):
            fail("legacy policy contains bounded data metadata")
        return
    raw_data, blobs_by_path = _validated_data_state(metadata, fail)
    entries = {entry["path"]: entry for entry in metadata["evidence_manifest"]}
    expected_witnesses, used = [], 0
    for path, blob in blobs_by_path.items():
        budget = min(data_witnesses.LIMITS["max_file_output_bytes"],
                     data_witnesses.LIMITS["max_output_bytes"] - used)
        if budget <= 0 or blob["output_budget"] != budget:
            fail("data output budget differs from deterministic selection")
        if blob.get("reason") == "credential_like_content":
            continue
        try:
            expected_blob, witnesses = data_witnesses.build(entries[path], raw_data[path], output_budget=budget)
        except (ValueError, TypeError, KeyError) as error:
            fail("invalid bounded data replay: " + str(error))
        if expected_blob != blob:
            fail("data raw provenance or deterministic coverage changed")
        expected_witnesses.extend(witnesses)
        used += sum(len(witness["text"].encode("utf-8")) for witness in witnesses)
    if metadata["data_witnesses"] != expected_witnesses:
        fail("exact data records, original offsets or sampled coverage changed")


def _validate_expansion(snapshot, inventory, segments, fail):
    policy = snapshot.get("eligibility_policy")
    if policy != evidence_expansion.DATA_POLICY and any(key in snapshot for key in ("data_blobs", "data_witnesses")):
        fail("legacy policy contains bounded data metadata")
    if policy is None:
        if any("evidence_kind" in item for item in inventory):
            fail("legacy inventory contains expansion metadata")
        return
    if policy not in evidence_expansion.SUPPORTED_POLICIES:
        fail("unknown source eligibility policy")
    entries = snapshot.get("evidence_manifest")
    if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
        fail("invalid expansion repository manifest")
    paths = []
    for entry in entries:
        if (not isinstance(entry, dict) or type(entry.get("bytes")) is not int or entry["bytes"] < 0
                or not isinstance(entry.get("mode"), str)):
            fail("malformed expansion repository entry")
        paths.append(_safe_path(entry.get("path")))
    if paths != sorted(set(paths)):
        fail("duplicate or unsorted expansion repository paths")
    by_path = {entry["path"]: entry for entry in entries}
    texts = {segment["path"]: segment["text"] for segment in segments}
    initial = [item for item in inventory if "evidence_kind" not in item]
    expected_base = {entry["path"] for entry in entries if entry["mode"] in {"100644", "100755"}
                     and not _excluded_reason(entry["path"]) and not evidence_expansion.blocked(entry["path"])}
    if {item["path"] for item in initial} != expected_base:
        fail("base source selection differs from expansion repository manifest")
    for item in inventory:
        entry = by_path.get(item["path"])
        if entry is None or item["bytes"] != entry["bytes"] or item.get("object_id") != entry.get("object_id"):
            fail("source inventory differs from expansion repository manifest")
    def read(entry):
        # Omitted binary/credential content is absent in replay; its byte hash
        # remains in inventory and it supplies no evidence or further references.
        text = texts.get(entry["path"])
        return text.encode("utf-8") if text is not None else bytes(entry["bytes"])
    data_result = {} if policy == evidence_expansion.DATA_POLICY else None
    raw_data, blobs_by_path = _validated_data_state(snapshot, fail) if data_result is not None else ({}, {})

    def replay_data(entry, budget):
        blob = blobs_by_path.get(entry["path"])
        if blob is None:
            fail("referenced bounded data acquisition missing")
        if blob.get("reason") == "credential_like_content":
            if blob["output_budget"] != budget:
                fail("credential omission output budget changed")
            return blob, []
        try:
            return data_witnesses.build(entry, raw_data[entry["path"]], output_budget=budget)
        except (ValueError, TypeError, KeyError) as error:
            fail("invalid bounded data replay: " + str(error))
    added, ledger = evidence_expansion.expand(entries, initial, read,
        text_for_item=lambda item: texts.get(item["path"]), priority=_priority,
        max_chars=snapshot.get("coverage", {}).get("max_characters", 0),
        policy=policy, data_handler=replay_data, data_result=data_result)
    expanded = [item for item in inventory if "evidence_kind" in item]
    expected = [(item["path"], item["evidence_kind"], item["evidence_order"]) for item in added]
    actual = [(item["path"], item["evidence_kind"], item.get("evidence_order")) for item in sorted(expanded, key=lambda i: i.get("evidence_order", -1))]
    if expected != actual or snapshot.get("evidence_expansion") != ledger:
        fail("directed evidence selection or need-resolution ledger changed")
    if data_result is not None and any(snapshot.get(key) != value for key, value in data_result.items()):
        fail("bounded data selection, raw provenance or exact record witnesses changed")
    _validate_dependencies(snapshot, fail)


def validate_repository(snapshot: dict) -> None:
    """Validate saved source text against its inventory and version identities.

    This detects internally inconsistent or accidentally changed replay inputs.
    It does not authenticate a newly forged, completely rehashed snapshot: the
    caller must bind this manifest and revision to its recorded ingestion run.
    """
    def fail(message):
        raise RepositoryError("Invalid repository snapshot: " + message)

    if not isinstance(snapshot, dict):
        fail("expected an object")
    for name in ("source", "source_binding", "revision", "manifest_sha256", "sha256"):
        if not isinstance(snapshot.get(name), str) or not snapshot[name]:
            fail("missing source identity")
    if not re.fullmatch(r"[0-9a-f]{64}", snapshot["source_binding"]):
        fail("invalid source binding")
    if snapshot.get("execution") != "none":
        fail("source reader must not execute repository content")
    inventory, files, segments, omitted, excluded = [snapshot.get(key) for key in ("inventory", "files", "segments", "omitted", "excluded")]
    if any(not isinstance(value, list) for value in (inventory, files, segments, omitted, excluded)):
        fail("source inventory and segments must be arrays")
    if not inventory or not segments:
        fail("no source content")
    paths = []
    for item in inventory:
        if not isinstance(item, dict) or not isinstance(item.get("included"), bool):
            fail("malformed inventory entry")
        if "evidence_kind" in item and (item["evidence_kind"] not in {"referenced_python_source", "referenced_configuration_or_task_source", "referenced_task_source_or_index"} or type(item.get("evidence_order")) is not int or item["evidence_order"] < 0):
            fail("invalid expansion inventory metadata")
        path = _safe_path(item.get("path"))
        if _excluded_reason(path) and not (snapshot.get("eligibility_policy") in evidence_expansion.SUPPORTED_POLICIES and item.get("evidence_kind") and not evidence_expansion.blocked(path)):
            fail("ineligible source path in inventory")
        if type(item.get("bytes")) is not int or item["bytes"] < 0:
            fail("invalid source byte count")
        digest = item.get("sha256")
        if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            fail("invalid source byte hash")
        if digest is None and item.get("reason") != "file_byte_limit":
            fail("unhashed source was not marked unread")
        if not item["included"] and not isinstance(item.get("reason"), str):
            fail("missing omission reason")
        paths.append(path)
    if len(set(paths)) != len(paths) or paths != sorted(paths):
        fail("duplicate or unsorted inventory paths")
    by_path = dict(zip(paths, inventory))
    for item in excluded:
        if not isinstance(item, dict) or not isinstance(item.get("reason"), str) or not isinstance(item.get("path"), str):
            fail("malformed exclusion entry")
        _safe_path(item.get("path", "").rstrip("/"))
    if excluded != sorted(excluded, key=lambda item: (item["path"], item["reason"])):
        fail("unsorted exclusions")
    expected_files = {path: item for path, item in by_path.items() if item["included"]}
    expected_omitted = {path: item for path, item in by_path.items() if not item["included"]}
    try:
        actual_files = {item["path"]: item for item in files}
        actual_omitted = {item["path"]: item for item in omitted}
    except (KeyError, TypeError):
        fail("malformed selected or omitted file list")
    if len(actual_files) != len(files) or actual_files != expected_files:
        fail("selected files do not match the source inventory")
    if len(actual_omitted) != len(omitted) or actual_omitted != expected_omitted:
        fail("omitted files do not match the source inventory")
    segment_paths, characters = [], 0
    for segment in segments:
        if not isinstance(segment, dict) or not isinstance(segment.get("text"), str):
            fail("malformed source segment")
        path = _safe_path(segment.get("path"))
        item = expected_files.get(path)
        if item is None:
            fail("segment has no selected source file")
        data = segment["text"].encode("utf-8")
        line_end = max(1, len(segment["text"].splitlines()))
        if (len(data) != item["bytes"] or _digest(data) != item["sha256"]
                or segment.get("sha256") != item["sha256"]):
            fail("source text differs from its recorded byte hash")
        if (type(segment.get("line_start")) is not int or segment["line_start"] != 1
                or type(segment.get("line_end")) is not int or segment["line_end"] != line_end
                or segment.get("id") != f"repo:{path}:L1-L{line_end}"):
            fail("source segment line range or ID changed")
        if item.get("characters") != len(segment["text"]) or item.get("line_count") != len(segment["text"].splitlines()):
            fail("source inventory text counts changed")
        if "object_id" in item:
            header = f"blob {len(data)}\0".encode()
            oid = item["object_id"]
            if not isinstance(oid, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
                fail("invalid Git blob identity")
            expected_oid = hashlib.sha1(header + data).hexdigest() if len(oid) == 40 else _digest(header + data)
            if oid != expected_oid:
                fail("source text differs from its Git blob identity")
        segment_paths.append(path)
        characters += len(segment["text"])
    if len(set(segment_paths)) != len(segment_paths) or set(segment_paths) != set(expected_files):
        fail("missing or duplicate whole-file segments")
    manifest = [{key: value for key, value in item.items() if key not in {"included", "reason"}} for item in inventory]
    try:
        manifest_sha = _manifest_hash(manifest, excluded, snapshot)
    except (KeyError, TypeError, AttributeError):
        fail("malformed source expansion provenance")
    if snapshot["manifest_sha256"] != manifest_sha or snapshot["sha256"] != manifest_sha:
        fail("source manifest changed")
    kind = snapshot.get("revision_kind")
    if kind == "content_manifest":
        if snapshot["revision"] != "content-manifest:" + manifest_sha or snapshot.get("commit") is not None or snapshot.get("tree_sha") is not None:
            fail("non-Git snapshot claims a Git identity")
    elif kind == "git_commit":
        commit = snapshot.get("commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit) or snapshot["revision"] != commit:
            fail("Git revision identity changed")
        tree = snapshot.get("tree_sha")
        if tree is None:
            if snapshot.get("commit_binding") != "github_codeload_full_commit_url" or not re.fullmatch(r"[0-9a-f]{64}", snapshot.get("archive_sha256", "")):
                fail("archive commit binding missing")
            label, _, _, remote_commit = _github_url(snapshot["source"], commit)
            if label != snapshot["source"] or remote_commit != commit:
                fail("archive source identity changed")
        elif not isinstance(tree, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", tree):
            fail("invalid Git tree identity")
        if "://" in snapshot["source"]:
            label, _, _, remote_commit = _github_url(snapshot["source"], commit)
            if label != snapshot["source"] or remote_commit != commit or snapshot["source_binding"] != _digest(label.encode()):
                fail("remote source identity changed")
            if tree is not None and snapshot.get("commit_binding") != "github_commit_tree_raw_blobs":
                fail("remote tree commit binding missing")
        if snapshot.get("commit_binding") == "github_commit_tree_raw_blobs":
            label, _, _, remote_commit = _github_url(snapshot["source"], commit)
            if label != snapshot["source"] or remote_commit != commit or tree is None:
                fail("tree source identity changed")
            entries = snapshot.get("tree_manifest")
            if snapshot.get("tree_manifest_sha256") != _canonical_hash(entries):
                fail("source tree manifest changed")
            tree_items, tree_excluded = _remote_tree(entries, tree, expand_evidence=snapshot.get("eligibility_policy") in evidence_expansion.SUPPORTED_POLICIES)
            expected_tree_items = {item["path"]: item for item in tree_items}
            if snapshot.get("eligibility_policy") in evidence_expansion.SUPPORTED_POLICIES:
                candidates = [{"path": entry["path"], "bytes": entry.get("size", 0), "mode": entry["mode"], "type": entry["type"], "object_id": entry["sha"]}
                              for entry in entries if entry["type"] != "tree"]
                if sorted(candidates, key=lambda i: i["path"]) != snapshot.get("evidence_manifest"):
                    fail("expansion repository manifest differs from pinned Git tree")
                for item in inventory:
                    if "evidence_kind" in item:
                        pinned = next(entry for entry in candidates if entry["path"] == item["path"])
                        expected_tree_items[item["path"]] = {"bytes": pinned["bytes"], "object_id": pinned["object_id"]}
                tree_excluded = [item for item in tree_excluded if item["path"] not in expected_tree_items]
            if set(expected_tree_items) != set(by_path) or tree_excluded != excluded:
                fail("source inventory is incomplete relative to its pinned tree")
            for path, item in by_path.items():
                pinned = expected_tree_items[path]
                if item["bytes"] != pinned["bytes"] or item.get("object_id") != pinned["object_id"]:
                    fail("source inventory differs from its pinned Git tree")
    else:
        fail("unknown revision kind")
    _validate_expansion(snapshot, inventory, segments, fail)
    coverage = snapshot.get("coverage")
    if not isinstance(coverage, dict) or coverage.get("inventory_complete") is not True:
        fail("missing source coverage")
    if type(coverage.get("complete")) is not bool:
        fail("invalid source coverage flag")
    expected = {"complete": not omitted, "eligible_files": len(inventory), "included_files": len(files),
                "omitted_files": len(omitted), "excluded_entries": len(excluded), "characters": characters}
    if any(coverage.get(key) != value for key, value in expected.items()):
        fail("coverage does not match source inventory")
    if type(coverage.get("max_characters")) is not int or coverage["max_characters"] < characters:
        fail("source character budget was exceeded")


def load_repository(source: str, revision: str | None = None, max_chars: int = 240000,
                    fetch_mode: str = "auto", expand_evidence: bool = True,
                    evidence_policy: str = evidence_expansion.POLICY) -> dict:
    """Return exact source segments and provenance without executing repository code.

    Local Git refs (including HEAD when omitted) resolve once to an immutable
    commit. Non-Git directories reject ``revision``. GitHub URLs require a full
    commit SHA. Selected files are kept whole; omitted source is inventoried.
    """
    if not isinstance(source, str) or not source.strip():
        raise RepositoryError("A source directory or GitHub repository URL is required")
    if type(max_chars) is not int or max_chars <= 0:
        raise RepositoryError("max_chars must be a positive integer")
    if type(expand_evidence) is not bool:
        raise RepositoryError("expand_evidence must be a boolean")
    if evidence_policy not in evidence_expansion.SUPPORTED_POLICIES:
        raise RepositoryError("Unknown source evidence policy")
    if fetch_mode not in {"auto", "files"}:
        raise RepositoryError("fetch_mode must be auto or files")
    source = source.strip()
    if "://" in source:
        label, url, name, commit = _github_url(source, revision)
        acquisition = {"requested_fetch_mode": fetch_mode}
        if fetch_mode == "files":
            acquisition.update(method="github_commit_tree_raw_blobs", attempts=[], archive_skipped=True)
            items, excluded, provenance = _github_source_snapshot(label, commit, acquisition, max_chars=max_chars, expand_evidence=expand_evidence, evidence_policy=evidence_policy)
        else:
            try:
                data = _download_archive(url, acquisition=acquisition, max_attempts=1)
            except RepositoryError as error:
                if not error.retryable and error.failure_kind != "download_limit":
                    raise
                items, excluded, provenance = _github_source_snapshot(label, commit, acquisition, max_chars=max_chars, expand_evidence=expand_evidence, evidence_policy=evidence_policy)
            else:
                try:
                    items, excluded, provenance = _archive_snapshot(data, name, commit, max_chars=max_chars, expand_evidence=expand_evidence, evidence_policy=evidence_policy)
                except RepositoryError as error:
                    error.acquisition = acquisition
                    raise
        provenance["source_acquisition"] = acquisition
        binding = _digest(label.encode())
    else:
        if fetch_mode != "auto":
            raise RepositoryError("Explicit source-file fetching requires a public GitHub source")
        supplied = Path(source).expanduser()
        if supplied.is_symlink():
            raise RepositoryError("Source directory must not be a symbolic link")
        directory = supplied.resolve()
        if not directory.is_dir():
            raise RepositoryError("Source input must be a directory")
        label = directory.name
        binding = _digest(str(directory).encode())
        is_git = (directory / ".git").exists() or ((directory / "HEAD").is_file() and (directory / "objects").is_dir())
        if is_git:
            items, excluded, provenance = _git_snapshot(directory, revision, max_chars=max_chars, expand_evidence=expand_evidence, evidence_policy=evidence_policy)
        else:
            if revision is not None:
                raise RepositoryError("Cannot verify a Git revision against a non-Git source directory")
            items, excluded, provenance = _directory_snapshot(directory, max_chars=max_chars, expand_evidence=expand_evidence, evidence_policy=evidence_policy)

    inventory, segments, included, omitted = [], [], [], []
    used_chars = 0
    for item in sorted(items, key=lambda item: (1, item["evidence_order"]) if "evidence_order" in item else (0, _priority(item["path"]))):
        metadata = {key: value for key, value in item.items() if key not in {"data", "omission_reason"}}
        text = None
        reason = item.get("omission_reason")
        if "data" in item:
            try:
                text = item["data"].decode("utf-8")
            except UnicodeDecodeError:
                reason = "not_utf8_source"
            else:
                if "\x00" in text:
                    reason = "binary_source"
                elif CREDENTIAL_CONTENT.search(text):
                    reason = "credential_like_content"
                metadata["characters"] = len(text)
                metadata["line_count"] = len(text.splitlines())
        if reason is None and used_chars + len(text) > max_chars:
            reason = "character_budget"
        if reason is not None:
            metadata.update(included=False, reason=reason)
            omitted.append(dict(metadata))
        else:
            metadata["included"] = True
            used_chars += len(text)
            included.append(dict(metadata))
            segments.append({"id": f"repo:{item['path']}:L1-L{max(1, metadata['line_count'])}",
                             "path": item["path"], "line_start": 1,
                             "line_end": max(1, metadata["line_count"]), "text": text,
                             "sha256": item["sha256"]})
        inventory.append(metadata)
    inventory.sort(key=lambda item: item["path"])
    excluded.sort(key=lambda item: (item["path"], item["reason"]))
    manifest = [{key: value for key, value in item.items() if key not in {"included", "reason"}} for item in inventory]
    manifest_sha = _manifest_hash(manifest, excluded, provenance)
    if provenance["revision_kind"] == "content_manifest":
        provenance["revision"] = "content-manifest:" + manifest_sha
    if not segments:
        raise RepositoryError("No eligible source file fits the source budget")
    snapshot = {"source": label, "source_binding": binding, **provenance,
            "manifest_sha256": manifest_sha, "sha256": manifest_sha,
            "files": included, "inventory": inventory, "segments": segments,
            "excluded": excluded, "omitted": omitted,
            "coverage": {"complete": not omitted, "inventory_complete": True,
                         "scope": "eligible UTF-8 author source plus bounded directly referenced repository evidence; unresolved dependencies and data remain unaudited" if expand_evidence else "eligible UTF-8 source files only; excluded documents, datasets, tests, labels, credentials and dependencies are not audited",
                         "reason": "All eligible source files supplied" if not omitted else "Source files omitted; this snapshot can support bounded positive findings but not whole-repository absence claims",
                         "eligible_files": len(inventory), "included_files": len(included),
                         "omitted_files": len(omitted), "excluded_entries": len(excluded),
                         "characters": used_chars, "max_characters": max_chars},
            "execution": "none"}
    validate_repository(snapshot)
    return snapshot
