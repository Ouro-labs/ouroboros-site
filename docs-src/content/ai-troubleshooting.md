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

## 작업 상태와 재개 {#recovery}

연결이 끊겼다고 기존 작업이 중단됐다고 단정하지 마세요. 원래 호스트 대화와 시작 응답에서 실제 `job_id`, `session_id`, `execution_id`, `auto_session_id`를 구분하고 작업 폴더와 소유 프로세스를 확인합니다. 독립 CLI의 예시는 다음과 같습니다. 대문자 자리에 **해당 종류의 실제 ID**를 넣고 설치된 도움말을 먼저 확인하세요.

```bash
ouroboros job status JOB_ID
ouroboros job result JOB_ID
ouroboros status execution EXECUTION_ID --events
ouroboros status auto AUTO_SESSION_ID
ouroboros resume --list
```

`job result`는 종료된 작업의 결과를 확인할 때 사용합니다. `resume --list`는 목록 조회이며 실제 재개가 아닙니다. 목록은 제한되거나 기록 재구성에 실패한 항목을 놓칠 수 있으므로 빈 결과를 작업 부재의 증거로 삼지 마세요. DB 열기 오류는 이력 없음과 다릅니다. 조회 명령의 종료 성공도 **조회 성공**이지 실행 성공이나 현재 프로세스 생존을 증명하지 않습니다. [상태 조회 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/status.py), [재개 목록 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/resume.py).

재개·취소·새 실행 전에는 기존 소유자와 최종 상태, Seed **파일 경로**, 작업 폴더·브랜치, 미커밋 파일 및 이미 발생한 외부 효과를 확인합니다. 응답이 사라진 것만으로 새 실행을 만들지 마세요. 이 기준 소스에서 `run workflow --resume`은 프로세스에만 있던 check package를 복구하지 못하는 특정 경우 이전 세션을 실패로 기록한 뒤 새 시도를 시작할 수 있습니다. 현재 설치의 동작과 대상 경로를 확인하고 선택하세요. 취소가 이미 발생한 외부 효과를 되돌리는 것도 아닙니다. [실행 재개 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py), [복구 안내](/docs/recovery-detail/).

## 업데이트가 부분 실패했을 때 {#update}

`ouroboros update --check`는 원격 배포 정보를 조회하므로 오프라인 검사가 아닙니다. 갱신 전 설치 관리자, 실제 실행 파일, 선택된 호스트와 진행 중인 작업을 확인하세요. 설정·플러그인 refresh는 파일을 바꿀 수 있습니다.

`Ouroboros partially updated`가 나오면 패키지는 이미 바뀌었을 수 있습니다. 같은 환경의 `ouroboros --version`과 출력된 실패 단계·복구 안내를 확인하고, 필요한 조치의 대상을 살핀 뒤 수행하세요. 이 소스에서는 이미 최신 상태에서 `ouroboros update`를 다시 실행해도 실패한 런타임 refresh를 자동 재시도하지 않습니다. 기존 설정을 삭제하거나 덮어써 오류를 숨기지 마세요. [업데이트 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/update.py), [상세 안내](/docs/update-detail/).

## 결과 확인과 인계 {#verify}

조치 후에는 같은 기기·호스트·설치에서 원래 증상을 다시 확인합니다. 실행 결과는 Seed 목표와 완료 조건, 실제 변경 파일, 테스트·평가의 출력 및 남은 실패와 대조합니다. job ID, health의 `ok`, 조회 성공, 실행 완료 표시 또는 평가 요청 자체는 요구 충족의 증거가 아닙니다. 모델 호출이나 실제 클라이언트 연결을 별도 시험하지 않았다면 그렇게 밝힙니다.

AI는 가린 오류와 판본, 확인한 ID 종류, 실제 수행한 검사와 결과, 변경 사항, 남은 불확실성 및 복구에 필요한 정보를 사용자에게 전달하세요. 상태나 외부 효과를 특정할 수 없다면 기록을 보존하고 임의로 재실행하지 않습니다. 더 자세한 흐름은 [진행상태](/docs/progress-detail/), [실패 복구](/docs/recovery-detail/), [진단 명령](/docs/diagnostics-detail/)을 참고하세요. 이 연결 페이지는 별도 판본 범위를 표시하므로 해당 표시를 함께 확인하세요.
