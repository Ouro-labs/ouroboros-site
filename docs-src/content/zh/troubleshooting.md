# 检查任务状态、评估与安全恢复

本页补充[快速开始](/docs/zh/quickstart/)的首次安装/MCP 排查入口，以及刚完成或中断一次任务后的检查步骤。它只翻译了初学者需要的环境分辨、ID 识别、状态查询、评估和安全恢复要点；它不是完整的 CLI、MCP 或故障排除手册，也不是整份故障排除指南的翻译。

> **版本与验证范围：**快速开始和状态说明以产品源码 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 为参照。恢复与评估详细指南中的部分细节来自较早的固定提交 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)，不能据此假定与当前 `main`、公开发行版 `0.59.9` 或你安装的插件/MCP 服务器完全相同。本文没有在真实模型和所有宿主上验证。先查看你所用版本的命令帮助和已连接服务器的工具/输入 schema。

## 安装或 MCP 连接异常：先区分环境

先记录出问题的设备/操作系统、宿主应用和会话、项目目录、实际错误，以及使用的是独立 CLI、宿主插件还是宿主启动的 MCP 服务器。若该终端能找到独立 CLI，可用 `ouroboros --version` 和 `ouroboros --help` 查看**该终端**中的安装；这不能说明宿主启动的服务器版本。终端找不到 `ouroboros` 也不能证明宿主插件或 MCP 服务器未安装。不同设备、用户、虚拟环境和宿主会话可能使用不同安装。

在出错的原宿主会话中，分别确认插件/服务器是否启用，以及症状属于服务器启动失败、连接失败、工具未发现还是认证失败。只查看相关设置与日志行即可；分享前遮盖令牌、凭据、私人路径、项目名和提示内容。不要发送完整配置、环境变量转储或凭据。若 CLI 不存在或其版本不支持下列命令，先查看宿主自己的安装/连接状态和当前版本帮助，不要为了猜测宿主服务器版本而另装一份。

有受支持的独立 CLI 时，才在对应安装的终端查看 `ouroboros mcp doctor` 失败的检查项。按源码 `592c667f`，默认命令检查启动前的环境条件，不会启动服务器；它不证明宿主已连接、认证有效或模型调用成功。检查自身也可能初始化本地记录或尝试网络访问。`ouroboros status health` 的健康行同样不能证明认证有效或任务成功。诊断通过只说明该项检查通过。

`ouroboros mcp doctor --probe-local-stdio` 是额外检查：它会启动临时本地子进程并探测服务器启动和工具发现；不会验证宿主配置的启动器、宿主认证或模型调用。其 Python 层面的限制不等同于操作系统隔离。Codex 的 `ouroboros codex doctor --live-mcp` 会启动配置中的 stdio 服务器；执行前先检查其命令和可能的网络/其他副作用，而且它不验证 URL 传输或模型调用。只有确认所用版本支持且确有必要时才运行这些选项。安装诊断可能显示启动参数；任何输出分享前都要脱敏。

不要仅因诊断失败就自动应用建议或覆盖设置。先确认将改哪个宿主、文件/服务器和影响范围，由用户决定是否修改；修改后在同一设备、用户、宿主和安装中重新检查工具发现与原始连接问题。未实际测试的宿主连接、认证或模型调用应明确标为未验证。以上是 AI 故障排除指南中与本页读者相关的简短入口；完整安装、更新及其他情形目前请参阅韩文指南。

## 先保存这些信息

开始查询或恢复前，记录执行启动时实际返回的 ID 字段和值、使用的宿主或 CLI、原始 Seed 文件及其内容、执行结果/产物、实际工作目录，以及结果中返回的 `worktree_path` 和 `worktree_branch`（如果有）。错误信息应先去除令牌、凭据和私人内容。

ID 前缀只能作提示；以启动结果中的字段名为准。不要把 `job_id` 当成 `session_id`，也不要猜一个 ID。

| 启动结果中的字段 | 表示什么 | 如何继续查询 |
| --- | --- | --- |
| `job_id` | 后台工作的状态与结果 | CLI：`ouroboros job status <JOB_ID>`；变化等待：`ouroboros job wait <JOB_ID>`；终止后：`ouroboros job result <JOB_ID>`。宿主 MCP 则使用服务器实际提供的 `ouroboros_job_status`、`ouroboros_job_wait`、`ouroboros_job_result`。 |
| `session_id` | 执行会话 | CLI：`ouroboros status run --session-id <SESSION_ID>`；如果宿主提供会话状态工具，可用该实际工具查询。 |
| `execution_id` | 执行事件与状态记录 | CLI：`ouroboros status execution <EXECUTION_ID> --events`。 |
| `auto_session_id` | Auto 访谈、Seed 和执行交接状态 | CLI：`ouroboros status auto <AUTO_SESSION_ID>`。 |

这些是产品源码 `592c667f` 中的 CLI 形式；安装版本可能不同。插件调用通常不会提供终端 `ouroboros` 命令。对于 MCP，先确认当前连接的服务器是否提供这些工具及其实际参数。

## 查看当前状态 {#status}

如果有 `job_id`，用同一个 ID 查询。工作仍为 `running` 时继续等待同一个 job；若显示 `acceptance_pending`，持久接收状态尚未确认，也用同一 job ID 重新查询，不要另起工作；到达终止状态后，再读取同一个 job 的结果。状态查询成功只表示查询完成，不能证明任务成功。空列表或“找不到”也不证明任务不存在：你可能在错误的项目、用户环境、数据库或宿主中查询，也可能拿错 ID 类型。

独立 CLI 可用以下命令查找记录：

```sh
# 查看最近的执行记录；需要更多记录时加 --all
ouroboros status executions
ouroboros status executions --all

# 查看实际的 execution ID 及其事件摘要
ouroboros status execution <EXECUTION_ID> --events

# 按实际 session ID 查看 Run/Stage/Step 投影
ouroboros status run --session-id <SESSION_ID>

# 列出仍在进行的 CLI 会话，不会选择或恢复会话
ouroboros resume --list
```

`ouroboros resume --list` 默认只列出有限数量的进行中会话，不是所有 job 或已结束记录的清单；列表中没有某个 ID，不能作为重新启动的依据。执行 ID、会话 ID 和 job ID 属于不同记录，按原始启动响应选择查询方式。

如果插件返回 `job_id: null` 或 `delegated_to_plugin`，不要对空 ID 调用 job 查询工具。结果可能由宿主创建的子会话或任务面板承载；回到原来的宿主对话，检查交接状态、子任务结果和工作路径。

## 评估没有开始、失败或显示 `unverified` {#evaluation}

执行完成后通常会尝试正式评估，但设置、执行结果和宿主路径都可能影响后续步骤。先核对实际 `session_id`、原始 Seed、产物/输出，以及报告的工作目录或 `worktree_path`。检查现有评估 job 和关联的 Ralph job 状态与结果；如果仍在运行，不要再启动一条重复链。

没有现存评估，且确实需要评估时，可在宿主请求：

```text
ooo evaluate <实际 SESSION_ID> [产物或输出]
```

使用实际 session ID 和要评估的产物；能确定项目根目录时，也应把绝对项目路径提供给评估流程。若 Seed 或产物不明确，先在原执行记录中确认，不要用猜测的文件代替。正式评估可能执行项目配置的检查并调用模型，因此可能花费时间、产生费用或运行项目命令。

- **`unverified` 不是通过。**它表示没有可用的已执行机械检查证据。先查看实际工作目录里的 `.ouroboros/mechanical.toml` 和检查结果，补充或修正适合该项目的可执行检查后，再按评估技能要求重新评估。自动探测也可能改写配置或调用模型；执行 `ouroboros detect` 前先阅读本机帮助并检查已有文件。
- **检查失败或评估被拒绝：**先读取失败阶段、命令输出和建议，再决定是否需要修复并重新运行。阶段 1 有代码变更且检查失败时，先修复再评估；如果尚无可评估的代码结果，应先运行任务。不要把错误响应改写成 `rejected`、`approved` 或成功。
- **评估超时或状态不明：**先用原有 job ID 查询状态和结果；不要因超时就启动另一个评估。

`auto_evolve: false`只控制**本次新评估**是否尝试安排新的 Ralph 后续任务；它不会取消已经启动的评估 job 或 Ralph 链。如果结果包含 `chained_ralph_job_id`，应单独检查该 job 到达终止状态并读取结果。`chained_ralph_skipped`、`chained_ralph_error` 也要保留为实际结果。开始回执不是完成证明。

## 连接中断或结果不清楚时 {#recovery}

1. 保留原始 ID、Seed、最后一次状态、执行输出、实际目录/worktree 与 branch；不要覆盖原记录。
2. 如果 job 仍在运行，用同一 ID 继续查询，并确认启动它的宿主或进程是否仍可用。记录中的 `running` 不总能证明进程现在仍然存活。
3. 若结果尚未确定，先检查工作目录、文件变化、Git branch 和可能发生的外部操作。连接中断或 `failed` 状态不能证明改动已回滚。
4. 确认旧任务已结束、保留结果并理解重复效果后，再决定是否运行或恢复。`resume --list` 只是列表查询；实际恢复可能创建新尝试或改变工作目录/branch。恢复命令的可用性和行为依安装版本而异，先查看当前帮助并确认目标 Seed 与路径。
5. 取消与回滚不是一回事。取消请求不保证 worker 已停止，也不会撤销已发生的文件或外部服务变更。不要仅凭请求已接收就启动替代任务。

状态显示、执行工作者完成和验收通过是不同结果。每次都检查真实产物、实际检查证据和最终评估状态。

## 更完整的指南（目前只有韩文）

本页范围之外的详细 ID/状态规则、恢复情形和评估/演进判定目前只提供韩文说明：

- [状态与 ID 详细指南（韩文）](/docs/status-guide/)
- [中断与恢复详细指南（韩文）](/docs/recovery-detail/)
- [评估与演进详细指南（韩文）](/docs/evaluation-evolution-detail/)
- [版本确认指南（韩文）](/docs/version-guide/)
