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


def _git_snapshot(directory, revision):
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
    items, excluded = [], []
    total_read = 0
    for entry in entries:
        try:
            header, encoded = entry.split(b"\t", 1)
            mode, kind, oid, size = header.decode("ascii").split()
            path = _safe_path(encoded.decode("utf-8"))
        except (ValueError, UnicodeError) as error:
            raise RepositoryError("Malformed or unsupported Git tree path") from error
        reason = _excluded_reason(path)
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
    return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit, "tree_sha": tree}


def _directory_snapshot(directory):
    items, excluded = [], []
    total_read, entries = 0, 0

    def walk_error(error):
        raise RepositoryError("Could not inventory the complete source directory") from error

    for base, dirs, names in os.walk(directory, followlinks=False, onerror=walk_error):
        dirs.sort()
        names.sort()
        kept = []
        for name in dirs:
            current = Path(base) / name
            path = _safe_path(current.relative_to(directory).as_posix())
            if current.is_symlink() or name.lower() in EXCLUDED_DIRS or name.startswith(".") or SENSITIVE_NAME.search(name):
                excluded.append({"path": path + "/", "reason": "symlink_or_excluded_directory"})
            else:
                kept.append(name)
        dirs[:] = kept
        entries += len(dirs) + len(names)
        if entries > MAX_ENTRIES:
            raise RepositoryError("Repository has too many entries")
        for name in names:
            current = Path(base) / name
            path = _safe_path(current.relative_to(directory).as_posix())
            reason = _excluded_reason(path)
            if current.is_symlink():
                reason = "symlink"
            if reason:
                excluded.append({"path": path, "reason": reason})
                continue
            try:
                descriptor = os.open(current, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
                with os.fdopen(descriptor, "rb") as stream:
                    info = os.fstat(stream.fileno())
                    if not stat.S_ISREG(info.st_mode):
                        excluded.append({"path": path, "reason": "not_regular_file"})
                        continue
                    item = {"path": path, "bytes": info.st_size, "sha256": None}
                    if info.st_size > MAX_FILE_BYTES:
                        item["omission_reason"] = "file_byte_limit"
                    else:
                        total_read += info.st_size
                        if total_read > MAX_READ_BYTES:
                            raise RepositoryError("Eligible source content exceeds its total byte limit")
                        data = stream.read(MAX_FILE_BYTES + 1)
                        if len(data) != info.st_size:
                            raise RepositoryError("Source file changed while its snapshot was read")
                        item.update(data=data, sha256=_digest(data))
            except OSError as error:
                raise RepositoryError("Could not safely read a regular source file") from error
            items.append(item)
    return items, excluded, {"revision_kind": "content_manifest", "commit": None, "tree_sha": None}


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


def _archive_snapshot(data, repository_name, commit):
    if len(data) > MAX_DOWNLOAD_BYTES:
        raise RepositoryError("Source archive exceeds its download limit")
    items, excluded, seen = [], [], set()
    total_expanded, total_read = 0, 0
    prefix = repository_name + "-" + commit
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r|gz") as archive:
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
                reason = _excluded_reason(path)
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
    except (tarfile.TarError, OSError, EOFError) as error:
        raise RepositoryError("Invalid or truncated source archive") from error
    if not items:
        raise RepositoryError("Source archive has no eligible source files")
    return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit,
                             "tree_sha": None, "commit_binding": "github_codeload_full_commit_url",
                             "archive_sha256": _digest(data)}


def _remote_tree(entries, tree_sha):
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
        reason = _excluded_reason(path)
        if entry["mode"] not in {"100644", "100755"} or entry["type"] != "blob":
            reason = "symlink_or_submodule"
        if reason:
            excluded.append({"path": path, "reason": reason})
        else:
            items.append({"path": path, "bytes": entry["size"], "object_id": entry["sha"], "sha256": None})
    return items, excluded


def _github_source_snapshot(label, commit, acquisition):
    """Read only eligible blobs after an archive transport/size failure.

    The recursive tree must be complete and hash-correct. Every eligible blob
    within the original per-file bound must be read and hash-checked, or the
    entire acquisition fails. Character-budget selection still happens later.
    """
    fallback = {"method": "github_commit_tree_raw_blobs", "max_source_files": SOURCE_ONLY_MAX_FILES,
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
        items, excluded = _remote_tree(entries, tree_sha)
        readable = [item for item in items if item["bytes"] <= MAX_FILE_BYTES]
        if not items or len(readable) > SOURCE_ONLY_MAX_FILES:
            raise RepositoryError("Source-only acquisition exceeds its eligible file limit or has no source")
        if sum(item["bytes"] for item in readable) > min(MAX_READ_BYTES, MAX_DOWNLOAD_BYTES):
            raise RepositoryError("Eligible source content exceeds its total byte limit")
        for item in items:
            if item["bytes"] > MAX_FILE_BYTES:
                item["omission_reason"] = "file_byte_limit"

        def blob(item):
            url = "https://raw.githubusercontent.com/" + owner_repo + "/" + commit + "/" + quote(item["path"], safe="/")
            raw = read(url, "blob", min(MAX_FILE_BYTES, item["bytes"]), item["path"])
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
        fallback.update(status="succeeded", eligible_files=len(items), fetched_files=len(readable), tree_sha=tree_sha)
        return items, excluded, {"revision_kind": "git_commit", "revision": commit, "commit": commit,
            "tree_sha": tree_sha, "commit_binding": "github_commit_tree_raw_blobs",
            "tree_manifest": entries, "tree_manifest_sha256": _canonical_hash(entries)}
    except (RepositoryError, TypeError, KeyError, ValueError) as error:
        fallback["status"] = "failed"
        if not isinstance(error, RepositoryError):
            error = RepositoryError("Malformed GitHub source tree metadata")
        error.acquisition = acquisition
        raise error


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
        path = _safe_path(item.get("path"))
        if _excluded_reason(path):
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
    manifest_sha = _canonical_hash({"eligible_source": manifest, "excluded": excluded})
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
            tree_items, tree_excluded = _remote_tree(entries, tree)
            expected_tree_items = {item["path"]: item for item in tree_items}
            if set(expected_tree_items) != set(by_path) or tree_excluded != excluded:
                fail("source inventory is incomplete relative to its pinned tree")
            for path, item in by_path.items():
                pinned = expected_tree_items[path]
                if item["bytes"] != pinned["bytes"] or item.get("object_id") != pinned["object_id"]:
                    fail("source inventory differs from its pinned Git tree")
    else:
        fail("unknown revision kind")
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
                    fetch_mode: str = "auto") -> dict:
    """Return exact source segments and provenance without executing repository code.

    Local Git refs (including HEAD when omitted) resolve once to an immutable
    commit. Non-Git directories reject ``revision``. GitHub URLs require a full
    commit SHA. Selected files are kept whole; omitted source is inventoried.
    """
    if not isinstance(source, str) or not source.strip():
        raise RepositoryError("A source directory or GitHub repository URL is required")
    if type(max_chars) is not int or max_chars <= 0:
        raise RepositoryError("max_chars must be a positive integer")
    if fetch_mode not in {"auto", "files"}:
        raise RepositoryError("fetch_mode must be auto or files")
    source = source.strip()
    if "://" in source:
        label, url, name, commit = _github_url(source, revision)
        acquisition = {"requested_fetch_mode": fetch_mode}
        if fetch_mode == "files":
            acquisition.update(method="github_commit_tree_raw_blobs", attempts=[], archive_skipped=True)
            items, excluded, provenance = _github_source_snapshot(label, commit, acquisition)
        else:
            try:
                data = _download_archive(url, acquisition=acquisition, max_attempts=1)
            except RepositoryError as error:
                if not error.retryable and error.failure_kind != "download_limit":
                    raise
                items, excluded, provenance = _github_source_snapshot(label, commit, acquisition)
            else:
                try:
                    items, excluded, provenance = _archive_snapshot(data, name, commit)
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
            items, excluded, provenance = _git_snapshot(directory, revision)
        else:
            if revision is not None:
                raise RepositoryError("Cannot verify a Git revision against a non-Git source directory")
            items, excluded, provenance = _directory_snapshot(directory)

    inventory, segments, included, omitted = [], [], [], []
    used_chars = 0
    for item in sorted(items, key=lambda item: _priority(item["path"])):
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
    manifest_sha = _canonical_hash({"eligible_source": manifest, "excluded": excluded})
    if provenance["revision_kind"] == "content_manifest":
        provenance["revision"] = "content-manifest:" + manifest_sha
    if not segments:
        raise RepositoryError("No eligible source file fits the source budget")
    snapshot = {"source": label, "source_binding": binding, **provenance,
            "manifest_sha256": manifest_sha, "sha256": manifest_sha,
            "files": included, "inventory": inventory, "segments": segments,
            "excluded": excluded, "omitted": omitted,
            "coverage": {"complete": not omitted, "inventory_complete": True,
                         "scope": "eligible UTF-8 source files only; excluded documents, datasets, tests, labels, credentials and dependencies are not audited",
                         "reason": "All eligible source files supplied" if not omitted else "Source files omitted; this snapshot can support bounded positive findings but not whole-repository absence claims",
                         "eligible_files": len(inventory), "included_files": len(included),
                         "omitted_files": len(omitted), "excluded_entries": len(excluded),
                         "characters": used_chars, "max_characters": max_chars},
            "execution": "none"}
    validate_repository(snapshot)
    return snapshot
