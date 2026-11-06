# Seed YAML: 명세 읽기와 작성

!!! warning "판본과 검증 범위"
    이 안내의 상세 동작은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 설치된 플러그인과 호스트 MCP 서버는 별도 판본입니다. 아래 합성·대역 시험은 표시된 조건에 한정되며 실제 모델·인증·모든 호스트의 동작을 증명하지 않습니다. 설치한 버전의 도움말과 [제품 시작 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조하세요. 구판 동작이 현재 설치에도 같다고 가정하지 않습니다.


기준: 2026-11-04, Ouroboros 소스 [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지는 [Seed 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py), [CLI YAML 로더](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py)와 [원본 작성 가이드](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/seed-authoring.md)를 대조했다. 직접 작성은 고급 경로다. 보통 요구를 정리하고 인터뷰·Seed 생성 결과를 검토한다. 설치된 버전이 다르면 그 버전의 스키마와 도움말을 확인한다.

Seed는 목표·제약·수용 기준을 실행과 평가의 기준으로 기록한다. 파일 파싱에 성공한 사실은 요구의 정확성, 실행 승인, 테스트 성공을 뜻하지 않는다. 실행 전 실제 프로젝트 경로·기존 변경·모델 비용·외부 효과를 검토한다. 아래 YAML은 **형식 예시**이며 이 문서를 작성하면서 모델이나 작업 실행에 사용하지 않았다.

!!! warning "공개 패키지 0.59.9와의 차이"
    아래 예시와 `verify_cwd` 설명은 위 고정 커밋 기준입니다. 2026-11-04 시험한 PyPI `ouroboros-ai==0.59.9`의 설치 파일에는 수용 기준 모델의 `verify_cwd` 필드가 없고, 실행기에도 고정 커밋의 동일한 작업 디렉터리 바인딩 경로가 없습니다. 따라서 이 예시를 해당 패키지에서 실행해 지정 디렉터리에서 검증된다고 가정하지 마세요. 자신의 설치본 스키마·소스와 실행 경로를 확인하고, 검증 명령의 실제 작업 디렉터리와 외부 효과를 안전한 임시 프로젝트에서 별도로 시험하세요. 합성 수용 기준 하나를 각 모델로 검증·직렬화했을 때 고정 소스는 `verify_cwd: app`을 보존했고 설치본은 해당 필드를 결과에서 제거했습니다. 별도 합성 YAML 한 사례에서 두 판본의 CLI 로더는 raw 필드를 읽었지만, 이어지는 Seed 모델 변환·직렬화에서 설치본은 필드를 제거했습니다. 이어 별도 합성 프로젝트에서 각 판본의 AC 검증 게이트로 `pwd`를 실행했을 때 고정 소스는 `app`, 설치본은 프로젝트 루트에서 실행됐습니다. 이 시험은 workspace digest와 동시 작업 판단을 대역 처리한 한 사례이며 실제 CLI 전체 실행·파일시스템 보안은 검증하지 않았습니다. [판본과 검증 범위](/docs/version-guide/#version-scope).

## 완전한 형식 예시

```yaml
goal: "오프라인 작업 목록 도구의 핵심 동작을 구현한다"
task_type: code
constraints:
  - "외부 네트워크 서비스를 사용하지 않는다"
  - "사용자의 기존 파일을 삭제하지 않는다"
acceptance_criteria:
  - description: "작업 추가와 목록 조회의 정상 및 빈 목록 사례가 통과한다"
    verify_command: "python -m unittest discover -s tests"
    verify_cwd: "."
    expected_artifacts:
      - "tasks.py"
      - "tests/test_tasks.py"
  - "사용자가 도구의 설치와 사용 방법을 README에서 찾을 수 있다"
ontology_schema:
  name: "TaskList"
  description: "로컬 작업과 상태를 표현하는 도메인"
  fields:
    - name: "task"
      type: "entity"
      description: "제목과 상태가 있는 작업"
      required: true
evaluation_principles:
  - name: "correctness"
    description: "관찰한 동작이 각 수용 기준에 부합한다"
    weight: 1.0
metadata:
  seed_id: "example_task_list_001"
  ambiguity_score: 0.1
```

고정 소스의 CLI YAML 로더와 `Seed.from_dict`로 이 예시를 파싱해 두 수용 기준과 첫 번째 검증 명령·작업 디렉터리·산출물 경로의 보존을 확인했다. 두 번째 문자열 기준에는 `verify_command`가 없으므로 이 예시 자체에 그 기준을 기계적으로 검사하는 명령은 지정되어 있지 않다. 파싱 성공은 검증이나 구현 완료가 아니다. 이 시험은 모델·검증 명령·작업 실행 없이 격리된 합성 파일을 사용했고 기존 가상환경의 의존성은 고정 lock과 일치하는지 확인하지 않았다.

위 테스트 명령과 파일 경로는 가상의 프로젝트를 설명한다. 현재 디렉터리에 해당 파일이 있다고 가정하거나 검증 명령을 그대로 실행하지 않는다. 검증 명령은 실제 실행 중 코드와 셸 작업을 수행할 수 있으므로 실행 전에 내용과 작업 위치를 확인한다. 이 판본의 기본 orchestrator에서 `--dry-run`은 실행을 차단하지 않는다. [첫 실행의 경고](/docs/first-run-detail/)를 먼저 읽는다.

## 인터뷰 없이 MCP로 생성한 Seed의 범위

`ouroboros_generate_seed`에 `session_context`를 전달하는 경로는 모델 없이 입력을 구조화한다. `goal`과 적어도 하나의 비어 있지 않은 `acceptance_criteria`가 없으면 도구는 오류가 아닌 `gap_questions_required`를 반환하며 Seed는 생성되지 않는다. 이 게이트는 **내용의 정확성이나 기준을 실제로 검증할 수 있는지 검사하지 않는다**. 입력에는 이미 합의된 표현을 넣고 결과를 검토한다. [MCP 호출과 응답 구분](/docs/mcp-reference-detail/)을 함께 본다.

고정 소스에서는 `goal`, `acceptance_criteria`, `constraints`, `decisions`, `project_type`만 이 경로에서 읽고, 알 수 없는 키는 무시한다. 앞뒤 공백은 제거하며 `decisions`는 `constraints` 뒤에 합쳐 중복을 제거한다. `project_type`이 `greenfield` 또는 `brownfield`가 아니면 `greenfield`로 대체한다. `metadata.ambiguity_score`에는 입력으로 계산한 점수가 아니라 고정된 `0.2` 상한이 기록된다. 따라서 숫자만 보고 인터뷰가 평가됐거나 요구가 충분히 명확하다고 판단하지 않는다. 세부 입력 타입·정규화는 [생성 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/session_seed.py)과 [핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/session_seed_handler.py)를 기준으로 확인한다. 이 내용은 고정 소스 대조이며 모든 입력 조합과 실제 모델 실행을 검증한 것은 아니다.

## 필드와 모델의 경계

| 필드 | 고정 모델의 입력과 의미 |
| --- | --- |
| `goal` | 필수 문자열이며 최소 길이 1. 사람은 공백이 아닌 구체적인 목표와 범위를 적고 실제 요구와 일치하는지 검토한다. |
| `ontology_schema` | 필수 객체. `name`과 `description`은 최소 길이 1인 문자열이며 `fields`는 생략 가능하다. 각 필드는 `name`, `type`(또는 `field_type`), `description`, 선택적 `required`를 받는다. 이는 도메인을 설명하는 렌즈이며 그 자체가 반드시 산출물의 출력 스키마라는 뜻은 아니다. |
| `metadata` | 객체 자체는 필수다. 모델에서 `seed_id`, `version`, `created_at`, `ambiguity_score`는 기본값을 갖고 점수는 0~1 범위다. 생성 경위와 미해결 내용을 기록하는 선택 필드도 있다. 점수는 정확성·승인의 증명이 아니다. `degraded`, `generation_mode`, `unresolved_slots`에는 조합 제약이 있다. |
| `acceptance_criteria` | 문자열 목록 또는 아래 구조화 객체 목록. 모델에서는 생략·빈 목록도 허용한다. **실제 작업에는 검증 가능한 기준을 쓰는 것이 중요하다.** 원본 가이드 맨 위는 필수라고 적지만 뒤의 필드 설명은 스키마에서 강제하지 않는다고 하며, 고정 모델은 후자와 같다. 빈 목록이 유용한 작업이나 품질을 보장하지 않는다. |
| `task_type` | 기본 `code`. 내장 값은 `code`, `research`, `analysis`, `artifact`, `document`, `documentation`, `presentation`; 다른 식별자는 생성 전에 전략 레지스트리에 등록돼 있어야 한다. |
| `constraints` | 선택적인 문자열 목록. 지켜야 할 제한을 구체적으로 적는다. |
| `evaluation_principles`, `exit_conditions` | 선택적인 평가 원칙과 종료 조건. 전자는 `name`, `description`, 0~1의 `weight`(기본 1), 후자는 `name`, `description`, `criteria`(또는 `evaluation_criteria`)를 받는다. 모델은 문자열 목록도 변환한다. 자연어 종료 조건을 적었다는 사실만으로 외부 효과나 비용 한도가 자동 강제된다고 가정하지 않는다. |
| `brownfield_context` | 선택적인 기존 프로젝트 문맥. 실제 작업 경로·읽기 전용 참고 경로와 기존 변경은 별도로 확인한다. |

`metadata.seed_id`를 YAML에서 생략하면 모델은 파싱할 때마다 새 ID를 생성한다. `created_at`을 생략해도 파싱 시각이 새로 생성된다. 같은 파일을 다시 읽어도 같은 식별자·생성 시각이 보장되지 않으므로 여러 명령이나 재개·계보에서 동일 Seed를 추적해야 한다면 확인한 값을 YAML에 명시해 보존한다. 명시적 빈 ID의 허용 여부는 사용하는 소비 경로마다 다를 수 있으며, [Workflow IR 검사](/docs/workflow-ir-detail/)는 빈 문자열과 공백을 거부한다. [Seed metadata 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py). 이 설명은 고정 소스와 Workflow IR의 격리 CLI 시험에 근거하며 모든 소비 경로의 재개 동작을 뜻하지 않는다.

모델의 `assumptions`는 미확인 가정이며 `requester_answers`와 `repo_facts`는 각각 요청자 답과 저장소 증거를 기록한다. `open_questions`는 기록에 남지만 실행 프롬프트에는 렌더링되지 않는다고 소스에 명시돼 있다. `ooo auto`의 `sourced_scope`가 있는 경우 worker에 전달하는 범위가 달라진다. 이 필드를 임의로 추가해 근거 없는 요구나 가정을 확정하지 않는다. 모델은 추가 필드를 허용하므로 **오타가 항상 오류가 되는 것은 아니다**. 알려진 키의 철자와 실제 소비 경로를 확인한다.

**출처가 지정된 Seed의 실행 계약:** Python의 [`SeedContract.from_seed`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed_contract.py)는 `sourced_scope`가 없을 때 일반 Seed의 목표·기준·제약·온톨로지 등을 계약으로 읽는다. `sourced_scope`가 있으면 해당 범위의 목표·제약·기준과 요청자 답변·저장소 근거를 사용하고, 모델이 작성한 온톨로지·가정·평가 원칙·종료 조건은 이 계약에서 제외한다. 출처 범위의 완료 기준이 빈 경우에는 고정 문구 `Resolve the request as stated in the goal.`을 대체 목표 기준으로 넣는다. **원본 Seed의 모델 작성 필드가 삭제되는 것은 아니며**, 이 계약 생성만으로 실제 실행·검증이나 출처의 진실성이 보장되는 것도 아니다. 고정 source의 문서 예제 Seed와 합성 `sourced_scope`를 사용해 일반 계약의 기준 2개, 빈 출처 기준의 대체 문구, 온톨로지 제외 및 원본 Seed 필드 보존을 확인했다. 실제 모델·호스트·평가 흐름은 미검증이다. 재현


## 구조화 수용 기준

각 항목의 `description`은 필수이며 빈 문자열과 공백만 있는 값은 거부된다. 기존 문자열 기준도 허용되고 내부 구조로 변환된다. 선택 필드는 다음과 같다.

- `verify_command`: 해당 기준의 증거를 얻는 명령. 실제로 실행될 수 있으므로 신뢰할 수 있는 명령만 선택한다. 작성만으로 명령 실행·성공이나 요구 충족을 뜻하지 않는다. 고정 runner의 한 합성 단일 기준 사례에서는 명령 표식 없이 완료 상태가 나왔다. [조건과 시험 범위](/docs/progress-detail/)를 확인하고 실제 명령 실행·결과를 별도 증거로 대조한다.
- `verify_cwd`: 명령을 실행할 작업공간 상대 디렉터리이며 `verify_command`가 있어야 한다. `.`은 루트다. 빠진 경로·이탈·심볼릭 링크 등은 유효한 검증 근거를 제공하지 못할 수 있다. 생략 시 특정 Node 명령은 유일한 중첩 프로젝트를 추론하는 등 별도 규칙이 있다. [원본 작업 디렉터리 규칙](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/seed-authoring.md#verification-working-directory).
- `expected_artifacts`: 작업공간 **상대** 파일·디렉터리의 정확한 경로 목록. 설명용 이름이나 glob이 아니라 존재 여부를 확인할 실제 경로다. 절대경로·`..`·백슬래시 등 이식 불가능한 경로는 거부된다. 최상위 이름에 공백이 있으면 `./`로 시작한다. 이 경로는 `verify_cwd`가 아니라 작업공간 루트 기준이다.
- `output_assertion`: 명령의 표준 출력과 표준 오류 결합 결과에 필요한 리터럴 문자열이며 `verify_command`가 필요하다. 단순 성공·종료 0 의미의 일부 문구는 별도 리터럴 검사로 남지 않는다.
- `verify_exemption_reason`: 명령을 둘 수 없는 해당 기준의 사유. `verify_command`와 함께 쓸 수 없다. verify-command 게이트의 `warn`/`block` 정책은 [설정 색인](/docs/config-reference-detail/)을 본다.
- `investment`: 난이도·위험도 등의 선택적 선언이다. 미기재를 낮은 위험의 증거로 삼지 않는다. `semantic_ac_key`는 기준 식별용이며 모델은 누락 시 생성한다. 명세를 수정하면서 이전 키를 무심코 유지하거나 수동 재사용하지 말고 해당 버전의 계보·재개 계약을 확인한다.

**기준 키의 입력 표현과 변경:** 고정 [키 생성과 Seed 검증 코드](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py)는 문자열 기준의 앞뒤 공백을 제거해 설명만 해시하고, 구조화 기준은 설명·검증 명령·산출물·출력 단언과 지정된 경우 작업 디렉터리를 해시한다. 따라서 같은 설명이라도 문자열과 구조화 객체는 같은 키를 보장하지 않는다. `verify_exemption_reason` 등 해시 입력에 없는 필드가 바뀌어도 이 함수가 계산하는 키는 같을 수 있다. 구조화 기준에 이미 명시된 유효 키는 materialize 과정에서 보존되므로 내용을 바꿨다고 자동으로 갱신된다고 가정하지 않는다. 키 일치만으로 의미 동등성이나 이전 검증 결과의 유효성을 판정하지 말고, 명세 변경 시 전체 성공 계약과 계보를 함께 검토한다. 합성 직접 함수 시험에서 공백 정규화·두 표현의 서로 다른 키·명령 변경·면제 이유 제외·명시 키 보존을 확인했다. 이는 모든 생성·재시도 경로의 연결이나 실제 검증 재사용을 시험한 결과가 아니다.


### `investment`가 실행 경로와 재개에 미치는 영향

구조화 기준의 `investment`는 `difficulty`와 `stakes`에 각각 `low`·`medium`·`high`를, `provenance`에 `declared`·`measured`·`inferred`·`absent`를, `confidence`에 `low`·`medium`·`high`를 받을 수 있다. 축이 빠지면 평가 시 미상으로 취급하고, provenance 기본값은 `declared`, confidence 기본값은 `low`다. 소스의 정책은 두 축이 모두 `low`이고 provenance가 `measured`, confidence가 `high`인 완전한 경우에만 노력 수준을 한 단계 낮출 **자격**을 부여한다. 그 외 불충분한 근거는 기본 수준을 보존하며, 어느 한 축이라도 `high`면 최소 `high`를 요구한다. 이는 비용 절감이나 특정 모델·런타임에서의 강제를 보장하는 약속이 아니다. 근거 없이 `measured`를 선언하지 않는다. [모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py), [평가 정책](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/effort_routing.py).

어느 기준에라도 이 메타데이터가 있는 새 Seed는 단일 기준이나 순차 실행이어도 기준별 executor 경로를 사용한다. 순차 선택은 그대로 유지된다. 재개에서 기준별 실행의 소유권을 복원하지 못하는 경로는 `resume_blocked: investment_authority_required`로 차단된다. 이는 **모든 재개가 무조건 차단된다는 뜻은 아니다**. 오류가 나면 실행 ID·실제 상태와 작업 공간을 보존하고 기존 작업이 여전히 실행 중이거나 외부 효과를 냈는지 확인한다. 원본 안내는 차단된 경우 새 실행을 제시하지만, 중복 실행의 비용·외부 효과·미완료 변경을 검토하기 전 자동으로 재시작하지 않는다. [실행과 재개 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py), [원본 작성 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/seed-authoring.md#optional-investment-metadata), [복구](/docs/recovery-detail/).

고정 소스의 모델·라우팅·실행·재개 경로를 독립 대조했다. 관련 기존 대역 테스트에서 runner의 investment 선택 6개와 effort routing 이벤트 13개가 통과했다. 실제 모델 실행, 모든 런타임의 노력 수준 적용이나 운영 재개는 시험하지 않았다.

### 실행 중 검증 게이트와 worker에게 보이는 내용

기본 설정 `execution.run_verify_commands: true`이고 해당 기준별 검증 게이트가 실행되는 경로에서는 `expected_artifacts` 존재와 `verify_command`를 검사한다. 이 설정이 모든 실행 경로에서 게이트가 반드시 실행된다는 보장은 아니다. [단일 기준과 실행 경로의 합성 비교](/docs/progress-detail/)를 확인한다. `false`이면 이 게이트를 건너뛰므로 파일 목록이나 명령을 Seed에 적었다는 사실만으로 검사했다고 판단할 수 없다. 실행 결과에서 실제 게이트·검증 근거를 확인한다. verifier가 실행 불가능한 경우에도 성공이 입증된 것으로 해석하지 않는다. 이 설정은 다른 모든 평가나 외부 도구의 동작을 끈다는 뜻은 아니다. [고정 설정 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md), [게이트 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/parallel_executor.py).

고정 게이트의 `expected_artifacts` 존재 검사는 각 경로를 작업공간 루트 기준으로 해석하고 절대 경로·`..`·작업공간 밖으로 해석되는 경로를 누락으로 처리한다. 임시 작업공간의 합성 함수 시험에서 일반 내부 파일과 내부 파일을 가리키는 심볼릭 링크는 존재로 취급됐고, 외부 파일을 가리키는 링크·끊어진 링크·상위 상대 경로·절대 경로는 누락으로 처리됐다. 이는 검사 시점의 존재 여부에 관한 한 사례이며 파일 내용의 정확성, 검사 뒤 변경이나 심볼릭 링크 경합, 전체 실행 경로의 보안을 보장하지 않는다. [고정 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/verify_gate_outcome.py).

검증 근거가 없거나 불명확하면 신뢰할 수 있는 명령인지와 부작용을 먼저 검토하고, 실제 작업공간의 올바른 `verify_cwd`에서 별도로 실행해 종료 코드와 표준 출력·오류를 보존한다. `expected_artifacts`는 작업공간 루트 기준으로 확인하고 `output_assertion`은 결합 출력과 대조한다. 파일이 만들어졌다는 사실만으로 명령 종료가 성공했다고 판단하지 않는다. 이 수동 확인은 게이트의 작업공간 digest·시간 제한·동시 변경 검사와 동등하지 않으며, 작업 중인 프로세스와 부작용을 먼저 확인해야 한다.

**명시된 명령과 재실행 샌드박스는 서로 다른 경로다.** 이 판본의 Seed `verify_command` 게이트는 작업공간에서 지정 명령을 POSIX 셸에 직접 전달한다. `execution.exec_sandbox`의 verifier replay용 격리가 이 경로에 적용된다고 가정하지 않는다. 작업공간 digest의 실행 전후 비교는 변경된 작업공간에서의 판정을 거부하거나 재검증하기 위한 것이지, 작업공간 밖 쓰기·네트워크 요청을 차단하거나 실행된 부작용을 되돌리는 샌드박스가 아니다. 실행 전 명령과 실제 권한·환경을 확인한다. 이는 소스 경로 대조이며 이번 조사에서 OS 격리를 시험하지 않았다. [셸 호출](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/verify_command_runner.py), [게이트](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/parallel_executor.py).

고정 소스의 atomic worker용 성공 계약 블록은 `expected_artifacts` 이름을 포함하지만 `verify_command`와 `output_assertion`은 의도적으로 숨긴다. 따라서 명령을 Seed에 넣었다는 이유만으로 worker가 그 명령을 봤거나 실행했다고 가정하지 않는다. 이는 이 프롬프트 구성 경로의 설명이며 모든 호스트·런타임의 전체 정보 노출에 관한 보안 보장은 아니다. [프롬프트 구성 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/atomic_prompt_builder.py).

## 수정과 검증

Seed 모델은 `frozen`이며 실행 중 목표·제약·수용 기준을 임의로 바꾸지 않는 계약이다. 이것이 디스크의 YAML을 수정할 수 없다는 뜻은 아니다. 생성 후 수정이 필요하면 요청자의 결정과 근거를 확인해 **기존 YAML을 직접 수정**하고 변경을 검토한다. 고정 [Seed 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/seed/SKILL.md)은 생성 후 수정을 위해 Seed 생성 도구를 다시 호출하지 않도록 안내한다. 이미 시작된 실행이나 계보에 바뀐 명세를 소급 적용했다고 가정하지 말고 별도 실행·재개의 영향을 확인한다.

이번 조사에서는 위 예제를 격리된 Python에서 `yaml.safe_load`와 고정 소스의 `Seed.from_dict`로 파싱하고 `to_dict` → YAML → 재파싱으로 구조가 보존되는지 확인했다. 빈 AC도 모델에서 허용됨을 별도로 확인했다. 이는 스키마·직렬화 시험이며 CLI 전체 실행, 실제 명령·산출물 존재, 모델 호출, 모든 옵션 조합이나 결과 품질을 검증한 것은 아니다. 실제 실행의 [작업 공간](/docs/existing-project-detail/), [검사 패키지](/docs/check-package-detail/), [평가](/docs/evaluation-evolution-detail/)와 [복구](/docs/recovery-detail/)를 함께 확인한다.

**이전 평가와 집중 실행:** 고정 소스의 `select_evolution_focus`는 이전 평가가 부모 Seed의 모든 기준을 정확히 한 번씩 해당 인덱스·내용으로 다루는지 확인하고, 조건에 따라 semantic key도 대조합니다. 평가가 구조적으로 불완전하거나 해당 key가 충돌하면 전체 후보 기준을 다시 활성화합니다. 유효한 이전 평가에 실패 기준이 있을 때, 변경되지 않고 권위 있는 PASS인 기준은 고정하고 실패·변경·추가·이의 제기·회귀된 기준은 활성화합니다. 기준의 동일성 판단은 key만이 아니라 부모와 후보의 전체 기준 객체 비교도 사용하므로, 키가 같아도 다른 필드가 바뀌면 해당 기준은 다시 열릴 수 있습니다. 실패 기준이 없어도 전체 gate가 끝나지 않은 상황은 전체를 활성화합니다. [고정 집중 선택](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/focus.py) · [평가 범위 확인](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/evaluation_coverage.py).

격리된 합성 Seed 두 기준의 직접 함수 시험에서 PASS 하나와 실패 하나는 각각 고정·활성화됐고, PASS 기준의 `verify_exemption_reason`만 바꿔 key를 유지했을 때는 둘 다 활성화됐습니다. 평가의 key를 불일치시키면 범위 검사가 실패하고 둘 다 활성화됐습니다. 이는 선택 함수와 합성 평가 한 사례이며 실제 재개, 명령 실행, 과거 검증의 진실성 또는 모든 key 조합을 검증하지 않습니다.
