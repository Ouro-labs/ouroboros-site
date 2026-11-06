# 설정 필드 상세 참조

!!! warning "판본과 검증 범위"
    아래 항목과 합성 관찰은 **고정 소스 `722172ef096767583679d04aef5e847458fee6b2`** 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)이나 공개 패키지 `0.59.9`, 실행 중인 호스트 서버에 동일하게 적용된다고 가정하지 마세요. 설치된 CLI 도움말 또는 연결된 서버의 실제 스키마를 우선 확인합니다. 2026-11-07 소스 트리 비교에서 두 커밋 사이 CLI 명령 디렉터리는 `init.py`·`run.py`의 Seed YAML 읽기에 UTF-8 인코딩이 명시됐고, MCP·설정 디렉터리와 제품 CLI·설정·MCP 참조 문서는 변경 파일이 없었습니다. 이는 의존 코드·설치물·런타임 전체의 동등성이나 실제 호스트 실행을 증명하지 않습니다. 현재 [CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [설정 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/config-reference.md), [MCP 도구 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools)를 함께 확인하세요. 전체 현재 CLI·MCP 스키마와 모든 설정 조합은 실사용으로 전수 검증하지 않았습니다.


기준: 2026-11-04, 고정 source `722172ef096767583679d04aef5e847458fee6b2`의 `OuroborosConfig` Pydantic JSON Schema를 추출했다. 이 표는 모델 필드의 선언을 보여 주며 환경 변수·설정 파일 우선순위, 동적 모델 선택과 유효성 검사의 모든 조건을 대신하지 않는다. 실제 적용 값은 설치한 버전의 `ouroboros config show`와 [원본 설정 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md), [설정 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/models.py)을 확인한다. `기본 없음`은 Schema에 정적 default가 없다는 뜻이며 필수 입력이라는 뜻이 아니다. credential 값은 입력·출력하지 않는다.

**저장·로그 설정의 적용 범위:** 고정 소스에서 독립 CLI `run`의 orchestrator 경로는 `persistence.enabled`와 관계없이 이벤트 저장소를 초기화한다. 합성 설정에서 `false`를 읽은 뒤 초기화 직후 중단한 시험에서도 없던 임시 DB 파일이 생성됐다. 이는 이벤트 내용이 저장됐다는 증거는 아니다. 따라서 이 설정을 개인정보 저장 차단 스위치로 사용하지 않는다. `logging.include_reasoning`도 선언만으로 모든 로그 경로의 제거·비기록을 보장하지 않는다. 실제 데이터·로그 흐름과 보존 정책을 별도로 확인한다. [고정 CLI 실행기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [설정 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/models.py). 정적 소스 대조이며 실행·모든 호스트는 시험하지 않았다.

**파일 로그의 보존·마스킹 경계:** 별도 관측 로거의 기본 설정은 파일 로깅 활성화, UTC 자정 기준 일별 회전과 `backupCount=7`이다. 이는 회전 파일 개수 설정이지 모든 로그·백업이 정확히 7일 후 삭제된다는 보장은 아니다. 파일 핸들러 생성에 `OSError`가 나면 파일 핸들러 없이 계속할 수 있으므로 파일 부재를 로그 발생이나 표준 오류 출력의 부재로 해석하지 않는다. 로깅 프로세서는 민감 필드와 자격증명 모양의 값을 마스킹하지만, 문자열 이벤트는 자격증명 모양이 아니면 그대로 남을 수 있다. 따라서 마스킹이 모든 개인정보·민감한 자유 문장을 제거한다고 가정하지 말고, 실제 배포의 로그 수집·접근·보존 및 공유 전에 검토한다. 이는 [고정 관측 로거 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/observability/logging.py)의 기본 경로에 대한 정적 대조이며 다른 로거·호스트의 출력과 실제 보존 기간은 검증하지 않았다.

## 실행 전에 확인할 기본값과 범위

- **권한은 설정값만으로 판단하지 않는다.** OpenCode 작업 런타임의 `orchestrator.opencode_permission_mode` 선언 기본값은 `bypassPermissions`다. 이 판본의 Seed orchestrator subprocess 실행은 런타임에 해당하는 bypass 모드를 강제하며 OpenCode CLI에서는 `--dangerously-skip-permissions`에 대응한다. 별도 OpenCode plugin 위임은 [브리지 권한 경계](/docs/opencode-bridge-detail/)를 따른다. LLM 어댑터의 인터뷰 용도도 별도의 명시적 `permission_mode` 인자가 없는 경우 OpenCode 등을 bypass로 선택한다. 설정 표의 `llm.opencode_permission_mode=acceptEdits`를 모든 실행의 승인 경계로 해석하지 않는다. 런타임별 전달 차이는 [런타임 지원](/docs/runtime-support-detail/), 실제 호출 경로는 [runner](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py)와 [LLM factory](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/providers/factory.py)를 참조한다.
- **실행 샌드박스는 전체 에이전트 격리가 아니다.** `execution.exec_sandbox`는 검증 명령 재실행 등 컨트롤러가 자체 권한으로 실행하는 명령을 대상으로 기본 활성화된다. 신뢰된 환경의 `OUROBOROS_EXEC_SANDBOX`가 인식 가능한 on/off 값이면 설정 파일보다 우선하며 프로젝트 `.env`에서는 설정할 수 없다. 빈 값이나 인식하지 못하는 값은 설정 파일로 되돌아간다. `off`·`0`·`false`·`no` 또는 설정의 `false`는 해당 명령을 비격리로 실행한다. 지원 백엔드를 사용할 수 없을 때는 명령을 실행하지 않고 결과가 `indeterminate`가 된다. 실행 시작 시 정책이 고정되므로 다른 값으로 재개하려 하면 거부된다. Seed에 명시된 `verify_command`의 성공 계약 게이트는 별도의 셸 직접 실행 경로이므로 이 설정이 그 명령의 네트워크·작업공간 밖 쓰기를 격리한다고 가정하지 않는다. 작업공간 digest 비교는 격리나 부작용 취소가 아니다. [Seed 검증 경계](/docs/seed-format-detail/)를 함께 확인한다. 이는 LLM 런타임이나 모든 외부 도구의 권한을 제한한다는 뜻이 아니다. [설정·플랫폼별 범위](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md), [스위치 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/exec_sandbox.py).
- **사용 통계는 기본 활성화된다.** 소스의 개인정보 계약은 명령·상태 등 제한된 차원의 익명 이벤트를 PostHog에 보내며 코드·프롬프트·Seed 내용·경로·인자를 수집하지 않는다고 명시한다. `DO_NOT_TRACK=1`, `OUROBOROS_TELEMETRY=0`, 또는 `telemetry.enabled: false` 중 하나로 비활성화할 수 있다. 어느 비활성화 조건도 `OUROBOROS_TELEMETRY=1`로 덮어쓰지 못하며, 설정을 읽지 못하거나 유효하지 않으면 비활성화된다. 이는 소스상 계약이며 이 문서 작성에서 실제 네트워크 전송을 검증한 것은 아니다. [원본 통계 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/TELEMETRY.md), [설정 판정](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py).


### `.env` 로딩과 작업 디렉터리

고정 소스의 설정 로더는 import 시 **현재 작업 디렉터리**의 `.env`를 먼저 읽고, 이어 `~/.ouroboros/.env`를 읽는다. 이미 프로세스 환경에 존재하는 값은 일반적으로 교체하지 않으므로, 두 파일에 같은 허용 키가 있고 프로세스에 값이 없다면 프로젝트 파일의 값이 홈 파일보다 먼저 적용된다. 예외적으로 API 키 형식의 템플릿 자리표시자 값은 비어 있는 것처럼 취급할 수 있다. 파일의 빈 값·값 없는 키는 건너뛰며 `${VAR}`를 다른 환경 변수로 치환하지 않는다. 설정 YAML과 개별 옵션의 최종 우선순위까지 이 순서로 일반화하지 말고 해당 설정의 설명을 확인한다.

프로젝트 `.env`는 신뢰하지 않는 입력으로 취급해 실행 파일 경로, 권한 모드, `PATH`·`PYTHONPATH`, `OUROBOROS_EXEC_SANDBOX` 등 [차단 목록](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/untrusted_env.py)의 키는 적용하지 않는다. 홈 파일과 이미 설정된 프로세스 환경은 같은 제한을 받지 않는다. 차단 목록이 프로젝트의 모든 설정·부작용을 무해하게 만든다는 뜻은 아니다. 서로 다른 프로젝트에서 값이 달라진다면 실행한 디렉터리와 세 소스를 확인하되, 비밀값을 출력하거나 공유하지 않는다. [로더 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py).

격리 임시 HOME·프로젝트에서 합성 키로 확인했을 때 중복 키는 프로젝트 값이, 홈 전용 키와 홈의 sandbox 값은 홈 값이 적용됐고, 프로젝트의 sandbox 값은 차단됐으며 `${UNRELATED}`는 문자 그대로 남았다. 이는 로더 import에 한정한 시험으로 실제 인증·모델 호출이나 모든 설정 경로를 검증하지 않았다.

| 경로 | 타입 / 제한 | Schema 기본값 | 설명 |
| --- | --- | --- | --- |
| `economics.default_tier` | string: frugal, standard, frontier | `"frugal"` | 적응형 라우팅의 기준 tier를 결정한다. 실제 시작 tier는 작업 신뢰와 정책에 따라 달라진다. |
| `economics.tiers` | object | `기본 없음` | tier별 모델·상대 비용·용도 정의. |
| `economics.escalation_threshold` | integer (minimum=1) | `2` | 일부 재시도 기반 모델 선택의 승격 임계값. 최상위 AC의 bounded route에는 적용되지 않는다. |
| `economics.downgrade_success_streak` | integer (minimum=1) | `5` | 호환용으로 허용되지만 읽지 않는다. 연속 성공에 따른 자동 하향은 없다. |
| `llm.backend` | string: claude, claude_code, litellm, codex, copilot, gemini, opencode, kiro, hermes, goose, pi, omp, ourocode, dsh, gjc, zcode, megacode | `"claude_code"` | 인터뷰·QA 등 LLM 전용 호출 백엔드. 실행 작업의 runtime과 별도. |
| `llm.permission_mode` | string: default, acceptEdits, bypassPermissions | `"default"` | OpenCode 이외 LLM 호출의 저장된 권한 모드. |
| `llm.opencode_permission_mode` | string: default, acceptEdits, bypassPermissions | `"acceptEdits"` | OpenCode LLM 호출의 저장된 권한 모드. 위 실행 경로별 예외 참조. |
| `llm.qa_model` | string | `"auto"` | 실행 후 QA 판정 모델. |
| `llm.dependency_analysis_model` | string | `"auto"` | AC 의존성 분석 모델. |
| `llm.ontology_analysis_model` | string | `"auto"` | 온톨로지 분석 모델. |
| `llm.context_compression_model` | string | `"auto"` | 워크플로 문맥 압축 모델. |
| `models.default` | string | `"auto"` | auto는 역할별 tier, tier명은 전체 역할에 해당 tier, 모델 ID는 전체 역할에 해당 ID를 선택. |
| `models.pin` | boolean | `false` | 역할별 저장 모델 ID를 사용할지. 꺼져 있으면 일반적으로 무시하지만 LiteLLM·Copilot은 예외. |
| `clarification.ambiguity_threshold` | number (minimum=0.0, maximum=1.0) | `0.2` | Seed 생성 진행을 허용하는 최대 모호성 점수. |
| `clarification.max_interview_rounds` | integer (minimum=1) | `10` | 인터뷰 질의·응답 최대 회차. |
| `clarification.model_tier` | string: frugal, standard, frontier | `"standard"` | 명확화 단계의 PAL tier. |
| `clarification.default_model` | string | `"auto"` | 인터뷰와 Seed 생성 모델. |
| `execution.max_iterations_per_ac` | integer (minimum=1) | `10` | AC 하나의 실행 반복 상한. |
| `execution.retrospective_interval` | integer (minimum=1) | `3` | 자동 회고 사이의 반복 횟수. |
| `execution.tui_autolaunch` | boolean | `false` | ooo run에서 TUI를 묻지 않고 열지 여부. |
| `execution.auto_evaluate` | boolean | `true` | 평가 가능한 종료 실행 뒤 정식 평가를 자동 등록한다. 독립 CLI와 MCP 실행에 적용되며 호출별 옵션이 우선한다. 세션·산출물이 없거나 등록에 실패하면 평가가 시작되지 않을 수 있다. |
| `execution.auto_evolve` | boolean | `true` | MCP 백그라운드 평가나 실행 후 successor 체인의 정식 평가에서 `final_approved=false`이면 제한된 Ralph 등록을 시도하며 `unverified`도 포함한다. 동기 `ouroboros_evaluate` 호출 자체가 이 체인을 등록하는 것은 아니다. 독립 CLI `ouroboros run`도 후속 체인을 등록하고 정상적으로 평가·Ralph의 종료까지 추적한다. 추적 중 Ctrl-C는 추적을 멈출 뿐 작업 취소를 뜻하지 않으며, 실제 job 상태를 확인해야 한다. `--auto-evolve`/`--no-auto-evolve` 또는 MCP 호출별 옵션이 설정에 우선한다. 평가 미실행, Seed 부재·등록 실패 시 Ralph가 시작된다는 보장은 없다. |
| `execution.auto_evolve_max_generations` | integer (minimum=1, maximum=10) | `3` | 자동 연결 Ralph의 최대 세대 수. |
| `execution.default_model` | string / null | `null` | Execute 모델 선택값. 모델 pin 정책과 백엔드 예외가 적용된다. |
| `execution.run_verify_commands` | boolean | `true` | AC 산출물과 verify_command를 확인하고 허용된 근거 명령을 재실행할지 여부. |
| `execution.verify_command_timeout_seconds` | integer (minimum=1) | `600` | 각 verify_command와 재실행 명령의 제한 시간(초). |
| `execution.exec_sandbox` | boolean | `true` | 컨트롤러 자체 명령의 격리. 위 경고 참조. |
| `execution.ac_retry_attempts` | integer (minimum=0) | `2` | 실패 AC를 실패 처리하기 전 재배정하는 횟수. stall 재시도는 제외. |
| `execution.cross_harness_redispatch` | boolean | `false` | 저장된 이 필드는 현재 활성화 근거로 읽히지 않는다. 다른 런타임 재배정은 프로세스 환경 `OUROBOROS_CROSS_HARNESS_REDISPATCH`의 명시적 opt-in이 필요하다. |
| `execution.n_version_tournament` | boolean | `false` | 선언된 opt-in 필드이나 이 판본의 tournament는 준비 코드이며 실행 트리거에 연결되지 않았다. true만으로 병렬 실행되지 않는다. |
| `execution.decomposition_mode` | string: bounce_only, off | `"bounce_only"` | bounce_only는 근거 있는 과대 작업 bounce 뒤에만 분할, off는 분할 비활성화. |
| `execution.context_pack` | boolean | `true` | 저장소 구조·검증 명령 등의 결정적 문맥을 worker 프롬프트에 추가. 고정 로더의 `OUROBOROS_CONTEXT_PACK`은 대소문자·앞뒤 공백을 정리한 `1/true/on/yes`, `0/false/off/no`만 각각 켜고 끄며 YAML보다 우선한다. 인식하지 못한 값은 YAML로 넘어가고, YAML을 읽거나 검증하는 과정에서 `ConfigError`가 나면 이 getter는 **true로 돌아간다**. 따라서 환경 변수 오타나 손상된 설정에서 문맥 수집이 꺼졌다고 가정하지 않는다. 합성 설정에서 이 getter의 우선순위만 확인했으며 실제 worker 프롬프트는 미시험이다. [로더](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py). |
| `execution.project_guidance` | array | `[]` | 프로젝트 guidance ID 허용 목록. 각 ID의 GUIDANCE.md를 실행 시스템 프롬프트에 추가. |
| `execution.default_policy` | string: ask, efficient, quality_first | `"quality_first"` | 새 실행의 기본 정책. 명시적 호출 인자가 우선하고 재개는 기존 계약을 유지. |
| `execution.transcript_verifier` | string: decide, record | `"record"` | record는 가상 판단만 기록, decide는 거부 시 실패와 재시도를 결정. verify_command 실패는 양쪽에서 결정. |
| `resilience.stagnation_enabled` | boolean | `true` | 정체 패턴 탐지 사용 여부. |
| `resilience.lateral_thinking_enabled` | boolean | `true` | 정체 시 관점 전환 사용 여부. |
| `resilience.lateral_model_tier` | string: frugal, standard, frontier | `"frontier"` | 관점 전환 호출의 모델 tier. |
| `resilience.lateral_temperature` | number (minimum=0.0, maximum=2.0) | `0.8` | 관점 전환 프롬프트의 sampling temperature. |
| `resilience.wonder_model` | string | `"auto"` | 발산 탐색 Wonder 모델. |
| `resilience.reflect_model` | string | `"auto"` | 수렴·종합 Reflect 모델. |
| `evaluation.stage1_enabled` | boolean | `true` | 이 YAML 필드는 현재 런타임 빌더에 연결되지 않는다. |
| `evaluation.stage2_enabled` | boolean | `true` | 이 YAML 필드는 현재 런타임 빌더에 연결되지 않는다. |
| `evaluation.stage3_enabled` | boolean | `true` | 이 YAML 필드는 현재 런타임 빌더에 연결되지 않는다. |
| `evaluation.satisfaction_threshold` | number (minimum=0.0, maximum=1.0) | `0.8` | 현재 미연결. Stage 2 게이트는 고정 0.8을 사용한다. |
| `evaluation.uncertainty_threshold` | number (minimum=0.0, maximum=1.0) | `0.3` | 이 YAML 필드는 현재 트리거 설정에 연결되지 않는다. |
| `evaluation.semantic_model` | string | `"auto"` | Stage 2 의미 평가 모델. |
| `evaluation.assertion_extraction_model` | string | `"auto"` | Seed 기준에서 검증 assertion을 추출하는 모델. |
| `consensus.min_models` | integer (minimum=2) | `3` | 현재 미연결. 단순 합의는 독립성 필터 후 성공 투표 2개 이상을 별도로 요구한다. |
| `consensus.threshold` | number (minimum=0.0, maximum=1.0) | `0.67` | 현재 미연결. 단순 합의는 별도 ConsensusConfig의 기본 0.66을 사용한다. |
| `consensus.diversity_required` | boolean | `true` | 현재 읽지 않는 필드. 이름만으로 제공자 다양성이 보장되지 않는다. |
| `consensus.models` | array | `["auto"]` | 단순 투표 모델 목록. auto는 역할 모델을 반복하며 백엔드별 예외가 있다. |
| `consensus.advocate_model` | string | `"auto"` | 숙의형 합의에서 찬성 논거 모델. |
| `consensus.devil_model` | string | `"auto"` | 숙의형 합의에서 반대 논거 모델. |
| `consensus.judge_model` | string | `"auto"` | 숙의형 합의에서 최종 판정 모델. |
| `llm_profiles` | object | `기본 없음` | 백엔드별 선택을 포함하는 재사용 LLM 작업 프로필. |
| `llm_role_profiles` | object | `기본 없음` | 논리적 작업 역할에서 LLM 프로필로의 매핑. |
| `persistence.enabled` | boolean | `true` | 선언된 이벤트 저장 선호값. 이 값만으로 저장이 꺼진다고 가정하지 않는다: 고정 독립 CLI `run`의 orchestrator 경로는 이 필드를 검사하지 않고 `EventStore()`를 만들고 초기화한다. 모든 진입점과 동적 참조는 별도 검증이 필요하다. |
| `persistence.database_path` | string | `"data/ouroboros.db"` | 설정 모델의 선언 기본값. 설정 파일이 없거나 실제 YAML에 필드가 없으면 설정 파일 디렉터리의 legacy `ouroboros.db`를 선택한다(기본 설정 위치는 `~/.ouroboros/`). 설정 파일이 없을 때는 대상 유형을 미리 검사하지 않으며, 파일이 있고 필드가 없는 분기는 기존 legacy 대상이 파일이 아니면 오류다. 비어 있지 않은 문자열로 명시하면 `~`를 확장하고 상대 경로는 설정 파일 디렉터리 기준, 절대 경로는 그대로 후보로 삼는다. 존재하는 명시 후보가 파일이 아니면 오류이고, 후보가 없을 때 legacy가 파일이면 legacy를 우선한다. 파일 대상 심볼릭 링크는 허용한다. 명시된 null·공백·비문자열 값은 유효하지 않다. [경로 선택](/docs/lifecycle-detail/). |
| `drift.warning_threshold` | number (minimum=0.0, maximum=1.0) | `0.3` | 드리프트 경고 이벤트 임계값. |
| `drift.critical_threshold` | number (minimum=0.0, maximum=1.0) | `0.5` | 드리프트 개입 임계값. warning 이상이어야 한다. |
| `runtime_controls.mcp_tool_timeout_seconds` | number (minimum=0) | `0` | 고정 소스에서 `ouroboros_evolve_step` 핸들러가 MCP 서버 어댑터에 제공하는 `handler.handle` 제한 시간(초). 어댑터는 보안 검사와 startup을 마친 뒤에만 이 제한을 적용하므로 전체 요청의 벽시계 상한이 아니다. `0`은 이 핸들러 호출의 어댑터 제한을 사용하지 않지만 클라이언트·generation watchdog·다른 도구의 별도 시간 제한이 없다는 뜻은 아니다. [핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py), [어댑터](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py). 합성 security·startup·handler를 주입한 직접 어댑터 시험에서 선행 단계는 제한 밖이고 느린 handler만 timeout되는 한 사례를 확인했다. 실제 evolve·서버·인증·운영 부하는 미시험이다. |
| `runtime_controls.generation_idle_timeout_seconds` | number (minimum=0) | `7200` | 이벤트 저장소 활동이 없는 세대의 idle 제한 시간(초). `0`은 이 검사만 비활성화한다. |
| `runtime_controls.generation_no_progress_timeout_seconds` | number (minimum=0) | `14400` | 마지막 실질 진전 이후 제한 시간(초). 활동이 전혀 없어도 경과하며 idle 검사가 비활성화되었거나 더 길면 먼저 작동할 수 있다. `0`은 이 검사만 비활성화한다. [watchdog 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/watchdog.py). |
| `runtime_controls.generation_safety_timeout_seconds` | number (minimum=0) | `0` | 세대의 최종 안전 시간 상한(초). 0은 비활성. |
| `runtime_controls.watchdog_poll_seconds` | number (exclusiveMinimum=0.0) | `15.0` | watchdog 검사 주기(초). |
| `logging.level` | string: debug, info, warning, error | `"info"` | 최소 로그 수준. |
| `logging.log_path` | string | `"logs/ouroboros.log"` | 설정 모델에 선언된 경로. 고정 `src/ouroboros`에서 이 필드를 읽는 직접 참조는 확인되지 않으며 독립 CLI의 `configure_cli_logging`은 저장된 `logging.level`만 별도 로깅 설정에 반영한다. 별도 로깅 설정의 기본 파일은 `~/.ouroboros/logs/ouroboros.log`다. 합성 임시 HOME의 한 직접 호출에서 설정한 별도 경로 대신 기본 파일에 메시지가 기록됐다. 해당 시험에서는 호출 전 모듈 import 후 로거가 이미 설정돼 있었다. 이 값을 바꿨다고 모든 로그가 해당 경로로 이동하거나 기존 경로에 기록되지 않는다고 가정하지 않는다. 동적 참조·다른 호스트 및 운영 환경의 실제 파일 출력은 미검증. [CLI 로깅 설정](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/logging_setup.py), [파일 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/observability/logging.py). |
| `logging.include_reasoning` | boolean | `true` | 선언된 reasoning 로그 선호값. 고정 `src/ouroboros`에서 이 이름의 직접 참조는 설정 모델 선언만 확인되어, `false`가 모든 reasoning·입력·민감정보 로깅을 막는다고 가정하지 않는다. 동적 참조·각 호스트의 실제 로그는 미검증이다. |
| `orchestrator.runtime_backend` | string: claude, claude_mcp, codex, opencode, hermes, gemini, kiro, copilot, goose, pi, omp, gjc, antigravity, grok, zcode, megacode, host | `"claude"` | 작업 실행에 사용할 에이전트 런타임. LLM 전용 백엔드와 별도. |
| `orchestrator.runtime_profile` | RuntimeProfileConfig / null | `null` | 단계별 라우팅과 백엔드 고유 프로필 선택을 위한 선택적 객체. |
| `orchestrator.permission_mode` | string: default, acceptEdits, bypassPermissions | `"acceptEdits"` | 저장된 런타임 권한 선호. Seed 실행 예외는 위 참조. |
| `orchestrator.opencode_permission_mode` | string: default, acceptEdits, bypassPermissions | `"bypassPermissions"` | OpenCode 런타임의 저장된 권한 모드. Seed 실행 예외는 위 참조. |
| `orchestrator.reasoning_effort` | string / null | `null` | 런타임 reasoning effort 선택값. 지원 여부는 백엔드에 따라 다르다. |
| `orchestrator.opencode_mode` | string / null | `null` | OpenCode 실행 모드 선택값. |
| `orchestrator.cli_path` | string / null | `null` | Claude CLI 경로. null이면 런타임의 기본 경로를 사용. |
| `orchestrator.codex_cli_path` | string / null | `null` | Codex 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.copilot_cli_path` | string / null | `null` | Copilot 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.copilot_transport` | string: cli, acp | `"cli"` | Copilot 작업 전송 방식. ACP는 실험적이며 LLM 전용 호출은 CLI를 유지. |
| `orchestrator.copilot_acp_fallback` | boolean | `true` | ACP가 prompt 제출 전 읽기 전용·도구 없는 경우 CLI로 전환하도록 허용. 인증 실패나 제출 후 재생에는 적용하지 않는다. |
| `orchestrator.opencode_cli_path` | string / null | `null` | OpenCode 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.opencode_stdout_idle_timeout_seconds` | number / null | `null` | OpenCode stdout 활동 유휴 시간 제한(초). null은 런타임 기본값. |
| `orchestrator.hermes_cli_path` | string / null | `null` | Hermes 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.gemini_cli_path` | string / null | `null` | Gemini 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.kiro_cli_path` | string / null | `null` | Kiro 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.goose_cli_path` | string / null | `null` | Goose 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.pi_cli_path` | string / null | `null` | Pi 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.omp_cli_path` | string / null | `null` | OMP 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.gjc_cli_path` | string / null | `null` | GJC 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.antigravity_cli_path` | string / null | `null` | Antigravity (agy) 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.grok_cli_path` | string / null | `null` | Grok 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.ourocode_cli_path` | string / null | `null` | ourocode (LLM 전용) 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.zcode_cli_path` | string / null | `null` | Zcode 실행 파일 또는 스크립트 경로. null이면 macOS 앱 경로와 PATH를 탐색한다. |
| `orchestrator.megacode_cli_path` | string / null | `null` | megacode harness 실행 파일 경로 선택값. null이면 런타임에서 탐색한다. |
| `orchestrator.dsh_cli_path` | string / null | `null` | dsh ACP 서버 실행 파일 경로. null이면 PATH에서 탐색한다. |
| `orchestrator.dsh_config_path` | string / null | `null` | dsh 백엔드에 필요한 신뢰된 절대 설정 경로. 상대 경로는 거부. |
| `orchestrator.verify_bash_path` | string / null | `null` | 검증 명령 실행에 사용할 bash 경로 선택값. |
| `orchestrator.default_max_turns` | integer (minimum=1) | `10` | 에이전트 실행 작업당 기본 최대 턴 수. |
| `orchestrator.max_parallel_workers` | integer (minimum=1) | `3` | AC worker의 적응형 동시 실행 상한. |
| `orchestrator.usage_limit_pause_hours` | number (exclusiveMinimum=0.0) | `5.0` | 제공자 사용량 제한 시 기본 대기 시간(시간). |
| `orchestrator.use_worktrees` | boolean | `true` | 변경 작업을 별도 Git worktree에서 실행할지 여부. |
| `orchestrator.worktree_root` | string | `"~/.ouroboros/worktrees"` | 관리 작업 worktree의 상위 경로. |
| `orchestrator.worktree_cleanup` | string: keep, remove, prune-merged | `"prune-merged"` | 자동 세션 종료 시 정리 정책. prune-merged는 병합되고 깨끗한 worktree만 제거. |
| `orchestrator.worktree_lock_stale_after_minutes` | integer (minimum=1) | `60` | 작업 lock을 오래된 것으로 판정해 복구하는 시간(분). |
| `orchestrator.pm_snapshot_worktrees` | boolean | `true` | PM brownfield 탐색에서 원격 기본 브랜치 기준 별도 snapshot 사용. 시작 시 해당 snapshot fetch와 hard reset이 수행된다. |
| `orchestrator.pm_snapshot_root` | string | `"~/.ouroboros/pm-snapshots"` | PM snapshot worktree의 상위 경로. |
| `telemetry.enabled` | boolean | `true` | 사용 통계 전송 설정. 옵트아웃과 실패 정책은 위 참조. |
| `seed.verify_command_gate` | string: warn, block | `"warn"` | AC에 verify_command와 verify_exemption_reason이 모두 없을 때 warn은 경고 후 계속, block은 실행을 거부. |
| `boundary.check_package` | string / null | `null` | 새 실행 check package 모드. null 기본은 record이며 결과를 기록만 하고 판정을 바꾸지 않는다. |
| `boundary.constructor_timeout_seconds` | integer (minimum=30, maximum=3600) | `600` | 읽기 전용 검사 생성 모델 호출 한 번의 제한 시간(초). |
| `boundary.check_timeout_seconds` | integer (minimum=5, maximum=1800) | `120` | 각 검사 admission 및 후보 검증 제한 시간(초). |
| `boundary.max_construction_attempts` | integer (minimum=1, maximum=5) | `2` | worker 시작 전 검사 패키지 생성 시도 상한. |
| `boundary.base_regression` | string / null | `null` | 기존 회귀 검사 정책. null은 record; decide의 효과는 check package 모드에 종속. |
| `boundary.worker_test_gate` | string / null | `null` | worker가 추가한 테스트의 게이트 정책. null은 record. |

## 중첩 객체: 단계 런타임과 LLM 프로필

위 114개 행은 최상위 모델의 중첩 객체를 펼친 색인이며, 동적 이름을 가진 객체의 모든 하위 키를 각각 센 숫자는 아니다. 아래는 설정 파일의 **일부 예시**다. 설정 모양 검증과 실제 백엔드의 설치·인증·실행 지원은 다르다. 예시는 특정 모델을 호출하지 않는다.

```yaml
orchestrator:
  runtime_backend: claude
  runtime_profile:
    backend_profile: my-codex-profile
    default: codex
    stages:
      execute: codex
      evaluate: claude
llm_profiles:
  review:
    max_turns: 3
    temperature: 0.2
    providers:
      codex:
        reasoning_effort: high
llm_role_profiles:
  semantic_evaluation: review
```

- `orchestrator.runtime_profile.stages`에서 허용하는 단계 키는 `interview`, `execute`, `evaluate`, `reflect`뿐이다. 해당 단계의 명시 설정 → `runtime_profile.default` → `orchestrator.runtime_backend` 순으로 선택한다. `default`와 각 단계의 값은 런타임 백엔드 등록 이름과 일부 별칭에 대해 검증된다. `backend_profile`은 빈 문자열이 아닌 백엔드 고유 프로필 이름이며, 실제 전달·지원 여부는 어댑터에 달려 있다. 위 이름은 사용자가 사전에 만든 프로필이라는 가상 예시다. [단계 정의와 선택](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator_stage.py), [설정 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/models.py).
- `llm_profiles.<이름>`은 `model`, `temperature`(0–2), `max_tokens`(1 이상), `top_p`(0–1), `max_turns`(1 이상), `reasoning_effort`(`low`, `medium`, `high`) 및 `providers`를 선택적으로 담는다. `providers.<백엔드>`에서 같은 값과 백엔드 고유 `profile`을 지정할 수 있다. 프로바이더별 `reasoning_effort`의 `xhigh`는 `codex` 또는 `codex_cli`에만 허용된다. 각 어댑터가 모든 값을 실제 지원한다는 뜻은 아니다.
- `llm_role_profiles.<역할>`은 위 프로필 이름을 가리킨다. 원본은 요청 모델 지정, 역할 매핑, 활성 백엔드별 프로필, 기존 역할 모델 필드, 백엔드 기본값의 순서를 설명한다. 이 프로필과 작업 런타임의 `runtime_profile`은 서로 다른 설정이다. **위 예제의 `temperature: 0.2`는 `semantic_evaluation` 역할 매핑만으로 호출에 적용되지 않는다.** 역할 기반 해석은 호출자가 지정한 `temperature`·`max_tokens`·`top_p`를 보존한다. Python 호출의 `CompletionConfig.profile`로 프로필을 명시한 경우에만 프로필의 해당 값이 해석에 포함되며, 이후 백엔드가 그 값을 지원·전달하는지는 별도다. 반면 `max_turns`·`reasoning_effort`는 역할 기반 해석에서도 사용될 수 있다. [프로필 해석 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/providers/profiles.py), [프로필과 역할의 원본 예제](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md).

`economics.tiers`도 동적 이름별 객체다. 각 tier는 양의 정수 `cost_factor`가 필요하고, 선택적으로 오름차순 두 정수의 `intelligence_range`, `{provider, model}` 객체 목록 `models`, 문자열 목록 `use_cases`를 가진다. 예시는 구조만 보여 주며 아래 이름이 설치된 모델이나 가격임을 의미하지 않는다.

```yaml
economics:
  tiers:
    frugal:
      cost_factor: 1
      intelligence_range: [9, 11]
      models:
        - provider: example-provider
          model: example-model
      use_cases: [routine_coding]
```

**복사해 실행하는 설정이 아니다.** 위 `example-provider`와 `example-model`은 실제 라우팅 가능한 값이 아니다. 고정 소스의 orchestrator는 `economics.tiers`가 완전히 빈 경우에만 기본 tier 목록으로 대체한다. 예제처럼 tier 하나라도 지정한 경우에는 빠진 `standard`·`frontier`를 자동으로 채우지 않고 지정한 목록을 그대로 사용하므로, 실제 설정에서는 사용할 각 tier와 런타임의 공급자·모델을 확인해야 한다. [라우터 초기화](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py), [tier별 모델 선택](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/model_routing.py).

이 예시들은 고정 소스와 설정 모델이 같은 로컬 체크아웃의 `OuroborosConfig.model_validate`로 구문·스키마만 확인했다. 역할 연결의 실제 모델 선택, 프로바이더 호출과 비용은 검증하지 않았다. 전체 이름과 예외는 [원본 설정 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md)를 확인한다.
