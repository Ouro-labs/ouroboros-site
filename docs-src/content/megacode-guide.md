# Megacode Harness에서 Ouroboros 사용하기

이 안내서는 Megacode Harness에 Ouroboros를 연결하고 첫 요청을 보내는 방법, 설치기가 바꾸는 파일, 갱신과 복구의 한계를 설명합니다. 근거는 Ouroboros 소스 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [Megacode 런타임 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/runtime-guides/megacode.md), 설치 구현과 런타임 코드입니다.

설치·로그인·인증·작업을 실제로 실행하지 않았으며 공개 배포판, Megacode 버전, 호스트 환경 간 동등성도 검증하지 않았습니다. 사용 중인 `ouroboros`와 `harness` 버전 및 도움말을 확인하세요.

## 작동 방식

이 통합은 두 흐름을 연결합니다. Megacode 세션은 복사된 Ouroboros skills, MCP 서버, `AGENTS.md`의 라우팅 표를 통해 Ouroboros를 사용합니다. 반대로 Ouroboros worker와 모델 완성 요청은 대화형 입력 없이 `harness -p`를 실행해 Megacode에서 처리합니다. Megacode 세션의 인증과 모델 선택은 Harness가 관리하며, Ouroboros가 Megacode에 직접 로그인하지는 않습니다.

## 설치 전제 조건

- 현재 터미널에서 실행할 수 있는 Megacode `harness` CLI. Megacode 안내에 따라 설치되어 있어야 합니다.
- 호스팅 `mega:*` 모델을 쓴다면 Harness 로그인, 또는 적절한 provider 키. 인증 상태는 검증하지 않았습니다.
- Ouroboros MCP 서버를 실행할 `uv`/`uvx` 또는 `pipx`. 설치 코드는 두 실행기를 찾아보며, 둘 다 없으면 설정을 중단합니다.
- `setup --runtime megacode`를 지원하는 Ouroboros CLI.

설치기는 `harness paths`를 호출해 Harness의 `CONFIG` 디렉터리를 확인합니다. 출력에 완전하고 유일하며 판별 가능한 `CONFIG` 항목이 있어야 합니다. 경로 표기에 제어 문자나 모호한 이스케이프가 있으면 파일을 쓰지 않고 중단합니다. Megacode 0.23에서는 경로 출력의 일부 이스케이프를 원래 문자와 구별할 수 없으므로, 거부되면 경로를 추측하거나 출력을 수동으로 바꾸지 마세요. 사용 중인 버전에서 실제 설정 경로와 지원 여부를 먼저 확인하세요.

Harness CLI 선택 우선순위는 `OUROBOROS_MEGACODE_CLI_PATH`, `~/.ouroboros/config.yaml`의 `orchestrator.megacode_cli_path`, `PATH`의 `harness` 순입니다. 단, 프로젝트 `.env`에서 온 환경 변수 재정의는 무시됩니다. 절대 실행 파일 경로나 디렉터리 구성요소가 없는 명령 이름을 사용할 수 있습니다. `./harness`, `bin/harness` 같은 상대 경로는 지원하지 않습니다. 명시한 경로가 유효하지 않으면 실패하며, 프로젝트 디렉터리에서 같은 이름의 실행 파일을 대신 찾지 않습니다. 자세한 내용은 고정 소스의 [경로 해석 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/_megacode_cli.py)을 참고하세요.

## 설치와 첫 사용

`harness`를 설치했고 현재 터미널에서 실행할 수 있는지 확인한 뒤 다음 명령을 실행합니다.

```sh
ouroboros setup --runtime megacode
```

설정이 끝나면 Harness를 실행합니다.

```sh
harness
```

Harness 세션에서 다음과 같은 Ouroboros 요청을 시도할 수 있습니다.

```text
ooo interview build me a small CLI
```

초기 설정은 Harness 로그인을 대신하지 않으며 MCP 연결이나 모델 요청이 작동한다는 증거도 아닙니다. `ooo`가 라우팅되지 않으면 같은 Harness 설정 디렉터리에서 서버 활성화·시작 상태, skill 탐색, 로그를 확인하세요. CLI 설치, 호스트 등록, MCP 연결, 인증 문제를 구분해야 합니다. 설치가 성공했다는 표시만으로 실제 연결을 확인할 수는 없습니다.

Ouroboros CLI에서 한 번의 Seed 실행에 Megacode 런타임을 지정할 수도 있습니다.

```sh
ouroboros run workflow seed.yaml --runtime megacode
```

이 경로에서도 Megacode 모델 backend를 사용하려면 문서에 제시된 환경 변수 형식을 사용할 수 있습니다.

```sh
OUROBOROS_LLM_BACKEND=megacode ouroboros run workflow seed.yaml --runtime megacode
```

`seed.yaml`은 실제 Seed 파일 경로로 바꾸세요. CLI 실행에서 런타임을 선택하는 것은 대화형 호스트에 MCP 설정을 설치하는 것과 다릅니다.

## 설치기가 수정하는 파일

아래 경로는 모두 `harness paths`가 출력하는 `CONFIG` 디렉터리를 기준으로 합니다.

| 경로 | 설치기가 쓰는 내용 | 설정을 다시 실행할 때 |
| --- | --- | --- |
| `config.toml` | `ouroboros setup --runtime megacode`가 관리하는 블록: skills 경로, worker/LLM 두 mode, `mcp.servers.ouroboros` 실행 설정 | 설치기 관리 블록만 교체하고 블록 밖 텍스트는 보존합니다. |
| `ouroboros/skills/` | 현재 Ouroboros 설치에 포함된 skills를 복사합니다. 각 디렉터리는 `SKILL.md` frontmatter의 `name`을 따릅니다. | **이 디렉터리 전체를 삭제하고 새 복사본으로 교체합니다.** 사용자 정의 skill이나 다른 로컬 파일은 사라지며 설치기가 백업하지 않습니다. |
| `AGENTS.md` | Ouroboros가 관리하는 `ooo <명령>` 라우팅 블록. Harness에는 여기서 필요한 keyword hook이 없어 라우팅 표를 사용합니다. | 설치기 관리 블록만 교체하고 나머지 텍스트는 보존합니다. |

기존 TOML에 `[skills]`, `[modes.ouroboros-worker]`, `[modes.ouroboros-llm]` 또는 `[mcp.servers.ouroboros]` 표가 있으면 설치기는 충돌한 표 이름을 알리고 중단합니다. 이를 자동 병합하거나 덮어쓰지 않습니다. TOML이 잘못되었거나 관리 대상이 심볼릭 링크이거나 `CONFIG` 경로를 안전하게 판별할 수 없는 경우에도 설정을 거부합니다. 설치를 진행하려고 사용자 설정을 바로 지우지 마세요. 먼저 설정 소유자가 충돌 항목을 어떻게 병합할지 결정해야 합니다.

이 설정은 공유 `~/.ouroboros/config.yaml`을 수정하지 않습니다. 다만 교체 대상인 `ouroboros/skills/`를 백업하지 않으며, 전체 파일 쓰기가 하나의 원자적 작업으로 처리된다고 보장하지도 않습니다. 해당 디렉터리에 사용자 정의 내용이 있다면 필요한 파일을 설치 대상 바깥에 복사하고 복사본을 읽을 수 있는지 확인한 다음 setup을 실행하세요. setup이 중간에 실패하면 기존 skills가 복구되었다고 가정하지 말고 위 세 경로를 다시 확인하세요. 기존 `config.toml`과 `AGENTS.md`의 관리 블록 밖 텍스트는 보존되지만, 설정 소유자가 두 파일 전체를 먼저 확인하고 복구 가능한 사본을 보관해야 합니다.

설치기는 Harness의 Ouroboros MCP 서버를 `sandbox = false`로 설정하고, `uvx` 또는 `pipx`로 `--runtime megacode --llm-backend megacode` 인수를 사용해 서버를 실행합니다. Harness의 `ouroboros-worker` mode에는 파일 읽기/쓰기/편집, 명령 실행, 검색 도구가 제공되며 대화형 질문은 비활성화됩니다. 기본적으로 Harness에 설정된 sandbox를 유지합니다. Ouroboros의 `bypassPermissions`를 사용하면 headless worker에 `--sandbox off`가 전달되어 프로젝트 밖에 쓸 수 있고 네트워크도 허용됩니다. 실행 전 프로젝트 디렉터리, Harness sandbox 설정, 실제 권한 mode를 확인하세요. 설정이 설치됐다는 사실이 작업이 격리됐다는 뜻은 아닙니다.

## 업그레이드 후 갱신

Ouroboros를 업그레이드한 뒤 다음 명령을 다시 실행합니다.

```sh
ouroboros setup --runtime megacode
```

복사한 skills와 설치기가 관리하는 `config.toml`, `AGENTS.md` 블록이 갱신됩니다. 특히 `ouroboros/skills/`는 통째로 교체되므로 사용자 정의 파일을 먼저 보관하세요. 설정 표가 충돌하면 자동 병합되지 않고 설치기가 중단됩니다. 실행 후 관리 블록, skills 디렉터리, 원래 블록 밖 텍스트를 확인하고 Harness에서 `ooo` 라우팅과 도구 탐색을 다시 점검하세요.

## 재시도와 복구의 한계

Harness의 headless `harness -p` 세션은 기존 세션을 이어서 실행할 수 없습니다. worker 또는 LLM 호출은 매번 새 세션이며 Megacode 런타임은 같은 Harness 세션을 자동 복구하지 않습니다. 중단되면 Ouroboros의 기존 job/session 기록과 Seed 작업 디렉터리에서 작업 계보, 실제 파일, 상태를 확인하세요. 기존 작업이 끝났고 이미 발생한 부작용을 파악한 뒤 Ouroboros에서 새 시도를 시작할지 결정하세요. 다시 실행하는 일을 Harness 세션 이어하기라고 표현하지 마세요.

각 `harness -p` 실행은 mode에 `mcp` 도구가 없어도 Harness 설정의 MCP 서버를 모두 시작합니다. 여기에는 Ouroboros 서버도 포함되므로 worker/LLM 호출마다 시작 시간이 추가됩니다. Megacode CLI는 다른 CLI 런타임에서 사용하는 실행 파일 신원 증명 기능에도 아직 포함되지 않습니다. 관련 한계는 [런타임 소스](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/megacode_runtime.py)와 [모델 어댑터 소스](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/megacode_llm_adapter.py)를 참고하세요.

## 호스트, 설치본, 버전 구분

`ouroboros setup --runtime megacode`는 Megacode Harness의 `CONFIG` 디렉터리에 서버, skills, 명령 라우팅을 설정합니다. Claude Code, Codex 등 다른 호스트의 MCP 설정은 변경하지 않습니다. 다른 호스트에는 해당 호스트용 설치 방법을 사용하세요. 반대로 Ouroboros CLI의 `--runtime megacode`는 단일 실행의 런타임을 선택하는 옵션이며 대화형 호스트를 Megacode로 전환하지 않습니다.

`harness --version`, `ouroboros --version`, 호스트가 실제로 실행하는 MCP 패키지는 서로 다른 설치본이나 버전을 가리킬 수 있습니다. 문제가 발생한 기기, 사용자, 호스트 세션, CLI 버전, Harness 버전, 설정 디렉터리를 기록하고 각 환경의 도움말과 호스트 로그를 확인한 뒤 차이를 판단하세요. 이 문서는 실제 인증 흐름, 모델 호출, 파일 변경, 설치 실패 후 현장 복구를 검증하지 않았으며, 공개 배포본이 고정 소스 커밋과 완전히 같은 동작을 하는지도 확인하지 않았습니다.
