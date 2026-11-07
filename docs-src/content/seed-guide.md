# Seed: 실행 전에 작업 기준을 검토하기

Seed는 목표, 제약, 완료 기준을 작업 전에 정리한 명세입니다. 실행이 시작되면 해당 실행은 Seed를 기준으로 움직입니다. Seed가 생성됐다는 사실이나 높은 등급은 사용자의 요구와 맞다는 증거가 아니므로, 실행 전에 내용을 직접 확인하고 승인하세요.

**판본:** 이 안내는 공개 제품 `main` `592c667f076c3dad7ef68d7844e91480d80135d0`을 기준으로 합니다. 기존 공개 [Seed 장](https://ouroboros.page/learn/seed/)은 2026-08-14에 확인한 구판 `0.51.5`의 예제입니다. 설치된 CLI·host skill·MCP 서버의 판본이 다를 수 있으므로 실제 응답과 설치 버전의 도움말을 확인하고, [판본 및 확인 범위](/docs/version-guide/#version-scope)를 참고하세요.

<details>
<summary>Seed 스키마와 판본을 대조한 근거</summary>
<p>현재 안내의 기능 근거는 제품 main의 <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md">seed skill</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md">interview skill</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/seed.py">Seed 모델</a>, <a href="https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py">Seed 생성 MCP 도구</a>입니다. YAML의 <code>acceptance_criteria</code> 형식과 기준 설명 필드는 release <code>v0.59.9</code>의 <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/skills/seed/SKILL.md#L73-L82">seed skill</a> 및 <a href="https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/seed.py#L583-L614">Seed 모델</a>에서도 확인했습니다. 기존 공개 <a href="https://ouroboros.page/learn/seed/">Seed 장</a>은 <code>0.51.5</code> / <code>d103058fe</code> 판본의 할 일 앱 예제를 설명합니다. 예제의 연속성은 유지하지만, 새 판본의 동작을 옛 출력이나 용어로 단정하지 않습니다. 제품 main, <code>v0.59.9</code> 배포 패키지, host skill 및 MCP 서버는 같은 판본으로 간주할 수 없습니다. 세부 스키마·합성 시험은 <a href="/docs/seed-format-detail/">Seed 형식 참조</a>, 판본 조건은 <a href="/docs/version-guide/#version-scope">판본 및 확인 범위</a>를 보세요.</p>
</details>

## Seed 만들기

일반적인 경로는 [인터뷰](/docs/interview-guide/)에서 실제 목표·제약·완료 기준을 확인한 다음, 같은 지원 호스트 대화에서 `ooo seed`를 요청하는 것입니다. 인터뷰가 완료됐다고 자동으로 Seed가 생성된다고 가정하지 마세요. 인터뷰 안내의 목표 재확인까지 마치고, 그 실제 세션을 사용해 생성합니다. host에서 해당 session ID가 필요하다고 하면 인터뷰가 반환한 ID를 그대로 사용하세요.

```text
ooo seed
```

이미 목표·제약·검증 가능한 성공 기준이 이 대화에서 합의돼 있다면, 제품 skill은 인터뷰 없이 그 내용을 Seed로 정리하는 경로도 허용합니다. 먼저 합의된 표현을 사용하고 누락 정보를 추측하지 않게 하세요. 기준이 빠졌으면 AI가 보충하지 않고 질문하게 해야 합니다. 직접 MCP 사용자는 서버가 `ouroboros_generate_seed`를 실제로 노출하는지 확인하고, 인터뷰 경로에는 반환된 `session_id`, 인터뷰 없는 경로에는 합의된 `session_context`를 사용합니다. 도구 호출에 필요한 schema가 지연 로드되는 host도 있습니다. 도구 이름이나 인자를 임의로 추정하지 마세요.

결과는 실제 응답에서 Seed YAML과 반환된 파일 경로/산출물 정보를 확인합니다. host가 파일 경로를 주지 않고 YAML만 반환할 수 있습니다. 다음 단계로 넘어가기 전에 YAML이 완전히 반환됐는지, 중간 오류·위임 상태만 받은 것은 아닌지 확인하세요. OpenCode의 `delegated_to_subagent`는 작업을 맡겼다는 영수증일 수 있습니다. 실제 자식 결과의 YAML과 ID를 받기 전에는 생성 완료로 취급하지 않습니다.

제품 main의 인터뷰 경로는 기본적으로 모호도 점수가 `0.2`보다 높으면 Seed 생성을 막습니다. 이는 사용자가 원하는 것을 충분히 반영했다는 보증이 아닙니다. 점수가 낮아도 목표·범위·완료 기준을 직접 검토하세요. 점수 gate를 우회하는 `force`는 별도 명시 선택을 위한 인터페이스이며, 빠진 결정을 채우는 방법으로 쓰지 마세요. 이 기능의 MCP 입력은 제품 main 소스 기준입니다. 현재 설치 서버에서 같은 필드가 있는지 먼저 확인하세요.

## 예제 Seed 읽기

아래 YAML은 기존 `/learn/`의 할 일 앱을 이어가는 **합성 형식 예시**입니다. 실제 인터뷰 결과·제품 생성 출력·실행 기록이 아닙니다.

```yaml
goal: "오늘의 할 일을 추가하고 완료 표시할 수 있는 웹앱과, 그 프로젝트의 설치·실행·접속·종료·테스트 방법을 설명하는 README를 만든다"
constraints:
  - "한 사람이 한 기기에서 사용한다"
  - "브라우저를 새로고침해도 작업이 남는다"
  - "계정과 기기 간 동기화는 이번 범위에서 제외한다"
acceptance_criteria:
  - description: "제목을 입력하고 추가하면 해당 작업이 목록에 나타난다"
  - description: "제목이 비어 있으면 새 작업이 추가되지 않는다"
  - description: "완료 표시를 켜고 새로고침한 뒤에도 완료 상태가 보인다"
  - description: "README에 프로젝트에서 확인한 의존성 설치 명령과 출처, 앱 실행·종료 방법, 실제 접속 URL과 포트가 기록된다"
  - description: "README에 테스트 명령과 검증 범위가 기록되며 테스트가 없으면 그 사실이 적혀 있다"
ontology_schema:
  name: "TodoList"
  description: "할 일 목록에서 다루는 작업과 완료 상태"
  fields:
    - name: "title"
      type: "string"
      description: "사용자가 입력한 작업 제목"
    - name: "completed"
      type: "boolean"
      description: "작업이 완료됐는지 여부"
metadata:
  # Seed 모델이 요구하는 생성 메타데이터. 실제 생성물은 제품이 채웁니다.
  ambiguity_score: 0.15
```

위 예제는 설명을 위한 **합성 Seed**입니다. 앞의 세 기준은 할 일 앱 동작을, 마지막 두 기준은 같은 프로젝트 README의 설치·실행·접속·종료·테스트 안내를 다룹니다. 생성 뒤 사용자는 실제 README를 읽고 앱을 시작해 기록된 URL로 접속하여 결과를 확인할 수 있습니다. 이는 확인할 결과의 예시일 뿐, 실제 README·앱·테스트 성공을 뜻하지 않습니다. `metadata`는 Seed 모델에서 필수인 최상위 필드이므로 YAML에서도 생략할 수 없습니다. `ambiguity_score`는 메타데이터 내부에서 선택값이며, 위 값은 형식 예시일 뿐 실제 인터뷰 점수나 검증 결과가 아닙니다. 손으로 작성한 Seed라면 `metadata: {}`도 모델 기본값으로 구성되지만, 예제에서는 의미를 보이도록 점수를 명시했습니다. 실제 생성은 제품이 생성 시각·ID 등 메타데이터를 채웁니다.

앱 동작 세 기준의 예시는 [합성 참고 예제](/docs/todo-reference-example/)에서 따로 살펴볼 수 있습니다. 이 코드는 제품 생성물이 아니며 README에 관한 두 기준은 실제 프로젝트에서 확인해야 합니다.

## 각 부분에서 확인할 것

| 필드 | 확인 질문 |
| --- | --- |
| `goal` | 필수. 작업이 끝났을 때 사용자가 실제로 무엇을 할 수 있어야 하나요? “좋은 앱”, “완벽하게”처럼 판정할 수 없는 단어만 남아 있지 않나요? |
| `constraints` | 선택 가능. 반드시 지킬 기술·환경·범위와 만들지 않을 일이 사용자의 답과 맞나요? 예제에서는 한 사용자, 지속 저장, 계정/동기화 제외를 적었습니다. |
| `acceptance_criteria` | 선택 가능하지만 실행 결과의 판정 기준으로 구체적으로 작성하세요. 각 항목이 완성된 결과의 관찰 가능한 상태인가요? 사용자가 직접 화면이나 테스트에서 확인할 수 있나요? 구현 방법을 요구사항처럼 쓴 것은 없나요? |
| `ontology_schema` | 필수. 도메인을 표현하는 이름과 설명을 적고, 각 필드에는 `name`, `type`, `description`이 필요합니다. 도메인 필드와 설명이 실제 기능과 맞나요? 이 표는 결과 화면의 모든 레이아웃이나 기술 선택을 고정하는 설계서가 아닙니다. |
| `metadata` | 필수 객체. 생성 시각과 Seed ID 등은 제품 기본값이 채울 수 있습니다. 이 예제는 선택값인 `ambiguity_score`만 기입합니다. 예시 점수를 실제 점수로 해석하지 마세요. |
| `verify_command` 등 선택 검증 필드 | 명령이 실제 실행될 수 있습니다. 실행 위치, 셸 동작과 외부 효과를 먼저 확인하고 신뢰할 수 있는 명령만 허용하세요. |

예제에는 `verify_command`가 없습니다. 이는 형식 설명용이며, 파싱되는 Seed라도 검증 가능한 실행 계약을 갖췄다는 뜻은 아닙니다. 실행기가 어떤 자동 검사를 수행할지 또는 평가가 수용 기준을 통과할지 증명하지 않습니다. 수용 기준의 타입, `verify_cwd`, `expected_artifacts`, `output_assertion`과 소비 경로 차이는 [Seed 형식 참조](/docs/seed-format-detail/)를 확인하세요.

### 실행 게이트와 정식 평가의 증거를 구분하기 {#seed-execution-and-evaluation-evidence}

이 할 일 예제의 다섯 AC에는 `verify_command`가 없고, [합성 HTML 참고 예제](/docs/todo-reference-example/)는 사람이 브라우저에서 확인하는 절차만 제공합니다. 이 확인은 제품의 Seed 실행이나 정식 평가가 실제로 실행됐다는 증거가 아닙니다. main `592c667`과 release `0.59.9`의 Seed 형식은 AC별 `verify_command`를 선택 필드로 받습니다. 실제 실행에서 이 필드를 사용하려면 `execution.run_verify_commands`가 켜져 있어야 합니다(두 소스의 기본값은 `true`이며 설치 설정은 다를 수 있습니다). 선언된 명령은 오케스트레이터가 작업 공간에서 실행하고 그 결과를 AC 성공 게이트에 사용합니다. 설명 문장만으로 실행 명령이 생기지는 않으므로, 실제 프로젝트가 만들어진 뒤 신뢰할 수 있는 검사와 작업 경로를 정하고 명령·작업 디렉터리·파일 및 네트워크 효과를 검토하세요. [main Seed 스키마](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/core/seed.py#L586-L616), [main 실행 게이트](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/parallel_executor.py#L9711-L9747), [main 실행 설정 기본값](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/models.py#L311) · 같은 경로의 [release Seed 스키마](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/core/seed.py#L583-L613), [실행 게이트](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/parallel_executor.py#L9680-L9725), [실행 설정 기본값](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/config/models.py#L310).

정식 평가의 Stage 1 기계 검사는 별도 경로입니다. 평가기는 프로젝트 루트 `.ouroboros/mechanical.toml`의 `lint`, `build`, `test`, `static`, `coverage` 명령을 사용합니다. 파일이 없으면 MCP 평가가 탐지를 시도할 수 있고, 해당 경로는 모델 호출과 TOML 파일 쓰기를 수반할 수 있으므로 기존 파일과 제안된 명령을 먼저 확인하세요. 다만 TOML 명령이 없다는 사실만으로 `unverified`라고 단정할 수는 없습니다. 같은 실행의 해당 AC에 연결된 유효한 recorded check-package 결과가 Stage 1에 합쳐질 수도 있습니다. 실행된 Stage 1 검사 결과와 사용할 수 있는 recorded check 결과가 모두 없으면 `approved`가 아니라 `unverified`입니다. 승인은 유효한 Stage 1 실행 증거가 있고 모든 검사가 통과해야 하며, 긍정적인 모델 의견은 실행 증거를 대신하지 않습니다. AC `verify_command`의 실행 게이트와 정식 평가 Stage 1은 서로 다른 경로이므로, 앞의 결과가 평가에 자동 재사용된다고 가정하지 마세요. 실제 프로젝트에서는 평가 결과의 검사·실행 여부·종료 결과와 해당 실행·AC에 속한 기록, `acceptance_state`를 함께 확인하고, 오류나 `unverified`를 통과로 바꾸지 않습니다. 이 합성 Seed YAML 자체에는 테스트 명령이나 실행·평가 결과가 없습니다. 연결된 [HTML 참고 예제](/docs/todo-reference-example/)에는 별도 브라우저 테스트 절차가 있지만, 그것은 문서용 표본에 대한 시험이며 제품 Seed 실행이나 AC 검증 증거가 아닙니다. [main 평가 입력과 탐지 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/evaluation_handlers.py#L549-L559), [main Stage 1 설정 로더](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/languages.py#L1018-L1062), [main 해당 AC 기록 조회와 병합](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/evaluation_handlers.py#L739-L760), [main Stage 1 기록 병합](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/models.py#L190-L203), [main 승인 조건](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/models.py#L568-L605) · release `0.59.9`의 [평가 입력](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/evaluation_handlers.py#L549-L559), [Stage 1 설정 로더](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/evaluation/languages.py#L1018-L1062), [기록 조회·병합 및 승인 조건](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/evaluation_handlers.py#L739-L760). 실제 기계 검사 설정의 구문과 검토할 부작용은 [평가 안내](/docs/evaluation-evolution-detail/)에서 확인하세요.

**생성 후 한 번 검토할 목록**

- 목표가 요청자의 의도와 범위를 정확히 담고 있다.
- 제약과 제외 범위가 인터뷰 답변과 맞는다.
- 기준 각각이 관찰 가능한 결과이며, 빠진 핵심 기능이나 모순이 없다.
- 저장소 경로가 실제 작업 프로젝트를 가리키고, 현재 변경사항을 보존한다.
- 위험·외부 효과·테스트 방법을 이해하고, 실행해도 되는 상태다.

점수 또는 등급은 내용 검토를 대신하지 않습니다. 제품 main의 `seed` skill은 생성된 Seed에 대한 QA를 한 차례 자문(advisory)으로 실행하며, 그 판정은 자동 차단 gate가 아닙니다. QA의 점수나 `A` 등급은 정확성·완성·테스트 통과의 증명으로 취급하지 마세요. `ooo auto`의 grade gate는 자동 실행 경로의 조건이며 일반 Seed 검토와 다릅니다.

## Seed가 틀렸으면 수정하기

목표나 기준이 사용자의 답과 다르면 **실행 전에** 고칩니다. 사용자가 확인하지 않은 제안은 자동으로 적용하지 마세요. 현재 제품 skill은 생성 도구를 다시 호출해 Seed를 재생성하지 않도록 안내합니다. 이후 수정은 해당 YAML의 기존 내용을 검토해 직접 편집하고, 이전 평가에서 통과한 기준·키·계보가 새 내용에도 유효하다고 가정하지 않습니다. 다음을 다시 확인하세요.

1. 고친 문장이 사용자 요청과 일치하는지.
2. 다른 필드와 충돌하거나 빠진 기준을 만들지 않았는지.
3. 이미 실행한 작업이 있으면 그 작업이 옛 Seed에 묶여 있는지, 새 Seed로 별도 실행할지.
4. 새 실행이 중복 작업·비용·외부 효과를 내지 않는지.

Seed 모델은 실행 내부에서 불변(frozen)으로 취급되지만, 이는 YAML 파일을 사람이 고칠 수 없다는 뜻이 아닙니다. 실행 중인 작업에 변경을 소급 적용하는 것도 아닙니다. 편집한 파일, 기존 실행 상태와 사용한 실제 ID를 함께 기록하세요.

## 언제 실행으로 넘어가나요? {#run-reviewed-seed}

검토한 Seed가 실제 의도와 맞고 실행할 준비가 됐을 때만, 같은 host 대화에서 다음을 요청합니다.

```text
ooo run
```

호스트가 특정 Seed를 요구하면 방금 검토한 실제 파일 경로나 YAML을 사용하세요. assistant가 다른 경로·이전 버전의 Seed를 고르면 진행 전에 멈춰 수정합니다. 터미널의 독립 CLI 명령은 다른 표면이므로 설치된 버전의 `ouroboros run --help`를 먼저 확인하고, CLI 경로는 [첫 실행](/docs/first-run-detail/) 및 [명령 색인](/docs/cli-reference-detail/#ouroboros-run)을 따릅니다.

실행 뒤에는 반환 ID를 기록하고 실제 파일 변경, 테스트 출력, 각 수용 기준의 평가 근거를 대조합니다. 작업 시작·종료 표시, `job_id`, `seed_ready`, QA score, 등급 또는 “완료” 텍스트만으로 요청 달성을 판단하지 않습니다. 실패·중단·불명확한 작업은 새로 시작하기 전에 [진행상태](/docs/progress-detail/)와 [복구 절차](/docs/recovery-detail/)를 보고 기존 프로세스와 외부 효과를 확인하세요.

## 분기와 문제 해결

- **Seed YAML이 반환되지 않았어요.** 생성 성공을 추측하거나 YAML을 만들어 내지 마세요. 오류·상태와 실제 `session_id`를 확인하고 인터뷰가 끝났는지 봅니다. 누락 기준 질문이 오면 답을 받은 다음 생성 요청을 다시 검토합니다.
- **인터뷰 점수 제한으로 생성되지 않았어요.** 누락된 목표·제약·검증 기준을 보충하거나 사용자의 의도를 다시 묻습니다. 의식적인 위험 수용 없이 `force`를 선택하지 않습니다.
- **인터뷰 세션을 찾지 못했어요.** 호스트 plugin과 독립 CLI의 저장소가 같다고 가정하지 말고, 실제 응답의 session ID와 어느 서버에 연결됐는지 확인하세요.
- **QA가 `REVISE` 또는 `FAIL`을 줬어요.** 현재 제품 skill에서 QA는 자문이며 결과를 자동 수정하지 않습니다. 제안을 원래 답·요청과 대조하고 원하는 수정만 직접 반영합니다.
- **YAML을 고친 뒤 실행이 이미 시작됐어요.** 기존 실행 상태와 결과가 어떤 Seed에 묶였는지 확인한 뒤 다음 행동을 정합니다. 중복 실행하지 않습니다.
- **도구가 위임됐거나 응답이 끊겼어요.** 영수증만으로 완료로 보지 않습니다. 반환된 작업·세션 ID로 host 상태를 확인하고 실제 YAML 또는 오류를 받습니다.

[Seed MCP 입력·결과 참조](/docs/mcp-reference-detail/#ouroboros_generate_seed)와 [첫 실행부터 결과 확인](/docs/first-run-detail/)을 이어서 보세요. 이 안내 작성에서 실제 host skill, MCP 서버, 모델 생성, 로컬 YAML 저장·편집 또는 프로젝트 실행을 하지 않았습니다. 사용자의 예시는 실제 생성 출력이 아니며, 위 YAML은 읽기 설명용 합성 자료입니다.
