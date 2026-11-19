# 完整字段和选项

## 1. 两端各自填写什么

| 位置 | 所有合法选项 | 含义和填写条件 |
| --- | --- | --- |
| `rules[].permission` | `allow` | 论文允许该角色在该阶段按指定用途访问该信息。不是要求它必须访问。 |
| 同上 | `deny` | 论文明确排除这种访问。不能把“没提到”填成禁止。 |
| `observations[].status` | `present` | 引用证据确认指定信息在指定范围内被该角色接收或使用。只在仓库里找到字段不够。 |
| 同上 | `absent` | 有足够证据确认这条信息流在指定边界没有发生。搜不到相关代码不够。 |
| 同上 | `possible` | 找到可能路径，但尚不能确认配置是否启用、路径是否到达等。 |

没有 `unknown`、`required` 或 `not_found` 这些枚举值。声明不明时 `rules: []`，没有足够实现证据时 `observations: []`。
每条规则和每条证据都要填非空 `reference`。`reference` 是出处说明或链接；程序不自动打开、验证它。

## 2. 怎样保证在比较同一件事：`target` 和 `edge`

下面五个字段必填，值均为**人工统一的非空文本**，没有固定的合法值列表：

| 字段 | 问题 | 例子 |
| --- | --- | --- |
| `role` | 谁拿到信息？ | `online attacker`、`benchmark designer` |
| `phase` | 在哪个阶段？ | `attack construction`、`evaluation` |
| `source` | 信息从哪里来？ | `victim user query`、`retrieved document` |
| `representation` | 实际拿到什么表示？ | `raw query text`、`slot-deleted query` |
| `operation` | 拿来做什么？ | `construct candidate payload` |

`target` 表示这次要审的信息流。`rules[].edge`、`observations[].edge` 描述各自适用的信息流。
`match_edge()` 要求所有字段完全相同；它不自动理解同义词，不做包含关系推理，大小写和空格也不自动统一。
因此“designer 在离线阶段拿到任务”和“online attacker 拿到未来用户任务”不能直接合并比较。

可选字段 `query_form` 只有两个显式选项：

| 选项 | 含义 |
| --- | --- |
| `full_query` | 完整 query |
| `partial_query` | 不完整 query，如删除一部分槽位但仍保留任务信息 |
| 省略整个字段 | 未指定 query 形态，或该记录未用此维度；不是第三个字符串选项 |

显式 `full_query`、`partial_query` 和省略彼此不匹配。不能填 JSON `null`。
当前不会从 full-query 的规则推导 partial-query 的权限：要判断部分 query 是否违规，必须有适用于该表示的声明及证据。

## 3. 实验范围 `scope` 的四个必填字段

这四个值也是非空自由文本，作用是固定所讨论的实验；**不是启动模型实验的配置参数**。

| 字段 | 填什么 | 为什么要填 |
| --- | --- | --- |
| `paper_version` | 论文版本及有关章节 | 防止把不同版本的声明混用 |
| `experiment_arm` | 实验条件或对照组 | 防止把更强 baseline 当成主条件 |
| `artifact_revision` | 代码 commit、release 或材料快照 | 固定实际核查的实现版本 |
| `configuration` | 与信息流有关的配置、入口、开关 | 防止把未启用的代码路径当成实际发生 |

`scope` 在内部记录上统一声明。程序验证这四个字段非空，但不会自动检查引用的代码是否真的属于所填 commit，或规则证据是否真的属于这个范围；这部分需要整理者核验。

## 4. 内部记录的其他字段

| 字段 | 选项或类型 | 用途 |
| --- | --- | --- |
| `id` | 必填非空字符串；同一批次唯一 | 内部证据记录 ID |
| `description` | 必填非空字符串 | 本条核查问题 |
| `source_group` | `archived` / `paper_text` / `synthetic` | 历史归档材料 / 论文或公开材料整理 / 人工构造的测试记录 |
| `rules` | 规则数组，可为空 | 每条有 `edge`、`permission`、`reference` |
| `observations` | 证据数组，可为空 | 每条有 `edge`、`status`、`reference` |
| `note` | 可选说明 | 背景和限制 |
| `input_provenance_gap` | 可选对象，含非空 `description`、`reference` | 单独记录输入来源不明；不会自动把结论改成不一致 |

`synthetic` 可用于底层单元测试，但核心规则拒绝用它产生真实论文级结论。
`paper_text` 不代表已经做过源码或运行核验，具体依据以 `reference` 为准。

## 5. 内部信息流如何判定

先处理冲突：声明为空、同时有 `allow` 和 `deny`、或证据同时有 `present` 和 `absent`，均为证据不足。
没有上述问题时：

| 声明 | 实现证据 | 结论 |
| --- | --- | --- |
| `deny` | `present` | `inconsistent`：确认发生禁止的信息流 |
| `allow` | `present` | `consistent_within_scope`：该信息流被允许 |
| `allow` 或 `deny` | `absent` | `consistent_within_scope`：未发生该流；`allow` 不强制实际访问 |
| `allow` 或 `deny` | 只有 `possible` | `insufficient_evidence`：可能路径不足以确认 |
| `allow` 或 `deny` | 无匹配证据 | `insufficient_evidence` |

`present + possible` 按已确认的 `present` 处理；`absent + possible` 按已确认的 `absent` 处理。
这些都是已匹配到同一个 `target` 的记录，其他信息流不会参与本条判定。

内部 `reason` 的全部输出值：

| 值 | 解释 |
| --- | --- |
| `policy_unspecified` | 没有匹配声明 |
| `conflicting_policy` | 同一目标有冲突声明 |
| `conflicting_observations` | 同一目标同时确认存在和不存在 |
| `forbidden_flow_confirmed` | 禁止的信息流已确认 |
| `permitted_flow_confirmed` | 允许的信息流已确认 |
| `absence_confirmed_at_boundary` | 边界处已确认不存在 |
| `path_or_configuration_unconfirmed` | 路径或配置尚未确认 |
| `no_matching_observation` | 没有匹配实现证据 |

## 6. 一篇论文如何输出一条结果

论文清单字段：`id`、`title`、`version`、`audit_scope` 为必填非空文本；
`required_checks` 是属于该论文的内部记录 ID 数组；`coverage_complete` 是人工填写的布尔值。

- 至少一条内部记录确认不一致：`has_confirmed_inconsistency: true`，`verdict: inconsistent`。
- 没有确认不一致，列出的记录全部已解决且 `coverage_complete: true`：`false`，`consistent_within_scope`。
- 其他情况：`false`，`insufficient_evidence`。

`coverage_complete` 只表示列明的 **audit_scope 已覆盖**，不表示论文所有实验都已经审完；它不是程序自动评估的置信度。
论文级 `reason` 为 `confirmed_inconsistency_in_scope`、`all_required_checks_consistent`、`unresolved_checks` 或 `audit_scope_not_fully_covered`。

## 7. 运行命令的全部选项

| 命令或选项 | 作用 |
| --- | --- |
| `list [--json]` | 列出内置论文 ID；JSON 中含版本和范围 |
| `audit PAPER [PAPER ...]` | 复核指定论文；可用 `all`；ID 不区分大小写，`-` 可替代 `_` |
| `evaluate PAPER [PAPER ...]` | 生成同样结论，再比较人工标签 |
| `--json` | 终端输出 JSON，默认是每篇一行的表格 |
| `--details` | 在 JSON 中保留内部声明和证据；配合 `--json` 或 `--output` |
| `--output PATH` | 额外保存 JSON；不覆盖已有文件 |
| `--cases FILE [FILE ...]` | 使用自己的内部记录；须同时指定 `--papers` |
| `--papers FILE` | 使用自己的论文清单；须同时指定 `--cases` |
| `--gold FILE` | 仅 `evaluate` 可用；包含清单中全部论文的预期 `verdict` |

所有选项放在子命令后。`--gold` 不包含在审计输入中；新增论文可直接 `audit`，不需要先给答案。
