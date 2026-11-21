# V6 declared-contract follow-up

Separate two-paper follow-up: ASPI and ObliInjection only. No original pilot attempts or verdicts enter this cohort or denominator.

Fresh URL-only follow-up adds an untrusted paper-only declaration phase and guarded citation recovery. Exact declaration locations do not validate policy meaning; independent source review and existing evidence gates still decide named claims. Static or sampled evidence establishes neither historical execution nor numerical effects.

Frozen commit: `15d8184ae20ef9d3d61dd5376b194aabb1d1eec7`. Recorded model invocations: 8.

| Paper | Status | Verdict | Inconsistency | Calls |
| --- | --- | --- | --- | --- |
| ASPI | completed | inconsistent | true | 4 |
| ObliInjection | completed | insufficient_evidence | null | 4 |

At most four recorded wrapper calls per paper: paper declaration, extraction, optional citation recovery, independent review. Cumulative ledgers are counted once; unknown actual model IDs stay null and missing usage never proves zero use.

Complete structured metadata is in report.json; original artifact hashes are in process_manifest.json.

## Selected final papers

### ASPI · 2026-11-21-v6-contract-followup/audits/aspi

Status: completed; phase outcome: completed; error code: none.

Reason: confirmed_inconsistency_in_scope. Model calls: 4.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; declared_contract=completed; extraction=completed; citation_repair=completed; semantic_review=completed; citation_validation_and_decision=completed.

Repository: https://github.com/scaleapi/aspi; revision: e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d.

Data files: 0; sampled files: 0; witnesses: 0.

Input channels: reviewed; 8 candidates; statuses {"unresolved": 6, "excluded": 2}; complete=false; truncated=true.

- Claim: Stage 2 injection generation receives instance-specific task and clarification metadata
  Result: confirmed; reason: bound_scoped_forbidden_delivery_confirmed; information level: partial_query.
  Scope: {"paper_version": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "experiment_arm": "Offline Stage 2 HR/GS/CP generation for clarif_user_HR, clarif_user_GS, and clarif_user_CP; conditional evaluation of generated grouped records", "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "segment_id": "paper:p3", "end": 3489, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "start": 3437}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 73, "source_kind": "code", "segment_id": "repo:src/aspi/common/litellm.py:L1-L151", "path": "src/aspi/common/litellm.py", "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 2353, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 73, "start": 2301, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 129, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 4662, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 134, "start": 4406, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 429, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 16277, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 436, "start": 16019, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 218, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 8172, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 220, "start": 8085, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 517, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 19704, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 520, "start": 19573, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 605, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 22863, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 605, "start": 22823, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1908, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 76050, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1911, "start": 75906, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 2153, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 86235, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 2156, "start": 86062, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1543, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61614, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1543, "start": 61552, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1550, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61878, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1550, "start": 61843, "repository_source": "https://github.com/scaleapi/aspi"}, {"source_kind": "paper", "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "segment_id": "paper:p13", "end": 201, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "start": 120}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 482, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 18219, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 485, "start": 18075, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 173, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 6213, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 173, "start": 6149, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 138, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 4835, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 138, "start": 4768, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 99, "source_kind": "code", "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809", "path": "src/aspi/dataset/pipeline.py", "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 3518, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 103, "start": 3330, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 132, "source_kind": "code", "segment_id": "repo:src/aspi/common/litellm.py:L1-L151", "path": "src/aspi/common/litellm.py", "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 5142, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 132, "start": 5092, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 125, "source_kind": "code", "segment_id": "repo:src/aspi/common/litellm.py:L1-L151", "path": "src/aspi/common/litellm.py", "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 4858, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 125, "start": 4794, "repository_source": "https://github.com/scaleapi/aspi"}]
- Claim: Evaluation-time attack construction receives the evaluated user-task object
  Result: unresolved; reason: bound_attacker_delivery_not_established; information level: other.
  Scope: {"paper_version": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "experiment_arm": "important_instructions or direct attack construction reused by exec_tool, clarif_tool, and clarif_ask_user", "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "segment_id": "paper:p3", "end": 3489, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "start": 3437}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1571, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 62903, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1571, "start": 62847, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1543, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61614, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1543, "start": 61552, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1550, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61878, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1550, "start": 61843, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1623, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 65217, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1627, "start": 65046, "repository_source": "https://github.com/scaleapi/aspi"}, {"source_kind": "paper", "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "segment_id": "paper:p5", "end": 1680, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "start": 1420}]
- Claim: Evaluation-time attack construction also receives the injection-task object
  Result: unresolved; reason: bound_policy_scope_not_established; information level: other.
  Scope: {"paper_version": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "experiment_arm": "important_instructions or direct attack construction reused by exec_tool, clarif_tool, and clarif_ask_user", "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "segment_id": "paper:p3", "end": 3489, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "start": 3437}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1571, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 62903, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1571, "start": 62847, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1544, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61691, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1544, "start": 61619, "repository_source": "https://github.com/scaleapi/aspi"}, {"repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "line_start": 1551, "source_kind": "code", "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317", "path": "src/aspi/eval/runner.py", "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55", "repository_manifest_sha256": "93664f66257e453655d0c74c0f4c6b65780a318c092be7e7f45859b265667ced", "end": 61922, "document_sha256": "9191b559dd7f2222dcca5a4e48742f2ec408d5d2133877b6e240ad9a805a52b1", "line_end": 1551, "start": 61883, "repository_source": "https://github.com/scaleapi/aspi"}]

Deployment auxiliary assessment: reviewed_no_named_findings; 0 named findings.

- Call 1 (declared_contract): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 44131, "cached_input_tokens": 0, "output_tokens": 6014, "reasoning_output_tokens": 45}.
- Call 2 (extraction): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 203914, "cached_input_tokens": 0, "output_tokens": 8024, "reasoning_output_tokens": 343}.
- Call 3 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 29364, "cached_input_tokens": 0, "output_tokens": 450, "reasoning_output_tokens": 99}.
- Call 4 (semantic_review): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 208590, "cached_input_tokens": 9216, "output_tokens": 1429, "reasoning_output_tokens": 127}.

### ObliInjection · 2026-11-21-v6-contract-followup/audits/obliinjection

Status: completed; phase outcome: completed; error code: none.

Reason: unresolved_checks. Model calls: 4.

Stages: ingestion=completed; source_discovery=completed; repository_ingestion=completed; declared_contract=completed; extraction=completed; citation_repair=completed; semantic_review=completed; citation_validation_and_decision=completed.

Repository: https://github.com/ReachalWang/ObliInjection; revision: b1f6a3f48c0cf121534374cbcef453832594867b.

Data files: 3; sampled files: 3; witnesses: 7.

- Data `data/amazon_reviews/amazon_reviews_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 1, "oversized_records": 56, "oversized_pointers": 0, "output_bytes": 30888, "omitted_records": 99, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_byte_limit", "record_sample_limit", "record_output_byte_limit"]}; sampled indices [1].
- Data `data/hotpotqa/hotpotqa_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 4, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 19946, "omitted_records": 96, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit"]}; sampled indices [0, 33, 66, 99].
- Data `data/multi_news/multi_news_shadow.json`: coverage {"raw_complete": true, "complete": false, "total_records": 100, "sampled_records": 2, "oversized_records": 0, "oversized_pointers": 0, "output_bytes": 26097, "omitted_records": 98, "sampling": "schema-diverse-then-spaced-v1", "omission_reasons": ["record_sample_limit", "record_output_byte_limit"]}; sampled indices [0, 33].

Input channels: reviewed; 28 candidates; statuses {"unresolved": 26, "represented": 2}; complete=false; truncated=true.

- Claim: HotpotQA question receipt at the GCG optimization input
  Result: unresolved; reason: bound_policy_scope_not_established; information level: exact_query.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "run.sh hotpotqa local-model optimization, conditional raw-data preparation branch", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p8", "end": 3865, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "start": 3783}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 75, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 3977, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 79, "start": 3759, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 79, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 3976, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 79, "start": 3933, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 16, "source_kind": "code", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "path": "configs/task_configs/hotpotqa_config.json", "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 785, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 16, "start": 760, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 24, "source_kind": "code", "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29", "path": "configs/task_configs/hotpotqa_config.json", "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 1111, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 26, "start": 951, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 255, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 12129, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 255, "start": 12053, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 271, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 13075, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 271, "start": 13002, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 103, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 4986, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 103, "start": 4884, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 72, "source_kind": "code", "segment_id": "repo:task/task.py:L1-L98", "path": "task/task.py", "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 2997, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 72, "start": 2932, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 33, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 1099, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 33, "start": 967, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 47, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 2284, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 47, "start": 2155, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 252, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 12129, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 255, "start": 11852, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 295, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 14671, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 295, "start": 14645, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 97, "source_kind": "code", "segment_id": "repo:task/target_task.py:L1-L309", "path": "task/target_task.py", "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 4566, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 97, "start": 4462, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 64, "source_kind": "code", "segment_id": "repo:task/task.py:L1-L98", "path": "task/task.py", "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 2645, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 64, "start": 2587, "repository_source": "https://github.com/ReachalWang/ObliInjection"}]
- Claim: Configured document records enter GCG optimization
  Result: unresolved; reason: bound_policy_scope_not_established; information level: document_content.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "run.sh local-model optimization for amazon_reviews, multi_news, or hotpotqa", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 972, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "start": 881}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 75, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 3924, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 78, "start": 3759, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 78, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 3923, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 78, "start": 3888, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"source_kind": "paper", "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 972, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "start": 920}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 33, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 1099, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 33, "start": 967, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 36, "source_kind": "code", "segment_id": "repo:obliinjection.py:L1-L213", "path": "obliinjection.py", "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 1337, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 36, "start": 1254, "repository_source": "https://github.com/ReachalWang/ObliInjection"}]
- Claim: Training instruction enters the attack message constructor
  Result: refuted; reason: bound_claim_refuted_explicit_permission; information level: other.
  Scope: {"paper_version": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "experiment_arm": "run.sh local-model training-context construction", "artifact_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Supplied paper and immutable source snapshot; no repository code executed"}
  Locators: [{"source_kind": "paper", "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 1834, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "start": 1753}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 332, "source_kind": "code", "segment_id": "repo:gcg/gcg.py:L1-L676", "path": "gcg/gcg.py", "file_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 16261, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 338, "start": 15962, "repository_source": "https://github.com/ReachalWang/ObliInjection"}, {"source_kind": "paper", "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "segment_id": "paper:p4", "end": 1790, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "start": 1753}, {"repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "line_start": 440, "source_kind": "code", "segment_id": "repo:gcg/gcg.py:L1-L676", "path": "gcg/gcg.py", "file_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898", "repository_manifest_sha256": "8cbf073c74b91bb4a3ec1104e9dea67c796a70b4aaa56edc68c1e9dc229352b9", "end": 22153, "document_sha256": "dd5d031e46cf91cea17a5bb6a909fd68a85f3c3ddacf42aa66c5dad0cef5aa7d", "line_end": 443, "start": 21891, "repository_source": "https://github.com/ReachalWang/ObliInjection"}]

Deployment auxiliary assessment: reviewed_no_named_findings; 0 named findings.

- Call 1 (declared_contract): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 37280, "cached_input_tokens": 0, "output_tokens": 4850, "reasoning_output_tokens": 53}.
- Call 2 (extraction): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 133593, "cached_input_tokens": 0, "output_tokens": 8660, "reasoning_output_tokens": 203}.
- Call 3 (citation_repair): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 22088, "cached_input_tokens": 0, "output_tokens": 229, "reasoning_output_tokens": 45}.
- Call 4 (semantic_review): completed; requested=gpt-6.1-sol; actual=null; actual IDs=[]; usage={"input_tokens": 138892, "cached_input_tokens": 0, "output_tokens": 2538, "reasoning_output_tokens": 60}.

## Earlier fresh attempts

## Material preflights: no paper verdicts

## Paper-only declaration metadata

### ASPI

```json
{
  "status": "validated_untrusted_proposal",
  "artifact_presence": {
    "declared_contract.request.json": true,
    "declared_contract.response.json": true,
    "declared_contract.json": true
  },
  "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
  "trust": "untrusted_declared_contract_proposal",
  "semantic_review_required": true,
  "citations_grounded": false,
  "counts": {
    "knowledge_rules": 5,
    "qualified_fields": 55,
    "task_input_components": 7,
    "task_input_relationships": 3,
    "recipe_inputs": 3,
    "generated_artifacts": 3,
    "unresolved_questions": 6,
    "limitations": 4,
    "proposed_citations": 107,
    "located_citations": 99,
    "citation_errors": 8
  },
  "qualification_counts": {
    "explicit": 43,
    "unspecified": 11,
    "uncertain": 1
  },
  "field_qualifications": [
    {
      "field": "knowledge_rules[0].role",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[0].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[0].source",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[0].allowed_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[0].forbidden_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "knowledge_rules[0].scope",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "knowledge_rules[0].exceptions",
      "qualification": "uncertain",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[1].role",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[1].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].source",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "knowledge_rules[1].allowed_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[1].forbidden_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].scope",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].exceptions",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[2].role",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].phase",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].source",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].allowed_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[2].forbidden_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[2].scope",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].exceptions",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].source",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[3].allowed_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[3].forbidden_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[3].scope",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[3].exceptions",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[4].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[4].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[4].source",
      "qualification": "explicit",
      "proposed_citation_count": 4,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[4].allowed_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[4].forbidden_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[4].scope",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "knowledge_rules[4].exceptions",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "task_input_definition.definition",
      "qualification": "explicit",
      "proposed_citation_count": 4,
      "located_citation_count": 3
    },
    {
      "field": "task_input_definition.components[0].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.components[1].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.components[2].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[3].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[4].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[5].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[6].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[0].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[1].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[2].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 6,
      "located_citation_count": 5
    },
    {
      "field": "construction_recipe.procedure",
      "qualification": "explicit",
      "proposed_citation_count": 6,
      "located_citation_count": 6
    },
    {
      "field": "construction_recipe.metadata_budget",
      "qualification": "explicit",
      "proposed_citation_count": 6,
      "located_citation_count": 6
    },
    {
      "field": "construction_recipe.scope",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "construction_recipe.inputs[0].description",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "construction_recipe.inputs[1].description",
      "qualification": "explicit",
      "proposed_citation_count": 5,
      "located_citation_count": 5
    },
    {
      "field": "construction_recipe.inputs[2].description",
      "qualification": "explicit",
      "proposed_citation_count": 4,
      "located_citation_count": 4
    },
    {
      "field": "construction_recipe.generated_artifacts[0].description",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "construction_recipe.generated_artifacts[1].description",
      "qualification": "explicit",
      "proposed_citation_count": 5,
      "located_citation_count": 5
    },
    {
      "field": "construction_recipe.generated_artifacts[2].description",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    }
  ],
  "citation_error_code_counts": {
    "citation_validation_error": 5,
    "ambiguous_citation": 3
  },
  "stages": [
    {
      "stage": "declared_contract",
      "status": "completed",
      "execution": "fresh_paper_only_call",
      "citations_grounded": false,
      "semantic_review_required": true,
      "citation_error_count": 8,
      "trust": "untrusted_declared_contract_proposal",
      "prompt_sha256": "b80246fdffcae4ac4f53829ddef864365df347ae2b4adf76a3cf83fa1f6dff5b"
    }
  ]
}
```

### ObliInjection

```json
{
  "status": "validated_untrusted_proposal",
  "artifact_presence": {
    "declared_contract.request.json": true,
    "declared_contract.response.json": true,
    "declared_contract.json": true
  },
  "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
  "trust": "untrusted_declared_contract_proposal",
  "semantic_review_required": true,
  "citations_grounded": false,
  "counts": {
    "knowledge_rules": 4,
    "qualified_fields": 50,
    "task_input_components": 7,
    "task_input_relationships": 5,
    "recipe_inputs": 3,
    "generated_artifacts": 3,
    "unresolved_questions": 5,
    "limitations": 4,
    "proposed_citations": 74,
    "located_citations": 73,
    "citation_errors": 1
  },
  "qualification_counts": {
    "explicit": 44,
    "unspecified": 4,
    "uncertain": 2
  },
  "field_qualifications": [
    {
      "field": "knowledge_rules[0].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[0].phase",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[0].source",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[0].allowed_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[0].forbidden_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 4,
      "located_citation_count": 4
    },
    {
      "field": "knowledge_rules[0].scope",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[0].exceptions",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].source",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].allowed_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].forbidden_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[1].scope",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[1].exceptions",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[2].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[2].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[2].source",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].allowed_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].forbidden_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].scope",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[2].exceptions",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[3].role",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].phase",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].source",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].allowed_knowledge",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "knowledge_rules[3].forbidden_knowledge",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "knowledge_rules[3].scope",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "knowledge_rules[3].exceptions",
      "qualification": "unspecified",
      "proposed_citation_count": 0,
      "located_citation_count": 0
    },
    {
      "field": "task_input_definition.definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[0].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[1].definition",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[2].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.components[3].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.components[4].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.components[5].definition",
      "qualification": "uncertain",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.components[6].definition",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[0].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[1].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[2].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "task_input_definition.relationships[3].relationship",
      "qualification": "uncertain",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "task_input_definition.relationships[4].relationship",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "construction_recipe.procedure",
      "qualification": "explicit",
      "proposed_citation_count": 3,
      "located_citation_count": 3
    },
    {
      "field": "construction_recipe.metadata_budget",
      "qualification": "explicit",
      "proposed_citation_count": 5,
      "located_citation_count": 5
    },
    {
      "field": "construction_recipe.scope",
      "qualification": "explicit",
      "proposed_citation_count": 4,
      "located_citation_count": 4
    },
    {
      "field": "construction_recipe.inputs[0].description",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "construction_recipe.inputs[1].description",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "construction_recipe.inputs[2].description",
      "qualification": "explicit",
      "proposed_citation_count": 2,
      "located_citation_count": 2
    },
    {
      "field": "construction_recipe.generated_artifacts[0].description",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "construction_recipe.generated_artifacts[1].description",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    },
    {
      "field": "construction_recipe.generated_artifacts[2].description",
      "qualification": "explicit",
      "proposed_citation_count": 1,
      "located_citation_count": 1
    }
  ],
  "citation_error_code_counts": {
    "ambiguous_citation": 1
  },
  "stages": [
    {
      "stage": "declared_contract",
      "status": "completed",
      "execution": "fresh_paper_only_call",
      "citations_grounded": false,
      "semantic_review_required": true,
      "citation_error_count": 1,
      "trust": "untrusted_declared_contract_proposal",
      "prompt_sha256": "b80246fdffcae4ac4f53829ddef864365df347ae2b4adf76a3cf83fa1f6dff5b"
    }
  ]
}
```

