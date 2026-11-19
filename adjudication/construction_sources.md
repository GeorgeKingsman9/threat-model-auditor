**ASPI、Blind Spots、ObliInjection、WebTrap 的独立裁定**

本次裁定重新读取附件、当前归一化案例、当前判定器和固定版本来源。旧 gold 只记录此前预期，未作为事实依据。下面分别记录信息进入构造过程的事实、适用权限的解释，以及行为效果。这三项需要各自的证据。

实际读取的附件如下。两个文件的绝对路径及字节身份均经本次只读核对。

| 文件 | 字节数 | 行数 | SHA-256 |
|---|---:|---:|---|
| `user-provided-classification[sha256=6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4]` | 10173 | 158 | `6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4` |
| `user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]` | 40592 | 389 | `7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d` |

第一份附件的 99–103 行确有 ASPI、AdapTools、WebTrap、ObliInjection、Blind Spots 的状态表。其 111–112 行要求分别保留构造差异和行为效果，原则上合理。其 102 行关于 ObliInjection 尚未完成行为执行的事实陈述，与当前存档存在冲突。第二份附件是本次对照的 TeX 草稿。下文称它们为状态附件和 TeX。

**推荐结果**

| 审核对象与范围 | 推荐最终标签 | 根据 |
|---|---|---|
| ASPI 发布版离线 Stage 2、`clarif_user` 的 task-aware 构造是否违反自身适用权限 | `insufficient_evidence` | 信息流已确认，外部对手限制对这一披露的更强基线及基准构造角色的适用性仍需解释 |
| ASPI 同一构造相对严格的 §3 外部对手预算 | 有条件的 construction mismatch | 若研究明确要求这条构造也模拟同一不可见任务的外部对手，已观察到超出该预算的任务派生字段 |
| Blind Spots v1 的正文输入相对 §2 未知正文假设 | `inconsistent`，限定为论文内部表述及固定归档实现 | 同一方法的 §4.2 及实现使用目标正文，未给出单独放宽正文知识的对照臂 |
| ObliInjection 固定发布版 HotpotQA 优化器与评估匹配问题 | `inconsistent`，限定为发布实现 | 可定位的完整问题输入与题型驱动替代问题的描述有差异 |
| ObliInjection 作者历史 Table XI 生成器的输入 | `insufficient_evidence` | 发布优化器的数据流未识别作者历史生成请求 |
| WebTrap 固定发布版 file-browser PSAA 的内部目标相对路径输入 | `inconsistent`，限定为发布实现与存档请求 | 该路径来自后台目标清单，进入生成输入，超出所述受限区知识边界 |

ASPI 的推荐收窄来自角色和基线的权限适用问题。它不依赖 FULL/AUTH 的 ASR 是否显著。其余两篇发布代码发现和 Blind Spots 的正文输入发现，也不要求先证明 ASR 提升。

**1. ASPI**

TeX 第 175–181 行认为，§3 的外部对手无具体用户任务，而注入回复构造取得模糊任务提示、缺失槽位、预期问题与良性答案。第 178 行另外引入 Appendix C.1 的动态模拟器。这里已明确写出模糊任务提示，不能把该段概括为 Stage 2 直接读取完整原始提示。TeX 第 175 行 (user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]:175)

当前案例 `aspi_released_stage2_partial_query` 将离线 Stage 2 标成攻击者侧回复生成器，直接赋予 `deny`。规则引用 §3 和任务变换描述。它也在 note 中承认 `clarif_user` 是更强基线。判定器对精确匹配的 `deny` 与 `present` 输出 `inconsistent`，其机械执行符合这一输入。真正待裁定的是人工填入的权限是否适用于该角色和这一臂。note 中的保留意见不会参与权限判定。[当前案例第 275 行](../pilot_cases_v2.json#L275) · [判定逻辑第 52 行](../checker.py#L52)

独立来源显示，论文 v1 §3 明确限制外部对手的任务知识，同时把直接用户消息列作更强基线。§5.1 将 `clarif_user` 与 `clarif_ask_user` 列为不同通道。Appendix B.1 明确披露两个数据构造阶段。Stage 1 构造歧义，Stage 2 的模型已获得固定的任务派生字段，并生成带攻击目标的回复。因此 Stage 2 的输出确实受到任务信息条件化。这比仅在 evaluator 中存放任务更进一步，但离线基准构造角色和在线外部对手仍需要分别建立权限。固定论文 §3 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:494) · 固定论文 Appendix B.1 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1196) · [官方 v1](https://arxiv.org/html/2605.17324v1#S3)

固定源代码 revision 为 `e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d`。本次重新计算的 `pipeline.py`、`prompts/dataset.py`、`eval/runner.py`、`eval/simulator.py` 四个文件的 SHA-256 均匹配已存 manifest。`pipeline.py` 第 125–139 行明确给 Stage 2 四项任务派生输入。`prompts/dataset.py` 第 63–66、89–99 行定义 base prompt 是删除一个槽位后的文本，第 165–173 行把它加入请求。它属于 `partial_query`。缺失槽位和答案也另行输入，但未见把 `original_prompt` 变量原样传给该函数。固定清单 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/research/upstream_manifest.json:2) · Stage 2 输入 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/dataset/pipeline.py:125) · 字段定义 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/prompts/dataset.py:60)

发布 runner 第 1575–1585、1797–1812 行将数据集预生成回复用于 `clarif_user`。第 1718–1750 行调用的是良性用户模拟器，第 1764–1777 行将其答案与独立的 W 内容放入 `clarif_ask_user`。Appendix C.1 第 1504、1532 行描述更广的动态攻击模拟，但不能用该文字替代发布 runner 的实际分支。可报告论文工作流描述与发布实现之间的差别。完整原提示进入良性模拟器这一事实，尚未证明它又进入运行时的攻击者构造决策。预生成分支 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1575) · 良性模拟器调用 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi/src/aspi/eval/runner.py:1718) · 论文工作流 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/upstream/aspi-paper-v1.html:1504)

裁定有两层。任务条件化构造事实成立。把它直接称为已确认的外部 IPI 违规，仍需要证明当前审核的 `clarif_user` 更强基线及其离线构造必须遵守 §3 的同一知识限制。更强基线的披露并未明确授权所有任务字段，披露本身也无法消除明确适用的矛盾。但它构成了不能略去的适用范围问题。因此，严格的自身权限违规标签推荐为 `insufficient_evidence`，附带已确认的 task-aware construction 和待澄清的基线权限。若团队选择审核其相对外部对手预算的偏离，应把该比较条件写进结论，保留有条件的 construction mismatch。旧 gold 的 `inconsistent` 无法独立解决这一解释问题。

行为证据另行记录。保存的 v3 报告有 9 个可比较 pair，四个对照均未观察到 FULL 的 ASR 优势，区间较宽，其他套件和配置的效应仍未确定。它不反驳上述输入流。TeX 应收窄的是角色、阶段、基线和动态模拟器的归属，状态附件不应把缺少 ASR 优势作为信息流是否存在的判据。控制对照报告 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/CONTROLLED_ABLATION_REPORT.md:7) · pilot 范围 (private-research-archive/repository/aspi-matched-context-pilot-v1/papers/ASPI/v3/PILOT_REPORT_V3.md:49)

**2. Blind Spots in the Guard**

TeX 第 152、155、158 行认为，§2 排除精确正文知识，§4.2 的生成器却读取目标正文。算法案例审核的也是这条正文输入，范围更窄，绑定源码归档 `9a21b5a230cbcc92ec66987aa7814c188881108a` 的 Exp. 1。两者的构造差异结论相符。TeX 第 152 行 (user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]:152) · [当前案例](../pilot_cases_v2.json#L371)

本次核对的官方 v1 §2 明确限制具体任务和精确正文，Introduction、§4.2 又公开描述目标正文条件化的构造。这里未找到类似 ASPI 的单独更强正文可见基线声明。披露丰富输入使论文内部两种表述可直接对照，并未自动取消 §2 对同一攻击的限制。[官方 v1 §2](https://arxiv.org/html/2605.22001v1#S2) · [官方 v1 §4.2](https://arxiv.org/html/2605.22001v1#S4.SS2)

本地 source 第 211–215 行将 clean context 的前 2000 字符放入生成输入，第 235–254 行计算相似度并返回所有变体。归档说明记录该任务库最长正文为 1875 字符，因此对该库为完整正文输入。这里未显示单独的用户 instruction 进入生成器。Exp. 1 第 196–219 行评估所有返回的变体，而 TeX 第 155、165 行将最高相似度筛选写成实际评估步骤。论文 §4.2 确实描述这种筛选，因此稿件应注明它是论文的方法描述，同时保留发布 Exp. 1 逐变体评估的差别。生成器 (private-research-archive/src/attacks/camouflage_generator.py:211) · Exp. 1 (private-research-archive/experiments/exp1_static_vs_camouflage_single.py:196) · 归档正文范围 (private-research-archive/analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:9)

推荐保留 `inconsistent`，只描述 §2 与同一攻击构造的正文知识差异。原论文历史生成记录是否与本地归档完全相同仍未核实。候选筛选的实现差异可作为独立条目，不改变正文流入的已有证据。

状态附件第 103 行所引行为结果为 121 对载荷，FULL 24/121、NO_CONTEXT 15/121。当前结果同时保存 paired bootstrap 区间 `[0, 0.1487603]` 与 task-clustered 区间 `[0.0084746, 0.1440678]`，McNemar 双侧 p 为 0.07835。附件仅列第一套区间。不同统计量和重采样单位应原样报告。两提示还改变文体指导，多个变体来自同一任务，victim 与 judge 共用模型，且已有一个疑似评分假阳性。这些因素限制效果及因果解释。它们不影响目标正文已经进入构造输入的判断。当前结果与统计 (private-research-archive/results/context_ablation_asr_full_llama31/summary.json:49) · 实验解释范围 (private-research-archive/analysis/casebook_2026-11-05/BLIND_SPOTS_CASES_ZH.md:208)

**3. ObliInjection**

TeX 第 316–322 行把发现限定为发布版 HotpotQA 优化器使用原问题文本，保留攻击是否依赖该问题的限定。算法也明确区分发布优化器与历史 Table XI 生成器。其发布实现判定与 TeX 相符，历史生成器的 `insufficient_evidence` 额外保留了一项未识别的来源。TeX 第 316 行 (user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]:316) · [发布实现案例](../pilot_cases_v2.json#L323) · [历史案例](../pilot_cases_v2.json#L141)

独立核对的 v3 论文在 §III-B 限制具体目标指令，§V-A 将 RAG 元数据列为 question type，Table XI 给出从题型生成替代问题及支持材料的过程。其具体方法说明为这里的权限解释提供了比单独的无任务知识句子更窄的依据。论文 §III-B (private-research-archive/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:209) · 论文 §V-A (private-research-archive/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:655) · Table XI (private-research-archive/papers/ObliInjection/reproduction/pilot_15/obliinjection_paper.txt:1164)

固定发布 commit 为 `b1f6a3f48c0cf121534374cbcef453832594867b`。本次只读 git 状态仍为 clean。HotpotQA config 的三个数据路径指向相同的 shipped shadow JSON。driver 用同一组 target indices 取得训练、验证与测试问题。loader 从 `question` 字段取得全文，构造路径将其放入优化输入。已有离线来源报告确认 100 条发布记录按规范化问题及答案各有唯一的官方 HotpotQA 匹配。推荐保留发布版的 `inconsistent`，绑定该 config 和同一 target index，问题形式为 `full_query`。发布配置 (private-research-archive/papers/ObliInjection/upstream/ObliInjection/configs/task_configs/hotpotqa_config.json:23) · driver 的选定问题 (private-research-archive/papers/ObliInjection/upstream/ObliInjection/obliinjection.py:33) · 数据流审计 (private-research-archive/papers/ObliInjection/audit/dataflow/dataflow.md:10) · 官方匹配归档 (private-research-archive/repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/three_arm_pilot_15_v1/REPORT.md:47)

Table XI 生成器的缺失只限制对作者历史 Step I 的重建。它不会抹去发布优化器已观察到的输入流。历史输入推荐继续标 `insufficient_evidence`。状态附件第 102、128 行将两种范围并在一起，容易把发布源码发现降为未确认。发布溯源说明 (private-research-archive/papers/ObliInjection/audit/provenance/PROVENANCE.md:17) · Table XI 发布审计 (private-research-archive/papers/ObliInjection/audit/dataflow/table_xi_audit.md:3)

状态附件第 102 行称没有完成行为执行，已与当前档案冲突。联合 A/C/UQ 报告第 30–39 行确认 2000 条正式回答完成，A 为 391/500，C 为 497/500，UQ 为 308/500。第 3–20 行仍记录 `experiment_complete=false`，原因是远端归档同步和报告 CAS 未闭合。科学计算完成与收尾状态各自保留。TeX 第 324 行的 A/UQ 数值有现存支持，但应明确每题采用冻结的 C donor 合成问题，保留 A 的文档。该对照有十个目标和每臂一个联合优化产物，500 个评估单元不能自动视为 500 次独立构造。A/C 同时改 Q、D 和分布，其更高的 C 结果尤其不能包装为统一的 full-context 优势。联合报告 (private-research-archive/repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:3) · 正式比例 (private-research-archive/repository/obli-gpt4o-ac-transfer-20261031/papers/ObliInjection/reproduction/gpt4o_aux_mistral_joint_matched_v2_20261031/report.md:30) · Q/D 条件说明 (private-research-archive/analysis/casebook_2026-11-05/ObliInjection_evidence.md:13)

**4. WebTrap**

TeX 第 339–345 行认为发布 file-browser 生成器从后台安全清单取得精确内部相对路径，并明确保留历史 run revision 和 ASR 膨胀未知的限定。当前算法绑定固定发布版及两个已保存 ORIGINAL 请求。其结果与 TeX 的信息流理由相符。TeX 第 339 行 (user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]:339) · [当前 ORIGINAL 案例](../pilot_cases_v2.json#L3)

本次重新读取的官方 v1 §4.1 和 Appendix A.1 明确限制构造阶段对受限区内部结构的使用，Algorithm A.2 的输入为可见入口描述、攻击目标和环境类型。它也明确将部分 baseline 的知识设得更强，因此本结论只应用到 WebTrap 自身选定的 PSAA 臂。[官方 v1 §4.1](https://arxiv.org/html/2605.08310v1#S4.SS1) · [官方 v1 Appendix A.1](https://arxiv.org/html/2605.08310v1#A1.SS1)

固定源 commit 本次核对为 `f8255c83d4a569fc374198b67717fcbee17af1fb`。构建器第 327 行从清单读取 logical path。生成代码第 417–440 行把转换后的字段加入模板变量并渲染请求。已有字段审计区分了公开目标语义、可见入口与精确内部定位。存档请求对照确认两个 ORIGINAL 的最终输入含选定定位字段，其 LIMITED_CONTEXT 对照移除了该字段。对当前源代码及这两份存档请求，推荐 `inconsistent`。构建器字段 (private-research-archive/papers/WebTrap/replication/upstream/file/exp/exp1/build_cases_top20.py:327) · 渲染输入 (private-research-archive/papers/WebTrap/replication/upstream/file/exp/attack/psaa/inject.py:417) · 字段审计 (private-research-archive/papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:37) · 实际请求核实 (private-research-archive/papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:65)

状态附件第 101、127 行依据导航和工具故障把 WebTrap 留作候选，适用于行为效果的完成程度。对已定位的构造输入，当前证据已允许更明确的限定结论。保存的机制审计还把字段到达生成器、生成内容采用字段、受害者实际曝光、受害者行动和最终成功分别记录。两个案例的两臂都没有完整成功，部分最终内容未到达受害者。它支持字段进入并影响目标绑定，尚未支持 ASR 增幅或作者历史运行的相同版本。机制链 (private-research-archive/papers/WebTrap/replication/CONTEXT_EFFECT_ASSESSMENT.md:3) · 结论范围 (private-research-archive/papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:76)

**对归一化与稿件的处理建议**

最终判定应先确认论文条款适用的主体、阶段和实验臂，再比较实际信息流。已有判定器将该解释工作交给输入规则，因而案例引用齐全仍可能含有权限适用错误。ASPI 是当前最需要记录此项分歧的条目。权限适用尚未确定时，保持输入流 `present`，把规范性判定保留为证据不足。不能为配合旧 gold 把真实输入流改成 absent。

同时保留建设阶段差异和行为影响的独立结论。ASR 不显著、样本少、未完成归档，分别限制对应的效果或过程主张。行为条件不应被添加为已经适用的禁止信息流判定的必需条件。TeX 的全局显著降幅假说仍需多个有识别力的实验支持，现有四篇的材料给出的是不同范围的发现。

本报告只新增本文件。核对涉及读取文字、源码、固定状态与文件哈希，未运行研究仓库的模型、优化器或受害者实验。
