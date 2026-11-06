# CLI 명령 참조

독립 터미널의 `ouroboros` 명령을 찾는 입구입니다. 호스트 대화의 `ooo` 스킬과 별도이며, 한쪽의 설치·버전이 다른 쪽의 MCP 서버를 증명하지 않습니다. 아래 설명은 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)을 기준으로 소스를 대조했습니다. 공개 배포판과 설치 버전은 다를 수 있으므로 `ouroboros --version`, `ouroboros --help`, **해당 하위 명령의** `--help`를 먼저 확인하세요.

모든 옵션의 상세와 예외는 [고정 제품 CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md)와 [CLI 등록 코드](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/main.py)에서 찾습니다. 이 페이지는 전체 옵션을 전수 설명하거나 모든 명령을 실행 검증한 목록이 아닙니다.

| 목적 | 명령·입력 | 출력과 다음 행동 | 영향·실패 시 |
| --- | --- | --- | --- |
| 준비 상태 확인 | `ouroboros status health` | 설정·DB·런타임·자격증명 관련 행을 확인 | `ok`는 실제 인증이나 모델 호출 성공이 아님. 오류 행과 설치 환경을 확인 |
| 첫 목표 정리 | `ouroboros init start "작업 관리 CLI 만들기"` | 대화형 인터뷰와 Seed 생성 여부를 확인 | 모델 호출과 로컬 파일 생성이 가능. 실행 시작 질문의 답을 확인하고, 실행 전 Seed를 읽으려면 거절 |
| 기존 Seed 실행 | `ouroboros run /실제/seed.yaml` | 실제 반환된 ID와 대상 프로젝트를 기록 | 작업 파일·외부 도구 및 비용에 영향. 예시 경로가 아닌 실제 파일과 작업 폴더를 확인 |
| 진행 조회 | `ouroboros job status JOB_ID`, `ouroboros status execution EXECUTION_ID --events` | 해당 ID의 상태·결과를 확인 | 조회 성공은 작업 성공이 아님. ID 종류를 혼용하지 않음 |
| 목록·복구 | `ouroboros resume --list` | 재개 후보 목록을 읽음 | 목록 조회는 재개가 아님. 목록이 비어도 이력이 없다고 단정하지 않음 |
| MCP 설치 진단 | `ouroboros mcp doctor` | 각 검사 행과 실패를 확인 | 기본은 서버를 시작하지 않지만 전체 명령의 네트워크 부재나 OS 격리를 보장하지 않음 |

`JOB_ID` 등은 설명용 자리표시자입니다. `ouroboros job result JOB_ID`는 종료된 job 결과를 읽을 때 사용합니다. 오류가 DB 접근 실패인지 없는 ID인지 구분하고, 중단 후 새 실행을 만들기 전에 기존 소유자·작업 폴더·외부 효과를 확인하세요. `run workflow --resume`은 특정 복구 실패 시 기존 세션 실패를 기록하고 새 시도를 시작할 수 있습니다. [제품 run 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py).

[상태와 복구](/docs/progress-detail/), [AI 진단 안내](/docs/ai-troubleshooting/)에서 증상별 순서를 볼 수 있습니다. [기존 CLI 색인](/docs/cli-reference-detail/)은 별도 고정 판본 `722172ef` 기반이므로 현재 제품이나 설치판과 동일하다고 가정하지 마세요. 예시는 사용법 설명이며 실제 모델 작업의 출력이 아닙니다.
