# 从 PDF 到一条论文结果：代码讲解

这份说明讲新增的文档入口。下面的代码块是实际函数中的短片段，只加入中文注释；省略的部分会明确说明。
`audit.py` 重放已有人工 JSON，`scan.py` 才从提供的论文文档开始。两种结果的证据范围不同。

```text
documents.load_document：读取文档、提取文字、保留页号与内容 hash
        ↓
scan.scan_source：组织单篇处理，保存各步骤产物
        ↓
client.generate：第一次抽取；第二次复核原文与抽取提议
        ↓
extraction.locate：检查引用是否确实位于指定页
        ↓
extraction.decide_extraction：只把支持的证据交给原有规则引擎
        ↓
benchmark / reports：每篇一行，包括失败与尚未运行的论文
```

## 1. `documents.load_document()`：先得到可定位的原文

输入是本地文件路径或论文 HTTP(S) URL。输出不是论文判定，而是一个文档对象：

```python
# documents.py / load_document()：返回值的实际结构。
return {
    "source": label,                    # URL 或本地 basename；不暴露本地完整目录。
    "sha256": hashlib.sha256(data).hexdigest(),  # 对实际读取的文档字节求 hash。
    "media_type": media_type,           # application/pdf、text/html 或 text/plain。
    "text": text,                       # 提取出的全文文字。
    "segments": segments,               # PDF 按 p1、p2 分页；HTML/TXT 使用 s1。
    "coverage": {"complete": bool(complete), "reason": reason},
    "links": _unique_links(links),      # 文档中的 HTTP(S) 链接；不自动审计链接的内容。
}
```

PDF 优先交给 `pdftotext` 提取文字：

```python
# documents.py / _pdf_pages()：参数是列表，没有 shell=True。
# PDF 字节从 stdin 传入；-layout 尽量保留排版；结果写入临时文本文件。
result = subprocess.run(
    ["pdftotext", "-layout", "-enc", "UTF-8", "-", str(output)],
    input=data, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    timeout=TIMEOUT_SECONDS, check=False,
)

# 转换成功后按换页符拆开，不把多页合成无法定位的一段文字。
pages = extracted.decode("utf-8", errors="replace").split("\f")
```

没有这个命令时可用可选的 `pypdf`；全无可提取文字时明确报“未提供 OCR”。
HTML 会移除 script/style 等内容；arXiv abstract URL 会转换为 PDF URL，普通 landing page 最多跟随一次 PDF 链接。
明显的 `/challenge` 或人机验证页面会被拒绝，不能作为论文正文继续处理。

`coverage.complete` **只描述文字提取覆盖**。PDF 每页都有文字不等于图表也已被理解，更不等于论文源码已被审计。
HTML 默认不能确认整篇覆盖，因此为 `false`。

## 2. `scan.scan_source()`：把处理过程留成文件

函数负责新建单篇输出目录，并按顺序读取、抽取、复核、校验、判定。
可以复用此前的 `prepared.json`，但会核对来源绑定，避免把另一篇文章的缓存用过来。

```python
# scan.py / scan_source()：prepared 是已读取的缓存对象；没有缓存时才重新读文档。
document = dict(prepared) if prepared is not None else load_document(source)

# 先保存原文、页号和 hash，再继续。save_json() 使用 "x" 模式，拒绝覆盖旧文件。
save_json(output_dir / "prepared.json", document)

# 模型输入超出限制就失败，不悄悄截掉后半篇再声称完成全文审计。
if len(document["text"]) > max_input_chars:
    raise ValueError("document exceeds the configured model input limit; not silently truncated")
```

`--prepare-only` 在读取之后停止：

```python
# scan.py / scan_source()：准备完成不等于模型已经给出论文结论。
if prepare_only:
    row.update(status="pending", verdict="not_run", reason="document_prepared_inference_not_run")
    row["stages"].append({"stage": "extraction", "status": "not_run"})
```

因此，存在 `prepared.json` 或 `report.html` 只能证明相应文件已生成，不能据此声称模型审计完成。

## 3. 两次 `generate()`：抽取提议，再复核证据

第一次让模型从文档中抽取适用性、信息流、声明、实现描述及短引文。
第二次重新提供同一文档与第一次提议，检查这些解释是否被原文支持。

```python
# scan.py / scan_source()：这是实际送给模型的内容。
# 不包含论文清单里的 expected、gold、人工案例或历史判定。
content = {"source_type": document["media_type"], "segments": document["segments"]}

# 第一次：按照 EXTRACTION_SCHEMA 生成结构化提议。
extraction = client.generate(EXTRACT_PROMPT, content, EXTRACTION_SCHEMA)

# 第二次：按照 REVIEW_SCHEMA 核对原文与提议。
review = client.generate(REVIEW_PROMPT, {**content, "proposal": extraction}, REVIEW_SCHEMA)
```

这两行位于实际代码的两个不同分支中：只有没有传入对应 replay JSON 时才调用模型。
`--extraction` 和 `--review` 同时提供时重放已保存输出，不调用模型，也不能冒充一次新的推理实验。

模型抽取接口比原有人工 JSON 多了明确的未知选项：

| 字段 | 可选值 | 未知值如何处理 |
| --- | --- | --- |
| `applicability` | `in_scope`、`out_of_scope`、`uncertain` | 不确定或复核有争议时保留证据不足。 |
| `permission` | `allow`、`deny`、`unspecified` | `unspecified` 不生成声明规则。 |
| `observation` | `present`、`absent`、`possible`、`unspecified` | `unspecified` 不生成实现观察。 |
| `query_form` | `full_query`、`partial_query`、`unspecified` | `unspecified` 转为原有匹配器中的未标注形态。 |

`allow` 只是允许，`deny` 要有明确限制；论文没说不是 `deny`。`present` 要有支持实际接收/使用的描述，
`absent` 要有肯定的边界证据，`possible` 只是潜在路径。完整 query 和部分 query 不能互相替代。

两次调用默认使用同一个 client；第二次复核不是独立人工复核，也不保证消除模型共同的错误。

## 4. `extraction.locate()`：先核实“引用确实在这里”

```python
# extraction.py / locate()：按模型给出的 segment_id 找到页或文本段。
segment = next((s for s in document["segments"] if s["id"] == citation["segment_id"]), None)
quote = citation["quote"]

# 页号不存在、引文为空、超过 300 字符或不是该页精确子串，都不能通过。
if segment is None or not quote.strip() or len(quote) > 300 or quote not in segment["text"]:
    raise ValueError("citation is not an exact substring of the specified segment")

# 同一页重复出现多次也不行，否则无法确定它指的是哪一处。
if segment["text"].count(quote) != 1:
    raise ValueError("citation is ambiguous within the segment; supply a unique substring")
```

通过后，代码记录该引文的 `start`、`end`、`segment_id` 和文档 SHA-256。
这证明引文位置可以回查，**不证明模型对引文的语义解释正确**；后者还依赖复核与人工检查。

## 5. `decide_extraction()`：把可用提议转成原有规则输入

函数先检查 JSON 结构、最多六条 flow，以及 review 是否恰好覆盖每个 flow 一次。
只对语义复核支持、引文能定位、状态不是 `unspecified` 的那部分创建规则或观察。

```python
# extraction.py / decide_extraction()：这是循环中的实际片段。
# field 是 declaration 或 implementation；value 是它对应的状态。
if value == "unspecified":
    continue                              # 未知值不伪装成 allow、deny 或 present。
try:
    locators[field] = locate(flow[field], document)  # 引文先通过精确位置检查。
    if by_index[index]["supported"]:     # 语义复核还必须支持这条 flow。
        case[destination].append({"edge": edge, state: value,
            "reference": json.dumps(locators[field], sort_keys=True)})
except ValueError as error:
    errors.append(f"{field}: {error}")    # 失败原因留在报告，不把该项当成已证实证据。
```

随后执行 `row = audit_case(case)`，复用原来的字段匹配和 `decide()`。
同一角色、阶段、信息、表示和用途上的 `deny + present` 才产生发现；不同阶段不能直接拼成冲突。

文档入口在论文聚合时明确固定 `coverage_complete=False`。
即使文字提取完整，也不能因此断言整篇实现已被覆盖；域内没有确认发现时，保留 `insufficient_evidence`。
非 IPI 论文需要抽取与复核一致、文档提取覆盖完整、主题引文可定位且没有 flow，才返回 `not_applicable`。

最终仍是一篇一条记录：内部任意一处确认发现就得到 `inconsistent`，同时保留原文定位和核查细节。
报告中的 `review_status="model_reviewed_not_human_verified"` 提醒读者，这还是待人工复核的文档证据判断。

## 6. `providers` / `CodexClient`：模型请求怎样发出、失败怎样保留

`scan.get_client()` 默认使用 `codex_provider.CodexClient`，沿用本机已保存的 ChatGPT Codex 登录。
它不把其他项目的 API key 当作备用凭据，也不会在失败后自动切换到 API 后端。
实际调用在临时空目录里进行，要求结构化 JSON，禁用工具并检查事件流。

```python
# codex_provider.py / CodexClient.generate()：模型输出了工具调用也要拒绝。
if any(is_tool_event(event) for event in events):
    entry["status"] = "tool_use_rejected"
    raise ValueError("Codex emitted a tool/command event; extraction rejected")

# 只有落盘文件存在还不够；事件流必须确认该次 turn 已完成。
if not completed:
    entry["status"] = "incomplete_event_stream"
    raise ValueError("Codex turn completion was not confirmed; no verdict produced")
```

函数还检查进程返回码、致命错误、完成之后是否又出现未完成 turn，以及最终文件是否为一个 JSON 对象。
CLI 输出一段文字、token 计数或错误消息，不能冒充符合 schema 的模型审计结果。
`ledger()` 只汇总实际报告的用量；缺失用量不是零用量，未暴露实际模型名时不能猜一个。
`max_calls` 限制包装器发起的 CLI 次数，不代表限制了 CLI 内部所有传输尝试。
默认接入使用账号额度及可能的 credits，不保证免费。

显式选择 `openai` 或 `anthropic` 时才使用 `providers.ModelClient`。
它要求 `--allow-api`、模型、预算与输入/输出价格，并在发送前计算预留额：

```python
# providers.py / ModelClient.generate()：先做本地预算/次数检查，再构造网络请求。
if len(self.calls) >= self.max_calls or self.charged + reservation > self.limit:
    raise BudgetExceeded("local inference budget/call limit reached; no request sent")
```

这是按操作人所填价格执行的本地保护，不是供应商账单保证。包装器不自动重试或更换供应商。

无论哪个后端，失败都会回到单篇记录：

```python
# scan.py / scan_source()：异常不是“没有不一致”，也不伪造模型结论。
row.update(status="failed", verdict="technical_failure", error=str(error),
           has_confirmed_inconsistency=None)
row["stages"].append({"stage": stage, "status": "failed", "error": str(error)})
```

`None` 表示本次没能给出结论。成功审计后的 `False` 表示没有确认发现，仍需结合证据状态阅读。

## 7. `benchmark.py`：逐篇执行，最后才对照 gold

文档模式把 `spec["source"]` 交给 `scan_source()`；论文 ID 只用于命名记录和目录。
`expected` 与历史结论没有随请求送给模型。

```python
# benchmark.py / main()：先完成逐篇处理。
row = scan_source(spec["source"], args.output / spec["id"], client,
                  args.mode == "prepare", spec["id"], prepared=prepared)
rows.append(row)

# main() 在整轮处理之后调用 add_comparisons(rows, specs)。
# 下面是 add_comparisons() 中的实际比较行；未完成的文章不评分。
row["matches_gold"] = (row["verdict"] == spec["expected"]) if row["status"] == "completed" else None
```

`regression` 模式使用已有人工 JSON；`prepare` 只准备文档；`scan` 才进行模型抽取、复核和判定。
这三者不能混成一次自动检测实验。
历史 gold 有些依据源码和本地归档，PDF-only 输入没有这些证据时出现不同结果，不自动意味着检测出错。
因此汇总叫 `reference_label_comparison`，不能直接称为未见论文准确率。

## 8. `reports.py`：每篇一行，过程展开查看

```python
# reports.py / _paper_state()：失败与未完成状态优先显示，不能被 verdict 掩盖。
if paper.get("error"):
    return status if status in ERROR_STATES else "error"
if status in ERROR_STATES | INCOMPLETE_STATES:
    return status

# reports.py / _confirmed()：三种值在报告中分开显示。
value = paper.get("has_confirmed_inconsistency")
if value is True:
    return "有"
if value is False:
    return "未确认"
return "未给出"
```

主表每篇一行，展开后显示 stages、证据、原因和原始记录。论文文本在 HTML 中经过转义，不能作为网页代码执行。
报告文件的存在不等于模型成功；应先看 `status`、`verdict` 和模型调用记录，再读发现。

| 看到的记录 | 可以说明什么 |
| --- | --- |
| `pending / not_run` | 文档可能已准备，但还没有模型审计结论。 |
| `failed / technical_failure` | 某步失败；不能当成论文没有问题。 |
| `completed / insufficient_evidence` | 流程产出结论，但现有文档证据不够。 |
| `completed / inconsistent` | 文档中存在通过当前定位与模型复核的候选冲突，仍需人工确认。 |
| `completed / not_applicable` | 该文档被判定为领域外；不是证明论文所有方面正确。 |

可以先不调用模型查看准备过程：

```bash
# 在仓库根目录运行；输出目录必须是新的。
python3 -B scan.py paper.pdf --prepare-only --output outputs/prepared-paper
```

真正的文档模型审计使用 `scan.py paper.pdf --output outputs/audited-paper`，会使用配置后端的额度。
它当前只依据所提供的论文文本，不能替代公开源码审计、历史请求验证或原论文实验复现。
