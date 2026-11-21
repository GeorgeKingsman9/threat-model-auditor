# V7：三类不一致分别取证，一篇论文汇总一次

普通入口只需一个PDF或论文网址。程序自动关联官方源码、固定版本、读取有界证据，再抽取、独立复核和判定；人工审计记录与参考标签不进入运行输入。

若用于Notion中的完整规则说明，见[3条核心判定＋4组通用规则的公式总表](FORMAL_RULES_ZH.md)。下文侧重V7工作流；获取路径的补充建模定义与当前实现限制在总表中分别标明。

```bash
python3 -B scan.py /path/to/paper.pdf --model gpt-6.1-sol --max-calls 6
python3 -B scan.py https://example.org/paper.pdf --model gpt-6.1-sol --max-calls 6
```

## 三条核心规则

仍固定同一范围：

\[
e=(role,phase,source,representation,operation),\qquad
\sigma=(paper\_version,experiment\_arm,artifact\_revision,configuration).
\]

以下各规则都要求原始论文与源码引用通过定位、独立语义复核、角色和分支对齐；模型提案本身不是证据。

| 类型 | 核心对比 | 不能据此判定的情形 |
| --- | --- | --- |
| `knowledge_boundary_violation` 知识边界违规 | 适用的禁止与该接收者的确认交付冲突 | 黑盒标签本身；未提及某信息；评估器收到信息 |
| `construction_contract_mismatch` 构造契约差异 | 明确的输入、生成或来源声明与同范围发布实现不相容 | 文中遗漏参数；未找到生成器；仅凭`shadow/train/question`文件或字段名 |
| `task_acquisition_deployment_gap` 任务获取／部署假设缺口 | 声明场景与实际构造对精确任务知识的依赖之间，有材料性的获取、时序或实例衔接缺口 | 没搜到获取路径；纯离线已知任务实验；已通过允许的同实例观察取得信息 |

**知识边界**保留原规则：

\[
A_K(e,\sigma)\land(\Gamma_{decl}\vdash deny(e))
\land(D_{impl}\models present(e))\Rightarrow I_K(e,\sigma).
\]

`allow/deny`仅表示论文授权；`present/absent/possible`仅表示实现观察。两者不能互相代填。

**构造契约**增加独立规则，不强行把构造过程转换为`deny`：

\[
A_C(\sigma)\land ExplicitContract(P,c,\sigma)
\land IncompatibleSource(C,c,\sigma)
\land DeliveredToConstructor(C,e,\sigma)
\land NoApplicableException(P,c,\sigma)
\Rightarrow I_C(c,\sigma).
\]

这里的“不相容”必须有正面来源／生成／信息精度证据。论文概念可以对应源码多个参数的语义组合，例如完整任务输入中的通用指令与具体问题；需要结合论文的组成定义和源码实际格式化边界核查，不能只比较变量名。若差异依赖“同一评估记录”，还需通过配置、稳定ID、索引及变换链证明该关系。无需用ASR差异代替源码判定。

**部署假设**单列规则，结论是有据的适用性缺口：

\[
A_D(\sigma)\land ClaimedScenario(P,\sigma)
\land TaskConditionedConstruction(C,q,\sigma)
\land MaterialTimingOrInstanceGap(P,C,q,\sigma)
\land Get_{\sigma}(q)=?
\Rightarrow I_D^{gap}(q,\sigma).
\]

其中\(Get_{\sigma}(q)=?\)表示在已命名的声明与实现范围内，必要获取环节的证据状态未确定，**不表示现实中不存在获取方法**。构造依赖、允许知识来源、实际输入来源、时序、任务关系、部署主张和材料性必须分别有证据并复核。单纯缺少一个路径不能触发该规则。

operator把任务交给构造器是实验输入事实，不自动构成攻击者知识授权。反之，允许的观察渠道确已使同一任务在构造前可见，或者论文明确限定离线已知任务时，应保留反证。观察之后的同任务条件化不能仅凭来源未解释就确认部署缺口。

## 论文级汇总

\[
I_{paper}\Longleftrightarrow
(\exists e\in\mathcal O_K:I_K(e))\lor
(\exists c\in\mathcal O_C:I_C(c))\lor
(\exists g\in\mathcal O_D:I_D^{gap}(g)).
\]

\(\mathcal O_K,\mathcal O_C,\mathcal O_D\)是本次固定范围内三类候选集合；范围元组\(\sigma\)本身不是候选集合。

任一类别有确认项，论文级`inconsistency=true`，同时列出`confirmed_issue_types`和具体位置。`knowledge_boundary_verdict`单独保留，因此部署缺口不会被误写成严格知识越权。未审清项继续显示，不会被一条局部发现抹去。

只有所列非空怀疑有反证、三个类别及原有输入覆盖证明义务闭合时，才允许范围内`false`；其他为`null`。这是带类型、带范围的审计，不能理解为整篇所有结论均错误。

当前实现还要求原V6知识边界／输入覆盖结果已为范围内一致，才允许保留论文级阴性；不会仅凭新增C/D被反驳，把原知识轨道的U升级成N。当前D确认分支也限于operator/configuration来源及指定时序组合；其他来源未覆盖不等于已证安全。详见公式总表的实现边界。

## 实现对应

| 模块 | 作用 |
| --- | --- |
| `declared_contract.py` | 只读论文，提出未受信任的声明与任务组成模型 |
| `input_channels.py`、`data_witnesses.py` | 分别寻找问题／文档等输入，提供固定版本的有界数据原文 |
| `extraction_v7.py` | 三类候选的自动映射、独立复核与论文级汇总 |
| `scope_review.py`及V5/V6门禁 | 原知识边界、接收角色、实例和路径验证 |
| `construction_contracts.py` | 构造契约差异的独立验收 |
| `deployment_v7.py` | 任务获取、时序及部署适用性缺口的独立验收 |
| `citation_repair.py`、`repair_guard.py` | 有界修复引用指针，不改分类或事实字段 |

三个类别都必须被回应，不能只把新类别留成可选辅助字段。每个候选还必须与实际输入链关联；来源在数据文件中出现，不等于交付。

带注释的核心代码摘录见[代码讲解](CODE_V7_ZH.md)。CLI默认V7；直接调用Python兼容函数`scan_source()`时需传`engine_version=7`。

当任务获取类别仍未审清且没有结构化候选时，默认最多增加一次`acquisition_pass`：从当前论文／源码和本次自动提案追查上游来源，区分实验地点、首次知识可见性与后续接收时点。它只能补充精确引用支持的路径前缀和未受信任的部署候选，不能改原有权限、角色、实例或判定标签。补充后仍须独立复核；缺少未来任务上的成功定理不应阻止提出候选，缺少定理也不能直接确认缺口。可用`--no-acquisition-pass`禁用，或在预算不足时保留未运行记录并优先完成复核。

## 复核失败的处理

基本调用为：只读论文声明、论文＋源码映射、独立复核；可增加一次任务来源核查、一次引用恢复，以及**最多一次复核重试**，每篇最多6次。复核重试的模型、提示、schema和输入字节保持不变；每次尝试各自记账。认证、额度、配置、结构化输出schema、上下文限制等明确失败不会盲目重试；不会换模型或切换API。

新日志保存安全错误类别、允许的状态码、事件结构、消息hash和长度、耗时及可取得的CLI版本；不记录任意原始stderr或凭据。旧MUZZLE失败因没有足够诊断而无法追溯具体服务根因，不能补造解释。

另提供显式恢复入口，只读原自动输出，在新目录中做一次复核，不重新取源码或抽取：

```bash
python3 -B scan.py --resume-review outputs/failed-attempt \
  --output outputs/review-recovery --model gpt-6.1-sol --max-calls 1
```

V7保存精确复核提示、schema和请求；历史版本若缺少这些材料，恢复会标为“当前提示的修改后复核”。原失败保留，不能覆盖或冒称全新PDF测试。`technical_failure`属于执行状态，不是论文阴性或证据不足结论。

## 验证边界

合成单元测试用于核验判定门禁和恢复机制；原网址全新运行用于观察自动抽取能力。两者不混作准确率。人工发现只在模型运行结束后用于对照，不修改自动提案、复核或标签。V4/V5/V6输出保持各自历史规则语义，可显式选择对应版本重放。
