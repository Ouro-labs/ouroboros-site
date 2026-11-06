# 실행 모니터와 대시보드 고르기

Ouroboros에는 목적이 다른 세 가지 관찰 화면이 있습니다. 진행 중인 실행을 보고 싶으면 **웹 대시보드** 또는 **터미널 모니터(TUI)**를, 진화 계보에서 수용 기준(AC)의 판정 추이를 보고 싶으면 MCP의 **AC 대시보드**를 고르세요. 어느 화면도 실행의 소유자나 승인 판정 자체를 대신하지 않습니다.

이 안내는 공개 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 CLI와 대시보드 구현을 기준으로 합니다. 설치된 패키지, host 플러그인, host가 실행하는 MCP 서버의 판본이 다를 수 있습니다. 실제 UI, 키 입력, 네트워크 노출, 인증 설정은 여기서 시험하지 않았습니다.

## 진행 중인 실행: 웹 대시보드

일반 CLI `ouroboros run`은 실행 ID가 준비되면 해당 실행 화면 URL을 출력할 수 있습니다. `ouroboros auto`는 실행 ID가 생기기 전이면 전체 실행 목록 URL을 출력할 수 있습니다. 이 두 명령은 **작업 실행 명령**이기도 하므로, 대시보드만 열려고 새 실행을 시작하지 마세요. 자동 대시보드 링크는 기본 활성화되어 있으며 실행 프로세스의 `OUROBOROS_DASHBOARD=0` (`off`, `false`, `no`도 가능)으로 끌 수 있습니다. DB 경로를 안정적으로 확인할 수 없거나 데몬을 시작할 수 없으면 링크가 생략될 수 있습니다. 이는 작업의 성공이나 실패를 나타내지 않습니다.

기존 실행을 관찰하려면 독립 CLI 환경에서 다음 모듈을 직접 실행할 수 있습니다.

```bash
python -m ouroboros.dashboard_web --help
python -m ouroboros.dashboard_web
```

도움말과 달리 두 번째 명령은 단순 조회가 아닙니다. 기본 설정의 EventStore DB를 대상으로 detached 서버를 시작하거나 같은 DB를 제공하는 기존 서버를 재사용하고, 접속 URL과 최근 실행을 출력합니다. 실행 ID가 이미 있다면 실제 ID를 사용해 특정 화면 URL을 출력할 수 있습니다.

```bash
python -m ouroboros.dashboard_web --run ACTUAL_EXECUTION_ID
```

`ACTUAL_EXECUTION_ID`는 자리표시자이므로 실제 반환된 실행 ID로 바꾸세요. DB를 지정할 경우 `--db` 뒤에 실제 SQLite 파일 경로를 전달합니다. 다른 사용자나 프로젝트의 DB를 실수로 열지 않도록 시작 전에 경로를 확인하세요. 이 모듈은 공개 main의 Python 패키지에 포함되며 별도 `ouroboros dashboard` 콘솔 명령으로 등록되지는 않았습니다.

웹 대시보드는 EventStore를 `mode=ro`로 읽어 실행 요약과 이벤트에서 만든 진행 보드를 표시하고, 실행별 SSE 연결은 새 이벤트를 반영합니다. 목록에는 목표 설명과 상태/AC 요약이 나타날 수 있고, 상세 보드·이벤트에는 프로젝트 정보와 작업 내용이 포함될 수 있습니다. 목표·수용 기준·질문·결과에 민감 정보가 있을 수 있으므로 URL을 전달하거나 snapshot을 공유하기 전에 해당 데이터가 공개되어도 되는지 확인하세요. 읽기 전용 SQLite 연결은 이 reader가 해당 DB 연결로 쓰지 않는다는 뜻입니다. 대시보드 시작 시 홈의 `.ouroboros` 디렉터리에 `dashboard.json`과 `dashboard.lock` 같은 daemon 상태 파일을 만들거나 갱신할 수 있으며, 애플리케이션 전체나 다른 프로세스의 쓰기까지 읽기 전용이라고 보장하지 않습니다.

### localhost와 네트워크 노출

자동 서버의 기본 주소는 `127.0.0.1`에 바인딩됩니다. 이는 사용자별 인증 경계가 아닙니다. HTTP 서버는 loopback에 도착한 요청에 대해 사용자 인증이나 권한 검사를 하지 않으므로, 같은 기기 또는 네트워크 네임스페이스에서 서버 포트에 연결할 수 있는 다른 프로세스·사용자와 로컬 프록시도 무인증 대시보드·API 데이터에 접근할 수 있습니다. `python -m ouroboros.dashboard_web --host HOST`로 바인딩 주소를 바꿀 수 있지만 `0.0.0.0` 같은 공개 인터페이스에 바인딩하면 네트워크에 접근할 수 있는 다른 사용자가 대시보드 데이터를 볼 수 있습니다. 민감한 목표·질문·이벤트가 담길 수 있는 URL과 데이터 접근을 보호하고, 별도의 인증·접근 통제·데이터 공개 범위를 검토하지 않은 채 바인딩을 넓히지 마세요.

루프백 주소는 대시보드 서버가 실행되는 기기에서만 `localhost`로 연결됩니다. 원격 host에서 출력한 `http://localhost:PORT`를 다른 기기의 브라우저에 그대로 입력해도 그 브라우저 기기의 localhost를 가리킵니다. 안전한 원격 접속 방식과 접근 통제는 네트워크 환경별로 별도 검토가 필요하며, 이 제품 안내는 터널이나 프록시 구성을 제공하거나 시험하지 않았습니다. 같은 DB를 서비스하는 기존 데몬이 재사용되면 새 `--host` 값이 기존 데몬의 바인딩을 바꾼다고 가정하지 마세요.

### 데몬 종료와 상태 확인

웹 서버는 호출한 CLI/MCP 세션과 분리된 프로세스로 시작할 수 있어, 브라우저 탭이나 호출 세션을 닫아도 계속 살아 있을 수 있습니다. 기본 구현은 성공한 목록 조회나 열려 있는 SSE 연결이 없는 상태가 600초 지속되면 종료를 시도합니다. 포트는 데몬이 현재 사용 가능한 포트를 자동 선택하며 module CLI에는 `--port` 옵션이 없습니다. `--host`는 바인딩 주소를 정할 뿐 포트를 고정하지 않습니다. 이 자동 종료 시간은 사용자 환경에서 검증한 보장이 아닙니다. `dashboard.json`의 PID나 출력된 주소만으로 프로세스가 아직 살아 있다고 단정하지 말고, 페이지 연결과 실제 서버 응답을 확인하세요. 다른 DB를 요청하면 다른 데몬을 시작해 상태 파일이 갱신될 수 있으며 기존 데몬은 강제 종료되지 않습니다. 기존 프로세스를 임의로 종료하거나 DB 파일을 삭제하지 마세요.

페이지에 실행이 안 보이거나 연결이 끊기면 다음을 확인합니다.

1. 실행을 시작한 것과 같은 사용자·설정 환경인지, URL의 host·port가 현재 서버 위치를 가리키는지 확인합니다.
2. URL을 만든 실행의 실제 `execution_id`와 EventStore 경로를 확인합니다. 웹 보드의 빈 목록이나 `/healthz` 응답은 실행 존재나 실행 성공을 증명하지 않습니다.
3. 별도의 상태 조회에서 같은 실제 ID의 job/session/execution 결과를 확인합니다. 조회 방식은 [상태 안내](/docs/status-guide/)를 따릅니다.
4. `picker_index_contract_unavailable` 또는 HTTP 503이 보이면 저장소 인덱스/투영 계약과 서버 판본이 맞지 않을 수 있습니다. DB를 삭제하거나 임의 마이그레이션하지 말고 DB 경로, 오류, 설치 판본을 보존해 확인하세요.

`/healthz`의 `ok`는 HTTP 데몬 응답만 뜻합니다. 잘못된 DB, 저장소 계약 문제 또는 작업 결과까지 검증한 것은 아닙니다. 서버가 응답하지 않는다고 원래 실행도 멈췄다고 단정하지 마세요.

## 진행 중인 실행: 터미널 모니터(TUI)

터미널에서 `ouroboros tui monitor`를 실행하면 EventStore에 기록된 세션 목록에서 선택해 관찰할 수 있습니다. 기본 TUI backend는 `python`이며 `--backend slt`는 대체 native backend를 선택합니다. 다른 DB를 보려면 `--db-path`에 실제 경로를 지정합니다. 현재 터미널에서 모니터를 열기 어렵다면 `ouroboros tui open`이 새 터미널을 시도하고, headless/지원되지 않는 터미널에서는 수동 실행 명령을 출력할 수 있습니다.

Python TUI 의존성이 없다면 CLI가 `ouroboros-ai[tui]` 설치를 안내합니다. 설치는 환경의 패키지를 변경할 수 있으므로 현재 CLI 환경과 변경 사항을 확인한 뒤 결정하세요. **Python backend**는 지정 DB의 상위 디렉터리를 만들고 EventStore를 초기화할 수 있습니다. `--backend slt` 분기는 이 Python `mkdir`/`EventStore.initialize()` 경로를 실행하지 않습니다. 그러나 이것이 SLT backend를 읽기 전용으로 만들지는 않습니다. main의 [SLT DB 코드](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/crates/ouroboros-tui/src/db.rs)는 `rusqlite::Connection::open(path)`를 호출합니다. 사용 중인 rusqlite `0.33`의 [API 문서](https://docs.rs/rusqlite/0.33.0/rusqlite/struct.Connection.html#method.open)에 따르면 이 호출은 기본적으로 읽기/쓰기 연결이며 해당 경로에 DB가 없으면 파일을 만들 수 있습니다. 생성 여부와 이후 동작은 실제 경로·상위 디렉터리·권한에 따라 달라질 수 있습니다. Python과 SLT 어느 쪽도 이 안내에서 실제 설치 DB로 시험하지 않았으므로 둘 다 무조건 무부작용이라고 가정하지 마세요. backend와 DB 경로, 데이터 상태를 확인한 후 실행하세요.

TUI는 실행을 관찰하지만 그 실행을 소유하지 않습니다. pause/resume 제어를 제공하지 않으며 TUI를 닫아도 별도 작업이 취소된다고 볼 수 없습니다. 실제 취소는 별도 작업이며 실행을 중단할 의도가 분명하고 실제 대상 ID를 확인한 경우에만 해당 취소 안내를 따르세요. 이 문서에서는 TUI를 실제로 실행하거나 키 입력을 시험하지 않았습니다.

## 진화 계보의 AC 대시보드

MCP 도구 `ouroboros_ac_dashboard`는 웹 대시보드와 다른 기능입니다. 실제 `lineage_id`를 받아 진화 세대별 수용 기준 결과를 텍스트로 표시합니다. 기본 `summary`는 최신 세대와 추이 요약, `full`은 AC × 세대 표, `ac`는 한 AC의 이력을 보여주며 이 모드에는 `ac_index`가 필요합니다. 표시되는 AC 번호는 1부터 시작합니다. 도구가 연결된 서버의 실제 도구 목록에 있는지 확인하고 존재하지 않는 경우 ID나 도구 이름을 만들어 호출하지 마세요.

이 결과는 계보에 저장된 AC 판정의 과거 요약이지 현재 실행의 실시간 모니터나 최종 승인 증거를 대신하지 않습니다. `U`/unresolved는 권위 있는 판정이 없다는 뜻이지 실패가 아닙니다. AC 대시보드의 출력이 비어 있거나 계보를 찾지 못하면 실제 lineage ID와 해당 서버의 EventStore 범위를 확인합니다. 도구 핸들러는 EventStore를 초기화해 사용하므로 실제 저장 경로와 판본을 확인하고, 이 조회가 모든 환경에서 무부작용이라고 가정하지 마세요.

## 출처와 확인하지 않은 범위

이 가이드는 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [TUI 명령](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/tui.py), [대시보드 실행 모듈](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/dashboard_web/__main__.py), [데몬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/dashboard_web/daemon.py), [HTTP 서버](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/dashboard_web/server.py), [EventStore reader](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/dashboard_web/reader.py), [AC dashboard MCP handler](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py)를 정적으로 대조했습니다. 구판 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2), 배포판 `0.59.9`, 실제 설치된 호스트의 판본·인증·데이터·동작은 대조 또는 시험하지 않았습니다. 실제 GUI 화면·TUI 키·서버 접속, 동시 실행, 성능, 네트워크 노출과 운영 중단 절차도 검증하지 않았습니다. 옵션과 동작은 설치된 판본의 도움말 및 도구 스키마를 먼저 확인하세요.
