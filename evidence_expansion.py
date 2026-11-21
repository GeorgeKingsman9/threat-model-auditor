"""Bounded static evidence needs; declarations here are metadata, never source.

Only references present in supplied author text can extend source eligibility.
Readers provide immutable repository entries and raw bytes. No dependencies are
installed, imported, executed, or resolved from a package registry.
"""
from __future__ import annotations

import ast
import fnmatch
import posixpath
from pathlib import PurePosixPath
import re
import sys
import warnings
import data_witnesses

POLICY = "directed-evidence-v2"
DATA_POLICY = "directed-evidence-v3"
SUPPORTED_POLICIES = {POLICY, DATA_POLICY}
VERSION = 1
LIMITS = {"max_added_files": 64, "max_added_bytes": 4 * 1024 * 1024,
          "max_config_bytes": 256 * 1024, "max_data_bytes": 64 * 1024,
          "max_template_matches": 32, "max_rounds": 8, "max_references": 1024}
CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml"}
DATA_SUFFIXES = CONFIG_SUFFIXES | {".csv", ".tsv", ".txt", ".jsonl"}
REFERENCE_SUFFIXES = DATA_SUFFIXES | {".py", ".pyi", ".npz", ".npy", ".parquet", ".arrow"}
VENDOR_DIRS = {"vendor", "third_party", "third-party"}
HARD_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
             "__pycache__", "dist", "build", "target", "test", "tests", "fixtures",
             "cases", "research", "adjudication", "reports", "results", "outputs",
             "artifacts", "benchmarks", "docs", "documentation", "notebooks",
             ".aws", ".ssh", ".codex"}
SENSITIVE = re.compile(r"(?:^|[._-])(?:credentials?|secrets?|tokens?|passwords?|private[_-]?keys?|api[_-]?keys?|gold|labels?|verdicts?|adjudicat\w*|pilot[_-]?results?)(?:[._-]|$)", re.I)
_QUOTED = re.compile(r'''["']([^"'\r\n]+)["']''')


def blocked(path):
    """Hard exclusions cannot be overridden by an untrusted source reference."""
    parts = PurePosixPath(path).parts
    return (not parts or path.startswith("/") or "\\" in path
            or any(p in {"", ".", ".."} or p.startswith(".") or SENSITIVE.search(p)
                   or any(ord(c) < 32 or ord(c) == 127 for c in p) for p in parts)
            or any(p.lower() in HARD_DIRS for p in parts[:-1]))


def candidate_kind(path, kind):
    if blocked(path):
        return None
    suffix = PurePosixPath(path).suffix.lower()
    if kind == "import" and suffix in {".py", ".pyi"}:
        return "referenced_python_source"
    if kind == "path" and suffix in {".py", ".pyi"}:
        return "referenced_python_source"
    if suffix in CONFIG_SUFFIXES and kind in {"path", "template"}:
        return "referenced_configuration_or_task_source"
    if suffix in DATA_SUFFIXES and kind == "path":
        return "referenced_task_source_or_index"
    return None


def _normal(value):
    if not isinstance(value, str) or not value or "\\" in value or "://" in value or "\x00" in value:
        return None
    if value.startswith(("/", "~")):
        return None
    result = posixpath.normpath(value)
    if result in {".", ".."} or result.startswith("../"):
        return None
    return result


def _pathlike(value):
    return (isinstance(value, str) and len(value) <= 400 and not any(c in value for c in "\n\r\t")
            and ("/" in value or PurePosixPath(value).suffix.lower() in REFERENCE_SUFFIXES)
            and not any(c in value for c in ("://", " ", "[", "]", "<", ">")))


def references(path, text):
    """Extract literal syntax only, with original author line numbers."""
    refs = []
    def add(kind, value, line, relative=False):
        if isinstance(value, str):
            refs.append({"from_path": path, "line": line, "kind": kind, "reference": value,
                         **({"relative_to_source": True} if relative else {})})

    if PurePosixPath(path).suffix.lower() in {".py", ".pyi"}:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                tree = ast.parse(text.lstrip("\ufeff"))
        except (SyntaxError, ValueError, RecursionError):
            return [{"from_path": path, "line": 1, "kind": "parse", "reference": "python_syntax_not_statically_parsed"}]
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] not in sys.stdlib_module_names:
                        add("import", alias.name, node.lineno)
            elif isinstance(node, ast.ImportFrom):
                module = "." * node.level + (node.module or "")
                if node.level or module.split(".")[0] not in sys.stdlib_module_names:
                    if node.module:
                        add("import", module, node.lineno)
                    for alias in node.names:
                        if alias.name != "*":
                            add("import", module + ("." if node.module else "") + alias.name, node.lineno)
            elif isinstance(node, ast.Call):
                name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
                if name in {"import_module", "__import__"} and node.args and isinstance(node.args[0], ast.Constant):
                    add("import", node.args[0].value, node.lineno)
                # Restricted __file__ joins, never eval/execute source expressions.
                if name == "join" and node.args:
                    first = ast.unparse(node.args[0])
                    if "dirname(__file__)" in first and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in node.args[1:]):
                        add("path", posixpath.join(*(a.value for a in node.args[1:])), node.lineno, True)
            elif isinstance(node, ast.JoinedStr):
                value = "".join(a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else "*" for a in node.values)
                # Finite config templates only, never dataset expansion.
                if "*" in value and PurePosixPath(value).suffix.lower() in REFERENCE_SUFFIXES:
                    if value.split("*", 1)[0] and PurePosixPath(value).suffix.lower() in CONFIG_SUFFIXES:
                        add("template", value, node.lineno)
                    else:
                        add("dynamic_path", value, node.lineno)
            elif isinstance(node, ast.Constant) and _pathlike(node.value):
                if not node.value.startswith("../"):
                    add("path", node.value, node.lineno)
    elif PurePosixPath(path).suffix.lower() in DATA_SUFFIXES:
        # Quoted scalar paths in JSON/YAML/TOML; no YAML constructors or plugins.
        for line, raw in enumerate(text.splitlines(), 1):
            for match in _QUOTED.finditer(raw):
                if _pathlike(match.group(1)):
                    add("path", match.group(1), line)
    elif PurePosixPath(path).suffix.lower() in {".sh", ".bash", ".zsh"}:
        for line, raw in enumerate(text.splitlines(), 1):
            if raw.lstrip().startswith("#"):
                continue
            for match in re.finditer(r"(?:[\w.-]+/)+[\w.-]+\.(?:json|ya?ml|toml|csv|tsv|txt|py)\b", raw):
                add("path", match.group(), line)
    # Identical references from the same line need only one proof edge.
    return sorted({tuple(sorted(r.items())): r for r in refs}.values(),
                  key=lambda r: (r["from_path"], r["line"], r["kind"], r["reference"]))


def resolve(ref, entries):
    """Resolve paths against this inventory only, without network/package lookup."""
    path, value, kind = ref["from_path"], ref["reference"], ref["kind"]
    if kind == "parse":
        return [], "syntax_not_resolved"
    if kind == "dynamic_path":
        return [], "dynamic_data_path_not_resolved"
    parent = posixpath.dirname(path)
    if kind == "import":
        dots = len(value) - len(value.lstrip("."))
        module = value[dots:].replace(".", "/")
        if dots:
            root = parent
            for _ in range(dots - 1): root = posixpath.dirname(root)
            roots = [root]
        else:
            roots = ["", parent]
            ancestor = parent
            while ancestor:
                ancestor = posixpath.dirname(ancestor)
                roots.append(ancestor)
        choices = []
        for root in dict.fromkeys(roots):
            stem = posixpath.join(root, module)
            choices.extend([stem + ".py", stem + ".pyi", stem + "/__init__.py"])
        matches = [p for p in dict.fromkeys(choices) if p in entries]
        if not matches and not dots:
            # Vendored import roots do not need to be installed or on sys.path.
            tails = ("/" + module + ".py", "/" + module + "/__init__.py")
            matches = [p for p in entries if p.endswith(tails) and any(c.lower() in VENDOR_DIRS for c in PurePosixPath(p).parts[:-1])]
            if len(matches) > 1:
                return [], "ambiguous_import_root"
        return matches, None if matches else "module_not_in_pinned_repository"
    paths = []
    roots = [parent] if ref.get("relative_to_source") or value.startswith("../") else ["", parent]
    for root in roots:
        target = _normal(posixpath.join(root, value))
        if target and target not in paths: paths.append(target)
    if not paths:
        return [], "path_outside_repository_or_nonliteral"
    if kind == "template":
        # * represents one path component, not recursive glob traversal.
        matches = sorted(p for p in entries if any(fnmatch.fnmatchcase(p, pattern) and p.count("/") == pattern.count("/") for pattern in paths))
        if len(matches) > LIMITS["max_template_matches"]:
            return [], "template_match_limit"
        return matches, None if matches else "template_not_in_pinned_repository"
    matches = [p for p in paths if p in entries]
    if matches:
        return matches[:1], None
    if any(any(p.startswith(root + "/") for p in entries) for root in paths):
        return [], "directory_reference_no_bulk_read"
    return [], "path_not_in_pinned_repository"


def expand(entries, initial_items, read, *, text_for_item, priority, max_chars,
           policy=POLICY, data_handler=None, data_result=None):
    """Return extra exact files and an explicit bounded need-resolution ledger."""
    if policy not in SUPPORTED_POLICIES:
        raise ValueError("Unknown directed evidence policy")
    if policy == DATA_POLICY and (data_handler is None or data_result is None):
        raise ValueError("Bounded data policy needs an explicit acquisition handler")
    entries = {entry["path"]: entry for entry in entries}
    known = {item["path"] for item in initial_items}
    added, needs, pending, inspected = [], [], [], set()
    used_chars = 0
    for item in sorted(initial_items, key=lambda item: priority(item["path"])):
        text = text_for_item(item)
        if text is not None and used_chars + len(text) <= max_chars:
            used_chars += len(text)
            pending.append((item["path"], text))
    added_bytes = 0
    data_seen, data_bytes, data_output = {}, 0, 0
    if data_result is not None:
        data_result.update(data_blobs=[], data_witnesses=[])
    for round_number in range(LIMITS["max_rounds"]):
        next_pending = []
        for path, text in pending:
            inspected.add(path)
            for ref in references(path, text):
                if len(needs) >= LIMITS["max_references"]:
                    needs.append({"from_path": path, "line": ref["line"], "kind": "limit", "reference": "remaining_references", "status": "unresolved", "reason": "reference_limit"})
                    pending = []
                    break
                targets, failure = resolve(ref, entries)
                if failure:
                    needs.append({**ref, "status": "unresolved", "reason": failure})
                for target in targets:
                    edge = {**ref, "target": target}
                    entry = entries[target]
                    evidence_kind = candidate_kind(target, ref["kind"])
                    reason = None
                    if entry.get("mode") not in {"100644", "100755"}:
                        reason = "submodule_or_nonregular_boundary"
                    elif target in known:
                        needs.append({**edge, "status": "already_eligible"})
                        continue
                    elif evidence_kind is None:
                        reason = "hard_exclusion_or_unsupported_type"
                    else:
                        count = entry["bytes"]
                        is_data = (policy == DATA_POLICY and PurePosixPath(target).suffix.lower() == ".json"
                                   and (count > LIMITS["max_data_bytes"] or any(
                                       p.lower() in {"data", "datasets"} for p in PurePosixPath(target).parts[:-1])))
                        if is_data:
                            if ref["kind"] != "path":
                                reason = "data_template_no_bulk_read"
                            elif target in data_seen:
                                needs.append({**edge, **data_seen[target]})
                                continue
                            elif count > data_witnesses.LIMITS["max_file_bytes"]:
                                reason = "data_file_byte_limit"
                            elif len(data_seen) >= data_witnesses.LIMITS["max_files"]:
                                reason = "data_file_limit"
                            elif data_bytes + count > data_witnesses.LIMITS["max_total_bytes"]:
                                reason = "data_total_byte_limit"
                            elif data_output >= data_witnesses.LIMITS["max_output_bytes"]:
                                reason = "data_output_byte_limit"
                            else:
                                budget = min(data_witnesses.LIMITS["max_file_output_bytes"],
                                             data_witnesses.LIMITS["max_output_bytes"] - data_output)
                                blob, witnesses = data_handler(entry, budget)
                                data_result["data_blobs"].append(blob)
                                data_result["data_witnesses"].extend(witnesses)
                                data_bytes += count
                                data_output += sum(len(w["text"].encode("utf-8")) for w in witnesses)
                                outcome = ({"status": "resolved_data_witness"} if witnesses else
                                           {"status": "unresolved", "reason": blob["reason"]})
                                data_seen[target] = outcome
                                needs.append({**edge, **outcome})
                                # Records and schema references never extend eligibility.
                                continue
                            needs.append({**edge, "status": "unresolved", "reason": reason})
                            continue
                        cap = LIMITS["max_config_bytes"] if evidence_kind == "referenced_configuration_or_task_source" and not any(p.lower() in {"data", "datasets"} for p in PurePosixPath(target).parts[:-1]) else LIMITS["max_data_bytes"]
                        if evidence_kind == "referenced_python_source": cap = 2 * 1024 * 1024
                        if count > cap: reason = "referenced_file_byte_limit"
                        elif len(added) >= LIMITS["max_added_files"]: reason = "expanded_file_limit"
                        elif added_bytes + count > LIMITS["max_added_bytes"]: reason = "expanded_total_byte_limit"
                        elif used_chars + count > max_chars: reason = "expansion_character_budget"
                    if reason:
                        needs.append({**edge, "status": "unresolved", "reason": reason})
                        continue
                    raw = read(entry)
                    if len(raw) != entry["bytes"]:
                        raise ValueError("Referenced raw byte size differs from repository inventory")
                    item = {key: value for key, value in entry.items() if key not in {"mode", "type"}}
                    import hashlib
                    item.update(data=raw, sha256=hashlib.sha256(raw).hexdigest(), evidence_kind=evidence_kind,
                                evidence_order=len(added))
                    known.add(target); added.append(item); added_bytes += len(raw)
                    needs.append({**edge, "status": "resolved"})
                    content = text_for_item(item)
                    if content is not None:
                        used_chars += len(content)
                        next_pending.append((target, content))
            if needs and needs[-1].get("reason") == "reference_limit": break
        if not next_pending or (needs and needs[-1].get("reason") == "reference_limit"):
            pending = []
            break
        pending = next_pending
    for path, _ in pending:
        if path not in inspected:
            needs.append({"from_path": path, "line": 1, "kind": "limit", "reference": "uninspected_references", "status": "unresolved", "reason": "expansion_round_limit"})
    return added, {"version": VERSION, "policy": policy, "limits": dict(LIMITS),
                   "derivation": "static reference metadata only; source evidence remains exact raw-byte segments",
                   "needed": needs, "unresolved": [n for n in needs if n["status"] == "unresolved"],
                   "over_limit": [n for n in needs if n.get("reason", "").endswith(("limit", "budget"))],
                   "added_files": len(added), "added_bytes": added_bytes,
                   "inspected_paths": sorted(inspected),
                   **({"data_policy": data_witnesses.POLICY, "data_limits": dict(data_witnesses.LIMITS),
                       "data_files": len(data_seen), "data_bytes": data_bytes,
                       "data_output_bytes": data_output,
                       "data_coverage_complete": all(blob.get("coverage", {}).get("complete") is True
                                                     for blob in data_result["data_blobs"])
                                                 and not any(n["status"] == "unresolved" for n in needs)}
                      if policy == DATA_POLICY else {})}
