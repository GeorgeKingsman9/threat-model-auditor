# V3 evidence contract

Each case retains the existing checker fields and adds `schema_version: 3`, a
nonempty `claim` naming the specific suspicion, and `issue_type` from
`information_boundary`, `experimental_protocol`, `task_integrity`, `acquisition_gap`,
`security_outcome`.

`assessment` has these fields:

```json
{
  "information_level": "exact_query",
  "policy_application": {
    "policy_kind": "attacker_knowledge_constraint",
    "status": "applicable",
    "reference": "fixed paper/source location proving applicability",
    "reason": "why this rule applies to this actor, phase, arm and information instance"
  },
  "delivery": {
    "status": "confirmed",
    "evidence_kind": "saved_request",
    "task_relation": "same_evaluated_instance",
    "reference": "source-to-recipient input-boundary evidence",
    "reason": "how the information actually reaches the claimed recipient"
  },
  "refutation": {
    "basis": "none",
    "reference": "",
    "reason": "no positive counterevidence establishes this suspicion false"
  }
}
```

Enums:

- information_level: exact_query, partial_query, task_category, document_content,
  runtime_trace, user_identity, resource_metadata, other.
- policy_application.policy_kind: attacker_knowledge_constraint,
  victim_security_goal, protocol_requirement, unspecified.
- policy_application.status: applicable, not_applicable, uncertain.
- delivery.status: confirmed, excluded, evaluator_only, unresolved.
- delivery.evidence_kind: paper_procedure, static_bound_path, saved_request,
  runtime, document_presence, possible_path, not_applicable.
- delivery.task_relation: same_evaluated_instance, training_instance, topic_only,
  different_instance, unknown.
- refutation.basis: none, explicit_permission, different_instance,
  excluded_delivery, different_issue_type.

Reasons must be nonempty. Affirmative policy, delivery and refutation judgments
need nonempty source references. Empty reference is allowed only for unresolved
judgments and a `none` refutation. Do not invent prohibitions or absences.

Confirmation requires applicable prohibition plus confirmed delivery supported
by a procedure, bound static path, saved request or runtime evidence. Mere document
presence and a possible path cannot confirm receipt. There must be matching
`deny` and `present` with no conflicting matched states. Training is not globally
permitted: an explicit prohibition that applies to training can still be violated.
The prohibition must be an attacker knowledge constraint, not the victim's
security goal. A successful exfiltration attack is not by itself a paper
threat-model inconsistency.

Refutation is scoped to the named claim. A specific permission, a proven distinct
instance, an excluded recipient boundary or a different issue type may refute that
claim. Merely missing evidence, reading all pages or selecting only allowed flows
does not establish a negative. The program does not establish source semantics
solely from these manually/model-produced flags.

Behavioral impact is separate optional metadata; lack of a significant effect
does not erase an established construction information flow.
