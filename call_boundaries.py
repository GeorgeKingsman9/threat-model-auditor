"""Exact static Python input-call identities; upstream code is never executed."""

import ast
import tokenize
from io import StringIO


def call_identity(text, start, end):
    """Identify the innermost call containing this citation, or fail closed.

    Only transparent statement prefixes may extend before a Call's own span.
    A citation spanning another statement/call is not cropped to make it fit.
    Parenthesized statement suffixes beyond Call.end are conservatively rejected.
    """
    if not (0 <= start < end <= len(text)):
        return None
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError, RecursionError):
        return None
    lines = text.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))

    def ast_offset(row, byte_col):
        line = lines[row - 1]
        return starts[row - 1] + len(line.encode('utf-8')[:byte_col].decode('utf-8'))

    def span(node):
        return (ast_offset(node.lineno, node.col_offset),
                ast_offset(node.end_lineno, node.end_col_offset))

    call_spans = [span(node) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if start == end:
        return None

    # Whitelist prefix starts by AST structure: Return / assignment / Expr,
    # optionally containing Await directly around the called expression.
    # Never ignore a second invocation in an assignment target or annotation.
    prefix_candidates = []
    for statement in ast.walk(tree):
        if not isinstance(statement, (ast.Return, ast.Assign, ast.AnnAssign, ast.Expr)):
            continue
        value = statement.value
        if value is None:
            continue
        prefix_starts = {span(statement)[0]}
        while isinstance(value, ast.Await):
            prefix_starts.add(span(value)[0])
            value = value.value
        if not isinstance(value, ast.Call):
            continue
        call_start, call_end = span(value)
        if start not in prefix_starts or not (start < call_start < end <= call_end):
            continue
        if any(a < call_start and b > start for a, b in call_spans):
            continue
        prefix_candidates.append(call_start)
    if prefix_candidates:
        start = max(prefix_candidates)

    candidates = [(a, b) for a, b in call_spans if a <= start and end <= b]
    if not candidates:
        return None
    boundary = min(candidates, key=lambda item: item[1] - item[0])
    # A comment located within a multiline Call is not a quoted input boundary.
    ignored = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
               tokenize.DEDENT, tokenize.ENCODING, tokenize.ENDMARKER}
    try:
        has_code = any(tok.type not in ignored
                       and starts[tok.start[0] - 1] + tok.start[1] < end
                       and starts[tok.end[0] - 1] + tok.end[1] > start
                       for tok in tokenize.generate_tokens(StringIO(text).readline))
    except (tokenize.TokenError, IndentationError):
        return None
    return boundary if has_code else None

