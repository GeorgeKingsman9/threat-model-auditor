# Threat Model Auditor

A small, deterministic checker for consistency between paper-declared information
access and manually normalized implementation evidence. One final row per paper.

把论文声明和实际信息流整理成 JSON，再检查二者是否一致。**目前是人工整理证据、程序判定；不会自动读取 PDF、分析任意 GitHub 源码，也不会运行原论文的攻击实验。**

## 快速运行

需要 Python 3.10+ 和可选的 Bash，无第三方 Python 依赖，不需要 API key、GPU 或模型调用。
进入本仓库目录后：

```bash
# 查看支持的论文 ID
python3 -B audit.py list

# 每篇只显示一行：是否确认不一致，以及证据状态
bash scripts/audit.sh aspi
bash scripts/audit.sh muzzle
python3 -B audit.py audit aspi obliinjection
python3 -B audit.py audit all

# 查看一篇论文的声明、实验范围和详细证据
python3 -B audit.py audit aspi --json --details

# 保存 JSON；拒绝覆盖已有文件
python3 -B audit.py audit all --output outputs/papers.json

# 对照我们已有的人工标签做回归检查
python3 -B audit.py evaluate all

# 检查程序行为
python3 -B -m unittest discover -s tests -v
```

`audit` 不读取人工标签。`evaluate` 先产生同样的判定，再和标签比较。
命令退出码：正常审计为 `0`（即使发现不一致）；标签不匹配为 `1`；输入或命令错误为 `2`。

示例输出：

```text
paper   confirmed_inconsistency   status
aspi    yes                       有已确认的不一致
muzzle  no                        证据不足
```

`no` 的准确意思是“当前证据未确认不一致”。旁边的状态区分“审计范围内一致”和“证据不足”。
一篇论文内可能需要核查几个角色或实验阶段；任意一处确认不一致，整篇便记为 `yes`，统计时只计一次。

## 输入是什么

每条内部记录包含同一实验范围下的两类信息：

- `rules`：论文明确允许或禁止的信息流，即声明模型。
- `observations`：实现中确认出现、确认没有出现或仅有可能出现的信息流，即实现证据模型。

`allow` / `deny` 是声明端的两个选项；`present` / `absent` / `possible` 是证据端的三个选项。
例如同一角色、阶段、信息、表示和用途下，`deny + present` 表示“论文排除这种访问，但实验确认发生”，判为不一致。
论文没有说明时留空 `rules`，不自行推断为 `deny`。

完整字段、所有选项和判定表见 [docs/OPTIONS_ZH.md](docs/OPTIONS_ZH.md)。
当前 pilot 的输入、范围和结果边界见 [docs/PILOT_ZH.md](docs/PILOT_ZH.md)。

## 新增论文

按 [examples/new_case.json](examples/new_case.json) 和 [examples/new_paper.json](examples/new_paper.json)
的结构填写。示例是明确标注的占位输入，不能作为真实论文的发现。
完成自己的证据整理后运行：

```bash
python3 -B audit.py audit my_paper \
  --cases examples/new_case.json \
  --papers examples/new_paper.json --json --details
```

示例缺少真实声明和证据，预期输出“证据不足”。将 `my_paper` 改为自己的 ID，并把两个 JSON 换成自己的记录。
新论文默认不需要 `gold`。需要测评时，另写 `{ "my_paper": "insufficient_evidence" }` 这样的论文级标签文件：

```bash
python3 -B audit.py evaluate my_paper \
  --cases examples/new_case.json --papers examples/new_paper.json \
  --gold examples/new_gold.json
```

## 可复现性和证据边界

随仓库提供的是当前研究者整理的 11 篇论文、15 条内部证据记录及预设标签。
它们用于演示和回归检查，已参与规则设计；标签一致率不能当作未见论文的检测准确率。

核心代码只检查格式、字段匹配和判定规则，不验证引用内容是否真实、是否足够，也不联网。
`paper_text` 的实现证据可能来自论文对实验过程的描述，不能等同于实际运行日志。
`archived` 记录中部分引用指向整理时的本地审计材料；这些历史路径不是本仓库中的文件。
详见 [docs/PROVENANCE.md](docs/PROVENANCE.md)。本仓库可重放给定记录的判定；对底层材料的独立核验需要对应来源。

代码与本仓库原创元数据采用 MIT 许可证。引用的论文、上游源码和外部材料仍遵循各自的许可；本仓库不重新授权这些材料。
