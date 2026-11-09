# UserLevel 플러그인: 발견·설치·신뢰·호출

기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지의 UserLevel 프로그램은 Claude·Codex 등 호스트에 Ouroboros를 연결하는 **호스트 플러그인과 별개**다. 호스트 설치는 [첫 실행](/docs/first-run-detail/), 호스트·MCP 연결은 [통합](/docs/integration-detail/)을 참조한다. 설치된 버전의 `ouroboros plugin --help`와 각 하위 명령 도움말이 우선이다.

**판본·확인 범위:** 세부 명령·위험 경계는 위 722판이다. 직접 인용한 plugin CLI, dispatcher, firewall, manifest, hooks, lockfile, trust store의 파일은 공개 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0) 및 release `v0.59.9`와 정적으로 비교했을 때 해당 경로의 차이가 보이지 않았다. 이는 선택 source 파일만의 비교다. 사용자의 독립 CLI·호스트 플러그인·manifest·실제 권한이나 OS sandbox 동작을 확인한 결과가 아니며 외부 plugin 실행도 검증하지 않았다. 설치본의 도움말과 실제 설치 위치·권한을 우선 확인한다.

UserLevel 플러그인은 `ouroboros.plugin.json`에 명령, entrypoint, 기능과 권한을 선언하고 별도 프로세스로 실행되는 프로그램이다. 설치·신뢰는 프로그램의 무해함을 증명하지 않는다. 아래는 고정 소스의 [CLI](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/plugin.py), [manifest](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/manifest.py), [호출 firewall](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/firewall.py)의 정적 설명이다. 아래 합성 시험 외에 외부 플러그인을 설치하거나 실행하지 않았다.

## 상태 확인과 설치 전 검토

독립 CLI가 설치된 환경에서 다음은 명령 표면과 기존 상태를 확인하는 출발점이다. `[경로]`는 검토할 실제 파일 또는 그 파일이 든 디렉터리이며 대괄호를 그대로 입력하지 않는다.

```text
ouroboros plugin --help
ouroboros plugin discover [경로]
ouroboros plugin list
ouroboros plugin inspect [설치된_이름]
```

`discover`는 로컬 manifest를 검증·표시하며 설치나 권한 승인을 하지 않는다. `inspect`와 `list`는 설치된 lockfile 및 신뢰 상태를 읽는다. `discover`는 버전·source 유형과 명령·capability·permission의 개수, namespace 및 필수 scope 등을 요약하고, `inspect`는 설치 위치·출처·신뢰 상태 등을 표시한다. 이 출력만으로 entrypoint와 모든 명령·권한의 세부 내용을 보여 준다고 가정하지 말고 manifest 원문에서 source, version, entrypoint, commands, capabilities와 permissions의 목적·위험·필수 여부를 직접 확인한다. 실행 파일과 출처도 별도로 검토한다. 출력·인자에는 개인 정보가 포함될 수 있다. 이 명령이 프로그램 코드의 안전성을 분석하거나 외부 사이트의 신뢰도를 보장한다는 뜻은 아니다.

Manifest는 `schema_version`, `name`, `version`, `source`, `entrypoint`와 명령·capability·permission 등을 나타낸다. 명령은 namespace·이름·인자·위험·확인 필요 여부, 권한은 정확한 `scope`, `risk`, `required` 등을 기술한다. schema 판본별 허용 필드와 hook 검증이 다르므로 [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/manifest.py)과 실제 `discover` 오류의 경로·JSON pointer를 확인한다. 선언은 실행기능이나 안전한 권한 강제의 증거가 아니다.

## 설치와 신뢰는 별도 단계

- `ouroboros plugin add [저장소_URL_또는_로컬_경로]`는 카탈로그에서 플러그인을 선택해 설치한다. URL이면 Git clone과 로컬 캐시가 발생한다. `--plugin`을 반복해 이름을 명시할 수 있으며 `#plugins/<이름>` 형태의 저장소 내부 경로를 붙인 URL은 거부한다. 설치 후 누락된 필수 권한이 비파괴 scope라면 같은 명령에서 부여할지 대화형으로 물을 수 있다(기본 No). 사용자가 Yes를 선택하면 이 단계에서 trust 기록도 변경된다. destructive scope는 별도 명시적 trust 명령이 필요하다.
- `ouroboros plugin install [이름]`은 알려진 카탈로그에서 이름을 해결한다. 이름이 여러 출처와 충돌하면 `--from`으로 출처를 지정해야 한다. `--from`은 저장소 URL 또는 절대 로컬 경로를 받으며, 기존 로컬 플러그인 디렉터리를 직접 가리키는 호환 경로도 있다. `install`은 비대화형이며 설치만으로 누락된 필수 scope를 자동 승인하지 않는다. 위 `add`의 선택적 승인 질문과 구분한다.
- 기본적으로 설치 파일은 `~/.ouroboros/plugins`, URL 캐시는 `~/.ouroboros/cache`, lockfile은 `~/.ouroboros/plugins.lock`, 신뢰 기록은 `~/.ouroboros/trust`에 있다. 알려진 카탈로그 기록도 `~/.ouroboros/plugin-catalogs.json`에 저장된다. 옵션으로 경로를 바꿀 수 있으므로 실제 명령·환경에서 사용된 경로를 확인한다. 설치와 재설치는 파일·lockfile·카탈로그 상태를 변경할 수 있다.
- `ouroboros plugin trust [이름] --scope [선언된_scope]`는 선언된 scope에 대한 승인을 기록한다. `--scope`는 반복 가능하며 **정확한 문자열**이다. 예를 들어 한 문자열이 더 긴 다른 scope를 자동으로 포함하지 않는다. 선언되지 않은 scope는 거부되고, 모든 필수 scope가 충족되기 전에는 일부만 부여해도 호출이 막힐 수 있다. `--audit-log`를 지정하면 JSONL을 추가로 쓸 수 있다. 선택한 scope의 실제 외부 효과와 명령의 확인 요구를 먼저 검토한다.

신뢰 대상은 버전·source 유형·source identity·artifact digest에 결합된다. 소스나 설치 바이트가 바뀌면 이전 승인이 그 새 대상에 적용된다고 가정하지 않는다. `inspect`의 상태와 현재 파일을 확인하고 차이의 원인을 조사한 뒤 필요한 범위만 다시 승인한다. 첫 설치, 권한 변경이나 원격 다운로드 자체를 이 안내가 승인하는 것은 아니다. [신뢰 저장소](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/trust_store.py), [lockfile](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/lockfile.py).

## 생명주기 훅과 버전 경계

훅은 manifest의 `hooks`에 선언하는 별도 entrypoint다. 현재 명령의 신뢰·확인과 별개로 스키마 버전, 훅 종류, 실패 정책, 선언된 필수 권한이 검증된다. 훅을 모든 실행에 자동 적용되는 일반적인 이벤트 버스로 가정하지 않는다. [훅 종류](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/hooks.py)와 [manifest 검증](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/manifest.py)을 먼저 확인한다.

- `before_invocation`은 신뢰와 확인을 통과한 후 명령 시작 전에 실행된다. `fail_closed`인 훅이 실패하면 해당 호출을 차단할 수 있다. `after_invocation`은 시작된 명령의 결과를 관찰하며 실패로 이미 알려진 결과를 바꾸는 용도로 쓰지 않는다.
- `on_error`, `on_cancel`은 실패·취소 이벤트 이후의 관찰용이며 `fail_open`이 요구된다. 명시적 `cancellation_requested`는 disable·무결성·필수 권한 신뢰 검사를 통과한 뒤 확인 질문과 명령 시작 전에 처리되며, 실패 이벤트를 기록한 후 `on_cancel`을 호출한다. 취소 훅은 정리 작업을 수행할 권한을 부여하는 계약이 아니다. 사전 신뢰 실패 등 명령 시작 전에 막힌 모든 경우에 훅이 실행된다고 가정하지 않는다.
- `before_tool_call`과 `after_tool_call`은 schema `0.4` 및 `0.6`의 도구 호출 경계에 관한 훅이다. before의 차단 권한에는 별도 필수 scope 조건이 있고, after는 `fail_open`이다. 일반적인 모든 호스트 도구 호출을 가로챈다는 의미는 아니다.
- `on_rewind`는 schema `0.6`의 커밋된 rewind **이후 관찰**이며 `fail_open`과 필수 `plugin:rewind:observe` scope가 요구된다. 되돌리기 거부나 재시도 권한을 의미하지 않는다. `before_artifact_write`, `after_artifact_write`는 이 고정 소스의 지연 후보이므로 사용 가능한 훅으로 추측하지 않는다.

이 설명은 고정 소스의 정적 대조와 훅 계약·manifest 검증·권한 scope 단위 테스트 46개를 격리 환경에서 실행한 결과에 근거한다. 실제 외부 플러그인, 모든 훅 실행 순서·타임아웃, 모든 호스트 도구 호출과 OS 권한 강제는 검증하지 않았다. 테스트는 기존 가상환경을 사용했으므로 모든 의존성이 고정 lock과 일치한다고 보장하지 않는다.

## 호출·비활성화·제거

호출 firewall은 제3자 플러그인의 필수 권한·신뢰를 확인하고, 명령이 확인을 요구하면 전달된 확인 콜백이 승인한 뒤 entrypoint를 하위 프로세스로 실행한다. 내장 `first_party` 플러그인은 신뢰 검사에서 예외지만 disable 검사 등 다른 경계가 없다는 뜻은 아니다. 독립 CLI dispatcher는 대화형 확인 콜백을 전달한다. **직접 Python `invoke_plugin`을 호출할 때 기본 `confirm`은 자동으로 `True`를 반환한다.** 사람의 승인 경계가 필요하면 호출자가 적절한 확인 콜백을 명시적으로 제공해야 한다. firewall은 호출자가 전달한 event sink에 이벤트를 보낸다. 독립 CLI dispatcher는 현재 이벤트를 로컬 목록에 수집한 뒤 별도로 영속하지 않으므로 CLI 호출만으로 내구 감사 기록이 남는다고 가정하지 않는다. 이벤트의 권한 표시는 선언된 필수 권한을 거친 수준이며, 이것이 프로세스의 실제 모든 파일·네트워크 접근을 추적하거나 OS 샌드박스로 차단한다는 뜻은 아니다. 명령 인자는 감사 이벤트에 그대로 들어갈 수 있고 stdout/stderr는 해시로 기록되지만 출력 자체는 호출자에게 전달될 수 있다. 비밀을 인자로 넣지 말고 로그·결과 공유 범위를 검토한다. 실행 경로와 호스트의 실제 권한을 별도로 확인한다.

고정 소스의 플러그인 명령과 lifecycle hook은 **호출 프로세스의 환경변수 전체를 복사해 상속**한다. 따라서 승인된 scope와 별도로 환경변수에 든 인증정보도 플러그인이 읽을 수 있다. 실행 전에 환경을 최소화하고 필요한 경우 별도 OS 격리를 적용한다. 구현은 현재 작업 디렉터리를 `OUROBOROS_PLUGIN_WORKDIR`, 그 아래 `.ouroboros/plugin-artifacts/<플러그인_이름>` 경로를 `OUROBOROS_PLUGIN_OUTPUT_DIR`로 전달하며, plugin home이 있으면 `OUROBOROS_PLUGIN_HOME`도 전달한다. 경로 변수의 존재가 해당 디렉터리의 생성이나 접근 제한을 보장하지는 않는다. 이는 [고정 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/firewall.py)의 정적 확인이며 환경 격리나 실제 외부 플러그인 실행은 시험하지 않았다.

독립 CLI dispatcher는 플러그인의 표준 출력·오류를 터미널로 전달하고, 실패나 차단의 설명을 표준 오류에 추가한다. 실행 결과에 종료 코드가 있으면 이를 전달하며, 신뢰 실패·비활성화·확인 거절처럼 실행 전에 차단되어 코드가 없는 경우 1로 처리한다. 고정 firewall의 일반 명령 하위 프로세스 제한은 300초이고 timeout 경로는 코드 124를 반환한다. 코드 124만으로 timeout을 단정할 수는 없다. 플러그인이 같은 코드로 종료할 수도 있다. lifecycle hook은 별도의 timeout 경로를 사용하므로 300초는 훅을 포함한 전체 호출 시간이나 자손 프로세스의 종료를 보장하지 않는다. 종료 코드와 함께 오류 메시지, 실제 실행 상태·부작용을 확인한다. 이는 [dispatcher](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/plugin_dispatch.py)와 [firewall](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/plugin/firewall.py)의 정적 대조이며 실제 timeout·외부 플러그인을 시험하지 않았다.

`ouroboros plugin disable [이름]`은 설치 lockfile을 유지하면서 disable 기록을 쓰고 신뢰 기록을 지운다. 다시 사용하려면 적절한 trust 경로가 필요하며, 필수 권한이 없는 플러그인은 scope 없이 재활성화할 수 있다. `--trust-root`를 사용했다면 같은 실제 경로를 지정해야 한다. `ouroboros plugin remove [이름]`은 lockfile 항목과 신뢰·disable 기록, 설치된 plugin home을 제거한다. 파일 삭제가 수반되므로 대상과 보존할 데이터를 먼저 확인한다. 오류에 따라 일부 상태나 파일이 남을 수 있으며 결과를 확인한다. 캐시 또는 플러그인이 만든 외부 데이터까지 모두 삭제하거나 외부 효과를 되돌린다고 가정하지 않는다.

`plugin remove`의 `--plugin-home-root`는 단순 검색 경로가 아니라 **삭제 대상 경로를 바꾼다.** 명시하면 lockfile에 기록된 설치 위치 대신 지정한 root 아래 `[이름]` 디렉터리를 재귀 삭제한다. 이 디렉터리가 실제 설치본인지 자동으로 확인하지 않으므로, override를 쓰기 전 확장된 root와 이름에 대응하는 실제 경로 및 보존할 내용을 확인한다. 명시하지 않으면 lockfile의 `plugin_home`을 사용한다. 격리된 합성 시험에서 설치된 이름에 다른 임시 root를 지정하자 그 아래 같은 이름의 sentinel 디렉터리가 삭제됐고 원래 합성 source는 남았다. 반복 제거는 설치 항목이 없어 오류였다. 실제 사용자 파일·권한 오류·동시 변경은 시험하지 않았다. [고정 제거 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/plugin.py). 이 관찰은 한 합성 디렉터리의 과거 시험이며 공개 재현 코드나 실제 사용자 파일 제거 결과는 제공하지 않는다.

**검증 범위:** 고정 커밋과 해당 소스·테스트 경로에 차이가 없는 로컬 체크아웃에서 manifest와 firewall의 기존 단위 테스트 **103개가 통과**했다. 임시 HOME·임시 디렉터리와 telemetry 비활성 환경을 썼다. 도움말은 로컬 CLI에서 확인했다. 이 단위 테스트는 외부 저장소 clone, 실제 외부 플러그인 설치·승인·호출, OS 격리 및 실제 외부 효과를 검증하지 않았다.

고정 소스의 신규 설치본에서 합성 로컬 manifest 한 개의 `discover` 성공과 잘못된 permission risk의 오류를 별도 임시 환경에서 확인했다. 이 시험은 플러그인 설치·실행이나 권한 강제를 검증하지 않는다.


## 합성 로컬 플러그인으로 확인한 한 경로

빈 임시 HOME의 실제 독립 CLI에서 직접 만든 최소 manifest를 `plugin discover`로 읽고 `plugin install`로 설치한 후, 필수 `demo:read` scope를 아직 승인하지 않은 `ouroboros local-demo ping`은 종료 1로 차단됐다. `plugin trust local-demo --scope demo:read` 후 같은 호출은 `/bin/echo`의 합성 표식을 출력하고 종료 0이었다. 이어서 `plugin disable local-demo`를 수행하자 호출은 다시 종료 1로 차단됐다. 각 단계의 실제 출력과 상태를 확인해야 하며, 이 경로는 **한 합성 로컬 프로그램의 결과**다. 타인의 프로그램에 권한을 주기 전에는 manifest뿐 아니라 실행 파일·환경·접근 범위를 검토한다. 시험에 쓴 허구 scope는 실제 권한 샌드박스가 아니다.

시험의 CLI·firewall 파일은 고정 Git blob과 일치한다. 임시 HOME/TMPDIR, `unshare -Urn`과 `OUROBOROS_TELEMETRY=0`을 사용해 실제 외부 모델이나 네트워크 서비스는 요청하지 않았다. 사용자·네트워크 namespace만으로 Unix socket·상속 FD·파일시스템 전체 격리를 증명하지 않으며 기존 가상환경의 모든 의존성이 lock과 일치하는지도 확인하지 않았다. 이 합성 실행의 내부 재현 기록은 공개 대상이 아니며 이 문서만으로 재현할 수 없다. 실제 외부 플러그인·원격 clone·권한의 OS 강제 및 실제 재활성화는 시험하지 않았다.
