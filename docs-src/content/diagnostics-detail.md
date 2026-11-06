# 설치·MCP·런타임 진단

!!! warning "판본과 검증 범위"
    이 문서의 상세 동작과 합성 관찰은 별도 언급이 없는 한 고정 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2) 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 사용 중인 플러그인과 MCP 서버는 각각 다른 판본일 수 있습니다. 여기에 기록된 시험은 해당 조건의 관찰이며 실제 사용자 환경·모델·호스트 전체를 검증하지 않았습니다. 실행 전 설치된 버전의 도움말과 [현재 제품 CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [현재 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros)를 대조하세요. 판본 차이를 확인하지 않은 기능은 동일하다고 가정하지 않습니다.


기준: 2026-11-04, Ouroboros source [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 독립 CLI의 진단 명령이며, 호스트 플러그인만 설치했다면 전역 `ouroboros` 명령이 있다고 가정하지 않는다. 설치 버전의 `--help`와 [설치·호스트 연결](/docs/first-run-detail/)을 먼저 확인한다. 아래 검사는 실제 작업 성공·모델 인증·외부 도구의 정상 동작을 모두 증명하지 않는다.

## 무엇을 확인할지 고르기

| 상황 | 명령 | 확인 범위와 결과 해석 |
| --- | --- | --- |
| 패키지·호스트 플러그인 설치가 서로 맞는지 | `ouroboros doctor install` | 패키지 버전, 호스트 플러그인·런처·설정 표면을 검사한다. 고정 소스는 설정을 변경하지 않는 검사이며 각 항목에 `pass`·`warn`·`fail`을 표시한다. 하나라도 `fail`이면 종료 1, 경고만으로는 종료 1이 아니다. 설치된 실제 도구를 호출하거나 작업 실행을 증명하지 않는다. |
| 이 판본의 MCP 도구 목록 확인 | `ouroboros mcp info` | 서버 객체를 구성하고 이름·버전·capabilities와 등록 도구·매개변수를 출력한다. `--runtime`은 작업 실행 런타임, `--llm-backend`는 인터뷰·Seed·평가용 백엔드를 선택하는 선택적 override이며 둘 다 생략하면 기본 구성 경로를 쓴다. 이는 실제 클라이언트 연결이나 인증·모델 실행 성공을 확인하는 검사가 아니다. 출력 전에 내부 서비스 구성이 필요하므로 단순 정적 텍스트 조회로 가정하지 않는다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/mcp.py) |
| MCP 서버 환경의 의존성·PID·EventStore 경로 | `ouroboros mcp doctor` | Python·패키지·MCP 프로파일·선택 런타임 의존성·Codex OAuth 준비 상태·EventStore 경로·PID를 검사한다. `fail`이 하나 이상이면 종료 1이고 `warn`만으로는 종료 1이 아니다. 런타임별 검사 조건이 있으므로 각 행과 remediation을 읽는다. |
| 로컬 환경의 제한된 런타임 사실 | `ouroboros mcp doctor-runtime` | PATH의 제한된 실행파일 메타데이터, 로컬 loopback 바인드 가능 여부, MCP PID registry의 제한된 메타데이터를 보고한다. 원본 collector는 프로세스 인자·자격증명·임의 환경 값과 registry **내용**을 읽지 않는다고 명시한다. 바인드는 임시 loopback 소켓의 가용성 검사이며 외부 연결·모델 호출 성공이 아니다. |
| 설정·실행 백엔드·자격증명 경로 및 이벤트 DB | `ouroboros status health` | 설정 로드, DB, runtime 및 자격증명 준비 상태를 검사한다. 이 판본은 기존 EventStore를 읽기 전용으로 열어 이벤트 테이블을 조회하고 schema를 생성하지 않는다. DB가 없으면 첫 실행 시 생성될 수 있다고 경고하며, `error`가 있으면 종료 1이다. 경고만으로 종료 1이 되지는 않는다. 자격증명 행의 검사 범위는 백엔드마다 다르다. Codex는 인증 파일 또는 환경변수의 존재를, 일부 공급자는 키 존재·빈값·템플릿을 확인한다. 일부 공급자 검사에서 `credentials.yaml`의 `api_key`는 먼저 문자열로 변환되므로 YAML의 null·숫자·불리언도 빈 문자열이 아닌 값으로 처리될 수 있다. 이 행의 `ok`만으로 키의 타입이나 유효성을 확인했다고 보지 않는다. 반면 일부 CLI 백엔드는 로그인 여부를 검사하지 않고 로컬 CLI 인증을 사용한다는 설명과 함께 `ok`를 반환한다. 따라서 `ok`는 공통적으로 실제 로그인·자격증명 유효성이나 모델 호출 성공을 보장하지 않는다. |

합성 임시 DB로 `status health`를 시험했을 때, 없는 파일은 warning·종료 0이었고 SQLite가 아닌 파일은 `invalid event store` 오류·종료 1이었다. 그 합성 파일을 다른 이름으로 옮기면 다시 missing warning이 됐지만 이는 **데이터 복구가 아니다**. 실제 DB를 이동·삭제하기 전에 실행 소유자와 백업을 확인하고 복구 절차를 검토한다. 이 시험은 실제 운영 DB나 모든 손상 유형을 검증하지 않았다.

MCP doctor의 EventStore 행은 **파일 존재와 크기**를 확인한다. 파일이 없어도 첫 사용 시 생성된다는 `pass`가 나올 수 있으며, 이 행만으로 SQLite 무결성·기존 데이터 복구·모델 실행을 증명할 수 없다. `status health`의 읽기 전용 event 조회와 검사 범위가 다르다. PID가 살아 있다는 결과도 올바른 세션 소유자나 작업의 정상 진행을 보증하지 않는다. 경고가 권하는 파일 삭제나 `VACUUM`을 그대로 실행하지 말고 실제 소유자·영향·백업을 먼저 확인한다. [MCP doctor 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/mcp_doctor.py), [health 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py), [복구](/docs/recovery-detail/).

`status health`에서 **Configuration이 error여도 다른 행이 구체적인 결과를 표시할 수 있다.** 원본은 YAML 로딩에 성공한 뒤 설정 모델 검증만 실패하면 Configuration 오류를 기록하면서 이미 읽은 설정으로 DB·런타임·자격증명 행도 검사한다. 따라서 다른 행의 `ok`나 `warning`을 전체 설정이 유효하다는 뜻으로 해석하지 말고 Configuration 오류부터 수정한 후 재검사한다. 임시 HOME에서 합성된 지원하지 않는 runtime 설정은 Configuration `error`와 DB `warning` 등 다른 행을 함께 출력했고 전체 종료 코드는 1이었다. 이는 한 사례이며 실제 인증·모델·운영 DB는 시험하지 않았다. 이 실험은 별도 user/network namespace에서 수행했으나 파일시스템·Unix 소켓이나 이탈 자손까지 격리한 것은 아니다. [health 분기](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py).

`ouroboros config validate`의 성공도 실행 파일의 유효성까지 증명하지 않는다. 고정 구현에서 선택된 backend의 설정된 CLI 경로는 존재 여부를 확인하지만, 그 경로가 실행 가능한 파일인지까지 확인하지 않는다. 경로가 빈 문자열이면 존재 검사 자체를 건너뛴다. 별도 빈 임시 HOME의 Codex 설정에서 빈 `codex_cli_path`도 실제 CLI 검증이 종료 0이었다. 빈 임시 HOME에서 합성 Codex CLI 경로를 일반 디렉터리로 지정해 실제 `config validate`를 실행했을 때 종료 코드 0과 유효하다는 메시지가 나왔다. 이 한 사례는 실제 backend 실행·인증을 시험한 것이 아니며, OS 수준 네트워크 격리도 검증하지 않았다. 실행 전에 설치된 CLI와 경로·실행 권한을 별도로 확인한다. [설정 검증 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/config.py).

Codex 사용 시 `status health`의 Runtime backend `ok`도 **실제 선택될 경로가 유효하다는 보장은 아니다**. 고정 구현의 health 검사는 환경 변수 후보가 잘못돼도 설정 파일의 다음 후보를 검사해 `ok`를 표시할 수 있다. 반면 Codex 경로 로더는 비어 있지 않은 `OUROBOROS_CODEX_CLI_PATH`를 설정 파일보다 우선한다. 합성 시험에서 resolver의 별도 명시 경로는 지정하지 않고, 존재하지 않는 환경 변수 경로와 실행 가능한 임시 설정 경로를 함께 지정하자 health 검사 함수는 설정 경로에 `ok`를 반환했지만, 경로 로더와 Codex resolver는 존재하지 않는 환경 변수 경로를 선택했다. resolver에 별도 명시 경로를 전달하면 그것이 우선한다. 따라서 이 조합에서는 두 경로와 해당 프로세스의 환경을 비교해 잘못된 override를 수정한 뒤 재검사한다. 이 시험은 개별 함수의 경로 선택만 확인했으며 실제 CLI 실행·모델 인증은 시험하지 않았다. [health 후보 검사](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/status.py), [Codex 경로 로더](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py), [Codex resolver](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/codex/cli_policy.py).

## 출력과 선택적 검사

격리된 임시 HOME의 합성 `credentials.yaml`로 자격증명 검사 함수를 직접 호출한 시험에서 해당 provider의 명시적 `null`·`false`·`0`은 자격증명 행 `ok`, 빈 문자열은 `warning`이었다. 첫 시험은 backend의 provider 매핑을 잘못 가정한 fixture여서 모두 `warning`이었고 올바른 provider로 고쳐 재실행했다. 이 함수 수준 시험은 전체 CLI health 결과, 실제 인증·모델 호출이나 OS 네트워크 격리를 검증하지 않았다. 별도 격리 HOME에서 실제 `status health` CLI를 합성 openrouter `null`·`false` 자격증명으로 실행했을 때 두 경우 모두 자격증명 행은 `ok`였지만 전체 명령은 각각 종료 1이었다. 최초 시험은 출력 핸들을 수집하지 못해 프로세스 종료를 확인한 뒤 새 임시 환경에서 재시험했다. 이 사례도 실제 인증이나 OS 네트워크 격리를 검증하지 않는다. 사용자 자격증명은 사용하지 않았다.

`ouroboros doctor install --json`, `ouroboros mcp doctor --json`, `ouroboros mcp doctor-runtime --json`은 JSON 출력이다. `status health`의 옵션은 설치 버전의 `ouroboros status health --help`를 확인한다. 일반 텍스트와 JSON 모두 경로·버전·실행파일·환경 진단을 포함할 수 있다. 특히 `doctor install`은 설정된 MCP launcher의 명령과 인자를 출력하므로, 그 인자에 비밀이 잘못 들어 있으면 출력에도 포함될 수 있다. 설정 파싱 오류의 세부 내용에도 입력 일부가 나타날 수 있다. 공유 전 전체 출력의 개인 경로·명령·오류·비밀값을 검토하고 가린다. 자격증명 값은 복사하지 않는다. 종료 코드만 보지 말고 각 경고·실패와 그 검사의 범위를 함께 읽는다.

`ouroboros mcp doctor --machine-snapshot`은 정적 기기 정보를 추가로 수집하는 **선택적** 검사다. 소스는 설정 본문을 읽지 않는 제한된 메타데이터라고 설명하지만 실행파일 경로·플랫폼·저장 위치 등이 출력될 수 있다. `--json`의 기본 결과는 검사 결과 **배열**이지만 `--machine-snapshot`을 함께 쓰면 최상위가 `checks` 배열과 `machine_snapshot`을 가진 **객체**로 바뀐다. 자동화는 선택한 옵션에 따라 최상위 타입을 확인해야 한다. snapshot의 개별 probe가 실패해도 이 옵션 자체는 진단 결과의 `fail` 판정에 합산되지 않는다. 정보 공유 전에 내용을 확인한다. [수집 범위 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/machine_snapshot.py).

`ouroboros mcp doctor --probe-local-stdio`는 **별도 선택**이다. 임시 HOME과 임시 EventStore를 사용하는 별도 자식 서버를 시작해 stdio 시작·프로토콜 발견·도구 목록 인식을 검사하고 종료한다. probe 자식은 Python audit hook으로 소켓 및 추가 하위 명령 실행을 차단하고 도구를 호출하지 않는다. OS 전체 네트워크 격리나 실제 호스트 설정·자격증명·모델 호출의 검증은 아니다. probe가 통과해도 기본 검사 중 다른 `fail`이 있으면 전체 명령의 종료 코드는 1이다. [probe 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/mcp_doctor.py).

격리된 빈 HOME의 고정 소스 CLI에서 `mcp doctor --json`과 `--machine-snapshot --json`을 각각 실행한 합성 환경 시험에서는 전자가 배열, 후자가 `checks` 배열과 `machine_snapshot` 객체를 반환했다. 두 명령 모두 종료 1이며 각각 9개 검사를 보고했다. 출력에 기기 메타데이터가 포함될 수 있어 시험 기록에는 값 대신 형태와 개수만 남겼다. 다른 기기·설치 버전의 검사 내용이나 종료 코드를 보장하지 않는다.

## 다음 행동

1. 오류가 난 행의 검사 대상과 현재 설치 경로를 대조한다. 별도 Python 환경의 MCP 2 서버와 Claude SDK 환경을 무작정 합치지 않는다. [런타임별 준비](/docs/runtime-support-detail/)와 [MCP 통합](/docs/integration-detail/)을 확인한다.
2. 설정 변경이나 재설치 전 현재 파일과 작업 상태를 확인한다. `config set`과 uninstall은 보존·되돌리기를 자동 보장하지 않으므로 [설정과 문제 진단](/docs/operations-detail/)의 주의를 따른다.
3. 오류나 `warn`의 원인을 고친 뒤 같은 명령으로 다시 확인한다. 실제 작업의 성공은 해당 작업·결과·검증을 별도로 확인해야 한다.

**검증 범위:** 고정 커밋과 관련 CLI 소스·테스트 경로 차이가 없는 로컬 checkout에서 임시 HOME·TMPDIR, telemetry 비활성 및 최소 환경으로 관련 기존 테스트 **184개 통과**. 별도 빈 HOME에서 `doctor install --json`은 경고만 있는 종료 0, `mcp doctor --json`은 SDK 검사 실패를 포함한 종료 1, `doctor-runtime --json`은 종료 0, `status health`는 종료 1이었다. `mcp doctor --probe-local-stdio --json`의 세 로컬 probe 행은 모두 pass였지만 기본 SDK 검사 실패로 전체 종료 1이었다. 이는 그 임시 설치의 결과이며 다른 환경의 통과 여부가 아니다. 실제 모델·외부 서버·호스트 인증이나 OS 수준 네트워크 격리는 시험하지 않았다.
