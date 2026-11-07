# 실행 상태와 ID를 안전하게 확인하기

상태 화면은 작업 기록을 읽는 출발점입니다. **조회 성공은 실행 성공이 아니고, 조회 결과가 없다는 사실도 작업이 없거나 안전하게 다시 시작해도 된다는 증거가 아닙니다.** 먼저 시작 도구가 반환한 원래 ID와 해당 실행을 시작한 인터페이스(CLI 또는 호스트)를 확인합니다.

## ID 종류부터 맞추기

| ID 모양/출처 | 가리키는 것 | 기본 조회 |
| --- | --- | --- |
| `job_…` — 백그라운드 시작 도구의 반환값 | 완료와 결과를 기다리는 job | 호스트 MCP `ouroboros_job_status` / `ouroboros_job_wait`; 종료 후 `ouroboros_job_result`. CLI라면 `ouroboros job status`, `wait`, `result` |
| MCP `ouroboros_interview`가 반환한 `session_id` | 저장된 Interview 기록(`state.interview_id`); 오케스트레이터 실행 세션이 아님 | 같은 host에서 실제 `ouroboros_interview` 도구와 schema를 확인하고, 같은 ID와 실제 답으로 인터뷰 이어가기; 상태 조회 명령에 넣지 않음 |
| `orch_…` — 오케스트레이터 실행 세션 ID | Seed 실행 세션 | `ouroboros status run --session-id SESSION_ID`; MCP `ouroboros_session_status`가 있으면 실제 execution session ID |
| execution/run ID — 실행 시작 응답이나 목록의 execution ID | Run/Stage/Step 기록 및 실행 이벤트 | `ouroboros status execution EXECUTION_ID --events`; 단계 projection은 `ouroboros status run EXECUTION_ID` |
| `auto_…` — Auto 시작 응답의 `auto_session_id` | Auto 인터뷰·handoff·후속 단계 상태 | `ouroboros status auto AUTO_SESSION_ID`; 호스트 세션 상태 조회도 실제 auto ID를 받을 수 있음 |
| `exec_…` 또는 다른 execution handle | 시작 도구가 제공한 특정 실행 handle일 수 있음 | 시작 응답에서 연결된 실제 `session_id`, `execution_id`, `job_id` 필드를 확인한 뒤 그 ID에 맞는 조회 선택 |

같은 `session_id`라는 필드명도 어느 도구가 반환했는지 구별하세요. MCP `ouroboros_interview`의 `session_id`는 Interview state ID이며 `ouroboros status run --session-id`와 `ouroboros_session_status`는 오케스트레이터 실행 세션을 조회합니다. Interview를 이어가려면 현재 연결 서버의 실제 도구 목록과 입력 schema에서 `ouroboros_interview`를 확인한 뒤, 같은 host 도구에 반환된 `session_id`와 현재 질문에 대한 실제 답을 전달합니다. 이는 상태를 읽는 조회가 아니라 인터뷰를 계속하는 호출이며 모델 요청·시간·provider 비용이 발생할 수 있습니다. OpenCode 위임에서는 접수 영수증이 아닌 자식 응답에 실제 ID와 질문이 있는지 확인하고, schema가 요구하면 실제 질문 텍스트도 전달하세요.

독립 CLI 인터뷰라면 기존 state directory를 사용해 `ouroboros init list`로 인터뷰 ID를 확인하고, 이어가기로 결정한 경우에만 `ouroboros init start --resume INTERVIEW_ID`를 실행합니다. 처음부터 사용자 지정 `--state-dir`을 썼다면 두 명령 모두 같은 기존 디렉터리를 전달하세요: `ouroboros init list --state-dir STATE_DIR`, `ouroboros init start --resume INTERVIEW_ID --state-dir STATE_DIR`. 이 명령은 조회 전용이 아닙니다. 인터뷰를 이어가고 모델을 호출해 상태를 저장하거나 Seed를 만들 수 있으며, 완료 뒤 `Start workflow now?` 확인은 기본 `yes`입니다. Seed 파일과 수용 기준을 검토하기 전에는 이 질문에 `n`으로 답해 workflow가 시작되지 않게 하세요. `ouroboros resume --list`는 오케스트레이터의 진행 중 실행 세션 목록이지 Interview 목록이 아닙니다. ID가 없으면 원래 응답과 알려진 기존 저장 상태를 확인하고, 찾지 못했다고 새 인터뷰를 시작하거나 ID를 추측하지 마세요. 이 구분은 고정 main `592c667f`와 release `v0.59.9`의 [Interview MCP handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py) · [release handler](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/authoring_handlers.py), [CLI init 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py) · [release init 구현](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/init.py)을 대조했습니다. 설치된 host/MCP 서버가 같은 판본이거나 해당 도구를 제공한다고 보장하지 않습니다.

ID 접두사는 힌트일 뿐입니다. 값이 반환된 JSON 필드명과 도구 설명이 최종 기준입니다. ID를 임의로 만들거나 job ID를 session ID 칸에 넣지 마세요. 실행 시작 응답에 `job_id: null` 또는 호스트 위임(`delegated_to_plugin`)이 있으면 job 조회 도구가 결과를 찾지 못할 수 있습니다. 이 경우 job ID를 추측하지 말고 같은 호스트의 자식 세션/작업 화면과 handoff 응답을 확인합니다. Auto의 인터뷰·Seed 작성·실행 handoff 완료 표시는 제품 작업의 성공이나 QA 승인과 같지 않습니다. [Auto 흐름과 handoff 경계](/docs/auto-detail/)

## 독립 CLI에서 찾아보기

먼저 정확한 프로젝트·사용자 환경에서 실행합니다. 잘못된 현재 디렉터리나 다른 Python 설치의 결과는 대상 실행과 다를 수 있습니다.

```sh
# 특정 실행의 상태와 이벤트 요약
ouroboros status execution EXECUTION_ID --events

# 최근 실행 ID (기본 최근 10개); 모두 보려면 --all
ouroboros status executions
ouroboros status executions --all

# 실제 세션 ID를 기준으로 Run/Stage/Step 투영
ouroboros status run --session-id SESSION_ID

# 끊긴 호스트에서 진행 중 세션 목록 (기본 최근 20개, 선택/재개 없음)
ouroboros resume --list
ouroboros resume --all --list

# 프로젝트별 완료 run 조회, 경로 생략 시 현재 디렉터리
ouroboros status project /path/to/project
```

`status execution`은 최근 lifecycle 상태·이벤트 유형·시각을 보여 주며 `--events`도 실행 이벤트 payload 전체가 아닙니다. `status run`은 기록 이벤트의 Run/Stage/Step projection입니다. `status executions`는 최근 10개가 기본이며 목록 제한을 넘는 기록은 `--all`을 사용합니다. `resume --list`는 **진행 중 세션** 목록이고, 종료된 실행이나 모든 job 기록 목록이 아닙니다. 기본 20개 제한 및 재구성 실패로 누락될 수 있으므로 목록에 없다는 이유만으로 실행을 다시 시작하지 마세요. `status project`는 지정한 프로젝트 경로를 대상으로 하므로 경로를 확인합니다. 상세 CLI와 ID별 차이는 [CLI 색인](/docs/cli-reference-detail/) 및 [진행 상태 설명](/docs/progress-detail/)을 참고하세요.

`ouroboros resume --list`는 source 구현에서 기존 EventStore를 SQLite 읽기 전용으로 엽니다. DB가 없으면 “진행 중 세션 없음”을 표시하며 DB를 만들지 않는 경로입니다. 반면 다른 status 조회는 모두 이런 부작용 없는 계약이라고 일반화하지 마세요. job status/result 핸들러는 JobManager snapshot과 미확정 시작 영수증 관찰을 수행할 수 있고, Auto 상태는 저장 상태를 읽습니다. 저장소·로그·동시 실행에 대한 영향이 실제 환경에서 모두 없다고 보장할 수 없으므로 기존 DB 경로와 설정을 확인하고, 읽기 전용 보장이 코드에 명시된 `job events`도 대상 DB를 확인한 뒤 사용하세요. `job events`는 **이벤트 저장소 읽기 전용**이지 터미널·파일시스템 전체가 무기록이라는 보장은 아닙니다. [job CLI 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/job.py), [resume 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/resume.py)

MCP 호스트에서는 도구 이름을 서버의 실제 `list_tools`와 대조합니다. 일반적인 대응은 `ouroboros_job_status({"job_id":"실제 job ID"})`, `ouroboros_job_wait`에 같은 `job_id` 및 필요 시 cursor/timeout, 종료 뒤 `ouroboros_job_result`입니다. 인터페이스마다 필드명과 옵션이 다르므로 CLI 플래그를 MCP 인자로 복사하지 말고 현재 연결 서버의 입력 스키마를 따릅니다. `wait`는 설정한 시간 동안 변화나 terminal 상태를 기다리는 조회이며, 모델 작업을 시작하거나 실행을 성공으로 바꾸지 않습니다. [MCP job handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py), [CLI job 옵션](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/job.py)

## 결과 읽는 순서

1. **같은 ID로 다시 조회**해 `running`, `paused`, `completed`, `failed`, `cancelled` 등 표시된 lifecycle 상태를 확인합니다. `acceptance_pending`이면 시작 요청의 영속 수락이 확인되지 않았고 워커 상태도 모릅니다. 응답에 `retry_start_allowed: false`가 있으면 중복 시작을 하지 말고 안내된 같은 `job_id`로 다시 조회합니다. 이 표시는 성공·실패의 terminal 결과가 아닙니다. [pending job 상태 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/job_read_state.py)
2. **job이 terminal일 때** 같은 ID의 `job result`를 읽습니다. 아직 terminal이 아니면 결과는 없을 수 있습니다. 완료 상태와 result의 실제 본문·평가를 별도로 확인합니다.
3. **실패·취소·불명확이면** 실행/세션 이벤트, Seed 경로, 작업 branch·파일, 외부 도구가 이미 수행한 효과를 살펴봅니다. failure 표시만으로 외부 변경이 모두 되돌아갔다고 가정하지 않습니다.
4. **ID가 없으면** 우선 올바른 사용자/DB와 호스트 연결인지, 원래 start 응답이 어느 필드로 ID를 줬는지 확인합니다. `status executions`, `resume --list`, Auto 상태는 서로 다른 기록 범위를 보므로 한 목록의 빈 결과로 다른 기록도 없다고 결론 내리지 마세요. 조회 오류도 “없음”과 구분합니다.

예를 들어 `ouroboros_job_wait`가 `running`을 반환하면 동일 job을 계속 관찰합니다. `completed`면 같은 job의 result를 확인합니다. `failed`면 오류 원인과 남은 파일·외부 효과를 검토하고, 재시도는 이전 작업이 여전히 실행 중이지 않으며 반복 효과를 안전하게 처리할 수 있음을 확인한 뒤 별도 판단합니다. 이 예시는 사용 절차이며 실제 결과를 나타내는 샘플 출력이 아닙니다.

## 재개와 취소는 별도 결정

목록 또는 상태 응답이 보여 주는 재개 안내를 그대로 실행하지 마세요. `resume --list`는 ID를 찾는 조회이고, interactive `ouroboros resume`는 선택 뒤 재접속 명령을 안내할 수 있지만 기존 작업 문맥이나 실행 권한의 복구를 보장하지 않습니다. 실제 재개는 같은 세션에 붙거나 새 시도를 만드는 등 작업 상태를 바꿀 수 있고, checkout/worktree를 복원하며 새 branch·파일을 만들 수도 있습니다. Seed 파일 경로가 기록된 Seed ID와 같다고 가정하지 말고 원래 YAML, 세션 ID, 작업 경로와 branch를 먼저 맞춰 봅니다. [복구 절차](/docs/recovery-detail/)

취소도 상태 조회와 다릅니다. `ouroboros_cancel_job` 또는 취소 CLI는 실제 작업에 취소를 요청하거나 상태 이벤트를 기록할 수 있습니다. 요청 접수는 워커 종료나 이미 실행된 외부 효과의 되돌림을 보장하지 않습니다. 이 가이드는 취소나 재개를 실행하라고 허가하지 않습니다. 사용자가 명시적으로 그 작업을 요청했을 때만 대상 ID·영향·남은 프로세스를 확인한 뒤 실행하고, 완료 후 같은 ID를 다시 조회해 결과를 확인합니다. [MCP 취소 handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py)

## 근거와 확인 범위

이 문서는 upstream 공개 main commit [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [status CLI](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/status.py), [resume CLI](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/resume.py), [job CLI](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/job.py), [job MCP handlers](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py), [session status handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py)와 기존 progress/recovery 설명을 정적으로 대조했습니다. 이 문서 작성 중 실제 사용자의 CLI·MCP 서버·DB·job·session을 조회하지 않았고, 모델이나 실행을 시작하지 않았습니다. 실제 호스트별 도구 스키마·설정, 살아 있는 작업의 조회 부작용·복구, release `0.59.9`와 main 사이의 재개 호환성은 검증하지 않았습니다. 따라서 설치된 서버의 도움말·도구 스키마와 보존된 실행 기록을 우선 확인하세요. [판본 확인 가이드](/docs/version-guide/)
