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

In a terminal with a new Python virtual environment activated:

```bash
python -m pip install ouroboros-ai
ouroboros --version
ouroboros setup
```

`pip install` does not pin the Git commit used by this document. `ouroboros --version` reports the CLI package in that terminal; it does not check the version of a server that the host may run separately. Review the setup result and the runtime you intend to use. For other installation paths and detailed prerequisites, see the [product installation guide](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md).

## 2. Describe Your Goal and Review the Seed

**Plugin:** Open the task folder in a new Claude Code or Codex session, then enter these commands in the host's **conversation**.

```text
ooo setup
ooo interview "A simple web app where I can add tasks for today and mark them complete"
```

**Standalone CLI:** Enter this command in a **terminal** opened in the task folder.

```bash
ouroboros init start "A simple web app where I can add tasks for today and mark them complete"
```

Answer the Interview's questions about decisions such as how to store tasks or mark them complete. For example, you might decide whether tasks should remain after a page refresh. That question is an **illustrative example**, not actual output.

A Seed is a specification that organizes the goal, constraints, and completion criteria. The steps for checking an actual Seed depend on your path.

### Create a Seed from a Plugin Conversation

The Interview skill in the source above confirms the goal after its questions and review, then offers to create a Seed. **Do not assume that a Seed was created just because the Interview ended.** Confirm the goal, then request `ooo seed` in the same conversation. If you received an interview session ID, you can target it when needed with `ooo seed <actual session ID>`.

After successful generation, check the **entire Seed YAML**, not just a completion message. Read the goal, work target, constraints, and verifiable completion criteria, then compare them with what you agreed to in the conversation. The skill also provides QA feedback, but a score alone does not establish that the content is correct. If you cannot see the YAML or its actual saved path, or generation failed or was interrupted, do not run it. Request generation again in the same session or check the recovery guidance. If no path is shown, do not guess that a file was saved; ask the host to confirm the Seed content and whether it was saved.

If the MCP server is unavailable, the skill uses a fallback path to create a Seed from the requirements confirmed in the conversation and may explain how to configure the server connection. In that case, still inspect the YAML actually presented and distinguish it from a confirmed saved file. The product guide above documents the plugin path for both Claude Code and Codex, but you must check the actual screens and skill invocation for your installed host and version. [Interview skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed skill](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

### Check the Seed in the Standalone CLI

The interactive Interview in the terminal asks whether to create a Seed. Approve creation, then check the actual Seed file path shown and its contents. If you see `Start workflow now?`, the default is yes. Choose `n` if you want to review the Seed before execution. If creation fails or is interrupted, do not assume a file exists. This behavior is based on the source above; check the screens in your installed version.

## 3. Run the Task and Review the Results

In a plugin conversation, ask Ouroboros to run the reviewed Seed YAML or specify its actual file path. In the standalone CLI, use the actual generated path in the terminal: `ouroboros run <Seed file path>`. Do not type an example path with angle brackets literally. Execution can change code and files and start commands and model calls.

A plugin background run uses a separate worktree by default, but confirm isolation from the returned `worktree_path` and `worktree_branch` fields; other dispatch modes can differ. A completed run normally starts formal evaluation, and rejection may trigger a bounded Ralph loop, with additional time and model costs. Check its status and final result.

Record the IDs and statuses actually returned while the task runs. A completion message or ID alone does not prove the requirements were met. Check the following:

1. Inspect created or modified files in the actual workspace or worktree reported by the run.
2. Read test and evaluation results, including any failed or unverified items.
3. Add a task and mark it complete in the app. If the Seed specified a persistence condition, verify it yourself after refreshing the page.

If evaluation has not started, failed, or returned `unverified`, first confirm the actual `session_id`, original Seed, artifact, and reported working directory or `worktree_path`. Check the status and result of any existing evaluation job and chained Ralph job before starting another; do not duplicate an active chain. When a new evaluation is appropriate, ask the host to run `ooo evaluate <actual session ID> [artifact]` and provide the absolute project path. `auto_evolve: false` prevents this evaluation from scheduling a new Ralph successor; it does not cancel an evaluation or chain already started. `unverified` is not approval: add or confirm executable checks, then follow the outcome-specific next step in the [evaluation guide](/docs/en/troubleshooting/#evaluation).

The right way to check status depends on the type of ID. Find the matching path in [Progress and status](/docs/en/troubleshooting/#status). If a connection fails or work is interrupted, preserve the existing records and read the [recovery guide](/docs/en/troubleshooting/#recovery) first. Work may still be running, so do not immediately start it again.

Next, explore the [Interview guide](/docs/interview-guide/), [Seed format](/docs/seed-guide/), and [Using Ouroboros with an existing project](/docs/existing-project-detail/).
