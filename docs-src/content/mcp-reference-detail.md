# MCP 도구와 입력 상세 참조

!!! warning "판본과 검증 범위"
    아래 항목과 합성 관찰은 **고정 소스 `722172ef096767583679d04aef5e847458fee6b2`** 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)이나 공개 패키지 `0.59.9`, 실행 중인 호스트 서버에 동일하게 적용된다고 가정하지 마세요. 설치된 CLI 도움말 또는 연결된 서버의 실제 스키마를 우선 확인합니다. 2026-11-07 소스 트리 비교에서 두 커밋 사이 CLI 명령 디렉터리는 `init.py`·`run.py`의 Seed YAML 읽기에 UTF-8 인코딩이 명시됐고, MCP·설정 디렉터리와 제품 CLI·설정·MCP 참조 문서는 변경 파일이 없었습니다. 이는 의존 코드·설치물·런타임 전체의 동등성이나 실제 호스트 실행을 증명하지 않습니다. 현재 [CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [설정 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/config-reference.md), [MCP 도구 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools)를 함께 확인하세요. 전체 현재 CLI·MCP 스키마와 모든 설정 조합은 실사용으로 전수 검증하지 않았습니다.


기준: upstream `722172ef096767583679d04aef5e847458fee6b2`, 2026-11-04. `get_ouroboros_tools(project_dir=임시 경로)`의 기본 핸들러를 격리 환경에서 생성하고 각 정의를 읽었다. 이 목록은 기본 팩토리의 결과로, 실제 서버 조립 시 추가되거나 호스트별로 달라질 수 있다. `required`는 스키마 필수 여부이며 조건부 필수·서로 배타적인 입력 규칙까지 뜻하지 않는다. 실행 전 연결된 서버의 스키마와 각 설명·핸들러를 확인한다. 표의 허용값·배열 항목·수치 범위는 이 서버가 반환한 입력 스키마에 한정하며 다른 조건부 검증은 핸들러를 확인한다. 이 목록을 추출할 때 도구 실행은 검증하지 않았다. 다른 절의 개별 시험은 해당 범위에서만 해석한다. 릴리스 0.59.9와 이 source 서버는 도구 이름 36개가 같지만 `ouroboros_interview`, `ouroboros_qa`의 입력 스키마에 차이가 있었다. 설치된 서버의 스키마를 우선한다.

표의 **스키마 기본값**은 이 판본의 `list_tools` JSON Schema에 명시된 값이다. 필드 생략 시 클라이언트가 값을 삽입하는지, 핸들러가 설정이나 실행 맥락에 따라 어떤 값을 사용하는지는 별도로 확인해야 한다. 스키마 기본값을 실제 모든 호출의 행동으로 일반화하지 않는다.

## 인터뷰에서 Seed 실행까지: 호출별 계약

아래는 고정 source의 기본 핸들러 기준이다. 입력 스키마가 선택으로 표시해도 호출 단계에 따라 필요한 값이 있다. MCP 도구와 CLI 명령은 인터페이스가 다르므로 입력명을 섞지 않는다. 각 도구의 세부 필드 및 다른 모드의 동작은 아래 개별 항목을 함께 확인한다.

| 단계 | 호출과 조건부 입력 | 확인할 결과와 부작용 |
| --- | --- | --- |
| 인터뷰 시작 | `ouroboros_interview`에 `initial_context`를 전달한다. 서버가 응답한 `session_id`는 후속 호출에 사용한다. | 일반 경로는 인터뷰 상태를 만들고 질문을 생성하며 모델 호출이 필요할 수 있다. OpenCode plugin 위임에서는 즉시 받은 `delegated_to_subagent`가 실제 인터뷰 완료가 아니다. |
| 답변 또는 재조회 | 답변은 `session_id`와 `answer`, 재조회는 `session_id`를 사용한다. plugin 자식의 실제 질문을 기록할 때와 서버가 `meta.ask_user_directly=true` 등으로 호스트에 직접 질문을 요청한 경우에는 사용자가 실제로 본 정확한 질문을 `last_question`으로 전달한다. `initial_context`가 남아 있으면 시작으로 분기할 수 있으므로 후속 턴에서 제거한다. | 사용자 답변과 질문의 연결을 확인한다. `calibration_input`은 일반 답변보다 우선해 별도 calibration 경로로 처리되며 대기 질문의 답이 아니다. 중단·복구 상태는 [인터뷰](/docs/interview-detail/)를 따른다. |
| Seed 생성 | `ouroboros_generate_seed`에 인터뷰 `session_id`를 주거나, 인터뷰 없이 확정된 `session_context`의 `goal`과 `acceptance_criteria`를 준다. 둘 다 주면 이 구현은 `session_id` 경로를 택한다. | context 경로는 모델 없이 생성하며 필요한 내용이 부족하면 `gap_questions_required`라는 비오류 결과를 돌려준다. 성공한 `seed_generated`와 구분한다. 인터뷰 경로는 모호성 게이트와 `client_gates` 조건이 적용된다. `force`는 점수 임계값 우회이지 다른 게이트나 모든 검증의 해제가 아니다. |
| 기존 Seed 실행 | `ouroboros_start_execute_seed`에 `seed_content` 또는 `seed_path`를 준다. `session_id` 재개에도 Seed 입력이 필요하고 둘 다 있으면 내용이 우선한다. `cwd`는 상대 경로 해석에 영향을 준다. | 일반 백그라운드에서는 반환된 job ID로 `ouroboros_job_status`/`ouroboros_job_wait`, `ouroboros_job_result`를 사용한다. OpenCode plugin 위임은 job ID가 `None`일 수 있으므로 Task pane에서 결과를 확인한다. 실행은 모델·도구 호출과 파일 변경을 수반할 수 있다. |

`ouroboros_execute_seed`는 대기형이고 `ouroboros_start_execute_seed`는 장시간 작업의 백그라운드형이다. 성공 응답이나 job ID는 작업 성공 판정이 아니며 종료 상태와 최종 결과·평가를 확인한다. 이 표는 source 대조이며 실제 모델 인터뷰와 Seed 실행은 검증하지 않았다. [인터뷰·Seed 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/authoring_handlers.py), [context 생성 결과](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/session_seed_handler.py), [실행 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py).

## 같은 이름의 패키지와 source 차이 {#package-source-differences}

격리된 `ouroboros-ai[mcp]==0.59.9`의 stdio 서버와 위 고정 source 서버를 각각 `--runtime claude-cli`로 시작해 `list_tools` 응답을 비교했다. 이름은 모두 36개로 같았다. 이때 source의 `ouroboros_interview`에는 `calibration_input`, `interview_calibration` 두 입력이 있으나 패키지 스키마에는 없었다. `ouroboros_qa.pass_threshold`는 source 스키마에 0 이상 1 이하 제약이 명시되지만 패키지 응답에는 그 JSON Schema 제한이 없었다. 이는 관찰한 스키마 차이이며 패키지 핸들러가 범위를 검증하지 않는다는 증거는 아니다. 소스와 패키지는 동일한 의존성 고정 설치가 아니었으며, 연결된 서버가 반환하는 스키마가 해당 연결의 기준이다.

## `ouroboros_execute_seed`

**조건부 입력:** 스키마에서 둘 다 선택으로 표시되지만 실행과 `session_id` 재개 모두 비어 있지 않은 `seed_content` 또는 `seed_path`가 필요하다. 둘 다 있으면 `seed_content`가 우선하고 경로는 읽지 않는다. `seed_path`는 해석된 `cwd` 또는 `~/.ouroboros/seeds` 내부로 제한된다. 허용 범위 안에서 파일이 없으면 경로 문자열을 인라인 YAML로 취급하므로 오타가 파일 미발견 대신 Seed 파싱 오류로 나타날 수 있다. 존재하는 파일·작업 경로를 먼저 확인한다. [공통 해석 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py).

Execute a seed (task specification) in Ouroboros. Worktree provisioning is internal; use_worktree is not a public argument. This is the handler for 'ooo run' commands — do NOT run 'ooo' in the shell; call this MCP tool instead.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `seed_content` | string | 아니요 | Inline seed YAML content to execute. |
| `seed_path` | string | 아니요 | Path to a seed YAML file. If the path does not exist, the value is treated as inline seed YAML. |
| `cwd` | string | 아니요 | Working directory used to resolve relative seed paths. |
| `session_id` | string | 아니요 | Optional session ID to resume. If not provided, a new session is created. |
| `efficiency_mode` | string; 허용: `adaptive`, `quality_first` | 아니요 | Execution efficiency policy. adaptive may start decomposed ACs on lower-cost tiers and escalate on recovery; quality_first keeps children at the parent starting tier. When omitted on a fresh start, execution.default_policy supplies it (default quality_first; adaptive only when the policy is ask). |
| `frugality_assurance` | string; 허용: `off`, `observe`, `strict` | 아니요 | Frugality assurance: off, lightweight observe, or explicit strict baseline eligibility. Defaults from efficiency_mode; strict is never enabled implicitly. |
| `model_tier` | string; 허용: `small`, `medium`, `large` | 아니요 | Model-tier routing: small/medium/large → frugal/standard/frontier execution tier (trusted decomposed children may run one tier below; retries escalate). Omit to preserve automatic runtime selection; pass medium explicitly to pin standard routing. |
| `max_iterations` | integer | 아니요 | Maximum number of execution iterations. Default: 10 |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA evaluation. Default: false |
| `auto_evaluate` | boolean | 아니요 | Override execution.auto_evaluate for this call. When true, a completed background execute_seed run enqueues formal 3-stage evaluation as a separate bounded background job. |
| `auto_evolve` | boolean | 아니요 | Override execution.auto_evolve for the chained evaluation. When true, a background evaluation with `final_approved=false` attempts a bounded Ralph continuation, including `unverified`; missing Seed or enqueue failure can prevent it. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision receipt authorizing a fresh successor. |
| `predecessor_execution_id` | string | 아니요 | Execution ID that the new successor follows. |
| `conductor_directive` | object | 아니요 | Bounded corrective context copied exactly from the selected conductor decision. Fresh successor executions only. |

인터뷰 `session_id`를 사용하는 `ouroboros_generate_seed` 경로의 `client_gates`에는 `seed_ready_acceptance_guard`와 `restate_goal_approved`가 기대된다. 고정 구현은 기본적으로 누락을 경고·메타데이터로 취급하며, 서버 환경의 `OUROBOROS_REQUIRE_CLIENT_GATES`가 `1`, `true`, `yes`, `on` 중 하나이면 누락 시 오류로 차단한다(공백·대소문자 정규화). `force`는 이 강제 검사를 우회하지 않는다. `session_context`만 주는 인터뷰 없는 경로는 이 검사 전에 별도 분기한다. 두 입력을 함께 주고 `session_id`가 있으면 세션 경로를 사용한다. 클라이언트 gate 이름 전달은 실제 사용자 승인이나 인터뷰의 질을 서버가 독립 검증한다는 뜻이 아니다. 이는 [고정 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/authoring_handlers.py)의 정적 대조다. 합성 plugin 경로에서 누락 경고 metadata, 강제 설정의 `force=True` 오류, 완전 gate 및 context stub 분기를 시험했으나 실제 Seed·모델·MCP 전송은 미시험이다.

**Conductor 후속 입력의 우선순위와 빈 객체:** 고정 실행 핸들러의 준비 함수는 요청의 `conductor_directive`가 `null`이 아니면 Seed 안의 같은 필드보다 요청 값을 우선한다. 비어 있지 않은 directive에는 `conductor_decision_id`와 `predecessor_execution_id` 및 일치하는 selected 영수증이 필요하며, 재개에 주입할 수 없다. 다만 요청에 빈 객체 `{}`를 명시하면 이 함수는 이를 placeholder로 보고 성공 반환하며 원본 Seed 내용을 그대로 둔다. Seed에 이미 비어 있지 않은 directive가 있는 경우에도 이 함수 단계에서 그 내용을 지우거나 selected 영수증을 검사하지 않는다. 신뢰된 Seed·요청을 검토하고 빈 객체를 사용해 기존 directive를 제거하거나 권한 조건을 만족시킨다고 가정하지 않는다. 이는 [고정 준비 함수](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py)의 직접 합성 시험이며, 후속 합성 fresh 요청에서 실제 시작 핸들러는 빈 객체를 받은 경우 성공 응답과 mock job 등록을 반환했다. 이 mock은 실행 coroutine을 닫는다. 별도의 직접 Execute 핸들러 합성 사례에서는 빈 객체가 같은 준비 단계를 통과한 뒤 실제 `Seed.from_dict` 변환 결과에도 내부 지시가 남았다. 해당 합성 Seed를 `build_system_prompt`에 별도로 직접 전달하면 내부 지시가 프롬프트 문자열에 포함됐다. 추가 합성 fresh legacy 시험에서는 실제 Execute handler와 runner가 지시 문구를 캡처 mock runtime의 system prompt에 전달했다. 대역은 즉시 예외를 내 작업 결과는 실패했으며 event ID 부재는 출력 관찰이다. 실제 모델·백그라운드 job·기본 fat-harness·후속 권한 검사나 전체 권한 우회 여부는 시험하지 않았다.

추가로 기본 fat-harness의 합성 fresh in-process 시험에서도 같은 내부 instruction이 실제 runner를 거쳐 mock runtime의 system prompt에 도달했다. 실제 작업은 실패했고 event ID는 prompt에 없었다. 독립 재현에서도 동일하게 관찰했지만 실제 모델·권한 효과, plugin·resume·백그라운드 경로는 미검증이다.

## `ouroboros_start_execute_seed`

**조건부 입력:** 위 [실행 도구](#ouroboros_execute_seed)와 같은 Seed 입력·우선순위·경로 제한을 사용한다. `session_id`를 주는 재개에도 `seed_content` 또는 `seed_path`가 필요하다.

Execute an existing Seed specification. Use when: a validated Seed (file path such as *.seed.yaml, or YAML) already exists and the user wants it run ("run the seed", "execute this spec"). Result: a background execution returning a job ID immediately; use ouroboros_ac_tree_hud for live progress snapshots and ouroboros_job_result for terminal output. Do not use when: the request is raw or ambiguous natural language with no Seed (use ouroboros_interview or ouroboros_start_auto instead). In plugin mode, execution is delegated to an OpenCode Task pane and job_id is None; results appear in the Task pane instead of being pollable via job_status/job_result. For 'ooo run', use MCP, not the shell. Worktree provisioning is internal; use_worktree is not a public argument.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `seed_content` | string | 아니요 | Inline seed YAML content to execute. |
| `seed_path` | string | 아니요 | Path to a seed YAML file. If the path does not exist, the value is treated as inline seed YAML. |
| `cwd` | string | 아니요 | Working directory used to resolve relative seed paths. |
| `session_id` | string | 아니요 | Optional session ID to resume. If not provided, a new session is created. |
| `efficiency_mode` | string; 허용: `adaptive`, `quality_first` | 아니요 | Execution efficiency policy. adaptive may start decomposed ACs on lower-cost tiers and escalate on recovery; quality_first keeps children at the parent starting tier. When omitted on a fresh start, execution.default_policy supplies it (default quality_first; adaptive only when the policy is ask). |
| `frugality_assurance` | string; 허용: `off`, `observe`, `strict` | 아니요 | Frugality assurance: off, lightweight observe, or explicit strict baseline eligibility. Defaults from efficiency_mode; strict is never enabled implicitly. |
| `model_tier` | string; 허용: `small`, `medium`, `large` | 아니요 | Model-tier routing: small/medium/large → frugal/standard/frontier execution tier (trusted decomposed children may run one tier below; retries escalate). Omit to preserve automatic runtime selection; pass medium explicitly to pin standard routing. |
| `max_iterations` | integer | 아니요 | Maximum number of execution iterations. Default: 10 |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA evaluation. Default: false |
| `auto_evaluate` | boolean | 아니요 | Override execution.auto_evaluate for this call. When true, a completed background execute_seed run enqueues formal 3-stage evaluation as a separate bounded background job. |
| `auto_evolve` | boolean | 아니요 | Override execution.auto_evolve for the chained evaluation. When true, a background evaluation with `final_approved=false` attempts a bounded Ralph continuation, including `unverified`; missing Seed or enqueue failure can prevent it. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision receipt authorizing a fresh successor. |
| `predecessor_execution_id` | string | 아니요 | Execution ID that the new successor follows. |
| `conductor_directive` | object | 아니요 | Bounded corrective context copied exactly from the selected conductor decision. Fresh successor executions only. |
| `idempotency_key` | string | 아니요 | Optional process-local idempotency key. A second call with the same key returns the same execution metadata and does NOT enqueue a new execution. Map TTL is process lifetime — not persistent across server restarts. |

`ouroboros_start_execute_seed`의 멱등 키는 앞뒤 공백을 제거해 사용한다. 고정 구현은 같은 키의 캐시가 있으면 새 `cwd`, Seed 또는 다른 인자의 일치 여부를 검사하기 **전에** 이전 실행 메타데이터나 위임 응답을 반환한다. 따라서 같은 키는 같은 실행 의도의 재시도에만 재사용하고 다른 Seed·작업 경로·설정에는 새 키를 사용한다. 서버 재시작 뒤에는 이 프로세스 로컬 캐시가 유지되지 않으므로 키만으로 재시작 간 중복 방지를 보장하지 않는다. 이는 [고정 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py)의 정적 대조다. 실제 핸들러에 mock job 등록과 메모리 SQLite를 연결한 순차 합성 시험에서 다른 Seed·존재하지 않는 cwd와 같은 정규화 키가 이전 metadata를 재생했다. 별도의 합성 시험에서는 한 핸들러 인스턴스에 동일 키의 두 호출을 강제로 겹쳤을 때 mock 등록이 한 번이었지만, 같은 프로세스의 새 핸들러 인스턴스는 같은 키를 다시 등록했다. 실제 job·서버 재시작·다중 프로세스·MCP 전송은 시험하지 않았다.

## Auto·QA·반복 실행의 입력과 결과 선택

아래는 고정 소스의 기본 핸들러를 연결한 안내다. 접수, 위임, 개별 반복의 수렴과 최종 성공은 서로 다르다. 실행·평가는 모델 호출이나 작업 디렉터리 변경을 수반할 수 있으므로 목적과 작업 범위를 확인한다.

| 목적과 도구 | 조건과 기본값 | 응답·다음 확인 및 부작용 |
| --- | --- | --- |
| 새 Auto: `ouroboros_start_auto` | 비어 있지 않은 `goal`이 필요하다. 기존 상태는 `resume`의 auto session ID로 지정한다. 재개할 때 `pipeline_timeout_seconds`, `efficiency_mode`, `frugality_assurance`를 명시하면 거부된다. | 비동기 접수 뒤 반환된 식별자로 작업 상태와 결과를 확인한다. 실제 Seed·실행 허용 판정과 결과를 확인하기 전 접수를 성공으로 보지 않는다. `ouroboros_auto`는 같은 파이프라인의 대기형이므로 클라이언트 제한 시간을 넘길 수 있다. [조건·degraded 예외](/docs/auto-detail/). |
| 임의 결과물 평가: `ouroboros_qa` | `artifact`는 문자열, `quality_bar`는 비어 있지 않은 값이 필요하다. `artifact_type` 기본은 `code`, `pass_threshold`는 유한한 0~1 수로 기본 0.80이다. `iteration_history`는 객체 배열이다. | `qa_session_id`를 생략하면 새 ID를 만들고, 회차는 전달한 이력 길이 + 1이다. ID만으로 이전 결과가 자동으로 평가 입력에 들어간다고 가정하지 말고 이력을 전달한다. 플러그인 위임 응답은 평가 완료가 아니다. [QA 실행·해석](/docs/qa-detail/). |
| 한 세대: `ouroboros_evolve_step` / `ouroboros_start_evolve_step` | `lineage_id`가 필요하다. 첫 세대에는 Seed YAML이 필요하고 이후는 기록에서 재구성한다. 기본은 `execute=true`, `parallel=true`, `skip_qa=false`. `execute=false`는 ontology만 다루며 실제 실행·평가 성공이 아니다. | 동기형은 한 세대 결과, 시작형은 보통 job ID를 반환한다. 플러그인 위임일 때 시작형의 `job_id`는 `None`일 수 있다. `ontology_stable`은 비성공 인계이므로 실제 실행을 거친 수렴과 구분한다. [반복 흐름](/docs/evaluation-evolution-detail/). |
| 여러 세대: `ouroboros_ralph` / `ouroboros_start_ralph` | 유효한 `lineage_id`와 새 계보의 Seed가 필요하다. 기본 최대 10세대, 세대당 1800초, 진동 창 3, 등급 하락 창 2다. conductor 지시로 만든 후속 호출은 `max_generations=1`로 제한된다. | 두 이름 모두 백그라운드 루프를 시작한다. 보통 job ID를 조회하고, OpenCode plugin 위임 시 `job_id=None`이므로 자식 결과를 확인한다. in-process의 회차 timeout과 전체 예산은 서로 다르고, plugin의 시간 제한은 자식 준수에 의존한다. 정지 사유만으로 QA 통과를 가정하지 않는다. |

### 기존 계보의 반복을 관찰하는 예시

다음은 **MCP 도구 인자 예시**이며 실행 결과가 아니다. 이미 기록된 계보 ID를 사용한다. 새 계보라면 검증된 Seed YAML 전체를 `seed_content`에 제공해야 한다. 두 호출 이름은 같은 백그라운드 루프를 시작하므로 하나만 선택한다. 실행 시 모델 호출과 프로젝트 변경이 발생할 수 있다.

```json
{"lineage_id": "기존-계보-ID", "max_generations": 2, "per_iteration_timeout_seconds": 600, "max_total_seconds": 1200}
```

이 객체를 `ouroboros_start_ralph`의 인자로 전달한 뒤 **반환된** `job_id`가 있으면 `ouroboros_job_wait` 또는 `ouroboros_job_status`로 관찰하고 종료 뒤 `ouroboros_job_result`를 읽는다. 취소 요청은 `ouroboros_cancel_job`에 그 job ID를 전달하며, 요청 접수와 실제 종료는 구분한다. 반환이 `status=delegated_to_plugin`, `job_id=null`이면 job 도구로 조회할 수 없고 해당 호스트의 자식 세션 결과를 확인해야 한다. ID를 임의로 만들어 job 도구에 전달하지 않는다.

`max_total_seconds`를 생략하면 핸들러가 `max_generations × per_iteration_timeout_seconds`로 유도한다. in-process 경로는 **새 회차를 시작하기 전** 전체 시간을 검사하고 각 회차 제한을 별도로 둔다. 따라서 전체 예산이 실행 중인 회차의 정확한 강제 종료 시각이라고 해석하지 않는다. plugin 경로의 시간 제한은 자식에게 전달되는 지시이며 부모 서버가 자식 프로세스를 직접 강제 종료하는 보장은 아니다. 중첩 Ralph 위임은 거부되며, 최종 중단 사유·개별 평가 결과·남은 변경을 함께 확인한다. 이 예시는 고정 핸들러 정적 대조이며 실제 반복·모델·위임·취소는 실행하지 않았다.

위 조건은 [Auto 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/auto_handler.py), [QA](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py), [evolve](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py), [Ralph](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/ralph_handlers.py) 정적 대조다. 실제 모델·호스트 위임과 입력 조합 전체는 시험하지 않았다.

**Auto의 중첩 `user_preferences`:** 기본 핸들러는 ledger 섹션 이름을 정확한 키로 받는다. 허용 키는 `goal`, `actors`, `inputs`, `outputs`, `constraints`, `non_goals`, `acceptance_criteria`, `verification_plan`, `failure_modes`, `runtime_context`다. 새 세션의 각 값은 빈 값이 아닌 문자열 또는 문자열·숫자의 비어 있지 않은 배열이어야 한다. 배열은 각 항목의 앞뒤 공백을 제거하고 빈 항목을 버린 뒤 줄바꿈으로 합친다. 배열 안의 boolean과 객체, 단독 숫자는 거부된다. 배열이 비어 있지 않아도 정규화 후 모든 항목이 공백이면 새 세션에서는 오류이고 재개에서는 해당 선호를 지우는 값이다. 재개에서는 특정 키의 `null`·빈 문자열·빈 배열로 해당 저장 선호를 지울 수 있지만, **`user_preferences` 전체를 생략하거나 `null`로 전달하는 것은 개별 키 삭제가 아니다.** 빈 객체도 저장된 모든 키를 지우지 않는다. 예를 들어 `{ "constraints": null }`은 재개에서 해당 선호만 제거하려는 입력이다. 유효한 키와 저장된 상태를 대조하고 이 값이 최종 Seed의 모든 조건 제거를 보장한다고 가정하지 않는다. 이는 [입력 파싱·재개 병합](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/auto_handler.py)과 [섹션 정의](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/auto/ledger.py)의 정적 대조다. 격리된 합성 입력으로 파서와 재개 병합 함수의 빈 객체 보존, 개별 null 삭제, 배열 정규화 및 boolean·단독 숫자 거부를 직접 확인했다. 최상위 null은 정적 대조이며 전체 핸들러·DB·모델·호스트 위임이나 모든 입력 조합은 시험하지 않았다.

## `ouroboros_auto`

Blocking form of ouroboros_start_auto (prefer that one; this call can outlast the client timeout). Runs ooo auto in the foreground. 일반 Seed는 요구 등급과 실행 허용 검토를 거치지만 sourced_scope가 있는 degraded Seed는 별도 안전 blocker 기준으로 실행될 수 있다. [Auto 경계](/docs/auto-detail/).

**조건부 입력:** 새 세션은 비어 있지 않은 `goal`이 필요하다. 기존 세션은 `resume`에 실제 auto session ID를 지정한다. `attach_execution`, `attach_job`, `attach_session` 중 하나를 쓰거나 `reconcile_run: true`를 요청할 때는 `resume`이 필요하다. 재개에 `pipeline_timeout_seconds`, `efficiency_mode`, `frugality_assurance`를 명시하면 기존 값과 같더라도 거부되므로 생략한다. `ouroboros_auto` 재개에서는 두 `max_*_rounds` 입력값 대신 저장된 한도를 사용하고, `skip_run`은 저장된 값 또는 이번 요청이 참이면 참으로 유지된다. 따라서 아래 스키마 기본값은 재개 시 저장 상태의 대체값이 아니다. 연결할 실행·작업 ID는 외부에서 확인한 값이어야 하며, reconciliation 요청을 새 실행의 성공으로 취급하지 않는다. [입력 검증 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/auto_handler.py).

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `goal` | string | 아니요 | Goal/task for ooo auto |
| `cwd` | string | 아니요 | Working directory |
| `resume` | string | 아니요 | Auto session id to resume |
| `max_interview_rounds` | integer | 아니요 | Max interview rounds 스키마 기본값: `50`. |
| `max_repair_rounds` | integer | 아니요 | Max repair rounds 스키마 기본값: `5`. |
| `skip_run` | boolean | 아니요 | Stop after Seed creation; degraded 경로를 포함한 실제 결과는 [Auto 안내](/docs/auto-detail/) 참조. 스키마 기본값: `false`. |
| `attach_execution` | string | 아니요 | Attach an externally verified execution id to an unknown run handoff |
| `attach_job` | string | 아니요 | Attach an externally verified job id to an unknown run handoff |
| `attach_session` | string | 아니요 | Attach an externally verified run session id to an unknown run handoff |
| `attach_source` | string | 아니요 | Source label for an attached run handle |
| `reconcile_run` | boolean | 아니요 | Try to reconcile an unknown run handoff without starting a duplicate run 스키마 기본값: `false`. |
| `reconcile_source` | string | 아니요 | Source label for run handoff reconciliation |
| `pipeline_timeout_seconds` | number | 아니요 | Top-level pipeline deadline in seconds. Defaults to 7200s for new sessions. Range: 60-86400. Cannot be changed on resume; the deadline is preserved across process restarts. |
| `user_preferences` | object | 아니요 | Caller-supplied user preferences keyed by ledger section name (e.g. runtime_context, constraints, non_goals). The Driver tags matching answers with [from-auto][user_preference] in the ledger. Keys must be valid ledger section names; values must be non-empty strings or non-empty lists of strings/numbers. On resume, null/empty values clear the persisted preference for that section. |
| `efficiency_mode` | string; 허용: `adaptive`, `quality_first` | 아니요 | Execution efficiency policy: adaptive may use lower-cost child tiers with recovery escalation; quality_first keeps child ACs at the parent starting tier. When omitted on a fresh start, a configured execution.default_policy supplies it (default quality_first; adaptive only when the policy is ask). |
| `frugality_assurance` | string; 허용: `off`, `observe`, `strict` | 아니요 | Frugality assurance: off, observe, or explicitly authorized strict. Defaults from efficiency_mode and is immutable on resume. |
| `complete_product` | boolean | 아니요 | Deprecated and ignored. The run job owns run -> evaluate -> ralph; follow it with ouroboros_job_status or ouroboros_job_wait instead. 스키마 기본값: `false`. |
| `domain` | string | 아니요 | Optional domain profile name (for example, coding) |
| `commit_policy` | string | 아니요 | Checkpoint commit policy: ac_checkpoint, final_only, or none |
| `worktree_policy` | string | 아니요 | Worktree isolation policy: auto, always, current, or none |

## `ouroboros_start_auto`

Build and verify a substantial change end-to-end. Use when: the work spans several files or replaces a framework, language, auth, storage, or API layer (rewrites and migrations included), or is a high-risk change, and the user wants it to end up working and tested; call it first instead of implementing inline, even if the user never says 'ooo'. Result: a bounded interview fills only the gaps, Seed 검토 후 실행을 백그라운드로 인계한다. 일반 등급 게이트와 degraded 예외는 [Auto 안내](/docs/auto-detail/)를 확인한다. 접수는 완료가 아니다. Do not use when: the request is a simple question or small unambiguous edit, or a validated Seed already exists (use ouroboros_start_execute_seed). Resume with the returned auto_session_id; poll with ouroboros_job_status / ouroboros_job_wait and read final state via ouroboros_job_result.

**조건부 입력:** 새 세션은 비어 있지 않은 `goal`이 필요하다. 기존 세션은 `resume`에 실제 auto session ID를 지정한다. `attach_execution`, `attach_job`, `attach_session` 중 하나를 쓰거나 `reconcile_run: true`를 요청할 때는 `resume`이 필요하다. 재개에 `pipeline_timeout_seconds`, `efficiency_mode`, `frugality_assurance`를 명시하면 기존 값과 같더라도 거부되므로 생략한다. `ouroboros_start_auto` 재개에서는 두 `max_*_rounds` 입력값 대신 저장된 한도를 사용하고, `skip_run`은 저장된 값 또는 이번 요청이 참이면 참으로 유지된다. 따라서 아래 스키마 기본값은 재개 시 저장 상태의 대체값이 아니다. 연결할 실행·작업 ID는 외부에서 확인한 값이어야 하며, reconciliation 요청을 새 실행의 성공으로 취급하지 않는다. [입력 검증 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/auto_handler.py).

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `goal` | string | 아니요 | Goal/task for ooo auto |
| `cwd` | string | 아니요 | Working directory |
| `resume` | string | 아니요 | Auto session id to resume |
| `max_interview_rounds` | integer | 아니요 | Max interview rounds 스키마 기본값: `50`. |
| `max_repair_rounds` | integer | 아니요 | Max repair rounds 스키마 기본값: `5`. |
| `skip_run` | boolean | 아니요 | Stop after Seed creation; degraded 경로를 포함한 실제 결과는 [Auto 안내](/docs/auto-detail/) 참조. 스키마 기본값: `false`. |
| `attach_execution` | string | 아니요 | Attach an externally verified execution id to an unknown run handoff |
| `attach_job` | string | 아니요 | Attach an externally verified job id to an unknown run handoff |
| `attach_session` | string | 아니요 | Attach an externally verified run session id to an unknown run handoff |
| `attach_source` | string | 아니요 | Source label for an attached run handle |
| `reconcile_run` | boolean | 아니요 | Try to reconcile an unknown run handoff without starting a duplicate run 스키마 기본값: `false`. |
| `reconcile_source` | string | 아니요 | Source label for run handoff reconciliation |
| `pipeline_timeout_seconds` | number | 아니요 | Top-level pipeline deadline in seconds. Defaults to 7200s for new sessions. Range: 60-86400. Cannot be changed on resume; the deadline is preserved across process restarts. |
| `user_preferences` | object | 아니요 | Caller-supplied user preferences keyed by ledger section name (e.g. runtime_context, constraints, non_goals). The Driver tags matching answers with [from-auto][user_preference] in the ledger. Keys must be valid ledger section names; values must be non-empty strings or non-empty lists of strings/numbers. On resume, null/empty values clear the persisted preference for that section. |
| `efficiency_mode` | string; 허용: `adaptive`, `quality_first` | 아니요 | Execution efficiency policy: adaptive may use lower-cost child tiers with recovery escalation; quality_first keeps child ACs at the parent starting tier. When omitted on a fresh start, a configured execution.default_policy supplies it (default quality_first; adaptive only when the policy is ask). |
| `frugality_assurance` | string; 허용: `off`, `observe`, `strict` | 아니요 | Frugality assurance: off, observe, or explicitly authorized strict. Defaults from efficiency_mode and is immutable on resume. |
| `complete_product` | boolean | 아니요 | Deprecated and ignored. The run job owns run -> evaluate -> ralph; follow it with ouroboros_job_status or ouroboros_job_wait instead. 스키마 기본값: `false`. |
| `domain` | string | 아니요 | Optional domain profile name (for example, coding) |
| `commit_policy` | string | 아니요 | Checkpoint commit policy: ac_checkpoint, final_only, or none |
| `worktree_policy` | string | 아니요 | Worktree isolation policy: auto, always, current, or none |

## 백그라운드 작업과 실행을 관찰·취소할 때

`job_id`는 시작 도구가 반환한 **백그라운드 작업 ID**, `session_id`/`execution_id`는 연결된 세션이나 실행의 ID다. 서로 교환하지 않는다. OpenCode plugin 위임의 `job_id=None`은 상태 조회용 ID가 아니므로 위임받은 Task pane을 확인한다. 다음은 고정 소스의 MCP 핸들러 기준이며 CLI의 옵션 기본값과 동일하다고 가정하지 않는다.

| 도구 | 필요한 입력과 기본값 | 응답 해석과 부작용 |
| --- | --- | --- |
| `ouroboros_session_status` | `session_id` 필수 | 세션의 단계·진행 상태를 조회한다. 작업 ID를 이 인자로 넣지 않는다. |
| `ouroboros_job_status` | `job_id` 필수, `view=full` | 작업 snapshot과 `meta`의 `status`, `is_terminal`, `result_available`, `cursor`, 연결 ID를 확인한다. `summary`·`compact`는 텍스트 상세도 선택이다. 종료 자체가 성공을 의미하지 않으며 실패·취소·중단과 결과 payload 오류는 `is_error`로 표시될 수 있다. |
| `ouroboros_job_wait` | `job_id` 필수, `cursor=0`, `timeout_seconds=0`, `view=full`, `stream=progress`, `wait_for=raw` | 기본은 즉시 snapshot; 명시적 timeout은 최대 5초로 제한된다. cursor·timeout은 음수가 아닌 정수여야 한다. 다음 호출에 반환 cursor를 넘긴다. `linked`는 연결된 스트림을 포함하지만 한 번에 모든 과거 이벤트를 받는다는 보장은 없다. 자세한 wakeup 조건과 페이지 경계는 [진행 조회](/docs/progress-detail/)를 본다. |
| `ouroboros_job_result` | `job_id` 필수 | 미종결이면 `is_error=false`일 수 있지만 `result_available=false`이므로 성공 결과가 아니다. 종결이면 보존된 결과와 오류 상태를 확인하고, handle이 없으면 결과를 사용할 수 없다는 오류가 발생할 수 있다. 원래 시작 응답이 `detached_job_acceptance_pending`이면, release `0.59.9`의 missing-handle `is_terminal=true`를 worker 종료로 해석하지 않는다. matching pending 영수증이 있을 때의 main `592c667f` 분기와 구분해 [판본별 조회·중복 실행 방지 경고](/docs/ai-troubleshooting/#recovery)를 먼저 확인한다. |
| `ouroboros_cancel_job` | `job_id` 필수 | 취소를 **요청**하고 반환된 상태를 관찰한다. 응답의 `is_error=false`만으로 모든 외부 효과가 중단되거나 되돌려졌다고 단정하지 않는다. |
| `ouroboros_cancel_execution` | `execution_id` 필수, `reason` 선택 | 이미 종결된 실행은 거부된다. 살아 있는 로컬 소유자에게 취소를 요청하면 `cancellation_requested`와 `in_flight=true`가 반환될 수 있으므로 최종 상태를 다시 확인한다. 다른 살아 있는 소유자가 가진 실행은 그 소유자를 통해 취소해야 할 수 있다. [복구 안내](/docs/recovery-detail/)에서 부작용과 재개 경계를 확인한다. |

`view`, `stream`, `wait_for`의 알 수 없는 문자열은 이 판본에서 기본값으로 정규화될 수 있으므로 오타가 명시적 오류로 발견된다고 가정하지 않는다. 위 내용은 [job 핸들러 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/job_handlers.py) 정적 대조이며 실제 작업 취소·외부 모델 호출 시험은 아니다.

**stdio 오류 처리 예:** 격리된 빈 HOME의 실제 stdio 서버와 설치된 MCP Python SDK `ClientSession`에서 존재하지 않는 합성 job ID를 조회했을 때, `ouroboros_job_status`는 `is_error=true`인 도구 결과를 반환했고 `ouroboros_job_result`는 `Job handle not found`를 포함한 `MCPError`를 발생시켰다. 클라이언트는 도구 결과의 오류 표시와 호출 예외를 모두 처리하고, 반환된 ID·서버와 작업 수명을 확인해야 한다. 이는 해당 SDK와 합성 누락 job의 관찰 한 사례이며 모든 오류나 다른 클라이언트의 표현을 보장하지 않는다. 핸들러에는 누락으로 보이는 job이 아직 대기 중인 경우 별도 pending 결과를 반환하는 분기도 있다. 실제 모델·live job·인증은 이 시험에서 사용하지 않았다.

## `ouroboros_session_status`

Get the status of an Ouroboros session. Returns information about the current phase, progress, and any errors.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | The session ID to query |

## `ouroboros_job_status`

Get the latest summary for a background Ouroboros job.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `job_id` | string | 예 | Job ID returned by a start tool |
| `view` | string | 아니요 | 'full' (default), 'summary', or 'compact'. |

## `ouroboros_job_wait`

Wait briefly for a background job to change state. Useful for conversational polling after a start command.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `job_id` | string | 예 | Job ID returned by a start tool |
| `cursor` | integer | 아니요 | Previous cursor from job_status or job_wait 스키마 기본값: `0`. |
| `timeout_seconds` | integer | 아니요 | Maximum seconds to wait for a change. Defaults to 0 so the tool returns an immediate snapshot and never holds the MCP client open unless the caller explicitly asks for long-polling. Values above 5 are capped so clients with MCP tool-call timeouts can poll safely. |
| `view` | string | 아니요 | 'full' (default), 'summary', or 'compact'. |
| `stream` | string | 아니요 | 'progress' (default) watches job/execution progress; 'linked' also streams linked session, lineage, and subagent events. |
| `wait_for` | string | 아니요 | 'raw' (default) returns on any job event, preserving existing behavior; 'ac_change' waits for AC/Sub-AC/phase progress or terminal status; 'attention_or_ac_change' additionally wakes for Synapse delivery status; 'phase_change' waits for phase transitions or terminal status; 'terminal' waits only for terminal status. |

**시간 제한 해석:** 위 영문은 722판 스키마의 설명입니다. 고정 722·main `592c667f`·release `0.59.9` 구현에서 `timeout_seconds=0`은 **앞으로의 상태 변화를 기다리지 않는다**는 뜻이며, snapshot·DB 조회 응답시간의 상한이 아닙니다. 이 경우 양수 대기용 guard를 적용하지 않으므로 클라이언트가 먼저 timeout할 수 있습니다. 양수 요청의 guard가 snapshot을 만들기 전에 시간 초과되면 `wait_timed_out: true`, `result_available: false` 응답이 나올 수 있습니다. 이는 작업의 종료나 취소가 아닙니다. 같은 실제 job ID와 소유자·서버를 확인하고 기존 작업 상태를 조회하며, 응답 지연만으로 중복 실행하지 마세요. 이 설명은 고정 소스의 정적 대조이며 실제 DB·호스트 시간은 검증하지 않았습니다. [722 guard](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/job_wait_guard.py#L112-L133) · [main guard](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_wait_guard.py#L112-L133) · [release guard](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/job_wait_guard.py#L77-L98) · [release timeout 응답](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/job_handlers.py#L208-L237)

## `ouroboros_job_result`

Get the final output for a completed background job.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `job_id` | string | 예 | Job ID returned by a start tool |

## `ouroboros_ac_tree_hud`

Return a render-ready markdown snapshot of the live acceptance-criteria tree for an Ouroboros session.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | Session ID to inspect. |
| `cursor` | integer | 아니요 | Previous EventStore row ID cursor. 스키마 기본값: `0`. |
| `view` | string | 아니요 | Verbosity: 'tree' (default) for the full AC tree, 'summary' for a short monitor, or 'compact' for one-line polling. |
| `max_nodes` | integer | 아니요 | Maximum tree nodes to render when view='tree'. 스키마 기본값: `50`. |

## `ouroboros_cancel_job`

Request cancellation for a background job.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `job_id` | string | 예 | Job ID returned by a start tool |

## 이벤트·투영·프로젝트 조회의 선택 기준

아래는 고정 소스의 기본 핸들러 기준이다. 조회 결과는 기록의 투영이므로 현재 프로세스가 실제로 살아 있거나 작업이 성공했다는 증거가 아니다. 이벤트 내용에는 민감한 입력이 들어갈 수 있으므로 결과를 공유하기 전에 확인한다. 상세 데이터 흐름은 [이벤트 조회와 투영](/docs/query-projections-detail/)을 참고한다.

| 도구 | 입력과 기본값 | 결과·주의할 부작용 |
|---|---|---|
| `ouroboros_query_events` | `session_id`, `event_type`은 선택; `limit=50`, `offset=0`. 세션 ID가 있으면 관련 세션 이벤트를, 없으면 전체에서 조회한다. | 응답의 `meta.total_events`는 **이번 페이지의 건수**이지 전체 일치 건수가 아니다. offset 페이지는 동시 추가 중 안정적인 스냅샷을 보장하지 않는다. 기본 EventStore를 초기화하므로 단순 조회라도 DB 생성 등 파일 부작용이 생길 수 있다. |
| `ouroboros_query_projection` | `session_id` 또는 `execution_id` 중 하나가 필수. 둘 다 있으면 실행 ID가 관련 이벤트 범위를 좁힌다. `seed_id`는 선택적 override, `limit`은 생략 가능하나 주면 양의 정수여야 한다. | Run/Stage/Step을 이벤트로 재구성한다. 이벤트가 없거나 지정 상한을 넘으면 부분 투영 대신 오류다. 핸들러가 자체 생성하는 저장소는 읽기 전용이며 스키마를 생성하지 않는다. |
| `ouroboros_project_status` | `project_dir` 생략 시 서버 생성 시 포착한 기본 디렉터리, 그것도 없으면 호출 시 현재 디렉터리. `workspace`는 선택적 정규 프로젝트 상대 경로; `limit=100`이며 양의 정수. | 성공 시 텍스트와 `structured_content`의 ProjectRecord, `meta.run_count`를 반환한다. 동일성 충돌·투영 실패·일치 실행 수의 상한 초과 시 부분 기록 대신 오류다. 자체 저장소는 읽기 전용이며 스키마를 생성하지 않는다. |

소스: [이벤트 조회 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/query_handlers.py), [투영 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/projection_handlers.py), [프로젝트 상태 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/project_status_handler.py). 위 내용은 소스 대조이며 이 표 추가에서 실제 MCP 서버나 운영 DB를 시험하지 않았다.

## `ouroboros_query_events`

Query the event history for an Ouroboros session. Returns a list of events matching the specified criteria.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 아니요 | Filter events by session ID. If not provided, returns events across all sessions. |
| `event_type` | string | 아니요 | Filter by event type (e.g., 'execution', 'evaluation', 'error') |
| `limit` | integer | 아니요 | Maximum number of events to return. Default: 50 |
| `offset` | integer | 아니요 | Number of events to skip for pagination. Default: 0 |

## `ouroboros_query_projection`

Build a read-only Run/Stage/Step projection from persisted Ouroboros events for a session or execution aggregate.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 아니요 | Optional orchestrator session ID to project. |
| `execution_id` | string | 아니요 | Optional execution aggregate ID. When session_id is also provided, this narrows related session-event lookup. |
| `seed_id` | string | 아니요 | Optional seed ID override. If omitted, the handler derives one from events and falls back to the queried ID. |
| `limit` | integer | 아니요 | Optional safety cap for related events. If the run has more events than this cap, the tool fails instead of returning a partial projection. |

## `ouroboros_project_status`

Resolve a project identity and rebuild its complete read-only run status from persisted Ouroboros session events. Identity conflicts, projection failures, and limits below the complete population return no partial record.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `project_dir` | string | 아니요 | Project or workspace directory. Defaults to the MCP server caller directory captured at startup. |
| `workspace` | string | 아니요 | Optional canonical project-relative workspace filter. |
| `limit` | integer | 아니요 | Complete-run safety cap. The query fails instead of truncating when the matching population exceeds this value. 스키마 기본값: `100`. |

## `ouroboros_generate_seed`

Generate an immutable Seed from a completed interview session, OR crystallize one directly from already-settled session context with NO interview (pass session_context instead of session_id; deterministic — material enters the Seed verbatim, and an incomplete submission returns gap questions, not a block). Offer that proactively once goal, constraints, and success criteria are settled; a Seed is useful even without running it. Interview path requires ambiguity_score <= 0.2 unless force=true.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 아니요 | Interview session ID to convert to a seed. Required unless session_context is provided. |
| `session_context` | object | 아니요 | Interview-less path: settled material from THIS session. Keys: goal (required), acceptance_criteria (required, verifiable checks), constraints, decisions (become constraints), project_type. Anchored verbatim — supply the user's own settled wording, never your paraphrase. |
| `ambiguity_score` | number | 아니요 | Ambiguity score for the interview (0.0 = clear, 1.0 = ambiguous). Required if interview didn't calculate it. Generation fails if > 0.2. |
| `client_gates` | array; 항목: string | 아니요 | Client-side interview gates acknowledged before seed generation. Expected values include seed_ready_acceptance_guard and restate_goal_approved. |
| `force` | boolean | 아니요 | Bypass the ambiguity-score threshold and generate the seed even when ambiguity_score > 0.2. Mirrors the CLI 'Generate Seed anyway' opt-in: the real score is still recorded in seed metadata for provenance, and the bypass is emitted to the audit log. Defaults to false. |

## `ouroboros_measure_drift`

Measure drift from the original seed goal. Calculates goal deviation score using weighted components: goal drift (50%), constraint drift (30%), ontology drift (20%). Returns drift metrics, analysis, and suggestions if drift exceeds threshold.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | The execution session ID to measure drift for |
| `current_output` | string | 예 | Current execution output to measure drift against the seed goal |
| `seed_content` | string | 예 | Original seed YAML content for drift calculation |
| `constraint_violations` | array | 아니요 | Known constraint violations (e.g., ['Missing tests', 'Wrong language']) |
| `current_concepts` | array | 아니요 | Concepts present in the current output (for ontology drift) |

## `ouroboros_interview`

Clarify a vague request before any implementation. Use when: the user wants something built but is unsure what ("help me figure out what to build", "add notifications", "make it production-ready", "build me X"), the request is ambiguous, or it lacks acceptance criteria; call it first, even if the user never says 'ooo'. Result: a short Socratic interview, one question at a time, that closes goals, constraints, and acceptance criteria, ready for Seed generation. Do not use when: a validated Seed already exists (use ouroboros_start_execute_seed) or the request is a simple question or small unambiguous edit. Start a new interview with initial_context, resume with session_id, or record an answer to the current question. In plugin mode, returns a delegation receipt (status=delegated_to_subagent) and the interview executes in an OpenCode Task pane; the real session_id is returned there.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `initial_context` | string | 아니요 | Initial context to start a new interview session |
| `session_id` | string | 아니요 | Session ID to resume an existing interview |
| `answer` | string | 아니요 | Response to the current interview question |
| `cwd` | string | 아니요 | Working directory for brownfield auto-detection. Defaults to the current working directory if not provided. |
| `last_question` | string | 아니요 | The question text from the previous child session's response. In plugin mode each dispatch creates a new child session whose questions are not automatically persisted server-side. Pass the child's last question here when submitting an answer so the interview transcript preserves the real question text instead of a placeholder. |
| `interview_id` | string | 아니요 | Optional caller-supplied id for a brand-new interview. Must match the server format 'interview_<16 lowercase hex>' and must NOT collide with an existing interview file. Only valid for the start action — supplying it together with session_id (resume) or answer is rejected with an error to prevent silent identifier hijacking; do not preserve this argument across turns. Used by the bounded auto driver to pre-allocate the id so a driver-level cancel cannot leave auto state out of sync with the persisted interview file (see Q00/ouroboros#687). |
| `confused_terms` | array; 항목: string | 아니요 | Explicit domain terms the user says they do not understand. Queued on the start turn and applied only after the first answer. |
| `references` | array; 항목: object | 아니요 | Bounded user-provided reference cues. Each object requires reference_id, label, and origin; url/excerpt are optional. |
| `calibration_input` | string | 아니요 | User-reported topic knowledge for session-local interview wording. This does not answer a pending question. |
| `interview_calibration` | object | 아니요 | Validated session-local language calibration transported by the runtime handle; it is not persisted in interview state. |

## `ouroboros_evaluate`

Evaluate an Ouroboros execution session using the three-stage evaluation pipeline. Stage 1 performs mechanical verification (lint, build, test). Stage 2 performs semantic evaluation of AC compliance and goal alignment. Stage 3 runs multi-model consensus if triggered by uncertainty or manual request.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | The execution session ID to evaluate |
| `artifact` | string | 예 | The execution output/artifact to evaluate |
| `seed_content` | string | 아니요 | Original seed YAML for goal/constraints extraction |
| `acceptance_criterion` | string | 아니요 | Specific acceptance criterion to evaluate against |
| `acceptance_criteria` | array | 아니요 | Multiple acceptance criteria for checklist evaluation. When two or more items are provided, each AC is evaluated independently and the results are aggregated into a pass/fail checklist (#366). Overrides acceptance_criterion. |
| `artifact_type` | string; 허용: `code`, `docs`, `config` | 아니요 | Type of artifact: code, docs, config. Default: code |
| `trigger_consensus` | boolean | 아니요 | Force Stage 3 consensus evaluation. Default: False |
| `working_dir` | string | 아니요 | Project root used to resolve Stage 1 mechanical verification commands and Stage 2 source-file visibility. Commands are read from .ouroboros/mechanical.toml; when the file is missing, the evaluator makes one AI detect call that inspects manifests (package.json, pyproject.toml, Cargo.toml, Makefile, ...) and authors the toml. Stage 1 skips every check when no toml is produced — it never guesses. |

## `ouroboros_start_evaluate`

Verify that finished work meets its acceptance criteria, not just that tests pass ("is it actually done?", "check it against the spec"). Start an evaluation in the background and return a job ID immediately. Use this instead of ouroboros_evaluate when the three-stage pipeline (mechanical + semantic + optional consensus) is expected to exceed the MCP client tool-call timeout. Poll with ouroboros_job_status / ouroboros_job_wait and read the verdict via ouroboros_job_result. In plugin mode with auto_evolve disabled, evaluation is delegated to an OpenCode Task pane and job_id is None. With auto_evolve enabled, the parent keeps evaluation pollable so a rejection can start Ralph.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | The execution session ID to evaluate |
| `artifact` | string | 예 | The execution output/artifact to evaluate |
| `seed_content` | string | 아니요 | Original seed YAML for goal/constraints extraction |
| `acceptance_criterion` | string | 아니요 | Specific acceptance criterion to evaluate against |
| `acceptance_criteria` | array | 아니요 | Multiple acceptance criteria for checklist evaluation. When two or more items are provided, each AC is evaluated independently and the results are aggregated into a pass/fail checklist (#366). Overrides acceptance_criterion. |
| `artifact_type` | string; 허용: `code`, `docs`, `config` | 아니요 | Type of artifact: code, docs, config. Default: code |
| `trigger_consensus` | boolean | 아니요 | Force Stage 3 consensus evaluation. Default: False |
| `working_dir` | string | 아니요 | Project root used to resolve Stage 1 mechanical verification commands and Stage 2 source-file visibility. Commands are read from .ouroboros/mechanical.toml; when the file is missing, the evaluator makes one AI detect call that inspects manifests (package.json, pyproject.toml, Cargo.toml, Makefile, ...) and authors the toml. Stage 1 skips every check when no toml is produced — it never guesses. |
| `auto_evolve` | boolean | 아니요 | Override execution.auto_evolve for this background call. When true, a background formal evaluation with `final_approved=false` attempts a bounded Ralph continuation, including `unverified`; missing Seed or enqueue failure can prevent it. |
| `seed_handoff_id` | string | 아니요 | Opaque parent-owned Seed handle for plugin evaluation |

## `ouroboros_checklist_verify`

Verify that a Run artifact satisfies every acceptance criterion in a Seed. Returns a per-AC checklist (pass/fail with evidence and failure reasons) plus ready-to-use run_feedback strings the caller can inject into a re-run prompt. Does NOT automatically re-execute — the caller (Ralph, workflow, or human) decides.

위 문장은 서버가 제공한 도구 설명이다. 고정 구현의 in-process 평가에서는 비공백 수용 기준이 하나면 단일 평가 경로를 사용하므로, 설명과 달리 다중 기준 경로의 `checklist`, `ac_count`, `passed_count`, `run_feedback` 메타데이터가 항상 있다고 가정하지 않는다. 기준이 없으면 오류다. OpenCode plugin 위임은 in-process 평가 분기보다 먼저 선택될 수 있으며 위임 응답과 실제 평가 결과를 별도로 확인해야 한다. 실제 결과의 판정과 검사 증거를 확인한다. 분기와 제한은 [Seed 기준별 체크리스트 요청](/docs/evaluation-evolution-detail/)을 참고한다.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 예 | The execution session ID being verified |
| `seed_content` | string | 예 | Seed YAML containing acceptance_criteria, goal, constraints. The seed's acceptance_criteria list is evaluated in full. |
| `artifact` | string | 예 | The Run output/artifact to verify against the seed's ACs |
| `artifact_type` | string; 허용: `code`, `docs`, `config` | 아니요 | Type of artifact: code, docs, config. Default: code |
| `working_dir` | string | 아니요 | Project working directory (for language auto-detection). |

## `ouroboros_lateral_think`

Get unstuck, or decide a hard trade-off, with lateral thinking personas. Use when: the user says they are stuck or going in circles ("I've tried three fixes", "nothing works"), the same fix has failed twice, progress has stalled, OR the user faces a consequential choice with no clear winner (architecture, library, trade-off; hard to undo, or the team is split); call it proactively on these signals, before proposing yet another fix; do not wait for the user to ask for 'lateral' or 'unstuck'. Result: fresh perspectives from different thinking modes: hacker (unconventional workarounds), researcher (seeks information), simplifier (reduces complexity), architect (restructures approach), or contrarian (challenges assumptions). For decisions, pass mode='decision': personas advise on the choice and the synthesis must converge on ONE recommendation with flip conditions. Do not use when: work is progressing normally with no stagnation signal and no open decision. Set persona='all' (or pass personas=['hacker','architect',...]) to fan out to MULTIPLE personas in parallel — each runs in its own Task pane with an independent LLM context (no cross-contamination).

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `problem_context` | string | 예 | Description of the stuck situation or problem |
| `current_approach` | string | 예 | What has been tried so far that isn't working |
| `persona` | string; 허용: `hacker`, `researcher`, `simplifier`, `architect`, `contrarian`, `all` | 아니요 | Single persona (hacker, researcher, simplifier, architect, contrarian) OR 'all' to dispatch ALL 5 personas in parallel as separate Task panes. |
| `stagnation_pattern` | string; 허용: `spinning`, `oscillation`, `no_drift`, `diminishing_returns` | 아니요 | Detected stagnation pattern used to suggest a persona when persona is omitted. |
| `personas` | array | 아니요 | Explicit list of personas to dispatch in parallel. Takes precedence over 'persona' arg. Example: ['hacker','contrarian','architect']. Each runs in its own parallel Task pane. |
| `failed_attempts` | array | 아니요 | Previous failed approaches to avoid repeating |
| `session_id` | string | 아니요 | Interview/lateral session id the fan-out belongs to. The id is recorded with the fan-out so a later ouroboros_submit_fanout_results from a different session is refused. |
| `mode` | string; 허용: `unstuck`, `decision` | 아니요 | 'unstuck' (default): break through stagnation. 'decision': personas advise on a consequential choice; problem_context describes the options, current_approach the currently favored one (or 'undecided'). The fan-out synthesis contract then requires ONE recommendation, its grounds, the strongest dissent, and flip conditions. |
| `research` | boolean | 아니요 | Deep tier opt-in: personas ground claims with web evidence when their runtime exposes web tools, and emit a machine-readable evidence block. Slower; never the default. Runtimes without web tools degrade to opinion-only instead of failing. |

## `ouroboros_submit_fanout_results`

Submit correlated results from a subagent fan-out back to Ouroboros. After spawning the advisory/persona/investigation subagents declared by a prior tool's 'meta' (which stamped a 'fanout_id' and a 'result_correlation_key'), call this tool with one {key, content} per child output — 'key' is the value of the correlation field for that child. A child you could not spawn at all is exactly {key, undispatched: true}; never invent output. If the registered fan-out has a session_id or correlation_key, include that exact value; omit either only when the registered fan-out has no corresponding binding. Omission never waives a registered binding. Missing required keys return 'status=partial'; retry with EVERY lane. Completed advisory fan-outs return a bounded disposable artifact envelope for 'ouroboros_fetch_artifact'. Host-execution submissions instead acknowledge delivery to the execution engine; keep polling 'ouroboros_job_wait' for verification and further dispatches.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `session_id` | string | 아니요 | Interview/lateral session id. Supply the exact session_id stamped in the originating fan-out when one was registered; omit only when that fan-out has no session binding. An omitted value does not bypass a registered binding. |
| `fanout_id` | string | 예 | The fanout_id stamped into the originating tool's meta. |
| `correlation_key` | string | 아니요 | The result_correlation_key from the originating meta (e.g. 'context.persona' or 'code_facts'). Supply the exact registered value when present; omit only when the fan-out has no correlation binding. Omission does not bypass a registered binding. |
| `results` | array | 예 | Correlated child outputs: objects with a 'key' (the correlation value) and a 'content' (the child result), or 'undispatched': true when the child never ran. |

## `ouroboros_fetch_artifact`

Fetch and integrity-check a disposable Ouroboros artifact by the contract_id returned in an artifact envelope, or offered to an advisory lane beside the lane_id that produced it. For fan-out completion, continue from the synthesis in the returned 'body'. This is an explicit read and never re-executes the originating work.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `contract_id` | string | 아니요 | The contract_id from a disposable artifact envelope. Omit it and pass lane_id alone to list instead: that lane's own recent findings in this project, newest first, as contract_ids to read back with this same tool. |
| `lane_id` | string | 아니요 | Optional. Narrows a fan-out artifact to the output of one lane, returning that lane's body alone. Pass the lane_id offered beside the contract_id; omit it to read the whole artifact. A supplied lane the artifact does not carry is an error, never a broader read. |

## `ouroboros_evolve_step`

Run exactly ONE generation of the evolutionary loop. For Gen 1: provide lineage_id and seed_content (YAML). For Gen 2+: provide lineage_id only (state reconstructed from events). Returns generation result, convergence signal, and next action (continue/converged/ontology_stable/stagnated/exhausted/failed). ontology_stable is a non-success handoff; rerun the same lineage with execute=true to perform Execute→Evaluate. Checkpoint metadata and expired-claim recovery require the in-process runtime; plugin delegation rejects non-default values for these options.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | Lineage ID to continue or new ID for Gen 1 |
| `seed_content` | string | 아니요 | Seed YAML text for Gen 1. Pass a YAML-formatted string (for example, newline-delimited 'goal: ...' fields), not JSON-shaped text or an object literal; some MCP clients may otherwise coerce the value to an object before Ouroboros receives it. Omit for Gen 2+ (seed reconstructed from events). |
| `execute` | boolean | 아니요 | Whether to run seed execution and evaluation. True (default): full pipeline with Execute→Validate→Evaluate. False: ontology-only evolution (fast, no execution). |
| `benchmark_control` | boolean | 아니요 | Run a deliberate full-graph frugality control. Default: false. Requires execute=true, Gen 2+, an explicit Git project_dir, and a clean baseline; unavailable through plugin delegation. |
| `parallel` | boolean | 아니요 | Whether to run ACs in parallel. True (default): parallel execution (fast, may cause import conflicts). False: sequential execution (slower, more stable code generation). |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA evaluation. Default: false |
| `recover_expired_claim` | boolean | 아니요 | Explicitly recover an expired lineage writer claim after confirming the prior owner process is dead. Default: false |
| `project_dir` | string | 아니요 | Project root directory for validation (pytest collection check). If omitted, auto-detected from execution output or CWD. |
| `commit_policy` | string | 아니요 | Optional checkpoint commit policy for passed ACs. |
| `auto_session_id` | string | 아니요 | Optional auto session id for checkpoint commit metadata. |
| `execution_id` | string | 아니요 | Optional execution id for checkpoint commit metadata. |
| `checkpoint_commits` | array | 아니요 | Existing checkpoint commit records for idempotency. |
| `checkpoint_attempted_ac_ids` | array | 아니요 | Acceptance criteria already considered for checkpoint commits. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision authorizing this successor generation. |
| `predecessor_execution_id` | string | 아니요 | Execution or generation that this successor follows. |
| `conductor_directive` | object | 아니요 | Bounded corrective context for this successor generation. |

## `ouroboros_start_evolve_step`

Start one evolve_step generation in the background and return a job ID immediately for later status checks. In plugin mode, evolution is delegated to an OpenCode Task pane and job_id is None — results appear in the Task pane instead of being pollable via job_status/job_result. Checkpoint metadata and expired-claim recovery require the in-process runtime; plugin delegation rejects non-default values for these options.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | Lineage ID to continue or new ID for Gen 1 |
| `seed_content` | string | 아니요 | Seed YAML text for Gen 1. Pass a YAML-formatted string (for example, newline-delimited 'goal: ...' fields), not JSON-shaped text or an object literal; some MCP clients may otherwise coerce the value to an object before Ouroboros receives it. Omit for Gen 2+ (seed reconstructed from events). |
| `execute` | boolean | 아니요 | Whether to run seed execution and evaluation. True (default): full pipeline with Execute→Validate→Evaluate. False: ontology-only evolution (fast, no execution). |
| `benchmark_control` | boolean | 아니요 | Run a deliberate full-graph frugality control. Default: false. Requires execute=true, Gen 2+, an explicit Git project_dir, and a clean baseline; unavailable through plugin delegation. |
| `parallel` | boolean | 아니요 | Whether to run ACs in parallel. True (default): parallel execution (fast, may cause import conflicts). False: sequential execution (slower, more stable code generation). |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA evaluation. Default: false |
| `recover_expired_claim` | boolean | 아니요 | Explicitly recover an expired lineage writer claim after confirming the prior owner process is dead. Default: false |
| `project_dir` | string | 아니요 | Project root directory for validation (pytest collection check). If omitted, auto-detected from execution output or CWD. |
| `commit_policy` | string | 아니요 | Optional checkpoint commit policy for passed ACs. |
| `auto_session_id` | string | 아니요 | Optional auto session id for checkpoint commit metadata. |
| `execution_id` | string | 아니요 | Optional execution id for checkpoint commit metadata. |
| `checkpoint_commits` | array | 아니요 | Existing checkpoint commit records for idempotency. |
| `checkpoint_attempted_ac_ids` | array | 아니요 | Acceptance criteria already considered for checkpoint commits. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision authorizing this successor generation. |
| `predecessor_execution_id` | string | 아니요 | Execution or generation that this successor follows. |
| `conductor_directive` | object | 아니요 | Bounded corrective context for this successor generation. |

## `ouroboros_ralph`

**conductor 후속 호출:** `max_generations`를 생략하면 기본값 10이 적용된다. conductor 지시가 확인된 후속 호출에서는 1 이외의 값이 거부되므로, 생략하지 말고 `max_generations: 1`을 명시한다. 이는 아래 `ouroboros_start_ralph`에도 적용된다. [핸들러 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/ralph_handlers.py).

Start a first-class Ralph loop in the background. The loop repeatedly runs evolve_step until QA passes, convergence is reached, a terminal evolution action occurs, cancellation is requested, or max_generations is reached. In non-plugin runtimes, returns a job_id immediately for ouroboros_job_status, ouroboros_job_wait, ouroboros_job_result, and ouroboros_cancel_job. In OpenCode plugin mode, returns job_id=None and delegates the loop to the plugin child session.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | Lineage ID to start or continue. |
| `seed_content` | string | 아니요 | Seed YAML content for generation 1. Omit for continuation. |
| `execute` | boolean | 아니요 | Whether each generation should execute and evaluate. Default: true. |
| `parallel` | boolean | 아니요 | Whether each generation may execute ACs in parallel. Default: true. |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA. Default: false. |
| `project_dir` | string | 아니요 | Project root forwarded to each evolve_step generation. |
| `commit_policy` | string | 아니요 | Optional checkpoint commit policy forwarded to evolve_step. |
| `auto_session_id` | string | 아니요 | Optional auto session id used for checkpoint commit metadata. |
| `execution_id` | string | 아니요 | Optional execution id used for checkpoint commit metadata. |
| `checkpoint_commits` | array | 아니요 | Existing checkpoint commit records forwarded to evolve_step. |
| `checkpoint_attempted_ac_ids` | array | 아니요 | Acceptance criteria already considered for checkpoint commits. |
| `max_generations` | integer | 아니요 | Maximum generations to run before stopping. Default: 10. Range: 1-10. |
| `per_iteration_timeout_seconds` | number | 아니요 | Per-iteration wall-clock bound in seconds. In-process runtime: hard-enforced via asyncio.timeout, the loop stops with stop_reason='iteration_timeout' on expiry. OpenCode plugin runtime: advisory bound advertised to the child session via prompt + subagent context — the child is expected to honor it and return stop_reason='iteration_timeout', but the parent MCP process cannot interrupt the child, so a non-conforming child session may still exceed this bound. Default: 1800. Range: 30-7200. |
| `oscillation_window` | integer | 아니요 | Number of trailing iterations whose findings_hash must match (and QA must not have passed) to stop with stop_reason='oscillation_detected'. Default: 3. Range: 2-10. Values < 2 are rejected because a single iteration cannot oscillate with itself. |
| `grade_regression_window` | integer | 아니요 | Number of trailing iterations whose non-None grades must strictly decrease to stop with stop_reason='grade_regressing'. Default: 2. Range: 2-10. Values < 2 are rejected because strict-decrease requires at least two grades to compare. |
| `max_total_seconds` | number | 아니요 | Total wall-clock budget for the entire Ralph loop in seconds. In the in-process runner this is enforced by RalphLoopRunner: checked at the top of every iteration BEFORE launching evolve_step, and on exhaustion the loop stops with stop_reason='wall_clock_exhausted'. In OpenCode plugin mode the bound is forwarded to the child session and the plugin is expected to self-enforce; the MCP server cannot abort a foreign child process. When omitted, a derived ceiling of max_generations * per_iteration_timeout_seconds is auto-applied (with a WARNING log) for standalone callers. Range: 1-86400. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision authorizing one successor generation. |
| `predecessor_execution_id` | string | 아니요 | Execution or generation that this successor follows. |
| `conductor_directive` | object | 아니요 | Deterministic non-relaxing directive for one successor generation. |

## `ouroboros_start_ralph`

Fire-and-forget alias for ouroboros_ralph. Starts the same runtime-owned Ralph loop. In non-plugin runtimes, returns a job_id immediately for ouroboros_job_status, ouroboros_job_wait, ouroboros_job_result, and ouroboros_cancel_job. In OpenCode plugin mode, delegates to a plugin child session and returns job_id=None with status='delegated_to_plugin'; results are not pollable via job_status/job_result.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | Lineage ID to start or continue. |
| `seed_content` | string | 아니요 | Seed YAML content for generation 1. Omit for continuation. |
| `execute` | boolean | 아니요 | Whether each generation should execute and evaluate. Default: true. |
| `parallel` | boolean | 아니요 | Whether each generation may execute ACs in parallel. Default: true. |
| `skip_qa` | boolean | 아니요 | Skip post-execution QA. Default: false. |
| `project_dir` | string | 아니요 | Project root forwarded to each evolve_step generation. |
| `commit_policy` | string | 아니요 | Optional checkpoint commit policy forwarded to evolve_step. |
| `auto_session_id` | string | 아니요 | Optional auto session id used for checkpoint commit metadata. |
| `execution_id` | string | 아니요 | Optional execution id used for checkpoint commit metadata. |
| `checkpoint_commits` | array | 아니요 | Existing checkpoint commit records forwarded to evolve_step. |
| `checkpoint_attempted_ac_ids` | array | 아니요 | Acceptance criteria already considered for checkpoint commits. |
| `max_generations` | integer | 아니요 | Maximum generations to run before stopping. Default: 10. Range: 1-10. |
| `per_iteration_timeout_seconds` | number | 아니요 | Per-iteration wall-clock bound in seconds. In-process runtime: hard-enforced via asyncio.timeout, the loop stops with stop_reason='iteration_timeout' on expiry. OpenCode plugin runtime: advisory bound advertised to the child session via prompt + subagent context — the child is expected to honor it and return stop_reason='iteration_timeout', but the parent MCP process cannot interrupt the child, so a non-conforming child session may still exceed this bound. Default: 1800. Range: 30-7200. |
| `oscillation_window` | integer | 아니요 | Number of trailing iterations whose findings_hash must match (and QA must not have passed) to stop with stop_reason='oscillation_detected'. Default: 3. Range: 2-10. Values < 2 are rejected because a single iteration cannot oscillate with itself. |
| `grade_regression_window` | integer | 아니요 | Number of trailing iterations whose non-None grades must strictly decrease to stop with stop_reason='grade_regressing'. Default: 2. Range: 2-10. Values < 2 are rejected because strict-decrease requires at least two grades to compare. |
| `max_total_seconds` | number | 아니요 | Total wall-clock budget for the entire Ralph loop in seconds. In the in-process runner this is enforced by RalphLoopRunner: checked at the top of every iteration BEFORE launching evolve_step, and on exhaustion the loop stops with stop_reason='wall_clock_exhausted'. In OpenCode plugin mode the bound is forwarded to the child session and the plugin is expected to self-enforce; the MCP server cannot abort a foreign child process. When omitted, a derived ceiling of max_generations * per_iteration_timeout_seconds is auto-applied (with a WARNING log) for standalone callers. Range: 1-86400. |
| `conductor_decision_id` | string | 아니요 | Selected conductor decision authorizing one successor generation. |
| `predecessor_execution_id` | string | 아니요 | Execution or generation that this successor follows. |
| `conductor_directive` | object | 아니요 | Deterministic non-relaxing directive for one successor generation. |

## `ouroboros_lineage_status`

Query the current state of an evolutionary lineage. Returns generation count, status, ontology evolution, and convergence progress.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | ID of the lineage to query |

## `ouroboros_evolve_rewind`

Rewind an evolutionary lineage to a specific generation. Truncates all generations after the target and emits a lineage.rewound event. The lineage can then continue evolving from the rewind point.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | ID of the lineage to rewind |
| `to_generation` | integer | 예 | Generation number to rewind to (inclusive) |

## `ouroboros_cancel_execution`

Cancel a running or paused Ouroboros execution. Validates that the execution exists and is not already in a terminal state (completed, failed, cancelled) before cancelling.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `execution_id` | string | 예 | The execution/session ID to cancel |
| `reason` | string | 아니요 | Reason for cancellation 스키마 기본값: `"Cancelled by user"`. |

## `ouroboros_brownfield`

Manage brownfield repository registrations. Scan home directory for repos, register/query repos, or set the default brownfield context for PM interviews.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `action` | string; 허용: `scan`, `register`, `query`, `set_default`, `set_defaults` | 아니요 | Action to perform: 'scan' to discover repos from ~/, 'register' to add a single repo, 'query' to list all registered repos from the DB without rescanning, get the default, or rank repos by 'text', 'set_default' to toggle a repo's default flag (supports multiple defaults; does NOT clear others). Auto-detected from parameters when omitted. |
| `path` | string | 아니요 | Absolute filesystem path of the repository. Required for 'register' and 'set_default' actions. |
| `name` | string | 아니요 | Human-readable name for the repository. Used with 'register'. Defaults to directory name. |
| `desc` | string | 아니요 | One-line description of the repository. Used with 'register'. Optional. |
| `is_default` | boolean | 아니요 | For 'set_default' action: set to true to mark as default, false to unmark. Defaults to true. |
| `default_only` | boolean | 아니요 | When true with 'query' action, return only the default repo instead of the full list. Defaults to false. |
| `scan_root` | string | 아니요 | Existing directory to walk for the 'scan' action. Defaults to the current user's home directory. |
| `indices` | string | 아니요 | Comma-separated repo numbers from the scan list (e.g. '6,18,19'). Used with 'set_defaults' action to replace all defaults at once. |
| `text` | string | 아니요 | Free-text topic for the 'query' action. When set, repos are ranked by BM25 relevance over name, description, path, manifest, README head, and top-level entries stored at scan time; only matching repos are returned, best first. offset/limit then page the ranked list (limit defaults to 10). |
| `offset` | integer | 아니요 | Number of rows to skip for 'query' pagination. Defaults to 0. |
| `limit` | integer | 아니요 | Maximum number of rows to return for 'query' pagination. Omit for no limit. |

## `ouroboros_pm_interview`

**조건부 입력:** 새 인터뷰에는 `initial_context`, 기존 인터뷰 재개 및 `action: "generate"`에는 `session_id`가 필요하다. `selected_repos`만 주면 자동으로 `select_repos` 단계가 선택되며 앞 단계의 `session_id`도 필요하다. `selected_repos`와 `initial_context`를 함께 주면 새 시작으로 감지된다. 명시적인 `action`은 자동 감지보다 우선한다. `answer`와 `answers`는 함께 사용할 수 없고, 단일 `answer`에는 해당 질문의 `last_question`을 함께 보낸다. 질문 목록이 서버에 계획된 경우 답변 배치의 질문 식별자가 그 목록과 정확히 일치해야 한다. 답변 형식을 모두 생략하면 기존 세션 재연결 경로다. [동작 감지·검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/pm_handler.py), [답변 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/pm_batch.py).

PM interview for product requirements gathering. Use when: the user wants a PRD or product requirements rather than code ("write a PRD", "spec this feature for the team"). Start with initial_context, continue with session_id + answer, or generate PM seed with action='generate'. In plugin mode, returns a delegation receipt (status=delegated_to_subagent) and the PM interview executes in an OpenCode Task pane — the real session_id is returned there.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `initial_context` | string | 아니요 | Initial product description to start a new PM interview |
| `session_id` | string | 아니요 | Session ID to resume an existing PM interview |
| `answer` | string | 아니요 | PM's response to a single-question turn. Pass the question it answers as 'last_question'. This singular form is mutually exclusive with 'answers'; for a turn that asked more than one question, use 'answers' instead. |
| `answers` | array; 최소 항목 1; 최대 항목 3; 항목: object (`question`, `answer` 필수; 추가 속성 불가) | 아니요 | A turn's answers, sent together: [{question, answer}, ...], one entry per question the turn asked. This batch form is mutually exclusive with 'answer'. A turn is recorded whole, so collect every answer before calling. Each entry names its own question and the batch accepts one to three entries. |
| `action` | string | 아니요 | Action to perform. Auto-detected from parameter presence when omitted: initial_context → 'start', session_id + answer → 'resume'. Use 'generate' explicitly to produce PM seed from completed interview. |
| `cwd` | string | 아니요 | Working directory for PM document output. Defaults to current working directory. Brownfield context is loaded from DB (is_default=true). |
| `selected_repos` | array; 항목: string | 아니요 | List of repository paths selected for brownfield context (2-step start: returned by step 1, sent back in step 2). All repos are assigned role=main. When provided with initial_context, starts the interview with the selected brownfield repos. |
| `last_question` | string | 아니요 | The question this answer is answering. A turn persists nothing when it asks, on any runtime, so an answer without its question is refused — there is no remembered question to file it under, and the round behind it is one somebody already answered. |

## `ouroboros_qa`

General-purpose QA verdict for any artifact type. Evaluates code, API responses, documents, screenshots, or custom artifacts against a quality bar. Returns structured verdict with score, differences, and actionable suggestions. Designed for iterative loop usage.

| 입력 | 타입 | 스키마 필수 | 설명 |
| --- | --- | --- | --- |
| `artifact` | string | 예 | The artifact content to evaluate (code, text, JSON, etc.) |
| `quality_bar` | string | 예 | Natural language description of what 'pass' means. E.g., 'All public functions must have type hints and docstrings.' |
| `artifact_type` | string; 허용: `code`, `api_response`, `document`, `screenshot`, `test_output`, `custom` | 아니요 | Type of artifact: code, api_response, document, screenshot, test_output, custom. Default: code |
| `reference` | string | 아니요 | Optional reference artifact for comparison (expected output, target schema, reference description). |
| `pass_threshold` | number; 최소 0.0; 최대 1.0 | 아니요 | Score threshold for pass verdict (0.0-1.0). Default: 0.80 |
| `qa_session_id` | string | 아니요 | QA session ID for multi-iteration tracking. If omitted, a new session is created. |
| `iteration_history` | array | 아니요 | Previous iteration results for loop context (JSON array). |
| `seed_content` | string | 아니요 | Optional seed YAML for additional context (goal, constraints). |


## 실제 stdio 서버에서 추가 노출된 도구

고정 소스의 `mcp serve --runtime claude-cli`를 격리 환경에서 시작하고 MCP `list_tools`를 호출했을 때 기본 팩토리의 32개 외에 다음 4개가 더 노출되었다. 도구 호출이나 호스트별 노출은 시험하지 않았다. 아래는 그 서버의 입력 JSON Schema에서 추출했다.

### `ouroboros_record_conductor_decision`

| 입력 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `decision_id` | string | 예 | Stable idempotent decision ID. |
| `phase` | string; 허용: `selected`, `completed`, `failed`, `declined` | 예 | Decision phase. |
| `attention_event_id` | string | 아니요 | Source attention relay/event ID; required for selected. |
| `evidence_event_ids` | array | 아니요 | Bounded evidence event IDs; required for selected. |
| `verification_summary` | string | 아니요 | Short read-only verifier conclusion; required for selected. |
| `selected_action` | string | 아니요 | Selected menu action; required for selected. |
| `selected_effect` | string; 허용: `read_only`, `successor_only`, `specification_change`, `user_escalation` | 아니요 | Action effect class; required for selected. |
| `actor_mode` | string; 허용: `run`, `auto`, `ralph`, `advisory` | 아니요 | Host policy mode; required for selected. |
| `engine_ownership_state` | string; 허용: `active`, `closed`, `unknown` | 아니요 | Authoritative ownership state from the attention envelope. |
| `action_arguments` | object | 아니요 | Action arguments; only a digest and bounded key list are persisted. |
| `conductor_directive` | object | 아니요 | Optional bounded corrective successor directive. |
| `root_job_id` | string | 아니요 | Root job used for the two-successor budget. |
| `predecessor_execution_id` | string | 아니요 | Execution that the selected successor will follow. |
| `user_approval_event_id` | string | 아니요 | Required approval receipt for specification changes. |
| `result_receipt` | string | 아니요 | Bounded outcome receipt or failure/decline reason for terminal phases. |
| `successor_execution_id` | string | 아니요 | New execution ID returned by a completed successor action. |

### `ouroboros_session_signal_targets`

| 입력 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `execution_id` | string | 예 | Execution ID returned by run/auto/evolve/ralph start or its job observer. |

### `ouroboros_session_signal`

| 입력 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `target_session_scope_id` | string | 예 | Stable logical AC session scope ID. |
| `target_session_attempt_id` | string | 예 | Exact runtime attempt ID; stale attempts fail closed. |
| `expected_execution_id` | string | 예 | Execution generation guard. |
| `mode` | string; 허용: `inform`, `after_turn`, `redirect`, `replace` | 예 | Requested Synapse delivery mode. For the direct path, the exact attempt must advertise the requested mode in ouroboros_session_signal_targets. For the sole fallback path, redirect may be requested while omitted from discovery only when fallback_mode=after_turn is explicit and that attempt advertises after_turn; its effective mode is then after_turn. Shipped adapters currently advertise/effect only inform and after_turn; redirect and replace remain reserved advertised/effective capabilities. |
| `fallback_mode` | string; 허용: `after_turn` | 아니요 | Explicit redirect-only fallback; after_turn is the sole valid value and is used only when the selected attempt advertises after_turn. |
| `message` | string | 예 | Bounded additive implementation intent; no secrets or transcripts. |
| `source` | string; 허용: `user`, `conductor`, `worker` | 예 | Audited source authority. |
| `contract_effect` | string; 허용: `additive`, `specification_change` | 아니요 | Whether this preserves the approved shared contract or changes the goal, ACs, constraints, or non-goals. 스키마 기본값: `"additive"`. |
| `reason` | string | 예 | Short user-visible rationale. |
| `idempotency_key` | string | 예 | Stable key for this exact execution/scope/attempt intent. |
| `expires_at` | string | 아니요 | Optional timezone-aware ISO-8601 expiry. |
| `user_approval_event_id` | string | 아니요 | Required approval receipt for replace mode. |
| `expected_contract_version` | integer | 아니요 | Optional shared execution-contract generation guard. |

### `ouroboros_ac_dashboard`

| 입력 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `lineage_id` | string | 예 | ID of the lineage to display |
| `mode` | string | 아니요 | Display mode: 'summary' (default), 'full', or 'ac' |
| `ac_index` | integer | 아니요 | AC index (1-based) for 'ac' mode. Required when mode='ac'. |
