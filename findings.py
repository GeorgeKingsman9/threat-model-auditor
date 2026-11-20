"""User-facing paper verdicts with concrete paper and implementation locations."""

from urllib.parse import quote


def project_result(row):
    """Keep uncertainty distinct from a scoped negative; never invent locations."""
    verdict = row.get("verdict")
    flag = True if verdict == "inconsistent" else False if verdict == "consistent_within_scope" else None
    findings, unresolved = [], []
    for evidence in row.get("evidence", []):
        if evidence.get("claim_result") == "confirmed":
            locators = evidence.get("locators", {})
            paper_locations, code_locations = [], []
            candidates = list(locators.values())
            candidates += evidence.get("source_validation", {}).get("code_path_locators", [])
            candidates += list(evidence.get("binding_validation", {}).get("locators", {}).values())
            for locator in candidates:
                if not isinstance(locator, dict):
                    continue
                if locator.get("source_kind") == "code" or locator.get("path"):
                    value = {key: locator[key] for key in ("path", "original_path", "line_start", "line_end",
                             "repository_source", "repository_revision", "file_sha256") if key in locator}
                    if value and value not in code_locations:
                        source = value.get("repository_source", "") or ""
                        revision = value.get("repository_revision", "")
                        if source.startswith("https://github.com/") and revision:
                            path = value.get("original_path", value.get("path", ""))
                            value["url"] = source + "/blob/" + revision + "/" + quote(path, safe="/")
                            if value.get("line_start"):
                                value["url"] += "#L" + str(value["line_start"])
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
        elif evidence.get("claim_result") == "unresolved":
            unresolved.append({"claim": evidence.get("claim"), "reason": evidence.get("reason")})
    row.update(inconsistency=flag, findings=findings, unresolved_findings=unresolved)
    return row
