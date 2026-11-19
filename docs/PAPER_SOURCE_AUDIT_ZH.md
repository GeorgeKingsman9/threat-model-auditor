# 论文与源码自动审计

`audit.py` 接收已经整理的证据；`scan.py --repo` 才是从论文与原始源码自动形成证据的入口。两者都汇总为每篇论文一条结论，但输入证据的产生方式不同。

旧 PDF 路径只向模型提供论文文本。仓库链接虽记录在报告中，却没有被抓取。ASPI 的旧自动输出对构造阶段的权限适用性保留争议，旧复核代码又把政策和交付轴一起降级。因此，修改人工 ASPI 记录没有改变那次 PDF 自动输出。

## 运行

```bash
# 同时输入原论文与固定提交的官方源码。
python3 -B scan.py https://arxiv.org/pdf/2605.17324v1 \
  --repo https://github.com/scaleapi/aspi \
  --repo-revision e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d \
  --max-input-chars 500000 --max-code-chars 320000 \
  --model gpt-6.1-sol --max-calls 3 \
  --output outputs/aspi-paper-source-new

# 本地源目录也可使用；没有 Git 身份时记录内容清单版本。
python3 -B scan.py paper.pdf --repo /path/to/source \
  --max-input-chars 500000 --max-code-chars 320000 \
  --model gpt-6.1-sol --max-calls 3 --output outputs/local-new

# 只准备并检查输入，不调用模型。
python3 -B scan.py paper.pdf --repo /path/to/source --prepare-only \
  --max-input-chars 500000 --output outputs/preparation-new

python3 -B audit.py rules --markdown
python3 -B audit.py rules --json
```

每次使用新的输出目录。`--max-input-chars` 限制总文本；`--max-code-chars` 限制选入源码的文本。源码文件保持完整，遗漏文件及原因写进清单。局部源码可能支持限定发现，不能据此认证整个仓库没有问题。

通常调用模型两次：抽取与复核。若引用不能精确定位且剩余预算足够，最多增加一次引文修复，再独立复核，因此例子设 `--max-calls 3`。`--no-citation-repair` 可关闭修复。调用上限不足时不悄悄超额调用；未解决引用仍导致弃判。网络或提供商失败不会自动重试或切换模型。

## 实际数据路径

1. `documents.load_document()` 读取原论文，保留文档哈希、页段和阅读顺序视图。
2. `source_bundle.load_repository()` 读取固定提交或本地内容快照，记录文件清单、原字节哈希、行号及遗漏情况。它不执行仓库代码、安装依赖或运行攻击。研究标签、数据、旧报告、测试及凭据不作为源码正文送给模型。
3. `extraction_v4.combine_inputs()` 将论文哈希和源码 manifest/revision 绑定为本次输入身份。回放必须匹配这一身份。
4. 第一次模型调用自动提出声明、实现、权限解释和代码路径；没有读取人工案例或 gold 的步骤。
5. 程序先检查引文。若有少量失败，且预算允许，增加至多一次自动修复：只能替换失败的引用指针，不能改权限、事实状态、代码路径结构或结论。候选检索使用词汇相关性，但候选本身不作为证据；替换后仍须精确定位。
6. 独立复核调用检查完整提案（包含修复后的引文）、声明、实现、权限适用和代码链，逐轴给出支持状态。
7. 程序核对原文引用、来源类型、源码链连续性及接收端点，然后交给既有通用判定规则。

## 新增的关键实现

```python
# 同一论文与固定源码组成一个有版本身份的输入。
source_snapshot = load_repository(repo, revision=commit, max_chars=max_code_chars)
combined = combine_inputs(paper, source_snapshot)

# 模型必须实际收到源码文本，而非只看到一个 GitHub 链接。
proposal = client.generate(EXTRACT_PROMPT, raw_paper_and_source, EXTRACTION_SCHEMA)
review = client.generate(REVIEW_PROMPT, {**raw_paper_and_source, "proposal": proposal}, REVIEW_SCHEMA)

# 权限与交付分开接纳。政策争议不会清空已证实的源码交付事实。
# 最终若缺适用禁令，仍会保留证据不足。
result = decide_extraction(proposal, review, combined)
```

自动提案中的 `scope_resolution` 记录共同知识合同、具体授权或未解决范围。更强投递通道不能自行变成知识豁免，明确的知识授权或诊断限定也不能被一般禁令覆盖。这些是通用语义要求，未编码论文名称或预期 verdict。

`code_path` 记录信息来源、变换、请求、存档读写和投递步骤。每步需要准确源码引用，前一步输出与后一步输入连接；确认构造交付还需要请求端点、实际实验分支及独立复核。文件中的字段存在、只被评分器读取、只在良性模拟器使用，均不能自动充当攻击构造交付证据。

## 如何理解自动结果

这是模型语义审计加确定性证据验收。精确引用和二次复核降低无依据结论，不能提供任意程序的信息流形式证明。记录的静态路径只说明所给代码快照，不自动证明作者历史运行或 ASR 变化。

政策存在争议时，新版仍可保留 `delivery=confirmed` 和相应源码路径，同时输出 `insufficient_evidence`。证据缺失与已证实不存在分别处理。规则全集、优先序、取值和例子见 [规则说明书](RULES_ZH.md)。

ASPI 的新鲜 V4 自动运行已完成：原始 PDF 与固定源码 → 自动提案 → 候选引文选择 → 独立复核 → 程序验收，输出限定的构造不一致。最终运行 3 次模型调用，未提供人工案例、gold 或旧提案。全部开发尝试、失败原因与范围见 [自动运行结果](PAPER_SOURCE_RESULTS_ZH.md)；旧 PDF 自动报告与人工规则回归分别保留，不替换历史结果。
