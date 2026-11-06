# 첫 작업 시작하기

설치 경로를 선택하고 **할 일을 추가하고 완료 표시하는 간단한 웹앱**을 목표로 Interview부터 결과 확인까지 살펴봅니다. 이 목표는 기존 [한국어 가이드의 연속 예제](https://ouroboros.page/learn/interview/)와 이어집니다.

이 안내는 제품 소스 [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 [설치 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 대조한 초안입니다. 공개 릴리스 `0.59.9`, 기존 가이드 0.51.5, 설치한 플러그인과 MCP 서버가 이 소스와 동일하다고 가정하지 마세요. 아래 흐름 전체를 실제 모델과 모든 호스트에서 실행해 검증하지 않았습니다. 화면과 질문은 버전·환경·답변에 따라 달라집니다.

## 시작하기 전에

- 인터넷 연결, 선택한 호스트 또는 Python 환경, 사용할 모델의 인증과 비용 조건을 확인합니다. 모델 호출은 시간과 비용이 들 수 있습니다.
- 실행은 파일을 만들거나 수정하고 명령을 실행할 수 있습니다. 첫 실습에는 기존 작업과 분리된 새 폴더를 사용하고 해당 폴더를 호스트에서 엽니다.
- 설치·설정은 패키지나 설정 파일을 변경할 수 있습니다. 제시되는 선택을 읽고 진행하세요. 사용 통계 설정은 설치한 버전과 서버 프로세스에 적용되는지 [설정 안내](/docs/config-reference-detail/)에서 확인하세요.

## 1. 설치 경로 고르기

| 사용하는 환경 | 준비와 설치 입력 위치 | 첫 작업 입력 위치 |
| --- | --- | --- |
| Claude Code 플러그인 | Claude Code와 `uv`가 필요합니다. 아래 설치 명령은 **터미널**에 입력합니다. | 새 Claude Code 세션의 대화 |
| Codex 플러그인 | 로그인된 Codex CLI와 `uvx`가 필요합니다. 아래 설치 명령은 **터미널**에 입력합니다. | 새 Codex 세션의 대화 |
| 독립 CLI | Python 3.12 이상과 사용할 런타임·인증이 필요합니다. 별도 가상환경에서 설치합니다. | **터미널** |

### Claude Code

터미널에서:

```bash
claude plugin marketplace add Q00/ouroboros
claude plugin install ouroboros@ouroboros
```

### Codex

터미널에서:

```bash
codex plugin marketplace add Q00/ouroboros
codex plugin add ouroboros@ouroboros
```

### 독립 CLI

처음 설치한다면 새 가상환경을 만들고 활성화해야 합니다. [독립 CLI 가상환경 안내](/docs/first-run-detail/#cli-venv)에 새 디렉터리 생성, 설치, 활성화와 확인 명령이 있습니다. 이 링크는 한국어 안내이며 제품 소스 `722172ef` 기준입니다. 이 quickstart의 `592c667f` 및 현재 공개 패키지와 판본이 다를 수 있으므로 설치된 버전의 도움말을 확인하세요.

가상환경을 활성화한 터미널에서:

```bash
python -m pip install ouroboros-ai
ouroboros --version
```

설치된 CLI와 인증 상태에 맞춰 런타임을 명시적으로 선택하세요. Claude Code CLI를 이미 설치하고 인증해 사용할 준비가 되었다면:

```bash
ouroboros setup --runtime claude-cli
```

Codex CLI를 이미 설치하고 인증해 사용할 준비가 되었다면:

```bash
ouroboros setup --runtime codex
```

아직 사용할 CLI가 없거나 인증하지 않았다면 먼저 해당 런타임을 설치하고 인증한 뒤 맞는 선택지를 사용하세요. 둘 다 설치되어 있다면 실제로 사용할 런타임을 고릅니다. 감지된 런타임이 하나뿐이면 인자 없는 `ouroboros setup`은 그것을 자동 선택합니다. 그 하나가 Claude Code CLI라면 `claude` SDK 경로를 선택합니다. 여러 런타임이 감지되면 대화형 setup은 선택을 묻습니다. 무인 모드에서는 감지된 후보 중 기존 설정이 있으면 유지하고, 그렇지 않으면 `claude`가 감지될 때 SDK 경로를 우선하며 그 외에는 첫 후보를 선택합니다. 기본 `ouroboros-ai` 패키지에는 Claude Agent SDK가 포함되지 않아 worker 사전 확인 단계에서 막힐 수 있습니다. Python SDK 경로가 목적이라면 설치한 버전의 SDK extra와 전제 조건을 먼저 확인하세요: [setup 런타임 선택](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/setup.py#L4806-L4861), [Claude 런타임 설정](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/claude_setup.py#L27-L64), [SDK 사전 확인](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/orchestrator/adapter.py#L1201-L1215), [`claude` 및 `claude-sdk` extras](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/pyproject.toml#L74-L82). 이 동작은 인용한 `592c667f` 소스 기준이므로 설치 버전의 도움말과 안내도 확인하세요.

`pip install`은 이 문서의 Git 커밋을 고정하지 않습니다. `ouroboros --version`은 해당 터미널의 CLI 패키지를 나타내며 호스트가 별도로 실행하는 서버의 버전은 확인하지 않습니다. 설정 결과와 사용할 런타임을 확인하세요. 다른 설치 경로와 세부 전제는 [제품 설치 안내](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/getting-started.md)를 참고하세요.

## 2. 목표를 이야기하고 Seed 검토하기

**플러그인:** 새 Claude Code 또는 Codex 세션에서 작업 폴더를 열고, 호스트 **대화에** 입력합니다.

```text
ooo setup
ooo interview "오늘 할 일을 추가하고 완료 표시할 수 있는 간단한 웹앱"
```

**독립 CLI:** 작업 폴더의 **터미널에** 입력합니다.

```bash
ouroboros init start "오늘 할 일을 추가하고 완료 표시할 수 있는 간단한 웹앱"
```

Interview가 저장 방식이나 완료 처리처럼 결정이 필요한 점을 질문하면 답합니다. 예를 들어 새로고침 뒤에도 할 일이 남아야 하는지 정할 수 있습니다. 이 문장의 질문은 **설명용 예시**이며 실제 출력이 아닙니다.

Seed는 목표·제약·완료 조건을 정리한 명세입니다. 아래는 경로별로 실제 Seed를 확인하는 방법입니다.

### 플러그인 대화에서 Seed 만들기

위 소스의 Interview 스킬은 질문과 검토를 마친 뒤 목표를 다시 확인하고 Seed 생성을 제안합니다. **Interview가 끝났다는 사실만으로 Seed가 자동 생성됐다고 가정하지 마세요.** 목표 확인에 동의한 뒤 같은 대화에서 `ooo seed`를 요청합니다. 인터뷰 세션 ID를 받았다면 필요할 때 `ooo seed <실제 세션 ID>`로 대상을 지정할 수 있습니다.

정상 생성 시 확인할 것은 완료 문구만이 아니라 **전체 Seed YAML**입니다. 목표, 작업 대상, 제약과 검증 가능한 완료 조건을 읽고 대화에서 합의한 내용과 비교하세요. 스킬은 QA 의견을 함께 제시하지만 점수만으로 내용이 맞다고 판단하지 않습니다. YAML 또는 실제 저장 경로를 확인하지 못했거나 생성이 실패·중단됐다면 실행하지 말고, 같은 세션에서 생성을 다시 요청하거나 복구 안내를 확인하세요. 경로가 표시되지 않으면 파일이 저장됐다고 추측하지 말고 호스트에 Seed 내용과 저장 여부를 확인합니다.

MCP 서버를 사용할 수 없으면 스킬은 대화의 확인된 요구로 Seed를 작성하는 대체 경로를 사용하며, 서버 연결을 위한 설정을 안내할 수 있습니다. 이 경우에도 실제 제시된 YAML을 확인하고 생성 여부를 구분합니다. Claude Code와 Codex 모두 위 제품 안내에서 플러그인 경로를 제공하지만, 실제 화면과 스킬 호출 방식은 설치한 호스트·버전에 따라 확인해야 합니다. [Interview 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/interview/SKILL.md) · [Seed 스킬](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/skills/seed/SKILL.md)

### 독립 CLI에서 Seed 확인하기

터미널의 대화형 Interview는 Seed 생성 여부를 묻습니다. 생성을 승인하고 출력된 실제 Seed 파일 경로와 내용을 확인하세요. `Start workflow now?`가 나오면 기본값은 예입니다. 실행 전에 검토하려면 `n`을 선택합니다. 생성이 실패하거나 중단되면 파일이 있다고 가정하지 마세요. 이 동작은 위 소스 기준이며 설치된 버전의 화면을 확인하세요.

## 3. 실행하고 결과 확인하기

플러그인 대화에서는 검토한 Seed YAML 또는 실제 파일 경로를 지정해 `ooo run`을 요청합니다. 독립 CLI에서는 실제 생성 경로를 사용해 터미널에서 `ouroboros run <Seed 파일 경로>`를 실행합니다. 꺾쇠 괄호를 포함한 예시 경로를 그대로 입력하지 마세요. 실행은 코드와 파일을 변경하고 명령 및 모델 호출을 시작할 수 있습니다.

플러그인의 백그라운드 실행은 기본적으로 별도 worktree를 사용하지만, 실제로 격리됐는지는 결과에 `worktree_path`와 `worktree_branch`가 있는지 확인하세요. 다른 실행 방식은 다를 수 있습니다. 완료 후 기본적으로 정식 평가가 시작되며, 거부되면 제한된 Ralph 반복이 이어질 수 있어 추가 시간과 모델 비용이 들 수 있습니다. 상태와 최종 결과를 확인하세요.

진행 중에는 실제로 반환된 ID와 상태를 기록합니다. 완료 표시나 ID만으로 요구가 충족됐다고 판단하지 말고 다음을 확인하세요.

1. 실행 결과에 보고된 실제 작업 폴더 또는 worktree에서 생성·변경된 파일을 살펴봅니다.
2. 테스트와 평가 결과를 읽고 실패 또는 미검증 항목을 확인합니다.
3. 앱 실행 정보가 아직 없다면 아래 요청 예시처럼 실제 작업 경로에서 시작 방법을 확인합니다. 답변의 명령과 출처, 포트·비용을 살펴 신뢰할 수 있는 방법을 선택한 뒤 앱을 열어 할 일을 추가하고 완료 표시합니다. Seed에 저장 조건이 있다면 새로고침 후에도 만족하는지 직접 확인합니다.

**독립 CLI 사용자:** 실제 생성 작업 경로에서 `README`와 프로젝트의 패키지 설정 파일을 직접 살펴 의존성 설치 방법, 시작 스크립트, URL·포트와 종료 방법을 확인하세요. 파일에 정보가 없거나 실행 방법을 판단할 수 없다면 이를 추측하지 말고, Claude Code 또는 Codex처럼 제품이 지원하는 플러그인 호스트에서 아래 요청 예시를 사용해 확인하세요.

실제 실행 결과에 표시된 작업 경로 또는 `worktree_path`에서 호스트 에이전트에게 다음처럼 요청할 수 있습니다. 이는 **자연어 요청 예시**이며, 특정 기술 스택·명령·URL이나 검증된 실행 결과를 뜻하지 않습니다.

```text
현재 작업 경로 <실제 작업 경로>의 프로젝트를 살펴보고, 필요한 의존성 설치 명령과 출처, 앱 시작 명령, 실제 접속 URL과 포트, 종료 방법 및 예상 비용을 알려 주세요. 실행 명령과 출처를 확인해 신뢰할 수 있는 방법을 선택한 뒤, 제가 직접 앱을 열어 할 일 추가와 완료 표시를 확인하겠습니다.
```

이 안내만으로 실제 앱 실행은 검증되지 않습니다. 답변이 프로젝트 내용과 실행 환경에 맞는지, 명령·출처를 신뢰할 수 있는지와 포트·비용을 검토한 뒤 진행하세요.

평가가 시작되지 않았거나 실패했거나 결과가 `unverified`라면, 먼저 실제 `session_id`, 원래 Seed, 산출물과 반환된 작업 경로 또는 `worktree_path`를 대조합니다. 이미 평가 job이나 연결된 Ralph job이 있으면 상태와 결과를 확인하고 중복 시작하지 마세요. **연결된 MCP를 사용하는 플러그인 호스트 대화**라면 새 평가가 필요한 경우에 호스트에 `ooo evaluate <실제 session ID> [산출물]`을 요청하고 실제 프로젝트 경로를 알려주세요. `auto_evolve: false`는 이번 평가에서 새 Ralph 후속을 예약하지 않게 할 뿐, 이미 시작된 평가나 chain을 취소하지 않습니다. **독립 CLI 터미널에는 이 호스트 명령을 입력하지 마세요.** 고정 소스 `592c667f`의 CLI에는 별도 평가 재실행 명령이 확인되지 않았습니다. 설치 버전의 `ouroboros --help`와 버전별 안내를 확인하고, 지원 경로를 찾지 못하면 호스트와 MCP가 연결된 경로를 사용하세요. `unverified`는 승인이 아닙니다. 실행 가능한 검사를 추가하거나 확인한 뒤, 결과별 다음 행동은 [평가 상세 안내](/docs/evaluation-evolution-detail/)에서 확인하세요.

상태 조회는 ID의 종류에 따라 다릅니다. [진행 상태](/docs/progress-detail/)에서 받은 ID에 맞는 경로를 확인하세요. 연결 실패나 중단이 생기면 기존 기록을 보존하고 [복구 안내](/docs/recovery-detail/)를 먼저 읽으세요. 작업이 아직 실행 중일 수 있으므로 곧바로 다시 시작하지 않습니다.

다음으로 [Interview 안내](/docs/interview-guide/), [Seed 형식](/docs/seed-guide/), [기존 프로젝트 적용](/docs/existing-project-detail/)을 살펴볼 수 있습니다.
