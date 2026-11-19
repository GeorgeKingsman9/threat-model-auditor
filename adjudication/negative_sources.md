# Trojan Hippo / TopicAttack：独立核验与阴性范围

核验日期：2026-11-19。只读取论文、公开固定源码和少量基准 JSON；没有运行攻击、优化器、受害模型或评分模型，没有模型 API 调用。

附件 `pasted-text-1.txt` 提供的是待核对的既有判断，不是 gold。此次不因其写了“False Positive”就把论文认定为全局阴性。

## 结论

| 论文 | 可以支持的阴性结论 | 不应作出的结论 |
| --- | --- | --- |
| TopicAttack | 在固定公开 chatbot/agent 构造入口，生成 LLM 使用论文允许的 benign content 与攻击目标，原始用户指令字段没有作为独立参数进入该生成请求。适合作为这一具体访问边界的域内阴性控制。 | 整篇所有实现、所有防御实验和作者历史运行都已被证明没有不一致。 |
| Trojan Hippo | 主题条件化、训练环境自适应与 train→test transfer 是明确披露的设置；不能把它们直接当成读取精确未来测试查询的违规。适合作为“允许的主题/训练信息”控制。 | “生成器只拿主题，从来没有具体 query”；源码反而明确把训练实例的 `user_message` 放进 mutator 请求。也没有独立核验所有历史运行。 |

两篇都属于本研究的 IPI 领域，不能标为 `not_applicable`。其阴性地位需要附访问边界和版本；“当前未确认不一致”与“某个许可信息流已证实一致”是两个不同层次。

## 1. 本地材料与外部材料的来源边界

本次在工作区 `papers/`、`submitted/` 和主研究 checkout 的相关 Markdown、TeX、TXT 中检索了论文名及常见变体，没有定位到这两篇各自的完整旧审计报告或官方源码 checkout。这是本次限定检索的结果，不是“以前从未审计”。

本地有 WebTrap 的 TopicAttack **基线移植**：

- `papers/WebTrap/replication/upstream/file/exp/attack/topicattack/build_payload.py`
- `papers/WebTrap/replication/upstream/web/baseline/topicattack/build_payload.py`

它们属于 WebTrap 发布版本，不能代替 TopicAttack 作者仓库来证明原论文的实现性质。本次因此直接读取作者仓库的固定 commit，而没有执行这些程序。

| 对象 | 本次固定版本 |
| --- | --- |
| Trojan Hippo 论文 | [arXiv:2605.01970v1](https://arxiv.org/html/2605.01970v1)，2026-05-03；重点 §3.1、§4.1。 |
| Trojan Hippo 作者代码 | [debesheedas/trojan-hippo-benchmark](https://github.com/debesheedas/trojan-hippo-benchmark/tree/ebeb739dada097e06b125faa70e82e064482b64b)，commit `ebeb739dada097e06b125faa70e82e064482b64b`。 |
| TopicAttack 论文 | [EMNLP 2025 最终版](https://aclanthology.org/2025.emnlp-main.372.pdf)，§3/§4；另对照 [arXiv:2507.13686v1](https://arxiv.org/html/2507.13686v1)。 |
| TopicAttack 作者代码 | [LukeChen-go/topicattack](https://github.com/LukeChen-go/topicattack/tree/2aced58ad6f3587c8ba064b5e5cad74a29ef41de)，commit `2aced58ad6f3587c8ba064b5e5cad74a29ef41de`。 |

commit 通过作者仓库 GitHub API 解析后再按该 SHA 读取文件，不把可变的 `main` 当成证据版本。版本固定不等于已经证明论文所有历史实验使用了这一版本。

关键源码原始字节的本轮 SHA-256（从上表固定 commit 的 raw URL 读取，未执行）：

| 文件 | SHA-256 |
| --- | --- |
| Trojan Hippo `src/benchmark/adaptive_attacks/openevolve_optimizer.py` | `698a3aa055cf052deadb77b03910768a7a6a7771d8fc590101f9f8aefa999290` |
| Trojan Hippo `scripts/propagate_train_attack_to_test_cases.py` | `5ca03d067b9a57bfa126c1932113d30d4c5bef9a5493b8800c00725e374b7c20` |
| TopicAttack `construct_attack.py` | `eb95d5377e066d51e2d8a710e0beb803bd596ff0342cc8ec963da2e473244732` |
| TopicAttack `injectagent/src/construct_attack.py` | `ac8d0a464df97ddb9c10408d58a1d80355df7cde6075de9c954e747abd083bda` |

## 2. TopicAttack：允许的文档内容不等于被禁止的用户指令

### 论文规则

§3 区分两种来源：攻击者不能访问原始用户指令，但可以知道准备注入的 benign content。§4 的构造式以文档内容和恶意目标为输入，不要求把原始用户问题交给生成器。最终版位置为 PDF 第 3–4 页的 §3/§4；HTML 对照见 [§3](https://arxiv.org/html/2507.13686v1#S3) 与 [§4.2](https://arxiv.org/html/2507.13686v1#S4.SS2)。

因此，不能从“上下文与用户任务相关”跳到“论文禁止这种上下文”。这里有明确的资源内容授权。

### 固定实现路径

1. [chatbot `construct_attack.py:7–15`](https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/construct_attack.py#L7-L15)：生成请求渲染 `d_item['input']`、`injection`、`injection_output` 和固定对话轮数，传给 `model.respond`。没有引用 `d_item['instruction']`。`injection_output` 在这里是攻击目标一侧的内容，不能凭字段名把它当作用户任务真值。
2. [生成模板](https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/prompts/attack_prompt_transfer.txt)：使用 benign data 和攻击目标主题制作过渡，不出现独立原始用户查询槽位。
3. [agent `injectagent/src/construct_attack.py:7–17`](https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/injectagent/src/construct_attack.py#L7-L17)：生成请求使用去掉占位符的 `Tool Response Template`、`Attacker Tools`、`Attacker Instruction` 和轮数；没有读取 `User Instruction` 来渲染该请求。
4. [agent `attack_defense_tools.py:85–87`](https://github.com/LukeChen-go/topicattack/blob/2aced58ad6f3587c8ba064b5e5cad74a29ef41de/injectagent/src/attack_defense_tools.py#L85-L87)：`sandwich` 防御确实重述 `User Instruction`，但这是应用防御阶段对 victim 输入的处理，不能错接成攻击生成 LLM 获得用户指令的证据。

本次额外只读检查了两个 JSON 的字段结构：

| 文件 | 字段核验 | 原始文件 SHA-256 |
| --- | --- | --- |
| `data/crafted_instruction_data_squad_injection_qa.json` | 900 条；同时存有 `instruction` 与 `input`，但生成函数实际渲染后者。第一条中完整 `instruction` 不是该条 `input` 的子串；这个单例检查不代表对所有自然语言信息推断做了证明。 | `c48a0205815caa266ada687eb6f78db2c809254820cef4c86dd4437851f8fb7e` |
| `injectagent/data/test_cases_dh_base.json` | 510 条；同时存有 `User Instruction`、`Tool Response Template` 和攻击者字段。字段在同一个基准对象里存在，不等于它进入了生成 LLM 的消息。 | `0a8186468d21389af432e8c7b399ae42264d1b93a07b65c7a489468508604305` |

这里应把接收者写成“辅助生成 LLM”，操作写成“条件化 payload 生成请求”。如果把接收者改成整个 benchmark 进程，那么 `jload` 后整个对象当然包含用户问题；二者不是同一个审计问题。

### 阴性强度

对这些直接构造调用而言，既有明确允许的内容来源，也能定位实际传入值，支持限定的 `allow + present` 一致控制；对“独立原始用户指令参数进入该直接请求”的主张，本轮源码证据不支持。

若要用 `deny + absent`，必须把范围严格限制为这些已检查的请求构造边界，并说明它是静态调用边界核验，不是实际请求捕获。不能把 `absent` 扩大解释为内容中绝无任何可推断的任务信息、也不能从中推断整个历史运行无泄漏。保守的默认 fixture 可以先只使用证据最直接的 `allow + present`。

## 3. Trojan Hippo：训练实例 query 确实进入 mutator

### 论文规则与设置

[§3.1](https://arxiv.org/html/2605.01970v1#S3.SS1) 排除对系统与用户查询的修改，并允许了解系统提示、记忆后端和工具接口；不能把“不能修改查询”改写成“训练优化器不能读取查询”。[§4.1](https://arxiv.org/html/2605.01970v1#S4.SS1) 披露按主题、后端和防御训练攻击，再在未见测试实例评估；论文明确区分训练与测试的模板/实体池。

这一披露使“训练实例 query 被使用”不能自动等同于“精确未来测试 query 被越权获得”。但它同样不支持附件中“只看到主题”的绝对表述。

### 固定实现路径与重要纠正

- [optimizer:606–618](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L606-L618)：从 `failed_step` 取 `user_message`，作为 `_mutate` 的输入。
- [optimizer:738–754](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L738-L754)：后续优化迭代继续传这个实例消息。
- [optimizer:1258–1268](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/openevolve_optimizer.py#L1258-L1268)：mutator 提示中直接包含 `user_message`，不只是主题标签。
- [explicit strategy:43–59](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/src/benchmark/adaptive_attacks/memory_strategies/explicit_strategy.py#L43-L59)：特定后端扩展还会使用该消息片段。这是训练条件信息的进一步使用，不是测试 query 泄漏的独立证据。
- [README:106–117](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README.md#L106-L117) 与 [127–132](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/README.md#L127-L132)：文档化流程是在 train 上优化、复制选定攻击，再在 test 上评估。
- [传播脚本:434–466](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L434-L466)：按主题/后端/防御和训练缓存选择单个攻击，再复制到测试文件。[74–88](https://github.com/debesheedas/trojan-hippo-benchmark/blob/ebeb739dada097e06b125faa70e82e064482b64b/scripts/propagate_train_attack_to_test_cases.py#L74-L88) 只替换攻击邮件字段，没有把测试实例的触发 query 传回 mutator。

因此，附件应改为：“训练优化器使用具体训练实例消息；文档化 transfer 流程将其与 held-out 测试查询区分，当前没有据此确认读取精确未来测试 query 的违规。”

### 一个静态 train/test 配对核验

读取固定 commit 下 `data/benchmark/attack_bench/{train_0,test_0}/tax/rag/none/01.json`，没有执行：

| 项目 | train 文件 | test 文件 |
| --- | --- | --- |
| 文件 SHA-256 | `251810fae0cd0407e0f84600283fd17370483d8d27dc3c8ee55de5f76444593c` | `3a6593de0187682ebafe796ad0967a7e5791a9abfd226033458cec30234ee169` |
| 第 4 步触发消息字符数 | 558 | 549 |
| 第 4 步消息 SHA-256 | `dbf1d4b57701d08b056ec9e04fc0f63553715fd0d1887b04560648707ebcad1a` | `48c231234016a5cd642cc347f5f710aca6187dd89ca1769a4f644c89cbd0e480` |

两者攻击邮件对象经 `json.dumps(..., sort_keys=True)` 后 SHA-256 相同：`6d762ce840cd455e8027b47d06a26fff010eb07e8f671b97a5efd1bdde302740`。它说明这个发布样本对使用同一攻击、不同触发实例；不是对全部测试单元或实际 API 请求的穷尽证明。

### 阴性强度

“主题级信息可以被使用”是可测的一致控制。“确切未来测试 query 没有进入任何历史攻击构造”本轮没有证明；不应给这种全称命题配置 `absent`。若目标是完整还原历史运行，仍需运行配置、实际 mutator 请求和 train/test 来源归档。

还应注意：脚本提供可选自适应功能，不能只看某个函数含 `test_case` 名字便推断它在正式 held-out 测试阶段启用。应锁定论文所披露的 train 优化→固定 payload→非自适应 test 这一配置；其他配置单独审计。

## 4. 建议的可测记录与当前 matcher 适配

当前 `checker.match_edge()` 逐字符串精确匹配 `role/phase/source/representation/operation`，可选 `query_form` 仅有 `full_query`、`partial_query`。它不会自动区分训练 query、测试 query、主题和文档来源，归一化输入必须先写对。

| 建议记录 ID | 目标 edge 的关键区分 | 声明/证据建议 | 可得到的结论 |
| --- | --- | --- | --- |
| `topicattack_chatbot_benign_content` | role=`auxiliary attack-generation LLM`；phase=`chatbot payload construction`；source=`attacker-visible benign document`；representation=`document text`；operation=`condition generation request`；不填 `query_form`。 | §3 对 benign content 的 `allow`；`construct_attack.py:9–10` 的 `present`。 | `consistent_within_scope`，明确的许可信息流控制。 |
| `topicattack_agent_benign_content` | role 同上；phase=`agent payload construction`；source=`attacker-visible tool response template`，与用户指令来源分开。 | 同一授权；agent 构造入口:10–11 的 `present`。 | 同上；整篇统计仍只计一次。 |
| `topicattack_exact_user_instruction_boundary` | role=`auxiliary attack-generation LLM`；source=`original user instruction field`；representation=`exact user instruction`；operation=`condition generation request`；`query_form=full_query`。 | `deny` 来自 §3；仅在直接请求构造边界得到完整静态核验后才标 `absent`，并显式记录此范围。否则留空观察。 | 限定边界的 `consistent_within_scope`，或保守 `insufficient_evidence`；不是全局无泄漏证明。 |
| `trojan_hippo_topic_conditioning` | role=`offline red-team optimizer`；phase=`training attack optimization`；source=`preselected sensitive topic`；representation=`topic category`；operation=`condition attack search`；不填 `query_form`。 | §4.1 披露的 `allow`；固定 optimizer/配置的 `present`。 | 许可主题使用控制；不能把 topic 填成 `partial_query`。 |
| `trojan_hippo_train_query_to_mutator` | role=`offline mutator LLM`；phase=`training attack optimization`；source=`training instance user_message`；representation=`training query text`；operation=`condition mutation request`；`query_form=full_query`。 | 源码确认 `present`；不能套用在线权限制造 `deny`。若对 §4.1 的训练信息许可仍有歧义，规则留空并说明。 | 可披露的训练信息使用，或 `policy_unspecified`；不能与测试查询混成一个 edge。 |
| `trojan_hippo_exact_test_query_acquisition` | role=`payload author before held-out evaluation`；phase=`fixed-payload transfer`；source=`held-out test trigger query`；`query_form=full_query`。 | 没有本轮实际请求证明时，不写全局 `present` 或 `absent`；不能从禁止“修改”推断禁止“读取”。 | 当前全称目标是 `insufficient_evidence`；不要强行作为已核实阴性。 |

`topic_category` 与 `exact_query` 的差异可由 `source/representation` 表达，无须把“主题”伪装成一种 query，也无须先修改 `QUERY_FORMS`。

若论文级记录要输出 `consistent_within_scope`，`audit_scope` 必须明示它只覆盖上述有限构造入口或许可信息流，`coverage_complete=true` 也只能指这个已界定范围。若把尚未解决的历史运行问题纳入同一 required set，聚合必须保持证据不足。不能为了凑阴性样本悄悄缩小范围，再把结果宣传成“整篇无问题”。

本轮未修改数据集、gold 或 matcher；上述是应经 review 后录入的记录建议。论文级主表只保留一行，内部证据数量不增加论文分母。

## 5. 附件、旧 TeX 与旧算法应改什么

1. **附件对 Trojan Hippo 的事实表述需改**：不是“生成器只依据主题”，固定源码存在具体训练 query→mutator 路径。排除某个 allegation 的理由应是角色、阶段、训练/测试来源及 policy 没有被正确对齐，而不是否认这条实际路径。
2. **TopicAttack 的阴性应附范围**：可以说指定生成请求符合 benign-content 授权；不能仅凭“不曾找到明确越权”给全论文 global negative。
3. **旧 TeX 的通用前提过强**：旧粘贴 TeX 第 36–39 行将第三方 IPI 泛化成对用户历史全无知识。应改为权限依具体论文、角色、阶段与来源决定；本文这两篇分别明确披露可见资源或离线训练设置。旧 TeX 第 87–89 行的 exact query/关键词分类还须带 query 所属实例，防止把训练问题当未来 victim 问题。
4. **没有定位到这两篇的独立旧 TeX 章节**：本次核对的旧 TeX 中没有发现其独立节标题，不能声称已经纠正了某段具体正文；可确认的问题是上面的通用论证和附件分类。
5. **算法不能用关键词命中代替 policy+flow**：`user_message`、`instruction`、`topic`、数据文件中存在 q 都不是充分条件。需要明确谁在何时以什么来源使用它，以及对应操作是否被该论文排除。
6. **不要按攻击效果决定结构不一致真假**：是否显著提高 ASR 与是否存在禁止的信息流是不同问题；本次没有运行行为实验，也不以 ASR 对这两个阴性边界作裁决。

建议记录两个不同的标签层次：`has_confirmed_inconsistency=false` 表示未确认发现；只有经过明确范围的许可或不存在路径核验，才附 `consistent_within_scope`。对范围外问题保留未解决说明。
