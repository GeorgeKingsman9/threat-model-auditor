"""Bounded, code-only *candidate* inputs for a static information-flow audit.

This is an obligation-discovery heuristic, not a receipt or policy checker. It
never executes source, imports the target repository, reads a paper, or consults
paper/repository identities. Names suggest channels and recipient roles; even a
fully traced candidate remains a candidate until independently reviewed.

Python assignments, parameters, imported local wrappers and argument bindings
are followed conservatively. Dynamic dispatch, control flow and runtime branch
selection are deliberately unresolved. The inventory is bounded and cannot
establish whole-repository closure, including when ``truncated`` is false.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import defaultdict
from pathlib import PurePosixPath


CHANNEL_KINDS = ("question", "task", "documents", "labels", "feedback", "other")
_WORDS = {
    "question": {"question", "questions", "query", "queries"},
    "task": {"task", "tasks", "instruction", "instructions", "objective", "objectives"},
    "documents": {"document", "documents", "doc", "docs", "context", "contexts", "source", "sources", "passage", "passages"},
    "labels": {"label", "labels", "answer", "answers"},
    "feedback": {"feedback", "reward", "rewards", "loss", "losses", "score", "scores", "gradient", "gradients"},
}
_GENERIC_INPUT = {"prompt", "prompts", "messages", "message", "input", "inputs", "data", "record", "records", "text", "texts"}
_CONSTRUCTOR = {"generate", "generation", "construct", "constructor", "build", "craft"}
_OPTIMIZER = {"optimize", "optimizer", "optimise", "optimization", "optimisation"}
_EVALUATOR = {"eval", "evaluate", "evaluation", "evaluator", "validate", "validation", "test", "judge", "classifier"}
_REQUEST = {"request", "complete", "completion", "completions", "chat", "invoke", "predict", "forward"}
_UTILITIES = {"print", "len", "any", "all", "sum", "min", "max", "abs", "round", "isinstance", "hasattr", "getattr", "range", "enumerate", "zip", "list", "dict", "set", "tuple", "str", "int", "float", "bool", "open", "append", "extend", "items", "keys", "values", "get", "load", "loads", "read", "write", "dump", "dumps", "join", "format", "split", "strip", "replace", "save", "sort", "sorted", "reshape", "to", "detach", "clone"}
_METADATA_ARGUMENTS = {"model", "model_name", "model_id", "model_path", "tokenizer", "tokenizer_name", "device",
                       "temperature", "top_p", "top_k", "max_tokens", "max_new_tokens", "max_n_tokens", "seed",
                       "batch_size", "num_workers", "log", "logger", "logging", "config", "configuration",
                       "url", "uri", "endpoint", "headers", "path", "cancellation_token"}
_METADATA_CALLEES = {"logger", "logging", "log", "wandb", "wandblogger", "config", "configuration", "settings"}
_INFRA_CALLEES = {"docker", "container", "containers", "image", "images", "plot", "plt", "ax", "fig", "figure", "subprocess", "asyncio", "argparse", "random", "storage", "progress", "collection", "col"}
_EXECUTION_VERBS = {"run", "step", "fit", "update", "search", "solve", "attack", "forward"}


def _metadata_name(value):
    words = _tokens(value)
    return bool(words & {"index", "indices", "idx", "position", "pos", "permutation", "permutations", "config", "configuration"})
_DECLARATIVE_SUFFIXES = {".json", ".jsonl", ".ndjson", ".yaml", ".yml", ".toml", ".ini", ".cfg",
                         ".csv", ".tsv", ".txt", ".md", ".rst", ".xml", ".bib", ".lock"}


def _tokens(value):
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return set(re.findall(r"[a-z]+", value.lower()))


def _kind(value):
    words = _tokens(value)
    # Query and document names take precedence over incidental target/loss
    # prefixes: target_train_question is one question channel, not a label.
    return next((kind for kind in CHANNEL_KINDS[:-1] if words & _WORDS[kind]),
                "labels" if words in ({"target"}, {"targets"}, {"expected"}, {"target", "output"}, {"target", "response"})
                else "other" if words & _GENERIC_INPUT else None)


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _dotted(node.value) + "." + node.attr
    return ""


class _File:
    def __init__(self, part, tree):
        self.part, self.tree = part, tree
        self.text = part["text"]
        self.lines = self.text.splitlines(keepends=True)
        self.starts = [0]
        for line in self.lines:
            self.starts.append(self.starts[-1] + len(line))
        self.scope = {}
        self.parents = {}
        self.assignments = defaultdict(list)
        self.functions = {}
        self.imports = {}
        self.calls = []
        self._index(tree, "", None)

    def span(self, node):
        def offset(row, column):
            line = self.lines[row - 1]
            return self.starts[row - 1] + len(line.encode("utf-8")[:column].decode("utf-8"))
        return offset(node.lineno, node.col_offset), offset(node.end_lineno, node.end_col_offset)

    def expr(self, node):
        start, end = self.span(node)
        return self.text[start:end]

    def cite(self, node):
        """Return a short literal quote, preferring unique statement context."""
        start, end = self.span(node)
        chosen = self.text[start:end]
        parent = node
        while (len(chosen) > 300 or self.text.count(chosen) != 1) and parent in self.parents:
            parent = self.parents[parent]
            a, b = self.span(parent) if hasattr(parent, "lineno") else (0, len(self.text))
            if b - a <= 300:
                start, end, chosen = a, b, self.text[a:b]
            elif len(chosen) <= 300:
                break
        if len(chosen) > 300:
            # A partial call is still literal candidate evidence; coverage
            # validation will require a valid exact code citation at this span.
            chosen = chosen[:300]
            end = start + len(chosen)
        return {"segment_id": self.part["id"], "quote": chosen}

    def anchor(self, node):
        start, end = self.span(node)
        return {"segment_id": self.part["id"], "start": start, "end": end,
                "line_start": self.part.get("line_start", 1) + node.lineno - 1,
                "line_end": self.part.get("line_start", 1) + node.end_lineno - 1}

    def _index(self, node, scope, parent):
        self.scope[node] = scope
        if parent is not None:
            self.parents[node] = parent
        child_scope = scope
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = scope + "." + node.name if scope else node.name
            self.functions[name] = node
            child_scope = name
        elif isinstance(node, ast.ClassDef):
            child_scope = scope + "." + node.name if scope else node.name
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                self.imports[alias.asname or alias.name] = (node.module or "", alias.name, node.level, node)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                self.imports[alias.asname or alias.name] = (alias.name, "", 0, node)
        elif isinstance(node, ast.Call):
            self.calls.append(node)
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for name in ast.walk(target):
                    if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store):
                        self.assignments[(scope, name.id)].append((node, node.value))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            for name in ast.walk(node.target):
                if isinstance(name, ast.Name):
                    self.assignments[(scope, name.id)].append((node, node.iter))
        for child in ast.iter_child_nodes(node):
            self._index(child, child_scope, node)


def _unique(records):
    seen, result = set(), []
    for record in records:
        key = json.dumps(record, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result


class _Discovery:
    def __init__(self, files, limits):
        self.files, self.limits = files, limits
        self.candidates = {}
        self.truncated = False
        self.steps = 0
        self.visits = 0
        self.max_steps = limits["max_ast_nodes"] * 4
        self.called_functions = set()
        self.issues = set()

    def resolve(self, file, call):
        name = _dotted(call.func)
        scope = file.scope[call]
        receiver, _, method = name.partition(".")
        if receiver in {"self", "cls"} and method and "." in scope:
            candidate = scope.rsplit(".", 1)[0] + "." + method
            if candidate in file.functions:
                return file, candidate, []
        for candidate in (scope + "." + name if scope else name, name):
            if candidate in file.functions:
                return file, candidate, []
        first, _, rest = name.partition(".")
        imported = file.imports.get(first)
        if imported:
            module, symbol, level, node = imported
            relative = PurePosixPath(file.part["path"]).parent
            if level:
                for _ in range(level - 1):
                    relative = relative.parent
                paths = [str(relative / module.replace(".", "/"))]
            else:
                paths = [module.replace(".", "/"), str(relative / module.replace(".", "/"))]
            target = ".".join(value for value in (symbol, rest) if value)
            for path in paths:
                for suffix in (".py", "/__init__.py"):
                    other = self.files.get(path + suffix)
                    if other and target in other.functions:
                        return other, target, [file.cite(node)]
        return None

    def _origin(self, file, node, kind, symbol=None):
        return {"kind": kind, "symbol": symbol or file.expr(node),
                "source_citation": file.cite(node), "source_anchor": file.anchor(node),
                "bindings": []}

    def trace(self, file, node, env, depth=0, seen=frozenset()):
        self.steps += 1
        if self.steps > self.max_steps:
            self.truncated = True
            self.issues.add("trace_step_limit")
            return []
        if depth > self.limits["max_trace_depth"]:
            self.truncated = True
            self.issues.add("trace_depth_limit")
            return []
        if node is None:
            return []
        name = _dotted(node)
        if isinstance(node, ast.Name):
            if name in env:
                return env[name]
            scope = file.scope[node]
            key = (file.part["id"], scope, name)
            if key not in seen:
                scopes = [scope, ""] if scope else [""]
                for lookup_scope in scopes:
                    definitions = [(statement, value) for statement, value in file.assignments[(lookup_scope, name)]
                                   if statement.lineno <= node.lineno and value is not node]
                    if definitions:
                        statement, value = definitions[-1]
                        origins = self.trace(file, value, env, depth + 1, seen | {key})
                        if origins:
                            explicit_kind = _kind(name)
                            if explicit_kind and explicit_kind != "other":
                                # A question selected with an index remains a
                                # question candidate, not a label/metadata
                                # channel merely because its selector is named
                                # target_data_indices. The assignment is the
                                # exact candidate representation boundary.
                                targets = [target for target in ast.walk(statement)
                                           if isinstance(target, ast.Name) and target.id == name
                                           and isinstance(target.ctx, ast.Store)]
                                target = targets[0] if targets else node
                                origin = self._origin(file, target, explicit_kind, name)
                                origin["bindings"] = _unique([cite for item in origins for cite in
                                                              item["bindings"] + [item["source_citation"]]]
                                                             + [file.cite(statement)])[-6:]
                                return [origin]
                            return [{**origin, "bindings": _unique(origin["bindings"] + [file.cite(statement)])[-6:]}
                                    for origin in origins]
            kind = _kind(name)
            return [self._origin(file, node, kind)] if kind else []
        if isinstance(node, (ast.Attribute, ast.Subscript)):
            specific = node.attr if isinstance(node, ast.Attribute) else (
                node.slice.value if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str) else "")
            kind = _kind(specific)
            if kind:
                return [self._origin(file, node, kind)]
        if isinstance(node, ast.Constant):
            # Literal prose, labels, paths and comments cannot self-create
            # an information channel. Dictionary keys are handled below.
            return []
        if isinstance(node, ast.Dict):
            origins = []
            for key, value in zip(node.keys, node.values):
                values = self.trace(file, value, env, depth, seen)
                if not values and isinstance(key, ast.Constant) and isinstance(key.value, str) and _kind(key.value):
                    if not isinstance(value, ast.Constant):
                        values = [self._origin(file, value, _kind(key.value))]
                origins.extend(values)
            return _unique(origins)[:16]
        if isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Attribute) and node.func.attr == "get" and node.args
                    and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)):
                kind = _kind(node.args[0].value)
                if kind:
                    return [self._origin(file, node, kind)]
            # Strings used as formatting templates do not become origins.
            children = list(node.args) + [keyword.value for keyword in node.keywords]
            resolved = self.resolve(file, node)
            if resolved and depth < self.limits["max_trace_depth"]:
                other, function, imports = resolved
                local = self.bind(file, node, other, function, env, depth + 1)
                key = (other.part["id"], function, "return")
                if key not in seen:
                    returns = [child for child in ast.walk(other.functions[function])
                               if isinstance(child, ast.Return) and other.scope[child] == function]
                    values = [origin for result in returns for origin in
                              self.trace(other, result.value, local, depth + 1, seen | {key})]
                    if values:
                        return [{**origin, "bindings": _unique(origin["bindings"] + imports + [file.cite(node)])[-6:]}
                                for origin in values]
        else:
            children = list(ast.iter_child_nodes(node))
        return _unique([origin for child in children for origin in
                        self.trace(file, child, env, depth, seen)])[:16]

    def bind(self, caller, call, callee, function, env, depth):
        definition = callee.functions[function]
        parameters = definition.args.posonlyargs + definition.args.args
        if (parameters and parameters[0].arg in {"self", "cls"}
                and isinstance(call.func, ast.Attribute)
                and _dotted(call.func.value) in {"self", "cls"}):
            parameters = parameters[1:]
        result = {}
        for parameter, argument in zip(parameters, call.args):
            result[parameter.arg] = self.trace(caller, argument, env, depth)
        for keyword in call.keywords:
            if keyword.arg:
                result[keyword.arg] = self.trace(caller, keyword.value, env, depth)
        return result

    def sink_hint(self, file, call, origins):
        callee = _dotted(call.func)
        words = _tokens(callee)
        scope_words = _tokens(file.scope[call]) | _tokens(file.part["path"])
        last = callee.rsplit(".", 1)[-1]
        if (last in _UTILITIES or words & (_METADATA_CALLEES | _INFRA_CALLEES)
                or "tokenizer" in words or last in {"__init__", "__new__"}
                or (last and last[0].isupper())):
            return None
        model_create = bool(words & {"create"} and words & {"model", "llm", "backend", "client", "chat", "completions", "responses"})
        model_call = bool(words & {"call"} and words & {"model", "llm"})
        request = bool(words & _REQUEST) or model_create or model_call
        # These operations prepare/parse a request instead of delivering it.
        if words & {"parse", "format", "formatted", "template", "normalize", "normalise"}:
            return None
        if words & {"build"} and words & {"prompt", "input", "classifier"}:
            return None
        if words & _EVALUATOR and (words & (_CONSTRUCTOR | _OPTIMIZER | {"attack"}) or request):
            return "evaluator_candidate", "evaluation_candidate"
        if scope_words & _EVALUATOR and (words & (_CONSTRUCTOR | _OPTIMIZER) or request):
            return "evaluator_candidate", "evaluation_candidate"
        if words & _OPTIMIZER:
            return "attacker_optimizer_candidate", "optimization_candidate"
        if words & _CONSTRUCTOR:
            role = "attacker_constructor_candidate" if scope_words & {"attack", "attacker", "constructor", "construct"} else "constructor_candidate"
            return role, "generation_candidate"
        if words & {"attack"}:
            return "attacker_constructor_candidate", "construction_candidate"
        if request:
            role = "evaluator_candidate" if scope_words & _EVALUATOR else (
                "attacker_optimizer_candidate" if scope_words & _OPTIMIZER else "model_recipient_candidate")
            return role, "model_request_candidate"
        # Arbitrarily named optimizers can still be discovered from an enclosing
        # attack/optimization function and their channel-bearing arguments.
        # This does not classify the routine as an actual attacker recipient.
        if (not scope_words & _EVALUATOR and scope_words & (_OPTIMIZER | {"attack", "attacker"})
                and (words & _EXECUTION_VERBS or words & {"receiver", "worker", "engine"})
                and (origins is None or any(origin["kind"] != "other" for origin in origins))):
            return "attack_context_recipient_candidate", "construction_or_optimization_candidate"
        if (not scope_words & _EVALUATOR and words & _EXECUTION_VERBS
                and (origins is None or any(origin["kind"] in {"question", "task", "documents"} for origin in origins))):
            return "unknown_recipient_candidate", "execution_input_candidate"
        return None

    def visit(self, file, call, env=None, bindings=(), depth=0, stack=frozenset()):
        self.visits += 1
        if self.visits > self.max_steps:
            self.truncated = True
            self.issues.add("call_visit_limit")
            return
        env = env or {}
        if depth > self.limits["max_trace_depth"]:
            self.truncated = True
            self.issues.add("wrapper_depth_limit")
            return
        resolved = self.resolve(file, call)
        if resolved:
            other, function, imports = resolved
            key = (other.part["id"], function)
            if key not in stack:
                self.called_functions.add(key)
                local = self.bind(file, call, other, function, env, 0)
                for inner in other.calls:
                    if other.scope[inner] == function:
                        self.visit(other, inner, local, tuple(_unique(list(bindings) + imports + [file.cite(call)]))[-6:],
                                   depth + 1, stack | {key})
                return
        if self.sink_hint(file, call, None) is None:
            return
        arguments = [(str(index), argument) for index, argument in enumerate(call.args)]
        arguments += [(keyword.arg or "**", keyword.value) for keyword in call.keywords]
        traced = []
        for argument, node in arguments:
            if argument in _METADATA_ARGUMENTS or _metadata_name(argument):
                continue
            origins = self.trace(file, node, env)
            kind = _kind(argument)
            if kind and kind != "other" and not isinstance(node, ast.Constant):
                matching = [origin for origin in origins if origin["kind"] == kind]
                if matching:
                    origins = matching
                else:
                    named = self._origin(file, node, kind)
                    named["bindings"] = _unique([cite for item in origins for cite in
                                                 item["bindings"] + [item["source_citation"]]])[-6:]
                    origins = [named]
            elif kind and not origins and not isinstance(node, ast.Constant):
                origins = [self._origin(file, node, kind)]
            traced.append((argument, node, origins))
        all_origins = [origin for _, _, origins in traced for origin in origins]
        hint = self.sink_hint(file, call, all_origins)
        if hint is None:
            return
        for argument, node, origins in traced:
            for origin in origins:
                call_anchor = file.anchor(call)
                key = json.dumps([file.part["path"], call_anchor, argument, origin["kind"]], sort_keys=True)
                identifier = "channel:" + hashlib.sha256(key.encode()).hexdigest()[:20]
                if identifier in self.candidates:
                    previous = self.candidates[identifier]
                    previous["bindings"] = _unique(previous["bindings"] + origin["bindings"]
                                                   + [origin["source_citation"]] + list(bindings))[-6:]
                    continue
                self.candidates[identifier] = {
                    "id": identifier, "status": "candidate", "path": file.part["path"],
                    "symbol": origin["symbol"], "channel_kind": origin["kind"],
                    "call": _dotted(call.func) or "<dynamic>", "argument": argument,
                    "citation": file.cite(call), "source_citation": origin["source_citation"],
                    "call_anchor": call_anchor, "source_anchor": origin["source_anchor"],
                    "bindings": _unique(origin["bindings"] + list(bindings))[-6:],
                    "role_hint": hint[0], "phase_hint": hint[1],
                }

    def run(self):
        # Expand caller arguments before processing free-standing function bodies.
        for file in self.files.values():
            for call in file.calls:
                if self.resolve(file, call):
                    self.visit(file, call)
        for file in self.files.values():
            for call in file.calls:
                if (file.part["id"], file.scope[call]) not in self.called_functions:
                    self.visit(file, call)
        def priority(item):
            role = item["role_hint"]
            return (0 if role in {"attacker_optimizer_candidate", "attacker_constructor_candidate", "attack_context_recipient_candidate"}
                    else 2 if role == "evaluator_candidate" else 1,
                    0 if item["channel_kind"] in {"question", "task"} else 2 if item["channel_kind"] == "other" else 1,
                    item["path"], item["call_anchor"]["start"], item["argument"], item["channel_kind"], item["id"])
        ranked = sorted(self.candidates.values(), key=priority)
        if len(ranked) > self.limits["max_candidates"]:
            self.truncated = True
            self.issues.add("candidate_limit")
        return ranked[:self.limits["max_candidates"]]


def discover_channels(document, *, max_candidates=32, max_files=160, max_chars=1000000,
                      max_ast_nodes=120000, max_trace_depth=5):
    """Inventory likely input channels in supplied Python code segments only.

    All limits are hard positive bounds. Unsupported/partial source, parse
    failures and exhausted limits remain explicit limitations. The result is
    deterministic and contains no asserted receipt, permission or verdict.
    ``max_trace_depth`` bounds wrappers/aliases, not Python syntax nesting.
    """
    limits = dict(max_candidates=max_candidates, max_files=max_files, max_chars=max_chars,
                  max_ast_nodes=max_ast_nodes, max_trace_depth=max_trace_depth)
    if any(type(value) is not int or value < 1 for value in limits.values()):
        raise ValueError("input-channel discovery limits must be positive integers")
    files, issues = {}, set()
    size = node_count = file_count = 0
    truncated = False
    parts = sorted((part for part in document.get("segments", [])
                    if part.get("source_kind") == "code"), key=lambda part: (part.get("path", ""), part["id"]))
    for part in parts:
        if not part.get("path", "").endswith(".py"):
            # Configuration/data witness segments share source_kind='code' in
            # the source bundle. They are evidence, not unparsed programs.
            if PurePosixPath(part.get("path", "")).suffix.lower() in _DECLARATIVE_SUFFIXES:
                continue
            issues.add("non_python_segments_not_traced")
            continue
        text = part.get("text", "")
        if file_count >= max_files or size + len(text) > max_chars:
            truncated = True
            issues.add("file_or_character_limit")
            continue
        file_count += 1
        size += len(text)
        if part.get("line_start", 1) != 1 or part["path"] in files:
            issues.add("partial_or_duplicate_file_segments_not_joined")
            continue
        try:
            tree = ast.parse(text)
            count = sum(1 for _ in ast.walk(tree))
        except (SyntaxError, ValueError, RecursionError):
            issues.add("python_parse_failure")
            continue
        if node_count + count > max_ast_nodes:
            truncated = True
            issues.add("ast_node_limit")
            continue
        node_count += count
        try:
            files[part["path"]] = _File(part, tree)
        except RecursionError:
            truncated = True
            issues.add("ast_recursion_limit")
    discovery = _Discovery(files, limits)
    try:
        candidates = discovery.run()
    except RecursionError:
        discovery.truncated = True
        discovery.issues.add("trace_recursion_limit")
        candidates = list(discovery.candidates.values())
    return {"schema_version": 1, "candidates": candidates, "limits": limits,
            "truncated": truncated or discovery.truncated,
            "discovery_complete": bool(files) and not (truncated or discovery.truncated or issues or discovery.issues),
            "limitations": sorted(issues | discovery.issues | {
                "lexical_roles_and_channels_are_candidates_not_receipt_or_policy_facts",
                "static_python_subset_does_not_establish_repository_or_runtime_closure"}),
            "statistics": {"parsed_files": len(files), "parsed_ast_nodes": node_count,
                           "source_characters": size, "total_candidates": len(discovery.candidates)}}


def candidate_citations_match(candidate, citations, document):
    """Check exact code support for both this origin and its input boundary.

    This gate never establishes channel semantics or a proven flow. The caller
    must separately require an independent review of the same channel and flow,
    and apply the normal receipt/policy/path gates. A candidate ID or a shared
    request citation alone cannot cover another input channel.
    """
    from extraction_v3 import locate
    from call_boundaries import call_identity

    parts = {part["id"]: part for part in document.get("segments", [])}
    origins, boundaries = [], []
    for citation in citations:
        try:
            locator = locate(citation, document)
            part = parts[locator["segment_id"]]
            if part.get("source_kind") != "code":
                continue
        except (ValueError, KeyError, TypeError):
            continue
        source = candidate["source_anchor"]
        if (locator["segment_id"] == source["segment_id"] and
                locator["start"] <= source["start"] and locator["end"] >= source["end"]):
            origins.append(locator)
        anchor = candidate["call_anchor"]
        if locator["segment_id"] == anchor["segment_id"]:
            identity = call_identity(part["text"], locator["start"], locator["end"])
            if identity == (anchor["start"], anchor["end"]):
                boundaries.append(locator)
    return bool(origins and boundaries)
