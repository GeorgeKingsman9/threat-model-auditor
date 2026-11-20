# V5：元素建模、自动取证与三篇开发案例的测试

**原来的 Notion 建模继续使用。** 声明与实现先对齐到同一信息流和审计范围，再运行一致性规则。此次增加了必要配置/固定依赖取材、接收角色与实例映射验收；公式及函数对应见 [建模映射](NOTION_MODEL_MAPPING_ZH.md)。

**修正校验器后，原自动证据重新验收为 1 篇限定不一致、0 篇阴性、2 篇不确定。** 原始模型运行均输出不确定；修正后的结果属于同一自动输出的确定性重放，没有手填证据、修改提案或重标 gold，也不是额外一次独立模型成功实验。

| 论文 | 首次V5新运行 | V5.1新运行 | 修正校验器后重放 | 当前可支持的结论 |
| --- | --- | --- | --- | --- |
| ASPI | 不确定 | 不确定（下载重试后完成） | **限定不一致** | 同一组记录中的任务派生部分查询进入Stage 2恶意回复生成；条件为评估选择这些生成的grouped记录及相应clarif_user分支 |
| MUZZLE | 不确定 | 不确定 | **不确定** | 已确认task-spec和trace两条独立路径进入PAIR优化器；trace明确允许，task-spec是否提供观察范围外的信息仍未证明 |
| ObliInjection | 不确定 | 不确定 | **不确定** | 已确认选入的任务段进入GCG优化器；真实目标/合成shadow来源及具体许可范围仍未确定，实例映射还有引用/表示验收缺口 |

本轮只重测上述3篇。内部多条信息流只用于定位，论文统计仍一篇一条；不能用MUZZLE的一条已排除怀疑代替整篇negative。本轮没有获得可认证的论文级阴性，也没有证明自动恢复全部既有人工发现。

## 原始输入与实际取得的材料

只提供原始论文URL，没有提供仓库地址、人工规则、案例、gold或旧模型提案。PDF和URL是两个可选入口；下面是这次实际使用的3个URL：

- [ASPI v1](https://arxiv.org/pdf/2605.17324v1)
- [MUZZLE](https://www.usenix.org/system/files/usenixsecurity26-syros.pdf)
- [ObliInjection v3](https://arxiv.org/pdf/2512.09321v3)

| 材料 | 固定版本 | 进入模型的eligible文件 |
| --- | --- | --- |
| ASPI源码 | `e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d` | 32/32 |
| MUZZLE源码及必要配置 | `9f3effa1668fa29dcba8f2454e711ddf9ef3c038` | 106/106；此前为81个 |
| MUZZLE固定PAIR子模块 | `16518e2dacc3da823a39ec3bc28d692bacaf17b6` | 36/37，1个文件超依赖字符预算；未把整个依赖称为已闭合 |
| ObliInjection源码及配置 | `b1f6a3f48c0cf121534374cbcef453832594867b` | 31/31；此前为19个 |

ObliInjection的shadow/test JSON在公开树中存在，但0.5–3.3MB的文件超过本轮64KiB数据取材限额；不能说作者未开源。全部源码eligible文件读入，也不代表数据、动态环境和历史运行均已核对。MUZZLE引用枚举也有明确限额，未证明全局依赖闭合。

## 为什么ASPI发生变化

首次V5输出存在权限适用性分歧、路径节点命名不连续，以及缺少实例映射。V5.1在不提供既有发现的条件下重新抽取、复核，已自动提出：共同知识限制适用于该构造、实际生成请求收到了部分查询，以及源记录与评估记录之间的条件静态映射。

当时的确定性校验器却要求组合ID的完整字符串连续出现在原文里。源ID由`suite_name / ut.ID / it.ID`组成，评估侧分别读取相应group字段；每侧的各分量都在同一处精确引用内，并有独立的源/评估定位与序列化、加载、分发链。把组合元组当单个原文子串拒绝，是表示验收问题。

V5.2仅对可解析的AST元组逐分量验收：所有分量须在每侧同一引用中精确出现，保留独立定位和复核通过的变换链；缺失分量、任意分号文本、未支持的映射仍不通过。没有修改自动提案、引用或模型复核。重放后该信息流通过所有验收。

具体位置是[论文第3页](https://arxiv.org/pdf/2605.17324v1#page=3)的任务知识限制，与[Stage 2模板绑定](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/dataset/pipeline.py#L130)、[构造请求](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/common/litellm.py#L73)。身份依据包括[源group的ID](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/dataset/pipeline.py#L218)与[评估侧取回ID](https://github.com/scaleapi/aspi/blob/e2a3f6ac87b2c00ac482252d067d22f3ecf57b9d/src/aspi/eval/runner.py#L1542)。

结论只涵盖生成grouped数据被选入相应`clarif_user_HR/GS/CP`分支的条件静态路径；不证明作者历史上选择了哪份文件、所有分支都有问题或ASR被抬高。

## 运行、修正与保留记录

| 阶段 | 冻结代码 | 新CLI调用 | 结果 |
| --- | --- | --- | --- |
| 首次V5 | `caa324b` | 7 | 3篇不确定 |
| V5.1重新抽取与复核 | `1202dde` | 9 | 3篇不确定；另保留ASPI下载失败尝试，0次模型调用 |
| V5.2确定性重新验收 | `dcc3f28` | 0 | 1篇限定不一致、2篇不确定 |

两轮新运行的调用上限均为每篇3次；提取、可选一次引用恢复、独立复核。请求模型固定`gpt-6.1-sol`，使用已有ChatGPT/Codex登录，未调用Claude API；CLI未暴露实际模型ID，保留null。合计报告input 1,885,954、output 19,865、reasoning 1,582 tokens；账号额度使用不保证免费。

ASPI第二轮第一次在PDF下载时超时，未进入模型。一次重试使用已验证的现有进程代理后完成；原失败记录、重试配置和产物均保留，没有修改系统代理。没有运行作者源码、攻击或ASR实验。

修正后的软件检查398项通过；其中包括多个接收者、不同实例反证、组合ID缺失分量、跨行/嵌套/同一行不同调用及非ASCII位置的检查。这是程序验证，不能算论文检测准确率。此前101条旧规范化记录兼容性检查也不能代替原始论文测试。

## 使用与报告

普通用户任选一个输入：

```bash
python3 -B scan.py /path/to/paper.pdf
python3 -B scan.py https://arxiv.org/abs/2605.17324v1
```

此次为可比性另外固定provider/model、每篇调用上限，并指定`--source-fetch files --require-source`；这些是运行设置，不是人工证据输入。默认源码和模型数据限额已与本次配置一致。自动生成的输出目录包含每篇结论、流程、定位、源码发现、快照和模型记录。

- [全部新运行与重放的可读报告](results/2026-11-21-v5-pilot/report.html)
- [机器可读结果](results/2026-11-21-v5-pilot/report.json)
- [所有尝试与原始产物hash](results/2026-11-21-v5-pilot/process_manifest.json)

完整原始论文、源码及模型输出保留在本机`outputs/2026-11-21-v5-pilot-175505`和`outputs/2026-11-21-v5-1-pilot-020638`；公开报告只发布摘要、定位与校验信息。新鲜模型输出和确定性重放分别标记，不计算跨阶段“准确率”。后续仍需解决ObliInjection的有界数据来源取证，并用新案例和真正的阴性对照评估自动化可靠性。
