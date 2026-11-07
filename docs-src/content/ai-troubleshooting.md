---
description: "설치, MCP 연결, 권한 범위, 작업 상태와 ID, 중단·실패 복구를 제품 main 592 기준으로 안내합니다. 설치된 호스트와 서버 판본을 확인하세요."
---

# AI를 위한 Ouroboros 진단과 복구

Ouroboros가 설치되지 않거나, MCP가 연결되지 않거나, 실행이 멈춘 것처럼 보일 때 AI와 사용자가 함께 쓰는 안내입니다. **환경 식별 → 증상 확인 → 기존 작업 보존 → 필요한 조치 → 결과 검증** 순서로 진행합니다. 호스트에 플러그인만 설치된 경우 터미널 CLI가 없을 수 있습니다.

이 페이지의 제품 코드 기준은 2026-11-07에 확인한 upstream main [`592c667f076c3dad7ef68d7844e91480d80135d0`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)입니다. 공개 패키지, 호스트 플러그인, 그 호스트가 실행하는 MCP 서버는 서로 다른 판본일 수 있습니다. **먼저 문제를 일으킨 환경과 설치된 버전의 도움말을 확인하세요.** 이 페이지의 소스 대조는 모든 호스트의 실제 연결, 인증, 모델 호출이나 복구 성공을 증명하지 않습니다.

## AI에게 전달할 정보

문제가 난 기기와 운영체제, 호스트 이름, 작업 폴더, 실행한 명령이나 대화 요청, 증상과 마지막 오류, 실제로 받은 ID를 알려 주세요. 터미널에서 독립 CLI를 사용했다면 다음으로 그 셸의 실행 파일과 버전을 확인할 수 있습니다.

```bash
command -v ouroboros
ouroboros --version
ouroboros --help
```

PowerShell에서는 `Get-Command ouroboros`로 실행 파일을 찾습니다. 명령이 없다는 것은 **그 셸에서** 찾지 못했다는 뜻입니다. 호스트의 플러그인이나 `uvx`로 실행되는 서버가 없다는 증거는 아닙니다. 호스트의 플러그인·MCP 상태 화면에서 활성 서버와 연결 오류를 확인하고, 가능할 때 그 서버의 실행 방식과 판본을 별도로 확인합니다. 다른 사용자, 원격 기기, 가상환경이나 `HOME`은 다른 설치를 선택할 수 있습니다.

**출력 공유 전 검토하세요.** 경로, 프로젝트명, 질문·답변, ID, 설정 오류, 서버 실행 인자에 개인정보나 비밀이 있을 수 있습니다. 키·토큰·자격증명, 전체 환경 변수나 설정 파일을 보내지 말고 필요한 오류를 가려서 전달하세요. `doctor install`도 설정된 launcher 인자를 표시할 수 있습니다. AI는 관찰한 사실과 추정, 수행한 명령과 제안만 한 명령을 구분해 보고해야 합니다.

## 증상별 첫 확인

| 증상 | 먼저 확인할 것 | 다음 행동 |
| --- | --- | --- |
| `ouroboros` 또는 `ooo`를 찾지 못함 | 셸 CLI와 호스트 플러그인을 구분하고 해당 세션의 설치·활성 상태 확인 | [설치와 호스트](/docs/setup-host-detail/)를 참고하고 설치된 도움말을 확인 |
| MCP 도구가 보이지 않음 | 실제 호스트의 서버 상태와 가린 오류, 서버 실행 방식 확인 | 아래 [MCP 연결](#mcp)을 확인 |
| 인증 오류 또는 health 경고 | 선택된 런타임과 해당 호스트의 인증 상태 확인 | 자격증명 값은 공유하지 않고 제공자의 로그인 절차 확인 |
| ID를 받았지만 응답이 없거나 창이 닫힘 | 기존 job 소유자, ID 종류와 작업 폴더 확인 | 아래 [작업 상태와 재개](#recovery)를 확인 |
| Codex가 예상보다 넓은 파일·네트워크 권한을 사용함 | 기존 job과 실제 worker 명령, 제품·Codex 판본 확인 | 아래 [권한과 격리 범위](#permission-scope)를 확인 |
| 업데이트 뒤 일부만 동작함 | 실제 패키지 버전과 실패한 refresh 단계 확인 | 아래 [부분 업데이트](#update)를 확인 |
| 완료라고 표시되지만 결과가 의심됨 | Seed의 조건, 변경 파일과 실제 검증 결과 확인 | 아래 [결과 확인](#verify)을 수행 |

## 진단 명령의 범위 {#diagnostics}

아래 명령은 독립 CLI가 있고 설치된 버전이 해당 명령을 제공할 때 터미널에서 실행합니다. 필요한 검사만 선택하고 각 행의 오류와 경고를 읽으세요. 상태 검사가 데이터 수정을 목적으로 하지 않더라도 로깅·초기화나 의존성 import가 파일 생성 또는 네트워크 요청을 일으킬 수 있습니다. 검사 전에 환경의 제약을 확인하세요.

| 명령 | 확인하는 범위 | 성공해도 알 수 없는 것 |
| --- | --- | --- |
| `ouroboros doctor install` | 패키지, 플러그인 및 MCP 설치 표면과 launcher | 호스트의 실제 연결이나 작업 성공 |
| `ouroboros status health` | 설정, DB 경로, 런타임 및 자격증명 존재 관련 검사 | 인증 유효성, 모델 호출이나 실제 실행 성공 |
| `ouroboros mcp doctor` | MCP 서버 실행 전 환경 검사. 기본 명령은 서버를 시작하지 않음 | 실제 호스트 연결이나 모델 호출 |
| `ouroboros mcp doctor-runtime` | 제한된 실행 파일 경로, loopback 바인딩 및 자체 서버 등록 정보 | 호스트와 서버 사이의 실제 연결 |
| `ouroboros codex doctor` | Codex의 `ooo auto` 규칙·스킬·서버 설정 | 실제 호스트 연결이나 모델 호출 |

`doctor install`, `mcp doctor`, `mcp doctor-runtime`은 `--json`을 지원합니다. `mcp doctor --machine-snapshot --json`은 기본 JSON 배열 대신 `checks`와 `machine_snapshot` 객체를 반환합니다. 실행 환경 정보가 출력되므로 JSON도 공유 전에 가립니다. `status health`에서 설정 오류와 다른 행의 `ok`가 함께 나와도 전체 설정이 유효하다는 뜻은 아닙니다. 검사와 종료 코드는 [설치 진단](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/doctor.py), [MCP 진단](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/mcp_doctor.py), [health 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/status.py)을 기준으로 합니다.

### MCP 연결 실패: 도구가 보이지 않을 때 {#mcp}

1. 호스트에서 해당 플러그인과 서버가 활성화됐는지, 오류가 연결 실패인지 도구 미발견인지 확인합니다. 독립 CLI의 정상 출력만으로 호스트 서버의 판본과 연결을 판단하지 않습니다.
2. 독립 CLI가 있으면 `ouroboros mcp doctor`의 실패 행을 살펴봅니다. 실패가 없더라도 호스트 설정과 인증이 맞는지는 별도입니다. Codex에서는 `ouroboros codex doctor`로 auto dispatch 설정을 확인할 수 있습니다.
3. 추가 확인이 필요하면 선택적 `ouroboros mcp doctor --probe-local-stdio`는 임시 자식 서버의 시작과 도구 발견을 검사합니다. 실제 호스트의 launcher나 모델 호출을 검사하지 않습니다. Python 수준 제한은 OS 격리가 아니며 일반 doctor 검사도 오프라인을 보장하지 않습니다. `ouroboros codex doctor --live-mcp`는 **설정된 stdio 서버를 실제로 시작**하므로 그 명령과 외부 효과를 먼저 확인하세요. URL 전송은 이 live 검사 대상이 아닙니다. [Codex 진단 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/codex.py).
4. 수정이 필요하면 변경 대상과 영향을 확인한 뒤 조치하고 같은 호스트에서 다시 연결을 확인합니다. `No runtimes found.`라면 setup을 무작정 반복하지 말고 해당 프로세스의 런타임 실행 파일·설정·도움말을 확인하세요. setup이 실패했어도 로컬 상태가 생성됐을 수 있습니다. [setup 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py).
5. Python `MCPClientAdapter` 경로는 SDK 예외 문자열에 `not found`가 있으면 도구 미발견으로 오분류할 수 있습니다. 후보 dev 오프라인 서버를 실제 도구 목록과 대조하고 독립 MCP SDK 호출로 확인한 한 사례에서는 등록된 `ouroboros_job_result`에 존재하지 않는 합성 job ID를 전달했을 때 `Job handle not found` 예외가 `Tool not found: ouroboros_job_result`로 표시됐습니다. 이는 Python adapter 경로의 해당 예외 분류이며 모든 호스트나 SDK에 일반화하지 마세요. 같은 호스트의 같은 서버가 연결됐는지, 서버의 실제 등록 tool 목록에 요청 tool이 있는지 확인하고, 정확한 job ID를 원래 시작 응답과 대조하세요. 원본 structured error와 관련 버전 정보를 보존하되 비밀값·전체 환경 설정·민감한 payload는 공유하지 마세요. [main `MCPClientAdapter`](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/client/adapter.py#L408-L412) · [release `v0.59.9`](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/client/adapter.py#L408-L412).

**Native Windows Codex Desktop 예외:** 기준 main과 release `v0.59.9` 모두 setup의 `auto` 모드가 기존 MCP 항목을 보존하거나 새 영구 항목 등록을 건너뛰면서 성공을 반환할 수 있습니다. 실제 Codex 설정의 Ouroboros 항목과 호스트 도구 목록을 확인하세요. setup 성공만으로 등록이나 연결을 증명할 수 없습니다. 설정 파일 전체를 공유하지 말고 해당 항목만 확인한 뒤 경로·인자를 가리세요. 별도 loopback HTTP 방식을 쓰려면 설치된 `ouroboros setup --help`와 변경 대상을 먼저 확인하고, 사용자가 승인한 설정 변경 범위 안에서만 `ouroboros setup --runtime codex --mcp-mode http`를 실행하세요. setup은 별도 실행할 서버 명령을 출력합니다. 그 명령을 직접 시작한 뒤 Codex를 열어야 하며, 등록 주소는 `http://127.0.0.1:8765/mcp`입니다. Windows에서 stdio를 사용할 때는 WSL 2의 Codex CLI와 그 환경을 확인하세요. [main Windows 동작](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/windows_codex_mcp.py) · [release `v0.59.9`](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/windows_codex_mcp.py)

## Codex 권한과 격리 범위가 예상과 다를 때 {#permission-scope}

1. 먼저 원래 호스트 대화에서 `job_id`, `session_id`, `execution_id`와 실제 작업 소유자·현재 상태를 확인하세요. [작업 상태와 재개](#recovery)에 따라 같은 job의 상태와 결과를 조회하고, 응답이 없다는 이유로 재실행하거나 사용자가 소유한 세션을 임의로 종료하지 마세요.
2. 관련 job의 실제 worker 명령과 선택된 backend/runtime을 확인하세요. Codex의 `--sandbox workspace-write`는 작업 공간 쓰기를 허용하는 sandbox이고, `--dangerously-bypass-approvals-and-sandbox`는 Codex 승인과 sandbox를 모두 우회합니다. 기본 설정 이름만으로 실제 실행 권한을 단정하지 말고, 토큰이나 전체 환경·설정 파일을 출력하지 마세요.
3. 경로마다 다를 수 있습니다. `CodexCliRuntime` 자체에서 permission mode를 지정하지 않은 경우 기본은 `acceptEdits`이며 `workspace-write`로 매핑됩니다. 이 기본값이 모든 내부 실행에 적용되는 것은 아닙니다. `use_case="interview"`에 명시 permission이 없으면 Codex interview factory가 질문 생성 경로에 bypass를 선택할 수 있습니다. Orchestrator task runner는 실행 중 전달된 adapter permission mode를 `bypassPermissions`로 덮어쓸 수 있습니다. 조건이 맞는 cross-harness 재시도와 일부 pytest 수집 오류 수정 경로도 별도로 bypass를 지정합니다. 따라서 하나의 Codex 설정이 중첩된 실행·재시도까지 모두 제한한다고 가정하지 마세요. 이 동작은 Ouroboros 공개 release `0.59.9`와 제품 기준 main `592c667`의 소스에서 확인했습니다.
4. 실제로 적용된 호스트 OS 격리도 확인하세요. 프로세스 namespace, 보이는 파일 시스템과 쓰기 가능한 경로, 네트워크 egress 범위를 현재 작업의 증거로 판단합니다. Codex sandbox 우회 flag가 보이면 Codex 설정만으로 OS 격리가 된다고 간주하지 마세요.
5. job 소유자와 현재 프로세스가 확인되지 않으면 작업 파일·브랜치와 외부 효과를 보존하고 사용자 세션을 종료하거나 인증·설정을 바꾸지 마세요. 정지나 취소가 필요하면 대상 job과 소유 프로세스를 먼저 특정하고 이미 발생한 효과를 확인하세요.
6. `model_tier=small`은 시작 tier 요청이지 실제 모델 적용이나 비용·토큰·모델 요청 횟수 상한을 보장하지 않습니다. 적용 여부와 실제 모델은 명시 model pin, router 활성 조건, runtime의 native model override 지원에 따라 달라질 수 있고, 역할별 별도 호출이 생길 수도 있습니다. 재시도·tier escalation도 더 높은 tier나 추가 세션을 만들 수 있으므로, 가능한 경우 실제 job/session의 모델·토큰·비용 기록을 확인하세요. 사용량 근거가 없으면 불명으로 보고하고 확인을 위해 반복 실행하지 마세요.

근거: main `592c667`의 [Codex factory](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/factory.py#L113-L143), [Codex runtime 기본값](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/codex_cli_runtime.py#L479-L492), [Codex flag 매핑](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/codex_permissions.py#L26-L50), [runner의 강제 모드와 adapter 덮어쓰기](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L731-L732) · [덮어쓰기 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/runner.py#L5190-L5217), [cross-harness 재시도](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/parallel_executor.py#L7068-L7074), [pytest 수집 오류 수정](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/server/adapter.py#L2147-L2159), [model tier 매핑](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L124-L180), [router activation conditions](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L381-L428), [선택 tier의 실제 적용 여부](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/model_routing.py#L503-L541). release **0.59.9**의 같은 근거는 [factory](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/factory.py#L113-L143), [runtime 기본값](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/codex_cli_runtime.py#L479-L492), [flag 매핑](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/codex_permissions.py#L26-L50), [runner 강제 모드](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/runner.py#L731-L732) · [adapter 덮어쓰기 구현](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/runner.py#L5190-L5217), [cross-harness](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/parallel_executor.py#L7052-L7057), [validation](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/server/adapter.py#L2147-L2159), [tier routing](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/model_routing.py#L124-L180), [router activation conditions](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/model_routing.py#L381-L428), [선택 tier의 실제 적용 여부](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/model_routing.py#L503-L541).

## 작업 상태와 재개 {#recovery}

연결이 끊겼다고 기존 작업이 중단됐다고 단정하지 마세요. 원래 호스트 대화의 시작 도구와 실제 반환 필드명을 먼저 확인하고, `job_id`, `session_id`, `execution_id`, `auto_session_id`를 구분하세요. `session_id`라는 필드명만으로 실행 세션이라고 단정할 수 없습니다. Interview MCP 시작 응답의 `session_id`는 `state.interview_id`이며, 오케스트레이터 실행 세션과 다른 ID입니다. 아래 실행 세션 명령에 넣지 마세요. `ouroboros status run --session-id`와 `ouroboros_session_status`는 오케스트레이터 세션 조회용입니다. [main Interview 시작 응답](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py#L2661-L2713) · [main 상태 조회 범위](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py#L291-L323) · [main 세션 재구성 조건](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/session.py#L1298-L1342) · [CLI run 상태 옵션](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/status.py#L374-L389). 같은 범위는 release `v0.59.9`에서도 대조했습니다([Interview 응답](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/authoring_handlers.py#L2686-L2738), [상태 조회](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/query_handlers.py#L291-L323), [재구성 조건](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/session.py#L1298-L1342), [CLI 옵션](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/status.py#L374-L389)).

```bash
ouroboros job status JOB_ID
ouroboros job result JOB_ID
ouroboros status execution EXECUTION_ID --events
ouroboros status run --session-id ORCHESTRATOR_SESSION_ID
ouroboros status auto AUTO_SESSION_ID
ouroboros resume --list
ouroboros resume --all --list
```

Interview를 이어가려면 원래 호스트/MCP에서 같은 `session_id`를 `ouroboros_interview`에 전달하고 사용자가 실제로 답한 내용을 `answer`로 보냅니다. 이 호출은 상태만 읽는 조회가 아니며 다음 질문 생성 등으로 모델 호출과 비용이 생길 수 있습니다. 독립 CLI의 인터뷰라면 **원래와 같은 상태 디렉터리**에서 `ouroboros init list`로 ID를 찾고 `ouroboros init start --resume INTERVIEW_ID`로 이어갑니다. `--state-dir`를 사용했다면 두 명령 모두 같은 경로를 지정하세요. `ouroboros resume --list`는 실행 세션 목록이지 인터뷰 목록이 아닙니다. 호스트 위임 응답이 `delegated_to_subagent`라면 receipt의 ID를 쓰지 말고 원래 호스트의 Task pane에서 실제 반환된 ID를 확인하세요. [main Interview continuation](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/authoring_handlers.py#L2280-L2305) · [main CLI 인터뷰 resume/list](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py#L1028-L1034) · [목록과 state-dir](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py#L1212-L1246). 동일 동작은 release `v0.59.9`의 [Interview continuation](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/mcp/tools/authoring_handlers.py#L2263-L2324) 및 [CLI 목록/resume](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/init.py#L1028-L1034)에서도 확인했습니다.

`ouroboros init start --resume INTERVIEW_ID`도 상태 조회만 하는 명령은 아닙니다. 인터뷰를 이어가며 질문·평가에 모델을 호출하고 비용이 생기거나 저장된 인터뷰 상태를 갱신할 수 있습니다. 진행에 따라 `Proceed to generate Seed specification?` 질문의 기본값은 `yes`이고, Seed를 만들면 뒤이어 `Start workflow now?`도 기본값 `yes`로 실제 workflow 실행을 시작할 수 있습니다. Seed를 검토한 뒤 실행하려면 `Start workflow now?`에서 기본값을 받아들이지 말고 `n`을 입력하세요. Seed 생성도 원하지 않으면 앞의 Seed 확인 질문에서 `n`을 선택합니다. [main 인터뷰/Seed/실행 흐름](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py#L560-L654) · [main Seed 저장과 실행 handoff](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py#L748-L812) · [release 흐름](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/init.py#L559-L653) · [release Seed 저장과 실행 handoff](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/init.py#L748-L812).

`job result`는 같은 실제 ID의 종료 출력이며, 성공한 작업뿐 아니라 `failed`, `cancelled`, `interrupted` 결과도 읽습니다. 상태·오류 필드와 반환된 실패 텍스트/페이로드를 작업 결과의 증거로 확인하세요. 조회 성공은 기록을 읽었다는 뜻이지 작업이 완료 조건을 통과했다는 뜻은 아닙니다. 기준 main 소스의 `worker_blocked`는 워커 판정 클래스에서 파생된 제한된 실패 범주이며, 그 자체로 실제 원인을 특정하지 않습니다. 결과와 연결된 세션·실행 ID, 워커의 관련 출력을 확인한 뒤에만 원인을 판단하세요. 소유 호스트에서 확인할 수 있다면 관련 stdout/stderr, 권한 오류, 선택된 backend/runtime 및 환경 오류를 필요한 범위에서 살펴보고, 공유 전 토큰·키·자격 증명과 무관한 환경값을 가리세요. job result가 원시 stdout/stderr를 항상 보존한다고 소스가 보장하지는 않습니다. 기존 작업 폴더·브랜치·미커밋 파일과 외부 효과를 보존하고, 소유자나 현재 상태가 불확실한 동안 재실행·재개·취소·중복 시작을 하지 마세요. `resume --list`는 실행 세션 후보 목록이며 인터뷰 목록이나 실제 재개가 아닙니다. 목록은 제한되거나 기록 재구성에 실패한 항목을 놓칠 수 있으므로 빈 결과를 작업 부재의 증거로 삼지 마세요. DB 열기 오류는 이력 없음과 다릅니다. [job 결과·상태 의미](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py), [워커 실패 범주](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/run_failure_cause.py), [상태 조회 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/status.py), [재개 목록 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/resume.py). 기준 소스는 `592c667` main이며 설치 릴리스와 호스트 연동은 다를 수 있습니다.

더 많은 실행 세션 후보를 보려면 `ouroboros resume --all --list`를 사용합니다. 정상적인 snapshot 경로에서는 기본 최근 20개 제한을 해제하지만, 재구성할 수 있는 `running` 또는 `paused` 세션 후보만 표시하고 재구성에 실패한 기록은 제외합니다. 오래된 EventStore의 fallback은 세션 이벤트를 다시 훑으면서 이 제한을 적용하지 않을 수 있으므로 `--all`을 추가해도 결과가 늘지 않을 수 있습니다. 어느 목록도 워커 프로세스가 현재 살아 있음, 전체 과거 이력, 작업 재개를 보장하지 않습니다. 설치된 도움말을 확인하고 이미 알고 있는 작업은 원래 ID로 따로 조회하세요. 이 동작은 기준 main과 release `v0.59.9`에서 확인했습니다: [main resume 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/resume.py) · [release `v0.59.9`](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/resume.py).

재개·취소·새 실행 전에는 기존 소유자와 최종 상태, Seed **파일 경로**, 작업 폴더·브랜치, 미커밋 파일 및 이미 발생한 외부 효과를 확인합니다. 응답이 사라진 것만으로 새 실행을 만들지 마세요. 이 기준 소스에서 `run workflow --resume`은 프로세스에만 있던 check package를 복구하지 못하는 특정 경우 이전 세션을 실패로 기록한 뒤 새 시도를 시작할 수 있습니다. 현재 설치의 동작과 대상 경로를 확인하고 선택하세요. 취소가 이미 발생한 외부 효과를 되돌리는 것도 아닙니다. [실행 재개 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py), [복구 안내](/docs/recovery-detail/).

## 업데이트가 부분 실패했을 때 {#update}

`ouroboros update --check`는 원격 배포 정보를 조회하므로 오프라인 검사가 아닙니다. 갱신 전 설치 관리자, 실제 실행 파일, 선택된 호스트와 진행 중인 작업을 확인하세요. 설정·플러그인 refresh는 파일을 바꿀 수 있습니다.

`Ouroboros partially updated`가 나오면 패키지는 이미 바뀌었을 수 있습니다. 같은 환경의 `ouroboros --version`과 출력된 실패 단계·복구 안내를 확인하고, 필요한 조치의 대상을 살핀 뒤 수행하세요. 이 소스에서는 이미 최신 상태에서 `ouroboros update`를 다시 실행해도 실패한 런타임 refresh를 자동 재시도하지 않습니다. 기존 설정을 삭제하거나 덮어써 오류를 숨기지 마세요. [업데이트 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/update.py), [상세 안내](/docs/update-detail/).

## 결과 확인과 인계 {#verify}

조치 후에는 같은 기기·호스트·설치에서 원래 증상을 다시 확인합니다. 실행 결과는 Seed 목표와 완료 조건, 실제 변경 파일, 테스트·평가의 출력 및 남은 실패와 대조합니다. job ID, health의 `ok`, 조회 성공, 실행 완료 표시 또는 평가 요청 자체는 요구 충족의 증거가 아닙니다. 모델 호출이나 실제 클라이언트 연결을 별도 시험하지 않았다면 그렇게 밝힙니다.

AI는 가린 오류와 판본, 확인한 ID 종류, 실제 수행한 검사와 결과, 변경 사항, 남은 불확실성 및 복구에 필요한 정보를 사용자에게 전달하세요. 상태나 외부 효과를 특정할 수 없다면 기록을 보존하고 임의로 재실행하지 않습니다. 더 자세한 흐름은 [진행상태](/docs/progress-detail/), [실패 복구](/docs/recovery-detail/), [진단 명령](/docs/diagnostics-detail/)을 참고하세요. 이 연결 페이지는 별도 판본 범위를 표시하므로 해당 표시를 함께 확인하세요.
