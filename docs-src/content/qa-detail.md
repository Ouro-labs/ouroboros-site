# QA: 산출물 평가와 반복 기록

기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). [QA 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/qa/SKILL.md), [MCP 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py), [독립 CLI](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/qa.py)를 기준으로 한다. 연결된 서버와 설치 판본이 다르면 해당 스키마와 도움말을 확인한다.

**판본 경계:** 본문은 722판에 대한 상세 설명이다. 해당 QA handler/CLI/skill 파일은 722판과 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)을 정적으로 비교했을 때 차이가 없었다. 그러나 공개 `v0.59.9` MCP 입력 schema는 `pass_threshold`의 JSON Schema 범위 제약을 main과 달리 제시하지 않는다. 이는 schema 표현의 차이이며 release handler가 범위를 검증하지 않는다는 뜻은 아니다. [main QA handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/qa.py), [0.59.9 QA handler](https://github.com/Q00/ouroboros/blob/v0.59.9/src/ouroboros/mcp/tools/qa.py). 실제 host schema, 위임과 모델 응답은 확인하지 않았다. 설치된 서버의 schema와 CLI 도움말을 따르고, 실행 결과·재개는 [진행 상태](/docs/progress-detail/) 및 [복구](/docs/recovery-detail/)의 별도 상세를 참조한다.

QA는 산출물을 정해진 품질 기준에 비추어 판단하는 모델 기반 검토다. 실행 세션의 [정식 평가](/docs/evaluation-evolution-detail/)와 별개이며, 높은 점수만으로 실제 동작·수용 기준 전체의 성공을 증명하지 않는다. 스킬은 행동이 있는 산출물에 대해 가능한 실행·브라우저·화면·파일 검증을 먼저 수행하고, 관찰한 실패가 모델의 PASS보다 우선하도록 안내한다. 수행하지 못한 검증은 생략 이유와 함께 남긴다. 직접 MCP의 기본 in-process 경로는 스킬 안내만으로 파일·브라우저 검사를 자동 수행하는 경로가 아니다. 고정 핸들러가 자체 생성하는 어댑터는 `max_turns=1`이며 도구 envelope를 지원하는 backend에는 `allowed_tools=[]`를 전달한다. 따라서 호스트나 사람이 안전하게 수행한 실제 검사의 결과를 `reference` 등에 명시하고 판정과 구분한다. 주입된 어댑터와 아래 plugin 위임 경로는 별도로 확인하며, 이 설정을 모든 호스트의 OS 격리나 외부 효과 차단 보장으로 해석하지 않는다. [어댑터 생성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py). 이 범위는 고정 소스 대조이며 실제 모델·도구 사용은 시험하지 않았다.

## 입력과 호출

호스트에서는 `ooo qa`와 산출물 및 품질 기준을 제공한다. MCP를 직접 사용하는 경우 `ouroboros_qa`의 `artifact`에는 **내용 문자열**을, `quality_bar`에는 통과 조건을 전달한다. 선택적으로 `artifact_type`(`code`, `api_response`, `document`, `screenshot`, `test_output`, `custom`), 관찰 증거가 포함된 `reference`, `seed_content`, `pass_threshold`를 전달할 수 있다. threshold 기본값은 0.80이며 유한한 0~1 숫자여야 한다. 핸들러는 `artifact`가 문자열인지 검사하지만 빈 문자열 자체를 거부하지는 않는다. 빈 내용이나 공백 기준이 유용한 평가 입력이라는 뜻은 아니다.

**스크린샷 입력 경계:** `screenshot`은 이 도구의 산출물 유형 표시이지, 직접 CLI나 MCP가 이미지 파일을 첨부해 시각적으로 읽는다는 보장이 아니다. 고정 CLI는 존재하는 일반 파일을 UTF-8 텍스트로 읽고, 직접 MCP는 `artifact` 문자열을 프롬프트의 텍스트 내용으로 전달한다. 따라서 PNG 등 바이너리 이미지 경로를 직접 CLI에 넣으면 UTF-8 디코딩 오류가 날 수 있고, 경로 문자열만 MCP에 넣어도 이미지 내용을 읽었다고 볼 수 없다. 시각 검사가 필요하면 호스트가 지원하는 별도 이미지·브라우저 도구로 실제 화면을 확인하고 관찰을 출처와 함께 전달한다. 해당 도구와 QA 호출의 실제 지원 여부는 설치 환경에서 확인한다. [CLI 입력 처리](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/qa.py), [QA 프롬프트 구성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py). 고정 소스 설치본의 입력 헬퍼를 합성 텍스트와 1×1 PNG로 직접 시험했을 때 텍스트는 읽혔고 PNG는 UTF-8 디코딩 오류가 났다. 이는 헬퍼 한 사례이며 전체 CLI·MCP·호스트·모델 호출은 시험하지 않았다.

이 호출은 모델에 산출물·기준·참고 자료와 이력을 전달하고 시간·비용을 발생시킬 수 있다. 실제 파일의 민감정보와 전송 범위를 확인한다. 직접 CLI는 `ouroboros qa ARTIFACT --quality-bar '통과 기준'` 형태이며 파일 경로 또는 텍스트를 받는다. **없는 경로 또는 디렉터리는 오류 대신 그 입력 문자열 자체로 평가될 수 있다.** `--reference`, `--seed-content`도 같은 규칙을 쓰므로 파일 존재와 내용을 먼저 확인한다. [CLI 색인](/docs/cli-reference-detail/)과 [워크플로](/docs/workflows-detail/)를 참고한다.

## 결과와 다음 반복

직접 MCP 경로에서 정상 응답은 `qa_session_id`, `iteration`, `score`, `verdict`, `loop_action`, `iteration_entry` 등을 `meta`에 담는다. 기본 threshold에서 점수 0.80 이상은 `pass`/`done`, 0.40 이상 0.80 미만은 `revise`/`continue`, 0.40 미만은 `fail`/`escalate`다. threshold를 바꾸면 **먼저 해당 threshold와 비교**하므로 0.40 미만 threshold에서 그 이상인 점수도 pass가 될 수 있다. 모델이 반환한 verdict 문자열이 점수와 달라도 이 핸들러는 점수로 verdict와 loop action을 다시 결정한다. 평가 오류나 파싱 실패는 성공적인 판정이 아니다.

모델 응답이 유효한 단일 판정으로 해석되지 않으면 파싱 오류가 될 수 있다. 특히 여러 JSON 판정이 경쟁하거나 일부가 잘못된 경우 주변 문장의 점수만 골라 통과로 바꾸지 않는다. 지원하는 단일 응답 fence가 주변 예시보다 우선할 수 있으므로 모든 복수 JSON이 무조건 거부된다고 일반화하지 않는다. 결과에서 `score`는 불리언이 아닌 유한한 0~1 숫자여야 한다. `dimensions`가 객체가 아니면 빈 객체가 되고 불리언과 유한하지 않은 값은 빠진다. 유한한 차원 숫자에는 0~1 범위 검사가 적용되지 않아 음수나 1 초과도 남을 수 있다. `differences`·`suggestions`가 목록이 아니면 빈 목록이 되며, 목록 원소는 문자열로 변환하고 공백을 제거한 후 비어 있지 않으면 유지한다. 이는 내용의 충실성을 보장하지 않으므로 원래 응답·오류 및 누락된 근거를 확인한다. [응답 파서](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py).

첫 결과의 `qa_session_id`와 `iteration_entry`를 보존한다. 이후 MCP 호출에는 같은 `qa_session_id`와 **이전 entry를 누적한 `iteration_history` 배열**을 함께 전달한다. 핸들러는 전달된 이력 길이 + 1을 반복 번호로 계산하고, ID만으로 이전 이력을 복원하지 않는다. 이력은 대상·검증 증거·민감정보의 출처를 확인한 뒤 유지한다. 이 호출 자체가 수정 작업을 자동 실행한다는 뜻은 아니다. 독립 CLI의 `--qa-session-id`는 있지만 이 판본의 CLI에는 `iteration_history` 옵션이 없으므로 ID만 넣어 MCP와 같은 반복 문맥이 재구성된다고 가정하지 않는다.

### 독립 CLI의 종료 코드 해석

고정 CLI는 핸들러 자체가 오류 `Result`를 반환하면 `QA failed`를 출력하고 종료 코드 1을 반환한다. 정상 도구 응답의 `meta.passed`가 명시적으로 `false`이면 종료 코드 2다. 그 외의 응답은 코드 0으로 끝나므로, `meta.passed`가 없거나 예상과 다른 위임·응답이라도 종료 코드만으로 PASS라고 단정하지 않는다. 출력된 판정과 이유, 실제 검사 증거를 확인한다. 이 설명은 [고정 CLI 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/qa.py)를 기준으로 한다. 고정 소스의 실제 Typer 명령을 합성 QAHandler 결과와 셸 환경 대역으로 실행한 한 시험에서 핸들러 오류·`passed: false`·`passed: true`·빈 metadata의 종료 코드는 각각 1·2·0·0이었다. 이는 공개 재현 파일이 없는 대역 관찰이며 실제 모델·호스트 위임·모든 응답 조합은 시험하지 않았다.

## OpenCode plugin 위임

plugin 경로에서 `status: delegated_to_subagent`, `dispatch_mode: plugin`은 위임 영수증이다. `_subagent`는 자식의 입력이며 verdict가 아니다. 호스트가 실제 자식 결과를 기다리고 JSON의 점수·판정·차이·제안을 읽어야 한다. 응답에 `iteration_entry`가 없으므로 스킬은 threshold와 0.40 기준으로 loop action을 계산해 entry를 구성하고 후속 호출의 이력에 넣도록 안내한다. 자식 결과를 파싱할 수 없으면 판정 미확인으로 보고한다. subprocess와 plugin의 실행·권한 경계는 [OpenCode 브리지](/docs/opencode-bridge-detail/)를 따른다.

정상 판정이라도 실측 실패를 덮지 않고, 결과·근거·미실행 항목과 다음 행동을 함께 제시한다. QA가 합격한 뒤 별도 정식 평가나 자동 후속 작업의 상태는 그 작업에서 다시 확인한다.

**검증 범위:** 고정 커밋과 QA 핸들러·CLI·스킬 및 대상 테스트 경로가 동일한 로컬 checkout에서 `tests/unit/mcp/tools/test_qa_parser.py`의 기존 대역 테스트 24개가 통과했다(telemetry 비활성). 점수 기반 판정 및 이력의 반복 번호 사례를 포함한다. 이 수치는 당시 로컬 test run의 기록이며 공개 재현 자료가 아니다. 임시 HOME·OS 네트워크 격리, 실제 모델·OpenCode 호스트와 모든 입력 조합은 이번 시험으로 검증하지 않았다.

독립 재검증에서는 고정 커밋과 관련 경로 차이가 없는 체크아웃에서 `test_qa_parser.py`, `test_qa_threshold.py`, `test_subagent.py`를 대상으로 `-k "qa or QA"`를 적용해 **54개 통과, 89개 미선택**이었다. 임시 HOME·TMPDIR과 telemetry 비활성 조건에서 전달된 이력의 반복 번호, 점수·임계값 판정, QA 위임 payload와 subprocess 분기를 대역으로 확인했다. 이 수치는 당시 로컬 test run의 기록이며 공개 재현 자료가 아니다. 실제 OpenCode 호스트·모델, OS 네트워크 격리와 모든 입력 조합을 검증한 결과는 아니다.
