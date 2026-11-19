# 已完成 v2 控制组基线：独立证据判读

判读日期：2026-11-19。只读本次已经完成的 `prepared.json`、`extraction.json`、`review.json`、`result.json`，逐条核对引用与结果；没有读取 gold 来决定结论。新增推理调用 0，攻击运行 0，push 0。本文不改写基线文件，也不把后续人工源码核验混入原始模型输入。

`pN` 指 `prepared.json` 的 PDF 页 segment。文中的 `[start:end)` 是 Python 字符串索引，结束位置不含在内，不是 PDF 坐标或字节偏移。

## 1. 四篇的实际基线状态

下列路径均相对于 auditor 仓库的 `outputs/`。

| 论文 | 已完成基线路径 | 原始论文级结果 | 独立裁定 |
| --- | --- | --- | --- |
| Trojan Hippo | `2026-11-19-controls-baseline-long-documents/trojan_hippo/` | `inconsistent`，`has_confirmed_inconsistency=true` | 对“论文攻击者信息权限不一致”而言是一次算法误报；触发项把受害者安全目标当成攻击者知识限制。 |
| ASB | `2026-11-19-controls-baseline-long-documents/asb/` | `insufficient_evidence`，`false` | 本轮没有确认的信息边界发现；有引文失败、不同攻击臂与另类协议问题，不能自动裁定整篇阴性。 |
| TopicAttack | `2026-11-19-controls-baseline/topicattack/` | `insufficient_evidence`，`false` | 没有误报成不一致；其政策句被重复充当 absence，且该句实际未通过定位。其余未知项部分属于非攻击者角色。 |
| AgentDojo | `2026-11-19-controls-baseline/agentdojo/` | `insufficient_evidence`，`false` | 没有误报成不一致；基线正确保留了一些角色区分，但混入防御者/评分器的未声明权限使论文汇总不足。 |

四项 `status` 都是 `completed`，说明处理流程完成，不等于其判定均正确。内部六条 flow 仍只是每篇的一组证据，论文分母为 4。

| 论文 | 内部 `inconsistent` | 内部 `consistent_within_scope` | 内部 `insufficient_evidence` |
| --- | ---: | ---: | ---: |
| Trojan Hippo | 1 | 2 | 3 |
| ASB | 0 | 2 | 4 |
| TopicAttack | 0 | 1 | 5 |
| AgentDojo | 0 | 4 | 2 |

这是对保存结果的清点，不是检测准确率、FPR 或未见论文性能。

## 2. Trojan Hippo：确实是一例信息边界算法 FP

### 实际触发的 flow

原始 `trojan_hippo_flow_5`，对应 `extraction.flows[4]`，不是训练/未来 query 来源问题：

- 接收/执行角色是 **target agent**；阶段是 baseline delayed activation。
- 信息是敏感用户消息，操作是未经同意把完整消息发给攻击者。
- 模型把 p5 的安全属性标为 `deny`，把 p22 的发送成功标为 `present`。
- 第二次模型复核 `flow_reviews[4].supported=true`，重复支持了这一解释。
- 两个引用都通过精确定位：声明为 p5 `[155:181)`，实现为 p22 `[2402:2426)`；`citation_errors=[]`。
- 原规则因 `deny + present` 返回 `forbidden_flow_confirmed`，论文聚合遂给出 `inconsistent`。

短语“without the user’s consent”和“Email sent successfully!”确实位于原文，所以这不是捏造引文或定位失败。

### 上下文揭示的语义类型错误

安全属性的前半句位于 p4 末尾、后半句续到 p5。该段主语是防御应当维持的安全性质，即攻击者不应借外部内容诱导外传用户信息。它描述**希望防御保住的安全目标**，并非限制攻击构造器“不能拿到某类信息”。

p22 的 Figure 11 图注明确把示例定位为 Finance、Mem0、**无防御**；相应位置在该页约 `[4076:4095)`。示例展示攻击成功，正是论文所研究的漏洞现象。攻击违反受害者的安全目标，不等于作者在实验中偷偷赋予攻击者被论文排除的先验知识。

另一个 p8 的 IFC outbound blocking 规则属于不同防御臂，不能拿来禁止无防御示例中的发送。基线把这条 IFC 规则单列为 `trojan_hippo_flow_6`，但没有阻止 flow_5 中的安全目标类型混淆。

**正式裁定**：`trojan_hippo_flow_5` 作为信息边界型论文不一致发现应撤销；仅由它支持的本次论文级 `inconsistent` 是误报。保存的攻击成功示例不需要被否认，也不需要重新运行。

这项裁定不证明 Trojan Hippo 全篇无其他问题。在线 observability、离线 critic 访问、IFC 标签表述和历史运行来源是不同待审目标；本次误报的撤销不对它们自动给出阴性结论。

### 可测修正

将原触发项保留为回归输入，但增加明确类型：`issue_type=security_outcome`、`policy_kind=victim_security_goal`。其 paper-text procedure 可以确认论文报告了外传，但不能进入攻击者知识约束的 `deny + present` 确认分支。

修正后的必要断言是：

1. 即使两个引文完全可定位、语义复核返回支持，这个受害者安全目标仍不能产生 `confirmed_inconsistency=true`。
2. 结果明确记下“问题类型不同”，不能把真实外传重写成 `absent`。
3. 相邻对照中，若真正适用于同一角色/阶段的攻击者知识禁止，与受绑定路径支持的实际交付同时存在，仍须能确认不一致。
4. 不能用“offline”或“训练”作通用免责标签；确实适用于训练攻击者的明确禁止仍可能被违反。

这些断言可离线重放原始提议、复核和文档检查，无需新推理。

## 3. TopicAttack：政策不能同时变成实现缺失的证明

### 基线逐项核对

| flow ID | 保存结果及原文位置 | 独立判读 |
| --- | --- | --- |
| `topicattack_flow_1` | `policy_unspecified`；声明与实现引用完全相同，均指定 p4，精确匹配次数均为 0，两个 locator 都缺失。 | 把方法段“原用户指令不可见”的同一句声明同时当成 `deny` 和 `absent`，存在证据自证问题；本轮定位失败先阻止了这一推断。 |
| `topicattack_flow_2` | `permitted_flow_confirmed`；许可定位 p4 `[675:707)`，生成提示定位 p13 `[468:503)`。 | benign content 被明确允许并用于过渡构造；这是一个有限、正面的许可一致控制。 |
| `topicattack_flow_3` | `no_matching_observation`；system-prompt 禁止定位 p3 `[5501:5549)`，没有实现观察。 | 保留不足合理，不能从论文没给实现验证反推出 `absent`。 |
| `topicattack_flow_4` | `policy_unspecified`；p7 `[4704:4743)`描述 GCG/AutoDAN 比较。 | 梯度比较臂不是 TopicAttack 主方法，不能把主方法无梯度权限直接移植过来制造冲突。 |
| `topicattack_flow_5` | `policy_unspecified`；attention 分析引用在 p8 精确匹配为 0。 | 即使修好引文，读取注意力的是 evaluator；它不能成为攻击者获得查询或模型内部状态的交付证据。 |
| `topicattack_flow_6` | `policy_unspecified`；Sandwich 重述指令位于 p12 `[5410:5451)`。 | 原指令由 defender 用来构造 victim 输入，不等于攻击生成器可读该指令。 |

`flow_1` 所引句在双栏提取文本中被换行、断字与另一栏内容打断：p4 约 `[4330:4342)`有唯一的 inaccessible 词，但模型提供的完整短句不是精确子串。故基线 reason 的 `policy_unspecified` 不能解释为“论文没有声明边界”；此处是引用未通过定位。`flow_5` 同样有跨栏/空白的引文不匹配。

### 为什么不能只修字符串就算阴性

把 quote 改短到能唯一定位，只能解决定位问题，不能让同一句权限声明自动成为实际输入不存在的证明。paper-only 结果应标清声明、描述的程序和独立边界证据之间的差别。

此前独立源码核验的默认构造器、模板、wrapper 和空 system prompt 可以作为**后续新增来源**，支持指定默认消息路径的独立用户指令排除；它们没有被传入这次基线模型，因此不能倒填为基线已验证的事实。

**正式裁定**：这次 TopicAttack 输出是证据不足，不是 FP，也不能直接计为“已核实全篇无不一致”。有一条许可一致 flow；精确用户指令排除则需要输入边界证据或更明确的程序证据。

### 可测修正

- 重放保存输出时，两个未定位引文继续给出具体 `citation_errors`；不能为了提高标签匹配而自动接受近似句子。
- 就算换成一条可定位的政策句，若 `implementation` 只是同一政策的重复、没有交付边界依据，也不能据此形成强 `excluded_delivery`。
- 对 evaluator/defender 的输入建立单独角色；不要把这些合法后台读取合并进攻击者 edge，也不把每个后台角色的“未声明权限”都变成目标攻击声明的必答问题。
- 若以后支持规范化空白/断字匹配，必须保留到原始 segment 的位置映射，并单独记录匹配方式；它不能代替语义来源核验。

## 4. ASB：不同攻击臂、引文失败与协议问题应分开

该基线并未确认信息边界不一致。主要情况如下：

| flow ID | 保存结果 | 证据判读 |
| --- | --- | --- |
| `asb_flow_1` | `permitted_flow_confirmed` | p5 `[4435:4453)`的 IPI 定义与 p17 `[2374:2402)`的 observation 修改示例对齐，属于允许的注入表面。 |
| `asb_flow_2` | `policy_unspecified` | 声明 quote 精确匹配为 0；p4 实际在 integrate their 后换行。实现 quote 在 p17 出现 8 次，被判歧义；两者不能被摘要成“未声明允许加工具”。 |
| `asb_flow_3` | `no_matching_observation` | PoT system-prompt 许可引文可定位，但实现引文在指定 p17 不匹配。尚不能把这一格式失败当作不存在实现。 |
| `asb_flow_4` | `no_matching_observation` | p4 `[2909:2936)`明确允许相应 backdoor 角色读取并修改用户提示；实现 quote 跨行，不是精确子串。它不向普通 IPI 攻击者授予同样权限。 |
| `asb_flow_5` | `permitted_flow_confirmed` | p6 的 DPI/IPI 间接 memory poisoning 权限与 p26 的实际 DPI 构造描述在广义操作上相容，但不能宣传已确认 IPI 构造也执行过。 |
| `asb_flow_6` | `policy_unspecified` | p28 的提示提供 demonstration tasks 给 PoT trigger 构造；尚未给出适用于该离线角色的单独权限，不能转写为精确未来测试任务的违规交付。 |

p26 关于执行工具集合的描述，与定义/示例中的攻击工具加入可能有文本或协议张力。它不是这次六条 flow 已确认的信息权限违反，更不能凭模型备注直接证明本地强制工具插入的真实调用过程。

**正式裁定**：原始 `insufficient_evidence` 可以保留为本次文档输入的结果。它不是 ASB“实验协议问题不存在”的反证，也不是全篇信息边界一致的证明。之前附件涉及强制插入、工具选择和 ASR 变化的论断，需要另查源码/运行记录，本次基线没有验证那些数值。

可测修正应分别检查攻击臂映射、精确引文错误、工具增补许可和实际工具选择协议；不要用 `deny` 代替缺失的声明，也不要把未核实的协议问题包装成知识边界发现。

## 5. AgentDojo：后台可见不等于攻击者可见

| flow ID | 保存结果及位置 | 独立判读 |
| --- | --- | --- |
| `agentdojo_flow_1` | `permitted_flow_confirmed`；p4 `[2580:2612)`、p16 `[1697:1731)`。 | benchmark 明确提供 ground-truth 工具调用辅助放置注入。外部攻击者在现实中如何获取它是另一种获取/外推问题，不能抹掉已披露的实验设置。 |
| `agentdojo_flow_2` | `permitted_flow_confirmed`；p6 `[2620:2655)`、p8 `[2579:2606)`。 | 身份信息和姓名消融在相应设置中被允许；不是整条用户 query 交付。 |
| `agentdojo_flow_3` | `permitted_flow_confirmed`；p6 `[2340:2365)`、p7 `[4135:4174)`。 | designated placeholder 注入与网页注入示例对应，不能扩大成控制整个工具返回或全部系统上下文。 |
| `agentdojo_flow_4` | `policy_unspecified`；p8 `[4327:4356)`。 | defender 重复用户指令，不构成 attacker 原始 query 接收。 |
| `agentdojo_flow_5` | `absence_confirmed_at_boundary`；声明/实现均为 p9 `[1510:1545)`同一片段。 | 文本描述工具过滤的先后程序，可支撑“所描述算法先选工具再读不可信数据”；同一程序句不能升级为所有历史运行都验证了严格隔离。 |
| `agentdojo_flow_6` | `policy_unspecified`；p4 `[2995:3024)`。 | utility evaluator 根据输出和环境变化评分；后台评估真值可见性不能当作攻击者真值可见性。 |

**正式裁定**：原始证据不足不是误报，也不能被提升为对整篇的真实阴性。已披露的辅助放置、身份权限和注入表面是有限一致控制。评估器和防御者的权限问题若不属于正在核对的攻击者 claim，应标明关系不适用，而不是凭空增加攻击者禁止条款。

本次没有复核附件中的 task-critical data 覆盖、Utility 提升等实验结果；那类 task-integrity 问题不应由这次文档基线代为证明或否定。

## 6. 对算法改动的共同验收条件

1. **声明类型先于状态组合**：只有适用的攻击者知识约束，才能与同一角色、阶段、来源、表示和用途上的实际交付组成信息边界发现。受害者安全目标与攻击成功不属于这个组合。
2. **来源存在不等于交付**：要求 procedure/static bound path/saved request/runtime 等具体输入边界依据。policy 自述、文档出现某字段或评估器使用它不能独自确认 attacker 交付或排除。
3. **定位与语义两种错误分开**：精确引文失败继续保留其错误；精确定位成功也不能掩盖语义类型错误。Trojan 是后者，Topic/ASB 的部分 flow 是前者。
4. **限定 claim 后聚合**：后台角色、对照攻击臂和与目标无关的安全结果可以保留为记录，但不应自动变成所核信息边界 claim 的阻塞项。真正相关且未解决的权限/路径问题仍须保持不足。
5. **历史基线不可回填**：保留原始模型提议、复核与判定，另输出人工裁定及新版重放结果。新增源码证据、修正抽取规则和新增模型推理必须区别记录。

本次已确认的算法 FP 仅为 Trojan 的这个安全目标误分类；其余三个基线 `insufficient_evidence` 不能凭预设负例身份自动计作正确阴性或漏报。本文不给出四篇控制组的 FPR 数字。

## 7. 固定证据摘要

四组原始模型提示版本相同：`prompt_sha256=bf81c8354772b44e724d75c05b1b326c45dec53dcd34903939f40b49d535b3b2`。原始文档与论文结果文件 hash 如下；这里的结果 hash 对 `result.json` 原始字节计算。

| 论文 | 文档 SHA-256 | 基线 `result.json` SHA-256 |
| --- | --- | --- |
| Trojan Hippo | `4e6fd2911c2ee90279fa6318e14396e2638490917954de9d9ea490caf1111cce` | `02874e1ae1552a6250ced5877cb828b2bf2376e14eb150edcb9208eec7ed341a` |
| ASB | `e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9` | `6657bb55a7b871024ca26b86c3c59a1ba3da069fc48b64b55781a00ba4409f68` |
| TopicAttack | `8e47318c5ddb97326c589c4b35bf602d0deea4077ec1f67856ef0f7317d5f6f7` | `0e0760b464bdbb55e4e0628c1edcf41974251cbb74a5a8c3359442ce338443e2` |
| AgentDojo | `26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913` | `6f3c7929e21dd86d701a4a36383e20758b77890387e2c90919804bb1f45816cc` |

对应公开文档入口（实际定位依据是保存的 `prepared.json`，本轮没有重新下载）：

- [Trojan Hippo v1](https://arxiv.org/pdf/2605.01970v1)，§3.2 安全目标、Figure 11、IFC 防御段。
- [ASB ICLR 2025 final](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf)，§3/§4 与附录实验设置。
- [TopicAttack EMNLP 2025 final](https://aclanthology.org/2025.emnlp-main.372.pdf)，§3/§4、生成提示、attention 分析和 Sandwich 防御。
- [AgentDojo NeurIPS 2024 final](https://papers.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf)，任务/攻击接口、知识消融、评估定义和附录放置辅助程序。
