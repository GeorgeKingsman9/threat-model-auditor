**TeX、既有说明与审核算法的逐篇裁定**

本表包含 2026 年 11 月 19 日对 ASPI 适用范围的纠正。原 11 篇的旧结构化结果为 7 项确认、1 项范围内一致、3 项证据不足。当前保留 5 项限定的不一致发现，FHA、LIAR 的旧确认仍需收窄，原 11 篇分布为 5／1／5。连同新增的 4 个域内控制，目前 registry 有 15 篇、25 条具体怀疑，分为 5 项限定发现、5 项限定怀疑被排除、5 项证据不足。此前 4／5／6 是 ASPI 纠正前的快照。这些数字描述已列明的审核范围。[旧结果](../adjudication/baseline/structured_results.json#L2) · [当前案例](../adjudication/reviewed_cases.json#L1) · [当前范围与标签](../adjudication/reviewed_papers.json#L1) · [复核标签](../adjudication/reviewed_gold.json#L1)

TeX 指 389 行的论文草稿。新附件指 158 行的既有判断说明，两者都是待核对材料。下表的“确认”仅指特定主体、阶段、实验臂和信息实例上的发现。“范围内一致”表示表中列出的怀疑已有具体反证。证据不足保留未解决的权限适用或交付来源问题。TeX (user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]:121) · 新附件 (user-provided-classification[sha256=6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4]:1)

**原 11 篇的逐项对照**

| 工作 | TeX／新附件的主张 | 旧结构化结果 | 独立原文裁定与范围 | 差异出在哪里 | 已做与待做的修改 |
|---|---|---|---|---|---|
| **AdapTools** | TeX 129–135 行将具体任务与失败推理输入直接视为超出黑盒能力。新附件 100 行保留为候选。 | 证据不足 | **证据不足**。最终版 §4.1 区分黑盒与灰盒，§4.3 描述离线策略开发，§4.5 描述预建库与线上推断。尚未将开发输入绑定到受限的 held-out 黑盒线上构造。 | TeX 混合了角色和阶段。旧算法的限定结论可以保留。 | registry 已保留线上来源未知。TeX 应更新最终版节号，明确离线输入与在线输入，撤下确定性的违规措辞。[最终版](https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4) · [当前案例](../adjudication/reviewed_cases.json#L507) |
| **Blind Spots** | TeX 152–158 行比较 §2 的未知正文假设与 §4.2 的目标正文输入。新附件 103、129 行因行为证据限制将其列为候选。 | 确认 | **保留限定发现**。固定归档 Exp. 1 确实把对应正文送入生成器，§2 的限制适用于该信息。§4.2 公开披露丰富输入，构成可核对的内部表述差异。 | 新附件把效果证据的强弱带入信息流判定。TeX 另述最高 ACS 筛选，但发布 Exp. 1 逐个评估返回的变体。 | registry 已保留正文流入。TeX 将候选筛选写成论文所述方法，并说明发布实现差别。行为影响继续单独报告。[原文 §2／§4.2](https://arxiv.org/html/2605.22001v1#S2) · 源代码 (private-research-archive/experiments/exp1_static_vs_camouflage_single.py:196) |
| **ASPI** | TeX 175–181 行认为任务派生字段与 §3 的外部对手限制冲突，并额外引用 C.1 模拟器。新附件 99、111 行保留 construction mismatch。 | 确认 | **保留限定构造发现**。§3 的更强基线放宽 direct-user 投递，没有授权具体任务知识。固定 Stage 2 将部分任务提示用于构造 `clarif_user` 回复，因此该条任务知识限制仍适用。 | 我们此前把“更强投递通道”推成“可能有更强任务知识”并降为 uncertain，超出了原文。信息流始终是 confirmed 的 `partial_query`。 | 已恢复该构造边的适用性与限定不一致标签。TeX 的 Stage 2 主论点可保留，C.1 动态模拟器仍应与发布实际分支区分，不推广到官方 `clarif_ask_user` W 或历史 ASR。[§3](https://arxiv.org/html/2605.17324v1#S3) · 固定分支 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575) |
| **MUZZLE** | TeX 198–204 行指出 operator 提供精确任务，未来线上攻击者的获取方式未说明。新附件 75–91 行已收窄为发现到部署的来源缺口。 | 证据不足 | **证据不足**。论文明确披露本地发现阶段的任务和遥测输入，足以排除“这项离线输入本身违规”的怀疑。另一个未来 victim 任务如何取得，仍未建立。 | TeX 的确定性标题强于正文。新附件收窄方向成立，未来来源未知仍不能直接称为已确认违规。 | registry 已拆成离线授权与线上获取两条。TeX 改为来源／迁移范围问题，保留未解决路径。[最终版 §2.3／§3](https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) · [当前两条](../adjudication/reviewed_cases.json#L564) |
| **FHA** | TeX 221–228 行将 direct 同查询构造列为确认，并把 universal 作为另一种设置。新附件未另列。 | 确认 | **证据不足**。同查询参与构造已确认，但论文明确将 §6 single-payload 实验列为初始诊断。其预算不能直接等同可部署攻击。§7 固定查询多 payload 鲁棒性也另有范围，不能自动继承诊断例外。 | 旧 TeX 与旧标注遗漏了论文自己的 diagnostic 限定。自动文档审查提出该限定后，独立原文复核修正了人工预期。 | 已撤下 direct 的无条件确认，另列 fixed-query 鲁棒性怀疑。TeX 应补诊断范围与训练／held-out 区分，保留构造依赖事实。[诊断限定 p6–7](https://arxiv.org/pdf/2604.20994v2#page=6) · [独立追加复核](../adjudication/policy_sources.md#L106) |
| **AGENTCON** | TeX 244–251 行指出构造依赖请求与其获取来源缺口。 | 确认 | **保留限定发现**。固定提交版 §3 排除精确请求和中间输出，§4.1 将攻击置于该约束下。§4.3 的原请求构造依赖请求条件化计划与损失，后续固定图像在不同请求上测试属于另一条件。 | 旧标签方向可保留，但接收者和表示需要更精确。证据支持优化过程依赖计划／损失，尚未证明原始 query 被交给独立生成 LLM 或未来部署请求已被获取。 | registry 已改为原请求基准中的构造优化。TeX 应明确这一限定。机器读取当前受 OpenReview 挑战页阻挡，不能把索引原文的人审发现写成此次 PDF 自动成功。[固定原文 §3／§4.3](https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4) · [当前案例](../adjudication/reviewed_cases.json#L758) |
| **Retrieval Barrier** | TeX 269–280 行承认问题定义给定查询，主要提出未来查询的时序／获取疑问。 | 范围内一致 | **限定怀疑被排除**。§2.1 明确给予构造过程目标查询，§4.1 在这一预算下使用它。部署获取问题仍可单列。 | TeX 的 Inconsistency 标题比正文更强。给定查询条件不能因为未来获取尚未说明而直接判违规。 | registry 保留授权反证。TeX 将标题改为部署来源问题，并明确基准中的查询输入本身被允许。[正式论文 §2.1](https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) |
| **LIAR** | TeX 295–301 行把 source 训练子集和 NQ→NQ 的同名语料条件解释为禁止知识库访问。 | 确认 | **证据不足**。§5.2 对 source 训练子集有具体授权，足以排除该读取本身违规。对受限 target 的直接读取和 source／target 文档重叠，缺少对象级证据。 | 旧 TeX 和输入标注把同名 benchmark 当成同一数据对象，并漏掉阶段性授权。V2 的字符串比较无法纠正这个前提。 | 已拆成 source 授权、target 直接读取、文档重叠三条。TeX 撤下已确认 target 访问的结论，保留待核实的数据身份问题。[§5.2](https://aclanthology.org/2024.emnlp-main.96.pdf#page=5) · [当前三条](../adjudication/reviewed_cases.json#L907) |
| **ObliInjection** | TeX 316–324 行限定发布版 HotpotQA 优化器读取原问题。新附件 102 行却称尚未完成行为执行，并引用未公开 Table XI 生成器。 | 确认 | **保留发布实现发现**。固定 config／driver 把同一评估题目的全文送入优化，区别于题型驱动替代问题的描述。作者历史 Table XI 输入仍未知。 | 新附件混合了发布优化器、历史生成器与效果完成度，且“未执行行为”已过时。TeX 的主要源码论点可保留。 | registry 保留发布版确认及历史未知。TeX 澄清 UQ 是每题对应的冻结 C donor 问题，效果限定为当前联合优化。下文另列完成状态。源码数据流 (private-research-archive/papers/ObliInjection/audit/dataflow/dataflow.md:10) · [当前两条](../adjudication/reviewed_cases.json#L219) |
| **WebTrap** | TeX 339–345 行指出内部目标路径进入发布生成器，并保留历史版本与 ASR 膨胀未知的限定。新附件 101、127 行因实验问题保留候选。 | 确认 | **保留限定发现**。固定 file-browser PSAA 代码与存档请求证明选定后台内部定位字段进入生成输入。原目标文本和可见入口是分别允许的信息。 | 新附件将行为过程的不完整带入构造证据状态。TeX 的字段结论与当前限定判定相符。 | registry 保留 ORIGINAL 和 LIMITED 控制，只审核该字段。继续保留历史运行与效果未知。[原文边界](https://arxiv.org/html/2605.08310v1#S4.SS1) · 已存字段与请求审计 (private-research-archive/papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:37) |
| **ICoA** | TeX 361–367 行已明确身份来源未说明，并承认未证明直接读取系统提示。 | 证据不足 | **证据不足**。固定实现使用与系统提示相同的身份常量，值相等尚未建立被禁止的读取来源。论文也未明确禁止通过其他途径知道身份。 | 核心限定已一致。确定性的示例标题仍应收窄。“继承”若指代码继承，宜改为使用相同固定身份。 | registry 保留系统读取与常量来源两条，不把值相等变成 source 相同。[最终版 §2／§4.1](https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) · [固定源码](https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49) |

**ASPI 适用范围的纠正**

此前降级的依据是我们推断披露的更强 direct-user 基线可能同时放宽任务知识。重新核对 §3 后，原文只说明投递通道更强，没有给该基线具体任务访问权。固定代码则把部分任务提示送入 Stage 2 注入回复构造，再由 `clarif_user` 使用该回复。一般知识限制与这条具体构造链能够对齐，恢复限定的 construction mismatch。Stage 1 的基准设计许可仍分别处理，官方 `clarif_ask_user` 的 W 分支和作者历史 ASR 也各有范围。[§3](https://arxiv.org/html/2605.17324v1#S3) · [当前案例](../adjudication/reviewed_cases.json#L81)

这次纠正发生在审定输入的权限解释，通用 V3 判定门继续使用相同规则。18 篇 PDF 自动结果中 ASPI 仍是证据不足，四个域内控制的自动结果也保持原记录。本次没有新增模型对 ASPI 的自动确认。[纠正后的源证据规则回归](results/2026-11-19-aspi-scope-correction/source-regression/report.md)

**FHA 对人工预期的纠正**

FHA 的自动审查指出了“initial diagnostic”及相应的非部署限定。独立复核在同一版本的 PDF 第 6–7 页确认了这一上下文，因此修正人工案例的权限适用性，而继续保留 query-conditioned construction 的交付证据。旧单查询结果不再直接计入确认。§7 固定查询多 payload 鲁棒性另立怀疑，其是否声称满足同一部署预算仍待澄清。自动系统在这里提供了纠错线索，随后由原文裁定改变 registry。[复核记录](../adjudication/policy_sources.md#L106) · [当前诊断案例](../adjudication/reviewed_cases.json#L686) · [当前鲁棒性案例](../adjudication/reviewed_cases.json#L1296)

**ObliInjection 的完成状态与效果范围**

新附件第 102 行的“没有完成行为执行”与联合实验档案冲突。存档确认已有 2000 条正式回答，CLEAN、A、C、UQ 各 500。A 为 391/500，UQ 为 308/500，C 为 497/500。报告开头仍有 `experiment_complete=false`，对应远端归档同步和报告 CAS 尚未闭合。科学回答的完成状态和归档发布状态应各自记录。新附件第 102 行 (user-provided-classification[sha256=6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4]:102) · 报告当前状态 (private-research-archive/repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:3) · 正式回答汇总 (private-research-archive/repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30)

这些回答来自十个目标和各臂一个联合优化产物，包含布局重复。A/UQ 的差异支持当前产物对构造问题的敏感性，推广到一般攻击效果仍有限制。A/C 还同时改变问题、文档及分布，且 C 的比例高于 A。构造信息流与效果问题应分别陈述。Q/D 条件及解释范围 (private-research-archive/analysis/casebook_2026-11-05/ObliInjection_evidence.md:13) · 重复单位和机制限制 (private-research-archive/analysis/casebook_2026-11-05/ObliInjection_evidence.md:109)

**新增四个域内控制**

它们与原 11 篇中的 Retrieval Barrier 一起，构成五项限定怀疑排除。每条都应带具体怀疑、固定来源和反证。

| 工作 | 新附件说法 | 当前能排除的具体怀疑 | 仍需保留的范围 |
|---|---|---|---|
| **Trojan Hippo** | 13、28–32 行把主题级构造与未来精确查询区分。 | 论文允许的主题 seed 条件本身不越界。固定 train/test 一对样例的传播步骤沿用同一攻击对象，两个 trigger 查询不同，该步骤没有用该 test trigger 再做 mutation。 | 新附件若被理解为生成器只见主题，则过窄。源码的训练 mutator 确实读取训练实例 `user_message`。当前反证仅覆盖命名的主题 seed 及一对固定传播边界。[独立来源审计](../adjudication/negative_sources.md#L1) · [当前两个案例](../adjudication/reviewed_cases.json#L1495) |
| **TopicAttack** | 14 行认为其遵守任务不可见边界。 | 固定 default chatbot 构造所读 benign document 有论文授权。构造模板、wrapper 与空默认 system 的完整请求边界排除了独立 `instruction` 字段交付。 | 这一结论绑定默认路径，仍允许从正文推测任务事实，未认证所有自定义模板或历史运行。[原文 §3](https://aclanthology.org/2025.emnlp-main.372.pdf#page=4) · [当前两个案例](../adjudication/reviewed_cases.json#L1356) |
| **AgentDojo** | 15、38–47 行报告关键内容覆盖和 utility 变化。 | 单凭内容覆盖或效用变化，无法推出攻击构造者收到被禁止的私有查询。该“足以推出信息越界”的推论被排除。 | 附件所报数值、配置、分母及原始缺陷尚未独立核实。当前记录是问题类型的逻辑控制。[原文指标区分](https://arxiv.org/html/2406.13352v3#S3.SS4) · [当前案例](../adjudication/reviewed_cases.json#L1196) |
| **ASB** | 55–65 行报告 harness 强制工具执行及 ASR 变化，并归为协议问题。 | 单凭强制动作或 ASR 改变，无法推出私有查询进入攻击构造。该跨类型推论被排除。 | 附件数值与强制执行缺陷的原始链路未独立复现。协议归因可以另审，当前结果只处理信息越界推论。[最终版补充](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=26) · [当前案例](../adjudication/reviewed_cases.json#L1246) |

Attention Is All You Need、ResNet、Adam 是另外三个域外输入，输出 `not_applicable`。它们只用于检查 IPI 审核的适用范围。四个新增域内控制则需要真正核对论文权限和具体怀疑，不能用域外识别替代。[测试清单](../benchmarks/source_review.json#L115)

**算法已修与仍有限制的部分**

V2 在人工输入同形 `deny` 与 `present` 时确认不一致。FHA、LIAR 暴露了旧输入前提的范围问题，ASPI 则暴露了我们后来推断知识例外时的过度解释。V3 要求权限适用、信息层次、实际交付证据及实例关系，并要求怀疑的排除有具体反证。它还区分攻击者知识限制与受害者安全目标，避免将攻击成功直接写成作者违反知识预算。行为效果作为独立元数据。[V3 规则](../scope_review.py#L1)

这些门槛检查结构与引用绑定，原文语义仍可能由人工或模型误读。registry 的标签一致回放只能验证规则是否处理了已给的规范化证据，不能当作从陌生论文端到端发现问题的准确率。ASPI 修正后的当前分布为 5／5／5，最新源证据回归另存。此前 4／5／6 的重审记录，以及更早 FHA 改判前同为 5／5／5 的记录，均保留各自版本和逐篇标签，不能仅凭总数相同当成同一次结果。[最新源证据回归](results/2026-11-19-aspi-scope-correction/source-regression/report.md)

**自动 PDF 测试的阶段性状态**

18 篇测试的 citation replay 快照记录 17 篇完成、AGENTCON 因访问挑战失败。17 篇中，Blind Spots 的引文通过同一 PDF 的默认阅读顺序视图重新定位后恢复确认，三个域外输入被识别，其余输出证据不足。这是零次新增模型调用的引用与判定回放，要求相同原 PDF 哈希和相同主输入。它修复了双栏 `-layout` 将文字交织导致的精确引文定位失败，没有把近似文本当作原句。阶段性回放 (historical local run: outputs/2026-11-19-v3-citation-replay/report.json) · Blind Spots 单篇结果 (historical local run: outputs/2026-11-19-v3-citation-replay/blind_spots/result.json) · [双文本抽取入口](../documents.py)

PDF-only 自动输入缺少部分代码和存档请求，因此不能直接拿完整证据 registry 的标签计算自动准确率。AGENTCON 的失败须单独报告，也不能填成模型阴性。旧 document-study 汇总还包含早先一次 Adam 技术失败，当前 citation replay 已完成该条，两个快照不应混用。最初自动测试快照 (historical local run: outputs/2026-11-19-v3-document-study/report.json) · AGENTCON 访问失败 (historical local run: outputs/2026-11-19-v3-citation-replay/agentcon/result.json)

四个域内控制的更新补测已经全部结束：四篇均为证据不足，没有确认信息边界不一致。Trojan 的 V2 错误告警被消除；其余三篇仍弃判，不能算作已确认阴性或据此计算普遍性误报率。

| 补测对象 | 原文裁定的有限目标 | 更新自动结果 | 引用与终态复核 |
|---|---|---|---|
| Trojan Hippo | 主题 seed 权限及命名 train/test 传播边界 | 证据不足 | 终态 completed，未确认信息边界违规 |
| TopicAttack | 许可正文与默认请求中独立 instruction 字段的排除 | 证据不足 | 终态 completed，未确认信息边界违规 |
| AgentDojo | utility／内容覆盖不直接推出信息交付 | 证据不足 | 终态 completed，未确认信息边界违规 |
| ASB | harness 动作归因不直接推出信息交付 | 证据不足 | 终态 completed，未确认信息边界违规 |

最终结果与所有过程已保留在 [结果总表](SOURCE_REVIEW_RESULTS_ZH.md) 和 [四篇控制重测](results/2026-11-19-source-review/negative-final/report.md)。每次输入和输出版本均保留。FHA 展示了模型提出新限定后应修正人工预期；不能为了旧标签一致而放松判定。

最终并列统计和完整过程请以 [重审结果索引](SOURCE_REVIEW_RESULTS_ZH.md) 为准，其中包含已完成的四篇补测及原始/最终文档回放。
