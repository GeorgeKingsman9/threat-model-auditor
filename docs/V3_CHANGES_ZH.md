# V3 改了什么，为什么改

这次改动来自实际误报与原始资料裁定，不以匹配旧 TeX 或旧标签为目标。
旧 V2 记录和结果保留，`--legacy` 可回放。新默认审核集是 15 篇、25 个明确列出的怀疑。

## 1. 先判断“禁止的是什么”

真实 V2 负例测试将 Trojan Hippo 的成功窃取示例判成论文不一致：
“没有用户同意不应发送”的安全目标被规范化成 deny，攻击成功被规范化成 present。
这证明攻击有效，不能证明作者把不允许的知识交给攻击者。

V3 的 `policy_kind` 区分攻击者知识限制、受害者安全目标和协议要求。
`issue_type` 另区分信息边界、执行协议、任务完整性、获取缺口和安全结果。

```python
# checker.audit_case 仍先用旧规则得到候选结论。
verdict, reason = decide(permissions, states)

# 再用有出处的范围、输入边界和问题类型审查候选。
# 即使都是 deny + present，受害者安全目标被攻破也不能确认论文违规。
assessment = assess_claim(case, verdict, reason, permissions, states)
verdict, reason = assessment["verdict"], assessment["reason"]
```

## 2. 禁令必须适用于当前角色、阶段和实验条件

ASPI 的 Stage 2 输入确有任务信息，但 §3 外部对手预算是否约束披露的强基线需要说明。
FHA 的旧 single-payload 案例有明确诊断实验限定，不能直接当可部署攻击预算违例。
LIAR 明确授权 source-training 子集；同名 NQ 不能证明目标文档或索引被读取。

```python
# V3 不根据论文名判断；任何论文都使用同一组字段。
policy = case["assessment"]["policy_application"]

# 需要确认的是适用于当前怀疑的攻击者知识约束。
# uncertain 不会因为找到了额外输入就自动变成 applicable。
if policy["policy_kind"] != "attacker_knowledge_constraint":
    # 返回证据不足，或在有正面类型反证时排除这一特定推论。
    pass
if policy["status"] != "applicable":
    # 保留已经确认的信息流，暂不确认权限违反。
    pass
```

完整枚举与证据要求见 [V3 数据契约](../adjudication/SCHEMA_V3_CONTRACT.md)。

## 3. “出现过数据”与“交给构造者”分开

`delivery` 要记录实际接收边界及依据：论文明确过程、固定生效源码路径、保存请求或运行记录。
仅在文档、数据集或评价器里出现 query，或找到可能路径，不足以确认构造者收到它。
`task_relation` 区分同一评估实例、训练实例、不同实例、主题和未知关系。
训练不是天然合法：如果明确禁令确实适用于训练阶段，仍可确认违规。

## 4. 阴性也要有正面证据

`claim_result` 是 `confirmed`、`refuted` 或 `unresolved`。
许可、不同实例、被排除的输入边界、不同问题类型可以提供反驳；仅没找到证据不能。

TopicAttack 的默认构造路径确实只接收许可正文及攻击目标；这与评价器持有用户问题不同。
Trojan 的一个已核 train/test 传播对可以排除相应测试 query 被用于该固定 payload 的怀疑，不能推广到全论文。
AgentDojo/ASB 的协议/效用现象只用于排除“这些现象本身证明信息越界”的推论，未确认附件中的百分比。

论文汇总始终一篇一条：任何确认不一致保留发现；只有明确列出的怀疑都被反证排除才记范围内一致；其余弃判。
“范围内一致”不等于整篇实现认证。

## 5. PDF 引文定位修复

两栏 PDF 的 `pdftotext -layout` 可能逐行交织左右栏。模型引用的真实段落因此不在主文本连续出现。
新增默认阅读顺序视图，仍来自同一组 PDF 字节，不进行模糊语义匹配。
定位记录原 PDF hash、文本视图、视图 hash 和原文 offset。

```python
# replay_study.enrich_document 必须先锁住原始证据版本。
if refreshed["sha256"] != original["sha256"]:
    raise ValueError("source PDF bytes changed")

# 不替换模型原先看到的主文本；只补同一 PDF 的阅读顺序视图。
# 页数、页 ID 和每页主文本也必须相同，才能复用固定模型输出。
```

政策句不能当自己的实现证据；同页重叠引文或无法跨视图证明独立的引用会弃判。
无法定位的域外主题引用归证据不足，不伪装成已经判断为非 IPI，也不误算成系统下载失败。

## 6. 行为影响和判定保持独立

`behavioral_impact` 只保留状态、依据和限制，不进入信息流判定。
没有显著 ASR 提升不能抹去已成立的构造差异；确认差异也不能直接推断效应大小或必要性。

## 7. 如何验证

测试覆盖安全目标误报、强基线适用性、source/target 身份、训练许可、输入边界、反证、查询粒度、
gold 不参与判定、Unicode/空白/两栏引文、不同视图、来源版本锁定、并列报告和历史回放。
四篇域内控制实际重测均无确认不一致，但仍全部证据不足；不能据此声称检测准确率高。

详见 [实际全部结果](SOURCE_REVIEW_RESULTS_ZH.md) 与 [逐篇 TeX／算法裁定](TEX_ALGORITHM_COMPARISON_ZH.md)。
