# 论文重审、误报测试与代码修正结果

这次分别做了原始资料裁定、规范化规则回归、PDF 自动审计及误报控制重测。表中的三类结果使用不同证据范围，不能合并计算准确率。

**最重要的结论：旧人工规范化记录与 TeX 都可能出错，自动模型也会误报。** FHA 的诊断实验限定由自动审计指出并经原文复核；Trojan 的成功窃取示例则被 V2 错当成论文信息权限违规。

## 每篇论文一行

“源证据重审”只回答 `reviewed_papers.json` 明确列出的怀疑。域内“范围内一致”不是整篇论文无问题；AgentDojo/ASB 两行只排除从效用／动作现象直接推出信息越界的逻辑推论。

| 论文 | 旧结构化回归 | 源证据重审 | 新 PDF 自动结果 | 域内误报控制：V2 → V3 |
| --- | --- | --- | --- | --- |
| AdapTools | 证据不足 | 证据不足 | 证据不足 | — |
| Blind Spots in the Guard | 确认不一致 | 确认不一致 | 确认不一致 | — |
| ASPI | 确认不一致 | 确认不一致（限定 Stage 2 构造） | 证据不足 | — |
| MUZZLE | 证据不足 | 证据不足 | 证据不足 | — |
| Breaking MCP with Function Hijacking Attacks (FHA) | 确认不一致 | 证据不足 | 证据不足 | — |
| AGENTCON | 确认不一致 | 确认不一致 | 技术失败 | — |
| Overcoming the Retrieval Barrier | 所列范围内一致／怀疑排除 | 所列范围内一致／怀疑排除 | 证据不足 | — |
| Glue Pizza and Eat Rocks (LIAR) | 确认不一致 | 证据不足 | 证据不足 | — |
| ObliInjection | 确认不一致 | 确认不一致 | 证据不足 | — |
| WebTrap | 确认不一致 | 确认不一致 | 证据不足 | — |
| ICoA | 证据不足 | 证据不足 | 证据不足 | — |
| Attention Is All You Need | — | 未运行 | 非 IPI，不适用 | — |
| Deep Residual Learning for Image Recognition | — | 未运行 | 非 IPI，不适用 | — |
| Adam: A Method for Stochastic Optimization | — | 未运行 | 非 IPI，不适用 | — |
| Trojan Hippo | — | 所列范围内一致／怀疑排除 | 证据不足 | 误报不一致 → 证据不足 |
| TopicAttack | — | 所列范围内一致／怀疑排除 | 证据不足 | 证据不足 → 证据不足 |
| AgentDojo | — | 所列范围内一致／怀疑排除 | 证据不足 | 证据不足 → 证据不足 |
| Agent Security Benchmark | — | 所列范围内一致／怀疑排除 | 证据不足 | 证据不足 → 证据不足 |

## 谁的判断需要改

- **ASPI 此前降为证据不足的解释需要纠正。** 我们将更强的 direct-user 投递基线推成了可能放宽任务知识的例外。§3 没有给出这种知识授权，固定 Stage 2 又确实取得部分任务提示并构造供 `clarif_user` 使用的回复，因此恢复限定的 construction mismatch。该发现不推广到官方 `clarif_ask_user` 的 W 分支，也不证明历史 ASR 膨胀。[§3](https://arxiv.org/html/2605.17324v1#S3)
- **TeX 与旧规范化记录仍需收窄：FHA、LIAR。** 分别涉及明确的诊断配置与 source-training 授权。当前原 11 篇为 5 篇确认不一致、1 篇给定范围内一致、5 篇证据不足。包含四个新增域内控制的 15 篇为 5／5／5。此前 4／5／6 的记录保留为 ASPI 修正前的快照。
- **算法真实误报：Trojan Hippo。** V2 将受害者“未经同意不应发送”的安全目标与攻击成功示例拼成 `deny + present`，错误升级为论文威胁模型矛盾。V3 的政策类型门与输入边界门阻止了这一推论。
- **新附件也有过强或过时说法。** Trojan 的训练 mutator 实际可看到训练 user request；不能说只看到主题。Obli 的正式回答存档已经完成，远端归档/CAS 收尾未闭合与“没有做行为执行”不同。构造信息流与行为效应分别裁定，不能用 p 值不显著抹去输入差异。
- **没有用模型反对旧标签就自动认定模型错。** FHA 是模型提示人工补查后修正旧判断的具体例子。AGENTCON 的同请求计划／优化损失与直接把原 query 发给生成 LLM 也分开表述。
- **未证实的百分比不作为 gold。** AgentDojo 60.87→72.19、ASB 73.58→9.25 未在本轮找到完整配置/原始运行，不能当已复现数值或信息越界证明。

## 实际完成了哪些测试

- 冻结 V2 的 4 篇域内控制：1 个不一致误报、3 篇证据不足。输入过长的初次失败另存为 attempts，明确增大上限后才完成两份长论文，未截断全文。
- 同一 4 篇在 V3 独立重测：4 篇均为证据不足，未再确认该误报。**这不等于 4 个已认证 true negative，也不支持“FPR=0”的普遍性结论。**
- 18 篇文档主测试：17 篇完成，AGENTCON 来源阻挡单列失败；最终 1 篇确认不一致（Blind Spots）、13 篇证据不足、3 篇域外不适用、1 篇技术失败。
- 修复 PDF 两栏引文定位后，用相同 PDF 字节哈希、相同原主文本、固定模型输出做零模型调用回放，恢复 Blind Spots 引文并将 Adam 的引用定位失败按证据不足/可核验主题处理，而不是伪造运行结果。
- 原始资料重审集合为 15 篇、25 个有限怀疑。ASPI 修正后的标签分布为 5／5／5，最新规则回放另存到 ASPI 范围纠正目录。此前 15／15 的标签一致记录属于当时的开发集回归，不能当端到端检测准确率。本次纠正来自原文与固定构造链的重新审定，没有新增模型对 ASPI 的自动确认。

## 完整过程与机器可读结果

- [逐篇 TeX／附件／算法裁定](TEX_ALGORITHM_COMPARISON_ZH.md)
- [V2 域内误报测试](results/2026-11-19-source-review/negative-baseline/report.md)
- [V3 域内控制独立重测](results/2026-11-19-source-review/negative-final/report.md)
- [18 篇自动审计最终回放](results/2026-11-19-source-review/automatic-final/report.md)
- [ASPI 修正后的 15 篇源证据规则回归](results/2026-11-19-aspi-scope-correction/source-regression/report.md)
- [ASPI 修正前的源证据回归快照](results/2026-11-19-source-review/source-regression/report.md)
- [修正前的并列字段及步骤 JSON，保留当时的 ASPI 标签](results/2026-11-19-source-review/comparison/report.json)
- [代码修正与中文注释](V3_CHANGES_ZH.md)

## 环境与重现

固定请求模型为 `gpt-6.1-sol`，使用本机既有 ChatGPT/Codex 登录；CLI 未回传实际模型标识时保留 null。Python 3.13.5、pdftotext 26.02.0。未使用 API-key 供应商；使用现有 Codex 额度。仅子进程继承已有系统代理，未改系统网络配置。

```bash
python3 -B audit.py evaluate all
python3 -B audit.py evaluate all --legacy
python3 -B audit.py audit trojan_hippo topicattack agentdojo asb --json --details
python3 -B benchmark.py --mode scan --manifest benchmarks/source_review.json --model gpt-6.1-sol --workers 2 --max-input-chars 300000 --max-calls 36 --output outputs/new-study
python3 -B replay_study.py --run outputs/new-study --refresh-pdf-views --output outputs/new-replay
python3 -B -m unittest discover -s tests -v
```

每次使用新输出目录。`--legacy` 保留旧 7／1／3，不改写历史快照。新文档的来源可能不可用，失败必须保留。
