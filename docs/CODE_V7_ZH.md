# V7 核心代码怎么走

以下是当前实现的关键摘录。完整实现见[`scan.py`](../scan.py)、[`extraction_v7.py`](../extraction_v7.py)、[`construction_contracts.py`](../construction_contracts.py)和[`deployment_v7.py`](../deployment_v7.py)；公式见[V7规则](AUTOMATIC_V7_ZH.md)。

## 1．只读论文建立声明提案

```python
# 投影只保留论文段落，不含源码、人工标签或旧审计结果。
contract_input = prepare_contract_input(document)

# 第一次模型调用：提出角色、知识范围、任务组成和构造过程。
proposal = generate_model(CONTRACT_PROMPT, contract_input, CONTRACT_SCHEMA)

# 核对结构、论文hash和引文位置。引文存在不代表解释正确。
# 返回值明确标为untrusted，不直接产生allow/deny。
declared_contract = validate_contract(proposal, document)

# 与当前论文/源码快照一起绑定，供后续重新核查。
# 后续仍必须引用原论文，不能引用提案来证明自己的判断。
evidence_document = engine.attach_declared_contract(evidence_document, declared_contract)
```

## 2．保留知识边界规则，分别运行另两个轨道

```python
# V7复制提案、去掉新增字段后交给历史V6门禁。
# 新轨道不会把unknown改成deny，也不改写旧轨道规则。
result = v6.decide_extraction(old_extraction, old_review, document, paper_id)
strict_rows = result.get("evidence", [])
boundary_verdict = result["verdict"]

# 第二轨道：核查明确的构造/输入/来源声明与实现是否不相容。
# strict_rows提供已经验收的接收者、实际路径和实例定位。
construction = project_construction_findings(
    extraction["construction_findings"], review["construction_reviews"],
    document, strict_rows, **options,
)

# 第三轨道：分别核查任务来源、时序、实例和部署假设。
# 确认部署缺口也不会生成“Q被禁止”这一权限。
deployment = project_deployment_findings_v7(
    extraction["deployment_findings"], review["deployment_reviews"],
    document, strict_rows, **options,
)
```

构造差异须通过原论文契约、实际来源、语义映射、比较理由、范围及例外复核；源码来源还须关联到实际攻击构造／优化器输入链。如果主张依赖同一评估记录，还要验收对应配置、ID、索引和变换链。

部署缺口须分别通过原论文场景与知识来源、实际输入来源、时序、任务关系、材料性及复核。明确限定的离线已知任务，或已经通过允许的同实例观察取得Q，都不能仅因没有再次解释来源而判为缺口。

## 3．一篇只汇总一次，同时保留类型

```python
crows, drows = construction["findings"], deployment["findings"]
result["evidence"] = strict_rows + crows + drows

# 任一轨道有已确认的限定发现，就有论文级positive。
# 未审清的其他项继续保留，不抹掉已经成立的局部发现。
confirmed = [row for row in result["evidence"]
             if row.get("claim_result") == "confirmed"]
if confirmed:
    result.update(
        verdict="inconsistent",
        reason="confirmed_typed_inconsistency_in_scope",
        has_confirmed_inconsistency=True,
    )
```

完整函数还检查三个类别的回应和输入覆盖。没有确认项不等于阴性；只有固定范围中的证明义务闭合，才允许范围内一致。`confirmed_issue_types`列出触发类别，`knowledge_boundary_verdict`保留原轨道结果。

## 4．这些状态分别表示什么

| 字段 | 选项 | 含义 |
| --- | --- | --- |
| `permission` | `allow / deny / unspecified` | 论文授权、禁止或未确定 |
| `observation` | `present / absent / possible / unspecified` | 匹配接收者上的信息流观察 |
| 构造`assessment` | `mismatch / aligned / uncertain` | 构造比较的自动提案／复核意见 |
| 部署`assessment` | `supported_gap / resolved / uncertain` | 部署假设比较的自动提案／复核意见 |
| `claim_result` | `confirmed / refuted / unresolved` | 程序通过证据门禁后的单项结果 |
| 论文`verdict` | `inconsistent / consistent_within_scope / insufficient_evidence` | 论文级结果；另有不适用和执行失败 |

因此模型输出`mismatch`不会直接变成`confirmed`。任何必要引用、交付、实例、范围或独立复核未通过，该项都会保留未解决状态。

## 5．复核失败怎样恢复

```python
# 外层先检查：仅V7、实际记录了可重试失败、允许一次恢复、还有调用预算。
# 第一次失败及其账本先保存，再为第二回使用独立阶段名。
stage = "semantic_review_retry1"

# prompt、schema、review_input与第一次完全相同。
# 不重新抽取、不添人工证据、不换模型；第二回仍失败则停止。
review = generate_model(engine.REVIEW_PROMPT, review_input, engine.REVIEW_SCHEMA)
```

摘录省略了外层条件。实际代码不会对明确的认证、额度、配置、schema或上下文限制错误盲目重试；每次都受调用上限约束。显式`--resume-review`在新目录做一次复核，并检查原自动来源、提案、hash及原目录未改变。

普通CLI默认V7；直接调用Python兼容函数`scan_source()`时需传`engine_version=7`。普通使用始终只需PDF或网址，不需要调用方填写这些结构化字段。

默认CLI还会在任务来源类别为空且未解决时做一次补充核查。`acquisition_pass.py`只读取当前绑定证据和自动提案，校验来源路径前缀、保留原路径，再追加未受信任的部署候选；最终判定仍由原独立复核和三轨道验收完成。Python调用若需要与CLI相同的补充和恢复配置，需同时传入`acquisition_passes=1, review_retries=1`。
