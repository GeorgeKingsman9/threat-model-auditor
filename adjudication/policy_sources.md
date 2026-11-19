# 论文权限条款与输入来源的独立裁定

核查日期为 2026-11-19，时区 Asia/Shanghai。本文对照附件、当前人工结构化结果、论文原文和已有本地审计，记录可以成立的结论及适用范围。这里的原文核查和文件阅读没有重新执行模型实验。

## 输入身份

| 输入 | 本次读取的身份 |
|---|---|
| 中文分类说明 | `user-provided-classification[sha256=6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4]`，10,173 bytes，SHA-256 `6bcd416a830f7be28d13098e53b04a243d0b1a4de6feaad20b7aea9538280ed4`。`wc -l` 计 157 个换行，`nl` 显示 158 行，最后一行没有换行。 |
| TeX 草稿 | `user-provided-tex[sha256=7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d]`，SHA-256 `7bf0e622b12efb0df51867444c318132d8f226108b259e6060350e234073b67d`。 |
| 结构化结果 | `analysis/threat_model_auditor/paper_pilot_results.json`，本次读取时 SHA-256 `eb2ca5da2de5a612ca959bec1994d0ae7b3e07332e1b63846bb4d92d85cd3af2`。 |

中文说明是待核实的归纳材料。其第 40 行的 AgentDojo `60.87 → 72.19` 和第 59 行的 ASB `73.58% → 9.25%` 在这次核查中没有找到对应原始运行和分母证据，本文不将这两组数字作为已验证结果。它们描述的内容覆盖和强制执行问题，在概念上需要与攻击者信息权限分别评估。

## 裁定规则

先确定数据所属对象、实验臂、阶段、角色和表示形式，再读该范围内最具体的权限条款。论文对离线 source 数据的明确授权应进入规则，不能仅保留较早的概括性 target 限制。给定损失的模型输入、优化器实际使用的信息、测试器用来评分的信息，以及未来部署者能获取的信息，需要分别取证。

如果受限制的任务字段参与了攻击产物的参数更新，这支持构造依赖。该证据仍需注明接收者是优化过程、模型请求或其他边界。用户原句进入优化目标不能自动表述为原句发送给了一个 payload-generation LLM。相同 benchmark 名称也不能确定 source/target 是同一份数据、同一子集或同一个实时索引。

## AGENTCON

**原文范围。** 核查的是 ICLR 2026 提交版 PDF。§3 Attack Constraints（PDF 第 4 页）限制精确用户请求、实时渲染页面及中间输出的可见性，同时允许一般任务和网站信息以及模型设计知识；这段本身没有清楚区分代表性 source request 与最终 target request。§4.3（第 6 页）把请求记为 `p`、HTML 记为 `q`，描述先取得基于请求的计划，再进行图像构造。Eq. 5 是该构造过程使用的条件损失。§5 User-Request Variability（第 9 页）说明图像构造后固定，再换成相似请求进行测试。 [§3](https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=4) · [§4.3](https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=6) · [§5](https://openreview.net/pdf/a7b8365a80d58906740ac477248926c6c6a43640.pdf#page=9)

**可确认的内容。** 文本描述的 source-request 构造过程依赖一个具体请求和相应计划。因为目标用于更新待构造产物，把它解释为仅在事后评分时出现不符合 §4.3 的方法叙述。角色应写成离线优化过程。没有在所读材料中建立将目标用户原句直接交给独立生成 LLM 的请求边界，也没有建立未来部署请求或私有实时计划进入该过程的来源链。

**权限上的保留。** §4.3 同时说明用一个请求构造的产物会转移到相似请求，§5 给出固定产物测试。构造用的代表性 source request 和部署时未知的 target request 不能直接合并。按 §3 与原始 source request 上的直接测试比较，可以记录论文内部范围表述的张力。要将此升级为实际部署阶段已确认的信息越界，需要确认被使用的请求就是受限制的目标请求，并确认这一实验臂声称遵守相同限制。现在材料支持构造依赖，尚未建立该部署来源链。

**对当前标注的裁定。** 当前结果第 438–509 行的 `inconsistent` 只有在明确解释为同一 source-request 实验与 §3 的文本范围对照时才有边界。作为已确认的未来用户上下文越界或 source-to-target 泄漏 gold，该标签过强。建议保留论文内部范围问题，并将部署阶段的字段权限/来源判为证据不足。TeX 第 244、247、251 行强调获取来源未说明，未写出 JSON 第 490 行编码的明确 `deny`，两份文件的判据不完全相同。

**获取限制。** 本次通过网页工具读取了原始 PDF 的已索引文本。真实投稿 ID 为 `AMIb7RWnBI`，公开入口为 [投稿 PDF](https://openreview.net/pdf?id=AMIb7RWnBI)。直接打开该入口或哈希 PDF URL 都出现 OpenReview 验证页；本机对正常 PDF、attachment、API PDF 入口的读取均返回 403。现有 `outputs/2026-11-19-document-preparation/agentcon/result.json` 记录的是验证页提取，该机器输入没有论文正文，不能当作模型已经重新读过这份 PDF 的证据。本次没有取得可供回放的本地完整 PDF，也没有建立新下载 PDF 的字节哈希。

## LIAR

**原文范围。** EMNLP 2024 最终论文 §3.1（PDF 第 3 页）概括限制对用户请求、现有目标知识及目标 LLM 内部参数的直接访问。§5.2（第 5 页）明确假定可以使用 source knowledge base 的训练子集，并写明面向未见 target 知识库和请求泛化。§5.3 同页也单独说明 source LLM 的使用。Table 1（第 7 页）报告 source 与 target benchmark 名称，其中包含同名条件。 [§3.1](https://aclanthology.org/2024.emnlp-main.96.pdf#page=3) · [§§5.2–5.3](https://aclanthology.org/2024.emnlp-main.96.pdf#page=5) · [Table 1](https://aclanthology.org/2024.emnlp-main.96.pdf#page=7)

**独立裁定。** §5.2 是该离线 source-training 阶段的明确授权，必须纳入策略。当前 `liar_same_benchmark_source_kb` 把 source 子集的读取套用 §3.1 的一般 `deny`，仅从同名 NQ-to-NQ 条件推出越界，缺少文档级身份、切分或实时目标索引的证据。Table 1 的同名条件不能单独建立这些事实。

**建议结论。** 已披露的 source-training 访问在该特定授权范围内一致。对受限制的 target 数据直接访问及 source/target 重叠，保持证据不足。可以保留摘要、§3.1 与具体训练授权之间的叙述张力。当前结果第 600–662 行、TeX 第 294–298 行据此标为已确认权限越界，强于现有证据，宜修改相应理由或判定对象。不能仅凭本次阅读把整篇认定为 false positive 或全面一致。

## MUZZLE

USENIX Security 2026 最终论文 §2.3（PDF 第 4–5 页）明确区分本地发现与线上投放，发现阶段允许观察 LLM 网络 I/O。§3.1、§3.3（第 5–6 页）披露 operator 给出的 benign task 和实验遥测。因而该离线任务输入的授权与其使用能对齐。 [§2.3](https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=4) · [§3.3](https://www.usenix.org/system/files/usenixsecurity26-syros.pdf#page=6)

当前 JSON 第 259–358 行把离线输入记为范围内一致，把未知未来线上任务的获得方式记为证据不足，与中文说明第 75–91 行收窄后的论点一致。TeX 第 198–204 行正文也指向相同来源缺口，但确定性的 Inconsistency 标题强于它提供的证据。已有本地 `analysis/casebook_2026-11-05/CASEBOOK_ZH.md:114,137` 还明确保留轨迹和反馈，显式任务字段删除不能代表完全关闭任务信息。后者是本地对照的范围说明。

## AdapTools

EMNLP 2026 最终论文 §4.1（PDF 第 4 页）分别限定黑盒第三方与灰盒 MCP 角色。§4.3（第 5 页）披露策略库构建中的任务和失败推理输入。§4.5（第 6–7 页）把策略库和转移矩阵描述为预先离线构建的组件，线上过程依据 MCP 交互推断上下文。 [§4.1](https://aclanthology.org/2026.emnlp-main.2055.pdf#page=4) · [§4.3](https://aclanthology.org/2026.emnlp-main.2055.pdf#page=5) · [§4.5](https://aclanthology.org/2026.emnlp-main.2055.pdf#page=6)

当前 JSON 第 10–60 行的证据不足结论应保留。它限定当前 held-out 黑盒在线任务进入构造的路径，所读资料无法将离线策略构建的输入绑定到该角色和阶段。中文说明第 100、126 行的候选分类与此一致。TeX 第 132、135 行直接写超出黑盒能力，混合了策略开发与受限线上阶段。已有本地 `papers/AdapTools/METHODOLOGY_COMPARISON.md:12–24` 也将该角色/时间绑定列为未解决证据问题。

## FHA

arXiv:2604.20994v2 §4 限制用户 prompt 的访问，§6.1 和 Appendix B.1 又明确把同一 benchmark 查询列入 direct 实验的构造输入。§7 则分别报告 source 查询训练和 held-out formulation 转移。相同查询参与 direct 构造有文本依据，不能仅从受害模型也在处理请求这一点推出。 [§4](https://arxiv.org/html/2604.20994v2#S4) · [§6.1](https://arxiv.org/html/2604.20994v2#S6.SS1) · [Appendix B.1](https://arxiv.org/html/2604.20994v2#A2.SS1) · [§7](https://arxiv.org/html/2604.20994v2#S7)

当前 JSON 第 366–431 行与 TeX 第 221–228 行的 direct 同查询对照基本一致。该记录的证据类型是论文描述，适合记录 direct 实验与一般知识限制之间的范围冲突。历史代码配置、未来查询获取和 held-out 请求泄漏均未由这条记录建立。§7 中的具体 transfer 条件应单独评估，不能用一条 direct 标签概括整篇。

## Overcoming the Retrieval Barrier

USENIX Security 2026 最终版 §2.1（PDF 第 4 页）把 query 明确设为给定输入。黑盒限制针对 corpus 内容及模型参数。§4.1 给定查询的评估与这一设定相符，§5.2 的 agentic 示例另有离线 FAQ 和代理重写查询的条件。 [§2.1](https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=4) · [§4.1](https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=6) · [§5.2](https://www.usenix.org/system/files/usenixsecurity26-chang-hongyan.pdf#page=11)

当前 JSON 第 520–592 行已经将给定查询范围内一致与未来查询来源缺口分别记录，这一判定可以保留。TeX 第 280 行也承认给定查询假设，主要差别是第 263、278 行的 Inconsistency 标题容易把部署时来源未证实写成正式权限违反。来源缺口应保留，其存在不改变给定输入基准本身的权限条款。

## WebTrap 与新附件的证据层级

WebTrap arXiv:2605.08310v1 §4.1 限定受限区域内部结构的知识。已有本地 `papers/WebTrap/replication/THREAT_MODEL_CODE_ALIGNMENT.md:3,53–71,76–82` 记录固定公开版的静态路径和两例最终生成请求，并保留历史运行与 ASR 影响的限制。TeX 第 339–345 行和 JSON 第 781–843 行的构造差异结论相符。20 例是公共实现/数据的静态范围，两例是实际存档请求核查范围。 [论文 §4.1](https://arxiv.org/html/2605.08310v1#S4.SS1)

中文说明第 101、127 行依据行为实验未完成而将总体列为候选。这不足以消除已记录的源码/请求差异，也不足以证明它抬高论文 ASR。应把构造边界和行为效应各自记录。新附件中的行为实验数值未在这次核查中重新对照底层数据。

## ICoA：来源相同的身份字段不等于直接读取系统提示

EMNLP 2026 最终版 §2（PDF 第 3 页）排除系统提示和工具定义的访问。§4.1（第 5 页）要求所用身份与系统提示中的用户匹配；Appendix B 也明确列出身份作为构造输入。前者是访问来源限制，后者是值的关系，不能直接据此认定发生了被禁止的读取。 [§2](https://aclanthology.org/2026.emnlp-main.2035.pdf#page=3) · [§4.1](https://aclanthology.org/2026.emnlp-main.2035.pdf#page=5) · [Appendix B](https://aclanthology.org/2026.emnlp-main.2035.pdf#page=12)

当前 JSON 第 850–946 行将直接读取和 benchmark 常量来源拆开，这个范围区分正确。它引用固定作者 commit `e333be8e1c319be3deb6942692aaed8e640a3954` 的 `src/agentdojo/attacks/icoa.py:41–49` 与 `src/agentdojo/data/system_messages.yaml:3`；本次网页读取这两个 raw URL 失败，所以这里将该调用边界记录为既有静态审计证据，没有冒称重新取得源码字节。论文原文能独立证实身份匹配的要求，不能独立补足实际读取路径或身份合法来源。建议继续保留 `insufficient_evidence`，不将常量相等改写成已确认的系统提示读取。 [固定构造文件](https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/attacks/icoa.py#L41-L49) · [固定配置](https://github.com/yslmoment/ICoA/blob/e333be8e1c319be3deb6942692aaed8e640a3954/src/agentdojo/data/system_messages.yaml#L3)

## AgentDojo / ASB：评估问题作为信息边界误报控制

### 原文与本地核查范围

AgentDojo 固定为 NeurIPS 2024 最终版（并以 [arXiv:2406.13352v3](https://arxiv.org/html/2406.13352v3) 核对正文）。§3.3 允许不同程度的攻击者先验知识；§3.4 分别定义 benign utility、utility under attack、targeted ASR。内容覆盖使任务难以完成可以影响效用解释，但不自动构成某个被禁止的用户信息流。 [最终论文](https://papers.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf) · [§§3.3–3.4](https://arxiv.org/html/2406.13352v3#S3.SS3)

本地可读的框架实现位于 `repository/aspi-continuation-compatibility-v1/papers/ASPI/upstream/agentdojo-0.1.35/`，它是 ASPI 保存的依赖副本，不能自动代表 AgentDojo 2024 历史实验配置。`agentdojo/agent_pipeline/tool_execution.py:66–74,103–115` 只执行最后一条 assistant 消息提出的工具调用；`agentdojo/benchmark.py:319–358` 单独汇集无注入任务的 utility/security 结果。本次未找到支持附件第 40 行具体百分比的完整 AgentDojo 旧审计或原始运行，不能将依赖源码当作该百分比的复现证据。

ASB 固定为 ICLR 2025 最终版，arXiv 身份为 2410.02644。§3.2（PDF 第 4 页）规定攻击目标和能力；Table 4（第 8 页）和 Appendix C.2.3（第 26–27 页）说明 ASR、PNA 等指标；Appendix C.2.5（第 28–29 页）解释模型输出解析及模拟工具实现。一次恶意工具调用究竟由模型选择还是由 harness 插入，是执行来源与测量问题，需要单独追踪。原文的工具目标指标不提供“用户请求被构造者违规读取”的推论。 [最终论文](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf) · [指标补充](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf#page=26) · [作者仓库](https://github.com/agiresearch/ASB)

本轮没有定位到 ASB 的本地固定作者 checkout、对应强制执行审计或原始日志。附件第 59 行的 `73.58% → 9.25%` 因而仍是未核实报告，不能作为已确认 ASB 缺陷、效应大小或信息边界 violation 的 gold。若后续取到调用日志，应记录模型原始 action、harness 重写/附加 action 和评分事件三个边界。

### 可测试的负例

以下是防止错误归因的测试目标，均不声称整篇论文已证明无问题，也不需要重新运行攻击：

| 控制 ID | 提供的证据 | 应有结果 |
|---|---|---|
| `agentdojo_utility_perturbation_only` | 只有“注入覆盖了完成任务需要的工具内容”以及 utility 差异；没有禁止的信息访问条款和构造流 | 不得输出已确认的信息权限不一致；记录效用/评估范围问题，信息边界保持证据不足。 |
| `asb_harness_action_attribution_only` | 只有模拟 harness 插入动作的报告或日志；没有用户私有信息进入构造端的边 | 不得把执行来源问题转成 query/context 越界；可以另列协议/指标缺陷候选。 |
| `asb_quantitative_claim_without_run` | 只有附件两个 ASR 数值，没有配置、分母和原始运行 | 将数量结论标为未核实，不从数值差直接生成任何权限 violation。 |
| `icoa_equal_identity_different_source` | 已知某常量与系统提示身份相等，但未见直接读取 | 对系统提示读取边保持证据不足；身份来源另立观察，不合并 source。 |

这里的“负例”是针对错误的信息边界判定。若 schema 只允许现有四种 verdict，缺少规则或缺少对应 observation 时应保留 `insufficient_evidence`，不能为了阴性计数填造 `absent` 或 `allow`。

## 对自动审计 gold 的要求

当前人工结果能校验规则实现是否按所给输入工作，不能独立证明 gold 解释正确。AGENTCON 需要区分代表性 source 请求、同请求 direct 诊断和未来 target 请求，并明确优化过程与模型生成器的接收边界。LIAR 需要纳入具体 source-training 授权，在没有对象级证据时保留 target-access 的未知状态。修正这两类范围绑定后，才能用它们判断自动提取器是否产生了误报。

## FHA 补充裁定：single-payload 诊断范围改变旧标签依据

**证据身份与本次操作。** 本节为 2026-11-19 的追加复核，优先于上文 FHA 节对 direct 实验的既有判断。只读了本地固定论文提取及其引用视图，没有额外调用模型或执行攻击。两个 prepared 文件都记录来源 `https://arxiv.org/pdf/2604.20994v2`、PDF SHA-256 `a418013dac0ff58898aa832f682702b1cf1c605f8edc2f05446b2035c2bbcccc`、41 个页段和同一 source binding `4f6146cfccfd5700712b1a2f91d019194296046c89122f7185d3be6baa2cee1d`。论文页眉标为 TMLR 08/2026，arXiv v2 日期为 2026-08-31。本节页码指 PDF 实际页码及对应的 `pN` 段。

本地读取位置：

- `analysis/threat_model_auditor/outputs/2026-11-19-v3-document-study/fha/prepared.json`，`segments[p4,p5,p6,p7,p12,p13,p14,p15,p23,p39]`。
- `analysis/threat_model_auditor/outputs/2026-11-19-v3-citation-replay/fha/prepared.json`，相同段的 `reading_order_text`；它与前一份记录相同 PDF 身份，本次另用该视图核对 §4 与 §6 的完整衔接。
- `extraction.json`、`review.json` 仅用于定位待核问题；以下结论依据 prepared 中的论文段落，不把自动模型意见作为原文证据。

**single-payload direct 不能继续直接标 confirmed。** PDF 第 4 页 §4 确实排除攻击者访问用户 prompt，并描述离线投放。第 5 页将单 payload 定义为带有具体查询的上下文；第 23 页 Appendix B.1 又明确将该查询置入构造过程，因此 query-conditioned construction 的 `delivery=confirmed` 仍有程序性证据。然而，第 6 页 §4 在转向主要 universal 配置时，明确把 §6 的单 payload 实验称为 “initial diagnostic”，并限定为 “rather than as a deployable attack”。第 7 页 §6 开头再次解释这些实验用于识别影响因素，而非独立提出的攻击配置。这是论文自己给出的实验用途和范围限定，不能像旧 case 那样只保留一般 no-prompt 条款和 direct 输入就认定同一部署契约已被违反。 [§4 权限，p4](https://arxiv.org/pdf/2604.20994v2#page=4) · [配置定位，p6](https://arxiv.org/pdf/2604.20994v2#page=6) · [§6 开头，p7](https://arxiv.org/pdf/2604.20994v2#page=7) · [Appendix B.1，p23](https://arxiv.org/pdf/2604.20994v2#page=23)

建议把现有 `fha_direct_exact_query` 修为 **unresolved / insufficient_evidence**：保留 `issue_type=information_boundary`、`delivery.status=confirmed`、`evidence_kind=paper_procedure`、`task_relation=same_evaluated_instance`；将 `policy_application.status` 从 `applicable` 改为 `uncertain`，同时引用 p4、p6、p7，解释一般部署预算与知情诊断范围的关系。`refutation.basis=none`：这条限定足以阻止直接确认部署预算违反，但没有必要据此制造一个覆盖整个 FHA 的显式查询授权，或宣称所有知情诊断天然豁免。如果 claim 仅为“论文把该单 payload 结果当作无查询部署结果”，p6 是相应反证；它与原有“所有单查询构造均已违规”的 claim 也须分别写明。

**固定查询、多 payload 鲁棒性实验必须另案。** 第 6 页也把位置/函数数量变化列为 universal 的训练配置；第 14 页 §7 的 multi-payload robustness 小节明确固定一个查询、改变工具列表，第 15 页继续报告对位置及数量扰动的鲁棒性。这不是 §6 单 payload 实验，因而不能把 p6 专门指向 §6 的诊断限定直接扩展到它。其查询参与训练和同查询评估具有程序性证据；但它同时被描述为训练和鲁棒性分析，尚不能仅从“没有再重复豁免”就认定作者将该已知训练查询当作未知未来请求取得。建议新增独立 case（例如 `fha_fixed_query_multi_payload_robustness`），记录 `delivery=confirmed`、representation 为 query-conditioned optimization、`policy_application=uncertain`、`refutation=none`，保持 **unresolved**，并明确待解决的是该特定鲁棒性实验是否被主张满足 no-user-prompt 的部署预算。它保留疑点，而非被上一段一并排除。 [配置列表，p6](https://arxiv.org/pdf/2604.20994v2#page=6) · [固定查询多 payload，p14](https://arxiv.org/pdf/2604.20994v2#page=14) · [鲁棒性结果，p15](https://arxiv.org/pdf/2604.20994v2#page=15)

**训练与 held-out 控制的界限。** 第 13 页 §7 的 deployment 小节明确安排 Arguments variation 训练和 Formulation diversity 的 held-out 测试，并将 Table 3 直接称为训练集结果；第 14 页 Table 4 和第 39 页 Appendix L 分别报告已训练产物在未见查询批次上的迁移。这能反驳“训练时使用 source 查询本身必然违规”的笼统主张，也提供所述 transfer 程序没有把目标测试查询作为训练输入的正面程序性证据；证据层级仍是 paper procedure。后续选择、停止条件、重复优化及精确字符串重叠是否接触测试数据，不由这些段落穷尽，不能扩张成对所有历史实现或所有测试泄漏路径的 `absent`。 [训练/测试区分，p13](https://arxiv.org/pdf/2604.20994v2#page=13) · [held-out 测试，p39](https://arxiv.org/pdf/2604.20994v2#page=39)

**本轮建议的实际修正。** 旧 direct single-query 的 confirmed 标签应撤下，保留已经确认的构造依赖；固定查询多 payload 不自动豁免，另建 unresolved case；明确披露的 source-training 和指定 held-out transfer 可以作为各自有限程序范围的控制。FHA 的论文级覆盖仍不完整，不能因为有这些控制而输出“整篇无信息问题”。本轮只追加本文，没有修改 case、paper manifest 或历史结果，也没有以自动模型意见替代底层原文。
