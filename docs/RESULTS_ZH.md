# 所有文章的实际测试过程与结果

本页记录 2026-11-19 的实际运行情况。每篇论文始终只贡献一条主表记录；内部信息流可展开查看。

## 已有结构化证据的规则回归

运行命令：

```bash
python3 -B benchmark.py --mode regression --output outputs/2026-11-19-regression-all-papers
```

原有 11 篇均完成规则回归：7 篇不一致、1 篇限定范围内一致、3 篇证据不足，与既有人工标签 11/11 一致。
三篇新增无关论文没有既有结构化记录，在这个模式中明确显示为未运行，没有用预期标签生成结论。

完整逐篇过程和证据：[Markdown](results/2026-11-19/regression/report.md)、[JSON](results/2026-11-19/regression/report.json)、[下载后打开的 HTML](results/2026-11-19/regression/report.html)。

这只是已知案例的回归；没有重新核实所有底层材料，不能作为自动文档审计准确率。

## PDF/网址入口的真实 pilot 尝试

已实际访问全部 14 个论文来源并提取文本：13 份 PDF 可提取文字；AGENTCON 来源返回 OpenReview 验证页，不能当作论文正文。
原始准备过程留在本地 outputs，未把论文全文重新上传此仓库。

随后通过既有 ChatGPT 登录尝试了 Attention 的 Codex 抽取。
沙箱内初始化失败；宿主检查允许初始化后，仍未获得可接受的结构化审计输出。
另一次最小诊断出现 stream reset / reconnect 事件。旧 wrapper 曾把错误归为 authentication_error，
该类别不足以证明登录失效；现在代码分别记录传输通知和终态失败。没有自动切换到 Claude 或 API-key 后端。

当前逐篇状态：

| 论文 | 文档读取 | 自动语义审计结果 |
| --- | --- | --- |
| AdapTools | PDF 文本已提取 | 未运行 |
| Blind Spots | PDF 文本已提取 | 未运行 |
| ASPI | PDF 文本已提取 | 未运行 |
| MUZZLE | PDF 文本已提取 | 未运行 |
| FHA | PDF 文本已提取 | 未运行 |
| AGENTCON | 验证页，未取得 PDF 正文 | 技术失败，未推理 |
| Retrieval Barrier | PDF 文本已提取 | 未运行 |
| LIAR | PDF 文本已提取 | 未运行 |
| ObliInjection | PDF 文本已提取 | 未运行 |
| WebTrap | PDF 文本已提取 | 未运行 |
| ICoA | PDF 文本已提取 | 未运行 |
| Attention Is All You Need | PDF 文本已提取 | Codex 尝试失败，无审计结论 |
| ResNet | PDF 文本已提取 | 未运行 |
| Adam | PDF 文本已提取 | 未运行 |

完整输入来源、内容 hash、页数、读取步骤、运行错误和预期标签分别保留在
[逐篇过程报告](results/2026-11-19/document-input/report.md)、
[机器可读 JSON](results/2026-11-19/document-input/report.json) 和
[下载后打开的 HTML](results/2026-11-19/document-input/report.html)。
这里的预期标签只用于显示评测设计；没有把未完成论文写成不一致、非不一致或已通过。

尚未获得 14 篇的自动模型判定，因此没有自动检测准确率、域外误报率或新的发现数。
Attention、ResNet、Adam 的设计预期是 `not_applicable`；当前它们不是已经通过的负例。

## 如何复现下一次运行

```bash
# 读取所有论文；失败保留在报告中
python3 -B benchmark.py --mode prepare --output outputs/next-preparation

# 使用本机可用的 Codex ChatGPT 登录；不会自动切换供应商
python3 -B benchmark.py --mode scan --prepared-dir outputs/next-preparation \
  --model YOUR_AVAILABLE_CODEX_MODEL --max-calls 28 --output outputs/next-document-audit
```

配置、模型可用性、网络传输及账号额度影响真实运行；离线单元测试通过不等于上述链路已经成功。
