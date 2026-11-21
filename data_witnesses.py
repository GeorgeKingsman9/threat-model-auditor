"""Bounded exact JSON record witnesses, with complete locally retained raw bytes.

This module only parses data. It never follows paths, schema references, imports,
or instructions found inside records. Offsets are zero-based half-open spans in
original UTF-8 bytes and Unicode text; witness text is never normalized.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re

POLICY = "bounded-json-records-v1"
LIMITS = {"max_files": 8, "max_file_bytes": 4 * 1024 * 1024,
          "max_total_bytes": 8 * 1024 * 1024, "max_records": 4,
          "max_total_records": 20000, "max_record_bytes": 32 * 1024,
          "max_file_output_bytes": 32 * 1024, "max_output_bytes": 128 * 1024,
          "max_record_pointer_bytes": 1024}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw, object_id):
    if not isinstance(object_id, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id):
        raise ValueError("Invalid data Git blob identity")
    value = f"blob {len(raw)}\0".encode() + raw
    return hashlib.sha1(value).hexdigest() if len(object_id) == 40 else digest(value)


def _pairs(values):
    result = {}
    for key, value in values:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _constant(value):
    raise ValueError("non-finite JSON constant")


_DECODER = json.JSONDecoder(object_pairs_hook=_pairs, parse_constant=_constant)


def _space(text, start):
    while start < len(text) and text[start] in " \r\n\t":
        start += 1
    return start


def _pointer(value):
    # JSON permits escaped surrogate code points, but generated locator metadata
    # must itself be valid UTF-8. Exact record text remains untouched.
    return str(value).encode("utf-8").decode("utf-8").replace("~", "~0").replace("/", "~1")


class _RecordLimit(ValueError):
    def __init__(self, count):
        self.count = count


def _members(text, start, value, pointer=""):
    """Decode direct members only; raw_decode gives original exact value spans."""
    position = _space(text, start + 1)
    for key in (range(len(value)) if isinstance(value, list) else value):
        if isinstance(value, dict):
            _, position = _DECODER.raw_decode(text, position)
            position = _space(text, position)
            if text[position] != ":":
                raise ValueError("missing JSON colon")
            position = _space(text, position + 1)
        member_start = position
        child, position = _DECODER.raw_decode(text, position)
        yield child, member_start, position, pointer + "/" + _pointer(key)
        position = _space(text, position)
        if position < len(text) and text[position] == ",":
            position = _space(text, position + 1)


def _records(text, value, start, end):
    """Arrays, ID-keyed maps and container wrappers use data-independent rules."""
    if isinstance(value, list):
        if len(value) > LIMITS["max_total_records"]:
            raise _RecordLimit(len(value))
        return list(_members(text, start, value))
    if isinstance(value, dict):
        # A map of objects is an ID-keyed dataset. Mixed records with scalar
        # fields remain whole records, even when they contain context arrays.
        if value and all(isinstance(child, dict) for child in value.values()):
            if len(value) > LIMITS["max_total_records"]:
                raise _RecordLimit(len(value))
            return list(_members(text, start, value))
        container_keys = {key for key, child in value.items()
                          if isinstance(child, list) and child
                          and all(isinstance(record, dict) for record in child)}
        if container_keys:
            count = sum(len(value[key]) for key in container_keys)
            if count > LIMITS["max_total_records"]:
                raise _RecordLimit(count)
            container_pointers = {"/" + _pointer(key) for key in container_keys}
            return [record for child, begin, _, pointer in _members(text, start, value)
                    if pointer in container_pointers
                    for record in _members(text, begin, child, pointer)]
    return [(value, start, end, "")]


def _signature(value):
    # Internal selection metadata only, never author source evidence.
    if isinstance(value, dict):
        return ("object", tuple(sorted((key, type(child).__name__) for key, child in value.items())))
    return (type(value).__name__,)


def build(entry, raw, *, output_budget=None):
    """Return (raw blob provenance, exact witnesses); malformed data is explicit.

    Raw bytes must already be filtered for credential-like material by the
    source reader. Even a parse failure keeps a hash-bound, size-capped raw blob
    so offline replay can reproduce the failure rather than trusting a summary.
    """
    if len(raw) != entry["bytes"] or len(raw) > LIMITS["max_file_bytes"]:
        raise ValueError("Data blob differs from its bounded inventory size")
    if entry.get("object_id") is not None and git_blob(raw, entry["object_id"]) != entry["object_id"]:
        raise ValueError("Data bytes differ from their pinned Git blob identity")
    budget = min(LIMITS["max_file_output_bytes"], LIMITS["max_output_bytes"]
                 if output_budget is None else output_budget)
    blob = {"path": entry["path"], "bytes": len(raw), "sha256": digest(raw),
            "policy": POLICY, "raw_base64": base64.b64encode(raw).decode("ascii"),
            "output_budget": budget,
            **({"object_id": entry["object_id"]} if "object_id" in entry else {})}
    coverage = {"raw_complete": True, "complete": False, "total_records": None,
                "sampled_records": 0, "oversized_records": 0,
                "oversized_pointers": 0,
                "sampling": "schema-diverse-then-spaced-v1", "output_bytes": 0,
                "omitted_records": None, "omission_reasons": []}
    blob["coverage"] = coverage
    try:
        text = raw.decode("utf-8")
        if "\x00" in text:
            raise ValueError("NUL in JSON data")
        value, end = _DECODER.raw_decode(text, _space(text, 0))
        if _space(text, end) != len(text):
            raise ValueError("trailing JSON data")
        records = _records(text, value, _space(text, 0), end)
    except _RecordLimit as error:
        coverage.update(total_records=error.count, omitted_records=error.count,
                        omission_reasons=["json_record_count_limit"])
        blob.update(status="unresolved", reason="json_record_count_limit")
        return blob, []
    except (ValueError, UnicodeError, RecursionError):
        blob.update(status="unresolved", reason="malformed_or_unsupported_json")
        return blob, []
    coverage["total_records"] = len(records)
    coverage["omitted_records"] = len(records)
    if len(records) > LIMITS["max_total_records"]:
        coverage["omission_reasons"] = ["json_record_count_limit"]
        blob.update(status="unresolved", reason="json_record_count_limit")
        return blob, []
    lengths = [len(text[begin:end].encode("utf-8")) for _, begin, end, _ in records]
    coverage["oversized_records"] = sum(size > LIMITS["max_record_bytes"] for size in lengths)
    pointer_lengths = [len(record[3].encode("utf-8")) for record in records]
    coverage["oversized_pointers"] = sum(size > LIMITS["max_record_pointer_bytes"] for size in pointer_lengths)
    # Schema diversity first, then even positions across the complete file.
    # Huge records are reported and skipped whole, never cut into evidence.
    distinct, order = set(), []
    for index, (record, _, _, _) in enumerate(records):
        if (lengths[index] > LIMITS["max_record_bytes"]
                or pointer_lengths[index] > LIMITS["max_record_pointer_bytes"]):
            continue
        signature = _signature(record)
        if signature not in distinct:
            distinct.add(signature)
            order.append(index)
            if len(order) >= LIMITS["max_records"]:
                break
    count = len(records)
    spaced = [round(i * (count - 1) / (LIMITS["max_records"] - 1))
              for i in range(LIMITS["max_records"])] if count else []
    order = list(dict.fromkeys(order + spaced + list(range(min(count, LIMITS["max_records"] * 2)))))
    chosen, used = [], 0
    for index in order:
        size = lengths[index]
        if (size > LIMITS["max_record_bytes"] or used + size > budget
                or pointer_lengths[index] > LIMITS["max_record_pointer_bytes"]):
            continue
        chosen.append(index); used += size
        if len(chosen) == LIMITS["max_records"]:
            break
    reasons = []
    if coverage["oversized_records"]:
        reasons.append("record_byte_limit")
    if coverage["oversized_pointers"]:
        reasons.append("record_pointer_byte_limit")
    if count > LIMITS["max_records"]:
        reasons.append("record_sample_limit")
    if any(index not in chosen and size <= LIMITS["max_record_bytes"] and used + size > budget
           for index, size in enumerate(lengths)):
        reasons.append("record_output_byte_limit")
    coverage.update(complete=bool(chosen) and len(chosen) == count,
                    sampled_records=len(chosen), output_bytes=used,
                    omitted_records=count - len(chosen), omission_reasons=reasons)
    witnesses = []
    for index in sorted(chosen):
        _, begin, end, pointer = records[index]
        excerpt = text[begin:end]
        byte_start = len(text[:begin].encode("utf-8"))
        line_start = text.count("\n", 0, begin) + 1
        line_end = line_start + excerpt.count("\n")
        witnesses.append({"id": f"data:{entry['path']}:B{byte_start}-B{byte_start + lengths[index]}",
                          "path": entry["path"], "text": excerpt,
                          "sha256": blob["sha256"], "text_sha256": digest(excerpt.encode("utf-8")),
                          "line_start": line_start, "line_end": line_end,
                          "char_start": begin, "char_end": end,
                          "byte_start": byte_start, "byte_end": byte_start + lengths[index],
                          "record_index": index, "record_pointer": pointer,
                          "coverage": "complete" if coverage["complete"] else "sampled",
                          **({"object_id": entry["object_id"]} if "object_id" in entry else {})})
    if witnesses:
        blob["status"] = "resolved"
    else:
        blob.update(status="unresolved", reason="json_no_bounded_records")
    return blob, witnesses


def decode_blob(blob):
    """Bound base64 before decoding; do not let replay allocate unbounded data."""
    value = blob.get("raw_base64")
    if not isinstance(value, str) or len(value) > 4 * ((LIMITS["max_file_bytes"] + 2) // 3):
        raise ValueError("Data raw byte encoding exceeds limit")
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, UnicodeError) as error:
        raise ValueError("Invalid data raw byte encoding") from error
