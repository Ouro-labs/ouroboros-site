# 호스트 설정과 복구

!!! warning "판본과 검증 범위"
    이 문서의 상세 동작과 합성 관찰은 별도 언급이 없는 한 고정 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 사용 중인 플러그인과 MCP 서버는 각각 다른 판본일 수 있습니다. 여기에 기록된 시험은 해당 조건의 관찰이며 실제 사용자 환경·모델·호스트 전체를 검증하지 않았습니다. 실행 전 설치된 버전의 도움말과 [현재 제품 CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [현재 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros)를 대조하세요. 판본 차이를 확인하지 않은 기능은 동일하다고 가정하지 않습니다.


조사일: 2026-11-04. 기준: [Q00/ouroboros `722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 설치된 버전이 다르면 먼저 `ouroboros --version`과 각 명령의 `--help`를 확인한다. 이 문서는 Codex 통합을 중심으로 설명하며 다른 런타임의 지원 범위는 [런타임 지원](/docs/runtime-support-detail/)을 참조한다.

## 먼저 구분하기

| 명령 | 범위와 주의점 |
| --- | --- |
| `ouroboros setup` | 런타임을 탐지하거나 `--runtime`으로 선택해 Ouroboros 설정과 해당 호스트 통합을 구성한다. 설정 파일과 호스트 산출물을 변경할 수 있다. `--non-interactive`는 질문을 생략할 뿐 읽기 전용이 아니다. |
| `ouroboros setup refresh` | 이전 통합의 산출물 설치 흔적을 검사해 해당 런타임 산출물을 갱신한다. Codex는 설정 디렉터리가 존재하거나 `codex` 실행 파일을 찾으면 갱신 대상이 된다. 여러 런타임에 영향을 줄 수 있다. 일부 실패 시 경고 후 종료 코드 1이다. |
| `ouroboros codex refresh` | Codex용 규칙과 스킬만 패키지에서 다시 설치한다. MCP 설정과 Ouroboros 설정은 변경하지 않는다. 관리 대상 규칙과 스킬은 덮어쓸 수 있으며, 남은 이전 산출물은 자동 정리하지 않는다. 실패 시 종료 코드 1이다. |
| `ouroboros codex doctor` | Codex 규칙, 자동 실행 스킬, MCP 설정의 정적 진단이다. 기본 실행은 MCP 서버를 시작하지 않는다. `--live-mcp`는 별도 프로세스를 시작한다. |

`setup`의 `--runtime`은 실행 호스트 통합을 고르는 것이며, LLM 인증이나 모델 서비스가 실제로 동작한다는 증거는 아니다. OpenCode의 `--opencode-mode plugin|subprocess`는 별도 선택이다. [공식 CLI 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md)와 [설정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup.py)을 참조한다.

Codex 설정의 기본 위치는 `~/.codex/config.toml`이며 `CODEX_HOME`이 설정되어 있으면 그 디렉터리를 사용한다. Ouroboros 자체 설정은 `~/.ouroboros/config.yaml`이다. 같은 컴퓨터에서도 실행 사용자, `HOME`, `CODEX_HOME`이 다르면 다른 설정을 보게 된다. Codex 프로필 선택과 MCP 등록은 별개다.

## Codex MCP 모드

**Codex 플러그인 세션 확인:** 고정 main `592c667f`와 release `0.59.9`의 welcome은 Ouroboros 런타임 설정과 Codex `config.toml`의 Ouroboros MCP 항목 등을 검사하므로, 플러그인이 현재 세션에서 MCP를 제공하더라도 `CODEX_SETUP_REQUIRED`가 나올 수 있다. 이 메시지나 `codex mcp list`에 항목이 없다는 사실만으로 서버 부재를 단정하거나 setup을 반복하지 말고, 같은 호스트·세션에서 플러그인 활성화와 서버·도구 목록을 확인한다. 목록에 보이는 것만으로 실제 도구 호출 성공을 보장하지는 않는다. 별도 setup은 MCP 등록뿐 아니라 런타임·모델 설정이나 관리 스킬·규칙을 바꿀 수 있으므로 대상과 영향을 먼저 검토하고 사용자가 결정한다. `preserve`도 유효한 기존 Codex 항목이 없으면 실패한다. 실제 호스트 연결은 이 설명에서 시험하지 않았다. [main welcome](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/welcome/SKILL.md#L545-L592) · [release welcome](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/skills/welcome/SKILL.md#L545-L592) · [main setup](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L1248-L1277) · [release setup](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/setup.py#L1246-L1275).

`--mcp-mode`는 **Codex 통합의 MCP 등록**에 적용된다. 다른 설정이나 산출물 전체의 보존을 약속하는 옵션이 아니다.

| 모드 | 이 버전의 동작 |
| --- | --- |
| `auto` (기본) | 관리 대상 MCP 항목은 갱신할 수 있고 사용자가 관리하는 기존 URL이나 사용자 정의 항목은 보존한다. 단, 비 Windows 경로에서는 기존 항목의 보존 여부를 확인하기 전에 관리 항목에 사용할 실행기를 먼저 해석한다. 실행기를 찾지 못하면 기존 사용자 URL이 유효해도 실패할 수 있다. 사용할 command 또는 URL이 없는 기존 항목은 오류로 처리한다. 네이티브 Windows에서는 별도의 안전 규칙을 적용한다. |
| `preserve` | 기존 MCP 항목을 변경하지 않으며 위 실행기 해석보다 먼저 별도로 검사한다. 기존 TOML이 유효하고 Ouroboros 항목에 사용 가능한 command 또는 URL이 있어야 한다. 설정 파일이나 항목이 없거나 유효하지 않으면 성공으로 간주하지 않는다. |
| `stdio` | 지원 호스트에서 관리되는 stdio 항목으로 교체한다. 기존 사용자 정의 항목도 교체될 수 있으므로 선택 전에 현재 설정과 복구 방법을 확인한다. |
| `http` | 네이티브 Windows Codex Desktop을 위한 명시적 loopback URL 설정이다. 다른 플랫폼에서는 오류다. |

`auto`가 기존 설정을 보존했다는 메시지는 연결 성공을 뜻하지 않는다. 실제 등록 경로와 Windows의 추가 제약은 [Windows/WSL](/docs/windows-wsl-detail/)과 [Windows 모드 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/windows_codex_mcp.py)을 확인한다. 표준 릴리스의 stdio 실행기는 의존성 격리를 위해 `uvx` 또는 `pipx` 등을 사용한다. 실행기가 없거나 TOML을 파싱할 수 없다면 setup이 실패할 수 있다. 오류 안내를 확인하고 누락된 도구를 설치하기 전에 버전과 환경을 확인한다.

## 점검과 복구 순서

1. `ouroboros setup --help`, `ouroboros codex refresh --help`, `ouroboros codex doctor --help`로 설치 버전의 옵션을 확인한다. 실행할 계정의 설정 위치도 확인한다.
2. `ouroboros codex doctor`로 정적 점검한다. `--codex-dir PATH`로 조사 대상 디렉터리를 지정할 수 있다. 이 지정은 그 명령의 점검 대상이며, 이후 refresh의 대상까지 바꾸지는 않는다.
3. 규칙이나 스킬이 누락·오래된 경우 변경 범위를 이해한 뒤 같은 `CODEX_HOME`에서 `ouroboros codex refresh`를 실행하고 doctor를 다시 실행한다. 이 명령은 MCP 설정을 고치지 않는다. MCP 항목 문제는 오류와 현재 설정을 확인하고 적절한 모드로 별도 복구한다.
4. 필요하면 `ouroboros codex doctor --live-mcp`로 설정된 **stdio** 서버를 실행해 MCP `initialize`와 `list_tools`, 자동 실행에 필요한 도구를 확인한다. 설정된 실행 명령 자체가 부작용이나 네트워크 사용을 할 수 있으므로 먼저 내용을 확인한다. URL 전송은 이 실시간 검사 대상이 아니다. 성공해도 모델 인증이나 실제 작업 전체가 검증된 것은 아니다.
5. `setup` 실패 시 출력과 해당 설정 파일을 확인한다. 구현에는 일부 다중 파일 변경에 대한 복구 처리가 있지만 모든 경우의 원자적 롤백을 보장하지 않는다. 남은 변경을 확인하고 필요한 경우 기존 백업에서 복구한다. 비밀값을 진단 자료에 포함하지 않는다.

업데이트 도중 통합 갱신이 실패하면 패키지는 이미 바뀌었을 수 있다. `update`가 출력한 정확한 복구 명령을 같은 환경에서 확인해 실행한다. 이미 최신 버전이면 다시 `update`를 실행해도 실패한 갱신이 자동으로 재실행되지 않는다. 자세한 내용은 [업데이트와 복구](/docs/update-detail/), MCP 일반 진단은 [진단](/docs/diagnostics-detail/)을 참조한다.

## 근거와 검증 범위

- 소스 확인: [setup refresh 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup_refresh.py), [Codex refresh/doctor 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/codex.py), 위 CLI 참조 및 setup 구현.
- 실제 확인: 별도 임시 `HOME`에서 로컬 체크아웃의 `ouroboros setup --help`를 실행해 옵션과 기본값을 확인했다. 이 체크아웃의 HEAD는 기준 커밋과 다르므로 실행 결과는 해당 체크아웃의 증거다. 사용자 설정 변경이나 실제 setup, 서버 실행, 모델 호출은 하지 않았다.
- 미검증: 실제 사용자 설정에서의 변경·복구, 네이티브 Windows 동작, 각 호스트의 실제 인증 및 연결. 환경에 따른 결과는 소스와 도움말만으로 보장할 수 없다.
