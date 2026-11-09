# Seed와 완료 판정 이해하기

!!! warning "판본과 검증 범위"
    이 문서의 상세 설명과 합성 관찰은 별도 표시가 없으면 2026-11-04 조사한 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 호스트 플러그인·MCP 서버는 별도 판본입니다. 합성·대역 사례는 표시된 조건에 한정되며 실제 모델, 운영 데이터 또는 전체 호스트를 검증하지 않습니다. 현재 설치의 도움말과 [제품 문서](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/docs)를 대조하고 구판과 동일하게 동작한다고 가정하지 마세요.


## Seed는 무엇인가

Seed는 목표, 제약, 검증 가능한 성공 기준을 담는 YAML 작업 명세입니다. 요구가 불명확하면 `ooo interview`로 먼저 구체화한 뒤 `ooo seed`를 요청할 수 있습니다. 이미 목표·제약·성공 기준이 합의됐다면 인터뷰를 반복하지 않고 Seed 생성을 요청할 수 있습니다. 응답에 YAML이 보이는지와 실제 파일이 저장됐는지는 별도로 확인하세요. [첫 실행](/docs/first-run-detail/)에서 호스트와 독립 CLI 경로를 구분하고, [고정 main Seed 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md), [release 0.59.9 Seed 스킬](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/skills/seed/SKILL.md), [722 Seed 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/seed/SKILL.md)의 구체 동작을 비교할 수 있습니다. 현재 설치의 응답과 파일 경로를 확인하세요.

## 모호도 점수와 문턱값은 어떻게 다른가

모호도 점수는 요구가 얼마나 불명확한지 나타냅니다. 고정 upstream README의 설명은 목표·제약·성공 기준의 명확성을 평가하고 그 가중 합을 1에서 빼는 방식입니다. 세부 명확성 점수는 모델의 판단이므로 같은 기준도 채점 결과가 달라질 수 있습니다.

`0.2`는 그 점수를 Seed 생성에 사용할 때 적용하는 기본 문턱값입니다. 실행할 코딩 모델을 바꿨다는 이유로 문턱값도 바뀐다고 해석하지 않습니다. `0.34`를 실패 확률 34%로 읽을 근거도 없습니다. 점수와 통과 기준을 구분한 뒤 부족한 목표·제약·성공 기준을 보완합니다. 강제 생성 등 예외는 사용 중인 버전의 스킬 안내와 실제 응답을 확인합니다.

근거: [고정 README의 Ambiguity Score 설명](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/README.md), [Seed 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/seed/SKILL.md).

## 명령 종료와 제품 완성은 왜 다른가

백그라운드 시작 응답은 작업을 접수했다는 증거입니다. 인터뷰 종료는 요구 정리가 끝났다는 뜻이며, 실행 완료는 파일 생성 단계를 마쳤다는 뜻일 수 있습니다. 제품 완성은 Seed의 요구와 실제 결과가 맞고 필요한 검증을 통과했는지로 판단합니다. 자동 평가와 독립 검수의 결과도 각각 확인합니다.

`job_`는 백그라운드 작업, `orch_`는 실행 세션, `exec_`는 실행을 식별합니다. 받은 값에 맞춰 [상태 조회](/docs/progress-detail/)를 하고, 실패가 있으면 [복구 안내](/docs/recovery-detail/)를 따릅니다.
