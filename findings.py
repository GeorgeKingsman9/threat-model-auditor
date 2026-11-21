"""User-facing paper verdicts with concrete paper and implementation locations."""

from urllib.parse import quote


def _locators(value):
    if isinstance(value, dict):
        if "segment_id" in value or ("path" in value and "line_start" in value):
            yield value
        else:
            for child in value.values():
                yield from _locators(child)
    elif isinstance(value, list):
        for child in value:
            yield from _locators(child)


def project_result(row):
    """Keep uncertainty distinct from a scoped negative; never invent locations."""
    verdict = row.get("verdict")
    flag = True if verdict == "inconsistent" else False if verdict == "consistent_within_scope" else None
    findings, unresolved = [], []
    for evidence in row.get("evidence", []):
        if evidence.get("claim_result") == "confirmed":
            locators = evidence.get("locators", {})
            paper_locations, code_locations = [], []
            candidates = list(_locators(locators))
            candidates += list(_locators(evidence.get("source_validation", {})))
            candidates += list(_locators(evidence.get("binding_validation", {}).get("locators", {})))
            for locator in candidates:
                if not isinstance(locator, dict):
                    continue
                if locator.get("source_kind") == "code" or locator.get("path"):
                    value = {key: locator[key] for key in ("path", "original_path", "line_start", "line_end",
                             "repository_source", "repository_revision", "file_sha256", "data_witness") if key in locator}
                    if value:
                        source = value.get("repository_source", "") or ""
                        revision = value.get("repository_revision", "")
                        if source.startswith("https://github.com/") and revision:
                            path = value.get("original_path", value.get("path", ""))
                            value["url"] = source + "/blob/" + revision + "/" + quote(path, safe="/")
                            if value.get("line_start"):
                                value["url"] += "#L" + str(value["line_start"])
                        if value not in code_locations:
                            code_locations.append(value)
                elif locator.get("segment_id"):
                    segment = locator["segment_id"].removeprefix("paper:")
                    value = {"segment_id": locator["segment_id"]}
                    if segment.startswith("p") and segment[1:].isdigit():
                        value["pdf_page"] = int(segment[1:])
                    if value not in paper_locations:
                        paper_locations.append(value)
            findings.append({"claim": evidence.get("claim", evidence.get("description")),
                             "reason": evidence.get("reason"), "scope": evidence.get("scope"),
                             "paper_locations": paper_locations, "code_locations": code_locations})
            if "issue_type" in evidence:
                findings[-1]["issue_type"] = evidence["issue_type"]
        elif evidence.get("claim_result") == "unresolved":
            unresolved.append({"claim": evidence.get("claim"), "reason": evidence.get("reason")})
            if "issue_type" in evidence:
                unresolved[-1]["issue_type"] = evidence["issue_type"]
    row.update(inconsistency=flag, findings=findings, unresolved_findings=unresolved)
    return row
