---
description: "첫 작업을 인터뷰, Seed 작성, 실행, 결과 확인까지 따라가는 한국어 빠른 시작입니다. 합성 할 일 앱 예제이며 제품 main 592 기준입니다."
---

# 첫 작업 시작하기

설치 경로를 선택하고 **할 일을 추가하고 완료 표시하는 간단한 웹앱**을 목표로 Interview부터 결과 확인까지 살펴봅니다. 이 목표는 기존 [한국어 가이드의 연속 예제](https://ouroboros.page/learn/interview/)와 이어집니다.

기존 코드나 보존할 변경이 있는 저장소라면 실행 전에 [기존 프로젝트 안내](/docs/existing-project-detail/)를 먼저 읽으세요.

이 안내는 제품 소스 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [설치 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조한 초안입니다. 공개 릴리스 `0.59.9`, 기존 가이드 0.51.5, 설치한 플러그인과 MCP 서버가 이 소스와 동일하다고 가정하지 마세요. 아래 흐름 전체를 실제 모델과 모든 호스트에서 실행해 검증하지 않았습니다. 화면과 질문은 버전·환경·답변에 따라 달라집니다.

## 시작하기 전에

- 인터넷 연결, 선택한 호스트 또는 Python 환경, 사용할 모델의 인증과 비용 조건을 확인합니다. 모델 호출은 시간과 비용이 들 수 있습니다.
- 실행은 파일을 만들거나 수정하고 명령을 실행할 수 있습니다. 첫 실습에는 기존 작업과 분리된 새 폴더를 사용하고 해당 폴더를 호스트에서 엽니다.
- 설치·설정은 패키지나 설정 파일을 변경할 수 있습니다. 제시되는 선택을 읽고 진행하세요. 사용 통계 설정은 설치한 버전과 서버 프로세스에 적용되는지 [설정 안내](/docs/config-reference-detail/)에서 확인하세요.
- **안전:** 신뢰하지 않는 저장소나 민감한 환경에서 직접 실행하지 마세요. Codex로 `OrchestratorRunner`를 거치는 실행은 승인과 sandbox를 끄는 native bypass를 강제할 수 있습니다. 계속 진행하기 전에 별도 OS·가상 머신·컨테이너의 파일 접근과 네트워크 격리를 확인하세요.
- **비용:** `small`은 전체 호출 횟수나 비용 상한이 아닙니다. 재시도는 더 강한 tier로 올라갈 수 있고 검증 등 별도 역할도 추가 호출을 할 수 있습니다. 비용 조건과 사용량 제한을 확인하세요.

<details>
<summary>소스 경로와 라우팅 세부 조건</summary>

<p><strong>신뢰와 격리:</strong> 새 작업 폴더는 보안 경계가 아닙니다. 고정 소스에서 명시 권한이 전달되지 않은 일부 CLI 기반 Interview 경로(예: Codex)는 <code>bypassPermissions</code>를 선택할 수 있고, 일부 대체 실행 재시도·검증 경로도 이 모드를 지정합니다. 추가로 <code>OrchestratorRunner</code> 초기화는 전달된 adapter 권한을 해당 실행기의 native bypass 모드로 강제 설정합니다. 따라서 기존 sandbox 설정이 그대로 적용된다고 가정하지 마세요. Codex에서 bypass는 승인과 sandbox를 모두 끕니다. 이는 특정 경로의 동작이지 모든 호스트 작업에 대한 설명은 아닙니다. 신뢰하지 않는 저장소나 민감한 환경에서는 직접 실행하지 마세요. 진행이 필요하면 별도 OS·가상 머신·컨테이너에서 실행하고 파일 접근 범위와 네트워크 정책을 먼저 확인하세요. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/factory.py#L113-L143">main Interview 권한 선택</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/codex_permissions.py#L26-L50">Codex 권한 매핑</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L879-L879">Runner adapter 권한 강제</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L5190-L5208">native bypass 설정</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/parallel_executor.py#L7068-L7074">재시도 경로</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/server/adapter.py#L2150-L2158">검증 경로</a> · <a href="https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros">release <code>v0.59.9</code> 같은 소스 경로</a></p>

<p><strong>호출과 비용:</strong> MCP 요청에서 <code>model_tier=small</code>은 <code>frugal</code> 실행 tier를 요청합니다. 특정 모델 실행을 보장하지는 않습니다. 명시 모델 pin, backend의 tier ladder 지원, native model override 지원, 설정에 따라 라우팅 활성 여부와 실제 모델이 달라집니다. 신뢰된 분해 작업은 한 단계 낮아질 수 있고, 일부 실패 재시도는 더 강한 모델 tier로 올라가며 검증 같은 별도 역할이 추가 모델 호출을 할 수 있습니다. <code>small</code>은 전체 호출 횟수나 비용 상한이 아닙니다. 시작 전에 사용할 모델 제공자의 비용 조건과 사용량 제한을 확인하세요. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1116-L1125">MCP tier 입력</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L360-L399">tier 라우팅 조건</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L503-L529">재시도 tier 상승</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/server/adapter.py#L2150-L2162">main 검증 호출</a> · <a href="https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros">release <code>v0.59.9</code> 같은 소스 경로</a></p>

</details>

## 1. 설치 경로 고르기

| 사용하는 환경 | 준비와 설치 입력 위치 | 첫 작업 입력 위치 |
| --- | --- | --- |
| [Claude Code 플러그인](#install-claude) | Claude Code와 `uv`가 필요합니다. 아래 설치 명령은 **터미널**에 입력합니다. | [새 Claude Code 세션의 대화](#worktree-first-task) |
| [Codex 플러그인](#install-codex) | 로그인된 Codex CLI와 `uvx`가 필요합니다. 아래 설치 명령은 **터미널**에 입력합니다. | [새 Codex 세션의 대화](#worktree-first-task) |
| [독립 CLI](#install-cli) | Python 3.12 이상과 사용할 런타임·인증이 필요합니다. 별도 가상환경에서 설치합니다. | [**터미널**](#worktree-first-task) |

**한 경로만 고르세요.** Claude Code 또는 Codex 플러그인은 사용할 호스트 하나의 설치 명령을 실행한 뒤 호스트 대화에 첫 작업을 입력합니다. 독립 CLI는 별도 경로입니다. Claude와 Codex 설치 명령은 아래에 바로 표시됩니다. 독립 CLI의 설치·MCP 단계는 해당 항목을 펼쳐 확인하고 명령은 터미널에 입력하세요.


<span id="install-claude"></span>

### Claude Code

터미널에서:

```bash
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
```

<span id="install-codex"></span>

### Codex

터미널에서:

```bash
codex plugin marketplace add Q00/ouroboros
codex plugin add ouroboros@ouroboros
```

<span id="install-cli"></span>

### 독립 CLI

<details>
<summary>독립 CLI 사용자: 설치·런타임·Codex MCP 설정 보기</summary>

<p>처음 설치한다면 새 가상환경을 만들고 활성화해야 합니다. <a href="/docs/first-run-detail/#cli-venv">독립 CLI 가상환경 안내</a>에 새 디렉터리 생성, 설치, 활성화와 확인 명령이 있습니다. 이 링크는 한국어 안내이며 제품 소스 <code>722172ef</code> 기준입니다. 이 quickstart의 <code>592c667f</code> 및 현재 공개 패키지와 판본이 다를 수 있으므로 설치된 버전의 도움말을 확인하세요.</p>

<p>macOS·Linux·WSL에서는 가상환경을 활성화한 터미널에서 명령을 실행합니다. Windows PowerShell은 <a href="/docs/first-run-detail/#cli-venv">가상환경 상세 안내</a>의 비활성화 직접 경로를 따르세요. 가상환경 디렉터리에서 다음을 실행해 확인한 절대 Python 경로를 기록합니다. 작업 폴더로 <code>Set-Location</code>한 뒤에도 같은 PowerShell 세션에서는 <code>$OuroborosPython</code>을 그대로 사용할 수 있습니다. 새 PowerShell 세션에서는 저장한 실제 절대 경로로 변수를 다시 지정하세요.</p>

<pre><code class="language-powershell">$OuroborosPython = (Resolve-Path .\.venv\Scripts\python.exe).Path
$OuroborosPython
&amp; $OuroborosPython -m ouroboros --version</code></pre>

<p>아래의 독립 CLI 설정·Interview·실행 명령에 대해서도 Windows PowerShell에서는 <code>&amp; $OuroborosPython -m ouroboros</code>를 앞에 붙입니다.</p>

<pre><code class="language-bash">python -m pip install ouroboros-ai
ouroboros --version</code></pre>

<p>설치된 CLI와 인증 상태에 맞춰 런타임을 명시적으로 선택하세요. Claude Code CLI를 이미 설치하고 인증해 사용할 준비가 되었다면:</p>

<pre><code class="language-bash">ouroboros setup --runtime claude-cli</code></pre>

<p>Windows PowerShell:</p>

<pre><code class="language-powershell">&amp; $OuroborosPython -m ouroboros setup --runtime claude-cli</code></pre>

<p><strong>플랫폼 지원 경계:</strong> 확인한 제품 문서에서 네이티브 Windows는 실험적이며 Codex CLI는 네이티브 Windows에서 지원하지 않습니다. Windows에서는 WSL2 경로를 권장합니다. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/platform-support.md#L16-L27">main</a> · <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/docs/platform-support.md#L16-L27">release 0.59.9</a>.</p>

<p>Codex CLI를 이미 설치하고 인증해 사용할 준비가 되었다면:</p>

<pre><code class="language-bash">ouroboros setup --runtime codex</code></pre>



<p>Windows PowerShell:</p>

<pre><code class="language-powershell">&amp; $OuroborosPython -m ouroboros setup --runtime codex</code></pre>

<p><strong>Codex CLI 서버 (macOS/Linux/WSL2 독립 CLI 경로):</strong> Codex 플러그인 설치와 별도 절차입니다. 아래 로컬 stdio 안내는 native Windows PowerShell에는 적용하지 않습니다. 공식 <code>0.59.9</code> CLI를 사용하고 같은 셸에서 <code>uvx</code>가 PATH에 있으면 <code>ouroboros setup --runtime codex</code>가 격리 런처 <code>uvx --from ouroboros-ai[mcp]==0.59.9 ...</code>를 Codex 설정에 등록합니다. 이때 현재 CLI 환경에 <code>[mcp]</code> extra는 필요하지 않습니다. 사용 중인 CLI 경로·판본과 런처를 확인하려면 <code>command -v ouroboros</code>, <code>ouroboros --version</code>, <code>command -v uvx</code>를 setup과 같은 셸에서 확인하세요. 설치 버전이 다르면 런처는 현재 설치판의 버전에 맞춰 고정됩니다.</p>

<p><code>uvx</code>가 없다면 MCP 2 서버용으로 아직 없는 별도 가상환경을 만드세요. 아래 macOS/Linux/WSL2 명령은 타임스탬프로 경로를 새로 만들고, 이미 존재하는 경로면 설치를 멈춥니다. 각 단계가 성공한 뒤 다음으로 진행하며, 실패했다면 같은 경로를 재사용하지 말고 새 이름을 고르세요.</p>

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

<p>Git/dev 체크아웃은 저장소 루트에서 그 소스와 같은 Python 환경에 <code>python -m pip install -e '.[mcp]'</code>를 설치하고, <code>command -v codex</code>가 성공하는 셸에서 <code>python -m ouroboros setup --runtime codex</code>를 실행하세요. setup 성공은 서버 항목 등록이지 Codex 연결이나 도구 발견의 검증이 아닙니다. Codex 호스트에서 실제 Ouroboros 도구가 보이는지 별도로 확인하세요. MCP 2 <code>[mcp]</code>를 MCP 1 의존성이 있는 <code>[claude]</code> 또는 <code>[claude-sdk]</code>와 같은 환경에 설치하지 마세요.</p>

<p><strong>Codex Desktop HTTP 등록은 서버 등록 방식일 뿐 네이티브 Windows Codex CLI의 전체 실행 지원을 입증하지 않습니다.</strong></p>

<p><strong>Native Windows Codex Desktop:</strong> <code>auto</code> 모드는 새 MCP 등록을 건너뛰고 성공을 보고할 수 있으므로 setup 성공을 등록 증거로 보지 마세요. 이 흐름 대신 WSL2를 사용하거나 <code>ouroboros setup --runtime codex --mcp-mode http</code>의 별도 loopback HTTP 경로를 검토하세요. HTTP 경로는 setup 출력에 제시되는 서버 명령을 별도로 실행한 뒤 Codex를 열어야 하며, <code>127.0.0.1:8765/mcp</code>를 사용합니다. <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/windows_codex_mcp.py">Windows 동작 (main)</a> · <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/windows_codex_mcp.py">Windows 동작 (0.59.9)</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/codex_mcp_launcher.py">Codex 런처</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L698-L720">setup 분기</a> · <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L73-L89">패키지 프로필</a></p>

<p>아직 사용할 CLI가 없거나 인증하지 않았다면 먼저 해당 런타임을 설치하고 인증한 뒤 맞는 선택지를 사용하세요. 둘 다 설치되어 있다면 실제로 사용할 런타임을 고릅니다. 감지된 런타임이 하나뿐이면 인자 없는 <code>ouroboros setup</code>은 그것을 자동 선택합니다. 그 하나가 Claude Code CLI라면 <code>claude</code> SDK 경로를 선택합니다. 여러 런타임이 감지되면 대화형 setup은 선택을 묻습니다. 무인 모드에서는 감지된 후보 중 기존 설정이 있으면 유지하고, 그렇지 않으면 <code>claude</code>가 감지될 때 SDK 경로를 우선하며 그 외에는 첫 후보를 선택합니다. 기본 <code>ouroboros-ai</code> 패키지에는 Claude Agent SDK가 포함되지 않아 worker 사전 확인 단계에서 막힐 수 있습니다. Python SDK 경로가 목적이라면 설치한 버전의 SDK extra와 전제 조건을 먼저 확인하세요: <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4806-L4861">setup 런타임 선택</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/claude_setup.py#L27-L64">Claude 런타임 설정</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/adapter.py#L1201-L1215">SDK 사전 확인</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L74-L82"><code>claude</code> 및 <code>claude-sdk</code> extras</a>. 이 동작은 인용한 <code>592c667f</code> 소스 기준이므로 설치 버전의 도움말과 안내도 확인하세요.</p>

<p><code>pip install</code>은 이 문서의 Git 커밋을 고정하지 않습니다. <code>ouroboros --version</code>은 해당 터미널의 CLI 패키지를 나타내며 호스트가 별도로 실행하는 서버의 버전은 확인하지 않습니다. 설정 결과와 사용할 런타임을 확인하세요. 다른 설치 경로와 세부 전제는 <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md">제품 설치 안내</a>를 참고하세요.</p>

</details>

## 2. 목표를 이야기하고 Seed 검토하기

<span id="worktree-first-task"></span>

!!! warning "실행 전 관리 worktree 경로 확인"
    worktree를 사용하는 실행은 관리 경로 `<worktree_root>/<저장소 이름>/<durable_id>`가 이미 있지만 대상 저장소에 Git worktree로 등록되지 않았다면 재귀 삭제를 시도할 수 있습니다. 기본 root는 `~/.ouroboros/worktrees`입니다. 새 CLI 실행과 ID가 별도 제공되지 않은 일반 MCP 실행은 ID를 실행 중 생성하므로 정확한 새 경로를 미리 알 수 없습니다. 시작 전에 실제 관리 root와 저장소별 디렉터리, 대상 저장소에서 `git worktree list --porcelain`으로 등록을 확인하고 진행 중 작업과 보존 자료를 살펴보세요. 재개는 실제 세션 ID와 저장된 workspace 경로가 있으면 그 기록도 대조하세요. 확인할 수 없으면 실행을 보류하고 임의로 삭제하거나 덮어쓰지 마세요. 확인 후에도 동시 변경에 따른 위험은 남으며 모든 경로의 삭제 성공을 뜻하지 않습니다. [source](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py#L328-L357) [CLI main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L843-L860) · [CLI release](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run.py#L843-L860) · [MCP main](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/execution_handlers.py#L1250-L1278)

**진행 순서:** Claude Code는 설정 → Interview → Seed 생성 → 공통 검토, Codex는 플러그인·MCP 연결 확인 → Interview → Seed 생성 → 공통 검토, 독립 CLI는 준비 → Interview → Seed 생성 승인 → 공통 검토 순서입니다.

<span id="plugin-first-task"></span>**Claude Code 플러그인:** 새 세션에서 작업 폴더를 열고 호스트 **대화에** 설정을 요청합니다.

```text
ooo setup
```

설정 질문에 답해 완료하세요. <span id="codex-first-task"></span>**Codex 플러그인:** 새 Codex 세션에서 작업 폴더를 열고 설치된 플러그인과 MCP 도구 연결을 확인하세요. 연결되지 않았다면 [진단 안내](/docs/ai-troubleshooting/#mcp)를 먼저 확인합니다. Codex용 독립 CLI 설정은 별도 경로입니다.

준비가 끝나면 호스트 대화의 다음 메시지로 Interview를 요청합니다.

```text
ooo interview "오늘 할 일을 추가하고 완료 표시할 수 있는 간단한 웹앱을 만들고, 프로젝트 README에 의존성 설치 방법, 앱 실행 명령, 실제 접속 주소와 포트, 종료 방법, 테스트 명령과 그 범위를 설명해 주세요."
```

### 플러그인 대화에서 Seed 만들기

Interview 스킬은 목표를 다시 확인하고 Seed 생성을 제안합니다. 목표 확인에 동의한 뒤 같은 대화에서 `ooo seed`를 요청합니다. 인터뷰 세션 ID를 받았다면 필요할 때 `ooo seed <실제 세션 ID>`로 대상을 지정할 수 있습니다. 스킬의 QA 의견은 참고하되 점수만으로 내용의 정확성을 판단하지 마세요.

MCP 서버를 사용할 수 없으면 스킬은 대화에서 확인한 요구로 Seed를 작성하는 대체 경로를 사용하며 서버 연결 설정을 안내할 수 있습니다. 이때도 실제 YAML과 저장 여부를 확인하세요. Claude Code와 Codex의 실제 화면과 스킬 호출 방식은 설치한 호스트·버전에 따라 확인해야 합니다. [Interview 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

<span id="cli-first-task"></span>**독립 CLI:** 작업 폴더의 **터미널에** 입력합니다.

```bash
ouroboros init start "오늘 할 일을 추가하고 완료 표시할 수 있는 간단한 웹앱을 만들고, 프로젝트 README에 의존성 설치 방법, 앱 실행 명령, 실제 접속 주소와 포트, 종료 방법, 테스트 명령과 그 범위를 설명해 주세요."
```

Windows PowerShell (project directory):

```powershell
& $OuroborosPython -m ouroboros init start "오늘 할 일을 추가하고 완료 표시할 수 있는 간단한 웹앱을 만들고, 프로젝트 README에 의존성 설치 방법, 앱 실행 명령, 실제 접속 주소와 포트, 종료 방법, 테스트 명령과 그 범위를 설명해 주세요."
```

### 독립 CLI에서 Seed 확인하기

터미널의 대화형 Interview에서 Seed 생성을 승인하고 출력된 실제 파일 경로와 내용을 확인하세요. `Start workflow now?`의 기본값은 예입니다. 실행 전에 검토하려면 `n`을 선택합니다. 이 동작은 위 소스 기준이므로 설치된 버전의 화면을 확인하세요.

### 두 경로 공통: 생성된 Seed 검토 {#shared-seed-review}

Interview의 질문에 답합니다. 예를 들어 새로고침 뒤에도 할 일이 남아야 하는지 정할 수 있습니다. 이는 **설명용 예시**이며 실제 출력이 아닙니다. Seed는 목표·제약·완료 조건을 정리한 명세입니다. **Interview 완료가 Seed 생성을 뜻하지는 않습니다.** 위에서 선택한 경로의 생성을 확인한 뒤 전체 YAML의 목표, 작업 대상, 제약과 검증 가능한 완료 조건을 검토하고, 저장된 실제 경로와 파일 내용까지 확인하세요. 승인하기 전에는 실행하지 마세요.

**검토 예시:** 다음은 필드 의미를 설명하는 일부 예시이며 전체 Seed나 실제 출력·결과가 아닙니다. 대화에서 실제 합의한 내용과 비교하세요.

- `goal`: 할 일을 추가하고 완료 표시하는 웹앱 만들기.
- `constraints`: 합의한 제약을 지키기. 예를 들어 동의한 경우에만 기존 데이터 보존.
- `acceptance_criteria`: 할 일을 추가하고 완료 표시한 뒤 새로고침해도 표시가 유지되는지 확인하기. 이 저장 조건은 합의한 경우에만 넣습니다.

반환된 실제 Seed 파일 경로와 선택한 작업 폴더는 YAML 필드가 항상 있다고 가정하지 말고 각각 확인하세요. 목표·제약·기준이나 작업 대상이 합의와 다르면 기존 YAML을 직접 수정하고 전체를 다시 검토합니다. [고정 Seed 모델](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/seed.py#L925-L948)

README 수용 기준이 의존성 설치, 앱 실행 명령, 실제 URL·포트, 종료 방법, 테스트 명령과 범위를 설명하도록 요구하는지 확인하세요. 테스트가 없다면 없다고 기록하도록 기준을 정할 수 있습니다. 이는 요청할 목표이지 README가 이미 존재하거나 정확하거나 테스트됐다는 뜻이 아닙니다.

**결과가 다를 때:**

- **YAML과 파일이 있으나 기준이 빠졌거나 목표와 다름:** 기존 YAML을 직접 수정하고 전체를 다시 검토하세요. 정상 생성된 파일을 재생성해 덮어쓰지 마세요. 기존 파일을 덮어쓰기 전에는 내용을 확인하세요.
- **YAML만 있고 저장된 파일이나 경로가 없음:** 반환된 YAML을 검토하고 적절한 새 Seed 파일에 저장한 뒤 실제 경로와 저장 내용을 확인하세요. 파일이 없다는 이유만으로 다시 생성하지 마세요.
- **YAML이 없거나 생성이 실패·중단됨:** 실행하지 마세요. 이 경우에만 생성 재개를 요청하거나 원본 Seed 산출물을 제공받으세요.

## 3. 실행하고 결과 확인하기

**진행 순서:** 아래 사전 확인과 경고를 읽고 → 검토한 Seed를 실행하고 → 반환된 ID와 작업 경로를 저장하고 → 파일·테스트·평가 결과를 확인한 뒤 → 문제가 있으면 [문제 해결](/docs/recovery-detail/)로 이동하세요.

실행 전에 선택한 작업 폴더가 Git 저장소라면 그 폴더의 터미널에서 `git rev-parse --verify HEAD`를 실행해 초기 커밋이 있는지 확인하세요. Git 저장소인데 이 확인이 실패해 커밋이 없다면 사용자가 파일과 보존할 변경을 먼저 검토하고 초기 커밋을 만들지 직접 결정한 뒤 진행합니다. 명령을 무조건 커밋으로 이어가거나 기존 파일을 임의로 변경하지 마세요. 고정 main `592c667f`와 release `0.59.9`의 일반 MCP worktree 활성 경로에서 커밋 없는 저장소는 작업 공간 준비에 실패해 `launch_workspace_unavailable`이 보고될 수 있습니다. Git 저장소가 아닌 폴더는 해당 구현에서 worktree를 만들지 않고 넘어가는 별도 경우이며 같은 격리가 보장되지 않습니다. OpenCode의 `dispatch_mode="plugin"` 위임이나 worktree 비활성 경로에도 이 결과를 일반화하지 마세요. [main 작업 공간 준비](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/worktree.py) · [release 작업 공간 준비](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/worktree.py).

일반 MCP 백그라운드 실행에서 `orchestrator.use_worktrees`의 기본값은 켜짐이며, 작업 폴더가 Git 저장소 안에 있을 때 별도 worktree 생성 대상이 됩니다. 생성은 실패할 수 있습니다. Git 저장소가 아니거나 설정이 꺼져 있으면 worktree 없이 지정한 작업 폴더에서 실행될 수 있습니다. 반환된 `worktree_path`와 `worktree_branch`가 있다면 확인하고, 없다면 실제 선택된 작업 경로를 확인하세요. OpenCode의 자식 Task에 위임하는 `dispatch_mode="plugin"` 경로는 일반적인 플러그인 설치와 구분되며, job ID나 관리 worktree 없이 진행되므로 Task 창에서 추적합니다. 완료 후 기본적으로 정식 평가가 시작됩니다. 일반 MCP 평가 job에서는 `auto_evolve`가 켜져 있고 `final_approved`가 `false`이면 `rejected`뿐 아니라 `unverified`도 제한된 Ralph 후속 등록을 시도할 수 있습니다. 실제 후속 실행 여부는 Seed 등 조건과 등록 결과에 따라 달라지며, 실행되면 추가 시간과 모델 비용이 들 수 있습니다. 상태와 최종 결과를 확인하세요.

플러그인 대화에서는 검토한 Seed YAML 또는 실제 파일 경로를 지정해 `ooo run`을 요청합니다. 독립 CLI에서는 실제 생성 경로를 사용해 터미널에서 `ouroboros run <Seed 파일 경로>`를 실행합니다. 꺾쇠 괄호를 포함한 예시 경로를 그대로 입력하지 마세요. Windows PowerShell에서는 실제 경로를 큰따옴표로 감싸고 다음처럼 실행합니다.

```powershell
& $OuroborosPython -m ouroboros run "<실제 Seed 파일 경로>"
```

실행은 코드와 파일을 변경하고 명령 및 모델 호출을 시작할 수 있습니다.

진행 중에는 실제로 반환된 ID와 상태를 기록합니다. 완료 표시나 ID만으로 요구가 충족됐다고 판단하지 말고 다음을 확인하세요.

1. 실행 결과에 보고된 실제 작업 폴더 또는 worktree에서 생성·변경된 파일을 살펴봅니다.
2. 테스트와 평가 결과를 읽고 실패 또는 미검증 항목을 확인합니다.
3. 실제 작업 경로의 README를 읽고 의존성 설치, 앱 시작, 실제 URL·포트, 종료 및 테스트 방법이 적혀 있는지 확인합니다. 명령과 출처를 검토한 뒤 신뢰할 수 있는지 판단하고, 실행 방법을 선택해 앱을 열어 할 일을 추가하고 완료 표시합니다. Seed에 저장 조건이 있다면 새로고침 후에도 만족하는지 직접 확인합니다.
4. README의 실행·테스트 안내를 실제 결과와 비교합니다. 파일이 없거나 설명이 빠졌거나 실행 결과와 다르면 해당 수용 기준은 아직 확인되지 않은 것입니다. 존재하지 않는 산출물이나 성공한 실행 결과라고 추정하지 마세요.

위의 세 가지 앱 동작을 살펴볼 수 있는 [합성 참고 예제](/docs/todo-reference-example/)는 문서용으로 별도 작성한 코드입니다. 실제 제품 생성물이 아니며 README 관련 수용 기준은 실제 프로젝트에서 따로 확인해야 합니다.

**독립 CLI 사용자:** 실제 생성 작업 경로에서 `README`와 프로젝트의 패키지 설정 파일을 직접 살펴 의존성 설치 방법, 시작 스크립트, URL·포트와 종료 방법을 확인하세요. 파일에 정보가 없거나 실행 방법을 판단할 수 없다면 이를 추측하지 말고, Claude Code 또는 Codex처럼 제품이 지원하는 플러그인 호스트에서 아래 요청 예시를 사용해 확인하세요.

실제 실행 결과에 표시된 작업 경로 또는 `worktree_path`에서 호스트 에이전트에게 다음처럼 요청할 수 있습니다. 이는 **자연어 요청 예시**이며, 특정 기술 스택·명령·URL이나 검증된 실행 결과를 뜻하지 않습니다.

```text
현재 작업 경로 <실제 작업 경로>의 프로젝트를 살펴보고, 필요한 의존성 설치 명령과 출처, 앱 시작 명령, 실제 접속 URL과 포트, 종료 방법 및 예상 비용을 알려 주세요. 실행 명령과 출처를 확인해 신뢰할 수 있는 방법을 선택한 뒤, 제가 직접 앱을 열어 할 일 추가와 완료 표시를 확인하겠습니다.
```

이 안내만으로 실제 앱 실행은 검증되지 않습니다. 답변이 프로젝트 내용과 실행 환경에 맞는지, 명령·출처를 신뢰할 수 있는지와 포트·비용을 검토한 뒤 진행하세요.

평가가 시작되지 않았거나 실패했거나 결과가 `unverified`라면, 먼저 실제 `session_id`, 원래 Seed, 산출물과 반환된 작업 경로 또는 `worktree_path`를 대조합니다. 이미 평가 job이나 연결된 Ralph job이 있으면 상태와 결과를 확인하고 중복 시작하지 마세요. **연결된 MCP를 사용하는 플러그인 호스트 대화**라면 새 평가가 필요한 경우에 호스트에 `ooo evaluate <실제 session ID> [산출물]`을 요청하고 실제 프로젝트 경로를 알려주세요. `auto_evolve: false`는 이번 평가에서 새 Ralph 후속을 예약하지 않게 할 뿐, 이미 시작된 평가나 chain을 취소하지 않습니다. **독립 CLI 터미널에는 이 호스트 명령을 입력하지 마세요.** 고정 소스 `592c667f`의 CLI에는 별도 평가 재실행 명령이 확인되지 않았습니다. 설치 버전의 `ouroboros --help`와 버전별 안내를 확인하고, 지원 경로를 찾지 못하면 호스트와 MCP가 연결된 경로를 사용하세요. `unverified`는 승인이 아닙니다. 실행 가능한 검사를 추가하거나 확인한 뒤, 결과별 다음 행동은 [평가 상세 안내](/docs/evaluation-evolution-detail/)에서 확인하세요.

상태 조회는 ID의 종류에 따라 다릅니다. [진행 상태](/docs/progress-detail/)에서 받은 ID에 맞는 경로를 확인하세요. 문제가 생기면 증상에 따라 확인합니다.

- 호스트에서 `ooo` 명령이나 플러그인을 찾지 못하면, 호스트 플러그인 설치·활성화와 새 대화 여부를 확인하세요. 터미널에서 `ouroboros`를 찾지 못한 것은 독립 CLI가 없다는 뜻일 수도 있습니다. [설치·설정 오류 안내](/docs/recovery-detail/#setup-errors)를 참고하세요.
- MCP 연결에 실패하면 서버가 호스트에서 활성화·연결됐는지와 실제 도구 목록을 확인하고, [MCP 연결 실패 안내](/docs/ai-troubleshooting/#mcp)를 따르세요.
- 실행이 중단됐거나 응답이 끊겼다면 기존 job·session·execution ID, Seed와 작업 경로를 보존하고 ID 종류에 맞춰 상태를 확인하세요. job ID가 있으면 같은 job ID로 결과도 조회합니다. 실행이 아직 진행 중일 수 있으므로 소유자와 상태를 확인하기 전 재시작하거나 중복 실행하지 마세요. [ID별 첫 상태 조회 안내](/docs/recovery-detail/#first-status-by-id)를 참고하세요.

복구 상세 안내는 구판 소스 `722172ef`를 기준으로 한 설명과 시험을 포함합니다. 제품 main `592c667f`, 공개 릴리스 `0.59.9`, 설치된 플러그인과 MCP 서버가 서로 다를 수 있으므로, 해당 설치의 버전과 도움말을 확인하고 판본 차이를 가정하지 마세요.

다음으로 [Interview 안내](/docs/interview-guide/), [Seed 형식](/docs/seed-guide/), [기존 프로젝트 적용](/docs/existing-project-detail/)을 살펴볼 수 있습니다.
