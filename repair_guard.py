"""Partition bounded citation selections without weakening mechanical checks.

An invalid selection is an abstention for its original pointer, not permission
to infer another candidate ID. Request/schema failures remain fatal. The strict
legacy applicator alone performs citation updates and preserves all other facts.
"""

from collections import Counter

from citation_repair import CHOICE_SCHEMA, apply_choices, choice_request
from extraction import validate_shape


def apply_bounded_choices(extraction, response, document, issues, request):
    """Return ``(fixed, accepted, rejected)`` for exact, unique offered IDs.

    Unknown IDs/targets are rejected individually. Every occurrence of a
    duplicated target is rejected, including a null or otherwise valid choice.
    Unique null selections abstain. A malformed response, changed request, or
    any failed legacy application check raises rather than partially applying.
    Inputs are never mutated; accepted records retain the legacy shape.
    """
    validate_shape(response, CHOICE_SCHEMA)
    if request != choice_request(extraction, document, issues):
        raise ValueError("citation choice candidates changed after preparation")

    tasks = {task["target"]: task for task in request["tasks"]}
    counts = Counter(choice["target"] for choice in response["choices"])
    usable, rejected = [], []
    for index, choice in enumerate(response["choices"]):
        target = choice["target"]
        candidate_id = choice["candidate_id"]
        if counts[target] > 1:
            reason = "duplicate_target"
        elif target not in tasks:
            reason = "unknown_target"
        elif candidate_id is not None and candidate_id not in {
                option["candidate_id"] for option in tasks[target]["choices"]}:
            reason = "unknown_candidate_id"
        else:
            # Keep null choices in the strict applicator's input: it owns the
            # established abstention behavior and all citation-only mutations.
            usable.append(choice)
            continue
        rejected.append({"index": index, "target": target, "candidate_id": candidate_id,
                         "reason": reason, "selection_reason": choice["reason"]})

    fixed, accepted = apply_choices(extraction, {"choices": usable}, document, issues, request)
    return fixed, accepted, rejected
