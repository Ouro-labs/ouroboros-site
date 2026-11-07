# Megacode Harness에서 Ouroboros 사용하기

이 안내서는 Megacode Harness에 Ouroboros를 연결하고 첫 요청을 보내는 방법, 설치기가 바꾸는 파일, 갱신과 복구의 한계를 설명합니다. 근거는 Ouroboros 소스 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [Megacode 런타임 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/runtime-guides/megacode.md), 설치 구현과 런타임 코드입니다.

설치·로그인·인증·작업을 실제로 실행하지 않았으며 공개 배포판, Megacode 버전, 호스트 환경 간 동등성도 검증하지 않았습니다. 사용 중인 `ouroboros`와 `harness` 버전 및 도움말을 확인하세요.

## 작동 방식

이 통합은 두 흐름을 연결합니다. Megacode 세션은 복사된 Ouroboros skills, MCP 서버, `AGENTS.md`의 라우팅 표를 통해 Ouroboros를 사용합니다. 반대로 Ouroboros worker와 모델 완성 요청은 대화형 입력 없이 `harness -p`를 실행해 Megacode에서 처리합니다. Megacode 세션의 인증과 모델 선택은 Harness가 관리하며, Ouroboros가 Megacode에 직접 로그인하지는 않습니다.

## 설치 전제 조건

- 현재 터미널에서 실행할 수 있는 Megacode `harness` CLI. Megacode 안내에 따라 설치되어 있어야 합니다.
- 호스팅 `mega:*` 모델을 쓴다면 Harness 로그인, 또는 적절한 provider 키. 인증 상태는 검증하지 않았습니다.
- Ouroboros MCP 서버를 실행할 `uv`/`uvx` 또는 `pipx`. 설치 코드는 두 실행기를 찾아보며, 둘 다 없으면 설정을 중단합니다.
- `setup --runtime megacode`가 실제 도움말에 나타나는 Ouroboros CLI. 고정 release `v0.59.9` Git tree에는 Megacode setup 구현 파일과 이 runtime 분기가 없습니다([해당 release의 CLI 명령 디렉터리](https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands)). 이 안내는 `main` `592c667f` 구현을 설명하며, release나 설치판에서 지원된다고 가정하지 않습니다. 설정 전에 사용할 CLI에서 `ouroboros setup --help`를 확인하세요.

설치기는 `harness paths`를 호출해 Harness의 `CONFIG` 디렉터리를 확인합니다. 출력에 완전하고 유일하며 판별 가능한 `CONFIG` 항목이 있어야 합니다. 경로 표기에 제어 문자나 모호한 이스케이프가 있으면 파일을 쓰지 않고 중단합니다. Megacode 0.23에서는 경로 출력의 일부 이스케이프를 원래 문자와 구별할 수 없으므로, 거부되면 경로를 추측하거나 출력을 수동으로 바꾸지 마세요. 사용 중인 버전에서 실제 설정 경로와 지원 여부를 먼저 확인하세요.

Harness CLI 선택 우선순위는 `OUROBOROS_MEGACODE_CLI_PATH`, `~/.ouroboros/config.yaml`의 `orchestrator.megacode_cli_path`, `PATH`의 `harness` 순입니다. 단, 프로젝트 `.env`에서 온 환경 변수 재정의는 무시됩니다. 절대 실행 파일 경로나 디렉터리 구성요소가 없는 명령 이름을 사용할 수 있습니다. `./harness`, `bin/harness` 같은 상대 경로는 지원하지 않습니다. 명시한 경로가 유효하지 않으면 실패하며, 프로젝트 디렉터리에서 같은 이름의 실행 파일을 대신 찾지 않습니다. 자세한 내용은 고정 소스의 [경로 해석 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/_megacode_cli.py)을 참고하세요.

## 설치와 첫 사용

`harness`를 설치했고 현재 터미널에서 실행할 수 있는지 확인합니다. 먼저 `ouroboros setup --runtime megacode`가 실제 설치 CLI의 도움말에 있는지 확인하세요. 설정을 실행하기 전에 그 명령이 선택할 **동일한 Harness 실행 파일**에 `paths`를 실행하고 `CONFIG` 경로를 확인해야 합니다. 선택 우선순위는 `OUROBOROS_MEGACODE_CLI_PATH` 환경 변수, `~/.ouroboros/config.yaml`의 `orchestrator.megacode_cli_path`, 마지막으로 `PATH`의 `harness`입니다. 앞의 두 경로 중 하나가 선택되면 단순히 `harness paths`를 실행하지 말고, 선택된 정확한 실행 파일에 `paths`를 전달하세요. 예를 들어 POSIX 셸에서 환경 변수 값이 선택된 경우 `"$OUROBOROS_MEGACODE_CLI_PATH" paths`, PowerShell에서는 `& $env:OUROBOROS_MEGACODE_CLI_PATH paths`를 사용합니다. 설정 파일 값이 선택됐다면 그 값의 정확한 실행 파일에 현재 셸의 인용 규칙을 적용하세요. 마지막 PATH 항목이 선택된 경우 `harness`가 alias나 함수가 아닌 동일 실행 파일인지 확인한 뒤 `harness paths`를 실행하고, 여러 파일이 검색되거나 실행 파일이 다르면 그 선택 경로를 직접 사용하세요. 환경 변수 설정은 셸마다 다르므로 `paths`와 setup 명령을 같은 환경에서 실행하고, 현재 디렉터리의 `.env`가 이 선택을 바꾼다고 가정하지 마세요. 어떤 실행 파일이 선택될지 모르거나 `paths`가 setup 대상과 같은 실행 파일에서 나온 것인지 확인할 수 없다면 멈추세요. OS별 기본 경로를 추측하지 말고, 경로가 없거나 출력이 불완전·모호하거나 해석할 수 없어도 중단하세요. 설치 구현은 완전하고 유일하게 판별되는 `CONFIG` 경로가 아니면 설정을 거부합니다. Megacode 0.23의 일부 이스케이프 표기는 원래 경로와 구별되지 않을 수 있으므로 거부된 경로를 직접 해독하거나 바꿔 넣지 마세요.

정확한 `CONFIG` 경로에서 기존 `ouroboros/skills/`, `config.toml`, `AGENTS.md`가 있는지와 내용을 먼저 살펴보세요. 보존할 것이 있으면 Harness 설정 디렉터리 바깥의 **새 위치**에 사본을 만들고, 기존 백업을 덮어쓰지 않도록 위치가 비어 있는지 확인하세요. 사본을 열어 예상한 파일과 내용이 들어 있는지 확인하고, 가능한 경우 파일 권한·메타데이터도 보존됐는지 확인하세요. 특히 `ouroboros/skills/`는 설정 시 디렉터리 전체가 제거된 뒤 새 복사본으로 대체됩니다. 사본과 내용을 확인할 수 없거나 원본을 보존해야 한다면 아래 명령을 실행하지 마세요. 설치기가 바꾸는 범위와 실패 시 한계는 [아래 파일 목록과 주의사항](#_4)에도 정리했습니다. main의 구현은 [Megacode 설정 코드](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/megacode_setup.py#L230-L340), [파일 쓰기 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4230-L4254)에서 확인할 수 있습니다. release `v0.59.9` Git tree에는 이 Megacode setup 경로가 없으며, 로컬에 있는 다른 패키지 소스가 그 release에서 지원된다는 증거는 아닙니다. 실제 설치본이나 각 OS의 파일시스템 권한 동작은 시험하지 않았습니다.

보존할 자료를 확인한 뒤에만 다음 설정 명령을 실행합니다.

```sh
ouroboros setup --runtime megacode
```

설정이 끝나면 사전 점검에서 `CONFIG` 경로를 확인한 **동일한 Harness 실행 파일**을 시작합니다. 사전 점검·setup·시작 사이에 선택 환경을 바꾸지 마세요. `OUROBOROS_MEGACODE_CLI_PATH`가 선택된 경우에는 아래처럼 그 변수를 그대로 실행하세요. PowerShell 명령은 Windows 셸용입니다.

```text
# POSIX 셸: 환경 변수 override가 선택된 경우
"$OUROBOROS_MEGACODE_CLI_PATH"

# PowerShell: 환경 변수 override가 선택된 경우
& $env:OUROBOROS_MEGACODE_CLI_PATH
```

`~/.ouroboros/config.yaml`의 override가 선택됐다면 설정값에 지정한 정확한 실행 파일을 현재 셸의 인용 규칙으로 실행하세요. 경로에 공백이 있다면 POSIX 셸에서는 큰따옴표로 감싸고, PowerShell에서는 작은따옴표로 감싼 경로를 call operator `&`로 실행합니다. **`harness`라는 이름은 사전 점검에서 PATH fallback이 실제 선택된 경우에만 사용하세요.**

```sh
harness
```

Harness 세션에서 다음과 같은 Ouroboros 요청을 시도할 수 있습니다.

```text
ooo interview build me a small CLI
```

초기 설정은 Harness 로그인을 대신하지 않으며 MCP 연결이나 모델 요청이 작동한다는 증거도 아닙니다. `ooo`가 라우팅되지 않으면 같은 Harness 설정 디렉터리에서 서버 활성화·시작 상태, skill 탐색, 로그를 확인하세요. CLI 설치, 호스트 등록, MCP 연결, 인증 문제를 구분해야 합니다. 설치가 성공했다는 표시만으로 실제 연결을 확인할 수는 없습니다.

Ouroboros CLI에서 한 번의 Seed 실행에 Megacode 런타임을 지정할 수도 있습니다.

!!! warning "CLI 실행 전에 별도 격리 경계를 확인하세요"
    아래 두 `ouroboros run ... --runtime megacode` 예제는 제품 main `592c667f`의 standalone CLI 경로입니다. 이 경로가 `OrchestratorRunner`를 통하면 runner가 adapter 권한을 `bypassPermissions`로 강제하고 Megacode 호출을 `harness -p --sandbox off`로 구성합니다. Harness sandbox를 보호 경계로 가정하지 마세요. 이것은 setup이 Harness MCP 서버 설정에 기록하는 `sandbox = false`와 별개인 CLI 실행 동작입니다. 실행 전에 별도 OS 사용자·VM·컨테이너가 적용하는 파일 및 네트워크 정책을 확인하고, 격리를 확인할 수 없다면 실행하지 마세요. 세부 근거와 범위는 [Megacode CLI sandbox 경계](#megacode-cli-sandbox-boundary)에서 확인하세요. release `0.59.9`에는 이 안내의 Megacode CLI runtime 구현이 없어 해당 예제의 지원을 뜻하지 않습니다([release orchestrator 소스 트리](https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator)).

```sh
ouroboros run workflow seed.yaml --runtime megacode
```

이 경로에서도 Megacode 모델 backend를 사용하려면 문서에 제시된 환경 변수 형식을 사용할 수 있습니다.

```sh
OUROBOROS_LLM_BACKEND=megacode ouroboros run workflow seed.yaml --runtime megacode
```

`seed.yaml`은 실제 Seed 파일 경로로 바꾸세요. CLI 실행에서 런타임을 선택하는 것은 대화형 호스트에 MCP 설정을 설치하는 것과 다릅니다.

## 설치기가 수정하는 파일

아래 경로는 모두 setup 명령이 실제 선택할 Harness 실행 파일의 `paths` 결과에서 확인한 동일한 `CONFIG` 디렉터리를 기준으로 합니다.

| 경로 | 설치기가 쓰는 내용 | 설정을 다시 실행할 때 |
| --- | --- | --- |
| `config.toml` | `ouroboros setup --runtime megacode`가 관리하는 블록: skills 경로, worker/LLM 두 mode, `mcp.servers.ouroboros` 실행 설정 | 설치기 관리 블록만 교체하고 블록 밖 텍스트는 보존합니다. 파일 자체는 다시 쓰며 코드에서 `0600` 모드를 지정합니다. |
| `ouroboros/skills/` | 현재 Ouroboros 설치에 포함된 skills를 복사합니다. 각 디렉터리는 `SKILL.md` frontmatter의 `name`을 따릅니다. | **이 디렉터리 전체를 삭제하고 새 복사본으로 교체합니다.** 사용자 정의 skill이나 다른 로컬 파일은 사라지며 설치기가 백업하지 않습니다. |
| `AGENTS.md` | Ouroboros가 관리하는 `ooo <명령>` 라우팅 블록. Harness에는 여기서 필요한 keyword hook이 없어 라우팅 표를 사용합니다. | 설치기 관리 블록만 교체하고 나머지 텍스트는 보존합니다. |

기존 TOML에 `[skills]`, `[modes.ouroboros-worker]`, `[modes.ouroboros-llm]` 또는 `[mcp.servers.ouroboros]` 표가 있으면 설치기는 충돌한 표 이름을 알리고 중단합니다. 이를 자동 병합하거나 덮어쓰지 않습니다. TOML이 잘못되었거나 관리 대상이 심볼릭 링크이거나 `CONFIG` 경로를 안전하게 판별할 수 없는 경우에도 설정을 거부합니다. 설치를 진행하려고 사용자 설정을 바로 지우지 마세요. 먼저 설정 소유자가 충돌 항목을 어떻게 병합할지 결정해야 합니다.

이 설정은 공유 `~/.ouroboros/config.yaml`을 수정하지 않습니다. 다만 교체 대상인 `ouroboros/skills/`를 백업하지 않으며, 세 대상의 쓰기가 하나의 원자적 작업으로 처리되거나 실패 시 전체 복구된다고 보장하지 않습니다. `config.toml` 쓰기는 코드에서 `0600` 모드를 지정합니다. `AGENTS.md`는 기존 파일의 권한 모드를 유지하고, 새 파일은 코드 기본값 `0644`를 사용합니다. 실제 권한 적용은 OS와 파일시스템에 따라 확인하세요. 설치가 중간에 실패하면 기존 skills가 복구되었다고 가정하지 말고 `config.toml`, `AGENTS.md`, `ouroboros/skills/`를 각각 다시 확인하세요. 기존 `config.toml`과 `AGENTS.md`의 관리 블록 밖 텍스트는 보존되지만, 두 파일 자체는 다시 쓰입니다. 설정 소유자는 사본을 먼저 확인하고 실행 후 관리 블록·파일 내용·권한을 점검해야 합니다.

### Megacode CLI sandbox 경계 {#megacode-cli-sandbox-boundary}

설치기는 Harness의 Ouroboros MCP 서버를 `sandbox = false`로 설정하고, `uvx` 또는 `pipx`로 `--runtime megacode --llm-backend megacode` 인수를 사용해 서버를 실행합니다. Harness의 `ouroboros-worker` mode에는 파일 읽기/쓰기/편집, 명령 실행, 검색 도구가 제공되며 대화형 질문은 비활성화됩니다. 이것은 setup이 만드는 MCP 서버 설정입니다. 별도로, standalone CLI의 `ouroboros run ... --runtime megacode`가 `OrchestratorRunner`를 통하면 runner가 adapter 권한을 `bypassPermissions`로 강제하고, Megacode runtime은 이를 `harness -p --sandbox off`로 전달합니다([runner 권한 처리](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L879), [권한 강제 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L5190-L5207), [Megacode 명령 구성](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/megacode_runtime.py#L239-L245)). 이 주장은 해당 CLI 경로에 한정되며, 일반적인 대화형 Harness 세션 전체나 다른 실행 경로를 설명하지 않습니다. 이 CLI 경로에서는 Harness sandbox 설정이 보호 경계라고 가정하지 마세요. 신뢰하지 않는 프로젝트나 민감한 환경에서 실행하기 전에는 별도 OS 사용자·VM·컨테이너의 파일 및 네트워크 정책을 확인하고, 격리를 확인할 수 없다면 실행하지 마세요. setup이 성공했다는 사실도 실제 작업이 격리됐다는 증거가 아닙니다.

## 업그레이드 후 갱신

Megacode setup 경로가 포함된 Ouroboros 버전으로 업그레이드했다면, 먼저 설치 CLI의 `ouroboros setup --help`와 위의 정확한 Harness 실행 파일·백업 절차를 다시 확인하세요. release `v0.59.9` Git tree에는 이 경로가 없으므로 업그레이드만으로 Megacode setup이 제공된다고 가정하지 마세요. 대상 버전이 해당 setup을 실제로 지원하고 보존 사본을 확인한 뒤에만 다음 명령을 다시 실행합니다.

```sh
ouroboros setup --runtime megacode
```

복사한 skills와 설치기가 관리하는 `config.toml`, `AGENTS.md` 블록이 갱신됩니다. 특히 `ouroboros/skills/`는 통째로 교체되므로 사용자 정의 파일을 먼저 보관하세요. 설정 표가 충돌하면 자동 병합되지 않고 설치기가 중단됩니다. 실행 후 관리 블록, skills 디렉터리, 원래 블록 밖 텍스트를 확인하고 Harness에서 `ooo` 라우팅과 도구 탐색을 다시 점검하세요.

## 재시도와 복구의 한계

Harness의 headless `harness -p` 세션은 기존 세션을 이어서 실행할 수 없습니다. worker 또는 LLM 호출은 매번 새 세션이며 Megacode 런타임은 같은 Harness 세션을 자동 복구하지 않습니다. 중단되면 Ouroboros의 기존 job/session 기록과 Seed 작업 디렉터리에서 작업 계보, 실제 파일, 상태를 확인하세요. 기존 작업이 끝났고 이미 발생한 부작용을 파악한 뒤 Ouroboros에서 새 시도를 시작할지 결정하세요. 다시 실행하는 일을 Harness 세션 이어하기라고 표현하지 마세요.

Q00 main `592c667f` 소스는 Harness 설정에 `[mcp.servers.ouroboros]` 항목을 쓰고 worker와 LLM completion 각각을 별도의 headless `harness -p` 호출로 구성하는 것을 확인합니다. Q00의 런타임 안내는 각 호출에서 Harness 설정의 MCP 서버가 시작된다고 설명하지만, 여기서는 Harness 자체 구현이나 설치된 `0.31.1` 프로세스를 실행해 그 동작을 독립 확인하지 않았습니다. 따라서 모든 설정 서버가 매 호출마다 시작된다고 일반화하지 마세요. worker mode의 도구 목록에서 `mcp`가 빠져 있다는 사실만으로 서버 프로세스의 시작 여부도 알 수 없습니다. 호출 지연이나 Ouroboros 도구 미발견을 조사할 때는 선택된 실제 `CONFIG` 경로와 MCP 서버 항목, 설치한 Harness 버전, 해당 서버의 시작·연결 상태를 확인하세요. 그 Harness 버전이 호출마다 서버를 시작한다면 시작 시간이 추가될 수 있습니다. Megacode CLI는 다른 CLI 런타임에서 사용하는 실행 파일 신원 증명 기능에도 아직 포함되지 않습니다. [Q00 런타임 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/runtime-guides/megacode.md#L63-L90) · [Harness MCP 항목을 쓰는 setup 코드](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/megacode_setup.py#L143-L160) · [worker 명령 구성](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/megacode_runtime.py#L219-L248) · [LLM completion 명령 구성](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/megacode_llm_adapter.py#L193-L218).

## 호스트, 설치본, 버전 구분

`ouroboros setup --runtime megacode`는 Megacode Harness의 `CONFIG` 디렉터리에 서버, skills, 명령 라우팅을 설정합니다. Claude Code, Codex 등 다른 호스트의 MCP 설정은 변경하지 않습니다. 다른 호스트에는 해당 호스트용 설치 방법을 사용하세요. 반대로 Ouroboros CLI의 `--runtime megacode`는 단일 실행의 런타임을 선택하는 옵션이며 대화형 호스트를 Megacode로 전환하지 않습니다.

`harness --version`, `ouroboros --version`, 호스트가 실제로 실행하는 MCP 패키지는 서로 다른 설치본이나 버전을 가리킬 수 있습니다. 문제가 발생한 기기, 사용자, 호스트 세션, CLI 버전, Harness 버전, 설정 디렉터리를 기록하고 각 환경의 도움말과 호스트 로그를 확인한 뒤 차이를 판단하세요. 이 문서는 실제 인증 흐름, 모델 호출, 파일 변경, 설치 실패 후 현장 복구를 검증하지 않았으며, 공개 배포본이 고정 소스 커밋과 완전히 같은 동작을 하는지도 확인하지 않았습니다.
