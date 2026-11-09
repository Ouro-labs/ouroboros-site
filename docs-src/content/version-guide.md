# 내가 쓰는 Ouroboros 판본 확인하기

Ouroboros에는 한 가지 “버전”만 있는 것이 아닙니다. 문서를 읽거나 문제를 확인할 때는 **제품 소스**, **터미널에서 실행하는 CLI 패키지**, **AI 호스트가 띄운 MCP 서버/플러그인**을 따로 적어 두세요. 호스트의 `ooo` 스킬과 터미널의 `ouroboros` 명령은 서로 다른 설치일 수 있습니다.

## 무엇을 확인하나요?

| 대상 | 확인 방법 | 그 확인으로 알 수 있는 것 |
| --- | --- | --- |
| 소스 checkout | 저장소에서 `git rev-parse HEAD`, `git describe --tags --always` | 현재 checkout의 commit과 그 commit에 붙은 가장 가까운 tag. 설치된 패키지나 실행 중 서버 버전은 아님 |
| 독립 CLI | 같은 터미널에서 `command -v ouroboros`, `ouroboros --version`, `ouroboros --help` | 해당 PATH가 선택한 명령 파일, 그 명령이 불러온 패키지 버전, 그 설치가 노출하는 도움말 |
| 호스트 MCP 서버 | 호스트의 실제 설정에서 실행 명령·인자·환경·작업 디렉터리를 확인한 뒤 서버 도구 목록과 입력 스키마 조회 | 그 연결이 제공하는 도구·스키마. `ouroboros --version`만으로는 호스트가 `uvx` 등으로 시작한 별도 환경을 확인할 수 없음 |
| 플러그인/스킬 | 해당 호스트의 플러그인 관리 화면과 설치된 스킬 내용 확인 | 호스트가 읽는 스킬·플러그인. 독립 CLI 설치의 존재나 버전을 증명하지 않음 |

독립 CLI가 있는 환경에서는 다음처럼 실행해 확인합니다.

```sh
command -v ouroboros
ouroboros --version
ouroboros --help
ouroboros status health
```

`status health`도 진단 정보입니다. 설정, DB, 런타임 실행 파일, 자격 증명의 존재를 확인할 수 있지만 인증 성공이나 모델 호출 성공을 보증하지 않습니다. 자격 증명 값을 공개된 출력이나 문서에 붙여 넣지 마세요. 명령을 찾지 못하면 플러그인만 설치된 구성일 수 있습니다. 먼저 [설치 경로](/docs/first-run-detail/)를 구분하고, 호스트 설정에서 실제 MCP 서버 명령을 확인하세요. 연결된 서버가 `list_tools`를 지원하면 도구 이름과 JSON 입력 스키마를 조회하되, 조회 결과는 해당 서버 연결에 한정됩니다.

## 이 문서의 판본 기준 {#version-scope}

이 사이트의 기존 CLI·설치 상세는 공개 upstream commit [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)를 기준으로 조사했습니다. 원본 [Getting Started](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/getting-started.md), [CLI 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md), [Seed 작성 가이드](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/seed-authoring.md)를 바탕으로 정리했습니다. 이 SHA는 문서가 기대하는 설치본을 뜻하지 않습니다.

여기에 새로 보강한 기능 설명과 소스 대조는 공개 upstream [main commit `592c667f076c3dad7ef68d7844e91480d80135d0`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)을 기준으로 합니다. `main`은 움직이는 참조 이름이므로 재현 가능한 인용에는 위 commit SHA를 사용합니다. 이 기준도 checkout 소스를 가리킬 뿐, 사용자의 설치물이 이 commit이라는 뜻은 아닙니다. 오래된 명령 상세는 722판과 설치된 CLI 도움말을, main 전용 설명은 기능이 설치판에 존재하는지 먼저 확인하세요.

공개 [release `v0.59.9`](https://github.com/Q00/ouroboros/tree/v0.59.9)는 commit [`5f5fca90662861201ff0a26f502edd22b272c4c6`](https://github.com/Q00/ouroboros/tree/5f5fca90662861201ff0a26f502edd22b272c4c6)을 가리킵니다. 이번에 대조한 `v0.59.9`와 main `592c667f` 소스의 차이는 다음처럼 범위를 한정해 이해해야 합니다.

- main에는 `skills/idk`와 인터뷰 보정 입력 경로가 있으며 `v0.59.9`에는 없습니다. [main 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/idk/SKILL.md), [main 인터뷰 처리](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py)
- `init.py`에서 main은 `megacode` runtime 선택지를 추가했습니다. 이 차이는 해당 선택지의 소스 존재를 말할 뿐, 설치 환경에서 실행 파일·인증·실행이 정상임을 뜻하지 않습니다. [main init.py](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py)
- 비교한 `init.py`와 `run.py`의 추가 차이는 YAML 파일을 UTF-8로 여는 명시적 인코딩 지정입니다. 두 파일의 diff는 [release 파일](https://github.com/Q00/ouroboros/blob/v0.59.9/src/ouroboros/cli/commands/init.py), [main 파일](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py), [main run.py](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py)에서 직접 비교할 수 있습니다.
- job 상태 조회에는 시작 수락이 아직 영속화되지 않은 `acceptance_pending` 관찰 상태가 main에 있습니다. 이 상태는 수락이나 워커 생존을 증명하지 않으며 같은 job ID로 재조회하라는 경계가 포함됩니다. [main job read-state 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/job_read_state.py)

위 항목은 해당 공개 Git 객체의 정적 소스 비교입니다. 모든 파일·의존성·배포 아티팩트의 완전한 기능 차이 목록도 아니고, 사용자의 실제 패키지를 검사한 결과도 아닙니다. release와 main 사이의 DB·실행 기록·capsule 호환성을 여기서 시험하지 않았습니다. 설치판본이 다르면 기능 존재와 입력 스키마를 설치된 서버의 도움말·도구 목록에 맞추고, 진행 중 세션을 판본 차이만으로 재개하거나 변환하지 마세요. 판본을 바꾼 뒤의 실행 기록 경계는 [진행 상태 안내](/docs/progress-detail/)와 [복구 안내](/docs/recovery-detail/)를 확인하세요.

### `0.59.9`의 실제 확인 범위

2026-11-04에 별도의 빈 Python 3.13 환경에 공개 `ouroboros-ai==0.59.9`를 설치하고, 그 독립 CLI에 대해 `ouroboros --version`, `ouroboros --help`, `ouroboros config init`, `ouroboros config validate`, `ouroboros status health`를 실행했습니다. 각 명령은 종료 코드 0을 반환했습니다. 버전은 `0.59.9`로 표시됐고, 설정 초기화는 그 시험용 HOME에 설정 파일을 만들었으며, 검증은 설정이 유효하다고 보고했습니다. health는 설정·미생성 DB·런타임 선택·자격 증명 template 상태를 진단했습니다. 설치판은 [공개 PyPI의 `0.59.9` 배포판](https://pypi.org/project/ouroboros-ai/0.59.9/)입니다.

이 시험은 격리된 임시 환경의 초기 CLI 확인입니다. 고정 소스 722와 패키지 전체가 동등함을 증명하지 않으며, 실제 사용자의 컴퓨터나 호스트에서 수행하지 않았습니다. 특히 인증 성공, 실제 모델 호출, 인터뷰와 Seed 생성, Seed 실행 및 작업 효과, Codex·Claude 등 각 host plugin/MCP 서버의 설치·연결은 시험하지 않았습니다. `status health`의 런타임/credential 진단은 실제 모델 요청의 성공 여부를 보장하지 않습니다. 동일 이름의 도구나 기능이 있더라도 배포판별 입력 schema 및 동작이 다를 수 있으므로 실제 연결된 서버의 스키마를 우선합니다. 자세한 상태·재개 ID 구분은 [상태 가이드](/docs/status-guide/)와 기존 [진행 상태](/docs/progress-detail/), [복구](/docs/recovery-detail/)를 함께 참고하세요.

## 판본 정보를 남길 때

오류를 공유할 때는 민감정보를 지우고 다음을 함께 적으면 어느 계층인지 구분하기 쉽습니다.

1. 소스 저장소를 썼다면 remote URL, commit SHA, tag.
2. 독립 CLI를 썼다면 `command -v ouroboros`, `ouroboros --version`, 문제와 관련된 `--help` 일부.
3. 호스트 도구를 썼다면 호스트 종류, 플러그인 이름/표시 판본, 실제 MCP 서버 실행 명령과 연결된 도구 이름·입력 스키마.
4. OS와 Python 환경, 문제를 재현한 명령·입력, 결과의 상태와 ID 종류.

환경 변수, 토큰, 개인 경로, Seed의 비공개 내용은 공유하지 않습니다. 이 안내 작성 시점에 실제 독자의 호스트 설정·설치 경로·인증은 검사하지 않았습니다.
