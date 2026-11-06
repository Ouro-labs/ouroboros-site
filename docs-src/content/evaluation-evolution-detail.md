# 평가·진화: 결과를 판정하고 다음 세대로 잇기

기준: 2026-11-04, [Q00/ouroboros `722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지는 고정 소스·테스트를 설명하며 설치된 다른 판본의 동작을 보장하지 않는다. 호스트 스킬과 독립 CLI는 별도 표면이다. 실제 모델 호출·프로젝트 명령·자동 반복은 비용과 파일 변경을 일으킬 수 있다.

**판본 경계:** 이 상세본은 기존 722판의 주요 내용·주의·예시를 보존한다. 정적 비교한 evaluation 파일에서는 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)에서 의미 평가 응답 parser가 boolean·비유한 점수를 거부하도록 달라졌다([main parser](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/semantic.py)). `v0.59.9`와 main의 unittest 자동 탐색도 `load_tests` hook 처리 및 Python 인코딩 선언 처리에서 다르다([main 탐색기](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/evaluation/stdlib_unittest_discovery.py), [release 탐색기](https://github.com/Q00/ouroboros/blob/v0.59.9/src/ouroboros/evaluation/stdlib_unittest_discovery.py)). 이는 확인한 파일의 차이다. 이 문서 전체의 main·release 기능 동등성, 실제 평가 파이프라인, 모델·호스트 동작은 검증하지 않았다. 설치 버전의 실제 검사 명령·출력과 결과를 우선하며, 상세 상태·재개 절차는 [진행 상태](/docs/progress-detail/), [복구](/docs/recovery-detail/)에 남아 있다.

## 결과를 받았다면 먼저 확인하세요 {#evaluation-next-steps}

평가가 끝났다는 표시만으로 원래 요청이 충족됐다고 판단하지 마세요. 실제 평가 결과에서 원래 Seed의 수용 기준과 실행된 검사, 각 단계의 판정을 확인합니다.

| 결과 | 다음 행동 |
| --- | --- |
| `approved` | 원래 요청과 Seed를 실제 산출물·검사 결과에 대조합니다. 승인만으로 요청 범위가 올바르게 구현됐다고 가정하지 않습니다. |
| `rejected` | 실패하거나 승인을 보류한 단계와 근거를 확인합니다. 기계 검사뿐 아니라 실행된 모델 검토가 보류했을 수도 있습니다. 원인을 수정한 뒤 필요한 실행이나 재평가를 선택합니다. |
| `unverified` | 실행된 기계 검사 증거가 있는지 확인합니다. 없다면 프로젝트에 맞고 신뢰할 수 있는 검사 명령을 준비한 뒤 다시 평가합니다. 긍정적인 모델 의견만으로 승인할 수는 없습니다. |

평가가 시작되지 않았거나 실패한 경우, 실제 세션 ID·원래 Seed·산출물·작업 경로를 확인하세요. 이미 평가 job이나 후속 Ralph job이 실행 중이면 중복 시작하지 않습니다. 호스트에서 재평가할 때는 `ooo evaluate`에 해당 세션을 지정하고, 자동 후속 작업 없이 평가만 원하면 `auto_evolve: false`를 요청할 수 있습니다. 이는 이미 시작된 작업을 취소하지 않습니다. 평가와 후속 작업은 명령 실행·모델 호출·추가 비용을 수반할 수 있습니다. 자세한 입력과 예외는 아래 [평가의 증거와 세 단계](#evaluation-evidence)를 확인하세요.

## 먼저 구분할 세 가지

| 질문 | 근거가 되는 기록 | 주의 |
| --- | --- | --- |
| 워커가 자기 작업을 마쳤나? | 실행 세션과 워커 결과 | `execution.ac.completed`의 역사적인 `passed` 표기는 워커 단위 완료이며 정식 수용 판정이 아니다. |
| 원래 수용 기준을 승인할 수 있나? | 평가의 `acceptance_state`, 각 단계와 실제 검사 결과 | 모델의 확신이나 워커 성공이 실행된 검증 증거를 대신하지 않는다. |
| 반복이 끝났나? | lineage·generation·Ralph job의 action과 종료 이유 | `ontology_stable`, 횟수 상한, 취소는 목표 달성의 동의어가 아니다. |

### 같은 “미검증”이어도 판정 경로를 확인하기

아래 **정식 평가 파이프라인**의 `acceptance_state=unverified`와 실행 중 **검사 패키지·기존 verifier의 AC 조정**은 서로 다른 결과 표면이다. 전자는 실행된 기계 검사 증거가 없으면 정식 평가에서 승인하지 않는다. 후자에서는 시도된 AC에 대해 패키지가 `unverified` 또는 `uncovered`이고 기존 verifier에도 증거가 없는 등 [조정 조건](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/boundary/acceptance.py)을 만족하면, 그 AC가 미검증으로 남으면서 실행 경로에서는 받아들여질 수 있다. `record` 모드에서 기록한 가상 거부도 그 자체로 실행 거부가 아니다. 미시도 기준이나 결정적 실패까지 받아들여진다는 뜻은 아니다. [검사 패키지의 모드·조정](/docs/check-package-detail/)을 함께 읽는다.

따라서 실행의 성공 상태만 보고 정식 평가의 `approved` 또는 각 기준의 검증을 추론하지 않는다. 실제 경로와 기준별 판정, `verification_coverage`, 검사 실행 증거를 확인하고 별도 정식 평가가 필요하다면 해당 결과도 확인한다. 이 설명은 고정 소스에 대한 정적 대조이며 실제 모델 실행은 시험하지 않았다.

[실행·평가 계약](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/execution-vs-evaluation.md), [평가 모델](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/models.py), [진화 루프](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/loop.py)를 기준으로 한다.

<span id="evaluation-evidence"></span>

## 평가의 증거와 세 단계

1. **기계 검사**는 lint·build·test·static·coverage의 설정된 명령을 실행한다. 실행된 검사 하나라도 실패하면 즉시 `rejected`이며 이후 모델 단계를 건너뛴다. `passed`로 표시된 생략 검사는 실행 증거가 아니다.
2. **의미 평가**는 수용 기준과 목표 적합성, 드리프트, 불확실성 등을 검토한다. 기계 검사가 전혀 없어도 피드백을 줄 수 있지만 승인 권한은 없다. 이 판본에서는 단계가 실행된 경우 `ac_compliance=false`, 점수 `<0.8`, 또는 reward-hacking 위험 `>=0.7`이 승인을 보류할 수 있다. `SemanticConfig.satisfaction_threshold` 값을 바꿔도 최종 게이트의 `0.8`이 바뀐다고 가정하지 않는다.
3. **합의**는 활성화되고 트리거된 경우에만 실행한다. 거부는 승인을 보류하지만 승인 투표가 실행된 기계 검사나 앞선 의미 평가의 보류를 대체하지 않는다. 단순 합의의 기본 비율은 `0.66`이며 성공적으로 수집된 투표 중 비율을 계산한다. 다수 호출이나 모델 이름만으로 서로 다른 모델·제공자라는 독립성이 입증되지 않는다. 어댑터, 실제 라우팅과 보고된 independence를 확인한다.

최종 `approved`에는 **실행된 검사 하나 이상과 전체 검사의 통과**가 필요하고, 실행된 모델 단계에 보류 이유가 없어야 한다. 실행한 검사 실패는 `rejected`, 검사 실행 증거가 없으면 `unverified`다. 여러 기준의 집계는 전부 승인일 때만 `approved`, 하나라도 거부면 `rejected`, 나머지는 `unverified`다. `unverified`는 모델의 긍정 피드백이 있어도 승인되지 않는다. 실행 단위 평가에서 공유된 빌드·테스트 한 번은 각 기준에 특화된 테스트를 각각 실행했다는 증거가 아니다. [게이트 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/models.py), [파이프라인](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/pipeline.py).

### 합의가 켜지는 조건

Stage 3이 켜져 있고 이전 단계에서 오류나 기계 실패로 종료되지 않았다면 트리거를 확인한다. 단 Stage 2에서 `ac_compliance=false`이면 수동 `trigger_consensus=true`가 아닌 한 Seed 변경 등 다른 트리거를 검사하기 전에 반환한다. 그 경계를 통과하면 수동 요청, Seed 변경, 온톨로지 변경, 목표 재해석, 드리프트, 불확실성, lateral thinking 채택 순서로 트리거를 확인한다. 기본 드리프트·불확실성 기준은 각각 `0.3`이며 비교는 **초과(`>`)**다. 첫 일치 조건만 보고된다. 수동 `trigger_consensus=true`는 의미 평가의 비준수에도 2차 의견을 요청하지만, 합의가 앞선 보류를 해제하지는 않는다. Stage 3 비활성화나 이전 단계 오류까지 무시한다는 뜻은 아니다. [트리거 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/trigger.py), [상세 가이드](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/evaluation-pipeline.md).

### coverage 출력 형식과 모호성

고정 파서는 coverage 명령의 **stdout**에서 `TOTAL 100 10 90%`처럼 두 정수 열과 정수 백분율이 있는 행 또는 `Coverage: 90.5%` 행을 인식한다. `TOTAL` 행의 소수 백분율·추가 branch 열은 이 판본에서 지원하지 않는다. 후보 측정 행이 잘못됐거나 서로 다른 수치가 둘 이상이면 하나를 임의로 고르지 않고 `None`을 반환한다. 같은 수치를 다른 소수 표기로 반복하는 경우는 하나로 취급한다. `Required Coverage: 70%` 같은 요구 문구는 측정값이 아니며 100% 초과도 거부한다. 지원되지 않는 `TOTAL`이 있다면 유효한 `Coverage:` 행을 함께 출력해도 모호하므로 수치를 반환하지 않는다. 형식과 실제 출력 전체를 확인한 후 설정된 명령과 평가 결과의 `coverage_score`를 함께 확인한다. [고정 파서](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/mechanical.py).

격리된 임시 Python 프로젝트에서 실제 coverage.py 7.13.5와 고정 `MechanicalVerifier.verify`를 실행한 사례에서는 기본 정수 `TOTAL`의 88%가 읽혔다. 같은 프로젝트의 `--precision=1` 보고서(87.5%)와 `--branch` 보고서(83%)는 명령 종료 0이어도 수치를 읽지 못해 기본 임계값에서 `passed=false`, `executed=false`, `coverage_score=None`이었다. 여기서 `executed=false`는 명령 미실행의 증거가 아니다. 실제 명령 종료 코드와 stdout을 별도로 확인한다. 이는 해당 버전·형식의 격리 사례이며 공개 재현 자료가 아니고, 모든 coverage 도구나 전체 평가를 검증한 결과도 아니다.

고정 소스의 파서에 아홉 합성 stdout 문자열을 직접 입력해 위 사례를 확인했다. 실제 coverage 도구 실행, stderr 출력이나 모든 포맷은 시험하지 않았다. 파서가 수치를 읽는 것만으로 테스트가 충분하거나 최종 평가가 승인됐다는 뜻은 아니다. 이는 격리된 합성 입력에 대한 관찰이며 독자가 재현할 공개 probe 파일은 제공하지 않는다.

### coverage 기준 `0.0`의 판정 경계

고정 소스에서 `coverage_threshold=0.0`이고 설정된 coverage 명령이 종료 0이지만 출력에서 수치를 읽을 수 없으면, **coverage 검사 자체는 `passed=true`, `executed=true`**로 기록될 수 있으며 `coverage_score`는 `None`이다. 동일 출력에 기본 `0.7`이면 해당 검사는 `passed=false`, `executed=false`로 남는다. 따라서 `0.0`에서 검사 성공을 측정된 coverage나 목표 달성의 증거로 해석하지 않는다. 이 경로는 최종 평가의 다른 단계가 반드시 승인된다는 뜻도 아니다. [고정 검사 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/mechanical.py).

합성 시험은 실제 `MechanicalVerifier.verify`에 종료 0과 수치 없는 출력을 반환하는 함수 대역을 주어 `0.7`과 `0.0`을 비교했다. 실제 명령·모델·전체 평가 파이프라인은 시험하지 않았다. 이는 한 대역 시험의 관찰이며 공개 재현 자료는 없다.

## `unverified`·실패를 진단하기

정상 MCP 평가의 기계 검사 명령은 프로젝트 루트 `.ouroboros/mechanical.toml`에서 온다. 파일이 없을 때 `run`과 MCP 평가가 각자의 경로에서 자동 탐지를 시도하지만, 탐지는 백엔드·권한·파일 쓰기 등의 이유로 실패할 수 있다. 파일이 없거나 파싱·허용 검사를 통과한 명령이 없어 모든 검사가 생략되면 승인할 수 없다. [설정과 진단](/docs/operations-detail/)에서 실제 작업 디렉터리와 실행 명령을 먼저 확인한다. `ouroboros detect`는 모델 호출과 파일 쓰기를 유발할 수 있고 `--force`는 기존 파일을 덮어쓸 수 있다.

| 관찰 | 해석과 다음 확인 |
| --- | --- |
| Stage 1이 `passed`이나 `NO CHECKS EXECUTED` | 생략된 검사는 통과 증거가 아니다. TOML·명령 차단 로그·실제 실행 가능한 테스트를 확인한다. |
| coverage 명령 종료 0, 측정값 `None` | 활성 기준에서 지원되지 않거나 모호한 출력이면 측정하지 못한 상태다. `TOTAL ... XX%` 또는 `Coverage: XX%` 등 지원되는 측정 행을 제공하고 다시 확인한다. 기본 기준 `0.7`, `0.0`은 수치 기준을 끄는 설정이지 측정값을 만들어 주지 않는다. |
| 명령 없음·timeout·비영점 종료 | 어떤 명령이 어느 작업 디렉터리에서 실행됐는지, 종료 코드와 출력 꼬리·timeout을 확인한다. 기본 timeout은 명령당 300초다. |
| 의미 점수는 높지만 비준수 또는 합의가 거부 | 모델 단계가 승인을 보류했을 수 있다. `stage2_result`, `stage3_result`와 사유를 읽고 확인한 사실과 추정을 분리한다. |
| 결과에 승인 대신 오류 | 평가가 정상 판정까지 도달하지 못한 것일 수 있다. 오류를 `rejected`나 `approved`로 치환하지 말고 job 결과와 로그를 확인한다. |

`.ouroboros/mechanical.toml`은 일반 shell 스크립트가 아니다. 이 판본의 TOML 입력은 명령을 인자 단위로 분리하고 허용 executable·저장소·경로 등의 검사를 적용한다. 직접 Python에서 만든 `MechanicalConfig`는 별도 신뢰 경로이며 TOML과 같은 검증을 받는다고 가정하지 않는다. MCP 평가 요청에 임의 명령을 별도 인자로 넣는 인터페이스도 아니다. 실행할 명령을 미리 읽고 작업공간과 권한을 검토한다. [기계 검사 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/mechanical.py), [명령 구성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/command_parsing.py), [원본 평가 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/evaluation-pipeline.md).

### 검증 명령을 직접 준비하기

**판본별 자동 탐지 경계:** 고정 `722172ef`의 manifest 없는 `unittest` 자동 탐색은 정적으로 `load_tests`가 바인딩된 테스트 모듈을 검사 근거에서 제외하고, 그런 훅이 있는 하위 패키지는 내려가지 않는다. 다른 적합한 테스트를 찾을 수 있으므로 훅이 있다는 이유만으로 전체 탐지가 반드시 실패한다는 뜻은 아니다. 비교한 공개 `0.59.9` 설치본의 대응 탐색기에는 이 두 분기가 없다. 따라서 한 판본의 자동 탐지 결과를 다른 판본에 그대로 적용하지 말고, 실제 발견·실행된 테스트 수와 수용 기준을 확인한다. 고정 소스는 파이썬 인코딩 선언과 BOM을 고려해 원본 바이트를 파싱하지만 설치본은 UTF-8 텍스트로 읽는다. 합성 fixture 세 개의 탐지 함수 시험에서는 훅 없는 대조군은 양쪽 모두 명령을 제안했고, 테스트 모듈이나 하위 패키지에 `load_tests`가 있는 사례는 고정 소스만 제안하지 않았다. 반환된 명령은 실행하지 않았고, 다른 입력과 두 판본의 전체 동등성은 검증하지 않았다. [고정 탐색기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/stdlib_unittest_discovery.py), [판본 범위](/docs/version-guide/#version-scope).

자동 탐지 결과가 없거나 프로젝트에 맞지 않는다면 대상 프로젝트의 `.ouroboros/mechanical.toml`을 직접 검토·작성할 수 있다. 예를 들어 **표준 라이브러리 `unittest` 테스트가 `tests/`에 있는 신뢰된 프로젝트**에서의 최소 예시는 다음과 같다.

```toml
# 프로젝트 루트/.ouroboros/mechanical.toml
test = "python -m unittest discover -s tests"
timeout = 120
```

최상위에 `lint`, `build`, `test`, `static`, `coverage` 명령을 문자열로 둘 수 있고 `timeout`은 각 명령의 초 단위 제한이다. 필요한 검사만 추가하며 실제 프로젝트의 환경·의존성·테스트 위치를 먼저 확인한다. 검사는 지정된 프로젝트 디렉터리에서 실행되며 인자 단위로 분리되므로 `&&`, 파이프 같은 shell 구문으로 연결하지 않는다. TOML 구문 오류나 허용되지 않는 실행 파일·저장소 경계를 벗어나는 일부 인자는 무시될 수 있다. 허용 목록은 안전한 실행 환경을 보장하지 않으며, 허용된 테스트·빌드도 파일 변경이나 네트워크 접근을 할 수 있으므로 명령과 대상 저장소를 신뢰하고 권한을 검토해야 한다. `--help` 등 검증하지 않는 모드도 거부될 수 있다. 고정 구현에서 명령 제한시간이나 취소 시 `process.kill()`은 직접 실행한 프로세스에 적용되며, 별도의 프로세스 그룹 전체 종료를 이 경로에서 보장하지 않는다. 실행한 테스트·빌드가 자식 프로세스를 만들 수 있다면 timeout 후에도 자손이나 외부 효과가 남았는지 확인하고 중복 재실행을 피한다. 이는 소스 대조이며 실제 자손 종료나 OS 격리를 시험한 결과가 아니다. [명령 실행 및 timeout 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/mechanical.py). 검사 후 Stage 1의 실제 명령·종료 코드·`executed` 여부와 테스트 수를 확인한다. 프로젝트에 맞지 않는 예제를 그대로 복사해 성공을 주장하지 않는다. [설정 로더와 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evaluation/languages.py), [원본 형식 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/evaluation-pipeline.md#project-level-command-overrides).

격리된 임시 프로젝트에 위 TOML과 단일 합성 unittest를 만들고 고정 소스와 동일한 로더·`MechanicalVerifier`로 테스트 검사 한 개가 실제 실행되어 종료 코드 0·`executed=true`임을 확인했다. 전체 평가, 모델 호출, 외부 환경 및 다른 프로젝트 명령을 검증한 것은 아니다.

호스트에서 `ooo evaluate`를 요청하면 세션 ID·원래 Seed·산출물·절대 작업 경로를 구분한다. 평가만 원하면 `auto_evolve: false`를 명시한다. MCP 백그라운드 평가에서 자동 진화가 켜지고 formal 결과의 `final_approved`가 `false`이면 후속 Ralph 등록을 시도한다. 여기에는 실행 증거가 없는 `unverified`도 포함된다. 원본 Seed를 불러올 수 없거나 등록이 실패하면 후속 작업은 시작되지 않을 수 있다. 반환된 evaluation job뿐 아니라 `chained_ralph_job_id`의 종료와 결과까지 확인한다. `chained_ralph_skipped` 또는 `chained_ralph_error`도 확인한다. 시작 영수증은 완료가 아니다. OpenCode plugin의 일부 경로는 `job_id=None`으로 위임될 수 있으므로 실제 반환된 표면을 따른다. [evaluate 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evaluate/SKILL.md), [연쇄 조건 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evaluation_job.py), [상태 추적](/docs/progress-detail/).

직접 MCP 백그라운드 평가를 시작하려면 `ouroboros_start_evaluate`에 실제 `session_id`와 평가할 `artifact`를 전달한다. 원래 기준을 평가하도록 `seed_content` 또는 명시적 수용 기준과 실제 `working_dir`을 함께 전달하고 반환된 기준을 대조한다. 이들은 CLI 인자가 아니라 연결된 MCP 도구의 JSON 입력이다. 예를 들어 `auto_evolve`를 `false`로 명시하면 이 호출의 자동 후속 진화를 끈다. 일반 경로는 반환된 `job_id`로 `ouroboros_job_wait`/`ouroboros_job_result`를 조회한다. OpenCode plugin 위임과 자동 진화 비활성화가 함께 적용되면 job을 만들지 않고 `job_id=null`로 반환하므로 Task pane의 자식 결과를 확인한다. 같은 plugin 조건에서도 자동 진화가 활성화되면 후속 작업을 관리하기 위해 부모가 조회 가능한 평가 job을 유지한다. ID가 없을 때 임의의 ID로 조회하지 않는다. 이는 [백그라운드 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evaluation_handlers.py)의 소스 대조이며 실제 모델 평가·호스트 위임을 시험한 결과가 아니다.

직접 MCP `ouroboros_evaluate`는 `session_id`와 `artifact`가 필수다. 유효한 비빈 `acceptance_criteria` 배열이 있으면 단수 `acceptance_criterion`보다 우선하고, 배열이 없거나 유효 항목이 없으면 단수 기준을 쓴다. 둘 다 없으면 유효한 `seed_content`의 수용 기준을 사용한다. 기준이 여러 개면 기준별로 평가하고, 하나면 단일 평가 경로다. Seed 파싱이 실패해도 이 핸들러는 경고를 기록하고 Seed 없이 계속할 수 있다. 기준을 얻지 못한 **in-process 단일 평가**는 일반적인 기본 기준을 사용하므로, 도구가 응답했다는 사실만으로 원래 Seed의 기준이 평가되었다고 판단하지 않는다. 전달한 YAML과 기준, 반환된 실제 기준·판정·검사 증거를 대조한다. Plugin 위임은 별도 경로이므로 그 결과까지 확인한다. 위 동작은 [고정 직접 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evaluation_handlers.py)의 정적 대조이며 실제 모델 평가를 실행한 결과가 아니다.

## 안전하지만 잘못된 산출물 확인

검사가 통과하고 변경이 안전해도 원래 요청의 중요한 산출물 유형이 바뀌면 결과는 틀릴 수 있다. 예를 들어 반복 실행할 CLI를 요청했는데 인수인계 문서만 생성하거나, 일괄 처리를 요청했는데 단일 사례 요약만 만든 경우다. 원본 Seed 자체가 요청을 잘못 담았다면 그 Seed의 기준에 대한 승인만으로 원래 요청의 충족을 증명할 수 없다.

완료를 선언하기 전 원래 사용자 요청과 이후 명시적 수정, Seed, 실제 결과를 대조한다. 요청한 코드·도구·워크플로·문서 등 **산출물 종류**와 범위가 맞는지, 반복 사용을 요청했다면 새 입력으로 실행할 수 있는지, 문서나 체크리스트를 최종 제품 대신 내세우지 않았는지 확인한다. 누락된 데이터는 `0`이나 통과로 바꾸지 말고 미확인·부족으로 표시한다. 실제 검사 명령과 결과가 파일의 존재뿐 아니라 요청한 동작을 뒷받침하는지도 확인한다.

차이가 발견되면 기존 Seed가 유효하다고 가정하고 반복을 계속하지 않는다. 원본 가이드의 **권장 판단**은 승인 없는 산출물 유형 변경을 차단하고, 더 좁은 범위를 의도했는지 불명확하면 사용자에게 확인하며, Seed에 잘못 인코딩됐다면 올바른 요청으로 다시 만드는 것이다. 유용하게 생성된 문서는 보조 산출물로 보존하되 요청한 도구가 없다면 부분 완료로 보고한다. 이는 사람이 적용할 진단·복구 절차이며 평가기가 모든 유형 변경을 자동으로 탐지하거나 차단한다는 보장은 아니다. [원본 가이드](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/guides/safe-but-wrong-output.md), [드리프트 측정의 한계](/docs/drift-detail/).

## Seed 기준별 체크리스트 요청

MCP의 `ouroboros_checklist_verify`는 실행 결과와 Seed의 수용 기준을 평가기에 전달하는 **직접 호출**이다. 필수 입력은 실제 실행 `session_id`, 전체 Seed YAML 문자열인 `seed_content`, 평가할 `artifact`다. `artifact_type`은 `code`(기본), `docs`, `config` 중 하나이며 `working_dir`을 선택적으로 전달할 수 있다. Seed 모델 자체는 빈 기준 목록을 허용하지만 이 도구는 비공백 수용 기준이 하나 이상 없으면 오류를 반환한다. 연결된 서버의 스키마와 실제 작업 디렉터리를 먼저 확인한다. [MCP 입력 색인](/docs/mcp-reference-detail/#ouroboros_checklist_verify), [핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evaluation_handlers.py).

핸들러는 모든 비공백 기준을 `EvaluateHandler`에 전달한다. OpenCode plugin 위임이 선택되면 in-process 분기 전에 위임 응답을 반환하므로 실제 평가 결과는 별도로 확인한다. **In-process 평가에서** 기준이 둘 이상이면 각 기준의 평가를 집계해 `checklist`, `ac_count`, `passed_count`, `run_feedback` 등의 결과를 제공한다. in-process에서 기준 하나는 기존 단일 평가 경로이므로 같은 다중 기준 메타데이터가 반드시 있다고 가정하지 않는다. 공통 기계 검사와 기준별 증거를 구분해 읽는다. 결과의 `checklist_verify`와 `seed_goal`, `acceptance_state`·실제 검사 증거 및 실패 사유를 확인하고, 실행된 검사 없는 모델 의견을 승인 증거로 바꾸지 않는다. 오류나 미검증을 통과로 치환하지 않는다.

이 도구는 별도의 백그라운드 시작 영수증이 아니라 평가 결과를 직접 기다리며, **재실행이나 Ralph를 자동으로 시작하지 않는다**. 후속 수정 여부는 호출자가 별도로 결정한다. 다만 평가 자체는 모델과 프로젝트의 설정된 기계 검사 명령을 호출할 수 있어 시간·비용과 실행 부작용이 있을 수 있다. 이 경로를 도구 입력의 존재만으로 실제 동작·외부 효과를 검증한 것으로 취급하지 않는다. 위 평가 게이트와 [검사 명령 경계](/docs/seed-format-detail/), [자동 후속 조건](/docs/config-reference-detail/)을 확인한다.

## 한 세대와 반복을 구분하기

`ooo evolve`의 `ouroboros_evolve_step` 한 호출은 한 generation을 진행한다. `execute=true` 기본 경로에서는 실행·평가 증거를 사용하며, `execute=false`의 온톨로지 전용 비교는 실제 결과의 수용을 증명하지 않는다. 후속 세대에서 Wonder는 미해결 질문을 만들고 Reflect는 그 근거로 온톨로지와 기준을 제안한다. 각 generation의 Seed·실행·평가는 같은 lineage 안에 남지만 ID와 과거 판정을 섞지 않는다.

!!! warning "관리 worktree의 자동 checkpoint commit"
    고정 `ouroboros_evolve_step`의 **in-process 경로**에서 `execute=true`이고 선택된 프로젝트가 Git 저장소이거나 명시되지 않은 경우, lineage worktree를 준비하기 전에 원본 경로가 Ouroboros가 생성했다고 기록한 관리 task worktree이고 해당 `ooo/<durable_id>` 브랜치를 체크아웃한 상태인지 확인한다. 그 조건을 만족하고 변경이 있으면 `git add -A` 후 해당 task branch에 generation checkpoint **commit을 자동으로 만들 수 있다**. 추적 파일의 변경과 Git이 무시하지 않는 미추적 파일이 포함될 수 있으므로 먼저 해당 경로의 변경과 민감정보를 확인한다. 무시된 미추적 파일은 추가되지 않지만 이미 추적된 파일은 별도다. 이 commit은 Git hook을 비활성화한 상태로 수행되므로 hook이 비밀이나 오류를 막아 주었다고 가정하지 않는다. 이는 별도의 `commit_policy`·`auto_session_id`와 평가 결과를 사용하는 AC 통과 checkpoint 처리와 다른 호출이며, 그 정책을 끄는 것만으로 이 generation checkpoint가 꺼진다고 가정하지 않는다. OpenCode plugin 위임 경로에서는 이 in-process 분기에 들어가지 않으며 해당 호스트의 실제 파일 변경은 별도 확인해야 한다. 일반 사용자 checkout이나 관리 출처·브랜치 검사를 통과하지 못한 worktree는 이 자동 commit 대상이 아니다. commit 실패 시 staging 등 앞선 Git 변경이 자동으로 되돌아간다고 가정하지 말고 실제 상태를 확인한다. 합성 관리 worktree에서 add 이후 commit 호출만 실패 대역으로 막은 한 사례에서는 HEAD는 그대로이고 tracked 수정과 신규 파일이 staged로 남았다. 실제 Git 오류 전체를 재현한 것은 아니다. 합성 관리 worktree의 직접 checkpoint 한 사례에서 추적 변경과 사전 staged 파일이 커밋되고 ignored 파일은 제외됐으며 합성 pre-commit hook은 실행되지 않았다. 다른 hook·실패·경합은 시험하지 않았다. 이는 [호출 경로](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py)와 [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/worktree.py)의 정적 대조이며 실제 사용자 저장소나 진화 실행은 시험하지 않았다.

한 세대를 기다리지 않고 시작하려면 MCP `ouroboros_start_evolve_step`에 `lineage_id`를 전달한다. 첫 세대에는 원래 Seed YAML을 `seed_content`로 함께 제공하고 프로젝트 경로를 확인한다. `execute`와 `parallel`은 기본 `true`, `skip_qa`는 기본 `false`다. 보통 반환된 job ID로 상태와 최종 결과를 조회하고, 실행 ID·lineage ID는 별도로 기록한다. OpenCode plugin 위임에서는 job이 아닌 Task pane에서 결과를 확인하며 `job_id=null`이다. 이 plugin 경로는 체크포인트 메타데이터나 만료 claim 복구의 비기본 옵션과 `benchmark_control=true`를 지원하지 않아 거부한다. In-process 경로에서도 같은 lineage의 유효한 미완료 claim이 있으면 시작이 거부될 수 있으므로 기존 작업의 소유 상태를 먼저 확인한다. 시작 결과만으로 generation이 완료되거나 수렴했다고 판단하지 않는다. 모델·파일 변경이 수반될 수 있으며 이 설명은 [고정 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py)의 정적 대조로, 실제 진화 실행은 시험하지 않았다.

| `action` | 읽는 법과 다음 행동 |
| --- | --- |
| `continue` | 열린 기준과 현재 기록을 확인하고 같은 lineage의 다음 단계를 진행한다. 이미 통과한 기준도 회귀를 확인할 수 있다. |
| `ontology_stable` | 유사도가 높아도 수용 검증은 별개다. 검증 없는 온톨로지 전용 종료를 성공으로 보고하지 않는다. |
| `converged` | 해당 진화 경로가 수렴 조건을 충족했다는 결과다. 실행·평가 및 각 기준의 근거를 함께 읽는다. |
| `stagnated` | 의미 있는 진전이 멈춘 종료 이유다. 막힌 원인과 사용자 목표를 다시 본다. |
| `exhausted` | 세대 상한 도달이다. 성공으로 바꾸지 말고 산출물과 미해결 기준을 남긴다. |
| `failed`, `interrupted` | 실패·중단 지점과 job/lineage를 확인하고 재시작 전에 실제 상태와 기존 결과를 살핀다. |

소스의 `EvolutionaryLoopConfig` 기본 최대 세대는 30, `ConvergenceCriteria` 기본 유사도 기준은 `0.95`·최소 세대는 2다. 다만 실행·평가된 결과가 outcome gate를 충족하면 첫 세대에서도 종료할 수 있으므로 “반드시 두 세대가 필요”하다고 단정하지 않는다. 온톨로지 유사도만으로 실행·평가가 필요한 모드의 승인이 만들어지지는 않는다. [수렴 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/convergence.py), [evolve 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evolve/SKILL.md).

MCP 소유 `ooo ralph`는 한 단계씩 호출하고 결과·종료 조건을 추적하는 별도 반복 경로이며 `RalphLoopConfig.max_generations` 기본은 **10**이다. 위 진화 엔진의 30과 같은 설정으로 혼동하지 않는다. `converged` 이후에도 권위 있는 QA 실패가 있으면 성공으로 보지 않는 경계가 있다. 시작 job·연쇄 job·lineage와 실행 세션의 서로 다른 ID를 기록한다. [Ralph 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/ralph_loop.py), [Ralph 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/ralph/SKILL.md).

## 중단과 되감기

다른 프로세스가 여전히 실행하는지 먼저 확인한다. 상태 기록에 `running`이 남았다는 것만으로 소유자가 살아 있다고 확정하지 않는다. 중단 세대를 재구성할 때 코드의 우선순위는 명시적으로 전달한 Seed, 유효한 중단 세대의 저장 Seed, 마지막 완료 세대의 저장 Seed다. 다른 세대의 Seed로 돌아갈 때 기존 phase resume 지점을 지운다. 중단된 Seed가 존재하지만 손상됐으면 조용히 과거 Seed로 바꾸지 않고 오류로 반환한다. 완료된 세대가 하나도 없고 복원할 Seed도 없다면 원래 Seed를 다시 제공해야 할 수 있다. [Seed 복구 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/evolution/step_seed.py), [복구 안내](/docs/recovery-detail/).

`ouroboros_evolve_rewind`의 `to_generation`은 **보존할 마지막 세대**이며 그보다 뒤 세대를 자르는 변경이다. 읽기 전용 상태 조회와 다르므로 대상 lineage와 보존할 산출물·기록을 먼저 확인한다. 파일 작업공간이나 외부 시스템의 효과가 자동으로 되돌아간다고 가정하지 않는다. [evolve 스킬](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/skills/evolve/SKILL.md).

## 검증 범위

고정 source의 승인 게이트·트리거·복구 구현과 스킬을 읽었다. 2026-11-04의 별도 빈 HOME·기존 Python 3.13 테스트 환경에서 `test_pipeline_acceptance_authority.py`, `test_trigger_consensus.py`, `test_pipeline_trigger_consensus.py`를 실행해 **35개 통과**했다. 모델 어댑터 대역을 사용하는 단위 검사이며 실모델·비용·호스트 UI·모든 릴리스 환경의 실행을 증명하지 않는다. 이 수치는 당시 로컬 test run의 기록이며 공개 재현 자료가 아니다. 상세 옵션과 판본별 차이는 [MCP 입력 색인](/docs/mcp-reference-detail/)과 [CLI 색인](/docs/cli-reference-detail/), 설치된 도구 스키마를 확인한다.

## 계보와 기준별 결과 조회 (MCP)

진화의 반환값에서 **lineage ID**를 보존한다. 이것은 job ID나 실행 세션 ID와 다르다. MCP 도구를 사용할 수 있는 호스트에서 아래는 자연어 명령이 아니라 도구 이름과 JSON 인자의 예다.

```json
{"lineage_id": "여기에-실제-lineage-id"}
```

- `ouroboros_lineage_status`에 위 인자를 주면 저장된 이벤트를 재생해 계보 상태·목표·현재 세대와 가능한 온톨로지, 세대 및 rewind 이력을 텍스트로 반환한다. `meta`에는 lineage ID, 상태, 세대 수, 목표와 있을 경우 frugality proof가 있다. 각 세대 요약의 `pending`은 승인되지 않은 모든 경우에 쓰이므로 실행이 계속 진행 중이라는 뜻은 아니다. ID가 비었거나 이벤트가 없거나 투영할 수 없으면 오류다. 조회가 새 세대를 실행하지는 않지만 기본 EventStore 초기화가 일어날 수 있어 파일 시스템에 대한 무부작용으로 간주하지 않는다.
- `ouroboros_ac_dashboard`는 같은 `lineage_id`를 필수로 받는다. `mode` 생략 또는 `summary`는 최신 세대 기준과 최근 이력, `full`은 세대별 매트릭스, `ac`는 한 기준의 이력을 보여준다. 예: `{"lineage_id":"여기에-실제-lineage-id","mode":"ac","ac_index":1}`. `ac_index`는 표시상 **1부터 시작**하며 `ac`에서 필수다. 구현은 1 이상의 범위를 별도로 강제하지 않으므로 정상 표시 번호를 직접 확인한다. 모르는 `mode`는 오류 대신 summary 형식으로 출력될 수 있다. `meta.mode`는 전달값이므로 형식과 혼동하지 않는다.
- 대시보드의 P/F/U는 각각 통과·실패·미해결이며 U를 실패나 성공으로 바꾸지 않는다. 이력·평가가 없으면 데이터 없음으로 표시한다. 조회 결과는 저장된 평가 이벤트의 투영으로, 현재 작업공간이 그대로이거나 새 평가 없이 목표가 충족됨을 보장하지 않는다. 기본 저장소 초기화와 보유한 저장소 연결 종료가 발생할 수 있다.

근거: 고정 소스의 [계보 상태 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/evolution_handlers.py), [AC 대시보드 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/query_handlers.py), [표시 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/dashboard.py). 실제 모델 실행·실제 운영 계보 검증은 하지 않았다.
