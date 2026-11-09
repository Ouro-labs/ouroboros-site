# 인터뷰: 질문에서 Seed 준비까지

!!! warning "판본과 검증 범위"
    이 안내의 상세 동작은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 설치된 플러그인과 호스트 MCP 서버는 별도 판본입니다. 아래 합성·대역 시험은 표시된 조건에 한정되며 실제 모델·인증·모든 호스트의 동작을 증명하지 않습니다. 설치한 버전의 도움말과 [제품 시작 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조하세요. 구판 동작이 현재 설치에도 같다고 가정하지 않습니다.


기준: 2026-11-04, Ouroboros 고정 소스 [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 문서는 [인터뷰 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/interview/SKILL.md)과 [MCP 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/authoring_handlers.py)를 기준으로 한다. 설치된 서버의 `ouroboros_interview` 입력과 반환 `meta`를 우선 확인한다. 패키지 0.59.9와 이 고정 소스의 calibration 입력 스키마는 차이가 있다([MCP 색인](/docs/mcp-reference-detail/#package-source-differences)). 실제 모델·대화·사용자 승인은 이 문서 작성에서 시험하지 않았다.

인터뷰는 모호한 요청을 목표·제약·수용 기준으로 구체화하는 과정이다. 이미 검토한 실행 Seed가 있거나 명확한 작은 수정인 경우에는 일반적으로 이 경로가 필요하지 않다. 질문 생성과 상태 관리는 MCP가 담당하지만 저장소 코드 확인과 사용자에게 질문하는 일은 호스트가 담당한다. MCP가 프로젝트를 직접 조사하거나 외부 페이지를 읽었다고 가정하지 않는다.

## 시작과 답변

호스트에서 `ooo interview`와 주제 또는 요청을 전달한다. 도구를 직접 호출하는 호스트라면 연결된 서버에서 `ouroboros_interview`를 발견한 뒤 새 세션의 `initial_context`와 필요하면 프로젝트 `cwd`를 전달한다. `session_id`는 반환된 실제 값을 기록하며, 아래는 셸 명령이 아닌 **MCP 인자 형식**이다.

```json
{"initial_context": "작업 목록 도구에 검색을 추가하고 싶다", "cwd": "/실제/프로젝트"}
```

반환 질문과 session ID를 구분해 기록하고, 목표·제약·의사결정은 실제 사용자 답을 받는다. 저장소에서 확인 가능한 사실은 해당 파일을 먼저 읽고 근거와 판단을 분리한다. 질문에 대한 답을 다음 호출에 `session_id`와 `answer`로 전달한다. 사용자 답에 이유·범위·제약이 있으면 의미를 보존하고, 스킬이 요구하는 Refine 확인을 거쳐 전달한다. 선택지의 짧은 라벨만으로 근거를 만들어내지 않는다.

서버 응답에 `meta.status=parent_question_required` 또는 `meta.ask_user_directly=true`가 있으면 호스트가 실제 질문을 하나 하고, 다음 `answer`와 함께 **그때 사용자가 실제로 본 정확한 질문**을 `last_question`으로 보낸다. 질문을 호스트가 직접 만든 다른 경로와 OpenCode plugin 자식 세션의 질문 기록에도 정확한 `last_question`이 필요할 수 있다. 질문 텍스트를 추측하거나 이전 세션의 질문을 재사용하지 않는다. 서버가 낸 질문을 그대로 잇는 일반 경로와 구분하고 연결된 버전의 오류·지시를 따른다.

OpenCode plugin 모드의 `status=delegated_to_subagent`는 실제 인터뷰 완료나 실제 session ID가 아니라 위임 영수증이다. Task pane의 실제 반환을 확인한다. [OpenCode 브리지](/docs/opencode-bridge-detail/). 서버에 도구가 진정으로 없을 때만 스킬의 Path B를 검토한다. 이 직접 인터뷰 결과는 대화 안에만 있으며 MCP에 영속된 세션으로 가장하지 않는다.

## 보조 문맥과 재개

- `confused_terms`는 사용자가 **명시적으로** 모른다고 한 용어다. `references`는 사용자가 제공한 `reference_id`, `label`, `origin` 및 선택적 `url`/`excerpt`이다. 첫 질문을 변경하는 요구사항이 아니며, 서버가 URL이나 파일을 자동으로 가져왔다는 뜻도 아니다. 필요하면 호스트가 별도로 자료와 권한을 확인한다.
- 소스 서버의 `calibration_input`과 `interview_calibration`은 질문의 설명 수준을 조정하며 pending 질문에 대한 답이 아니다. 전달받은 calibration은 런타임 핸들로 다음 호출에 전달할 수 있지만 인터뷰 상태에 영속된다고 가정하지 않는다. 사용자가 용어 뜻을 물으면 같은 질문을 설명·재표현하고 실제 답을 기다린다.
- 연결이 끊기면 새 인터뷰를 무작정 만들지 않고 실제 `session_id`와 상태·저장 위치를 확인한다. recoverable 오류는 스킬이 같은 세션으로 최대 두 번 재시도하도록 안내한다. 실패가 계속되면 직접 인터뷰로 전환할 수 있지만 그 이후의 대화가 서버 상태에 자동 기록되는 것은 아니다. [복구](/docs/recovery-detail/).
- `meta.reason=initial_context_too_large`는 `is_error=false`일 수 있으며 사용자에게 그대로 물을 질문이 아니다. 응답의 `meta.max_chars` 안에서 원래 목표·제약·성공 기준을 요약해 같은 `session_id`의 `answer`로 다시 전달하고, 실제 첫 질문을 기다린다. 누락된 내용을 확정된 요구로 만들지 않는다.

### 이해 수준에 맞춰 질문 다시 듣기

호스트가 [idk 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/idk/SKILL.md)을 지원하면 `ooo idk 멱등성은 모르지만 REST API는 만들어 봤다`처럼 모르는 용어와 이미 해 본 일을 말할 수 있다. `/ouroboros:idk`도 스킬에서 안내하는 표기다. 호스트가 이해한 근거와 설명 수준을 보여 주고, 이후 인터뷰 질문의 용어·예시를 조정한다. 하나의 낯선 단어만으로 사용자의 전반적인 능력을 추정하거나 요구사항 검증을 느슨하게 하는 기능은 아니다.

질문을 받는 도중 이 기능을 사용했다면 **기존 질문에 답한 것으로 처리하지 않는다**. 호스트가 질문의 판단 내용과 제약을 유지하면서 설명하거나 바꿔 묻고 실제 답변을 기다린다. 소스 서버를 직접 다루는 경우 `calibration_input`은 사용자의 설명이고, 응답에 `meta.interview_calibration`이 있으면 다음 인터뷰 호출에 `interview_calibration`으로 전달할 수 있다. 이 값은 대화의 임시 문맥이며 영구 사용자 프로필이나 인터뷰 상태에 저장된 설정으로 취급하지 않는다. 연결된 패키지·호스트가 이 입력을 지원하는지 먼저 확인한다. 이 안내는 고정 스킬과 도구 스키마의 소스 대조이며 실제 호스트 대화는 미시험이다.

## 자문, 종료와 Seed

질문별 자문이나 lateral review payload가 반환되면 호스트 능력과 반환된 dispatch 계약에 따라 실제 작업을 수행한다. 자문은 사람의 결정을 대체하지 않는다. fan-out 제출 시에는 반환된 ID·correlation 값을 정확히 보존하고 실행하지 못한 자식을 `undispatched`로 표시하며, partial이면 보유 결과 전체를 재제출한다. [fan-out 안내](/docs/fanout-detail/). 측정이나 코드 조사 결과도 출처와 사용자의 판단을 구분한다.

`meta.seed_ready=true`는 곧바로 완료나 Seed 생성의 증거가 아니다. 고정 스킬은 Seed-ready Acceptance Guard를 수행하고, 통과 후 합의한 목표를 다시 제시해 사용자 승인을 받도록 한다. 사용자가 목표를 수정하면 정확한 후속 질문을 `last_question`으로 돌려보내고 인터뷰 상태를 갱신한 뒤 다시 검토한다. 명시적 종료 요청을 전달할 때는 스킬이 지정하는 `[from-user][refined][closure]` 표식을 사용한다. 이후 별도 `ooo seed` 단계에서 실제 생성된 파일과 내용을 검토한다. [Seed 형식](/docs/seed-format-detail/), [워크플로](/docs/workflows-detail/).

독립 CLI에서 `ouroboros interview`는 `ouroboros init`과 같은 명령 그룹의 별칭이다. 따라서 새 인터뷰의 명령 표기는 `ouroboros interview start "목표"` 또는 `ouroboros init start "목표"`다. 실행 전 설치 버전에서 각각 `--help`를 확인한다. 예를 들어 상태 디렉터리를 지정한 목록은 `ouroboros interview list --state-dir /실제/상태디렉터리` 또는 `ouroboros init list --state-dir /실제/상태디렉터리`로 조회한다. 고정 소스의 CLI 등록을 대조하고 격리 합성 상태 디렉터리에서 실제 두 명령을 시험한 결과, 빈 상태와 손상 JSON 하나만 있는 상태에서 두 명령 모두 같은 빈 목록 메시지와 종료 코드 0을 반환했고 손상 파일은 보존됐다. 별도로 격리 환경에서 두 `start --help`의 명령 경로와 공백을 정규화한 stdout이 같고 종료 0·stderr 비어 있음을 확인했다. 이는 도움말과 목록의 제한된 시험이며 실제 `start`·모델 인터뷰와 모든 오류가 동일하게 실행된다는 증거는 아니다. 손상 파일이 있으면 빈 목록만으로 파일이 없다고 단정하지 않는다. [그룹 등록](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/main.py).

`ouroboros init list`는 선택한 상태 디렉터리의 `interview_*.json`을 읽어 유효한 세션을 수정 시각 역순으로 표시한다. 고정 구현은 개별 파일을 읽거나 검증하는 데 실패하면 경고를 남기고 해당 파일을 건너뛴다. 경고의 콘솔 노출은 로깅 설정에 따라 다르다. 따라서 `No interviews found`나 목록 누락은 파일이 없다는 증거가 아니다. 상태 디렉터리·경고와 로그를 살펴보고 손상 파일은 변경 전에 안전하게 보존한다. 격리된 임시 HOME에 합성 손상 JSON 하나만 두고 실제 CLI를 실행했을 때 경고와 `No interviews found`, 종료 코드 0이 함께 나왔고 파일은 보존됐다. 별도의 격리 상태 디렉터리에서 합성 `in_progress`·`completed`·`aborted` 세 건과 손상 JSON 한 건을 함께 조회하자 정상 세 건은 업데이트 시각 역순으로 표시됐고 손상 건은 생략됐으며 네 파일의 바이트가 보존됐다(종료 0). 실제 사용자 파일, 권한 오류, 실제 재개와 운영 복구는 시험하지 않았다. [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/interview.py), [CLI](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py).

### 독립 CLI의 완료된 인터뷰에서 Seed 생성

[독립 CLI](/docs/first-run-detail/#install-check)의 인터뷰와 호스트 플러그인의 MCP 세션을 같은 저장소로 가정하지 않는다. 독립 CLI의 상태 디렉터리에 저장된 인터뷰를 썼다면 `ouroboros init list`로 실제 ID와 상태를 확인한다. 고정 CLI의 `ouroboros seed INTERVIEW_ID`는 `completed` 인터뷰에서 Seed 생성을 다시 시도하는 별도 명령이다. 생성 경로는 모델 호출과 파일 쓰기를 포함하므로 중복 생성의 비용과 기존 산출물을 먼저 확인하고, 반환된 경로와 내용을 검토한다. 기본 상태 위치는 `~/.ouroboros/data`이며 별도 위치를 사용했다면 `--state-dir /실제/상태디렉터리`를 지정한다. CLI는 다른 상태를 거부하고 오류에서 `ooo interview --resume`을 안내할 수 있으나, **독립 CLI**에서 재개 명령은 `ouroboros init start --resume INTERVIEW_ID`다. 취소·중단된 인터뷰가 모두 재개 가능한 것은 아니다. 이 독립 `seed` 명령은 생성 중 `KeyboardInterrupt`를 받으면 `Seed generation interrupted.`를 표시하면서 종료 코드 **0**을 반환한다. 자동화에서 종료 코드만으로 생성 성공을 판단하지 말고 실제 반환 경로와 Seed 내용을 확인한다. 고정 구현의 예외 처리에 `KeyboardInterrupt`를 주입한 대역 시험에서 코드 0을 확인했으며, 실제 모델 생성 도중 중단·부분 파일은 시험하지 않았다. [독립 Seed 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/seed.py), [인터뷰 재개](/docs/recovery-detail/).

이 명령 설명은 고정 소스 확인이다. 실제 모델을 사용하는 Seed 생성과 기존 파일에 대한 영향을 이 문서 작성에서 시험하지 않았다.

### 내부 어댑터: 용어 설명과 참조 대비

고정 소스에서 인터뷰 상태는 기본 질문에 실제 응답이 생기기 전에는 어댑터 질문을 만들지 않는다. 그 후 명시된 `confused_terms`가 있으면 내장 용어집에서 정확한 용어 또는 별칭을 대소문자 구분 없이 찾고, 처음 맞는 팩에서 최대 세 항목을 제시한 뒤 이 프로젝트에서의 의미를 다시 묻는다. 기본 내장 팩은 `ui_ux_basics`다. 보류 중 용어는 선택 시 소비되므로 일치하는 용어가 없더라도 그 차례에 다시 자동 제시된다고 가정하지 않는다. 용어 설명은 사용자의 선택이나 요구사항 확정이 아니다. [선택 규칙](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/interview_adapters/triggers.py), [인터뷰 상태](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/interview.py).

그 다음 미해결 참조가 있으면 순서상 첫 참조의 라벨·선택적 URL·발췌를 담아 무엇을 따르고 피할지 묻는다. 이는 외부 자료 자동 수집이 아니라 전달된 문맥을 이용한 질문이다. 참조 대비 답변을 요구사항 후보로 변환하는 경로는 출처를 `reference-derived`, 해결 상태를 `needs_confirmation`으로 표시하며, 답변만으로 자동 확정된 요구사항이라고 보지 않는다. 질문·응답의 provenance 및 이후 확정 경로도 함께 확인해야 한다. [참조 대비](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/interview_adapters/reference_contrast.py), [후보 추출](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/requirement_distillation.py).

고정 소스와 동일한 관련 구현에서 용어 선택·참조 대비의 기존 합성 단위 테스트 11개가 통과했다. 이는 실제 모델·호스트 대화나 모든 표현·재개 상태의 검증은 아니다.

**검증 범위:** 고정 스킬·MCP 도구 정의와 관련 구현을 정적으로 대조했다. 관련 구현·대상 테스트가 고정 커밋과 동일한 별도 checkout에서 과대 초기 입력 envelope, 참조 문맥, calibration 및 `last_question`을 이용한 재개 관련 기존 대역 테스트 78개가 통과했다. 임시 HOME·TMPDIR와 가짜 모델을 사용하고 Python 프로세스의 IP 연결·DNS를 차단했지만 OS 수준 네트워크 격리나 별도 환경으로 실행되는 모든 하위 프로세스까지 보장하지는 않았다. 실제 서버의 질문 생성·사용자 대화·자문 실행·세션 재시작·OpenCode UI 및 모든 입력 조합은 검증하지 않았다. 모델 호출에는 외부 제공자와 비용이 수반될 수 있으며, 실제 호스트가 반환한 상태와 사용자 지시가 우선한다.
