---
description: "本草稿用合成待办应用示例介绍从 Interview、Seed 到执行和结果检查的首次流程，依据产品 main 592，尚未在所有真实宿主中验证。"
---

# 开始第一个任务

> **部分翻译：** 本快速入门为草稿。状态、评估与恢复的简要指南提供中文；更广泛的详细指南目前为韩语。

选择一种安装方式，然后从 Interview 一直走到结果检查，完成一个**可以添加待办并标记完成的简单网页应用**。这个目标延续了[贯穿韩语指南的示例](https://ouroboros.page/learn/interview/)。

如果仓库中已有代码或需要保留的更改，请在运行前先阅读[现有项目指南（韩文）](/docs/existing-project-detail/)。

本指南草稿对照的是产品源码 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 中的[安装指南](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)。请勿假设公开发行版 `0.59.9`、现有指南标注的 `0.51.5`，以及你安装的插件和 MCP 服务器与此源码版本相同。本文的完整流程尚未在所有真实模型和宿主环境中运行验证。界面和问题会因版本、环境和你的回答而异。

## 开始前

- 检查网络连接、所选宿主或 Python 环境，以及计划使用的模型所需的认证和费用条件。模型调用可能需要时间，也可能产生费用。
- 执行过程可能创建或修改文件并运行命令。首次练习请使用一个与现有工作隔离的新目录，并在宿主中打开该目录。
- 安装和设置可能会更改软件包或配置文件。请先阅读每个提示再继续。查看[设置指南（韩文）](/docs/config-reference-detail/)，确认使用统计设置是否适用于你安装的版本和服务器进程。
- **安全：**不要直接在不可信代码库或敏感环境中运行。通过 `OrchestratorRunner` 的 Codex 执行路径可能强制使用 native bypass，从而关闭审批和 sandbox。继续前，请先确认独立操作系统、虚拟机或容器的文件与网络隔离。
- **费用：**`small` 不是总调用次数或总费用上限。重试可能升到更高 tier，验证等独立角色也可能增加调用。请检查提供方费用和用量控制。

<details>
<summary>源码条件与路由细节</summary>

<p><strong>信任与隔离：</strong> 新工作目录不是安全边界。在所引用的源码中，未显式传入权限模式时，部分基于 CLI 的 Interview 路径（包括 Codex）可能选择 <code>bypassPermissions</code>；部分备用运行时重试和验证路径也会请求该模式。此外，<code>OrchestratorRunner</code> 初始化会强制把传入 adapter 的权限设为该运行时的 native bypass 模式，因此不要假设原有 sandbox 设置仍然生效。对 Codex 而言，bypass 会同时取消审批门和 sandbox。这是特定路径的行为，并非每个宿主操作都会如此。不要直接在不可信代码库或敏感环境中运行。如确需继续，请使用独立隔离的操作系统、虚拟机或容器，并先检查其文件访问范围和网络策略。<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/factory.py#L113-L143">main Interview 权限解析</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/codex_permissions.py#L26-L50">Codex 权限映射</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L879-L879">Runner adapter 权限强制</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L5190-L5208">native bypass 设置</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/parallel_executor.py#L7068-L7074">重试路径</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/server/adapter.py#L2150-L2158">验证路径</a> · <a href="https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros">release <code>v0.59.9</code> 对应源码路径</a></p>

<p><strong>调用与费用：</strong> MCP 请求中的 <code>model_tier=small</code> 表示请求 <code>frugal</code> 执行 tier，但不保证实际运行某个特定模型。显式模型 pin、backend 的 tier ladder 支持、native model override 支持和配置会影响路由是否生效及实际模型。可信的分解子任务可能降低一个 tier；部分失败重试会升到更强 tier，验证等独立角色也可能额外调用模型。<code>small</code> 不是总调用次数或总费用上限。开始前请检查模型提供方的费用条款和用量控制。<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1116-L1125">MCP tier 参数</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L360-L399">tier 路由条件</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L503-L529">重试 tier 路由</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/server/adapter.py#L2150-L2162">验证模型调用</a> · <a href="https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros">release <code>v0.59.9</code> 对应源码路径</a></p>

</details>

## 1. 选择安装方式

| 使用环境 | 准备事项与安装命令的输入位置 | 第一个任务的输入位置 |
| --- | --- | --- |
| [Claude Code 插件](#install-claude) | 需要 Claude Code 和 `uv`。请在**终端**中输入下方安装命令。 | [新 Claude Code 会话的对话](#worktree-first-task) |
| [Codex 插件](#install-codex) | 需要已登录的 Codex CLI 和 `uvx`。请在**终端**中输入下方安装命令。 | [新 Codex 会话的对话](#worktree-first-task) |
| [独立 CLI](#install-cli) | 需要 Python 3.12 或更高版本，以及计划使用的运行时和认证方式。请在单独的虚拟环境中安装。 | [**终端**](#worktree-first-task) |

**请选择一种使用路径。**使用 Claude Code 或 Codex 插件时，只执行计划使用的那个宿主对应的安装命令，然后在宿主对话中输入第一个任务。独立 CLI 是另一条路径；Claude 和 Codex 安装命令直接显示在下方；独立 CLI 的安装与 MCP 步骤需要展开对应内容，并在终端中输入命令。


<span id="install-claude"></span>

### Claude Code

在终端中运行：

```bash
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
```

<span id="install-codex"></span>

### Codex

在终端中运行：

```bash
codex plugin marketplace add Q00/ouroboros
codex plugin add ouroboros@ouroboros
```

<span id="install-cli"></span>

### 独立 CLI

<details>
<summary>独立 CLI 用户：展开查看安装、运行时和 Codex MCP 设置</summary>

<p><strong>共同准备</strong></p>

<h4 id="standalone-cli-venv-zh">创建独立的 Python 环境</h4>

<p>独立 CLI 请使用新的 Python 3.12+ 虚拟环境。以下示例会在当前目录创建新的 <code>ouroboros-cli-env</code> 文件夹；如果该路径已存在，先停止并另选路径。<a href="/docs/first-run-detail/#cli-venv">独立 CLI 虚拟环境指南</a>为韩语页面，依据产品源码 <code>722172ef</code> 编写；其版本可能与本快速入门依据的 <code>592c667f</code> 以及当前公开软件包不同，请检查已安装版本的帮助信息。</p>

<p><strong>macOS、Linux 或 WSL 终端：</strong></p>

<pre><code class="language-bash">python3 --version &amp;&amp;
mkdir ouroboros-cli-env &amp;&amp;
cd ouroboros-cli-env &amp;&amp;
python3 -m venv .venv &amp;&amp;
source .venv/bin/activate &amp;&amp;
python -m pip install ouroboros-ai &amp;&amp;
ouroboros --version</code></pre>

<p><strong>Windows PowerShell：</strong>请使用 Python 3 Launcher；示例会在创建环境前检查它所选的解释器是否为 Python 3.12 或更高版本。</p>

<pre><code class="language-powershell">$ErrorActionPreference = "Stop"
py -3 --version
if ($LASTEXITCODE -ne 0) { throw "请通过 Python Launcher 安装或注册 Python 3.12 或更高版本。" }
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw "所选 Python 版本低于 3.12；请安装或注册 Python 3.12 或更高版本。" }
if (Test-Path .\ouroboros-cli-env) { throw "请另选一个新目录；此路径已存在。" }
New-Item -ItemType Directory -Path .\ouroboros-cli-env | Out-Null
Set-Location .\ouroboros-cli-env
py -3 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "虚拟环境创建失败。" }
$OuroborosPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
$OuroborosPython
& $OuroborosPython -m pip install ouroboros-ai
if ($LASTEXITCODE -ne 0) { throw "软件包安装失败。" }
& $OuroborosPython -m ouroboros --version
if ($LASTEXITCODE -ne 0) { throw "CLI 版本检查失败。" }</code></pre>

<p>此方法直接使用虚拟环境解释器，不运行 <code>Activate.ps1</code>，也不需要更改执行策略。请保留输出的绝对路径并存入 <code>$OuroborosPython</code>；使用 <code>Set-Location</code> 移动到项目目录后，它仍指向同一虚拟环境。打开新的 PowerShell 会话时，请再次将保存的准确绝对解释器路径赋给 <code>$OuroborosPython</code>。这些 Windows 命令依据 Python 和 PowerShell 约定编写，未在 Windows 上实际运行。</p>

<p>在已激活虚拟环境的终端中运行：</p>

<pre><code class="language-bash">python -m pip install ouroboros-ai
ouroboros --version</code></pre>

<p><strong>选择 Claude CLI</strong></p>

<p>请根据已安装并完成认证、准备使用的 CLI 明确选择运行时。如果已经安装 Claude Code CLI 并完成认证，请运行：</p>

<pre><code class="language-bash">ouroboros setup --runtime claude-cli</code></pre>

<p>Windows PowerShell：</p>

<pre><code class="language-powershell">&amp; $OuroborosPython -m ouroboros setup --runtime claude-cli</code></pre>

<p><strong>Codex CLI 与 Windows 支持范围</strong></p>

<p><strong>平台支持范围：</strong>已核对的产品文档将原生 Windows 标为实验性，且不支持在原生 Windows 上使用 Codex CLI。Windows 用户建议使用 WSL2 路径。 <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/platform-support.md#L16-L27">main</a> · <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/docs/platform-support.md#L16-L27">release 0.59.9</a>.</p>

<p>如果已经安装 Codex CLI 并完成认证，请运行：</p>

<pre><code class="language-bash">ouroboros setup --runtime codex</code></pre>



<p>Windows PowerShell：</p>

<pre><code class="language-powershell">&amp; $OuroborosPython -m ouroboros setup --runtime codex</code></pre>

<p><strong>Codex：已有 uvx</strong></p>

<p><strong>Codex CLI 服务器（macOS/Linux/WSL2 独立 CLI 路径）：</strong>这与安装 Codex 插件是两回事。以下本地 stdio 步骤不适用于原生 Windows PowerShell。在同一 shell 中使用官方 <code>0.59.9</code> CLI 且 PATH 中有 <code>uvx</code> 时，<code>ouroboros setup --runtime codex</code> 会注册隔离启动器 <code>uvx --from ouroboros-ai[mcp]==0.59.9 ...</code>；当前 CLI 环境无需安装 <code>[mcp]</code> extra。请在运行 setup 的同一 shell 中检查 <code>command -v ouroboros</code>、<code>ouroboros --version</code> 和 <code>command -v uvx</code>，确认使用的 CLI 与启动器。其他已安装发行版会将启动器固定到各自的安装版本。</p>

<p><strong>Codex：没有 uvx</strong></p>

<p>如果没有 <code>uvx</code>，请在一个尚不存在的路径创建单独的 MCP 2 环境。以下 macOS/Linux/WSL2 命令使用时间戳生成路径，并在路径已存在时停止。每一步成功后再继续；若失败，请换一个新路径，不要复用未完整安装的环境。</p>

<pre><code class="language-bash">MCP_VENV="$HOME/.venvs/ouroboros-codex-mcp2-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$HOME/.venvs" &amp;&amp;
test ! -e "$MCP_VENV" &amp;&amp;
python -m venv "$MCP_VENV" &amp;&amp;
source "$MCP_VENV/bin/activate" &amp;&amp;
test "$(command -v python)" = "$MCP_VENV/bin/python" &amp;&amp;
python -m pip install 'ouroboros-ai[mcp]==0.59.9' &amp;&amp;
test "$(command -v ouroboros)" = "$MCP_VENV/bin/ouroboros" &amp;&amp;
python -m pip show ouroboros-ai mcp &amp;&amp;
! command -v uvx &amp;&amp;
command -v codex &amp;&amp;
ouroboros setup --runtime codex</code></pre>

<p><strong>开发源码检出</strong></p>

<p>若使用 Git/dev 源码检出，请在仓库根目录向该源码的 Python 环境安装 <code>python -m pip install -e '.[mcp]'</code>，然后在 <code>command -v codex</code> 成功的 shell 中运行 <code>python -m ouroboros setup --runtime codex</code>。setup 成功只表示服务器入口已注册，并不验证 Codex 的实时连接或工具发现；请另行确认 Codex 中实际出现了 Ouroboros 工具。MCP 2 <code>[mcp]</code> 不要与包含 MCP 1 依赖的 <code>[claude]</code> 或 <code>[claude-sdk]</code> 安装在同一环境中。</p>

<p><strong>Windows 例外</strong></p>

<p><strong>Codex Desktop HTTP 只是服务器注册方式，并不能证明原生 Windows Codex CLI 的端到端执行受支持。</strong></p>

<p><strong>原生 Windows Codex Desktop：</strong><code>auto</code> 模式可能跳过新的 MCP 注册却报告成功；不要把成功提示当作已注册的证明。请使用 WSL2 执行以上 stdio 步骤，或查看独立的 loopback HTTP 流程：<code>ouroboros setup --runtime codex --mcp-mode http</code>。该流程要求先单独启动 setup 打印的服务器命令，再打开 Codex，并使用 <code>127.0.0.1:8765/mcp</code>。<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/windows_codex_mcp.py">Windows 行为（main）</a> · <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/windows_codex_mcp.py">Windows 行为（0.59.9）</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/codex_mcp_launcher.py">Codex 启动器</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L698-L720">setup 分支</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L73-L89">软件包配置</a></p>

<p>如果计划使用的 CLI 尚未安装或尚未完成认证，请先按照该运行时的提供方说明完成安装和认证，再选择相应选项。若两者都已安装，请选择实际计划使用的一种。如果只检测到一个运行时，不带运行时参数执行 <code>ouroboros setup</code> 会自动选择它；若该运行时是 Claude Code CLI，则会选择 <code>claude</code> SDK 路径。检测到多个运行时时，交互模式会提示你选择。非交互模式下，如果现有配置对应的运行时仍可用，程序会保留该配置；否则，若检测到 <code>claude</code>，会优先选择 SDK 路径，再不然选择第一个可用运行时。基础 <code>ouroboros-ai</code> 软件包不包含 Claude Agent SDK，因此 worker 预检可能会在执行前停止。如果你需要 Python SDK 路径，请先检查已安装版本对应的 SDK extra 和前置条件：<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4806-L4861">setup 运行时选择</a>、<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/claude_setup.py#L27-L64">Claude 运行时设置</a>、<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/adapter.py#L1201-L1215">SDK 预检</a>，以及 <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L74-L82"><code>claude</code> 与 <code>claude-sdk</code> extras</a>。此处行为依据源码版本 <code>592c667f</code>；也请查看你所安装版本的帮助和说明。</p>

<p><code>pip install</code> 不会固定本文所依据的 Git commit。<code>ouroboros --version</code> 显示的是该终端中的 CLI 软件包版本；它不会检查宿主可能单独运行的服务器版本。请检查设置结果和计划使用的运行时。其他安装方式和详细前提条件请参阅<a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md">产品安装指南</a>。</p>

</details>

## 2. 描述目标并检查 Seed

<span id="worktree-first-task"></span>

!!! warning "运行前检查受管理 worktree 路径"
    使用 worktree 的执行在准备时，如果 `<worktree_root>/<仓库名称>/<durable_id>` 已存在但未在目标仓库注册为 Git worktree，可能尝试递归删除该路径。默认 root 为 `~/.ouroboros/worktrees`。新的 CLI 执行以及未另行提供 ID 的普通 MCP 执行会在运行中生成 ID，因此无法事先知道精确的新路径。开始前请检查实际管理 root、仓库对应目录、在目标仓库用 `git worktree list --porcelain` 检查 Git worktree 注册，以及进行中的工作和需要保留的数据。恢复时，如有实际 session ID 和已保存的 workspace 路径，也请核对这些记录。若无法确认，请暂缓执行，不要擅自删除或覆盖不确定的路径。检查后仍可能发生并发变化；这也不代表所有路径都能删除成功。 [source](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py#L328-L357) [CLI main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L843-L860) · [CLI release](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run.py#L843-L860) · [MCP main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1250-L1278)

**操作顺序：**Claude Code：设置 → Interview → 创建 Seed → 共同检查；Codex：检查插件和 MCP 连接 → Interview → 创建 Seed → 共同检查；独立 CLI：准备 → Interview → 批准创建 Seed → 共同检查。

<span id="plugin-first-task"></span>**Claude Code 插件：**在新会话中打开任务目录，然后在宿主的**对话中**请求设置。

```text
ooo setup
```

回答设置问题并完成设置。<span id="codex-first-task"></span>**Codex 插件：**在新的 Codex 会话中打开任务目录，确认已安装的插件和 MCP 工具已连接；如未连接，请先查看 [MCP 诊断指南（韩文）](/docs/ai-troubleshooting/#mcp)。独立 Codex CLI 设置是另一条路径。

准备好后，在宿主对话的下一条消息中发送 Interview 请求。

```text
ooo interview "构建一个简单的网页应用，让我可以添加今天的待办并将其标记为完成。项目 README 需说明依赖安装方法、应用启动命令、实际访问地址和端口、停止方法，以及测试命令和测试范围。"
```

### 在插件对话中创建 Seed

Interview skill 会重新确认目标并提出创建 Seed。同意目标后，在同一对话中请求 `ooo seed`。如果收到了 interview session ID，需要指定目标时可使用 `ooo seed <实际 session ID>`。skill 会提供 QA 意见，但仅凭分数无法证明内容正确。

如果 MCP 不可用，skill 会使用备用路径，根据对话中确认的需求创建 Seed，并可能说明服务器连接设置。仍需检查实际显示的 YAML 和文件是否保存。产品指南涵盖 Claude Code 和 Codex 插件，但实际界面及 skill 调用方式取决于已安装的宿主和版本。[Interview skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

<span id="cli-first-task"></span>**独立 CLI：**在任务目录的**终端**中输入：

```bash
ouroboros init start "构建一个简单的网页应用，让我可以添加今天的待办并将其标记为完成。项目 README 需说明依赖安装方法、应用启动命令、实际访问地址和端口、停止方法，以及测试命令和测试范围。"
```

Windows PowerShell（项目目录中）：

```powershell
& $OuroborosPython -m ouroboros init start "构建一个简单的网页应用，让我可以添加今天的待办并将其标记为完成。项目 README 需说明依赖安装方法、应用启动命令、实际访问地址和端口、停止方法，以及测试命令和测试范围。"
```

### 在独立 CLI 中检查 Seed

在终端的交互式 Interview 中批准创建 Seed，然后检查实际显示的文件路径和内容。出现 `Start workflow now?` 时，默认答案是“是”；如需先检查再执行，请选择 `n`。此行为依据上述源码，请以已安装版本的实际界面为准。

### 两种路径共同步骤：检查生成的 Seed {#shared-seed-review}

回答 Interview 的问题。例如，你可以决定刷新页面后待办是否仍应保留；这只是**说明性示例**，不是实际输出。Seed 是整理目标、约束和完成条件的规格说明。**Interview 结束不等于 Seed 已创建。**按照上面所选路径确认生成，检查完整 YAML 中的目标、工作对象、约束和可验证的完成条件，并核对实际保存路径和文件内容。批准前不要运行。

**检查示例：**以下只是字段含义的局部示例，不是完整 Seed，也不是实际输出或结果。请与对话中实际达成的约定比较。

- `goal`：构建可以添加待办并标记完成的网页应用。
- `constraints`：遵守已约定的约束；例如，仅在已约定时保留现有数据。
- `acceptance_criteria`：检查添加并完成的待办在刷新后仍保留完成状态。只有约定了持久化条件时才加入此项。

请分别核对实际返回的 Seed 文件路径和所选工作文件夹，不要假设 YAML 中一定存在工作文件夹字段。如果目标、约束、标准或工作对象与约定不符，请直接编辑现有 YAML 并重新检查完整内容。[固定版本 Seed 模型](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/seed.py#L925-L948)

检查 README 验收标准是否要求说明依赖安装、应用启动命令、实际 URL 和端口、停止方法，以及测试命令和范围。如果没有测试，可以要求 README 明确说明。这是所要求的结果，不表示 README 已存在、准确或经过测试。

**如果结果不同：**

- **已有 YAML 和文件，但缺少标准或与目标不符：**直接编辑现有 YAML，再重新检查完整内容。不要重新生成并覆盖已成功创建的文件；覆盖现有文件前先检查其内容。
- **已返回 YAML，但没有保存文件或路径：**检查该 YAML，将它保存到合适的新 Seed 文件，再核对实际路径和保存内容。不要仅因文件缺失而重新生成。
- **没有 YAML，或生成失败、中断：**不要运行。只有此时才请求恢复生成或索取原始 Seed 产物。

## 3. 运行任务并检查结果

**操作顺序：**先阅读下方检查和警告 → 运行已检查的 Seed → 保存实际返回的 ID 与工作路径 → 检查文件、测试和评估结果 → 遇到问题时查看[故障排除](/docs/zh/troubleshooting/#recovery)。

如果这是刚初始化的 Git 仓库，且普通 MCP 后台运行将使用默认的受管理 worktree 设置，请在项目目录运行 `git rev-parse --verify HEAD` 检查是否已有初始提交。如果因没有提交而失败，请先检查文件，并由你自己决定是否以及提交哪些内容，再重试；不要让代理自动创建提交。此检查只针对默认受管理 worktree 路径：非 Git 目录、`orchestrator.use_worktrees: false`，以及独立的 `dispatch_mode="plugin"` OpenCode Task 路径可能有不同表现。在针对候选版本 `965c1d94` 的一次隔离试验中，对执行过 `git init` 但尚无提交的仓库返回了 `launch_workspace_unavailable`；该观察不能推广到所有宿主或分派模式。请参阅固定版本的 [main worktree 基准检查](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py#L374-L385)、[默认 worktree 设置](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/models.py#L775-L780)及对应的 [release `0.59.9` worktree 源码](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/worktree.py#L374-L385)。

**实际工作位置：** 普通 MCP 后台运行中，`orchestrator.use_worktrees` 默认开启；工作目录位于 Git 仓库内时，才有条件创建独立 worktree，但创建也可能失败。工作目录不在 Git 仓库内或该设置关闭时，可能不使用 worktree，而直接在指定的工作目录中执行。如果返回了 `worktree_path` 和 `worktree_branch`，请核对它们；否则请确认实际选用的工作目录。`dispatch_mode="plugin"` 是委派给 OpenCode 子 Task 的路径，与普通插件安装不同：它没有 job ID 或受管理的 worktree，应在 Task 窗格中追踪。

**自动后续评估：** 运行完成后不一定会启动正式评估。普通 MCP 运行只有在 `auto_evaluate` 已开启且运行结果符合评估条件时，才会尝试登记正式评估 job。设置关闭、结果不符合条件或登记失败时，评估可能不会启动；请核对实际评估状态和 job ID。评估启动后，普通 MCP 评估 job 中若 `auto_evolve` 已开启且 `final_approved` 为 `false`，`rejected` 和 `unverified` 都可能触发对有次数限制的 Ralph 后续任务的登记尝试。是否实际运行取决于 Seed 是否可用及登记结果等条件；运行时可能产生额外时间和模型费用。请检查状态和最终结果。

在插件对话中，请求 Ouroboros 运行已检查的 Seed YAML，或指定其实际文件路径。使用独立 CLI 时，请在终端中使用实际生成路径运行 `ouroboros run <Seed 文件路径>`。不要原样输入带尖括号的示例路径。Windows PowerShell 中，请将实际路径放在双引号内并运行：

```powershell
& $OuroborosPython -m ouroboros run "<实际 Seed 文件路径>"
```

执行过程可能会更改代码和文件，并启动命令及模型调用。

**说明用虚构示例：**假设原执行结束后满足条件，一个评估 job 进入等待队列。等待不代表已批准。如果实际返回了评估 job ID，请检查该 job 的状态和结果。即使评估批准，也仍需单独打开实际应用并检查需求。这不是实际输出，也不表示每次运行都会创建评估；宿主与独立 CLI 的状态查看路径可能不同。[main 后续评估条件](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run_successors.py#L58-L95) · [release 后续评估条件](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run_successors.py#L58-L95)

运行过程中，请记录实际返回的 ID 和状态。仅凭完成提示或 ID 不能证明需求已满足。请检查以下内容：

1. 在运行结果报告的实际工作目录或 worktree 中检查创建或修改的文件。
2. 阅读测试和评估结果，并检查失败或未经验证的项目。
3. 阅读实际工作路径中的 README，确认其中说明了依赖安装、应用启动、实际 URL 和端口、停止方法及测试方式。先检查命令和来源，再决定是否运行；然后打开应用、添加待办并标记为完成。如果 Seed 规定了持久化条件，请在刷新页面后亲自确认该条件仍然满足。
4. 将 README 的运行和测试说明与实际结果对照。如果文件不存在、内容不完整或与观察到的行为不一致，该验收标准仍未验证。不要推断未观察到的产物或成功运行结果。

**独立 CLI 用户：**请在实际生成的工作路径中查看 `README` 和项目软件包配置文件，查找依赖安装说明、启动脚本、URL 和端口以及停止方法。如果这些文件没有提供相关信息，或你无法判断如何运行，请勿猜测；请改用 Claude Code 或 Codex 等受支持的插件宿主，并使用下面的请求进行确认。

根据运行结果报告的实际工作路径或 `worktree_path`，可以在宿主中这样请求：

```text
请检查 <实际工作路径> 中的项目，并告诉我依赖安装命令及其来源、应用启动命令、实际 URL 和端口、停止方法以及预计费用。我会检查命令和来源，选择自己信任的方案，然后打开应用，确认能否添加待办并标记为完成。
```

这个请求示例并未验证应用是否确实能够运行。请确认回答符合项目和环境，并在继续之前检查命令、来源、端口及费用。

如果评估尚未启动、失败，或结果为 `unverified`，先核对实际 `session_id`、原始 Seed、产物以及返回的工作目录或 `worktree_path`。启动新评估前，先检查现有评估 job 和关联 Ralph job 的状态及结果；不要重复启动仍在运行的链。**如果是在连接了 MCP 的插件宿主对话中**，确需重新评估时，可请求宿主运行 `ooo evaluate <实际 session ID> [产物]`，并提供实际项目路径。`auto_evolve: false`只阻止本次评估安排新的 Ralph 后续任务，不会取消已经启动的评估或链。**不要在独立 CLI 终端输入这个宿主命令。**固定源码 `592c667f` 中没有单独的 CLI 评估重跑命令。请查看已安装版本的 `ouroboros --help` 和对应版本的指南；如果找不到受支持的方式，请使用连接了 MCP 的宿主。`unverified`不代表通过：补充或确认可执行检查，再按照[评估简要指南](/docs/zh/troubleshooting/#evaluation)中的结果对应步骤处理。

状态查询方式取决于 ID 的类型。请在[状态简要指南](/docs/zh/troubleshooting/#status)中查找对应路径。如果连接失败或任务中断，请保留现有记录，并先阅读[恢复简要指南](/docs/zh/troubleshooting/#recovery)。任务可能仍在运行，因此不要立即重新启动。

接下来可以阅读 [Interview 指南（韩文）](/docs/interview-guide/)、[Seed 格式（韩文）](/docs/seed-guide/)和[在现有项目中使用 Ouroboros（韩文）](/docs/existing-project-detail/)。
