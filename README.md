# Threat Model Auditor

**当前版本已完成源证据重审、ASPI 范围解释纠正和真实误报测试。** 原 11 篇的严格范围判定从旧 7／1／3 改为 5 篇确认不一致、1 篇范围内一致、5 篇证据不足；四个新增域内控制另有有限范围反证。ASPI 的发现限定于发布 Stage 2 为 `clarif_user` 构造回复时使用部分任务信息，未推广到官方 `clarif_ask_user` 分支或历史 ASR。
18 篇 PDF 测试保留所有状态，四篇曾被怀疑误报的工作已实际重测。
结果、错因和代码改动见 [全部重审结果](docs/SOURCE_REVIEW_RESULTS_ZH.md)、[逐篇 TeX 对照](docs/TEX_ALGORITHM_COMPARISON_ZH.md)、[V3 中文注释](docs/V3_CHANGES_ZH.md)。


A small, deterministic checker for consistency between paper-declared information
access and manually normalized implementation evidence. One final row per paper.

支持两种入口：`audit.py` 复核已经人工整理的 JSON；新增的实验性 `scan.py` 接收 PDF/论文网址，调用模型抽取并复核原文依据，再交给规则引擎判断。每篇仍只输出一条结果。

`scan.py` 默认接现有 Codex CLI 的 ChatGPT 登录，使用该账号的 Codex 额度；不要求另配 Claude API。
模型判断尚需人工复核，文档入口目前只审提供的论文文本，不会自动运行攻击、证明历史实验输入，或完整审计任意源码仓库。

新增 **论文＋源码自动入口**：`scan.py --repo ... --repo-revision ...` 实际读取固定源码快照，再自动抽取与独立复核跨文件信息流。输入不含人工审定案例或 gold；不执行仓库代码。完整命令和范围见 [论文与源码自动审计](docs/PAPER_SOURCE_AUDIT_ZH.md)。

ASPI 的最终原始论文＋源码新鲜自动运行已输出限定 `inconsistent`，3 次调用，12 步代码链与全部引文通过验收。此前失败尝试也保留，详见 [实际自动结果与过程](docs/PAPER_SOURCE_RESULTS_ZH.md)。这是一篇已知开发案例的验证，不是总体检测准确率。

讲解时先看 [核心判定简版](docs/RULES_SUMMARY_ZH.md)，只保留三个关键判断及公式。全部规则的定义、数量、优先序、状态取值及例子见 [完整说明书](docs/RULES_ZH.md)。可运行 `python3 -B audit.py rules --json` 导出；核心业务规则 30 条，源码验收要求 15 条，抽取门与结构校验单列。

## 输入 PDF 或论文网址

需要已安装且以 ChatGPT 登录的 Codex CLI。PDF 提取需要 Poppler 的 `pdftotext`，或可选的 `pypdf` 包。

```bash
# 如本机没有 pdftotext，可在自己的 Python 环境安装 PDF 读取依赖
python3 -m pip install pypdf

# 本地上传的 PDF：将文件路径作为输入
python3 -B scan.py paper.pdf --output outputs/my-paper

# 论文网址（支持 arXiv abstract/PDF、普通 PDF 和部分论文 landing page）
python3 -B scan.py https://arxiv.org/abs/2605.17324v1 --output outputs/aspi-document

# 只读取文档、保留页码，不使用任何模型额度
python3 -B scan.py paper.pdf --prepare-only --output outputs/prepared-paper
```

输出目录包含原始文档文本提取、抽取结果、模型复核、规则判定、JSON 报告，以及可直接打开的 `report.html` / `report.md`。
过程和设置详见 [docs/DOCUMENT_AUDIT_ZH.md](docs/DOCUMENT_AUDIT_ZH.md)。
逐段中文注释讲解见 [docs/CODE_WALKTHROUGH_ZH.md](docs/CODE_WALKTHROUGH_ZH.md)。

## 展示所有文章的过程和结果

```bash
# 已有 11 篇的规则回归；另外 3 篇无关负例显示为尚未在此模式运行
python3 -B benchmark.py --mode regression --output outputs/regression

# 读取完整 14 篇清单，含 Attention、ResNet、Adam 三篇无关论文
python3 -B benchmark.py --mode prepare --output outputs/documents

# 用现有 Codex 登录做文档自动审计；沿用已提取的文档
python3 -B benchmark.py --mode scan --prepared-dir outputs/documents --output outputs/document-audit
```

每次运行使用一个新目录。**失败、访问受阻、尚未运行的文章仍保留一行**；不会把它们算成“没有不一致”。
无关论文应为 `not_applicable`（该领域审计不适用），用于测适用性筛选；不能和域内已核实一致的论文混算。

**最新实际进度**见 [重审结果](docs/SOURCE_REVIEW_RESULTS_ZH.md)：Codex 子进程继承已有系统代理后已完成真实文档测试；17 篇完成、1 篇来源阻挡。早先未运行的记录保留在历史结果页。

## 快速运行

需要 Python 3.10+ 和可选的 Bash。下面的已有 JSON 回归入口无第三方依赖，也不调用模型。
进入本仓库目录后：

```bash
# 查看支持的论文 ID
python3 -B audit.py list

# 每篇只显示一行：是否确认不一致，以及证据状态
bash scripts/audit.sh aspi
bash scripts/audit.sh muzzle
python3 -B audit.py audit aspi obliinjection
python3 -B audit.py audit all

# 查看一篇论文的声明、实验范围和详细证据
python3 -B audit.py audit aspi --json --details

# 保存 JSON；拒绝覆盖已有文件
python3 -B audit.py audit all --output outputs/papers.json

# 对照我们已有的人工标签做回归检查
python3 -B audit.py evaluate all

# 检查程序行为
python3 -B -m unittest discover -s tests -v
```

`audit` 不读取人工标签。`evaluate` 先产生同样的判定，再和标签比较。
命令退出码：正常审计为 `0`（即使发现不一致）；标签不匹配为 `1`；输入或命令错误为 `2`。

示例输出：

```text
paper   confirmed_inconsistency   status
aspi    yes                       有已确认的不一致
muzzle  no                        证据不足
```

`no` 的准确意思是“当前证据未确认不一致”。旁边的状态区分“审计范围内一致”和“证据不足”。
一篇论文内可能需要核查几个角色或实验阶段；任意一处确认不一致，整篇便记为 `yes`，统计时只计一次。

## 输入是什么

每条内部记录包含同一实验范围下的两类信息：

- `rules`：论文明确允许或禁止的信息流，即声明模型。
- `observations`：实现中确认出现、确认没有出现或仅有可能出现的信息流，即实现证据模型。

`allow` / `deny` 是声明端的两个选项；`present` / `absent` / `possible` 是证据端的三个选项。
例如同一角色、阶段、信息、表示和用途下，`deny + present` 表示“论文排除这种访问，但实验确认发生”，判为不一致。
论文没有说明时留空 `rules`，不自行推断为 `deny`。

完整字段、所有选项和判定表见 [docs/OPTIONS_ZH.md](docs/OPTIONS_ZH.md)。
当前 pilot 的输入、范围和结果边界见 [docs/PILOT_ZH.md](docs/PILOT_ZH.md)。

## 新增论文

按 [examples/new_case.json](examples/new_case.json) 和 [examples/new_paper.json](examples/new_paper.json)
的结构填写。示例是明确标注的占位输入，不能作为真实论文的发现。
完成自己的证据整理后运行：

```bash
python3 -B audit.py audit my_paper \
  --cases examples/new_case.json \
  --papers examples/new_paper.json --json --details
```

示例缺少真实声明和证据，预期输出“证据不足”。将 `my_paper` 改为自己的 ID，并把两个 JSON 换成自己的记录。
新论文默认不需要 `gold`。需要测评时，另写 `{ "my_paper": "insufficient_evidence" }` 这样的论文级标签文件：

```bash
python3 -B audit.py evaluate my_paper \
  --cases examples/new_case.json --papers examples/new_paper.json \
  --gold examples/new_gold.json
```

## 可复现性和证据边界

默认集合是经原始资料重审的 15 篇论文、25 个限定怀疑及分离保存的裁定标签；旧 11 篇集合用 `--legacy` 保留。
它们用于演示和回归检查，已参与规则设计；标签一致率不能当作未见论文的检测准确率。

核心 `checker.py` 只检查格式、字段匹配和判定规则，不联网。
新增文档入口还会进行原文子串定位和模型语义复核；这仍不是独立人工核验证据。
`paper_text` 的实现证据可能来自论文对实验过程的描述，不能等同于实际运行日志。
`archived` 记录中部分引用指向整理时的本地审计材料；这些历史路径不是本仓库中的文件。
详见 [docs/PROVENANCE.md](docs/PROVENANCE.md)。本仓库可重放给定记录的判定；对底层材料的独立核验需要对应来源。

代码与本仓库原创元数据采用 MIT 许可证。引用的论文、上游源码和外部材料仍遵循各自的许可；本仓库不重新授权这些材料。
