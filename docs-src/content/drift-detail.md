# 목표 이탈 측정과 결과 해석

기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 아래는 [MCP 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evaluation_handlers.py)와 [계산 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/observability/drift.py)을 대조한 설명이다. 설치한 서버의 스키마가 다를 수 있다.

**판본·검증 범위:** 설명은 722판이다. 인용한 `evaluation_handlers.py`, `drift.py`, `status` skill의 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 release `v0.59.9` 대응 파일을 정적으로 비교했을 때 해당 경로에서 차이가 보이지 않았다. 이는 선택한 파일의 비교이지 설치된 서버·모델 설정·의존성 전체의 동등성 검증은 아니다. 실제 모델 제공자 호출, MCP 종단 간 사용, 사용자 실행의 점수는 시험하지 않았다. 현재 서버 schema를 확인하고 수치만으로 성공을 판정하지 않는다.

`ooo status`는 우선 세션 상태를 조회한다. 이탈 측정을 요청하면 호스트가 별도 `ouroboros_measure_drift` 도구를 호출한다. 이 점수는 현재 결과 **설명**과 원래 목표의 정렬, 제공된 위반 목록과 개념 목록을 비교하는 관찰값이다. 실제 코드 실행·테스트·외부 효과나 수용 기준 충족을 증명하는 [정식 평가](/docs/evaluation-evolution-detail/)와 다르다. 낮은 점수를 완료 승인이나 보안 검증으로 사용하지 않는다. [상태 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/status/SKILL.md), [진행 상태](/docs/progress-detail/).

## 입력과 비용

MCP 도구 `ouroboros_measure_drift`에는 실제 실행의 `session_id`, 현재 결과를 나타내는 비어 있지 않은 `current_output` 문자열, 원본 Seed **YAML 본문** `seed_content`가 필요하다. 파일 경로 문자열을 주면 이 도구가 파일을 읽는다고 가정하지 않는다. `constraint_violations`와 `current_concepts`는 선택적 배열이다. 누락하거나 빈 배열로 주면 각각 빈 목록으로 처리한다. 실제 확인한 위반과 결과의 개념을 제공하고, 확인하지 못한 항목을 없다고 단정하지 않는다. [MCP 입력 색인](/docs/mcp-reference-detail/#ouroboros_measure_drift), [Seed 형식](/docs/seed-format-detail/).

목표 이탈 계산은 공백이 아닌 출력에 대해 설정된 semantic evaluator를 호출하려 한다. 빈 문자열은 MCP 핸들러가 거부하지만 공백만 있는 문자열은 통과한 뒤 모델 호출 없이 목표 이탈 1로 계산한다. Seed 목표와 현재 출력이 모델 제공자에게 전달될 수 있고 비용이 생길 수 있으므로 민감정보·권한·비용 범위를 먼저 확인한다. 실패·시간 초과·유효하지 않은 응답이면 어휘 기반 점수로 폴백하고 경고를 기록한다. 이 판본의 응답 metadata에는 어떤 방식으로 계산했는지를 나타내는 별도 필드가 없으므로 숫자만 보고 모델 평가가 성공했다고 단정하지 않는다. 로그에는 오류 상세가 포함될 수 있다. 실제 공급자 호출은 이번 조사에서 시험하지 않았다.

## 점수의 의미

| 요소 | 고정 구현의 계산 | 해석 시 주의 |
| --- | --- | --- |
| 목표 | semantic alignment가 유효하면 `1 - alignment`; 실패 시 목표와 출력 단어 집합의 Jaccard 거리 | 설명의 유사도이지 구현이 실제로 존재하거나 안전하다는 판정이 아니다. 폴백과 의미 평가의 점수는 다를 수 있다. |
| 제약 | 제공된 위반 수 × 0.1, 최대 1 | 빈 목록은 0이다. 도구가 제약을 자동 검사해 위반이 없음을 증명했다는 뜻이 아니다. |
| 온톨로지 | 소문자 개념 이름과 Seed ontology 필드 이름의 Jaccard 거리 | 현재 개념이 빈 목록이면 Seed 필드 유무와 관계없이 1이다. 현재 개념이 있고 Seed 필드가 비어 있으면 0이다. |

어휘 폴백의 토큰화는 형태소 분석이 아니다. 목표와 결과를 공백으로 나눈 뒤 각 조각에서 영숫자가 아닌 문자를 제거하므로 한국어 어미·띄어쓰기와 구두점에 민감하다. 이 구현은 문장부호만 있는 조각을 제거 후 빈 문자열 토큰으로 남길 수도 있다. 예를 들어 합성 `alpha !`와 `beta !`는 빈 토큰을 공유해 어휘 거리가 약 0.667로 계산된다. 이는 의미적 공통성의 증거가 아니다. 격리 임시 HOME에서 해당 토큰 집합과 산식을 확인했으며 실제 모델 호출이나 사용자 작업의 점수는 측정하지 않았다. [토큰화 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/observability/drift.py).

결합 점수는 `0.5 × 목표 + 0.3 × 제약 + 0.2 × 온톨로지`다. 이 측정기의 `is_acceptable`은 **0.3 이하**이며 0.3을 초과하면 `EXCEEDED`와 검토 제안을 반환한다. 이는 측정 코드에 정의된 경계다. 별도 설정 `drift.warning_threshold`와 `drift.critical_threshold`는 같은 값처럼 취급하지 않는다. 예를 들어 목표 0.2, 알려진 위반 하나(0.1), 온톨로지 0.5라면 결합은 `0.5×0.2 + 0.3×0.1 + 0.2×0.5 = 0.23`이다. 이는 **계산 예시**이며 실제 작업의 측정 결과가 아니다.

반환 `meta`에서 session/seed ID, 세 요소, `combined_drift`, `threshold`, `is_acceptable`, `suggestions`를 확인한다. 정보가 빠졌거나 근거가 약하면 원본 결과·제약·개념을 다시 살피고 사람이 판단한다. 목표와 결과 설명에 데이터가 포함되므로 출력·로그 공유 범위를 확인한다. 이 MCP 핸들러는 측정 결과를 반환하며 그 자체가 작업 재실행·합의·수정이나 실제 행동의 되돌리기를 보장하지 않는다.

**확인 범위:** 고정 커밋과 대상 소스·테스트 파일 차이가 없는 별도 checkout에서 임시 HOME·TMPDIR 및 telemetry 비활성 조건으로 `tests/unit/observability/test_drift.py` **39개가 통과**했다. 해당 테스트는 대역 semantic adapter·실패 폴백과 점수 계산을 다룬다. 이 수치는 당시 로컬 시험의 기록이며 공개 재현 자료는 없다. 실제 제공자·비용·MCP 서버 종단 간 호출과 OS 네트워크 격리는 검증하지 않았다.
