# Python API: Seed와 이벤트를 부분적으로 다루기

!!! warning "판본과 검증 범위"
    별도 표시가 없으면 이 문서의 계약·관찰은 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 실제 호스트 서버는 별도 판본이며 동등성을 전제하지 않습니다. 합성·대역 시험은 표시된 조건의 관찰로 실제 사용자 DB·모델·모든 호스트를 검증하지 않습니다. 일부 과거 재현 자료는 공개되지 않았으므로 해당 관찰을 독립 재현한 근거로 취급하지 말고 링크된 고정 소스와 설치 버전을 대조하세요. 현재 [제품 문서](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/docs)도 확인합니다.


기준: 2026-11-04, [Q00/ouroboros `722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지는 제품의 전체 인터뷰·실행·평가를 직접 구현하는 튜토리얼이 아니라, 기존 애플리케이션에서 **데이터 모델을 읽거나 작은 격리 실험을 설계할 때**의 출발점이다. 호스트 플러그인과 독립 CLI 사용은 [첫 실행](/docs/first-run-detail/), MCP 서버 연결은 [통합](/docs/integration-detail/)을 참조한다. Python 3.12 이상 및 해당 버전의 의존성이 필요하다. 내부 Python API의 모든 버전 호환성이나 배포 패키지와 고정 source의 동일성을 보증하지 않는다.

[공개 Python 심벌 대응표](/docs/python-api-inventory-detail/)는 고정 소스의 Core·MCP 재수출과 문서 내 이름 언급, 미검증 우선순위를 보여 준다.

## 어느 경계를 고를까

| 필요한 일 | 출발점 | 주의할 점 |
| --- | --- | --- |
| Seed 데이터 검사·교환 | `ouroboros.core.Seed`, `SeedMetadata`, `OntologySchema` | 유효한 객체를 만든 것만으로 요구사항이 합의되거나 실행·평가가 완료되지 않는다. |
| 실패를 명시적으로 전달 | `ouroboros.core.Result`와 관련 오류 타입 | `is_ok` 확인 후 `value`, `is_err` 확인 후 `error`를 읽는다. 잘못된 쪽을 읽으면 `ValueError`가 난다. |
| 저장된 이벤트 조회 | `ouroboros.persistence.event_store.EventStore` | 기본 DB를 암묵적으로 열지 말고 대상·권한·읽기 전용 여부를 먼저 확인한다. 실행·job·lineage의 ID를 구분한다. |
| 외부 도구 연동 | [MCP 통합](/docs/integration-detail/) | 설정의 신뢰 경계와 서버별 연결 결과를 확인한다. 단순 연결 상태가 개별 서버의 성공을 보증하지 않는다. |
| 실행·평가·재개 | [워크플로 선택](/docs/workflows-detail/), [구조](/docs/architecture-detail/) | 단순 Seed 객체 또는 임의 이벤트 삽입으로 제품의 생명주기·승인·복구 권한을 우회하지 않는다. |

## Python 입력·로그 보조 함수의 경계

고정 소스는 `ouroboros.core`에서 `InputValidator`, `validate_api_key_format`, `mask_api_key`, `sanitize_for_logging`을 공개한다. 이들은 호출자가 직접 사용하는 보조 함수이며 모든 진입점에 자동 적용되는 인증·인가나 개인정보 제거 계층이 아니다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/security.py)을 설치한 판본과 대조한다.

- `validate_api_key_format(key, provider)`는 형식만 검사하며 유효성·권한을 확인하지 않는다. 등록된 공급자는 해당 패턴을 쓰지만 **알 수 없는 공급자명은 오류가 아니라 일반 형식 검사로 넘어간다**. 공급자 이름과 인증은 별도 검증한다. `mask_api_key`는 기본적으로 마지막 네 문자를 남기므로 그 결과도 완전한 삭제는 아니다.
- `InputValidator.validate_initial_context`와 `validate_user_response`는 빈 값·공백만 있는 값을 거부하고 양쪽 공백을 제거한 문자열의 길이를 각각 50,000자·10,000자와 비교한다. 검증만 하며 원래 문자열을 변환해 반환하지 않는다. `validate_llm_response`는 빈 문자열을 허용하고 길이 100,000자를 넘으면 거부한다. `validate_seed_file_size`의 입력은 문자 수가 아니라 바이트 수이며 0 이하와 1,000,000 초과를 거부한다. 각 함수는 `(유효 여부, 오류 문자열)`을 돌려준다.
- `validate_path_containment(path, root)`는 호출 시점의 `Path.resolve()` 결과가 root 내부인지 확인한다. 이후 경로나 심볼릭 링크가 바뀌는 상황까지 원자적으로 보호하거나 파일을 열어 주는 권한 경계는 아니다. 실제 파일 접근 시 별도 신뢰·동시 변경 통제가 필요하다.
- `sanitize_for_logging`은 중첩 컨테이너를 복사하며 민감한 필드명·일부 자격증명 형태 등을 정제하지만, 일반 필드의 임의 개인정보나 모든 비밀 형태를 탐지한다는 보장은 없다. 수집을 최소화하고 별도의 기록 정책을 적용한다. 반환 사본을 실제 로그에 사용해야 하며 원본은 바뀌지 않는다.

합성 입력으로 알려지지 않은 공급자 fallback, 기본 마스킹, 응답의 공백 처리와 빈 모델 응답, 0바이트 Seed 거부, 일반 필드 값의 유지 및 임시 경로 내부·탈출 판정을 확인했다. 실제 키·사용자 데이터·파일 접근 경쟁·전체 호출 경로는 시험하지 않았다. 재현 코드는 공개되지 않았다.

## 예제 1: 모델 구성과 직렬화만 확인

아래는 외부 모델·네트워크·사용자 파일을 호출하지 않는 예제다. 실제 요구를 그대로 복사한 Seed나 실행 지시는 아니다. `metadata`와 `ontology_schema`는 필수이며, 나열된 필드는 전체 스키마가 아니다.

```python
from ouroboros.core import Result, Seed, SeedMetadata, OntologySchema
from ouroboros.core.seed import ac_text

result = Result.ok(21).map(lambda n: n * 2)
assert result.is_ok and result.value == 42

seed = Seed(
    goal="Write a greeting",
    constraints=("No external service",),
    acceptance_criteria=("The greeting prints hello",),
    ontology_schema=OntologySchema(name="Greeting", description="A greeting task"),
    metadata=SeedMetadata(ambiguity_score=0.15),
)
restored = Seed.from_dict(seed.to_dict())
assert restored.goal == seed.goal
assert ac_text(restored.acceptance_criteria[0]) == "The greeting prints hello"
```

이 판본의 [Seed 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py)은 문자열 수용 기준을 구조화된 `AcceptanceCriterionSpec`으로 변환한다. 이전 [Core API 설명](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/core.md)의 `tuple[str, ...]`만을 현재 내부 표현으로 가정하지 않는다. 구조화된 기준에는 `description`, `verify_command`, `verify_cwd`, `expected_artifacts`, `output_assertion` 등이 있다. `expected_artifacts`는 작업공간 상대 **실제 경로**이며 설명 문구가 아니다. 수용 기준에 검사 명령을 넣는 것은 나중에 명령이 실행될 가능성을 만든다. 출처와 작업공간, 외부 효과를 검토한 것만 사용하고 이 예제는 명령을 포함하지 않는다.

`Seed`는 frozen Pydantic 모델이지만 `to_dict()` 결과는 일반 데이터다. 이 버전의 `SeedMetadata`는 `decision_provenance` 딕셔너리도 별도 동결한다. 격리 객체에서 속성 재할당과 해당 딕셔너리의 항목 변경이 각각 거부됐고, `model_dump()` 사본을 바꿔도 원본은 유지됐다. 이는 해당 필드의 실험이며 모든 Python 객체·우회적 변경의 불가능성을 증명하지 않는다. [metadata 동결 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py). 복사·수정한 dict를 새 Seed로 읽는 것은 같은 객체의 변경이 아니며, 임의 변경을 기존 승인·실행의 증거로 취급하지 않는다. 사용자와 협의한 수정 및 변경 기록의 경계는 [첫 실행](/docs/first-run-detail/)을 따른다. 오류 타입과 `Result.map`, `map_err`, `and_then`의 세부는 [공식 Core 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/core.md)와 [현재 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py)을 대조한다.

**Result 판정과 콜백 예외:** 고정 구현에서는 `Result.err(...)`도 Python의 진릿값으로는 참이다. `if result:` 대신 `result.is_ok` 또는 `result.is_err`를 검사한다. `Result.ok(None)`은 성공이므로 값이 `None`인지로도 판정하지 않는다. `map`, `map_err`, `and_then`은 적용되는 콜백이 예외를 던지면 그 예외를 `Err`로 변환하지 않고 전파한다. 경계에서 예상 가능한 예외를 명시적으로 처리한다. 격리된 합성 실행으로 `Err`의 진릿값, `Ok(None)`과 `map` 콜백의 `ZeroDivisionError` 전파를 확인했다. 다른 콜백의 전파는 같은 [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py)의 정적 대조이며 모든 예외 유형을 시험한 것은 아니다.

**오류를 기록·공유하기 전:** `OuroborosError`의 문자열 표현은 `message`와 `details`를 포함하며, `ProviderError.from_exception`은 원래 예외의 문자열을 메시지로 보존한다. `ValidationError.safe_value`는 필드 이름과 일부 문자열 접두사로 값을 가리지만, 모든 개인정보를 탐지하지 못하고 `message`나 `details`를 정제하지 않는다. 따라서 오류 전체를 안전하다고 가정해 로그·이슈·외부 응답에 그대로 내보내지 말고 별도 비밀·개인정보 제거 정책을 적용한다. 합성 값으로 민감 필드 마스킹과 일반 필드 노출, `details`와 원래 예외 메시지의 보존을 확인했다. 이는 고정 [오류 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py)의 일부 사례이며 모든 비밀 유형이나 로그 경로를 검증한 것은 아니다. 재현 자료는 공개되지 않았다.

## 예제 2: 임시 이벤트 저장과 재생

다음은 **빈 메모리 SQLite**에 이 예제 전용 이벤트 하나를 저장하고 같은 집계의 이벤트를 읽는다. 실제 실행 DB와 사용자 데이터를 사용하지 않는다. 임의의 `example.*` 이벤트는 제품의 세션 시작·종료나 수용 판정이 아니다.

```python
import asyncio
from ouroboros.events.base import BaseEvent
from ouroboros.persistence.event_store import EventStore

async def main():
    store = EventStore("sqlite+aiosqlite:///:memory:")
    await store.initialize()
    try:
        event = BaseEvent(
            type="example.note.created",
            aggregate_type="example",
            aggregate_id="demo",
            data={"note": "hello"},
        )
        await store.append(event)
        events = await store.replay("example", "demo")
        assert len(events) == 1 and events[0].data["note"] == "hello"
    finally:
        await store.close()

asyncio.run(main())
```

[EventStore 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py)은 SQLite 백엔드를 요구한다. 쓰기 저장소의 `initialize()`는 기본적으로 스키마를 만든다. `replay`는 집계 유형과 ID가 일치하는 이벤트를 시간·ID 순으로 돌려주며, 이 목록만으로 전체 사용자 작업이 성공했는지는 알 수 없다. 실제 저장소를 조회할 때는 기존 DB 백업·접근권한을 확인하고 `read_only=True` 및 스키마 생성 없이 여는 경로를 검토한다. 이 페이지는 실제 사용자 DB 읽기·복구를 시험하지 않았다.

**증분 조회의 순서와 cursor:** 내부 Python API `get_events_after(aggregate_type, aggregate_id, last_row_id, limit=...)`는 해당 집계에서 SQLite rowid가 cursor보다 큰 이벤트를 조회하고 `(events, max_rowid)`를 반환한다. `limit`을 명시하면 rowid 오름차순으로 페이지를 만들고, 빈 페이지는 전달받은 cursor를 그대로 반환한다. `limit=None`이면 페이지 제한 없이 timestamp·ID 순으로 반환하면서 반환 cursor는 최대 rowid다. `max_row_id`를 지정하면 그 rowid까지 포함해 범위를 제한한다. 따라서 제한된 페이지의 반환 순서를 사건 발생 시각 순서로 가정하지 말고, cursor를 개별 집계와 DB에 결합해 보관한다. 이는 내부 Python API 설명이며 MCP 조회에 같은 인자가 있다는 뜻이 아니다. 동시 쓰기·DB 교체·삭제 후 cursor 의미와 외부 효과는 별도 검증이 필요하다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py).

고정 소스와 관련 테스트가 동일한 checkout에서 telemetry opt-out과 임시 HOME·TMPDIR로 기존 합성 테스트를 실행해, timestamp 역순으로 저장한 두 이벤트가 `limit=1`에서 rowid 순으로 빠짐없이 반환되는 사례 1개가 통과했다. 운영 DB·동시 쓰기·OS 네트워크 격리는 시험하지 않았다.

`BaseEvent`에는 ID·type·시각·집계·data·event_version이 있고, 저장 시 특정 `raw_*` 및 구독 원문 관련 키는 [정제 규칙](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/events/base.py)에 따라 제외된다. 이 정제는 임의의 비밀이나 개인정보를 모두 제거한다는 보증이 아니다. 세션 시작·종료 및 수용 판정에는 전용 조건부 저장 경계가 있으므로 직접 만든 이벤트로 상태를 위조하거나 완료를 강제하지 않는다. [이벤트 구조](/docs/architecture-detail/), [상태와 복구](/docs/recovery-detail/).

## 예제 3: 파일 저장소에서 읽기 전용으로 결과 후보 조회

다음 예제는 임시 DB를 **직접 생성한 뒤 닫고**, 별도의 읽기 전용 연결에서 집계별 이벤트를 조회한다. `query_events`의 결과는 이벤트이지 최종 성공 판정이 아니다. 실제 작업의 결과와 ID 관계는 [조회 안내](/docs/query-projections-detail/)를 따른다.

!!! warning "빈 문자열은 필터가 아닙니다"
    이 판본의 Python `EventStore.query_events`는 `aggregate_id`, `aggregate_type`, `event_type`이 빈 문자열이면 해당 조건을 추가하지 않는다. 예를 들어 선택한 ID를 실수로 `""`로 전달하면 빈 결과가 아니라 다른 집계의 이벤트가 포함될 수 있다. 민감한 저장소에서는 호출 전에 필터가 비어 있지 않은지 검증하고 DB 자체의 접근 권한을 제한한다. 이 필터는 권한 검사나 행 단위 보안이 아니다. 이는 Python API의 설명이며 MCP 도구 전체의 입력 규칙을 의미하지 않는다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py).

빈 메모리 SQLite의 합성 집계 두 개로 `aggregate_id="one"`은 한 집계만, `aggregate_id=""`와 `None`은 두 집계를 반환함을 확인했다. 나머지 두 필터의 빈 문자열 동작은 같은 소스 분기의 정적 대조이며 실제 사용자 DB와 모든 입력 조합은 시험하지 않았다. 재현 스크립트는 공개되지 않았다.

```python
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from ouroboros.events.base import BaseEvent
from ouroboros.persistence.event_store import EventStore, sqlite_database_url

async def demo(path):
    url = sqlite_database_url(path)
    writer = EventStore(url)
    await writer.initialize()
    try:
        await writer.append(BaseEvent(
            type="example.note.created", aggregate_type="example",
            aggregate_id="demo", data={"note": "hello"},
        ))
    finally:
        await writer.close()

    reader = EventStore(url, read_only=True)
    await reader.initialize(create_schema=False)
    try:
        page = await reader.query_events(
            aggregate_type="example", aggregate_id="demo", limit=10, offset=0,
        )
        assert len(page) == 1 and page[0].data["note"] == "hello"
        assert not await reader.query_events(
            aggregate_type="example", aggregate_id="other", limit=10,
        )
    finally:
        await reader.close()

with TemporaryDirectory() as tmp:
    asyncio.run(demo(Path(tmp) / "events.sqlite"))
```

이 판본의 [`query_events`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py)는 시각 내림차순과 동일 시각 ID 내림차순으로 반환한다. 비어 있는 필터는 적용되지 않으므로 호출 전 ID를 검증한다. `offset` 기반 페이지 사이에 새 이벤트가 삽입되면 중복·누락이 가능해 안정적인 실시간 cursor로 취급하지 않는다. 이벤트 수신 순서와 시간 순서도 같다고 가정하지 않는다. 실 DB에서는 올바른 경로·접근 권한·백업을 확인하고 내용을 외부에 노출하지 않는다. 읽기 전용 모드는 조회 권한의 적절성이나 데이터 익명화를 보증하지 않는다.

## 이벤트 쓰기와 종료 상태의 경계

이 절은 고정 판본의 내부 Python API 계약이다. 위 예제의 일반 이벤트와 달리 세션 생명주기·최종 수락 이벤트를 임의의 일반 이벤트처럼 쓰면 안 된다. [`EventStore.append`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/event_store.py)는 일반 이벤트에 `None`을 반환하지만 종료 세션 이벤트에는 조건부 전환의 승패를 `True` 또는 `False`로 반환한다. 따라서 반환값의 truthiness만으로 모든 append의 성공 여부를 해석하지 않는다. 세션 시작은 별도 중복 방지 경로로, 최종 AC 수락은 종료 세션 계획의 전용 경로로 처리한다.

`append_batch`는 한 트랜잭션으로 처리하지만 세션 시작·종료, 최종 AC 수락 및 Workflow IR lifecycle 이벤트를 거부한다. 이 이벤트를 섞은 배치의 거부를 개별 이벤트가 모두 기록된 것으로 해석하지 않는다. `append_durable(event, timeout=...)`은 초기화된 저장소의 **일반 append-only 이벤트**용이며 양수 timeout이 필요하다. 세션 시작·종료, 최종 수락과 Workflow IR에는 사용할 수 없다. 구현은 시간 제한 시 트랜잭션 정리까지 기다리는 계약을 두지만 이를 모든 외부 작업의 롤백이나 프로세스 강제 종료 이후 복구 보장으로 확대하지 않는다. 이 쓰기 경계는 소스 대조이며 동시 취소·프로세스 종료 시험은 여기서 수행하지 않았다.

## 설정과 버전 점검

`OuroborosConfig` 및 기본 경로 해석은 [설정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/models.py), 읽기는 [loader](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py)에 있다. 기본 config·DB 경로는 현재 사용자 환경을 가리킬 수 있다. 자동 쓰기, 변경 또는 원격 호출에 앞서 명시적 경로와 권한·비용 범위를 확인한다. [설정 색인](/docs/config-reference-detail/)의 값은 source JSON Schema의 정적 기본값이며 환경·검증 후 실효값과 다를 수 있다.

**검증 범위:** 2026-11-04 Linux 환경에서 고정 source `722172ef`를 `PYTHONPATH`로 사용하고 Python 3.13.16·별도 임시 HOME·`OUROBOROS_TELEMETRY=0`·기존 임시 의존성 환경으로 첫 두 예제의 assertion과 종료 코드 0을 확인했다. 세 번째 예제는 같은 고정 source와 동일한 EventStore 파일, 기존 Q00 가상환경·telemetry opt-out에서 합성 임시 파일 DB로 조회 assertion을 확인했다. 실제 사용자 DB는 사용하지 않았다. 배포 패키지 의존성(`mcp` 2.2.0)을 사용한 첫 두 예제의 source 호환성 시험은 source lock 그대로의 설치나 실제 모델·외부 호스트·실사용 복구를 검증하지 않는다. 이 결과는 예제의 실행 근거일 뿐 전체 API의 안정성 보증이 아니다.


<a id="python-mcp-client-example"></a>

## 예제 4: 로컬 MCP 서버에 연결하고 종료

외부 서비스나 모델 없이 Python 클라이언트 경계를 살펴보는 예제다. 고정 소스에 호환되는 `ouroboros-ai`와 MCP Python 패키지가 설치된 **격리 환경**에서 두 파일을 같은 임시 디렉터리에 만든다. 첫 파일 `mcp-adapter-server.py`는 예제 문자열만 반환하는 stdio 서버다. 둘째 파일 `mcp-adapter-journey.py`는 그 서버를 자식 프로세스로 실행해 연결·발견·호출·연결 해제를 확인한다. 명령과 스크립트의 출처를 검토하고 신뢰할 수 없는 서버를 실행하지 않는다.

```python
"""Synthetic local stdio server; no external services or model."""
from mcp.server import MCPServer

server = MCPServer('local-example', version='1')

@server.tool()
def echo_case(value: str) -> str:
    """Return an example string."""
    return 'synthetic:' + value

if __name__ == '__main__':
    server.run(transport='stdio')
```

```python
"""Isolated stdio adapter journey; server is local synthetic echo only."""
import asyncio
import sys
from pathlib import Path

from ouroboros.mcp.client.adapter import MCPClientAdapter
from ouroboros.mcp.types import MCPServerConfig, TransportType

async def main():
    config = MCPServerConfig(
        name='synthetic', transport=TransportType.STDIO,
        command=sys.executable,
        args=(str(Path(__file__).with_name('mcp-adapter-server.py')),),
        timeout=5,
    )
    client = MCPClientAdapter(max_retries=1)
    connected = await client.connect(config)
    if connected.is_err:
        raise RuntimeError(f'connection failed: {connected.error}')
    try:
        tools = await client.list_tools()
        assert tools.is_ok and any(tool.name == 'echo_case' for tool in tools.value)
        result = await client.call_tool('echo_case', {'value': 'case'})
        assert result.is_ok and not result.value.is_error
        assert result.value.text_content == 'synthetic:case'
        print('connected=true tool=echo_case outer=ok inner_error=false text=synthetic:case')
    finally:
        closed = await client.disconnect()
        assert closed.is_ok, str(closed.error)
    assert not client.is_connected
    after_close = await client.list_tools()
    assert after_close.is_err
    print('disconnected=true list_after_disconnect=error')

asyncio.run(main())
```

같은 디렉터리에서 `python mcp-adapter-journey.py`로 실행한다. 연결과 도구 호출은 각각 `Result`를 반환하므로 바깥 결과의 `is_err`를 먼저 살핀다. 도구가 응답한 경우에도 내부 `MCPToolResult.is_error`를 확인해야 한다. 위 예제의 `assert`는 이 제한된 실험의 확인용이며 운영 코드에서는 `python -O`에서도 사라지지 않도록 명시적 오류 처리를 쓴다. `finally`에서 연결 해제하고 `disconnect()` 결과도 확인한다. 연결 실패·취소·오류 응답과 재시도는 별도 경로다. 실제 서버로 변경하면 해당 서버 프로세스 실행, 환경변수 상속, 권한·비용 및 외부 효과가 달라진다. [MCP 통합과 신뢰 경계](/docs/integration-detail/)를 먼저 확인한다.

정상 호출만으로 오류 처리를 확인할 수는 없다. 위 클라이언트 예제의 `try` 블록에서 정상 호출 뒤에 다음을 넣으면, 같은 합성 서버에 필수 `value`를 빠뜨려 **의도적으로** 입력 오류를 요청한다. `result.is_ok`는 MCP 응답을 받았다는 바깥 결과이며, 도구의 성공 여부는 `is_error`를 따로 읽는다. 실제 서버의 오류 문구는 민감한 정보를 포함할 수 있으므로 무조건 출력·공유하지 않는다.

```python
bad = await client.call_tool('echo_case', {})
if bad.is_err:
    print('호출 자체 실패')
elif bad.value.is_error:
    print('서버가 도구 오류를 반환')
else:
    print('오류가 아닌 응답: 서버 계약을 다시 확인')
```

같은 고정 source와 기존 가상환경을 사용한 별도 합성 실행에서 이 누락 요청은 바깥 `is_ok=True`, 안쪽 `is_error=True`였고 연결 해제 후 조회는 바깥 오류였다. 임시 HOME·TMPDIR와 Linux 사용자·네트워크 namespace를 사용했다. 이 관찰은 입력 검증 오류 한 건에 한정되며 모든 서버, 예외 및 연결 실패의 표현은 보장하지 않는다. 재현 스크립트는 공개되지 않았다. 실제 인증·모델·원격 서버는 사용하지 않았다.

**검증:** 2026-11-04 고정 source `722172ef`의 설치본과 별도 임시 HOME/TMPDIR, telemetry opt-out, Linux 사용자·네트워크 namespace에서 위 두 파일을 실행했다. 실제 `MCPClientAdapter`의 연결·도구 발견·정상 결과(`synthetic:case`)·연결 해제·해제 후 목록 조회 오류를 확인하고 프로세스가 종료 코드 0으로 끝났다. 사용한 설치본의 `adapter.py` 등 네 파일은 고정 Git blob과 일치했지만 전체 의존성의 동등성은 확인하지 않았다. 테스트는 한 Linux 환경의 합성 stdio 서버 하나에 한정되며, 네트워크 namespace만으로 Unix socket이나 상속 파일 디스크립터까지 전부 격리했다는 뜻은 아니다. 원격 인증, 실서비스·실모델, 연결 실패 시 정리, 재시도 및 모든 오류는 시험하지 않았다. [어댑터 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/adapter.py)과 [원본 Python MCP API](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/mcp.md)도 확인한다.


## 예제 5: Python 인터뷰 한 회차와 명시적 저장

`InterviewEngine`은 Python에서 질문 생성과 응답 기록을 다루는 경계다. 아래는 외부 모델 대신 고정 질문만 반환하는 대역을 사용하며, **실제 인터뷰나 Seed 생성이 아니다**. 임시 디렉터리에서만 상태 파일을 만들고 종료 시 지운다. 실행 전 설치 버전이 이 문서의 고정 소스와 같은지 확인한다.

```python
"""Synthetic InterviewEngine journey; uses a fake adapter and temporary files."""
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from ouroboros.bigbang import InterviewEngine
from ouroboros.core import Result


class FakeAdapter:
    async def complete(self, messages, config):
        return Result.ok(SimpleNamespace(content="What should the tool do first?"))


async def main():
    with TemporaryDirectory(prefix="interview-demo-") as temp:
        engine = InterviewEngine(llm_adapter=FakeAdapter(), state_dir=Path(temp), model="fake")
        start = await engine.start_interview("Build a small task list", interview_id="example")
        assert start.is_ok, start.error
        state = start.value
        question = await engine.ask_next_question(state)
        assert question.is_ok, question.error
        result = await engine.record_response(state, "Add and list tasks", question.value)
        assert result.is_ok, result.error
        before = await engine.load_state("example")
        assert before.is_ok and len(before.value.rounds) == 0
        saved = await engine.save_state(state)
        assert saved.is_ok, saved.error
        loaded = await engine.load_state("example")
        assert loaded.is_ok and len(loaded.value.rounds) == 1
        missing = await engine.load_state("missing")
        assert missing.is_err
        print("fake question, record, explicit save, reload, missing ID: PASS")


asyncio.run(main())
```

고정 구현에서 생성자는 `state_dir`을 만들고 `start_interview`는 초기 상태를 JSON으로 바로 저장한다. `record_response(state, user_response, question)`은 메모리의 상태를 갱신하지만 자동 저장하지 않는다. 이 예제는 응답 직후 저장 전 `load_state`에서 0회, 명시적 `save_state` 후 1회를 확인한다. 누락 ID는 `Result.err`다. 저장 결과가 성공이라도 구현은 내구성 확인이 불확실하면 경고할 수 있으므로 성공 응답을 모든 저장 장애에 대한 보장으로 취급하지 않는다. `state_dir`의 기본은 사용자 홈의 `.ouroboros/data`이고 상태에 인터뷰 내용이 담길 수 있다. 실제 데이터로 바꾸기 전에 저장 위치·권한·보존 정책을 정한다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/interview.py).

명시적인 `interview_id`는 재사용 시 기존 파일을 덮어쓸 수 있으므로 새 ID와 저장 경로를 신중히 선택한다. `cwd`를 주면 기존 프로젝트 탐지를 수행할 수 있으며 위 예제는 생략한다. `ask_next_question`에 실제 adapter를 사용하면 모델 요청과 비용이 발생할 수 있다. 반환된 질문이 적절한지, 답변과 후속 Seed·실행·평가가 성공했는지는 별도로 확인한다. 내부 JSON 상태와 EventStore 이벤트는 다른 저장 경계다. 이 예제에서 가짜 모델 한 회, 명시적 저장·재조회·없는 ID만 시험했고 실제 모델·오류 전체·동시 저장과 호스트는 시험하지 않았다.

## 예제 6: Python에서 Seed 파일 저장과 다시 읽기

고정 버전은 `ouroboros.bigbang`에서 동기 `save_seed_sync(seed, path)`와 비동기 `load_seed(path)`를 내보낸다. 둘 다 `Result`를 돌려주며 로드는 `await`가 필요하다. 아래는 이미 신뢰할 수 있는 `Seed` 객체와 새 임시 디렉터리를 준비한 호출자가 쓰는 함수다. 모델이나 워크플로를 실행하지 않는다.

```python
from pathlib import Path
from ouroboros.bigbang import load_seed, save_seed_sync
from ouroboros.core import Seed

async def write_and_read(seed: Seed, target: Path) -> Seed:
    saved = save_seed_sync(seed, target)
    if saved.is_err:
        raise RuntimeError(f"Seed 저장 실패: {saved.error}")
    loaded = await load_seed(saved.value)
    if loaded.is_err:
        raise RuntimeError(f"Seed 로드 실패: {loaded.error}")
    return loaded.value
```

**쓰기 경계:** 저장은 부모 디렉터리를 만들고 기존 대상 파일을 교체할 수 있다. 실제 Seed나 사용자 파일을 덮어쓰지 않도록 먼저 경로와 기존 내용을 확인하고 시험에는 전용 임시 디렉터리를 쓴다. 고정 구현의 `write_owner_only`는 새 임시 파일을 소유자 전용 모드로 만든 뒤 대상을 교체하며, 내구성 확인이 불확실해도 호출은 경고 후 성공 `Result`를 반환할 수 있다. 성공만으로 모든 파일시스템에서 내구성을 보장하지 않는다. Seed에는 민감한 요구사항이 담길 수 있으므로 디렉터리 접근 권한과 보존 정책도 확인한다. 로드는 없는 파일이나 일부 파싱·검증 오류를 `Result.err`로 반환하지만 모든 예외와 모든 입력을 포괄한다는 뜻은 아니다. [고정 저장·로드 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/seed_generator.py), [파일 교체 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/owner_only.py).

격리된 합성 Seed 한 건을 Linux 임시 디렉터리에서 저장·재로드했을 때 데이터가 일치했고, 기존 대상 교체·모드 `0600` 및 없는 파일의 오류 반환을 확인했다. 실제 프로젝트, 다른 파일시스템, 비정상 종료·동시 쓰기와 모든 손상 파일은 시험하지 않았다. 로컬 재현 코드는 공개되지 않았다.

## 예제 7: 프로세스 내부 도구 레지스트리

`ouroboros.mcp.tools.ToolRegistry`는 도구 정의와 비동기 `handle(arguments)`를 가진 핸들러를 이름·분류별로 관리하는 Python 객체다. 다음은 모델이나 서버 없이 합성 핸들러를 등록하고 직접 호출하는 예다. 이 객체에 등록하는 것만으로 실행 중인 MCP 서버에 도구가 노출되지는 않는다. 실제 서버 연결과 인증·입력 검증은 별도로 설계해야 한다.

```python
import asyncio
from ouroboros.core.types import Result
from ouroboros.mcp.types import MCPToolDefinition, MCPToolResult, MCPContentItem, ContentType
from ouroboros.mcp.tools import ToolRegistry

class Echo:
    @property
    def definition(self):
        return MCPToolDefinition(name="sample_echo", description="synthetic echo")

    async def handle(self, arguments):
        item = MCPContentItem(type=ContentType.TEXT, text=str(arguments.get("text", "")))
        return Result.ok(MCPToolResult(content=(item,)))

async def main():
    registry = ToolRegistry()
    registry.register(Echo(), category="example")
    result = await registry.call("sample_echo", {"text": "hello"})
    if result.is_err:
        raise RuntimeError(str(result.error))
    print(result.value.text_content)
    registry.unregister("sample_echo")

asyncio.run(main())
```

같은 이름을 다시 등록하면 `ValueError`이고, 없는 이름의 호출은 오류 `Result`다. 핸들러 예외는 `MCPToolError`로 감싸지만 핸들러가 반환한 `Result`는 그대로 전달한다. 레지스트리는 `arguments`를 스키마에 따라 자동 검증하지 않으므로 핸들러가 검증해야 한다. `unregister` 후 빈 분류 이름은 `list_categories()`에 남을 수 있다. 전역 레지스트리는 프로세스 내 공유 상태이므로 다른 호출자의 등록을 임의로 `clear()`하지 않는다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/registry.py) · [핸들러 프로토콜](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py).

2026-11-04 합성 시험은 빈 HOME/TMPDIR, 비활성 telemetry, Linux user/network namespace와 기존 가상환경에서 등록·호출·중복 거부·등록 해제·없는 도구 오류를 확인했다. 등록 해제 후 빈 분류가 남는 것도 관찰했다. 고정 Git 객체와 시험한 `registry.py`의 SHA-256은 일치했다. 실제 MCP 서버·권한·동시 접근 및 모든 입력 조합은 검증하지 않았다. namespace는 Unix socket과 상속 파일 디스크립터까지 모두 격리했다는 뜻이 아니다. 재현 코드는 공개되지 않았다.


## 예제 8: 합성 도구를 stdio MCP 서버로 제공

`ToolRegistry`와 달리 `MCPServerAdapter`에 핸들러를 직접 등록한 뒤 `serve()`를 실행하면 MCP 전송을 통해 도구를 제공한다. 아래 파일을 신뢰할 수 있는 로컬 작업 디렉터리에 `synthetic_server.py`로 저장한다. 핸들러는 입력을 직접 검증해야 하며 이 예제는 텍스트만 되돌린다. `serve`는 요청을 받는 동안 블록하고, 소유 리소스가 있다면 종료 시 `shutdown()`으로 정리한다. 전송에 쓰이는 stdout에 임의의 `print`를 넣지 않는다.

```python
"""Synthetic stdio server; run only as a trusted local subprocess."""
import asyncio
from ouroboros.core.types import Result
from ouroboros.mcp.server import MCPServerAdapter
from ouroboros.mcp.types import (MCPToolDefinition, MCPToolParameter, ToolInputType,
                                  MCPToolResult, MCPContentItem, ContentType)

class Echo:
    @property
    def definition(self):
        return MCPToolDefinition(name='sample_echo', description='Synthetic echo',
            parameters=(MCPToolParameter(name='text', type=ToolInputType.STRING),))

    async def handle(self, arguments):
        text = arguments.get('text')
        if not isinstance(text, str):
            return Result.ok(MCPToolResult(content=(MCPContentItem(
                type=ContentType.TEXT, text='text must be a string'),), is_error=True))
        return Result.ok(MCPToolResult(content=(MCPContentItem(
            type=ContentType.TEXT, text='synthetic:' + text),)))

async def main():
    server = MCPServerAdapter(name='synthetic-server', version='1')
    server.register_tool(Echo())
    try:
        await server.serve(transport='stdio')
    finally:
        await server.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
```

[예제 4](#python-mcp-client-example)의 `MCPServerConfig`에서 `command`를 서버 Python 실행 파일, `args`를 저장한 `synthetic_server.py`의 절대 경로로 지정한 후 `list_tools()`와 `call_tool("sample_echo", {"text": "hello"})`를 사용할 수 있다. 프로세스 실행은 코드를 실행하는 권한을 수반하므로 신뢰한 서버 경로만 지정한다. 호출의 바깥 `Result`와 내부 `is_error`를 모두 검사하고 클라이언트를 `finally`에서 해제한다. 도구 등록 시 같은 이름은 기존 핸들러를 덮어쓰므로 고유 이름을 사용한다. 이 예제는 인증이나 네트워크 공개를 설정하지 않는다. 네트워크 전송을 선택하기 전 [호스트·MCP 통합](/docs/integration-detail/)의 인증과 바인딩 조건을 검토한다. [고정 서버 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py) · [핸들러 계약](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py).

고정 공식 API 문서는 생성자 `version` 기본값을 `1.0.0`으로 표시하지만 해당 소스의 기본값은 `None`이며 이때 설치된 패키지의 `__version__`을 사용한다. 위 예제는 차이를 피하려고 버전을 명시한다. 2026-11-04 고정 소스 archive, 기존 가상환경, 빈 HOME/TMPDIR, telemetry opt-out 및 Linux user/network namespace에서 실제 adapter 서버를 자식 프로세스로 실행해 도구 목록·정상 호출·필수 인자 누락의 도구 오류·클라이언트 해제를 확인했다. 인자 누락은 SDK 스키마 검증에서 거부될 수 있으며 핸들러의 모든 오류를 검증한 것은 아니다. 실제 외부 서버·인증·네트워크 전송·장애 시 정리와 의존성 lock 동등성은 미검증이다. namespace만으로 Unix socket이나 상속 FD까지 격리했다고 가정하지 않는다. 재현 코드는 공개되지 않았다.


## 예제 9: 연결 관리자를 통해 MCP 도구 발견과 호출

[예제 4](#python-mcp-client-example)의 합성 `mcp-adapter-server.py`를 같은 디렉터리에 두고 다음 코드를 실행한다. `MCPServerConfig.command`는 로컬 프로세스를 실행하므로 명령과 서버 코드를 신뢰할 수 있을 때만 연결한다. 이 사례는 한 서버를 명시적으로 등록·연결한다. 여러 서버의 동시 연결, `connect_all`과 충돌 우선순위, 실제 인증 및 네트워크 서비스는 시험하지 않았다.

```python
"""Synthetic local stdio MCP manager/provider journey."""
import asyncio
import sys
from pathlib import Path
from ouroboros.mcp.client.manager import MCPClientManager
from ouroboros.mcp.types import MCPServerConfig, TransportType
from ouroboros.orchestrator.mcp_tools import MCPToolProvider

async def main():
    manager = MCPClientManager(max_retries=1, default_timeout=5)
    config = MCPServerConfig(name='synthetic', transport=TransportType.STDIO,
        command=sys.executable, args=(str(Path(__file__).with_name('mcp-adapter-server.py')),), timeout=5)
    added = await manager.add_server(config)
    assert added.is_ok, str(added.error)
    connected = await manager.connect('synthetic')
    assert connected.is_ok, str(connected.error)
    try:
        provider = MCPToolProvider(manager, tool_prefix='mcp_')
        tools = await provider.get_tools()
        assert any(t.name == 'mcp_echo_case' and t.server_name == 'synthetic' for t in tools)
        result = await provider.call_tool('mcp_echo_case', {'value': 'case'})
        assert result.is_ok and not result.value.is_error and result.value.text_content == 'synthetic:case'
        invalid = await provider.call_tool('mcp_echo_case', {})
        assert invalid.is_ok and invalid.value.is_error
        missing = await provider.call_tool('missing', {})
        assert missing.is_err
        print('discovery=ok echo=synthetic:case invalid=tool_error missing=provider_error')
    finally:
        closed = await manager.disconnect('synthetic')
        assert closed.is_ok, str(closed.error)
    assert not await manager.list_all_tools()
    print('disconnect=ok tools_after_disconnect=empty')

asyncio.run(main())
```

`get_tools()`가 연결된 서버의 도구를 발견하고 provider 내부 이름표를 갱신한다. 연결이나 도구 변경 후에는 다시 발견해야 한다. provider는 외부 `Result` 오류와 성공 결과 안의 `is_error`를 구분하므로 둘 다 검사한다. 표본의 잘못된 인자는 바깥 성공·내부 도구 오류였고 존재하지 않는 provider 도구는 바깥 오류였다. `disconnect`는 연결을 닫지만 등록 자체를 지우지는 않는다. 이름 충돌과 기본 제공 도구 차단 등은 [고정 provider 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_tools.py)과 [관리자 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/manager.py)을 확인한다.

2026-11-04 고정 소스의 두 파일을 Git 객체와 대조하고 기존 가상환경, 격리 HOME/TMPDIR, telemetry opt-out 및 user/network namespace에서 위 합성 stdio 경로를 실행했다. 이 단일 서버 시험은 정상 호출·필수 인자 누락·없는 도구·연결 해제 후 목록을 확인했다. 다중 합성 서버의 별도 사례는 아래에서 다루며 실제 모델·외부 서버·네트워크와 모든 실패 정리는 미검증이다. namespace만으로 Unix socket·상속 FD 격리까지 보장하지 않는다. 재현 재현 스크립트는 공개되지 않았다.

### 여러 stdio 서버와 충돌·종료의 관찰 범위

고정 소스의 합성 시험에서 동일한 `echo_case`를 제공하는 `zeta`, `alpha` 순서로 등록하고 세 번째 실패 서버를 더한 뒤 `connect_all()`을 호출했다. 두 서버는 연결되고 하나는 실패했다. `MCPToolProvider.get_tools()`의 충돌 정리는 이름과 서버명을 정렬해 이 입력에서 `alpha`를 선택했지만, `MCPClientManager.find_tool_server()`는 등록 순서의 첫 연결 서버인 `zeta`를 반환했다. 두 API가 항상 같은 서버를 고른다고 가정하지 말고, 특정 서버가 필요하면 `manager.call_tool(server_name, tool_name, arguments)`로 명시하고 반환된 오류와 도구 내부 오류를 확인한다. 내장 도구 및 다른 이름 조합은 별도로 확인해야 한다. [관리자 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/manager.py), [도구 충돌 정리 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_tools.py).

같은 합성 시험에서 `connect_all()` 뒤 `disconnect_all()`은 연결된 두 서버에 대해 각각 다른 태스크에서 cancel scope를 종료할 수 없다는 오류 결과를 반환했다. 최초에는 전체 종료 성공을 기대한 assertion이 실패했고, 오류 결과를 명시한 재시험은 통과했다. 이 실행이 끝난 후 합성 서버 경로의 프로세스는 `pgrep`에 나타나지 않았지만, 이것만으로 모든 자식·자원 정리나 다른 런타임의 동작을 보장할 수 없다. 각 연결·종료 결과를 확인하고, 이 사례를 모든 transport·버전으로 일반화하지 않는다. 임시 HOME/TMPDIR, telemetry opt-out, user/network namespace와 기존 가상환경을 사용했으며 네임스페이스만으로 Unix socket·상속 FD를 모두 차단하지 않는다. 실제 인증·외부 서버·연결 실패의 모든 조합과 의존성 lock 일치는 미검증이다. 시험 코드와 첫 실패·재시험 출력은 공개되지 않은 재현 자료에 있다.


**제한된 우회 시험:** 위 실패 뒤 별도의 두 합성 stdio 서버에서 같은 태스크가 `await manager.connect("zeta")`, 이어 `await manager.connect("alpha")`로 순차 연결하고 두 서버를 호출한 뒤, **연결 역순**으로 `await manager.disconnect("alpha")`, `await manager.disconnect("zeta")`를 호출하자 두 종료 결과가 성공이었다. 각 `Result`를 검사하고 실제 연결에 성공한 이름만 역순으로 정리하는 접근을 이 환경에서 시험할 수 있다. 이는 완전한 정리 보장이 아니다. 같은 태스크에서 연결해도 정순 종료한 비교 시험에서는 첫 서버 종료가 현재 cancel scope가 아니라는 오류를 반환했고 둘째는 성공했다. 두 경우 모두 manager의 도구 목록은 비었지만 이는 자식 프로세스나 모든 자원이 정리됐다는 증거가 아니다. `connect_all()`은 각 연결을 별도 asyncio task에서 실행하고 `disconnect_all()`은 호출 태스크에서 순차 종료한다는 소스와 오류가 태스크 경계에 부합하지만, 이 관찰만으로 모든 실패의 원인을 단정하지 않는다. 별도 합성 시험에서는 첫 서버 연결 성공 뒤 존재하지 않는 두 번째 실행 파일의 연결이 `Result.err`를 반환했고, 같은 태스크의 `finally`에서 첫 서버를 종료하자 성공했다. 이는 두 번째 프로세스가 시작되기 전 실패한 한 사례다. 별도의 합성 시험에서 두 번째 stdio 서버 시작 후 초기화 대기 중 연결 태스크를 취소하고 취소 예외를 잡았을 때, 해당 서버의 manager 상태는 `connecting`에 남았다. 같은 태스크에서 그 이름을 `disconnect`하자 `disconnected`로 바뀌고 앞서 연결한 서버의 종료도 성공했다. 이 시험은 취소 예외를 잡은 뒤 정리를 관찰하며 취소를 재전파하지 않았다. 실제 취소 정책을 설계할 때 이를 성공 완료로 취급하지 않는다. 시작 후 다른 실패·반복 취소·재연결·외부 서버·다른 transport와 SDK 버전은 미검증이다. 자세한 조건은 공개되지 않은 재현 자료에 있다. 상세는 공개되지 않은 재현 자료를 참고한다. 합성 서버명으로 시험 종료 뒤 `pgrep`에서 남은 프로세스가 없음을 확인했지만 모든 자원에 대한 증거는 아니다. 상세 스크립트와 순서별 출력은 공개되지 않은 재현 자료이다.

## 예제 10: Python MCP 서버의 프롬프트 등록

고정 소스의 `MCPServerAdapter`에는 도구 외에 프롬프트 템플릿을 등록하는 `register_prompt`가 있다. 이는 MCP 클라이언트가 요청할 때 문자열을 만들어 주는 인터페이스이며, 프롬프트 등록이나 조회만으로 모델을 호출하거나 작업을 실행하지 않는다. 아래 합성 예에서 인수 내용은 서버에 전달되므로 민감 정보를 넣지 말고 서버를 신뢰해야 한다.

```python
from ouroboros.core.types import Result
from ouroboros.mcp.server import MCPServerAdapter
from ouroboros.mcp.types import MCPPromptArgument, MCPPromptDefinition

class ExamplePrompt:
    @property
    def definition(self):
        return MCPPromptDefinition(
            name="synthetic_prompt", description="Synthetic prompt",
            arguments=(MCPPromptArgument(name="topic", required=True),),
        )

    async def handle(self, arguments):
        return Result.ok("Inspect: " + arguments["topic"])

server = MCPServerAdapter(name="prompt-probe", version="1")
server.register_prompt(ExamplePrompt())
# 서버 생명주기는 위 예제 8처럼 신뢰된 로컬 stdio에서 serve와 shutdown으로 관리한다.
```

클라이언트는 연결 후 `await client.list_prompts()`로 정의를 확인하고 `await client.get_prompt_result("synthetic_prompt", {"topic": "sample"})`의 `Result`와 `messages`를 확인한다. `get_prompt`는 텍스트 메시지를 합친 호환 문자열을 반환하며 역할과 비텍스트 콘텐츠가 필요한 경우 `get_prompt_result`를 사용한다. 고정 stdio SDK 브리지는 등록된 정의를 기준으로 미선언 인수와 빠진 필수 인수를 거부하고 인수 값을 문자열로 변환해 핸들러에 전달한다. 반면 adapter의 Python `get_prompt` 직접 호출은 핸들러에 인수를 전달하므로 정의만으로 모든 직접 호출 입력 검증이 보장되지는 않는다. [고정 서버 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py), [클라이언트 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/adapter.py).

2026-11-04 격리 합성 stdio 서버와 Ouroboros 클라이언트에서 프롬프트 열거, 인수·텍스트·user 역할, 호환 문자열, 필수 인수 누락·미선언 인수·없는 이름 오류 및 정상 종료를 확인했다. 재현 코드는 공개되지 않은 재현 자료, 공개되지 않은 재현 자료다. 해당 server/client/types 파일은 고정 commit의 Git blob과 일치하며 기존 가상환경 의존성의 lock 일치는 미확인이다. 실제 외부 서버·인증·모델·비텍스트 메시지·네트워크 transport 및 모든 오류는 미검증이다. 실행은 빈 임시 HOME/TMPDIR, telemetry opt-out 및 user/network namespace에서 수행했으며, 이 namespace가 Unix socket이나 상속 파일 디스크립터까지 모두 차단했다는 뜻은 아니다.

## Python MCP 서버의 리소스 등록

`MCPServerAdapter.register_resource(handler)`는 `definitions`에 `MCPResourceDefinition` 시퀀스를 제공하고 `async handle(uri)`에서 `Result[MCPResourceContent, MCPServerError]`를 반환하는 핸들러를 등록한다. 이 메서드는 URI별로 핸들러를 저장하며 같은 URI를 다시 등록하면 이전 핸들러를 교체한다. 직접 `read_resource`는 정확한 URI를 먼저 찾고, 없으면 `등록 URI + /`로 시작하는 항목 중 가장 긴 등록 URI를 선택한다. 따라서 `example://host/items/42`는 `example://host/items`에 도달할 수 있지만 `example://host/items-other`는 그 자식이 아니다. 알려지지 않은 URI는 오류 Result이고, 핸들러 예외도 서버 오류 Result로 감싼다. 이 prefix 선택은 동적 URI에 대한 **인가나 입력 검증을 대신하지 않는다**. 핸들러가 전체 URI와 접근 권한을 검증하고 필요한 내용만 반환해야 한다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py), [핸들러 계약](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py).

**여러 URI를 가진 핸들러 일부를 교체할 때:** 같은 URI의 `read_resource`는 새 핸들러로 라우팅되더라도 `list_resources`가 이전 정의를 보여줄 수 있다. 고정 구현은 URI별 핸들러를 교체하지만 목록은 남아 있는 각 핸들러의 `definitions` 전체를 순회하며 처음 본 URI를 유지하기 때문이다. 한 핸들러가 A·B를 정의한 뒤 별도 핸들러로 B만 교체한 합성 직접 호출에서 B의 목록 이름은 이전 정의였고 B 읽기는 새 핸들러에 도달했다. 목록의 메타데이터와 실제 처리자가 다를 수 있으므로 핸들러 설계에서 URI의 중복 등록을 피하고 등록 변경 뒤 목록과 읽기를 각각 확인한다. 이 시험은 직접 adapter 호출이며 stdio·동시 등록·외부 서버 전체를 검증하지 않았다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py), 재현 자료는 공개되지 않았다.

2026-11-04에 고정 소스와 빈 임시 HOME의 격리 합성 직접 호출에서 정확한 경로·자식·가장 긴 prefix·경계 불일치 및 같은 URI 재등록 교체를 확인했다. 재현 자료는 공개되지 않았다. 별도 합성 stdio 서버와 실제 `MCPClientAdapter`를 사용한 시험에서도 두 리소스 열거, 정확 경로·자식·최장 prefix·경계 불일치·동일 URI 교체 및 연결 해제를 확인했다. 해당 시험의 재현 코드는 공개되지 않았다. 다른 transport·인증·동시 등록·실제 외부 서버는 검증하지 않았다. 기본 서버의 리소스 읽기는 [통합 안내](/docs/integration-detail/)를 참고한다.
