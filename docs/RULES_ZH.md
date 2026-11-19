# 判定规则与源码证据验收说明书

当前核心业务判定有 **30 条**：基础边判定 8 条、V3 范围与反证新增 19 条、论文汇总 3 条。论文加源码路径另外有 **15 条证据验收规则（SRC）**。还有 **10 项自动抽取 V3 验收/分流条件（X）**与 **11 组结构校验（V）**。这些数量分别统计，不把状态值、模型步骤或测试数加进核心规则数。

本说明由 `rule_catalog.py` 的 `catalog()` 生成。它描述现有程序，自己不作裁定、不调用模型，也不读取 gold。可用 `python rule_catalog.py` 导出 JSON，用 `python rule_catalog.py --format markdown` 重建本文件。

## 计数和执行顺序

- 核心业务规则只数 B/S/P 清单条目，同一语义检查在多个位置复用不重复计数。
- B02/B03 也出现在 scope_review 中，S04/S06 各有两个落点。
- P03 是一个汇总弃判规则，按是否存在未决检查产生两种 reason code。
- X 是自动抽取验收/分流条件分组，V 是输入校验分组，均单列而不加入核心规则总数。
- SRC 是论文加源码路径的证据验收规则，按职责归并后单列，不按每个 if 或每个状态值计数。
- citation-only repair 是失败引文的候选修复步骤，最终仍满足原有引用标准，不新增核心规则或 SRC 验收规则。
- 状态值、模型提示中的工作步骤、测试数量和 golden 标签均不算业务规则。

基础层先执行 B01–B08。同一层按优先序检查，先满足者返回。V3 再按 scope 优先序复核基础结果，最后按 P01–P03 汇总 required_checks。优先序是代码位置，不是严重程度。所有例子均假定更早的门已通过。

role/phase/source/representation/operation 及可选 query_form 全部精确相同才连接权限与观察，不用模糊匹配。 每个 case 的版本、实验臂、修订和配置需明确填写。程序不会仅凭这些非空字符串独立核实引用是否真的属于该范围。完整查询禁令也不会自动变成部分查询禁令。

`conflicting_policy` 与 `conflicting_observations` 在两层共用 B02/B03。S04 与 S06 虽有重复落点，各只算一条。P03 的两种 reason code 都表达同一个未闭合范围的汇总规则。按 reason 字符串机械相加会得到另一数量，因此本清单按去重后的判定条件计数。

输出对应关系为 confirmed → inconsistent、refuted → consistent_within_scope、unresolved → insufficient_evidence。V2 只保留旧基础结果并标记 legacy_v2，不能当作已通过 V3 证据门。

**范围限制：**consistent_within_scope 只排除 required_checks 中明确列出的怀疑。它不认证整篇论文、全部实现或全部历史运行。结构错误直接拒绝输入，证据不足才产生 insufficient_evidence。行为影响是独立元数据，ASR 不显著不能消除已证明的禁止输入交付。

## 核心业务规则

### 基础边判定（8 条）

#### B01

- 触发条件：没有与目标边精确匹配的权限记录。
- 结果：insufficient_evidence。原因码：`policy_unspecified`。
- 优先序：base 1。函数：`checker.decide`。
- 正例：permissions 为空，不能从论文沉默推出 deny。
- 不触发例：存在匹配的 deny。

#### B02

- 触发条件：同一目标边同时匹配 allow 和 deny。
- 结果：insufficient_evidence / unresolved。原因码：`conflicting_policy`。
- 优先序：base 2; scope 2。函数：`checker.decide, scope_review.assess_claim`。
- 正例：同一范围内两条权限记录互相冲突。
- 不触发例：只有一条匹配的 allow。

#### B03

- 触发条件：同一目标边同时观察到 present 和 absent。
- 结果：insufficient_evidence / unresolved。原因码：`conflicting_observations`。
- 优先序：base 3; scope 3。函数：`checker.decide, scope_review.assess_claim`。
- 正例：同一配置既声明输入含目标信息，又声明该输入排除了它。
- 不触发例：present 与 possible 并存不构成此冲突。

#### B04

- 触发条件：匹配权限为 deny，匹配观察包含 present。
- 结果：inconsistent（V3 仍须经过范围门）。原因码：`forbidden_flow_confirmed`。
- 优先序：base 4。函数：`checker.decide`。
- 正例：禁止的同一信息边被观察到。
- 不触发例：只有 possible，不能确认实际交付。

#### B05

- 触发条件：匹配权限为 allow，匹配观察包含 present。
- 结果：consistent_within_scope（V3 仍须经过反证门）。原因码：`permitted_flow_confirmed`。
- 优先序：base 5。函数：`checker.decide`。
- 正例：明确允许的输入实际收到该信息。
- 不触发例：allow 没有相应观察，不自动产生一致结论。

#### B06

- 触发条件：匹配观察含 absent 且不含 present，权限没有冲突。
- 结果：consistent_within_scope（基础边判定）。原因码：`absence_confirmed_at_boundary`。
- 优先序：base 6。函数：`checker.decide`。
- 正例：肯定性的输入边界证据表明目标信息未到达。
- 不触发例：搜索时未找到相关代码不能标 absent。

#### B07

- 触发条件：没有 present 或 absent，只有可能路径 possible。
- 结果：insufficient_evidence。原因码：`path_or_configuration_unconfirmed`。
- 优先序：base 7。函数：`checker.decide`。
- 正例：代码存在可选读取路径，但目标配置是否启用未核实。
- 不触发例：有匹配的 present 时优先适用 B04/B05。

#### B08

- 触发条件：存在单一匹配权限，但没有匹配观察。
- 结果：insufficient_evidence。原因码：`no_matching_observation`。
- 优先序：base 8。函数：`checker.decide`。
- 正例：观察记录属于另一角色、阶段或 query_form。
- 不触发例：相同目标边已有 absent。

### V3 范围与反证（19 条）

#### S01

- 触发条件：target 标注 full_query/partial_query，但 information_level 未对应 exact_query/partial_query。
- 结果：insufficient_evidence / unresolved。原因码：`query_form_information_level_conflict`。
- 优先序：scope 1。函数：`scope_review.assess_claim`。
- 正例：target 为 full_query，assessment 却称 partial_query。
- 不触发例：full_query 对应 exact_query。

#### S02

- 触发条件：delivery 为 excluded 或 evaluator_only，但匹配观察含 present。
- 结果：insufficient_evidence / unresolved。原因码：`delivery_exclusion_conflicts_with_present`。
- 优先序：scope 4。函数：`scope_review.assess_claim`。
- 正例：同一边一处称仅评分器可见，另一处称构造输入已收到。
- 不触发例：仅评分器可见，且没有匹配 present。

#### S03

- 触发条件：delivery 为 confirmed，但匹配观察含 absent。
- 结果：insufficient_evidence / unresolved。原因码：`delivery_confirmation_conflicts_with_absent`。
- 优先序：scope 5。函数：`scope_review.assess_claim`。
- 正例：结构化交付标为确认，却有同边 absent。
- 不触发例：confirmed 与 present 相符。

#### S04

- 触发条件：policy.status 已确定为 applicable/not_applicable，但没有非空范围引用。
- 结果：insufficient_evidence / unresolved。原因码：`policy_scope_evidence_missing`。
- 优先序：scope 6,18。函数：`scope_review.assess_claim`。
- 正例：声称禁令适用此阶段，却未提供范围证据引用。
- 不触发例：uncertain 不要求确定范围的引用，但不能确认违规。

#### S05

- 触发条件：delivery 不为 unresolved，却没有非空交付边界引用。
- 结果：insufficient_evidence / unresolved。原因码：`delivery_boundary_evidence_missing`。
- 优先序：scope 7。函数：`scope_review.assess_claim`。
- 正例：标 confirmed，但 delivery.reference 为空。
- 不触发例：confirmed 具有输入边界证据引用。

#### S06

- 触发条件：已确定的 delivery 仅有非边界证据，或进入确认路径后仍未建立 confirmed 的实际输入交付。
- 结果：insufficient_evidence / unresolved。原因码：`delivery_to_input_boundary_not_established`。
- 优先序：scope 8,21。函数：`scope_review.assess_claim`。
- 正例：只有 document_presence/possible_path，或 delivery 仍 unresolved。
- 不触发例：有引用的 static_bound_path 确认目标输入实际接收信息。

#### S07

- 触发条件：refutation.basis 不为 none，但没有非空反证引用。
- 结果：insufficient_evidence / unresolved。原因码：`refutation_evidence_missing`。
- 优先序：scope 9。函数：`scope_review.assess_claim`。
- 正例：声称明确授权可排除怀疑，但未引用授权依据。
- 不触发例：有具体授权反证引用。

#### S08

- 触发条件：反证为 explicit_permission，匹配权限仅 allow，观察含 present，政策为适用的 attacker_knowledge_constraint，且引用与 confirmed 边界交付齐备。
- 结果：consistent_within_scope / refuted。原因码：`claim_refuted_explicit_permission`。
- 优先序：scope 10。函数：`scope_review.assess_claim`。
- 正例：该实验臂明确允许构造输入使用任务，且证明确实收到任务。
- 不触发例：只写 stronger baseline，尚未核实其信息授权，不足以触发。

#### S09

- 触发条件：反证为 different_instance，信息属于 training_instance/topic_only/different_instance，交付有边界引用且不为 unresolved，无匹配 present，政策有据为 not_applicable。
- 结果：consistent_within_scope / refuted。原因码：`claim_refuted_different_instance`。
- 优先序：scope 11。函数：`scope_review.assess_claim`。
- 正例：证据证明收到的是另一训练实例，目标评测实例禁令不适用。
- 不触发例：只因数据集名称相同就断言实例不同或相同。

#### S10

- 触发条件：反证为 excluded_delivery，delivery 为 excluded/evaluator_only，边界引用齐备，且没有匹配 present。
- 结果：consistent_within_scope / refuted。原因码：`claim_refuted_excluded_delivery`。
- 优先序：scope 12。函数：`scope_review.assess_claim`。
- 正例：肯定性边界证据证明任务只到评分器，没有到被怀疑的构造输入。
- 不触发例：没有找到输入日志，不能当作交付排除证据。

#### S11

- 触发条件：反证为 different_issue_type，issue_type 不是 information_boundary，policy_kind 为 victim_security_goal/protocol_requirement，并有反证引用。
- 结果：consistent_within_scope / refuted（仅排除本类怀疑）。原因码：`claim_refuted_different_issue_type`。
- 优先序：scope 13。函数：`scope_review.assess_claim`。
- 正例：已证明讨论的是受害系统安全目标被攻破，而非论文违反攻击者知识约束。
- 不触发例：只是把 issue_type 改名，政策仍是攻击者知识限制。

#### S12

- 触发条件：提供了反证 basis，但该类反证的必要条件未满足。
- 结果：insufficient_evidence / unresolved。原因码：`refutation_not_supported_by_scoped_evidence`。
- 优先序：scope 14。函数：`scope_review.assess_claim`。
- 正例：explicit_permission 反证只有 allow，没有匹配 present。
- 不触发例：授权、适用范围与实际交付同时满足 S08。

#### S13

- 触发条件：没有成立的反证，且 issue_type 不是 information_boundary。
- 结果：insufficient_evidence / unresolved。原因码：`information_boundary_issue_not_established`。
- 优先序：scope 15。函数：`scope_review.assess_claim`。
- 正例：仅有实验协议或任务完整性争议，尚未建立信息边界问题。
- 不触发例：明确的 information_boundary 怀疑继续后续范围检查。

#### S14

- 触发条件：进入确认路径，但 policy_kind 不是 attacker_knowledge_constraint。
- 结果：insufficient_evidence / unresolved。原因码：`policy_is_not_attacker_knowledge_constraint`。
- 优先序：scope 16。函数：`scope_review.assess_claim`。
- 正例：把受害系统不应泄露信息的安全目标当成攻击者不可知信息的限制。
- 不触发例：政策确实约束攻击者能知道什么。

#### S15

- 触发条件：进入确认路径，但 policy.status 不为 applicable。
- 结果：insufficient_evidence / unresolved。原因码：`policy_scope_not_established`。
- 优先序：scope 17。函数：`scope_review.assess_claim`。
- 正例：禁令是否适用于离线构造角色仍 uncertain。
- 不触发例：原文明确限制同一角色、阶段和实验臂。

#### S16

- 触发条件：进入确认路径，但 task_relation 为 different_instance 或 unknown。
- 结果：insufficient_evidence / unresolved。原因码：`evaluated_instance_alignment_not_established`。
- 优先序：scope 19。函数：`scope_review.assess_claim`。
- 正例：知道查询来自某基准，但尚不能对齐被评测的那条实例。
- 不触发例：有同一评测实例的边界证据。

#### S17

- 触发条件：task_relation 为 topic_only，却把 information_level 标成 exact_query/partial_query。
- 结果：insufficient_evidence / unresolved。原因码：`topic_information_is_not_instance_query`。
- 优先序：scope 20。函数：`scope_review.assess_claim`。
- 正例：仅给主题标签，却声称收到该实例的完整或部分查询。
- 不触发例：只就 task_category 这一信息层级提出怀疑。

#### S18

- 触发条件：前述范围门全部通过，基础 verdict 为 inconsistent，匹配权限仅 deny，观察含 present。
- 结果：inconsistent / confirmed。原因码：`scoped_forbidden_delivery_confirmed`。
- 优先序：scope 22。函数：`scope_review.assess_claim`。
- 正例：适用禁令、同一信息对象、实际构造输入交付三者形成同范围证据。
- 不触发例：只有攻击成功或 ASR 差异，却没有证明禁止信息到达目标输入。

#### S19

- 触发条件：范围门通过，但基础层没有确认被禁止的交付，且无成立反证。
- 结果：insufficient_evidence / unresolved。原因码：`base_rule_does_not_confirm_forbidden_delivery`。
- 优先序：scope 23。函数：`scope_review.assess_claim`。
- 正例：allow+present 未提供 explicit_permission 反证，V3 不自动排除怀疑。
- 不触发例：deny+present 且所有范围门通过，适用 S18。

### 论文汇总（3 条）

#### P01

- 触发条件：该论文 required_checks 中至少一条为 inconsistent。
- 结果：inconsistent。原因码：`confirmed_inconsistency_in_scope`。
- 优先序：paper 1。函数：`checker.summarize_paper`。
- 正例：一个必要检查已确认不一致，另一个仍不足，也保留这项发现。
- 不触发例：不在 required_checks 中的发现不能决定本论文范围的结果。

#### P02

- 触发条件：没有确认不一致，required_checks 非空，coverage_complete 为 true，且没有缺失或 insufficient_evidence 的必要检查。
- 结果：consistent_within_scope。原因码：`all_required_checks_consistent`。
- 优先序：paper 2。函数：`checker.summarize_paper`。
- 正例：所有明确列出的怀疑都已被同范围反证排除。
- 不触发例：空检查列表不能认证整篇论文一致。

#### P03

- 触发条件：既不满足 P01，也不满足 P02。
- 结果：insufficient_evidence。原因码：`unresolved_checks`, `audit_scope_not_fully_covered`。
- 优先序：paper 3。函数：`checker.summarize_paper`。
- 正例：缺失/不足的必要检查用 unresolved_checks，否则覆盖未闭合用 audit_scope_not_fully_covered。
- 不触发例：有确认发现时由 P01 优先决定论文结果。

## 自动抽取 V3 的验收与域分流

以下 10 项是自动输入进入核心规则前的条件分组，单列统计。X01–X04 直接决定域分流，X05–X09 限制可接纳证据，X10 准备覆盖标记。X05/X07/X08 的代码写入 citation_errors，其余部分条件没有专用 reason code。它们不是新增的人工审定业务规则。

#### X01

- 触发条件：抽取与复核同意域外、文档完整，但提议仍含 flows。
- 结果：insufficient_evidence。原因码：`out_of_scope_proposal_contains_claims`。
- 优先序：extraction_v3 1。函数：`extraction_v3.decide_extraction`。
- 正例：域外声明同时提出一个信息流怀疑。
- 不触发例：域外且 flows 为空，继续检查域外引用。

#### X02

- 触发条件：完整域外文档无 flows，但适用性引用无法精确定位。
- 结果：insufficient_evidence。原因码：`applicability_citation_unverified`。
- 优先序：extraction_v3 2。函数：`extraction_v3.decide_extraction`。
- 正例：引用的主题短语不在指定片段。
- 不触发例：唯一匹配的主题引用可以定位。

#### X03

- 触发条件：抽取与复核同意域外，文档完整、无 flows，适用性引用已定位。
- 结果：not_applicable，单独的域外结果。原因码：`reviewed_out_of_domain`。
- 优先序：extraction_v3 3。函数：`extraction_v3.decide_extraction`。
- 正例：与 IPI 无关的论文经过完整文档和主题引用检查。
- 不触发例：域外结果不是 consistent_within_scope，也不进入论文一致率分母。

#### X04

- 触发条件：适用性复核不支持、双方分类不同，或尚不能进入 in_scope 分支。
- 结果：insufficient_evidence。原因码：`applicability_uncertain_or_disputed`。
- 优先序：extraction_v3 4。函数：`extraction_v3.decide_extraction`。
- 正例：抽取称 in_scope，复核称 uncertain。
- 不触发例：双方同意 in_scope，继续逐项检查。

#### X05

- 触发条件：某 flow 复核不支持，或 policy_kind/status、delivery、refutation 任一轴与提议不一致。
- 结果：记录复核分歧，降为 uncertain/unresolved/none，不接纳该项权限或观察。原因码：`semantic_review_disagrees_with_proposed_assessment`。
- 优先序：extraction_v3 5。函数：`extraction_v3.decide_extraction`。
- 正例：复核认为禁令适用性 uncertain，提议却标 applicable。
- 不触发例：复核支持且四轴一致仍需引用检查。

#### X06

- 触发条件：政策范围、交付、反证或非 unspecified 权限/观察的引用无法通过 locate。
- 结果：对应引用保持空或记录不入库，并记录 citation_errors，随后由核心规则裁定。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：extraction_v3 6。函数：`extraction_v3.decide_extraction, extraction_v3.locate`。
- 正例：引文不存在、过长或在同一视图中多处匹配，不能成为肯定证据。
- 不触发例：短引文在同 PDF 的指定文本视图唯一精确匹配。

#### X07

- 触发条件：implementation 与 declaration 的引用定位区间重叠。
- 结果：清除观察，delivery 降为 unresolved 并清空引用。原因码：`policy_sentence_cannot_establish_implementation`。
- 优先序：extraction_v3 7。函数：`extraction_v3.decide_extraction`。
- 正例：用同一句禁止访问声明，同时证明实现没有访问。
- 不触发例：独立的程序描述与政策引文不重叠。

#### X08

- 触发条件：非 unresolved 的 delivery 与 declaration 的引用定位区间重叠。
- 结果：delivery 降为 unresolved 并清空引用。原因码：`policy_sentence_cannot_establish_delivery_boundary`。
- 优先序：extraction_v3 8。函数：`extraction_v3.decide_extraction`。
- 正例：用禁令原句本身证明信息确实未到构造输入。
- 不触发例：有另一处独立输入边界描述。

#### X09

- 触发条件：delivery 为 unresolved，而反证依赖 explicit_permission/different_instance/excluded_delivery。
- 结果：清除这三类依赖交付的反证 basis，随后执行核心判定。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：extraction_v3 9。函数：`extraction_v3.decide_extraction`。
- 正例：交付引用失败后，不能保留依赖该交付的明确授权反证。
- 不触发例：different_issue_type 不在此清除范围。

#### X10

- 触发条件：仅当 flows 非空、复核完成列明范围、无具体未决问题、文档覆盖完整时设置 coverage_complete。
- 结果：生成有限范围论文输入，交给 P01–P03，不新增一致标签。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：extraction_v3 10。函数：`extraction_v3.decide_extraction`。
- 正例：仍有未决问题时 coverage_complete=false，即使部分怀疑已排除。
- 不触发例：已有确认发现仍由 P01 保留，不被覆盖不足抹去。

## 论文加源码的证据验收规则

以下 15 条 SRC 规则描述当前 `source_bundle.py` 与 `extraction_v4.py`，不加入 30 条核心业务规则。其优先序是阅读/处理阶段，不表示函数内部所有条件都按这一张清单串行执行。源码快照一致性与引文落点由代码检查，授权含义、共同合同是否覆盖此角色、引用能否支持实际调用关系仍须独立语义复核。合法枚举、连上的符号名或非空引文不能独自证明这些语义。

SRC 中列出的代码验收错误通常出现在 source_validation.validation_errors，读取/结构错误会直接拒绝输入。它们不等同于论文结论的 reason。

#### SRC01

- 触发条件：源码必须有可核实的冻结身份。本地 Git 读取解析后的提交对象，GitHub 使用完整提交 SHA，普通目录只能用 content-manifest 身份。
- 结果：缺少或混用身份则拒绝快照，不把目录当前内容假称指定提交。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 1。函数：`source_bundle.load_repository, source_bundle._git_snapshot, source_bundle._github_url, source_bundle.validate_repository`。
- 正例：普通目录只有内容 manifest，不能附会一个未验证的 Git revision。
- 不触发例：已核实的 Git 提交和对应清单可以进入后续验收。

#### SRC02

- 触发条件：源码文本、字节数、文件 SHA、整文件行号/片段 ID、Git blob（如有）、inventory 与 manifest 必须自洽。
- 结果：篡改、缺段、重复或摘要不符则拒绝，完整重算的伪造快照仍须靠外部归档绑定鉴别。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 2。函数：`source_bundle.validate_repository, extraction_v4.combine_inputs`。
- 正例：缓存文本改了一个字符却保留旧 SHA，应被拒绝。
- 不触发例：原始快照所有摘要一致，只证明内部一致，不自动认证来源真实。

#### SRC03

- 触发条件：源码只作为受限静态数据读取。路径、符号/硬链接、特殊文件、敏感/标签内容、字节数、文件数、展开量与时间均受读取器约束。
- 结果：危险或超限输入拒绝或明确列为 excluded/omitted，execution 必须为 none。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 3。函数：`source_bundle._safe_path, source_bundle._excluded_reason, source_bundle._git, source_bundle._directory_snapshot, source_bundle._download_archive, source_bundle._archive_snapshot, source_bundle.load_repository, source_bundle.validate_repository`。
- 正例：归档路径逃逸或来源文件在读取中改变，不能静默接纳。
- 不触发例：普通合格 UTF-8 源文件可整文件读取，不执行其脚本或安装依赖。

#### SRC04

- 触发条件：输入摘要须覆盖 paper SHA、repository manifest/revision、实际有序选入片段、论文阅读视图以及送模型的元数据。抽取和复核的 input_binding 都必须等于这次完整输入。
- 结果：选文件预算、阅读视图、元数据或版本变化则拒绝复用模型输出，保留 paper/code 引用域与各自来源身份。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 4。函数：`extraction_v4.combine_inputs, extraction_v4.model_content, extraction_v4.validate_input_binding, extraction_v4.decide_extraction`。
- 正例：提交不变但选入源码集合改变，不能继续重放旧 input_binding。
- 不触发例：同一冻结 paper+source 及完全相同模型输入的输出可以接受绑定检查。

#### SRC05

- 触发条件：V4 抽取/复核须符合各自严格 schema，每次最多六条源码怀疑，复核索引恰好覆盖每条一次。
- 结果：结构错误或漏复核直接拒绝，不产生证据不足研究标签。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 5。函数：`extraction_v4.decide_extraction, extraction.validate_shape`。
- 正例：索引 0 被复核两次而索引 1 漏掉，应拒绝。
- 不触发例：两个 flow 各有唯一且完整的复核项。

#### SRC06

- 触发条件：非 unspecified 权限声明以及政策适用性/共同规则/具体例外的引文必须定位到 paper 域，不能只引用代码注释。失败引文可进入一次有预算的候选修复，但最终标准仍是精确 _locate。
- 结果：政策引用不合域或修复后仍不能定位时不接纳该权限，policy 降为 uncertain。原因码：`declaration_source`, `scope_resolution_citation`。
- 优先序：source_validation 6。函数：`extraction_v4._locate, extraction_v4._scope_check, extraction_v4.decide_extraction, citation_repair.citation_issues, citation_repair.repair_request, citation_repair.choice_request, citation_repair.apply_choices, citation_repair.apply_repairs`。
- 正例：代码注释称允许读取任务，不足以替代论文中的知识授权。
- 不触发例：具体实验臂的论文授权短引可被定位。

#### SRC07

- 触发条件：必须解决共同知识合同与具体规则的关系。common_contract 需要共同规则引文，knowledge/diagnostic/unknown 的 override 不能仍按未变的 common_contract 接纳，specific_rule 需要具体规则引文。
- 结果：unresolved 或冲突降为政策不足，明确知识授权/诊断范围由独立语义复核确认。原因码：`scope_resolution_unresolved`, `common_contract_conflicts_with_specific_scope`, `scope_resolution_citation`。
- 优先序：source_validation 7。函数：`extraction_v4._scope_check, extraction_v4.decide_extraction`。
- 正例：只放宽投递通道的 stronger baseline 不自动豁免共同知识约束。
- 不触发例：论文明确给出知识授权或 diagnostic 限定，按其具体范围复核。

#### SRC08

- 触发条件：code_path 每一步及 implementation/delivery 的引文须精确定位到 code 域，附文件路径、行号、文件 SHA、提交与 manifest 身份。候选修复只能替换失败引文，已知原文件的代码引文不得换文件，不改变源码链结构。
- 结果：最终仍无法精确定位的引文使路径验收失败，词汇相似候选本身不算证据。原因码：`source_path_citation`, `source_boundary_citation`。
- 优先序：source_validation 8。函数：`extraction_v4._locate, extraction_v4._path_check, citation_repair.citation_issues, citation_repair.repair_request, citation_repair.choice_request, citation_repair.apply_choices, citation_repair.apply_repairs`。
- 正例：候选窗口词汇相似，但不能定位或不支持该绑定，不能接纳为证据。
- 不触发例：提供的冻结代码行含对应绑定，可唯一精确定位且通过新的独立复核。

#### SRC09

- 触发条件：code_path 长度为 2–16 步，每步输入/输出符号非空，相邻步骤的 output_symbol 与下一步 input_symbol 完全相等。
- 结果：断链、空符号或长度越界则不接纳 confirmed 代码交付。原因码：`source_path_requires_two_to_sixteen_steps`, `source_path_empty_symbol`, `source_path_disconnected`。
- 优先序：source_validation 9。函数：`extraction_v4._path_check`。
- 正例：构造输出 A，下一步却从无连接证据的 B 读取。
- 不触发例：相邻符号与实际引用均支持连续链。

#### SRC10

- 触发条件：路径至少包含 request 和 delivery，首次 request 不晚于最后一次 delivery，experiment_arm 不得为空或 unresolved/unknown 等占位值。
- 结果：缺少接收端、次序异常或未解析实验臂则路径不足。原因码：`source_path_requires_request_and_delivery`, `source_path_delivery_precedes_request`, `source_path_experiment_arm_missing`。
- 优先序：source_validation 10。函数：`extraction_v4._path_check`。
- 正例：只有数据字段与模板，却没有请求输入或被评测分支的投递绑定。
- 不触发例：请求和后续分支投递都有代码引文并标明同一实验臂。

#### SRC11

- 触发条件：静态源码路径的 delivery.evidence_kind 必须为 static_bound_path。
- 结果：runtime/saved_request 等标注不能由源码快照证明，应使路径验收失败。原因码：`source_snapshot_cannot_establish_runtime`。
- 优先序：source_validation 11。函数：`extraction_v4._path_check`。
- 正例：已发布代码存在该链，不等于证明作者历史请求实际这样运行。
- 不触发例：结论只指提供的静态修订与绑定分支。

#### SRC12

- 触发条件：政策轴须同时通过 declaration_supported、scope_resolution_supported、范围验收及 policy_kind/status 一致性检查。
- 结果：政策失败时只清除该权限并降为 uncertain，不因此抹去独立成立的源码交付。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 12。函数：`extraction_v4.decide_extraction`。
- 正例：共同知识约束是否适用有争议，仍保存已经通过源码链复核的部分查询交付事实。
- 不触发例：引用真实但复核不支持其权限含义，不能确认 deny 适用。

#### SRC13

- 触发条件：交付轴须同时通过 implementation_supported、code_path_supported、路径验收及 delivery 枚举一致性检查，与政策轴独立。
- 结果：交付失败则降为 unresolved，present/absent 降为 possible，政策可保留。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 13。函数：`extraction_v4.decide_extraction`。
- 正例：模型找到了禁令，但请求到评测分支链没有闭合，只能保留可能路径。
- 不触发例：政策 disputed 但代码链与交付轴通过，交付事实仍可保留。

#### SRC14

- 触发条件：反证轴必须与复核 basis 一致，通常还须政策轴通过，excluded_delivery 可独立保留。之后继续经过 V3 引文/交付门和 S08–S12 必要条件。
- 结果：不支持的反证改为 none，不因总体 supported 一票决定所有证据轴。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 14。函数：`extraction_v4.decide_extraction, extraction_v3.decide_extraction, scope_review.assess_claim`。
- 正例：政策语义未支持时，不保留依赖该授权的 explicit_permission 反证。
- 不触发例：有独立交付排除证据可继续验收 excluded_delivery，而不是自动宣称全篇一致。

#### SRC15

- 触发条件：合并 coverage.complete 需要 paper 与源码各自完整。源码完整仅指全部合格文件已供应，不能覆盖被排除的内容。存在 omitted 源文件时不得以有限片段认证负面不存在。
- 结果：有限证据仍可支持已闭合的正面发现，但不足覆盖不能触发 P02。原因码：无专用 reason code，处理方式见本条结果。
- 优先序：source_validation 15。函数：`source_bundle.load_repository, source_bundle.validate_repository, extraction_v4.combine_inputs, extraction_v3.decide_extraction, checker.summarize_paper`。
- 正例：部分源码包含一条确认禁止输入链，可以记录发现，不能据此排除其余分支。
- 不触发例：合格文件完整仍只对列明的怀疑/分支作有限范围结果。

## 输入结构校验

以下按接口职责归为校验组，不把一个字段、一个枚举值或一次 raise 算成一条业务规则。

- **V01** `checker.audit_case, checker.required_text`：案例 id/description/source_group、四项 scope 为非空文本，source_group 属于允许集合。 失败处理：拒绝输入，不生成论文结论。
- **V02** `checker.match_edge, checker.matching_records`：每条边精确包含五个必填字段及可选 query_form，字段为非空文本，权限/观察取值有效且引用非空。 失败处理：拒绝无效记录，非目标边的有效记录不参与该目标判定。
- **V03** `scope_review.assess_claim`：schema_version 必须为整数 2/3，基础 verdict 有效且 reason 非空。 失败处理：ValueError，不能把结构损坏记为证据不足。
- **V04** `scope_review._validate_assessment`：V3 claim 非空，issue_type 有效，assessment 及三个子对象字段精确齐全，所有枚举有效，reason 非空，reference 为字符串。 失败处理：ValueError，引用可为空但肯定判定须再过范围门。
- **V05** `scope_review.assess_claim`：V3 permissions/observations 为 set/frozenset，内容只能取允许值。 失败处理：ValueError，不执行范围裁定。
- **V06** `checker.run_pilot`：cases 为非空数组，案例 ID 唯一。 失败处理：拒绝整批输入。
- **V07** `checker.summarize_paper`：论文身份与范围文本非空，coverage_complete 为布尔值，required_checks 为不重复的非空字符串 ID 列表，不允许 synthetic 案例决定真实论文。 失败处理：拒绝非法论文输入。列表本身允许为空，但不能触发 P02。
- **V08** `checker.run_paper_pilot`：papers 为非空数组，一个 paper ID 只选一个版本/范围，一个检查不分配给多篇论文。 失败处理：拒绝有歧义的批次。
- **V09** `checker.run_pilot, checker.run_paper_pilot`：可选 gold 为对象、ID 集合完全一致、标签有效，只在裁定后比对。 失败处理：拒绝无效 gold。有效 gold 不参与生成 verdict。
- **V10** `extraction.validate_shape, extraction_v3.decide_extraction`：自动抽取与复核输出严格符合各自 schema，每次最多六条怀疑，复核索引恰好覆盖每条一次。 失败处理：ValueError，不把不合格式的模型输出当研究结论。
- **V11** `extraction_v3.locate, extraction_v3.normalized_with_offsets, extraction_v3.overlapping_locators`：引文非空且不超过 300 字符，指定片段存在，仅进行 Unicode NFKD/空白规范化后的唯一精确匹配，优先同页 reading_order_text 再 primary。同页跨文本视图无法证明独立，按重叠处理。 失败处理：引用失败进入 X02/X06。同一文档 SHA 与具体文本视图 SHA 记入定位结果，不能靠编辑距离或语义近似补齐。

## 状态取值（不是规则）

例如 deny 是权限值，applicable 是适用性值，confirmed 是交付值。单有任一取值都不能确认论文不一致。只有条件组合满足相应规则才产生结果。

| 字段 | 允许值 |
| --- | --- |
| `permission` | `allow`, `deny` |
| `observation` | `present`, `absent`, `possible` |
| `verdict` | `inconsistent`, `consistent_within_scope`, `insufficient_evidence` |
| `claim_result` | `confirmed`, `refuted`, `unresolved` |
| `source_group` | `archived`, `paper_text`, `synthetic` |
| `curated_case.schema_version` | `2`, `3` |
| `query_form` | `full_query`, `partial_query` |
| `issue_type` | `information_boundary`, `experimental_protocol`, `task_integrity`, `acquisition_gap`, `security_outcome` |
| `information_level` | `exact_query`, `partial_query`, `task_category`, `document_content`, `runtime_trace`, `user_identity`, `resource_metadata`, `other` |
| `policy_kind` | `attacker_knowledge_constraint`, `victim_security_goal`, `protocol_requirement`, `unspecified` |
| `policy_application.status` | `applicable`, `not_applicable`, `uncertain` |
| `delivery.status` | `confirmed`, `excluded`, `evaluator_only`, `unresolved` |
| `delivery.evidence_kind` | `paper_procedure`, `static_bound_path`, `saved_request`, `runtime`, `document_presence`, `possible_path`, `not_applicable` |
| `delivery.task_relation` | `same_evaluated_instance`, `training_instance`, `topic_only`, `different_instance`, `unknown` |
| `refutation.basis` | `none`, `explicit_permission`, `different_instance`, `excluded_delivery`, `different_issue_type` |
| `validation_mode` | `legacy_v2`, `scope_review_v3` |
| `extraction_v3.applicability` | `in_scope`, `out_of_scope`, `uncertain` |
| `extraction_v3.permission` | `allow`, `deny`, `unspecified` |
| `extraction_v3.observation` | `present`, `absent`, `possible`, `unspecified` |
| `extraction_v3.query_form` | `full_query`, `partial_query`, `unspecified` |
| `extraction_v3.domain_verdict` | `not_applicable` |
| `extraction_v4.scope_resolution.basis` | `common_contract`, `specific_rule`, `unresolved` |
| `extraction_v4.schema_version` | `4` |
| `extraction_v4.scope_resolution.override_dimension` | `none`, `knowledge`, `delivery`, `diagnostic`, `unknown` |
| `extraction_v4.code_path.kind` | `source`, `transform`, `request`, `artifact_write`, `artifact_read`, `delivery` |
| `source.revision_kind` | `git_commit`, `content_manifest` |

## 人工审定输入与自动抽取的差别

人工 curation 由审计者阅读指定版本、代码修订和归档证据，决定 claim、权限适用范围、实际输入边界和反证，再填写结构化记录。核心 checker 只验证结构与字段间的一致性。它不会因为 reference 非空就独立证明引用语义正确，也不会重新打开引用中的网页或代码。人工标错权限轴或实例范围，仍可能得到错误结果。

自动 extraction_v3 先由模型提出记录，再由模型复核，最后接受确定性的结构、引文定位与重叠检查。引文真实且复核同意仍不能保证语义正确，模型也可能遗漏怀疑。输出标为 model_reviewed_not_human_verified，证据范围仅限提供的文档。它不能把论文中的方法说明提升为历史请求或运行证据。

自动 extraction_v4 增加冻结源码和 SRC 验收，并分别复核政策、实际交付、范围解释与源码链。政策有争议时，已经独立建立的交付事实应保留。输出标为 source_aware_model_reviewed_not_human_verified，仍是提供的 paper+source 的静态审查，不证明历史运行、ASR 因果影响或所有通道均已覆盖。

V4 的 citation-only repair 只在有预算时对定位失败的引文做一次有界候选修复。每个请求最多处理 24 处 issue。词汇相似度只用来寻找候选窗口，不是证据，也不进入最终匹配判据。程序先验证候选引用精确且唯一，模型只选候选编号或 null，不自由生成新的引文。只能改 failed-citation 清单中的引文指针，不能改 claim、permission、政策状态、信息层级、实验臂或 code_path 结构。修复后的提议必须重新经过独立复核，最终引文仍由 exact _locate 验收，失败则继续弃判。这是工作步骤改进，不新增规则或放宽证据标准。

人工改审定标签、手工重写自动提议或仅修复金标输入，都不能宣称自动能力已修复。自动改进必须以受控候选修复、实际独立复核和最终精确定位后的自动输出为证据，分别保留原提议与修复记录。

两条路径最后都执行 B/S/P。人工审定得到的回归通过率不等于自动 PDF 审计准确率，不同文档批次、版本或历史快照必须分别报告。

自动模型的工作步骤为：

1. 从提供的文档形成至多六个明确且有界的怀疑和必要的允许对照。
2. 抽取角色、阶段、实验臂、信息对象、权限、交付与反证，并提供原文短引。
3. V4 先定位 citation issue。在预算允许时，最多进行一次有界的 citation-only 候选修复，只能替换失败引文。
4. 对修复后的提议重新进行独立模型复核，分别核对政策、交付、范围解释和源码链。V3 仍执行其独立复核流程。
5. 由确定性代码按原标准校验结构、精确定位引文，处理自证与复核分歧。词汇相似候选不参与最终证据匹配。
6. 将可接纳记录转成 V3 输入，执行同一 B/S/P 核心规则。

模型提示中的 actor/phase/arm/instance 区分、deny 必须有明确排除、absent 必须有肯定边界证据等，是抽取与复核任务要求。它们不是按提示句子数量计出的新增程序规则，也不是独立原文验证保证。

## 清单覆盖边界

已按 SRC01–SRC15 收录当前 extraction_v4/source_bundle 的证据验收职责。源码读取器的路径/资源限制按职责归并，不声称逐个 if、每个文件类型或全部运行系统逻辑各算一条规则。

本清单也不把文档下载、OCR、提供商预算、支付许可、报告渲染与测试用例数量计作论文信息边界判定规则。它不授权运行研究仓库或重新实施任何实验。
