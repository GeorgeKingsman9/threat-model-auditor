# 审计规则总表：3条核心判定＋4组通用规则

这是一份可放进Notion的公式整理，对应当前V7代码。七组是说明书的组织方式，不代表代码只有七个条件。MUZZLE当前不确定、ObliInjection限定构造不一致的结果保持不变；此次没有修改判定代码或重跑模型。

这里的“证据支持／证明”表示原始材料、定位、路径和独立复核通过相应门禁，不表示现有LLM审计器已成为任意程序的可靠形式证明器。

## 基础符号

$$
e=(r,p,s,\rho,o),\qquad
\sigma=(v_P,a,v_C,c).
$$

| 符号 | 含义 |
| --- | --- |
| $r,p,s,\rho,o$ | 接收角色、阶段、信息来源、表示形式、操作／用途 |
| $v_P,a,v_C,c$ | 论文版本、实验分支、源码版本、配置／条件分支 |
| $\Gamma$ | 声明模型：知识预算、构造契约、适用场景及明确例外 |
| $D$ | 实现证据：源码、配置、数据记录、输入边界及实例映射 |
| $E=(\Gamma,D)$ | 当前固定范围内的审计证据 |
| $P,N,U$ | 本项确认不一致、本项怀疑被反驳、本项尚未解决 |

声明和实现仍是原来的两个模型；三条核心规则是比较这两个模型的三种方式。每项判断都带自己的$\sigma$，论文最终只汇总一次。

## R1：对齐与证据验收（通用）

对类别$t\in\{K,C,D\}$，定义局部验收条件：

$$
V_t(x,\sigma)=L_t\land J_t\land A_t\land B_t\land\neg X_t.
$$

- $L_t$：原始引用精确、来源域正确、版本和输入hash固定。
- $J_t$：独立语义复核支持该类别所需事实。
- $A_t$：角色、阶段、来源、语义表示及适用范围对齐。
- $B_t$：必要的接收边界、连通路径和实例对应成立。
- $X_t$：该候选自身存在尚未解决的必要证据冲突。

这些条件按类别解释。构造或部署规则不必先通过知识禁止规则。某项未解决也不会抹掉另一项独立成立的局部发现。

**角色分开：**

$$
Present(Q,evaluator)\nRightarrow Present(Q,attacker),\qquad
Present(Q,evaluator)\nRightarrow Absent(Q,attacker).
$$

**粒度分开：**

$$
\rho_{full}(Q)=Q,\qquad
\rho_{partial}(Q)=f(Q),\qquad
\rho_{meta}(Q)=m(Q).
$$

完整问题、删减问题和题型元数据不能互相代填许可。当前代码明确匹配这些表示，未实现信息偏序／格上的通用自动推理。不能仅因禁止完整Q，就自动推导禁止所有partial Q；也不能仅因允许题型，就自动授权完整Q。

**实例分开：**

$$
InstanceOK_t=ReqAny_t\lor(ReqSame_t\land VerifiedSame_t).
$$

实例要求必须来自该类别的适用契约，未知要求不能当作any-instance。配置、ID、索引和变换链提供对应证据；相同文本、文件名、train/test标签不足以建立同／异实例。

## R2：知识授权、实验给定与获取路径分开（通用）

三个命题分别记录：

$$
Given_\Gamma(Q),\qquad Supplied_D(Q),\qquad Get_{\sigma}(Q).
$$

它们分别表示：论文明确假设攻击者已知Q、实验实际提供Q、声明场景中取得Q的路径有据。

$$
Given_\Gamma(Q)\Rightarrow Allow_\Gamma(Q\mid Given(Q)),
$$
$$
Allow_\Gamma(Q)\nRightarrow Get_\sigma(Q)=\top,\qquad
Supplied_D(Q)\nRightarrow Allow_\Gamma(Q).
$$

明确的known-query假设可以是合法的条件研究设定，结论要带该条件。operator提供输入是实现／流程事实，不自动构成知识授权，也不证明现实线上获取途径。黑盒的具体访问限制与任务知识预算应分别读取，不能从标签直接推出Q被禁止或Q来源已建立。

此处$Allow(Q)$只讨论知识可见性，不自动授权修改Q、任意使用Q或扩大其他攻击能力；页面修改能力也不自动授予Q知识。

对于当前接收者$r$及关于Q的信息流$e_Q$，可以简记：

$$
BlackBox(r)\nRightarrow Deny_\Gamma(e_Q),\qquad
BlackBox(r)\nRightarrow Get_\sigma(Q)=\top.
$$

建议在Notion中把“有据的获取路径”定义为：

$$
Path_\sigma(Q_i,t_c)\iff
\exists\pi:\ Allowed_\Gamma(\pi,\sigma)
\land Verified_D(\pi)
\land InstanceMap_D(\pi,i)
\land t_{available}(\pi)\le t_c.
$$

$t_c$是构造／优化使用信息的时间。路径须从允许来源到达匹配接收者，并建立所需任务／信息表示对应。首次知识可见时点与后续接收时点应分别记录。已合法取得某个离线任务的信息，不自动证明另一个未来任务的信息同样可得。

获取采用三值**证据状态**：

下式$Path_\sigma(Q)$简写当前接收者、信息表示、实例和构造时点对应的$Path_\sigma(Q_i,t_c)$；简写不删除上述条件。

$$
Get_\sigma(Q)=
\begin{cases}
\top,&E\vdash Path_\sigma(Q),\ E\nvdash\neg Path_\sigma(Q),\\
\bot,&E\vdash\neg Path_\sigma(Q),\ E\nvdash Path_\sigma(Q),\\
?,&\text{其他，包括证据冲突。}
\end{cases}
$$

最关键的是：

$$
E\nvdash Path_\sigma(Q)\quad\not\Rightarrow\quad E\vdash\neg Path_\sigma(Q).
$$

“尚未建立路径”与“已证明路径不存在”不同。否定只能针对有肯定排除证据且覆盖闭合的固定接口／范围，不能扩写成现实世界不可能获得Q。

这是对来源问题的补充建模定义。当前程序用结构化来源、时序、关系、路径定位及复核来验收，尚未实现任意程序的完整获取路径推导器。

## R3：知识边界违规（核心K）

$$
V_K(e,\sigma)\land
(\Gamma\vdash_\sigma deny(e))\land
(D\models_\sigma present(e))
\Rightarrow R_K(e,\sigma)=P.
$$

这里要求适用的攻击者知识限制、明确的信息粒度和必要实例关系。`present`须到达匹配的攻击构造器／优化器边界，仅在数据文件中出现不够。构造模型须追到实际生成请求；受约束优化器的实际输入边界可以构成终点，不必虚构另一个后续LLM请求。

## R4：构造契约差异（核心C）

$$
V_C(\kappa,\sigma)\land Contract_\Gamma(\kappa,\sigma)
\land Incompatible_D(\kappa,\sigma)
\land Used_D(\kappa,\sigma)
\land NoException_\Gamma(\kappa,\sigma)
\Rightarrow R_C(\kappa,\sigma)=P.
$$

$\kappa$表示被审查的构造契约，与范围元组中的配置$c$不同。

- $Contract$：明确的构造输入、生成方式、来源或信息精度声明。
- $Incompatible$：同范围源码中的正面不相容证据，包含论文概念到实际参数组合的语义对应。
- $Used$：与经过验收的实际攻击构造／优化接收路径关联。
- $NoException$：适用范围和明确例外经复核，没有成立的例外覆盖该差异。

这里需要有据的适用范围判断；“尚不知道是否有例外”仍为U，不能把搜索未发现例外当成已排除所有例外。

此规则不需要强行生成`deny`。文中没提某参数、没找到生成器、文件叫shadow，都不能单独证明不相容。若差异依赖复用评估题目，须另证同实例关系。

例如，ObliInjection本轮确认的是限定raw分支中的构造来源差异；不自动等价于作者历史运行违规或ASR因Q而必然提高。

## R5：任务获取／部署假设缺口（核心D）

这里$S$是绑定在当前固定范围$\sigma$内的声明场景，$Get_S$简写$Get_{\sigma,S}$；场景名称不能代替版本／分支／配置范围。

来源未建立，首先产生待核查义务：

$$
Claim_\Gamma(S)\land Use_D(Q,S)\land Get_S(Q)=?
\Rightarrow Obl(Q,S).
$$

$Obl$只表示应追查来源，不是positive。确认第三类还需要：

$$
V_D(g,\sigma)\land Claim_\Gamma(S)\land Use_D(Q,S)
\land Mat(g,S)\land Mis(g,S)\land Get_S(Q)=?
\Rightarrow R_D(g,\sigma;S)=P_{gap}.
$$

- $Claim$：论文确实声明了相应线上／离线到线上场景。
- $Use$：发布构造路径实际接收、使用该任务信息。
- $Mat$：知识依赖对所审路径或适用性主张有材料性，不要求证明一切攻击都必须依赖Q或ASR必然增加。
- $Mis$：来源、时序或任务实例之间存在经证据与复核支持的衔接缺口，不能定义成“没找到路径”。

$P_{gap}$确认的是带范围的获取／适用性假设缺口，不是“不可能取得Q”，也不会生成`deny`。沙箱是实验地点，不能自行推出offline-only；可用于同实例构造的允许观察渠道则必须作为反证选项保留。

**MUZZLE当前可直接写成：**

$$
Supplied_D(Q)=\top,\qquad
Source_D(Q)=operator\ file,\qquad
Get_{S_{online}}(Q)=?.
$$

这足以登记来源义务。当前自动候选及复核的范围、材料性和必要实现证据未全部通过，所以仍为$U$，不在本次规则整理中改标签。

观察前由operator提供Q，单独看也不能确认时序缺口：如果构造发生在允许观察同一Q之后，该观察可能构成有效来源。是否确为同一实例、何时可见、来源是否允许，仍需证据；未知时保留U。

## R6：反证、冲突与不确定（通用）

对一个固定候选，采用三值结论：

$$
R_t(x)=
\begin{cases}
P,&\text{对应核心确认条件全部通过},\\
N,&\text{对应的肯定反证及其验收条件通过},\\
U,&\text{其他情况，包括本项必要证据冲突。}
\end{cases}
$$

| 类别 | 可成立的反证 |
| --- | --- |
| K | 适用的明确allow；已验证排除攻击者交付；仅针对同实例的限制被有效异实例证据排除；已证评估器接收且该攻击者限制不适用 |
| C | 同范围构造来源确实对齐，或明确且适用的例外成立 |
| D | 明确的offline-only范围，或同路径的获取／不需要该知识已有肯定证据 |

适用allow可以反驳相应知识禁止怀疑，无须额外证明有人实际行使该许可。`absent`、`possible`、没发现违规、没有引用、仅主题相似、实例未知，都不能自行生成论文级阴性。共同规则与具体例外先解决适用关系；仍冲突时保留U。

当前冲突检查主要作用于明确匹配的归一化记录，尚非任意自然语言或不同信息表示重叠关系的完整语义判定。

## R7：论文级汇总与执行状态（通用）

设$\Sigma$为本次固定的审计范围集合，$\mathcal O_\Sigma$为其中三类的有限待核查项。每项保留自己的范围，不跨分支借结论。

当前程序的汇总可表示为：

$$
R_{paper}=\begin{cases}
P,&\exists x\in\mathcal O_\Sigma:R(x)=P,\\
N,&N_0\land Closed(\Sigma)
\land\forall x\in\mathcal O_C\cup\mathcal O_D:R(x)=N,\\
U,&\text{其他情况。}
\end{cases}
$$

$N_0$表示原知识边界／输入覆盖轨道已经输出范围内一致，要求非空怀疑及相应反证。$Closed$包含新增类别回应、未解决项与必要覆盖检查。当前V7不会仅凭C/D全部反驳，就把原知识轨道的U升级为N；这是当前实现的保守限制。

局部positive可以与其他未解决项并存。阴性仅限命名审计范围；不能删去未解决项或缩小候选集合后宣称整篇没有问题。

执行状态另外记录：

$$
RunStatus\ne completed\Rightarrow\text{本轮科学判定未完成}.
$$

技术失败、不适用、尚未运行，不混作论文P/N/U。静态路径支持的是条件实现结论，不自动证明作者历史执行或效果因果关系。

## 与实际代码的对应及当前限制

| 规则 | 主要实现 |
| --- | --- |
| R1 | `checker.match_edge`、V4引用／路径、V5角色／实例、V6输入通道验收 |
| R2 | `declared_contract.py`、`deployment_v7.py`的来源／时序／任务关系、`acquisition_pass.py`；通用Path推导是补充定义，非已完成的程序证明器 |
| R3 | `scope_review._assess_bound_claim`，配合V5源证据验收 |
| R4 | `construction_contracts.project_construction_findings` |
| R5 | `deployment_v7.project_deployment_findings_v7` |
| R6 | 上述各轨道的refuted／unresolved分支 |
| R7 | `extraction_v7.decide_extraction`、`findings.project_result`及`scan.py`状态记录 |

当前D实现比研究公式更窄：实际来源只对operator/configuration两类确认；来源规则须为明确观察许可或知识约束；场景须为online／offline-to-online；时序须为pre-observation，或post-observation＋future-task-transfer＋offline-to-online。它还要求有据的路径关联、材料性及提案与复核的supported-gap一致。其他来源并未据此证明安全，只是当前没有相同确认分支。

K、C、D各自有类型和证据门禁；源码中的所有校验分支、调用预算、下载和恢复机制不另计作研究判定规则。具体实现与运行过程见[V7方法](AUTOMATIC_V7_ZH.md)及[V7结果](V7_PILOT_RESULTS_ZH.md)。
