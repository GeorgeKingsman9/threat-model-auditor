"""Resume one failed automatic semantic review from unchanged local artifacts.

This is an explicit new attempt, never an implicit provider retry. It performs
one model call at most; no source discovery, acquisition, extraction or citation
editing occurs. The original failed attempt is immutable. A saved V7 contract
preserves the exact review prompt; older attempts lacking it are clearly marked
as amended reviews with the current engine, not exact frozen continuations.
"""

import copy
import hashlib
import importlib
import json
from pathlib import Path
import time

import extraction_v4 as v4
from extraction import validate_shape
from findings import project_result
from reports import write_reports


MAX_PARENT_FILE_BYTES = 48 * 1024 * 1024


def _save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read(directory, name, hashes):
    path = directory / name
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_PARENT_FILE_BYTES:
        raise ValueError("recovery requires bounded regular parent artifacts")
    before = _digest(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if _digest(path) != before:
        raise ValueError("parent artifact changed during recovery preparation")
    hashes[name] = before
    return value


def _same_parent(directory, hashes):
    if any(not (directory / name).is_file() or (directory / name).is_symlink()
           or _digest(directory / name) != digest for name, digest in hashes.items()):
        raise ValueError("parent artifacts changed during review recovery")


def _copy_parent(directory, output, name, hashes):
    """Preserve the validated artifact's bytes, not a JSON reserialization."""
    source = directory / name
    expected = hashes.get(name)
    if expected is None or source.is_symlink() or not source.is_file():
        raise ValueError("recovery cannot copy an unvalidated parent artifact")
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("parent artifact changed before recovery copying")
    with (output / name).open("xb") as stream:
        stream.write(data)
    if _digest(source) != expected or _digest(output / name) != expected:
        raise ValueError("parent artifact bytes changed during recovery copying")


def _require_one_call(client):
    if client is None or not callable(getattr(client, "generate", None)):
        raise ValueError("review recovery requires an explicit inference client")
    maximum, calls = getattr(client, "max_calls", None), getattr(client, "calls", None)
    if type(maximum) is not int or not isinstance(calls, list) or maximum - len(calls) < 1:
        raise ValueError("review recovery requires at least one remaining counted call")


def _load_acquisition(directory, hashes, engine, version, combined, effective, filename):
    """Reapply the bounded supplemental pass, not its claimed classification."""
    names = ("acquisition_pass.request.json", "acquisition_pass.response.json",
             "acquisition_pass.checks.json", "extraction.acquisition.json")
    if not any((directory / name).exists() for name in names):
        if filename == "extraction.acquisition.json":
            raise ValueError("parent effective acquisition proposal has no pass artifacts")
        return {}
    if version != 7:
        raise ValueError("acquisition pass artifacts require V7")
    from acquisition_pass import prepare_acquisition_input, apply_acquisition_pass
    extras = {"extraction.json": _read(directory, "extraction.json", hashes),
              names[0]: _read(directory, names[0], hashes)}
    expected_request = prepare_acquisition_input(engine.model_content(combined), extras["extraction.json"])
    if extras[names[0]] != expected_request:
        raise ValueError("parent acquisition input differs from original bound proposal")
    successful = any((directory / name).exists() for name in names[2:])
    if successful:
        for name in names[1:]:
            extras[name] = _read(directory, name, hashes)
        refined, notes = apply_acquisition_pass(extras["extraction.json"], extras[names[1]], combined)
        if refined != extras["extraction.acquisition.json"] or notes != extras["acquisition_pass.checks.json"]:
            raise ValueError("parent acquisition result/checks differ from revalidated pass")
        if filename == "extraction.acquisition.json" and effective != refined:
            raise ValueError("effective proposal differs from verified acquisition pass")
        if filename == "extraction.repaired.json":
            # A repair following the pass can alter only checked citation fields.
            from citation_repair import citation_issues
            from repair_guard import apply_bounded_choices
            for name in ("citation_repair.request.json", "citation_repair.response.json"):
                extras[name] = _read(directory, name, hashes)
            repaired, _, _ = apply_bounded_choices(refined, extras["citation_repair.response.json"],
                combined, citation_issues(refined, combined), extras["citation_repair.request.json"])
            if repaired != effective:
                raise ValueError("effective proposal differs from verified acquisition/citation recovery")
        elif filename != "extraction.acquisition.json":
            raise ValueError("successful acquisition pass is not the effective proposal")
    else:
        failure = _read(directory, "acquisition_pass.failure.json", hashes)
        extras["acquisition_pass.failure.json"] = failure
        if (failure.get("original_proposal_preserved") is not True
                or filename == "extraction.acquisition.json"):
            raise ValueError("failed acquisition pass cannot supply an effective new proposal")
        if (directory / names[1]).exists():
            extras[names[1]] = _read(directory, names[1], hashes)
    return extras


def _load_parent(directory, hashes, max_input_chars):
    result = _read(directory, "result.json", hashes)
    if (result.get("status") != "failed" or result.get("verdict") != "technical_failure"
            or result.get("requested_workflow") != "automatic_from_paper"
            or result.get("source_audit", {}).get("status") != "loaded"):
        raise ValueError("recovery accepts only a failed automatic paper/source audit")
    failed = [item for item in result.get("stages", []) if item.get("status") == "failed"]
    if not failed or failed[-1].get("stage") not in {"semantic_review", "semantic_review_retry1"}:
        raise ValueError("parent failure is not an unfinished semantic review")
    if (directory / "review.json").exists():
        raise ValueError("parent already contains a review; recovery must not replace it")
    ledger = _read(directory, "inference.json", hashes)
    calls = ledger.get("calls")
    if not isinstance(calls, list) or not calls or calls[-1].get("status") in {"completed", "completed_with_warnings"}:
        raise ValueError("parent has no recorded failed model call")
    snapshot = _read(directory, "inference." + failed[-1]["stage"] + ".json", hashes)
    if snapshot.get("calls") != calls:
        raise ValueError("parent failed-review snapshot differs from its final ledger")
    prepared = _read(directory, "prepared.json", hashes)
    repository = _read(directory, "repository.json", hashes)
    discovery = _read(directory, "source_discovery.json", hashes)
    combined = _read(directory, "combined_input.json", hashes)
    request = _read(directory, "request.json", hashes)
    filename = result.get("effective_extraction_file", "extraction.json")
    if filename not in {"extraction.json", "extraction.repaired.json", "extraction.acquisition.json"}:
        raise ValueError("parent effective extraction filename is not recognized")
    extraction = _read(directory, filename, hashes)
    version = extraction.get("schema_version")
    if type(version) is not int or version not in {4, 5, 6, 7}:
        raise ValueError("review recovery supports only source-aware V4–V7 proposals")
    engine = importlib.import_module("extraction_v" + str(version))
    validate_shape(extraction, engine.EXTRACTION_SCHEMA)
    engine.validate_input_binding(combined)
    if (discovery.get("status") != "selected"
            or discovery.get("repository") != repository.get("source")
            or discovery.get("revision") != repository.get("revision")
            or result.get("source_audit", {}).get("revision") != repository.get("revision")
            or combined.get("paper_sha256") != prepared.get("sha256")
            or combined.get("repository", {}).get("manifest_sha256") != repository.get("manifest_sha256")
            or request.get("input_sha256") != combined["sha256"]
            or extraction.get("input_binding") != combined["sha256"]):
        raise ValueError("parent automatic provenance or paper/source input binding differs")
    rebuilt = engine.combine_inputs(prepared, repository)
    contract = None
    if (directory / "declared_contract.json").exists():
        contract = _read(directory, "declared_contract.json", hashes)
        if version < 6:
            raise ValueError("legacy parent unexpectedly contains a declared contract")
        rebuilt = engine.attach_declared_contract(rebuilt, contract)
    if rebuilt != combined:
        raise ValueError("parent combined evidence differs from its frozen paper/source artifacts")
    extra_artifacts = _load_acquisition(directory, hashes, engine, version, combined, extraction, filename)
    content = {**engine.model_content(combined), "proposal": extraction}
    if len(json.dumps(content, ensure_ascii=False, sort_keys=True)) > max_input_chars:
        raise ValueError("recovery model payload exceeds its configured input limit")
    saved_contract = None
    has_contract, has_request = ((directory / "review.contract.json").exists(),
                                 (directory / "review.request.json").exists())
    if has_contract != has_request:
        raise ValueError("parent saved review contract/request is incomplete")
    if has_contract:
        saved_contract = _read(directory, "review.contract.json", hashes)
        saved_input = _read(directory, "review.request.json", hashes)
        if (saved_input != content or saved_contract.get("engine_version") != version
                or saved_contract.get("input_binding") != combined["sha256"]
                or saved_contract.get("review_input_sha256") != v4._hash_json(content)
                or saved_contract.get("schema") != engine.REVIEW_SCHEMA
                or saved_contract.get("schema_sha256") != v4._hash_json(saved_contract.get("schema"))
                or not isinstance(saved_contract.get("prompt"), str)
                or saved_contract.get("prompt_sha256") != hashlib.sha256(saved_contract["prompt"].encode()).hexdigest()):
            raise ValueError("saved review contract differs from its frozen payload/schema/prompt")
        prompt, schema = saved_contract["prompt"], saved_contract["schema"]
        mode = "saved_exact_review_contract"
    else:
        if version >= 7:
            raise ValueError("V7 recovery requires its saved exact review contract")
        prompt, schema = engine.REVIEW_PROMPT, engine.REVIEW_SCHEMA
        mode = "amended_current_review_legacy_parent"
    return {"result": result, "prepared": prepared, "repository": repository,
            "discovery": discovery, "combined": combined, "extraction": extraction,
            "filename": filename, "request": request, "declared_contract": contract,
            "engine": engine, "engine_version": version, "content": content,
            "prompt": prompt, "schema": schema, "mode": mode, "extra_artifacts": extra_artifacts}


def resume_review(run_dir, output_dir, client, max_input_chars=1200000):
    """Return one result row after at most one independently dispatched review.

    Validation, model and decision failures are kept as a new failed row. No
    fallback, retry, source refresh or input edits are performed by this helper.
    """
    parent, output = Path(run_dir).resolve(), Path(output_dir).resolve()
    if parent == output or parent in output.parents or output in parent.parents:
        raise ValueError("review recovery output must be separate from its parent attempt")
    output.mkdir(parents=True, exist_ok=False)
    started, hashes = time.monotonic(), {}
    row = {"id": "recovered_paper", "title": "Recovered automatic paper audit",
           "source": parent.name, "status": "running", "stages": [], "evidence": [],
           "has_confirmed_inconsistency": None, "recovery_mode": "review_only",
           "requested_workflow": "automatic_from_paper"}
    stage, loaded, review = "parent_validation", None, None
    try:
        if type(max_input_chars) is not int or max_input_chars <= 0:
            raise ValueError("recovery input limit must be a positive integer")
        loaded = _load_parent(parent, hashes, max_input_chars)
        _require_one_call(client)
        original = loaded["result"]
        row.update({key: copy.deepcopy(original[key]) for key in (
            "id", "title", "source", "input_mode", "source_audit", "source_discovery") if key in original})
        row["stages"].append({"stage": stage, "status": "completed",
                              "verified_parent_artifacts": len(hashes)})
        _same_parent(parent, hashes)
        for name, key in (("prepared.json", "prepared"), ("repository.json", "repository"),
                          ("source_discovery.json", "discovery"), ("combined_input.json", "combined"),
                          ("request.json", "request"), (loaded["filename"], "extraction")):
            _copy_parent(parent, output, name, hashes)
        if loaded["declared_contract"] is not None:
            _copy_parent(parent, output, "declared_contract.json", hashes)
        for name, value in loaded["extra_artifacts"].items():
            if not (output / name).exists():
                _copy_parent(parent, output, name, hashes)
        row["effective_extraction_file"] = loaded["filename"]
        provenance = {"mode": loaded["mode"], "parent_attempt_id": parent.name,
            "parent_artifact_sha256": hashes, "original_request_prompt_sha256": loaded["request"].get("prompt_sha256"),
            "review_prompt_sha256": hashlib.sha256(loaded["prompt"].encode()).hexdigest(),
            "current_engine_prompt_sha256": loaded["engine"].prompt_hash(),
            "review_schema_sha256": v4._hash_json(loaded["schema"]),
            "review_input_sha256": v4._hash_json(loaded["content"]),
            "input_binding": loaded["combined"]["sha256"], "engine_version": loaded["engine_version"],
            "max_new_model_calls": 1, "source_refreshed": False, "proposal_modified": False,
            "classification_fields_modified": False}
        row["recovery"] = provenance
        _save(output / "recovery.json", provenance)
        _save(output / "review.request.json", loaded["content"])
        _save(output / "review.contract.json", {
            "prompt": loaded["prompt"], "schema": loaded["schema"],
            "prompt_sha256": provenance["review_prompt_sha256"],
            "schema_sha256": provenance["review_schema_sha256"],
            "review_input_sha256": provenance["review_input_sha256"],
            "input_binding": provenance["input_binding"], "engine_version": loaded["engine_version"]})
        stage = "semantic_review"
        before_calls = len(client.calls)
        try:
            review = client.generate(loaded["prompt"], loaded["content"], loaded["schema"])
        finally:
            if callable(getattr(client, "ledger", None)):
                _save(output / "inference.semantic_review.json", client.ledger())
        if len(client.calls) - before_calls != 1:
            raise ValueError("review recovery client did not record exactly one invocation")
        _same_parent(parent, hashes)
        validate_shape(review, loaded["schema"])
        if review.get("input_binding") != loaded["combined"]["sha256"]:
            raise ValueError("recovered review is bound to different evidence")
        _save(output / "review.json", review)
        row["stages"].append({"stage": stage, "status": "completed", "execution": loaded["mode"]})
        stage = "citation_validation_and_decision"
        row.update(loaded["engine"].decide_extraction(
            loaded["extraction"], review, loaded["combined"], row["id"]))
        row.update(status="completed", prompt_sha256=loaded["engine"].prompt_hash())
        row["stages"].append({"stage": stage, "status": "completed", "verdict": row["verdict"]})
    except Exception as error:
        row.update(status="failed", verdict="technical_failure", error=str(error),
                   error_type=type(error).__name__, has_confirmed_inconsistency=None)
        row["stages"].append({"stage": stage, "status": "failed", "error": str(error)})
    row["duration_seconds"] = round(time.monotonic() - started, 3)
    if client is not None and callable(getattr(client, "ledger", None)):
        _save(output / "inference.json", client.ledger())
    _save(output / "parent_integrity.json", {"artifact_sha256": hashes,
          "unchanged": all((parent / name).is_file() and not (parent / name).is_symlink()
                           and _digest(parent / name) == digest for name, digest in hashes.items())})
    project_result(row)
    _save(output / "result.json", row)
    report = {"run_type": "automatic_review_recovery", "papers": [row],
              "summary": {"paper_count": 1, "statuses": {row["status"]: 1}, "verdicts": {row["verdict"]: 1}}}
    if client is not None and callable(getattr(client, "ledger", None)):
        report["inference"] = client.ledger()
    _save(output / "report.json", report)
    write_reports(report, output)
    return row
