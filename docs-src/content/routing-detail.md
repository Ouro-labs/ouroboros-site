# 실행 정책, 모델 라우팅과 비용 근거

기준: 2026-11-04, Ouroboros 고정 source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지는 [실행 선호 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py), [MCP 입력 처리](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py), [설정 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md)와 [run 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/run/SKILL.md)을 대조한다. 연결된 서버·호스트의 버전과 실행 영수증을 확인한다. 이 페이지의 정책 비교는 모델 비용·품질·권한을 실제로 측정한 결과가 아니다.

**판본 경계:** 아래 정책과 기본값은 722판 계약이다. 직접 인용한 preference·handler·skill 경로를 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 release `v0.59.9`와 정적으로 대조했을 때 해당 파일 차이는 발견하지 못했다. 다만 `v0.59.9`와 main의 추가 관련 파일인 [runner.py](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py)와 [config-reference.md](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/config-reference.md)는 서로 다르며, 이 가이드가 그 모든 차이를 설명하거나 현재 설치 환경에서 정책을 확인했다는 뜻은 아니다. 실제 모델 선택·청구·호스트 대화·strict baseline은 미검증이다. 설치된 버전의 설정과 실행 영수증을 확인하며, 실행 중 재개·복구에는 [진행 상태](/docs/progress-detail/)와 [복구](/docs/recovery-detail/)의 ID별 경계를 적용한다.

## 시작할 때 선택하는 것

`execution.default_policy`는 **새 실행**의 기본 선택이며 실제 MCP 입력 이름은 `efficiency_mode`와 `frugality_assurance`다. 품질 목표, 실행 예산, 도구 권한은 서로 다르다. 하나의 이름만으로 품질이나 지출 상한이 보장되지 않는다.

| 설정의 선택 | 새 실행의 기본 해석 | 의미와 한계 |
| --- | --- | --- |
| `quality_first` | `quality_first` / `off` | 기본값이다. 분해된 자식의 시작 tier를 비용을 이유로 부모보다 낮추지 않는다. 모든 호출이 가장 비싼 모델이거나 결과가 올바르다는 뜻은 아니다. |
| `efficient` | `adaptive` / `observe` | 신뢰 승인을 받은 분해 자식은 더 낮은 시작 tier를 사용할 수 있고 복구 시 높일 수 있다. 모든 작업이 낮은 tier에서 시작하거나 반드시 절약된다는 뜻은 아니다. |
| `ask` | 호스트가 선택을 묻는 경로 | `ooo run`·`ooo auto` 스킬은 명시적 선택에 따라 위 조합을 보낸다. 직접 MCP 호출은 호스트의 질문을 자동으로 재현하지 않는다. `ask` 설정에서 선호 인자를 모두 생략하면 새 실행은 `adaptive` / `observe`로 해석된다. |

새 실행에서 호출자가 명시한 값이 생략값을 채우는 설정보다 우선한다. `adaptive`에 생략된 assurance는 `observe`, `quality_first`에는 `off`로 해석된다. `strict`는 **별도의 명시적 선택**이며 `efficient`에서 자동으로 켜지지 않는다. 설정을 영속 변경하는 `ouroboros config set execution.default_policy efficient`는 사용자 설정 파일을 쓴다. 이 판본의 설정 변경은 자동 백업을 보장하지 않으므로 먼저 [운영 안내](/docs/operations-detail/)를 확인한다.

직접 `ouroboros_start_execute_seed`를 호출할 때 사용할 수 있는 예시는 다음과 같다. 실제 Seed 경로와 권한을 확인해 사용하는 **MCP 인자 형식**이며 셸 명령이 아니다. 선택을 바꾸지 않으려면 두 선호 인자를 생략하고 시작 영수증의 실제 해석값을 확인한다.

```json
{
  "seed_path": "<검토한 실제 Seed 경로>",
  "efficiency_mode": "adaptive",
  "frugality_assurance": "observe"
}
```

두 입력은 독립적으로 명시할 수 있으므로 시작 영수증의 실제 조합과 실행 ID·작업 위치를 확인한다. 스키마·경로 조건과 host 플러그인 위임의 차이는 [MCP 입력 색인](/docs/mcp-reference-detail/#ouroboros_start_execute_seed), [fan-out](/docs/fanout-detail/)을 본다. `auto`의 작성·실행 인계와 모델 선택은 동일한 단일 호출이 아니다.

## Assurance와 재개

- `off`는 frugality verdict/attention을 끈다. 이미 필요한 내부 telemetry가 전혀 생기지 않는다고 보장하지 않는다.
- `observe`는 라우팅·토큰·grounding 증거를 가볍게 관찰하는 경로다. 증거가 불완전하면 절약이나 실패를 추정하지 말고 해당 결과와 누락 이유를 확인한다.
- `strict`는 추가 비용이 들 수 있는 기준선 증명에 대한 별도 명시적 허가다. 이 판본의 shadow replay는 별도 환경 flag와 명시적 strict 외에도 분해와 격리 attestation이 필요하다. 고정 구현의 bundled runtime/live 분해는 이 계약을 갖추지 않아 baseline dispatch가 격리된다. **strict를 설정했다는 사실은 실제 비교 실행이나 절약 증명이 아니다.** [runner](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runner.py), [요구사항](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/active-conductor/requirements.md).

실행 선호와 해결된 라우팅 계약은 실행과 함께 보존된다. MCP 실행 재개에 `efficiency_mode` 또는 `frugality_assurance`의 빈 문자열이 아닌 값을 다시 명시하면 **같은 값이어도 거부**된다. Auto 재개도 두 값을 생략하고 보존된 계약을 사용한다. 의도적으로 정책을 바꾸려면 새 successor 실행의 승인·연결과 기존 작업공간·외부 효과를 확인한다. [재개](/docs/recovery-detail/), [MCP 실행 재개 입력 검사](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/execution_handlers.py#L226-L245), [Auto 재개 입력 검사](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/auto_handler.py#L397-L427). 기존 모델 ID가 더 이상 지원되지 않으면 같은 런타임의 재개가 조용히 최신 모델로 바뀐다고 가정하지 않는다.

## Tier와 실제 모델

MCP `model_tier`의 `small`, `medium`, `large`는 내부 `frugal`, `standard`, `frontier`에 각각 대응한다. 생략하면 자동 선택을 보존한다. [MCP 색인](/docs/mcp-reference-detail/)과 실제 서버의 허용값을 확인한다. 독립 CLI의 `--model`과 `models.default`는 별도의 표면이므로 같은 인자명·값이라고 가정하지 않는다. 명시 모델이나 tier 선택, pin 설정, 백엔드의 모델 지원이 최종 경로에 영향을 미친다.

고정 소스의 기본 `economics.default_tier: frugal`은 모든 작업이 frugal로 시작한다는 뜻이 아니다. 기본 base는 한 단계 위인 standard이며 최상위·신뢰되지 않은 자식은 base에서 시작한다. `adaptive`에서 명시적 신뢰를 받은 분해 자식은 한 단계 낮출 수 있다. 재시도는 경로에 따라 승격될 수 있고 성공 연속 횟수에 따른 자동 하향은 없다. `cost_factor`는 상대적 모델 라우팅 값이지 실제 달러 요금이 아니다. [설정 색인](/docs/config-reference-detail/), [재시도와 재배정](/docs/ac-recovery-detail/).

지원 런타임의 기본·별칭·선택 가능한 모델은 다르다. 특히 일반적인 자동 Codex 경로는 Codex 자체 선택을 유지한다. 이 판본은 `OUROBOROS_MODEL_TIER_ROUTING=1`로 해당 적응 사다리에 opt-in할 수 있으며 명시적 pin이 우선한다. 원본은 `0`/`off`/`false`로 라우팅 비활성화를 설명한다. resolved `default`·`auto`·`current`는 모델 강제의 증거가 아니다. 실제 실행에 어떤 모델이 적용됐는지는 런타임 보고와 공급자 기록을 확인한다. [원본 라우팅 설정](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/config-reference.md).

## 비용과 비교를 읽는 법

시작 tier·상대 cost factor·관측된 토큰만으로 실제 청구액이나 하드 한도를 계산할 수 없다. 모델별 입력·출력 토큰, 재시도·평가·후속 반복·추가 모델, 공급자의 단가·계약·캐시, 호스트·외부 도구 비용과 누락된 usage를 분리해야 한다. `observe`나 `strict` verdict, 예상 비용 및 시작 영수증은 공급자 청구서가 아니다. 사용량이 누락되면 미확인으로 둔다.

`benchmark_control`은 evolve의 별도 전체 그래프 비교 요청으로 기본이 꺼져 있다. 고정 핸들러는 내구 `EventStore`, `execute=true`, 기존 완료 세대가 있는 Gen 2+, 명시적 Git 프로젝트와 깨끗한 baseline을 요구하며 plugin 위임 경로를 허용하지 않는다. 이것은 단순 조회가 아니라 실행·비용·작업공간 효과가 생길 수 있다. 서로 다른 입력·모델·환경으로 얻은 수치를 절약 증거로 합산하지 않는다. [핸들러 조건](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py), [평가와 진화](/docs/evaluation-evolution-detail/).

**검증 범위:** 고정 커밋과 관련 source·테스트 경로 차이가 없는 로컬 checkout에서 빈 임시 HOME/TMPDIR과 telemetry off로 실행 선호·MCP 기본값·정책 안내의 기존 테스트 18개가 통과했다. 가짜 입력 및 단위 테스트이며 실제 모델 선택·토큰 청구·호스트 대화·strict baseline·OS 네트워크 격리는 시험하지 않았다.

독립 재검증에서는 같은 고정 커밋과 관련 소스·테스트 경로에 차이가 없는 checkout에서 빈 임시 HOME/TMPDIR과 telemetry 비활성 조건으로 `test_execution_preferences.py`, `test_execution_preference_defaults.py`, `test_runtime_native_routing_contract.py`를 실행해 **35개가 통과**했다. 기본 정책·명시적 선호·재개 계약 보존과 불일치 분기를 다루는 대역 테스트다. 실제 모델·호스트 대화·공급자 청구 및 OS 네트워크 격리는 이 결과로 검증되지 않는다.
