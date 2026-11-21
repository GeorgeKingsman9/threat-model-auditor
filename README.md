# Threat Model Auditor

默认入口已升级为V6：直接运行 `python3 -B scan.py PAPER.pdf` 或 `python3 -B scan.py PAPER_URL`，输出目录自动生成。在原声明模型与实现信息流比较之上，分别审查问题、文档、标签及反馈输入，取得固定版本的有界数据原文样本，并单列部署来源问题。输出仍是一篇一条三值结论及具体位置。见 [V6实现与边界](docs/AUTOMATIC_V6_ZH.md)；[V5说明](docs/AUTOMATIC_V5_ZH.md)保留作历史记录。

**V5三篇开发案例历史测试**：两轮原始URL自动运行均为3篇不确定；修复组合记录ID的确定性校验后，原自动提案与独立复核重新验收为 **ASPI限定不一致、MUZZLE与ObliInjection不确定**。重放没有修改证据或增加模型调用，也不是独立新实验。该轮没有论文级negative，软件检查398项通过。见[完整过程、结果与失败尝试](docs/V5_PILOT_RESULTS_ZH.md)及[原Notion元素建模与代码对应](docs/NOTION_MODEL_MAPPING_ZH.md)。

给出一份本地 PDF 或论文网址，自动读取论文、发现明确关联的官方源码、固定源码版本，再抽取声明与信息流、独立复核、运行规则，最后**每篇论文输出一条带证据链的结果**。

用户不需要先整理 `cases.json`、写 `allow/deny` 或提供 gold。人工案例和标签用于开发、规则回归与事后评估，不是自动审计的前置输入，也不能据其标签一致率声称自动检测准确率。

## 直接运行一篇论文

需要 Python 3.10+、已安装并使用 ChatGPT 登录的 Codex CLI。PDF 文字提取需要 Poppler 的 `pdftotext`，或可选 Python 包 `pypdf`：

```bash
# 仅在没有 PDF 文字提取工具时安装；不需要 GPU。
python3 -m pip install pypdf

# 本地 PDF：自动查找论文明确关联的官方源码。
python3 -B scan.py input.pdf --output outputs/my-paper

# 论文 URL：同一条自动流程。
python3 -B scan.py https://arxiv.org/abs/2605.17324v1 --output outputs/aspi

# 只审论文文本，不发现或读取源码。
python3 -B scan.py input.pdf --paper-only --output outputs/paper-only

# 只准备输入与发现记录，不调用模型。
# 默认仍可读取公共论文链接、发现并读取明确关联的源码。
python3 -B scan.py input.pdf --prepare-only --output outputs/prepared
```

每次使用一个新的输出目录。默认使用现有 ChatGPT/Codex 登录与账号额度；不需要另配 Claude API 或手写证据 JSON，也不保证账号使用免费。`--model` 可指定自己可用的模型，未指定时不猜测实际模型名称。

完整流程、发现边界与输出解释见 [自动工作流说明](docs/AUTOMATIC_WORKFLOW_ZH.md)。

**此前V4源码重试**：MUZZLE与ObliInjection曾分别自动取得并读入81/81、19/19个eligible源码文件；V5继续补配置和固定依赖。历史取材修复、全部尝试和当时判定原因见 [源码重试报告](docs/SOURCE_RETRY_RESULTS_ZH.md)。

**此前V4默认入口重测**：只给论文网址或原始PDF，4篇均完成，得到1篇positive、0篇negative、3篇不确定。该历史运行与新V5测试分别保留；逐篇结果及所有失败尝试见 [默认入口重测报告](docs/AUTOMATIC_RETEST_RESULTS_ZH.md)。

## 默认自动流程

1. **读论文**：提取 PDF 页码、原文与内容 hash；支持本地 PDF/HTML/TXT、公开论文 URL，以及部分可明确解析的 landing page。
2. **发现源码**：检查论文及支持的关联入口中的明确代码链接，保留候选、关联依据和选择/放弃记录。普通引用中的 GitHub 链接不自动等于作者实现。
3. **固定与读取**：明确找到官方源码时固定版本，读取可支持的源码快照，记录文件、行号、hash 和预算遗漏；不执行仓库代码。
4. **V6 抽取与复核**：先只读论文，提出尚未受信任的声明模型及任务组成；再将论文概念与源码、数据原文样本对齐，分别提出权限、接收角色、实例关系与跨文件信息流，并逐项回应静态输入候选；最后独立复核。通常3次调用，必要时增加1次有界引文恢复，仍要求精确定位。V4/V5保留用于历史比较。
5. **规则与报告**：核对政策类型、角色、阶段、信息实例及交付路径；一篇一行汇总，可展开查看依据、理由和未解决问题。

**没有找到明确源码或存在归属歧义时，保存发现记录，只审提供的论文文本。** 这不能验证实际实现，也不能因为“未发现代码/违规”就输出 negative。明确选择的源码若读取失败，失败同样须保留，不能冒充完整审计成功。

`--paper-only` 保留仅论文路径。`--repo` 是可选高级覆盖，用于指定已知关联或本地源码，不是普通用户必须填写的参数：

```bash
# 高级用法：显式覆盖源码来源，并固定公开仓库的完整提交。
python3 -B scan.py input.pdf \
  --repo https://github.com/OWNER/REPOSITORY \
  --repo-revision FULL_COMMIT_SHA \
  --output outputs/explicit-source
```

源码读取范围、V4 证据验收与历史显式仓库命令见 [论文与源码审计说明](docs/PAPER_SOURCE_AUDIT_ZH.md)。

## 怎样看结果

输出目录中的 `report.html` 可以直接打开；另有 `report.md`、`report.json`、单篇结果及对应步骤的输入/输出。源码发现、版本、文件选择、引用和模型调用记录都应与本次结果一起阅读。

| 结果 | 意思 |
| --- | --- |
| `inconsistent` | 在明确范围内确认了声明与构造信息流的不一致；不能自动推广到整篇或历史实验。 |
| `consistent_within_scope` | 所列怀疑有具体授权、不同实例或排除交付等反证；不是只因没找到问题。 |
| `insufficient_evidence` | 权限、关联、路径或证据不足；不能翻译成“没有问题”。 |
| `not_applicable` | 非本研究针对的 IPI 领域，不等于论文所有方面正确。 |
| `technical_failure` | 下载、解析、模型等步骤失败，没有形成有效论文结论。 |
| `not_run` | 只准备了输入，尚未调用模型审计。 |

失败和未运行也保留一行。内部可能核对多个阶段或信息流，但统计论文结果时只计一次。

模型抽取和独立复核仍可能误读语义。精确引文与规则验收不等于任意程序的信息流形式证明，不会执行攻击、验证作者历史实际请求，或自动证明 ASR 被抬高。

## 已有结果与验证范围

**ASPI 的真实 V4 论文＋源码运行已经完成**：原始 PDF 与固定源码输入，3 次模型调用，12 步代码链与引文通过验收，输出限定构造不一致。发现限定于任务派生的部分查询进入 Stage 2 恶意回复构造、再用于相应 `clarif_user_HR` 分支，未推广到官方 W 分支或历史 ASR。[实际结果与全部尝试](docs/PAPER_SOURCE_RESULTS_ZH.md)

该成功运行使用明确给定的固定仓库。默认源码发现是其前置环节；一个旧成功结果不能代替新输入的关联发现验证。这是已知开发案例的能力验证，不是泛化准确率。

原始资料重审目前保留 15 篇、25 个有限怀疑，分为 5 项限定发现、5 项限定怀疑排除、5 项证据不足；其中 AgentDojo/ASB 的排除是跨问题类型的逻辑对照。四篇 PDF 控制重测均为证据不足，不能算作已认证自动 true negative。旧人工回归、旧 PDF 输出与真实 V4 结果分别保留，不相互覆盖。

- [全部重审结果及机器可读报告](docs/SOURCE_REVIEW_RESULTS_ZH.md)
- [逐篇 TeX、附件与算法的裁定](docs/TEX_ALGORITHM_COMPARISON_ZH.md)
- [核心判定简版](docs/RULES_SUMMARY_ZH.md) · [完整规则说明](docs/RULES_ZH.md)
- [代码中文讲解](docs/CODE_WALKTHROUGH_ZH.md) · [V3 修正说明](docs/V3_CHANGES_ZH.md)

## 开发与回归评估

下面是开发者入口，读取已有规范化案例；**不代表从新论文自动发现证据**，普通用户无须先执行这些步骤：

```bash
# 当前源证据裁定记录的规则回归；不调用模型。
python3 -B audit.py evaluate all

# 保留旧 11 篇数据与结果的回归入口。
python3 -B audit.py evaluate all --legacy

# 查看已整理的论文记录；不同于 scan.py 自动读新论文。
python3 -B audit.py audit aspi muzzle --json --details

# 查看规则与运行离线程序测试。
python3 -B audit.py rules --json
python3 -B -m unittest discover -s tests -v
```

`audit` 不读取 gold；`evaluate` 先判定，再与标签比较。规范化案例和 gold 已参与开发，回放一致率不能替代端到端自动检测的准确率、召回率或误报率。

人工扩展数据结构见 [字段选项](docs/OPTIONS_ZH.md) 与 `examples/`。这些资料供维护案例集和规则测试使用，不是“上传一篇论文”所需的人工准备。

完整原文、源码快照、模型原始输出留在本地运行目录，默认不上传 GitHub。部分历史审计路径属于本地研究归档；其来源边界见 [PROVENANCE](docs/PROVENANCE.md)。

代码与原创元数据采用 MIT 许可证。论文、上游源码及外部材料遵循各自许可，本仓库不重新授权这些材料。
