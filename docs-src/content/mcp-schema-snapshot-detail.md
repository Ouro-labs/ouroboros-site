# MCP 입력 스키마 캡처와 해석

기준: 2026-11-04, 고정 소스 [Q00/ouroboros `722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). [도구별 입력과 조건부 동작](/docs/mcp-reference-detail/)과 함께 읽는다.

**판본·자산 출처:** 이 페이지와 JSON 자산은 722판의 기본 stdio 서버에서 관찰한 `list_tools` 입력 schema 스냅샷이다. 자산 `assets/mcp-input-schema-722172ef.json`은 JSON object 36개, 64,669 bytes이며 SHA-256은 `64c06b10adebd6534b6a2211cc840dac633407105554abf7e1dbf318d0afdd12`다. 이 값은 이 파일의 정확한 본문 식별자일 뿐 현재 MCP 서버의 schema 증명은 아니다. 722판의 [tool definitions](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/definitions.py)와 [stdio adapter](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py)를 근거로 한다. 대응하는 정의·adapter 파일은 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 release `v0.59.9`와 정적으로 대조했을 때 차이가 보이지 않았다. 이 파일 비교와 별도 snapshot은 다른 설치·호스트의 동적 도구 등록, schema, 실제 핸들러 검증을 대체하지 않는다. 해당 설치 서버가 반환한 `list_tools` 결과를 우선한다.

**공개 자산 점검:** JSON을 구조적으로 읽고 스키마 이름·입력 정의·설명으로 구성된 것을 확인했다. 캡처에는 사용자 tool-call 입력·응답, 세션·작업 데이터가 포함되지 않으며 개인 홈 경로·계정명·credential/API key 패턴도 발견하지 못했다. 다만 이 파일은 상세한 도구 API 표면과 설명을 공개하므로 제품의 내부 입력 계약을 노출하는 공개 문서 자산이다. 이는 조사 목적상 의도된 내용이다. 이 점검은 자동 패턴 검사와 구조 확인으로, 모든 문자열의 의미나 이후 변경된 자산을 보증하지 않는다.

[기본 stdio 서버의 `list_tools` 입력 스키마 JSON](/docs/assets/mcp-input-schema-722172ef.json)은 도구 이름을 키로 하여 MCP가 노출한 `inputSchema` 전체를 보존한 **한 환경의 캡처**다. 도구 응답, 실제 호출 결과, 인증·권한, 런타임 구성이나 설치된 다른 버전의 계약은 담지 않는다. 도구 설명문도 서버가 반환한 그대로이며 실제 핸들러의 추가 검증이나 조건부 입력은 별도로 확인해야 한다. 특히 스키마에서 필수가 아니거나 중첩 제약이 생략되었다고 해서 어떤 값이든 유효하다거나 실제 실행에 안전하다는 의미는 아니다.

이 캡처에서 36개 도구의 최상위 필드 288개 중 array는 22개이며 그중 5개에만 `items`가 명시돼 있다. object 12개에는 최상위 필드 스키마에 `properties`가 없다. 예외적으로 `ouroboros_pm_interview.answers`는 1–3개 객체이며 각 객체에 길이 1 이상 문자열 `question`과 `answer`가 필요하고 추가 속성은 금지된다. 같은 도구의 최상위 `not`은 `answer`와 `answers`의 동시 전달을 금지한다. 이 JSON Schema 조건은 실제 사용자 응답과 질문의 대응 등 핸들러의 모든 의미 검사를 대신하지 않는다. 그 외 배열·객체의 내부 구조는 캡처만으로 지어내지 말고 각 [도구 설명과 소스](/docs/mcp-reference-detail/)를 따른다.

## 재현과 한계

고정 커밋 archive의 `src/ouroboros` 추적 파일 809개를 해당 Git 객체와 비교해 내용 차이 0개를 확인했다. 격리된 기존 Python 환경을 사용했고 의존성이 고정 커밋의 lock과 동일한지는 확인하지 않았다. 임시 HOME/TMPDIR, telemetry·dashboard opt-out 및 Linux 사용자·네트워크 namespace에서 서버를 띄워 MCP `initialize`와 `list_tools`만 호출했다. 모델·실제 도구 실행·사용자 데이터는 사용하지 않았다. 네트워크 namespace는 Unix socket과 상속 파일 디스크립터까지 모두 격리했다는 증거가 아니다. 36개 도구명과 개수는 확인했지만 환경이나 호스트별 동적 등록 전체를 대표하지 않는다. 당시 캡처 스크립트·실행 환경은 내부 재현 기록이며 공개되지 않는다. archive로 다시 재현하려면 고정 커밋의 archive와 해당 환경을 별도로 준비해야 한다.
