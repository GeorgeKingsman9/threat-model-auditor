# V6 pilot results

Four selected paper results. Earlier failures and zero-inference material preflights are separate attempts, not extra papers or negative findings.

Development-case pilot, not an independent accuracy estimate. Static/sampled evidence is bounded to named claims and inspected source; no historical execution or numerical effect is established.

Frozen commit: `dc8314a83f23c95a34fef9e4e90eb2580ddb1f03`. Recorded model invocations: 11.

| Paper | Status | Verdict | Inconsistency | Calls |
| --- | --- | --- | --- | --- |
| ASPI | failed | technical_failure | null | 2 |
| MUZZLE | failed | technical_failure | null | 3 |
| ObliInjection | completed | insufficient_evidence | null | 3 |
| TopicAttack | completed | insufficient_evidence | null | 3 |

Counts are recorded wrapper invocations; final cumulative ledgers are counted once. Null actual model IDs remain unknown. Missing usage or ledgers do not prove zero use.

Complete structured metadata is in report.json; original artifact hashes are in process_manifest.json.

## Selected final papers

### ASPI · 2026-11-21-v6-pilot-165549/audits/aspi

Status: failed; phase outcome: failed; error code: citation_repair_error.

Reason: not recorded. Model calls: 2.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=completed; citation_repair=failed (citation_repair_error).

Repository: https://github.com/scaleapi/aspi; revision: e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 8 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.

- Call 1 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 179930, "cached_input_tokens": 0, "output_tokens": 9941, "reasoning_output_tokens": 403}.
- Call 2 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 40923, "cached_input_tokens": 0, "output_tokens": 126, "reasoning_output_tokens": 84}.

### MUZZLE · 2026-11-21-v6-pilot-165549/audits/muzzle-source-retry

Status: failed; phase outcome: failed; error code: semantic_review_error.

Reason: not recorded. Model calls: 3.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=completed; citation_repair=completed; semantic_review=failed (semantic_review_error).

Repository: https://github.com/gsiros/muzzle; revision: 9f3effa1668fa29dcba8f2454e711ddf9ef3c038.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 33 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.

- Call 1 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 215271, "cached_input_tokens": 0, "output_tokens": 7758, "reasoning_output_tokens": 259}.
- Call 2 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 23458, "cached_input_tokens": 0, "output_tokens": 229, "reasoning_output_tokens": 72}.
- Call 3 (semantic_review): cli_failed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={}.

### ObliInjection · 2026-11-21-v6-pilot-165549/audits/obliinjection

Status: completed; phase outcome: completed; error code: none.

Reason: unresolved_checks. Model calls: 3.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=completed; citation_repair=completed; semantic_review=completed; citation_validation_and_decision=completed.

Repository: https://github.com/ReachalWang/ObliInjection; revision: b1f6a3f48c0cf121534374cbcef453832594867b.

Data files: 3; sampled files: 3; witnesses: 7.

- Data `data/amazon_reviews/amazon_reviews_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 1, "oversized_records": 56, "oversized_pointers": 0, "output_bytes": 30888, "omitted_records": 99, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_byte_limit", "record_sample_limit", "record_output_byte_limit"]}; sampled indices [1].
- Data `data/hotpotqa/hotpotqa_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 4, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 19946, "omitted_records": 96, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit"]}; sampled indices [0, 33, 66, 99].
- Data `data/multi_news/multi_news_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 2, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 26097, "omitted_records": 98, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit", "record_output_byte_limit"]}; sampled indices [0, 33].

Input channels: reviewed; 28 candidates; statuses {"unresolved": 24, "excluded": 2, "represented": 2}; complete=false; truncated=true.

- Claim: Q1: The optimizer receives the configured HotpotQA question, including the same first selected question used for evaluation on the raw branch.
  Result: unresolved; reason: bound_policy_scope_not_established; information level: exact_query.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "ObliInjection / obliinjection.py / hotpotqa / supplied configuration / raw-loading branch / first selected question", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 643, "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 721}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 3759, "path": "obliinjection.py", "line_end": 80, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 75, "end": 4013, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 3933, "path": "obliinjection.py", "line_end": 79, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 79, "end": 3977, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 760, "path": "configs/task_configs/hotpotqa_config.json", "line_end": 16, "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "line_start": 16, "end": 785, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 951, "path": "configs/task_configs/hotpotqa_config.json", "line_end": 26, "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "line_start": 24, "end": 1111, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 12053, "path": "task/target_task.py", "line_end": 255, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 255, "end": 12129, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 13002, "path": "task/target_task.py", "line_end": 271, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 271, "end": 13075, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 4462, "path": "task/target_task.py", "line_end": 97, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 97, "end": 4566, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 4884, "path": "task/target_task.py", "line_end": 103, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 103, "end": 4986, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2155, "path": "obliinjection.py", "line_end": 47, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 47, "end": 2284, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2932, "path": "task/task.py", "line_end": 72, "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "segment_id": "repo:task/task.py:L1-L98", "line_start": 72, "end": 2997, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2587, "path": "task/task.py", "line_end": 64, "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "segment_id": "repo:task/task.py:L1-L98", "line_start": 64, "end": 2645, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 967, "path": "obliinjection.py", "line_end": 33, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 33, "end": 1099, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}]
- Claim: D1: The optimizer receives source-document lists from the configured raw records, which are also selected for test evaluation.
  Result: unresolved; reason: bound_policy_scope_not_established; information level: document_content.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "ObliInjection / obliinjection.py / hotpotqa / supplied configuration / raw-loading branch", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 881, "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 972}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 3759, "path": "obliinjection.py", "line_end": 78, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 75, "end": 3924, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 3888, "path": "obliinjection.py", "line_end": 78, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 78, "end": 3924, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 760, "path": "configs/task_configs/hotpotqa_config.json", "line_end": 16, "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "line_start": 16, "end": 785, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 951, "path": "configs/task_configs/hotpotqa_config.json", "line_end": 26, "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "line_start": 24, "end": 1111, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 11919, "path": "task/target_task.py", "line_end": 257, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 253, "end": 12168, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 12755, "path": "task/target_task.py", "line_end": 271, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 266, "end": 13015, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 4336, "path": "task/target_task.py", "line_end": 95, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 95, "end": 4385, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 4762, "path": "task/target_task.py", "line_end": 101, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 101, "end": 4809, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2155, "path": "obliinjection.py", "line_end": 47, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 47, "end": 2284, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2736, "path": "task/task.py", "line_end": 69, "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "segment_id": "repo:task/task.py:L1-L98", "line_start": 69, "end": 2793, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 2417, "path": "task/task.py", "line_end": 61, "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "segment_id": "repo:task/task.py:L1-L98", "line_start": 61, "end": 2467, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 967, "path": "obliinjection.py", "line_end": 33, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 33, "end": 1099, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 1254, "path": "obliinjection.py", "line_end": 36, "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "segment_id": "repo:obliinjection.py:L1-L213", "line_start": 36, "end": 1337, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}]
- Claim: T1: Optimization uses the configured training instruction; the source does not establish access to the distinct test instruction through this edge.
  Result: unresolved; reason: bound_policy_scope_not_established; information level: other.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "ObliInjection / obliinjection.py / initial optimization message construction / configured training instruction", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 486, "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 567}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 21891, "path": "gcg/gcg.py", "line_end": 443, "file_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898", "segment_id": "repo:gcg/gcg.py:L1-L676", "line_start": 440, "end": 22153, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"source_kind": "paper", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 1717, "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 1790}, {"source_kind": "paper", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 1717, "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 1834}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 341, "path": "task/task.py", "line_end": 14, "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "segment_id": "repo:task/task.py:L1-L98", "line_start": 14, "end": 394, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "source_kind": "code", "document_sha256": "df7ea038913292e65c888620907846576a799dd3954794fed4330038fa982de0", "start": 754, "path": "task/target_task.py", "line_end": 26, "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "segment_id": "repo:task/target_task.py:L1-L309", "line_start": 26, "end": 806, "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "repository_source": "https://github.com/ReachalWang/ObliInjection"}]

Deployment auxiliary assessment: reviewed_no_named_findings; 0 named findings.

- Call 1 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 115153, "cached_input_tokens": 0, "output_tokens": 10697, "reasoning_output_tokens": 385}.
- Call 2 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 41336, "cached_input_tokens": 0, "output_tokens": 467, "reasoning_output_tokens": 82}.
- Call 3 (semantic_review): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 122212, "cached_input_tokens": 0, "output_tokens": 2401, "reasoning_output_tokens": 71}.

### TopicAttack · 2026-11-21-v6-pilot-165549/audits/topicattack

Status: completed; phase outcome: completed; error code: none.

Reason: unresolved_checks. Model calls: 3.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=completed; citation_repair=completed; semantic_review=completed; citation_validation_and_decision=completed.

Repository: https://github.com/LukeChen-go/topicattack; revision: 2aced58ad6f3587c8ba064b5e5cad74a29ef41de.

Data files: 1; sampled files: 1; witnesses: 4.

- Data `data/crafted_instruction_data_squad_injection_qa.json`: coverage {"raw_complete": true, "complete": false, "total_records": 900, "sampled_records": 4, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 5703, "omitted_records": 896, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit"]}; sampled indices [0, 300, 599, 899].

Input channels: reviewed; 12 candidates; statuses {"unresolved": 11, "excluded": 1}; complete=false; truncated=true.

- Claim: Chatbot transition generator receives permitted benign document content
  Result: refuted; reason: bound_claim_refuted_explicit_permission; information level: document_content.
  Scope: {"paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "experiment_arm": "Chatbot TopicAttack offline construction; construct_attack.py defaults", "artifact_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 314, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p4", "end": 396}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 2885, "path": "chatbot.py", "line_end": 88, "file_sha256": "21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4", "segment_id": "repo:chatbot.py:L1-L172", "line_start": 81, "end": 3150, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 314, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p4", "end": 346}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 234, "path": "construct_attack.py", "line_end": 9, "file_sha256": "eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732", "segment_id": "repo:construct_attack.py:L1-L36", "line_start": 9, "end": 366, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 243, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p4", "end": 346}, {"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 209, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p13", "end": 280}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 661, "path": "construct_attack.py", "line_end": 18, "file_sha256": "eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732", "segment_id": "repo:construct_attack.py:L1-L36", "line_start": 18, "end": 695, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 700, "path": "construct_attack.py", "line_end": 20, "file_sha256": "eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732", "segment_id": "repo:construct_attack.py:L1-L36", "line_start": 19, "end": 800, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 371, "path": "construct_attack.py", "line_end": 10, "file_sha256": "eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732", "segment_id": "repo:construct_attack.py:L1-L36", "line_start": 10, "end": 442, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 1165, "path": "chatbot.py", "line_end": 42, "file_sha256": "21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4", "segment_id": "repo:chatbot.py:L1-L172", "line_start": 37, "end": 1368, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}]
- Claim: Chatbot attack callable receives a record containing the original question
  Result: unresolved; reason: bound_policy_scope_not_established; information level: exact_query.
  Scope: {"paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "experiment_arm": "Chatbot run_baselines.py default naive/none, raw Inj-SQuAD input", "artifact_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 3482, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p4", "end": 3544}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 293, "path": "shield.py", "line_end": 16, "file_sha256": "357bcc1d3d32054b13747f2f0e68a7ac7e111772cf0021836d40e7bfa1270c4d", "segment_id": "repo:shield.py:L1-L46", "line_start": 16, "end": 347, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 1436, "path": "run_baselines.py", "line_end": 42, "file_sha256": "f68b8988ba538b6343e5d5b80b665efc045f3a7b233384b67ade46b2d05117fb", "segment_id": "repo:run_baselines.py:L1-L74", "line_start": 42, "end": 1556, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 396, "path": "shield.py", "line_end": 18, "file_sha256": "357bcc1d3d32054b13747f2f0e68a7ac7e111772cf0021836d40e7bfa1270c4d", "segment_id": "repo:shield.py:L1-L46", "line_start": 18, "end": 492, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"source_kind": "paper", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 243, "paper_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7", "segment_id": "paper:p4", "end": 308}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 1168, "path": "run_baselines.py", "line_end": 41, "file_sha256": "f68b8988ba538b6343e5d5b80b665efc045f3a7b233384b67ade46b2d05117fb", "segment_id": "repo:run_baselines.py:L1-L74", "line_start": 36, "end": 1406, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}, {"repository_manifest_sha256": "ea80ca1f1e1851dc09cd98968cee47739650a7de9d68e0bf1386f98f9d13b684", "source_kind": "code", "document_sha256": "d83711bbe4f9e9a331fa1af9a3f20ab3223dd977b2a020134c9d1d3c87181c58", "start": 1271, "path": "run_baselines.py", "line_end": 39, "file_sha256": "f68b8988ba538b6343e5d5b80b665efc045f3a7b233384b67ade46b2d05117fb", "segment_id": "repo:run_baselines.py:L1-L74", "line_start": 39, "end": 1301, "repository_revision": "2aced58ad6f3587c8ba064b5e5cad74a29ef41de", "repository_source": "https://github.com/LukeChen-go/topicattack"}]

Deployment auxiliary assessment: reviewed_no_named_findings; 0 named findings.

- Call 1 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 74542, "cached_input_tokens": 0, "output_tokens": 5403, "reasoning_output_tokens": 121}.
- Call 2 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 16858, "cached_input_tokens": 0, "output_tokens": 152, "reasoning_output_tokens": 65}.
- Call 3 (semantic_review): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 77101, "cached_input_tokens": 0, "output_tokens": 1453, "reasoning_output_tokens": 114}.

## Earlier fresh attempts

### MUZZLE · 2026-11-21-v6-pilot-165549/audits/muzzle

Status: failed; phase outcome: failed; error code: required_source_unavailable.

Reason: not recorded. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; source_discovery=failed (required_source_unavailable).

Repository: unavailable; revision: unknown.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 0 candidates; statuses {}; complete=null; truncated=null.

Deployment auxiliary assessment: not_assessed; 0 named findings.


## Material preflights: no paper verdicts

### ASPI · 2026-11-21-v6-preflight-164433/aspi

Status: pending; phase outcome: prepared_without_inference; error code: none.

Reason: document_prepared_inference_not_run. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=not_run.

Repository: https://github.com/scaleapi/aspi; revision: e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 8 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.


### MUZZLE · 2026-11-21-v6-preflight-164433/muzzle

Status: pending; phase outcome: prepared_without_inference; error code: none.

Reason: document_prepared_inference_not_run. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=not_run.

Repository: https://github.com/gsiros/muzzle; revision: 9f3effa1668fa29dcba8f2454e711ddf9ef3c038.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 33 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.


### ObliInjection · 2026-11-21-v6-preflight-164433/obliinjection

Status: pending; phase outcome: prepared_without_inference; error code: none.

Reason: document_prepared_inference_not_run. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=not_run.

Repository: https://github.com/ReachalWang/ObliInjection; revision: b1f6a3f48c0cf121534374cbcef453832594867b.

Data files: 3; sampled files: 3; witnesses: 7.

- Data `data/amazon_reviews/amazon_reviews_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 1, "oversized_records": 56, "oversized_pointers": 0, "output_bytes": 30888, "omitted_records": 99, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_byte_limit", "record_sample_limit", "record_output_byte_limit"]}; sampled indices [1].
- Data `data/hotpotqa/hotpotqa_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 4, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 19946, "omitted_records": 96, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit"]}; sampled indices [0, 33, 66, 99].
- Data `data/multi_news/multi_news_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 2, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 26097, "omitted_records": 98, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit", "record_output_byte_limit"]}; sampled indices [0, 33].

Input channels: not_assessed; 28 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.


### TopicAttack · 2026-11-21-v6-preflight-164433/topicattack

Status: failed; phase outcome: failed; error code: required_source_unavailable.

Reason: not recorded. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; source_discovery=failed (required_source_unavailable).

Repository: unavailable; revision: unknown.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: not_assessed; 0 candidates; statuses {}; complete=null; truncated=null.

Deployment auxiliary assessment: not_assessed; 0 named findings.


### TopicAttack · 2026-11-21-v6-topicattack-discovery-retry/.

Status: pending; phase outcome: prepared_without_inference; error code: none.

Reason: document_prepared_inference_not_run. Model calls: 0.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; extraction=not_run.

Repository: https://github.com/LukeChen-go/topicattack; revision: 2aced58ad6f3587c8ba064b5e5cad74a29ef41de.

Data files: 1; sampled files: 1; witnesses: 4.

- Data `data/crafted_instruction_data_squad_injection_qa.json`: coverage {"raw_complete": true, "complete": false, "total_records": 900, "sampled_records": 4, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 5703, "omitted_records": 896, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit"]}; sampled indices [0, 300, 599, 899].

Input channels: not_assessed; 12 candidates; statuses {}; complete=null; truncated=true.

Deployment auxiliary assessment: not_assessed; 0 named findings.

