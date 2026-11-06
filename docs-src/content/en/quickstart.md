# Start Your First Task

> **Partial translation:** This quickstart is a draft. Brief status, evaluation and recovery guidance is available in English; broader detailed guidance is currently in Korean.

Choose an installation path, then follow an example from Interview through result review to build a **simple web app where you can add tasks and mark them complete**. This goal continues the [Korean guide's running example](https://ouroboros.page/learn/interview/).

This draft is checked against the installation guide at product source [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) ([installation guide](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)). Do not assume that public release `0.59.9`, the existing guide's `0.51.5`, or your installed plugin and MCP server match this source. The full flow below has not been run and verified with every real model and host. Screens and questions vary by version, environment, and your answers.

## Before You Start

- Check your internet connection, the host or Python environment you chose, and the authentication and cost conditions for the model you plan to use. Model calls can take time and incur costs.
- Execution can create or modify files and run commands. For your first exercise, use a new folder separate from existing work, and open that folder in your host.
- Installation and setup can change packages or configuration files. Read each prompt before proceeding. Check the [settings guide](/docs/config-reference-detail/) to see whether the usage statistics setting applies to your installed version and server process.

## 1. Choose an Installation Path

| Environment | Prerequisites and where to enter installation commands | Where to enter your first task |
| --- | --- | --- |
| Claude Code plugin | Claude Code and `uv` are required. Enter the commands below in a **terminal**. | A new Claude Code session's conversation |
| Codex plugin | A signed-in Codex CLI and `uvx` are required. Enter the commands below in a **terminal**. | A new Codex session's conversation |
| Standalone CLI | Python 3.12 or later and the runtime and authentication you plan to use are required. Install in a separate virtual environment. | **Terminal** |

**Choose one path.** For a Claude Code or Codex plugin, use the installation commands for the host you plan to use, then enter your first task in that host conversation. The standalone CLI is a separate path. Expand its setup details below and enter those commands in a terminal.


### Claude Code

In a terminal:

```bash
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
```

### Codex

In a terminal:

```bash
codex plugin marketplace add Q00/ouroboros
codex plugin add ouroboros@ouroboros
```

### Standalone CLI

<details>
<summary>Standalone CLI users: open for installation, runtime, and Codex MCP setup</summary>

<p>For a first install, create and activate a new virtual environment. The <a href="/docs/first-run-detail/#cli-venv">standalone CLI virtual environment guide</a> has commands to create a new directory, install, activate, and check it. That linked guide is in Korean and is based on product source <code>722172ef</code>. Its version may differ from this quickstart's <code>592c667f</code> and from the current public package, so check the help for your installed version.</p>

<p>In a terminal with the virtual environment activated:</p>

<pre><code class="language-bash">python -m pip install ouroboros-ai
ouroboros --version</code></pre>

<p>Choose a runtime explicitly to match the CLI you have installed and authenticated. If Claude Code CLI is already installed and ready to use with your authentication, run:</p>

<pre><code class="language-bash">ouroboros setup --runtime claude-cli</code></pre>

<p>If Codex CLI is already installed and ready to use with your authentication, run:</p>

<pre><code class="language-bash">ouroboros setup --runtime codex</code></pre>

<p><strong>Codex CLI server (macOS/Linux/WSL2 standalone path):</strong> This is separate from installing the Codex plugin. The local stdio steps below do not apply to native Windows PowerShell. With the official <code>0.59.9</code> CLI and <code>uvx</code> on PATH in the same shell, <code>ouroboros setup --runtime codex</code> registers an isolated launcher, <code>uvx --from ouroboros-ai[mcp]==0.59.9 ...</code>; the current CLI environment does not need the <code>[mcp]</code> extra. In the same shell, check <code>command -v ouroboros</code>, <code>ouroboros --version</code>, and <code>command -v uvx</code> so you know which CLI and launcher setup will use. Other installed releases pin the launcher to their own installed version.</p>

<p>Without <code>uvx</code>, create a separate MCP 2 environment at a path that does not exist. These macOS/Linux/WSL2 commands use a timestamped path and stop if that path already exists. Continue only after each step succeeds; after a failure, choose a new path instead of reusing the partial environment.</p>

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

<p>For a Git/dev checkout, from the repository root install <code>python -m pip install -e '.[mcp]'</code> into that source's Python environment, then run <code>python -m ouroboros setup --runtime codex</code> in a shell where <code>command -v codex</code> succeeds. Setup success means the server entry was registered; it does not verify the live Codex connection or tool discovery. Confirm that Ouroboros tools actually appear in Codex. Keep MCP 2 <code>[mcp]</code> separate from <code>[claude]</code> or <code>[claude-sdk]</code>, which include MCP 1 dependencies.</p>

<p><strong>Native Windows Codex Desktop:</strong> <code>auto</code> mode may skip a new MCP registration while reporting success; do not treat setup success as proof of registration. Use WSL2 for the stdio steps above, or review the separate loopback HTTP flow with <code>ouroboros setup --runtime codex --mcp-mode http</code>. That flow requires starting the server command printed by setup before opening Codex and uses <code>127.0.0.1:8765/mcp</code>. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/windows_codex_mcp.py">Windows behavior (main)</a> · <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/windows_codex_mcp.py">Windows behavior (0.59.9)</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/codex_mcp_launcher.py">Codex launcher</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L698-L720">setup branch</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L73-L89">package profiles</a></p>

<p>If you have not installed or authenticated the CLI you plan to use, complete that provider's setup first, then choose the matching option. If both are installed, select the one you intend to use. If only one runtime is detected, <code>ouroboros setup</code> without a runtime argument selects it automatically; if that runtime is Claude Code CLI, it selects the <code>claude</code> SDK path. With multiple detected runtimes, interactive setup prompts you to choose. In non-interactive mode, setup keeps an existing configuration if its runtime is available; otherwise it prefers the <code>claude</code> SDK path when Claude is detected, then falls back to the first available runtime. The base <code>ouroboros-ai</code> package does not include the Claude Agent SDK, so worker preflight can stop before execution. If you intend to use the Python SDK, first check the SDK extra and prerequisites for your installed version: <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4806-L4861">setup runtime selection</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/claude_setup.py#L27-L64">Claude runtime setup</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/adapter.py#L1201-L1215">SDK preflight</a>, and the <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L74-L82"><code>claude</code> and <code>claude-sdk</code> extras</a>. This behavior describes source revision <code>592c667f</code>; check the help and guidance for your installed version too.</p>

<p><code>pip install</code> does not pin the Git commit used by this document. <code>ouroboros --version</code> reports the CLI package in that terminal; it does not check the version of a server that the host may run separately. Review the setup result and the runtime you intend to use. For other installation paths and detailed prerequisites, see the <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md">product installation guide</a>.</p>

</details>

## 2. Describe Your Goal and Review the Seed

**Plugin:** Open the task folder in a new Claude Code or Codex session, then enter these commands in the host's **conversation**.

```text
ooo setup
ooo interview "Build a simple web app where I can add tasks for today and mark them complete. Make the project README explain dependency installation, the app start command, its actual URL and port, how to stop it, and the test commands and what they cover."
```

**Standalone CLI:** Enter this command in a **terminal** opened in the task folder.

```bash
ouroboros init start "Build a simple web app where I can add tasks for today and mark them complete. Make the project README explain dependency installation, the app start command, its actual URL and port, how to stop it, and the test commands and what they cover."
```

Answer the Interview's questions about decisions such as how to store tasks or mark them complete. For example, you might decide whether tasks should remain after a page refresh. That question is an **illustrative example**, not actual output. Before running, review the complete Seed YAML and confirm its acceptance criteria require the project README to explain this project's dependency installation, app start command, actual URL and port, stop instructions, and test commands and their scope. If there is no test suite, the criteria can require the README to say so. If a criterion is missing or does not match your goal, revise and review the Seed first. This is a requested outcome, not a claim that a README has already been created, is accurate, or has been tested.

A Seed is a specification that organizes the goal, constraints, and completion criteria. The steps for checking an actual Seed depend on your path.

### Create a Seed from a Plugin Conversation

The Interview skill in the source above confirms the goal after its questions and review, then offers to create a Seed. **Do not assume that a Seed was created just because the Interview ended.** Confirm the goal, then request `ooo seed` in the same conversation. If you received an interview session ID, you can target it when needed with `ooo seed <actual session ID>`.

After successful generation, check the **entire Seed YAML**, not just a completion message. Read the goal, work target, constraints, and verifiable completion criteria, then compare them with what you agreed to in the conversation. In particular, confirm that the README acceptance criteria cover dependency installation, app startup, the actual address and port, how to stop the app, and test commands and scope. If a requirement is missing, revise or regenerate and review the Seed before execution. The skill also provides QA feedback, but a score alone does not establish that the content is correct. If you cannot see the YAML or its actual saved path, or generation failed or was interrupted, do not run it. Request generation again in the same session or check the recovery guidance. If no path is shown, do not guess that a file was saved; ask the host to confirm the Seed content and whether it was saved.

If the MCP server is unavailable, the skill uses a fallback path to create a Seed from the requirements confirmed in the conversation and may explain how to configure the server connection. In that case, still inspect the YAML actually presented and distinguish it from a confirmed saved file. The product guide above documents the plugin path for both Claude Code and Codex, but you must check the actual screens and skill invocation for your installed host and version. [Interview skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

### Check the Seed in the Standalone CLI

The interactive Interview in the terminal asks whether to create a Seed. Approve creation, then check the actual Seed file path shown and its contents. If you see `Start workflow now?`, the default is yes. Choose `n` if you want to review the Seed before execution. Confirm that its README acceptance criteria cover installation, startup, the actual address and port, stopping, and tests; if anything is missing, revise or regenerate and review before running. If creation fails or is interrupted, do not assume a file exists. This behavior is based on the source above; check the screens in your installed version.

## 3. Run the Task and Review the Results

In a plugin conversation, ask Ouroboros to run the reviewed Seed YAML or specify its actual file path. In the standalone CLI, use the actual generated path in the terminal: `ouroboros run <Seed file path>`. Do not type an example path with angle brackets literally. Execution can change code and files and start commands and model calls.

For a normal MCP background run, `orchestrator.use_worktrees` is enabled by default, and a working directory inside a Git repository is eligible for a separate worktree. Creation can fail. Outside a Git repository, or when the setting is disabled, execution may use the specified working directory without a worktree. Check `worktree_path` and `worktree_branch` if returned; otherwise confirm the actual selected working directory. The `dispatch_mode="plugin"` path delegates to an OpenCode child Task, which is distinct from ordinary plugin installation: it has no job ID or managed worktree, so follow it in the Task pane. A completed run normally starts formal evaluation. In a normal MCP evaluation job, when `auto_evolve` is enabled and `final_approved` is `false`, both `rejected` and `unverified` results may trigger an attempt to enqueue a bounded Ralph continuation. Whether it actually runs depends on conditions including Seed availability and the enqueue result; it can add time and model costs. Check its status and final result.

Record the IDs and statuses actually returned while the task runs. A completion message or ID alone does not prove the requirements were met. Check the following:

1. Inspect created or modified files in the actual workspace or worktree reported by the run.
2. Read test and evaluation results, including any failed or unverified items.
3. Read the README in the actual working path and check that it explains dependency installation, app startup, the actual URL and port, how to stop the app, and how to run tests. Review commands and sources before deciding whether to run them; then open the app, add a task, and mark it complete. If the Seed specified a persistence condition, verify it yourself after refreshing the page.
4. Compare the README's run and test instructions with what actually happened. If the file is missing, incomplete, or disagrees with observed behavior, that acceptance criterion is not yet verified. Do not infer an artifact or successful run that you did not observe.

**Standalone CLI users:** In the actual generated working path, inspect the `README` and project package configuration files for dependency instructions, start scripts, the URL and port, and how to stop the app. If those files do not provide the information or you cannot determine how to run it, do not guess; use the request below in a supported plugin host such as Claude Code or Codex.

From the working path reported by the run or its `worktree_path`, you can ask the host agent:

```text
Inspect the project in <actual working path> and tell me the dependency installation commands and their sources, the app start command, the actual URL and port, how to stop it, and any expected costs. I will review the commands and sources, choose an approach I trust, then open the app and check adding a task and marking it complete.
```

This request example does not verify that the app can actually be run. Check that the answer fits the project and environment, and review the commands, sources, port, and costs before proceeding.

If evaluation has not started, failed, or returned `unverified`, first confirm the actual `session_id`, original Seed, artifact, and reported working directory or `worktree_path`. Check the status and result of any existing evaluation job and chained Ralph job before starting another; do not duplicate an active chain. **In a plugin host conversation with connected MCP**, when a new evaluation is appropriate, ask the host to run `ooo evaluate <actual session ID> [artifact]` and provide the actual project path. `auto_evolve: false` prevents this evaluation from scheduling a new Ralph successor; it does not cancel an evaluation or chain already started. **Do not enter this host command in a standalone CLI terminal.** The fixed source `592c667f` has no separate CLI command for rerunning evaluation. Check `ouroboros --help` and version-specific guidance for your installed version; if you cannot find a supported path, use a host with connected MCP. `unverified` is not approval: add or confirm executable checks, then follow the outcome-specific next step in the [evaluation guide](/docs/en/troubleshooting/#evaluation).

The right way to check status depends on the type of ID. Find the matching path in [Progress and status](/docs/en/troubleshooting/#status). If a connection fails or work is interrupted, preserve the existing records and read the [recovery guide](/docs/en/troubleshooting/#recovery) first. Work may still be running, so do not immediately start it again.

Next, explore the [Interview guide](/docs/interview-guide/), [Seed format](/docs/seed-guide/), and [Using Ouroboros with an existing project](/docs/existing-project-detail/).
