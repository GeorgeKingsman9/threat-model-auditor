# 当前 pilot 到底跑了什么

## 运行设置

这是本地、确定性的**规则复核实验**。输入是我们事先人工整理好的声明和证据 JSON；
没有调用 LLM，没有生成新攻击，没有训练，也没有重新执行被审论文的原实验。
因此当前没有模型名、temperature、seed、GPU 型号或攻击预算这些运行参数。

程序分两步：先对给定证据应用规则，再按论文聚合。`evaluate` 额外比较既有人工标签。
每篇论文只贡献一条最终结果。原始 `checker.py` 入口仍保留，便于复用规则引擎。

## 内置论文与固定审计范围

| ID | 核查重点 | 当前规范化记录给出的结果 |
| --- | --- | --- |
| `aspi` | 分开看 Stage 1 designer 与 Stage 2 的部分 query 访问 | 不一致 |
| `obliinjection` | 公开 optimizer 的完整目标 query，与 Table XI 历史输入来源 | 不一致，仍有未解决子问题 |
| `webtrap` | 原始 file-browser 信息边界；本地对照不计为另一篇论文 | 不一致 |
| `blind_spots` | Exp. 1 的文档访问与声明边界 | 不一致 |
| `fha` | 直接 same-query 条件与用户 prompt 可见性限制 | 不一致 |
| `agentcon` | benchmark request 构造与未来 request 的可见性假设 | 不一致 |
| `liar` | same-benchmark 条件的源知识库文档访问 | 不一致 |
| `retrieval_barrier` | 明确给定 query 的检索 benchmark 输入 | 此审计范围内一致 |
| `muzzle` | 离线 operator 提供任务，与在线未来任务的来源分开 | 证据不足 |
| `adaptools` | held-out 在线任务可见性，与离线开发分开 | 证据不足 |
| `icoa` | 直接 system-prompt 读取与 benchmark identity 来源分开 | 证据不足 |

准确版本、代码 revision、实验臂和配置以 JSON 中的 `version`、`audit_scope` 和 `scope` 为准：

```bash
python3 -B audit.py list --json
python3 -B audit.py audit aspi --json --details
```

这里的结果是**按随附记录重新计算的结果**，不是本次重新读取并核实全部论文后的独立结论。
部分记录依赖本地历史材料，公开程度见 [PROVENANCE.md](PROVENANCE.md)。

## 当前怎样测评

```bash
python3 -B audit.py evaluate all
```

当前 11 篇的预期分布为：7 篇确认不一致、1 篇审计范围内一致、3 篇证据不足。
这组已知案例参与过规则调整；11/11 标签一致仅说明当前回归没有改变预设判断，**不是 100% 自动审计准确率**。
本仓库尚未提供独立保留集，也没有测量论文/代码信息抽取的 precision 或 recall。

正式评估应先固定标注规则、输入和版本，再把未参与开发的论文交由独立标注者整理；
以论文为计数单位，分别报告不一致的 precision/recall、证据不足比例和证据定位是否正确。
不能通过看到答案后反复修改同一批案例来声称泛化效果提升。
