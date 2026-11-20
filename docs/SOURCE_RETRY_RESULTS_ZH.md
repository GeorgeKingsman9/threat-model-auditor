# MUZZLE 与 ObliInjection：源码重试结果

**两篇源码均已成功获取、校验并读入模型。最终自动结论仍为两篇证据不足；原因已不是源码下载失败。** 本次只提供原始论文网址，仓库和固定版本由程序自动确定，没有传人工证据、gold、旧提案或 `--repo`。

| 论文 | 自动取得的源码 | 模型实际读取 | 最终自动结果 |
| --- | --- | --- | --- |
| MUZZLE | `gsiros/muzzle`，commit `9f3effa1668fa29dcba8f2454e711ddf9ef3c038` | 81/81个符合过滤规则的源码文件，424,481原始字节；每个Git blob与SHA256均验证 | `insufficient_evidence` |
| ObliInjection | `ReachalWang/ObliInjection`，commit `b1f6a3f48c0cf121534374cbcef453832594867b` | 19/19个符合过滤规则的源码文件，140,284原始字节；每个Git blob与SHA256均验证 | `insufficient_evidence` |

这里的81/81、19/19指eligible源码范围。配置、数据集、依赖和其他过滤项仍有排除，不能称为全仓库或历史实验审计。

## 上次为什么没有拿到

- **ObliInjection是识别器缺陷。** 首页已有正确GitHub地址，但 `Our code and data` 与 `are available at:` 分成两行，原规则未把它认作作者代码声明。已通用支持段内软换行，仍保留空行、baseline和相关工作边界。
- **MUZZLE是取材方式不合适。** 仓库blob约23MB，而符合规则的源码约424KB。整包诊断90秒只取得约3.2MB；改为固定commit的完整Git tree与逐文件源码读取，诊断17.065秒取得并验证81个源码文件。
- **首次正式复跑还有本次路由设置错误。** 成功诊断的raw源码CDN走现有代理，复跑却把该域名设为直连，导致再次超时。这次失败和仅论文输出保留，没有改写为成功。最终复跑恢复已验证的CDN代理路由；系统代理未改动。

最终取材过程MUZZLE的83次HTTP请求、ObliInjection的21次请求全部成功，分别为2次Git元数据请求及81/19次源码文件请求。本轮跳过已知慢的archive，直接使用逐文件方式；不是模型重复生成直到得到期望标签。

## 取得源码后为什么仍是不确定

**MUZZLE：** trace与同次LLM请求中观察到的system prompt，被复核为论文明确允许的信息源，这项疑点已排除。另一条路径确认 `task_spec.instruction → PAIRConfig.original_user_task → initialize_conversations`，但被排除的PAIR helper/converser实现使攻击模型请求的最终序列化和接收尚未确认；该文本是否已属于允许观察的trace也未确定。因此不能直接把初始化参数当成已完成的禁止信息交付。

**ObliInjection：** 训练问题全文进入消息格式化和梯度优化已确认；但配置、数据与任务索引尚未核对，无法确认它是真实评估问题、论文允许的shadow question，还是另一实例。不能只凭代码变量叫training或test就确定两者关系。

另外，ObliInjection一条记录的edge是victim evaluation、`present`指评估器收到问题；复核同时支持 `evaluator_only`、`not_applicable` 和排除攻击构造交付。当前 [scope_review.py](../scope_review.py#L128) 门禁却先将 `evaluator_only + present` 一概判作冲突。这是接收角色与判定门禁不对齐，不能写成源码证明攻击者获得test query，也不能据此把整篇判为一致。原始输出保留，未手工改字段。

所以，**下载与代码来源识别已修复；自动恢复既有ObliInjection发现的能力尚未完成。** 剩余工作在必要配置、任务关系、依赖取材，以及角色和交付状态的对齐，不能继续归因于作者没有开源。

## 本轮设置与全部过程

- 最终代码：`08440d0`；程序检查325项通过。源码识别、读取和判定输入绑定均有离线测试。
- 请求模型：`gpt-6.1-sol`，现有ChatGPT/Codex登录；CLI未报告实际模型ID，保留null。
- 每篇最终3次CLI调用：新鲜抽取、一次引文恢复、独立复核。引文恢复只换指针，没有改分类字段；两篇剩余引文错误均为0。
- 本轮源码字符预算500,000、模型数据JSON上限800,000，确保MUZZLE全部81个eligible文件进入模型；实际数据分别664,715和262,753字符。
- 最终6次调用报告input 588,686 tokens、output 8,272、reasoning 989。账号额度使用不等于免费，次数不等于费用上限。
- 含第一次路由错误的纸面审计，本轮共10次CLI调用；诊断和prepare-only不调用模型，不计作审计结果。
- 没有运行作者项目、攻击或ASR实验；也没有修改人工案例或参考标签来配合自动结果。

最终命令形态：

```bash
python3 -B scan.py PAPER_URL \
  --source-fetch files --require-source \
  --provider codex --model gpt-6.1-sol --max-calls 3 \
  --max-input-chars 800000 --max-code-chars 500000 \
  --output outputs/new-source-retry
```

`--source-fetch files`仍自动发现仓库；`--require-source`让源码失败在模型调用前停止。本轮raw CDN走已验证的现有代理，其他公开材料使用记录中的进程路由，未更改全局网络设置。

- [最终机器可读结果、源码覆盖与引文位置](results/2026-11-20-source-retry/report.json)
- [所有尝试、配置和原始产物hash](results/2026-11-20-source-retry/process_manifest.json)

本机完整HTML为 `outputs/2026-11-20-muzzle-obli-source-retry-091205/combined/report.html`，含每篇执行步骤、原始证据和未决原因。较早失败、原始模型输出及源码快照均保留；公开摘要不复制整份论文或源码。这两篇为已知开发案例，结果不构成泛化准确率。
