# 论文审计：测试过程与结果

运行类型：document\_scan  
生成时间：2026\-11\-19T09:38:19\.549993\+00:00  
论文记录：4

主表每篇论文一行。“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。

## 本次运行汇总

```json
{
  "paper_count": 4,
  "statuses": {
    "completed": 4
  },
  "verdicts": {
    "insufficient_evidence": 4
  },
  "reference_label_comparison": {
    "matched": 0,
    "completed": 4,
    "total": 4,
    "interpretation": "historical labels may use evidence outside the PDF; not accuracy"
  }
}
```

## 论文结果

| 论文 ID | 论文 | 运行 / 判定 | 已确认不一致 | 标签对照 | 来源 |
| --- | --- | --- | --- | --- | --- |
| trojan\_hippo | Trojan Hippo information\-budget audit | 证据不足 | 未确认 | 未评分；预期：未记录状态 | https://arxiv\.org/pdf/2605\.01970v1 |
| topicattack | TopicAttack information\-budget audit | 证据不足 | 未确认 | 未评分；预期：未记录状态 | https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf |
| agentdojo | AgentDojo information\-budget audit | 证据不足 | 未确认 | 未评分；预期：未记录状态 | https://papers\.neurips\.cc/paper\_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54\-Paper\-Datasets\_and\_Benchmarks\_Track\.pdf |
| asb | ASB information\-budget audit | 证据不足 | 未确认 | 未评分；预期：未记录状态 | https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b\-Paper\-Conference\.pdf |

## 逐篇测试过程

### 1. Trojan Hippo information\-budget audit

论文 ID：trojan\_hippo  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 22, "characters": 214103, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/debesheedas/troja", "https://doi\.org/10\.12688/f1000research\.169927\.1", "https://www\.an", "https://claude\.com/import\-memory", "https://doi\.org/10\.48550/arxiv\.2504\.14064", "https://doi\.org/10\.48550/arxiv\.2407\.12784", "https://doi\.org/10", "https://doi\.org/10\.48550/arxiv\.2406\.13352", "https://doi\.org/10\.1145/3716628", "https://doi\.org/10\.1016/j\.icte\.2025\.12\.001", "https://arstechnica\.com/security", "https://openai\.com/index/scaling\-ai\-for\-", "https://get\.mem\.ai/", "https://blog\.google/products/gemini/google\-gemini\-update\-august\-2024/", "https://notebooklm\.google/", "https://deepmind\.google/mode", "https://doi\.org/10\.48550/arxiv\.2504\.19956", "https://deepmind\.google/models/project\-astra/", "https://openai\.com/blog/memory\-and\-new\-controls\-for\-chatgpt", "https://help\.openai\.com/en/articles/8983136\-what\-", "https://developers\.openai\.com/api/docs/models/gpt\-5", "https://developers\.openai\.com/api/docs/models/gpt\-", "https://chatgpt\.com/", "https://open", "https://unit42\.paloalton", "https://www\.sciencedirect\.com/science/article/abs/pii/S0167739X250", "https://doi\.org/10\.1016/j\.future\.2025\.107994", "https://www\.sciencedirect", "https://reference\.langchain\.co", "https://www\.personal\.ai/", "https://doi\.org/10\.4", "https://doi\.org/10\.48550/arxiv\.2511\.15759", "https://embracethere", "https://embracethe", "https://www\.ovid\.com/journals/prin/fulltext/10\.1037/pri0000292", "https://github\.com/algorithmicsuperintelligence/openevolve", "https://www\.zendesk\.com/newsroom/press\-", "https://doi\.org/10\.48550/arxiv\.2506\.23844", "https://doi\.org/", "https://doi\.org/10\.48550/arx"\], "sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce"\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 3\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "trojan_hippo_claim_1",
    "source_group": "paper_text",
    "description": "A construction feedback boundary is described; whether it exceeds the applicable training information budget remains unresolved.",
    "scope": {
      "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
      "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "adaptive attack optimizer",
      "phase": "training-time payload construction",
      "source": "LLM critic evaluating training rollouts",
      "representation": "numeric score and improvement feedback",
      "operation": "refine attack candidates"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Critic-feedback suspicion: adaptive construction receives failure explanations beyond the deployed adversary's exfiltration-only feedback.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "other",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "uncertain",
        "reason": "The restriction describes adversary observability, but the paper separately permits adaptive optimization in a training environment. Its applicability to critic feedback during that construction phase is unclear.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 2490, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2438, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "paper_procedure",
        "task_relation": "training_instance",
        "reason": "The described optimization loop uses critic feedback. It does not specify the critic's inputs or establish delivery of internal traces or raw queries to the mutator.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 5320, \"match\": \"normalized_exact\", \"segment_id\": \"p5\", \"start\": 5228, \"text_view\": \"reading_order\", \"text_view_sha256\": \"a95cdfda163a087844f68ce70cea711fae092677f6c30cf939e87c89ce566b59\"}"
      },
      "refutation": {
        "basis": "none",
        "reason": "Training optimization is disclosed, but no specific permission for internal-state diagnostics or exclusion of such diagnostics is supplied.",
        "reference": ""
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [
      "semantic_review_disagrees_with_proposed_assessment"
    ],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 2438,
        "end": 2490,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
      },
      "delivery": {
        "segment_id": "p5",
        "start": 5228,
        "end": 5320,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "a95cdfda163a087844f68ce70cea711fae092677f6c30cf939e87c89ce566b59"
      },
      "implementation": {
        "segment_id": "p6",
        "start": 98,
        "end": 142,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
      }
    },
    "semantic_review": {
      "index": 0,
      "supported": false,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "uncertain",
      "delivery": "unresolved",
      "refutation": "none",
      "reason": "p5–p6 describe critic scoring and improvement feedback, but do not establish which feedback reaches the mutator or whether it contains internal-state diagnostics. Applicability of p4's observability budget to training construction remains unresolved; disclosed adaptation alone grants no exception."
    }
  },
  {
    "id": "trojan_hippo_claim_2",
    "source_group": "paper_text",
    "description": "Paper-level separation refutes this suspicion. It does not establish which training query text, if any, reaches the payload LLM.",
    "scope": {
      "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
      "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "adaptive attack optimizer",
      "phase": "payload construction before held-out evaluation",
      "source": "held-out test cases",
      "representation": "evaluation user queries",
      "operation": "condition attack optimization",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "refutation_not_supported_by_scoped_evidence",
    "matching_rules": [
      {
        "edge": {
          "role": "adaptive attack optimizer",
          "phase": "payload construction before held-out evaluation",
          "source": "held-out test cases",
          "representation": "evaluation user queries",
          "operation": "condition attack optimization",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1527, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1467, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "adaptive attack optimizer",
          "phase": "payload construction before held-out evaluation",
          "source": "held-out test cases",
          "representation": "evaluation user queries",
          "operation": "condition attack optimization",
          "query_form": "full_query"
        },
        "status": "absent",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1762, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1648, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Held-out-query suspicion: training optimization accesses the same query instances later used for evaluation.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "policy_kind": "protocol_requirement",
        "status": "applicable",
        "reason": "The exclusion specifically concerns held-out instances during attack optimization.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 3730, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3695, \"text_view\": \"primary\", \"text_view_sha256\": \"e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09\"}"
      },
      "delivery": {
        "status": "excluded",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reason": "The described procedure separates construction cases from held-out evaluation cases.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1356, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1265, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
      },
      "refutation": {
        "basis": "different_instance",
        "reason": "Optimization uses a distinct training instance; shared sensitive topics do not establish shared evaluation queries.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 3028, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2994, \"text_view\": \"primary\", \"text_view_sha256\": \"e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09\"}"
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p6",
        "start": 3695,
        "end": 3730,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
      },
      "delivery": {
        "segment_id": "p6",
        "start": 1265,
        "end": 1356,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
      },
      "refutation": {
        "segment_id": "p6",
        "start": 2994,
        "end": 3028,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
      },
      "declaration": {
        "segment_id": "p6",
        "start": 1467,
        "end": 1527,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
      },
      "implementation": {
        "segment_id": "p6",
        "start": 1648,
        "end": 1762,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
      }
    },
    "semantic_review": {
      "index": 1,
      "supported": true,
      "policy_kind": "protocol_requirement",
      "policy_application": "applicable",
      "delivery": "excluded",
      "refutation": "different_instance",
      "reason": "p6 affirmatively separates optimization on one training case from four unseen test cases using disjoint template and entity pools. This excludes the claimed held-out-instance access; shared topics do not establish identical queries or mutator receipt of training query text."
    }
  },
  {
    "id": "trojan_hippo_claim_3",
    "source_group": "paper_text",
    "description": "Permission to know architecture does not imply permission to inspect memory contents, internal execution state, or held-out queries.",
    "scope": {
      "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
      "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "attacker",
      "phase": "attack construction",
      "source": "agent architecture and interface specification",
      "representation": "system prompt, backend, and tool interface",
      "operation": "adapt payload to the target configuration"
    },
    "verdict": "insufficient_evidence",
    "reason": "evaluated_instance_alignment_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker",
          "phase": "attack construction",
          "source": "agent architecture and interface specification",
          "representation": "system prompt, backend, and tool interface",
          "operation": "adapt payload to the target configuration"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1972, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 1863, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Architecture-knowledge control: knowledge of the system prompt, memory backend, and tool interface is explicitly permitted.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "other",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "This specific knowledge grant applies to the modeled attacker.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1972, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 1863, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "possible_path",
        "task_relation": "unknown",
        "reason": "Configuration-specific optimization is described, but the exact architecture material delivered to the mutator is not supplied.",
        "reference": ""
      },
      "refutation": {
        "basis": "none",
        "reason": "The explicit white-box grant defeats a suspicion based solely on architecture knowledge.",
        "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 2124, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2060, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 1863,
        "end": 1972,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
      },
      "refutation": {
        "segment_id": "p4",
        "start": 2060,
        "end": 2124,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
      },
      "declaration": {
        "segment_id": "p4",
        "start": 1863,
        "end": 1972,
        "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
      }
    },
    "semantic_review": {
      "index": 2,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "unresolved",
      "refutation": "explicit_permission",
      "reason": "p4 explicitly permits knowledge of the system prompt, memory backend, and tool interface, defeating an architecture-knowledge mismatch. Actual delivery to the mutator is unspecified, and this grant does not extend to internal state or held-out queries."
    }
  }
]
```

#### 备注

```json
[
  "Only supplied paper text was audited; no code, saved requests, or independently observed runtime evidence was supplied.",
  "The example exfiltration trace demonstrates a victim security failure, not prohibited attacker knowledge during construction.",
  "Critic inputs, feedback delivery to the mutator, and the training applicability of the observability restriction remain unanswered.",
  "The supplied text does not establish raw training-query delivery to the optimizer.",
  "The example exfiltration demonstrates a victim security failure, not prohibited construction knowledge; causal impact of any construction-budget mismatch is unestablished.",
  "Review is limited to supplied text and the explicit listed suspicions."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "trojan_hippo",
  "title": "Trojan Hippo information-budget audit",
  "source": "https://arxiv.org/pdf/2605.01970v1",
  "status": "completed",
  "has_confirmed_inconsistency": false,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 22,
      "characters": 214103,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/debesheedas/troja",
        "https://doi.org/10.12688/f1000research.169927.1",
        "https://www.an",
        "https://claude.com/import-memory",
        "https://doi.org/10.48550/arxiv.2504.14064",
        "https://doi.org/10.48550/arxiv.2407.12784",
        "https://doi.org/10",
        "https://doi.org/10.48550/arxiv.2406.13352",
        "https://doi.org/10.1145/3716628",
        "https://doi.org/10.1016/j.icte.2025.12.001",
        "https://arstechnica.com/security",
        "https://openai.com/index/scaling-ai-for-",
        "https://get.mem.ai/",
        "https://blog.google/products/gemini/google-gemini-update-august-2024/",
        "https://notebooklm.google/",
        "https://deepmind.google/mode",
        "https://doi.org/10.48550/arxiv.2504.19956",
        "https://deepmind.google/models/project-astra/",
        "https://openai.com/blog/memory-and-new-controls-for-chatgpt",
        "https://help.openai.com/en/articles/8983136-what-",
        "https://developers.openai.com/api/docs/models/gpt-5",
        "https://developers.openai.com/api/docs/models/gpt-",
        "https://chatgpt.com/",
        "https://open",
        "https://unit42.paloalton",
        "https://www.sciencedirect.com/science/article/abs/pii/S0167739X250",
        "https://doi.org/10.1016/j.future.2025.107994",
        "https://www.sciencedirect",
        "https://reference.langchain.co",
        "https://www.personal.ai/",
        "https://doi.org/10.4",
        "https://doi.org/10.48550/arxiv.2511.15759",
        "https://embracethere",
        "https://embracethe",
        "https://www.ovid.com/journals/prin/fulltext/10.1037/pri0000292",
        "https://github.com/algorithmicsuperintelligence/openevolve",
        "https://www.zendesk.com/newsroom/press-",
        "https://doi.org/10.48550/arxiv.2506.23844",
        "https://doi.org/",
        "https://doi.org/10.48550/arx"
      ],
      "sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce"
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 3
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
      "reason": "unresolved_checks"
    }
  ],
  "evidence": [
    {
      "id": "trojan_hippo_claim_1",
      "source_group": "paper_text",
      "description": "A construction feedback boundary is described; whether it exceeds the applicable training information budget remains unresolved.",
      "scope": {
        "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "adaptive attack optimizer",
        "phase": "training-time payload construction",
        "source": "LLM critic evaluating training rollouts",
        "representation": "numeric score and improvement feedback",
        "operation": "refine attack candidates"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Critic-feedback suspicion: adaptive construction receives failure explanations beyond the deployed adversary's exfiltration-only feedback.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "other",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "uncertain",
          "reason": "The restriction describes adversary observability, but the paper separately permits adaptive optimization in a training environment. Its applicability to critic feedback during that construction phase is unclear.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 2490, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2438, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "paper_procedure",
          "task_relation": "training_instance",
          "reason": "The described optimization loop uses critic feedback. It does not specify the critic's inputs or establish delivery of internal traces or raw queries to the mutator.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 5320, \"match\": \"normalized_exact\", \"segment_id\": \"p5\", \"start\": 5228, \"text_view\": \"reading_order\", \"text_view_sha256\": \"a95cdfda163a087844f68ce70cea711fae092677f6c30cf939e87c89ce566b59\"}"
        },
        "refutation": {
          "basis": "none",
          "reason": "Training optimization is disclosed, but no specific permission for internal-state diagnostics or exclusion of such diagnostics is supplied.",
          "reference": ""
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [
        "semantic_review_disagrees_with_proposed_assessment"
      ],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 2438,
          "end": 2490,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
        },
        "delivery": {
          "segment_id": "p5",
          "start": 5228,
          "end": 5320,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "a95cdfda163a087844f68ce70cea711fae092677f6c30cf939e87c89ce566b59"
        },
        "implementation": {
          "segment_id": "p6",
          "start": 98,
          "end": 142,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
        }
      },
      "semantic_review": {
        "index": 0,
        "supported": false,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "uncertain",
        "delivery": "unresolved",
        "refutation": "none",
        "reason": "p5–p6 describe critic scoring and improvement feedback, but do not establish which feedback reaches the mutator or whether it contains internal-state diagnostics. Applicability of p4's observability budget to training construction remains unresolved; disclosed adaptation alone grants no exception."
      }
    },
    {
      "id": "trojan_hippo_claim_2",
      "source_group": "paper_text",
      "description": "Paper-level separation refutes this suspicion. It does not establish which training query text, if any, reaches the payload LLM.",
      "scope": {
        "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "adaptive attack optimizer",
        "phase": "payload construction before held-out evaluation",
        "source": "held-out test cases",
        "representation": "evaluation user queries",
        "operation": "condition attack optimization",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "refutation_not_supported_by_scoped_evidence",
      "matching_rules": [
        {
          "edge": {
            "role": "adaptive attack optimizer",
            "phase": "payload construction before held-out evaluation",
            "source": "held-out test cases",
            "representation": "evaluation user queries",
            "operation": "condition attack optimization",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1527, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1467, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "adaptive attack optimizer",
            "phase": "payload construction before held-out evaluation",
            "source": "held-out test cases",
            "representation": "evaluation user queries",
            "operation": "condition attack optimization",
            "query_form": "full_query"
          },
          "status": "absent",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1762, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1648, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Held-out-query suspicion: training optimization accesses the same query instances later used for evaluation.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "policy_kind": "protocol_requirement",
          "status": "applicable",
          "reason": "The exclusion specifically concerns held-out instances during attack optimization.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 3730, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3695, \"text_view\": \"primary\", \"text_view_sha256\": \"e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09\"}"
        },
        "delivery": {
          "status": "excluded",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reason": "The described procedure separates construction cases from held-out evaluation cases.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1356, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 1265, \"text_view\": \"reading_order\", \"text_view_sha256\": \"2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1\"}"
        },
        "refutation": {
          "basis": "different_instance",
          "reason": "Optimization uses a distinct training instance; shared sensitive topics do not establish shared evaluation queries.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 3028, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2994, \"text_view\": \"primary\", \"text_view_sha256\": \"e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09\"}"
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p6",
          "start": 3695,
          "end": 3730,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
        },
        "delivery": {
          "segment_id": "p6",
          "start": 1265,
          "end": 1356,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
        },
        "refutation": {
          "segment_id": "p6",
          "start": 2994,
          "end": 3028,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "e2ea2ca121f34c78b2558c31c1df27b6e9ef1949692414a60a8571b203feef09"
        },
        "declaration": {
          "segment_id": "p6",
          "start": 1467,
          "end": 1527,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
        },
        "implementation": {
          "segment_id": "p6",
          "start": 1648,
          "end": 1762,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "2ca711c3c52c225833ed6dfaae1f0d6d42371ac88763f2ad0897c80abb2d44c1"
        }
      },
      "semantic_review": {
        "index": 1,
        "supported": true,
        "policy_kind": "protocol_requirement",
        "policy_application": "applicable",
        "delivery": "excluded",
        "refutation": "different_instance",
        "reason": "p6 affirmatively separates optimization on one training case from four unseen test cases using disjoint template and entity pools. This excludes the claimed held-out-instance access; shared topics do not establish identical queries or mutator receipt of training query text."
      }
    },
    {
      "id": "trojan_hippo_claim_3",
      "source_group": "paper_text",
      "description": "Permission to know architecture does not imply permission to inspect memory contents, internal execution state, or held-out queries.",
      "scope": {
        "paper_version": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
        "experiment_arm": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "attacker",
        "phase": "attack construction",
        "source": "agent architecture and interface specification",
        "representation": "system prompt, backend, and tool interface",
        "operation": "adapt payload to the target configuration"
      },
      "verdict": "insufficient_evidence",
      "reason": "evaluated_instance_alignment_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker",
            "phase": "attack construction",
            "source": "agent architecture and interface specification",
            "representation": "system prompt, backend, and tool interface",
            "operation": "adapt payload to the target configuration"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1972, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 1863, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Architecture-knowledge control: knowledge of the system prompt, memory backend, and tool interface is explicitly permitted.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "other",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "This specific knowledge grant applies to the modeled attacker.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 1972, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 1863, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "possible_path",
          "task_relation": "unknown",
          "reason": "Configuration-specific optimization is described, but the exact architecture material delivered to the mutator is not supplied.",
          "reference": ""
        },
        "refutation": {
          "basis": "none",
          "reason": "The explicit white-box grant defeats a suspicion based solely on architecture knowledge.",
          "reference": "{\"document_sha256\": \"4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce\", \"end\": 2124, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2060, \"text_view\": \"reading_order\", \"text_view_sha256\": \"f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe\"}"
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 1863,
          "end": 1972,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
        },
        "refutation": {
          "segment_id": "p4",
          "start": 2060,
          "end": 2124,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
        },
        "declaration": {
          "segment_id": "p4",
          "start": 1863,
          "end": 1972,
          "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "f39ab1227d4f73dea9f3f3d46668abf931d8a2c60b29d72a4ab8ac4c6f808dbe"
        }
      },
      "semantic_review": {
        "index": 2,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "unresolved",
        "refutation": "explicit_permission",
        "reason": "p4 explicitly permits knowledge of the system prompt, memory backend, and tool interface, defeating an architecture-knowledge mismatch. Actual delivery to the mutator is unspecified, and this grant does not extend to internal state or held-out queries."
      }
    }
  ],
  "document_sha256": "4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce",
  "schema_version": 3,
  "applicability": "in_scope",
  "scope": "Paper-only audit of adaptive construction feedback, held-out information separation, and permitted architecture knowledge. The supplied text establishes no definite prohibited construction input.",
  "review_status": "model_reviewed_not_human_verified",
  "evidence_scope": "listed_claims_document_only",
  "notes": [
    "Only supplied paper text was audited; no code, saved requests, or independently observed runtime evidence was supplied.",
    "The example exfiltration trace demonstrates a victim security failure, not prohibited attacker knowledge during construction.",
    "Critic inputs, feedback delivery to the mutator, and the training applicability of the observability restriction remain unanswered.",
    "The supplied text does not establish raw training-query delivery to the optimizer.",
    "The example exfiltration demonstrates a victim security failure, not prohibited construction knowledge; causal impact of any construction-budget mismatch is unestablished.",
    "Review is limited to supplied text and the explicit listed suspicions."
  ],
  "unresolved_questions": [
    "What inputs does the LLM critic receive, and which resulting feedback reaches the mutator?",
    "Does the exfiltration-only observability restriction apply during training optimization, or only during deployed attack execution?",
    "Does the mutator receive training query text, topic labels alone, or other derived information?"
  ],
  "verdict": "insufficient_evidence",
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 3
  },
  "input_mode": "document_only",
  "prompt_sha256": "a2c05a361fc0a14027ff29bfb1bf05e6678aec9369c63dd16cc4f9349ec8ce76",
  "duration_seconds": 60.435,
  "cohort": "previously_suspected_control",
  "expected": null,
  "expected_basis": "pending_independent_adjudication",
  "comparison_note": "A suspected false positive is not assumed clean; resolve against source evidence.",
  "matches_gold": null
}
```

### 2. TopicAttack information\-budget audit

论文 ID：topicattack  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 19, "characters": 99756, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/", "https://copilot\.microsoft\.com/", "https://www\.perplexity\.ai/", "https://learnprompting", "https://dropbox\.tech/machine\-learning/", "https://simonwillison\.net/"\], "sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7"\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 3\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "topicattack_claim_1",
    "source_group": "paper_text",
    "description": "Query-related fabricated dialogue can arise from permitted benign content. Its similarity to the original question does not prove access to that question.",
    "scope": {
      "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
      "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "TopicAttack transition-generation model",
      "phase": "payload construction",
      "source": "original user input instruction",
      "representation": "raw query text",
      "operation": "potential inclusion in transition-generation inputs",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "delivery_to_input_boundary_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "TopicAttack transition-generation model",
          "phase": "payload construction",
          "source": "original user input instruction",
          "representation": "raw query text",
          "operation": "potential inclusion in transition-generation inputs",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 308, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 243, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Exact-query exposure: the supplied examples do not establish that the original evaluation query reaches the transition-generation model.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The restriction applies to TopicAttack construction for the same target instruction.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 3544, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 3482, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "possible_path",
        "task_relation": "same_evaluated_instance",
        "reason": "The construction template names data and topic inputs. Case studies show user queries alongside payloads, but do not establish query delivery to the auxiliary model or supply actual placeholder bindings.",
        "reference": ""
      },
      "refutation": {
        "basis": "none",
        "reason": "No saved construction requests or independently verified input bindings establish either exposure or exclusion.",
        "reference": ""
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 3482,
        "end": 3544,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
      },
      "declaration": {
        "segment_id": "p4",
        "start": 243,
        "end": 308,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
      }
    },
    "semantic_review": {
      "index": 0,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "unresolved",
      "refutation": "none",
      "reason": "p4 excludes original-query knowledge from TopicAttack construction. p13 supplies a content-conditioned template, but no actual bindings establish query delivery or exclusion. Queries displayed beside payloads in case studies do not establish auxiliary-model receipt."
    }
  },
  {
    "id": "topicattack_claim_2",
    "source_group": "paper_text",
    "description": "Knowing document content and its topic is distinct from receiving the original user query.",
    "scope": {
      "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
      "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "TopicAttack transition-generation model",
      "phase": "payload construction",
      "source": "benign external content",
      "representation": "data content in the construction prompt",
      "operation": "generate a conversation transitioning toward the injected objective"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "TopicAttack transition-generation model",
          "phase": "payload construction",
          "source": "benign external content",
          "representation": "data content in the construction prompt",
          "operation": "generate a conversation transitioning toward the injected objective"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "TopicAttack transition-generation model",
          "phase": "payload construction",
          "source": "benign external content",
          "representation": "data content in the construction prompt",
          "operation": "generate a conversation transitioning toward the injected objective"
        },
        "status": "present",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 412, \"match\": \"normalized_exact\", \"segment_id\": \"p13\", \"start\": 252, \"text_view\": \"primary\", \"text_view_sha256\": \"7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Permitted benign-content control: TopicAttack conditions transition construction on the content being injected.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The grant covers this actor, construction phase, and injected document.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reason": "The published construction prompt explicitly uses supplied data content.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 551, \"match\": \"normalized_exact\", \"segment_id\": \"p13\", \"start\": 468, \"text_view\": \"primary\", \"text_view_sha256\": \"7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349\"}"
      },
      "refutation": {
        "basis": "explicit_permission",
        "reason": "Document-conditioned construction is expressly permitted.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
      }
    },
    "claim_result": "refuted",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 314,
        "end": 396,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
      },
      "delivery": {
        "segment_id": "p13",
        "start": 468,
        "end": 551,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349"
      },
      "refutation": {
        "segment_id": "p4",
        "start": 314,
        "end": 396,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
      },
      "declaration": {
        "segment_id": "p4",
        "start": 314,
        "end": 396,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
      },
      "implementation": {
        "segment_id": "p13",
        "start": 252,
        "end": 412,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349"
      }
    },
    "semantic_review": {
      "index": 1,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "confirmed",
      "refutation": "explicit_permission",
      "reason": "p13 explicitly supplies benign data to the transition-generation model, and p4 expressly permits knowledge of that content. This permission does not establish access to the exact user query."
    }
  },
  {
    "id": "topicattack_claim_3",
    "source_group": "paper_text",
    "description": "The comparison supports gradient access in that arm only. It does not establish raw-query delivery or TopicAttack access to victim internals.",
    "scope": {
      "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
      "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "GCG and AutoDAN comparison implementations",
      "phase": "attack optimization",
      "source": "comparison victim models",
      "representation": "model gradients used for prompt optimization",
      "operation": "construct gradient-based baseline attacks"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "GCG and AutoDAN comparison implementations",
          "phase": "attack optimization",
          "source": "comparison victim models",
          "representation": "model gradients used for prompt optimization",
          "operation": "construct gradient-based baseline attacks"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4041, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3777, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "GCG and AutoDAN comparison implementations",
          "phase": "attack optimization",
          "source": "comparison victim models",
          "representation": "model gradients used for prompt optimization",
          "operation": "construct gradient-based baseline attacks"
        },
        "status": "present",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4167, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 4055, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Gradient-access exception: victim-model gradients are used in an explicitly stronger comparison arm.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "other",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The passage explicitly introduces the comparison as an exception to the preceding model-ignorance assumption.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4040, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3944, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "unknown",
        "reason": "The paper describes model-specific optimization, but does not specify optimization-instance versus evaluation-instance relationships.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4254, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 4169, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
      },
      "refutation": {
        "basis": "explicit_permission",
        "reason": "This is a disclosed stronger baseline arm; its access does not establish forbidden access by TopicAttack.",
        "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4041, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3777, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
      }
    },
    "claim_result": "refuted",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p7",
        "start": 3944,
        "end": 4040,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
      },
      "delivery": {
        "segment_id": "p7",
        "start": 4169,
        "end": 4254,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
      },
      "refutation": {
        "segment_id": "p7",
        "start": 3777,
        "end": 4041,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
      },
      "declaration": {
        "segment_id": "p7",
        "start": 3777,
        "end": 4041,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
      },
      "implementation": {
        "segment_id": "p7",
        "start": 4055,
        "end": 4167,
        "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "match": "normalized_exact",
        "text_view": "reading_order",
        "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
      }
    },
    "semantic_review": {
      "index": 2,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "confirmed",
      "refutation": "explicit_permission",
      "reason": "p7 specifically introduces gradient-based optimization despite the earlier model-ignorance assumption, supporting a gradient-access exception for these comparison implementations. It does not authorize every knowledge type or establish raw-query access, identical optimization/evaluation records, or TopicAttack access to victim internals."
    }
  }
]
```

#### 备注

```json
[
  "Only supplied paper text was available; no static code, saved requests, or runtime traces were supplied.",
  "Reported attack success and defense failures establish security outcomes, not violations of attacker knowledge restrictions.",
  "Exact construction-input bindings and possible original-query exposure remain unanswered.",
  "The relationship between gradient-optimization instances and evaluated instances remains unspecified.",
  "Supplied procedures support construction findings; reported attack success does not establish a knowledge-budget violation or the causal impact of forbidden access."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "topicattack",
  "title": "TopicAttack information-budget audit",
  "source": "https://aclanthology.org/2025.emnlp-main.372.pdf",
  "status": "completed",
  "has_confirmed_inconsistency": false,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 19,
      "characters": 99756,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/",
        "https://copilot.microsoft.com/",
        "https://www.perplexity.ai/",
        "https://learnprompting",
        "https://dropbox.tech/machine-learning/",
        "https://simonwillison.net/"
      ],
      "sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7"
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 3
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
      "reason": "unresolved_checks"
    }
  ],
  "evidence": [
    {
      "id": "topicattack_claim_1",
      "source_group": "paper_text",
      "description": "Query-related fabricated dialogue can arise from permitted benign content. Its similarity to the original question does not prove access to that question.",
      "scope": {
        "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "TopicAttack transition-generation model",
        "phase": "payload construction",
        "source": "original user input instruction",
        "representation": "raw query text",
        "operation": "potential inclusion in transition-generation inputs",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "delivery_to_input_boundary_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "TopicAttack transition-generation model",
            "phase": "payload construction",
            "source": "original user input instruction",
            "representation": "raw query text",
            "operation": "potential inclusion in transition-generation inputs",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 308, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 243, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Exact-query exposure: the supplied examples do not establish that the original evaluation query reaches the transition-generation model.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The restriction applies to TopicAttack construction for the same target instruction.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 3544, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 3482, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "possible_path",
          "task_relation": "same_evaluated_instance",
          "reason": "The construction template names data and topic inputs. Case studies show user queries alongside payloads, but do not establish query delivery to the auxiliary model or supply actual placeholder bindings.",
          "reference": ""
        },
        "refutation": {
          "basis": "none",
          "reason": "No saved construction requests or independently verified input bindings establish either exposure or exclusion.",
          "reference": ""
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 3482,
          "end": 3544,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
        },
        "declaration": {
          "segment_id": "p4",
          "start": 243,
          "end": 308,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
        }
      },
      "semantic_review": {
        "index": 0,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "unresolved",
        "refutation": "none",
        "reason": "p4 excludes original-query knowledge from TopicAttack construction. p13 supplies a content-conditioned template, but no actual bindings establish query delivery or exclusion. Queries displayed beside payloads in case studies do not establish auxiliary-model receipt."
      }
    },
    {
      "id": "topicattack_claim_2",
      "source_group": "paper_text",
      "description": "Knowing document content and its topic is distinct from receiving the original user query.",
      "scope": {
        "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "TopicAttack transition-generation model",
        "phase": "payload construction",
        "source": "benign external content",
        "representation": "data content in the construction prompt",
        "operation": "generate a conversation transitioning toward the injected objective"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "TopicAttack transition-generation model",
            "phase": "payload construction",
            "source": "benign external content",
            "representation": "data content in the construction prompt",
            "operation": "generate a conversation transitioning toward the injected objective"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "TopicAttack transition-generation model",
            "phase": "payload construction",
            "source": "benign external content",
            "representation": "data content in the construction prompt",
            "operation": "generate a conversation transitioning toward the injected objective"
          },
          "status": "present",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 412, \"match\": \"normalized_exact\", \"segment_id\": \"p13\", \"start\": 252, \"text_view\": \"primary\", \"text_view_sha256\": \"7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Permitted benign-content control: TopicAttack conditions transition construction on the content being injected.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The grant covers this actor, construction phase, and injected document.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reason": "The published construction prompt explicitly uses supplied data content.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 551, \"match\": \"normalized_exact\", \"segment_id\": \"p13\", \"start\": 468, \"text_view\": \"primary\", \"text_view_sha256\": \"7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349\"}"
        },
        "refutation": {
          "basis": "explicit_permission",
          "reason": "Document-conditioned construction is expressly permitted.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 396, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 314, \"text_view\": \"reading_order\", \"text_view_sha256\": \"0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407\"}"
        }
      },
      "claim_result": "refuted",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 314,
          "end": 396,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
        },
        "delivery": {
          "segment_id": "p13",
          "start": 468,
          "end": 551,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349"
        },
        "refutation": {
          "segment_id": "p4",
          "start": 314,
          "end": 396,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
        },
        "declaration": {
          "segment_id": "p4",
          "start": 314,
          "end": 396,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "0a692b2efb3c2711f0231994579cafff779c8799f9ddd29754ce8d73710bb407"
        },
        "implementation": {
          "segment_id": "p13",
          "start": 252,
          "end": 412,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7adf3e2073ac2ceb5f38a27b63dc33ee105a3d87f7adfc73bdbe22435be9e349"
        }
      },
      "semantic_review": {
        "index": 1,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "confirmed",
        "refutation": "explicit_permission",
        "reason": "p13 explicitly supplies benign data to the transition-generation model, and p4 expressly permits knowledge of that content. This permission does not establish access to the exact user query."
      }
    },
    {
      "id": "topicattack_claim_3",
      "source_group": "paper_text",
      "description": "The comparison supports gradient access in that arm only. It does not establish raw-query delivery or TopicAttack access to victim internals.",
      "scope": {
        "paper_version": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
        "experiment_arm": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "GCG and AutoDAN comparison implementations",
        "phase": "attack optimization",
        "source": "comparison victim models",
        "representation": "model gradients used for prompt optimization",
        "operation": "construct gradient-based baseline attacks"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "GCG and AutoDAN comparison implementations",
            "phase": "attack optimization",
            "source": "comparison victim models",
            "representation": "model gradients used for prompt optimization",
            "operation": "construct gradient-based baseline attacks"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4041, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3777, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "GCG and AutoDAN comparison implementations",
            "phase": "attack optimization",
            "source": "comparison victim models",
            "representation": "model gradients used for prompt optimization",
            "operation": "construct gradient-based baseline attacks"
          },
          "status": "present",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4167, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 4055, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Gradient-access exception: victim-model gradients are used in an explicitly stronger comparison arm.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "other",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The passage explicitly introduces the comparison as an exception to the preceding model-ignorance assumption.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4040, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3944, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "unknown",
          "reason": "The paper describes model-specific optimization, but does not specify optimization-instance versus evaluation-instance relationships.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4254, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 4169, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
        },
        "refutation": {
          "basis": "explicit_permission",
          "reason": "This is a disclosed stronger baseline arm; its access does not establish forbidden access by TopicAttack.",
          "reference": "{\"document_sha256\": \"8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7\", \"end\": 4041, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 3777, \"text_view\": \"reading_order\", \"text_view_sha256\": \"d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08\"}"
        }
      },
      "claim_result": "refuted",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p7",
          "start": 3944,
          "end": 4040,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
        },
        "delivery": {
          "segment_id": "p7",
          "start": 4169,
          "end": 4254,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
        },
        "refutation": {
          "segment_id": "p7",
          "start": 3777,
          "end": 4041,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
        },
        "declaration": {
          "segment_id": "p7",
          "start": 3777,
          "end": 4041,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
        },
        "implementation": {
          "segment_id": "p7",
          "start": 4055,
          "end": 4167,
          "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
          "match": "normalized_exact",
          "text_view": "reading_order",
          "text_view_sha256": "d930a3fa4f5ea18acca37371d8fa8177fb54a941c6a90c241428f78891767b08"
        }
      },
      "semantic_review": {
        "index": 2,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "confirmed",
        "refutation": "explicit_permission",
        "reason": "p7 specifically introduces gradient-based optimization despite the earlier model-ignorance assumption, supporting a gradient-access exception for these comparison implementations. It does not authorize every knowledge type or establish raw-query access, identical optimization/evaluation records, or TopicAttack access to victim internals."
      }
    }
  ],
  "document_sha256": "8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7",
  "schema_version": 3,
  "applicability": "in_scope",
  "scope": "The supplied paper describes construction from benign content and an injected objective, with no demonstrated forbidden information flow. Exact-query delivery remains unverified; victim-model access is explicitly introduced for a separate gradient-based comparison.",
  "review_status": "model_reviewed_not_human_verified",
  "evidence_scope": "listed_claims_document_only",
  "notes": [
    "Only supplied paper text was available; no static code, saved requests, or runtime traces were supplied.",
    "Reported attack success and defense failures establish security outcomes, not violations of attacker knowledge restrictions.",
    "Exact construction-input bindings and possible original-query exposure remain unanswered.",
    "The relationship between gradient-optimization instances and evaluated instances remains unspecified.",
    "Supplied procedures support construction findings; reported attack success does not establish a knowledge-budget violation or the causal impact of forbidden access."
  ],
  "unresolved_questions": [
    "What exact values populate {data} and {topic} in the auxiliary-model requests for chatbot and agent evaluations?",
    "Do any actual TopicAttack construction requests include original user instructions beyond the permitted benign content?",
    "Which instances are used for gradient optimization, and how do they relate to the evaluated instances?"
  ],
  "verdict": "insufficient_evidence",
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "claim_result_counts": {
    "unresolved": 1,
    "refuted": 2
  },
  "input_mode": "document_only",
  "prompt_sha256": "a2c05a361fc0a14027ff29bfb1bf05e6678aec9369c63dd16cc4f9349ec8ce76",
  "duration_seconds": 67.525,
  "cohort": "previously_suspected_control",
  "expected": null,
  "expected_basis": "pending_independent_adjudication",
  "comparison_note": "A suspected false positive is not assumed clean; resolve against source evidence.",
  "matches_gold": null
}
```

### 3. AgentDojo information\-budget audit

论文 ID：agentdojo  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 26, "characters": 91997, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://agentdojo\.spylab\.ai", "https://github\.com/ethz\-spylab/agentdojo", "https://www\-cdn\.anthropic", "https://docs\.anthropic\.com/en/docs/tool\-use", "https://cohere\.com/command", "https://x\.com/goodside/status/1569128808308957185", "https://cookbook\.openai\.com/examples/", "https://www\.youtube\.com/watch?v=", "https://lakeraai\.github\.io/chainguard/", "https://github\.com/tiangolo/fastapi", "https://simonwillison", "https://simonwillison\.net/2023/Apr/25/dual\-llm\-pattern/", "https://drive\.google\.com/file/d/16nhDqSTRVac\_GbcC3\-9WMjVaJZfmcwLO/", "https://chatgpt\.com/share/"\], "sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913"\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 4\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "agentdojo_claim_1",
    "source_group": "paper_text",
    "description": "This is derived placement information, not evidence that raw user instructions reach a payload LLM.",
    "scope": {
      "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
      "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "attack placement helper",
      "phase": "construction",
      "source": "user-task ground-truth tool sequence",
      "representation": "task-specific injection candidate locations",
      "operation": "select placeholders in outputs of tools required for the task"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "attack placement helper",
          "phase": "construction",
          "source": "user-task ground-truth tool sequence",
          "representation": "task-specific injection candidate locations",
          "operation": "select placeholders in outputs of tools required for the task"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attack placement helper",
          "phase": "construction",
          "source": "user-task ground-truth tool sequence",
          "representation": "task-specific injection candidate locations",
          "operation": "select placeholders in outputs of tools required for the task"
        },
        "status": "present",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 1759, \"match\": \"normalized_exact\", \"segment_id\": \"p16\", \"start\": 1608, \"text_view\": \"primary\", \"text_view_sha256\": \"802ea754233c52acc250001436b16af05cb8aae4fe15d0a82c6631790ff6e329\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Task-plan access: attack placement uses the evaluated task’s ground-truth tool sequence.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "other",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The specific design expressly supports task-aware placement using this derived plan.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reason": "The paper’s illustrative attack passes the current task ID to the placement helper.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 190, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 147, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
      },
      "refutation": {
        "basis": "explicit_permission",
        "reason": "Task-plan-assisted placement is an intended capability.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
      }
    },
    "claim_result": "refuted",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 2563,
        "end": 2636,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
      },
      "delivery": {
        "segment_id": "p17",
        "start": 147,
        "end": 190,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
      },
      "refutation": {
        "segment_id": "p4",
        "start": 2563,
        "end": 2636,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
      },
      "declaration": {
        "segment_id": "p4",
        "start": 2563,
        "end": 2636,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
      },
      "implementation": {
        "segment_id": "p16",
        "start": 1608,
        "end": 1759,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "802ea754233c52acc250001436b16af05cb8aae4fe15d0a82c6631790ff6e329"
      }
    },
    "semantic_review": {
      "index": 0,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "confirmed",
      "refutation": "explicit_permission",
      "reason": "p4 and p16 expressly support ground-truth-assisted placement; p17 delivers task-specific candidates to the attack constructor. This confirms derived placement access, not raw-query access or its causal impact."
    }
  },
  {
    "id": "agentdojo_claim_2",
    "source_group": "paper_text",
    "description": "Object access alone does not establish full-query delivery to a payload generator or an information-budget violation.",
    "scope": {
      "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
      "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "attack constructor",
      "phase": "construction",
      "source": "evaluated user-task object",
      "representation": "potential full user prompt",
      "operation": "potentially read task instructions while constructing an injection",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_is_not_attacker_knowledge_constraint",
    "matching_rules": [],
    "matching_observations": [
      {
        "edge": {
          "role": "attack constructor",
          "phase": "construction",
          "source": "evaluated user-task object",
          "representation": "potential full user prompt",
          "operation": "potentially read task instructions while constructing an injection",
          "query_form": "full_query"
        },
        "status": "possible",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 76, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 0, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Raw-query access: the attack interface receives a user-task object, but payload use of its full prompt is unproven.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "policy_kind": "unspecified",
        "status": "uncertain",
        "reason": "No specific full-query exclusion or grant is supplied.",
        "reference": ""
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "possible_path",
        "task_relation": "same_evaluated_instance",
        "reason": "The interface exposes a task object, while the shown body uses its ID rather than raw prompt text.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 76, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 0, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
      },
      "refutation": {
        "basis": "none",
        "reason": "The illustrative body does not establish an exclusion across evaluated attacks.",
        "reference": ""
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [],
    "locators": {
      "delivery": {
        "segment_id": "p17",
        "start": 0,
        "end": 76,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
      },
      "implementation": {
        "segment_id": "p17",
        "start": 0,
        "end": 76,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
      }
    },
    "semantic_review": {
      "index": 1,
      "supported": true,
      "policy_kind": "unspecified",
      "policy_application": "uncertain",
      "delivery": "unresolved",
      "refutation": "none",
      "reason": "p17 passes a user-task object but only shows ID use. Full-prompt use by evaluated constructors remains unproven, and no specific full-query budget is supplied. Neither a mismatch nor exclusion is established."
    }
  },
  {
    "id": "agentdojo_claim_3",
    "source_group": "paper_text",
    "description": "The reported small performance effect does not determine consistency; the relevant access is permitted.",
    "scope": {
      "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
      "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "Important message attack constructor",
      "phase": "construction",
      "source": "victim user and model names",
      "representation": "substituted payload placeholders",
      "operation": "address the victim using known identities"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "Important message attack constructor",
          "phase": "construction",
          "source": "victim user and model names",
          "representation": "substituted payload placeholders",
          "operation": "address the victim using known identities"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2698, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2604, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "Important message attack constructor",
          "phase": "construction",
          "source": "victim user and model names",
          "representation": "substituted payload placeholders",
          "operation": "address the victim using known identities"
        },
        "status": "present",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 1656, \"match\": \"normalized_exact\", \"segment_id\": \"p19\", \"start\": 1547, \"text_view\": \"primary\", \"text_view_sha256\": \"45bd2286be8e57e1f6f1e83a6955f3b3b04404cb0cacc8256374953712d29e9a\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Identity access: baseline payloads incorporate the user and model names.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "user_identity",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The framework permits stronger knowledge settings, and the evaluated identity-aware arm is expressly described.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2529, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2424, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reason": "The evaluation description explicitly identifies identity use in the attack prompt.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2606, \"match\": \"normalized_exact\", \"segment_id\": \"p8\", \"start\": 2579, \"text_view\": \"primary\", \"text_view_sha256\": \"1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049\"}"
      },
      "refutation": {
        "basis": "explicit_permission",
        "reason": "Identity-aware attackers are an explicitly supported setting.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2655, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2604, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
      }
    },
    "claim_result": "refuted",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p6",
        "start": 2424,
        "end": 2529,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "delivery": {
        "segment_id": "p8",
        "start": 2579,
        "end": 2606,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
      },
      "refutation": {
        "segment_id": "p6",
        "start": 2604,
        "end": 2655,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "declaration": {
        "segment_id": "p6",
        "start": 2604,
        "end": 2698,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "implementation": {
        "segment_id": "p19",
        "start": 1547,
        "end": 1656,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "45bd2286be8e57e1f6f1e83a6955f3b3b04404cb0cacc8256374953712d29e9a"
      }
    },
    "semantic_review": {
      "index": 2,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "confirmed",
      "refutation": "explicit_permission",
      "reason": "p6 explicitly permits identity-aware attacks; p8 and p19 establish user/model name substitution in evaluated payloads. The reported performance effect is separate from this permitted access."
    }
  },
  {
    "id": "agentdojo_claim_4",
    "source_group": "paper_text",
    "description": "This establishes outcome-conditioned selection, not raw evaluation-query delivery to a payload LLM.",
    "scope": {
      "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
      "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "adaptive Max selector",
      "phase": "evaluation-time attack selection",
      "source": "candidate attack success on a security case",
      "representation": "per-case best-attack selection",
      "operation": "select the most effective candidate prompt"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Per-case selection: Max uses comparative attack effectiveness to select a prompt for each task pair.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "other",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "uncertain",
        "reason": "The specific adaptive reporting arm expressly permits per-case best-attack selection.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3697, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3591, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reason": "Selection is described for the evaluated cases; its implementation mechanism is not supplied.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3099, \"match\": \"normalized_exact\", \"segment_id\": \"p8\", \"start\": 3038, \"text_view\": \"primary\", \"text_view_sha256\": \"1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049\"}"
      },
      "refutation": {
        "basis": "none",
        "reason": "The reported aggregate explicitly uses this success criterion.",
        "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3589, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3505, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [
      "semantic_review_disagrees_with_proposed_assessment"
    ],
    "locators": {
      "policy_scope": {
        "segment_id": "p6",
        "start": 3591,
        "end": 3697,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "delivery": {
        "segment_id": "p8",
        "start": 3038,
        "end": 3099,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
      },
      "refutation": {
        "segment_id": "p6",
        "start": 3505,
        "end": 3589,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "declaration": {
        "segment_id": "p6",
        "start": 3591,
        "end": 3697,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
      },
      "implementation": {
        "segment_id": "p8",
        "start": 3008,
        "end": 3099,
        "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
      }
    },
    "semantic_review": {
      "index": 3,
      "supported": false,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "unresolved",
      "refutation": "explicit_permission",
      "reason": "p6 explicitly permits per-case any-success reporting, and p8 describes Max accordingly. These establish the permitted selection criterion, but do not establish outcome information reaching an executing attacker selector rather than an evaluator."
    }
  }
]
```

#### 备注

```json
[
  "Evidence is limited to supplied paper text and embedded illustrative code; no repository, runtime traces, or saved requests were supplied.",
  "No explicit applicable attacker-knowledge exclusion was identified in the supplied text.",
  "Full-query use by evaluated attack constructors remains unanswered.",
  "Max's implementation and the recipient of per-case outcome information remain unresolved.",
  "Supplied text and illustrative code establish no prohibited information flow; they do not establish implementation-wide absence or causal behavioral impact."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "agentdojo",
  "title": "AgentDojo information-budget audit",
  "source": "https://papers.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf",
  "status": "completed",
  "has_confirmed_inconsistency": false,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 26,
      "characters": 91997,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://agentdojo.spylab.ai",
        "https://github.com/ethz-spylab/agentdojo",
        "https://www-cdn.anthropic",
        "https://docs.anthropic.com/en/docs/tool-use",
        "https://cohere.com/command",
        "https://x.com/goodside/status/1569128808308957185",
        "https://cookbook.openai.com/examples/",
        "https://www.youtube.com/watch?v=",
        "https://lakeraai.github.io/chainguard/",
        "https://github.com/tiangolo/fastapi",
        "https://simonwillison",
        "https://simonwillison.net/2023/Apr/25/dual-llm-pattern/",
        "https://drive.google.com/file/d/16nhDqSTRVac_GbcC3-9WMjVaJZfmcwLO/",
        "https://chatgpt.com/share/"
      ],
      "sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913"
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 4
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
      "reason": "unresolved_checks"
    }
  ],
  "evidence": [
    {
      "id": "agentdojo_claim_1",
      "source_group": "paper_text",
      "description": "This is derived placement information, not evidence that raw user instructions reach a payload LLM.",
      "scope": {
        "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "attack placement helper",
        "phase": "construction",
        "source": "user-task ground-truth tool sequence",
        "representation": "task-specific injection candidate locations",
        "operation": "select placeholders in outputs of tools required for the task"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "attack placement helper",
            "phase": "construction",
            "source": "user-task ground-truth tool sequence",
            "representation": "task-specific injection candidate locations",
            "operation": "select placeholders in outputs of tools required for the task"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attack placement helper",
            "phase": "construction",
            "source": "user-task ground-truth tool sequence",
            "representation": "task-specific injection candidate locations",
            "operation": "select placeholders in outputs of tools required for the task"
          },
          "status": "present",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 1759, \"match\": \"normalized_exact\", \"segment_id\": \"p16\", \"start\": 1608, \"text_view\": \"primary\", \"text_view_sha256\": \"802ea754233c52acc250001436b16af05cb8aae4fe15d0a82c6631790ff6e329\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Task-plan access: attack placement uses the evaluated task’s ground-truth tool sequence.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "other",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The specific design expressly supports task-aware placement using this derived plan.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reason": "The paper’s illustrative attack passes the current task ID to the placement helper.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 190, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 147, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
        },
        "refutation": {
          "basis": "explicit_permission",
          "reason": "Task-plan-assisted placement is an intended capability.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2636, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2563, \"text_view\": \"primary\", \"text_view_sha256\": \"c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d\"}"
        }
      },
      "claim_result": "refuted",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 2563,
          "end": 2636,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
        },
        "delivery": {
          "segment_id": "p17",
          "start": 147,
          "end": 190,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
        },
        "refutation": {
          "segment_id": "p4",
          "start": 2563,
          "end": 2636,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
        },
        "declaration": {
          "segment_id": "p4",
          "start": 2563,
          "end": 2636,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "c22f7fbf597461eddaf68e416422ed3a6b78377f0bfc033baa251962914b489d"
        },
        "implementation": {
          "segment_id": "p16",
          "start": 1608,
          "end": 1759,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "802ea754233c52acc250001436b16af05cb8aae4fe15d0a82c6631790ff6e329"
        }
      },
      "semantic_review": {
        "index": 0,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "confirmed",
        "refutation": "explicit_permission",
        "reason": "p4 and p16 expressly support ground-truth-assisted placement; p17 delivers task-specific candidates to the attack constructor. This confirms derived placement access, not raw-query access or its causal impact."
      }
    },
    {
      "id": "agentdojo_claim_2",
      "source_group": "paper_text",
      "description": "Object access alone does not establish full-query delivery to a payload generator or an information-budget violation.",
      "scope": {
        "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "attack constructor",
        "phase": "construction",
        "source": "evaluated user-task object",
        "representation": "potential full user prompt",
        "operation": "potentially read task instructions while constructing an injection",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_is_not_attacker_knowledge_constraint",
      "matching_rules": [],
      "matching_observations": [
        {
          "edge": {
            "role": "attack constructor",
            "phase": "construction",
            "source": "evaluated user-task object",
            "representation": "potential full user prompt",
            "operation": "potentially read task instructions while constructing an injection",
            "query_form": "full_query"
          },
          "status": "possible",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 76, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 0, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Raw-query access: the attack interface receives a user-task object, but payload use of its full prompt is unproven.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "policy_kind": "unspecified",
          "status": "uncertain",
          "reason": "No specific full-query exclusion or grant is supplied.",
          "reference": ""
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "possible_path",
          "task_relation": "same_evaluated_instance",
          "reason": "The interface exposes a task object, while the shown body uses its ID rather than raw prompt text.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 76, \"match\": \"normalized_exact\", \"segment_id\": \"p17\", \"start\": 0, \"text_view\": \"primary\", \"text_view_sha256\": \"f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810\"}"
        },
        "refutation": {
          "basis": "none",
          "reason": "The illustrative body does not establish an exclusion across evaluated attacks.",
          "reference": ""
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [],
      "locators": {
        "delivery": {
          "segment_id": "p17",
          "start": 0,
          "end": 76,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
        },
        "implementation": {
          "segment_id": "p17",
          "start": 0,
          "end": 76,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "f4f2852c86ace0001a9143c60e5652ec6315fa4272cb87fad34691109d460810"
        }
      },
      "semantic_review": {
        "index": 1,
        "supported": true,
        "policy_kind": "unspecified",
        "policy_application": "uncertain",
        "delivery": "unresolved",
        "refutation": "none",
        "reason": "p17 passes a user-task object but only shows ID use. Full-prompt use by evaluated constructors remains unproven, and no specific full-query budget is supplied. Neither a mismatch nor exclusion is established."
      }
    },
    {
      "id": "agentdojo_claim_3",
      "source_group": "paper_text",
      "description": "The reported small performance effect does not determine consistency; the relevant access is permitted.",
      "scope": {
        "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "Important message attack constructor",
        "phase": "construction",
        "source": "victim user and model names",
        "representation": "substituted payload placeholders",
        "operation": "address the victim using known identities"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "Important message attack constructor",
            "phase": "construction",
            "source": "victim user and model names",
            "representation": "substituted payload placeholders",
            "operation": "address the victim using known identities"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2698, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2604, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "Important message attack constructor",
            "phase": "construction",
            "source": "victim user and model names",
            "representation": "substituted payload placeholders",
            "operation": "address the victim using known identities"
          },
          "status": "present",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 1656, \"match\": \"normalized_exact\", \"segment_id\": \"p19\", \"start\": 1547, \"text_view\": \"primary\", \"text_view_sha256\": \"45bd2286be8e57e1f6f1e83a6955f3b3b04404cb0cacc8256374953712d29e9a\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Identity access: baseline payloads incorporate the user and model names.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "user_identity",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The framework permits stronger knowledge settings, and the evaluated identity-aware arm is expressly described.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2529, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2424, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reason": "The evaluation description explicitly identifies identity use in the attack prompt.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2606, \"match\": \"normalized_exact\", \"segment_id\": \"p8\", \"start\": 2579, \"text_view\": \"primary\", \"text_view_sha256\": \"1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049\"}"
        },
        "refutation": {
          "basis": "explicit_permission",
          "reason": "Identity-aware attackers are an explicitly supported setting.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 2655, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 2604, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
        }
      },
      "claim_result": "refuted",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p6",
          "start": 2424,
          "end": 2529,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "delivery": {
          "segment_id": "p8",
          "start": 2579,
          "end": 2606,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
        },
        "refutation": {
          "segment_id": "p6",
          "start": 2604,
          "end": 2655,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "declaration": {
          "segment_id": "p6",
          "start": 2604,
          "end": 2698,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "implementation": {
          "segment_id": "p19",
          "start": 1547,
          "end": 1656,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "45bd2286be8e57e1f6f1e83a6955f3b3b04404cb0cacc8256374953712d29e9a"
        }
      },
      "semantic_review": {
        "index": 2,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "confirmed",
        "refutation": "explicit_permission",
        "reason": "p6 explicitly permits identity-aware attacks; p8 and p19 establish user/model name substitution in evaluated payloads. The reported performance effect is separate from this permitted access."
      }
    },
    {
      "id": "agentdojo_claim_4",
      "source_group": "paper_text",
      "description": "This establishes outcome-conditioned selection, not raw evaluation-query delivery to a payload LLM.",
      "scope": {
        "paper_version": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
        "experiment_arm": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "adaptive Max selector",
        "phase": "evaluation-time attack selection",
        "source": "candidate attack success on a security case",
        "representation": "per-case best-attack selection",
        "operation": "select the most effective candidate prompt"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Per-case selection: Max uses comparative attack effectiveness to select a prompt for each task pair.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "other",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "uncertain",
          "reason": "The specific adaptive reporting arm expressly permits per-case best-attack selection.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3697, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3591, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reason": "Selection is described for the evaluated cases; its implementation mechanism is not supplied.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3099, \"match\": \"normalized_exact\", \"segment_id\": \"p8\", \"start\": 3038, \"text_view\": \"primary\", \"text_view_sha256\": \"1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049\"}"
        },
        "refutation": {
          "basis": "none",
          "reason": "The reported aggregate explicitly uses this success criterion.",
          "reference": "{\"document_sha256\": \"26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913\", \"end\": 3589, \"match\": \"normalized_exact\", \"segment_id\": \"p6\", \"start\": 3505, \"text_view\": \"primary\", \"text_view_sha256\": \"be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d\"}"
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [
        "semantic_review_disagrees_with_proposed_assessment"
      ],
      "locators": {
        "policy_scope": {
          "segment_id": "p6",
          "start": 3591,
          "end": 3697,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "delivery": {
          "segment_id": "p8",
          "start": 3038,
          "end": 3099,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
        },
        "refutation": {
          "segment_id": "p6",
          "start": 3505,
          "end": 3589,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "declaration": {
          "segment_id": "p6",
          "start": 3591,
          "end": 3697,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "be1a9c5e4a8f142a2bdd7301e8471d31168da5d3a03785e6ea4eccd0f1566e2d"
        },
        "implementation": {
          "segment_id": "p8",
          "start": 3008,
          "end": 3099,
          "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "1fc028cb29d8c53f3600f4ce0e6b399075f523c3b0af1341a44e269be010d049"
        }
      },
      "semantic_review": {
        "index": 3,
        "supported": false,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "unresolved",
        "refutation": "explicit_permission",
        "reason": "p6 explicitly permits per-case any-success reporting, and p8 describes Max accordingly. These establish the permitted selection criterion, but do not establish outcome information reaching an executing attacker selector rather than an evaluator."
      }
    }
  ],
  "document_sha256": "26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913",
  "schema_version": 3,
  "applicability": "in_scope",
  "scope": "The supplied paper describes task-aware injection placement, identity-conditioned payloads, and adaptive attack selection. These accesses are explicitly supported; no prohibited attacker information flow is established. Raw user-query delivery remains unresolved.",
  "review_status": "model_reviewed_not_human_verified",
  "evidence_scope": "listed_claims_document_only",
  "notes": [
    "Evidence is limited to supplied paper text and embedded illustrative code; no repository, runtime traces, or saved requests were supplied.",
    "No explicit applicable attacker-knowledge exclusion was identified in the supplied text.",
    "Full-query use by evaluated attack constructors remains unanswered.",
    "Max's implementation and the recipient of per-case outcome information remain unresolved.",
    "Supplied text and illustrative code establish no prohibited information flow; they do not establish implementation-wide absence or causal behavioral impact."
  ],
  "unresolved_questions": [
    "Do evaluated attack implementations read user_task.PROMPT or other task fields beyond the ID and placement candidates?",
    "What mechanism implements Max selection: post hoc aggregation, online feedback, or a separate selection procedure?"
  ],
  "verdict": "insufficient_evidence",
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "claim_result_counts": {
    "refuted": 2,
    "unresolved": 2
  },
  "input_mode": "document_only",
  "prompt_sha256": "a2c05a361fc0a14027ff29bfb1bf05e6678aec9369c63dd16cc4f9349ec8ce76",
  "duration_seconds": 68.336,
  "cohort": "previously_suspected_control",
  "expected": null,
  "expected_basis": "pending_independent_adjudication",
  "comparison_note": "A suspected false positive is not assumed clean; resolve against source evidence.",
  "matches_gold": null
}
```

### 4. ASB information\-budget audit

论文 ID：asb  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 36, "characters": 187606, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://arxiv\.org/abs/", "https://artificialanalysis\.ai/", "https://www\.anthropic\.com/news/", "https://arxiv\.org/abs/2211\.14719", "https://www", "https://rapidapi\.com/hub", "https://www\.alignmentforum\.org/posts/pNcFYZnPdXyL2RfgA/", "https://aclanthology\.org/2024", "https://aclanthology\.org/2025\.coling\-main\.37/", "https://arxiv\.org/abs/2307", "https://learnprompting\.org/docs/", "https://learnprompting\.org/docs/prompt\_", "https://www\.usenix\.org/conference/usenixsecurity24/", "https://arxiv\.org/abs/2311\.10813", "https://arxiv\.org/abs/2403\.16971", "https://chatgpt\.com/gpts", "https://openai\.com/index/", "https://owasp\.org/www\-", "https://arxiv\.org/abs/2305\.15334", "https://arxiv", "https://openreview\.net/forum?id=dHng2O0Jjr", "https://research\.nccgroup\.com/2022/", "https://arxiv\.org/abs/2409\.07429", "https://simonwillison\.net/", "https://simonwillison", "https://arxiv\.org/abs/2406\.14598", "https://arxiv\.org/abs/2502\.14662", "https://arxiv\.org/abs/2402", "https://aclanthology\.org/2024\.findings\-acl\.624", "https://openreview\.net/forum?id=8FgdMHbW27", "https://python\.langchain\.com/docs/integrations/vectorstores/", "https://platform\.openai\.com/docs/api\-reference/chat/create", "https://github\.com/agiresearch/ASB/blob/main/aios/llm\_core/llm\_", "https://github\.com/agiresearch/ASB/blob/main/pyopenagi/agents/react\_", "https://github\.com/agiresearch/ASB/blob/main/data/all\_normal\_tools", "https://github\.com/agiresearch/ASB/blob/main/data/all\_attack\_tools", "https://github\.com/agiresearch/ASB/blob/main/pyopenagi/tools/"\], "sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9"\} |
| extraction | 已完成 | \{"stage": "extraction", "status": "completed", "applicability": "in\_scope", "flow\_count": 2\} |
| semantic\_review | 已完成 | \{"stage": "semantic\_review", "status": "completed", "applicability": "in\_scope"\} |
| citation\_validation\_and\_decision | 已完成 | \{"stage": "citation\_validation\_and\_decision", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |

#### 证据

```json
[
  {
    "id": "asb_claim_1",
    "source_group": "paper_text",
    "description": "This is a described task-text construction boundary, rather than an inference from an evaluation equation. It does not establish access to the particular evaluated tasks.",
    "scope": {
      "paper_version": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
      "experiment_arm": "Paper-text audit of query access during trigger construction and database access during memory poisoning. The supplied procedures establish no prohibited information flow.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "PoT attacker and trigger-generation LLM",
      "phase": "trigger construction",
      "source": "attacker-held tasks",
      "representation": "task texts in a trigger-generation prompt",
      "operation": "supply tasks to GPT-4o to generate an appendable phrase",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "PoT attacker and trigger-generation LLM",
          "phase": "trigger construction",
          "source": "attacker-held tasks",
          "representation": "task texts in a trigger-generation prompt",
          "operation": "supply tasks to GPT-4o to generate an appendable phrase",
          "query_form": "full_query"
        },
        "permission": "allow",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "PoT attacker and trigger-generation LLM",
          "phase": "trigger construction",
          "source": "attacker-held tasks",
          "representation": "task texts in a trigger-generation prompt",
          "operation": "supply tasks to GPT-4o to generate an appendable phrase",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 834, \"match\": \"normalized_exact\", \"segment_id\": \"p28\", \"start\": 761, \"text_view\": \"primary\", \"text_view_sha256\": \"0789935a9f84964002dc99c9d4df4158af8a05d4932323c1dc76b2b616663bf0\"}"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Task-conditioned trigger generation: the attacker supplies task text to GPT-4o when constructing phrase triggers; evaluation-task inclusion is unresolved.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "applicable",
        "reason": "The user-prompt access grant explicitly concerns the backdoor attacker and permits the task access implicated here.",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "unknown",
        "reason": "The paper supplies a task-conditioned generation prompt and describes using it, but does not identify which tasks populate that prompt.",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 5680, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 5611, \"text_view\": \"primary\", \"text_view_sha256\": \"a103d0ac78f553bdffa6ea51c526d0420c68cb043554710fe645e5e6bacdfc8d\"}"
      },
      "refutation": {
        "basis": "explicit_permission",
        "reason": "Task access is explicitly permitted for this attack arm.",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
      }
    },
    "claim_result": "refuted",
    "citation_errors": [],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 2892,
        "end": 2958,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
      },
      "delivery": {
        "segment_id": "p7",
        "start": 5611,
        "end": 5680,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "a103d0ac78f553bdffa6ea51c526d0420c68cb043554710fe645e5e6bacdfc8d"
      },
      "refutation": {
        "segment_id": "p4",
        "start": 2892,
        "end": 2958,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
      },
      "declaration": {
        "segment_id": "p4",
        "start": 2892,
        "end": 2958,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
      },
      "implementation": {
        "segment_id": "p28",
        "start": 761,
        "end": 834,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "0789935a9f84964002dc99c9d4df4158af8a05d4932323c1dc76b2b616663bf0"
      }
    },
    "semantic_review": {
      "index": 0,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "confirmed",
      "refutation": "explicit_permission",
      "reason": "p7 and p28 describe task texts reaching GPT-4o for trigger construction. p4 explicitly permits PoT attacker access to user prompts, so this establishes no prohibited knowledge flow. Whether those texts include evaluated tasks remains unresolved; p26 separates demonstrations from testing tasks only."
    }
  },
  {
    "id": "asb_claim_2",
    "source_group": "paper_text",
    "description": "The procedural counterevidence resolves the direct-write inference. It does not independently prove that every implementation respects the black-box restriction.",
    "scope": {
      "paper_version": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
      "experiment_arm": "Paper-text audit of query access during trigger construction and database access during memory poisoning. The supplied procedures establish no prohibited information flow.",
      "artifact_revision": "supplied document only; no execution artifact",
      "configuration": "v3 typed policy, applicability and delivery review"
    },
    "target": {
      "role": "memory-poisoning attacker",
      "phase": "poison construction and insertion",
      "source": "RAG database and embedder internals",
      "representation": "internal database structure or embedder details",
      "operation": "use internal access to construct or insert poisoned records"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Direct database-write suspicion: providing a poisoned database might imply white-box access, but the experimental procedure describes poisoning through agent execution.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "resource_metadata",
      "policy_application": {
        "policy_kind": "attacker_knowledge_constraint",
        "status": "uncertain",
        "reason": "The restriction applies specifically to the memory-poisoning attacker and excludes the internal access named in this suspicion.",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 3464, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 3400, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "possible_path",
        "task_relation": "unknown",
        "reason": "No supplied source-to-attacker boundary delivers database structure or embedder internals.",
        "reference": ""
      },
      "refutation": {
        "basis": "none",
        "reason": "The described insertion route is an agent saving an attack-induced plan, which counters the inference that the poisoned-database formalization requires direct internal access.",
        "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 4053, \"match\": \"normalized_exact\", \"segment_id\": \"p18\", \"start\": 3965, \"text_view\": \"primary\", \"text_view_sha256\": \"00d0640400c9b3e75847d58fb3e2b8283505b5557e0fbfa6910f3fe15026c218\"}"
      }
    },
    "claim_result": "unresolved",
    "citation_errors": [
      "semantic_review_disagrees_with_proposed_assessment"
    ],
    "locators": {
      "policy_scope": {
        "segment_id": "p4",
        "start": 3400,
        "end": 3464,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
      },
      "refutation": {
        "segment_id": "p18",
        "start": 3965,
        "end": 4053,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "00d0640400c9b3e75847d58fb3e2b8283505b5557e0fbfa6910f3fe15026c218"
      },
      "declaration": {
        "segment_id": "p3",
        "start": 1750,
        "end": 1788,
        "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "match": "normalized_exact",
        "text_view": "primary",
        "text_view_sha256": "7a6ef2ebadd134976eee53d08f0e196f868956bf3e15b5457753872ffe58cdae"
      }
    },
    "semantic_review": {
      "index": 1,
      "supported": true,
      "policy_kind": "attacker_knowledge_constraint",
      "policy_application": "applicable",
      "delivery": "excluded",
      "refutation": "excluded_delivery",
      "reason": "The black-box restriction in p3–p4 applies to memory poisoning. p6, p18 and p26 affirmatively describe DPI-induced plans saved by the agent, countering the inference that providing a poisoned database requires direct internal access. Exclusion concerns that claimed insertion route, not every possible implementation."
    }
  }
]
```

#### 备注

```json
[
  "Only supplied paper text was examined; no static code, saved requests, or runtime records were supplied.",
  "Distinct PoT demonstration and testing tasks do not establish that trigger-generation tasks were also distinct.",
  "Reported attack success and defense failures are security outcomes, not evidence of inconsistent attacker knowledge.",
  "Specific questions about trigger-generation task identities and poisoned-memory source tasks versus evaluation tasks remain unanswered.",
  "Only supplied paper text supports these findings; no implementation or runtime evidence was supplied.",
  "Construction procedures do not establish causal effects of task overlap. Reported attack success and defense failures are security outcomes, not knowledge-budget violations."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "asb",
  "title": "ASB information-budget audit",
  "source": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf",
  "status": "completed",
  "has_confirmed_inconsistency": false,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 36,
      "characters": 187606,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://arxiv.org/abs/",
        "https://artificialanalysis.ai/",
        "https://www.anthropic.com/news/",
        "https://arxiv.org/abs/2211.14719",
        "https://www",
        "https://rapidapi.com/hub",
        "https://www.alignmentforum.org/posts/pNcFYZnPdXyL2RfgA/",
        "https://aclanthology.org/2024",
        "https://aclanthology.org/2025.coling-main.37/",
        "https://arxiv.org/abs/2307",
        "https://learnprompting.org/docs/",
        "https://learnprompting.org/docs/prompt_",
        "https://www.usenix.org/conference/usenixsecurity24/",
        "https://arxiv.org/abs/2311.10813",
        "https://arxiv.org/abs/2403.16971",
        "https://chatgpt.com/gpts",
        "https://openai.com/index/",
        "https://owasp.org/www-",
        "https://arxiv.org/abs/2305.15334",
        "https://arxiv",
        "https://openreview.net/forum?id=dHng2O0Jjr",
        "https://research.nccgroup.com/2022/",
        "https://arxiv.org/abs/2409.07429",
        "https://simonwillison.net/",
        "https://simonwillison",
        "https://arxiv.org/abs/2406.14598",
        "https://arxiv.org/abs/2502.14662",
        "https://arxiv.org/abs/2402",
        "https://aclanthology.org/2024.findings-acl.624",
        "https://openreview.net/forum?id=8FgdMHbW27",
        "https://python.langchain.com/docs/integrations/vectorstores/",
        "https://platform.openai.com/docs/api-reference/chat/create",
        "https://github.com/agiresearch/ASB/blob/main/aios/llm_core/llm_",
        "https://github.com/agiresearch/ASB/blob/main/pyopenagi/agents/react_",
        "https://github.com/agiresearch/ASB/blob/main/data/all_normal_tools",
        "https://github.com/agiresearch/ASB/blob/main/data/all_attack_tools",
        "https://github.com/agiresearch/ASB/blob/main/pyopenagi/tools/"
      ],
      "sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9"
    },
    {
      "stage": "extraction",
      "status": "completed",
      "applicability": "in_scope",
      "flow_count": 2
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
      "reason": "unresolved_checks"
    }
  ],
  "evidence": [
    {
      "id": "asb_claim_1",
      "source_group": "paper_text",
      "description": "This is a described task-text construction boundary, rather than an inference from an evaluation equation. It does not establish access to the particular evaluated tasks.",
      "scope": {
        "paper_version": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "experiment_arm": "Paper-text audit of query access during trigger construction and database access during memory poisoning. The supplied procedures establish no prohibited information flow.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "PoT attacker and trigger-generation LLM",
        "phase": "trigger construction",
        "source": "attacker-held tasks",
        "representation": "task texts in a trigger-generation prompt",
        "operation": "supply tasks to GPT-4o to generate an appendable phrase",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "PoT attacker and trigger-generation LLM",
            "phase": "trigger construction",
            "source": "attacker-held tasks",
            "representation": "task texts in a trigger-generation prompt",
            "operation": "supply tasks to GPT-4o to generate an appendable phrase",
            "query_form": "full_query"
          },
          "permission": "allow",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "PoT attacker and trigger-generation LLM",
            "phase": "trigger construction",
            "source": "attacker-held tasks",
            "representation": "task texts in a trigger-generation prompt",
            "operation": "supply tasks to GPT-4o to generate an appendable phrase",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 834, \"match\": \"normalized_exact\", \"segment_id\": \"p28\", \"start\": 761, \"text_view\": \"primary\", \"text_view_sha256\": \"0789935a9f84964002dc99c9d4df4158af8a05d4932323c1dc76b2b616663bf0\"}"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Task-conditioned trigger generation: the attacker supplies task text to GPT-4o when constructing phrase triggers; evaluation-task inclusion is unresolved.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "applicable",
          "reason": "The user-prompt access grant explicitly concerns the backdoor attacker and permits the task access implicated here.",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "unknown",
          "reason": "The paper supplies a task-conditioned generation prompt and describes using it, but does not identify which tasks populate that prompt.",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 5680, \"match\": \"normalized_exact\", \"segment_id\": \"p7\", \"start\": 5611, \"text_view\": \"primary\", \"text_view_sha256\": \"a103d0ac78f553bdffa6ea51c526d0420c68cb043554710fe645e5e6bacdfc8d\"}"
        },
        "refutation": {
          "basis": "explicit_permission",
          "reason": "Task access is explicitly permitted for this attack arm.",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 2958, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 2892, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
        }
      },
      "claim_result": "refuted",
      "citation_errors": [],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 2892,
          "end": 2958,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
        },
        "delivery": {
          "segment_id": "p7",
          "start": 5611,
          "end": 5680,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "a103d0ac78f553bdffa6ea51c526d0420c68cb043554710fe645e5e6bacdfc8d"
        },
        "refutation": {
          "segment_id": "p4",
          "start": 2892,
          "end": 2958,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
        },
        "declaration": {
          "segment_id": "p4",
          "start": 2892,
          "end": 2958,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
        },
        "implementation": {
          "segment_id": "p28",
          "start": 761,
          "end": 834,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "0789935a9f84964002dc99c9d4df4158af8a05d4932323c1dc76b2b616663bf0"
        }
      },
      "semantic_review": {
        "index": 0,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "confirmed",
        "refutation": "explicit_permission",
        "reason": "p7 and p28 describe task texts reaching GPT-4o for trigger construction. p4 explicitly permits PoT attacker access to user prompts, so this establishes no prohibited knowledge flow. Whether those texts include evaluated tasks remains unresolved; p26 separates demonstrations from testing tasks only."
      }
    },
    {
      "id": "asb_claim_2",
      "source_group": "paper_text",
      "description": "The procedural counterevidence resolves the direct-write inference. It does not independently prove that every implementation respects the black-box restriction.",
      "scope": {
        "paper_version": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
        "experiment_arm": "Paper-text audit of query access during trigger construction and database access during memory poisoning. The supplied procedures establish no prohibited information flow.",
        "artifact_revision": "supplied document only; no execution artifact",
        "configuration": "v3 typed policy, applicability and delivery review"
      },
      "target": {
        "role": "memory-poisoning attacker",
        "phase": "poison construction and insertion",
        "source": "RAG database and embedder internals",
        "representation": "internal database structure or embedder details",
        "operation": "use internal access to construct or insert poisoned records"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Direct database-write suspicion: providing a poisoned database might imply white-box access, but the experimental procedure describes poisoning through agent execution.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "resource_metadata",
        "policy_application": {
          "policy_kind": "attacker_knowledge_constraint",
          "status": "uncertain",
          "reason": "The restriction applies specifically to the memory-poisoning attacker and excludes the internal access named in this suspicion.",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 3464, \"match\": \"normalized_exact\", \"segment_id\": \"p4\", \"start\": 3400, \"text_view\": \"primary\", \"text_view_sha256\": \"7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c\"}"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "possible_path",
          "task_relation": "unknown",
          "reason": "No supplied source-to-attacker boundary delivers database structure or embedder internals.",
          "reference": ""
        },
        "refutation": {
          "basis": "none",
          "reason": "The described insertion route is an agent saving an attack-induced plan, which counters the inference that the poisoned-database formalization requires direct internal access.",
          "reference": "{\"document_sha256\": \"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9\", \"end\": 4053, \"match\": \"normalized_exact\", \"segment_id\": \"p18\", \"start\": 3965, \"text_view\": \"primary\", \"text_view_sha256\": \"00d0640400c9b3e75847d58fb3e2b8283505b5557e0fbfa6910f3fe15026c218\"}"
        }
      },
      "claim_result": "unresolved",
      "citation_errors": [
        "semantic_review_disagrees_with_proposed_assessment"
      ],
      "locators": {
        "policy_scope": {
          "segment_id": "p4",
          "start": 3400,
          "end": 3464,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7c7e8969a460b6a6e142711875b20e7ae6fbcefbd96136bc53980ffff6a7d62c"
        },
        "refutation": {
          "segment_id": "p18",
          "start": 3965,
          "end": 4053,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "00d0640400c9b3e75847d58fb3e2b8283505b5557e0fbfa6910f3fe15026c218"
        },
        "declaration": {
          "segment_id": "p3",
          "start": 1750,
          "end": 1788,
          "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
          "match": "normalized_exact",
          "text_view": "primary",
          "text_view_sha256": "7a6ef2ebadd134976eee53d08f0e196f868956bf3e15b5457753872ffe58cdae"
        }
      },
      "semantic_review": {
        "index": 1,
        "supported": true,
        "policy_kind": "attacker_knowledge_constraint",
        "policy_application": "applicable",
        "delivery": "excluded",
        "refutation": "excluded_delivery",
        "reason": "The black-box restriction in p3–p4 applies to memory poisoning. p6, p18 and p26 affirmatively describe DPI-induced plans saved by the agent, countering the inference that providing a poisoned database requires direct internal access. Exclusion concerns that claimed insertion route, not every possible implementation."
      }
    }
  ],
  "document_sha256": "e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9",
  "schema_version": 3,
  "applicability": "in_scope",
  "scope": "Paper-text audit of query access during trigger construction and database access during memory poisoning. The supplied procedures establish no prohibited information flow.",
  "review_status": "model_reviewed_not_human_verified",
  "evidence_scope": "listed_claims_document_only",
  "notes": [
    "Only supplied paper text was examined; no static code, saved requests, or runtime records were supplied.",
    "Distinct PoT demonstration and testing tasks do not establish that trigger-generation tasks were also distinct.",
    "Reported attack success and defense failures are security outcomes, not evidence of inconsistent attacker knowledge.",
    "Specific questions about trigger-generation task identities and poisoned-memory source tasks versus evaluation tasks remain unanswered.",
    "Only supplied paper text supports these findings; no implementation or runtime evidence was supplied.",
    "Construction procedures do not establish causal effects of task overlap. Reported attack success and defense failures are security outcomes, not knowledge-budget violations."
  ],
  "unresolved_questions": [
    "Which tasks were supplied to GPT-4o for phrase-trigger generation, and did they include evaluated PoT tasks?",
    "Which source tasks were used to generate poisoned memories, and how do they relate to the subsequent evaluation tasks?"
  ],
  "verdict": "insufficient_evidence",
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "claim_result_counts": {
    "refuted": 1,
    "unresolved": 1
  },
  "input_mode": "document_only",
  "prompt_sha256": "a2c05a361fc0a14027ff29bfb1bf05e6678aec9369c63dd16cc4f9349ec8ce76",
  "duration_seconds": 54.942,
  "cohort": "previously_suspected_control",
  "expected": null,
  "expected_basis": "pending_independent_adjudication",
  "comparison_note": "A suspected false positive is not assumed clean; resolve against source evidence.",
  "matches_gold": null
}
```
