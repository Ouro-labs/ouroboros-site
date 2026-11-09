# MCP 도구 참조

MCP 도구는 호스트 또는 MCP 클라이언트가 서버에 호출합니다. `ooo`는 지원 호스트의 대화 요청이고 `ouroboros`는 독립 터미널 CLI입니다. 아래의 JSON은 **MCP 도구 인자 예시**이며 셸 명령이 아닙니다. 제공되는 도구와 입력 스키마는 서버·런타임·버전에 따라 다르므로 연결된 서버의 도구 목록과 스키마를 우선 확인하세요.

기준 소스는 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)입니다. 전체 도구의 상세 입력은 실제 서버의 도구 발견 결과와 [도구 등록·구현](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools)을 대조합니다. [제품 MCP API 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/api/mcp.md)는 Python API와 일부 도구 계약을 설명하지만 서버의 전체 실시간 스키마를 대체하지 않습니다.

| 목적 | 도구와 입력 | 출력·오류를 읽는 법 | 영향 |
| --- | --- | --- | --- |
| 목표에서 자동 시작 | `ouroboros_start_auto`에 `{"goal": "작업 관리 CLI 만들기"}` | 반환된 job 및 auto session 식별자를 보존하고 이어서 조회. 오류·차단과 최종 실행 결과를 구분 | 인터뷰·모델 호출과 후속 실행이 발생할 수 있음. 대상과 비용을 확인 |
| 백그라운드 상태 | `ouroboros_job_status`에 `{"job_id": "실제 job ID"}` | 같은 job의 상태를 읽고 종료 후 제공되는 `ouroboros_job_result` 확인 | 응답이 지연돼도 중복 실행하지 않음 |
| 세션 상태 | `ouroboros_session_status`에 실제 오케스트레이터 세션 ID 또는 `auto_` 세션 ID | 관련 상태와 오류·연결된 작업을 확인. Interview 세션 ID나 job ID와 혼용하지 않음 | 저장된 상태가 현재 프로세스 생존이나 완료 검증을 증명하지 않음 |
| 설치·연결 진단 | 호스트의 MCP 상태와 오류 확인; 독립 CLI가 있다면 `ouroboros mcp doctor` | 호스트 연결과 별도 CLI 진단을 구분 | 선택적 live probe는 자식 서버를 시작하므로 실행 전 영향 확인 |

예시 ID와 목표는 실제 호출 결과가 아닙니다. 도구 미발견, 스키마 오류 또는 인증 실패가 나면 임의 인자를 추측하지 말고 연결된 서버의 오류와 버전을 확인하세요. `ouroboros_start_auto`의 접수는 Seed 검토·실행·평가 전체의 성공을 뜻하지 않습니다. 자세한 반환과 상태 경계는 [auto 핸들러](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/auto_handler.py), [job 핸들러](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py), [세션 조회](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py)를 참고하세요.

[AI 진단 안내](/docs/ai-troubleshooting/)에는 MCP 실패와 복구 순서가 있습니다. [기존 MCP 색인](/docs/mcp-reference-detail/)과 [스키마 캡처](/docs/mcp-schema-snapshot-detail/)는 이전 고정 소스 `722172ef` 및 특정 환경 기준입니다. 현재 서버의 도구 목록이나 전체 호스트의 실사용 검증으로 취급하지 마세요.

직접 `ouroboros_qa` MCP·자동화 호출 전 `pass_threshold`가 유한한 0~1 숫자인지 확인하세요. 고정 main `592c667f`는 이를 검증하지만 release `0.59.9`는 float 변환 후 범위를 검증하지 않고 점수와 비교합니다. 잘못된 threshold로 나온 PASS를 신뢰하지 마세요. [QA 판본과 입력 경계](/docs/qa-detail/) · [main 검증](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/qa.py#L696-L706) · [release 비교](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/qa.py#L820-L827)

**Interview 입력 판본 차이:** 고정 main `592c667f`의 `ouroboros_interview`는 비어 있지 않은 `calibration_input`을 `answer`·재개보다 먼저 처리합니다. release `0.59.9`의 schema와 handler에는 `calibration_input`과 `interview_calibration`이 없으며, 지원하지 않는 인자가 handler까지 전달된 경우 `initial_context` 없이 `session_id`와 해당 calibration 인자만 있으면 재개 분기, `answer`도 있으면 답변 분기로 갈 수 있습니다. 호스트나 schema가 먼저 인자를 거부할 수도 있습니다. release에는 두 인자를 보내지 말고 기존 호스트 대화에서 설명을 요청하세요. 세션 ID와 진행 상태를 보존하고 추가 모델 호출·비용 가능성을 확인하세요. 설치된 서버의 실제 schema와 호스트 동작은 미검증입니다. [main 분기](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py#L2100-L2125) · [main 입력](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/interview_calibration.py#L22-L42) · [release 분기](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/authoring_handlers.py#L2093-L2115)

**시작 수락 미확정:** `detached_job_acceptance_pending` 영수증은 durable job 행의 수락이 확인되지 않은 상태이며 worker가 이미 있을 수 있습니다. 고정 main `592c667f`는 알려진 pending 영수증을 조회할 때 `acceptance_pending` 비종결로 표시할 수 있지만, release `0.59.9`의 `ouroboros_job_result`는 행을 찾지 못하면 `job_handle_not_found`, `lifecycle_status: invalid`, `is_terminal: true`를 반환할 수 있습니다. 이는 작업 종료의 증거가 아닙니다. 후속 not found만으로 중복 실행하지 말고 원래 영수증과 실제 ID, 같은 서버·DB, 소유자 및 진행 중인 작업을 확인하세요. `job_wait`의 not-found 표시는 별도 계약입니다. 실제 호스트 schema·worker 상태는 미검증입니다. [main pending 조회](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/job_read_state.py#L124-L160) · [release result](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/job_handlers.py#L2065-L2083) · [시작 영수증](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/background.py#L295-L310)

## 이벤트 이력 조회 {#query-events}

`ouroboros_query_events`는 연결된 MCP 서버의 이벤트 저장소에서 기록을 조회하는 **도구**입니다. 터미널 명령이 아닙니다. 아래 입력은 설명용이며 `session_id`에는 실제 실행에서 확인한 오케스트레이터 세션 ID를 넣습니다. Interview ID나 job ID를 같은 값으로 가정하지 마세요.

```json
{"session_id": "실제 세션 ID", "limit": 20, "offset": 0}
```

네 입력은 모두 선택 사항입니다. `session_id`(문자열)가 있으면 그 세션과 연결된 실행 범위의 이벤트를 조회합니다. 생략하거나 빈 문자열이면 전체 세션의 이벤트를 조회하므로, 다른 작업의 기록도 응답에 포함될 수 있습니다. `event_type`(문자열)은 이벤트 유형의 정확한 값으로 필터링하며 생략하거나 빈 문자열이면 전체 유형입니다. 두 필터가 모두 생략되거나 빈 문자열이면 모든 세션의 모든 유형을 조회하므로 호출 전에 범위를 확인하세요. `limit`(정수)은 최대 반환 개수로 기본값 `50`, `offset`(정수)은 건너뛸 개수로 기본값 `0`입니다. 더 많은 기록을 확인할 때는 같은 필터로 offset을 조정하세요. 서버가 제공하는 실제 스키마와 오류를 우선 확인합니다.

응답은 사람이 읽는 텍스트로 이벤트 유형, ID, 시각, aggregate 유형·ID와 데이터 일부를 표시합니다. 데이터 문자열이 100자를 넘으면 앞부분만 표시하므로 전체 데이터라고 가정하지 마세요. 반환 metadata의 `total_events`는 **이번 응답에 들어온 개수**이며 전체 일치 건수가 아닙니다. 결과가 없으면 일치하는 이벤트가 없다는 문구가 나오고, 조회 실패는 도구 오류로 반환됩니다. 오류나 빈 결과만으로 작업의 성공·완료 또는 기록 전체의 부재를 단정하지 마세요.

이 도구는 작업 실행이나 모델 호출을 요청하지 않지만, 기본 핸들러는 읽기 전용 연결을 지정하지 않고 이벤트 저장소를 초기화합니다. 설정된 저장소의 디렉터리·DB·스키마가 생성되거나 SQLite 보조 파일과 로그가 생길 수 있으므로 무변경 조회로 가정하지 마세요. 기록의 데이터와 세션 ID가 응답이나 로그에 노출될 수 있으니 공유 전에 민감 정보를 확인하세요. 주입된 저장소와 호스트 설정에 따라 실제 영향은 다를 수 있습니다.

이 계약은 고정 main `592c667f`와 release `0.59.9`의 대응 핸들러·저장소 소스가 동일한 정적 비교 범위입니다. 설치된 서버에서 도구 노출이나 실제 DB·호스트 동작은 검증하지 않았습니다. [main 도구 정의·핸들러](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py#L414-L532) · [release 도구 정의·핸들러](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/query_handlers.py#L414-L532) · [저장소 조회](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/persistence/event_store.py#L2142-L2188) · [저장소 초기화](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/persistence/event_store.py#L692-L737)
