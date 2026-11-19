# 论文审计：测试过程与结果

运行类型：curated\_regression  
生成时间：2026\-11\-19T09:43:22\.636039\+00:00  
论文记录：18

主表每篇论文一行。“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。

## 本次运行汇总

```json
{
  "paper_count": 18,
  "statuses": {
    "completed": 15,
    "not_run": 3
  },
  "verdicts": {
    "insufficient_evidence": 6,
    "inconsistent": 4,
    "consistent_within_scope": 5,
    "not_run": 3
  },
  "reference_label_comparison": {
    "matched": 15,
    "scored": 15,
    "completed": 15,
    "total": 18,
    "interpretation": "historical labels may use evidence outside the PDF; not accuracy"
  }
}
```

## 论文结果

| 论文 ID | 论文 | 运行 / 判定 | 已确认不一致 | 标签对照 | 来源 |
| --- | --- | --- | --- | --- | --- |
| adaptools | AdapTools | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| blind\_spots | Blind Spots in the Guard | 有已确认的不一致 | 有 | 匹配；预期：有已确认的不一致 | 未记录 |
| aspi | ASPI | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| muzzle | MUZZLE | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| fha | Breaking MCP with Function Hijacking Attacks \(FHA\) | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| agentcon | AGENTCON | 有已确认的不一致 | 有 | 匹配；预期：有已确认的不一致 | 未记录 |
| retrieval\_barrier | Overcoming the Retrieval Barrier | 审计范围内一致 | 未确认 | 匹配；预期：审计范围内一致 | 未记录 |
| liar | Glue Pizza and Eat Rocks \(LIAR\) | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| obliinjection | ObliInjection | 有已确认的不一致 | 有 | 匹配；预期：有已确认的不一致 | 未记录 |
| webtrap | WebTrap | 有已确认的不一致 | 有 | 匹配；预期：有已确认的不一致 | 未记录 |
| icoa | ICoA | 证据不足 | 未确认 | 匹配；预期：证据不足 | 未记录 |
| attention | Attention Is All You Need | 尚未运行 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://papers\.nips\.cc/paper\_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa\-Paper\.pdf |
| resnet | Deep Residual Learning for Image Recognition | 尚未运行 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://arxiv\.org/pdf/1512\.03385v1 |
| adam | Adam: A Method for Stochastic Optimization | 尚未运行 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://arxiv\.org/pdf/1412\.6980v1 |
| trojan\_hippo | Trojan Hippo | 审计范围内一致 | 未确认 | 匹配；预期：审计范围内一致 | 未记录 |
| topicattack | TopicAttack | 审计范围内一致 | 未确认 | 匹配；预期：审计范围内一致 | 未记录 |
| agentdojo | AgentDojo | 审计范围内一致 | 未确认 | 匹配；预期：审计范围内一致 | 未记录 |
| asb | Agent Security Bench \(ASB\) | 审计范围内一致 | 未确认 | 匹配；预期：审计范围内一致 | 未记录 |

## 逐篇测试过程

### 1. AdapTools

论文 ID：adaptools  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "adaptools\_final\_black\_box\_online\_task\_access", "source\_group": "paper\_text", "description": "Check whether the final paper establishes a held\-out black\-box online input flow for the case\-specific user task\.", "scope": \{"paper\_version": "AdapTools EMNLP 2026 final §§4\.1, 4\.3 and 4\.5", "experiment\_arm": "Third\-party black\-box online condition", "artifact\_revision": "EMNLP 2026 proceedings and archived implementation audit", "configuration": "Held\-out online task, separate from offline strategy generation and grey\-box MCP access"\}, "target": \{"role": "third\-party black\-box adversary", "phase": "held\-out online prompt construction", "source": "current user task", "representation": "case\-specific task details", "operation": "receive as generation input"\}, "verdict": "insufficient\_evidence", "reason": "evaluated\_instance\_alignment\_not\_established", "matching\_rules": \[\{"edge": \{"role": "third\-party black\-box adversary", "phase": "held\-out online prompt construction", "source": "current user task", "representation": "case\-specific task details", "operation": "receive as generation input"\}, "permission": "deny", "reference": "§4\.1, https://aclanthology\.org/2026\.emnlp\-main\.2055\.pdf\#page=4"\}\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The held\-out online black\-box constructor receives the current evaluated user task in breach of the final paper’s black\-box knowledge restriction\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2026\.emnlp\-main\.2055\.pdf\#page=4", "reason": "§4\.1 excludes current task/state information for the third\-party black\-box actor\. This check is limited to that online arm, rather than the grey\-box MCP actor or offline library development\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "possible\_path", "task\_relation": "unknown", "reference": "", "reason": "§4\.3 describes task\-conditioned offline development, while §4\.5 describes a prebuilt library and online inference\. No bound input path ties those development inputs to the current held\-out black\-box task\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "§4\.3 and Fig\. 2 disclose task\-conditioned strategy generation and failure reasoning during library construction \(https://aclanthology\.org/2026\.emnlp\-main\.2055\.pdf\#page=5\)\. §4\.5 describes the library as prebuilt offline and describes online context inference from MCP interactions \(https://aclanthology\.org/2026\.emnlp\-main\.2055\.pdf\#page=6\)\. Available evidence does not bind the strategy\-generation inputs to the held\-out black\-box online condition\. See papers/AdapTools/METHODOLOGY\_COMPARISON\.md:12–17\."\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "adaptools_final_black_box_online_task_access",
    "source_group": "paper_text",
    "description": "Check whether the final paper establishes a held-out black-box online input flow for the case-specific user task.",
    "scope": {
      "paper_version": "AdapTools EMNLP 2026 final §§4.1, 4.3 and 4.5",
      "experiment_arm": "Third-party black-box online condition",
      "artifact_revision": "EMNLP 2026 proceedings and archived implementation audit",
      "configuration": "Held-out online task, separate from offline strategy generation and grey-box MCP access"
    },
    "target": {
      "role": "third-party black-box adversary",
      "phase": "held-out online prompt construction",
      "source": "current user task",
      "representation": "case-specific task details",
      "operation": "receive as generation input"
    },
    "verdict": "insufficient_evidence",
    "reason": "evaluated_instance_alignment_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "third-party black-box adversary",
          "phase": "held-out online prompt construction",
          "source": "current user task",
          "representation": "case-specific task details",
          "operation": "receive as generation input"
        },
        "permission": "deny",
        "reference": "§4.1, https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The held-out online black-box constructor receives the current evaluated user task in breach of the final paper’s black-box knowledge restriction.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4",
        "reason": "§4.1 excludes current task/state information for the third-party black-box actor. This check is limited to that online arm, rather than the grey-box MCP actor or offline library development.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "possible_path",
        "task_relation": "unknown",
        "reference": "",
        "reason": "§4.3 describes task-conditioned offline development, while §4.5 describes a prebuilt library and online inference. No bound input path ties those development inputs to the current held-out black-box task."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "§4.3 and Fig. 2 disclose task-conditioned strategy generation and failure reasoning during library construction (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=5). §4.5 describes the library as prebuilt offline and describes online context inference from MCP interactions (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=6). Available evidence does not bind the strategy-generation inputs to the held-out black-box online condition. See papers/AdapTools/METHODOLOGY_COMPARISON.md:12–17."
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "adaptools",
  "title": "AdapTools",
  "version": "EMNLP 2026 final",
  "audit_scope": "Held-out online black-box task delivery; offline strategy development and grey-box MCP access are distinct.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 1,
  "resolved_checks": 0,
  "confirmed_findings": [],
  "unresolved_checks": [
    "adaptools_final_black_box_online_task_access"
  ],
  "claim_result_counts": {
    "unresolved": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "adaptools_final_black_box_online_task_access",
      "source_group": "paper_text",
      "description": "Check whether the final paper establishes a held-out black-box online input flow for the case-specific user task.",
      "scope": {
        "paper_version": "AdapTools EMNLP 2026 final §§4.1, 4.3 and 4.5",
        "experiment_arm": "Third-party black-box online condition",
        "artifact_revision": "EMNLP 2026 proceedings and archived implementation audit",
        "configuration": "Held-out online task, separate from offline strategy generation and grey-box MCP access"
      },
      "target": {
        "role": "third-party black-box adversary",
        "phase": "held-out online prompt construction",
        "source": "current user task",
        "representation": "case-specific task details",
        "operation": "receive as generation input"
      },
      "verdict": "insufficient_evidence",
      "reason": "evaluated_instance_alignment_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "third-party black-box adversary",
            "phase": "held-out online prompt construction",
            "source": "current user task",
            "representation": "case-specific task details",
            "operation": "receive as generation input"
          },
          "permission": "deny",
          "reference": "§4.1, https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The held-out online black-box constructor receives the current evaluated user task in breach of the final paper’s black-box knowledge restriction.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4",
          "reason": "§4.1 excludes current task/state information for the third-party black-box actor. This check is limited to that online arm, rather than the grey-box MCP actor or offline library development.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "possible_path",
          "task_relation": "unknown",
          "reference": "",
          "reason": "§4.3 describes task-conditioned offline development, while §4.5 describes a prebuilt library and online inference. No bound input path ties those development inputs to the current held-out black-box task."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "§4.3 and Fig. 2 disclose task-conditioned strategy generation and failure reasoning during library construction (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=5). §4.5 describes the library as prebuilt offline and describes online context inference from MCP interactions (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=6). Available evidence does not bind the strategy-generation inputs to the held-out black-box online condition. See papers/AdapTools/METHODOLOGY_COMPARISON.md:12–17."
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "adaptools_final_black_box_online_task_access",
          "source_group": "paper_text",
          "description": "Check whether the final paper establishes a held-out black-box online input flow for the case-specific user task.",
          "scope": {
            "paper_version": "AdapTools EMNLP 2026 final §§4.1, 4.3 and 4.5",
            "experiment_arm": "Third-party black-box online condition",
            "artifact_revision": "EMNLP 2026 proceedings and archived implementation audit",
            "configuration": "Held-out online task, separate from offline strategy generation and grey-box MCP access"
          },
          "target": {
            "role": "third-party black-box adversary",
            "phase": "held-out online prompt construction",
            "source": "current user task",
            "representation": "case-specific task details",
            "operation": "receive as generation input"
          },
          "verdict": "insufficient_evidence",
          "reason": "evaluated_instance_alignment_not_established",
          "matching_rules": [
            {
              "edge": {
                "role": "third-party black-box adversary",
                "phase": "held-out online prompt construction",
                "source": "current user task",
                "representation": "case-specific task details",
                "operation": "receive as generation input"
              },
              "permission": "deny",
              "reference": "§4.1, https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4"
            }
          ],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The held-out online black-box constructor receives the current evaluated user task in breach of the final paper’s black-box knowledge restriction.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4",
              "reason": "§4.1 excludes current task/state information for the third-party black-box actor. This check is limited to that online arm, rather than the grey-box MCP actor or offline library development.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "possible_path",
              "task_relation": "unknown",
              "reference": "",
              "reason": "§4.3 describes task-conditioned offline development, while §4.5 describes a prebuilt library and online inference. No bound input path ties those development inputs to the current held-out black-box task."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "§4.3 and Fig. 2 disclose task-conditioned strategy generation and failure reasoning during library construction (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=5). §4.5 describes the library as prebuilt offline and describes online context inference from MCP interactions (https://aclanthology.org/2026.emnlp-main.2055.pdf#page=6). Available evidence does not bind the strategy-generation inputs to the held-out black-box online condition. See papers/AdapTools/METHODOLOGY_COMPARISON.md:12–17."
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 2. Blind Spots in the Guard

论文 ID：blind\_spots  
运行 / 判定：有已确认的不一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "blind\_spots\_exp1\_document\_access", "source\_group": "archived", "description": "Compare the target\-document access implemented in the archived Exp1 generation condition with §2’s stated knowledge boundary\.", "scope": \{"paper\_version": "Blind Spots in the Guard arXiv:2605\.22001v1, §2 and §4\.2", "experiment\_arm": "Exp1 FULL\_CONTEXT generation path in the local public\-source archive", "artifact\_revision": "Source archive revision 9a21b5a230cbcc92ec66987aa7814c188881108a", "configuration": "Target\-document field used with the archived corpus, compared specifically with the §2 boundary"\}, "target": \{"role": "attacker\-side generator", "phase": "content generation", "source": "target document for the evaluated case", "representation": "clean target document text", "operation": "receive as generation input"\}, "verdict": "inconsistent", "reason": "scoped\_forbidden\_delivery\_confirmed", "matching\_rules": \[\{"edge": \{"role": "attacker\-side generator", "phase": "content generation", "source": "target document for the evaluated case", "representation": "clean target document text", "operation": "receive as generation input"\}, "permission": "deny", "reference": "https://arxiv\.org/html/2605\.22001v1\#S2; https://arxiv\.org/html/2605\.22001v1\#S4\.SS2"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side generator", "phase": "content generation", "source": "target document for the evaluated case", "representation": "clean target document text", "operation": "receive as generation input"\}, "status": "present", "reference": "src/attacks/camouflage\_generator\.py:211–215; experiments/exp1\_static\_vs\_camouflage\_single\.py:196–219; results/context\_ablation\_asr\_full\_llama31/RUN\_PROVENANCE\.md:3–14; analysis/casebook\_2026\-11\-05/BLIND\_SPOTS\_CASES\_ZH\.md:9"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The archived Exp\. 1 generator receives the evaluated target document despite §2's restriction on knowing that document\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "document\_content", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "https://arxiv\.org/html/2605\.22001v1\#S2; https://arxiv\.org/html/2605\.22001v1\#S4\.SS2", "reason": "Section 2 expressly excludes the exact clean target document for this attack\. Section 4\.2 discloses the richer document\-conditioned method without defining a separate stronger document\-visible arm\."\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "src/attacks/camouflage\_generator\.py:211–215; experiments/exp1\_static\_vs\_camouflage\_single\.py:196–219; results/context\_ablation\_asr\_full\_llama31/RUN\_PROVENANCE\.md:3–14; analysis/casebook\_2026\-11\-05/BLIND\_SPOTS\_CASES\_ZH\.md:9", "reason": "The Exp\. 1 driver passes the case's clean\_context to the generator\. The generator includes its first 2000 characters, covering the full documents in this archived task bank\."\}, "refutation": \{"basis": "none", "reference": "https://arxiv\.org/html/2605\.22001v1\#S4\.SS2; analysis/casebook\_2026\-11\-05/BLIND\_SPOTS\_CASES\_ZH\.md:3–11", "reason": "The method's disclosure confirms the document\-conditioned construction\. No separate permission or different\-instance explanation resolves the §2 restriction for the scoped arm\."\}\}, "claim\_result": "confirmed", "note": "Introduction and §4\.2 independently disclose generation with the target document, so the mismatch concerns the §2 formulation\. Logs for the original paper’s historical generation run remain unverified\. This edge is document content: it says nothing about receipt of the separate user instruction\.", "behavioral\_impact": \{"status": "confounded", "reference": "results/context\_ablation\_asr\_full\_llama31/summary\.json:10–21,49–63; analysis/casebook\_2026\-11\-05/BLIND\_SPOTS\_CASES\_ZH\.md:208–212", "description": "The archived comparison reports FULL 24/121 versus NO\_CONTEXT 15/121\. Paired and task\-clustered bootstrap intervals use different resampling units\. Prompt wording changes and clustered variants limit a single\-field causal interpretation\."\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "inconsistent", "reason": "confirmed\_inconsistency\_in\_scope"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "inconsistent", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "blind_spots_exp1_document_access",
    "source_group": "archived",
    "description": "Compare the target-document access implemented in the archived Exp1 generation condition with §2’s stated knowledge boundary.",
    "scope": {
      "paper_version": "Blind Spots in the Guard arXiv:2605.22001v1, §2 and §4.2",
      "experiment_arm": "Exp1 FULL_CONTEXT generation path in the local public-source archive",
      "artifact_revision": "Source archive revision 9a21b5a230cbcc92ec66987aa7814c188881108a",
      "configuration": "Target-document field used with the archived corpus, compared specifically with the §2 boundary"
    },
    "target": {
      "role": "attacker-side generator",
      "phase": "content generation",
      "source": "target document for the evaluated case",
      "representation": "clean target document text",
      "operation": "receive as generation input"
    },
    "verdict": "inconsistent",
    "reason": "scoped_forbidden_delivery_confirmed",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "content generation",
          "source": "target document for the evaluated case",
          "representation": "clean target document text",
          "operation": "receive as generation input"
        },
        "permission": "deny",
        "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "content generation",
          "source": "target document for the evaluated case",
          "representation": "clean target document text",
          "operation": "receive as generation input"
        },
        "status": "present",
        "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The archived Exp. 1 generator receives the evaluated target document despite §2's restriction on knowing that document.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2",
        "reason": "Section 2 expressly excludes the exact clean target document for this attack. Section 4.2 discloses the richer document-conditioned method without defining a separate stronger document-visible arm."
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9",
        "reason": "The Exp. 1 driver passes the case's clean_context to the generator. The generator includes its first 2000 characters, covering the full documents in this archived task bank."
      },
      "refutation": {
        "basis": "none",
        "reference": "https://arxiv.org/html/2605.22001v1#S4.SS2; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:3–11",
        "reason": "The method's disclosure confirms the document-conditioned construction. No separate permission or different-instance explanation resolves the §2 restriction for the scoped arm."
      }
    },
    "claim_result": "confirmed",
    "note": "Introduction and §4.2 independently disclose generation with the target document, so the mismatch concerns the §2 formulation. Logs for the original paper’s historical generation run remain unverified. This edge is document content: it says nothing about receipt of the separate user instruction.",
    "behavioral_impact": {
      "status": "confounded",
      "reference": "results/context_ablation_asr_full_llama31/summary.json:10–21,49–63; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:208–212",
      "description": "The archived comparison reports FULL 24/121 versus NO_CONTEXT 15/121. Paired and task-clustered bootstrap intervals use different resampling units. Prompt wording changes and clustered variants limit a single-field causal interpretation."
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "blind_spots",
  "title": "Blind Spots in the Guard",
  "version": "arXiv:2605.22001v1",
  "audit_scope": "Only the evaluated-case clean_context input to the archived Exp. 1 generator at revision 9a21b5a230cbcc92ec66987aa7814c188881108a, assessed against §2. Candidate selection, all other channels and author historical run provenance are outside this finite input check.",
  "verdict": "inconsistent",
  "has_confirmed_inconsistency": true,
  "reason": "confirmed_inconsistency_in_scope",
  "coverage_complete": true,
  "required_checks": 1,
  "resolved_checks": 1,
  "confirmed_findings": [
    "blind_spots_exp1_document_access"
  ],
  "unresolved_checks": [],
  "claim_result_counts": {
    "confirmed": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [
    {
      "case_id": "blind_spots_exp1_document_access",
      "status": "confounded",
      "reference": "results/context_ablation_asr_full_llama31/summary.json:10–21,49–63; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:208–212",
      "description": "The archived comparison reports FULL 24/121 versus NO_CONTEXT 15/121. Paired and task-clustered bootstrap intervals use different resampling units. Prompt wording changes and clustered variants limit a single-field causal interpretation."
    }
  ],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "blind_spots_exp1_document_access",
      "source_group": "archived",
      "description": "Compare the target-document access implemented in the archived Exp1 generation condition with §2’s stated knowledge boundary.",
      "scope": {
        "paper_version": "Blind Spots in the Guard arXiv:2605.22001v1, §2 and §4.2",
        "experiment_arm": "Exp1 FULL_CONTEXT generation path in the local public-source archive",
        "artifact_revision": "Source archive revision 9a21b5a230cbcc92ec66987aa7814c188881108a",
        "configuration": "Target-document field used with the archived corpus, compared specifically with the §2 boundary"
      },
      "target": {
        "role": "attacker-side generator",
        "phase": "content generation",
        "source": "target document for the evaluated case",
        "representation": "clean target document text",
        "operation": "receive as generation input"
      },
      "verdict": "inconsistent",
      "reason": "scoped_forbidden_delivery_confirmed",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "content generation",
            "source": "target document for the evaluated case",
            "representation": "clean target document text",
            "operation": "receive as generation input"
          },
          "permission": "deny",
          "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "content generation",
            "source": "target document for the evaluated case",
            "representation": "clean target document text",
            "operation": "receive as generation input"
          },
          "status": "present",
          "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The archived Exp. 1 generator receives the evaluated target document despite §2's restriction on knowing that document.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2",
          "reason": "Section 2 expressly excludes the exact clean target document for this attack. Section 4.2 discloses the richer document-conditioned method without defining a separate stronger document-visible arm."
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9",
          "reason": "The Exp. 1 driver passes the case's clean_context to the generator. The generator includes its first 2000 characters, covering the full documents in this archived task bank."
        },
        "refutation": {
          "basis": "none",
          "reference": "https://arxiv.org/html/2605.22001v1#S4.SS2; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:3–11",
          "reason": "The method's disclosure confirms the document-conditioned construction. No separate permission or different-instance explanation resolves the §2 restriction for the scoped arm."
        }
      },
      "claim_result": "confirmed",
      "note": "Introduction and §4.2 independently disclose generation with the target document, so the mismatch concerns the §2 formulation. Logs for the original paper’s historical generation run remain unverified. This edge is document content: it says nothing about receipt of the separate user instruction.",
      "behavioral_impact": {
        "status": "confounded",
        "reference": "results/context_ablation_asr_full_llama31/summary.json:10–21,49–63; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:208–212",
        "description": "The archived comparison reports FULL 24/121 versus NO_CONTEXT 15/121. Paired and task-clustered bootstrap intervals use different resampling units. Prompt wording changes and clustered variants limit a single-field causal interpretation."
      }
    }
  ],
  "expected": "inconsistent",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "blind_spots_exp1_document_access",
          "source_group": "archived",
          "description": "Compare the target-document access implemented in the archived Exp1 generation condition with §2’s stated knowledge boundary.",
          "scope": {
            "paper_version": "Blind Spots in the Guard arXiv:2605.22001v1, §2 and §4.2",
            "experiment_arm": "Exp1 FULL_CONTEXT generation path in the local public-source archive",
            "artifact_revision": "Source archive revision 9a21b5a230cbcc92ec66987aa7814c188881108a",
            "configuration": "Target-document field used with the archived corpus, compared specifically with the §2 boundary"
          },
          "target": {
            "role": "attacker-side generator",
            "phase": "content generation",
            "source": "target document for the evaluated case",
            "representation": "clean target document text",
            "operation": "receive as generation input"
          },
          "verdict": "inconsistent",
          "reason": "scoped_forbidden_delivery_confirmed",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "content generation",
                "source": "target document for the evaluated case",
                "representation": "clean target document text",
                "operation": "receive as generation input"
              },
              "permission": "deny",
              "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "content generation",
                "source": "target document for the evaluated case",
                "representation": "clean target document text",
                "operation": "receive as generation input"
              },
              "status": "present",
              "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The archived Exp. 1 generator receives the evaluated target document despite §2's restriction on knowing that document.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "document_content",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "https://arxiv.org/html/2605.22001v1#S2; https://arxiv.org/html/2605.22001v1#S4.SS2",
              "reason": "Section 2 expressly excludes the exact clean target document for this attack. Section 4.2 discloses the richer document-conditioned method without defining a separate stronger document-visible arm."
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "src/attacks/camouflage_generator.py:211–215; experiments/exp1_static_vs_camouflage_single.py:196–219; results/context_ablation_asr_full_llama31/RUN_PROVENANCE.md:3–14; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9",
              "reason": "The Exp. 1 driver passes the case's clean_context to the generator. The generator includes its first 2000 characters, covering the full documents in this archived task bank."
            },
            "refutation": {
              "basis": "none",
              "reference": "https://arxiv.org/html/2605.22001v1#S4.SS2; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:3–11",
              "reason": "The method's disclosure confirms the document-conditioned construction. No separate permission or different-instance explanation resolves the §2 restriction for the scoped arm."
            }
          },
          "claim_result": "confirmed",
          "note": "Introduction and §4.2 independently disclose generation with the target document, so the mismatch concerns the §2 formulation. Logs for the original paper’s historical generation run remain unverified. This edge is document content: it says nothing about receipt of the separate user instruction.",
          "behavioral_impact": {
            "status": "confounded",
            "reference": "results/context_ablation_asr_full_llama31/summary.json:10–21,49–63; analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:208–212",
            "description": "The archived comparison reports FULL 24/121 versus NO_CONTEXT 15/121. Paired and task-clustered bootstrap intervals use different resampling units. Prompt wording changes and clustered variants limit a single-field causal interpretation."
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "inconsistent",
      "reason": "confirmed_inconsistency_in_scope"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "inconsistent",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 3. ASPI

论文 ID：aspi  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "aspi\_stage1\_designer\_task", "source\_group": "archived", "description": "Check the original task prompt used by the benchmark designer during Stage 1 dataset construction\.", "scope": \{"paper\_version": "ASPI arXiv:2605\.17324v1, §§4\.1–4\.2 and Appendix B\.1", "experiment\_arm": "Released Stage 1 benchmark construction", "artifact\_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "configuration": "Official dataset pipeline, original task to ambiguous task"\}, "target": \{"role": "benchmark designer", "phase": "dataset construction", "source": "original benchmark task", "representation": "original task prompt", "operation": "read to construct ambiguous task", "query\_form": "full\_query"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "benchmark designer", "phase": "dataset construction", "source": "original benchmark task", "representation": "original task prompt", "operation": "read to construct ambiguous task", "query\_form": "full\_query"\}, "permission": "allow", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi\-paper\-v1\.html:1196–1257; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/v2/THREAT\_MODEL\_REAUDIT\_V2\.md:8"\}\], "matching\_observations": \[\{"edge": \{"role": "benchmark designer", "phase": "dataset construction", "source": "original benchmark task", "representation": "original task prompt", "operation": "read to construct ambiguous task", "query\_form": "full\_query"\}, "status": "present", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline\.py:106–121,429–436"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The Stage 1 benchmark designer's read of the original task constitutes a prohibited information flow\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi\-paper\-v1\.html:1196–1257; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/v2/THREAT\_MODEL\_REAUDIT\_V2\.md:8", "reason": "The paper specifies the benchmark designer's original\-task input during Stage 1 construction\. This permission is scoped to that designer and stage\."\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline\.py:106–121,429–436", "reason": "The original task for the benchmark pair enters Stage 1 to produce its ambiguous variant\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi\-paper\-v1\.html:1196–1257; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/v2/THREAT\_MODEL\_REAUDIT\_V2\.md:8", "reason": "The scoped original\-task read is an explicitly described and permitted benchmark\-construction input\."\}\}, "claim\_result": "refuted", "note": "The paper specifies the designer's use in Stage 1\. Permission for the external attacker or Stage 2 is a separate question\.", "behavioral\_impact": \{"status": "not\_tested", "reference": "analysis/threat\_model\_auditor/adjudication/construction\_sources\.md:17", "description": "This case concerns the designer's access entitlement\. No behavioral effect is required for that question\."\}\}, \{"id": "aspi\_released\_stage2\_partial\_query", "source\_group": "archived", "description": "Compare the task\-derived base prompt supplied to the released Stage 2 reply generator with the external attacker’s task access in §3\.", "scope": \{"paper\_version": "ASPI arXiv:2605\.17324v1, §3, §4\.2, §5\.1 and Appendix B", "experiment\_arm": "Released Stage 2 dataset authoring for the clarif\_user direct\-user baseline", "artifact\_revision": "Vendored ASPI upstream e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d", "configuration": "Offline Stage 2 partial\-task input in the disclosed clarif\_user direct\-user baseline; applicability of the §3 external\-adversary knowledge restriction is unresolved"\}, "target": \{"role": "attacker\-side reply generator", "phase": "offline Stage 2 construction", "source": "Stage 1 transformation of the original benchmark task", "representation": "slot\-deleted base prompt with retained task\-specific wording", "operation": "receive as generation input", "query\_form": "partial\_query"\}, "verdict": "insufficient\_evidence", "reason": "policy\_scope\_not\_established", "matching\_rules": \[\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side reply generator", "phase": "offline Stage 2 construction", "source": "Stage 1 transformation of the original benchmark task", "representation": "slot\-deleted base prompt with retained task\-specific wording", "operation": "receive as generation input", "query\_form": "partial\_query"\}, "status": "present", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline\.py:125–139; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset\.py:165–173; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner\.py:1575–1585,1797–1812"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The released offline Stage 2 task\-conditioned reply construction violates its applicable knowledge budget, conditional on §3's external\-adversary restriction governing the stronger clarif\_user baseline\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "partial\_query", "policy\_application": \{"status": "uncertain", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi\-paper\-v1\.html:494–500,1196–1200,1263–1310; analysis/threat\_model\_auditor/adjudication/construction\_sources\.md:25", "reason": "Section 3 limits an external adversary and explicitly includes direct\-user turns as a stronger baseline\. Appendix B discloses offline task\-aware construction\. Whether the same external knowledge restriction governs this construction role and stronger baseline is unresolved, so no unconditional deny is normalized onto the edge\."\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline\.py:125–139; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset\.py:165–173; repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner\.py:1575–1585,1797–1812", "reason": "Stage 2 receives the slot\-deleted base prompt for the same benchmark pair, and its saved reply is used by the released clarif\_user branch\."\}, "refutation": \{"basis": "none", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/upstream/aspi\-paper\-v1\.html:494–500; analysis/threat\_model\_auditor/adjudication/construction\_sources\.md:33", "reason": "Confirmed task\-conditioned authoring remains\. Neither the role ambiguity nor the stronger\-baseline disclosure supplies an explicit permission that definitively refutes every reading of the claim\."\}\}, "claim\_result": "unresolved", "note": "Task\-conditioned partial\-query input is confirmed\. A mismatch relative to a strict external\-adversary budget remains a conditional comparison\. The published direct\-user baseline and offline construction role require an applicability decision before assigning that external deny rule to this edge\. The stronger\-baseline disclosure does not itself grant every task field\. The actual\-question and tool\-return branches have separate scope\.", "behavioral\_impact": \{"status": "inconclusive", "reference": "repository/aspi\-matched\-context\-pilot\-v1/papers/ASPI/v3/CONTROLLED\_ABLATION\_REPORT\.md:7–25", "description": "The archived nine\-pair matched pilot shows no FULL\-context ASR advantage and has limited precision\. This effect result does not determine policy applicability or negate the confirmed partial\-task input\."\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "aspi_stage1_designer_task",
    "source_group": "archived",
    "description": "Check the original task prompt used by the benchmark designer during Stage 1 dataset construction.",
    "scope": {
      "paper_version": "ASPI arXiv:2605.17324v1, §§4.1–4.2 and Appendix B.1",
      "experiment_arm": "Released Stage 1 benchmark construction",
      "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
      "configuration": "Official dataset pipeline, original task to ambiguous task"
    },
    "target": {
      "role": "benchmark designer",
      "phase": "dataset construction",
      "source": "original benchmark task",
      "representation": "original task prompt",
      "operation": "read to construct ambiguous task",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "benchmark designer",
          "phase": "dataset construction",
          "source": "original benchmark task",
          "representation": "original task prompt",
          "operation": "read to construct ambiguous task",
          "query_form": "full_query"
        },
        "permission": "allow",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "benchmark designer",
          "phase": "dataset construction",
          "source": "original benchmark task",
          "representation": "original task prompt",
          "operation": "read to construct ambiguous task",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The Stage 1 benchmark designer's read of the original task constitutes a prohibited information flow.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
        "reason": "The paper specifies the benchmark designer's original-task input during Stage 1 construction. This permission is scoped to that designer and stage."
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436",
        "reason": "The original task for the benchmark pair enters Stage 1 to produce its ambiguous variant."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
        "reason": "The scoped original-task read is an explicitly described and permitted benchmark-construction input."
      }
    },
    "claim_result": "refuted",
    "note": "The paper specifies the designer's use in Stage 1. Permission for the external attacker or Stage 2 is a separate question.",
    "behavioral_impact": {
      "status": "not_tested",
      "reference": "analysis/threat_model_auditor/adjudication/construction_sources.md:17",
      "description": "This case concerns the designer's access entitlement. No behavioral effect is required for that question."
    }
  },
  {
    "id": "aspi_released_stage2_partial_query",
    "source_group": "archived",
    "description": "Compare the task-derived base prompt supplied to the released Stage 2 reply generator with the external attacker’s task access in §3.",
    "scope": {
      "paper_version": "ASPI arXiv:2605.17324v1, §3, §4.2, §5.1 and Appendix B",
      "experiment_arm": "Released Stage 2 dataset authoring for the clarif_user direct-user baseline",
      "artifact_revision": "Vendored ASPI upstream e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
      "configuration": "Offline Stage 2 partial-task input in the disclosed clarif_user direct-user baseline; applicability of the §3 external-adversary knowledge restriction is unresolved"
    },
    "target": {
      "role": "attacker-side reply generator",
      "phase": "offline Stage 2 construction",
      "source": "Stage 1 transformation of the original benchmark task",
      "representation": "slot-deleted base prompt with retained task-specific wording",
      "operation": "receive as generation input",
      "query_form": "partial_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side reply generator",
          "phase": "offline Stage 2 construction",
          "source": "Stage 1 transformation of the original benchmark task",
          "representation": "slot-deleted base prompt with retained task-specific wording",
          "operation": "receive as generation input",
          "query_form": "partial_query"
        },
        "status": "present",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The released offline Stage 2 task-conditioned reply construction violates its applicable knowledge budget, conditional on §3's external-adversary restriction governing the stronger clarif_user baseline.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "partial_query",
      "policy_application": {
        "status": "uncertain",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500,1196–1200,1263–1310; analysis/threat_model_auditor/adjudication/construction_sources.md:25",
        "reason": "Section 3 limits an external adversary and explicitly includes direct-user turns as a stronger baseline. Appendix B discloses offline task-aware construction. Whether the same external knowledge restriction governs this construction role and stronger baseline is unresolved, so no unconditional deny is normalized onto the edge."
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812",
        "reason": "Stage 2 receives the slot-deleted base prompt for the same benchmark pair, and its saved reply is used by the released clarif_user branch."
      },
      "refutation": {
        "basis": "none",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500; analysis/threat_model_auditor/adjudication/construction_sources.md:33",
        "reason": "Confirmed task-conditioned authoring remains. Neither the role ambiguity nor the stronger-baseline disclosure supplies an explicit permission that definitively refutes every reading of the claim."
      }
    },
    "claim_result": "unresolved",
    "note": "Task-conditioned partial-query input is confirmed. A mismatch relative to a strict external-adversary budget remains a conditional comparison. The published direct-user baseline and offline construction role require an applicability decision before assigning that external deny rule to this edge. The stronger-baseline disclosure does not itself grant every task field. The actual-question and tool-return branches have separate scope.",
    "behavioral_impact": {
      "status": "inconclusive",
      "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/CONTROLLED_ABLATION_REPORT.md:7–25",
      "description": "The archived nine-pair matched pilot shows no FULL-context ASR advantage and has limited precision. This effect result does not determine policy applicability or negate the confirmed partial-task input."
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "aspi",
  "title": "ASPI",
  "version": "arXiv:2605.17324v1",
  "audit_scope": "Stage 1 original-task access and released offline Stage 2 partial-task input used for clarif_user at the frozen revision. The external §3 restriction's applicability to the stronger direct-user baseline remains unresolved. Other channels and historical dynamic generation have separate scope.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 2,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [
    "aspi_released_stage2_partial_query"
  ],
  "claim_result_counts": {
    "refuted": 1,
    "unresolved": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [
    {
      "case_id": "aspi_stage1_designer_task",
      "status": "not_tested",
      "reference": "analysis/threat_model_auditor/adjudication/construction_sources.md:17",
      "description": "This case concerns the designer's access entitlement. No behavioral effect is required for that question."
    },
    {
      "case_id": "aspi_released_stage2_partial_query",
      "status": "inconclusive",
      "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/CONTROLLED_ABLATION_REPORT.md:7–25",
      "description": "The archived nine-pair matched pilot shows no FULL-context ASR advantage and has limited precision. This effect result does not determine policy applicability or negate the confirmed partial-task input."
    }
  ],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "aspi_stage1_designer_task",
      "source_group": "archived",
      "description": "Check the original task prompt used by the benchmark designer during Stage 1 dataset construction.",
      "scope": {
        "paper_version": "ASPI arXiv:2605.17324v1, §§4.1–4.2 and Appendix B.1",
        "experiment_arm": "Released Stage 1 benchmark construction",
        "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "configuration": "Official dataset pipeline, original task to ambiguous task"
      },
      "target": {
        "role": "benchmark designer",
        "phase": "dataset construction",
        "source": "original benchmark task",
        "representation": "original task prompt",
        "operation": "read to construct ambiguous task",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "benchmark designer",
            "phase": "dataset construction",
            "source": "original benchmark task",
            "representation": "original task prompt",
            "operation": "read to construct ambiguous task",
            "query_form": "full_query"
          },
          "permission": "allow",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "benchmark designer",
            "phase": "dataset construction",
            "source": "original benchmark task",
            "representation": "original task prompt",
            "operation": "read to construct ambiguous task",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The Stage 1 benchmark designer's read of the original task constitutes a prohibited information flow.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
          "reason": "The paper specifies the benchmark designer's original-task input during Stage 1 construction. This permission is scoped to that designer and stage."
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436",
          "reason": "The original task for the benchmark pair enters Stage 1 to produce its ambiguous variant."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
          "reason": "The scoped original-task read is an explicitly described and permitted benchmark-construction input."
        }
      },
      "claim_result": "refuted",
      "note": "The paper specifies the designer's use in Stage 1. Permission for the external attacker or Stage 2 is a separate question.",
      "behavioral_impact": {
        "status": "not_tested",
        "reference": "analysis/threat_model_auditor/adjudication/construction_sources.md:17",
        "description": "This case concerns the designer's access entitlement. No behavioral effect is required for that question."
      }
    },
    {
      "id": "aspi_released_stage2_partial_query",
      "source_group": "archived",
      "description": "Compare the task-derived base prompt supplied to the released Stage 2 reply generator with the external attacker’s task access in §3.",
      "scope": {
        "paper_version": "ASPI arXiv:2605.17324v1, §3, §4.2, §5.1 and Appendix B",
        "experiment_arm": "Released Stage 2 dataset authoring for the clarif_user direct-user baseline",
        "artifact_revision": "Vendored ASPI upstream e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
        "configuration": "Offline Stage 2 partial-task input in the disclosed clarif_user direct-user baseline; applicability of the §3 external-adversary knowledge restriction is unresolved"
      },
      "target": {
        "role": "attacker-side reply generator",
        "phase": "offline Stage 2 construction",
        "source": "Stage 1 transformation of the original benchmark task",
        "representation": "slot-deleted base prompt with retained task-specific wording",
        "operation": "receive as generation input",
        "query_form": "partial_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side reply generator",
            "phase": "offline Stage 2 construction",
            "source": "Stage 1 transformation of the original benchmark task",
            "representation": "slot-deleted base prompt with retained task-specific wording",
            "operation": "receive as generation input",
            "query_form": "partial_query"
          },
          "status": "present",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The released offline Stage 2 task-conditioned reply construction violates its applicable knowledge budget, conditional on §3's external-adversary restriction governing the stronger clarif_user baseline.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "partial_query",
        "policy_application": {
          "status": "uncertain",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500,1196–1200,1263–1310; analysis/threat_model_auditor/adjudication/construction_sources.md:25",
          "reason": "Section 3 limits an external adversary and explicitly includes direct-user turns as a stronger baseline. Appendix B discloses offline task-aware construction. Whether the same external knowledge restriction governs this construction role and stronger baseline is unresolved, so no unconditional deny is normalized onto the edge."
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812",
          "reason": "Stage 2 receives the slot-deleted base prompt for the same benchmark pair, and its saved reply is used by the released clarif_user branch."
        },
        "refutation": {
          "basis": "none",
          "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500; analysis/threat_model_auditor/adjudication/construction_sources.md:33",
          "reason": "Confirmed task-conditioned authoring remains. Neither the role ambiguity nor the stronger-baseline disclosure supplies an explicit permission that definitively refutes every reading of the claim."
        }
      },
      "claim_result": "unresolved",
      "note": "Task-conditioned partial-query input is confirmed. A mismatch relative to a strict external-adversary budget remains a conditional comparison. The published direct-user baseline and offline construction role require an applicability decision before assigning that external deny rule to this edge. The stronger-baseline disclosure does not itself grant every task field. The actual-question and tool-return branches have separate scope.",
      "behavioral_impact": {
        "status": "inconclusive",
        "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/CONTROLLED_ABLATION_REPORT.md:7–25",
        "description": "The archived nine-pair matched pilot shows no FULL-context ASR advantage and has limited precision. This effect result does not determine policy applicability or negate the confirmed partial-task input."
      }
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "aspi_stage1_designer_task",
          "source_group": "archived",
          "description": "Check the original task prompt used by the benchmark designer during Stage 1 dataset construction.",
          "scope": {
            "paper_version": "ASPI arXiv:2605.17324v1, §§4.1–4.2 and Appendix B.1",
            "experiment_arm": "Released Stage 1 benchmark construction",
            "artifact_revision": "e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
            "configuration": "Official dataset pipeline, original task to ambiguous task"
          },
          "target": {
            "role": "benchmark designer",
            "phase": "dataset construction",
            "source": "original benchmark task",
            "representation": "original task prompt",
            "operation": "read to construct ambiguous task",
            "query_form": "full_query"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "benchmark designer",
                "phase": "dataset construction",
                "source": "original benchmark task",
                "representation": "original task prompt",
                "operation": "read to construct ambiguous task",
                "query_form": "full_query"
              },
              "permission": "allow",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "benchmark designer",
                "phase": "dataset construction",
                "source": "original benchmark task",
                "representation": "original task prompt",
                "operation": "read to construct ambiguous task",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The Stage 1 benchmark designer's read of the original task constitutes a prohibited information flow.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
              "reason": "The paper specifies the benchmark designer's original-task input during Stage 1 construction. This permission is scoped to that designer and stage."
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:106–121,429–436",
              "reason": "The original task for the benchmark pair enters Stage 1 to produce its ambiguous variant."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196–1257; repository/aspi-matched-context-pilot-v1/papers/ASPI/v2/THREAT_MODEL_REAUDIT_V2.md:8",
              "reason": "The scoped original-task read is an explicitly described and permitted benchmark-construction input."
            }
          },
          "claim_result": "refuted",
          "note": "The paper specifies the designer's use in Stage 1. Permission for the external attacker or Stage 2 is a separate question.",
          "behavioral_impact": {
            "status": "not_tested",
            "reference": "analysis/threat_model_auditor/adjudication/construction_sources.md:17",
            "description": "This case concerns the designer's access entitlement. No behavioral effect is required for that question."
          }
        },
        {
          "id": "aspi_released_stage2_partial_query",
          "source_group": "archived",
          "description": "Compare the task-derived base prompt supplied to the released Stage 2 reply generator with the external attacker’s task access in §3.",
          "scope": {
            "paper_version": "ASPI arXiv:2605.17324v1, §3, §4.2, §5.1 and Appendix B",
            "experiment_arm": "Released Stage 2 dataset authoring for the clarif_user direct-user baseline",
            "artifact_revision": "Vendored ASPI upstream e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d",
            "configuration": "Offline Stage 2 partial-task input in the disclosed clarif_user direct-user baseline; applicability of the §3 external-adversary knowledge restriction is unresolved"
          },
          "target": {
            "role": "attacker-side reply generator",
            "phase": "offline Stage 2 construction",
            "source": "Stage 1 transformation of the original benchmark task",
            "representation": "slot-deleted base prompt with retained task-specific wording",
            "operation": "receive as generation input",
            "query_form": "partial_query"
          },
          "verdict": "insufficient_evidence",
          "reason": "policy_scope_not_established",
          "matching_rules": [],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side reply generator",
                "phase": "offline Stage 2 construction",
                "source": "Stage 1 transformation of the original benchmark task",
                "representation": "slot-deleted base prompt with retained task-specific wording",
                "operation": "receive as generation input",
                "query_form": "partial_query"
              },
              "status": "present",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The released offline Stage 2 task-conditioned reply construction violates its applicable knowledge budget, conditional on §3's external-adversary restriction governing the stronger clarif_user baseline.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "partial_query",
            "policy_application": {
              "status": "uncertain",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500,1196–1200,1263–1310; analysis/threat_model_auditor/adjudication/construction_sources.md:25",
              "reason": "Section 3 limits an external adversary and explicitly includes direct-user turns as a stronger baseline. Appendix B discloses offline task-aware construction. Whether the same external knowledge restriction governs this construction role and stronger baseline is unresolved, so no unconditional deny is normalized onto the edge."
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125–139; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:165–173; repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575–1585,1797–1812",
              "reason": "Stage 2 receives the slot-deleted base prompt for the same benchmark pair, and its saved reply is used by the released clarif_user branch."
            },
            "refutation": {
              "basis": "none",
              "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494–500; analysis/threat_model_auditor/adjudication/construction_sources.md:33",
              "reason": "Confirmed task-conditioned authoring remains. Neither the role ambiguity nor the stronger-baseline disclosure supplies an explicit permission that definitively refutes every reading of the claim."
            }
          },
          "claim_result": "unresolved",
          "note": "Task-conditioned partial-query input is confirmed. A mismatch relative to a strict external-adversary budget remains a conditional comparison. The published direct-user baseline and offline construction role require an applicability decision before assigning that external deny rule to this edge. The stronger-baseline disclosure does not itself grant every task field. The actual-question and tool-return branches have separate scope.",
          "behavioral_impact": {
            "status": "inconclusive",
            "reference": "repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/CONTROLLED_ABLATION_REPORT.md:7–25",
            "description": "The archived nine-pair matched pilot shows no FULL-context ASR advantage and has limited precision. This effect result does not determine policy applicability or negate the confirmed partial-task input."
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 4. MUZZLE

论文 ID：muzzle  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "muzzle\_offline\_task\_spec", "source\_group": "paper\_text", "description": "Check the disclosure of operator\-provided benign task text in offline discovery\.", "scope": \{"paper\_version": "MUZZLE USENIX Security 2026 final §§2\.3, 3\.1 and 3\.3", "experiment\_arm": "Offline discovery for the configured benign task", "artifact\_revision": "USENIX Security 2026 proceedings, documented input", "configuration": "Operator supplies the benign task in the task specification"\}, "target": \{"role": "offline discovery framework", "phase": "operator task specification intake", "source": "operator\-provided benign task", "representation": "benign task text", "operation": "receive as discovery input", "query\_form": "full\_query"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "offline discovery framework", "phase": "operator task specification intake", "source": "operator\-provided benign task", "representation": "benign task text", "operation": "receive as discovery input", "query\_form": "full\_query"\}, "permission": "allow", "reference": "§3\.1, https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=5"\}\], "matching\_observations": \[\{"edge": \{"role": "offline discovery framework", "phase": "operator task specification intake", "source": "operator\-provided benign task", "representation": "benign task text", "operation": "receive as discovery input", "query\_form": "full\_query"\}, "status": "present", "reference": "§3\.3, https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=6"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Using the operator\-supplied benign task in offline discovery exceeds MUZZLE’s declared discovery\-stage permissions\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=5", "reason": "§§2\.3 and 3\.1 specifically disclose local discovery and the operator\-provided task specification; this is a positive entitlement for the scoped discovery stage\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "training\_instance", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=6", "reason": "§3\.3 supplies the configured benign task to offline discovery\. This concerns the operator\-defined development instance, not an arbitrary future victim\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=5", "reason": "The paper specifically authorizes this offline task input\. That permission refutes the claim that this disclosed input alone violates the discovery\-stage model\."\}\}, "claim\_result": "refuted", "note": "The paper discloses the operator\-provided task for offline discovery\. This scope is distinct from online observation\."\}, \{"id": "muzzle\_online\_task\_provenance", "source\_group": "paper\_text", "description": "Check whether the stated online website privileges establish access to an arbitrary future victim's exact task\.", "scope": \{"paper\_version": "MUZZLE USENIX Security 2026 final §2\.3", "experiment\_arm": "Online deployment under standard user\-level website privileges", "artifact\_revision": "USENIX Security 2026 proceedings, online task provenance unestablished", "configuration": "Separate future victim task, as distinct from the operator\-specified lab task"\}, "target": \{"role": "standard\-privilege online attacker", "phase": "online attack execution", "source": "future victim task", "representation": "victim's exact task text", "operation": "receive as request input", "query\_form": "full\_query"\}, "verdict": "insufficient\_evidence", "reason": "information\_boundary\_issue\_not\_established", "matching\_rules": \[\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Standard online website privileges establish how an attacker obtains an arbitrary future victim’s exact task\.", "issue\_type": "acquisition\_gap", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "uncertain", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=4", "reason": "§2\.3 specifies ordinary online website privileges but does not establish a permission or acquisition mechanism for an arbitrary future task\. The offline grant cannot be extended to this different stage\.", "policy\_kind": "unspecified"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "", "reason": "No future\-task acquisition path or corresponding online request boundary was established in the reviewed paper evidence\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "§2\.3 states online website privileges without a specific entitlement to an arbitrary future task\. The documented offline input is scoped to a task supplied by the lab operator\.", "input\_provenance\_gap": \{"description": "The lab operator supplies the full task during offline discovery\. The paper leaves open how a standard\-privilege website user would obtain an equivalent task for a future online victim\.", "reference": "MUZZLE §2\.3 \(https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=4\) and §3\.3 \(https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf\#page=6\)"\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "muzzle_offline_task_spec",
    "source_group": "paper_text",
    "description": "Check the disclosure of operator-provided benign task text in offline discovery.",
    "scope": {
      "paper_version": "MUZZLE USENIX Security 2026 final §§2.3, 3.1 and 3.3",
      "experiment_arm": "Offline discovery for the configured benign task",
      "artifact_revision": "USENIX Security 2026 proceedings, documented input",
      "configuration": "Operator supplies the benign task in the task specification"
    },
    "target": {
      "role": "offline discovery framework",
      "phase": "operator task specification intake",
      "source": "operator-provided benign task",
      "representation": "benign task text",
      "operation": "receive as discovery input",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "offline discovery framework",
          "phase": "operator task specification intake",
          "source": "operator-provided benign task",
          "representation": "benign task text",
          "operation": "receive as discovery input",
          "query_form": "full_query"
        },
        "permission": "allow",
        "reference": "§3.1, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "offline discovery framework",
          "phase": "operator task specification intake",
          "source": "operator-provided benign task",
          "representation": "benign task text",
          "operation": "receive as discovery input",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "§3.3, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Using the operator-supplied benign task in offline discovery exceeds MUZZLE’s declared discovery-stage permissions.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
        "reason": "§§2.3 and 3.1 specifically disclose local discovery and the operator-provided task specification; this is a positive entitlement for the scoped discovery stage.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "training_instance",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6",
        "reason": "§3.3 supplies the configured benign task to offline discovery. This concerns the operator-defined development instance, not an arbitrary future victim."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
        "reason": "The paper specifically authorizes this offline task input. That permission refutes the claim that this disclosed input alone violates the discovery-stage model."
      }
    },
    "claim_result": "refuted",
    "note": "The paper discloses the operator-provided task for offline discovery. This scope is distinct from online observation."
  },
  {
    "id": "muzzle_online_task_provenance",
    "source_group": "paper_text",
    "description": "Check whether the stated online website privileges establish access to an arbitrary future victim's exact task.",
    "scope": {
      "paper_version": "MUZZLE USENIX Security 2026 final §2.3",
      "experiment_arm": "Online deployment under standard user-level website privileges",
      "artifact_revision": "USENIX Security 2026 proceedings, online task provenance unestablished",
      "configuration": "Separate future victim task, as distinct from the operator-specified lab task"
    },
    "target": {
      "role": "standard-privilege online attacker",
      "phase": "online attack execution",
      "source": "future victim task",
      "representation": "victim's exact task text",
      "operation": "receive as request input",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "information_boundary_issue_not_established",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Standard online website privileges establish how an attacker obtains an arbitrary future victim’s exact task.",
    "issue_type": "acquisition_gap",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4",
        "reason": "§2.3 specifies ordinary online website privileges but does not establish a permission or acquisition mechanism for an arbitrary future task. The offline grant cannot be extended to this different stage.",
        "policy_kind": "unspecified"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "",
        "reason": "No future-task acquisition path or corresponding online request boundary was established in the reviewed paper evidence."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "§2.3 states online website privileges without a specific entitlement to an arbitrary future task. The documented offline input is scoped to a task supplied by the lab operator.",
    "input_provenance_gap": {
      "description": "The lab operator supplies the full task during offline discovery. The paper leaves open how a standard-privilege website user would obtain an equivalent task for a future online victim.",
      "reference": "MUZZLE §2.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) and §3.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6)"
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "muzzle",
  "title": "MUZZLE",
  "version": "USENIX Security 2026 final",
  "audit_scope": "Specific offline operator-task entitlement and unresolved acquisition of a separate future online victim task.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 2,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [
    "muzzle_online_task_provenance"
  ],
  "claim_result_counts": {
    "refuted": 1,
    "unresolved": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [
    {
      "case_id": "muzzle_online_task_provenance",
      "description": "The lab operator supplies the full task during offline discovery. The paper leaves open how a standard-privilege website user would obtain an equivalent task for a future online victim.",
      "reference": "MUZZLE §2.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) and §3.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6)"
    }
  ],
  "evidence": [
    {
      "id": "muzzle_offline_task_spec",
      "source_group": "paper_text",
      "description": "Check the disclosure of operator-provided benign task text in offline discovery.",
      "scope": {
        "paper_version": "MUZZLE USENIX Security 2026 final §§2.3, 3.1 and 3.3",
        "experiment_arm": "Offline discovery for the configured benign task",
        "artifact_revision": "USENIX Security 2026 proceedings, documented input",
        "configuration": "Operator supplies the benign task in the task specification"
      },
      "target": {
        "role": "offline discovery framework",
        "phase": "operator task specification intake",
        "source": "operator-provided benign task",
        "representation": "benign task text",
        "operation": "receive as discovery input",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "offline discovery framework",
            "phase": "operator task specification intake",
            "source": "operator-provided benign task",
            "representation": "benign task text",
            "operation": "receive as discovery input",
            "query_form": "full_query"
          },
          "permission": "allow",
          "reference": "§3.1, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "offline discovery framework",
            "phase": "operator task specification intake",
            "source": "operator-provided benign task",
            "representation": "benign task text",
            "operation": "receive as discovery input",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "§3.3, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Using the operator-supplied benign task in offline discovery exceeds MUZZLE’s declared discovery-stage permissions.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
          "reason": "§§2.3 and 3.1 specifically disclose local discovery and the operator-provided task specification; this is a positive entitlement for the scoped discovery stage.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "training_instance",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6",
          "reason": "§3.3 supplies the configured benign task to offline discovery. This concerns the operator-defined development instance, not an arbitrary future victim."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
          "reason": "The paper specifically authorizes this offline task input. That permission refutes the claim that this disclosed input alone violates the discovery-stage model."
        }
      },
      "claim_result": "refuted",
      "note": "The paper discloses the operator-provided task for offline discovery. This scope is distinct from online observation."
    },
    {
      "id": "muzzle_online_task_provenance",
      "source_group": "paper_text",
      "description": "Check whether the stated online website privileges establish access to an arbitrary future victim's exact task.",
      "scope": {
        "paper_version": "MUZZLE USENIX Security 2026 final §2.3",
        "experiment_arm": "Online deployment under standard user-level website privileges",
        "artifact_revision": "USENIX Security 2026 proceedings, online task provenance unestablished",
        "configuration": "Separate future victim task, as distinct from the operator-specified lab task"
      },
      "target": {
        "role": "standard-privilege online attacker",
        "phase": "online attack execution",
        "source": "future victim task",
        "representation": "victim's exact task text",
        "operation": "receive as request input",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "information_boundary_issue_not_established",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Standard online website privileges establish how an attacker obtains an arbitrary future victim’s exact task.",
      "issue_type": "acquisition_gap",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4",
          "reason": "§2.3 specifies ordinary online website privileges but does not establish a permission or acquisition mechanism for an arbitrary future task. The offline grant cannot be extended to this different stage.",
          "policy_kind": "unspecified"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "",
          "reason": "No future-task acquisition path or corresponding online request boundary was established in the reviewed paper evidence."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "§2.3 states online website privileges without a specific entitlement to an arbitrary future task. The documented offline input is scoped to a task supplied by the lab operator.",
      "input_provenance_gap": {
        "description": "The lab operator supplies the full task during offline discovery. The paper leaves open how a standard-privilege website user would obtain an equivalent task for a future online victim.",
        "reference": "MUZZLE §2.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) and §3.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6)"
      }
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "muzzle_offline_task_spec",
          "source_group": "paper_text",
          "description": "Check the disclosure of operator-provided benign task text in offline discovery.",
          "scope": {
            "paper_version": "MUZZLE USENIX Security 2026 final §§2.3, 3.1 and 3.3",
            "experiment_arm": "Offline discovery for the configured benign task",
            "artifact_revision": "USENIX Security 2026 proceedings, documented input",
            "configuration": "Operator supplies the benign task in the task specification"
          },
          "target": {
            "role": "offline discovery framework",
            "phase": "operator task specification intake",
            "source": "operator-provided benign task",
            "representation": "benign task text",
            "operation": "receive as discovery input",
            "query_form": "full_query"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "offline discovery framework",
                "phase": "operator task specification intake",
                "source": "operator-provided benign task",
                "representation": "benign task text",
                "operation": "receive as discovery input",
                "query_form": "full_query"
              },
              "permission": "allow",
              "reference": "§3.1, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "offline discovery framework",
                "phase": "operator task specification intake",
                "source": "operator-provided benign task",
                "representation": "benign task text",
                "operation": "receive as discovery input",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "§3.3, https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Using the operator-supplied benign task in offline discovery exceeds MUZZLE’s declared discovery-stage permissions.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
              "reason": "§§2.3 and 3.1 specifically disclose local discovery and the operator-provided task specification; this is a positive entitlement for the scoped discovery stage.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "training_instance",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6",
              "reason": "§3.3 supplies the configured benign task to offline discovery. This concerns the operator-defined development instance, not an arbitrary future victim."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=5",
              "reason": "The paper specifically authorizes this offline task input. That permission refutes the claim that this disclosed input alone violates the discovery-stage model."
            }
          },
          "claim_result": "refuted",
          "note": "The paper discloses the operator-provided task for offline discovery. This scope is distinct from online observation."
        },
        {
          "id": "muzzle_online_task_provenance",
          "source_group": "paper_text",
          "description": "Check whether the stated online website privileges establish access to an arbitrary future victim's exact task.",
          "scope": {
            "paper_version": "MUZZLE USENIX Security 2026 final §2.3",
            "experiment_arm": "Online deployment under standard user-level website privileges",
            "artifact_revision": "USENIX Security 2026 proceedings, online task provenance unestablished",
            "configuration": "Separate future victim task, as distinct from the operator-specified lab task"
          },
          "target": {
            "role": "standard-privilege online attacker",
            "phase": "online attack execution",
            "source": "future victim task",
            "representation": "victim's exact task text",
            "operation": "receive as request input",
            "query_form": "full_query"
          },
          "verdict": "insufficient_evidence",
          "reason": "information_boundary_issue_not_established",
          "matching_rules": [],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Standard online website privileges establish how an attacker obtains an arbitrary future victim’s exact task.",
          "issue_type": "acquisition_gap",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4",
              "reason": "§2.3 specifies ordinary online website privileges but does not establish a permission or acquisition mechanism for an arbitrary future task. The offline grant cannot be extended to this different stage.",
              "policy_kind": "unspecified"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "",
              "reason": "No future-task acquisition path or corresponding online request boundary was established in the reviewed paper evidence."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "§2.3 states online website privileges without a specific entitlement to an arbitrary future task. The documented offline input is scoped to a task supplied by the lab operator.",
          "input_provenance_gap": {
            "description": "The lab operator supplies the full task during offline discovery. The paper leaves open how a standard-privilege website user would obtain an equivalent task for a future online victim.",
            "reference": "MUZZLE §2.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) and §3.3 (https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6)"
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 5. Breaking MCP with Function Hijacking Attacks \(FHA\)

论文 ID：fha  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "fha\_direct\_exact\_query", "source\_group": "paper\_text", "description": "Check construction\-side access to the exact evaluation query in the paper\-described direct single\-query FHA experiment\.", "scope": \{"paper\_version": "Breaking MCP with Function Hijacking Attacks, arXiv:2604\.20994v2, §§4 and 6\.1, Appendix B\.1", "experiment\_arm": "Direct single\-query FHA", "artifact\_revision": "Fixed arXiv v2 text only", "configuration": "Same benchmark query is used in the documented direct construction and its evaluation"\}, "target": \{"role": "attacker\-side construction procedure", "phase": "offline construction for direct evaluation", "source": "benchmark evaluation case", "representation": "exact evaluated user query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "verdict": "insufficient\_evidence", "reason": "policy\_scope\_not\_established", "matching\_rules": \[\{"edge": \{"role": "attacker\-side construction procedure", "phase": "offline construction for direct evaluation", "source": "benchmark evaluation case", "representation": "exact evaluated user query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "permission": "deny", "reference": "§4 Threat model and objectives, https://arxiv\.org/html/2604\.20994v2\#S4"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side construction procedure", "phase": "offline construction for direct evaluation", "source": "benchmark evaluation case", "representation": "exact evaluated user query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "status": "present", "reference": "§6\.1 Direct FHAs and Appendix B\.1 documented input, https://arxiv\.org/html/2604\.20994v2\#S6\.SS1 and https://arxiv\.org/html/2604\.20994v2\#A2\.SS1"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Whether the disclosed single\-payload diagnostic violates an applicable no\-query budget, rather than merely using a query\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "uncertain", "reference": "https://arxiv\.org/pdf/2604\.20994v2\#page=6; https://arxiv\.org/pdf/2604\.20994v2\#page=7", "reason": "The paper explicitly calls the §6 single\-payload experiment an initial diagnostic rather than a deployable attack\. Query delivery is confirmed, but the old generic denial does not establish the budget applicable to this diagnostic\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "same\_evaluated\_instance", "reference": "https://arxiv\.org/html/2604\.20994v2\#S6\.SS1 and https://arxiv\.org/html/2604\.20994v2\#A2\.SS1", "reason": "The direct procedure and Appendix B\.1 describe the evaluated query as a construction input\. This is paper\-method evidence, not a captured historical generator request\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "Re\-adjudicated after automated document review surfaced the explicit diagnostic qualification\. The input flow remains confirmed; the normative scope is unresolved\. Do not infer that every fixed\-query condition inherits this diagnostic exception\."\}, \{"id": "fha\_fixed\_query\_robustness", "source\_group": "paper\_text", "description": "Separate the primary fixed\-query robustness configuration from the earlier single\-payload diagnostic\.", "scope": \{"paper\_version": "FHA arXiv:2604\.20994v2 §§4 and 7, PDF pp\. 6 and 14–15", "experiment\_arm": "Primary fixed\-query multi\-payload robustness configuration; separate from §6 single\-payload diagnostics", "artifact\_revision": "Fixed arXiv v2 text only", "configuration": "A fixed query conditions construction and candidate evaluation; its scope relative to the general no\-user\-prompt statement remains unsettled"\}, "target": \{"role": "attacker\-side construction procedure", "phase": "fixed\-query robustness construction", "source": "benchmark evaluation case", "representation": "exact evaluated user query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "verdict": "insufficient\_evidence", "reason": "policy\_scope\_not\_established", "matching\_rules": \[\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side construction procedure", "phase": "fixed\-query robustness construction", "source": "benchmark evaluation case", "representation": "exact evaluated user query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "status": "present", "reference": "https://arxiv\.org/pdf/2604\.20994v2\#page=14; https://arxiv\.org/pdf/2604\.20994v2\#page=15"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Whether the fixed\-query multi\-payload robustness construction uses a query forbidden by its own applicable budget\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "uncertain", "reference": "https://arxiv\.org/pdf/2604\.20994v2\#page=6; https://arxiv\.org/pdf/2604\.20994v2\#page=14", "reason": "This primary configuration is distinct from the explicit §6 diagnostic exception\. A specific applicability argument is still required; do not invent an exception or assume the earlier one applies\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "same\_evaluated\_instance", "reference": "https://arxiv\.org/pdf/2604\.20994v2\#page=14; https://arxiv\.org/pdf/2604\.20994v2\#page=15", "reason": "The documented fixed\-query construction and optimization contexts are query\-conditioned\. This is an optimizer boundary, not proof of raw query text delivered to a separate generator LLM\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "Additional question identified by the automatic review and independently checked against the fixed paper\. No deployable or historical leakage is asserted\."\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "fha_direct_exact_query",
    "source_group": "paper_text",
    "description": "Check construction-side access to the exact evaluation query in the paper-described direct single-query FHA experiment.",
    "scope": {
      "paper_version": "Breaking MCP with Function Hijacking Attacks, arXiv:2604.20994v2, §§4 and 6.1, Appendix B.1",
      "experiment_arm": "Direct single-query FHA",
      "artifact_revision": "Fixed arXiv v2 text only",
      "configuration": "Same benchmark query is used in the documented direct construction and its evaluation"
    },
    "target": {
      "role": "attacker-side construction procedure",
      "phase": "offline construction for direct evaluation",
      "source": "benchmark evaluation case",
      "representation": "exact evaluated user query",
      "operation": "receive as construction input",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side construction procedure",
          "phase": "offline construction for direct evaluation",
          "source": "benchmark evaluation case",
          "representation": "exact evaluated user query",
          "operation": "receive as construction input",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "§4 Threat model and objectives, https://arxiv.org/html/2604.20994v2#S4"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side construction procedure",
          "phase": "offline construction for direct evaluation",
          "source": "benchmark evaluation case",
          "representation": "exact evaluated user query",
          "operation": "receive as construction input",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "§6.1 Direct FHAs and Appendix B.1 documented input, https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Whether the disclosed single-payload diagnostic violates an applicable no-query budget, rather than merely using a query.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=7",
        "reason": "The paper explicitly calls the §6 single-payload experiment an initial diagnostic rather than a deployable attack. Query delivery is confirmed, but the old generic denial does not establish the budget applicable to this diagnostic.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reference": "https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1",
        "reason": "The direct procedure and Appendix B.1 describe the evaluated query as a construction input. This is paper-method evidence, not a captured historical generator request."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "Re-adjudicated after automated document review surfaced the explicit diagnostic qualification. The input flow remains confirmed; the normative scope is unresolved. Do not infer that every fixed-query condition inherits this diagnostic exception."
  },
  {
    "id": "fha_fixed_query_robustness",
    "source_group": "paper_text",
    "description": "Separate the primary fixed-query robustness configuration from the earlier single-payload diagnostic.",
    "scope": {
      "paper_version": "FHA arXiv:2604.20994v2 §§4 and 7, PDF pp. 6 and 14–15",
      "experiment_arm": "Primary fixed-query multi-payload robustness configuration; separate from §6 single-payload diagnostics",
      "artifact_revision": "Fixed arXiv v2 text only",
      "configuration": "A fixed query conditions construction and candidate evaluation; its scope relative to the general no-user-prompt statement remains unsettled"
    },
    "target": {
      "role": "attacker-side construction procedure",
      "phase": "fixed-query robustness construction",
      "source": "benchmark evaluation case",
      "representation": "exact evaluated user query",
      "operation": "receive as construction input",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side construction procedure",
          "phase": "fixed-query robustness construction",
          "source": "benchmark evaluation case",
          "representation": "exact evaluated user query",
          "operation": "receive as construction input",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Whether the fixed-query multi-payload robustness construction uses a query forbidden by its own applicable budget.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=14",
        "reason": "This primary configuration is distinct from the explicit §6 diagnostic exception. A specific applicability argument is still required; do not invent an exception or assume the earlier one applies.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15",
        "reason": "The documented fixed-query construction and optimization contexts are query-conditioned. This is an optimizer boundary, not proof of raw query text delivered to a separate generator LLM."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "Additional question identified by the automatic review and independently checked against the fixed paper. No deployable or historical leakage is asserted."
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "fha",
  "title": "Breaking MCP with Function Hijacking Attacks (FHA)",
  "version": "arXiv:2604.20994v2",
  "audit_scope": "The disclosed §6 single-payload diagnostic and the separate §7 fixed-query multi-payload configuration; neither is equated with held-out or live user-query access.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 2,
  "resolved_checks": 0,
  "confirmed_findings": [],
  "unresolved_checks": [
    "fha_direct_exact_query",
    "fha_fixed_query_robustness"
  ],
  "claim_result_counts": {
    "unresolved": 2
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "fha_direct_exact_query",
      "source_group": "paper_text",
      "description": "Check construction-side access to the exact evaluation query in the paper-described direct single-query FHA experiment.",
      "scope": {
        "paper_version": "Breaking MCP with Function Hijacking Attacks, arXiv:2604.20994v2, §§4 and 6.1, Appendix B.1",
        "experiment_arm": "Direct single-query FHA",
        "artifact_revision": "Fixed arXiv v2 text only",
        "configuration": "Same benchmark query is used in the documented direct construction and its evaluation"
      },
      "target": {
        "role": "attacker-side construction procedure",
        "phase": "offline construction for direct evaluation",
        "source": "benchmark evaluation case",
        "representation": "exact evaluated user query",
        "operation": "receive as construction input",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side construction procedure",
            "phase": "offline construction for direct evaluation",
            "source": "benchmark evaluation case",
            "representation": "exact evaluated user query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "§4 Threat model and objectives, https://arxiv.org/html/2604.20994v2#S4"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side construction procedure",
            "phase": "offline construction for direct evaluation",
            "source": "benchmark evaluation case",
            "representation": "exact evaluated user query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "§6.1 Direct FHAs and Appendix B.1 documented input, https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Whether the disclosed single-payload diagnostic violates an applicable no-query budget, rather than merely using a query.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=7",
          "reason": "The paper explicitly calls the §6 single-payload experiment an initial diagnostic rather than a deployable attack. Query delivery is confirmed, but the old generic denial does not establish the budget applicable to this diagnostic.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reference": "https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1",
          "reason": "The direct procedure and Appendix B.1 describe the evaluated query as a construction input. This is paper-method evidence, not a captured historical generator request."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "Re-adjudicated after automated document review surfaced the explicit diagnostic qualification. The input flow remains confirmed; the normative scope is unresolved. Do not infer that every fixed-query condition inherits this diagnostic exception."
    },
    {
      "id": "fha_fixed_query_robustness",
      "source_group": "paper_text",
      "description": "Separate the primary fixed-query robustness configuration from the earlier single-payload diagnostic.",
      "scope": {
        "paper_version": "FHA arXiv:2604.20994v2 §§4 and 7, PDF pp. 6 and 14–15",
        "experiment_arm": "Primary fixed-query multi-payload robustness configuration; separate from §6 single-payload diagnostics",
        "artifact_revision": "Fixed arXiv v2 text only",
        "configuration": "A fixed query conditions construction and candidate evaluation; its scope relative to the general no-user-prompt statement remains unsettled"
      },
      "target": {
        "role": "attacker-side construction procedure",
        "phase": "fixed-query robustness construction",
        "source": "benchmark evaluation case",
        "representation": "exact evaluated user query",
        "operation": "receive as construction input",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side construction procedure",
            "phase": "fixed-query robustness construction",
            "source": "benchmark evaluation case",
            "representation": "exact evaluated user query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Whether the fixed-query multi-payload robustness construction uses a query forbidden by its own applicable budget.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=14",
          "reason": "This primary configuration is distinct from the explicit §6 diagnostic exception. A specific applicability argument is still required; do not invent an exception or assume the earlier one applies.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15",
          "reason": "The documented fixed-query construction and optimization contexts are query-conditioned. This is an optimizer boundary, not proof of raw query text delivered to a separate generator LLM."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "Additional question identified by the automatic review and independently checked against the fixed paper. No deployable or historical leakage is asserted."
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "fha_direct_exact_query",
          "source_group": "paper_text",
          "description": "Check construction-side access to the exact evaluation query in the paper-described direct single-query FHA experiment.",
          "scope": {
            "paper_version": "Breaking MCP with Function Hijacking Attacks, arXiv:2604.20994v2, §§4 and 6.1, Appendix B.1",
            "experiment_arm": "Direct single-query FHA",
            "artifact_revision": "Fixed arXiv v2 text only",
            "configuration": "Same benchmark query is used in the documented direct construction and its evaluation"
          },
          "target": {
            "role": "attacker-side construction procedure",
            "phase": "offline construction for direct evaluation",
            "source": "benchmark evaluation case",
            "representation": "exact evaluated user query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "verdict": "insufficient_evidence",
          "reason": "policy_scope_not_established",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side construction procedure",
                "phase": "offline construction for direct evaluation",
                "source": "benchmark evaluation case",
                "representation": "exact evaluated user query",
                "operation": "receive as construction input",
                "query_form": "full_query"
              },
              "permission": "deny",
              "reference": "§4 Threat model and objectives, https://arxiv.org/html/2604.20994v2#S4"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side construction procedure",
                "phase": "offline construction for direct evaluation",
                "source": "benchmark evaluation case",
                "representation": "exact evaluated user query",
                "operation": "receive as construction input",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "§6.1 Direct FHAs and Appendix B.1 documented input, https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Whether the disclosed single-payload diagnostic violates an applicable no-query budget, rather than merely using a query.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=7",
              "reason": "The paper explicitly calls the §6 single-payload experiment an initial diagnostic rather than a deployable attack. Query delivery is confirmed, but the old generic denial does not establish the budget applicable to this diagnostic.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "same_evaluated_instance",
              "reference": "https://arxiv.org/html/2604.20994v2#S6.SS1 and https://arxiv.org/html/2604.20994v2#A2.SS1",
              "reason": "The direct procedure and Appendix B.1 describe the evaluated query as a construction input. This is paper-method evidence, not a captured historical generator request."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "Re-adjudicated after automated document review surfaced the explicit diagnostic qualification. The input flow remains confirmed; the normative scope is unresolved. Do not infer that every fixed-query condition inherits this diagnostic exception."
        },
        {
          "id": "fha_fixed_query_robustness",
          "source_group": "paper_text",
          "description": "Separate the primary fixed-query robustness configuration from the earlier single-payload diagnostic.",
          "scope": {
            "paper_version": "FHA arXiv:2604.20994v2 §§4 and 7, PDF pp. 6 and 14–15",
            "experiment_arm": "Primary fixed-query multi-payload robustness configuration; separate from §6 single-payload diagnostics",
            "artifact_revision": "Fixed arXiv v2 text only",
            "configuration": "A fixed query conditions construction and candidate evaluation; its scope relative to the general no-user-prompt statement remains unsettled"
          },
          "target": {
            "role": "attacker-side construction procedure",
            "phase": "fixed-query robustness construction",
            "source": "benchmark evaluation case",
            "representation": "exact evaluated user query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "verdict": "insufficient_evidence",
          "reason": "policy_scope_not_established",
          "matching_rules": [],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side construction procedure",
                "phase": "fixed-query robustness construction",
                "source": "benchmark evaluation case",
                "representation": "exact evaluated user query",
                "operation": "receive as construction input",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Whether the fixed-query multi-payload robustness construction uses a query forbidden by its own applicable budget.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://arxiv.org/pdf/2604.20994v2#page=6; https://arxiv.org/pdf/2604.20994v2#page=14",
              "reason": "This primary configuration is distinct from the explicit §6 diagnostic exception. A specific applicability argument is still required; do not invent an exception or assume the earlier one applies.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "same_evaluated_instance",
              "reference": "https://arxiv.org/pdf/2604.20994v2#page=14; https://arxiv.org/pdf/2604.20994v2#page=15",
              "reason": "The documented fixed-query construction and optimization contexts are query-conditioned. This is an optimizer boundary, not proof of raw query text delivered to a separate generator LLM."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "Additional question identified by the automatic review and independently checked against the fixed paper. No deployable or historical leakage is asserted."
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 6. AGENTCON

论文 ID：agentcon  
运行 / 判定：有已确认的不一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "agentcon\_same\_request\_conditioned\_optimization", "source\_group": "paper\_text", "description": "Compare the original same\-request construction procedure with the stated input restrictions without claiming literal query delivery to an auxiliary generation LLM\.", "scope": \{"paper\_version": "AGENTCON, ICLR 2026 submission, hash\-identified PDF a7b8365a80d58906740ac477248926c6c6a43640, §§3, 4\.1, 4\.3 and 5\.2", "experiment\_arm": "Original\-request construction and evaluation before user\-request\-variability transfer", "artifact\_revision": "Fixed OpenReview submission URL, read through indexed paper text; no newly downloaded local PDF bytes", "configuration": "Simulated same\-request benchmark; distinct from fixed\-image evaluation on later request variants"\}, "target": \{"role": "attacker\-side construction optimizer", "phase": "offline construction for the original\-request benchmark", "source": "original benchmark request and its first\-stage intermediate plan", "representation": "query\-conditioned construction loss and intermediate plan", "operation": "condition construction updates"\}, "verdict": "inconsistent", "reason": "scoped\_forbidden\_delivery\_confirmed", "matching\_rules": \[\{"edge": \{"role": "attacker\-side construction optimizer", "phase": "offline construction for the original\-request benchmark", "source": "original benchmark request and its first\-stage intermediate plan", "representation": "query\-conditioned construction loss and intermediate plan", "operation": "condition construction updates"\}, "permission": "deny", "reference": "https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=4"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side construction optimizer", "phase": "offline construction for the original\-request benchmark", "source": "original benchmark request and its first\-stage intermediate plan", "representation": "query\-conditioned construction loss and intermediate plan", "operation": "condition construction updates"\}, "status": "present", "reference": "https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=6 and https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=9"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The original\-request benchmark constructs its image using a request\-conditioned intermediate plan and loss, despite §3 excluding access to intermediate agent outputs and exact requests\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "runtime\_trace", "policy\_application": \{"status": "applicable", "reference": "https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=4", "reason": "§3 excludes exact user requests and intermediate outputs\. §4\.1 expressly places the proposed attack under §3, and the original\-request benchmark is not separately declared an exempt stronger\-baseline arm\. The later request\-variation condition is separate\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "same\_evaluated\_instance", "reference": "https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=6 and https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=9", "reason": "§4\.3 obtains the request\-conditioned plan before construction; Eq\. 5 conditions the construction objective on the request and plan, and Implementation Considerations propagates that objective into construction updates\. §5\.2 later replaces the original request while fixing the image from the preceding successful task\. This establishes construction dependence for that original\-request arm, not merely evaluator\-side scoring\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "confirmed", "note": "Paper\-text inconsistency for the original same\-request benchmark\. The representation records query\-conditioned construction and a first\-stage plan; it does not assert raw request text was sent to an auxiliary payload\-generation LLM\. Historical code execution, production traces and future\-query access are not established\. In this paper p denotes the request and q denotes HTML\.", "input\_provenance\_gap": \{"description": "The procedure establishes original\-request benchmark construction\. How a marketplace seller obtains a specific future target request or live intermediate plan remains unresolved and is not part of the confirmed same\-request finding\.", "reference": "https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=4 and https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf\#page=6"\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "inconsistent", "reason": "confirmed\_inconsistency\_in\_scope"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "inconsistent", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "agentcon_same_request_conditioned_optimization",
    "source_group": "paper_text",
    "description": "Compare the original same-request construction procedure with the stated input restrictions without claiming literal query delivery to an auxiliary generation LLM.",
    "scope": {
      "paper_version": "AGENTCON, ICLR 2026 submission, hash-identified PDF a7b8365a80d58906740ac477248926c6c6a43640, §§3, 4.1, 4.3 and 5.2",
      "experiment_arm": "Original-request construction and evaluation before user-request-variability transfer",
      "artifact_revision": "Fixed OpenReview submission URL, read through indexed paper text; no newly downloaded local PDF bytes",
      "configuration": "Simulated same-request benchmark; distinct from fixed-image evaluation on later request variants"
    },
    "target": {
      "role": "attacker-side construction optimizer",
      "phase": "offline construction for the original-request benchmark",
      "source": "original benchmark request and its first-stage intermediate plan",
      "representation": "query-conditioned construction loss and intermediate plan",
      "operation": "condition construction updates"
    },
    "verdict": "inconsistent",
    "reason": "scoped_forbidden_delivery_confirmed",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side construction optimizer",
          "phase": "offline construction for the original-request benchmark",
          "source": "original benchmark request and its first-stage intermediate plan",
          "representation": "query-conditioned construction loss and intermediate plan",
          "operation": "condition construction updates"
        },
        "permission": "deny",
        "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side construction optimizer",
          "phase": "offline construction for the original-request benchmark",
          "source": "original benchmark request and its first-stage intermediate plan",
          "representation": "query-conditioned construction loss and intermediate plan",
          "operation": "condition construction updates"
        },
        "status": "present",
        "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The original-request benchmark constructs its image using a request-conditioned intermediate plan and loss, despite §3 excluding access to intermediate agent outputs and exact requests.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "runtime_trace",
      "policy_application": {
        "status": "applicable",
        "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4",
        "reason": "§3 excludes exact user requests and intermediate outputs. §4.1 expressly places the proposed attack under §3, and the original-request benchmark is not separately declared an exempt stronger-baseline arm. The later request-variation condition is separate.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9",
        "reason": "§4.3 obtains the request-conditioned plan before construction; Eq. 5 conditions the construction objective on the request and plan, and Implementation Considerations propagates that objective into construction updates. §5.2 later replaces the original request while fixing the image from the preceding successful task. This establishes construction dependence for that original-request arm, not merely evaluator-side scoring."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "confirmed",
    "note": "Paper-text inconsistency for the original same-request benchmark. The representation records query-conditioned construction and a first-stage plan; it does not assert raw request text was sent to an auxiliary payload-generation LLM. Historical code execution, production traces and future-query access are not established. In this paper p denotes the request and q denotes HTML.",
    "input_provenance_gap": {
      "description": "The procedure establishes original-request benchmark construction. How a marketplace seller obtains a specific future target request or live intermediate plan remains unresolved and is not part of the confirmed same-request finding.",
      "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6"
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "agentcon",
  "title": "AGENTCON",
  "version": "ICLR 2026 hash-identified OpenReview submission snapshot",
  "audit_scope": "Paper-described original same-request benchmark optimization using a request-conditioned intermediate plan/loss under §3. Literal query delivery to an auxiliary LLM, future target acquisition and live deployment are not established.",
  "verdict": "inconsistent",
  "has_confirmed_inconsistency": true,
  "reason": "confirmed_inconsistency_in_scope",
  "coverage_complete": false,
  "required_checks": 1,
  "resolved_checks": 1,
  "confirmed_findings": [
    "agentcon_same_request_conditioned_optimization"
  ],
  "unresolved_checks": [],
  "claim_result_counts": {
    "confirmed": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [
    {
      "case_id": "agentcon_same_request_conditioned_optimization",
      "description": "The procedure establishes original-request benchmark construction. How a marketplace seller obtains a specific future target request or live intermediate plan remains unresolved and is not part of the confirmed same-request finding.",
      "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6"
    }
  ],
  "evidence": [
    {
      "id": "agentcon_same_request_conditioned_optimization",
      "source_group": "paper_text",
      "description": "Compare the original same-request construction procedure with the stated input restrictions without claiming literal query delivery to an auxiliary generation LLM.",
      "scope": {
        "paper_version": "AGENTCON, ICLR 2026 submission, hash-identified PDF a7b8365a80d58906740ac477248926c6c6a43640, §§3, 4.1, 4.3 and 5.2",
        "experiment_arm": "Original-request construction and evaluation before user-request-variability transfer",
        "artifact_revision": "Fixed OpenReview submission URL, read through indexed paper text; no newly downloaded local PDF bytes",
        "configuration": "Simulated same-request benchmark; distinct from fixed-image evaluation on later request variants"
      },
      "target": {
        "role": "attacker-side construction optimizer",
        "phase": "offline construction for the original-request benchmark",
        "source": "original benchmark request and its first-stage intermediate plan",
        "representation": "query-conditioned construction loss and intermediate plan",
        "operation": "condition construction updates"
      },
      "verdict": "inconsistent",
      "reason": "scoped_forbidden_delivery_confirmed",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side construction optimizer",
            "phase": "offline construction for the original-request benchmark",
            "source": "original benchmark request and its first-stage intermediate plan",
            "representation": "query-conditioned construction loss and intermediate plan",
            "operation": "condition construction updates"
          },
          "permission": "deny",
          "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side construction optimizer",
            "phase": "offline construction for the original-request benchmark",
            "source": "original benchmark request and its first-stage intermediate plan",
            "representation": "query-conditioned construction loss and intermediate plan",
            "operation": "condition construction updates"
          },
          "status": "present",
          "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The original-request benchmark constructs its image using a request-conditioned intermediate plan and loss, despite §3 excluding access to intermediate agent outputs and exact requests.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "runtime_trace",
        "policy_application": {
          "status": "applicable",
          "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4",
          "reason": "§3 excludes exact user requests and intermediate outputs. §4.1 expressly places the proposed attack under §3, and the original-request benchmark is not separately declared an exempt stronger-baseline arm. The later request-variation condition is separate.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9",
          "reason": "§4.3 obtains the request-conditioned plan before construction; Eq. 5 conditions the construction objective on the request and plan, and Implementation Considerations propagates that objective into construction updates. §5.2 later replaces the original request while fixing the image from the preceding successful task. This establishes construction dependence for that original-request arm, not merely evaluator-side scoring."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "confirmed",
      "note": "Paper-text inconsistency for the original same-request benchmark. The representation records query-conditioned construction and a first-stage plan; it does not assert raw request text was sent to an auxiliary payload-generation LLM. Historical code execution, production traces and future-query access are not established. In this paper p denotes the request and q denotes HTML.",
      "input_provenance_gap": {
        "description": "The procedure establishes original-request benchmark construction. How a marketplace seller obtains a specific future target request or live intermediate plan remains unresolved and is not part of the confirmed same-request finding.",
        "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6"
      }
    }
  ],
  "expected": "inconsistent",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "agentcon_same_request_conditioned_optimization",
          "source_group": "paper_text",
          "description": "Compare the original same-request construction procedure with the stated input restrictions without claiming literal query delivery to an auxiliary generation LLM.",
          "scope": {
            "paper_version": "AGENTCON, ICLR 2026 submission, hash-identified PDF a7b8365a80d58906740ac477248926c6c6a43640, §§3, 4.1, 4.3 and 5.2",
            "experiment_arm": "Original-request construction and evaluation before user-request-variability transfer",
            "artifact_revision": "Fixed OpenReview submission URL, read through indexed paper text; no newly downloaded local PDF bytes",
            "configuration": "Simulated same-request benchmark; distinct from fixed-image evaluation on later request variants"
          },
          "target": {
            "role": "attacker-side construction optimizer",
            "phase": "offline construction for the original-request benchmark",
            "source": "original benchmark request and its first-stage intermediate plan",
            "representation": "query-conditioned construction loss and intermediate plan",
            "operation": "condition construction updates"
          },
          "verdict": "inconsistent",
          "reason": "scoped_forbidden_delivery_confirmed",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side construction optimizer",
                "phase": "offline construction for the original-request benchmark",
                "source": "original benchmark request and its first-stage intermediate plan",
                "representation": "query-conditioned construction loss and intermediate plan",
                "operation": "condition construction updates"
              },
              "permission": "deny",
              "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side construction optimizer",
                "phase": "offline construction for the original-request benchmark",
                "source": "original benchmark request and its first-stage intermediate plan",
                "representation": "query-conditioned construction loss and intermediate plan",
                "operation": "condition construction updates"
              },
              "status": "present",
              "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The original-request benchmark constructs its image using a request-conditioned intermediate plan and loss, despite §3 excluding access to intermediate agent outputs and exact requests.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "runtime_trace",
            "policy_application": {
              "status": "applicable",
              "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4",
              "reason": "§3 excludes exact user requests and intermediate outputs. §4.1 expressly places the proposed attack under §3, and the original-request benchmark is not separately declared an exempt stronger-baseline arm. The later request-variation condition is separate.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "same_evaluated_instance",
              "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9",
              "reason": "§4.3 obtains the request-conditioned plan before construction; Eq. 5 conditions the construction objective on the request and plan, and Implementation Considerations propagates that objective into construction updates. §5.2 later replaces the original request while fixing the image from the preceding successful task. This establishes construction dependence for that original-request arm, not merely evaluator-side scoring."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "confirmed",
          "note": "Paper-text inconsistency for the original same-request benchmark. The representation records query-conditioned construction and a first-stage plan; it does not assert raw request text was sent to an auxiliary payload-generation LLM. Historical code execution, production traces and future-query access are not established. In this paper p denotes the request and q denotes HTML.",
          "input_provenance_gap": {
            "description": "The procedure establishes original-request benchmark construction. How a marketplace seller obtains a specific future target request or live intermediate plan remains unresolved and is not part of the confirmed same-request finding.",
            "reference": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4 and https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6"
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "inconsistent",
      "reason": "confirmed_inconsistency_in_scope"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "inconsistent",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 7. Overcoming the Retrieval Barrier

论文 ID：retrieval\_barrier  
运行 / 判定：审计范围内一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "retrieval\_barrier\_declared\_query", "source\_group": "paper\_text", "description": "Check the use of a supplied target query inside the paper's explicitly query\-conditioned retrieval evaluation\.", "scope": \{"paper\_version": "Overcoming the Retrieval Barrier, USENIX Security 2026 proceedings, §§2\.1 and 4\.1", "experiment\_arm": "Given\-query retrieval benchmark", "artifact\_revision": "Fixed USENIX proceedings PDF only", "configuration": "Selected dataset queries supplied as target inputs under the paper's retrieval procedure"\}, "target": \{"role": "attacker\-side retrieval construction procedure", "phase": "offline construction for retrieval evaluation", "source": "benchmark\-selected target query", "representation": "exact selected query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "attacker\-side retrieval construction procedure", "phase": "offline construction for retrieval evaluation", "source": "benchmark\-selected target query", "representation": "exact selected query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "permission": "allow", "reference": "§2\.1 Problem Definition 1 states that the query is given \(proceedings p\. 1569\), https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=4"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side retrieval construction procedure", "phase": "offline construction for retrieval evaluation", "source": "benchmark\-selected target query", "representation": "exact selected query", "operation": "receive as construction input", "query\_form": "full\_query"\}, "status": "present", "reference": "§4\.1 benchmark sampling and reported per\-target\-query evaluation \(proceedings pp\. 1571–1572\), https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=6"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Using the supplied target query in the given\-query retrieval benchmark violates its black\-box access restrictions\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=4", "reason": "§2\.1 explicitly gives the query to the scoped construction procedure\. Its black\-box limitations concern corpus contents and model parameters, rather than withholding this query\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "same\_evaluated\_instance", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=6", "reason": "§4\.1 samples and supplies target queries for the documented query\-conditioned evaluation\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=4", "reason": "The explicit given\-query entitlement refutes the claim that use of that supplied query itself violates the benchmark restrictions\. It does not establish future query acquisition at deployment\."\}\}, "claim\_result": "refuted", "note": "The documented black\-box restrictions concern the external corpus and model parameters\. §5\.2 separately reports retrospective FAQ construction and possible agent\-side rewrites\.", "input\_provenance\_gap": \{"description": "The benchmark assumes the query is given\. The query\-conditioned result leaves open how an external actor obtains an exact future query in deployment\.", "reference": "Overcoming the Retrieval Barrier §2\.1 \(https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=4\) and §5\.2 \(https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf\#page=12\)"\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "consistent\_within\_scope", "reason": "all\_required\_checks\_consistent"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "consistent\_within\_scope", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "retrieval_barrier_declared_query",
    "source_group": "paper_text",
    "description": "Check the use of a supplied target query inside the paper's explicitly query-conditioned retrieval evaluation.",
    "scope": {
      "paper_version": "Overcoming the Retrieval Barrier, USENIX Security 2026 proceedings, §§2.1 and 4.1",
      "experiment_arm": "Given-query retrieval benchmark",
      "artifact_revision": "Fixed USENIX proceedings PDF only",
      "configuration": "Selected dataset queries supplied as target inputs under the paper's retrieval procedure"
    },
    "target": {
      "role": "attacker-side retrieval construction procedure",
      "phase": "offline construction for retrieval evaluation",
      "source": "benchmark-selected target query",
      "representation": "exact selected query",
      "operation": "receive as construction input",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side retrieval construction procedure",
          "phase": "offline construction for retrieval evaluation",
          "source": "benchmark-selected target query",
          "representation": "exact selected query",
          "operation": "receive as construction input",
          "query_form": "full_query"
        },
        "permission": "allow",
        "reference": "§2.1 Problem Definition 1 states that the query is given (proceedings p. 1569), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side retrieval construction procedure",
          "phase": "offline construction for retrieval evaluation",
          "source": "benchmark-selected target query",
          "representation": "exact selected query",
          "operation": "receive as construction input",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "§4.1 benchmark sampling and reported per-target-query evaluation (proceedings pp. 1571–1572), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Using the supplied target query in the given-query retrieval benchmark violates its black-box access restrictions.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
        "reason": "§2.1 explicitly gives the query to the scoped construction procedure. Its black-box limitations concern corpus contents and model parameters, rather than withholding this query.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "same_evaluated_instance",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6",
        "reason": "§4.1 samples and supplies target queries for the documented query-conditioned evaluation."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
        "reason": "The explicit given-query entitlement refutes the claim that use of that supplied query itself violates the benchmark restrictions. It does not establish future query acquisition at deployment."
      }
    },
    "claim_result": "refuted",
    "note": "The documented black-box restrictions concern the external corpus and model parameters. §5.2 separately reports retrospective FAQ construction and possible agent-side rewrites.",
    "input_provenance_gap": {
      "description": "The benchmark assumes the query is given. The query-conditioned result leaves open how an external actor obtains an exact future query in deployment.",
      "reference": "Overcoming the Retrieval Barrier §2.1 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) and §5.2 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=12)"
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "retrieval_barrier",
  "title": "Overcoming the Retrieval Barrier",
  "version": "USENIX Security 2026 final",
  "audit_scope": "Only the explicitly given-query retrieval benchmark: assess the allegation that using its supplied query violates its black-box restrictions. Future-query deployment acquisition is a separate metadata gap.",
  "verdict": "consistent_within_scope",
  "has_confirmed_inconsistency": false,
  "reason": "all_required_checks_consistent",
  "coverage_complete": true,
  "required_checks": 1,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [],
  "claim_result_counts": {
    "refuted": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [
    {
      "case_id": "retrieval_barrier_declared_query",
      "description": "The benchmark assumes the query is given. The query-conditioned result leaves open how an external actor obtains an exact future query in deployment.",
      "reference": "Overcoming the Retrieval Barrier §2.1 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) and §5.2 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=12)"
    }
  ],
  "evidence": [
    {
      "id": "retrieval_barrier_declared_query",
      "source_group": "paper_text",
      "description": "Check the use of a supplied target query inside the paper's explicitly query-conditioned retrieval evaluation.",
      "scope": {
        "paper_version": "Overcoming the Retrieval Barrier, USENIX Security 2026 proceedings, §§2.1 and 4.1",
        "experiment_arm": "Given-query retrieval benchmark",
        "artifact_revision": "Fixed USENIX proceedings PDF only",
        "configuration": "Selected dataset queries supplied as target inputs under the paper's retrieval procedure"
      },
      "target": {
        "role": "attacker-side retrieval construction procedure",
        "phase": "offline construction for retrieval evaluation",
        "source": "benchmark-selected target query",
        "representation": "exact selected query",
        "operation": "receive as construction input",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side retrieval construction procedure",
            "phase": "offline construction for retrieval evaluation",
            "source": "benchmark-selected target query",
            "representation": "exact selected query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "permission": "allow",
          "reference": "§2.1 Problem Definition 1 states that the query is given (proceedings p. 1569), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side retrieval construction procedure",
            "phase": "offline construction for retrieval evaluation",
            "source": "benchmark-selected target query",
            "representation": "exact selected query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "§4.1 benchmark sampling and reported per-target-query evaluation (proceedings pp. 1571–1572), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Using the supplied target query in the given-query retrieval benchmark violates its black-box access restrictions.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
          "reason": "§2.1 explicitly gives the query to the scoped construction procedure. Its black-box limitations concern corpus contents and model parameters, rather than withholding this query.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "same_evaluated_instance",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6",
          "reason": "§4.1 samples and supplies target queries for the documented query-conditioned evaluation."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
          "reason": "The explicit given-query entitlement refutes the claim that use of that supplied query itself violates the benchmark restrictions. It does not establish future query acquisition at deployment."
        }
      },
      "claim_result": "refuted",
      "note": "The documented black-box restrictions concern the external corpus and model parameters. §5.2 separately reports retrospective FAQ construction and possible agent-side rewrites.",
      "input_provenance_gap": {
        "description": "The benchmark assumes the query is given. The query-conditioned result leaves open how an external actor obtains an exact future query in deployment.",
        "reference": "Overcoming the Retrieval Barrier §2.1 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) and §5.2 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=12)"
      }
    }
  ],
  "expected": "consistent_within_scope",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "retrieval_barrier_declared_query",
          "source_group": "paper_text",
          "description": "Check the use of a supplied target query inside the paper's explicitly query-conditioned retrieval evaluation.",
          "scope": {
            "paper_version": "Overcoming the Retrieval Barrier, USENIX Security 2026 proceedings, §§2.1 and 4.1",
            "experiment_arm": "Given-query retrieval benchmark",
            "artifact_revision": "Fixed USENIX proceedings PDF only",
            "configuration": "Selected dataset queries supplied as target inputs under the paper's retrieval procedure"
          },
          "target": {
            "role": "attacker-side retrieval construction procedure",
            "phase": "offline construction for retrieval evaluation",
            "source": "benchmark-selected target query",
            "representation": "exact selected query",
            "operation": "receive as construction input",
            "query_form": "full_query"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side retrieval construction procedure",
                "phase": "offline construction for retrieval evaluation",
                "source": "benchmark-selected target query",
                "representation": "exact selected query",
                "operation": "receive as construction input",
                "query_form": "full_query"
              },
              "permission": "allow",
              "reference": "§2.1 Problem Definition 1 states that the query is given (proceedings p. 1569), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side retrieval construction procedure",
                "phase": "offline construction for retrieval evaluation",
                "source": "benchmark-selected target query",
                "representation": "exact selected query",
                "operation": "receive as construction input",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "§4.1 benchmark sampling and reported per-target-query evaluation (proceedings pp. 1571–1572), https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Using the supplied target query in the given-query retrieval benchmark violates its black-box access restrictions.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
              "reason": "§2.1 explicitly gives the query to the scoped construction procedure. Its black-box limitations concern corpus contents and model parameters, rather than withholding this query.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "same_evaluated_instance",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6",
              "reason": "§4.1 samples and supplies target queries for the documented query-conditioned evaluation."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4",
              "reason": "The explicit given-query entitlement refutes the claim that use of that supplied query itself violates the benchmark restrictions. It does not establish future query acquisition at deployment."
            }
          },
          "claim_result": "refuted",
          "note": "The documented black-box restrictions concern the external corpus and model parameters. §5.2 separately reports retrospective FAQ construction and possible agent-side rewrites.",
          "input_provenance_gap": {
            "description": "The benchmark assumes the query is given. The query-conditioned result leaves open how an external actor obtains an exact future query in deployment.",
            "reference": "Overcoming the Retrieval Barrier §2.1 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) and §5.2 (https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=12)"
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "consistent_within_scope",
      "reason": "all_required_checks_consistent"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "consistent_within_scope",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 8. Glue Pizza and Eat Rocks \(LIAR\)

论文 ID：liar  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 3\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "liar\_same\_benchmark\_source\_kb", "source\_group": "paper\_text", "description": "Apply the specific source\-training grant to the disclosed source subset; do not infer target access from the benchmark name\.", "scope": \{"paper\_version": "Glue pizza and eat rocks \(LIAR\), EMNLP 2024 proceedings, ACL Anthology 2024\.emnlp\-main\.96", "experiment\_arm": "Table 1, Natural Questions as both source and target database", "artifact\_revision": "Final published paper\. Implementation and historical run artifacts were outside this evidence review\.", "configuration": "Offline construction using the disclosed training subset of the same named benchmark corpus as evaluation"\}, "target": \{"role": "attacker\-side training procedure", "phase": "offline construction", "source": "Natural Questions source knowledge\-base training subset in the NQ\-to\-NQ condition", "representation": "documents from the knowledge base", "operation": "read as training input"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "attacker\-side training procedure", "phase": "offline construction", "source": "Natural Questions source knowledge\-base training subset in the NQ\-to\-NQ condition", "representation": "documents from the knowledge base", "operation": "read as training input"\}, "permission": "allow", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side training procedure", "phase": "offline construction", "source": "Natural Questions source knowledge\-base training subset in the NQ\-to\-NQ condition", "representation": "documents from the knowledge base", "operation": "read as training input"\}, "status": "present", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5 \(§5\.2\) and https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=7 \(Table 1\)"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "Reading the explicitly supplied source knowledge\-base training subset in LIAR’s same\-named\-benchmark condition violates the paper’s access restrictions\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "document\_content", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5", "reason": "§5\.2 specifically authorizes a training subset of a source knowledge base\. That specific source\-stage entitlement must be applied rather than substituting §3\.1’s general target\-access limitation\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "paper\_procedure", "task\_relation": "training\_instance", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5 and https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=7", "reason": "§5\.2 discloses source training documents; Table 1 identifies the same benchmark name in some source/target conditions\. The latter does not prove document or live\-index identity\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5", "reason": "Specific source\-training access is an explicit entitlement\. This refutes the scoped allegation against the disclosed source subset, without proving target\-access or document\-disjointness claims\."\}\}, "claim\_result": "refuted", "note": "The source\-training entitlement refutes this specific access allegation\. Target database reads and source/target document overlap remain separate unresolved checks\. No implementation or historical\-run evidence was reviewed for these identity questions\."\}, \{"id": "liar\_target\_kb\_direct\_access", "source\_group": "paper\_text", "description": "Check direct target access separately from disclosed source access\.", "scope": \{"paper\_version": "Glue pizza and eat rocks \(LIAR\), EMNLP 2024 proceedings, ACL Anthology 2024\.emnlp\-main\.96", "experiment\_arm": "Same\-named source/target benchmark condition, with target object identity unestablished", "artifact\_revision": "Final published paper\. Implementation and historical run artifacts were outside this evidence review\.", "configuration": "Distinguish authorized source training subset from the restricted target database or index"\}, "target": \{"role": "attacker\-side training procedure", "phase": "offline construction", "source": "restricted target knowledge base or live target index", "representation": "target database documents", "operation": "read directly as construction input"\}, "verdict": "insufficient\_evidence", "reason": "evaluated\_instance\_alignment\_not\_established", "matching\_rules": \[\{"edge": \{"role": "attacker\-side training procedure", "phase": "offline construction", "source": "restricted target knowledge base or live target index", "representation": "target database documents", "operation": "read directly as construction input"\}, "permission": "deny", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=3"\}\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The construction procedure directly reads the restricted target knowledge base rather than the expressly authorized source training subset\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "document\_content", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=3", "reason": "§3\.1 restricts direct access to target knowledge\-base contents\. §5\.2’s narrower grant concerns source training data and does not itself authorize a direct read of the target object\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "", "reason": "The paper evidence identifies a source subset and benchmark names, but does not bind a construction read to the restricted target database or its live index\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "No direct target\-read observation is inferred from the same benchmark name; no absence is asserted\."\}, \{"id": "liar\_source\_target\_document\_overlap", "source\_group": "paper\_text", "description": "Keep document\-level identity unresolved instead of converting benchmark\-name equality into an observed target read\.", "scope": \{"paper\_version": "Glue pizza and eat rocks \(LIAR\), EMNLP 2024 proceedings, ACL Anthology 2024\.emnlp\-main\.96", "experiment\_arm": "Same\-named source/target benchmark condition, with target object identity unestablished", "artifact\_revision": "Final published paper\. Implementation and historical run artifacts were outside this evidence review\.", "configuration": "Distinguish authorized source training subset from the restricted target database or index"\}, "target": \{"role": "attacker\-side training procedure", "phase": "offline source\-data selection", "source": "source and target benchmark corpus objects", "representation": "document\-level source/target identity or overlap", "operation": "use target\-identical documents in construction"\}, "verdict": "insufficient\_evidence", "reason": "information\_boundary\_issue\_not\_established", "matching\_rules": \[\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The same benchmark label establishes that LIAR’s construction documents overlap the restricted target documents\.", "issue\_type": "acquisition\_gap", "assessment": \{"information\_level": "document\_content", "policy\_application": \{"status": "uncertain", "reference": "https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=5 and https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf\#page=7", "reason": "Applying the target restriction requires identity and scope evidence for the particular documents\. The source entitlement and same\-name table do not supply that binding\. No independent universal disjointness rule is invented\.", "policy\_kind": "unspecified"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "document\_presence", "task\_relation": "unknown", "reference": "", "reason": "Table 1 identifies benchmark names, not document\-level membership, splitting or live\-index identity\. No object\-level overlap evidence was established\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "This record does not assert that overlap is absent or intrinsically prohibited\. It records the unresolved object\-identity premise needed for the target\-access allegation\."\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "liar_same_benchmark_source_kb",
    "source_group": "paper_text",
    "description": "Apply the specific source-training grant to the disclosed source subset; do not infer target access from the benchmark name.",
    "scope": {
      "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
      "experiment_arm": "Table 1, Natural Questions as both source and target database",
      "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
      "configuration": "Offline construction using the disclosed training subset of the same named benchmark corpus as evaluation"
    },
    "target": {
      "role": "attacker-side training procedure",
      "phase": "offline construction",
      "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
      "representation": "documents from the knowledge base",
      "operation": "read as training input"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side training procedure",
          "phase": "offline construction",
          "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
          "representation": "documents from the knowledge base",
          "operation": "read as training input"
        },
        "permission": "allow",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side training procedure",
          "phase": "offline construction",
          "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
          "representation": "documents from the knowledge base",
          "operation": "read as training input"
        },
        "status": "present",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 (§5.2) and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7 (Table 1)"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "Reading the explicitly supplied source knowledge-base training subset in LIAR’s same-named-benchmark condition violates the paper’s access restrictions.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
        "reason": "§5.2 specifically authorizes a training subset of a source knowledge base. That specific source-stage entitlement must be applied rather than substituting §3.1’s general target-access limitation.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "paper_procedure",
        "task_relation": "training_instance",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
        "reason": "§5.2 discloses source training documents; Table 1 identifies the same benchmark name in some source/target conditions. The latter does not prove document or live-index identity."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
        "reason": "Specific source-training access is an explicit entitlement. This refutes the scoped allegation against the disclosed source subset, without proving target-access or document-disjointness claims."
      }
    },
    "claim_result": "refuted",
    "note": "The source-training entitlement refutes this specific access allegation. Target database reads and source/target document overlap remain separate unresolved checks. No implementation or historical-run evidence was reviewed for these identity questions."
  },
  {
    "id": "liar_target_kb_direct_access",
    "source_group": "paper_text",
    "description": "Check direct target access separately from disclosed source access.",
    "scope": {
      "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
      "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
      "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
      "configuration": "Distinguish authorized source training subset from the restricted target database or index"
    },
    "target": {
      "role": "attacker-side training procedure",
      "phase": "offline construction",
      "source": "restricted target knowledge base or live target index",
      "representation": "target database documents",
      "operation": "read directly as construction input"
    },
    "verdict": "insufficient_evidence",
    "reason": "evaluated_instance_alignment_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side training procedure",
          "phase": "offline construction",
          "source": "restricted target knowledge base or live target index",
          "representation": "target database documents",
          "operation": "read directly as construction input"
        },
        "permission": "deny",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The construction procedure directly reads the restricted target knowledge base rather than the expressly authorized source training subset.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3",
        "reason": "§3.1 restricts direct access to target knowledge-base contents. §5.2’s narrower grant concerns source training data and does not itself authorize a direct read of the target object.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "",
        "reason": "The paper evidence identifies a source subset and benchmark names, but does not bind a construction read to the restricted target database or its live index."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "No direct target-read observation is inferred from the same benchmark name; no absence is asserted."
  },
  {
    "id": "liar_source_target_document_overlap",
    "source_group": "paper_text",
    "description": "Keep document-level identity unresolved instead of converting benchmark-name equality into an observed target read.",
    "scope": {
      "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
      "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
      "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
      "configuration": "Distinguish authorized source training subset from the restricted target database or index"
    },
    "target": {
      "role": "attacker-side training procedure",
      "phase": "offline source-data selection",
      "source": "source and target benchmark corpus objects",
      "representation": "document-level source/target identity or overlap",
      "operation": "use target-identical documents in construction"
    },
    "verdict": "insufficient_evidence",
    "reason": "information_boundary_issue_not_established",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The same benchmark label establishes that LIAR’s construction documents overlap the restricted target documents.",
    "issue_type": "acquisition_gap",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
        "reason": "Applying the target restriction requires identity and scope evidence for the particular documents. The source entitlement and same-name table do not supply that binding. No independent universal disjointness rule is invented.",
        "policy_kind": "unspecified"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "document_presence",
        "task_relation": "unknown",
        "reference": "",
        "reason": "Table 1 identifies benchmark names, not document-level membership, splitting or live-index identity. No object-level overlap evidence was established."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "This record does not assert that overlap is absent or intrinsically prohibited. It records the unresolved object-identity premise needed for the target-access allegation."
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "liar",
  "title": "Glue Pizza and Eat Rocks (LIAR)",
  "version": "EMNLP 2024 final",
  "audit_scope": "Specific source-training grant, alleged direct target-database access and unresolved document identity/overlap. Same benchmark names do not establish target-object reads.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 3,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [
    "liar_target_kb_direct_access",
    "liar_source_target_document_overlap"
  ],
  "claim_result_counts": {
    "refuted": 1,
    "unresolved": 2
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "liar_same_benchmark_source_kb",
      "source_group": "paper_text",
      "description": "Apply the specific source-training grant to the disclosed source subset; do not infer target access from the benchmark name.",
      "scope": {
        "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
        "experiment_arm": "Table 1, Natural Questions as both source and target database",
        "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
        "configuration": "Offline construction using the disclosed training subset of the same named benchmark corpus as evaluation"
      },
      "target": {
        "role": "attacker-side training procedure",
        "phase": "offline construction",
        "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
        "representation": "documents from the knowledge base",
        "operation": "read as training input"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side training procedure",
            "phase": "offline construction",
            "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
            "representation": "documents from the knowledge base",
            "operation": "read as training input"
          },
          "permission": "allow",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side training procedure",
            "phase": "offline construction",
            "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
            "representation": "documents from the knowledge base",
            "operation": "read as training input"
          },
          "status": "present",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 (§5.2) and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7 (Table 1)"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "Reading the explicitly supplied source knowledge-base training subset in LIAR’s same-named-benchmark condition violates the paper’s access restrictions.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
          "reason": "§5.2 specifically authorizes a training subset of a source knowledge base. That specific source-stage entitlement must be applied rather than substituting §3.1’s general target-access limitation.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "paper_procedure",
          "task_relation": "training_instance",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
          "reason": "§5.2 discloses source training documents; Table 1 identifies the same benchmark name in some source/target conditions. The latter does not prove document or live-index identity."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
          "reason": "Specific source-training access is an explicit entitlement. This refutes the scoped allegation against the disclosed source subset, without proving target-access or document-disjointness claims."
        }
      },
      "claim_result": "refuted",
      "note": "The source-training entitlement refutes this specific access allegation. Target database reads and source/target document overlap remain separate unresolved checks. No implementation or historical-run evidence was reviewed for these identity questions."
    },
    {
      "id": "liar_target_kb_direct_access",
      "source_group": "paper_text",
      "description": "Check direct target access separately from disclosed source access.",
      "scope": {
        "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
        "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
        "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
        "configuration": "Distinguish authorized source training subset from the restricted target database or index"
      },
      "target": {
        "role": "attacker-side training procedure",
        "phase": "offline construction",
        "source": "restricted target knowledge base or live target index",
        "representation": "target database documents",
        "operation": "read directly as construction input"
      },
      "verdict": "insufficient_evidence",
      "reason": "evaluated_instance_alignment_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side training procedure",
            "phase": "offline construction",
            "source": "restricted target knowledge base or live target index",
            "representation": "target database documents",
            "operation": "read directly as construction input"
          },
          "permission": "deny",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The construction procedure directly reads the restricted target knowledge base rather than the expressly authorized source training subset.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3",
          "reason": "§3.1 restricts direct access to target knowledge-base contents. §5.2’s narrower grant concerns source training data and does not itself authorize a direct read of the target object.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "",
          "reason": "The paper evidence identifies a source subset and benchmark names, but does not bind a construction read to the restricted target database or its live index."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "No direct target-read observation is inferred from the same benchmark name; no absence is asserted."
    },
    {
      "id": "liar_source_target_document_overlap",
      "source_group": "paper_text",
      "description": "Keep document-level identity unresolved instead of converting benchmark-name equality into an observed target read.",
      "scope": {
        "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
        "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
        "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
        "configuration": "Distinguish authorized source training subset from the restricted target database or index"
      },
      "target": {
        "role": "attacker-side training procedure",
        "phase": "offline source-data selection",
        "source": "source and target benchmark corpus objects",
        "representation": "document-level source/target identity or overlap",
        "operation": "use target-identical documents in construction"
      },
      "verdict": "insufficient_evidence",
      "reason": "information_boundary_issue_not_established",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The same benchmark label establishes that LIAR’s construction documents overlap the restricted target documents.",
      "issue_type": "acquisition_gap",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
          "reason": "Applying the target restriction requires identity and scope evidence for the particular documents. The source entitlement and same-name table do not supply that binding. No independent universal disjointness rule is invented.",
          "policy_kind": "unspecified"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "document_presence",
          "task_relation": "unknown",
          "reference": "",
          "reason": "Table 1 identifies benchmark names, not document-level membership, splitting or live-index identity. No object-level overlap evidence was established."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "This record does not assert that overlap is absent or intrinsically prohibited. It records the unresolved object-identity premise needed for the target-access allegation."
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 3
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "liar_same_benchmark_source_kb",
          "source_group": "paper_text",
          "description": "Apply the specific source-training grant to the disclosed source subset; do not infer target access from the benchmark name.",
          "scope": {
            "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
            "experiment_arm": "Table 1, Natural Questions as both source and target database",
            "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
            "configuration": "Offline construction using the disclosed training subset of the same named benchmark corpus as evaluation"
          },
          "target": {
            "role": "attacker-side training procedure",
            "phase": "offline construction",
            "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
            "representation": "documents from the knowledge base",
            "operation": "read as training input"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side training procedure",
                "phase": "offline construction",
                "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
                "representation": "documents from the knowledge base",
                "operation": "read as training input"
              },
              "permission": "allow",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side training procedure",
                "phase": "offline construction",
                "source": "Natural Questions source knowledge-base training subset in the NQ-to-NQ condition",
                "representation": "documents from the knowledge base",
                "operation": "read as training input"
              },
              "status": "present",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 (§5.2) and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7 (Table 1)"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "Reading the explicitly supplied source knowledge-base training subset in LIAR’s same-named-benchmark condition violates the paper’s access restrictions.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "document_content",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
              "reason": "§5.2 specifically authorizes a training subset of a source knowledge base. That specific source-stage entitlement must be applied rather than substituting §3.1’s general target-access limitation.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "paper_procedure",
              "task_relation": "training_instance",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
              "reason": "§5.2 discloses source training documents; Table 1 identifies the same benchmark name in some source/target conditions. The latter does not prove document or live-index identity."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5",
              "reason": "Specific source-training access is an explicit entitlement. This refutes the scoped allegation against the disclosed source subset, without proving target-access or document-disjointness claims."
            }
          },
          "claim_result": "refuted",
          "note": "The source-training entitlement refutes this specific access allegation. Target database reads and source/target document overlap remain separate unresolved checks. No implementation or historical-run evidence was reviewed for these identity questions."
        },
        {
          "id": "liar_target_kb_direct_access",
          "source_group": "paper_text",
          "description": "Check direct target access separately from disclosed source access.",
          "scope": {
            "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
            "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
            "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
            "configuration": "Distinguish authorized source training subset from the restricted target database or index"
          },
          "target": {
            "role": "attacker-side training procedure",
            "phase": "offline construction",
            "source": "restricted target knowledge base or live target index",
            "representation": "target database documents",
            "operation": "read directly as construction input"
          },
          "verdict": "insufficient_evidence",
          "reason": "evaluated_instance_alignment_not_established",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side training procedure",
                "phase": "offline construction",
                "source": "restricted target knowledge base or live target index",
                "representation": "target database documents",
                "operation": "read directly as construction input"
              },
              "permission": "deny",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3"
            }
          ],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The construction procedure directly reads the restricted target knowledge base rather than the expressly authorized source training subset.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "document_content",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=3",
              "reason": "§3.1 restricts direct access to target knowledge-base contents. §5.2’s narrower grant concerns source training data and does not itself authorize a direct read of the target object.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "",
              "reason": "The paper evidence identifies a source subset and benchmark names, but does not bind a construction read to the restricted target database or its live index."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "No direct target-read observation is inferred from the same benchmark name; no absence is asserted."
        },
        {
          "id": "liar_source_target_document_overlap",
          "source_group": "paper_text",
          "description": "Keep document-level identity unresolved instead of converting benchmark-name equality into an observed target read.",
          "scope": {
            "paper_version": "Glue pizza and eat rocks (LIAR), EMNLP 2024 proceedings, ACL Anthology 2024.emnlp-main.96",
            "experiment_arm": "Same-named source/target benchmark condition, with target object identity unestablished",
            "artifact_revision": "Final published paper. Implementation and historical run artifacts were outside this evidence review.",
            "configuration": "Distinguish authorized source training subset from the restricted target database or index"
          },
          "target": {
            "role": "attacker-side training procedure",
            "phase": "offline source-data selection",
            "source": "source and target benchmark corpus objects",
            "representation": "document-level source/target identity or overlap",
            "operation": "use target-identical documents in construction"
          },
          "verdict": "insufficient_evidence",
          "reason": "information_boundary_issue_not_established",
          "matching_rules": [],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The same benchmark label establishes that LIAR’s construction documents overlap the restricted target documents.",
          "issue_type": "acquisition_gap",
          "assessment": {
            "information_level": "document_content",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://aclanthology.org/2024.emnlp-main.96.pdf#page=5 and https://aclanthology.org/2024.emnlp-main.96.pdf#page=7",
              "reason": "Applying the target restriction requires identity and scope evidence for the particular documents. The source entitlement and same-name table do not supply that binding. No independent universal disjointness rule is invented.",
              "policy_kind": "unspecified"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "document_presence",
              "task_relation": "unknown",
              "reference": "",
              "reason": "Table 1 identifies benchmark names, not document-level membership, splitting or live-index identity. No object-level overlap evidence was established."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "This record does not assert that overlap is absent or intrinsically prohibited. It records the unresolved object-identity premise needed for the target-access allegation."
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 9. ObliInjection

论文 ID：obliinjection  
运行 / 判定：有已确认的不一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "obli\_released\_optimizer\_full\_target\_query", "source\_group": "archived", "description": "Check if the released HotpotQA optimizer uses the complete question used by evaluation for the same selected case\.", "scope": \{"paper\_version": "ObliInjection arXiv:2512\.09321v3, §§III\-B, IV and V\-A, Appendix Table XI", "experiment\_arm": "Released HotpotQA optimization and evaluation data flow", "artifact\_revision": "Public release b1f6a3f48c0cf121534374cbcef453832594867b", "configuration": "Released HotpotQA JSON prepared by the shipped loader, with the same selected case for optimization and evaluation"\}, "target": \{"role": "attacker\-side optimizer", "phase": "optimization before evaluation", "source": "selected target\-question record in the released HotpotQA evaluation data", "representation": "full evaluation\-matched target question", "operation": "read as optimization input", "query\_form": "full\_query"\}, "verdict": "inconsistent", "reason": "scoped\_forbidden\_delivery\_confirmed", "matching\_rules": \[\{"edge": \{"role": "attacker\-side optimizer", "phase": "optimization before evaluation", "source": "selected target\-question record in the released HotpotQA evaluation data", "representation": "full evaluation\-matched target question", "operation": "read as optimization input", "query\_form": "full\_query"\}, "permission": "deny", "reference": "papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:209–214; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:245–255; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:655–665; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:1164–1173"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side optimizer", "phase": "optimization before evaluation", "source": "selected target\-question record in the released HotpotQA evaluation data", "representation": "full evaluation\-matched target question", "operation": "read as optimization input", "query\_form": "full\_query"\}, "status": "present", "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task\_configs/hotpotqa\_config\.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection\.py:33–47; papers/ObliInjection/audit/dataflow/dataflow\.md:12–34; repository/obli\-gpt4o\-ac\-transfer\-20261031/papers/ObliInjection/reproduction/three\_arm\_pilot\_15\_v1/REPORT\.md:47–53"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The released HotpotQA optimizer receives the full evaluation\-matched target question beyond the documented question\-type\-driven surrogate construction\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:209–214; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:245–255; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:655–665; papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:1164–1173", "reason": "The scoped method constructs a surrogate from question\-type metadata\. Full text of the question used in the same target evaluation exceeds that described construction\."\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task\_configs/hotpotqa\_config\.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection\.py:33–47; papers/ObliInjection/audit/dataflow/dataflow\.md:12–34; repository/obli\-gpt4o\-ac\-transfer\-20261031/papers/ObliInjection/reproduction/three\_arm\_pilot\_15\_v1/REPORT\.md:47–53", "reason": "The shipped HotpotQA configuration and selected indices route the question field into optimization and evaluation\. Archived offline provenance verifies the matching original benchmark question and answer\."\}, "refutation": \{"basis": "none", "reference": "papers/ObliInjection/audit/dataflow/dataflow\.md:10–34; papers/ObliInjection/audit/provenance/PROVENANCE\.md:32–53", "reason": "The optimizer input is a complete evaluation\-matched question\. The missing historical generator does not refute this released\-code input path\."\}\}, "claim\_result": "confirmed", "note": "This confirms full evaluation\-matched question text in the released source path\. The archived offline report separately verifies the official HotpotQA match after Unicode normalization and outer\-whitespace removal\. Historical Table XI generator inputs are assessed separately and remain unverified\.", "behavioral\_impact": \{"status": "confounded", "reference": "repository/obli\-gpt4o\-ac\-transfer\-20261031/papers/ObliInjection/reproduction/gpt4o\_aux\_mistral\_joint\_matched\_v2\_20261031/report\.md:30–39; analysis/casebook\_2026\-11\-05/ObliInjection\_evidence\.md:13–20,109–121", "description": "Archived formal answers exist\. A/UQ differ by 16\.6 percentage points, while C exceeds A and A/C also change source documents\. Ten targets and one joint optimized artifact per arm limit broader causal claims\. Remote archive closeout is a separate process status\."\}\}, \{"id": "obli\_table\_xi\_historical\_question", "source\_group": "archived", "description": "Determine whether the historical HotpotQA Table XI shadow generator received a verbatim test question as a generation input\.", "scope": \{"paper\_version": "ObliInjection arXiv:2512\.09321v3, Appendix Table XI", "experiment\_arm": "Historical metadata\-conditioned HotpotQA shadow generation", "artifact\_revision": "Historical run revision unverified; public release b1f6a3f48c0cf121534374cbcef453832594867b inspected separately", "configuration": "Paper\-described question\-type\-only procedure; matching historical request and generator unavailable in the reviewed archive"\}, "target": \{"role": "shadow\-data generator", "phase": "historical metadata\-conditioned construction", "source": "original HotpotQA test item", "representation": "verbatim test question", "operation": "receive as generation input", "query\_form": "full\_query"\}, "verdict": "insufficient\_evidence", "reason": "evaluated\_instance\_alignment\_not\_established", "matching\_rules": \[\{"edge": \{"role": "shadow\-data generator", "phase": "historical metadata\-conditioned construction", "source": "original HotpotQA test item", "representation": "verbatim test question", "operation": "receive as generation input", "query\_form": "full\_query"\}, "permission": "deny", "reference": "repository/obli\-gpt4o\-ac\-transfer\-20261031/papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:1164–1173"\}\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The author's historical Table XI question\-type\-only shadow generator received the verbatim evaluation question\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "repository/obli\-gpt4o\-ac\-transfer\-20261031/papers/ObliInjection/reproduction/pilot\_15/obliinjection\_paper\.txt:1164–1173", "reason": "This claim is explicitly scoped to the paper\-described question\-type\-only historical procedure\. A verbatim target question would exceed the inputs described for that procedure\."\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "papers/ObliInjection/audit/dataflow/table\_xi\_audit\.md:3–24; papers/ObliInjection/audit/provenance/PROVENANCE\.md:50–57", "reason": "No matching historical generator or request is available in the reviewed archive\. Released optimizer inputs cannot establish that historical generator's request\."\}, "refutation": \{"basis": "none", "reference": "papers/ObliInjection/audit/dataflow/table\_xi\_audit\.md:3–24", "reason": "Missing historical evidence leaves the claim unresolved and provides no explicit permission or demonstrated excluded delivery\."\}\}, "claim\_result": "unresolved", "note": "Scope is the question\-type\-only procedure described in Table XI\. The report on the public optimizer and missing Table XI generator is papers/ObliInjection/audit/provenance/PROVENANCE\.md:32–56\. Neither establishes the historical run's inputs\.", "behavioral\_impact": \{"status": "not\_tested", "reference": "papers/ObliInjection/audit/dataflow/table\_xi\_audit\.md:26–31", "description": "Local surrogate reconstructions and released\-code comparisons do not identify the effect of the author's unobserved historical Table XI input\."\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "inconsistent", "reason": "confirmed\_inconsistency\_in\_scope"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "inconsistent", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "obli_released_optimizer_full_target_query",
    "source_group": "archived",
    "description": "Check if the released HotpotQA optimizer uses the complete question used by evaluation for the same selected case.",
    "scope": {
      "paper_version": "ObliInjection arXiv:2512.09321v3, §§III-B, IV and V-A, Appendix Table XI",
      "experiment_arm": "Released HotpotQA optimization and evaluation data flow",
      "artifact_revision": "Public release b1f6a3f48c0cf121534374cbcef453832594867b",
      "configuration": "Released HotpotQA JSON prepared by the shipped loader, with the same selected case for optimization and evaluation"
    },
    "target": {
      "role": "attacker-side optimizer",
      "phase": "optimization before evaluation",
      "source": "selected target-question record in the released HotpotQA evaluation data",
      "representation": "full evaluation-matched target question",
      "operation": "read as optimization input",
      "query_form": "full_query"
    },
    "verdict": "inconsistent",
    "reason": "scoped_forbidden_delivery_confirmed",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side optimizer",
          "phase": "optimization before evaluation",
          "source": "selected target-question record in the released HotpotQA evaluation data",
          "representation": "full evaluation-matched target question",
          "operation": "read as optimization input",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side optimizer",
          "phase": "optimization before evaluation",
          "source": "selected target-question record in the released HotpotQA evaluation data",
          "representation": "full evaluation-matched target question",
          "operation": "read as optimization input",
          "query_form": "full_query"
        },
        "status": "present",
        "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The released HotpotQA optimizer receives the full evaluation-matched target question beyond the documented question-type-driven surrogate construction.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
        "reason": "The scoped method constructs a surrogate from question-type metadata. Full text of the question used in the same target evaluation exceeds that described construction."
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53",
        "reason": "The shipped HotpotQA configuration and selected indices route the question field into optimization and evaluation. Archived offline provenance verifies the matching original benchmark question and answer."
      },
      "refutation": {
        "basis": "none",
        "reference": "papers/ObliInjection/audit/dataflow/dataflow.md:10–34; papers/ObliInjection/audit/provenance/PROVENANCE.md:32–53",
        "reason": "The optimizer input is a complete evaluation-matched question. The missing historical generator does not refute this released-code input path."
      }
    },
    "claim_result": "confirmed",
    "note": "This confirms full evaluation-matched question text in the released source path. The archived offline report separately verifies the official HotpotQA match after Unicode normalization and outer-whitespace removal. Historical Table XI generator inputs are assessed separately and remain unverified.",
    "behavioral_impact": {
      "status": "confounded",
      "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30–39; analysis/casebook_2026-11-05/ObliInjection_evidence.md:13–20,109–121",
      "description": "Archived formal answers exist. A/UQ differ by 16.6 percentage points, while C exceeds A and A/C also change source documents. Ten targets and one joint optimized artifact per arm limit broader causal claims. Remote archive closeout is a separate process status."
    }
  },
  {
    "id": "obli_table_xi_historical_question",
    "source_group": "archived",
    "description": "Determine whether the historical HotpotQA Table XI shadow generator received a verbatim test question as a generation input.",
    "scope": {
      "paper_version": "ObliInjection arXiv:2512.09321v3, Appendix Table XI",
      "experiment_arm": "Historical metadata-conditioned HotpotQA shadow generation",
      "artifact_revision": "Historical run revision unverified; public release b1f6a3f48c0cf121534374cbcef453832594867b inspected separately",
      "configuration": "Paper-described question-type-only procedure; matching historical request and generator unavailable in the reviewed archive"
    },
    "target": {
      "role": "shadow-data generator",
      "phase": "historical metadata-conditioned construction",
      "source": "original HotpotQA test item",
      "representation": "verbatim test question",
      "operation": "receive as generation input",
      "query_form": "full_query"
    },
    "verdict": "insufficient_evidence",
    "reason": "evaluated_instance_alignment_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "shadow-data generator",
          "phase": "historical metadata-conditioned construction",
          "source": "original HotpotQA test item",
          "representation": "verbatim test question",
          "operation": "receive as generation input",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The author's historical Table XI question-type-only shadow generator received the verbatim evaluation question.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
        "reason": "This claim is explicitly scoped to the paper-described question-type-only historical procedure. A verbatim target question would exceed the inputs described for that procedure."
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24; papers/ObliInjection/audit/provenance/PROVENANCE.md:50–57",
        "reason": "No matching historical generator or request is available in the reviewed archive. Released optimizer inputs cannot establish that historical generator's request."
      },
      "refutation": {
        "basis": "none",
        "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24",
        "reason": "Missing historical evidence leaves the claim unresolved and provides no explicit permission or demonstrated excluded delivery."
      }
    },
    "claim_result": "unresolved",
    "note": "Scope is the question-type-only procedure described in Table XI. The report on the public optimizer and missing Table XI generator is papers/ObliInjection/audit/provenance/PROVENANCE.md:32–56. Neither establishes the historical run's inputs.",
    "behavioral_impact": {
      "status": "not_tested",
      "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:26–31",
      "description": "Local surrogate reconstructions and released-code comparisons do not identify the effect of the author's unobserved historical Table XI input."
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "obliinjection",
  "title": "ObliInjection",
  "version": "arXiv:2512.09321v3",
  "audit_scope": "The complete evaluation-matched HotpotQA question delivered to the released optimizer at revision b1f6a3f48c0cf121534374cbcef453832594867b, plus the separate and unverified original Table XI generator-input claim. No behavioral-impact condition determines either information-boundary verdict.",
  "verdict": "inconsistent",
  "has_confirmed_inconsistency": true,
  "reason": "confirmed_inconsistency_in_scope",
  "coverage_complete": false,
  "required_checks": 2,
  "resolved_checks": 1,
  "confirmed_findings": [
    "obli_released_optimizer_full_target_query"
  ],
  "unresolved_checks": [
    "obli_table_xi_historical_question"
  ],
  "claim_result_counts": {
    "confirmed": 1,
    "unresolved": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [
    {
      "case_id": "obli_released_optimizer_full_target_query",
      "status": "confounded",
      "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30–39; analysis/casebook_2026-11-05/ObliInjection_evidence.md:13–20,109–121",
      "description": "Archived formal answers exist. A/UQ differ by 16.6 percentage points, while C exceeds A and A/C also change source documents. Ten targets and one joint optimized artifact per arm limit broader causal claims. Remote archive closeout is a separate process status."
    },
    {
      "case_id": "obli_table_xi_historical_question",
      "status": "not_tested",
      "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:26–31",
      "description": "Local surrogate reconstructions and released-code comparisons do not identify the effect of the author's unobserved historical Table XI input."
    }
  ],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "obli_released_optimizer_full_target_query",
      "source_group": "archived",
      "description": "Check if the released HotpotQA optimizer uses the complete question used by evaluation for the same selected case.",
      "scope": {
        "paper_version": "ObliInjection arXiv:2512.09321v3, §§III-B, IV and V-A, Appendix Table XI",
        "experiment_arm": "Released HotpotQA optimization and evaluation data flow",
        "artifact_revision": "Public release b1f6a3f48c0cf121534374cbcef453832594867b",
        "configuration": "Released HotpotQA JSON prepared by the shipped loader, with the same selected case for optimization and evaluation"
      },
      "target": {
        "role": "attacker-side optimizer",
        "phase": "optimization before evaluation",
        "source": "selected target-question record in the released HotpotQA evaluation data",
        "representation": "full evaluation-matched target question",
        "operation": "read as optimization input",
        "query_form": "full_query"
      },
      "verdict": "inconsistent",
      "reason": "scoped_forbidden_delivery_confirmed",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side optimizer",
            "phase": "optimization before evaluation",
            "source": "selected target-question record in the released HotpotQA evaluation data",
            "representation": "full evaluation-matched target question",
            "operation": "read as optimization input",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side optimizer",
            "phase": "optimization before evaluation",
            "source": "selected target-question record in the released HotpotQA evaluation data",
            "representation": "full evaluation-matched target question",
            "operation": "read as optimization input",
            "query_form": "full_query"
          },
          "status": "present",
          "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The released HotpotQA optimizer receives the full evaluation-matched target question beyond the documented question-type-driven surrogate construction.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
          "reason": "The scoped method constructs a surrogate from question-type metadata. Full text of the question used in the same target evaluation exceeds that described construction."
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53",
          "reason": "The shipped HotpotQA configuration and selected indices route the question field into optimization and evaluation. Archived offline provenance verifies the matching original benchmark question and answer."
        },
        "refutation": {
          "basis": "none",
          "reference": "papers/ObliInjection/audit/dataflow/dataflow.md:10–34; papers/ObliInjection/audit/provenance/PROVENANCE.md:32–53",
          "reason": "The optimizer input is a complete evaluation-matched question. The missing historical generator does not refute this released-code input path."
        }
      },
      "claim_result": "confirmed",
      "note": "This confirms full evaluation-matched question text in the released source path. The archived offline report separately verifies the official HotpotQA match after Unicode normalization and outer-whitespace removal. Historical Table XI generator inputs are assessed separately and remain unverified.",
      "behavioral_impact": {
        "status": "confounded",
        "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30–39; analysis/casebook_2026-11-05/ObliInjection_evidence.md:13–20,109–121",
        "description": "Archived formal answers exist. A/UQ differ by 16.6 percentage points, while C exceeds A and A/C also change source documents. Ten targets and one joint optimized artifact per arm limit broader causal claims. Remote archive closeout is a separate process status."
      }
    },
    {
      "id": "obli_table_xi_historical_question",
      "source_group": "archived",
      "description": "Determine whether the historical HotpotQA Table XI shadow generator received a verbatim test question as a generation input.",
      "scope": {
        "paper_version": "ObliInjection arXiv:2512.09321v3, Appendix Table XI",
        "experiment_arm": "Historical metadata-conditioned HotpotQA shadow generation",
        "artifact_revision": "Historical run revision unverified; public release b1f6a3f48c0cf121534374cbcef453832594867b inspected separately",
        "configuration": "Paper-described question-type-only procedure; matching historical request and generator unavailable in the reviewed archive"
      },
      "target": {
        "role": "shadow-data generator",
        "phase": "historical metadata-conditioned construction",
        "source": "original HotpotQA test item",
        "representation": "verbatim test question",
        "operation": "receive as generation input",
        "query_form": "full_query"
      },
      "verdict": "insufficient_evidence",
      "reason": "evaluated_instance_alignment_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "shadow-data generator",
            "phase": "historical metadata-conditioned construction",
            "source": "original HotpotQA test item",
            "representation": "verbatim test question",
            "operation": "receive as generation input",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The author's historical Table XI question-type-only shadow generator received the verbatim evaluation question.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
          "reason": "This claim is explicitly scoped to the paper-described question-type-only historical procedure. A verbatim target question would exceed the inputs described for that procedure."
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24; papers/ObliInjection/audit/provenance/PROVENANCE.md:50–57",
          "reason": "No matching historical generator or request is available in the reviewed archive. Released optimizer inputs cannot establish that historical generator's request."
        },
        "refutation": {
          "basis": "none",
          "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24",
          "reason": "Missing historical evidence leaves the claim unresolved and provides no explicit permission or demonstrated excluded delivery."
        }
      },
      "claim_result": "unresolved",
      "note": "Scope is the question-type-only procedure described in Table XI. The report on the public optimizer and missing Table XI generator is papers/ObliInjection/audit/provenance/PROVENANCE.md:32–56. Neither establishes the historical run's inputs.",
      "behavioral_impact": {
        "status": "not_tested",
        "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:26–31",
        "description": "Local surrogate reconstructions and released-code comparisons do not identify the effect of the author's unobserved historical Table XI input."
      }
    }
  ],
  "expected": "inconsistent",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "obli_released_optimizer_full_target_query",
          "source_group": "archived",
          "description": "Check if the released HotpotQA optimizer uses the complete question used by evaluation for the same selected case.",
          "scope": {
            "paper_version": "ObliInjection arXiv:2512.09321v3, §§III-B, IV and V-A, Appendix Table XI",
            "experiment_arm": "Released HotpotQA optimization and evaluation data flow",
            "artifact_revision": "Public release b1f6a3f48c0cf121534374cbcef453832594867b",
            "configuration": "Released HotpotQA JSON prepared by the shipped loader, with the same selected case for optimization and evaluation"
          },
          "target": {
            "role": "attacker-side optimizer",
            "phase": "optimization before evaluation",
            "source": "selected target-question record in the released HotpotQA evaluation data",
            "representation": "full evaluation-matched target question",
            "operation": "read as optimization input",
            "query_form": "full_query"
          },
          "verdict": "inconsistent",
          "reason": "scoped_forbidden_delivery_confirmed",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side optimizer",
                "phase": "optimization before evaluation",
                "source": "selected target-question record in the released HotpotQA evaluation data",
                "representation": "full evaluation-matched target question",
                "operation": "read as optimization input",
                "query_form": "full_query"
              },
              "permission": "deny",
              "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side optimizer",
                "phase": "optimization before evaluation",
                "source": "selected target-question record in the released HotpotQA evaluation data",
                "representation": "full evaluation-matched target question",
                "operation": "read as optimization input",
                "query_form": "full_query"
              },
              "status": "present",
              "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The released HotpotQA optimizer receives the full evaluation-matched target question beyond the documented question-type-driven surrogate construction.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209–214; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:245–255; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655–665; papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
              "reason": "The scoped method constructs a surrogate from question-type metadata. Full text of the question used in the same target evaluation exceeds that described construction."
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23–26; papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33–47; papers/ObliInjection/audit/dataflow/dataflow.md:12–34; repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47–53",
              "reason": "The shipped HotpotQA configuration and selected indices route the question field into optimization and evaluation. Archived offline provenance verifies the matching original benchmark question and answer."
            },
            "refutation": {
              "basis": "none",
              "reference": "papers/ObliInjection/audit/dataflow/dataflow.md:10–34; papers/ObliInjection/audit/provenance/PROVENANCE.md:32–53",
              "reason": "The optimizer input is a complete evaluation-matched question. The missing historical generator does not refute this released-code input path."
            }
          },
          "claim_result": "confirmed",
          "note": "This confirms full evaluation-matched question text in the released source path. The archived offline report separately verifies the official HotpotQA match after Unicode normalization and outer-whitespace removal. Historical Table XI generator inputs are assessed separately and remain unverified.",
          "behavioral_impact": {
            "status": "confounded",
            "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30–39; analysis/casebook_2026-11-05/ObliInjection_evidence.md:13–20,109–121",
            "description": "Archived formal answers exist. A/UQ differ by 16.6 percentage points, while C exceeds A and A/C also change source documents. Ten targets and one joint optimized artifact per arm limit broader causal claims. Remote archive closeout is a separate process status."
          }
        },
        {
          "id": "obli_table_xi_historical_question",
          "source_group": "archived",
          "description": "Determine whether the historical HotpotQA Table XI shadow generator received a verbatim test question as a generation input.",
          "scope": {
            "paper_version": "ObliInjection arXiv:2512.09321v3, Appendix Table XI",
            "experiment_arm": "Historical metadata-conditioned HotpotQA shadow generation",
            "artifact_revision": "Historical run revision unverified; public release b1f6a3f48c0cf121534374cbcef453832594867b inspected separately",
            "configuration": "Paper-described question-type-only procedure; matching historical request and generator unavailable in the reviewed archive"
          },
          "target": {
            "role": "shadow-data generator",
            "phase": "historical metadata-conditioned construction",
            "source": "original HotpotQA test item",
            "representation": "verbatim test question",
            "operation": "receive as generation input",
            "query_form": "full_query"
          },
          "verdict": "insufficient_evidence",
          "reason": "evaluated_instance_alignment_not_established",
          "matching_rules": [
            {
              "edge": {
                "role": "shadow-data generator",
                "phase": "historical metadata-conditioned construction",
                "source": "original HotpotQA test item",
                "representation": "verbatim test question",
                "operation": "receive as generation input",
                "query_form": "full_query"
              },
              "permission": "deny",
              "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173"
            }
          ],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The author's historical Table XI question-type-only shadow generator received the verbatim evaluation question.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164–1173",
              "reason": "This claim is explicitly scoped to the paper-described question-type-only historical procedure. A verbatim target question would exceed the inputs described for that procedure."
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24; papers/ObliInjection/audit/provenance/PROVENANCE.md:50–57",
              "reason": "No matching historical generator or request is available in the reviewed archive. Released optimizer inputs cannot establish that historical generator's request."
            },
            "refutation": {
              "basis": "none",
              "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:3–24",
              "reason": "Missing historical evidence leaves the claim unresolved and provides no explicit permission or demonstrated excluded delivery."
            }
          },
          "claim_result": "unresolved",
          "note": "Scope is the question-type-only procedure described in Table XI. The report on the public optimizer and missing Table XI generator is papers/ObliInjection/audit/provenance/PROVENANCE.md:32–56. Neither establishes the historical run's inputs.",
          "behavioral_impact": {
            "status": "not_tested",
            "reference": "papers/ObliInjection/audit/dataflow/table_xi_audit.md:26–31",
            "description": "Local surrogate reconstructions and released-code comparisons do not identify the effect of the author's unobserved historical Table XI input."
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "inconsistent",
      "reason": "confirmed_inconsistency_in_scope"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "inconsistent",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 10. WebTrap

论文 ID：webtrap  
运行 / 判定：有已确认的不一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "webtrap\_original\_internal\_path", "source\_group": "archived", "description": "Determine whether the exact restricted\-area relative path reached the final generator in the saved ORIGINAL requests\.", "scope": \{"paper\_version": "WebTrap arXiv:2605\.08310v1, §§4\.1–4\.2", "experiment\_arm": "PSAA file\-browser ORIGINAL", "artifact\_revision": "Upstream f8255c83d4a569fc374198b67717fcbee17af1fb; archived paired Pro requests", "configuration": "Saved final generation requests for case\_0001 and case\_0004"\}, "target": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "verdict": "inconsistent", "reason": "scoped\_forbidden\_delivery\_confirmed", "matching\_rules": \[\{"edge": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "permission": "deny", "reference": "https://arxiv\.org/html/2605\.08310v1\#S4\.SS1; https://arxiv\.org/html/2605\.08310v1\#A1\.SS1; papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:7–11"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "status": "present", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:53–71; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–11"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The saved ORIGINAL final generator requests receive the case\-specific restricted\-area path despite the stated restricted\-area knowledge boundary\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "resource\_metadata", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "https://arxiv\.org/html/2605\.08310v1\#S4\.SS1; https://arxiv\.org/html/2605\.08310v1\#A1\.SS1; papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:7–11", "reason": "The scoped PSAA condition limits construction to visible user\-area information and excludes restricted\-area internal structure\. The target is the selected exact internal path\."\}, "delivery": \{"status": "confirmed", "evidence\_kind": "saved\_request", "task\_relation": "same\_evaluated\_instance", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:53–71; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–11", "reason": "The saved case\_0001 and case\_0004 final requests include the selected internal relative\-path field from the case manifest\."\}, "refutation": \{"basis": "none", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:53–71; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–11", "reason": "The selected path is additional internal metadata, as distinguished from the permitted objective and visible entrance information\."\}\}, "claim\_result": "confirmed", "note": "Evidence concerns the specified public revision and saved requests\. Author\-run configuration and effect on success rate are separate unverified claims\.", "behavioral\_impact": \{"status": "inconclusive", "reference": "papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–27", "description": "The archived two\-case study confirms changed target binding in generation\. Neither arm completes the attack, and exposure varies across cases\. No ASR increase is established\."\}\}, \{"id": "webtrap\_limited\_internal\_path", "source\_group": "archived", "description": "Check the same exact path input in the saved requests for the local LIMITED\_CONTEXT comparison arm\.", "scope": \{"paper\_version": "WebTrap arXiv:2605\.08310v1, §§4\.1–4\.2", "experiment\_arm": "PSAA file\-browser LIMITED\_CONTEXT \(local comparison\)", "artifact\_revision": "Archived paired Pro requests, upstream comparison base f8255c83d4a569fc374198b67717fcbee17af1fb", "configuration": "Saved final generation requests for case\_0001 and case\_0004"\}, "target": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_excluded\_delivery", "matching\_rules": \[\{"edge": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "permission": "deny", "reference": "https://arxiv\.org/html/2605\.08310v1\#S4\.SS1; https://arxiv\.org/html/2605\.08310v1\#A1\.SS1; papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:7–11"\}\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side generator", "phase": "final content generation", "source": "internal goal manifest", "representation": "case\-specific exact restricted\-area relative path", "operation": "receive as request input"\}, "status": "absent", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:63–70; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–7"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The saved LIMITED\_CONTEXT final generator requests receive the selected case\-specific restricted\-area path despite the stated restricted\-area knowledge boundary\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "resource\_metadata", "policy\_application": \{"status": "applicable", "policy\_kind": "attacker\_knowledge\_constraint", "reference": "https://arxiv\.org/html/2605\.08310v1\#S4\.SS1; https://arxiv\.org/html/2605\.08310v1\#A1\.SS1; papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:7–11", "reason": "The scoped PSAA condition limits construction to visible user\-area information and excludes restricted\-area internal structure\. The target is the selected exact internal path\."\}, "delivery": \{"status": "excluded", "evidence\_kind": "saved\_request", "task\_relation": "same\_evaluated\_instance", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:63–70; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–7", "reason": "The saved case\_0001 and case\_0004 final requests establish absence of the selected internal relative\-path field at the generator boundary\. Generic template vocabulary remains\."\}, "refutation": \{"basis": "excluded\_delivery", "reference": "papers/WebTrap/replication/THREAT\_MODEL\_CODE\_ALIGNMENT\.md:63–70; papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–7", "reason": "The exact alleged input is absent in the two saved LIMITED\_CONTEXT requests, refuting the selected field\-level delivery claim within this scope\."\}\}, "claim\_result": "refuted", "note": "The saved final requests establish absence of the selected path input in these two cases\. Generic template vocabulary remains in the comparison arm\.", "behavioral\_impact": \{"status": "inconclusive", "reference": "papers/WebTrap/replication/CONTEXT\_EFFECT\_ASSESSMENT\.md:3–27", "description": "The archived two\-case study confirms changed target binding in generation\. Neither arm completes the attack, and exposure varies across cases\. No ASR increase is established\."\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "inconsistent", "reason": "confirmed\_inconsistency\_in\_scope"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "inconsistent", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "webtrap_original_internal_path",
    "source_group": "archived",
    "description": "Determine whether the exact restricted-area relative path reached the final generator in the saved ORIGINAL requests.",
    "scope": {
      "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
      "experiment_arm": "PSAA file-browser ORIGINAL",
      "artifact_revision": "Upstream f8255c83d4a569fc374198b67717fcbee17af1fb; archived paired Pro requests",
      "configuration": "Saved final generation requests for case_0001 and case_0004"
    },
    "target": {
      "role": "attacker-side generator",
      "phase": "final content generation",
      "source": "internal goal manifest",
      "representation": "case-specific exact restricted-area relative path",
      "operation": "receive as request input"
    },
    "verdict": "inconsistent",
    "reason": "scoped_forbidden_delivery_confirmed",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "final content generation",
          "source": "internal goal manifest",
          "representation": "case-specific exact restricted-area relative path",
          "operation": "receive as request input"
        },
        "permission": "deny",
        "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "final content generation",
          "source": "internal goal manifest",
          "representation": "case-specific exact restricted-area relative path",
          "operation": "receive as request input"
        },
        "status": "present",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The saved ORIGINAL final generator requests receive the case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "resource_metadata",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
        "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "saved_request",
        "task_relation": "same_evaluated_instance",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
        "reason": "The saved case_0001 and case_0004 final requests include the selected internal relative-path field from the case manifest."
      },
      "refutation": {
        "basis": "none",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
        "reason": "The selected path is additional internal metadata, as distinguished from the permitted objective and visible entrance information."
      }
    },
    "claim_result": "confirmed",
    "note": "Evidence concerns the specified public revision and saved requests. Author-run configuration and effect on success rate are separate unverified claims.",
    "behavioral_impact": {
      "status": "inconclusive",
      "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
      "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
    }
  },
  {
    "id": "webtrap_limited_internal_path",
    "source_group": "archived",
    "description": "Check the same exact path input in the saved requests for the local LIMITED_CONTEXT comparison arm.",
    "scope": {
      "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
      "experiment_arm": "PSAA file-browser LIMITED_CONTEXT (local comparison)",
      "artifact_revision": "Archived paired Pro requests, upstream comparison base f8255c83d4a569fc374198b67717fcbee17af1fb",
      "configuration": "Saved final generation requests for case_0001 and case_0004"
    },
    "target": {
      "role": "attacker-side generator",
      "phase": "final content generation",
      "source": "internal goal manifest",
      "representation": "case-specific exact restricted-area relative path",
      "operation": "receive as request input"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_excluded_delivery",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "final content generation",
          "source": "internal goal manifest",
          "representation": "case-specific exact restricted-area relative path",
          "operation": "receive as request input"
        },
        "permission": "deny",
        "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side generator",
          "phase": "final content generation",
          "source": "internal goal manifest",
          "representation": "case-specific exact restricted-area relative path",
          "operation": "receive as request input"
        },
        "status": "absent",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The saved LIMITED_CONTEXT final generator requests receive the selected case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "resource_metadata",
      "policy_application": {
        "status": "applicable",
        "policy_kind": "attacker_knowledge_constraint",
        "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
        "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
      },
      "delivery": {
        "status": "excluded",
        "evidence_kind": "saved_request",
        "task_relation": "same_evaluated_instance",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
        "reason": "The saved case_0001 and case_0004 final requests establish absence of the selected internal relative-path field at the generator boundary. Generic template vocabulary remains."
      },
      "refutation": {
        "basis": "excluded_delivery",
        "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
        "reason": "The exact alleged input is absent in the two saved LIMITED_CONTEXT requests, refuting the selected field-level delivery claim within this scope."
      }
    },
    "claim_result": "refuted",
    "note": "The saved final requests establish absence of the selected path input in these two cases. Generic template vocabulary remains in the comparison arm.",
    "behavioral_impact": {
      "status": "inconclusive",
      "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
      "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "webtrap",
  "title": "WebTrap",
  "version": "arXiv:2605.08310v1",
  "audit_scope": "Only the selected internal target-relative-path field in the saved final generator requests for case_0001 and case_0004 under ORIGINAL and the local LIMITED_CONTEXT control, with source base f8255c83d4a569fc374198b67717fcbee17af1fb. Other information channels, other cases, historical author runs and behavioral effects are outside this finite input check.",
  "verdict": "inconsistent",
  "has_confirmed_inconsistency": true,
  "reason": "confirmed_inconsistency_in_scope",
  "coverage_complete": true,
  "required_checks": 2,
  "resolved_checks": 2,
  "confirmed_findings": [
    "webtrap_original_internal_path"
  ],
  "unresolved_checks": [],
  "claim_result_counts": {
    "confirmed": 1,
    "refuted": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [
    {
      "case_id": "webtrap_original_internal_path",
      "status": "inconclusive",
      "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
      "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
    },
    {
      "case_id": "webtrap_limited_internal_path",
      "status": "inconclusive",
      "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
      "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
    }
  ],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "webtrap_original_internal_path",
      "source_group": "archived",
      "description": "Determine whether the exact restricted-area relative path reached the final generator in the saved ORIGINAL requests.",
      "scope": {
        "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
        "experiment_arm": "PSAA file-browser ORIGINAL",
        "artifact_revision": "Upstream f8255c83d4a569fc374198b67717fcbee17af1fb; archived paired Pro requests",
        "configuration": "Saved final generation requests for case_0001 and case_0004"
      },
      "target": {
        "role": "attacker-side generator",
        "phase": "final content generation",
        "source": "internal goal manifest",
        "representation": "case-specific exact restricted-area relative path",
        "operation": "receive as request input"
      },
      "verdict": "inconsistent",
      "reason": "scoped_forbidden_delivery_confirmed",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "permission": "deny",
          "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "status": "present",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The saved ORIGINAL final generator requests receive the case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "resource_metadata",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
          "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "saved_request",
          "task_relation": "same_evaluated_instance",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
          "reason": "The saved case_0001 and case_0004 final requests include the selected internal relative-path field from the case manifest."
        },
        "refutation": {
          "basis": "none",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
          "reason": "The selected path is additional internal metadata, as distinguished from the permitted objective and visible entrance information."
        }
      },
      "claim_result": "confirmed",
      "note": "Evidence concerns the specified public revision and saved requests. Author-run configuration and effect on success rate are separate unverified claims.",
      "behavioral_impact": {
        "status": "inconclusive",
        "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
        "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
      }
    },
    {
      "id": "webtrap_limited_internal_path",
      "source_group": "archived",
      "description": "Check the same exact path input in the saved requests for the local LIMITED_CONTEXT comparison arm.",
      "scope": {
        "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
        "experiment_arm": "PSAA file-browser LIMITED_CONTEXT (local comparison)",
        "artifact_revision": "Archived paired Pro requests, upstream comparison base f8255c83d4a569fc374198b67717fcbee17af1fb",
        "configuration": "Saved final generation requests for case_0001 and case_0004"
      },
      "target": {
        "role": "attacker-side generator",
        "phase": "final content generation",
        "source": "internal goal manifest",
        "representation": "case-specific exact restricted-area relative path",
        "operation": "receive as request input"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_excluded_delivery",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "permission": "deny",
          "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "status": "absent",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The saved LIMITED_CONTEXT final generator requests receive the selected case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "resource_metadata",
        "policy_application": {
          "status": "applicable",
          "policy_kind": "attacker_knowledge_constraint",
          "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
          "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
        },
        "delivery": {
          "status": "excluded",
          "evidence_kind": "saved_request",
          "task_relation": "same_evaluated_instance",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
          "reason": "The saved case_0001 and case_0004 final requests establish absence of the selected internal relative-path field at the generator boundary. Generic template vocabulary remains."
        },
        "refutation": {
          "basis": "excluded_delivery",
          "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
          "reason": "The exact alleged input is absent in the two saved LIMITED_CONTEXT requests, refuting the selected field-level delivery claim within this scope."
        }
      },
      "claim_result": "refuted",
      "note": "The saved final requests establish absence of the selected path input in these two cases. Generic template vocabulary remains in the comparison arm.",
      "behavioral_impact": {
        "status": "inconclusive",
        "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
        "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
      }
    }
  ],
  "expected": "inconsistent",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "webtrap_original_internal_path",
          "source_group": "archived",
          "description": "Determine whether the exact restricted-area relative path reached the final generator in the saved ORIGINAL requests.",
          "scope": {
            "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
            "experiment_arm": "PSAA file-browser ORIGINAL",
            "artifact_revision": "Upstream f8255c83d4a569fc374198b67717fcbee17af1fb; archived paired Pro requests",
            "configuration": "Saved final generation requests for case_0001 and case_0004"
          },
          "target": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "verdict": "inconsistent",
          "reason": "scoped_forbidden_delivery_confirmed",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "final content generation",
                "source": "internal goal manifest",
                "representation": "case-specific exact restricted-area relative path",
                "operation": "receive as request input"
              },
              "permission": "deny",
              "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "final content generation",
                "source": "internal goal manifest",
                "representation": "case-specific exact restricted-area relative path",
                "operation": "receive as request input"
              },
              "status": "present",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The saved ORIGINAL final generator requests receive the case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "resource_metadata",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
              "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "saved_request",
              "task_relation": "same_evaluated_instance",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
              "reason": "The saved case_0001 and case_0004 final requests include the selected internal relative-path field from the case manifest."
            },
            "refutation": {
              "basis": "none",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:53–71; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–11",
              "reason": "The selected path is additional internal metadata, as distinguished from the permitted objective and visible entrance information."
            }
          },
          "claim_result": "confirmed",
          "note": "Evidence concerns the specified public revision and saved requests. Author-run configuration and effect on success rate are separate unverified claims.",
          "behavioral_impact": {
            "status": "inconclusive",
            "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
            "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
          }
        },
        {
          "id": "webtrap_limited_internal_path",
          "source_group": "archived",
          "description": "Check the same exact path input in the saved requests for the local LIMITED_CONTEXT comparison arm.",
          "scope": {
            "paper_version": "WebTrap arXiv:2605.08310v1, §§4.1–4.2",
            "experiment_arm": "PSAA file-browser LIMITED_CONTEXT (local comparison)",
            "artifact_revision": "Archived paired Pro requests, upstream comparison base f8255c83d4a569fc374198b67717fcbee17af1fb",
            "configuration": "Saved final generation requests for case_0001 and case_0004"
          },
          "target": {
            "role": "attacker-side generator",
            "phase": "final content generation",
            "source": "internal goal manifest",
            "representation": "case-specific exact restricted-area relative path",
            "operation": "receive as request input"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_excluded_delivery",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "final content generation",
                "source": "internal goal manifest",
                "representation": "case-specific exact restricted-area relative path",
                "operation": "receive as request input"
              },
              "permission": "deny",
              "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side generator",
                "phase": "final content generation",
                "source": "internal goal manifest",
                "representation": "case-specific exact restricted-area relative path",
                "operation": "receive as request input"
              },
              "status": "absent",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The saved LIMITED_CONTEXT final generator requests receive the selected case-specific restricted-area path despite the stated restricted-area knowledge boundary.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "resource_metadata",
            "policy_application": {
              "status": "applicable",
              "policy_kind": "attacker_knowledge_constraint",
              "reference": "https://arxiv.org/html/2605.08310v1#S4.SS1; https://arxiv.org/html/2605.08310v1#A1.SS1; papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:7–11",
              "reason": "The scoped PSAA condition limits construction to visible user-area information and excludes restricted-area internal structure. The target is the selected exact internal path."
            },
            "delivery": {
              "status": "excluded",
              "evidence_kind": "saved_request",
              "task_relation": "same_evaluated_instance",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
              "reason": "The saved case_0001 and case_0004 final requests establish absence of the selected internal relative-path field at the generator boundary. Generic template vocabulary remains."
            },
            "refutation": {
              "basis": "excluded_delivery",
              "reference": "papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:63–70; papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–7",
              "reason": "The exact alleged input is absent in the two saved LIMITED_CONTEXT requests, refuting the selected field-level delivery claim within this scope."
            }
          },
          "claim_result": "refuted",
          "note": "The saved final requests establish absence of the selected path input in these two cases. Generic template vocabulary remains in the comparison arm.",
          "behavioral_impact": {
            "status": "inconclusive",
            "reference": "papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3–27",
            "description": "The archived two-case study confirms changed target binding in generation. Neither arm completes the attack, and exposure varies across cases. No ASR increase is established."
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "inconsistent",
      "reason": "confirmed_inconsistency_in_scope"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "inconsistent",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 11. ICoA

论文 ID：icoa  
运行 / 判定：证据不足

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "icoa\_direct\_system\_read", "source\_group": "paper\_text", "description": "Check for a direct read of the system prompt by the ICoA content constructor\.", "scope": \{"paper\_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026\.emnlp\-main\.2035", "experiment\_arm": "AgentDojo 0\.1\.34 benchmark identity framing", "artifact\_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954", "configuration": "Static source and configuration for the released AgentDojo benchmark setup"\}, "target": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "victim system prompt", "representation": "system prompt content", "operation": "read directly"\}, "verdict": "insufficient\_evidence", "reason": "evaluated\_instance\_alignment\_not\_established", "matching\_rules": \[\{"edge": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "victim system prompt", "representation": "system prompt content", "operation": "read directly"\}, "permission": "deny", "reference": "https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=3"\}\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The ICoA content constructor directly reads the victim system prompt to obtain its user identity\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "user\_identity", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=3", "reason": "§2 denies access to the system prompt for the content constructor\. A same\-valued benchmark constant is a separate source and is not automatically a direct read of that prompt\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "", "reason": "The reviewed evidence identifies a matching identity constant but no direct system\-prompt read at the construction boundary\. Matching values neither establish such a read nor prove its absence\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "Published threat model and pinned static source\. The §4\.1 identity requirement and the code constant establish identity matching from a separate source\. They provide no direct\-read observation for the system\-prompt edge\. See https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=5 and https://github\.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa\.py\#L41\-L49\."\}, \{"id": "icoa\_benchmark\_identity\_source", "source\_group": "paper\_text", "description": "Determine whether the stated threat model covers the fixed benchmark identity used by the released implementation\.", "scope": \{"paper\_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026\.emnlp\-main\.2035", "experiment\_arm": "AgentDojo 0\.1\.34 benchmark identity framing", "artifact\_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954", "configuration": "Static source and configuration for the released AgentDojo benchmark setup"\}, "target": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "fixed benchmark code constant", "representation": "benchmark user identity matching the victim system prompt", "operation": "use to format content"\}, "verdict": "insufficient\_evidence", "reason": "policy\_scope\_not\_established", "matching\_rules": \[\], "matching\_observations": \[\{"edge": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "fixed benchmark code constant", "representation": "benchmark user identity matching the victim system prompt", "operation": "use to format content"\}, "status": "present", "reference": "https://github\.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa\.py\#L41\-L49 and https://github\.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system\_messages\.yaml\#L3"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The matching benchmark identity constant is established to be an unauthorized source of user identity under ICoA’s declared access model\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "user\_identity", "policy\_application": \{"status": "uncertain", "reference": "https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=3 and https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=5", "reason": "§2 excludes system\-prompt access and §4\.1 requires a matching identity, but the paper does not specify whether this separately sourced benchmark identity is permitted or prohibited\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "https://github\.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa\.py\#L41\-L49 and https://github\.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system\_messages\.yaml\#L3", "reason": "The cited fixed implementation audit binds the construction constant and configured system\-prompt identity to matching values\. This is static\-source evidence for use of the separate constant, not a captured runtime request or a direct prompt read\."\}, "refutation": \{"basis": "none", "reference": "", "reason": "No positive counterevidence refutes this scoped suspicion\."\}\}, "claim\_result": "unresolved", "note": "Published method and pinned static source\. §2 restricts system\-prompt access and leaves the rules for knowing the same identity through other means unspecified\. The two pinned code/configuration constants have the same value\.", "input\_provenance\_gap": \{"description": "The benchmark uses a matching identity constant\. The paper leaves open how an attacker obtains that identity under the stated access constraints\.", "reference": "ICoA §2 \(https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=3\) and §4\.1 \(https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf\#page=5\)"\}\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "insufficient\_evidence", "reason": "unresolved\_checks"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "insufficient\_evidence", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "icoa_direct_system_read",
    "source_group": "paper_text",
    "description": "Check for a direct read of the system prompt by the ICoA content constructor.",
    "scope": {
      "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
      "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
      "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
      "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
    },
    "target": {
      "role": "attacker-side content constructor",
      "phase": "content construction",
      "source": "victim system prompt",
      "representation": "system prompt content",
      "operation": "read directly"
    },
    "verdict": "insufficient_evidence",
    "reason": "evaluated_instance_alignment_not_established",
    "matching_rules": [
      {
        "edge": {
          "role": "attacker-side content constructor",
          "phase": "content construction",
          "source": "victim system prompt",
          "representation": "system prompt content",
          "operation": "read directly"
        },
        "permission": "deny",
        "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3"
      }
    ],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The ICoA content constructor directly reads the victim system prompt to obtain its user identity.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "user_identity",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3",
        "reason": "§2 denies access to the system prompt for the content constructor. A same-valued benchmark constant is a separate source and is not automatically a direct read of that prompt.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "",
        "reason": "The reviewed evidence identifies a matching identity constant but no direct system-prompt read at the construction boundary. Matching values neither establish such a read nor prove its absence."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "Published threat model and pinned static source. The §4.1 identity requirement and the code constant establish identity matching from a separate source. They provide no direct-read observation for the system-prompt edge. See https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49."
  },
  {
    "id": "icoa_benchmark_identity_source",
    "source_group": "paper_text",
    "description": "Determine whether the stated threat model covers the fixed benchmark identity used by the released implementation.",
    "scope": {
      "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
      "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
      "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
      "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
    },
    "target": {
      "role": "attacker-side content constructor",
      "phase": "content construction",
      "source": "fixed benchmark code constant",
      "representation": "benchmark user identity matching the victim system prompt",
      "operation": "use to format content"
    },
    "verdict": "insufficient_evidence",
    "reason": "policy_scope_not_established",
    "matching_rules": [],
    "matching_observations": [
      {
        "edge": {
          "role": "attacker-side content constructor",
          "phase": "content construction",
          "source": "fixed benchmark code constant",
          "representation": "benchmark user identity matching the victim system prompt",
          "operation": "use to format content"
        },
        "status": "present",
        "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The matching benchmark identity constant is established to be an unauthorized source of user identity under ICoA’s declared access model.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "user_identity",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3 and https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5",
        "reason": "§2 excludes system-prompt access and §4.1 requires a matching identity, but the paper does not specify whether this separately sourced benchmark identity is permitted or prohibited.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3",
        "reason": "The cited fixed implementation audit binds the construction constant and configured system-prompt identity to matching values. This is static-source evidence for use of the separate constant, not a captured runtime request or a direct prompt read."
      },
      "refutation": {
        "basis": "none",
        "reference": "",
        "reason": "No positive counterevidence refutes this scoped suspicion."
      }
    },
    "claim_result": "unresolved",
    "note": "Published method and pinned static source. §2 restricts system-prompt access and leaves the rules for knowing the same identity through other means unspecified. The two pinned code/configuration constants have the same value.",
    "input_provenance_gap": {
      "description": "The benchmark uses a matching identity constant. The paper leaves open how an attacker obtains that identity under the stated access constraints.",
      "reference": "ICoA §2 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) and §4.1 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5)"
    }
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "icoa",
  "title": "ICoA",
  "version": "EMNLP 2026 final and cited fixed author commit e333be8e1c319be3deb6942692aaed8e640a3954",
  "audit_scope": "Direct system-prompt read versus use of a matching separately sourced benchmark identity constant; source-specific permission remains unresolved.",
  "verdict": "insufficient_evidence",
  "has_confirmed_inconsistency": false,
  "reason": "unresolved_checks",
  "coverage_complete": false,
  "required_checks": 2,
  "resolved_checks": 0,
  "confirmed_findings": [],
  "unresolved_checks": [
    "icoa_direct_system_read",
    "icoa_benchmark_identity_source"
  ],
  "claim_result_counts": {
    "unresolved": 2
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [
    {
      "case_id": "icoa_benchmark_identity_source",
      "description": "The benchmark uses a matching identity constant. The paper leaves open how an attacker obtains that identity under the stated access constraints.",
      "reference": "ICoA §2 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) and §4.1 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5)"
    }
  ],
  "evidence": [
    {
      "id": "icoa_direct_system_read",
      "source_group": "paper_text",
      "description": "Check for a direct read of the system prompt by the ICoA content constructor.",
      "scope": {
        "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
        "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
        "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
        "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
      },
      "target": {
        "role": "attacker-side content constructor",
        "phase": "content construction",
        "source": "victim system prompt",
        "representation": "system prompt content",
        "operation": "read directly"
      },
      "verdict": "insufficient_evidence",
      "reason": "evaluated_instance_alignment_not_established",
      "matching_rules": [
        {
          "edge": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "victim system prompt",
            "representation": "system prompt content",
            "operation": "read directly"
          },
          "permission": "deny",
          "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3"
        }
      ],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The ICoA content constructor directly reads the victim system prompt to obtain its user identity.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "user_identity",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3",
          "reason": "§2 denies access to the system prompt for the content constructor. A same-valued benchmark constant is a separate source and is not automatically a direct read of that prompt.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "",
          "reason": "The reviewed evidence identifies a matching identity constant but no direct system-prompt read at the construction boundary. Matching values neither establish such a read nor prove its absence."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "Published threat model and pinned static source. The §4.1 identity requirement and the code constant establish identity matching from a separate source. They provide no direct-read observation for the system-prompt edge. See https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49."
    },
    {
      "id": "icoa_benchmark_identity_source",
      "source_group": "paper_text",
      "description": "Determine whether the stated threat model covers the fixed benchmark identity used by the released implementation.",
      "scope": {
        "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
        "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
        "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
        "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
      },
      "target": {
        "role": "attacker-side content constructor",
        "phase": "content construction",
        "source": "fixed benchmark code constant",
        "representation": "benchmark user identity matching the victim system prompt",
        "operation": "use to format content"
      },
      "verdict": "insufficient_evidence",
      "reason": "policy_scope_not_established",
      "matching_rules": [],
      "matching_observations": [
        {
          "edge": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "fixed benchmark code constant",
            "representation": "benchmark user identity matching the victim system prompt",
            "operation": "use to format content"
          },
          "status": "present",
          "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The matching benchmark identity constant is established to be an unauthorized source of user identity under ICoA’s declared access model.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "user_identity",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3 and https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5",
          "reason": "§2 excludes system-prompt access and §4.1 requires a matching identity, but the paper does not specify whether this separately sourced benchmark identity is permitted or prohibited.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3",
          "reason": "The cited fixed implementation audit binds the construction constant and configured system-prompt identity to matching values. This is static-source evidence for use of the separate constant, not a captured runtime request or a direct prompt read."
        },
        "refutation": {
          "basis": "none",
          "reference": "",
          "reason": "No positive counterevidence refutes this scoped suspicion."
        }
      },
      "claim_result": "unresolved",
      "note": "Published method and pinned static source. §2 restricts system-prompt access and leaves the rules for knowing the same identity through other means unspecified. The two pinned code/configuration constants have the same value.",
      "input_provenance_gap": {
        "description": "The benchmark uses a matching identity constant. The paper leaves open how an attacker obtains that identity under the stated access constraints.",
        "reference": "ICoA §2 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) and §4.1 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5)"
      }
    }
  ],
  "expected": "insufficient_evidence",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "icoa_direct_system_read",
          "source_group": "paper_text",
          "description": "Check for a direct read of the system prompt by the ICoA content constructor.",
          "scope": {
            "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
            "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
            "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
            "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
          },
          "target": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "victim system prompt",
            "representation": "system prompt content",
            "operation": "read directly"
          },
          "verdict": "insufficient_evidence",
          "reason": "evaluated_instance_alignment_not_established",
          "matching_rules": [
            {
              "edge": {
                "role": "attacker-side content constructor",
                "phase": "content construction",
                "source": "victim system prompt",
                "representation": "system prompt content",
                "operation": "read directly"
              },
              "permission": "deny",
              "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3"
            }
          ],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The ICoA content constructor directly reads the victim system prompt to obtain its user identity.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "user_identity",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3",
              "reason": "§2 denies access to the system prompt for the content constructor. A same-valued benchmark constant is a separate source and is not automatically a direct read of that prompt.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "",
              "reason": "The reviewed evidence identifies a matching identity constant but no direct system-prompt read at the construction boundary. Matching values neither establish such a read nor prove its absence."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "Published threat model and pinned static source. The §4.1 identity requirement and the code constant establish identity matching from a separate source. They provide no direct-read observation for the system-prompt edge. See https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49."
        },
        {
          "id": "icoa_benchmark_identity_source",
          "source_group": "paper_text",
          "description": "Determine whether the stated threat model covers the fixed benchmark identity used by the released implementation.",
          "scope": {
            "paper_version": "ICoA, EMNLP 2026 proceedings, ACL Anthology 2026.emnlp-main.2035",
            "experiment_arm": "AgentDojo 0.1.34 benchmark identity framing",
            "artifact_revision": "Author repository commit e333be8e1c319be3deb6942692aaed8e640a3954",
            "configuration": "Static source and configuration for the released AgentDojo benchmark setup"
          },
          "target": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "fixed benchmark code constant",
            "representation": "benchmark user identity matching the victim system prompt",
            "operation": "use to format content"
          },
          "verdict": "insufficient_evidence",
          "reason": "policy_scope_not_established",
          "matching_rules": [],
          "matching_observations": [
            {
              "edge": {
                "role": "attacker-side content constructor",
                "phase": "content construction",
                "source": "fixed benchmark code constant",
                "representation": "benchmark user identity matching the victim system prompt",
                "operation": "use to format content"
              },
              "status": "present",
              "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The matching benchmark identity constant is established to be an unauthorized source of user identity under ICoA’s declared access model.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "user_identity",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3 and https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5",
              "reason": "§2 excludes system-prompt access and §4.1 requires a matching identity, but the paper does not specify whether this separately sourced benchmark identity is permitted or prohibited.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49 and https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3",
              "reason": "The cited fixed implementation audit binds the construction constant and configured system-prompt identity to matching values. This is static-source evidence for use of the separate constant, not a captured runtime request or a direct prompt read."
            },
            "refutation": {
              "basis": "none",
              "reference": "",
              "reason": "No positive counterevidence refutes this scoped suspicion."
            }
          },
          "claim_result": "unresolved",
          "note": "Published method and pinned static source. §2 restricts system-prompt access and leaves the rules for knowing the same identity through other means unspecified. The two pinned code/configuration constants have the same value.",
          "input_provenance_gap": {
            "description": "The benchmark uses a matching identity constant. The paper leaves open how an attacker obtains that identity under the stated access constraints.",
            "reference": "ICoA §2 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) and §4.1 (https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5)"
          }
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "insufficient_evidence",
      "reason": "unresolved_checks"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "insufficient_evidence",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "curated_ipi",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 12. Attention Is All You Need

论文 ID：attention  
运行 / 判定：尚未运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 尚未运行 | \{"stage": "load\_curated\_records", "status": "not\_run", "reason": "no curated records; needs document\-input audit"\} |

#### 证据

```json
[]
```

#### 备注

```json
[]
```

#### 完整论文记录 JSON

```json
{
  "id": "attention",
  "title": "Attention Is All You Need",
  "source": "https://papers.nips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
  "status": "not_run",
  "verdict": "not_run",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "not_run",
      "reason": "no curated records; needs document-input audit"
    }
  ],
  "evidence": [],
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors.",
  "matches_gold": null
}
```

### 13. Deep Residual Learning for Image Recognition

论文 ID：resnet  
运行 / 判定：尚未运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 尚未运行 | \{"stage": "load\_curated\_records", "status": "not\_run", "reason": "no curated records; needs document\-input audit"\} |

#### 证据

```json
[]
```

#### 备注

```json
[]
```

#### 完整论文记录 JSON

```json
{
  "id": "resnet",
  "title": "Deep Residual Learning for Image Recognition",
  "source": "https://arxiv.org/pdf/1512.03385v1",
  "status": "not_run",
  "verdict": "not_run",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "not_run",
      "reason": "no curated records; needs document-input audit"
    }
  ],
  "evidence": [],
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors.",
  "matches_gold": null
}
```

### 14. Adam: A Method for Stochastic Optimization

论文 ID：adam  
运行 / 判定：尚未运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 尚未运行 | \{"stage": "load\_curated\_records", "status": "not\_run", "reason": "no curated records; needs document\-input audit"\} |

#### 证据

```json
[]
```

#### 备注

```json
[]
```

#### 完整论文记录 JSON

```json
{
  "id": "adam",
  "title": "Adam: A Method for Stochastic Optimization",
  "source": "https://arxiv.org/pdf/1412.6980v1",
  "status": "not_run",
  "verdict": "not_run",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "not_run",
      "reason": "no curated records; needs document-input audit"
    }
  ],
  "evidence": [],
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors.",
  "matches_gold": null
}
```

### 15. Trojan Hippo

论文 ID：trojan\_hippo  
运行 / 判定：审计范围内一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "trojan\_hippo\_explicit\_topic\_seed", "source\_group": "archived", "description": "Check the suspicion that choosing a sensitive topic for an explicit\-memory training seed is itself forbidden exact\-future\-task access\.", "scope": \{"paper\_version": "Trojan Hippo, arXiv:2605\.01970v1, Sections 3\.1 and 4\.1", "experiment\_arm": "Topic\-conditioned explicit\-memory seed construction during adaptive training", "artifact\_revision": "debesheedas/trojan\-hippo\-benchmark ebeb739dada097e06b125faa70e82e064482b64b; openevolve\_optimizer\.py SHA256 698a3aa055cf052deadb77b03910768a7a6a7771d8fc590101f9f8aefa999290", "configuration": "Static explicit\-memory branch with nonempty attack\_goal and tax in its description\. Only topic selection is judged here\. The separate source path that passes a concrete training user\_message to the mutator is acknowledged and is not relabelled topic\-only\."\}, "target": \{"role": "offline explicit\-memory seed builder", "phase": "adaptive training seed construction", "source": "configured attack goal topic", "representation": "sensitive topic category", "operation": "condition seed\-email topic"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "offline explicit\-memory seed builder", "phase": "adaptive training seed construction", "source": "configured attack goal topic", "representation": "sensitive topic category", "operation": "condition seed\-email topic"\}, "permission": "allow", "reference": "https://arxiv\.org/html/2605\.01970v1\#S4\.SS1 \(Section 4\.1, topic\-specific training and held\-out evaluation\)"\}\], "matching\_observations": \[\{"edge": \{"role": "offline explicit\-memory seed builder", "phase": "adaptive training seed construction", "source": "configured attack goal topic", "representation": "sensitive topic category", "operation": "condition seed\-email topic"\}, "status": "present", "reference": "https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive\_attacks/openevolve\_optimizer\.py\#L606\-L622; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive\_attacks/openevolve\_optimizer\.py\#L1168\-L1189"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The explicit\-memory offline seed builder violates the declared boundary merely by conditioning a seed on the configured tax topic\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "task\_category", "policy\_application": \{"status": "applicable", "reference": "https://arxiv\.org/html/2605\.01970v1\#S4\.SS1 \(Section 4\.1, topic\-specific training and held\-out evaluation\)", "reason": "Section 4\.1 explicitly defines attack generation for a selected topic, backend and defense\. That positive topic\-conditioned procedure applies to this offline seed branch\. No permission for arbitrary exact future test queries is inferred\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "topic\_only", "reference": "https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive\_attacks/openevolve\_optimizer\.py\#L606\-L622; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive\_attacks/openevolve\_optimizer\.py\#L1168\-L1189", "reason": "The explicit\-memory branch invokes \_build\_explicit\_seed\_emails; this helper derives a topic phrase from attack\_goal\.description and inserts that category into seed templates\. This source\-level path confirms the category input for the named operation, not the absence of concrete training queries elsewhere\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "https://arxiv\.org/html/2605\.01970v1\#S4\.SS1 \(Section 4\.1, topic\-specific training and held\-out evaluation\)", "reason": "The named allegation treats the documented topic condition as prohibited user\-query access\. The paper explicitly authorizes this topic\-conditioned attack\-generation procedure, refuting that narrow allegation\."\}\}, "claim\_result": "refuted"\}, \{"id": "trojan\_hippo\_tax\_rag\_transfer\_pair", "source\_group": "archived", "description": "Check a single fixed released train\_0 to test\_0 tax/rag/none pair rather than all Trojan Hippo historical executions\.", "scope": \{"paper\_version": "Trojan Hippo, arXiv:2605\.01970v1, Section 4\.1 train/test separation", "experiment\_arm": "One released tax/rag/none train\_0 and test\_0 01\.json pair plus the fixed\-payload propagation step", "artifact\_revision": "debesheedas/trojan\-hippo\-benchmark ebeb739dada097e06b125faa70e82e064482b64b; train\-file SHA256 251810fae0cd0407e0f84600283fd17370483d8d27dc3c8ee55de5f76444593c; test\-file SHA256 3a6593de0187682ebafe796ad0967a7e5791a9abfd226033458cec30234ee169", "configuration": "Static one\-pair transfer boundary only, no \-\-adaptive test execution\. Released step\-4 query hashes differ: train dbf1d4b57701d08b056ec9e04fc0f63553715fd0d1887b04560648707ebcad1a; test 48c231234016a5cd642cc347f5f710aca6187dd89ca1769a4f644c89cbd0e480\. Attack\-email objects have identical sorted\-key JSON SHA256 6d762ce840cd455e8027b47d06a26fff010eb07e8f671b97a5efd1bdde302740\. This does not establish absence of test\-query leakage in all branches or historical runs\."\}, "target": \{"role": "attack\-payload mutator", "phase": "fixed\-payload transfer for one released train/test pair", "source": "held\-out test\_0 tax/rag/none/01 step\-4 query", "representation": "held\-out test trigger query text", "operation": "condition payload regeneration during propagation", "query\_form": "full\_query"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_different\_instance", "matching\_rules": \[\], "matching\_observations": \[\{"edge": \{"role": "attack\-payload mutator", "phase": "fixed\-payload transfer for one released train/test pair", "source": "held\-out test\_0 tax/rag/none/01 step\-4 query", "representation": "held\-out test trigger query text", "operation": "condition payload regeneration during propagation", "query\_form": "full\_query"\}, "status": "absent", "reference": "https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L434\-L466; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L74\-L88; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/train\_0/tax/rag/none/01\.json; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/test\_0/tax/rag/none/01\.json"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The fixed propagation step for the released train\_0/tax/rag/none/01\.json to test\_0/tax/rag/none/01\.json pair feeds the held\-out test trigger query back into attack\-payload mutation\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "not\_applicable", "reference": "https://arxiv\.org/html/2605\.01970v1\#S4\.SS1 \(Section 4\.1, topic\-specific training and held\-out evaluation\); https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README\.md\#L127\-L132", "reason": "No prohibition is invented from the inability to modify user queries\. The suspected transfer of a training\-query input to this distinct test instance is refuted at the selected propagation boundary; the training mutator and held\-out transfer are different phases and instances\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "excluded", "evidence\_kind": "static\_bound\_path", "task\_relation": "different\_instance", "reference": "https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L434\-L466; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L74\-L88; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/train\_0/tax/rag/none/01\.json; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/test\_0/tax/rag/none/01\.json", "reason": "Positive boundary evidence: propagation chooses an existing attack using training caches and grouping metadata, then replaces only insert\_attack\_email\.attack\_email; it makes no mutator request with the test trigger\. The selected released pair has a different train and test trigger query and the same attack\-email object\. The exact training user\_message path elsewhere therefore is not evidence of delivery of this test query\."\}, "refutation": \{"basis": "different\_instance", "reference": "https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L434\-L466; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate\_train\_attack\_to\_test\_cases\.py\#L74\-L88; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/train\_0/tax/rag/none/01\.json; https://github\.com/debesheedas/trojan\-hippo\-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack\_bench/test\_0/tax/rag/none/01\.json", "reason": "The cited concrete training query and the named held\-out query are distinct instances, and the selected transfer operation excludes the claimed regeneration input\. This refutes only this one\-pair propagation allegation, not future\-query acquisition across the paper\."\}\}, "claim\_result": "refuted"\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "consistent\_within\_scope", "reason": "all\_required\_checks\_consistent"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "consistent\_within\_scope", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "trojan_hippo_explicit_topic_seed",
    "source_group": "archived",
    "description": "Check the suspicion that choosing a sensitive topic for an explicit-memory training seed is itself forbidden exact-future-task access.",
    "scope": {
      "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Sections 3.1 and 4.1",
      "experiment_arm": "Topic-conditioned explicit-memory seed construction during adaptive training",
      "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; openevolve_optimizer.py SHA256 698a3aa055cf052deadb77b03910768a7a6a7771d8fc590101f9f8aefa999290",
      "configuration": "Static explicit-memory branch with nonempty attack_goal and tax in its description. Only topic selection is judged here. The separate source path that passes a concrete training user_message to the mutator is acknowledged and is not relabelled topic-only."
    },
    "target": {
      "role": "offline explicit-memory seed builder",
      "phase": "adaptive training seed construction",
      "source": "configured attack goal topic",
      "representation": "sensitive topic category",
      "operation": "condition seed-email topic"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "offline explicit-memory seed builder",
          "phase": "adaptive training seed construction",
          "source": "configured attack goal topic",
          "representation": "sensitive topic category",
          "operation": "condition seed-email topic"
        },
        "permission": "allow",
        "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "offline explicit-memory seed builder",
          "phase": "adaptive training seed construction",
          "source": "configured attack goal topic",
          "representation": "sensitive topic category",
          "operation": "condition seed-email topic"
        },
        "status": "present",
        "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The explicit-memory offline seed builder violates the declared boundary merely by conditioning a seed on the configured tax topic.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "task_category",
      "policy_application": {
        "status": "applicable",
        "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
        "reason": "Section 4.1 explicitly defines attack generation for a selected topic, backend and defense. That positive topic-conditioned procedure applies to this offline seed branch. No permission for arbitrary exact future test queries is inferred.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "topic_only",
        "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189",
        "reason": "The explicit-memory branch invokes _build_explicit_seed_emails; this helper derives a topic phrase from attack_goal.description and inserts that category into seed templates. This source-level path confirms the category input for the named operation, not the absence of concrete training queries elsewhere."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
        "reason": "The named allegation treats the documented topic condition as prohibited user-query access. The paper explicitly authorizes this topic-conditioned attack-generation procedure, refuting that narrow allegation."
      }
    },
    "claim_result": "refuted"
  },
  {
    "id": "trojan_hippo_tax_rag_transfer_pair",
    "source_group": "archived",
    "description": "Check a single fixed released train_0 to test_0 tax/rag/none pair rather than all Trojan Hippo historical executions.",
    "scope": {
      "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Section 4.1 train/test separation",
      "experiment_arm": "One released tax/rag/none train_0 and test_0 01.json pair plus the fixed-payload propagation step",
      "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; train-file SHA256 251810fae0cd0407e0f84600283fd17370483d8d27dc3c8ee55de5f76444593c; test-file SHA256 3a6593de0187682ebafe796ad0967a7e5791a9abfd226033458cec30234ee169",
      "configuration": "Static one-pair transfer boundary only, no --adaptive test execution. Released step-4 query hashes differ: train dbf1d4b57701d08b056ec9e04fc0f63553715fd0d1887b04560648707ebcad1a; test 48c231234016a5cd642cc347f5f710aca6187dd89ca1769a4f644c89cbd0e480. Attack-email objects have identical sorted-key JSON SHA256 6d762ce840cd455e8027b47d06a26fff010eb07e8f671b97a5efd1bdde302740. This does not establish absence of test-query leakage in all branches or historical runs."
    },
    "target": {
      "role": "attack-payload mutator",
      "phase": "fixed-payload transfer for one released train/test pair",
      "source": "held-out test_0 tax/rag/none/01 step-4 query",
      "representation": "held-out test trigger query text",
      "operation": "condition payload regeneration during propagation",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_different_instance",
    "matching_rules": [],
    "matching_observations": [
      {
        "edge": {
          "role": "attack-payload mutator",
          "phase": "fixed-payload transfer for one released train/test pair",
          "source": "held-out test_0 tax/rag/none/01 step-4 query",
          "representation": "held-out test trigger query text",
          "operation": "condition payload regeneration during propagation",
          "query_form": "full_query"
        },
        "status": "absent",
        "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The fixed propagation step for the released train_0/tax/rag/none/01.json to test_0/tax/rag/none/01.json pair feeds the held-out test trigger query back into attack-payload mutation.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "not_applicable",
        "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation); https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README.md#L127-L132",
        "reason": "No prohibition is invented from the inability to modify user queries. The suspected transfer of a training-query input to this distinct test instance is refuted at the selected propagation boundary; the training mutator and held-out transfer are different phases and instances.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "excluded",
        "evidence_kind": "static_bound_path",
        "task_relation": "different_instance",
        "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
        "reason": "Positive boundary evidence: propagation chooses an existing attack using training caches and grouping metadata, then replaces only insert_attack_email.attack_email; it makes no mutator request with the test trigger. The selected released pair has a different train and test trigger query and the same attack-email object. The exact training user_message path elsewhere therefore is not evidence of delivery of this test query."
      },
      "refutation": {
        "basis": "different_instance",
        "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
        "reason": "The cited concrete training query and the named held-out query are distinct instances, and the selected transfer operation excludes the claimed regeneration input. This refutes only this one-pair propagation allegation, not future-query acquisition across the paper."
      }
    },
    "claim_result": "refuted"
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "trojan_hippo",
  "title": "Trojan Hippo",
  "version": "arXiv:2605.01970v1; released source ebeb739dada097e06b125faa70e82e064482b64b",
  "audit_scope": "Two bounded suspicions only: permitted tax-topic conditioning in the explicit-memory offline seed helper, and alleged held-out-query feedback in the fixed propagation boundary of the single released train_0/test_0 tax/rag/none/01 pair. Explicitly does not claim that the training mutator sees only topic labels; its concrete training-query input is acknowledged. No global claim about all tests, configurations or historical executions.",
  "verdict": "consistent_within_scope",
  "has_confirmed_inconsistency": false,
  "reason": "all_required_checks_consistent",
  "coverage_complete": true,
  "required_checks": 2,
  "resolved_checks": 2,
  "confirmed_findings": [],
  "unresolved_checks": [],
  "claim_result_counts": {
    "refuted": 2
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "trojan_hippo_explicit_topic_seed",
      "source_group": "archived",
      "description": "Check the suspicion that choosing a sensitive topic for an explicit-memory training seed is itself forbidden exact-future-task access.",
      "scope": {
        "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Sections 3.1 and 4.1",
        "experiment_arm": "Topic-conditioned explicit-memory seed construction during adaptive training",
        "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; openevolve_optimizer.py SHA256 698a3aa055cf052deadb77b03910768a7a6a7771d8fc590101f9f8aefa999290",
        "configuration": "Static explicit-memory branch with nonempty attack_goal and tax in its description. Only topic selection is judged here. The separate source path that passes a concrete training user_message to the mutator is acknowledged and is not relabelled topic-only."
      },
      "target": {
        "role": "offline explicit-memory seed builder",
        "phase": "adaptive training seed construction",
        "source": "configured attack goal topic",
        "representation": "sensitive topic category",
        "operation": "condition seed-email topic"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "offline explicit-memory seed builder",
            "phase": "adaptive training seed construction",
            "source": "configured attack goal topic",
            "representation": "sensitive topic category",
            "operation": "condition seed-email topic"
          },
          "permission": "allow",
          "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "offline explicit-memory seed builder",
            "phase": "adaptive training seed construction",
            "source": "configured attack goal topic",
            "representation": "sensitive topic category",
            "operation": "condition seed-email topic"
          },
          "status": "present",
          "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The explicit-memory offline seed builder violates the declared boundary merely by conditioning a seed on the configured tax topic.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "task_category",
        "policy_application": {
          "status": "applicable",
          "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
          "reason": "Section 4.1 explicitly defines attack generation for a selected topic, backend and defense. That positive topic-conditioned procedure applies to this offline seed branch. No permission for arbitrary exact future test queries is inferred.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "topic_only",
          "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189",
          "reason": "The explicit-memory branch invokes _build_explicit_seed_emails; this helper derives a topic phrase from attack_goal.description and inserts that category into seed templates. This source-level path confirms the category input for the named operation, not the absence of concrete training queries elsewhere."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
          "reason": "The named allegation treats the documented topic condition as prohibited user-query access. The paper explicitly authorizes this topic-conditioned attack-generation procedure, refuting that narrow allegation."
        }
      },
      "claim_result": "refuted"
    },
    {
      "id": "trojan_hippo_tax_rag_transfer_pair",
      "source_group": "archived",
      "description": "Check a single fixed released train_0 to test_0 tax/rag/none pair rather than all Trojan Hippo historical executions.",
      "scope": {
        "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Section 4.1 train/test separation",
        "experiment_arm": "One released tax/rag/none train_0 and test_0 01.json pair plus the fixed-payload propagation step",
        "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; train-file SHA256 251810fae0cd0407e0f84600283fd17370483d8d27dc3c8ee55de5f76444593c; test-file SHA256 3a6593de0187682ebafe796ad0967a7e5791a9abfd226033458cec30234ee169",
        "configuration": "Static one-pair transfer boundary only, no --adaptive test execution. Released step-4 query hashes differ: train dbf1d4b57701d08b056ec9e04fc0f63553715fd0d1887b04560648707ebcad1a; test 48c231234016a5cd642cc347f5f710aca6187dd89ca1769a4f644c89cbd0e480. Attack-email objects have identical sorted-key JSON SHA256 6d762ce840cd455e8027b47d06a26fff010eb07e8f671b97a5efd1bdde302740. This does not establish absence of test-query leakage in all branches or historical runs."
      },
      "target": {
        "role": "attack-payload mutator",
        "phase": "fixed-payload transfer for one released train/test pair",
        "source": "held-out test_0 tax/rag/none/01 step-4 query",
        "representation": "held-out test trigger query text",
        "operation": "condition payload regeneration during propagation",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_different_instance",
      "matching_rules": [],
      "matching_observations": [
        {
          "edge": {
            "role": "attack-payload mutator",
            "phase": "fixed-payload transfer for one released train/test pair",
            "source": "held-out test_0 tax/rag/none/01 step-4 query",
            "representation": "held-out test trigger query text",
            "operation": "condition payload regeneration during propagation",
            "query_form": "full_query"
          },
          "status": "absent",
          "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The fixed propagation step for the released train_0/tax/rag/none/01.json to test_0/tax/rag/none/01.json pair feeds the held-out test trigger query back into attack-payload mutation.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "not_applicable",
          "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation); https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README.md#L127-L132",
          "reason": "No prohibition is invented from the inability to modify user queries. The suspected transfer of a training-query input to this distinct test instance is refuted at the selected propagation boundary; the training mutator and held-out transfer are different phases and instances.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "excluded",
          "evidence_kind": "static_bound_path",
          "task_relation": "different_instance",
          "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
          "reason": "Positive boundary evidence: propagation chooses an existing attack using training caches and grouping metadata, then replaces only insert_attack_email.attack_email; it makes no mutator request with the test trigger. The selected released pair has a different train and test trigger query and the same attack-email object. The exact training user_message path elsewhere therefore is not evidence of delivery of this test query."
        },
        "refutation": {
          "basis": "different_instance",
          "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
          "reason": "The cited concrete training query and the named held-out query are distinct instances, and the selected transfer operation excludes the claimed regeneration input. This refutes only this one-pair propagation allegation, not future-query acquisition across the paper."
        }
      },
      "claim_result": "refuted"
    }
  ],
  "expected": "consistent_within_scope",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "trojan_hippo_explicit_topic_seed",
          "source_group": "archived",
          "description": "Check the suspicion that choosing a sensitive topic for an explicit-memory training seed is itself forbidden exact-future-task access.",
          "scope": {
            "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Sections 3.1 and 4.1",
            "experiment_arm": "Topic-conditioned explicit-memory seed construction during adaptive training",
            "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; openevolve_optimizer.py SHA256 698a3aa055cf052deadb77b03910768a7a6a7771d8fc590101f9f8aefa999290",
            "configuration": "Static explicit-memory branch with nonempty attack_goal and tax in its description. Only topic selection is judged here. The separate source path that passes a concrete training user_message to the mutator is acknowledged and is not relabelled topic-only."
          },
          "target": {
            "role": "offline explicit-memory seed builder",
            "phase": "adaptive training seed construction",
            "source": "configured attack goal topic",
            "representation": "sensitive topic category",
            "operation": "condition seed-email topic"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "offline explicit-memory seed builder",
                "phase": "adaptive training seed construction",
                "source": "configured attack goal topic",
                "representation": "sensitive topic category",
                "operation": "condition seed-email topic"
              },
              "permission": "allow",
              "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "offline explicit-memory seed builder",
                "phase": "adaptive training seed construction",
                "source": "configured attack goal topic",
                "representation": "sensitive topic category",
                "operation": "condition seed-email topic"
              },
              "status": "present",
              "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The explicit-memory offline seed builder violates the declared boundary merely by conditioning a seed on the configured tax topic.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "task_category",
            "policy_application": {
              "status": "applicable",
              "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
              "reason": "Section 4.1 explicitly defines attack generation for a selected topic, backend and defense. That positive topic-conditioned procedure applies to this offline seed branch. No permission for arbitrary exact future test queries is inferred.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "topic_only",
              "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L622; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1168-L1189",
              "reason": "The explicit-memory branch invokes _build_explicit_seed_emails; this helper derives a topic phrase from attack_goal.description and inserts that category into seed templates. This source-level path confirms the category input for the named operation, not the absence of concrete training queries elsewhere."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation)",
              "reason": "The named allegation treats the documented topic condition as prohibited user-query access. The paper explicitly authorizes this topic-conditioned attack-generation procedure, refuting that narrow allegation."
            }
          },
          "claim_result": "refuted"
        },
        {
          "id": "trojan_hippo_tax_rag_transfer_pair",
          "source_group": "archived",
          "description": "Check a single fixed released train_0 to test_0 tax/rag/none pair rather than all Trojan Hippo historical executions.",
          "scope": {
            "paper_version": "Trojan Hippo, arXiv:2605.01970v1, Section 4.1 train/test separation",
            "experiment_arm": "One released tax/rag/none train_0 and test_0 01.json pair plus the fixed-payload propagation step",
            "artifact_revision": "debesheedas/trojan-hippo-benchmark ebeb739dada097e06b125faa70e82e064482b64b; train-file SHA256 251810fae0cd0407e0f84600283fd17370483d8d27dc3c8ee55de5f76444593c; test-file SHA256 3a6593de0187682ebafe796ad0967a7e5791a9abfd226033458cec30234ee169",
            "configuration": "Static one-pair transfer boundary only, no --adaptive test execution. Released step-4 query hashes differ: train dbf1d4b57701d08b056ec9e04fc0f63553715fd0d1887b04560648707ebcad1a; test 48c231234016a5cd642cc347f5f710aca6187dd89ca1769a4f644c89cbd0e480. Attack-email objects have identical sorted-key JSON SHA256 6d762ce840cd455e8027b47d06a26fff010eb07e8f671b97a5efd1bdde302740. This does not establish absence of test-query leakage in all branches or historical runs."
          },
          "target": {
            "role": "attack-payload mutator",
            "phase": "fixed-payload transfer for one released train/test pair",
            "source": "held-out test_0 tax/rag/none/01 step-4 query",
            "representation": "held-out test trigger query text",
            "operation": "condition payload regeneration during propagation",
            "query_form": "full_query"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_different_instance",
          "matching_rules": [],
          "matching_observations": [
            {
              "edge": {
                "role": "attack-payload mutator",
                "phase": "fixed-payload transfer for one released train/test pair",
                "source": "held-out test_0 tax/rag/none/01 step-4 query",
                "representation": "held-out test trigger query text",
                "operation": "condition payload regeneration during propagation",
                "query_form": "full_query"
              },
              "status": "absent",
              "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The fixed propagation step for the released train_0/tax/rag/none/01.json to test_0/tax/rag/none/01.json pair feeds the held-out test trigger query back into attack-payload mutation.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "not_applicable",
              "reference": "https://arxiv.org/html/2605.01970v1#S4.SS1 (Section 4.1, topic-specific training and held-out evaluation); https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README.md#L127-L132",
              "reason": "No prohibition is invented from the inability to modify user queries. The suspected transfer of a training-query input to this distinct test instance is refuted at the selected propagation boundary; the training mutator and held-out transfer are different phases and instances.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "excluded",
              "evidence_kind": "static_bound_path",
              "task_relation": "different_instance",
              "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
              "reason": "Positive boundary evidence: propagation chooses an existing attack using training caches and grouping metadata, then replaces only insert_attack_email.attack_email; it makes no mutator request with the test trigger. The selected released pair has a different train and test trigger query and the same attack-email object. The exact training user_message path elsewhere therefore is not evidence of delivery of this test query."
            },
            "refutation": {
              "basis": "different_instance",
              "reference": "https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/train_0/tax/rag/none/01.json; https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/data/benchmark/attack_bench/test_0/tax/rag/none/01.json",
              "reason": "The cited concrete training query and the named held-out query are distinct instances, and the selected transfer operation excludes the claimed regeneration input. This refutes only this one-pair propagation allegation, not future-query acquisition across the paper."
            }
          },
          "claim_result": "refuted"
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "consistent_within_scope",
      "reason": "all_required_checks_consistent"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "consistent_within_scope",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "previously_suspected_control",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 16. TopicAttack

论文 ID：topicattack  
运行 / 判定：审计范围内一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 2\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "topicattack\_default\_chatbot\_benign\_document", "source\_group": "archived", "description": "Check the original suspicion that document\-conditioned TopicAttack generation itself violates the no\-user\-instruction knowledge boundary\.", "scope": \{"paper\_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4\.2", "experiment\_arm": "Released default chatbot attack construction using attack\_prompt\_transfer\.txt", "artifact\_revision": "LukeChen\-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; construct\_attack\.py SHA256 eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732", "configuration": "Static source boundary only: default GPTChatbot, default empty chatbot\_system\.txt, default transition template\. Independent user\-instruction access is a separate required claim; no historical runtime assertions\."\}, "target": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "attacker\-visible benign document input field", "representation": "benign document text", "operation": "condition transition\-generation request"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_explicit\_permission", "matching\_rules": \[\{"edge": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "attacker\-visible benign document input field", "representation": "benign document text", "operation": "condition transition\-generation request"\}, "permission": "allow", "reference": "https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf\#page=4 \(Section 3, Attackers Knowledge, continued from PDF page 3\)"\}\], "matching\_observations": \[\{"edge": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "attacker\-visible benign document input field", "representation": "benign document text", "operation": "condition transition\-generation request"\}, "status": "present", "reference": "https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct\_attack\.py\#L7\-L15; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack\_prompt\_transfer\.txt"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The default chatbot attack\-generation request violates the declared knowledge boundary merely by including the benign document text\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "document\_content", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf\#page=4 \(Section 3, Attackers Knowledge, continued from PDF page 3\)", "reason": "Section 3 expressly permits the attacker to know the benign content being injected\. This rule applies to document content, not to the separate original user\-instruction field\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "confirmed", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct\_attack\.py\#L7\-L15; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack\_prompt\_transfer\.txt", "reason": "construct\_attack\.py formats d\_item\[input\] into the default transition template and passes the rendered message to model\.respond\. This is a bound source\-level input path, not merely a dataset field existing and not a saved model request\."\}, "refutation": \{"basis": "explicit\_permission", "reference": "https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf\#page=4 \(Section 3, Attackers Knowledge, continued from PDF page 3\)", "reason": "The named suspicion mistakes explicitly permitted document visibility for prohibited access to the original user instruction\. Permission refutes this specific access claim, without asserting global paper consistency\."\}\}, "claim\_result": "refuted"\}, \{"id": "topicattack\_default\_chatbot\_user\_instruction\_excluded", "source\_group": "archived", "description": "Check whether the original user\-instruction field is independently delivered in the default chatbot construction messages\.", "scope": \{"paper\_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4\.2", "experiment\_arm": "Released default chatbot generation request, including its wrapper and empty system prompt", "artifact\_revision": "LukeChen\-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; chatbot\.py SHA256 21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4; default chatbot\_system\.txt empty SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "configuration": "Full direct request\-construction boundary only\. construct\_attack\.py reads the default template and passes a rendered string; GPTChatbot\.respond constructs messages from that string plus the empty default system prompt\. No custom template/system, natural\-language inference, other generator, or historical\-run claim\."\}, "target": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "independent original user instruction field", "representation": "original user instruction text", "operation": "condition transition\-generation request", "query\_form": "full\_query"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_excluded\_delivery", "matching\_rules": \[\{"edge": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "independent original user instruction field", "representation": "original user instruction text", "operation": "condition transition\-generation request", "query\_form": "full\_query"\}, "permission": "deny", "reference": "https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf\#page=4 \(Section 3, Attackers Knowledge, continued from PDF page 3\)"\}\], "matching\_observations": \[\{"edge": \{"role": "auxiliary attack\-generation LLM", "phase": "default chatbot payload construction", "source": "independent original user instruction field", "representation": "original user instruction text", "operation": "condition transition\-generation request", "query\_form": "full\_query"\}, "status": "absent", "reference": "https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct\_attack\.py\#L7\-L15; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot\.py\#L63\-L91; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot\_system\.txt; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack\_prompt\_transfer\.txt"\}\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The released default chatbot constructor sends d\_item\[instruction\] as an independent input to the auxiliary attack\-generation LLM\.", "issue\_type": "information\_boundary", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "applicable", "reference": "https://aclanthology\.org/2025\.emnlp\-main\.372\.pdf\#page=4 \(Section 3, Attackers Knowledge, continued from PDF page 3\)", "reason": "The no\-original\-user\-input restriction applies to the attack\-generation LLM in this declared construction setting\. The separate allowed benign\-document input is not reclassified as a query\.", "policy\_kind": "attacker\_knowledge\_constraint"\}, "delivery": \{"status": "excluded", "evidence\_kind": "static\_bound\_path", "task\_relation": "same\_evaluated\_instance", "reference": "https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct\_attack\.py\#L7\-L15; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot\.py\#L63\-L91; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot\_system\.txt; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack\_prompt\_transfer\.txt", "reason": "Positive request\-boundary proof: the constructor renders only input, attacker injection, attacker target topic and fixed turn count; the selected template contains those slots; GPTChatbot\.respond sends only the supplied rendered string and the empty default system string\. No instruction\-field slot or conversation\-history append exists on this selected direct path\. The enclosing dataset object may still store instruction for evaluation\. This does not exclude inference of task facts from allowed content\."\}, "refutation": \{"basis": "excluded\_delivery", "reference": "https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct\_attack\.py\#L7\-L15; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot\.py\#L63\-L91; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot\_system\.txt; https://github\.com/LukeChen\-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack\_prompt\_transfer\.txt", "reason": "The alleged independent instruction\-field delivery is excluded by the complete selected message\-construction path, not by a repository\-wide failed text search\. The conclusion is limited to this default direct request\."\}\}, "claim\_result": "refuted"\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "consistent\_within\_scope", "reason": "all\_required\_checks\_consistent"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "consistent\_within\_scope", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "topicattack_default_chatbot_benign_document",
    "source_group": "archived",
    "description": "Check the original suspicion that document-conditioned TopicAttack generation itself violates the no-user-instruction knowledge boundary.",
    "scope": {
      "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
      "experiment_arm": "Released default chatbot attack construction using attack_prompt_transfer.txt",
      "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; construct_attack.py SHA256 eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732",
      "configuration": "Static source boundary only: default GPTChatbot, default empty chatbot_system.txt, default transition template. Independent user-instruction access is a separate required claim; no historical runtime assertions."
    },
    "target": {
      "role": "auxiliary attack-generation LLM",
      "phase": "default chatbot payload construction",
      "source": "attacker-visible benign document input field",
      "representation": "benign document text",
      "operation": "condition transition-generation request"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_explicit_permission",
    "matching_rules": [
      {
        "edge": {
          "role": "auxiliary attack-generation LLM",
          "phase": "default chatbot payload construction",
          "source": "attacker-visible benign document input field",
          "representation": "benign document text",
          "operation": "condition transition-generation request"
        },
        "permission": "allow",
        "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "auxiliary attack-generation LLM",
          "phase": "default chatbot payload construction",
          "source": "attacker-visible benign document input field",
          "representation": "benign document text",
          "operation": "condition transition-generation request"
        },
        "status": "present",
        "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The default chatbot attack-generation request violates the declared knowledge boundary merely by including the benign document text.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "document_content",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
        "reason": "Section 3 expressly permits the attacker to know the benign content being injected. This rule applies to document content, not to the separate original user-instruction field.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "confirmed",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
        "reason": "construct_attack.py formats d_item[input] into the default transition template and passes the rendered message to model.respond. This is a bound source-level input path, not merely a dataset field existing and not a saved model request."
      },
      "refutation": {
        "basis": "explicit_permission",
        "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
        "reason": "The named suspicion mistakes explicitly permitted document visibility for prohibited access to the original user instruction. Permission refutes this specific access claim, without asserting global paper consistency."
      }
    },
    "claim_result": "refuted"
  },
  {
    "id": "topicattack_default_chatbot_user_instruction_excluded",
    "source_group": "archived",
    "description": "Check whether the original user-instruction field is independently delivered in the default chatbot construction messages.",
    "scope": {
      "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
      "experiment_arm": "Released default chatbot generation request, including its wrapper and empty system prompt",
      "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; chatbot.py SHA256 21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4; default chatbot_system.txt empty SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "configuration": "Full direct request-construction boundary only. construct_attack.py reads the default template and passes a rendered string; GPTChatbot.respond constructs messages from that string plus the empty default system prompt. No custom template/system, natural-language inference, other generator, or historical-run claim."
    },
    "target": {
      "role": "auxiliary attack-generation LLM",
      "phase": "default chatbot payload construction",
      "source": "independent original user instruction field",
      "representation": "original user instruction text",
      "operation": "condition transition-generation request",
      "query_form": "full_query"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_excluded_delivery",
    "matching_rules": [
      {
        "edge": {
          "role": "auxiliary attack-generation LLM",
          "phase": "default chatbot payload construction",
          "source": "independent original user instruction field",
          "representation": "original user instruction text",
          "operation": "condition transition-generation request",
          "query_form": "full_query"
        },
        "permission": "deny",
        "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
      }
    ],
    "matching_observations": [
      {
        "edge": {
          "role": "auxiliary attack-generation LLM",
          "phase": "default chatbot payload construction",
          "source": "independent original user instruction field",
          "representation": "original user instruction text",
          "operation": "condition transition-generation request",
          "query_form": "full_query"
        },
        "status": "absent",
        "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
      }
    ],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The released default chatbot constructor sends d_item[instruction] as an independent input to the auxiliary attack-generation LLM.",
    "issue_type": "information_boundary",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "applicable",
        "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
        "reason": "The no-original-user-input restriction applies to the attack-generation LLM in this declared construction setting. The separate allowed benign-document input is not reclassified as a query.",
        "policy_kind": "attacker_knowledge_constraint"
      },
      "delivery": {
        "status": "excluded",
        "evidence_kind": "static_bound_path",
        "task_relation": "same_evaluated_instance",
        "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
        "reason": "Positive request-boundary proof: the constructor renders only input, attacker injection, attacker target topic and fixed turn count; the selected template contains those slots; GPTChatbot.respond sends only the supplied rendered string and the empty default system string. No instruction-field slot or conversation-history append exists on this selected direct path. The enclosing dataset object may still store instruction for evaluation. This does not exclude inference of task facts from allowed content."
      },
      "refutation": {
        "basis": "excluded_delivery",
        "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
        "reason": "The alleged independent instruction-field delivery is excluded by the complete selected message-construction path, not by a repository-wide failed text search. The conclusion is limited to this default direct request."
      }
    },
    "claim_result": "refuted"
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "topicattack",
  "title": "TopicAttack",
  "version": "EMNLP 2025 final; released source 2aced58ad6f3587c8ba064b5e5cad74a29ef41de",
  "audit_scope": "Two specific allegations at the default released chatbot construction boundary: that explicitly allowed benign-document conditioning is prohibited, and that the independent original user-instruction field enters that generation request. Includes the selected wrapper and empty default system prompt. Excludes custom templates, agent/defense branches, natural-language inference from permitted content, and unobserved historical executions.",
  "verdict": "consistent_within_scope",
  "has_confirmed_inconsistency": false,
  "reason": "all_required_checks_consistent",
  "coverage_complete": true,
  "required_checks": 2,
  "resolved_checks": 2,
  "confirmed_findings": [],
  "unresolved_checks": [],
  "claim_result_counts": {
    "refuted": 2
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "topicattack_default_chatbot_benign_document",
      "source_group": "archived",
      "description": "Check the original suspicion that document-conditioned TopicAttack generation itself violates the no-user-instruction knowledge boundary.",
      "scope": {
        "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
        "experiment_arm": "Released default chatbot attack construction using attack_prompt_transfer.txt",
        "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; construct_attack.py SHA256 eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732",
        "configuration": "Static source boundary only: default GPTChatbot, default empty chatbot_system.txt, default transition template. Independent user-instruction access is a separate required claim; no historical runtime assertions."
      },
      "target": {
        "role": "auxiliary attack-generation LLM",
        "phase": "default chatbot payload construction",
        "source": "attacker-visible benign document input field",
        "representation": "benign document text",
        "operation": "condition transition-generation request"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_explicit_permission",
      "matching_rules": [
        {
          "edge": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "attacker-visible benign document input field",
            "representation": "benign document text",
            "operation": "condition transition-generation request"
          },
          "permission": "allow",
          "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "attacker-visible benign document input field",
            "representation": "benign document text",
            "operation": "condition transition-generation request"
          },
          "status": "present",
          "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The default chatbot attack-generation request violates the declared knowledge boundary merely by including the benign document text.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "document_content",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
          "reason": "Section 3 expressly permits the attacker to know the benign content being injected. This rule applies to document content, not to the separate original user-instruction field.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "confirmed",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
          "reason": "construct_attack.py formats d_item[input] into the default transition template and passes the rendered message to model.respond. This is a bound source-level input path, not merely a dataset field existing and not a saved model request."
        },
        "refutation": {
          "basis": "explicit_permission",
          "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
          "reason": "The named suspicion mistakes explicitly permitted document visibility for prohibited access to the original user instruction. Permission refutes this specific access claim, without asserting global paper consistency."
        }
      },
      "claim_result": "refuted"
    },
    {
      "id": "topicattack_default_chatbot_user_instruction_excluded",
      "source_group": "archived",
      "description": "Check whether the original user-instruction field is independently delivered in the default chatbot construction messages.",
      "scope": {
        "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
        "experiment_arm": "Released default chatbot generation request, including its wrapper and empty system prompt",
        "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; chatbot.py SHA256 21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4; default chatbot_system.txt empty SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "configuration": "Full direct request-construction boundary only. construct_attack.py reads the default template and passes a rendered string; GPTChatbot.respond constructs messages from that string plus the empty default system prompt. No custom template/system, natural-language inference, other generator, or historical-run claim."
      },
      "target": {
        "role": "auxiliary attack-generation LLM",
        "phase": "default chatbot payload construction",
        "source": "independent original user instruction field",
        "representation": "original user instruction text",
        "operation": "condition transition-generation request",
        "query_form": "full_query"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_excluded_delivery",
      "matching_rules": [
        {
          "edge": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "independent original user instruction field",
            "representation": "original user instruction text",
            "operation": "condition transition-generation request",
            "query_form": "full_query"
          },
          "permission": "deny",
          "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
        }
      ],
      "matching_observations": [
        {
          "edge": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "independent original user instruction field",
            "representation": "original user instruction text",
            "operation": "condition transition-generation request",
            "query_form": "full_query"
          },
          "status": "absent",
          "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
        }
      ],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The released default chatbot constructor sends d_item[instruction] as an independent input to the auxiliary attack-generation LLM.",
      "issue_type": "information_boundary",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "applicable",
          "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
          "reason": "The no-original-user-input restriction applies to the attack-generation LLM in this declared construction setting. The separate allowed benign-document input is not reclassified as a query.",
          "policy_kind": "attacker_knowledge_constraint"
        },
        "delivery": {
          "status": "excluded",
          "evidence_kind": "static_bound_path",
          "task_relation": "same_evaluated_instance",
          "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
          "reason": "Positive request-boundary proof: the constructor renders only input, attacker injection, attacker target topic and fixed turn count; the selected template contains those slots; GPTChatbot.respond sends only the supplied rendered string and the empty default system string. No instruction-field slot or conversation-history append exists on this selected direct path. The enclosing dataset object may still store instruction for evaluation. This does not exclude inference of task facts from allowed content."
        },
        "refutation": {
          "basis": "excluded_delivery",
          "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
          "reason": "The alleged independent instruction-field delivery is excluded by the complete selected message-construction path, not by a repository-wide failed text search. The conclusion is limited to this default direct request."
        }
      },
      "claim_result": "refuted"
    }
  ],
  "expected": "consistent_within_scope",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 2
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "topicattack_default_chatbot_benign_document",
          "source_group": "archived",
          "description": "Check the original suspicion that document-conditioned TopicAttack generation itself violates the no-user-instruction knowledge boundary.",
          "scope": {
            "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
            "experiment_arm": "Released default chatbot attack construction using attack_prompt_transfer.txt",
            "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; construct_attack.py SHA256 eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732",
            "configuration": "Static source boundary only: default GPTChatbot, default empty chatbot_system.txt, default transition template. Independent user-instruction access is a separate required claim; no historical runtime assertions."
          },
          "target": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "attacker-visible benign document input field",
            "representation": "benign document text",
            "operation": "condition transition-generation request"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_explicit_permission",
          "matching_rules": [
            {
              "edge": {
                "role": "auxiliary attack-generation LLM",
                "phase": "default chatbot payload construction",
                "source": "attacker-visible benign document input field",
                "representation": "benign document text",
                "operation": "condition transition-generation request"
              },
              "permission": "allow",
              "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "auxiliary attack-generation LLM",
                "phase": "default chatbot payload construction",
                "source": "attacker-visible benign document input field",
                "representation": "benign document text",
                "operation": "condition transition-generation request"
              },
              "status": "present",
              "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The default chatbot attack-generation request violates the declared knowledge boundary merely by including the benign document text.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "document_content",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
              "reason": "Section 3 expressly permits the attacker to know the benign content being injected. This rule applies to document content, not to the separate original user-instruction field.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "confirmed",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
              "reason": "construct_attack.py formats d_item[input] into the default transition template and passes the rendered message to model.respond. This is a bound source-level input path, not merely a dataset field existing and not a saved model request."
            },
            "refutation": {
              "basis": "explicit_permission",
              "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
              "reason": "The named suspicion mistakes explicitly permitted document visibility for prohibited access to the original user instruction. Permission refutes this specific access claim, without asserting global paper consistency."
            }
          },
          "claim_result": "refuted"
        },
        {
          "id": "topicattack_default_chatbot_user_instruction_excluded",
          "source_group": "archived",
          "description": "Check whether the original user-instruction field is independently delivered in the default chatbot construction messages.",
          "scope": {
            "paper_version": "TopicAttack, EMNLP 2025 final, Section 3 and Section 4.2",
            "experiment_arm": "Released default chatbot generation request, including its wrapper and empty system prompt",
            "artifact_revision": "LukeChen-go/topicattack 2aced58ad6f3587c8ba064b5e5cad74a29ef41de; chatbot.py SHA256 21fd3e1323bc7279cad32ccf36bd0b88f69c0c50baeb9fae5f918f201dcbf0e4; default chatbot_system.txt empty SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "configuration": "Full direct request-construction boundary only. construct_attack.py reads the default template and passes a rendered string; GPTChatbot.respond constructs messages from that string plus the empty default system prompt. No custom template/system, natural-language inference, other generator, or historical-run claim."
          },
          "target": {
            "role": "auxiliary attack-generation LLM",
            "phase": "default chatbot payload construction",
            "source": "independent original user instruction field",
            "representation": "original user instruction text",
            "operation": "condition transition-generation request",
            "query_form": "full_query"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_excluded_delivery",
          "matching_rules": [
            {
              "edge": {
                "role": "auxiliary attack-generation LLM",
                "phase": "default chatbot payload construction",
                "source": "independent original user instruction field",
                "representation": "original user instruction text",
                "operation": "condition transition-generation request",
                "query_form": "full_query"
              },
              "permission": "deny",
              "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)"
            }
          ],
          "matching_observations": [
            {
              "edge": {
                "role": "auxiliary attack-generation LLM",
                "phase": "default chatbot payload construction",
                "source": "independent original user instruction field",
                "representation": "original user instruction text",
                "operation": "condition transition-generation request",
                "query_form": "full_query"
              },
              "status": "absent",
              "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt"
            }
          ],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The released default chatbot constructor sends d_item[instruction] as an independent input to the auxiliary attack-generation LLM.",
          "issue_type": "information_boundary",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "applicable",
              "reference": "https://aclanthology.org/2025.emnlp-main.372.pdf#page=4 (Section 3, Attackers Knowledge, continued from PDF page 3)",
              "reason": "The no-original-user-input restriction applies to the attack-generation LLM in this declared construction setting. The separate allowed benign-document input is not reclassified as a query.",
              "policy_kind": "attacker_knowledge_constraint"
            },
            "delivery": {
              "status": "excluded",
              "evidence_kind": "static_bound_path",
              "task_relation": "same_evaluated_instance",
              "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
              "reason": "Positive request-boundary proof: the constructor renders only input, attacker injection, attacker target topic and fixed turn count; the selected template contains those slots; GPTChatbot.respond sends only the supplied rendered string and the empty default system string. No instruction-field slot or conversation-history append exists on this selected direct path. The enclosing dataset object may still store instruction for evaluation. This does not exclude inference of task facts from allowed content."
            },
            "refutation": {
              "basis": "excluded_delivery",
              "reference": "https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/chatbot.py#L63-L91; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/chatbot_system.txt; https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt",
              "reason": "The alleged independent instruction-field delivery is excluded by the complete selected message-construction path, not by a repository-wide failed text search. The conclusion is limited to this default direct request."
            }
          },
          "claim_result": "refuted"
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "consistent_within_scope",
      "reason": "all_required_checks_consistent"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "consistent_within_scope",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "previously_suspected_control",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 17. AgentDojo

论文 ID：agentdojo  
运行 / 判定：审计范围内一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "agentdojo\_utility\_only\_information\_inference", "source\_group": "paper\_text", "description": "Exclude the particular inference from task\-integrity outcomes to an information\-boundary finding; do not declare the paper globally free of information issues\.", "scope": \{"paper\_version": "AgentDojo, NeurIPS 2024 final; arXiv:2406\.13352v3 body cross\-check, §§3\.3–3\.4", "experiment\_arm": "Logical control for a reported task\-utility perturbation, not a reproduced experiment", "artifact\_revision": "Fixed conference PDF and arXiv v3; attachment report is not an independently verified run", "configuration": "Assess only whether a reported content\-overwrite/utility phenomenon by itself proves unauthorized private\-query delivery"\}, "target": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "victim private request", "representation": "exact private user\-request text", "operation": "receive as construction input"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_different\_issue\_type", "matching\_rules": \[\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The reported task\-critical\-content overwrite or utility change by itself establishes prohibited private\-query delivery to an attack constructor\.", "issue\_type": "task\_integrity", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "uncertain", "reference": "https://arxiv\.org/html/2406\.13352v3\#S3\.SS3", "reason": "§3\.3 allows varying attacker knowledge and §3\.4 defines distinct utility and targeted\-success outcomes\. Those definitions do not bind a particular prohibited private\-query flow for the phenomenon in this control\.", "policy\_kind": "protocol\_requirement"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "", "reason": "No corresponding raw construction request or private\-query delivery evidence was supplied for this reported phenomenon\."\}, "refutation": \{"basis": "different\_issue\_type", "reference": "https://arxiv\.org/html/2406\.13352v3\#S3\.SS4", "reason": "Content integrity and task utility concern task completion and outcome interpretation\. Those outcomes alone do not establish prohibited information receipt; this refutes only the claimed sufficiency of that inference\."\}\}, "claim\_result": "refuted", "note": "The attachment’s reported 60\.87→72\.19 utility figures have not been independently checked against configuration, denominator or raw runs\. No content\-overwrite defect or effect size is recorded as confirmed\. This is an issue\-type inference control, not a whole\-paper negative\."\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "consistent\_within\_scope", "reason": "all\_required\_checks\_consistent"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "consistent\_within\_scope", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "agentdojo_utility_only_information_inference",
    "source_group": "paper_text",
    "description": "Exclude the particular inference from task-integrity outcomes to an information-boundary finding; do not declare the paper globally free of information issues.",
    "scope": {
      "paper_version": "AgentDojo, NeurIPS 2024 final; arXiv:2406.13352v3 body cross-check, §§3.3–3.4",
      "experiment_arm": "Logical control for a reported task-utility perturbation, not a reproduced experiment",
      "artifact_revision": "Fixed conference PDF and arXiv v3; attachment report is not an independently verified run",
      "configuration": "Assess only whether a reported content-overwrite/utility phenomenon by itself proves unauthorized private-query delivery"
    },
    "target": {
      "role": "attacker-side content constructor",
      "phase": "content construction",
      "source": "victim private request",
      "representation": "exact private user-request text",
      "operation": "receive as construction input"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_different_issue_type",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The reported task-critical-content overwrite or utility change by itself establishes prohibited private-query delivery to an attack constructor.",
    "issue_type": "task_integrity",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://arxiv.org/html/2406.13352v3#S3.SS3",
        "reason": "§3.3 allows varying attacker knowledge and §3.4 defines distinct utility and targeted-success outcomes. Those definitions do not bind a particular prohibited private-query flow for the phenomenon in this control.",
        "policy_kind": "protocol_requirement"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "",
        "reason": "No corresponding raw construction request or private-query delivery evidence was supplied for this reported phenomenon."
      },
      "refutation": {
        "basis": "different_issue_type",
        "reference": "https://arxiv.org/html/2406.13352v3#S3.SS4",
        "reason": "Content integrity and task utility concern task completion and outcome interpretation. Those outcomes alone do not establish prohibited information receipt; this refutes only the claimed sufficiency of that inference."
      }
    },
    "claim_result": "refuted",
    "note": "The attachment’s reported 60.87→72.19 utility figures have not been independently checked against configuration, denominator or raw runs. No content-overwrite defect or effect size is recorded as confirmed. This is an issue-type inference control, not a whole-paper negative."
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "agentdojo",
  "title": "AgentDojo",
  "version": "NeurIPS 2024 final; arXiv:2406.13352v3 body cross-check",
  "audit_scope": "Control only: whether the reported task-content/utility phenomenon alone proves prohibited private-query delivery. The phenomenon and attachment numbers are not independently verified, and no whole-paper negative claim is made.",
  "verdict": "consistent_within_scope",
  "has_confirmed_inconsistency": false,
  "reason": "all_required_checks_consistent",
  "coverage_complete": true,
  "required_checks": 1,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [],
  "claim_result_counts": {
    "refuted": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "agentdojo_utility_only_information_inference",
      "source_group": "paper_text",
      "description": "Exclude the particular inference from task-integrity outcomes to an information-boundary finding; do not declare the paper globally free of information issues.",
      "scope": {
        "paper_version": "AgentDojo, NeurIPS 2024 final; arXiv:2406.13352v3 body cross-check, §§3.3–3.4",
        "experiment_arm": "Logical control for a reported task-utility perturbation, not a reproduced experiment",
        "artifact_revision": "Fixed conference PDF and arXiv v3; attachment report is not an independently verified run",
        "configuration": "Assess only whether a reported content-overwrite/utility phenomenon by itself proves unauthorized private-query delivery"
      },
      "target": {
        "role": "attacker-side content constructor",
        "phase": "content construction",
        "source": "victim private request",
        "representation": "exact private user-request text",
        "operation": "receive as construction input"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_different_issue_type",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The reported task-critical-content overwrite or utility change by itself establishes prohibited private-query delivery to an attack constructor.",
      "issue_type": "task_integrity",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://arxiv.org/html/2406.13352v3#S3.SS3",
          "reason": "§3.3 allows varying attacker knowledge and §3.4 defines distinct utility and targeted-success outcomes. Those definitions do not bind a particular prohibited private-query flow for the phenomenon in this control.",
          "policy_kind": "protocol_requirement"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "",
          "reason": "No corresponding raw construction request or private-query delivery evidence was supplied for this reported phenomenon."
        },
        "refutation": {
          "basis": "different_issue_type",
          "reference": "https://arxiv.org/html/2406.13352v3#S3.SS4",
          "reason": "Content integrity and task utility concern task completion and outcome interpretation. Those outcomes alone do not establish prohibited information receipt; this refutes only the claimed sufficiency of that inference."
        }
      },
      "claim_result": "refuted",
      "note": "The attachment’s reported 60.87→72.19 utility figures have not been independently checked against configuration, denominator or raw runs. No content-overwrite defect or effect size is recorded as confirmed. This is an issue-type inference control, not a whole-paper negative."
    }
  ],
  "expected": "consistent_within_scope",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "agentdojo_utility_only_information_inference",
          "source_group": "paper_text",
          "description": "Exclude the particular inference from task-integrity outcomes to an information-boundary finding; do not declare the paper globally free of information issues.",
          "scope": {
            "paper_version": "AgentDojo, NeurIPS 2024 final; arXiv:2406.13352v3 body cross-check, §§3.3–3.4",
            "experiment_arm": "Logical control for a reported task-utility perturbation, not a reproduced experiment",
            "artifact_revision": "Fixed conference PDF and arXiv v3; attachment report is not an independently verified run",
            "configuration": "Assess only whether a reported content-overwrite/utility phenomenon by itself proves unauthorized private-query delivery"
          },
          "target": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "victim private request",
            "representation": "exact private user-request text",
            "operation": "receive as construction input"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_different_issue_type",
          "matching_rules": [],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The reported task-critical-content overwrite or utility change by itself establishes prohibited private-query delivery to an attack constructor.",
          "issue_type": "task_integrity",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://arxiv.org/html/2406.13352v3#S3.SS3",
              "reason": "§3.3 allows varying attacker knowledge and §3.4 defines distinct utility and targeted-success outcomes. Those definitions do not bind a particular prohibited private-query flow for the phenomenon in this control.",
              "policy_kind": "protocol_requirement"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "",
              "reason": "No corresponding raw construction request or private-query delivery evidence was supplied for this reported phenomenon."
            },
            "refutation": {
              "basis": "different_issue_type",
              "reference": "https://arxiv.org/html/2406.13352v3#S3.SS4",
              "reason": "Content integrity and task utility concern task completion and outcome interpretation. Those outcomes alone do not establish prohibited information receipt; this refutes only the claimed sufficiency of that inference."
            }
          },
          "claim_result": "refuted",
          "note": "The attachment’s reported 60.87→72.19 utility figures have not been independently checked against configuration, denominator or raw runs. No content-overwrite defect or effect size is recorded as confirmed. This is an issue-type inference control, not a whole-paper negative."
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "consistent_within_scope",
      "reason": "all_required_checks_consistent"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "consistent_within_scope",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "previously_suspected_control",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```

### 18. Agent Security Bench \(ASB\)

论文 ID：asb  
运行 / 判定：审计范围内一致

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| load\_curated\_records | 已完成 | \{"stage": "load\_curated\_records", "status": "completed", "required\_checks": 1\} |
| field\_matching\_and\_rule\_decision | 已完成 | \{"stage": "field\_matching\_and\_rule\_decision", "status": "completed", "evidence": \[\{"id": "asb\_forced\_tool\_only\_information\_inference", "source\_group": "paper\_text", "description": "Exclude the particular inference from action\-attribution/measurement issues to an information\-boundary finding\.", "scope": \{"paper\_version": "Agent Security Bench \(ASB\), ICLR 2025 final, §3\.2, Table 4 and Appendix C\.2\.3/C\.2\.5", "experiment\_arm": "Logical control for reported harness\-forced tool execution, not a reproduced experiment", "artifact\_revision": "Fixed conference PDF; no corresponding pinned local execution audit or raw run established", "configuration": "Assess only whether a reported forced\-action/ASR phenomenon by itself proves unauthorized private\-query delivery"\}, "target": \{"role": "attacker\-side content constructor", "phase": "content construction", "source": "victim private request", "representation": "exact private user\-request text", "operation": "receive as construction input"\}, "verdict": "consistent\_within\_scope", "reason": "claim\_refuted\_different\_issue\_type", "matching\_rules": \[\], "matching\_observations": \[\], "other\_observation\_count": 0, "validation\_mode": "scope\_review\_v3", "claim": "The reported harness\-forced tool execution or ASR change by itself establishes prohibited private\-query delivery to an attack constructor\.", "issue\_type": "experimental\_protocol", "assessment": \{"information\_level": "exact\_query", "policy\_application": \{"status": "uncertain", "reference": "https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b\-Paper\-Conference\.pdf\#page=4 and https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b\-Paper\-Conference\.pdf\#page=8", "reason": "§3\.2 defines attack goals/capabilities and Table 4 defines outcome metrics\. The report of an externally selected action does not by itself bind an applicable private\-query prohibition and delivery edge\.", "policy\_kind": "protocol\_requirement"\}, "delivery": \{"status": "unresolved", "evidence\_kind": "not\_applicable", "task\_relation": "unknown", "reference": "", "reason": "No raw construction input, model action, harness rewrite and scored\-event chain was independently established for the reported phenomenon\."\}, "refutation": \{"basis": "different\_issue\_type", "reference": "https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b\-Paper\-Conference\.pdf\#page=26 and https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b\-Paper\-Conference\.pdf\#page=28", "reason": "Appendix C\.2\.3 defines outcome metrics and C\.2\.5 distinguishes parsing model output and executing simulated tools\. A forced action is an execution\-attribution/protocol allegation; it does not itself prove unauthorized information receipt\. Only that claimed implication is refuted\."\}\}, "claim\_result": "refuted", "note": "The attachment’s reported 73\.58%→9\.25% ASR figures and the alleged forced\-action defect remain unverified\. This case does not affirm that ASB is otherwise conformant or that its whole information model is problem\-free\."\}\]\} |
| paper\_aggregation | 已完成 | \{"stage": "paper\_aggregation", "status": "completed", "verdict": "consistent\_within\_scope", "reason": "all\_required\_checks\_consistent"\} |
| compare\_after\_decision | 已完成 | \{"stage": "compare\_after\_decision", "status": "completed", "expected": "consistent\_within\_scope", "matches\_gold": true\} |

#### 证据

```json
[
  {
    "id": "asb_forced_tool_only_information_inference",
    "source_group": "paper_text",
    "description": "Exclude the particular inference from action-attribution/measurement issues to an information-boundary finding.",
    "scope": {
      "paper_version": "Agent Security Bench (ASB), ICLR 2025 final, §3.2, Table 4 and Appendix C.2.3/C.2.5",
      "experiment_arm": "Logical control for reported harness-forced tool execution, not a reproduced experiment",
      "artifact_revision": "Fixed conference PDF; no corresponding pinned local execution audit or raw run established",
      "configuration": "Assess only whether a reported forced-action/ASR phenomenon by itself proves unauthorized private-query delivery"
    },
    "target": {
      "role": "attacker-side content constructor",
      "phase": "content construction",
      "source": "victim private request",
      "representation": "exact private user-request text",
      "operation": "receive as construction input"
    },
    "verdict": "consistent_within_scope",
    "reason": "claim_refuted_different_issue_type",
    "matching_rules": [],
    "matching_observations": [],
    "other_observation_count": 0,
    "validation_mode": "scope_review_v3",
    "claim": "The reported harness-forced tool execution or ASR change by itself establishes prohibited private-query delivery to an attack constructor.",
    "issue_type": "experimental_protocol",
    "assessment": {
      "information_level": "exact_query",
      "policy_application": {
        "status": "uncertain",
        "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=4 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=8",
        "reason": "§3.2 defines attack goals/capabilities and Table 4 defines outcome metrics. The report of an externally selected action does not by itself bind an applicable private-query prohibition and delivery edge.",
        "policy_kind": "protocol_requirement"
      },
      "delivery": {
        "status": "unresolved",
        "evidence_kind": "not_applicable",
        "task_relation": "unknown",
        "reference": "",
        "reason": "No raw construction input, model action, harness rewrite and scored-event chain was independently established for the reported phenomenon."
      },
      "refutation": {
        "basis": "different_issue_type",
        "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=26 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=28",
        "reason": "Appendix C.2.3 defines outcome metrics and C.2.5 distinguishes parsing model output and executing simulated tools. A forced action is an execution-attribution/protocol allegation; it does not itself prove unauthorized information receipt. Only that claimed implication is refuted."
      }
    },
    "claim_result": "refuted",
    "note": "The attachment’s reported 73.58%→9.25% ASR figures and the alleged forced-action defect remain unverified. This case does not affirm that ASB is otherwise conformant or that its whole information model is problem-free."
  }
]
```

#### 备注

```json
[
  "Curated regression: no fresh paper reading, code verification or model extraction in this run."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "asb",
  "title": "Agent Security Bench (ASB)",
  "version": "ICLR 2025 final",
  "audit_scope": "Control only: whether the reported forced-tool/ASR phenomenon alone proves prohibited private-query delivery. Neither the defect nor attachment numbers are independently verified; no whole-paper negative claim is made.",
  "verdict": "consistent_within_scope",
  "has_confirmed_inconsistency": false,
  "reason": "all_required_checks_consistent",
  "coverage_complete": true,
  "required_checks": 1,
  "resolved_checks": 1,
  "confirmed_findings": [],
  "unresolved_checks": [],
  "claim_result_counts": {
    "refuted": 1
  },
  "validation_modes": [
    "scope_review_v3"
  ],
  "behavioral_impact": [],
  "input_provenance_gaps": [],
  "evidence": [
    {
      "id": "asb_forced_tool_only_information_inference",
      "source_group": "paper_text",
      "description": "Exclude the particular inference from action-attribution/measurement issues to an information-boundary finding.",
      "scope": {
        "paper_version": "Agent Security Bench (ASB), ICLR 2025 final, §3.2, Table 4 and Appendix C.2.3/C.2.5",
        "experiment_arm": "Logical control for reported harness-forced tool execution, not a reproduced experiment",
        "artifact_revision": "Fixed conference PDF; no corresponding pinned local execution audit or raw run established",
        "configuration": "Assess only whether a reported forced-action/ASR phenomenon by itself proves unauthorized private-query delivery"
      },
      "target": {
        "role": "attacker-side content constructor",
        "phase": "content construction",
        "source": "victim private request",
        "representation": "exact private user-request text",
        "operation": "receive as construction input"
      },
      "verdict": "consistent_within_scope",
      "reason": "claim_refuted_different_issue_type",
      "matching_rules": [],
      "matching_observations": [],
      "other_observation_count": 0,
      "validation_mode": "scope_review_v3",
      "claim": "The reported harness-forced tool execution or ASR change by itself establishes prohibited private-query delivery to an attack constructor.",
      "issue_type": "experimental_protocol",
      "assessment": {
        "information_level": "exact_query",
        "policy_application": {
          "status": "uncertain",
          "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=4 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=8",
          "reason": "§3.2 defines attack goals/capabilities and Table 4 defines outcome metrics. The report of an externally selected action does not by itself bind an applicable private-query prohibition and delivery edge.",
          "policy_kind": "protocol_requirement"
        },
        "delivery": {
          "status": "unresolved",
          "evidence_kind": "not_applicable",
          "task_relation": "unknown",
          "reference": "",
          "reason": "No raw construction input, model action, harness rewrite and scored-event chain was independently established for the reported phenomenon."
        },
        "refutation": {
          "basis": "different_issue_type",
          "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=26 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=28",
          "reason": "Appendix C.2.3 defines outcome metrics and C.2.5 distinguishes parsing model output and executing simulated tools. A forced action is an execution-attribution/protocol allegation; it does not itself prove unauthorized information receipt. Only that claimed implication is refuted."
        }
      },
      "claim_result": "refuted",
      "note": "The attachment’s reported 73.58%→9.25% ASR figures and the alleged forced-action defect remain unverified. This case does not affirm that ASB is otherwise conformant or that its whole information model is problem-free."
    }
  ],
  "expected": "consistent_within_scope",
  "matches_gold": true,
  "status": "completed",
  "stages": [
    {
      "stage": "load_curated_records",
      "status": "completed",
      "required_checks": 1
    },
    {
      "stage": "field_matching_and_rule_decision",
      "status": "completed",
      "evidence": [
        {
          "id": "asb_forced_tool_only_information_inference",
          "source_group": "paper_text",
          "description": "Exclude the particular inference from action-attribution/measurement issues to an information-boundary finding.",
          "scope": {
            "paper_version": "Agent Security Bench (ASB), ICLR 2025 final, §3.2, Table 4 and Appendix C.2.3/C.2.5",
            "experiment_arm": "Logical control for reported harness-forced tool execution, not a reproduced experiment",
            "artifact_revision": "Fixed conference PDF; no corresponding pinned local execution audit or raw run established",
            "configuration": "Assess only whether a reported forced-action/ASR phenomenon by itself proves unauthorized private-query delivery"
          },
          "target": {
            "role": "attacker-side content constructor",
            "phase": "content construction",
            "source": "victim private request",
            "representation": "exact private user-request text",
            "operation": "receive as construction input"
          },
          "verdict": "consistent_within_scope",
          "reason": "claim_refuted_different_issue_type",
          "matching_rules": [],
          "matching_observations": [],
          "other_observation_count": 0,
          "validation_mode": "scope_review_v3",
          "claim": "The reported harness-forced tool execution or ASR change by itself establishes prohibited private-query delivery to an attack constructor.",
          "issue_type": "experimental_protocol",
          "assessment": {
            "information_level": "exact_query",
            "policy_application": {
              "status": "uncertain",
              "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=4 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=8",
              "reason": "§3.2 defines attack goals/capabilities and Table 4 defines outcome metrics. The report of an externally selected action does not by itself bind an applicable private-query prohibition and delivery edge.",
              "policy_kind": "protocol_requirement"
            },
            "delivery": {
              "status": "unresolved",
              "evidence_kind": "not_applicable",
              "task_relation": "unknown",
              "reference": "",
              "reason": "No raw construction input, model action, harness rewrite and scored-event chain was independently established for the reported phenomenon."
            },
            "refutation": {
              "basis": "different_issue_type",
              "reference": "https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=26 and https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=28",
              "reason": "Appendix C.2.3 defines outcome metrics and C.2.5 distinguishes parsing model output and executing simulated tools. A forced action is an execution-attribution/protocol allegation; it does not itself prove unauthorized information receipt. Only that claimed implication is refuted."
            }
          },
          "claim_result": "refuted",
          "note": "The attachment’s reported 73.58%→9.25% ASR figures and the alleged forced-action defect remain unverified. This case does not affirm that ASB is otherwise conformant or that its whole information model is problem-free."
        }
      ]
    },
    {
      "stage": "paper_aggregation",
      "status": "completed",
      "verdict": "consistent_within_scope",
      "reason": "all_required_checks_consistent"
    },
    {
      "stage": "compare_after_decision",
      "status": "completed",
      "expected": "consistent_within_scope",
      "matches_gold": true
    }
  ],
  "notes": [
    "Curated regression: no fresh paper reading, code verification or model extraction in this run."
  ],
  "cohort": "previously_suspected_control",
  "expected_basis": "source_adjudicated_listed_suspicions",
  "comparison_note": "Reference applies only to the listed source-adjudicated suspicions. Machine PDF-only claims may differ; inspect claim-level semantics before scoring errors."
}
```
