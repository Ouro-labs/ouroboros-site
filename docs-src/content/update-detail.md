# 설치된 Ouroboros 갱신과 부분 실패

!!! warning "판본과 검증 범위"
    이 문서의 상세 동작과 합성 관찰은 별도 언급이 없는 한 고정 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 사용 중인 플러그인과 MCP 서버는 각각 다른 판본일 수 있습니다. 여기에 기록된 시험은 해당 조건의 관찰이며 실제 사용자 환경·모델·호스트 전체를 검증하지 않았습니다. 실행 전 설치된 버전의 도움말과 [현재 제품 CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [현재 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros)를 대조하세요. 판본 차이를 확인하지 않은 기능은 동일하다고 가정하지 않습니다.


기준: 2026-11-04, 고정 소스 [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 아래는 이 커밋의 독립 CLI [update 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/update.py)을 설명한다. 배포 패키지 `0.59.9`를 비롯한 설치본이 이 소스와 같다고 가정하지 말고, **해당 설치 환경의** `ouroboros --version`, `ouroboros update --help`, 설치 관리자와 호스트 설정을 먼저 확인한다. 호스트에 설치한 플러그인의 갱신과 독립 CLI 패키지의 갱신은 서로 다른 경로일 수 있다. [설치 경로](/docs/first-run-detail/#install-check), [런타임별 차이](/docs/runtime-support-detail/).

## 플러그인과 CLI의 갱신 대상을 먼저 구분하기 {#plugin-only-update}

아래는 제품 main `592c667f`와 release `0.59.9`의 소스·스킬을 대조한 범위입니다. **호스트에 plugin만 설치했다면 터미널에 `ouroboros`가 없어도 정상일 수 있습니다.** 명령이 없거나 도움말을 실행할 수 없다는 이유만으로 구형 설치·손상이라고 단정하지 마세요. `ooo update` 스킬은 별도 CLI의 `ouroboros update` 호출을 전제로 하므로 plugin-only 설치에서 그대로 동작한다고 보장할 수 없습니다.

| 실제 설치 형태 | 먼저 확인할 대상 | 갱신 후 확인할 것 |
| --- | --- | --- |
| 호스트 plugin만 사용 | 같은 호스트의 실제 plugin 출처·참조와 MCP launcher의 command/args. 별도 CLI 존재를 가정하지 않습니다. | 해당 호스트가 지원하는 plugin 갱신의 범위·기존 pin을 확인합니다. 전역 CLI 신규 설치나 pin 해제를 자동 복구로 대신하지 않습니다. |
| 독립 CLI | 실제 실행 파일과 그 환경의 설치 관리자·extras·원래 설치 기록. `--check`는 원격 정보를 조회합니다. | 같은 환경의 패키지 버전과 실패 단계. 다른 CLI 환경의 성공을 해당 설치의 갱신으로 세지 않습니다. |
| CLI와 호스트 plugin 모두 사용 | CLI 패키지, 설치된 plugin metadata, 그 plugin이 띄우는 MCP 서버를 별도 식별합니다. | 패키지 갱신, 호스트 통합 refresh, 실제 연결된 서버의 도구·판본을 각각 확인합니다. 하나의 버전 일치나 종료 0이 나머지 성공을 보장하지 않습니다. |

고정 Codex descriptor `.mcp.codex.json`은 서버 의존성을 `ouroboros-ai[mcp]==0.59.9`로 지정합니다. plugin을 refresh해도 **선택된 descriptor에 그 pin이 남아 있으면** 별도 CLI 업그레이드가 그 서버 의존성을 바꾸지 않습니다. 반면 조사한 Claude `.mcp.json`의 의존성은 무버전 `ouroboros-ai[mcp]`이므로 두 host의 판본 선택을 같은 방식으로 가정하지 않습니다. 설치된 plugin version 표시는 실제 서버 프로세스 버전·schema 검증을 대신하지 않습니다.

이 두 제품 판본의 updater는 패키지가 최신이면 runtime refresh 분기 전에 반환하므로 `--runtime all`을 붙여 재실행해도 plugin 갱신을 강제하지 않습니다. 업그레이드가 진행되는 경우에도 `--runtime codex`의 setup/rules·skills refresh와 `--runtime all` 분기의 별도 Codex marketplace refresh는 구분해야 합니다. plugin 하나의 문제를 해결하려고 관련 없는 host까지 `all`로 갱신하거나 기존 marketplace 참조를 임의로 해제하지 마세요. 부분 실패의 실제 단계와 범위부터 확인합니다.

근거: [main update 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/update/SKILL.md), [release update 스킬](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/skills/update/SKILL.md), [main updater](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/update.py#L1052-L1070), [release updater](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/update.py#L1051-L1069), [Codex descriptor](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/.mcp.codex.json), [Claude descriptor](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/.mcp.json). 이는 정적 대조이며 실제 host 갱신·서버 재연결·모델 실행은 시험하지 않았습니다.

## 무엇을 확인하고 변경하는가

| 명령/옵션 | 이 소스의 동작과 범위 |
| --- | --- |
| `ouroboros update --check` | PyPI에서 비-yanked 배포 파일이 하나 이상인 최신 버전 후보를 조회해 현재 버전과 비교한다. 현재 Python·플랫폼에서 그 후보가 설치 가능하다는 보장은 아니다. 패키지나 런타임을 갱신하지 않는다. 런타임 선택에 따라 Codex 플러그인 버전도 조회할 수 있다. **오프라인 검사가 아니며** PyPI 실패 시 종료 1이다. 플러그인 상태를 알 수 없다는 경고는 일치의 증거가 아니다. |
| `ouroboros update --dry-run` | 최신 버전 확인과 설치 정체성 검사를 수행하고 실행할 명령을 미리 보여준다. PyPI 조회가 필요하고, 상황에 따라 OMP 설정을 읽는 명령을 호출할 수 있다. 패키지 업그레이드와 설정 쓰기를 실행한 증거가 아니다. 최신 버전이 이미 설치돼 있으면 업그레이드 경로의 모든 단계를 미리 보여준다는 보장도 없다. |
| `ouroboros update` | 최신 버전이 있으면 기본값 **Yes**인 확인 후 패키지를 갱신하고 선택된 런타임 통합을 새로 고친다. `-y`/`--yes`는 확인을 생략하며, `--check`·`--dry-run`과 다르다. 이미 최신이어도 `--check`가 아니면 OMP가 설치된 경우 MCP tool timeout 설정을 확인하고 필요 시 변경을 시도한다. |
| `--prerelease` / `--no-prerelease` | 비교 대상에 사전 출시 버전을 포함하거나 제외한다. 생략하면 현재 설치가 사전 출시인지에 따라 선택한다. 비-yanked 배포 파일이 하나 이상 있는 릴리스를 후보로 찾는다. 이 단계는 현재 Python 버전·플랫폼·배포 파일의 호환성을 확인하지 않으므로 후보가 이 환경에 설치 가능하다고 보장하지 않는다. |
| `--runtime auto` | 기본값. 저장된 백엔드를 기준으로 갱신할 런타임을 정한다. 구성 오류가 있으면 사용 가능한 업데이트가 있을 때 변경 전에 중단할 수 있다. |
| `--runtime none` | 새 패키지 버전으로의 **업그레이드 후 런타임 refresh**를 건너뛴다. 전체 명령이 아무 설정도 건드리지 않는다는 의미는 아니다. |
| `--runtime all` | Claude와 Codex 플러그인 및 설치된 런타임 산출물의 refresh를 시도한다. 각 호스트 설정과 기존 참조, 실제 실행 파일을 먼저 확인한다. 다른 선택지는 설치본 도움말을 확인한다. |

이 구현은 실행 중인 설치의 **uv 또는 pipx receipt**로 관리자·환경·extras 등 원래 설치 프로필을 식별하고 해당 설치를 다시 사용한다. 정체성을 안전하게 확인하지 못하거나 uv의 기록된 버전 제약이 목표 버전과 충돌하면 변경 전 실패하도록 되어 있다. 임의의 전역 `pip`나 다른 가상환경이 현재 실행 파일을 갱신할 것이라고 가정하지 않는다. receipt를 직접 고치는 대신 원래 설치 관리자·프로필을 확인한다. 패키지 설치·갱신은 네트워크와 디스크 변경을 수반한다.

## 갱신 전과 후

1. 현재 실행 파일과 버전, 관리자·환경 및 필요한 extras를 기록한다. 진행 중인 작업의 ID·종료 상태와 작업 트리 변경, 호스트 플러그인 버전을 확인한다. 로컬 변경이나 DB가 원격에 보관됐다고 가정하지 않는다.
2. `--check`로 버전 정보를 확인하고 릴리스의 변경 사항과 이 환경의 호환성을 검토한다. `--dry-run`은 네트워크 없는 시험이 아니며, 설치 identity를 확인할 수 없다면 실패할 수 있다. 설치 유형·호스트 설정에 따라 표시되는 경로와 실행 계획을 확인한다.
3. 실제 갱신을 결정하면 사용할 runtime 범위와 확인 프롬프트를 검토한다. 패키지 업그레이드는 외부 패키지 획득과 로컬 환경 변경을, refresh는 호스트 설정·플러그인 관련 변경을 수반할 수 있다. 로그에 토큰이나 개인 데이터를 남기지 않는다.
4. 완료 출력과 **실행 중인 동일 환경**의 버전, 해당 호스트가 실제 노출하는 도구·설정을 확인한다. 필요하면 해당 호스트 세션을 재시작한다. 버전 번호나 프로세스 종료 0만으로 모든 런타임 통합과 실제 모델 호출 성공을 판단하지 않는다.

## 부분 갱신과 복구

업그레이드 명령 성공 후에도 새 설치 버전을 확인하지 못하거나 목표보다 낮으면 런타임 refresh를 진행하지 않고 실패한다. 패키지는 이미 바뀌었을 수 있으므로 출력과 같은 환경의 버전부터 확인한다. 패키지 갱신 뒤 일부 플러그인·설정 refresh가 실패하면 `Ouroboros partially updated`와 실패 단계·복구 명령을 출력하고 종료 1을 반환한다. 그 명령의 실제 대상과 부작용을 확인한 뒤 필요한 단계만 다시 수행한다. **패키지가 이미 최신일 때 `ouroboros update`를 다시 실행해도 실패한 런타임 refresh를 다시 시도하지 않는다.** 무조건 반복 실행하지 말고 출력된 복구 안내와 설치 버전의 `setup --help`를 확인한다.

Claude CLI가 없는 경우에는 코드가 해당 refresh를 건너뛰고 추후 setup 안내를 표시할 수 있다. Codex 플러그인의 pinned marketplace ref나 버전 불일치 경고도 실제 참조를 확인하기 전에는 해결됐다고 판단하지 않는다. `--runtime none`으로 의도적으로 생략한 통합도 따로 설정 여부를 확인한다. 특정 호스트 세션 재시작은 해당 프로세스의 연결·상태에 영향을 줄 수 있으므로 진행 중인 작업부터 확인한다.

**검증 범위:** 고정 커밋과 해당 update 소스·대상 테스트 차이가 없는 로컬 checkout에서 PyPI·설치 관리자 등 외부 호출을 대역 처리한 `TestCheckFlow`와 Codex check 테스트 **6개가 통과**했다. 실제 PyPI 조회, 패키지 업그레이드, 런타임 refresh, 사용자 설정 변경과 모든 설치 관리자 조합은 시험하지 않았다. 위 부작용·분기는 소스와 테스트 기반 설명이며 다른 배포판의 동작 보장이 아니다. [원본 update 테스트](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/tests/unit/cli/test_update.py).
