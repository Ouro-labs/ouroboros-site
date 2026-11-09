# EventStore 이벤트 계약과 해석

!!! warning "판본과 검증 범위"
    별도 표시가 없으면 이 문서의 계약·관찰은 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 실제 호스트 서버는 별도 판본이며 동등성을 전제하지 않습니다. 합성·대역 시험은 표시된 조건의 관찰로 실제 사용자 DB·모델·모든 호스트를 검증하지 않습니다. 일부 과거 재현 자료는 공개되지 않았으므로 해당 관찰을 독립 재현한 근거로 취급하지 말고 링크된 고정 소스와 설치 버전을 대조하세요. 현재 [제품 문서](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/docs)도 확인합니다.


기준: 2026-11-04, Ouroboros 소스 [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). [원본 이벤트 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/events.md), [`BaseEvent`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/events/base.py) 및 [투영 조회 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/projection_handlers.py)을 대조했다. 이벤트는 관찰된 기록이다. 현재 프로세스가 살아 있거나 외부 행동이 성공했다는 보증이 아니며, 필드 계약이 확인되지 않은 다른 버전·내부 이벤트를 안정된 공개 API로 가정하지 않는다.

## 버전과 저장 형식

`BaseEvent`의 기본 필드는 `id`, `type`, `timestamp`, `aggregate_type`, `aggregate_id`, `data`, 선택적 `consensus_id`, `event_version`이다. 새 객체의 `timestamp` 기본 생성값은 UTC지만 호출자가 전달한 시각을 이 모델이 UTC로 강제 변환한다는 뜻은 아니다. 새 객체의 버전 기본값은 1이다. `to_db_dict()`는 `type`을 행의 `event_type`으로, `data`를 `payload`로 저장하고 `event_version`을 **payload 내부**에 삽입한다. 별도의 이벤트 버전 DB 열이 아니다. 입력 `data`에 같은 이름이 있어도 저장 시 객체의 버전으로 덮인다.

`BaseEvent.from_db_row()`는 딕셔너리 payload에서 버전을 꺼내 별도 속성으로 두고 `data`에서는 그 키를 뺀다. 버전 키가 없거나 정수가 아니면 0으로 취급한다. 0은 원본 문서에서 스키마 고정 전 legacy 행을 뜻하지만, 잘못된 비정수 값도 구현상 0이 되므로 **0만으로 정상적인 오래된 행이라고 확정하지 않는다**. 이 생성자는 미지원 정수 버전을 일반적으로 거부하는 검증기가 아니다. 원본의 호환성 권고는 소비자가 지원 버전을 확인해 모르는 버전을 명시적으로 거부하는 것이다. 타입별 소비자의 실제 검사는 별도로 확인한다. 또한 이 판본의 `to_db_dict()`는 행에 `consensus_id`를 포함하지만 `from_db_row()`는 그 값을 복원 생성자에 전달하지 않아 해당 메서드로 읽은 객체의 `consensus_id`가 `None`이다. 임시 객체 왕복과 격리 SQLite의 실제 `EventStore.append` 뒤 조회로 이를 확인했다. DB 행에는 값이 있었으나 `EventStore.replay`와 `query_events`의 반환 객체에서는 `None`이었다. 합성 이벤트 한 건을 임시 SQLite에 저장하고 고정 stdio MCP 서버에서 `ouroboros://events/{session_id}`를 읽는 시험에서도 DB 행의 `consensus_id`는 보존됐지만 리소스 응답의 해당 필드는 `null`이었다. 이는 한 이벤트와 이 리소스 경로의 관찰이며 실제 사용자 데이터나 다른 전송·모든 소비자를 검증하지 않았다. 재현 코드는 공개되지 않았다. Projection 핸들러가 사용하는 관련 이벤트 조회도 이 복원 메서드를 거치지만, projection 결과가 이 필드에 의해 실제로 달라지는지는 확인하지 않았다. 모든 DB 조회·소비 경로의 결과를 이 시험만으로 일반화하지 않는다.

원본은 **문서화된 버전별 필드**를 해당 버전에서 삭제·이름 변경하지 않으며 필드 추가는 가능하다고 기술한다. 이는 모든 내부 payload나 다른 제품 릴리스의 필드까지 고정한다는 뜻이 아니다. 소비자는 추가 필드와 과거 누락 필드를 고려하고, 필수 입력의 타입·범위를 검사하며 미지원 버전이나 불일치는 오류로 남긴다. `event_version`과 특정 이벤트 payload의 `schema_version`은 서로 다른 버전이다.

저장 전 재귀 sanitizer는 `raw_` 및 일부 subscribed/event payload 이름의 키를 제거한다. 이는 모든 개인정보·비밀을 탐지하거나 로그와 모든 저장 경로에서 제거한다는 보안 보장이 아니다. 이벤트와 조회 결과를 공유하기 전에 실제 내용과 접근 권한을 확인한다.

## 주요 이벤트의 의미

| 이벤트 | 해석과 주의 |
| --- | --- |
| `orchestrator.session.started` | `execution_id`, `seed_id`, 시작 시각을 기록한다. 새 runner의 `project_id`, `project_root`, `workspace_path`는 함께 쓰는 선택적 identity anchor이며 과거 행에는 없을 수 있다. 이것만으로 권한이나 수락을 부여하지 않는다. |
| `orchestrator.session.completed`, `.failed`, `.cancelled` | 세션 수명주기의 완료·실패·취소 기록이다. 취소 기록이 외부 도구의 종료나 외부 효과 되돌림까지 증명하지 않는다. |
| `execution.ac.completed` | 이름과 legacy `passed`/`failed`에도 불구하고 **worker 실행 단위의 완료 상태**다. 정식 AC 승인 판정은 평가 결과 `ACResult` / `EvaluationSummary.ac_results`를 확인한다. |
| `execution.ac.capsule.compiled`, `.attempt.dispatched`, `.dispatch.sealed` | capsule·provider 진입·결과 미확정의 경계를 기록한다. sealed 시도는 외부 효과가 이미 발생했을 수 있어 자동 재발송하지 않는 복구 계약을 확인해야 한다. |
| `mcp.job.acceptance_pending_observed` | `job_receipt` aggregate의 과거 접수 지연 관찰이다. 실제 job 생성·현재 생존·재시도 허가가 아니다. 정상 job 이벤트가 우선하며 persistence 실패 시 메모리 fallback만 남을 수 있다. |
| `mcp.job.created`, `.cancelled` | job 생성 시 소유자와 선택적 Linux identity, 취소 상태를 기록한다. Linux의 누락·손상·미지원 identity는 소유자 사망의 증거가 아니라 unknown이다. |
| `artifact.referenced` | 본문이 내구 저장된 뒤 기록되는 제한된 참조다. 원문이 이 이벤트에 들어 있다고 가정하지 말고 필요한 경우 [artifact 조회](/docs/artifacts-detail/)를 이용한다. envelope의 `schema_version` 1과 2를 구분한다. |
| `workflow.run.*`, `workflow.node.*`, `workflow.edge.traversed`, `workflow.checkpoint.saved` | Workflow IR 실행의 별도 lifecycle 계열이다. `workflow_id`와 node/edge/attempt, 실패 사유 또는 checkpoint 참조를 해당 유형에 맞게 읽는다. 제한된 데이터·참조이며 원문 프롬프트나 표준 출력을 되살리는 경로가 아니다. |

위 표는 진단에 중요한 예시이며 이벤트 전체 목록이 아니다. 유형별 구체적인 필수 필드·조건과 interview latency 이벤트는 [고정 원본 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/events.md)를 확인한다. 시각이 있는 기록 하나만으로 전후 관계나 전체 요구 충족을 추론하지 않는다.

## 기록에서 상태로

실제 세션·실행 ID를 확인한 뒤 [이벤트·투영 조회](/docs/query-projections-detail/)에서 조회 범위와 반환 상한을 선택한다. `ouroboros_query_events`는 세션을 생략하면 범위가 넓어지고, 페이지 출력은 payload 전체가 아닐 수 있다. `ouroboros_query_projection`은 저장된 관련 이벤트에서 Run/Stage/Step을 **요청 시 계산**한다. 이벤트의 존재, 투영의 상태, 별도 평가 판정, 외부 서비스의 실제 결과는 서로 다른 증거다. projection에 필요한 이벤트가 없거나 한도를 초과하면 부분 결과를 완전한 상태로 취급하지 않는다. [생명주기와 복구](/docs/lifecycle-detail/), [평가](/docs/evaluation-evolution-detail/)도 함께 본다.

**확인 범위:** 고정 소스와 관련 이벤트 경로가 동일한 로컬 checkout에서 `tests/unit/events/test_base.py`의 기존 단위 테스트 **19개 통과**. 버전 주입·legacy/비정수 fallback·직렬화 왕복 등을 다룬다. telemetry를 비활성화했으나 이 테스트 실행의 빈 HOME·OS 네트워크 격리는 확인하지 않았다. 실제 사용자 DB, 모든 이벤트 생산자·소비자, 프로세스 재시작 및 외부 효과는 시험하지 않았다.
