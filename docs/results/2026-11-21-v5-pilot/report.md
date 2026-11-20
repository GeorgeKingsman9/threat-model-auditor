# 论文审计：测试过程与结果

运行类型：V5 pilot: all execution attempts  
生成时间：2026\-11\-20T18:06:38\.423626\+00:00  
论文记录：10

主表每篇论文一行。“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。

## 本次运行汇总

```json
{
  "paper_results": {
    "count": 6,
    "statuses": {
      "completed": 6
    },
    "verdicts": {
      "insufficient_evidence": 6
    },
    "confirmed_inconsistencies": 0
  },
  "attempts": {
    "count": 7,
    "statuses": {
      "completed": 6,
      "failed": 1
    },
    "verdicts": {
      "insufficient_evidence": 6,
      "technical_failure": 1
    },
    "confirmed_inconsistencies": 0
  },
  "denominator_note": "Each run has one selected final per frozen paper; earlier failed attempts do not add papers. Displayed rows are attempts.",
  "model_invocation_count": 16,
  "invocation_count_complete": true,
  "usage": {
    "input_tokens": 1885954,
    "cached_input_tokens": 0,
    "output_tokens": 19865,
    "reasoning_output_tokens": 1582
  },
  "usage_reporting_complete": true,
  "scope_note": "Known development-case pilot; no independent accuracy estimate. Static source receipt does not establish historical execution or whole-repository correctness.",
  "usage_note": "Counts are wrapper CLI invocations. Stage ledgers are cumulative snapshots and are not added again. Unknown actual model IDs remain null. Missing usage does not prove zero use.",
  "runs": [
    {
      "run_id": "2026-11-21-v5-pilot-175505",
      "label": "V5 pilot",
      "created_at": "2026-11-20T17:55:05.183273+00:00",
      "code_commit": "caa324b4aecd599fd518dac281b96c51707c9c6c",
      "code_files_sha256": {
        "scan.py": "924ec125af907bc992726d7f6d8ede1c99d04bec2236f04579997236b30c3b2f",
        "source_bundle.py": "97df35758b3680021fdc439b53a69b03bfcddd63a81d25ea67c3532f5ca8385f",
        "source_discovery.py": "6720533635bc81a1cd5861e1d9d46b2352b3daa7fadd35592ddddf4b492dfe75",
        "evidence_expansion.py": "9c70267a2a5fc166f8b97b9d3dcf62d897cf56b205239d1ccd1003e3156b22a3",
        "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
        "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
        "extraction_v5.py": "b2dbd866ec2af4b1aba8d28c60bf7280257b1aaf10570c2bb1e2da3bf3eceb8f",
        "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
        "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
        "findings.py": "b7b51453a4ce53dd7097a1fd8804a3e810feb014a3971c8572427ac731aabe96",
        "citation_repair.py": "400e17b6e54c74ac25ecec5335a6ae566666f4b58753fedc4eec5112edcc4fb7",
        "codex_provider.py": "b70a294c7d66b39d3b13b7a5c3e09a6a980d31b86eebeca94dcdba23f71c34dd"
      },
      "frozen_config_sha256": "5605504e9c6c56289b6e763bef9fa09f8307a26750d08bb2cb41876301ee7270",
      "paper_summary": {
        "count": 3,
        "statuses": {
          "completed": 3
        },
        "verdicts": {
          "insufficient_evidence": 3
        },
        "confirmed_inconsistencies": 0
      },
      "attempt_summary": {
        "count": 3,
        "statuses": {
          "completed": 3
        },
        "verdicts": {
          "insufficient_evidence": 3
        },
        "confirmed_inconsistencies": 0
      },
      "selected_final_attempts": {
        "aspi": "aspi",
        "muzzle": "muzzle",
        "obliinjection": "obliinjection"
      },
      "paper_results": [
        {
          "paper_id": "aspi",
          "attempt_id": "aspi",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        },
        {
          "paper_id": "muzzle",
          "attempt_id": "muzzle",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        },
        {
          "paper_id": "obliinjection",
          "attempt_id": "obliinjection",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        }
      ],
      "attempt_results": [
        {
          "attempt_id": "aspi",
          "paper_id": "aspi",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 3,
          "selected_final": true
        },
        {
          "attempt_id": "muzzle",
          "paper_id": "muzzle",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 2,
          "selected_final": true
        },
        {
          "attempt_id": "obliinjection",
          "paper_id": "obliinjection",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 2,
          "selected_final": true
        }
      ],
      "frozen_limits": {
        "requested_model": "gpt-6.1-sol",
        "max_calls_per_paper": 3,
        "max_total_cli_calls": 9,
        "max_input_chars": 1200000,
        "max_code_chars": 500000,
        "source_fetch": "files",
        "require_source": true
      }
    },
    {
      "run_id": "2026-11-21-v5-1-pilot-020638",
      "label": "V5.1 pilot",
      "created_at": "2026-11-20T18:06:38.423626+00:00",
      "code_commit": "1202ddebfd2a85f29348d39de7be6a1b3c718459",
      "code_files_sha256": {
        "scan.py": "6f4973d8bca07a05abba247bf042c3ee0d4fcde7b6ff02710d85bbe80dc57d11",
        "source_bundle.py": "97df35758b3680021fdc439b53a69b03bfcddd63a81d25ea67c3532f5ca8385f",
        "source_discovery.py": "6720533635bc81a1cd5861e1d9d46b2352b3daa7fadd35592ddddf4b492dfe75",
        "evidence_expansion.py": "9c70267a2a5fc166f8b97b9d3dcf62d897cf56b205239d1ccd1003e3156b22a3",
        "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
        "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
        "extraction_v5.py": "9cb88bfd857d90ae75b6fb667c0d3a1952f4c22f569dfa7f08511baa72b100a9",
        "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
        "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
        "findings.py": "d5ff5e03081911982c6ee45011055e9e037918ef5ac8e02053980fbca552fcdd",
        "citation_repair.py": "400e17b6e54c74ac25ecec5335a6ae566666f4b58753fedc4eec5112edcc4fb7",
        "codex_provider.py": "b70a294c7d66b39d3b13b7a5c3e09a6a980d31b86eebeca94dcdba23f71c34dd"
      },
      "frozen_config_sha256": "04138c5c1fd5082793de03f95814803d5a33cdc992cab418930dc02bb5281135",
      "paper_summary": {
        "count": 3,
        "statuses": {
          "completed": 3
        },
        "verdicts": {
          "insufficient_evidence": 3
        },
        "confirmed_inconsistencies": 0
      },
      "attempt_summary": {
        "count": 4,
        "statuses": {
          "failed": 1,
          "completed": 3
        },
        "verdicts": {
          "technical_failure": 1,
          "insufficient_evidence": 3
        },
        "confirmed_inconsistencies": 0
      },
      "selected_final_attempts": {
        "aspi": "aspi-download-retry",
        "muzzle": "muzzle",
        "obliinjection": "obliinjection"
      },
      "paper_results": [
        {
          "paper_id": "aspi",
          "attempt_id": "aspi-download-retry",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        },
        {
          "paper_id": "muzzle",
          "attempt_id": "muzzle",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        },
        {
          "paper_id": "obliinjection",
          "attempt_id": "obliinjection",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "has_confirmed_inconsistency": false
        }
      ],
      "attempt_results": [
        {
          "attempt_id": "aspi",
          "paper_id": "aspi",
          "status": "failed",
          "verdict": "technical_failure",
          "invocation_count": 0,
          "selected_final": false
        },
        {
          "attempt_id": "aspi-download-retry",
          "paper_id": "aspi",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 3,
          "selected_final": true
        },
        {
          "attempt_id": "muzzle",
          "paper_id": "muzzle",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 3,
          "selected_final": true
        },
        {
          "attempt_id": "obliinjection",
          "paper_id": "obliinjection",
          "status": "completed",
          "verdict": "insufficient_evidence",
          "invocation_count": 3,
          "selected_final": true
        }
      ],
      "frozen_limits": {
        "requested_model": "gpt-6.1-sol",
        "max_calls_per_paper": 3,
        "max_total_cli_calls": 9,
        "max_input_chars": 1200000,
        "max_code_chars": 500000,
        "source_fetch": "files",
        "require_source": true
      }
    }
  ],
  "deterministic_revalidation": {
    "cohort_type": "deterministic_revalidation",
    "based_on_run": "2026-11-21-v5-1-pilot-020638",
    "model_invocation_count": 0,
    "independent_inference": false,
    "paper_summary": {
      "count": 3,
      "statuses": {
        "completed": 3
      },
      "verdicts": {
        "inconsistent": 1,
        "insufficient_evidence": 2
      },
      "confirmed_inconsistencies": 1
    },
    "created_at": "2026-11-20T18:15:55.757849+00:00",
    "code_commit": "dcc3f28db50e99571393cee2763c4d88a2e458bf",
    "code_files_sha256": {
      "extraction_v5.py": "e6cb06f2cec52922b5756fb586801beefd7df68964d7e84268decf98ca47a1ac",
      "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
      "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
      "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
      "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
      "call_boundaries.py": "939b8812406d0b0d038d72d3755a2514a977fbb97cdb7558d66ebea8794aa5cf",
      "findings.py": "d5ff5e03081911982c6ee45011055e9e037918ef5ac8e02053980fbca552fcdd"
    },
    "metadata_path": "revalidated/revalidation_metadata.json",
    "metadata_sha256": "1175304ad2226e7b5c66989328e7545ede43d745029c843a4fa75534ca1dbdbb"
  }
}
```

## 论文结果

| 论文 ID | 论文 | 运行 / 判定 | 已确认不一致 | 标签对照 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 2026\-11\-21\-v5\-pilot\-175505/aspi/aspi | V5 pilot · ASPI · aspi | 证据不足 | 未确认 | 未评分 | https://arxiv\.org/pdf/2605\.17324v1 |
| 2026\-11\-21\-v5\-pilot\-175505/muzzle/muzzle | V5 pilot · MUZZLE · muzzle | 证据不足 | 未确认 | 未评分 | https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf |
| 2026\-11\-21\-v5\-pilot\-175505/obliinjection/obliinjection | V5 pilot · ObliInjection · obliinjection | 证据不足 | 未确认 | 未评分 | https://arxiv\.org/pdf/2512\.09321v3 |
| 2026\-11\-21\-v5\-1\-pilot\-020638/aspi/aspi | V5\.1 pilot · ASPI · aspi | 运行失败 | 未给出 | 未评分 | https://arxiv\.org/pdf/2605\.17324v1 |
| 2026\-11\-21\-v5\-1\-pilot\-020638/aspi/aspi\-download\-retry | V5\.1 pilot · ASPI · aspi\-download\-retry | 证据不足 | 未确认 | 未评分 | https://arxiv\.org/pdf/2605\.17324v1 |
| 2026\-11\-21\-v5\-1\-pilot\-020638/muzzle/muzzle | V5\.1 pilot · MUZZLE · muzzle | 证据不足 | 未确认 | 未评分 | https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf |
| 2026\-11\-21\-v5\-1\-pilot\-020638/obliinjection/obliinjection | V5\.1 pilot · ObliInjection · obliinjection | 证据不足 | 未确认 | 未评分 | https://arxiv\.org/pdf/2512\.09321v3 |
| 2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/aspi | V5\.1 pilot · deterministic revalidation · ASPI | 有已确认的不一致 | 有 | 未评分 | https://arxiv\.org/pdf/2605\.17324v1 |
| 2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/muzzle | V5\.1 pilot · deterministic revalidation · MUZZLE | 证据不足 | 未确认 | 未评分 | https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf |
| 2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/obliinjection | V5\.1 pilot · deterministic revalidation · ObliInjection | 证据不足 | 未确认 | 未评分 | https://arxiv\.org/pdf/2512\.09321v3 |

## 逐篇测试过程

### 1. V5 pilot · ASPI · aspi

论文 ID：2026\-11\-21\-v5\-pilot\-175505/aspi/aspi  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 34, "characters": 149931, "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "manifest\_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8", "source\_segments": 32, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 32, "included\_files": 32, "omitted\_files": 0, "excluded\_entries": 6, "characters": 464472, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "fresh\_model\_call"\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 2, "remaining\_issues": 0, "classification\_fields\_modified": false\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_constructor",
      "attacker_delivery": "unresolved",
      "instance_requirement": "unspecified",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_requirement_policy_scope_unverified",
        "attacker_delivery_path_not_established"
      ]
    },
    "source_validation": {
      "policy_supported": false,
      "delivery_supported": false,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "scope_resolution_unresolved",
        "source_path_disconnected",
        "source_path_disconnected",
        "source_path_disconnected",
        "source_path_recipient_delivery_boundary_not_aligned",
        "instance_requirement_policy_scope_unverified",
        "attacker_delivery_path_not_established"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p3",
        "start": 3437,
        "end": 3489,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
        "source_kind": "paper",
        "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 3443,
        "end": 3518,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 103,
        "line_end": 103
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4768,
        "end": 4835,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 138,
        "line_end": 138
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 16019,
        "end": 16277,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 429,
        "line_end": 436
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4156,
        "end": 4250,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 121,
        "line_end": 122
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 18107,
        "end": 18367,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 482,
        "line_end": 490
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 6149,
        "end": 6213,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 173,
        "line_end": 173
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4456,
        "end": 4693,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 131,
        "line_end": 134
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 3330,
        "end": 3518,
        "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 99,
        "line_end": 103
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-pilot-175505/aspi/aspi",
  "title": "V5 pilot · ASPI · aspi",
  "run_id": "2026-11-21-v5-pilot-175505",
  "run_label": "V5 pilot",
  "paper_id": "aspi",
  "attempt_id": "aspi",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/aspi/result.json",
  "source": "https://arxiv.org/pdf/2605.17324v1",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 34,
      "characters": 149931,
      "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
      "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
      "source_segments": 32,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 32,
        "included_files": 32,
        "omitted_files": 0,
        "excluded_entries": 6,
        "characters": 464472,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "fresh_model_call"
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 2,
      "remaining_issues": 0,
      "classification_fields_modified": false
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1
  },
  "document_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
  "input_binding": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
  "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77",
  "request_hashes": {
    "input_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
    "model_content_sha256": "cfc1c420ce20761cb915d2936d79d26a7c54cc3b622bbc4f5f3dbefe4bcc6b94",
    "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77"
  },
  "repository": {
    "url": "https://github.com/scaleapi/aspi",
    "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
    "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 32,
      "included_files": 32,
      "omitted_files": 0,
      "excluded_entries": 6,
      "characters": 464472,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 350,
      "unresolved": 321,
      "over_limit": 0
    },
    "evidence_expansion_counts": {
      "added_files": 0,
      "added_bytes": 0,
      "inspected_paths": 32
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/scaleapi/aspi"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 3,
    "calls": [
      {
        "invocation": 1,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "7da46424f2d981b2f5478872dd5c231db2efa7b3512d1182f94d4803cdd82743",
        "usage": {
          "input_tokens": 173485,
          "cached_input_tokens": 0,
          "output_tokens": 2343,
          "reasoning_output_tokens": 144
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "d7683c2acc2109d4c07c7848c9a844b144108ecfcf60403248ddb03266b5e1cb",
        "usage": {
          "input_tokens": 16817,
          "cached_input_tokens": 0,
          "output_tokens": 92,
          "reasoning_output_tokens": 0
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 3,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "c2a7ce90e0076974f99cbffbc423146103088dd6a372c9578050ec441e74aba7",
        "usage": {
          "input_tokens": 174297,
          "cached_input_tokens": 0,
          "output_tokens": 404,
          "reasoning_output_tokens": 96
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 364599,
      "cached_input_tokens": 0,
      "output_tokens": 2839,
      "reasoning_output_tokens": 240
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 3,
    "preflight_failure_count": 0
  },
  "duration_seconds": 130.083,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_constructor",
        "attacker_delivery": "unresolved",
        "instance_requirement": "unspecified",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_requirement_policy_scope_unverified",
          "attacker_delivery_path_not_established"
        ]
      },
      "source_validation": {
        "policy_supported": false,
        "delivery_supported": false,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "scope_resolution_unresolved",
          "source_path_disconnected",
          "source_path_disconnected",
          "source_path_disconnected",
          "source_path_recipient_delivery_boundary_not_aligned",
          "instance_requirement_policy_scope_unverified",
          "attacker_delivery_path_not_established"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p3",
          "start": 3437,
          "end": 3489,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
          "source_kind": "paper",
          "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 3443,
          "end": 3518,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 103,
          "line_end": 103
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4768,
          "end": 4835,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 138,
          "line_end": 138
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 16019,
          "end": 16277,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 429,
          "line_end": 436
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4156,
          "end": 4250,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 121,
          "line_end": 122
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 18107,
          "end": 18367,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 482,
          "line_end": 490
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 6149,
          "end": 6213,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 173,
          "line_end": 173
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4456,
          "end": 4693,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 131,
          "line_end": 134
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 3330,
          "end": 3518,
          "document_sha256": "bd9c0ef304d99cefa2b7b13cf7b19aecf0b9ebbd35304e0ca430699556b9a450",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 99,
          "line_end": 103
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Does the paper's specific injection-construction procedure grant its offline constructor task knowledge despite the common restriction on access to the specific user task?",
    "Which concrete construction output_path was consumed by evaluation args.dataset, and which stable suite/user_task_id/injection_task_id bindings connect the generated and evaluated records?",
    "Which evaluation configuration selected the supplied pre-generated operator variants, simulator model, and attack branch for the reported experiments?"
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 2. V5 pilot · MUZZLE · muzzle

论文 ID：2026\-11\-21\-v5\-pilot\-175505/muzzle/muzzle  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 21, "characters": 124184, "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "manifest\_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a", "source\_segments": 106, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 106, "included\_files": 106, "omitted\_files": 0, "excluded\_entries": 129, "characters": 445602, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "fresh\_model\_call"\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "audit\_scope\_not\_fully\_covered"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "consistent_within_scope",
    "reason": "bound_claim_refuted_explicit_permission",
    "claim_result": "refuted",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "unresolved",
      "instance_requirement": "unspecified",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "attacker_delivery_path_not_established"
      ]
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": false,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "source_path_disconnected",
        "source_path_disconnected",
        "source_path_disconnected",
        "source_path_recipient_delivery_boundary_not_aligned",
        "attacker_delivery_path_not_established"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 254,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14079,
        "end": 14127,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 314,
        "line_end": 314
      },
      {
        "segment_id": "paper:p5",
        "start": 111,
        "end": 179,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "paper:p6",
        "start": 1687,
        "end": 1793,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14614,
        "end": 14680,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 325,
        "line_end": 325
      },
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 179,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "paper:p8",
        "start": 2065,
        "end": 2146,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
        "start": 6878,
        "end": 6909,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "source_kind": "code",
        "path": "muzzle/prototype/utils/network/vllm_proxy.py",
        "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 185,
        "line_end": 185
      },
      {
        "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
        "start": 5923,
        "end": 5986,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "source_kind": "code",
        "path": "muzzle/prototype/utils/network/vllm_proxy.py",
        "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 159,
        "line_end": 159
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 32885,
        "end": 32999,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 780,
        "line_end": 781
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 34319,
        "end": 34434,
        "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 809,
        "line_end": 811
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-pilot-175505/muzzle/muzzle",
  "title": "V5 pilot · MUZZLE · muzzle",
  "run_id": "2026-11-21-v5-pilot-175505",
  "run_label": "V5 pilot",
  "paper_id": "muzzle",
  "attempt_id": "muzzle",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/muzzle/result.json",
  "source": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "audit_scope_not_fully_covered",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 21,
      "characters": 124184,
      "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
      "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
      "source_segments": 106,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 106,
        "included_files": 106,
        "omitted_files": 0,
        "excluded_entries": 129,
        "characters": 445602,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "fresh_model_call"
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "audit_scope_not_fully_covered"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "refuted": 1
  },
  "document_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
  "input_binding": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
  "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77",
  "request_hashes": {
    "input_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
    "model_content_sha256": "13c27ad40acdb19ffd648d55b11f85cb542946d1bcfa3522efafd456a025f83d",
    "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77"
  },
  "repository": {
    "url": "https://github.com/gsiros/muzzle",
    "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
    "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 106,
      "included_files": 106,
      "omitted_files": 0,
      "excluded_entries": 129,
      "characters": 445602,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 1,
    "dependency_reference_counts": {
      "needed": 1025,
      "unresolved": 817,
      "over_limit": 1
    },
    "evidence_expansion_counts": {
      "added_files": 25,
      "added_bytes": 21498,
      "inspected_paths": 88
    },
    "dependencies": [
      {
        "mount_path": "modules/JailbreakingLLMs",
        "url": "https://github.com/gsiros/ag-pair",
        "revision": "16518e2dacc3da823a39ec3bc28d692bacaf17b6",
        "coverage": {
          "complete": false,
          "inventory_complete": true,
          "eligible_files": 37,
          "included_files": 36,
          "omitted_files": 1,
          "excluded_entries": 30,
          "characters": 143726,
          "max_characters": 150000
        }
      }
    ]
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/gsiros/muzzle"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 2,
    "calls": [
      {
        "invocation": 1,
        "stage": "extraction",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "bf73aa2d6cde0b59513cd21075dac88110ea3a5f6a517cc749b682c85f14a0d6",
        "usage": {
          "input_tokens": 199038,
          "cached_input_tokens": 0,
          "output_tokens": 2294,
          "reasoning_output_tokens": 205
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "55d92ed2b031b7f83e78d177ee2fa8ba13b86cfbdb05fc5f02d6348c26d86feb",
        "usage": {
          "input_tokens": 199630,
          "cached_input_tokens": 0,
          "output_tokens": 376,
          "reasoning_output_tokens": 37
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 398668,
      "cached_input_tokens": 0,
      "output_tokens": 2670,
      "reasoning_output_tokens": 242
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 2,
    "preflight_failure_count": 0
  },
  "duration_seconds": 154.587,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "consistent_within_scope",
      "reason": "bound_claim_refuted_explicit_permission",
      "claim_result": "refuted",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "unresolved",
        "instance_requirement": "unspecified",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "attacker_delivery_path_not_established"
        ]
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": false,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "source_path_disconnected",
          "source_path_disconnected",
          "source_path_disconnected",
          "source_path_recipient_delivery_boundary_not_aligned",
          "attacker_delivery_path_not_established"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 254,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14079,
          "end": 14127,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 314,
          "line_end": 314
        },
        {
          "segment_id": "paper:p5",
          "start": 111,
          "end": 179,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "paper:p6",
          "start": 1687,
          "end": 1793,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14614,
          "end": 14680,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 325,
          "line_end": 325
        },
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 179,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "paper:p8",
          "start": 2065,
          "end": 2146,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
          "start": 6878,
          "end": 6909,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "source_kind": "code",
          "path": "muzzle/prototype/utils/network/vllm_proxy.py",
          "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 185,
          "line_end": 185
        },
        {
          "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
          "start": 5923,
          "end": 5986,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "source_kind": "code",
          "path": "muzzle/prototype/utils/network/vllm_proxy.py",
          "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 159,
          "line_end": 159
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 32885,
          "end": 32999,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 780,
          "line_end": 781
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 34319,
          "end": 34434,
          "document_sha256": "6c2ef9d2f302fc6904204be3e79a53ecca4bc383a4922c60b6457fcf822f17a8",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 809,
          "line_end": 811
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Which concrete --spec file, AGENT_CONFIG_PATH, BROWSER_CONFIG_PATH, and model environment settings selected the reported main-workflow runs?",
    "Which installed PAIR module resolved the dynamic imports, and does it match the pinned dependency snapshot?",
    "What stable run and transcript record identifiers connect a concrete PROBE source record to its final evaluated attack run?"
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 3. V5 pilot · ObliInjection · obliinjection

论文 ID：2026\-11\-21\-v5\-pilot\-175505/obliinjection/obliinjection  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 18, "characters": 136067, "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "manifest\_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b", "source\_segments": 31, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 31, "included\_files": 31, "omitted\_files": 0, "excluded\_entries": 7, "characters": 147332, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "fresh\_model\_call"\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "unresolved",
      "instance_requirement": "unspecified",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_requirement_policy_scope_unverified",
        "attacker_delivery_path_not_established"
      ]
    },
    "source_validation": {
      "policy_supported": false,
      "delivery_supported": false,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "scope_resolution_unresolved",
        "source_path_disconnected",
        "source_path_recipient_delivery_boundary_not_aligned",
        "instance_requirement_policy_scope_unverified",
        "attacker_delivery_path_not_established"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p4",
        "start": 881,
        "end": 972,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
        "source_kind": "paper",
        "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 4268,
        "end": 4302,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 86,
        "line_end": 86
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 4268,
        "end": 4353,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 86,
        "line_end": 87
      },
      {
        "segment_id": "repo:gcg/gcg.py:L1-L676",
        "start": 20126,
        "end": 20139,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898",
        "source_kind": "code",
        "path": "gcg/gcg.py",
        "file_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 404,
        "line_end": 404
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2417,
        "end": 2467,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 61,
        "line_end": 61
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2736,
        "end": 2793,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 69,
        "line_end": 69
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 2155,
        "end": 2284,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 47,
        "line_end": 47
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 2432,
        "end": 2543,
        "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 50,
        "line_end": 50
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-pilot-175505/obliinjection/obliinjection",
  "title": "V5 pilot · ObliInjection · obliinjection",
  "run_id": "2026-11-21-v5-pilot-175505",
  "run_label": "V5 pilot",
  "paper_id": "obliinjection",
  "attempt_id": "obliinjection",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/obliinjection/result.json",
  "source": "https://arxiv.org/pdf/2512.09321v3",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 18,
      "characters": 136067,
      "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
      "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
      "source_segments": 31,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 31,
        "included_files": 31,
        "omitted_files": 0,
        "excluded_entries": 7,
        "characters": 147332,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "fresh_model_call"
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1
  },
  "document_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
  "input_binding": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
  "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77",
  "request_hashes": {
    "input_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
    "model_content_sha256": "0ffc8c4b2c6fafd93665bae0fa051a7f76db6c3fc399ea6ea9eec66180ae4114",
    "prompt_sha256": "226c274a636a455787eb5e3d373c53976d7f358dfdb445a55c90a101af5e5a77"
  },
  "repository": {
    "url": "https://github.com/ReachalWang/ObliInjection",
    "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
    "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 31,
      "included_files": 31,
      "omitted_files": 0,
      "excluded_entries": 7,
      "characters": 147332,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 225,
      "unresolved": 176,
      "over_limit": 9
    },
    "evidence_expansion_counts": {
      "added_files": 12,
      "added_bytes": 7062,
      "inspected_paths": 31
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/ReachalWang/ObliInjection"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 2,
    "calls": [
      {
        "invocation": 1,
        "stage": "extraction",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "330f4e909aef3ddda6bb6ec263c660aa1bd32e9d7fbbe04354ae3245cdaff1bf",
        "usage": {
          "input_tokens": 80464,
          "cached_input_tokens": 0,
          "output_tokens": 2025,
          "reasoning_output_tokens": 220
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "b62a4102d5ad5b544581464a64fb29d38e2fa8fb02e7289b204a44f2a8a400c0",
        "usage": {
          "input_tokens": 80792,
          "cached_input_tokens": 0,
          "output_tokens": 389,
          "reasoning_output_tokens": 45
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 161256,
      "cached_input_tokens": 0,
      "output_tokens": 2414,
      "reasoning_output_tokens": 265
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 2,
    "preflight_failure_count": 0
  },
  "duration_seconds": 94.483,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "unresolved",
        "instance_requirement": "unspecified",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_requirement_policy_scope_unverified",
          "attacker_delivery_path_not_established"
        ]
      },
      "source_validation": {
        "policy_supported": false,
        "delivery_supported": false,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "scope_resolution_unresolved",
          "source_path_disconnected",
          "source_path_recipient_delivery_boundary_not_aligned",
          "instance_requirement_policy_scope_unverified",
          "attacker_delivery_path_not_established"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p4",
          "start": 881,
          "end": 972,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
          "source_kind": "paper",
          "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 4268,
          "end": 4302,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 86,
          "line_end": 86
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 4268,
          "end": 4353,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 86,
          "line_end": 87
        },
        {
          "segment_id": "repo:gcg/gcg.py:L1-L676",
          "start": 20126,
          "end": 20139,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898",
          "source_kind": "code",
          "path": "gcg/gcg.py",
          "file_sha256": "0a0596100dc82f0ea86909a9b317b4860a58cfa00d8389e394c3e9bbdcf48898",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 404,
          "line_end": 404
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2417,
          "end": 2467,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 61,
          "line_end": 61
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2736,
          "end": 2793,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 69,
          "line_end": 69
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 2155,
          "end": 2284,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 47,
          "line_end": 47
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 2432,
          "end": 2543,
          "document_sha256": "6ea9edd51f61a5c6437b083c8ce196fd4f9f3ffdc27a1dc4c2b68672c2c3ffc6",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 50,
          "line_end": 50
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Did TargetTask.__prepare_data load existing processed target_data.npz files or execute its raw-JSON fallback for the reported experiments?",
    "What are the contents and record identities of the referenced shadow JSON files and processed caches, and how do they map to the paper's evaluated target records?",
    "Does the paper's allowance for access to certain clean segments cover the test collections supplied to GCG.run?"
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 4. V5\.1 pilot · ASPI · aspi

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/aspi/aspi  
运行 / 判定：运行失败

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 运行失败 | \{"stage": "ingestion", "status": "failed", "error\_code": "document\_download\_timeout"\} |

#### 证据

```json
[]
```

#### 备注

```json
[
  "Earlier attempt retained; excluded from the paper denominator."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/aspi/aspi",
  "title": "V5.1 pilot · ASPI · aspi",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "aspi",
  "attempt_id": "aspi",
  "selected_final": false,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/aspi/result.json",
  "source": "https://arxiv.org/pdf/2605.17324v1",
  "status": "failed",
  "verdict": "technical_failure",
  "has_confirmed_inconsistency": null,
  "reason_code": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "failed",
      "error_code": "document_download_timeout"
    }
  ],
  "coverage_complete": null,
  "claim_result_counts": {},
  "document_sha256": null,
  "input_binding": null,
  "prompt_sha256": null,
  "request_hashes": {},
  "repository": {
    "url": null,
    "revision": null,
    "manifest_sha256": null,
    "coverage": {},
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 0,
      "unresolved": 0,
      "over_limit": 0
    },
    "evidence_expansion_counts": {
      "inspected_paths": 0
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": null,
    "reason_code": null,
    "repository_url": null
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 0,
    "calls": [],
    "usage": {
      "input_tokens": 0,
      "cached_input_tokens": 0,
      "output_tokens": 0,
      "reasoning_output_tokens": 0
    },
    "usage_reporting_complete": false,
    "actual_model_unknown_invocations": 0,
    "preflight_failure_count": 0
  },
  "duration_seconds": 41.456,
  "evidence": [],
  "unresolved_questions": [],
  "notes": [
    "Earlier attempt retained; excluded from the paper denominator."
  ],
  "error_code": "document_download_timeout",
  "error_type": "DocumentError"
}
```

### 5. V5\.1 pilot · ASPI · aspi\-download\-retry

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/aspi/aspi\-download\-retry  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 34, "characters": 149931, "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "manifest\_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8", "source\_segments": 32, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 32, "included\_files": 32, "omitted\_files": 0, "excluded\_entries": 6, "characters": 464472, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "fresh\_model\_call"\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 2, "remaining\_issues": 0, "classification\_fields\_modified": false\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_evaluated_instance_alignment_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_constructor",
      "attacker_delivery": "confirmed",
      "instance_requirement": "same_evaluated_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p3",
        "start": 3437,
        "end": 3489,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
        "source_kind": "paper",
        "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 2301,
        "end": 2353,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 73,
        "line_end": 73
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4414,
        "end": 4693,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 130,
        "line_end": 134
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 8085,
        "end": 8172,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 218,
        "line_end": 220
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 19573,
        "end": 19704,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 517,
        "line_end": 520
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 22601,
        "end": 22624,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 599,
        "line_end": 599
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 22823,
        "end": 22863,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 605,
        "line_end": 605
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 75906,
        "end": 76050,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 1908,
        "line_end": 1911
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 86651,
        "end": 86733,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 2166,
        "line_end": 2167
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 86062,
        "end": 86141,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 2153,
        "line_end": 2154
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 61494,
        "end": 61691,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 1542,
        "line_end": 1544
      },
      {
        "segment_id": "paper:p13",
        "start": 1046,
        "end": 1192,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "7c7bbacd40cf3714d9a74630309e65dbbb994e5d4aadb5bb4f61f37d3a9d7928",
        "source_kind": "paper",
        "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 16019,
        "end": 16277,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 429,
        "line_end": 436
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4156,
        "end": 4250,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 121,
        "line_end": 122
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 18075,
        "end": 18219,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 482,
        "line_end": 485
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 6149,
        "end": 6213,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 173,
        "line_end": 173
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4768,
        "end": 4835,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 138,
        "line_end": 138
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 3330,
        "end": 3518,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 99,
        "line_end": 103
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 5092,
        "end": 5142,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 132,
        "line_end": 132
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 4794,
        "end": 4858,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 125,
        "line_end": 125
      }
    ],
    "missing_obligations": [
      {
        "kind": "same_instance_mapping",
        "conditional_on_policy_scope": false
      }
    ]
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/aspi/aspi-download-retry",
  "title": "V5.1 pilot · ASPI · aspi-download-retry",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "aspi",
  "attempt_id": "aspi-download-retry",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/aspi-download-retry/result.json",
  "source": "https://arxiv.org/pdf/2605.17324v1",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 34,
      "characters": 149931,
      "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
      "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
      "source_segments": 32,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 32,
        "included_files": 32,
        "omitted_files": 0,
        "excluded_entries": 6,
        "characters": 464472,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "fresh_model_call"
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 2,
      "remaining_issues": 0,
      "classification_fields_modified": false
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1
  },
  "document_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
  "input_binding": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
    "model_content_sha256": "cfc1c420ce20761cb915d2936d79d26a7c54cc3b622bbc4f5f3dbefe4bcc6b94",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/scaleapi/aspi",
    "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
    "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 32,
      "included_files": 32,
      "omitted_files": 0,
      "excluded_entries": 6,
      "characters": 464472,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 350,
      "unresolved": 321,
      "over_limit": 0
    },
    "evidence_expansion_counts": {
      "added_files": 0,
      "added_bytes": 0,
      "inspected_paths": 32
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/scaleapi/aspi"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 3,
    "calls": [
      {
        "invocation": 1,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "db81d8bea89210f688a3e12e562584926e6ea746d33424001b49aa2fb388525c",
        "usage": {
          "input_tokens": 173833,
          "cached_input_tokens": 0,
          "output_tokens": 3398,
          "reasoning_output_tokens": 183
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "1f3ea8250018e2d671dd67440b034d690f683f5c67189c74fd1a3bd8876baf26",
        "usage": {
          "input_tokens": 16269,
          "cached_input_tokens": 0,
          "output_tokens": 91,
          "reasoning_output_tokens": 0
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 3,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "a6de94b8f35956ad83b7557790150c84183313210f1d1a1818f7fce5923cba5f",
        "usage": {
          "input_tokens": 175195,
          "cached_input_tokens": 0,
          "output_tokens": 375,
          "reasoning_output_tokens": 75
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 365297,
      "cached_input_tokens": 0,
      "output_tokens": 3864,
      "reasoning_output_tokens": 258
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 3,
    "preflight_failure_count": 0
  },
  "duration_seconds": 121.299,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_evaluated_instance_alignment_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_constructor",
        "attacker_delivery": "confirmed",
        "instance_requirement": "same_evaluated_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p3",
          "start": 3437,
          "end": 3489,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
          "source_kind": "paper",
          "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 2301,
          "end": 2353,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 73,
          "line_end": 73
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4414,
          "end": 4693,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 130,
          "line_end": 134
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 8085,
          "end": 8172,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 218,
          "line_end": 220
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 19573,
          "end": 19704,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 517,
          "line_end": 520
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 22601,
          "end": 22624,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 599,
          "line_end": 599
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 22823,
          "end": 22863,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 605,
          "line_end": 605
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 75906,
          "end": 76050,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 1908,
          "line_end": 1911
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 86651,
          "end": 86733,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 2166,
          "line_end": 2167
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 86062,
          "end": 86141,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 2153,
          "line_end": 2154
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 61494,
          "end": 61691,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 1542,
          "line_end": 1544
        },
        {
          "segment_id": "paper:p13",
          "start": 1046,
          "end": 1192,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "7c7bbacd40cf3714d9a74630309e65dbbb994e5d4aadb5bb4f61f37d3a9d7928",
          "source_kind": "paper",
          "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 16019,
          "end": 16277,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 429,
          "line_end": 436
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4156,
          "end": 4250,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 121,
          "line_end": 122
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 18075,
          "end": 18219,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 482,
          "line_end": 485
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 6149,
          "end": 6213,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 173,
          "line_end": 173
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4768,
          "end": 4835,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 138,
          "line_end": 138
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 3330,
          "end": 3518,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 99,
          "line_end": 103
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 5092,
          "end": 5142,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 132,
          "line_end": 132
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 4794,
          "end": 4858,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 125,
          "line_end": 125
        }
      ],
      "missing_obligations": [
        {
          "kind": "same_instance_mapping",
          "conditional_on_policy_scope": false
        }
      ]
    }
  ],
  "unresolved_questions": [
    "Which generated JSONL paths and --grouped/--dataset configuration were selected for the paper's historical runs?",
    "The benign simulator explicitly receives original_prompt under paper Appendix C; that permitted simulator channel does not resolve the separate constructor access above.",
    "generate_injected_response can receive the full original task, but the supplied evaluator calls generate_benign_response and uses pre-generated clarif_user variants. What actual caller, if any, binds the injected simulator method during evaluated attack construction?"
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 6. V5\.1 pilot · MUZZLE · muzzle

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/muzzle/muzzle  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 21, "characters": 124184, "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "manifest\_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a", "source\_segments": 106, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 106, "included\_files": 106, "omitted\_files": 0, "excluded\_entries": 129, "characters": 445602, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 2, "execution": "fresh\_model\_call"\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 2, "remaining\_issues": 0, "classification\_fields\_modified": false\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "any_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14614,
        "end": 14680,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 325,
        "line_end": 325
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 33522,
        "end": 33766,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 792,
        "line_end": 796
      },
      {
        "segment_id": "paper:p6",
        "start": 3168,
        "end": 3232,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 34319,
        "end": 34434,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 809,
        "line_end": 811
      }
    ],
    "missing_obligations": []
  },
  {
    "id": "uploaded_paper_claim_2",
    "verdict": "consistent_within_scope",
    "reason": "bound_claim_refuted_explicit_permission",
    "claim_result": "refuted",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "any_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14614,
        "end": 14680,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 325,
        "line_end": 325
      },
      {
        "segment_id": "paper:p5",
        "start": 111,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "paper:p8",
        "start": 3520,
        "end": 3573,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14079,
        "end": 14127,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 314,
        "line_end": 314
      },
      {
        "segment_id": "paper:p6",
        "start": 1687,
        "end": 1793,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
        "start": 5923,
        "end": 5986,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "source_kind": "code",
        "path": "muzzle/prototype/utils/network/vllm_proxy.py",
        "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 159,
        "line_end": 159
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 32952,
        "end": 32999,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 781,
        "line_end": 781
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 34319,
        "end": 34434,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 809,
        "line_end": 811
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/muzzle/muzzle",
  "title": "V5.1 pilot · MUZZLE · muzzle",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "muzzle",
  "attempt_id": "muzzle",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/muzzle/result.json",
  "source": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 21,
      "characters": 124184,
      "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
      "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
      "source_segments": 106,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 106,
        "included_files": 106,
        "omitted_files": 0,
        "excluded_entries": 129,
        "characters": 445602,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 2,
      "execution": "fresh_model_call"
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 2,
      "remaining_issues": 0,
      "classification_fields_modified": false
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1,
    "refuted": 1
  },
  "document_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
  "input_binding": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
    "model_content_sha256": "13c27ad40acdb19ffd648d55b11f85cb542946d1bcfa3522efafd456a025f83d",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/gsiros/muzzle",
    "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
    "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 106,
      "included_files": 106,
      "omitted_files": 0,
      "excluded_entries": 129,
      "characters": 445602,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 1,
    "dependency_reference_counts": {
      "needed": 1025,
      "unresolved": 817,
      "over_limit": 1
    },
    "evidence_expansion_counts": {
      "added_files": 25,
      "added_bytes": 21498,
      "inspected_paths": 88
    },
    "dependencies": [
      {
        "mount_path": "modules/JailbreakingLLMs",
        "url": "https://github.com/gsiros/ag-pair",
        "revision": "16518e2dacc3da823a39ec3bc28d692bacaf17b6",
        "coverage": {
          "complete": false,
          "inventory_complete": true,
          "eligible_files": 37,
          "included_files": 36,
          "omitted_files": 1,
          "excluded_entries": 30,
          "characters": 143726,
          "max_characters": 150000
        }
      }
    ]
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/gsiros/muzzle"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 3,
    "calls": [
      {
        "invocation": 1,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "c8a13ff028ccff2f7ea7cf68feaee1e885a4f4021e64c668dcfd280bd0b5bc97",
        "usage": {
          "input_tokens": 199378,
          "cached_input_tokens": 0,
          "output_tokens": 3258,
          "reasoning_output_tokens": 171
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "3dce254fdf5c8d9152ea57aceb96ff9283e3e5f0768141020436bbdd805b58e2",
        "usage": {
          "input_tokens": 16434,
          "cached_input_tokens": 0,
          "output_tokens": 107,
          "reasoning_output_tokens": 0
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 3,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "246daed37ac36834d5261c2f8a843a26fc7302f984f62eadb0d5c8c1974e9213",
        "usage": {
          "input_tokens": 200631,
          "cached_input_tokens": 0,
          "output_tokens": 659,
          "reasoning_output_tokens": 49
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 416443,
      "cached_input_tokens": 0,
      "output_tokens": 4024,
      "reasoning_output_tokens": 220
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 3,
    "preflight_failure_count": 0
  },
  "duration_seconds": 179.448,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "any_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14614,
          "end": 14680,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 325,
          "line_end": 325
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 33522,
          "end": 33766,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 792,
          "line_end": 796
        },
        {
          "segment_id": "paper:p6",
          "start": 3168,
          "end": 3232,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 34319,
          "end": 34434,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 809,
          "line_end": 811
        }
      ],
      "missing_obligations": []
    },
    {
      "id": "uploaded_paper_claim_2",
      "verdict": "consistent_within_scope",
      "reason": "bound_claim_refuted_explicit_permission",
      "claim_result": "refuted",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "any_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14614,
          "end": 14680,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 325,
          "line_end": 325
        },
        {
          "segment_id": "paper:p5",
          "start": 111,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "paper:p8",
          "start": 3520,
          "end": 3573,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14079,
          "end": 14127,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 314,
          "line_end": 314
        },
        {
          "segment_id": "paper:p6",
          "start": 1687,
          "end": 1793,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
          "start": 5923,
          "end": 5986,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "source_kind": "code",
          "path": "muzzle/prototype/utils/network/vllm_proxy.py",
          "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 159,
          "line_end": 159
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 32952,
          "end": 32999,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 781,
          "line_end": 781
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 34319,
          "end": 34434,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 809,
          "line_end": 811
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Does the operator-provided task instruction contain information absent from the victim's recorded LLM I/O? The concrete task specification and corresponding transcript contents are not supplied.",
    "Which concrete --spec path, environment configuration and run records correspond to the reported experiments?",
    "Does the deployed import environment resolve prototype.agents.summarizer to the supplied muzzle/prototype/agents/summarizer.py implementation?"
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 7. V5\.1 pilot · ObliInjection · obliinjection

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/obliinjection/obliinjection  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 18, "characters": 136067, "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "coverage": \{"complete": true\}\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit"\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "manifest\_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b", "source\_segments": 31, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 31, "included\_files": 31, "omitted\_files": 0, "excluded\_entries": 7, "characters": 147332, "max\_characters": 500000\}\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "fresh\_model\_call"\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 1, "remaining\_issues": 1, "classification\_fields\_modified": false\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "uploaded_paper_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "same_evaluated_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p4",
        "start": 1836,
        "end": 1931,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
        "source_kind": "paper",
        "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 3759,
        "end": 3924,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 75,
        "line_end": 78
      },
      {
        "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
        "start": 760,
        "end": 785,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "source_kind": "code",
        "path": "configs/task_configs/hotpotqa_config.json",
        "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 16,
        "line_end": 16
      },
      {
        "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
        "start": 951,
        "end": 1111,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "source_kind": "code",
        "path": "configs/task_configs/hotpotqa_config.json",
        "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 24,
        "line_end": 26
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 11966,
        "end": 12129,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 254,
        "line_end": 255
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 4762,
        "end": 4809,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 101,
        "line_end": 101
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2736,
        "end": 2793,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 69,
        "line_end": 69
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 967,
        "end": 1099,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 33,
        "line_end": 33
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 2155,
        "end": 2284,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 47,
        "line_end": 47
      },
      {
        "segment_id": "paper:p4",
        "start": 881,
        "end": 973,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
        "source_kind": "paper",
        "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 14538,
        "end": 14682,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 292,
        "line_end": 296
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 4244,
        "end": 4385,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 93,
        "line_end": 95
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 5568,
        "end": 5717,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 113,
        "line_end": 116
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2417,
        "end": 2467,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 61,
        "line_end": 61
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 1254,
        "end": 1337,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 36,
        "line_end": 36
      }
    ],
    "missing_obligations": [
      {
        "kind": "same_instance_mapping",
        "conditional_on_policy_scope": false
      }
    ]
  }
]
```

#### 备注

```json
[
  "Selected final paper result."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/obliinjection/obliinjection",
  "title": "V5.1 pilot · ObliInjection · obliinjection",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "obliinjection",
  "attempt_id": "obliinjection",
  "selected_final": true,
  "cohort_type": "fresh_model_audit",
  "source_result_path": "audits/obliinjection/result.json",
  "source": "https://arxiv.org/pdf/2512.09321v3",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 18,
      "characters": 136067,
      "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
      "coverage": {
        "complete": true
      }
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit"
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
      "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
      "source_segments": 31,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 31,
        "included_files": 31,
        "omitted_files": 0,
        "excluded_entries": 7,
        "characters": 147332,
        "max_characters": 500000
      }
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "fresh_model_call"
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 1,
      "remaining_issues": 1,
      "classification_fields_modified": false
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope"
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks"
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1
  },
  "document_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
  "input_binding": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
    "model_content_sha256": "0ffc8c4b2c6fafd93665bae0fa051a7f76db6c3fc399ea6ea9eec66180ae4114",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/ReachalWang/ObliInjection",
    "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
    "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 31,
      "included_files": 31,
      "omitted_files": 0,
      "excluded_entries": 7,
      "characters": 147332,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 225,
      "unresolved": 176,
      "over_limit": 9
    },
    "evidence_expansion_counts": {
      "added_files": 12,
      "added_bytes": 7062,
      "inspected_paths": 31
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/ReachalWang/ObliInjection"
  },
  "inference": {
    "provider": "codex",
    "requested_model": "gpt-6.1-sol",
    "max_calls": 3,
    "invocation_count": 3,
    "calls": [
      {
        "invocation": 1,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "8431247647d725c99e9b53c9ce3f78892655f8bf5d3e2b93f1cf31089feead9d",
        "usage": {
          "input_tokens": 80793,
          "cached_input_tokens": 0,
          "output_tokens": 3520,
          "reasoning_output_tokens": 273
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 2,
        "stage": "citation_repair",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "4654e798d2aea16d95abd13847ee73d7d9575875c2497b9350745bf581f9ffd4",
        "usage": {
          "input_tokens": 16694,
          "cached_input_tokens": 0,
          "output_tokens": 138,
          "reasoning_output_tokens": 45
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      },
      {
        "invocation": 3,
        "stage": "semantic_review",
        "status": "completed",
        "requested_model": "gpt-6.1-sol",
        "actual_model": null,
        "actual_models": [],
        "request_sha256": "bc1afc4a0368855173a41c81e0fdd0e1bdf7cbe352842d0f854c519e9b607b94",
        "usage": {
          "input_tokens": 82204,
          "cached_input_tokens": 0,
          "output_tokens": 396,
          "reasoning_output_tokens": 39
        },
        "execution": {
          "returncode": 0,
          "turn_completed": true,
          "fatal_error_count": 0,
          "error_notification_count": 0
        }
      }
    ],
    "usage": {
      "input_tokens": 179691,
      "cached_input_tokens": 0,
      "output_tokens": 4054,
      "reasoning_output_tokens": 357
    },
    "usage_reporting_complete": true,
    "actual_model_unknown_invocations": 3,
    "preflight_failure_count": 0
  },
  "duration_seconds": 133.687,
  "evidence": [
    {
      "id": "uploaded_paper_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "same_evaluated_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p4",
          "start": 1836,
          "end": 1931,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
          "source_kind": "paper",
          "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 3759,
          "end": 3924,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 75,
          "line_end": 78
        },
        {
          "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
          "start": 760,
          "end": 785,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "source_kind": "code",
          "path": "configs/task_configs/hotpotqa_config.json",
          "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 16,
          "line_end": 16
        },
        {
          "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
          "start": 951,
          "end": 1111,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "source_kind": "code",
          "path": "configs/task_configs/hotpotqa_config.json",
          "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 24,
          "line_end": 26
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 11966,
          "end": 12129,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 254,
          "line_end": 255
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 4762,
          "end": 4809,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 101,
          "line_end": 101
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2736,
          "end": 2793,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 69,
          "line_end": 69
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 967,
          "end": 1099,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 33,
          "line_end": 33
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 2155,
          "end": 2284,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 47,
          "line_end": 47
        },
        {
          "segment_id": "paper:p4",
          "start": 881,
          "end": 973,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
          "source_kind": "paper",
          "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 14538,
          "end": 14682,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 292,
          "line_end": 296
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 4244,
          "end": 4385,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 93,
          "line_end": 95
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 5568,
          "end": 5717,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 113,
          "line_end": 116
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2417,
          "end": 2467,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 61,
          "line_end": 61
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 1254,
          "end": 1337,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 36,
          "line_end": 36
        }
      ],
      "missing_obligations": [
        {
          "kind": "same_instance_mapping",
          "conditional_on_policy_scope": false
        }
      ]
    }
  ],
  "unresolved_questions": [
    "What are the contents and provenance of data/hotpotqa/hotpotqa_shadow.json? The supplied source cannot determine whether its sources are synthetic shadows, real target segments, or a mixture.",
    "Did a particular run load processed ./data/hotpotqa/train/source_num_3/target_data.npz and ./data/hotpotqa/test/source_num_10/target_data.npz, or enter raw fallback? Cache contents and their record mappings are unavailable; the conditional identity result does not cover arbitrary existing caches.",
    "The separate HotpotQA question channel remains relevant: __get_hotpotqa reads train_data[i]['question'], and obliinjection.py supplies target_train_question to gcg.run. Are these generated shadow questions or the actual evaluated questions, and how does the paper's specific-target-instruction restriction cover them?",
    "Does access to the configured source lists fall within the paper's allowance for certain clean segments, or supply the complete genuine target context? Missing data prevents resolving that scope."
  ],
  "notes": [
    "Selected final paper result."
  ]
}
```

### 8. V5\.1 pilot · deterministic revalidation · ASPI

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/aspi  
运行 / 判定：有已确认的不一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 34, "characters": 149931, "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893", "coverage": \{"complete": true\}, "inherited\_from\_source\_attempt": true\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit", "inherited\_from\_source\_attempt": true\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "manifest\_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8", "source\_segments": 32, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 32, "included\_files": 32, "omitted\_files": 0, "excluded\_entries": 6, "characters": 464472, "max\_characters": 500000\}, "inherited\_from\_source\_attempt": true\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "reused\_prior\_model\_result", "inherited\_from\_source\_attempt": true\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 2, "remaining\_issues": 0, "classification\_fields\_modified": false, "inherited\_from\_source\_attempt": true\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope", "inherited\_from\_source\_attempt": true\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks", "inherited\_from\_source\_attempt": true\} |
| deterministic\_revalidation | 已完成 | \{"stage": "deterministic\_revalidation", "status": "completed", "previous\_verdict": "insufficient\_evidence", "verdict": "inconsistent", "model\_calls": 0, "evidence\_edited": false\} |

#### 证据

```json
[
  {
    "id": "aspi_claim_1",
    "verdict": "inconsistent",
    "reason": "bound_scoped_forbidden_delivery_confirmed",
    "claim_result": "confirmed",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_constructor",
      "attacker_delivery": "confirmed",
      "instance_requirement": "same_evaluated_instance",
      "instance_relation": "same",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": true,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": true,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p3",
        "start": 3437,
        "end": 3489,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
        "source_kind": "paper",
        "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 2301,
        "end": 2353,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 73,
        "line_end": 73
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4414,
        "end": 4693,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 130,
        "line_end": 134
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 8085,
        "end": 8172,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 218,
        "line_end": 220
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 19573,
        "end": 19704,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 517,
        "line_end": 520
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 22601,
        "end": 22624,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 599,
        "line_end": 599
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 22823,
        "end": 22863,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 605,
        "line_end": 605
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 75906,
        "end": 76050,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 1908,
        "line_end": 1911
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 86651,
        "end": 86733,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 2166,
        "line_end": 2167
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 86062,
        "end": 86141,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 2153,
        "line_end": 2154
      },
      {
        "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
        "start": 61494,
        "end": 61691,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "source_kind": "code",
        "path": "src/aspi/eval/runner.py",
        "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 1542,
        "line_end": 1544
      },
      {
        "segment_id": "paper:p13",
        "start": 1046,
        "end": 1192,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "7c7bbacd40cf3714d9a74630309e65dbbb994e5d4aadb5bb4f61f37d3a9d7928",
        "source_kind": "paper",
        "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 16019,
        "end": 16277,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 429,
        "line_end": 436
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4156,
        "end": 4250,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 121,
        "line_end": 122
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 18075,
        "end": 18219,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 482,
        "line_end": 485
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 6149,
        "end": 6213,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 173,
        "line_end": 173
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 4768,
        "end": 4835,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 138,
        "line_end": 138
      },
      {
        "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
        "start": 3330,
        "end": 3518,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "source_kind": "code",
        "path": "src/aspi/dataset/pipeline.py",
        "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 99,
        "line_end": 103
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 5092,
        "end": 5142,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 132,
        "line_end": 132
      },
      {
        "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
        "start": 4794,
        "end": 4858,
        "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "source_kind": "code",
        "path": "src/aspi/common/litellm.py",
        "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
        "repository_source": "https://github.com/scaleapi/aspi",
        "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
        "line_start": 125,
        "line_end": 125
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/deterministic_revalidation/aspi",
  "title": "V5.1 pilot · deterministic revalidation · ASPI",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "aspi",
  "attempt_id": "deterministic_revalidation/aspi",
  "selected_final": false,
  "cohort_type": "deterministic_revalidation",
  "source_result_path": "revalidated/aspi/result.json",
  "source": "https://arxiv.org/pdf/2605.17324v1",
  "status": "completed",
  "verdict": "inconsistent",
  "has_confirmed_inconsistency": true,
  "reason_code": "confirmed_inconsistency_in_scope",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 34,
      "characters": 149931,
      "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
      "coverage": {
        "complete": true
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
      "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
      "source_segments": 32,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 32,
        "included_files": 32,
        "omitted_files": 0,
        "excluded_entries": 6,
        "characters": 464472,
        "max_characters": 500000
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "reused_prior_model_result",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 2,
      "remaining_issues": 0,
      "classification_fields_modified": false,
      "inherited_from_source_attempt": true
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "deterministic_revalidation",
      "status": "completed",
      "previous_verdict": "insufficient_evidence",
      "verdict": "inconsistent",
      "model_calls": 0,
      "evidence_edited": false
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "confirmed": 1
  },
  "document_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
  "input_binding": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
    "model_content_sha256": "cfc1c420ce20761cb915d2936d79d26a7c54cc3b622bbc4f5f3dbefe4bcc6b94",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/scaleapi/aspi",
    "revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
    "manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 32,
      "included_files": 32,
      "omitted_files": 0,
      "excluded_entries": 6,
      "characters": 464472,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 350,
      "unresolved": 321,
      "over_limit": 0
    },
    "evidence_expansion_counts": {
      "added_files": 0,
      "added_bytes": 0,
      "inspected_paths": 32
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/scaleapi/aspi"
  },
  "inference": {
    "invocation_count": 0,
    "calls": [],
    "usage": {
      "input_tokens": 0,
      "cached_input_tokens": 0,
      "output_tokens": 0,
      "reasoning_output_tokens": 0
    },
    "usage_reporting_complete": true,
    "execution": "deterministic_revalidation_no_model_call"
  },
  "duration_seconds": 121.299,
  "evidence": [
    {
      "id": "aspi_claim_1",
      "verdict": "inconsistent",
      "reason": "bound_scoped_forbidden_delivery_confirmed",
      "claim_result": "confirmed",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_constructor",
        "attacker_delivery": "confirmed",
        "instance_requirement": "same_evaluated_instance",
        "instance_relation": "same",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": true,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": true,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p3",
          "start": 3437,
          "end": 3489,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "990c019be9fcc7d8ea9ba571bda1a612096691b369976ac845ee928d8228d275",
          "source_kind": "paper",
          "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 2301,
          "end": 2353,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 73,
          "line_end": 73
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4414,
          "end": 4693,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 130,
          "line_end": 134
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 8085,
          "end": 8172,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 218,
          "line_end": 220
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 19573,
          "end": 19704,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 517,
          "line_end": 520
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 22601,
          "end": 22624,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 599,
          "line_end": 599
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 22823,
          "end": 22863,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 605,
          "line_end": 605
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 75906,
          "end": 76050,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 1908,
          "line_end": 1911
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 86651,
          "end": 86733,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 2166,
          "line_end": 2167
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 86062,
          "end": 86141,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 2153,
          "line_end": 2154
        },
        {
          "segment_id": "repo:src/aspi/eval/runner.py:L1-L2317",
          "start": 61494,
          "end": 61691,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "source_kind": "code",
          "path": "src/aspi/eval/runner.py",
          "file_sha256": "2af5bd9333578ae6634cbbe568149927b6f42b271beddc5fcbea3cdb08b1ae55",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 1542,
          "line_end": 1544
        },
        {
          "segment_id": "paper:p13",
          "start": 1046,
          "end": 1192,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "7c7bbacd40cf3714d9a74630309e65dbbb994e5d4aadb5bb4f61f37d3a9d7928",
          "source_kind": "paper",
          "paper_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 16019,
          "end": 16277,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 429,
          "line_end": 436
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4156,
          "end": 4250,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 121,
          "line_end": 122
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 18075,
          "end": 18219,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 482,
          "line_end": 485
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 6149,
          "end": 6213,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 173,
          "line_end": 173
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 4768,
          "end": 4835,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 138,
          "line_end": 138
        },
        {
          "segment_id": "repo:src/aspi/dataset/pipeline.py:L1-L809",
          "start": 3330,
          "end": 3518,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "source_kind": "code",
          "path": "src/aspi/dataset/pipeline.py",
          "file_sha256": "3e913be19d9fb33c876fe500130e893516d7b06fba5fc089cbc7d36d8503ddbd",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 99,
          "line_end": 103
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 5092,
          "end": 5142,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 132,
          "line_end": 132
        },
        {
          "segment_id": "repo:src/aspi/common/litellm.py:L1-L151",
          "start": 4794,
          "end": 4858,
          "document_sha256": "4bf2584e38897f9ac0ba8f52e6e3d8cc1e5e2e8522100a4cb924ce5b1e629a49",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "source_kind": "code",
          "path": "src/aspi/common/litellm.py",
          "file_sha256": "057fa8ef273d282ff14dfa6f2fe3e6cee6d03e64f2456101d9bf658b13bd0c9c",
          "repository_source": "https://github.com/scaleapi/aspi",
          "repository_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
          "repository_manifest_sha256": "b76db0af8b8d143e13942f3a2c77d9e542862e7858f50bde485f2470ada9e7b8",
          "line_start": 125,
          "line_end": 125
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Which generated JSONL paths and --grouped/--dataset configuration were selected for the paper's historical runs?",
    "The benign simulator explicitly receives original_prompt under paper Appendix C; that permitted simulator channel does not resolve the separate constructor access above.",
    "generate_injected_response can receive the full original task, but the supplied evaluator calls generate_benign_response and uses pre-generated clarif_user variants. What actual caller, if any, binds the injected simulator method during evaluated attack construction?"
  ],
  "notes": [
    "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
  ],
  "reused_inference_from": "2026-11-21-v5-1-pilot-020638/aspi/aspi-download-retry",
  "revalidation": {
    "code_commit": "dcc3f28db50e99571393cee2763c4d88a2e458bf",
    "code_files_sha256": {
      "extraction_v5.py": "e6cb06f2cec52922b5756fb586801beefd7df68964d7e84268decf98ca47a1ac",
      "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
      "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
      "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
      "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
      "call_boundaries.py": "939b8812406d0b0d038d72d3755a2514a977fbb97cdb7558d66ebea8794aa5cf",
      "findings.py": "d5ff5e03081911982c6ee45011055e9e037918ef5ac8e02053980fbca552fcdd"
    },
    "reference_artifacts_sha256": {
      "result.json": "a52d6f3eb24c30b94f297268ed1a4ef0071dff6d1305203dca32c00721410b0c",
      "extraction.repaired.json": "56c79b84f52b655e7b5056cd223e14cb3903513307074ad744a7ebc4c690eb27",
      "review.json": "dda80cdec69422efec1aabea6c5c134083a38acbd92613dd9ee7bc068fd903de",
      "combined_input.json": "e9041aec152848603d150b035b37e58513be05b1585fc134852c856a4976196d",
      "request.json": "164fcddce86743c0321b0eca9055e5adcb150efc9880fdf8fba469e736f52ab0"
    },
    "original_verdict": "insufficient_evidence",
    "model_calls": 0,
    "evidence_edited": false
  }
}
```

### 9. V5\.1 pilot · deterministic revalidation · MUZZLE

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/muzzle  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 21, "characters": 124184, "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0", "coverage": \{"complete": true\}, "inherited\_from\_source\_attempt": true\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit", "inherited\_from\_source\_attempt": true\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038", "manifest\_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a", "source\_segments": 106, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 106, "included\_files": 106, "omitted\_files": 0, "excluded\_entries": 129, "characters": 445602, "max\_characters": 500000\}, "inherited\_from\_source\_attempt": true\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 2, "execution": "reused\_prior\_model\_result", "inherited\_from\_source\_attempt": true\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 2, "remaining\_issues": 0, "classification\_fields\_modified": false, "inherited\_from\_source\_attempt": true\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope", "inherited\_from\_source\_attempt": true\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks", "inherited\_from\_source\_attempt": true\} |
| deterministic\_revalidation | 已完成 | \{"stage": "deterministic\_revalidation", "status": "completed", "previous\_verdict": "insufficient\_evidence", "verdict": "insufficient\_evidence", "model\_calls": 0, "evidence\_edited": false\} |

#### 证据

```json
[
  {
    "id": "muzzle_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "any_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14614,
        "end": 14680,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 325,
        "line_end": 325
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 33522,
        "end": 33766,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 792,
        "line_end": 796
      },
      {
        "segment_id": "paper:p6",
        "start": 3168,
        "end": 3232,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 34319,
        "end": 34434,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 809,
        "line_end": 811
      }
    ],
    "missing_obligations": []
  },
  {
    "id": "muzzle_claim_2",
    "verdict": "consistent_within_scope",
    "reason": "bound_claim_refuted_explicit_permission",
    "claim_result": "refuted",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "any_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": []
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p5",
        "start": 78,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14614,
        "end": 14680,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 325,
        "line_end": 325
      },
      {
        "segment_id": "paper:p5",
        "start": 111,
        "end": 179,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "paper:p8",
        "start": 3520,
        "end": 3573,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
        "start": 14079,
        "end": 14127,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/pair.py",
        "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 314,
        "line_end": 314
      },
      {
        "segment_id": "paper:p6",
        "start": 1687,
        "end": 1793,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
        "source_kind": "paper",
        "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
      },
      {
        "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
        "start": 5923,
        "end": 5986,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "source_kind": "code",
        "path": "muzzle/prototype/utils/network/vllm_proxy.py",
        "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 159,
        "line_end": 159
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 32952,
        "end": 32999,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 781,
        "line_end": 781
      },
      {
        "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
        "start": 34319,
        "end": 34434,
        "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "source_kind": "code",
        "path": "muzzle/prototype/agents/explorer.py",
        "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
        "repository_source": "https://github.com/gsiros/muzzle",
        "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
        "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
        "line_start": 809,
        "line_end": 811
      }
    ],
    "missing_obligations": []
  }
]
```

#### 备注

```json
[
  "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/deterministic_revalidation/muzzle",
  "title": "V5.1 pilot · deterministic revalidation · MUZZLE",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "muzzle",
  "attempt_id": "deterministic_revalidation/muzzle",
  "selected_final": false,
  "cohort_type": "deterministic_revalidation",
  "source_result_path": "revalidated/muzzle/result.json",
  "source": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 21,
      "characters": 124184,
      "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
      "coverage": {
        "complete": true
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
      "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
      "source_segments": 106,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 106,
        "included_files": 106,
        "omitted_files": 0,
        "excluded_entries": 129,
        "characters": 445602,
        "max_characters": 500000
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 2,
      "execution": "reused_prior_model_result",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 2,
      "remaining_issues": 0,
      "classification_fields_modified": false,
      "inherited_from_source_attempt": true
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "deterministic_revalidation",
      "status": "completed",
      "previous_verdict": "insufficient_evidence",
      "verdict": "insufficient_evidence",
      "model_calls": 0,
      "evidence_edited": false
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1,
    "refuted": 1
  },
  "document_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
  "input_binding": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
    "model_content_sha256": "13c27ad40acdb19ffd648d55b11f85cb542946d1bcfa3522efafd456a025f83d",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/gsiros/muzzle",
    "revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
    "manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 106,
      "included_files": 106,
      "omitted_files": 0,
      "excluded_entries": 129,
      "characters": 445602,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 1,
    "dependency_reference_counts": {
      "needed": 1025,
      "unresolved": 817,
      "over_limit": 1
    },
    "evidence_expansion_counts": {
      "added_files": 25,
      "added_bytes": 21498,
      "inspected_paths": 88
    },
    "dependencies": [
      {
        "mount_path": "modules/JailbreakingLLMs",
        "url": "https://github.com/gsiros/ag-pair",
        "revision": "16518e2dacc3da823a39ec3bc28d692bacaf17b6",
        "coverage": {
          "complete": false,
          "inventory_complete": true,
          "eligible_files": 37,
          "included_files": 36,
          "omitted_files": 1,
          "excluded_entries": 30,
          "characters": 143726,
          "max_characters": 150000
        }
      }
    ]
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/gsiros/muzzle"
  },
  "inference": {
    "invocation_count": 0,
    "calls": [],
    "usage": {
      "input_tokens": 0,
      "cached_input_tokens": 0,
      "output_tokens": 0,
      "reasoning_output_tokens": 0
    },
    "usage_reporting_complete": true,
    "execution": "deterministic_revalidation_no_model_call"
  },
  "duration_seconds": 179.448,
  "evidence": [
    {
      "id": "muzzle_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "any_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14614,
          "end": 14680,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 325,
          "line_end": 325
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 33522,
          "end": 33766,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 792,
          "line_end": 796
        },
        {
          "segment_id": "paper:p6",
          "start": 3168,
          "end": 3232,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 34319,
          "end": 34434,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 809,
          "line_end": 811
        }
      ],
      "missing_obligations": []
    },
    {
      "id": "muzzle_claim_2",
      "verdict": "consistent_within_scope",
      "reason": "bound_claim_refuted_explicit_permission",
      "claim_result": "refuted",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "any_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": []
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p5",
          "start": 78,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14614,
          "end": 14680,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 325,
          "line_end": 325
        },
        {
          "segment_id": "paper:p5",
          "start": 111,
          "end": 179,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "9e85ba997315a4ed9c3e45e75cfa4eedeff10bdab43a926f5bca3ebbfa32789d",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "paper:p8",
          "start": 3520,
          "end": 3573,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2a076136af292214a2d9f53d8b47c2ff136dd0d645dda53bcf5cf5883f2e042b",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/pair.py:L1-L399",
          "start": 14079,
          "end": 14127,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/pair.py",
          "file_sha256": "d34697a2d00a3ebe806aea12491071a5b9b609eda1ded0d781f6ff7d5780a993",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 314,
          "line_end": 314
        },
        {
          "segment_id": "paper:p6",
          "start": 1687,
          "end": 1793,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "ad43fe0220c23781870630a636e892b4a277f379041d024b789e783249486729",
          "source_kind": "paper",
          "paper_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
        },
        {
          "segment_id": "repo:muzzle/prototype/utils/network/vllm_proxy.py:L1-L276",
          "start": 5923,
          "end": 5986,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "source_kind": "code",
          "path": "muzzle/prototype/utils/network/vllm_proxy.py",
          "file_sha256": "6a8d9de2070303bdb11f01daef7bd333ae16788975c5054f5d64854b0e257331",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 159,
          "line_end": 159
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 32952,
          "end": 32999,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 781,
          "line_end": 781
        },
        {
          "segment_id": "repo:muzzle/prototype/agents/explorer.py:L1-L973",
          "start": 34319,
          "end": 34434,
          "document_sha256": "d92de9120105ff603059a7791cc18e66d983f6f2bdd6fb2ba670c8599c65ab6a",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "source_kind": "code",
          "path": "muzzle/prototype/agents/explorer.py",
          "file_sha256": "4c9acd02b0c07150d30d7061c4596646bd72ef4e4eefee0472bca38436572ae4",
          "repository_source": "https://github.com/gsiros/muzzle",
          "repository_revision": "9f3effa1668fa29dcba8f2454e711ddf9ef3c038",
          "repository_manifest_sha256": "823dac591b659a547975459e2db577c867d8ea3937637f1fde1dfd857c39099a",
          "line_start": 809,
          "line_end": 811
        }
      ],
      "missing_obligations": []
    }
  ],
  "unresolved_questions": [
    "Does the operator-provided task instruction contain information absent from the victim's recorded LLM I/O? The concrete task specification and corresponding transcript contents are not supplied.",
    "Which concrete --spec path, environment configuration and run records correspond to the reported experiments?",
    "Does the deployed import environment resolve prototype.agents.summarizer to the supplied muzzle/prototype/agents/summarizer.py implementation?"
  ],
  "notes": [
    "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
  ],
  "reused_inference_from": "2026-11-21-v5-1-pilot-020638/muzzle/muzzle",
  "revalidation": {
    "code_commit": "dcc3f28db50e99571393cee2763c4d88a2e458bf",
    "code_files_sha256": {
      "extraction_v5.py": "e6cb06f2cec52922b5756fb586801beefd7df68964d7e84268decf98ca47a1ac",
      "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
      "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
      "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
      "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
      "call_boundaries.py": "939b8812406d0b0d038d72d3755a2514a977fbb97cdb7558d66ebea8794aa5cf",
      "findings.py": "d5ff5e03081911982c6ee45011055e9e037918ef5ac8e02053980fbca552fcdd"
    },
    "reference_artifacts_sha256": {
      "result.json": "46c96a9a93a46fc7321743ef0c9d4ccd89286834983a695d03fcb1654f45712f",
      "extraction.repaired.json": "145d1eed061d9d3748dbc7fc1534cdb5ef0322288b5147541954bc8da6aa724a",
      "review.json": "8de6897e8835d0be0d2b955ff2ad23a1f28e20b0549998e479ef9bc350b98daf",
      "combined_input.json": "adc3d222a7a365b4019aca118e2a66464dec1718d87b267a915bddb3749615ba",
      "request.json": "6c87170983500f0d6e34c118600011e843b9e66dbe75ba1d476f69ba2d66ac09"
    },
    "original_verdict": "insufficient_evidence",
    "model_calls": 0,
    "evidence_edited": false
  }
}
```

### 10. V5\.1 pilot · deterministic revalidation · ObliInjection

论文 ID：2026\-11\-21\-v5\-1\-pilot\-020638/deterministic\_revalidation/obliinjection  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 18, "characters": 136067, "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e", "coverage": \{"complete": true\}, "inherited\_from\_source\_attempt": true\} |
| source\_discovery | 已完成 | \{"stage": "source\_discovery", "status": "completed", "discovery\_status": "selected", "reason\_code": "unique\_self\_associated\_code\_link\_resolved\_to\_full\_commit", "inherited\_from\_source\_attempt": true\} |
| repository\_ingestion | 已完成 | \{"stage": "repository\_ingestion", "status": "completed", "revision": "b1f6a3f48c0cf121534374cbcef453832594867b", "manifest\_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b", "source\_segments": 31, "coverage": \{"complete": true, "inventory\_complete": true, "eligible\_files": 31, "included\_files": 31, "omitted\_files": 0, "excluded\_entries": 7, "characters": 147332, "max\_characters": 500000\}, "inherited\_from\_source\_attempt": true\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 1, "execution": "reused\_prior\_model\_result", "inherited\_from\_source\_attempt": true\} |
| citation\_repair | 已完成 | \{"stage": "citation\_repair", "status": "completed", "issues\_before": 2, "accepted\_replacements": 1, "remaining\_issues": 1, "classification\_fields\_modified": false, "inherited\_from\_source\_attempt": true\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope", "inherited\_from\_source\_attempt": true\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason\_code": "unresolved\_checks", "inherited\_from\_source\_attempt": true\} |
| deterministic\_revalidation | 已完成 | \{"stage": "deterministic\_revalidation", "status": "completed", "previous\_verdict": "insufficient\_evidence", "verdict": "insufficient\_evidence", "model\_calls": 0, "evidence\_edited": false\} |

#### 证据

```json
[
  {
    "id": "obliinjection_claim_1",
    "verdict": "insufficient_evidence",
    "reason": "bound_policy_scope_not_established",
    "claim_result": "unresolved",
    "validation_mode": "flow_binding_v1",
    "issue_type": "information_boundary",
    "flow_binding": {
      "semantics_version": 1,
      "observation_target": "matched_edge",
      "recipient_role": "attacker_optimizer",
      "attacker_delivery": "confirmed",
      "instance_requirement": "same_evaluated_instance",
      "instance_relation": "unknown",
      "alignment_verified": true,
      "exclusion_verified": false
    },
    "binding_validation": {
      "recipient_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "source_validation": {
      "policy_supported": true,
      "delivery_supported": true,
      "binding_supported": true,
      "instance_alignment_supported": false,
      "exclusion_supported": false,
      "validation_errors": [
        "instance_mapping_source_identity_record_not_cited",
        "instance_mapping_evaluation_identity_record_not_cited",
        "instance_mapping_requires_distinct_source_and_evaluation_bindings"
      ]
    },
    "citation_errors": [],
    "safe_locator_metadata": [
      {
        "segment_id": "paper:p4",
        "start": 1836,
        "end": 1931,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
        "source_kind": "paper",
        "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 3759,
        "end": 3924,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 75,
        "line_end": 78
      },
      {
        "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
        "start": 760,
        "end": 785,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "source_kind": "code",
        "path": "configs/task_configs/hotpotqa_config.json",
        "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 16,
        "line_end": 16
      },
      {
        "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
        "start": 951,
        "end": 1111,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "source_kind": "code",
        "path": "configs/task_configs/hotpotqa_config.json",
        "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 24,
        "line_end": 26
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 11966,
        "end": 12129,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 254,
        "line_end": 255
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 4762,
        "end": 4809,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 101,
        "line_end": 101
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2736,
        "end": 2793,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 69,
        "line_end": 69
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 967,
        "end": 1099,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 33,
        "line_end": 33
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 2155,
        "end": 2284,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 47,
        "line_end": 47
      },
      {
        "segment_id": "paper:p4",
        "start": 881,
        "end": 973,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
        "source_kind": "paper",
        "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 14538,
        "end": 14682,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 292,
        "line_end": 296
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 4244,
        "end": 4385,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 93,
        "line_end": 95
      },
      {
        "segment_id": "repo:task/target_task.py:L1-L309",
        "start": 5568,
        "end": 5717,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "source_kind": "code",
        "path": "task/target_task.py",
        "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 113,
        "line_end": 116
      },
      {
        "segment_id": "repo:task/task.py:L1-L98",
        "start": 2417,
        "end": 2467,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "source_kind": "code",
        "path": "task/task.py",
        "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 61,
        "line_end": 61
      },
      {
        "segment_id": "repo:obliinjection.py:L1-L213",
        "start": 1254,
        "end": 1337,
        "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "source_kind": "code",
        "path": "obliinjection.py",
        "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
        "repository_source": "https://github.com/ReachalWang/ObliInjection",
        "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
        "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
        "line_start": 36,
        "line_end": 36
      }
    ],
    "missing_obligations": [
      {
        "kind": "same_instance_mapping",
        "conditional_on_policy_scope": false
      }
    ]
  }
]
```

#### 备注

```json
[
  "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "2026-11-21-v5-1-pilot-020638/deterministic_revalidation/obliinjection",
  "title": "V5.1 pilot · deterministic revalidation · ObliInjection",
  "run_id": "2026-11-21-v5-1-pilot-020638",
  "run_label": "V5.1 pilot",
  "paper_id": "obliinjection",
  "attempt_id": "deterministic_revalidation/obliinjection",
  "selected_final": false,
  "cohort_type": "deterministic_revalidation",
  "source_result_path": "revalidated/obliinjection/result.json",
  "source": "https://arxiv.org/pdf/2512.09321v3",
  "status": "completed",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason_code": "unresolved_checks",
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 18,
      "characters": 136067,
      "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
      "coverage": {
        "complete": true
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "source_discovery",
      "status": "completed",
      "discovery_status": "selected",
      "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "repository_ingestion",
      "status": "completed",
      "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
      "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
      "source_segments": 31,
      "coverage": {
        "complete": true,
        "inventory_complete": true,
        "eligible_files": 31,
        "included_files": 31,
        "omitted_files": 0,
        "excluded_entries": 7,
        "characters": 147332,
        "max_characters": 500000
      },
      "inherited_from_source_attempt": true
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 1,
      "execution": "reused_prior_model_result",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_repair",
      "status": "completed",
      "issues_before": 2,
      "accepted_replacements": 1,
      "remaining_issues": 1,
      "classification_fields_modified": false,
      "inherited_from_source_attempt": true
    },
    {
      "stage": "semantic_review",
      "status": "completed",
      "applicability": "in_scope",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "citation_validation_and_decision",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason_code": "unresolved_checks",
      "inherited_from_source_attempt": true
    },
    {
      "stage": "deterministic_revalidation",
      "status": "completed",
      "previous_verdict": "insufficient_evidence",
      "verdict": "insufficient_evidence",
      "model_calls": 0,
      "evidence_edited": false
    }
  ],
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1
  },
  "document_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
  "input_binding": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
  "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95",
  "request_hashes": {
    "input_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
    "model_content_sha256": "0ffc8c4b2c6fafd93665bae0fa051a7f76db6c3fc399ea6ea9eec66180ae4114",
    "prompt_sha256": "ccd992509dc0d89c0d0a64f9ba1be582b1586e155a1ef688b4f14bc3a35bfc95"
  },
  "repository": {
    "url": "https://github.com/ReachalWang/ObliInjection",
    "revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
    "manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
    "coverage": {
      "complete": true,
      "inventory_complete": true,
      "eligible_files": 31,
      "included_files": 31,
      "omitted_files": 0,
      "excluded_entries": 7,
      "characters": 147332,
      "max_characters": 500000
    },
    "dependency_snapshot_count": 0,
    "dependency_reference_counts": {
      "needed": 225,
      "unresolved": 176,
      "over_limit": 9
    },
    "evidence_expansion_counts": {
      "added_files": 12,
      "added_bytes": 7062,
      "inspected_paths": 31
    },
    "dependencies": []
  },
  "source_discovery": {
    "status": "selected",
    "reason_code": "unique_self_associated_code_link_resolved_to_full_commit",
    "repository_url": "https://github.com/ReachalWang/ObliInjection"
  },
  "inference": {
    "invocation_count": 0,
    "calls": [],
    "usage": {
      "input_tokens": 0,
      "cached_input_tokens": 0,
      "output_tokens": 0,
      "reasoning_output_tokens": 0
    },
    "usage_reporting_complete": true,
    "execution": "deterministic_revalidation_no_model_call"
  },
  "duration_seconds": 133.687,
  "evidence": [
    {
      "id": "obliinjection_claim_1",
      "verdict": "insufficient_evidence",
      "reason": "bound_policy_scope_not_established",
      "claim_result": "unresolved",
      "validation_mode": "flow_binding_v1",
      "issue_type": "information_boundary",
      "flow_binding": {
        "semantics_version": 1,
        "observation_target": "matched_edge",
        "recipient_role": "attacker_optimizer",
        "attacker_delivery": "confirmed",
        "instance_requirement": "same_evaluated_instance",
        "instance_relation": "unknown",
        "alignment_verified": true,
        "exclusion_verified": false
      },
      "binding_validation": {
        "recipient_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "source_validation": {
        "policy_supported": true,
        "delivery_supported": true,
        "binding_supported": true,
        "instance_alignment_supported": false,
        "exclusion_supported": false,
        "validation_errors": [
          "instance_mapping_source_identity_record_not_cited",
          "instance_mapping_evaluation_identity_record_not_cited",
          "instance_mapping_requires_distinct_source_and_evaluation_bindings"
        ]
      },
      "citation_errors": [],
      "safe_locator_metadata": [
        {
          "segment_id": "paper:p4",
          "start": 1836,
          "end": 1931,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
          "source_kind": "paper",
          "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 3759,
          "end": 3924,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 75,
          "line_end": 78
        },
        {
          "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
          "start": 760,
          "end": 785,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "source_kind": "code",
          "path": "configs/task_configs/hotpotqa_config.json",
          "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 16,
          "line_end": 16
        },
        {
          "segment_id": "repo:configs/task_configs/hotpotqa_config.json:L1-L29",
          "start": 951,
          "end": 1111,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "source_kind": "code",
          "path": "configs/task_configs/hotpotqa_config.json",
          "file_sha256": "1321b4374550440c51967efe73e1d31c6feb17696f83e0d2ffe48cc04ed6201b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 24,
          "line_end": 26
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 11966,
          "end": 12129,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 254,
          "line_end": 255
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 4762,
          "end": 4809,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 101,
          "line_end": 101
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2736,
          "end": 2793,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 69,
          "line_end": 69
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 967,
          "end": 1099,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 33,
          "line_end": 33
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 2155,
          "end": 2284,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 47,
          "line_end": 47
        },
        {
          "segment_id": "paper:p4",
          "start": 881,
          "end": 973,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "bc9941edd9d94ca84b98a626792bc9e6e71a13c78455a0a94c254b431a5ee77b",
          "source_kind": "paper",
          "paper_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 14538,
          "end": 14682,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 292,
          "line_end": 296
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 4244,
          "end": 4385,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 93,
          "line_end": 95
        },
        {
          "segment_id": "repo:task/target_task.py:L1-L309",
          "start": 5568,
          "end": 5717,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "source_kind": "code",
          "path": "task/target_task.py",
          "file_sha256": "b06637266d8751f67c49c80b7cf0ddb146421545d6bfa125a94c1764905892a1",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 113,
          "line_end": 116
        },
        {
          "segment_id": "repo:task/task.py:L1-L98",
          "start": 2417,
          "end": 2467,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "source_kind": "code",
          "path": "task/task.py",
          "file_sha256": "645e8dc36f8e9bdf5ed33f8d9c48c3a557e3fa6bbec7b04f807ec33c7859d92b",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 61,
          "line_end": 61
        },
        {
          "segment_id": "repo:obliinjection.py:L1-L213",
          "start": 1254,
          "end": 1337,
          "document_sha256": "ea9d48fab461cc760c30d017266dfff43f78a02915b8924593b5017190973d74",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "source_kind": "code",
          "path": "obliinjection.py",
          "file_sha256": "60edf58d7626f455261b7e42ba777033143ff0b1905def8e85d0c7ae39810f16",
          "repository_source": "https://github.com/ReachalWang/ObliInjection",
          "repository_revision": "b1f6a3f48c0cf121534374cbcef453832594867b",
          "repository_manifest_sha256": "56bc87f4cce70872cd970e1a206733961478d9e49837a2504d58d4773842f17b",
          "line_start": 36,
          "line_end": 36
        }
      ],
      "missing_obligations": [
        {
          "kind": "same_instance_mapping",
          "conditional_on_policy_scope": false
        }
      ]
    }
  ],
  "unresolved_questions": [
    "What are the contents and provenance of data/hotpotqa/hotpotqa_shadow.json? The supplied source cannot determine whether its sources are synthetic shadows, real target segments, or a mixture.",
    "Did a particular run load processed ./data/hotpotqa/train/source_num_3/target_data.npz and ./data/hotpotqa/test/source_num_10/target_data.npz, or enter raw fallback? Cache contents and their record mappings are unavailable; the conditional identity result does not cover arbitrary existing caches.",
    "The separate HotpotQA question channel remains relevant: __get_hotpotqa reads train_data[i]['question'], and obliinjection.py supplies target_train_question to gcg.run. Are these generated shadow questions or the actual evaluated questions, and how does the paper's specific-target-instruction restriction cover them?",
    "Does access to the configured source lists fall within the paper's allowance for certain clean segments, or supply the complete genuine target context? Missing data prevents resolving that scope."
  ],
  "notes": [
    "Deterministic decision revalidation of the existing extraction/review. No new model call; not independent inference and excluded from fresh paper denominators."
  ],
  "reused_inference_from": "2026-11-21-v5-1-pilot-020638/obliinjection/obliinjection",
  "revalidation": {
    "code_commit": "dcc3f28db50e99571393cee2763c4d88a2e458bf",
    "code_files_sha256": {
      "extraction_v5.py": "e6cb06f2cec52922b5756fb586801beefd7df68964d7e84268decf98ca47a1ac",
      "extraction_v4.py": "32237af4c332dd25ec9f91a672b4e1806cd02e7e68424756090895281aa31753",
      "extraction_v3.py": "f2610495b29cd38fdcac5aa50756766dc3d96742547a552df6f8635268f898ac",
      "checker.py": "859d59dda2b4f465e6efd248b410ec4bdd68896e2adeb03eac32fc2c210cfb0c",
      "scope_review.py": "c37baf0bf981c2aa03212555a90e8e09e3030811514eb7e433765cb4077a4640",
      "call_boundaries.py": "939b8812406d0b0d038d72d3755a2514a977fbb97cdb7558d66ebea8794aa5cf",
      "findings.py": "d5ff5e03081911982c6ee45011055e9e037918ef5ac8e02053980fbca552fcdd"
    },
    "reference_artifacts_sha256": {
      "result.json": "cfdca61eb3ce7b17ec4a78314b20a296805239b3adf9fd788a768f86e5c0b806",
      "extraction.repaired.json": "d4cf5e4a24d7427c7231701afbef8bbfc7b2387ee31c0ac0533862a60c74a3ac",
      "review.json": "4a2c7feeaed2c016ec17f7ddad009324da0050511d206f701e4f341429282dd9",
      "combined_input.json": "dedc09ace1dc21e8075c2fbe03114871e41bd84cd3bfc6869818e4322aa6ebae",
      "request.json": "8452aca41e4cb9dd0b1041c9c348fbc5865fe21da9055103bc0bb76ef3061729"
    },
    "original_verdict": "insufficient_evidence",
    "model_calls": 0,
    "evidence_edited": false
  }
}
```
