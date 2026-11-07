# 처음 설치한 뒤 첫 결과까지

!!! warning "판본과 검증 범위"
    이 안내의 상세 동작은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 설치된 플러그인과 호스트 MCP 서버는 별도 판본입니다. 아래 합성·대역 시험은 표시된 조건에 한정되며 실제 모델·인증·모든 호스트의 동작을 증명하지 않습니다. 설치한 버전의 도움말과 [제품 시작 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조하세요. 구판 동작이 현재 설치에도 같다고 가정하지 않습니다.


## 현재 상황

설치를 마치고 첫 작업을 시작하려는 단계입니다. **AI 호스트의 플러그인**과 **독립 터미널 CLI** 중 자신이 설치한 경로를 고르세요. 플러그인은 `uvx`로 서버를 실행할 수 있으므로, 설치가 끝났어도 터미널에 `ouroboros` 명령이 없을 수 있습니다.

### 처음이라면 이 순서로

1. **준비:** 인터넷 연결과 터미널, 선택한 AI 호스트 또는 Python 환경, 해당 모델 런타임의 설치·로그인 및 비용 조건을 확인합니다. 모델 호출을 쓰는 작업은 시간과 비용이 들 수 있습니다. 작업 폴더의 파일을 변경할 수 있으므로 처음에는 새 폴더를 사용하세요.
2. **설치:** 아래 [설치 상태 확인](#install-check)에서 호스트 플러그인 또는 독립 CLI 하나를 선택합니다. `ooo`는 호스트 대화에, `ouroboros`는 터미널에 입력합니다. 독립 CLI와 호스트 서버는 서로 다른 설치일 수 있습니다.
3. **작업 폴더:** 예를 들어 터미널에서 `mkdir ~/ouroboros-first-project && cd ~/ouroboros-first-project`를 실행하면 새 폴더를 만들고 이동합니다. 이미 같은 이름이 있으면 `mkdir`이 실패하고 이동하지 않습니다. 다른 이름을 골라 다시 시도하세요. 호스트 플러그인 사용자는 이 폴더를 호스트에서 엽니다. 폴더는 홈에 로컬로 남으며 자동 백업되지 않습니다.
4. **목표에서 Seed까지:** 아래 [호스트 경로](#host-first-task) 또는 [독립 CLI 경로](#cli-first-task)를 따릅니다. Seed는 목표·제약·완료 조건을 담는 작업 명세입니다. 실행 전 실제 생성된 내용을 읽어 조건과 작업 대상을 확인하세요.
5. **실행 후 확인:** 받은 ID로 [진행상태](/docs/progress-detail/)를 확인하고, 실제 결과 파일과 테스트·기능을 살핍니다. ID나 완료 표시만으로 요구 충족을 판단하지 않습니다. 문제가 생기면 [복구 안내](/docs/recovery-detail/)를 보세요.

이 문서의 예제는 순서를 설명하는 가상 시나리오입니다. 실제 모델을 사용한 설치부터 결과까지의 전 과정은 시험하지 않았습니다. 공개 `0.59.9`의 초기 CLI 설치·진단 확인 범위는 [판본과 검증 범위](/docs/version-guide/#version-scope)에 표시합니다. 다른 격리 합성·대역 시험의 조건과 한계는 해당 설명과 연결된 상세 문서에서 각각 확인하세요.

### 사용 통계와 첫 실행 전 선택

고정 판본은 사용 통계를 기본으로 활성화하며, 원본은 제한된 익명 이벤트를 PostHog에 전송한다고 설명합니다. 전송을 원하지 않으면 설치·실행 **전에** 해당 프로세스에 `OUROBOROS_TELEMETRY=0` 또는 `DO_NOT_TRACK=1`을 설정하거나 홈 설정의 `telemetry.enabled: false`를 사용하세요. 호스트 플러그인도 MCP 서버 프로세스가 이 환경 설정을 실제로 받는지 확인해야 합니다. 다른 도구의 통신이나 모델 제공자 호출까지 중단하는 설정은 아닙니다. 수집 범위, 설정 우선순위와 주의점은 [사용 통계 안내](/docs/config-reference-detail/)를 확인하세요. 이는 고정 소스의 정책이며 실제 전송 여부는 이 문서에서 시험하지 않았습니다.

### 설치 상태부터 확인 {#install-check}

| 사용 환경 | 설치와 준비 | 사용할 곳 |
| --- | --- | --- |
| Codex 플러그인 | 로그인된 Codex CLI와 `uvx`가 필요합니다. 터미널에서 `codex plugin marketplace add Q00/ouroboros`, `codex plugin add ouroboros@ouroboros`를 실행합니다. | 새 Codex 세션에서 `ooo`로 환영·준비 흐름을 시작합니다. 설정 과정은 환경을 변경할 수 있으므로 제시되는 내용을 확인합니다. |
| Claude Code 플러그인 | Claude Code와 `uvx`가 필요합니다. 터미널에서 `claude plugin marketplace add Q00/ouroboros`, `claude plugin install ouroboros@ouroboros`를 실행합니다. | 새 Claude Code 세션에서 `ooo setup` 설정 마법사를 시작합니다. 설정·선택한 프로젝트 지침 파일 등이 변경될 수 있습니다. |
| 독립 터미널 CLI | Python 3.12 이상의 [가상환경에 설치](#cli-venv)합니다. 런타임을 고르고 필요한 패키지 extra를 확인한 뒤 별도로 설정합니다. | 터미널에서 `ouroboros --version`과 `ouroboros status health`를 확인합니다. |

### 독립 CLI를 가상환경에 설치하기 {#cli-venv}

macOS·Linux·WSL 터미널에서는 `python3 --version`으로 Python 3.12 이상인지 먼저 확인하세요. `python3`이 더 낮은 버전을 가리키면 아래 명령의 `python3`을 설치된 3.12 이상 실행 파일로 바꿉니다. Python의 `venv` 기능도 필요합니다. 운영체제에서 별도 패키지로 제공한다면 해당 OS의 안내에 따라 설치하세요.

다음은 **새 디렉터리**에 공개 패키지를 설치하는 예입니다. 첫 `mkdir`은 같은 이름이 이미 있으면 실패하며, `&&`로 이어진 나머지 명령도 실행되지 않습니다. 기존 환경을 사용하거나 덮어쓰지 말고 다른 새 이름을 고르세요. 설치에는 인터넷 연결이 필요합니다.

```bash
mkdir ~/ouroboros-cli-env &&
python3 -m venv ~/ouroboros-cli-env/.venv &&
~/ouroboros-cli-env/.venv/bin/python -m pip install ouroboros-ai &&
~/ouroboros-cli-env/.venv/bin/ouroboros --version
```

macOS·Linux·WSL에서 설치가 성공하면 같은 터미널에서 `. ~/ouroboros-cli-env/.venv/bin/activate`를 실행하고 `command -v ouroboros`가 이 가상환경의 실행 파일을 가리키는지 확인합니다.

Windows PowerShell에서는 작업할 위치를 먼저 확인한 뒤 아래 예를 실행하세요. 현재 디렉터리에 `ouroboros-cli-env`가 이미 있으면 중단하고 다른 새 이름을 선택합니다. Python Launcher가 선택한 Python 3.12 이상과 인터넷 연결이 필요합니다. 이 예제는 가상환경의 Python을 직접 호출하므로 활성화 스크립트나 실행 정책 변경이 필요하지 않습니다.

```powershell
$ErrorActionPreference = "Stop"
py -3 --version
if ($LASTEXITCODE -ne 0) { throw "Python 3.12 이상을 Python Launcher에 설치 또는 등록하세요." }
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if ($LASTEXITCODE -ne 0) { throw "선택된 Python이 3.12보다 낮습니다." }
if (Test-Path .\ouroboros-cli-env) { throw "이미 존재하는 경로입니다. 다른 새 폴더를 선택하세요." }
New-Item -ItemType Directory -Path .\ouroboros-cli-env | Out-Null
Set-Location .\ouroboros-cli-env
py -3 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "가상환경 생성에 실패했습니다." }
.\.venv\Scripts\python.exe -m pip install ouroboros-ai
if ($LASTEXITCODE -ne 0) { throw "패키지 설치에 실패했습니다." }
.\.venv\Scripts\python.exe -m ouroboros --version
if ($LASTEXITCODE -ne 0) { throw "CLI 확인에 실패했습니다." }
```

위 예는 현재 PowerShell 세션의 `$ErrorActionPreference`를 `Stop`으로 바꾸고 새 디렉터리로 이동합니다. 이후 같은 디렉터리에서 CLI를 사용할 때도 `.\.venv\Scripts\python.exe -m ouroboros ...` 형식을 사용하세요. 다른 디렉터리에서는 확인한 가상환경의 실제 Python 경로를 지정합니다. 실행 정책 변경 없이 활성화를 생략한 경로이며, 이 블록은 Windows Actions의 PowerShell 파일 실행에서 Python 3.12·3.13과 공개 0.59.9로 확인했지만 사용자 PC나 대화형 붙여넣기는 시험하지 않았습니다.

이 절의 `pip install ouroboros-ai`는 기본 패키지만 설치합니다. 아직 `ouroboros setup`을 실행하지 말고, 먼저 [런타임별 요구사항](/docs/runtime-support-detail/)을 확인해 실행 파일·인증·필요한 extra를 갖춘 뒤 명시적으로 런타임을 선택하세요. 특히 `claude`는 Claude Agent SDK 경로이며 `[claude]` 또는 `[claude-sdk]` extra가 필요합니다. 설치된 Claude CLI만으로 SDK가 설치되지는 않습니다. `claude-cli`는 별도 MCP 2 프로필 경로이고 `[claude-cli]` extra 자체는 비어 있지만 MCP 서버용 `[mcp]` 프로필이 필요합니다. `ouroboros setup`은 자동으로 하나의 감지된 런타임을 선택할 수도 있고 사용자 설정을 변경할 수 있으므로, 런타임 선택과 기존 설정을 검토한 후 진행하세요. 준비 후 `ouroboros status health` 결과를 읽습니다. 정상 표시는 모델 인증·호출 성공을 보장하지 않습니다. 새 터미널에서는 다시 활성화하거나 위 절대 경로를 사용하세요. `deactivate`는 현재 셸에서 가상환경을 벗어납니다. 가상환경은 로컬에 남고 자동 백업되지 않습니다.

설치 중 오류가 나면 출력의 마지막 오류와 선택한 Python 버전을 확인하세요. 가상환경 생성이나 설치가 중간에 실패했다면 일부 파일이 남을 수 있으므로, 기존 디렉터리를 자동으로 지우지 말고 확인 후 새 이름으로 다시 시도합니다. 이 경로는 공개 배포물을 설치하므로 아래 고정 커밋과 동일하다고 가정하지 않습니다. 공개 `0.59.9`의 신규 가상환경 설치와 초기 진단은 시험했지만, 이 명령으로 설치되는 미래 버전과 실제 모델 인증·첫 작업은 시험하지 않았습니다.

**버전과 문서 범위:** 이 문서는 upstream 커밋 `722172ef096767583679d04aef5e847458fee6b2`를 기준으로 하며 위 `pip install`은 그 커밋을 고정하지 않습니다. 실제로 시험한 공개 패키지 `0.59.9`는 이 커밋과 여러 파일이 달랐습니다. 예를 들어 고정 소스에 있는 `megacode` 런타임은 해당 패키지에서 확인되지 않았고, `config set`의 boolean 입력 처리도 다릅니다. 배포 버전과 커밋을 같은 것으로 가정하지 말고 설치된 버전의 도움말·배포물과 [런타임 차이](/docs/runtime-support-detail/)를 확인하세요. 비교는 설치된 패키지 파일과 고정 Git 객체의 바이트를 대조한 결과입니다.

### 이 문서의 소스 판본을 독립 환경에서 확인하기 {#pinned-source}

아래는 공개 PyPI 릴리스 대신 이 문서의 **Git 커밋**을 별도 디렉터리와 Python 가상환경에 설치해 확인하는 경로입니다. Python 3.13과 `git`, `uv`가 필요합니다. 기존 저장소나 가상환경이 아닌 새 작업 디렉터리에서 실행하세요. `git clone`과 의존성 설치에는 네트워크 및 저장 공간이 필요할 수 있습니다.

```bash
git clone https://github.com/Q00/ouroboros.git ouroboros-pinned &&
cd ouroboros-pinned &&
git checkout --detach 722172ef096767583679d04aef5e847458fee6b2 &&
test "$(git rev-parse HEAD)" = 722172ef096767583679d04aef5e847458fee6b2 &&
python3.13 -m venv .venv &&
uv pip install --python .venv/bin/python . &&
.venv/bin/ouroboros --version &&
.venv/bin/ouroboros --help
```

각 단계는 `&&`로 연결되어 clone·checkout이 실패하거나 실제 HEAD가 위 전체 SHA와 다르면 설치를 진행하지 않습니다. 이 설치는 의존성 lock을 적용하지 않으므로 환경과 시점에 따라 의존성 결과가 달라질 수 있습니다. 버전 출력은 Git 태그·빌드 환경에 따라 달라질 수 있으므로 SHA 대신 사용하지 않습니다. 시험에서는 로컬 Git 복제본의 해당 커밋과 캐시된 의존성으로 오프라인 설치해 `0.59.10.dev36`과 도움말을 확인했습니다. 별도 시험에서 공개 GitHub 복제와 해당 SHA 확인도 성공했으나 설치에는 기존 캐시를 사용했습니다. 새 의존성 다운로드, 다른 OS·Python, 실제 인증·모델 실행은 시험하지 않았습니다. 이 가상환경은 **독립 CLI**용이며 Codex·Claude 등 호스트가 따로 실행하는 MCP 서버나 플러그인을 이 커밋으로 바꾸지 않습니다. 기존 설치를 덮어쓰지 않도록 위처럼 가상환경의 실행 파일을 명시하세요. 다음 설정·실행은 별도 설정 변경이나 모델 비용을 일으킬 수 있습니다.

위 고정 소스를 설치한 뒤 아래의 짧은 `ouroboros` 명령을 따라가려면, **같은 셸에서 아직 `ouroboros-pinned`에 있을 때** 다음을 실행해 그 가상환경을 활성화하세요. 표시되는 실행 파일이 방금 만든 `ouroboros-pinned/.venv/bin/ouroboros`인지 확인한 후 작업 프로젝트로 이동합니다. 가상환경 활성화는 현재 셸에만 적용되며 새 터미널이나 호스트 MCP 서버에는 적용되지 않습니다. 다른 셸에서는 다시 활성화하거나 실행 파일의 절대 경로를 사용합니다. 활성화하지 않은 채 아래의 `ouroboros`를 호출하면 PATH의 다른 버전이 실행될 수 있습니다. `deactivate`로 현재 셸의 가상환경을 나갈 수 있습니다.

```bash
. .venv/bin/activate && command -v ouroboros && ouroboros --version
```

독립 CLI 설정은 파일을 변경할 수 있습니다. 고정 버전에서 `ouroboros setup`에 런타임을 지정하지 않고 하나만 감지되면 자동 선택합니다. `--non-interactive`는 읽기 전용 미리보기가 아닙니다. 여러 런타임을 감지했을 때 이번 실행에서 감지된 기존 설정을 우선하고, 그 설정이 감지되지 않았다면 Claude, 그다음 감지된 첫 항목을 선택하는 자동 선택 순서는 **`--non-interactive`일 때만** 적용됩니다. 대화형 실행에서는 런타임 번호 목록과 `Select runtime` 질문이 표시됩니다. 기존 backend가 감지된 목록에 포함되면 현재 항목으로 표시되고 기본 선택이 되며, 포함되지 않으면 첫 감지 항목이 기본값입니다. 실행 전 대상 런타임과 설정 변경 범위를 확인하세요. 지정 없이 사용 가능한 런타임을 찾지 못하면 `No runtimes found.`와 종료 코드 1이 나옵니다. 일부 런타임은 PATH 외 명시 경로나 기존 설정도 감지에 사용하므로 해당 환경을 함께 확인한 뒤 [런타임 준비 안내](/docs/runtime-support-detail/)를 따라 다시 시도하세요. 종료 코드 1이 변경이 없었다는 보장은 아닙니다. 빈 임시 HOME·제한된 PATH에서 `setup --non-interactive`를 실행한 시험에서는 실패해도 홈에 `.ouroboros` 디렉터리가 생성됐습니다. 이는 해당 합성 실패 사례이며 설치나 실제 인증·모델 호출 성공을 검증한 것은 아닙니다. [고정 setup 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup.py).

독립 CLI의 기본 패키지만으로 모든 실행 런타임과 선택 기능이 설치되지는 않습니다. 선택한 런타임의 실행 파일·인증과 필요한 추가 패키지를 [런타임 안내](/docs/runtime-support-detail/)에서 확인하세요. 고정 원본은 독립 MCP 2 서버와 TUI를 함께 쓰는 경우 `[mcp,tui]` extras와 호환 런타임 선택을 권합니다. 공개 PyPI 패키지를 사용할 때는 해당 환경에서 `pip install 'ouroboros-ai[mcp,tui]'`를 사용할 수 있지만, 위에서 고정 Git 소스를 설치했다면 이 명령은 공개 배포물로 바꾸거나 버전을 다시 해석할 수 있습니다. 고정 소스의 extras가 필요하면 동일한 SHA를 다시 확인한 `ouroboros-pinned` 디렉터리에서 해당 가상환경에 `uv pip install --python .venv/bin/python '.[mcp,tui]'`를 검토하세요. 별도 새 가상환경의 고정 checkout에서 캐시만으로 이 extras 설치와 MCP 2.3.0·TUI 배포판을 확인했습니다. 이 설치본에서 합성 로컬 stdio 서버의 도구 발견과 호출 한 사례도 확인했다. 같은 설치본의 Python TUI는 빈 세션과 합성 세션 하나의 제한된 PTY 경로를 시험했습니다. 실제 운영 세션·전체 화면·접근성 및 SLT는 미검증입니다. 기존 환경의 충돌이나 실제 외부 서버·호스트 설정도 검증하지 않았으며 일반 설치에서는 의존성 다운로드·변경이 발생할 수 있습니다. [TUI 시험 범위](/docs/progress-detail/)를 확인하세요. 기존 패키지의 제거 또는 충돌 자동 방지나 lock과 같은 의존성 재현을 보장한다고 가정하지 말고 설치 전후 환경을 확인하세요. Claude Agent SDK용 `[claude]`·`[claude-sdk]`와 이를 포함하는 `[all]`은 MCP 1 환경이므로 같은 Python 환경에서 MCP 2용 `[mcp]`와 결합하지 않습니다. 실제 설치 명령의 대상 환경과 버전을 먼저 확인하세요.

`uvx`가 없다면 [고정 판본의 설치 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/getting-started.md)에서 uv 설치부터 진행합니다. Codex CLI가 설치되지 않았거나 로그인되지 않았다면 [공식 Codex 시작 안내](https://developers.openai.com/codex/quickstart)를 먼저 따릅니다. 명령이 지원되지 않으면 설치된 호스트의 도움말과 [원본 Codex 런타임 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/codex.ko.md)를 확인합니다.

### 환영 안내를 다시 열거나 건너뛰기

호스트가 이 스킬을 제공한다면 `/ouroboros:welcome`은 첫 사용 안내와 준비 상태 확인을 엽니다. `/ouroboros:welcome --force`는 완료된 환영 안내를 다시 열고, `--skip`은 안내를 건너뛰고 완료 표시를 기록하는 경로입니다. 이는 **호스트 스킬**이지 독립 터미널의 `ouroboros welcome` 명령이 아닙니다. 제공되는 스킬 이름과 호출 방식은 설치한 호스트·버전을 확인하세요.

고정 스킬은 이전 환영 완료 표시가 있어도 현재 설정 준비를 별도로 확인하며, 준비되지 않았다면 설정을 진행할지 나중에 할지 묻도록 지시합니다. 나중에 하기를 선택했다는 사실은 MCP 연결이 준비됐다는 뜻이 아닙니다. **준비 확인의 범위는 호스트마다 다릅니다.** Claude Code 조건은 Ouroboros 설정에서 실행 백엔드가 `claude` 또는 `claude_mcp`이고 LLM 백엔드가 `claude`인지 확인합니다. Codex 조건은 두 백엔드가 `codex`인지에 더해 Codex 실행 파일이 실행 가능한지와 Codex 설정의 Ouroboros MCP 항목에 실행 가능한 명령 또는 비어 있지 않은 URL이 있는지 확인합니다. 어느 조건도 모델 인증, 실제 MCP 연결 또는 전체 실행 성공을 증명하지 않습니다. 완료 정보는 `~/.ouroboros/prefs.json`에 기록될 수 있고, 안내 중 인증된 GitHub 사용자에게 선택적으로 별을 누를지 물을 수 있습니다. 선택한 설정 경로는 로컬 설정을 수정하거나 패키지를 내려받을 수 있으므로 제시되는 작업을 확인하세요. 이 설명은 [고정 환영 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/welcome/SKILL.md)의 지침을 대조한 것이며 실제 호스트 환영 대화는 이 문서 작성에서 실행하지 않았습니다.

## 입력

첫 작업의 목표와 완료 조건을 준비하세요. 예를 들어 “작업을 추가하고 목록에서 확인하는 CLI를 만든다. `add`와 `list`를 테스트한다”라고 적을 수 있습니다. [전체 예제](/docs/example-detail/)에서 이 입력과 확인 기준을 함께 볼 수 있습니다.

독립 CLI의 `init start`에 목표 대신 파일 경로를 입력할 수도 있습니다. 고정 버전은 경로 후보가 줄바꿈 없이 240자 이내이며 존재하는 일반 파일이고 지원 확장자(`.md`, `.markdown`, `.txt`, `.rst`, `.json`, `.yaml`, `.yml`)인 경우 내용을 읽고 검증을 통과하면 인터뷰 맥락으로 사용합니다. 상대 경로는 현재 디렉터리 기준이며 절대 경로와 `~`도 사용할 수 있습니다. 읽기나 내용 검증이 실패하면 오류가 납니다. JSON/YAML은 PM Seed 후보 여부를 판단하기 위해 먼저 YAML로 파싱하므로 파싱 오류가 날 수 있으며, PM Seed로 인식되면 별도 검증·변환을 거칩니다. **오타로 없는 경로 또는 디렉터리는 파일 오류가 아니라 입력한 문자열 그대로 해석될 수 있습니다.** 실행 전에 파일 존재와 내용·민감정보를 확인하세요. 빈 임시 디렉터리에서 합성 파일은 내용으로, 없는 경로와 디렉터리는 문자열로 반환되는 것을 입력 해석 함수 수준에서 확인했습니다. 실제 인터뷰·모델 전송은 시험하지 않았습니다. [고정 입력 해석 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/initial_context.py), [CLI 호출 위치](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py).

### 호스트 플러그인으로 첫 작업 실행 {#host-first-task}

작업할 프로젝트 폴더를 호스트에서 열고 다음을 **호스트 대화에** 입력합니다.

1. `ooo interview "작업 관리 CLI 만들기"`로 목표와 완료 조건을 구체화합니다.
2. 인터뷰가 끝나면 `ooo seed`로 Seed YAML을 생성합니다. 대화의 YAML 또는 저장된 파일에 필요한 기능과 검증 기준이 들어 있는지 읽습니다. **인터뷰 종료만으로 실행할 Seed가 생겼다고 가정하지 않습니다.**
3. 출력된 실제 파일 경로를 사용해 같은 대화에 `ooo run [생성된 Seed 파일 경로]`라고 입력합니다. 경로 대신 YAML만 받았다면 그 YAML을 지정해 실행해 달라고 요청합니다. 반환된 `job_id`, `session_id`, `execution_id` 중 실제로 받은 값을 기록합니다.
4. 반환된 ID로 같은 작업을 조회합니다.

### 독립 CLI로 첫 작업 실행 {#cli-first-task}

1. 프로젝트 폴더에서 `ouroboros init start "작업 관리 CLI 만들기"`를 실행합니다. 이 대화형 CLI는 인터뷰 후 Seed 생성 여부를 확인합니다. 생성을 승인하고 성공하면 **`Start workflow now?`를 묻습니다. 기본 응답은 예**이므로 먼저 Seed를 검토하려면 `n`을 입력하세요. 인터뷰가 중단되거나 Seed 생성을 거절·실패하면 파일 경로나 실행이 없을 수 있습니다.
2. 출력된 **실제 Seed 파일 경로**를 기록하고 YAML의 목표와 완료 조건을 읽습니다. 생성기는 기본적으로 `~/.ouroboros/seeds/`에 Seed를 저장합니다. 생성 결과의 실제 경로를 우선합니다. 고정 버전의 이 CLI 경로는 생성된 `seed_id`로 파일명을 정하고 같은 경로의 파일이 있으면 저장 시 교체할 수 있으므로, 재생성 전에 기존 Seed를 확인·보존하세요. 이는 소스 대조와 별도 합성 저장 시험에서 확인한 경계이며, 실제 인터뷰에서 동일 ID가 생성되는 빈도나 충돌은 시험하지 않았습니다. [CLI 생성·저장 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py), [합성 저장 시험](/docs/python-api-detail/).
3. 1번에서 실행을 거절한 경우에만, 검토한 경로를 사용해 `ouroboros run /path/to/seed.yaml`을 실행합니다. 1번에서 실행을 수락했다면 실행을 시도한 것이므로 시작 전 오류가 있었는지와 기존 작업의 상태·결과를 먼저 확인하고 중복 실행하지 않습니다. `seed_abc123` 같은 설명용 값을 그대로 입력하지 않습니다.
4. 반환된 ID를 기록합니다. 실행 후 QA, 자동 평가와 조건에 따른 Ralph 반복이 이어질 수 있으므로 각 작업과 최종 결과를 확인합니다. 이 동작은 설정과 버전에 따라 달라집니다.

3번을 나중에 실행할 때도 **의도한 프로젝트 폴더에서** 실행하세요. 고정 버전에서는 전역 `~/.ouroboros/seeds/`의 Seed에 대상 경로가 따로 지정되지 않았다면 `ouroboros run`을 실행한 현재 폴더가 작업 대상이 됩니다. 검토 후 다른 폴더에서 새 `ouroboros run`을 시작하면 대상도 달라질 수 있습니다. 이는 이전 실행의 `--resume` 재개와 구분하세요. Seed metadata·brownfield 대상이나 명시적 `--project-dir`이 있는 경우는 별도 우선순위를 따릅니다. 시작 시 출력하는 프로젝트 경로와 이후 작업 위치를 확인하고, 경로를 명확히 지정하려면 [기존 프로젝트 안내](/docs/existing-project-detail/)를 참조하세요. [고정 소스의 경로 선택](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py).

인터뷰에 쓰는 모델 백엔드와 Seed 실행에 쓰는 에이전트 런타임은 별개입니다. 예를 들어 둘 다 Codex로 지정하려면 `ouroboros init start --llm-backend codex --runtime codex "작업 관리 CLI 만들기"`를 사용할 수 있습니다. `--runtime`만 지정해도 인터뷰 백엔드가 바뀌는 것은 아닙니다. 각 백엔드의 설치·로그인과 비용 조건을 먼저 확인하고, 생략 시 실제 선택된 환경을 출력과 설정에서 확인하세요. [고정 소스의 옵션 정의](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py).

기존 PM Seed가 감지되고 개발 Seed는 없으면 처음 입력한 목표 대신 PM Seed를 사용할지 질문할 수 있습니다. 이 질문의 기본값은 아니요이며, 수락하면 선택한 PM Seed가 인터뷰 맥락으로 사용됩니다. 또한 인터뷰 중 `Ctrl+C`는 저장 안내와 종료 코드 0을 반환할 수 있으므로 성공이나 Seed 생성의 증거로 삼지 말고 실제 파일·상태를 확인하세요. 중단된 인터뷰의 재개는 [인터뷰 안내](/docs/interview-detail/)를 참조합니다.

!!! warning "실행과 비용 경계"
    이 판본에서 기본 orchestrator 실행의 `--dry-run`은 실제 실행을 막지 않습니다. 플래그 이름만 믿고 시험하지 마세요. 이 버전에서 `--no-orchestrator`만 사용한 경로는 실제 작업 대신 실행 예정 메시지만 표시하는 자리표시자입니다. 하지만 `--mcp-config`를 함께 지정하면 orchestrator를 다시 활성화하고, `--resume`을 지정하면 orchestrator 재개 경로를 사용합니다. 따라서 `--no-orchestrator --dry-run`에 이 옵션 중 하나를 더해도 실제 실행될 수 있습니다. 모델 호출과 반복은 시간·비용을 발생시킬 수 있습니다. 자동 평가나 반복을 시작하지 않으려면 독립 CLI의 `--no-auto-evaluate --no-auto-evolve`를 사용하고 `ouroboros run workflow --help`에서 설치 버전의 도움말을 먼저 확인하세요. `ouroboros run --help`는 하위 명령 목록만 보일 수 있습니다. 이 두 옵션은 별도의 실행 후 QA까지 끄는 옵션은 아닙니다. QA 생략은 `--no-qa`입니다. [원본 CLI 옵션](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md).

### 평가를 따로 요청할 때

호스트에서는 실행 세션과 Seed, 관찰한 결과를 지정해 `ooo evaluate`를 요청할 수 있습니다. 평가만 원한다면 `auto_evolve: false`로 자동 수정 반복을 끄도록 명시하세요. 평가도 모델 호출을 수반할 수 있습니다. MCP 백그라운드 평가에서 기본 자동 진화가 켜져 있으면 `final_approved: false`인 결과는 `unverified`를 포함해 Ralph 등록을 시도합니다. Seed를 불러오지 못하거나 등록이 실패하면 시작되지 않을 수 있으므로 연결된 job·skip·오류와 종료 상태를 확인합니다. 실제 검사 없이 나온 의미 평가만으로 승인됐다고 판단하지 않습니다. [평가 스킬 원본](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evaluate/SKILL.md), [평가 단계](/docs/architecture-detail/#_3).

## 예상

호스트 인터뷰 뒤에는 별도로 Seed를 만듭니다. CLI의 `init start`는 인터뷰 뒤 생성이 승인되고 성공한 경우 Seed 파일 경로를 표시합니다. 중단·거절·실패 시에는 파일이 있다고 가정하지 않습니다. 실행 요청 뒤에는 작업을 식별할 ID를 받을 수 있습니다. **ID를 받았다는 것만으로 기능이 완성되지는 않습니다.** 실제 ID와 파일 경로는 실행 환경마다 다릅니다.

## 확인

Seed에 `add`·`list`와 테스트 조건이 들어 있는지 먼저 읽으세요. 실행 뒤에는 응답의 `worktree_path`·`worktree_branch` 또는 독립 CLI가 출력하는 `Task worktree`·`Task branch`가 있는지 확인하고, 실제 보고된 작업 위치에서 결과를 살펴보세요. 모든 실행에 별도 worktree가 있다고 가정하지 말고 경로가 보고되지 않으면 실행 결과와 프로젝트 경로를 확인합니다. 그다음 [호스트 상태 조회](/docs/progress-detail/#host-status) 또는 [CLI 상태 조회](/docs/progress-detail/#cli-status)에서 같은 ID의 단계와 검증 결과를 읽고, 생성된 프로젝트에서 기능을 직접 실행해 입력한 작업이 목록에 나타나는지 확인하세요.

## 다음 행동

요구와 테스트가 모두 맞으면 자신의 작업 목표로 넘어갑니다. Seed에 조건이 빠졌다면 기존 YAML의 필요한 부분을 직접 수정하거나 호스트에 수정 내용을 지시하고 다시 읽어 확인하세요. 해당 Seed를 다시 생성하면 기존 온톨로지를 잃을 수 있으므로 `ouroboros_generate_seed`를 다시 호출하지 않습니다. 선택적 refine 절차에서는 사용자가 채택한 변경만 기존 YAML에 적용하고 수정 기록을 남깁니다. 실행 중이거나 ID만 받았다면 [진행상태 확인](/docs/progress-detail/)으로, 설치·인증·실행 오류라면 [실패 복구](/docs/recovery-detail/)로 이동하세요.

설치·인증·연결에서 막히면 [설치와 설정 오류](/docs/recovery-detail/#setup-errors)를 봅니다. 키나 토큰의 값은 대화나 문서에 붙여 넣지 않습니다.

![인터뷰 명령 시연](/assets/learn/ooo-interview.gif)

!!! note "첫 성공의 기준"
    Seed에 적은 요구가 결과 파일에 구현되고, 요구한 검증이 통과하며, 실제 기능을 실행해 확인해야 합니다. 이 사이트의 [예제](/docs/example-detail/)는 이 흐름을 읽어 보는 가상 시나리오입니다.

Seed와 모호도 점수의 뜻이 낯설면 [개념 안내](/docs/concepts-detail/)를 읽습니다. 명령의 정의는 [원문 출처](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2/docs)에서 확인할 수 있습니다.
