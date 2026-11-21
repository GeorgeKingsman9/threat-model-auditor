# Notion 的元素建模怎样进入代码

**已经使用，比较规则与自动抽取要分开评价。** 代码仍按此前的声明模型和实现模型比较信息流；模型能否从新论文、配置和源码准确恢复这些元素，是另一项需要真实测试的能力。

## 同一条信息流、同一个范围

\[
e=(\mathrm{role},\mathrm{phase},\mathrm{source},\mathrm{representation},\mathrm{operation}),
\qquad
\sigma=(\mathrm{paper\_version},\mathrm{experiment\_arm},\mathrm{artifact\_revision},\mathrm{configuration}).
\]

| 原建模中的部分 | 程序中的表示与作用 |
| --- | --- |
| 元素/信息流 $e$ | `checker.py` 的 `EDGE_FIELDS`、`match_edge()`；五个维度按固定顺序匹配，显式的 full/partial query 也分别匹配 |
| 固定审计范围 $\sigma$ | `SCOPE_FIELDS` 和每条记录的 `scope`；更换接收角色、阶段、实验分支或版本，不能沿用另一条记录的结论 |
| 声明模型 $\Gamma_{decl}$ | `rules`：论文对该信息流的 `allow/deny`，并附论文原文定位；未声明的权限不能凭空补为 deny |
| 实现模型 $D_{impl}$ | `observations`：该接收者上的 `present/absent/possible`，附源码、配置和交付边界依据 |
| 一致性规则 $R$ | `checker.audit_case()` 调用基础比较与 `scope_review.assess_claim()`；后者核对权限适用性、角色、实例、交付与冲突 |
| 论文级输出 | `checker.summarize_paper()` 汇总内部信息流，`findings.project_result()` 输出一篇一个三值答案及具体位置 |

当前默认`extraction_v6.py`在V5的接收者、实例映射和引用验收上继续实现这条建模路线：先由`declared_contract.py`只读论文、提出声明与任务组成；再从论文及自动取得的源码中建立上述元素，最后独立复核。它没有用人工gold代填字段。

第一阶段的声明仍是未受信任提案，不能直接作为`rules`或证据。后续必须重新引用原论文并建立适用关系。`input_channels.py`把问题、文档等不同输入参数分别列为待核查候选；`data_witnesses.py`提供固定数据文件的有界原文记录。候选、数据字段存在及文件名均不会直接生成`deny/present`。部署来源问题由`deployment_findings.py`单列，未知获取路径不会被当成禁止许可。详见[V6实现说明](AUTOMATIC_V6_ZH.md)。

## 核心比较

在同一 $e,\sigma$ 下，记 $A$ 为权限适用、接收角色与必要实例关系已对齐、引用/路径通过验收且无证据冲突：

\[
A(e,\sigma)\land
\bigl(\Gamma_{decl}\vdash\mathrm{deny}(e)\bigr)\land
\bigl(D_{impl}\models\mathrm{present}(e)\bigr)
\Longrightarrow R(e,\sigma)=\mathrm{inconsistent}.
\]

例如，`partial_query` 进入攻击优化器，不会因变量名是 training 就自动获得许可；但评估器收到 query 也不能直接证明攻击者收到 query。必须比较相应角色、来源、表示、用途及范围。

论文级：任一信息流有确认的不一致，就输出 `true`；全部**所列怀疑**有反证且证明义务闭合，才输出范围内 `false`；其他情况输出 `null`。范围内 false 不认证整篇所有行为。

## 现在还没有形式证明什么

`match_edge()` 比较的是已经归一化后的结构，不会自行理解两段不同自然语言是否同义。当前由模型提出归一化和跨文件路径，独立复核与确定性程序验收引用、结构及状态。它不是自动证明任意程序语义的静态分析器；分阶段模型调用仍可能共同误读或漏提候选信息流。

静态范围可以明确写成“当评估选择该生成数据并进入某分支时”。此时可用源码中的同一记录、稳定 ID、序列化/加载和索引变换证明条件下的身份关系，不必冒充已经知道作者历史上用了哪份文件。历史运行、真实/合成数据来源和效果差异仍各需自己的证据。
