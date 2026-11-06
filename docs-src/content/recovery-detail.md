# 멈춤과 실패를 기록에서 복구하기 {#_1}

!!! warning "판본과 검증 범위"
    이 문서의 상세 동작과 합성 관찰은 별도 언급이 없는 한 고정 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 사용 중인 플러그인과 MCP 서버는 각각 다른 판본일 수 있습니다. 아래의 ID별 독립 CLI 조회 구문(job status/result, status run/execution/auto)은 고정 722와 main 592의 CLI 구현을 대조했습니다. 여기에 기록된 시험은 해당 조건의 관찰이며 실제 사용자 환경·모델·호스트 전체를 검증하지 않았습니다. 실행 전 설치된 버전의 도움말과 [현재 제품 CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [현재 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros)를 대조하세요. 판본 차이를 확인하지 않은 기능은 동일하다고 가정하지 않습니다.


## 가진 ID로 먼저 현재 상태 확인하기 {#first-status-by-id}

시작 응답에서 받은 ID의 **필드명**을 보고 첫 조회를 고릅니다. 아래 CLI 명령은 독립 CLI가 설치된 동일한 사용자·프로젝트 환경에서만 사용하세요. 호스트 플러그인에서는 그 호스트 세션에 실제로 연결된 MCP 도구와 입력 schema를 확인하고 같은 종류의 ID를 전달합니다.

| 시작 응답에 있는 ID | 독립 CLI에서 첫 조회 | 호스트에서 첫 조회 |
| --- | --- | --- |
| `job_id` | `ouroboros job status JOB_ID` | 실제 연결된 `ouroboros_job_status`에 같은 job ID |
| `session_id` | `ouroboros status run --session-id SESSION_ID` | 현재 서버가 제공하는 session status 조회 도구와 실제 입력 schema |
| `execution_id` | `ouroboros status execution EXECUTION_ID --events` | 현재 서버가 제공하는 실행 상태/이벤트 조회 도구와 실제 입력 schema |
| `auto_session_id` | `ouroboros status auto AUTO_SESSION_ID` | 서버에 해당 auto 상태 조회가 있으면 그 실제 도구와 schema |

`job_id`가 아직 terminal 상태가 아니면 같은 job ID로 `ouroboros job wait JOB_ID` 또는 호스트의 `ouroboros_job_wait`를 사용해 다시 확인합니다. terminal 상태를 확인한 뒤에만 같은 ID의 `ouroboros job result JOB_ID` 또는 실제 호스트 result 도구로 결과를 읽습니다. `job_id`, `session_id`, `execution_id`, `auto_session_id`는 서로 다른 레코드이므로 서로 바꿔 넣지 않습니다. `auto_session_id` 조회가 후속 Ralph 상태를 보여 주더라도 실행 job의 상세 결과를 대신하지 않습니다.

조회 결과와 별도로 기록의 소유 프로세스가 실제로 살아 있는지, 작업 경로·branch와 파일 상태, 이미 발생한 외부 효과를 확인하세요. 저장된 `running` 표시만으로 프로세스 생존을 단정하지 않습니다. 새 실행, 취소 또는 재개는 첫 조회가 아니며 이 안내가 이를 자동 승인하지 않습니다. 일부 상태 조회는 DB 초기화·로그·상태 기록에 영향을 줄 수 있으므로 아래의 조회 부작용 경계와 [진행상태·ID 안내](/docs/status-guide/)를 읽고, 설치 버전과 실제 DB 경로를 확인하세요. 존재하지 않는 DB를 만들거나 다른 사용자/프로젝트의 DB를 초기화하지 마세요.

## 현재 상황 {#_2}

인터뷰나 실행이 멈췄거나, 연결이 끊겼거나, 검증이 실패한 상태입니다. 먼저 [진행상태 안내](/docs/progress-detail/)에서 같은 ID의 현재 상태를 읽으세요. 새 실행을 바로 시작하면 어느 작업이 결과를 냈는지 구분하기 어려워집니다.

## 증상별로 먼저 볼 곳 {#_3}

| 현재 보이는 증상 | 먼저 확인할 것 | 이어서 볼 안내 |
| --- | --- | --- |
| 응답이 없거나 연결이 끊겼다 | 받은 ID의 종류와 같은 작업의 기록·소유 프로세스를 확인한다. 응답 유실만으로 종료나 재시작 가능을 단정하지 않는다. | [진행상태와 ID](/docs/progress-detail/), 이 페이지의 호스트·독립 CLI 복구 |
| 완료 표시가 있는데 원하는 기능이나 테스트 결과를 찾지 못한다 | 실제 작업 경로·branch, Seed의 기준과 **실행된** 검사 결과를 확인한다. 작업자 완료와 수용 판정은 별개다. | [기존 프로젝트의 작업 공간](/docs/existing-project-detail/), [평가와 실행 근거](/docs/evaluation-evolution-detail/) |
| 수용 기준(AC)이 실패하거나 재시도 중이다 | 해당 AC·attempt와 오류, 검증 결과 및 작업 공간을 확인한다. 재시도 가능 횟수는 안전이나 성공을 보장하지 않는다. | [AC 실패를 읽는 순서](/docs/ac-recovery-detail/) |
| 파일이나 산출물 본문이 보이지 않는다 | 응답의 실제 경로와 artifact ID를 확인하고 작업 파일·EventStore 기록·artifact 본문 저장소를 구분한다. 삭제나 재실행 전에 기존 결과를 보존한다. | [산출물 조회와 복구 경계](/docs/artifacts-detail/), [이벤트 조회](/docs/query-projections-detail/) |
| 설치·인증·설정에서 막힌다 | 설치 경로와 현재 환경의 실제 오류를 확인한다. 진단 통과가 모델 실행과 모든 설정의 유효성을 보장하지는 않는다. | [설치와 설정 오류](#setup-errors), [진단 명령](/docs/diagnostics-detail/) |

조회 명령도 일부는 저장소·로그를 만들거나 상태 복구 기록을 남길 수 있습니다. 경로와 부작용을 각 안내에서 확인하고, 외부 작업 결과가 불명확하면 중복 실행 전에 실제 대상의 상태를 확인하세요.

### 독립 CLI에서 먼저 상태를 찾는 순서 {#cli}

다음은 **독립 CLI가 설치된 같은 환경**에서 확인하는 경로입니다. 호스트 플러그인만 있다면 [호스트에서 복구](#host-recovery)를 따르세요. 명령의 ID는 실제 출력의 값으로 바꾸고 인증정보는 기록하지 않습니다.

1. 실행 ID가 있으면 `ouroboros status execution EXECUTION_ID --events`로 해당 실행을 확인합니다. 조회의 종료 코드가 0이어도 실행 결과가 성공이라는 뜻은 아닙니다.
2. 실행 ID를 잃었다면 `ouroboros status executions`에서 최근 실행을, `ouroboros resume --list`에서 진행 중 실행 세션을 찾습니다. 이 두 목록은 대상과 ID 종류가 다르고 기본 표시 개수에도 제한이 있습니다. 중단된 **독립 CLI 인터뷰**의 ID는 해당 상태 디렉터리의 `ouroboros init list`에서 찾습니다. 인터뷰 목록은 읽거나 검증할 수 없는 파일을 생략할 수 있으므로 빈 목록만으로 기록이 없다고 단정하지 않습니다. [실행 목록과 ID 구분](/docs/progress-detail/#cli-status), [인터뷰 목록과 상태 디렉터리](/docs/interview-detail/).
3. 기록상 `running`이어도 소유 프로세스가 실제로 살아 있는지 확인합니다. 살아 있거나 외부 효과가 불명확하면 새 작업을 시작하지 않습니다. 별도의 background job이 있다면 [job 상태와 결과](/docs/progress-detail/)를 확인합니다.
4. 일시 중지·실패·종료 여부와 작업공간을 확인한 다음 아래의 [독립 CLI 복구](#independent-cli-recovery)를 읽습니다. 목록 조회는 재개가 아니며, 재개 시 새 시도가 생기거나 기존 파일이 복원되지 않을 수 있습니다.


## 새 실행에서 이미 완료된 기준 표시하기 {#_5}

독립 CLI의 `--skip-completed`는 기존 세션의 재개가 아니라 **새 실행**에 이미 충족한 최상위 수용 기준 번호를 전달하는 선택지다. 먼저 이전 작업이 실제로 종료됐는지와 작업공간·Seed 버전·외부 효과를 확인한다. 기준은 현재 Seed에 쓰인 순서의 **1부터 시작하는 번호**이므로 Seed를 변경했다면 번호를 다시 대조한다. 예를 들어 기준이 최소 세 개인 Seed에서 다음은 1번과 3번을 표시하는 형식이다. 파일 이름과 근거는 예시다.

```yaml
completed_acs:
  - ac: 1
    reason: "기존 작업의 근거를 직접 확인함"
    commit: "검토한_커밋_식별자"
  - 3
```

검토한 파일을 `completed.yaml`로 보존했다면 새 실행에 `ouroboros run workflow --skip-completed completed.yaml seed.yaml`처럼 지정할 수 있다. 이 명령은 실제 작업을 시작할 수 있으며 이 예시 자체가 실행을 승인하거나 파일·커밋 존재를 뜻하지 않는다. 로더는 `completed_acs` 목록 또는 최상위 YAML 목록을 읽고, 범위 밖 번호를 거부한다. `reason`과 `commit`은 기록용 값이며 이 로더가 커밋의 존재나 해당 기준의 충족을 증명하지는 않는다. 매핑에서 `completed_acs` 키가 없거나 오타가 나면 로더는 오류 대신 빈 목록으로 취급하므로 표기를 확인해야 한다. `--no-orchestrator` 자리표시자 경로도 이 옵션을 실제 적용하지 않는다. 이미 있는 세션을 `--resume`으로 재개하면 이 옵션은 무시된다. [고정 CLI 로더 및 실행 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py).

고정 소스의 **기준별 병렬 executor 경로**에서는 선행 기준이 실패·차단되면 표시된 기준도 차단될 수 있다. 선행 조건을 통과한 표시 기준이 성공 계약을 가지고 `execution.run_verify_commands`가 켜져 있다면 게이트를 실행하고 실패 시 그 기준을 보통 작업으로 실행한다. 성공 계약이 없거나 설정이 꺼져 게이트를 거치지 않으면 기존 작업 상태를 충족한 것으로 *가정*한다. 따라서 번호를 파일에 적은 사실이나 `SATISFIED_EXTERNALLY` 결과만으로 해당 기능이 실제로 검증됐다고 해석하지 말고 검증 상태와 증거를 읽는다. 이 설명은 [고정 executor](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/parallel_executor.py)의 정적 대조다. 고정 커밋과 해당 파일이 일치하는 테스트 세 건을 격리 환경에서 실행해 계약 없는 기준의 `verification_status=assumed`, 실패한 `verify_command`의 일반 실행 전환, 산출물 부재 시 실행 및 존재 시 `verification_status=verified` 사례를 확인했다. 이 시험은 작업자 실행을 대역으로 사용하며 모든 실행 경로·실제 작업과 모델 실행은 시험하지 않았다. [검증 게이트와 실행 설정](/docs/seed-format-detail/)도 확인한다.

## 실행 실패 후 이어질 수 있는 자동 평가 {#_6}

독립 CLI의 고정 orchestrator 경로에서 `Execution failed`가 출력되어도 즉시 모든 후속 작업이 멈춘다고 가정하지 않는다. 실행 결과 객체가 있고 자동 평가가 활성화된 경우, 재구성한 세션 상태가 `failed`이며 비어 있지 않은 결과 텍스트와 session ID가 있으면 CLI는 정식 평가를 등록하고 그 결과 및 조건부 Ralph 후속 작업을 기다릴 수 있다. 이 비공백 검사는 의미 있는 산출물을 보장하지 않는다. 결과 본문이 비어도 ID·상태 헤더만으로 조건을 통과할 수 있다. `completed`도 같은 평가 대상이고, `cancelled`·`paused`는 이 자동 평가 대상에서 제외된다. 세션 재구성에 실패하면 실행 성공 플래그와 취소 summary를 이용한 대체 상태 판단이 사용될 수 있다. 평가 등록 실패는 경고로 표시되며 원래 실행 판정은 바꾸지 않는다. 실패한 실행의 CLI는 후속 처리 뒤에도 오류 종료 경로를 따른다. 자동 평가·진화를 원치 않을 때는 실행 전에 `--no-auto-evaluate --no-auto-evolve`를 지정하고 별도의 성공 후 QA는 `--no-qa`와 구분한다. 중단하거나 다시 실행하기 전 세션과 후속 job ID·작업 공간·외부 효과를 확인한다. 이는 [CLI 호출 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [후속 처리](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run_successors.py), [평가 가능 조건](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/run_evaluate_chain.py)의 정적 대조다. 고정 소스의 mock 기반 선택 테스트 6건과 헤더만 있는 합성 결과의 평가 가능 판정도 시험했다. 실제 모델·평가 job·Ralph 연쇄는 실행하지 않았다.

## 사용량 제한으로 일시 중지됐을 때 {#_7}

고정 소스의 제공자 사용량·쿼터 제한 경로는 복구 가능한 제한으로 판별되면 세션을 `paused`로 남기고 재개 시각을 기록할 수 있다. 제공자 응답의 본문·메타데이터에 사용 가능한 대기 시간이 없을 때 기본 대기값은 5시간이며, `OUROBOROS_USAGE_LIMIT_PAUSE_HOURS`가 비어 있지 않으면 이를 우선하고, 아니면 `config.yaml`의 `orchestrator.usage_limit_pause_hours`, 그다음 기본값을 사용한다. 유효한 양의 값이 필요하고 설정 기본 대기시간의 상한은 365일이다. 제공자 응답의 대기 정보와 설정값은 서로 다를 수 있으므로 실제 기록된 이유·시각을 확인한다.

고정 `SessionRepository`의 고아 세션 탐지는 `pause_kind=usage_limit`이고 유효한 `resume_after`가 있거나 `paused_at`과 양의 `pause_seconds`로 시각을 계산할 수 있으면, 그 시각과 staleness threshold를 합한 시점까지 해당 paused 세션을 고아 후보에서 제외한다. 메타데이터가 없거나 유효하지 않으면 이 특례가 적용되지 않으며, 특례가 끝난 뒤에는 heartbeat·마지막 활동 등 다른 조건도 함께 확인한다. 이는 고아 정리 후보 판정의 설명이지 해당 시각에 **자동 재개되거나** 제공자의 한도가 복구된다는 보장은 아니다. 실제 소유 프로세스와 job·외부 효과를 확인하고, 자동 정리 또는 중복 재실행을 가정하지 않는다. [설정 우선순위](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py), [일시 중지 판단](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py), [고아 판정](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/session.py)의 정적 대조이며 실제 사용량 제한·시간 경과·정리는 시험하지 않았다.

## 체크포인트가 없다고 표시될 때 {#_8}

고정 기준별 executor 경로는 checkpoint store가 연결되어 있으면 실행 시작 시에도 `load`를 시도한다. `CheckpointStore.load`는 현재와 이전 세 단계 각각의 오류를 모두 `Checkpoint corruption`으로 출력하므로, `Checkpoint not found at level 0`부터 3까지라면 **각 후보의 `Path.exists()` 검사 결과가 거짓이라는 뜻이지 파일 내용의 손상이 입증된 것은 아니다**. 끊어진 심볼릭 링크도 이 결과가 될 수 있다. 새 임시 Git 작업의 합성 CLI 성공 시험에서도 이 네 줄 뒤에 실행이 이어졌다. 반대로 JSON 파싱·무결성·읽기 오류가 함께 나오면 실제 손상이나 접근 오류일 수 있다. 파일이 있어야 하는 재개 상황에서는 이벤트·작업공간·백업과 각 오류를 보존해 조사하고 단순 새 작업으로 판단하지 않는다. 이 executor의 `load`가 반환한 오류는 유효 체크포인트 복원 분기를 건너뛰며, 예외와 다른 복구 경로는 별도로 처리된다. 자동 복구 성공·안전한 재실행을 뜻하지 않는다. [로드 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/checkpoint.py), [executor 복원 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/parallel_executor.py). 이는 고정 소스 및 빈 임시 HOME의 mock CLI 출력·별도 합성 부재/손상 시험의 대조이며 운영 저장소나 모든 예외는 시험하지 않았다.

고정 소스의 Python `RecoveryManager.recover`를 직접 사용하는 경로에서는 `CheckpointStore.load`가 현재 파일과 이전 세 단계에서 유효한 체크포인트를 찾지 못하면 `No valid checkpoint found` 오류를 반환한다. 여기에는 **파일이 전혀 없는 경우뿐 아니라 존재하는 후보가 모두 손상되었거나 로더가 읽기 오류를 Result 오류로 반환한 경우도 포함**된다. `recover`는 이 메시지를 보고 `ok(None)`과 새 시작 안내로 바꿀 수 있으므로, 그 결과만으로 이전 체크포인트가 없었다거나 데이터가 안전하게 복구됐다고 판단하지 않는다. 해당 저장소를 사용하는지, 설정된 디렉터리의 후보·로그·백업과 이벤트·외부 결과를 먼저 확인한다. 이는 [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/checkpoint.py)의 정적 대조이며 CLI나 모든 재개 경로가 이 메서드를 사용한다는 뜻이 아니다. 파일 존재 확인에서 발생하는 모든 OS 예외가 같은 결과로 변환되는 것은 아니다. 격리된 합성 시험에서 후보가 모두 없는 경우와 잘못된 JSON 네 개가 있는 경우 모두 `ok(None)`이었지만 손상 사례의 표준 출력에는 파싱 오류가 표시됐다. 정상 백업 복원과 실제 사용자 데이터는 시험하지 않았다. [체크포인트 저장 경계](/docs/lifecycle-detail/). 현재 파일이 손상되고 `.1`이 유효한 합성 사례에서는 `load`와 `recover`가 `.1`의 상태를 반환했지만, 이 조회 자체가 현재 파일을 고치거나 외부 작업을 되돌리는 것은 아니다. 다른 손상·동시성·운영 환경은 시험하지 않았다.

## 입력 {#_9}

사용한 경로(호스트 플러그인 또는 독립 CLI), 실제 작업 ID, 마지막 정상 단계, 키·토큰·개인정보를 가린 오류, Seed 경로를 모으세요. 이 정보로 살아 있는 작업과 종료된 시도를 구분합니다.

### 호스트 플러그인에서 복구 {#host-recovery}

플러그인만 설치했다면 아래 터미널 명령을 바로 실행하지 않습니다. 기존 호스트 대화에서 실제 문서를 읽히고 다음처럼 요청합니다.

```text
이 복구 안내와 원문을 읽고 기존 작업부터 확인해 줘.
작업 ID: [실제 받은 ID]
증상: [키·토큰·개인정보를 가린 오류와 마지막 정상 단계]
현재 상태를 조회해 연결만 끊긴 것인지 실행이 종료된 것인지 구분해 줘.
살아 있는 작업은 유지하고, 종료된 경우에는 해당 버전이 지원하는 재개 방법과
기존 시도에 미치는 영향을 설명해 줘. 새 작업을 중복 시작하지 마.
```

`job_` 값은 작업 조회에, 세션 ID는 재개 대상을 확인하는 데 씁니다. 특정 중단을 요청할 때 호스트 `ooo cancel`은 job ID를 `ouroboros_cancel_job`, 세션·실행 ID를 `ouroboros_cancel_execution`에 구분해 전달합니다. `cancel_requested` 또는 `cancellation_requested`는 중단 요청이 전달된 상태이므로 `cancelled` 같은 최종 상태를 다시 확인합니다. [취소 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/cancel/SKILL.md). job ID를 세션 ID 자리에 넣지 않습니다. 별도 CLI에서 취소 시 세션이 다른 살아 있는 프로세스의 소유로 표시되면 CLI가 그 소유자에게서 취소하라고 안내할 수 있습니다. 기록의 취소와 실제 워커 종료는 구분해 확인하세요. 호스트에서는 기존 Seed 경로와 세션 ID를 확인한 뒤 `ooo run [실제 Seed 경로]`와 함께 “세션 [실제 세션 ID]를 재개해 줘”라고 요청합니다. 호스트가 제공하는 실행 도구의 `session_id`에 해당 값을 사용하는지 확인하세요. 지원 여부가 불확실하면 [고정 실행 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/run/SKILL.md)과 설치 버전을 대조합니다.

**판본을 바꾼 뒤 재개할 때:** 고정 커밋의 AC 실행 capsule은 v3을 쓰고 v2도 읽는 경로가 있지만, 시험한 공개 `0.59.9` 설치본은 v2를 사용합니다. 고정 소스의 v2 권한 보존에는 `verify_cwd` 등의 조건이 있으므로 양방향 재개가 자동으로 호환된다고 가정하지 않습니다. 기존 기록과 작업 공간을 보존하고 설치 판본과 실제 재개 조건을 확인하세요. 이 비교는 정적 소스 대조이며 실제 판본 간 재개는 시험하지 않았습니다. [고정 capsule 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/ac_execution_capsule.py), [판본 범위](/docs/version-guide/#version-scope).

### 독립 CLI에서 복구 {#independent-cli-recovery}

다음 명령은 [독립 CLI 설치 경로](/docs/first-run-detail/#install-check)를 사용하는 경우에 해당합니다.

| 관찰 | 다음 행동 | 확인 기준 |
| --- | --- | --- |
| 인터뷰가 중단됨 | `ouroboros init list`로 ID와 상태를 찾는다. 재개 가능한 세션은 `ouroboros init start --resume INTERVIEW_ID`를 검토한다 | 질문이 이어지는지 확인한다. 재개만으로 Seed가 생성된다고 가정하지 않는다 |
| 실행 중 연결이 끊김 | `ouroboros resume --list`로 세션 ID를 찾고 `ouroboros status run --session-id SESSION_ID` | 같은 세션의 단계가 진행 중인지 확인 |
| 일시정지되었거나 비종결 상태인데 소유자가 사라진 것으로 보임 | 기존 Seed·세션·소유자와 작업 위치를 확인한 뒤 재개의 영향을 검토한다. 재개 경로는 `ouroboros run /path/to/seed.yaml --resume SESSION_ID` | 재개가 가능한지, 별도 새 시도가 시작됐는지와 이전 branch를 구별해 확인 |
| `failed`, `cancelled`, `completed`로 종결됨 | 같은 세션을 재개한다고 가정하지 않는다. 결과·작업 branch·외부 효과를 보존하고 새 실행의 필요와 범위를 판단한다 | 고정 구현의 저수준 재개는 이 세 terminal 상태를 거부한다. 새 실행이나 외부 효과 복구 절차는 여기서 검증하지 않았다 |
| 명시적으로 중단해야 함 | 먼저 대상 ID를 확인한 뒤 `ouroboros cancel execution SESSION_ID` | 중단 결과와 남은 작업 파일 확인 |
| 평가에서 테스트가 빠짐 | `.ouroboros/mechanical.toml`의 명령을 점검. 새로 생성하기 전 `ouroboros detect`의 모델 호출·파일 쓰기와 `--force`의 덮어쓰기를 확인 | 실제 테스트 명령이 채택되고 실행됐는지 확인 |

질문 생성 실패 후 재시도를 거절해 `aborted`가 된 인터뷰는 고정 CLI에서 종결 상태로 취급하며 재개와 Seed 확정을 거부한다. 이 경우 기존 상태와 필요한 내용을 보존하고 새 인터뷰를 시작해야 한다. 실패 상태 저장 자체가 실패했다면 CLI가 해당 세션을 재개하지 말라고 안내하므로 오류를 먼저 확인한다. 이 조건은 단순 연결 끊김의 모든 경우를 뜻하지 않는다. [인터뷰 CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py).

`ouroboros cancel execution --list`의 행 수를 서로 다른 세션 수로 해석하지 않는다. 고정 구현은 세션 lifecycle 이벤트마다 현재 상태를 재구성하면서 ID를 중복 제거하지 않아 같은 활성 세션이 여러 행에 표시될 수 있다. 실제 대상은 **session ID**로 구분하고 상태와 소유자를 따로 확인한다. 시작·일시정지 이벤트를 가진 합성 세션 하나의 격리 시험에서 실제 목록에 같은 ID가 두 행으로 표시됐고 종료 0이었다. 이 시험은 취소를 실행하지 않았으며 이벤트 ID·종류만 전후 동일함을 확인했다. 사용자 DB·동시 변경과 모든 이벤트 조합은 미검증이다. [고정 취소 목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/cancel.py), [이벤트 조회](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py).

실제로 취소 요청을 보냈다면 요청 수락 표시 뒤에도 세션 상태가 취소로 바뀌었는지 다시 조회한다. 격리 시험에서 직접 생성한 자식이 소유한 준비 상태 세션에 별도 CLI로 요청했고, 자식이 요청을 소비한 뒤 SQLite의 `cancelled` 상태를 확인했다. 추가 격리 시험에서는 합성 런타임이 메시지를 내는 동안 요청을 소비해 `cancelled`가 됐지만, 첫 메시지 전에 대역 런타임이 대기하면 요청 접수 뒤에도 상태가 `running`으로 남다가 메시지가 재개된 뒤에만 취소됐다. 종료된 하위 프로세스는 대역의 정리 코드가 직접 수거했다. 이는 특정 합성 경로의 관찰이며 실제 모델·외부 도구의 취소나 효과 되돌리기를 보장하지 않는다.

고정 독립 CLI는 재구성된 세션이 Foundation A 프로세스 로컬 권한 계약을 갖지 않아 해당 취소 프로토콜이 `None`을 반환하면, 과거 호환 경로에서 acceptance 종료 계획의 수집을 시도하고, 성공하면 세션의 취소 기록 저장을 시도한다. 수집·쓰기 오류나 동시 terminal 전이가 있을 수 있으므로 결과를 별도로 확인한다. 이 경로는 OS 프로세스를 종료하는 동작이 아니며, 기록이 `cancelled`가 됐다는 사실만으로 남은 외부 도구·효과의 중단을 증명하지 않는다. 계약이 유효한 세션은 소유자의 살아 있는 실행을 신호하거나 다른 소유자·영속 기록 대기 등을 별도 처리하므로 두 경로를 혼동하지 않는다. 이는 [CLI 취소 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/cancel.py)와 [권한 프로토콜](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/execution_authority.py)의 정적 대조이며 실제 과거 사용자 세션·외부 프로세스는 시험하지 않았다.

격리된 고정 source CLI 시험에서 존재하지 않는 세션에 `ouroboros cancel execution`을 호출하면 `Session not found` 오류를 표시하면서도 종료 코드는 0이었다. 종료 코드만으로 취소 성공을 판단하지 말고 출력과 대상 상태를 확인한다. 이는 없는 세션의 관찰이며 모든 취소 상황의 종료 코드를 뜻하지 않는다.

취소 대상만 살펴보려면 `ouroboros cancel execution --list`를 사용할 수 있다. 고정 소스는 실행 이벤트를 재구성해 `running`·`paused`만 표시하고 재구성에 실패한 세션은 건너뛴다. 따라서 빈 목록만으로 살아 있는 작업이 없다고 확정하지 않는다. 이 명령은 취소하지 않지만 EventStore를 초기화한다. 빈 임시 HOME에서 실제 CLI를 실행했을 때 종료 0·`No active executions found`와 함께 `~/.ouroboros/ouroboros.db` 및 로그가 생성됐다. `resume --list`의 DB 부재 처리와 다르며 실제 운영 DB·손상 상태는 시험하지 않았다. 대상 ID와 DB 위치를 먼저 확인하고, 전체 취소가 필요한 명시적 판단 없이 `--all`을 쓰지 않는다. `--all`은 고정 구현에서 별도 확인 질문 없이 전체 비종결 후보에 취소를 시도하며, 일부 실패는 경고로 표시할 수 있으므로 출력과 각 상태를 확인한다. [취소 명령 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/cancel.py).

대화형 `ouroboros cancel execution`에서 세션을 선택한 뒤 취소 확인에 **No**로 답하거나 확인을 중단하면 취소 요청은 진행하지 않는다. 다만 고정 구현은 확인 요청과 응답 또는 중단에 관한 HITL 이벤트를 EventStore에 기록하려 하므로, 화면의 `No executions were modified`를 저장소에 아무 기록도 추가되지 않았다는 뜻으로 해석하지 않는다. 목록에서 번호를 고르기 전에 `q`로 나오면 해당 확인 이벤트 경로에는 들어가지 않지만, EventStore 초기화와 조회는 이미 이뤄졌으므로 전체 과정이 무기록이라고 가정하지 않는다. 이 설명은 [고정 취소 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/cancel.py)의 정적 대조다. 합성 세션의 실제 CLI에서 No를 선택한 한 사례는 HITL 요청·응답 기록과 running 상태를 확인했다. 실제 워커·확인 중단·저장 실패는 시험하지 않았다.

`ouroboros resume`은 세션을 **찾는** 명령이며 그 자체로 실행을 다시 시작하지 않습니다. `resume --list`는 고정 소스의 일반 snapshot 경로에서 기본적으로 최근 활동 순의 진행 중 세션 최대 20개를 표시하므로 찾는 ID가 없다는 사실만으로 해당 세션이 없거나 종결됐다고 판단하지 않습니다. 다만 snapshot helper가 없어 호환성 전체 replay 경로로 전환되면 이 경로는 20개 제한과 최근 활동 정렬을 적용하지 않습니다. 이는 [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/resume.py)의 정적 대조이며 25개 합성 tracker의 함수 수준 시험에서 일반 경로 20개와 호환 경로 25개를 확인했습니다. 실제 오래된 EventStore·CLI 전체는 미시험입니다. 표시 개수 제한을 없애려면 `ouroboros resume --all --list`를 사용합니다. 다만 고정 구현은 후보 세션의 재구성이 실패하면 해당 세션을 목록에서 건너뛰므로 `--all`도 모든 진행 기록을 보여 준다고 보장하지 않습니다. 종료된 세션이나 백그라운드 job의 전체 목록도 아닙니다. 원하는 ID가 없다면 원래 DB 경로와 보존된 이벤트, 조회 오류 및 소유 프로세스를 별도로 확인하고 빈 목록만으로 부재나 안전한 재시작을 단정하지 않습니다. 격리된 합성 EventStore에서 한 세션의 시작 이벤트 유형을 바꿔 이력을 불완전하게 만든 뒤 실제 `resume --all --list`를 실행하자, 정상 세션은 표시됐지만 불완전 세션은 표시되지 않았고 종료 코드는 0이었습니다. 이벤트 행은 조회 전후 같았습니다. 이는 한 합성 이력의 관찰이며 손상된 운영 세션이나 살아 있는 작업을 시험한 결과는 아닙니다. [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/resume.py). 고정 소스의 저수준 재개는 이미 `failed`·`cancelled`·`completed`인 세션을 거부합니다. 비종결 세션에서 재개를 시도하더라도 프로세스 로컬 실행 권한을 복구할 수 없어 `process_local_resume_unavailable`이 반환되면 기존 세션을 실패로 기록할 수 있고, 독립 CLI는 그 특정 오류에서 별도 확인 없이 현재 프로젝트의 새 시도를 시작하는 경로가 있습니다. 이 경로는 이미 실패한 모든 세션의 재개나 검사 패키지 소실에 한정된 일반 복구 보장이 아닙니다. 이전 시도 작업은 작업 branch에 남을 수 있으므로 새 시도의 시작 여부와 각 branch를 확인하고 결과를 비교하세요. [CLI 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [재개 상태 확인](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py).

재개 전에 기록된 **작업 경로와 task branch가 실제로 존재하는지** 확인하고, 사라진 경로를 정리하거나 다시 만들기 전에 가능한 기존 작업을 보존하세요. 고정 소스에서 재개 시 저장된 workspace 경로가 없으면 복원을 시도합니다. Git worktree 목록에 해당 경로가 등록되어 있으면 디스크에 경로가 없어도 재생성 전에 반환할 수 있으므로 복원 성공을 보장하지 않습니다. 먼저 `git worktree list`와 실제 디스크 경로·branch를 함께 확인하세요. 해당 경로가 목록에 없을 때는 기존 branch로 worktree를 만들려 하고, branch도 없으면 저장소의 현재 `HEAD`에서 같은 이름의 branch를 새로 만들 수 있습니다. 다른 worktree가 이미 그 branch를 사용하면 오류가 날 수 있습니다. 이 과정에서 이전 경로에만 있던 미커밋·미추적 파일이 복구된다고 가정하지 마세요. CLI의 `Project directory`, `Task worktree`, `Task branch` 출력과 원래 작업의 상태를 비교하세요. 이는 [workspace 복원 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/worktree.py)과 [CLI 재개 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py)의 정적 대조이며, 격리된 임시 Git 저장소에서 경로와 branch가 모두 없는 상태로 내부 `_ensure_worktree`를 호출했을 때 현재 HEAD에 branch가 생성되고 추적 파일이 나타나는 한 사례를 확인했습니다. 별도 격리 임시 Git 저장소에서는 worktree를 등록한 뒤 자기 임시 디렉터리만 지워 경로가 없고 등록이 남은 상태를 만들었습니다. 내부 `_ensure_worktree`는 정상 반환했지만 등록은 남고 경로는 생성되지 않았습니다. 이는 해당 합성 stale 사례의 확인이며 재개 CLI 전체나 사라진 실제 사용자 worktree의 복구, 모든 Git 오류를 시험한 결과는 아닙니다.

`resume --list`는 EventStore를 SQLite 읽기 전용으로 열며 DB가 없으면 생성하지 않고 목록 없음과 종료 0을 반환한다. 반면 존재하는 DB를 열거나 전체 조회할 수 없으면 오류와 종료 2를 반환한다. SQLite 읽기 전용은 CLI 로깅을 포함한 모든 파일 부작용이 없다는 뜻은 아니다. 고정 소스와 차이가 없는 checkout의 격리 HOME에서 DB 부재는 종료 0·DB 미생성, 합성 비SQLite 파일은 종료 2·원본 바이트 보존을 확인했다. 실제 운영 DB·권한 오류·OS 네트워크 격리는 시험하지 않았다. [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/resume.py).

호스트 스킬을 사용할 수 있다면 `ooo resume-session` 또는 `/ouroboros:resume-session`으로 MCP 연결이 끊긴 뒤의 재접속 안내를 요청할 수 있다. 이 스킬은 `ouroboros resume --list`를 셸에서 실행하고, 선택한 행의 **session ID**와, 값이 있는 경우 **execution ID**와 Seed ID를 구분해 보여 준다. execution ID 또는 Seed ID가 없으면 목록에 `-`로 표시되므로 없는 값을 실제 ID로 사용하지 않는다. 목록에서 더 오래된 항목을 보려면 `ooo resume-session --all`을 요청한다. Execution ID는 `ouroboros status execution EXECUTION_ID --events`의 조회에, session ID는 원래 Seed 파일과 함께 `ouroboros run workflow --orchestrator --resume SESSION_ID SEED.yaml`의 재개 인자에 사용한다. `ouroboros tui monitor`는 관찰 경로이며 실제 실행 재개가 아니다. 위 목록 누락·새 시도 가능성과 [모니터의 EventStore 초기화 경계](/docs/progress-detail/)를 먼저 확인한다. 이 안내는 [고정 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/resume-session/SKILL.md)과 명령 소스를 대조한 것이며, 실제 호스트 연결 해제와 재접속을 시험한 결과는 아니다.


대화형 `ouroboros resume`에서 세션을 선택하면 상태 조회와 재개 명령을 **안내**하지만 명령을 실행하지 않습니다. 고정 구현의 안내문은 기록된 `seed_id`가 있으면 이를 그대로 재개 명령의 Seed 위치에 넣습니다. 이 값이 실제 YAML 파일 경로인지 검증하거나 원래 파일을 찾아 주는 것은 아닙니다. 안내된 값이 ID라면 복사해 실행하지 말고 보존한 원래 Seed 파일의 실제 경로와 세션 ID를 확인해 대체하세요. 기록이 없으면 `<seed.yaml>` 자리표시자를 출력합니다. 안내문은 현재 작업의 실행 권한이나 재개 성공을 보장하지 않습니다. [안내문 생성 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/resume.py). 격리된 합성 세션 하나를 실제 CLI의 PTY에서 선택했을 때 Seed ID가 파일 경로 자리의 인자로 그대로 출력됐고, 선택 전후 이벤트 ID·유형과 세션 상태는 변하지 않았습니다. 실제 사용자 세션이나 모델 재개는 시험하지 않았습니다.

### 설치와 설정 오류 {#setup-errors}

호스트에서 `ooo`를 찾지 못하면 플러그인 설치와 새 세션을 확인합니다. Codex에서는 `ooo` 환영·준비 흐름을, Claude에서는 `ooo setup` 설정 마법사를 사용할 수 있습니다. 준비·설정 과정은 설정이나 선택한 프로젝트 파일을 변경할 수 있으므로 화면에 제시된 내용을 확인합니다. 플러그인만 설치했다면 터미널의 `ouroboros: command not found`는 별도 CLI가 없다는 뜻일 수 있습니다. [설치 경로](/docs/first-run-detail/)를 먼저 구분합니다. 독립 CLI의 `ouroboros status health`가 오류를 내면 구성, DB, 런타임 CLI, 인증 상태 중 어느 항목인지 확인합니다. 독립 CLI를 찾지 못하면 Python 버전(3.12 이상)과 설치 환경을 확인합니다. 인증 값은 출력·문서에 복사하지 않습니다.

**Codex 프로필 형식을 판별할 수 없다는 오류:** `Cannot determine Codex profile format`과 worker profile 등록 실패가 나오면, 같은 환경에서 `command -v codex`와 `codex --help`를 실행해 의도한 CLI가 선택됐는지, 도움말이 정상 종료되고 `--profile` 지원을 표시하는지 확인합니다. 사용하는 Codex 버전과 설정 위치(`HOME` 또는 지정된 `CODEX_HOME`)도 확인하세요. 고정 Ouroboros는 도움말의 특정 형식을 인식해 프로필 방식을 판별하므로, 옵션이 보이기만 하면 반드시 호환된다는 뜻은 아닙니다. 타임아웃·실행 오류·인식하지 못한 형식도 판별 실패로 이어질 수 있습니다. [형식 감지 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/codex/runtime_profile.py).

다시 설정하기 전에 기존 설정과 화면에 표시된 변경 범위를 확인하고 필요한 파일을 보존하세요. 고정 구현은 이 등록 실패에서 조건부로 스냅샷 복원을 시도하지만, 복원 메시지만으로 모든 파일이 반드시 원래 상태라고 판단하지 않습니다. 올바른 호환 CLI와 설정 위치를 확인한 뒤 setup을 재시도하고 결과를 다시 확인합니다. 격리된 합성 시험에서는 가짜 CLI의 인식되지 않는 도움말에서 setup이 실패했고, 인식 가능한 형식으로 바꾼 뒤 재시도는 성공했습니다. 실제 Codex 인증이나 모델 호출은 이 시험의 범위가 아닙니다. [설정의 복원 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup.py).

복구 뒤에도 테스트 실패가 남으면 완료로 취급하지 말고 해당 테스트의 실패 원인을 고칩니다. 명령 동작의 출처는 [CLI 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md)입니다.

## 예상 {#_10}

상태 조회는 기록된 상태를 보여줍니다. `running` 기록만으로 소유 프로세스가 지금 살아 있다고 단정하지 말고 job 상태와 해당 호스트의 프로세스·연결 상태를 함께 확인하세요. 재개 가능한 인터뷰는 질문을 이어갈 수 있지만 완료·Seed 생성 여부는 별도로 확인합니다. 비종결 실행 세션의 `run --resume`은 특정 프로세스 로컬 권한 상실 오류에서 이전 시도와 구분되는 새 시도를 만들 수 있습니다. 이미 종결된 세션의 동일 ID 재개는 거부됩니다. 재개 명령이 성공해도 테스트 통과를 뜻하지 않습니다.

## 확인 {#_11}

재개 전후의 세션 ID와 시도를 대조하고 이전 작업 branch의 파일이 보존됐는지 확인하세요. 복구 후 같은 작업의 상태와 결과 파일을 다시 읽고, 실패했던 테스트가 실제로 실행돼 통과했는지 확인하세요. 연결만 끊겼고 실행 중이었다면 재개하지 않은 같은 ID의 진행 상태를 계속 확인합니다.

## 다음 행동 {#_12}

작업이 살아 있으면 [진행상태 확인](/docs/progress-detail/)으로 돌아갑니다. 종결된 작업은 원인과 기존 결과·외부 효과를 확인하고 새 작업이 필요한지 판단하세요. 일시정지 또는 비종결 세션은 재개의 영향을 확인한 뒤 위 절차를 따르세요. 테스트가 계속 실패하면 프로젝트의 코드·검증 명령을 고치고 다시 결과를 확인합니다. 설치나 인증 문제라면 [첫 실행의 설치 경로](/docs/first-run-detail/#install-check)와 해당 버전의 도움말을 확인하세요.

## 격리 합성 시험의 상세 사례 {#synthetic-test-details}

### 예: 실행은 실패했지만 상태 조회는 성공한 경우 {#_4}

독립 CLI의 한 격리 합성 시험에서 실행 출력은 `Verify gate failed: verify_command exited with status 3`과 `Execution failed`를 표시했고 실행 명령의 종료 코드는 1이었다. 같은 실행의 ID로 다른 프로세스에서 `ouroboros status execution EXECUTION_ID --events`를 조회하자 종료 코드는 0이었지만 상태는 `failed`였고 이벤트 목록에 `execution.terminal`이 있었다. 그 뒤에도 다른 이벤트가 기록될 수 있다. **조회 성공은 실행 성공이 아니다.**

이런 출력을 보면 다음 순서로 확인한다.

1. 새 작업을 시작하지 말고 원래 출력의 실행 ID, 실패한 기준과 검증 명령, 실행 경로 및 종료 상태를 기록한다. ID가 없다면 [ID 찾기](/docs/progress-detail/#cli-status)부터 진행한다.
2. 같은 환경과 저장소를 가리키는지 확인한 후 실제 실행 ID로 상태를 조회한다. 조회 자체가 실패했다면 실행 실패와 혼동하지 말고 DB 경로와 오류를 확인한다.
3. 기록된 작업 공간에서 실패한 검증의 출력과 결과물을 살핀다. 검증 명령을 다시 실행하기 전 파일 변경이나 외부 효과가 있는지 확인한다. 자동 평가·후속 작업이 켜져 있었다면 연결된 job도 확인한다.
4. 원인과 기존 결과를 보존한 뒤 [독립 CLI 복구](#independent-cli-recovery)의 종료 상태별 절차를 따른다. `failed` 세션의 재개를 보장하지 않으며 새 실행은 별도의 결정이다.

이는 2026-11-04에 고정 원본 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)을 사용한 합성 Seed와 가짜 런타임의 한 사례다. 검증 명령은 임시 표식을 쓴 뒤 의도적으로 종료 3을 반환했고 QA·자동 평가·자동 진화는 껐다. 실제 모델·외부 서비스·재개 및 다른 실패 유형은 검증하지 않았으므로 출력과 종료 코드를 일반화하지 않는다.

### 준비된 세션을 대상으로 한 재개 시험 {#prepared-session-retry-test}

임시 Git 저장소의 별도 합성 CLI 시험에서는 준비된 `paused` 세션의 프로세스가 종료된 뒤 `--resume` 호출이 권한 부재 경고와 함께 **새 시도**를 시작했다. 기존 세션과 새 시도의 서로 다른 branch가 출력과 당시 Git 목록에 나타났다. 런타임·preflight는 대역이고 검증 명령은 합성이며 checkpoint 부재 경고와 불충분한 frugality 근거도 있었다. 실제 작업 중 중단·모델·외부 효과·병합은 미시험이다.

별도의 합성 시험에서는 준비 후 `paused`를 기록한 첫 Python 프로세스가 종료된 뒤 두 번째 프로세스가 같은 임시 SQLite에서 저수준 재개를 호출했다. `process_local_resume_unavailable`과 mock 실행 0을 assertion했고, 이어 출력에서 `failed` 상태가 관찰됐다. 이는 실제 작업 중 중단이나 CLI fallback을 시험한 결과가 아니다.

고정 소스 기준 격리 시험에서는 실제 이벤트 저장소에 준비 직후 `running`으로 기록된 세션의 소유 프로세스를 종료하고, 새 Python 프로세스에서 저수준 `OrchestratorRunner.resume_session`을 직접 호출했다. 이 호출은 `process_local_resume_unavailable` 오류를 반환하고 세션을 `failed`로 기록했으며 대역 런타임 호출은 없었다. 이는 **준비 단계의 한 사례**이지 실행 중인 모델이나 CLI·MCP 서버 재시작 전체의 복구 시험이 아니다. 위의 CLI 새 시도 경로와도 구분해야 한다. 프로세스 재시작만으로 작업 문맥이나 외부 효과가 복구된다고 가정하지 않는다.
