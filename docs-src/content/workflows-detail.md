# 목적에 맞는 워크플로 선택

기준: 2026-11-04 [upstream 722172ef](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 아래 `ooo` 예시는 **지원되는 호스트 대화용 요청**이며 독립 터미널 CLI의 구문과 같다고 가정하지 않는다. 예시는 실제 실행 결과가 아니다. 모델과 도구 호출, 반복에는 비용·시간 및 작업 공간 변경이 발생할 수 있다.

**판본·확인 범위:** 이 안내는 위 고정 722판의 사용자 흐름과 링크된 스킬·핸들러를 설명한다. 링크된 source 파일을 2026-11-07 기준 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 release `v0.59.9`와 정적으로 비교했을 때 해당 인용 경로에서 차이는 발견하지 못했다. 이는 인용한 파일의 비교이지 전체 배포판, 간접 런타임·도구 계약, 호스트별 스키마나 동작의 완전한 동등성 검증이 아니다. 실제 호스트 대화·모델·외부 효과는 문서에서 실행하지 않았다. 설치된 호스트의 스킬, 도구 목록, 입력 스키마를 확인하고 ID별 작업 상태·복구는 [진행 상태](/docs/progress-detail/), [복구](/docs/recovery-detail/) 상세를 함께 본다.

| 상황 | 시작점 | 성공으로 보기 전 확인 |
| --- | --- | --- |
| 실제 작업 전에 짧게 과정을 배워 보고 싶음 | `ooo tutorial` | 대화에서 만든 요약은 연습용 Mini-Seed이며 실행 가능한 Seed 파일이 아니다. |
| 요구가 모호하거나 만들 범위를 정해야 함 | `ooo interview` → `ooo seed` | 인터뷰 종료와 Seed 생성은 별개다. 생성된 목표·범위·제약·수용 기준을 읽는다. |
| 여러 파일에 걸친 작업을 명세부터 실행·검증까지 진행 | `ooo auto` | 시작 영수증은 완료가 아니다. 실제 job 및 이어지는 작업의 최종 상태·결과를 확인한다. |
| 이미 검토한 Seed가 있음 | `ooo run [실제 Seed 경로]` | 결과의 실행·평가 및 이어지는 작업 상태와 산출물을 확인한다. 기존 Seed가 있으면 auto의 goal 문자열에 경로를 쓰는 것만으로 기존 계보가 연결되지 않는다. |
| 완성된 작업이 기준에 맞는지 정식 평가 | `ooo evaluate [실제 실행 세션 ID]` | 사용한 검사와 관찰한 동작, 각 수용 기준 및 최종 판정을 읽는다. 평가만 원하면 자동 수정 반복을 끄도록 명시한다. |
| 산출물의 빠른 품질 검토 | `ooo qa [실제 파일 경로]` | 단일 품질 판정은 실행 세션의 정식 3단계 평가와 다르다. 동작을 실제로 관찰했는지 구분한다. |
| 목표를 세대별로 개선·검증 | `ooo evolve` 또는 기존 lineage에 `ooo ralph` | lineage와 실행 세션 ID를 구분하고 실제 종료 이유와 각 세대의 근거를 확인한다. |
| 제품 요구사항 문서가 필요 | `ooo pm` | 질문에 대한 사용자의 답과 도구가 만든 PRD를 검토한다. PRD 작성은 구현 완료가 아니다. |
| 같은 장애가 반복되거나 중요한 선택에 다각도 분석이 필요 | `ooo unstuck` | 관점·근거·제안과 실제로 확인된 결과를 분리한다. |

## 짧은 대화형 튜토리얼

호스트 대화에서 직접 `ooo tutorial` 또는 `/ouroboros:tutorial`을 요청한다. [고정 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/tutorial/SKILL.md)은 사용자의 아이디어에 관해 짧게 질문하고, 답을 목표·제약·수용 기준의 **Mini-Seed**로 정리한 뒤 Interview → Seed → Execute → Evaluate의 관계와 다음 선택을 설명한다. 아이디어가 없다면 작업 관리 CLI 예제를 사용하도록 안내한다. 약 5분은 안내상의 목표 시간이지 보장된 실행 시간은 아니다. 이 스킬은 명시적으로 호출하는 호스트 스킬이며 독립 터미널의 `ouroboros tutorial` 명령이 아니다.

Mini-Seed는 설명용 대화 요약이다. 모호도 점수나 실제 Seed 파일이 자동 생성됐다고 가정하지 않는다. 실제 프로젝트에 적용하려면 `ooo interview`로 요구를 구체화하고 `ooo seed` 결과를 검토한 다음 실행을 선택한다. 실행·평가·진행 조회에는 해당 호스트의 MCP 연결이 필요하며 [설치와 연결](/docs/setup-host-detail/)을 먼저 확인한다. 튜토리얼에서 명령을 소개하는 것과 그 명령을 실제로 실행한 것은 다르다. 위 안내는 고정 스킬 지침을 읽은 결과이며 실제 호스트 대화는 이 문서에서 시험하지 않았다.

## 예제 1: 큰 작업을 자동으로 시작

호스트에서 아래처럼 프로젝트를 열고 목표·제약·필요한 결과를 말한다.

```text
ooo auto "기존 작업 목록 앱에 검색 기능을 추가하고 기존 테스트와 새 검색 테스트를 확인해 줘. 외부 배포는 하지 마."
```

[auto 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/auto/SKILL.md)의 계약은 인터뷰·Seed·검토를 거쳐 실행을 인계하는 백그라운드 파이프라인이다. 받은 `job_id`와 `auto_session_id`를 보존하고, `detached`, `blocked`, `failed` 또는 최종 결과를 구분한다. 인계가 끝났다는 사실은 앱이 요구대로 동작한다는 증거가 아니다. 해당 스킬은 실제 MCP 시작 도구가 없을 때 수동으로 비슷한 일을 해 놓고 `ooo auto` 성공으로 부르지 않도록 한다. 기존 Seed를 실행할 때는 `ooo run`을 사용한다.

## 예제 2: 기존 실행의 평가만 요청

```text
ooo evaluate [실제로 받은 실행 세션 ID]
수정 반복은 시작하지 말고 이 작업의 결과와 수용 기준만 평가해 줘.
```

호스트는 실제 세션·산출물·원본 Seed와 프로젝트 경로를 확인한 뒤, 평가만 원한다는 선택을 `auto_evolve: false`로 전달할 수 있다. MCP 백그라운드 평가의 기본 자동 진화는 `final_approved: false`일 때 Ralph 등록을 시도하며, 거부뿐 아니라 `unverified`도 포함한다. Seed를 불러오지 못하거나 등록이 실패하면 시작되지 않을 수 있으므로 연결된 job·skip·오류를 확인한다. 실제로 실행된 기계적 검사가 없으면 `unverified`이며, 의미 평가나 합의의 긍정적 의견만으로 승인되지 않는다. 독립 CLI `ouroboros qa`에서 평가 대상·참조·Seed 값을 파일 경로로 쓸 때는 실제 일반 파일이 존재하는지 먼저 확인한다. 없는 경로나 디렉터리는 오류가 아니라 문자 그대로 평가에 전달될 수 있다. 고정 소스의 입력 해석 함수를 임시 디렉터리에서 시험한 결과 일반 파일은 내용으로 읽혔고 없는 경로와 디렉터리는 원래 문자열로 반환됐다. 이는 함수 수준 시험이며 QA 명령 전체나 모델 호출의 성공을 확인한 것은 아니다. 독립 CLI의 `ouroboros seed`는 생성 중 키보드 인터럽트에도 종료 코드 0을 반환하므로 출력된 경로와 파일을 확인한다. 모델 평가는 행동 관찰을 대체하지 않는다. [evaluate 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evaluate/SKILL.md), [평가 구조](/docs/architecture-detail/).

## 예제 3: 세대별 개선과 반복

`ooo evolve`는 인터뷰와 Seed 뒤 lineage를 만들고 한 세대씩 진행한다. 기본 실행 경로에서는 각 세대의 실행과 평가가 포함된다. `ontology_stable`은 수렴 성공이 아니며, `converged`, `stagnated`, `exhausted`, `failed`를 구분해야 한다. 상태 조회는 세대를 실행하거나 반복을 자동 재개하지 않는다. 다만 lineage 상태 핸들러는 EventStore를 초기화하므로 파일이나 스키마 생성이 없다고 가정하지 않는다. 종료된 세대를 되감는 `rewind`는 이후 세대를 잘라내므로 대상과 영향을 확인한다. [evolve 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evolve/SKILL.md).

`ooo ralph --lineage-id [실제 lineage ID]`는 MCP가 소유하는 반복 작업을 시작·관찰하는 경로다. 기본 세대 상한은 10이며 성공·수렴뿐 아니라 실패·취소·상한 도달로도 멈출 수 있다. 이미 존재하는 lineage를 이어갈 때와 새 Seed로 새 lineage를 시작할 때를 구분한다. lineage ID는 평가에 필요한 실행 세션 ID가 아니다. 백그라운드 job이나 플러그인 위임의 결과를 확인하기 전에는 완료를 보고하지 않는다. [ralph 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/ralph/SKILL.md).

## 제품 요구사항과 기존 저장소

`ooo pm`은 코드 구현이 아닌 제품 요구사항을 위한 인터뷰다. 호스트는 `ouroboros_pm_interview`가 반환한 질문에 사용자의 답을 받아 전달하고, 질문이 여러 개면 각 질문과 답을 한 번에 묶는다. 응답의 `meta.is_complete`와 생성 실패 여부를 확인한 다음 생성된 PRD와 PM Seed 경로를 검토한다. **PM Seed는 바로 실행할 Seed가 아니다.** 실행 명세를 만들려면 스킬이 안내하는 `ooo interview <실제 PM Seed 경로>` 다음 `ooo seed` 경로를 따른다. PM 도구가 없는 경우 해당 스킬은 임의의 직접 Python 대체를 금지하고 지원 호스트 설정 후 재시도하도록 안내한다. [PM 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/pm/SKILL.md), [MCP 입력](/docs/mcp-reference-detail/#ouroboros_pm_interview).

PM 인터뷰 완료 시 고정 구현은 PM Seed를 저장한 다음 현재 작업 디렉터리의 `.ouroboros/pm.md`를 작성한다. 같은 디렉터리의 다른 PM 세션이나 완료된 세션의 생성 재시도도 같은 `pm.md`를 **덮어쓸 수 있다**. 시작과 재시도 전에 기존 파일과 작업 디렉터리를 확인하고 필요한 내용은 안전한 곳에 보존한다. 두 파일 저장은 하나의 원자적 작업이 아니므로 문서 저장 실패 후 Seed만 남을 수도 있다. 생성 또는 저장 실패 응답은 `is_error=false`, `meta.is_complete=true`이면서 `meta.generation_failed=true`일 수 있다. 응답의 실패 표시와 두 산출물의 경로·내용을 확인한다. 완료된 세션의 생성 실패는 안내된 `action="generate"`와 `session_id`로 재시도할 수 있지만, 모델을 다시 호출하고 기존 산출물을 덮어쓸 수 있으므로 비용과 파일 영향을 먼저 확인한다. [PM 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/pm_handler.py), [문서 저장 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/pm_document.py). 이 설명은 소스 확인이며 실제 모델 생성이나 재시도를 시험하지 않았다.

### 독립 CLI의 PM 인터뷰

호스트 스킬과 별도로 고정 source에는 터미널에서 실행하는 `ouroboros pm`이 있다. 새 인터뷰는 `ouroboros pm`, 기존 세션은 `ouroboros pm --resume <PM 세션 ID>`로 시작한다. `--output <디렉터리>`는 사람이 읽을 `pm.md`의 위치를 바꾸며 생략 시 **실행 당시 현재 디렉터리**의 `.ouroboros/`를 사용한다. `--model`, `--pin-models`/`--no-pin-models`, `--debug`는 모델 선택·고정·로그에 영향을 준다. `--output`이 PM Seed나 인터뷰 상태의 저장 위치까지 바꾼다고 가정하지 않는다.

이 CLI는 새 인터뷰를 시작할 때 등록된 brownfield 저장소가 있으면 저장소 근거를 전달할 수 없으므로 진행을 거부한다. 재개할 때는 현재 등록 목록 대신 불러온 세션 상태와 PM 메타데이터의 저장소 관련 정보를 검사하며, 해당 기록이 brownfield이면 재개를 거부한다. 기존 등록을 임의로 해제하지 말고 해당 프로젝트의 근거가 필요하면 위의 호스트 `ooo pm` 경로를 사용한다. 인터뷰는 모델 호출과 로컬 상태 저장을 수반한다. 완료되고 답변한 라운드가 있을 때 PM Seed와 `pm.md`를 생성하며, 같은 출력 디렉터리의 기존 `pm.md`를 덮어쓸 수 있다. 생성 후 개발 인터뷰로 바로 이어갈지 묻고 기본 선택은 **Yes**이므로 원치 않으면 명시적으로 거절한다. PM Seed는 실행 가능한 최종 Seed가 아니다. 인터럽트 시 CLI는 종료 코드 0을 반환하므로 종료 코드만으로 산출물 생성 성공을 판정하지 말고 출력 경로와 파일 내용을 확인한다. [독립 CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/pm.py), [문서 저장 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/pm_document.py). 고정 소스와 격리 HOME의 `ouroboros pm --help`를 확인했으며 실제 PM 인터뷰·모델·이어지는 개발 인터뷰는 시험하지 않았다.

`ooo brownfield`는 기존 저장소를 인터뷰 문맥으로 등록·선택하는 호스트 워크플로다. 목록과 `find <주제>`는 등록 DB를 조회하며 파일시스템을 다시 걷지 않는다. `scan`은 기본적으로 홈을 최대 두 디렉터리 단계까지 훑고 숨김·잡음 디렉터리는 건너뛰며, 발견한 worktree만 등록하고 다른 위치의 worktree 계열을 자동 확장하지 않는다. 새로 추가하거나 이동한 저장소는 필요할 때 다시 scan하고, 검색 누락을 디스크에 저장소가 없다는 증거로 해석하지 않는다. `set <번호>`는 기본 저장소 목록을 교체하므로 기존 선택을 확인한다. `detect`는 모델 호출로 `.ouroboros/mechanical.toml`을 작성하므로 비용과 파일 변경이 발생할 수 있다. [brownfield 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/brownfield/SKILL.md), [MCP 입력](/docs/mcp-reference-detail/#ouroboros_brownfield), [기존 프로젝트 적용](/docs/existing-project-detail/).

## Seed를 GitHub 이슈로 게시

`ooo publish <실제 Seed 경로>`는 독립 CLI가 아닌 호스트 스킬이며, 인증된 `gh` CLI와 유효한 Seed 및 쓰기 가능한 대상 저장소가 필요하다. 스킬은 저장소와 Seed ID에 대한 기존 이슈를 확인하고 Epic과 작업 이슈 계획을 보여 준 뒤 게시 여부를 묻는다. 승인된 범위에서 진행하면 새 Epic·Task 이슈와 필요한 라벨을 만들고 Epic에 작업 체크리스트 댓글도 남긴다. 이는 **외부 쓰기**이며 취소 전 확인 단계와 생성된 결과를 구분해야 한다. 자동 중복 검색의 결과가 모든 중복의 부재를 보장한다고 가정하지 않는다. 비공개 Seed의 공개 저장소 게시 여부와 공유 가능한 내용을 먼저 확인한다. 이 안내에서는 게시를 실행하지 않았다. [publish 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/publish/SKILL.md).

## 막힌 문제와 어려운 선택: unstuck / lateral

같은 해결책이 반복 실패하거나 되돌리기 어려운 선택에 명확한 우열이 없을 때 호스트 스킬 `ooo lateral`을 사용할 수 있다. 이는 독립 `ouroboros lateral` CLI 명령이 아니다. `ooo lateral architect`는 한 관점을, `ooo lateral debate hacker architect contrarian`은 지정된 여러 관점을 요청한다. 스킬의 `ooo lateral` 또는 `ooo lateral @all`은 다섯 관점 토론이다. 다섯 이름은 `hacker`, `researcher`, `simplifier`, `architect`, `contrarian`이며 잘못된 이름은 조용히 대체하지 않는다. 일반 진행 중인 작업이나 첫 번째 오류에 자동 적용하는 기능은 아니다. [unstuck 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/unstuck/SKILL.md).

호스트는 실제 문제와 시도한 접근을 모아 `ouroboros_lateral_think`를 호출한다. 선택 문제에서는 `mode: "decision"`을 사용하고 옵션과 현재 선호안을 각각 `problem_context`, `current_approach`에 전달한다. 선호가 없으면 `current_approach: "undecided"`를 쓸 수 있다. 예를 들어 다음은 MCP **인자 객체**이며 CLI 명령이나 실행 결과가 아니다.

```json
{
  "problem_context": "기존 배포의 장애 복구를 위해 관리형 DB와 자체 운영 DB 중 선택",
  "current_approach": "undecided",
  "mode": "decision",
  "personas": ["architect", "researcher", "contrarian"],
  "research": false
}
```

두 필수 문자열이 없거나 비면 오류다. `personas`가 단일 `persona`보다 우선하며, 도구의 decision 모드에서 둘 다 생략하면 다섯 관점 토론을 선택한다. 일반 unstuck 모드에서 개별 관점을 생략할 때는 스킬이 알려진 정체 패턴을 전달해 선택하게 한다. `research: true`는 명시적 연구 요청에서만 사용하는 선택이며, 런타임에 웹 도구가 없으면 의견만으로 축소될 수 있다. 반드시 외부 근거를 수집했다는 뜻이 아니다. [도구 스키마](/docs/mcp-reference-detail/#ouroboros_lateral_think), [모드 계약](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/lateral_decision.py).

응답은 호스트와 실행 방식에 따라 단일 프롬프트, 플러그인의 `_subagents`, 또는 표시용 텍스트와 구조화 dispatch를 포함한 inline 결과로 달라진다. 여러 관점 요청만으로 실제 병렬 실행이나 완료를 보장하지 않으며 호스트가 dispatch를 수행하고 모든 결과를 기다려야 한다. 표시 텍스트를 `---`로 나눠 결과를 복원하지 않는다. decision 결과는 한 가지 추천·근거·가장 강한 반론·추천이 바뀔 조건으로 종합하고 실제로 확인한 출처만 인용한다. 사용자가 선택을 받아들인 뒤 결정 기록을 제안할 수 있으나 `ouroboros_record_conductor_decision`은 기록이지 자동 실행의 증거가 아니다. 모델·하위 에이전트·웹 도구 사용에는 해당 환경의 권한과 비용 조건이 적용된다. 이 예제는 고정 소스와 대역 테스트를 근거로 하며 실제 호스트 토론이나 모델 호출은 실행하지 않았다. [핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/lateral_think_handler.py), [결정 기록 경계](/docs/synapse-detail/).

## 사용 전에 확인할 공통 정보

- 프로젝트 경로와 기존 변경, 사용 가능한 런타임·도구, 외부 효과의 허용 범위를 확인한다. 플러그인이나 워크트리 격리가 항상 있다고 가정하지 않는다. `ooo run`은 기본적으로 작업 worktree를 사용하도록 요청한다. 응답의 `worktree_path`와 `worktree_branch`는 실제 작업 경로와 branch를 확인하는 단서이며, 그 자체가 운영체제·네트워크·도구 권한의 보안 격리를 증명하지 않는다.
- 실제 수용 기준, 검사 명령·작업 경로, 필요한 모델과 제한을 제공한다. 자동 검증을 지시하는 것과 결과를 실제로 확인한 것은 다르다.
- 받은 job·실행 세션·lineage ID를 섞지 않고 기록한다. 시작·진행·종료·승인·산출물 사용은 서로 다른 상태다. [진행상태](/docs/progress-detail/)와 [복구](/docs/recovery-detail/)를 사용한다.
- 예제의 명령과 도구 이름은 고정 버전의 스킬을 요약했다. 설치된 버전의 도구 스키마, 호스트 연결 및 권한·비용 범위를 실제 실행 전에 확인한다. 이 페이지의 예제들은 문서 설계 사례이며 실모델 호출로 확인하지 않았다.
