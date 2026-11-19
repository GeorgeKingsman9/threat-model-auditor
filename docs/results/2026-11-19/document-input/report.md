# 论文审计：测试过程与结果

运行类型：document\_input\_pilot\_attempt  
生成时间：2026\-11\-19T07:50:28\.010903\+00:00  
论文记录：14

主表每篇论文一行。“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。

## 本次运行汇总

```json
{
  "paper_count": 14,
  "statuses": {
    "pending": 12,
    "failed": 2
  },
  "verdicts": {
    "not_run": 12,
    "technical_failure": 2
  },
  "interpretation": "14 papers remain visible: 12 prepared but inference not run, 1 document blocked, 1 attempted Codex inference with no accepted output. No automatic detection accuracy can be computed."
}
```

## 论文结果

| 论文 ID | 论文 | 运行 / 判定 | 已确认不一致 | 标签对照 | 来源 |
| --- | --- | --- | --- | --- | --- |
| adaptools | adaptools | 待运行 | 未给出 | 未评分；预期：证据不足 | https://aclanthology\.org/2026\.emnlp\-main\.2055\.pdf |
| blind\_spots | blind\_spots | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://arxiv\.org/pdf/2605\.22001v1 |
| aspi | aspi | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://arxiv\.org/pdf/2605\.17324v1 |
| muzzle | muzzle | 待运行 | 未给出 | 未评分；预期：证据不足 | https://www\.usenix\.org/system/files/usenixsecurity26\-syros\.pdf |
| fha | fha | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://arxiv\.org/pdf/2604\.20994v2 |
| agentcon | agentcon | 运行失败 | 未给出 | 未评分；预期：有已确认的不一致 | https://openreview\.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640\.pdf |
| retrieval\_barrier | retrieval\_barrier | 待运行 | 未给出 | 未评分；预期：审计范围内一致 | https://www\.usenix\.org/system/files/usenixsecurity26\-chang\-hongyan\.pdf |
| liar | liar | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://aclanthology\.org/2024\.emnlp\-main\.96\.pdf |
| obliinjection | obliinjection | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://arxiv\.org/pdf/2512\.09321v3 |
| webtrap | webtrap | 待运行 | 未给出 | 未评分；预期：有已确认的不一致 | https://arxiv\.org/pdf/2605\.08310v1 |
| icoa | icoa | 待运行 | 未给出 | 未评分；预期：证据不足 | https://aclanthology\.org/2026\.emnlp\-main\.2035\.pdf |
| attention | attention | 运行失败 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://papers\.nips\.cc/paper\_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa\-Paper\.pdf |
| resnet | resnet | 待运行 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://arxiv\.org/pdf/1512\.03385v1 |
| adam | adam | 待运行 | 未给出 | 未评分；预期：不适用（非 IPI 论文） | https://arxiv\.org/pdf/1412\.6980v1 |

## 逐篇测试过程

### 1. adaptools

论文 ID：adaptools  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 22, "characters": 117911, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \[\], "sha256": "b46cc0e65f08e44205e0ac5dfd53528fcfe2b77ae75ece013e5b51c8f6e95a05"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "adaptools",
  "title": "adaptools",
  "source": "https://aclanthology.org/2026.emnlp-main.2055.pdf",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 22,
      "characters": 117911,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [],
      "sha256": "b46cc0e65f08e44205e0ac5dfd53528fcfe2b77ae75ece013e5b51c8f6e95a05"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "b46cc0e65f08e44205e0ac5dfd53528fcfe2b77ae75ece013e5b51c8f6e95a05",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "insufficient_evidence",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 2. blind\_spots

论文 ID：blind\_spots  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 8, "characters": 45116, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \[\], "sha256": "0e674fdc3fe80b7af7c69bfd54f00907f9beded3e122cbda76f20fe33f168455"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "blind_spots",
  "title": "blind_spots",
  "source": "https://arxiv.org/pdf/2605.22001v1",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 8,
      "characters": 45116,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [],
      "sha256": "0e674fdc3fe80b7af7c69bfd54f00907f9beded3e122cbda76f20fe33f168455"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "0e674fdc3fe80b7af7c69bfd54f00907f9beded3e122cbda76f20fe33f168455",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 3. aspi

论文 ID：aspi  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 34, "characters": 149931, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/scaleapi/aspi", "https://arxiv\.org/abs/2009\.11352", "https://arxiv\.org/", "https://doi\.org/10\.1145/3733799\.3762982", "https://openreview\.net/forum?id=", "https://proceedings", "https://openreview\.net/", "https://arxiv", "https://www\.usenix\.org/conference/", "https://arxiv\.org/abs/2603\.15714", "https://arxiv\.org/abs/2603\.26233", "https://aclanthology\.org/2020\.emnlp\-main\.466/", "https://huggingface\.co/", "https://doi\.org/10\.1145/3605764\.3623985", "https://arxiv\.org/abs/2602\.10525", "https://openreview\.net/forum", "https://arxiv\.org/abs/2507\.22034", "https://arxiv\.org/abs/2603\.10749", "https://arxiv\.org/abs/2511", "https://doi\.org/10\.1145/3690624\.3709179", "https://openreview\.net/forum?id=X2yzXtH4wp", "https://aclanthology\.org/2024", "https://arxiv\.org/abs/2508\.09124", "https://arxiv\.org/abs/2407\.19056", "https://simonwillison\.net/", "https://arxiv\.org/abs/2403\.04960", "https://arxiv\.org/abs/2603\.01357", "https://openreview\.net/forum?id=oKn9c6ytLx", "https://deepmind\.google/models/gemini/pro/", "https://www\.litellm\.ai"\], "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "aspi",
  "title": "aspi",
  "source": "https://arxiv.org/pdf/2605.17324v1",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 34,
      "characters": 149931,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/scaleapi/aspi",
        "https://arxiv.org/abs/2009.11352",
        "https://arxiv.org/",
        "https://doi.org/10.1145/3733799.3762982",
        "https://openreview.net/forum?id=",
        "https://proceedings",
        "https://openreview.net/",
        "https://arxiv",
        "https://www.usenix.org/conference/",
        "https://arxiv.org/abs/2603.15714",
        "https://arxiv.org/abs/2603.26233",
        "https://aclanthology.org/2020.emnlp-main.466/",
        "https://huggingface.co/",
        "https://doi.org/10.1145/3605764.3623985",
        "https://arxiv.org/abs/2602.10525",
        "https://openreview.net/forum",
        "https://arxiv.org/abs/2507.22034",
        "https://arxiv.org/abs/2603.10749",
        "https://arxiv.org/abs/2511",
        "https://doi.org/10.1145/3690624.3709179",
        "https://openreview.net/forum?id=X2yzXtH4wp",
        "https://aclanthology.org/2024",
        "https://arxiv.org/abs/2508.09124",
        "https://arxiv.org/abs/2407.19056",
        "https://simonwillison.net/",
        "https://arxiv.org/abs/2403.04960",
        "https://arxiv.org/abs/2603.01357",
        "https://openreview.net/forum?id=oKn9c6ytLx",
        "https://deepmind.google/models/gemini/pro/",
        "https://www.litellm.ai"
      ],
      "sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "cd6e0fee0fd70d712be88b44b90606e720e30b7184cbf4ff9df5d6393b475893",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 4. muzzle

论文 ID：muzzle  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 21, "characters": 124184, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://www\.usenix\.org/conference/usenixsecurity26/presentation/syros", "https://arxiv\.org/abs/2602\.09222", "https://github\.com/gsi", "https://github\.com/bgrins/the\_zoo", "http://gitea\.zoo/alice/hello\-zoo/issues", "https://doi\.org/10\.5281/zeno", "https://arxi", "https://claude\.com", "https://browser\-use\.com/", "https://search\.google/ways", "https://www\.search\.google/ways\-to\-sea", "https://arxiv\.org/", "https://huggin", "https://github\.com/microso", "https://www\.mi", "https://openai\.com", "https://op", "https://huggingface\.co/m", "https://huggingface\.co", "https://huggingface\.co/P", "https://huggingfac", "https://www\.diabrowser\.c", "https://arxiv\.org/abs/2404\.13208", "https://arxiv\.org/abs/2505\.05849", "https://html", "http://www\.w3\.org/TR/2004/REC", "https://www\.dobrowser\.io/", "https://www\.w3\.org/Security/", "https://arxiv\.org/abs/2307\.15043", "https://adnanthekhan\.com/posts/clinejection/"\], "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "muzzle",
  "title": "muzzle",
  "source": "https://www.usenix.org/system/files/usenixsecurity26-syros.pdf",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 21,
      "characters": 124184,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://www.usenix.org/conference/usenixsecurity26/presentation/syros",
        "https://arxiv.org/abs/2602.09222",
        "https://github.com/gsi",
        "https://github.com/bgrins/the_zoo",
        "http://gitea.zoo/alice/hello-zoo/issues",
        "https://doi.org/10.5281/zeno",
        "https://arxi",
        "https://claude.com",
        "https://browser-use.com/",
        "https://search.google/ways",
        "https://www.search.google/ways-to-sea",
        "https://arxiv.org/",
        "https://huggin",
        "https://github.com/microso",
        "https://www.mi",
        "https://openai.com",
        "https://op",
        "https://huggingface.co/m",
        "https://huggingface.co",
        "https://huggingface.co/P",
        "https://huggingfac",
        "https://www.diabrowser.c",
        "https://arxiv.org/abs/2404.13208",
        "https://arxiv.org/abs/2505.05849",
        "https://html",
        "http://www.w3.org/TR/2004/REC",
        "https://www.dobrowser.io/",
        "https://www.w3.org/Security/",
        "https://arxiv.org/abs/2307.15043",
        "https://adnanthekhan.com/posts/clinejection/"
      ],
      "sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "d893e5adb7586b2d460a086591d7b480d8afe23a3faf8046a6fc8affdb4c90d0",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "insufficient_evidence",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 5. fha

论文 ID：fha  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 41, "characters": 145552, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/GraySwanAI/nanoGCG", "https://github\.com/modelcontextprotocol/servers\-archived/", "https://jmlr\.org/tmlr/ethics\.html", "https://arxiv\.org/abs/2407\.00121", "https://arxiv\.org/abs/2406\.13352", "https://doi\.org/10\.24963/ijcai\.2024/890", "https://arxiv\.org/abs/2402\.12329", "https://arxiv\.org/abs/2407\.19354", "https://arxiv\.org/abs/2503\.23278", "https://www\.ibm\.com/downloads/", "https://adversa\.ai/", "https://invariantlabs", "https://arxiv\.org/abs/2310\.06825", "https://arxiv\.org/abs/2504\.19277", "https://doi\.org/10\.1007/", "https://www\.usenix\.org/conference/usenixsecurity18/presentation/kumar", "https://arxiv\.org/abs/2310\.04451", "https://arxiv\.org/abs/2410\.18890", "https://arxiv", "https://arxiv\.org/abs/2303\.08774", "https://arxiv\.org/abs/2305\.15334", "https://arxiv\.org/abs/2505\.09388", "https://arxiv\.org/abs/2409\.15398", "https://arxiv\.org/abs/2302\.04761", "https://arxiv\.org/abs/2302\.13971", "https://nvlpubs\.nist\.gov/", "http://dx\.doi\.org/10\.1007/s11704\-024\-40231\-1", "https://arxiv\.org/abs/2410", "https://arxiv\.org/abs/2407\.17915", "https://arxiv\.org/abs/2210\.03629", "https://arxiv\.org/abs/2407\.04295", "https://arxiv\.org/abs/2403", "https://arxiv\.org/abs/2407\.20859", "https://arxiv\.org/abs/2307", "https://arxiv\.org/abs/2406\.04313", "https://github\.com/hanbaoergogo/MPMA\.git"\], "sha256": "a418013dac0ff58898aa832f682702b1cf1c605f8edc2f05446b2035c2bbcccc"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "fha",
  "title": "fha",
  "source": "https://arxiv.org/pdf/2604.20994v2",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 41,
      "characters": 145552,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/GraySwanAI/nanoGCG",
        "https://github.com/modelcontextprotocol/servers-archived/",
        "https://jmlr.org/tmlr/ethics.html",
        "https://arxiv.org/abs/2407.00121",
        "https://arxiv.org/abs/2406.13352",
        "https://doi.org/10.24963/ijcai.2024/890",
        "https://arxiv.org/abs/2402.12329",
        "https://arxiv.org/abs/2407.19354",
        "https://arxiv.org/abs/2503.23278",
        "https://www.ibm.com/downloads/",
        "https://adversa.ai/",
        "https://invariantlabs",
        "https://arxiv.org/abs/2310.06825",
        "https://arxiv.org/abs/2504.19277",
        "https://doi.org/10.1007/",
        "https://www.usenix.org/conference/usenixsecurity18/presentation/kumar",
        "https://arxiv.org/abs/2310.04451",
        "https://arxiv.org/abs/2410.18890",
        "https://arxiv",
        "https://arxiv.org/abs/2303.08774",
        "https://arxiv.org/abs/2305.15334",
        "https://arxiv.org/abs/2505.09388",
        "https://arxiv.org/abs/2409.15398",
        "https://arxiv.org/abs/2302.04761",
        "https://arxiv.org/abs/2302.13971",
        "https://nvlpubs.nist.gov/",
        "http://dx.doi.org/10.1007/s11704-024-40231-1",
        "https://arxiv.org/abs/2410",
        "https://arxiv.org/abs/2407.17915",
        "https://arxiv.org/abs/2210.03629",
        "https://arxiv.org/abs/2407.04295",
        "https://arxiv.org/abs/2403",
        "https://arxiv.org/abs/2407.20859",
        "https://arxiv.org/abs/2307",
        "https://arxiv.org/abs/2406.04313",
        "https://github.com/hanbaoergogo/MPMA.git"
      ],
      "sha256": "a418013dac0ff58898aa832f682702b1cf1c605f8edc2f05446b2035c2bbcccc"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "a418013dac0ff58898aa832f682702b1cf1c605f8edc2f05446b2035c2bbcccc",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 6. agentcon

论文 ID：agentcon  
运行 / 判定：运行失败

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 运行失败 | \{"stage": "ingestion", "status": "failed", "error": "prepared document source does not match the requested paper"\} |

#### 证据

```json
[]
```

#### 备注

```json
[
  "The cached URL response is an OpenReview access-challenge HTML page, not the paper PDF. The cached source mismatch correctly prevented inference."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "agentcon",
  "title": "agentcon",
  "source": "https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf",
  "status": "failed",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "failed",
      "error": "prepared document source does not match the requested paper"
    }
  ],
  "evidence": [],
  "verdict": "technical_failure",
  "error": "prepared document source does not match the requested paper",
  "duration_seconds": 0.0,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null,
  "notes": [
    "The cached URL response is an OpenReview access-challenge HTML page, not the paper PDF. The cached source mismatch correctly prevented inference."
  ]
}
```

### 7. retrieval\_barrier

论文 ID：retrieval\_barrier  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 21, "characters": 142451, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://www\.usenix\.org/conference/usenixsecurity26/presentation/chang\-hongyan", "https://docs\.weaviate\.io/", "https://zenodo\.org/records/", "https://genai\.owasp\.org/resource/owasp\-", "https://www\.aim", "https://bailian\.console\.aliyun", "https://www", "https://azure\.microsoft\.com/en\-", "https://web\.stanford\.edu/", "https://cursor", "https://arxiv\.org/abs/2508\.12175", "https://arxiv\.org/", "https://learn\.microsoft\.com/en\-", "https://blog"\], "sha256": "618906131d9aa7b6225ea3b0e2cc7e12c11694cf54842ac3cc4dc1d2f8f45285"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "retrieval_barrier",
  "title": "retrieval_barrier",
  "source": "https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 21,
      "characters": 142451,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://www.usenix.org/conference/usenixsecurity26/presentation/chang-hongyan",
        "https://docs.weaviate.io/",
        "https://zenodo.org/records/",
        "https://genai.owasp.org/resource/owasp-",
        "https://www.aim",
        "https://bailian.console.aliyun",
        "https://www",
        "https://azure.microsoft.com/en-",
        "https://web.stanford.edu/",
        "https://cursor",
        "https://arxiv.org/abs/2508.12175",
        "https://arxiv.org/",
        "https://learn.microsoft.com/en-",
        "https://blog"
      ],
      "sha256": "618906131d9aa7b6225ea3b0e2cc7e12c11694cf54842ac3cc4dc1d2f8f45285"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "618906131d9aa7b6225ea3b0e2cc7e12c11694cf54842ac3cc4dc1d2f8f45285",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.003,
  "cohort": "curated_ipi",
  "expected": "consistent_within_scope",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 8. liar

论文 ID：liar  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 17, "characters": 89373, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://www\.bbc\.com/news/articles/cd11gzejgz4o/", "https://www\.reddit\.com/r/Pizza/comments/1a19s0/", "https://www\.washingtonpost\.com/google\-halt\-ai\-search/", "https://huggingface\.co/datasets/Salesforce/wikitext/", "https://python\.langchain\.com/google\_search/"\], "sha256": "4a8138a9eaa1bce8fc300cdeaa9c83ce64f4440c99b596b5687c4e54d2cfd0e0"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "liar",
  "title": "liar",
  "source": "https://aclanthology.org/2024.emnlp-main.96.pdf",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 17,
      "characters": 89373,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://www.bbc.com/news/articles/cd11gzejgz4o/",
        "https://www.reddit.com/r/Pizza/comments/1a19s0/",
        "https://www.washingtonpost.com/google-halt-ai-search/",
        "https://huggingface.co/datasets/Salesforce/wikitext/",
        "https://python.langchain.com/google_search/"
      ],
      "sha256": "4a8138a9eaa1bce8fc300cdeaa9c83ce64f4440c99b596b5687c4e54d2cfd0e0"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "4a8138a9eaa1bce8fc300cdeaa9c83ce64f4440c99b596b5687c4e54d2cfd0e0",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 9. obliinjection

论文 ID：obliinjection  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 18, "characters": 136067, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/ReachalWang/ObliInjection", "https://dx\.doi\.org/10\.14722/ndss\.2026\.240702", "https://www\.aboutamazon\.com/news/amazon\-ai/", "https://blog\.google/products/search/", "https://github", "https://github\.com/GraySwanAI/nanoGCG", "https://twitter\.com/yoheinakajima/", "https://github\.com/tatsu\-lab/stanford"\], "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "obliinjection",
  "title": "obliinjection",
  "source": "https://arxiv.org/pdf/2512.09321v3",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 18,
      "characters": 136067,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/ReachalWang/ObliInjection",
        "https://dx.doi.org/10.14722/ndss.2026.240702",
        "https://www.aboutamazon.com/news/amazon-ai/",
        "https://blog.google/products/search/",
        "https://github",
        "https://github.com/GraySwanAI/nanoGCG",
        "https://twitter.com/yoheinakajima/",
        "https://github.com/tatsu-lab/stanford"
      ],
      "sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "deca13eaa2047e83d2a932d2194ef5e2533b1523b30c74f2a83fd0bb26d3d88e",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 10. webtrap

论文 ID：webtrap  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 31, "characters": 143482, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/liuyaojialiuyaojia/WebTrap", "https://openreview\.net/forum?id=lIVRgt4nLv", "https://proceedings\.mlr\.press/v267/", "https://aclanthology\.org/2025\.emnlp\-main\.372/", "https://aclanthology\.org/2025\.acl\-long\.890/", "https://aclanthology\.org/2025\.acl\-long\.897/", "https://proceedings\.neurips\.cc/paper\_files/paper/2024/hash/", "https://arxiv\.org/abs/2412\.19437", "https://papers\.nips\.cc/paper\_", "https://proceedings\.mlr\.press/", "https://openreview\.net/forum?id=Ip1cCUAllL", "https://arxiv\.org/abs/2507\.06261", "https://arxiv\.org/abs/2508", "https://doi\.org/10\.1145/3605764", "https://doi\.org/10\.1007/978\-3\-031\-73113\-6\_10", "https://arxiv\.org/abs/2507\.20534", "https://aclanthology\.org/2024\.acl\-long\.50/", "https://openreview", "https://aclanthology\.org/2024\.tacl\-1\.9/", "https://openreview\.net/forum?id=zAdUB0aCTQ", "https://www\.usenix\.org/conference/usenixsecurity24/presentation/liu\-yupei", "https://proceedings\.mlr\.press/v235/lu24e\.html", "https://arxiv\.org/abs/2505\.09388", "https://doi\.org/10\.1145/3690624\.3709179", "https://aclanthology", "https://aclanthology\.org/2024\.findings\-acl\.624/", "https://openreview\.net/forum?id=V4y0CpX4hK", "https://aclanthology\.org/2025\.acl\-long", "https://openreview\.net/forum?id=oKn9c6ytLx"\], "sha256": "00dedf8131efd61f11ece27e6087310a7c0aa675003ce9942eeea6b05a75766a"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "webtrap",
  "title": "webtrap",
  "source": "https://arxiv.org/pdf/2605.08310v1",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 31,
      "characters": 143482,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/liuyaojialiuyaojia/WebTrap",
        "https://openreview.net/forum?id=lIVRgt4nLv",
        "https://proceedings.mlr.press/v267/",
        "https://aclanthology.org/2025.emnlp-main.372/",
        "https://aclanthology.org/2025.acl-long.890/",
        "https://aclanthology.org/2025.acl-long.897/",
        "https://proceedings.neurips.cc/paper_files/paper/2024/hash/",
        "https://arxiv.org/abs/2412.19437",
        "https://papers.nips.cc/paper_",
        "https://proceedings.mlr.press/",
        "https://openreview.net/forum?id=Ip1cCUAllL",
        "https://arxiv.org/abs/2507.06261",
        "https://arxiv.org/abs/2508",
        "https://doi.org/10.1145/3605764",
        "https://doi.org/10.1007/978-3-031-73113-6_10",
        "https://arxiv.org/abs/2507.20534",
        "https://aclanthology.org/2024.acl-long.50/",
        "https://openreview",
        "https://aclanthology.org/2024.tacl-1.9/",
        "https://openreview.net/forum?id=zAdUB0aCTQ",
        "https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei",
        "https://proceedings.mlr.press/v235/lu24e.html",
        "https://arxiv.org/abs/2505.09388",
        "https://doi.org/10.1145/3690624.3709179",
        "https://aclanthology",
        "https://aclanthology.org/2024.findings-acl.624/",
        "https://openreview.net/forum?id=V4y0CpX4hK",
        "https://aclanthology.org/2025.acl-long",
        "https://openreview.net/forum?id=oKn9c6ytLx"
      ],
      "sha256": "00dedf8131efd61f11ece27e6087310a7c0aa675003ce9942eeea6b05a75766a"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "00dedf8131efd61f11ece27e6087310a7c0aa675003ce9942eeea6b05a75766a",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.002,
  "cohort": "curated_ipi",
  "expected": "inconsistent",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 11. icoa

论文 ID：icoa  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 19, "characters": 116646, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://yslmoment\.github\.io/ICoA", "https://www\.lake"\], "sha256": "4da820429fd4d07f8832c6d2ee8f588688f3d507b3601275dd92bff09d411ee2"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "id": "icoa",
  "title": "icoa",
  "source": "https://aclanthology.org/2026.emnlp-main.2035.pdf",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 19,
      "characters": 116646,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://yslmoment.github.io/ICoA",
        "https://www.lake"
      ],
      "sha256": "4da820429fd4d07f8832c6d2ee8f588688f3d507b3601275dd92bff09d411ee2"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "4da820429fd4d07f8832c6d2ee8f588688f3d507b3601275dd92bff09d411ee2",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.004,
  "cohort": "curated_ipi",
  "expected": "insufficient_evidence",
  "expected_basis": "prior_curated_evidence",
  "comparison_note": "Historical label for the version and audit scope in paper_pilot.json; its source-code or archived evidence may not be present in this PDF. A different PDF-only result is not automatically a detection error.",
  "matches_gold": null
}
```

### 12. attention

论文 ID：attention  
运行 / 判定：运行失败

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 11, "characters": 38171, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["https://github\.com/"\], "sha256": "d87d482d5ae7960e2e43d7dd6d21377e60e73e8fce1bf2a01aff7aca8a08c537"\} |
| extraction | 运行失败 | \{"stage": "extraction", "status": "failed", "error": "Codex CLI failed \(authentication\_error\); no retry or fallback attempted"\} |

#### 证据

```json
[]
```

#### 备注

```json
[
  "No accepted structured model output was obtained. The original wrapper category is retained, but does not prove a failed login.",
  "A separate minimal Codex test reported stream resets and reconnect attempts. No Claude/OpenAI API-key backend was used."
]
```

#### 完整论文记录 JSON

```json
{
  "id": "attention",
  "title": "attention",
  "source": "https://papers.nips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
  "status": "failed",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 11,
      "characters": 38171,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "https://github.com/"
      ],
      "sha256": "d87d482d5ae7960e2e43d7dd6d21377e60e73e8fce1bf2a01aff7aca8a08c537"
    },
    {
      "stage": "extraction",
      "status": "failed",
      "error": "Codex CLI failed (authentication_error); no retry or fallback attempted"
    }
  ],
  "evidence": [],
  "document_sha256": "d87d482d5ae7960e2e43d7dd6d21377e60e73e8fce1bf2a01aff7aca8a08c537",
  "verdict": "technical_failure",
  "error": "Codex CLI failed (authentication_error); no retry or fallback attempted",
  "duration_seconds": 128.946,
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Unrelated topic control for applicability screening. not_applicable does not assert global paper consistency.",
  "matches_gold": null,
  "notes": [
    "No accepted structured model output was obtained. The original wrapper category is retained, but does not prove a failed login.",
    "A separate minimal Codex test reported stream resets and reconnect attempts. No Claude/OpenAI API-key backend was used."
  ]
}
```

### 13. resnet

论文 ID：resnet  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 12, "characters": 97713, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \["http://image\-net\.org/challenges/LSVRC/2015/", "http://mscoco\.org/dataset/", "http://host\.robots\.ox\.ac\.uk:8080/leaderboard/", "http://host\.robots\.ox\.ac\.uk:8080/anonymous/3OJ4OJ\.html"\], "sha256": "1e0651b6810ecba34a3dbc5b5b0209226f889004607c1f203540a48d64e5a93a"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "title": "resnet",
  "source": "https://arxiv.org/pdf/1512.03385v1",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 12,
      "characters": 97713,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [
        "http://image-net.org/challenges/LSVRC/2015/",
        "http://mscoco.org/dataset/",
        "http://host.robots.ox.ac.uk:8080/leaderboard/",
        "http://host.robots.ox.ac.uk:8080/anonymous/3OJ4OJ.html"
      ],
      "sha256": "1e0651b6810ecba34a3dbc5b5b0209226f889004607c1f203540a48d64e5a93a"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "1e0651b6810ecba34a3dbc5b5b0209226f889004607c1f203540a48d64e5a93a",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.001,
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Unrelated topic control for applicability screening. not_applicable does not assert global paper consistency.",
  "matches_gold": null
}
```

### 14. adam

论文 ID：adam  
运行 / 判定：待运行

#### 测试过程

| 步骤 | 状态 | 记录 |
| --- | --- | --- |
| ingestion | 已完成 | \{"stage": "ingestion", "status": "completed", "segments": 9, "characters": 41440, "coverage": \{"complete": true, "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"\}, "source\_links": \[\], "sha256": "935a5a15616961aff21529d86a754570028843407adfe858f1d18584b84293a7"\} |
| extraction | 尚未运行 | \{"stage": "extraction", "status": "not\_run"\} |

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
  "title": "adam",
  "source": "https://arxiv.org/pdf/1412.6980v1",
  "status": "pending",
  "has_confirmed_inconsistency": null,
  "stages": [
    {
      "stage": "ingestion",
      "status": "completed",
      "segments": 9,
      "characters": 41440,
      "coverage": {
        "complete": true,
        "reason": "Text extracted from every PDF page; OCR and visual content are not inspected"
      },
      "source_links": [],
      "sha256": "935a5a15616961aff21529d86a754570028843407adfe858f1d18584b84293a7"
    },
    {
      "stage": "extraction",
      "status": "not_run"
    }
  ],
  "evidence": [],
  "document_sha256": "935a5a15616961aff21529d86a754570028843407adfe858f1d18584b84293a7",
  "verdict": "not_run",
  "reason": "document_prepared_inference_not_run",
  "duration_seconds": 0.001,
  "cohort": "out_of_domain",
  "expected": "not_applicable",
  "expected_basis": "domain_selection",
  "comparison_note": "Unrelated topic control for applicability screening. not_applicable does not assert global paper consistency.",
  "matches_gold": null
}
```
