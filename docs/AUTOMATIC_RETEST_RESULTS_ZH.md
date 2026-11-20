# 仅给论文输入：真实自动重测

本轮最终完成 **4 篇：1 篇 positive、0 篇 negative、3 篇不确定**。这次实际只传论文网址或原始 PDF，没有传 `--repo`、人工 cases/gold 或旧模型提案。代码版本为 `3ff7787`，请求模型为 `gpt-6.1-sol`，使用现有 ChatGPT/Codex 登录。CLI 没有暴露实际模型标识，报告保留 null。

## 每篇一个结果

| 论文 | 输入 | 自动取材 | 最终结果 | 实际判定依据／缺口 |
| --- | --- | --- | --- | --- |
| ASPI | 论文 PDF 网址 | 自动关联 `scaleapi/aspi`；固定 `e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d`，读取29/32个eligible源码文件 | **Positive / inconsistent** | Stage 2作者请求接收同实例的部分任务信息，生成回复存入对应组，再进入预生成 `clarif_user_HR` 分支。任务知识限制适用，交付静态路径与独立复核通过。 |
| Overcoming the Retrieval Barrier | 论文 PDF 网址 | 读到论文；未解析完整的 Zenodo 源码链接，没有读取源码 | **不确定 / insufficient_evidence** | 目标query与embedding API访问被论文明确允许，这两项疑点已排除；邮件历史是否进一步进入攻击构造仍未确认，因此整篇未输出negative。 |
| MUZZLE | 论文 PDF 网址 | 自动发现 `gsiros/muzzle`，固定 `9f3effa1668fa29dcba8f2454e711ddf9ef3c038`；源码archive下载超时，降级仅论文 | **不确定 / insufficient_evidence** | 发现阶段的trace访问已有授权；配置是否含特权信息、是否进一步交给攻击构造者仍不明确。此轮未解决的问题与先前人工记录的未来query来源缺口并非完全相同。 |
| ObliInjection | 本机原始 `arXiv:2512.09321v3` PDF | 完成PDF提取；没有自动确定源码来源 | **不确定 / insufficient_evidence** | 仅按论文描述不能恢复我们已知的发布版优化器源码级发现。本轮没有自动发现该已知问题，不能算成功检出。 |

ASPI的确认只覆盖指定生成dataset、`ask_user`被调用且HR变体非空时的条件静态路径。不证明作者历史运行使用了该配置，不证明ASR变化，不扩展到 `exec_tool`、`clarif_tool` 或 `clarif_ask_user`。源码预算遗漏3个eligible文件，不能声称全仓库覆盖。

## 相比旧入口验证了什么

- ASPI现在从一个论文网址出发，自动找到、固定并读取源码，自动抽取和复核后确认不一致；不再依赖手动指定仓库或整理证据。
- 其余三篇实际使用论文文本形成结果，材料缺口均保留，不能包装成完成了源码审计。
- **自动negative能力仍未验证成功**。Retrieval Barrier排除了具体疑点，但另有未解决项，所以不计true negative。
- 四篇都是已知开发案例；人工参考标签在模型运行结束后才附加。同标签2/4只是事后对照，不是陌生论文检测准确率。

## 运行与调用记录

最终三篇网址批次完成7次CLI调用：ASPI 3次（抽取、引文恢复、独立复核），MUZZLE 2次，Retrieval Barrier 2次。本地ObliInjection完成2次，总计最终有效运行9次；逐篇仍只计一条论文结果。逐阶段账本分别保存，不能把累计3/5/7次相加。

本次没有调用付费API后端，没有执行论文仓库、攻击或ASR实验。Codex使用账号额度；调用次数不等于费用/token上限，未报告用量也不等于零用量。

默认命令形式为：

```bash
python3 -B benchmark.py --mode scan \
  --only aspi retrieval_barrier muzzle \
  --provider codex --model gpt-6.1-sol \
  --max-calls 9 --workers 1 --model-timeout 300 \
  --output outputs/new-auto-retest

python3 -B scan.py /path/to/original-paper.pdf \
  --provider codex --model gpt-6.1-sol --max-calls 3 \
  --output outputs/new-local-pdf-test
```

本机当时系统代理指向失效端口，本轮仅用子进程路由让公共材料直连、模型走已验证的现有代理；未改系统设置。外层执行环境允许Codex CLI初始化，子模型仍使用只读沙箱、禁用工具。完整进程配置hash与每次尝试见下方清单；正常网络环境不需要沿用本机端口。

## 测试中发现并修复的程序问题

ASPI最初获取GitHub完整提交信息时出现HTTP正文截断，异常未被捕获，导致整个批次中断。修复改为读取单条提交列表固定SHA，捕获截断下载，并在每篇边界保留失败记录。模型调用账本也改为逐阶段落盘，避免后续论文失败丢掉先前调用记录。**未修改判定规则、参考标签或已有审定输入来凑结果。**

程序检查 **300/300通过**。这属于软件行为验证，不是300篇论文或检测准确率。

## 所有尝试保留

| 尝试 | 实际结果 |
| --- | --- |
| 原默认网络：三篇网址 | 三篇正文下载失败，未调用模型。 |
| 原本地PDF尝试 | ObliInjection论文读取成功，但CLI初始化失败；1次已分发CLI调用，无完整usage。 |
| 初次隔离路由，修复前代码 | ASPI的HTTP截断异常中断批次；MUZZLE已完成两次模型调用并判不确定；Retrieval Barrier未运行。批次未写出完整账本，不能恢复精确用量。 |
| 修复后全新网址批次 | 三篇全部completed：ASPI positive，MUZZLE与Retrieval Barrier不确定；7次已完成CLI调用。 |
| 修复后本地原始PDF | ObliInjection completed / 不确定；2次已完成CLI调用。 |

这些是同一4篇论文的开发尝试，不增加论文分母。全部已知CLI分发共12次，其中11次有已完成模型步骤；较早失败/中断的用量不完整，不能拼出完整费用。

- [最终机器可读摘要与证据位置](results/2026-11-20-automatic-retest/report.json)
- [全部尝试、配置与原始产物hash](results/2026-11-20-automatic-retest/process_manifest.json)

本机完整原文、源码快照、模型提议和复核留在 `outputs/2026-11-20-default-auto-retest-081314/`。合并HTML位于其 `combined/report.html`，主表每篇一行，下面可展开完整步骤。公开摘要不复制整份论文或源码。

当前主要缺口包括：断行的非GitHub源码链接解析、Zenodo等来源接入、大源码archive的可靠读取，以及权限适用性和角色信息流的语义抽取。不能用人工补答案替代这些自动能力。
