# 지금 어디까지 진행됐는지 확인

!!! warning "판본과 검증 범위"
    이 문서의 상세 설명과 합성 관찰은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 호스트 플러그인·MCP 서버는 별도 판본입니다. 합성·대역 사례는 표시된 조건에 한정되며 실제 모델, 운영 데이터 또는 전체 호스트를 검증하지 않습니다. 현재 설치의 도움말과 [제품 문서](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/docs)를 대조하고 구판과 동일하게 동작한다고 가정하지 마세요.


## 현재 상황

실행 뒤 ID를 받았거나 작업이 오래 걸려 결과가 궁금한 상태입니다. 실행 출력의 **ID 종류**와 **사용한 실행 경로**를 먼저 찾으세요. 상태 조회는 같은 기록을 읽는 작업입니다. `run`을 다시 시작해 상태를 확인하지 않습니다.

## 빠른 조회 {#quick-status}

시작 응답의 실제 ID 필드와 같은 사용자·host·DB 환경을 확인한 뒤 아래에서 일치하는 행을 고르세요. `exec_...` 같은 handle은 ID 종류를 단정하지 말고, 시작 응답에서 연결된 `job_id`, `session_id`, `execution_id` 또는 `auto_session_id`를 먼저 확인합니다. CLI 명령은 독립 CLI용입니다. 호스트에서는 해당 서버가 실제 제공하는 MCP 도구와 필드명을 사용하세요.

| 실제 반환된 값 | 독립 CLI 조회 | 호스트에서 확인 |
| --- | --- | --- |
| `job_...` | `ouroboros job status JOB_ID` | `ouroboros_job_status` 또는 같은 ID의 `ouroboros_job_wait`; 종결 상태 뒤 `ouroboros_job_result` |
| `auto_...` (`auto_session_id`) | `ouroboros status auto AUTO_SESSION_ID` | 해당 버전에서 제공하는 세션 상태 도구 또는 Auto 시작 응답의 연결 ID |
| `orch_...` 또는 session ID | `ouroboros status run --session-id SESSION_ID` | 실제 session ID를 받는 세션 상태 도구가 있을 때 사용 |
| 실행 ID | `ouroboros status execution EXECUTION_ID --events` | 시작 응답의 실제 실행 ID에 맞는 조회 도구 |
| 실행 집계 ID | `ouroboros status run --execution-id EXECUTION_ID` | 서버가 실제 제공하는 실행 상태 도구 |
| ID를 잃음 | `ouroboros resume --list` 또는 `ouroboros status executions` | 원래 대화의 시작 응답과 host의 실제 세션·작업 목록 |

상태에 따라 다음 행동도 달라집니다.

| 조회된 상태 | 다음 행동 |
| --- | --- |
| `running` 또는 아직 대기 중 | 새 실행을 만들지 말고 같은 ID를 다시 조회하거나 해당 job의 wait를 사용합니다. 대기 시간 종료·변경 없음은 완료가 아닙니다. |
| `completed` | job이면 같은 ID의 result를 읽고, 실제 작업 경로의 파일·수용 기준·검사 및 평가 결과를 확인합니다. `completed`만으로 요구 충족을 단정하지 않습니다. |
| `failed` 또는 `cancelled` | 같은 ID의 결과와 오류를 읽고 작업 공간·파일·외부 효과를 살핍니다. 실패/취소가 변경을 되돌렸다고 가정하지 말고 즉시 다시 실행하지 않습니다. |
| ID 없음, 빈 목록, DB/조회 오류 | ID 필드, host·사용자·DB 경로와 조회 오류를 확인합니다. 이는 작업이 없거나 재시작해도 된다는 증거가 아닙니다. 기록을 보존하고 [복구 순서](/docs/recovery-detail/)를 먼저 봅니다. |

모든 상태 조회가 무기록인 것은 아닙니다. [상태 가이드](/docs/status-guide/)와 아래 저장소 변경 경고를 확인하고, 실제 명령·도구가 맞는지 설치 도움말에서 검토하세요.

!!! warning "조회도 저장소 상태를 바꿀 수 있습니다"
    모든 상태 조회가 파일 시스템상 읽기 전용인 것은 아닙니다. 고정 버전의 `ouroboros job status`와 `job result`는 기본 쓰기 가능한 EventStore를 초기화하며 DB·스키마·로그를 만들 수 있습니다. 또 소유자 프로세스가 죽고 연결된 실행의 살아 있는 보유자가 없다는 등 고아 조건이 확인되면 조회 과정에서 `interrupted` 이벤트를 기록할 수 있습니다. 새 임시 HOME에서 존재하지 않는 job을 조회했을 때 오류와 함께 SQLite DB·WAL/SHM·로그가 생성되는 것을 확인했습니다. 이는 모든 상태 명령이 같은 부작용을 갖는다는 뜻은 아닙니다. 같은 환경·DB·ID를 확인하고 기록의 보존이 중요하면 조회 전에 접근 및 백업 방침을 확인하세요. [`job` CLI](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/job.py), [job 상태 복구 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/job_manager.py).

## 입력

실제 출력의 `job_`·`auto_`·`orch_`·`exec_` ID와 플러그인 또는 CLI 중 사용한 경로가 필요합니다. ID를 잃어버렸다면 호스트에서는 기존 대화의 시작 응답을 찾아 달라고 요청하고, CLI에서는 아래 목록 명령으로 찾습니다. 찾지 못하면 호스트에 해당 버전에서 제공하는 세션·실행 목록을 조회해 달라고 요청하세요. 목록도 없거나 해당 작업을 특정할 수 없으면 추측한 ID로 재개하지 말고 기록과 결과 파일을 보존하세요. 인증 값은 공유하지 마세요.

### 호스트 플러그인에서 조회 {#host-status}

터미널용 `ouroboros`가 없어도 기존 AI 세션에서 조회를 요청할 수 있습니다. 출력에서 실제로 받은 값을 넣어 다음처럼 요청합니다.

```text
이 문서와 원문 출처를 읽고 내 Ouroboros 작업 상태를 조회해 줘.
받은 ID: [실제 ID를 여기에 붙여 넣기]
새 실행이나 재개 없이 현재 상태, 통과한 검증, 남은 실패를 알려 줘.
가용 도구와 실제로 읽은 문서 위치를 근거로 제시해 줘.
```

| 받은 값 | 호스트가 확인할 대상 |
| --- | --- |
| `job_...` | 백그라운드 작업. 해당 버전에 제공되는 `ouroboros_job_status` 또는 `ouroboros_job_wait`로 조회하고 종료 후 `ouroboros_job_result`로 결과 확인 |
| `orch_...`·세션 ID | 실행 세션. 제공되는 `ouroboros_session_status` 또는 `ouroboros_ac_tree_hud`로 조회 |
| `auto_...`만 있음 | 자동 실행 시작 응답에서 연결된 `job_id`를 먼저 찾기. 인터뷰/Seed 인계 완료와 제품 완성을 구분하기 |
| `exec_...`만 있음 | 시작 응답이나 이전 대화에서 연결된 세션·job ID를 찾기. 독립 CLI가 있다면 아래 실행 ID 조회도 가능 |

도구가 없는 버전이면 같은 이름의 도구가 있다고 추측하지 말고 설치된 버전의 도움말로 돌아갑니다. `resume --list`는 일반 snapshot 경로에서 최근 진행 중 세션을 기본 최대 20개 표시하며 백그라운드 job 목록과 같지 않습니다. 호환 전체 replay 경로는 이 제한과 정렬을 적용하지 않습니다. 더 오래된 진행 중 세션을 찾으려면 `ouroboros resume --all --list`를 확인합니다. 종결된 세션은 이 목록에 포함되지 않습니다. [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/resume.py).

### 독립 CLI에서 조회 {#cli-status}

아래 명령은 [독립 CLI를 설치한 경우](/docs/first-run-detail/#install-check)에 사용합니다. 표의 대문자와 예시 경로는 실제 값으로 바꿉니다.

| 갖고 있는 값 | 확인 명령 | 읽을 것 |
| --- | --- | --- |
| `job_...` | `ouroboros job status JOB_ID`, 종료 후 `ouroboros job result JOB_ID` | 작업 상태와 결과; 살아 있는 소유 프로세스 및 저장소 설정을 확인 |
| `auto_...` | `ouroboros status auto AUTO_SESSION_ID` | 자동 인터뷰·Seed·실행 인계 상태 |
| `orch_...` 또는 실행 세션 ID | `ouroboros status run --session-id SESSION_ID` | Run/Stage/Step 투영과 각 단계 상태 |
| 실행 집계 ID | `ouroboros status run --execution-id EXECUTION_ID` | 해당 실행의 단계별 상태 |
| 실행 ID | `ouroboros status execution EXECUTION_ID` | 실행 상세 정보; 필요하면 `--events` 추가 |
| ID를 잃어버림 | `ouroboros resume --list` 또는 `ouroboros status executions` | 세션 목록 또는 최근 실행에서 ID 찾기 |
| 프로젝트 전체 | `ouroboros status project /path/to/project` | 관련 실행의 프로젝트 기록 |

`ouroboros status executions`는 영속된 루트 실행 이력을 기본 10개 보여 줍니다. `--limit N`은 양의 정수이며 `--all`은 표시 개수 제한을 해제하지만, `--all`과 함께 잘못된 `--limit`을 지정해도 먼저 오류와 종료 64가 납니다. 재개 세션을 연결된 실행 ID로 묶고 선택된 lifecycle 이벤트의 시각·ID 역순으로 정렬한 뒤 제한을 적용합니다. 세션 내부의 완료·실패·취소는 뒤늦은 진행 이벤트로 덮지 않지만 서로 다른 세션 사이의 선택은 시각·ID를 따릅니다. 이는 저장된 기록의 투영이지 프로세스가 지금 살아 있다는 증거가 아닙니다. 설정된 DB를 읽기 전용으로 열 수 없거나 스키마 조회가 실패하면 종료 1이므로 이 오류를 실행 이력이 없다는 뜻으로 바꾸지 않습니다. 고정 소스 및 기존 대역 테스트 18개가 격리 HOME에서 통과했으며(31개 미선택), 실제 운영 DB·프로세스 및 OS 네트워크 격리는 시험하지 않았습니다. [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py). 합성 실행 12개를 넣은 격리 SQLite의 실제 `status executions` CLI에서는 기본 10개, `--all` 12개, `--all --limit 0` 종료 64를 확인했다. 운영 중 세션과 OS 네트워크 격리는 시험하지 않았다.

`ouroboros status execution EXECUTION_ID`의 고정 구현은 실행 ID, 가장 최근 lifecycle 상태·이벤트 유형·시각을 표시합니다. 도움말의 metadata·progress 표현만으로 Seed, 산출물, 상세 단계나 실시간 프로세스 정보를 제공한다고 가정하지 않습니다. `--events`는 관련 이벤트의 시각·유형·상태를 시간 및 ID 순으로 표시하는 요약 표이며 payload 전체가 아닙니다. 이벤트 조회는 설정된 EventStore를 읽기 전용으로 열고 관련 세션이 있으면 그 세션 이벤트를 합쳐 ID로 중복 제거합니다. 연결 세션이 없으면 execution 집계 이벤트를 조회합니다. 기록된 lifecycle이 없으면 종료 2, DB를 열거나 조회하지 못하면 종료 1입니다. 이벤트 시각이 부정확하거나 동시 변경이 있으면 표를 외부 효과의 완전한 감사 기록으로 취급하지 않습니다. [고정 명령 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py)을 대조하고, 격리된 합성 SQLite의 시작·종료 이벤트 두 개로 실제 CLI를 확인했습니다. 상세와 `--events`는 종료 0으로 위 필드와 요약을 표시했고 합성 payload 표식은 출력하지 않았으며 없는 ID는 종료 2였습니다. 사용자 DB·실행 중인 세션과 OS 수준 네트워크 격리는 시험하지 않았습니다.

`status run`은 `--session-id`·`--execution-id`·위치 인수 중 하나가 필요합니다. 조회 오류가 나면 종료 코드뿐 아니라 저장소 경로와 오류를 함께 확인합니다. 고정 소스의 격리 임시 HOME 시험에서는 이벤트 DB를 열 수 없는 상태에서 세션 조회가 종료 1로 실패했고, 별도로 빈 DB·스키마를 준비한 뒤 존재하지 않는 세션을 조회하면 `No events found`와 종료 2가 나왔습니다. 선택자를 생략하면 종료 64였고, 서로 맞지 않는 세션과 실행 ID를 함께 지정한 시험은 종료 1이었습니다. DB 오류를 세션이 없다는 증거로 해석하지 마세요. [상태 명령 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py).

??? info "격리 합성 시험의 세부 관찰과 한계"

    별도 합성 Seed와 mock 런타임의 한 사례에서는 실제 `OrchestratorRunner` 실행 후 임시 SQLite 세션을 재구성하고, 별도 CLI 프로세스의 `status execution ... --events`에서 `complete`와 `execution.terminal` 표시를 관찰했습니다. 해당 Seed는 검증 가능한 기준 명령이 없어 경고가 발생했으므로 이 표시는 수용 기준 충족의 증거가 아닙니다. 실제 CLI 작업 시작·모델·재시작 복구는 시험하지 않았습니다.

    두 기준의 합성 runner 사례에서는 `exit 0`과 `exit 3` 검증 명령을 사용해 각각 기준 `completed`와 `failed`, 전체 세션 `failed`를 기록했습니다. 별도 상태 CLI의 종료 0은 조회 성공이며 실행 성공이 아닙니다. 이는 mock worker와 임시 저장소의 사례로 실제 모델·CLI 시작·재시작을 검증하지 않습니다.

    **기준 개수와 실행 경로를 확인하세요.** 고정 runner의 mock 시험에서 특별 경로 조건이 없는 `parallel=True` 단일 기준은 실패 명령의 표식 파일이 만들어지지 않았는데도 `success=True`·`completed`였습니다. 같은 실패 명령을 포함한 두 기준 사례에서는 표식이 만들어지고 `failed`였습니다. 고정 소스는 이 조건의 한 기준을 whole-seed 경로로, 두 기준을 기준별 executor 경로로 분기합니다. fat harness·순차 레벨 강제·investment metadata·acceptance authority와 `parallel` 값 등에 따라 경로는 달라집니다. 고정 독립 CLI의 새 실행은 기본적으로 fat-harness를 켜며 명시적 `orchestrator.execution_mode: legacy`는 이를 끕니다. 같은 단일 실패 명령을 넣은 합성 `CliRunner` 시험에서 기본은 표식이 생기고 종료 1이었으며, legacy는 표식 없이 종료 0이었습니다. 런타임 생성과 preflight는 대역이며 실제 모델·터미널 CLI·재개는 미시험입니다. 모든 단일 기준이나 호스트에서 검증이 생략된다고 일반화하지 말고, **명령이 실제 실행됐는지와 결과**를 별도 증거로 확인하세요.

    별도의 비-Git 임시 프로젝트 시험에서는 설치된 CLI entrypoint를 별도 프로세스로 시작하고 `sitecustomize`로 런타임 생성·preflight만 대역 처리했다. 합성 실패 검증 명령의 실행 표식과 CLI 종료 1을 확인한 뒤 다른 CLI 프로세스로 상태를 조회해 종료 0 및 `failed`·`execution.terminal`을 확인했다. 실제 모델·Git worktree 성공·재시작·자동 후속은 시험하지 않았다.

    이 시험은 합성 ID와 임시 DB에 한정하며 실제 실행이나 모든 오류 조건을 시험하지 않았습니다. 재시험에는 `OUROBOROS_TELEMETRY=0`을 설정했습니다. 최초 빈 DB 경로 시험에서는 해당 opt-out이 빠져 익명 통계 안내가 출력됐으며 실제 외부 전송 여부는 확인하지 못했습니다. OS 수준 네트워크 격리는 사용하지 않았고 사용자 DB나 모델은 사용하지 않았습니다.


### detached 시작 거절의 판본 차이

고정 커밋은 detached worker의 시작 전 거절을 새 launch token과 job 정보로 확인하며 Windows에서는 venv redirector와 자식 PID 차이를 고려합니다. 시험한 공개 `0.59.9` 설치본에는 해당 token 경로가 없고 PID 일치를 요구합니다. 시작 오류의 전달이나 상태를 판본에 따라 확인하고, 이 차이만으로 실제 장애나 보안 영향을 단정하지 않습니다. Windows worker 실행은 시험하지 않았습니다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/detached_jobs.py), [판본 범위](/docs/version-guide/#version-scope).

### 백그라운드 job의 변경 기다리기

`ouroboros job wait JOB_ID --cursor 0 --timeout-seconds 5`는 별도의 새 작업을 시작하지 않고 해당 job의 변경을 짧게 기다립니다. `--timeout-seconds` 기본값은 **0초 변경 대기 없는 조회**이고, 이 판본의 핸들러는 변경 대기 요청을 최대 5초로 제한합니다. 이 숫자는 전체 응답 시간의 상한이 아닙니다. 고정 소스와 동일한 테스트의 합성 느린 job manager는 0초를 받아도 스냅샷 조회에 1.05초를 쓴 후 결과를 반환했습니다. 이는 장기 변경 대기를 요청하지 않는다는 뜻이지 즉시 응답이나 실행 종료를 보장하지 않습니다. 해당 단위 시험은 임시 HOME과 네트워크 namespace에서 통과했으며 실제 job·운영 지연은 시험하지 않았습니다. [고정 테스트](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/tests/unit/mcp/test_job_manager.py). 반환된 상태와 cursor를 확인하고 같은 job의 다음 조회에 cursor를 전달합니다. 타임아웃이나 변경 없음은 성공·종료가 아니므로 종결 상태를 확인하고 `ouroboros job result JOB_ID`로 결과를 읽습니다. 장시간 작업이 자동으로 백그라운드에서 계속된다는 보장도 아닙니다.

| 명령과 옵션 | 기본값 | 사용 시 판단 |
|---|---|---|
| `job wait JOB_ID --cursor N` | `0` | 같은 job의 직전 wait/status cursor를 전달한다. `job events --since` cursor와 혼용하지 않는다. |
| `job wait --timeout-seconds N` | `0`초 | 대기 요청은 최대 5초로 제한된다. 기다림이 끝나도 종결 여부는 별도다. |
| `job wait --view VALUE` | `full` | `summary`, `compact` 중 선택할 수 있다. 출력 축약이 이벤트 전체 보존이나 종료를 뜻하지 않는다. |
| `job wait --stream VALUE` | `progress` | `linked`는 관련 스트림도 조회하며 아래 pagination 경계를 따른다. |
| `job result JOB_ID` | 필수 ID 외 옵션 없음 | 완료된 job의 결과를 읽는다. 핸들러 실패와 비종결 상태를 확인하고 `completed`를 제품 검증 성공으로 단정하지 않는다. |
| `resume --list` / `resume --all` | 둘 다 꺼짐 | `--list`는 선택 프롬프트 없이 표시, `--all`/`-a`는 일반 snapshot 경로의 기본 20개 제한을 해제한다. 호환 전체 replay 경로는 기본 제한을 적용하지 않는다. 실제 재개는 별도다. 상세와 조회 누락은 [복구](/docs/recovery-detail/)를 본다. |

고정 CLI 선언과 관련 핸들러를 대조하고 임시 HOME에서 `job wait --help`, `job result --help`, `resume --help`의 종료 0을 확인했다. 이는 도움말 및 소스 확인이며 실제 실행 중인 job을 기다리거나 운영 세션을 재개한 검증은 아니다.

기본 `--stream progress`는 job·실행 진행을 보고 `--stream linked`는 연결된 세션·lineage·하위 에이전트 이벤트도 포함합니다. linked는 공통 rowid cursor로 연결된 각 스트림을 페이지당 최대 10개씩 살펴보고, 공통 경계까지 수집한 중복 제거 이벤트를 반환합니다. 응답 한 건이 최대 10개 페이지라는 뜻은 아닙니다. 더 남았다는 표시가 있으면 반환 cursor로 이어서 조회합니다(구조화 응답의 `stream_has_more`, 간결 텍스트의 `more=1`). 이 표시는 보수적이어서 스트림에 정확히 10개만 있어도 다음 페이지가 비어 있을 수 있습니다. full 텍스트는 수집된 이벤트 중 마지막 10개만 표시하므로 CLI 텍스트를 구조화 응답의 전체 이벤트와 동일시하지 않습니다. 이 cursor와 아래 `job events`의 `--since`는 서로 다른 조회 계약이므로 임의로 바꿔 쓰지 말고 각 응답의 설명에 따라 사용합니다. CLI는 핸들러의 텍스트를 출력하며 `--wait-for` 옵션은 제공하지 않습니다. MCP `ouroboros_job_wait`는 별도의 `wait_for` 입력으로 phase·terminal 등의 깨우기 조건을 지정할 수 있습니다. CLI와 MCP의 지원 옵션을 설치된 버전에서 확인하고, 조회가 항상 읽기 전용이라고 가정하지 않습니다. [CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/job.py), [대기 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/job_handlers.py), [MCP 입력](/docs/mcp-reference-detail/#ouroboros_job_wait). 이 설명은 고정 소스 대조이며 실제 살아 있는 job의 대기·재개를 시험하지 않았습니다.

`job status`·`job wait`·`job result`의 독립 CLI 래퍼는 기본적으로 핸들러 내부 콘솔 진단을 억제하고 결과 텍스트를 출력한다. 로그가 화면에 없다는 이유만으로 오류나 부작용이 없었다고 판단하지 않는다. `OUROBOROS_JOB_VERBOSE=1`은 콘솔 진단 억제를 해제하는 선택지이며, 오류와 로그에는 경로·작업 정보가 포함될 수 있으므로 공유 전에 검토한다. 이 경계는 `job events`에 일반화하지 않는다. 파일 로깅은 별도로 유지될 수 있으므로 로그 위치·권한과 보존도 확인한다. 이는 [고정 CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/job.py)의 정적 대조이며 실제 호스트별 로깅 설정은 시험하지 않았다.

### Job 이벤트를 페이지로 읽기

`ouroboros job events JOB_ID --since 0 --limit 100 --db-path /path/to/ouroboros.db`는 선택한 SQLite EventStore에서 해당 job의 이벤트를 JSON으로 조회합니다. 경로를 생략하면 설정된 런타임 DB를 선택합니다. 반환 `cursor`는 마지막으로 본 SQLite rowid이며 다음 페이지에서 같은 job과 DB에 `--since`로 전달합니다. 제한된 페이지는 이벤트 timestamp가 아니라 **rowid 순서**로 반환됩니다. 늦게 저장된 과거 시각의 이벤트는 더 뒤에 나올 수 있으므로 목록 순서를 사건 시각순으로 단정하지 말고 각 이벤트의 timestamp도 확인합니다. 반대로 timestamp로 페이지를 재정렬한 뒤 그 순서로 cursor를 만들어서는 안 됩니다. DB를 교체·복원하거나 다른 DB로 바꾼 뒤에는 이전 cursor의 연속성을 가정하지 말고 조회 범위를 다시 확인합니다. 빈 페이지는 입력 cursor를 그대로 돌려주므로, 이후 새 이벤트가 생길 수 있는 작업에서는 같은 cursor로 다시 조회합니다. 기본 제한은 100이며 `--since`는 0 이상, `--limit`은 양수여야 합니다. 이는 지속적인 구독이나 고정 시점의 완전한 스냅샷이 아니며, `count=0`은 job의 성공·완료 또는 존재하지 않음의 증거가 아닙니다. job ID의 종류와 `status`·`result`를 함께 확인합니다.

이 명령은 EventStore를 read-only로 열고 누락 DB·스키마를 생성하지 않지만, CLI 전체의 로깅·환경 초기화까지 부작용이 없다는 보장은 아닙니다. DB가 없으면 오류와 종료 코드 1을 반환하므로 운영 DB를 새로 만들거나 초기화해 해결하지 않습니다. 이벤트 payload에는 작업 내용이 포함될 수 있어 공유 전 검토합니다. 고정 소스와 합성 SQLite 네 행을 이용한 격리 CLI 시험에서 다른 job의 행을 제외하고 두 페이지로 반환했으며 마지막 빈 페이지는 cursor를 유지했습니다. 실제 운영 DB와 동시 삽입은 시험하지 않았습니다. [`job events` 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/job.py), [rowid 페이지 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py).

## 예상

조회는 같은 작업의 단계 상태와 가능한 경우 검증 결과를 돌려줍니다. `job_` 조회가 끝나면 결과를 추가로 읽어야 할 수 있습니다. 기록을 찾지 못했다는 응답은 작업 실패 판정과 다르므로 ID 종류와 조회 대상을 다시 확인하세요.

## 확인

조회 결과의 ID가 처음 받은 ID 또는 연결된 세션·실행 ID와 맞는지 대조하세요. 진행 중인지, 종료됐는지, 실패했는지와 실패한 검증이 있는지를 읽고, 종료됐다면 결과 파일에서 Seed의 요구를 확인합니다. 상태가 `completed`여도 실제 기능과 테스트 결과가 맞아야 완료로 판단할 수 있습니다.

## 다음 행동

진행 중이라면 같은 ID를 다시 조회하세요. 종료됐고 요구와 검증이 맞으면 결과를 사용하세요. 실패·정지·연결 끊김이 남으면 ID와 마지막 정상 단계를 가지고 [복구 순서](/docs/recovery-detail/)로 이동하세요.

![TUI 모니터 시연](/docs/assets/ooo-tui-monitor.gif)

지속적인 터미널 관찰에는 `ouroboros monitor`를 사용할 수 있습니다. 기본 Python TUI에는 선택 의존성이 필요하므로 설치가 빠졌다면 `pip install 'ouroboros-ai[tui]'` 또는 `uvx --python '>=3.12' --from 'ouroboros-ai[tui]' ouroboros tui monitor`를 사용합니다. 별도 `--backend slt`는 native 바이너리가 필요할 수 있습니다. 관찰 화면은 결과의 독립 검증을 대신하지 않습니다. 명령 근거는 [CLI 상태 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md)에 있습니다.

### 별도 터미널에서 모니터 열기

`ouroboros tui open --db-path /경로/events.db --cwd /프로젝트`는 가능한 경우 **새 터미널 프로세스에서** Python 모니터를 열도록 요청합니다. 두 옵션을 생략하면 현재 설정의 EventStore 경로와 명령을 실행한 현재 디렉터리를 사용합니다. 이 명령에는 `--backend` 옵션이 없으므로 SLT를 원하면 별도 터미널에서 위의 `tui monitor --backend slt`를 직접 실행하세요. 터미널을 띄우는 것은 실행 재개가 아닙니다.

SSH 또는 headless 환경이거나 지원 터미널을 찾지 못하면 새 창 대신 다른 터미널에서 실행할 명령을 출력하고 정상 종료합니다. 터미널 프로세스 생성에 성공했다는 출력도 모니터가 실제로 열렸거나 DB 연결에 성공했다는 증거가 아닙니다. 생성 직후 프로세스의 출력은 버려지므로 창과 DB 경로를 직접 확인하세요. PATH에서 `ouroboros`를 찾지 못하면 수동 명령에 `uvx`가 들어가며 실행 시 패키지 다운로드가 발생할 수 있습니다. 수동 명령의 경로와 실행 환경을 먼저 확인하세요. 지정한 모니터의 DB 초기화 영향은 아래 안내를 따릅니다. [고정 CLI 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/tui.py).

격리된 임시 HOME에서 합성 SSH 환경과 존재하지 않는 DB 경로를 지정한 실제 CLI는 수동 명령을 출력하고 종료 코드 0을 반환했으며 DB를 만들지 않았습니다. 이는 **headless 분기만** 확인한 결과입니다. 실제 터미널 창 생성과 모니터 연결은 시험하지 않았습니다.

### 대시보드와 키

두 백엔드의 화면 번호는 다릅니다. 아래는 고정 upstream 소스와 [TUI 사용 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/tui-usage.ko.md)의 계약이며 고정 설치본에서 빈 Python 선택 화면의 `q` 종료와 합성 세션 표시 후 Enter·대시보드 문구·`q` 종료를 각각 격리 PTY의 한 사례로 확인했습니다. 화면이 표시한 세션 ID의 정확성·운영 세션·나머지 키와 SLT는 시험하지 않았습니다.

| 키 | 기본 Python Textual | 네이티브 `slt` |
| --- | --- | --- |
| `1` | 대시보드: 단계·AC 트리·선택 노드 | 대시보드 |
| `2` | 실행: 타임라인·단계 출력 | 실행: 단계 출력·이벤트 |
| `3` | 로그 (`l`도 가능) | 계보 (`e`도 가능) |
| `4` | 디버그 (`d`도 가능) | 세션 (`s`도 가능) |
| `s` / `e` | 세션 선택 / 계보 | 세션 / 계보 |
| `l` | 로그 화면 | 실행 화면에서 로그 패널 열기 |
| `q` | TUI 종료 | TUI 종료 |

Textual은 세션 선택 화면에서 시작하고 SLT는 최근 세션을 불러옵니다. `ouroboros tui monitor --backend slt`에는 PATH의 `ouroboros-tui` 바이너리와 대화형 터미널이 필요합니다. 두 백엔드 모두 `--db-path /실제/이벤트.db`로 확인할 저장소를 지정할 수 있으며 생략하면 구성된 EventStore 경로를 해석합니다. 경로를 잘못 지정하면 원하는 작업이 보이지 않을 수 있고, Python 백엔드는 해당 경로의 부모 디렉터리와 이벤트 저장소를 초기화하므로 먼저 올바른 경로와 권한을 확인하세요. 저장 경로의 기존 설치 호환 조건은 [생명주기와 저장](/docs/lifecycle-detail/)을 참고합니다.

`ouroboros tui monitor`는 실행의 **관찰자**이므로 정상적인 실제 실행을 일시정지·재개할 권한이 없습니다. 특히 SLT는 DB를 열 수 없거나 이벤트가 없는 경우 데모 데이터로 대체할 수 있습니다. 이때 `p`/`r`은 데모를 제어할 뿐 사용자의 작업을 제어한 증거가 아닙니다. 상태가 비어 보일 때는 DB와 세션 ID를 대조하고, 실행 제어는 해당 실행 소유 경로와 [복구 안내](/docs/recovery-detail/)를 확인하세요.
