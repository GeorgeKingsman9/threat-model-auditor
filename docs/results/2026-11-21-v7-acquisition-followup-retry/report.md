# V7: original-URL audit results

1 fresh original-URL audit(s) only: MUZZLE. This cohort is separate from earlier runs; older outcomes, curated findings and expected labels do not enter its denominator or model input.

A typed paper result combines knowledge-boundary violations, explicit construction-contract mismatches and bounded task-acquisition/deployment gaps. These types are retained separately. A deployment gap does not prove forbidden or impossible knowledge, historical execution, or an ASR effect.

| Paper | Audit status | Paper result | Knowledge-boundary result | Confirmed types | Calls / review retries |
| --- | --- | --- | --- | --- | --- |
| MUZZLE | completed | insufficient_evidence | insufficient_evidence | none | 4 / 0 |

At most 6 wrapper calls per paper, 6 total; at most one identical-payload review retry and 1 acquisition pass. Failed calls remain counted. Cumulative ledgers are counted once. Unknown actual model IDs remain null; unreported usage does not prove zero use.

Full structured metadata: [report.json](report.json). Original artifact hashes: [process_manifest.json](process_manifest.json).

## MUZZLE

Original input: https://www.usenix.org/system/files/usenixsecurity26-syros.pdf

Result: **insufficient_evidence**; reason: unresolved_checks. Audit error: none.

### Process

| Stage | Status | Details |
| --- | --- | --- |
| ingestion | completed |  |
| source_discovery | completed | unique_self_associated_code_link_resolved_to_full_commit |
| repository_ingestion | completed |  |
| declared_contract | completed | fresh_paper_only_call |
| extraction | completed | fresh_model_call |
| citation_repair | completed |  |
| semantic_review | completed |  |
| citation_validation_and_decision | completed | unresolved_checks |

Repository: https://github.com/gsiros/muzzle at `9f3effa1668fa29dcba8f2454e711ddf9ef3c038`. Data files: 0; exact excerpts: 0.

### Findings and unresolved checks

#### 1. Operator task specification reaches the PAIR optimizer independently of the transcript

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_policy_scope_not_established`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "run_rtm.py main workflow; Explorer.handle_dispatched_task PROBE branch; PAIRAgent", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The PROBE branch forwards task_spec.instruction through PAIRConfig to the actual optimizer invocation. The common knowledge restriction covers optimization, but whether this task information is observable in permitted LLM I/O remains unresolved. Operator-input disclosure alone grants no exception.

Locations:

- paper paper:p5
- [muzzle/prototype/agents/pair.py:325](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L325)
- [muzzle/prototype/agents/explorer.py:793–798](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L793)
- paper paper:p5
- paper paper:p6
- [run_rtm.py:131–133](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L131)
- [run_rtm.py:137–140](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L137)
- [muzzle/prototype/agents/explorer.py:809–811](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L809)

#### 2. Reflection details reach the PAIR optimizer

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_policy_scope_not_established`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "run_rtm.py main workflow; Explorer.handle_reflection partial/failure with component == instruction", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: Judge details, including conditional assertion information, pass through Explorer reflection and PAIRConfig.feedback to _run_pair. Paper-described diagnosis and refinement support ordinary feedback, but do not clearly resolve optimizer access to every assertion-derived detail.

Locations:

- paper paper:p5
- [muzzle/prototype/agents/pair.py:325](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L325)
- [muzzle/prototype/agents/pair.py:316](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L316)
- paper paper:p9
- [muzzle/prototype/agents/judge.py:349–352](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L349)
- [muzzle/prototype/agents/explorer.py:913–916](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L913)
- [muzzle/prototype/agents/explorer.py:932–933](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L932)

#### 3. Judge model receives malicious instruction and execution transcript for evaluation

Type: `knowledge_boundary_violation`; result: **refuted**; reason: `bound_claim_refuted_explicit_permission`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "run_rtm.py main workflow; JudgeAgent.handle_judge", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The formatter and actual Judge model request establish evaluator receipt of the serialized analytical inputs. Paper p9 expressly permits transcript evaluation and conditional assertion grounding. This receiver-specific permission establishes no exclusion of downstream attacker access.

Locations:

- paper paper:p9
- [muzzle/prototype/agents/judge.py:290–293](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L290)
- paper paper:p9
- paper paper:p9
- [muzzle/prototype/agents/judge.py:285](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L285)
- paper paper:p9

#### 4. Online applicability leaves precise-task acquisition and transfer unresolved

Type: `task_acquisition_deployment_gap`; result: **unresolved**; reason: `deployment_contract_obligations_unresolved`.

Scope: Online applicability of the task-conditioned main workflow, separate from its sandbox experimental location..

- paper_claim: The threat model includes offline discovery followed by online execution. (supported=True).
- conditional_construction: The PROBE construction branch independently supplies the operator task to PAIR. (supported=True).
- required_knowledge: The exact task can materially influence generated payloads by aligning the malicious step with task completion. (supported=False).
- source_boundary: Discovery explicitly permits observation of local web-agent/LLM traffic. (supported=True).
- actual_source: The entry point loads a selected task file; Explorer forwards its instruction independently of the transcript. (supported=True).
- timing: First task knowledge comes from the loaded spec before Explorer emulates the benign task. Optimizer receipt occurs later, after probe observations. (supported=True).
- task_relation: Within the workflow, the task_spec instruction drives victim execution and the separate optimizer task field. This semantic alias does not establish a concrete historical record identity. (supported=False).
- deployment_scope: The stated scenario distinguishes discovery interception from deployment in the wild; sandbox ethics does not resolve task acquisition. (supported=True).
- Acquisition: unresolved; Operator-file provenance is established for the experiment. Acquisition of a future online victim's precise task through the permitted discovery channel is not established.
- Independent review: The online scenario and task-conditioned optimization are explicit, and the task is first loaded from an operator file before observation. However, the paper also explicitly starts discovery with a supplied task and later deploys crafted payloads; the evidence does not establish that online execution requires acquiring a different future victim's precise task. The acquisition/transfer question remains material but does not yet prove a gap.

Locations:

- paper paper:p4
- [muzzle/prototype/agents/explorer.py:793–798](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L793)
- [muzzle/prototype/agents/pair.py:325](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L325)
- [modules/JailbreakingLLMs/PAIR/system_prompts.py:137](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/system_prompts.py#L137)
- [run_rtm.py:131](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L131)
- paper paper:p4
- [run_rtm.py:133](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L133)
- [muzzle/prototype/agents/explorer.py:793–798](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L793)
- [muzzle/prototype/agents/explorer.py:956](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L956)
- [muzzle/prototype/agents/explorer.py:962](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L962)
- [muzzle/prototype/agents/explorer.py:159](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L159)
- [muzzle/prototype/agents/explorer.py:792–796](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L792)
- paper paper:p4
- paper paper:p5
- [run_rtm.py:131–133](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L131)
- [run_rtm.py:137–140](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/run_rtm.py#L137)
- [muzzle/prototype/agents/explorer.py:809–811](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L809)

### Invocation ledger

| Call | Stage | Status | Input / output tokens | Requested / actual model |
| --- | --- | --- | --- | --- |
| 1 | declared_contract | completed | 35042 / 4401 | gpt-6.1-sol / unknown |
| 2 | extraction | completed | 232940 / 10870 | gpt-6.1-sol / unknown |
| 3 | citation_repair | completed | 38590 / 452 | gpt-6.1-sol / unknown |
| 4 | semantic_review | completed | 239024 / 3359 | gpt-6.1-sol / unknown |

Paper-only declaration: untrusted_declared_contract_proposal; 66/67 citations mechanically located. The proposal is not permission evidence.

Input-channel closure: False; category closure: False. A confirmed bounded issue does not require all other candidates to be resolved.
