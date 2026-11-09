# Disposable Memory 산출물 조회와 보존

기준: 2026-11-04, 고정 Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지는 [저장소 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py), [CLI 명령](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/artifacts.py), [MCP 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/fanout_handler.py)를 기준으로 한다. 설치된 버전과 실제 연결 서버의 스키마가 다를 수 있다.

**판본과 확인 범위:** 위의 artifact 저장소·CLI·MCP handler 파일은 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 `v0.59.9`와 정적으로 비교했을 때 이 선택 파일 경로에서 차이가 보이지 않았다. 이는 이 파일들의 소스 비교이며 저장소 주변 코드·의존성·배포판·연결된 host schema의 완전한 동등성은 뜻하지 않는다. 이 상세본의 합성 저장소/stdio 관찰은 당시 고정 source에서 수행한 범위에 한정하며, 실제 사용자의 artifact, host, model, 운영 동시성은 확인하지 않았다. 실행 상세와 추가 주의는 [기존 진행 상태](/docs/progress-detail/) 및 [복구](/docs/recovery-detail/)도 참조한다.

여기서 artifact는 작업공간에 생성된 임의의 파일 전체가 아니라, Disposable Memory가 **contract ID에 연결해 보관한 본문**이다. 일반 결과의 제한된 envelope는 본문 전체가 아니며, 명시적 조회가 별도로 필요할 수 있다. 프로젝트의 `.ouroboros/artifacts/artifacts.db`와 실행 이벤트의 EventStore는 별도다. 하나만 보존해서 다른 쪽까지 복구된다고 가정하지 않는다. 본문에는 작업 내용이나 민감정보가 있을 수 있으므로 파일·조회 출력·백업의 접근 및 보존 범위를 확인한다. [구조와 저장](/docs/architecture-detail/), [생명주기](/docs/lifecycle-detail/).

## 호스트 MCP에서 결과 읽기

1. 앞선 fan-out이나 실행의 결과에서 실제 `contract_id`를 보존한다. 작업 `job_id`, 실행·세션 ID, lane ID를 대신 넣지 않는다. 완료 전 영수증과 실제 결과를 구분한다.
2. 같은 프로젝트의 artifact 서비스가 연결된 서버에서 `ouroboros_fetch_artifact`에 `{"contract_id": "실제로 받은 ID"}`를 전달한다. 셸 명령이 아닌 MCP 입력 예시다. 이 도구는 저장된 본문을 명시적으로 읽으며 원래 작업을 재실행하지 않는다.
3. fan-out에서 특정 lane의 출력만 필요하면 원래 결과와 함께 받은 정확한 `lane_id`도 전달한다. 지정 lane이 없거나 잘못됐을 때 전체 본문으로 넓혀 읽는다고 가정하지 않는다. `contract_id` 없이 `lane_id`만 주면 해당 프로젝트에서 그 lane의 최근 발견 목록을 조회한다. 둘 다 없으면 오류다. [MCP 입력 색인](/docs/mcp-reference-detail/#ouroboros_fetch_artifact).
4. 반환된 본문은 작업 결과의 일부이며 정확성·실제 외부 효과·전체 작업 승인 증거와 같지 않다. 내용과 연결된 작업의 상태를 함께 확인한다.

고정 구현에서 `lane_id`만 전달하는 최근 목록은 현재 프로젝트의 최근 24시간(`now` 기준)의 `question_advisory` 중 `code_context`와 `data_context` lane만 대상으로 하며 lane마다 최대 20개를 최신순으로 제시한다. 각 항목은 본문이 아니라 contract ID·lane ID·발행 시각을 가리킨다. 다른 lane이나 오래된 결과, 다른 종류의 artifact에 대한 전체 검색이 아니다. 저장소 조회 실패는 빈 결과로 돌아갈 수 있고 개별 본문 읽기 실패는 건너뛴다. 다만 artifact 서비스 자체가 설정되지 않으면 이 MCP 분기는 빈 목록이 아닌 오류를 반환하며, 서비스가 있는 상태에서 비적격 lane을 단독 조회하면 빈 목록이 반환된다. 따라서 빈 목록을 해당 프로젝트에 근거가 전혀 없다는 증거로 취급하지 않는다. 24시간 안이라도 코드와 데이터가 바뀔 수 있으며 목록은 조회 시 사실의 최신성을 재검증하지 않는다. 결과를 재사용하기 전에 근거와 현재 상태를 다시 대조한다. 실제 서버의 호스트별 프로젝트 경로와 노출 여부는 별도 확인한다. [최근 목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/recent_findings.py), [MCP 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/fanout_handler.py). 이 범위는 고정 소스 대조이며 실제 호스트의 연결 상태나 저장소 장애는 시험하지 않았다.

**인터뷰 시작 시점의 별도 기준 자료:** 위의 교차 세션 최근 목록과 별도로, 고정 `question_advisory` 경로는 같은 인터뷰의 start 단계에 서버가 기록한 provenance를 가진 최근 24시간 내 발행물에서 `code_context`·`web_context`를 찾아 해당 lane에 제공할 수 있다. 일반 교차 세션 목록에는 `web_context`가 포함되지 않는다. 조건에 맞는 기준 자료가 없거나 저장소 조회에 실패하면 이 경로는 빈 결과로 돌아가며 일반 fan-out 경로를 계속한다. 기준 자료에 한 lane만 있으면 그 lane만 제공될 수 있다. 기존 목록에 같은 contract가 있으면 중복 제공하지 않고, 20개가 가득 차 있으면 기준 자료를 유지하기 위해 마지막 항목 하나를 뺀다. 이는 **본문의 사실을 다시 검증하거나 실제 외부 웹 정보의 최신성을 보장하는 기능이 아니다.** 근거가 바뀌었을 가능성을 고려하고 필요한 경우 원본을 다시 조사한다. [고정 선택 및 병합 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/recent_findings.py), [호출 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/question_advisory.py). 해당 고정 소스의 기존 단위 테스트 5건은 격리 임시 HOME·네트워크 namespace에서 통과했다. 테스트의 저장소·합성 제출 사례에 한정되며 실제 호스트·모델·외부 웹 조회는 미시험이다. 이는 공개 재현 artifact가 제공되지 않는 당시 로컬 시험 관찰이다.

**ID 경계:** 고정 SQLite 저장소의 `contract_id`는 1–128자 문자열이며 문자 종류 자체는 제한하지 않는다. `#`은 lane 구분자가 아니라 ID의 일부일 수 있으므로 분리하지 말고, lane은 별도 `lane_id`로 전달한다. 예를 들어 `ordinary#id`는 그 전체가 ID다. 셸에서 실제 ID에 공백이나 `#`이 있으면 셸 인용을 사용해 하나의 인자로 전달한다. 이는 저장소의 규칙이며 모든 호스트의 입력·표시 제약을 보장하지 않는다. 격리된 임시 SQLite 저장소에서 합성 `ordinary#id`, 한글·슬래시·공백을 포함한 ID와 128자 ID의 발행·정확한 조회를 확인했고 빈 ID와 129자는 거부됐다. 실제 호스트·MCP 전송 및 모든 문자 조합은 미검증이다. [고정 ID 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_schema.py). 이 내용은 당시 격리된 합성 저장소 관찰이며 공개 재현 코드는 제공하지 않는다.

**본문 조회의 lane 범위:** `contract_id`와 함께 `lane_id`를 생략하거나 JSON `null`로 주면 전체 artifact 조회 경로를 사용한다. `lane_id`를 빈 문자열·공백을 포함해 명시하면 전체 조회로 넓히지 않고 그 값을 그대로 lane 조회에 전달한다. 따라서 빈 lane을 전체 본문의 별칭으로 사용하지 말고, 정확한 lane을 지정하거나 전체 조회가 의도된 경우에만 생략한다. 이는 [고정 핸들러 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/fanout_handler.py)와 가짜 저장소의 직접 핸들러 시험이다. 합성 오류에서 빈 lane은 오류를 반환했고 전체 조회는 호출되지 않았다. 실제 저장소의 모든 lane·호스트 권한과 MCP 전송은 이 시험의 범위가 아니다. 이 한 사례는 공개 재현 자료가 없는 합성 관찰이다.

**저장소와 MCP 입력의 공백 차이:** 고정 MCP fetch 핸들러는 조회 전에 `contract_id`의 앞뒤 공백을 제거한다. 반면 저장소는 그 공백도 ID에 포함한다. 합성 SQLite에 ` edge `와 `edge`를 서로 다른 본문으로 저장한 직접 핸들러 시험에서, 저장소의 `fetch(' edge ')`는 공백 있는 ID를 읽었지만 MCP 핸들러에 같은 문자열을 전달하면 `edge` 본문을 반환했다. 내부 공백이 있는 별도 합성 ID는 보존됐다. 따라서 앞뒤 공백이 있는 ID를 MCP에서 그대로 식별할 수 있다고 가정하지 말고, 반환된 `contract_id`와 본문을 확인한다. 새 ID는 앞뒤 공백 없이 생성하는 편이 안전하다. 별도의 격리 stdio MCP 서버와 Python SDK 전송에서도 같은 두 ID와 내부 공백 사례가 재현됐다. 첫 시도는 SDK 속성명 오기로 실패했고 수정 후 통과했다. 다른 호스트·모든 공백 문자는 미검증이다. [고정 fetch 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/fanout_handler.py). 직접 핸들러 및 stdio 관찰은 공개 재현 코드가 없는 격리 시험에 한정한다.

## 독립 CLI에서 읽기

독립 CLI가 설치돼 있고 프로젝트와 실제 contract ID를 확인한 경우 다음 명령을 사용한다. `[PROJECT]`와 `[CONTRACT_ID]`는 실제 값으로 교체하며 괄호를 그대로 입력하지 않는다.

```text
ouroboros artifacts fetch [CONTRACT_ID] --project-dir [PROJECT]
ouroboros artifacts replay [CONTRACT_ID] --project-dir [PROJECT]
```

두 명령 모두 저장된 JSON 본문을 출력한다. `replay`는 저장된 본문을 읽는 이름이며 모델·도구·원래 작업을 다시 실행하지 않는다. `--project-dir` 기본값은 현재 디렉터리이므로 다른 프로젝트에서 호출하면 잘못된 저장소를 볼 수 있다. 출력 본문을 채팅·공개 이슈·로그로 복사하기 전 민감정보를 확인한다. CLI 조회 경로와 MCP lane 한정 조회는 동일한 인터페이스가 아니다.

- 계약이나 저장소가 없으면 `Artifact contract does not exist` 계열 오류를 확인한다. 실제 프로젝트 경로와 contract ID를 다시 대조한다.
- 본문이 정리된 계약은 `tombstoned` 오류가 될 수 있다. 이는 해당 저장소에 row는 남지만 본문이 없다는 뜻이며, 재실행이나 본문의 자동 복구가 아니다.
- 손상된 JSON·열 수 없는 DB 등은 별도의 읽기 오류다. 파일을 지우거나 덮어쓰기 전에 상태와 백업을 보존한다. 빈 DB와 실제 작업 결과가 없는 것은 같은 의미가 아니다.

이 판본의 저장소 읽기는 읽기 전용 연결을 사용하고 없는 DB를 조회할 때 새 artifact DB를 만들지 않도록 구현돼 있다. 다만 CLI 전체의 모든 초기화·로그 부작용이나 다른 버전의 동작은 이 설명으로 보장하지 않는다. [저장소 읽기 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py).

## 본문 크기와 발행 실패

고정 구현의 `ArtifactStore.put_for_contract`는 본문을 정규 JSON의 UTF-8 바이트로 직렬화한 뒤 크기를 검사한다. 기본 상한은 **1 MiB (1,048,576바이트)**이며 이 크기까지는 허용하고 초과하면 `ArtifactTooLargeError`를 반환한다. 글자 수나 출력 파일 크기가 아니라 직렬화된 전체 본문의 바이트 수이므로 JSON 구조와 비ASCII 문자도 계산에 포함한다. 생성자가 더 낮은 상한을 설정할 수 있으나 1 MiB보다 높일 수는 없다. JSON으로 손실 없이 표현할 수 없는 값은 크기와 별도로 거부될 수 있다. 크기 검사는 저장소 초기화 전에 수행되므로 초과를 성공으로 취급하거나 무조건 동일 ID에 다른 본문을 다시 쓰지 않는다. 결과를 줄이거나 여러 독립 contract로 나누는 것은 작업 의미·재실행·외부 효과를 확인한 뒤 결정한다. [상수](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/disposable_memory.py), [크기 검사](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py), [직렬화](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_schema.py).

고정 소스와 해당 테스트가 동일한 checkout에서 임시 HOME·작업 디렉터리를 사용한 기존 단위 테스트로 정확히 1 MiB의 본문은 저장되고 1바이트 초과 본문은 거부되며 새 저장소는 생성되지 않는 사례를 확인했다. 이는 저장소 API의 합성 테스트이며 실제 호스트 전달·모델 출력과 모든 직렬화 입력을 시험한 것은 아니다. OS 수준 네트워크 격리는 검증하지 않았다.

## 정리와 복구 경계

`ouroboros artifacts prune --project-dir [PROJECT]`는 기본적으로 삭제 **후보 목록**을 보여 주고 본문을 삭제하지 않는다. 기본 TTL은 90일이며 `--ttl 30d`처럼 초(`s`), 분(`m`), 시간(`h`), 일(`d`), 주(`w`) 단위를 지정할 수 있다. 이 명령의 기본 계획 모드도 저장소를 초기화하므로 아직 없는 artifact 디렉터리·DB를 만들 수 있다. `--ttl`만 바꾸는 것은 삭제 승인이 아니다. `0d`도 유효하므로 게시 시각이 미래가 아닌 본문은 TTL 조건을 즉시 만족할 수 있다. 다만 기본 90일 replay 보존 조건은 별도로 남는다. `--ttl 0d --allow-replay-tombstone`은 그 보존 조건도 우회해 최근 본문을 후보로 포함할 수 있으며 `--apply`까지 더하면 실제 삭제한다. 음수·소수·지원하지 않는 단위는 거부된다. 빈 임시 프로젝트의 CLI 시험에서 `0d`는 종료 0·DB 생성, `-1d`·`1.5d`·`bogus`는 종료 1·DB 미생성이었다. 기존 본문이나 실제 삭제는 이 시험에서 다루지 않았다. 별도 격리 임시 프로젝트에서 합성 본문 두 개의 생성 시각을 오래된 시각과 현재 시각으로 두고 실제 CLI 계획 모드를 시험했다. `--ttl 0d`는 오래된 본문만, `--allow-replay-tombstone`을 추가하면 두 본문 모두 후보로 표시했으며 종료 코드는 각각 0이고 본문 두 개는 그대로 남았다. 이 시험은 `--apply` 실제 삭제, 운영 데이터와 동시성을 검증하지 않는다. 고정 구현은 후보의 나이를 마지막 조회나 갱신이 아닌 저장된 `created_at`으로 계산하고, 시각을 읽을 수 없는 행은 후보에서 제외한다. 후보 계획은 본문이 남은 row와 생성 시각을 보며 현재 사용 중인 실행·호스트·소비자가 있는지는 조회하지 않는다. CLI 도움말의 inactive 표현만으로 실행 중인 작업의 본문이 자동 보호된다고 가정하지 말고, 적용 전 관련 작업과 보존 요구를 별도로 확인한다. [후보 계산 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py). 이 경계는 소스 대조이며 실제 운영 중 동시 정리를 시험한 것은 아니다.

`--apply`는 후보의 본문을 지우고 tombstone을 기록하는 실제 변경이다. 기본 보존 조건은 TTL과 90일 replay 보존 기간을 함께 본다. `--allow-replay-tombstone`을 사용하면 TTL이 지났지만 90일 replay 보존 기간 안에 있는 본문도 후보가 될 수 있다. 본문이 지워지면 `fetch`/`replay`로 되살릴 수 없으므로 대상 프로젝트·후보·보존 의무와 복원 가능한 백업을 먼저 확인한다. 적용 시 저장소는 DB 공간 회수를 위한 `VACUUM`도 시도하지만 성공을 보장하지 않는다. 고정 CLI는 적용 시 **계획된 후보마다** `removed` 행을 출력하지만, 최종 `Removed N`은 실제 UPDATE가 성공한 행 수로 계산한다. 다른 정리 작업이 동시에 본문을 먼저 지우면 후보 행과 실제 제거 수가 다를 수 있으므로 개별 `removed` 문구만으로 이 호출이 그 본문을 삭제했다고 단정하지 않는다. 저장소의 `body IS NOT NULL` 조건은 중복 제거 집계를 막지만, 사용자 데이터 보존이나 운영 동시성 안전 전체를 보장하지 않는다. 이 차이는 소스 대조이며 동시 정리는 시험하지 않았다. 이 안내를 읽는 것 자체는 삭제를 승인하거나 실행하지 않는다. [CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/artifacts.py), [보존 조건 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py).

저장소의 `put_for_contract` 경로에서 같은 contract ID의 재발행은 새 결과로 무조건 덮어쓰지 않는다. ID·본문 크기 검사와 설정된 precommit 검사는 기존 row 판정보다 먼저 실행된다. 고정 저장소는 동일한 정규화 본문이면 기존 발행의 runtime·소요 시간·이벤트 수가 담긴 envelope를 반환하고, 다른 본문이면 충돌 오류를 낸다. 본문이 tombstone 처리된 ID에는 동일 본문이어도 재발행이 거부되며, 구현의 오류는 재실행에 새 contract ID를 할당하라고 안내한다. 새 ID를 쓰더라도 이전 외부 행동이 되돌려지거나 중복이 방지되는 것은 아니므로 상태·외부 결과·권한을 확인한 뒤 재실행을 결정한다. 고정 저장소의 관련 기존 대역 테스트 4개가 임시 HOME에서 통과했다(27개 미선택). 이는 저장소 구현에 한정되며 호스트별 force-rerun 전체 경로를 실모델로 시험한 것은 아니다. [발행 및 충돌 처리](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/persistence/artifact_store.py).

백업·복원은 운영 환경의 SQLite 일관성, WAL 및 별도 EventStore·작업공간을 함께 고려해야 한다. DB 파일을 실행 중 임의로 복사·삭제하는 방식이 일관된 백업이라는 증거는 없다. EventStore 재생이나 artifact `replay`는 실제 외부 서비스의 행동을 되돌리지 않는다.

별도 임시 프로젝트의 합성 본문 하나를 저장한 뒤 실제 CLI 프로세스에서 `fetch` → `prune --ttl 0d --allow-replay-tombstone` 계획 → 같은 옵션의 `--apply` → `replay`를 순서대로 시험했다. 각각 종료 코드는 0, 0, 0, 1이었고 적용 명령은 본문 1개 제거를 보고했으며 replay는 tombstone 오류를 반환했다. CLI 프로세스에는 임시 HOME과 `OUROBOROS_TELEMETRY=0`을 지정했고 임시 디렉터리는 종료 후 제거했다. 본문 생성용 부모 Python은 import 전에 telemetry 비활성화 여부를 별도로 확인하지 않았고 실제 외부 전송 여부도 확인하지 않았다. 이는 합성 데이터의 단일 실행이며 실제 사용자 본문, 동시 정리, 백업 복구나 운영 삭제의 안전성을 검증하지 않는다.

**검증 범위:** 고정 커밋과 관련 파일 차이가 없는 로컬 checkout에서 artifact store와 CLI의 기존 단위 테스트 36개가 임시 HOME·임시 작업 디렉터리 조건으로 통과했다. 테스트는 임시 데이터의 발행·조회·정리 경로를 다루며 실제 사용자의 저장소, 외부 모델, 모든 호스트·동시 장애, 운영 백업과 복원을 시험한 것은 아니다. 별도 빈 임시 HOME·프로젝트에서 실제 `artifacts prune --project-dir` 기본 실행은 후보 없음과 종료 0을 표시하면서 `.ouroboros/artifacts/artifacts.db`를 생성했다. 사용자 artifact나 모델은 사용하지 않았고 OS 수준 네트워크 격리는 시험하지 않았다. 이 실험은 기존 본문의 삭제·동시성이나 운영 복구를 시험한 것이 아니다. 이 문서 작성 중 사용자 artifact를 읽거나 삭제하지 않았다.
