# 文档输入、自动审计与逐篇报告

## 两种运行各在做什么

`audit.py` 读取既有人工结构化记录，适合确定性回归。
`scan.py` 从新 PDF/URL 开始，先提取文本，再由模型提取和复核，最后运行同一个规则引擎。
它不会按论文 ID 查表取回既有判定。新入口不会把已有 gold 送进抽取提示。

默认推理接入为 Codex CLI 的既有 ChatGPT 登录。它会使用该账号的额度；本程序不保证账号用量永远免费。
命令运行在临时空目录、只读沙箱，使用 JSON Schema 输出，禁用 shell/web/app 等工具并不加载用户 MCP 配置。
未登录或 CLI 不支持所需选项时会明确失败，不自动转到付费 API。
可通过 `--model MODEL_ID` 固定自己可用的模型；不指定时使用 CLI 默认，报告不会把默认值猜成实际模型。

`python3 -B codex_provider.py --doctor` 可只检查 CLI 版本、登录类型和命令选项；不启动模型，
也不验证实际网络传输、账号额度或 app-server 初始化能否成功。

## 单篇流程

1. **读取**：支持本地 PDF/HTML/TXT 或公开 HTTP(S) URL。arXiv abstract 链接转 PDF；部分 landing page 可跟随 PDF 链接。限制 20 MiB，保留内容 hash。
2. **提取文本**：PDF 按页保留 `p1`、`p2` 等定位；HTML 不保证全文覆盖。图像/扫描页没有自动 OCR。模型输入超限时报告失败，不静默截断。
3. **模型抽取**：区分 IPI 适用性、角色、阶段、query 形态和用途，提取声明/实现描述。论文文本作为数据，不能给审计器下指令。
4. **模型复核**：独立一次调用重新核对同一原文与提议，检查是否混淆实验臂、离线/在线角色、完整/部分 query，以及是否把没说当作禁止。
5. **引文校验**：提议引用必须是指定页/segment 内可唯一定位的精确子串；不能定位、歧义或语义复核不支持的流不能提供确认不一致所需的那部分依据。
6. **规则判断**：经过上述检查的同一目标上，`deny + present` 产生发现，再按论文汇总。
7. **写报告**：每篇主表一行；展开可看步骤、定位、证据解释、原因与未解决问题。技术失败不转成“无不一致”。

这里的“模型复核”不是独立人工复核，也没有消除模型的语义错误。
报告标明 `review_status: model_reviewed_not_human_verified`。
全文中没有找到违规不能证明整个实现一致，因此文档入口不会自动声称覆盖整篇实现。

## 输出状态

| 状态 | 意思 |
| --- | --- |
| `inconsistent` | 文档中找到经过引文校验和模型复核的声明/实验描述冲突，仍需人工确认 |
| `insufficient_evidence` | 不能确认不一致，或缺实现/运行材料；不是证明没有问题 |
| `not_applicable` | 完整提取的文档被两次判断为非 IPI 领域，并有原文主题定位 |
| `technical_failure` | 下载、PDF、模型、schema、限额等步骤失败；没有产生论文结论 |
| `not_run` | 只完成读取准备，尚未进行模型审计 |

由于 PDF-only 输入没有自动提供完整源码和运行归档，某些原先人工确认不一致的论文可能在此入口变为证据不足。
这必须连同具体缺口报告，不能用修改标签或事先补入答案掩盖差异。

## 逐篇产物

每篇目录保留 `prepared.json`（原文文本及页号）、`request.json`（提示版本 hash 和设置）、
`extraction.json`、`review.json`、`result.json`。最后两份模型文件只在对应步骤实际成功时存在。
汇总有 `report.json`、`report.html`、`report.md`。原始全文和模型输出留在本地 `outputs/`，默认不上传 GitHub。
公开报告只包括必要的原创解释、原文定位和来源链接，不打包整篇论文。

## 14 篇 pilot

[benchmarks/papers.json](../benchmarks/papers.json) 包括原 11 篇以及 Attention、ResNet、Adam 三篇无关论文。
Attention 有大量 query/key 术语，用于检查程序是否误把注意力机制当成 IPI。
已有 Retrieval Barrier 是限定范围的域内一致样例，和三个域外控制分别报告。

`benchmark.py` 的 `expected` 仅在文档判定结束后用于比较，绝不送进模型；`--only aspi muzzle` 可选子集。
旧标签中有些依赖源码和本地历史归档，因此 `reference_label_comparison` 是历史对照，不能称为 PDF-only 检测准确率。
这批文章是开发用 pilot，不是独立保留集。

## 可选 API 后端

不使用 Codex 登录时，可以显式选 `--provider openai` 或 `--provider anthropic`。
须同时给出模型、API key 环境变量、`--allow-api`、预算和每百万 token 的输入/输出价格。
程序不自动选择 Claude、读取其他项目密钥、重试失败调用或切换供应商。
本地预算按所填价格保守预留，未知失败保留预留额；它不是供应商账单的替代品。

```bash
# API 示例为占位参数；只有主动执行并配置好参数才会产生请求
python3 -B scan.py paper.pdf --output outputs/api-run \
  --provider openai --model YOUR_MODEL --allow-api \
  --max-cost-usd 3 --input-price YOUR_INPUT_RATE --output-price YOUR_OUTPUT_RATE
```

API 形状依据 [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
及 [Anthropic Messages](https://platform.claude.com/docs/en/api/messages/create)；
Codex 接入依据 [官方非交互运行说明](https://learn.chatgpt.com/docs/non-interactive-mode)。
