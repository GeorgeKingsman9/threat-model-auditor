# V7: original-URL audit results

2 fresh original-URL audit(s) only: MUZZLE, ObliInjection. This cohort is separate from earlier runs; older outcomes, curated findings and expected labels do not enter its denominator or model input.

A typed paper result combines knowledge-boundary violations, explicit construction-contract mismatches and bounded task-acquisition/deployment gaps. These types are retained separately. A deployment gap does not prove forbidden or impossible knowledge, historical execution, or an ASR effect.

| Paper | Audit status | Paper result | Knowledge-boundary result | Confirmed types | Calls / review retries |
| --- | --- | --- | --- | --- | --- |
| MUZZLE | completed | insufficient_evidence | insufficient_evidence | none | 4 / 0 |
| ObliInjection | completed | inconsistent | insufficient_evidence | construction_contract_mismatch | 4 / 0 |

At most 5 wrapper calls per paper, 10 total; at most one identical-payload review retry and 0 acquisition pass. Failed calls remain counted. Cumulative ledgers are counted once. Unknown actual model IDs remain null; unreported usage does not prove zero use.

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

#### 1. Original-task conditioning of the PAIR attacker model

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_policy_scope_not_established`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "muzzle/prototype/agents/pair.py::_run_pair; initialized attacker conversations", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The prototype supplies original_user_task through the selected webagent_prompt, conversation serialization and AttackLM API request. Its observability through permitted traces is unproved; operator provision supplies no knowledge exception.

Locations:

- paper paper:p5
- [modules/JailbreakingLLMs/PAIR/language_models.py:85–87](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/language_models.py#L85)
- [modules/JailbreakingLLMs/PAIR/system_prompts.py:140](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/system_prompts.py#L140)
- paper paper:p5
- paper paper:p6
- [muzzle/prototype/agents/pair.py:217](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L217)
- [modules/JailbreakingLLMs/PAIR/common.py:89](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/common.py#L89)
- [modules/JailbreakingLLMs/PAIR/system_prompts.py:3](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/system_prompts.py#L3)
- [modules/JailbreakingLLMs/PAIR/common.py:77–82](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/common.py#L77)
- [muzzle/prototype/agents/pair.py:239](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L239)
- [modules/JailbreakingLLMs/PAIR/conversers.py:143](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/conversers.py#L143)
- [modules/JailbreakingLLMs/PAIR/conversers.py:98](https://github.com/gsiros/ag-pair/blob/16518e2dacc3da823a39ec3bc28d692bacaf17b6/PAIR/conversers.py#L98)

#### 2. [declared-contract prose omitted] conditions PAIR conversation initialization

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `flow_binding_alignment_unverified`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "prototype reflection branch: component == \"instruction\"", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: Conditional reflection receipt is traceable: Explorer forwards details in reflection, handle_step assigns feedback, and webagent_prompt interpolates it into the same attacker request as flow 0. Judge adds assertion results to details. The proposed empty path and missing recipient citation do not represent this chain; downstream permission remains uncertain.

Locations:

- paper paper:p5
- [muzzle/prototype/agents/explorer.py:915](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/explorer.py#L915)
- [muzzle/prototype/agents/pair.py:218](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/pair.py#L218)

#### 3. Summarizer receives execution transcripts through its generation request

Type: `knowledge_boundary_violation`; result: **refuted**; reason: `bound_claim_refuted_explicit_permission`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "prototype SummarizerAgent.handle_transcript; BENIGN and ADVERSARIAL branches", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The handler stringifies its transcript and embeds it in the cited Summarizer model request. Paper pages 5–8 permit and prescribe this trace channel. No record mapping is supplied.

Locations:

- paper paper:p5
- [muzzle/prototype/agents/summarizer.py:48–52](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/summarizer.py#L48)
- paper paper:p6
- [muzzle/prototype/agents/summarizer.py:86](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/summarizer.py#L86)
- [muzzle/prototype/agents/summarizer.py:34](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/summarizer.py#L34)
- [muzzle/prototype/agents/summarizer.py:39](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/summarizer.py#L39)

#### 4. Judge receives malicious instructions and transcript evidence for evaluation

Type: `knowledge_boundary_violation`; result: **refuted**; reason: `bound_claim_refuted_evaluator_policy_inapplicable`.

Scope: {"paper_version": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "experiment_arm": "prototype JudgeAgent.handle_judge; optional assertion branch", "artifact_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The formatter and terminal call prove Judge receipt, including conditional assertion grounding expressly permitted on page 9. This endpoint does not exclude downstream constructor receipt; Explorer forwards its results in the instruction-reflection branch.

Locations:

- paper paper:p9
- [muzzle/prototype/agents/judge.py:290–291](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L290)
- paper paper:p9
- paper paper:p9
- [muzzle/prototype/agents/judge.py:285](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L285)
- paper paper:p9
- [muzzle/prototype/agents/judge.py:87](https://github.com/gsiros/muzzle/blob/9f3effa1668fa29dcba8f2454e711ddf9ef3c038/muzzle/prototype/agents/judge.py#L87)

### Invocation ledger

| Call | Stage | Status | Input / output tokens | Requested / actual model |
| --- | --- | --- | --- | --- |
| 1 | declared_contract | completed | 35042 / 5122 | gpt-6.1-sol / unknown |
| 2 | extraction | completed | 235475 / 10611 | gpt-6.1-sol / unknown |
| 3 | citation_repair | completed | 24903 / 245 | gpt-6.1-sol / unknown |
| 4 | semantic_review | completed | 241311 / 3272 | gpt-6.1-sol / unknown |

Paper-only declaration: untrusted_declared_contract_proposal; 77/78 citations mechanically located. The proposal is not permission evidence.

Input-channel closure: False; category closure: False. A confirmed bounded issue does not require all other candidates to be resolved.

## ObliInjection

Original input: https://arxiv.org/pdf/2512.09321v3

Result: **inconsistent**; reason: confirmed_typed_inconsistency_in_scope. Audit error: none.

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
| citation_validation_and_decision | completed | confirmed_typed_inconsistency_in_scope |

Repository: https://github.com/ReachalWang/ObliInjection at `b1f6a3f48c0cf121534374cbcef453832594867b`. Data files: 3; exact excerpts: 7.

### Findings and unresolved checks

#### 1. HotpotQA GCG receives the same record's precise question that its test evaluation uses.

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_query_form_information_level_conflict`.

Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "HotpotQA open-weight ObliInjection; raw fallback; args.target_data_indices=[0,33]; args.injected_data_num=1; first target evaluation", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: Optimizer receipt and conditional record-0 identity are proved. The question supplies the specific QA direction alongside the generic template; paper:p3-p4 and p8 partition the context into document segments. Separate question storage does not make this task information permitted. The proposed policy uncertainty is therefore unsupported.

Locations:

- paper paper:p4
- [obliinjection.py:79](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L79)
- paper paper:p17
- [task/task.py:18](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L18)
- [task/target_task.py:252–255](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L252)
- [task/target_task.py:292–296](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L292)
- [task/target_task.py:97](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L97)
- [task/target_task.py:113–116](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L113)
- [task/task.py:72](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L72)
- [obliinjection.py:33](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L33)
- [configs/task_configs/hotpotqa_config.json:24–26](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/configs/task_configs/hotpotqa_config.json#L24)
- [task/target_task.py:255](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L255)
- [task/target_task.py:271](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L271)
- [obliinjection.py:47](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L47)
- [gcg/gcg.py:473–475](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/gcg/gcg.py#L473)
- [gcg/gcg.py:655–657](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/gcg/gcg.py#L655)
- [task/target_task.py:35](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L35)

#### 2. GCG directly receives raw-record source documents for optimization, independently of its question input.

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_query_form_information_level_conflict`.

Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "HotpotQA open-weight ObliInjection; raw fallback; args.target_data_indices=[0,33]; args.injected_data_num=1", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The raw loader, selection, repetition and GCG.run argument prove document receipt. The clean-segment qualification prevents a blanket deny; this flow supplies no individual document mapping or established permission.

Locations:

- paper paper:p4
- [obliinjection.py:78](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L78)
- [task/target_task.py:250–255](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L250)
- [task/target_task.py:258](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L258)
- [task/target_task.py:293–295](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L293)
- [task/target_task.py:95](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L95)
- [task/target_task.py:113–114](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L113)
- [task/task.py:69](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L69)
- [obliinjection.py:33](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L33)
- [obliinjection.py:36](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L36)

#### 3. The optimization formatter receives a configured generic train instruction, distinct from the configured test instruction.

Type: `knowledge_boundary_violation`; result: **unresolved**; reason: `bound_query_form_information_level_conflict`.

Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "HotpotQA open-weight ObliInjection optimization", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}.

- Independent review: The actual optimizer construction call receives the generic train template. General task knowledge and proxy instructions are permitted. Different template text alone does not establish different record identity.

Locations:

- paper paper:p4
- [gcg/gcg.py:472–474](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/gcg/gcg.py#L472)
- paper paper:p4
- paper paper:p6
- [task/task.py:14](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L14)
- [task/target_task.py:26](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L26)

#### 4. The raw HotpotQA branch reuses the evaluated record's question where the stated construction uses a question proxy generated from question type.

Type: `construction_contract_mismatch`; result: **confirmed**; reason: `construction_contract_mismatch_confirmed`.

Scope: Only the linked HotpotQA raw fallback with [0,33], one injected task, and first target evaluation; no claim about caches or historical author runs..

- contract: The paper describes generating a question and supporting facts from question-type metadata, then optimizing with generated shadow inputs and separately generated validation inputs. (supported=True).
- implemented_source: In the conditional raw branch, train and test resolve to the same file, extract the same record-0 question, and pass it to optimization and test evaluation. This is record reuse, independently of whether that record was originally synthetic. (supported=True).
- exceptions: Multi-task optimization still generates shadow inputs per task. The distinct unseen-task transfer experiment does not authorize same-record reuse in this conditional arm. Possible clean-segment access concerns document contents rather than this question-generation contract. (supported=True).
- Comparison: For the same-record conditional arm proved in flow 0, the optimizer uses the evaluated record's precise question rather than a distinct question proxy constructed from type metadata. This establishes a bounded released-branch construction mismatch without establishing original question provenance or historical execution.
- Mapping: The code's generic instruction plus question is the complete task-specific QA direction, while formatted source documents provide context. The paper says each HotpotQA segment is a document and explicitly generates a question as part of the shadow-input recipe. Thus the separate question argument is a material construction component even though its formal placement within st versus xt remains uncertain.
- Independent review: Paper:p4-p6 and p17 prescribe generated shadow task information from metadata. Configuration, raw loaders, selection and singleton formatting positively bind the same record-0 question to optimization and first test evaluation under the stated conditional arm. This reuses evaluated task information instead of a separate question proxy. Clean-document access and unseen-task transfer provide no exception; original provenance and historical execution remain unproved.

Locations:

- paper paper:p17
- paper paper:p10
- paper paper:p6
- [configs/task_configs/hotpotqa_config.json:24–26](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/configs/task_configs/hotpotqa_config.json#L24)
- [task/target_task.py:255](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L255)
- [task/target_task.py:271](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L271)
- [obliinjection.py:79](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L79)
- paper paper:p3
- paper paper:p8
- paper paper:p17
- [task/target_task.py:35](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L35)
- [task/target_task.py:37](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L37)
- [task/target_task.py:40](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L40)
- [attacker/attacker.py:120](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/attacker/attacker.py#L120)
- paper paper:p8
- paper paper:p11
- paper paper:p4
- [task/task.py:72](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L72)
- [obliinjection.py:47](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L47)
- [gcg/gcg.py:473–475](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/gcg/gcg.py#L473)
- [gcg/gcg.py:655–657](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/gcg/gcg.py#L655)
- [task/task.py:18](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/task.py#L18)
- [task/target_task.py:252–255](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L252)
- [task/target_task.py:292–296](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L292)
- [task/target_task.py:97](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L97)
- [task/target_task.py:113–116](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/task/target_task.py#L113)
- [obliinjection.py:33](https://github.com/ReachalWang/ObliInjection/blob/b1f6a3f48c0cf121534374cbcef453832594867b/obliinjection.py#L33)

### Invocation ledger

| Call | Stage | Status | Input / output tokens | Requested / actual model |
| --- | --- | --- | --- | --- |
| 1 | declared_contract | completed | 37284 / 4781 | gpt-6.1-sol / unknown |
| 2 | extraction | completed | 136288 / 11603 | gpt-6.1-sol / unknown |
| 3 | citation_repair | completed | 33616 / 393 | gpt-6.1-sol / unknown |
| 4 | semantic_review | completed | 142988 / 2738 | gpt-6.1-sol / unknown |

Paper-only declaration: untrusted_declared_contract_proposal; 78/78 citations mechanically located. The proposal is not permission evidence.

Input-channel closure: False; category closure: False. A confirmed bounded issue does not require all other candidates to be resolved.
