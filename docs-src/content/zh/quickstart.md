# 开始第一个任务

> **部分翻译：** 本快速入门为草稿。状态、评估与恢复的简要指南提供中文；更广泛的详细指南目前为韩语。

选择一种安装方式，然后从 Interview 一直走到结果检查，完成一个**可以添加待办并标记完成的简单网页应用**。这个目标延续了[贯穿韩语指南的示例](https://ouroboros.page/learn/interview/)。

本指南草稿对照的是产品源码 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 中的[安装指南](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)。请勿假设公开发行版 `0.59.9`、现有指南标注的 `0.51.5`，以及你安装的插件和 MCP 服务器与此源码版本相同。本文的完整流程尚未在所有真实模型和宿主环境中运行验证。界面和问题会因版本、环境和你的回答而异。

## 开始前

- 检查网络连接、所选宿主或 Python 环境，以及计划使用的模型所需的认证和费用条件。模型调用可能需要时间，也可能产生费用。
- 执行过程可能创建或修改文件并运行命令。首次练习请使用一个与现有工作隔离的新目录，并在宿主中打开该目录。
- 安装和设置可能会更改软件包或配置文件。请先阅读每个提示再继续。查看[设置指南](/docs/config-reference-detail/)，确认使用统计设置是否适用于你安装的版本和服务器进程。

## 1. 选择安装方式

| 使用环境 | 准备事项与安装命令的输入位置 | 第一个任务的输入位置 |
| --- | --- | --- |
| Claude Code 插件 | 需要 Claude Code 和 `uv`。请在**终端**中输入下方安装命令。 | 新 Claude Code 会话的对话 |
| Codex 插件 | 需要已登录的 Codex CLI 和 `uvx`。请在**终端**中输入下方安装命令。 | 新 Codex 会话的对话 |
| 独立 CLI | 需要 Python 3.12 或更高版本，以及计划使用的运行时和认证方式。请在单独的虚拟环境中安装。 | **终端** |

### Claude Code

在终端中运行：

```bash
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
```

### Codex

在终端中运行：

```bash
codex plugin marketplace add Q00/ouroboros
codex plugin add ouroboros@ouroboros
```

### 独立 CLI

首次安装时，请先创建并激活新的虚拟环境。[独立 CLI 虚拟环境指南](/docs/first-run-detail/#cli-venv)提供了创建新目录、安装、激活和检查环境的命令。该链接页面为韩语，依据产品源码 `722172ef` 编写；其版本可能与本快速入门依据的 `592c667f` 以及当前公开软件包不同，请检查已安装版本的帮助信息。

在已激活虚拟环境的终端中运行：

```bash
python -m pip install ouroboros-ai
ouroboros --version
```

请根据已安装并完成认证、准备使用的 CLI 明确选择运行时。如果已经安装 Claude Code CLI 并完成认证，请运行：

```bash
ouroboros setup --runtime claude-cli
```

如果已经安装 Codex CLI 并完成认证，请运行：

```bash
ouroboros setup --runtime codex
```


**Codex CLI 服务器（macOS/Linux/WSL2 独立 CLI 路径）：**这与安装 Codex 插件是两回事。以下本地 stdio 步骤不适用于原生 Windows PowerShell。在同一 shell 中使用官方 `0.59.9` CLI 且 PATH 中有 `uvx` 时，`ouroboros setup --runtime codex` 会注册隔离启动器 `uvx --from ouroboros-ai[mcp]==0.59.9 ...`；当前 CLI 环境无需安装 `[mcp]` extra。请在运行 setup 的同一 shell 中检查 `command -v ouroboros`、`ouroboros --version` 和 `command -v uvx`，确认使用的 CLI 与启动器。其他已安装发行版会将启动器固定到各自的安装版本。

如果没有 `uvx`，请在一个尚不存在的路径创建单独的 MCP 2 环境。以下 macOS/Linux/WSL2 命令使用时间戳生成路径，并在路径已存在时停止。每一步成功后再继续；若失败，请换一个新路径，不要复用未完整安装的环境。

```bash
MCP_VENV="$HOME/.venvs/ouroboros-codex-mcp2-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$HOME/.venvs" &&
test ! -e "$MCP_VENV" &&
python -m venv "$MCP_VENV" &&
source "$MCP_VENV/bin/activate" &&
test "$(command -v python)" = "$MCP_VENV/bin/python" &&
python -m pip install 'ouroboros-ai[mcp]==0.59.9' &&
test "$(command -v ouroboros)" = "$MCP_VENV/bin/ouroboros" &&
python -m pip show ouroboros-ai mcp &&
! command -v uvx &&
command -v codex &&
ouroboros setup --runtime codex
```

若使用 Git/dev 源码检出，请在仓库根目录向该源码的 Python 环境安装 `python -m pip install -e '.[mcp]'`，然后在 `command -v codex` 成功的 shell 中运行 `python -m ouroboros setup --runtime codex`。setup 成功只表示服务器入口已注册，并不验证 Codex 的实时连接或工具发现；请另行确认 Codex 中实际出现了 Ouroboros 工具。MCP 2 `[mcp]` 不要与包含 MCP 1 依赖的 `[claude]` 或 `[claude-sdk]` 安装在同一环境中。

**原生 Windows Codex Desktop：**`auto` 模式可能跳过新的 MCP 注册却报告成功；不要把成功提示当作已注册的证明。请使用 WSL2 执行以上 stdio 步骤，或查看独立的 loopback HTTP 流程：`ouroboros setup --runtime codex --mcp-mode http`。该流程要求先单独启动 setup 打印的服务器命令，再打开 Codex，并使用 `127.0.0.1:8765/mcp`。[Windows 行为（main）](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/windows_codex_mcp.py) · [Windows 行为（0.59.9）](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/windows_codex_mcp.py) · [Codex 启动器](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/codex_mcp_launcher.py) · [setup 分支](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L698-L720) · [软件包配置](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L73-L89)

如果计划使用的 CLI 尚未安装或尚未完成认证，请先按照该运行时的提供方说明完成安装和认证，再选择相应选项。若两者都已安装，请选择实际计划使用的一种。如果只检测到一个运行时，不带运行时参数执行 `ouroboros setup` 会自动选择它；若该运行时是 Claude Code CLI，则会选择 `claude` SDK 路径。检测到多个运行时时，交互模式会提示你选择。非交互模式下，如果现有配置对应的运行时仍可用，程序会保留该配置；否则，若检测到 `claude`，会优先选择 SDK 路径，再不然选择第一个可用运行时。基础 `ouroboros-ai` 软件包不包含 Claude Agent SDK，因此 worker 预检可能会在执行前停止。如果你需要 Python SDK 路径，请先检查已安装版本对应的 SDK extra 和前置条件：[setup 运行时选择](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4806-L4861)、[Claude 运行时设置](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/claude_setup.py#L27-L64)、[SDK 预检](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/adapter.py#L1201-L1215)，以及 [`claude` 与 `claude-sdk` extras](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L74-L82)。此处行为依据源码版本 `592c667f`；也请查看你所安装版本的帮助和说明。

`pip install` 不会固定本文所依据的 Git commit。`ouroboros --version` 显示的是该终端中的 CLI 软件包版本；它不会检查宿主可能单独运行的服务器版本。请检查设置结果和计划使用的运行时。其他安装方式和详细前提条件请参阅[产品安装指南](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)。

## 2. 描述目标并检查 Seed

**插件：**在新的 Claude Code 或 Codex 会话中打开任务目录，然后在宿主的**对话中**输入以下命令。

```text
ooo setup
ooo interview "一个可以添加今天的待办并将其标记为完成的简单网页应用"
```

**独立 CLI：**在任务目录的**终端**中输入：

```bash
ouroboros init start "一个可以添加今天的待办并将其标记为完成的简单网页应用"
```

Interview 可能会询问任务存储方式、如何标记为完成等需要决定的问题。请回答这些问题。例如，你可以决定刷新页面后待办是否仍应保留。这句话是**说明性示例**，不是实际输出。

Seed 是整理目标、约束和完成条件的规格说明。不同使用路径检查实际 Seed 的方式有所不同。

### 在插件对话中创建 Seed

上述源码中的 Interview skill 会在提问和检查完成后再次确认目标，然后提出创建 Seed。**不要因为 Interview 已结束就认定 Seed 已经创建。**确认目标后，请在同一对话中请求 `ooo seed`。如果你收到了 interview session ID，需要指定目标时可以使用 `ooo seed <实际 session ID>`。

成功生成后，请检查**完整的 Seed YAML**，而不只是完成提示。阅读目标、项目/目标路径、约束和可验证的完成条件，并与对话中达成一致的内容核对。skill 还会提供 QA 意见，但仅凭分数无法证明内容正确。如果看不到 YAML 或实际保存路径，或者生成失败、被中断，请勿运行它；请在同一会话中再次请求生成，或查看恢复指南。如果没有显示路径，不要猜测文件已经保存；请让宿主确认 Seed 内容及其是否已保存。

如果 MCP 服务器不可用，skill 会使用备用路径，根据对话中已确认的需求创建 Seed，并可能说明如何配置服务器连接。即使如此，也要检查实际显示的 YAML，并区分它与已确认保存的文件。上面的产品指南分别介绍了 Claude Code 和 Codex 的插件安装方式，但实际界面和 skill 调用方式仍需根据已安装的宿主和版本确认。[Interview skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

### 在独立 CLI 中检查 Seed

终端中的交互式 Interview 会询问是否创建 Seed。批准创建后，请检查实际显示的 Seed 文件路径及文件内容。如果出现 `Start workflow now?`，默认答案是“是”。如需先检查再执行，请选择 `n`。如果创建失败或被中断，不要假设文件已经存在。此行为依据上述源码；请以已安装版本的实际界面为准。

## 3. 运行任务并检查结果

在插件对话中，请求 Ouroboros 运行已检查的 Seed YAML，或指定其实际文件路径。使用独立 CLI 时，请在终端中使用实际生成路径运行 `ouroboros run <Seed 文件路径>`。不要原样输入带尖括号的示例路径。执行过程可能会更改代码和文件，并启动命令及模型调用。

普通 MCP 后台运行中，`orchestrator.use_worktrees` 默认开启；工作目录位于 Git 仓库内时，才有条件创建独立 worktree，但创建也可能失败。工作目录不在 Git 仓库内或该设置关闭时，可能不使用 worktree，而直接在指定的工作目录中执行。如果返回了 `worktree_path` 和 `worktree_branch`，请核对它们；否则请确认实际选用的工作目录。`dispatch_mode="plugin"` 是委派给 OpenCode 子 Task 的路径，与普通插件安装不同：它没有 job ID 或受管理的 worktree，应在 Task 窗格中追踪。运行完成后通常会启动正式评估。普通 MCP 评估 job 中，当 `auto_evolve` 开启且 `final_approved` 为 `false` 时，`rejected` 和 `unverified` 都可能触发对有次数限制的 Ralph 后续任务的登记尝试。是否实际运行取决于 Seed 是否可用及登记结果等条件；运行时可能产生额外时间和模型费用。请检查状态和最终结果。

运行过程中，请记录实际返回的 ID 和状态。仅凭完成提示或 ID 不能证明需求已满足。请检查以下内容：

1. 在运行结果报告的实际工作目录或 worktree 中检查创建或修改的文件。
2. 阅读测试和评估结果，并检查失败或未经验证的项目。
3. 如果还没有应用启动信息，请在实际工作路径下使用下面的请求，先询问如何启动应用。检查命令、来源、端口和费用，选择自己信任的方案后，再打开应用、添加待办并标记为完成。如果 Seed 规定了持久化条件，请在刷新页面后亲自确认该条件仍然满足。

**独立 CLI 用户：**请在实际生成的工作路径中查看 `README` 和项目软件包配置文件，查找依赖安装说明、启动脚本、URL 和端口以及停止方法。如果这些文件没有提供相关信息，或你无法判断如何运行，请勿猜测；请改用 Claude Code 或 Codex 等受支持的插件宿主，并使用下面的请求进行确认。

根据运行结果报告的实际工作路径或 `worktree_path`，可以在宿主中这样请求：

```text
请检查 <实际工作路径> 中的项目，并告诉我依赖安装命令及其来源、应用启动命令、实际 URL 和端口、停止方法以及预计费用。我会检查命令和来源，选择自己信任的方案，然后打开应用，确认能否添加待办并标记为完成。
```

这个请求示例并未验证应用是否确实能够运行。请确认回答符合项目和环境，并在继续之前检查命令、来源、端口及费用。

如果评估尚未启动、失败，或结果为 `unverified`，先核对实际 `session_id`、原始 Seed、产物以及返回的工作目录或 `worktree_path`。启动新评估前，先检查现有评估 job 和关联 Ralph job 的状态及结果；不要重复启动仍在运行的链。**如果是在连接了 MCP 的插件宿主对话中**，确需重新评估时，可请求宿主运行 `ooo evaluate <实际 session ID> [产物]`，并提供实际项目路径。`auto_evolve: false`只阻止本次评估安排新的 Ralph 后续任务，不会取消已经启动的评估或链。**不要在独立 CLI 终端输入这个宿主命令。**固定源码 `592c667f` 中没有单独的 CLI 评估重跑命令。请查看已安装版本的 `ouroboros --help` 和对应版本的指南；如果找不到受支持的方式，请使用连接了 MCP 的宿主。`unverified`不代表通过：补充或确认可执行检查，再按[评估详细指南](/docs/zh/troubleshooting/#evaluation)中的结果对应步骤处理。

状态查询方式取决于 ID 的类型。请在[进度与状态](/docs/zh/troubleshooting/#status)中查找对应路径。如果连接失败或任务中断，请保留现有记录，并先阅读[恢复指南](/docs/zh/troubleshooting/#recovery)。任务可能仍在运行，因此不要立即重新启动。

接下来可以阅读 [Interview 指南](/docs/interview-guide/)、[Seed 格式](/docs/seed-guide/)和[在现有项目中使用 Ouroboros](/docs/existing-project-detail/)。
