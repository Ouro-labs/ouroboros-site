# CLI 하위 명령과 인자 상세 참조

!!! warning "판본과 검증 범위"
    아래 항목과 합성 관찰은 **고정 소스 `722172ef096767583679d04aef5e847458fee6b2`** 기준입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)이나 공개 패키지 `0.59.9`, 실행 중인 호스트 서버에 동일하게 적용된다고 가정하지 마세요. 설치된 CLI 도움말 또는 연결된 서버의 실제 스키마를 우선 확인합니다.

    **문자 인코딩:** main은 CLI가 실행 Seed YAML을 읽고, `init`의 PM Seed 선택 미리보기(`_display_pm_seed_info`: 이름·목표·PM ID 요약)에 표시할 값을 읽을 때 UTF-8을 명시합니다. 이는 `init`의 모든 Seed 읽기가 아니라 해당 미리보기 경로입니다. main의 사용자 정의 agent Markdown 로더도 UTF-8을 명시합니다. 반면 722와 확인한 `v0.59.9` 소스의 해당 세 경로는 플랫폼 기본 인코딩을 사용합니다. 따라서 비-UTF-8 기본 인코딩 환경에서 비ASCII Seed·PM Seed·agent Markdown은 main과 다르게 디코딩되거나 읽기 오류가 날 수 있습니다. 이는 소스에서 도출한 조건부 차이이며 실제 Windows 로캘·설정은 시험하지 않았습니다. Python UTF-8 mode가 기본 인코딩에 영향을 줄 수 있으므로 Windows 전체에 같은 결과라고 단정하지 마세요. 사용 전 설치된 버전과 `--help`, 파일의 실제 인코딩 및 해당 Python 프로세스의 기본 인코딩을 확인하고, 읽기 오류가 나면 파일을 보존한 채 원본 오류를 확인하세요. [main `run` Seed 로더](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/run.py#L182-L187) · [release `v0.59.9` `run` Seed 로더](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/run.py#L182-L187) · [main PM Seed 미리보기](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/init.py#L909-L920) · [release `v0.59.9` PM Seed 미리보기](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/init.py#L909-L920) · [main agent Markdown 로더](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/plugin/agents/registry.py#L336-L348) · [release `v0.59.9` agent Markdown 로더](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/plugin/agents/registry.py#L336-L348).

    이 비교는 확인한 소스 경로의 차이만 설명합니다. 의존 코드·설치물·런타임 전체의 동등성이나 실제 호스트 실행을 증명하지 않습니다. 현재 [CLI 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md), [설정 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/config-reference.md), [MCP 도구 소스](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools)를 함께 확인하세요. 전체 현재 CLI·MCP 스키마와 모든 설정 조합은 실사용으로 전수 검증하지 않았습니다.


기준: upstream `722172ef096767583679d04aef5e847458fee6b2`, 2026-11-04. 고정 소스의 Typer 명령 트리를 격리 Python에서 로드하여 자동 추출했다. 숨김 명령을 제외하며 옵션의 적용 조건·기본값·부작용은 [CLI 원본 참조](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md), 해당 명령 `--help`와 구현을 확인한다. 인자 이름과 타입은 선언된 표면이며 유효성 검사 전체를 뜻하지 않는다. `[OPTIONS]`에는 `--help`가 자동 포함된다. 각 명령의 영문 설명은 원본 help에서 발췌했으며, 별도 한국어 표와 주의 문구는 구현을 대조해 보완한 안내다. help와 보완 설명이 다르면 고정 소스의 호출 경로와 설치한 판본을 확인한다.

## 명령군 바로 찾기

이 색인은 길다. 작업을 시작하려면 [자동 실행](#ouroboros-auto), [Seed 생성](#ouroboros-seed), [인터뷰 시작](#ouroboros-init-start), [워크플로 실행](#ouroboros-run-workflow), [QA](#ouroboros-qa)를 확인한다. 기존 작업은 [job 조회](#ouroboros-job), [상태 조회](#ouroboros-status), [취소](#ouroboros-cancel), [재개](#ouroboros-resume)에서 찾는다.

운영과 확장은 [artifact](#ouroboros-artifacts), [설정](#ouroboros-config), [진단](#ouroboros-doctor), [MCP](#ouroboros-mcp), [설치·프로젝트 설정](#ouroboros-setup), [정리](#ouroboros-cleanup), [플러그인](#ouroboros-plugin), [업데이트](#ouroboros-update), [Workflow IR](#ouroboros-workflow-ir), [Zcode](#ouroboros-zcode)로 이동한다. 결정과 부작용을 먼저 살피려면 각 명령의 상세 안내와 아래의 선택표를 함께 읽는다.

## 설정·진단·정리: 선택 전 확인

아래 기본값과 부작용은 위 고정 판본의 구현 기준이다. 자세한 조건과 검증 범위는 연결된 안내를 확인한다. 이 표는 설치한 다른 버전의 동작을 보장하지 않는다.

| 명령과 선택 | 생략 시 기본 동작 / 상호작용 | 부작용과 확인할 점 |
| --- | --- | --- |
| `config [--web] [--host HOST] [--port PORT] [--no-browser]` | 웹 강제는 꺼져 있고 host는 `localhost`, port 생략 또는 `0`은 빈 포트를 고른다. 일반 TTY는 TUI지만 하네스 문맥에서는 웹을 선택할 수 있다. | GUI를 연다. `--web`은 웹을 강제하고 `--no-browser`는 자동 브라우저 열기를 막는다. host 변경 시 노출 범위를 별도 검토한다. [설정 화면](/docs/operations-detail/). |
| `config show [SECTION] [--json]` | 섹션과 JSON 생략 시 유효 설정을 텍스트로 표시한다. `--json`과 섹션을 함께 주면 이 판본은 섹션을 무시하고 전체 유효 설정을 출력한다. | 출력에 경로·설정값이 포함될 수 있다. 공유 전 검토한다. [설정 출력](/docs/operations-detail/). |
| `config init` / `config set KEY VALUE` / `config undo` | init은 없는 파일만 만든다. set은 키와 값을 필수로 받고 검증 후 저장한다. undo는 기존 백업과 현재 파일을 교환한다. | set은 YAML을 다시 쓰며 성공 시 자동 백업을 보장하지 않는다. undo의 백업이 직전 상태라는 보장도 없다. [설정 복구](/docs/operations-detail/). |
| `config backend [NEW_BACKEND]` | 인자 생략은 현재 backend 조회다. 인자 지정은 설정 과정에 위임한다. | 전환은 MCP 등록 등 여러 파일을 변경할 수 있고 일부 실패 시 전체가 원상 복구된다고 가정하지 않는다. [백엔드 전환](/docs/operations-detail/). |
| `mcp doctor [--json] [--machine-snapshot] [--probe-local-stdio]` | 세 옵션은 기본 꺼짐. `--json`만 쓰면 검사 결과 배열, snapshot도 쓰면 `checks`와 `machine_snapshot` 객체다. | snapshot은 선택적 메타데이터를 수집하며 출력에 경로가 들어갈 수 있다. stdio probe는 격리된 자식 서버를 시작한다. `fail` 행이 있으면 종료 1; 실제 모델 인증을 증명하지 않는다. [진단 범위](/docs/diagnostics-detail/). |
| `doctor install [--json]` / `mcp doctor-runtime [--json]` / `status health` | JSON 옵션은 기본 꺼져 있다. health는 별도 옵션을 설치 버전 도움말에서 확인한다. | 각 검사의 범위가 다르며 경고만으로 실패 종료하지 않을 수 있다. 출력에 환경 정보가 포함될 수 있으므로 공유 전 확인한다. [설치·런타임 진단](/docs/diagnostics-detail/). |
| `cleanup [--dry-run] [--force] [--state-all]` | 세 옵션 모두 기본 꺼져 있다. 기본 명령은 dry-run이 아니며 실제 제거한다. | `--dry-run`은 미리보기, `--force`는 깨끗한 미병합 worktree도 후보에 포함, `--state-all`은 blocked/failed 상태 파일도 포함한다. 후보·진행 중 작업과 보존 여부를 확인한다. 경고와 종료 0이 함께 나올 수 있다. [삭제 경계](/docs/cleanup-detail/). |

## `ouroboros`

Ouroboros - Self-Improving AI Workflow System

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--version / -V` | boolean | 아니요 | Show version and exit. |
| `--install-completion` | boolean | 아니요 | Install completion for the current shell. |
| `--show-completion` | boolean | 아니요 | Show completion for the current shell, to copy it or customize the installation. |

## `ouroboros auto`

Run bounded full-quality ooo auto pipeline. Detached auto background work is non-terminal tracked work. Wait for completion with: ouroboros job wait JOB_ID Retrieve completed results with: ouroboros job result JOB_ID

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `GOAL` | str | 아니요 | Goal/task for ooo auto. |
| `--resume` | str | 아니요 | Resume an auto session id. |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Runtime backend used by ooo auto. The same flag is applied to BOTH (a) interview/Seed authoring (in-process via the matching MCP authoring handler) AND (b) the run-handoff that dispatches the executor. The first interview question is generated in-process even when --runtime is set to a heavyweight backend like codex; see docs/auto-runtime-semantics.md. Supported values include claude, codex, opencode, hermes, gemini, copilot, kiro, pi, gjc, antigravity, grok, and zcode. |
| `--max-interview-rounds` | int range | 아니요 | Maximum auto interview rounds. Defaults to 50 for new sessions and to the persisted bound on resume; explicit values raise (never lower) the bound. The interview closes early once ambiguity converges or stagnation-driven lateral steps exhaust, so the cap is rarely reached. |
| `--max-repair-rounds` | int range | 아니요 | Maximum Seed repair rounds. Defaults to 5 for new sessions and to the persisted bound on resume; explicit values raise (never lower) the bound. |
| `--skip-run` | boolean | 아니요 | Stop after Seed creation; 실제 상태와 degraded 예외는 [Auto 안내](/docs/auto-detail/) 참조. |
| `--no-wait` | boolean | 아니요 | Fire-and-forget: return as soon as the execute run-handoff job is started instead of waiting for it to finish. WARNING: in direct CLI mode the in-process job dies with the CLI, so detached execution does NOT survive process exit unless a persistent owner (e.g. a running 'ouroboros mcp serve') holds it. Default off: auto waits for the run job to reach a terminal state and reports the verdict. |
| `--show-ledger` | boolean | 아니요 | Print assumptions and non-goals. |
| `--status` | boolean | 아니요 | Print persisted auto session status without running. |
| `--attach-execution` | str | 아니요 | Attach an externally verified execution id to an unknown run handoff. |
| `--attach-job` | str | 아니요 | Attach an externally verified job id. |
| `--attach-session` | str | 아니요 | Attach an externally verified run session id. |
| `--attach-source` | str | 아니요 | Source label for an attached run handle. |
| `--reconcile-run` | boolean | 아니요 | Try to reconcile an unknown run handoff without starting a duplicate run. |
| `--reconcile-source` | str | 아니요 | Source label for run handoff reconciliation. |
| `--quiet` | boolean | 아니요 | Suppress live phase/grade/repair progress lines; only the final summary prints. |
| `--timeout` | float | 아니요 | 신규 세션의 파이프라인 기한(기본 7200초, 60–86400). 기본 인계 대기에도 같은 예산이 적용된다. 기한 시 연결된 실행 완료 증거가 우선될 수 있고, 그렇지 않으면 job 취소를 **시도**한 뒤 차단·재개 가능 판정을 돌려준다. 취소는 best-effort이며 오류가 억제될 수 있으므로 help의 취소 문구만으로 실제 종료·외부 효과 부재를 보장하지 않는다. 재개 시 원래 기한이 유지되며 이 옵션을 다시 지정하면 거부된다. [Auto 인계](/docs/auto-detail/). |
| `--complete-product` | boolean | 아니요 | Deprecated and ignored. The run job now owns run -> evaluate -> ralph; follow it with 'ooo status' or the job tools instead. |
| `--requester-command` | str | 아니요 | Ask the requester instead of assuming: for each interview question auto would answer with a conservative default or an assumption, run this command (split like a shell, run without one) with a JSON question on stdin and use its stdout answer. Overrides OUROBOROS_AUTO_REQUESTER_COMMAND. Off by default. |
| `--requester-timeout` | float | 아니요 | Seconds to wait for one requester answer before keeping auto's draft (default 300). Overrides OUROBOROS_AUTO_REQUESTER_TIMEOUT_SECONDS. |

`--requester-command`는 신뢰한 외부 프로그램을 실제 실행하고 질문·목표·초안을 전달한다. 셸을 생략해도 격리되지는 않는다. 시간 초과 시 시작한 프로세스의 종료를 시도하지만 자손 프로세스와 외부 효과의 종료를 보장하지 않는다. 출력·실패 처리는 [Auto requester 경계](/docs/auto-detail/)를 확인한다.

## `ouroboros seed`

Generate a Seed YAML specification from an interview.

독립 CLI에서 생성 중 키보드 인터럽트는 종료 코드 0을 반환한다. 종료 코드만으로 생성 성공을 판정하지 말고 출력된 Seed 경로와 파일 내용을 확인한다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/seed.py).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SESSION_ID` | str | 예 | Interview session ID to crystallize into a Seed. |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |
| `--llm-backend` | choice: claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, omp, zcode, dsh, megacode | 아니요 | LLM backend for ambiguity scoring and seed generation (claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, zcode, or dsh). |

### Seed 생성 입력과 확인

| 입력 | 기본값·조건과 영향 |
| --- | --- |
| `SESSION_ID` | 완료(`completed`)된 인터뷰 ID가 필요하다. 불러오지 못하거나 완료되지 않은 상태면 종료 1이다. |
| `--state-dir` | 생략하면 `~/.ouroboros/data`; 지정하면 이미 존재하는 디렉터리여야 한다. |
| `--llm-backend` | 생략하면 어댑터 구성에 따른다. 지정하면 Seed 생성·모호성 점수에 해당 백엔드를 사용하며 모델 호출과 파일 생성이 일어날 수 있다. |
| 결과 확인 | 출력된 Seed 경로와 내용을 확인한다. 인터럽트는 종료 0이므로 코드만으로 성공을 판단하지 않는다. [인터뷰 복구](/docs/recovery-detail/), [Seed 형식](/docs/seed-format-detail/). |

## `ouroboros qa`

General-purpose QA verdict for any artifact.

이 CLI는 `ARTIFACT`, `--reference`, `--seed-content` 값이 존재하는 일반 파일일 때만 내용을 읽는다. 없는 경로나 디렉터리는 오류 대신 문자열 자체로 평가에 전달되므로, 경로 오타가 모델 호출과 잘못된 평가로 이어질 수 있다. 파일을 의도했다면 호출 전에 실제 경로와 내용을 확인한다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/qa.py).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `ARTIFACT` | str | 예 | Artifact text or path to a file to evaluate. |
| `--quality-bar / -q` | str | 아니요 | Natural-language description of what PASS means. |
| `--artifact-type / -t` | str | 아니요 | Artifact type: code, api_response, document, screenshot, test_output, custom. |
| `--reference / -r` | str | 아니요 | Optional reference text or path for comparison. |
| `--pass-threshold` | float range | 아니요 | Score threshold for PASS verdict. |
| `--qa-session-id` | str | 아니요 | Existing QA session ID for iterative checks. |
| `--seed-content` | str | 아니요 | Optional Seed YAML text or path for additional context. |

### QA 입력과 결과 해석

| 입력 또는 옵션 | 고정 판본의 기본값과 사용 시 주의 |
| --- | --- |
| `ARTIFACT` | 필수 문자열이다. 경로가 일반 파일이면 UTF-8 **텍스트**로 읽는다. `--artifact-type screenshot`을 지정해도 이 CLI가 이미지 바이너리를 디코딩하거나 시각 모델에 전달한다는 뜻은 아니다. 읽을 수 없는 파일·비UTF-8 내용은 파일 읽기 단계에서 실패할 수 있다. |
| `--quality-bar` | 기본은 정확성·완전성·내적 일관성·목적 적합성을 요구하는 일반 기준이다. 실제 업무의 수용 조건을 명시하는 편이 구체적인 판정에 도움이 된다. MCP 직접 호출에서는 이 인자가 필수다. |
| `--artifact-type` | 기본 `code`. 종류는 심사 프롬프트의 문맥을 고르며, 이 옵션만으로 실행·테스트·이미지 판독이 수행됐다는 증거가 되지 않는다. |
| `--reference`, `--seed-content` | 기본 없음. 각각 텍스트 또는 존재하는 일반 파일의 UTF-8 내용을 전달한다. 기준과 자료는 모델에 전달될 수 있으므로 비밀과 공유 범위를 먼저 검토한다. |
| `--pass-threshold` | 기본 `0.80`, 허용 범위 `0.0`–`1.0`. 점수 문턱이며 모델 평가의 정확성을 보장하지 않는다. |
| `--qa-session-id` | 기본은 새 `qa-...` ID. 같은 ID만 넘기는 것이 이전 평가 전체를 CLI 인자로 다시 보내는 것과 같지 않다. 반복 이력과 실제 입력의 차이는 [QA 안내](/docs/qa-detail/)를 본다. |

CLI는 핸들러 오류면 종료 코드 1, 결과의 `meta.passed`가 정확히 `false`면 2다. 그 외 종료 0은 모든 결과가 PASS라는 보장이 아니므로 표시된 판정과 메타데이터를 함께 확인한다. 이 경로는 모델 호출 또는 호스트 위임으로 이어질 수 있다. [CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/qa.py), [QA 핸들러](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/qa.py). 위 표는 고정 소스 대조이며 실제 모델·이미지 판독 시험은 하지 않았다.

## `ouroboros init`

Start interactive interview to refine requirements.

## `ouroboros init start`

Start an interactive interview to refine your requirements. This command initiates the Big Bang phase, which transforms vague ideas into clear, executable requirements through iterative questioning. Example: ouroboros init start "I want to build a task management CLI tool" ouroboros init start --orchestrator "Build a REST API" ouroboros init start --orchestrator --runtime codex "Build a REST API" ouroboros init start --llm-backend codex "Build a REST API" ouroboros init start --resume interview_20260116_120000 ouroboros init start --model frontier "Build a REST API" ouroboros init start

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `CONTEXT` | str | 아니요 | Initial context or idea (interactive prompt if not provided). |
| `--resume / -r` | str | 아니요 | Resume an existing interview by ID. |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |
| `--orchestrator / -o` | boolean | 아니요 | Use Claude Code (Max Plan) instead of LiteLLM. No API key required. |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Agent runtime backend for the workflow execution step after seed generation (claude, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, gjc, antigravity, grok, or zcode). |
| `--llm-backend` | choice: claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, omp, zcode, dsh, megacode | 아니요 | LLM backend for interview, ambiguity scoring, and seed generation (claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, zcode, or dsh). |
| `--debug / -d` | boolean | 아니요 | Show verbose logs including debug messages. |
| `--model / -m` | str | 아니요 | Model for every role in this command: auto (latest of each role's tier), frugal, standard, frontier, or a model id. Tier names work on every backend; Claude aliases such as opus only on Claude backends. Default: models.default in config. |
| `--pin-models / --no-pin-models` | boolean | 아니요 | Run the per-role model ids saved in config (research and reproducibility). Default: models.pin in config (off). |

### `init start` 선택과 우선순위

아래는 고정 소스의 선언과 호출 경로를 읽은 표다. 실제 모델·호스트 실행을 뜻하지 않는다. `--help`는 격리 HOME에서 옵션의 존재만 확인했다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/init.py), [첫 실행](/docs/first-run-detail/).

| 입력 | 생략 시 / 우선순위 | 사용 시 영향과 주의 |
| --- | --- | --- |
| `CONTEXT`, `--resume` | 둘 다 생략하면 아이디어를 질문한다. `--resume`이 있으면 새 context 입력·PM Seed 선택을 건너뛴다. | context가 제공돼도 개발 Seed가 없고 PM Seed가 있으면 대체할지 물을 수 있다. 재개 ID는 인터뷰 ID다. |
| `--state-dir` | `~/.ouroboros/data` | 명시 경로는 이미 존재하는 디렉터리여야 한다. 인터뷰 상태의 읽기·저장 위치다. |
| `--llm-backend`, `--orchestrator` | 명시 LLM backend > `--orchestrator`의 Claude Code 호환 선택 > 저장된 `llm.backend` | 인터뷰·모호성 평가·Seed 생성의 LLM 선택이다. 예전 help의 LiteLLM 고정 기본값으로 가정하지 않는다. |
| `--runtime` | 실행 런타임 설정에 맡김 | 생성한 Seed를 질문 후 실행할 때의 런타임이며 인터뷰 LLM을 바꾸지 않는다. 나중에 실행하는 경우 그 명령에서 따로 선택한다. |
| `--model`, `--pin-models` / `--no-pin-models` | 생략 시 저장된 `models.default`, `models.pin` 등 기존 모델 해석 규칙을 사용 | 명시 선택은 이 명령의 모델 해석과 자식 프로세스에 전달된다. 실제 모델 비용·접근 권한을 확인한다. |
| `--debug` | 꺼짐 | 상세 로그를 출력하므로 공유 전 민감 내용 포함 여부를 확인한다. |

Seed 생성 후 즉시 실행 질문에서 기본 답은 실행이다. 실행을 원하지 않으면 명시적으로 거절한다. Ctrl+C가 종료 코드 0인 경우가 있어 종료 코드만으로 완료를 판단하지 않는다.

## `ouroboros init list`

List all interview sessions.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |

## `ouroboros interview`

Start interactive interview to refine requirements.

고정 버전에서는 `interview`와 `init`이 같은 명령 그룹에 등록된다. 따라서 `interview start`와 `init start`의 입력·기본값·부작용은 [위의 start 표](#ouroboros-init-start)를 따르며, 표시된 영문 help 중 `--orchestrator` 설명만으로 실제 백엔드 우선순위를 판단하지 않는다. `interview list`와 `init list`도 같은 목록 동작을 사용한다. 기본 상태 위치는 `~/.ouroboros/data`, `--state-dir`은 기존 디렉터리여야 한다. 목록은 `interview_*.json` 중 유효한 상태만 갱신 시각 역순으로 보여주며 읽기·검증 오류가 난 파일은 건너뛰므로 빈 목록을 파일 부재로 확정하지 않는다. 손상 파일 보존과 합성 목록 시험은 [인터뷰 안내](/docs/interview-detail/)를 참조한다. [그룹 등록](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/main.py), [목록 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/bigbang/interview.py).

## `ouroboros interview start`

Start an interactive interview to refine your requirements. This command initiates the Big Bang phase, which transforms vague ideas into clear, executable requirements through iterative questioning. Example: ouroboros init start "I want to build a task management CLI tool" ouroboros init start --orchestrator "Build a REST API" ouroboros init start --orchestrator --runtime codex "Build a REST API" ouroboros init start --llm-backend codex "Build a REST API" ouroboros init start --resume interview_20260116_120000 ouroboros init start --model frontier "Build a REST API" ouroboros init start

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `CONTEXT` | str | 아니요 | Initial context or idea (interactive prompt if not provided). |
| `--resume / -r` | str | 아니요 | Resume an existing interview by ID. |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |
| `--orchestrator / -o` | boolean | 아니요 | Use Claude Code (Max Plan) instead of LiteLLM. No API key required. |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Agent runtime backend for the workflow execution step after seed generation (claude, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, gjc, antigravity, grok, or zcode). |
| `--llm-backend` | choice: claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, omp, zcode, dsh, megacode | 아니요 | LLM backend for interview, ambiguity scoring, and seed generation (claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, zcode, or dsh). |
| `--debug / -d` | boolean | 아니요 | Show verbose logs including debug messages. |
| `--model / -m` | str | 아니요 | Model for every role in this command: auto (latest of each role's tier), frugal, standard, frontier, or a model id. Tier names work on every backend; Claude aliases such as opus only on Claude backends. Default: models.default in config. |
| `--pin-models / --no-pin-models` | boolean | 아니요 | Run the per-role model ids saved in config (research and reproducibility). Default: models.pin in config (off). |

## `ouroboros interview list`

List all interview sessions.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |

## `ouroboros run`

Execute Ouroboros workflows.

## `ouroboros run workflow`

Seed YAML로 orchestrator 실행을 시작한다. 기본 모드는 모델 호출과 파일 변경을 수행할 수 있다. `--no-orchestrator`만 선택한 경로는 이 판본에서 실제 실행이 아닌 자리표시자다. 단, `--mcp-config` 또는 `--resume`을 함께 지정하면 orchestrator 경로가 사용되며 `--dry-run`은 이를 막지 못한다. 아래 표와 [첫 실행의 안전 경계](/docs/first-run-detail/)를 확인한다. 아래 `--check-package`의 영문 설명은 샌드박스가 적용되는 경우를 서술한다. `execution.exec_sandbox`를 끄면 검사 명령은 비격리로 실행되며, 켜져 있어도 플랫폼별 읽기·루프백 네트워크 제한은 다르다. 검사 패키지와 명시적 Seed `verify_command`는 서로 다른 경로이므로 [검사 패키지](/docs/check-package-detail/)와 [Seed 검증 경계](/docs/seed-format-detail/)를 먼저 확인한다.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SEED_FILE` | file | 예 | Path to the seed YAML file. |
| `--orchestrator / -o / --no-orchestrator / -O` | boolean | 아니요 | 기본 orchestrator 경로를 사용한다. 단독 `--no-orchestrator` 경로는 `Would execute ...`만 출력하는 자리표시자다. `--mcp-config`가 있으면 다시 orchestrator를 켜고, `--resume`이 있으면 orchestrator 재개 경로를 사용하므로 실제 실행될 수 있다. |
| `--resume / -r` | str | 아니요 | Resume a previous orchestrator session by ID. |
| `--mcp-config` | path | 아니요 | Path to MCP client configuration YAML file for external tool integration. |
| `--mcp-tool-prefix` | str | 아니요 | Prefix to add to all MCP tool names (e.g., 'mcp_'). |
| `--project-dir` | directory | 아니요 | Explicit project directory for resolving seed-relative paths. |
| `--dry-run / -n` | boolean | 아니요 | 도움말에는 실행 없이 검증한다고 표시되지만, 이 판본의 orchestrator 경로에서는 전달되지 않아 실제 실행될 수 있다. `--no-orchestrator` 단독 경로는 자리표시자로서 dry-run 문구만 표시한다. `--mcp-config` 또는 `--resume`이 함께 있으면 `--no-orchestrator`를 지정해도 orchestrator 경로로 들어가므로 이 조합에서도 실행될 수 있다. [원본 설명](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/cli-reference.md). |
| `--debug / -d` | boolean | 아니요 | Show logs and agent thinking (verbose output). |
| `--sequential / -s` | boolean | 아니요 | Execute ACs sequentially instead of in parallel (default: parallel). |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Agent runtime backend for orchestrator mode (claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, gjc, antigravity, grok, or zcode). |
| `--no-qa` | boolean | 아니요 | Skip post-execution QA evaluation. |
| `--max-decomposition-depth` | int range | 아니요 | Maximum recursive AC decomposition depth. 0 disables decomposition; default 2. Depths above 4 use the historical legacy non-resumable path. |
| `--skip-completed` | str | 아니요 | Path to a YAML marker file listing already-satisfied top-level ACs. Entries use 1-based AC numbers under completed_acs. |
| `--check-package / --no-check-package` | boolean | 아니요 | Before the worker starts, build executable checks from the acceptance criteria and admit them on the current tree. By default they only record what they would have decided on the finished work (record mode); --check-package lets them decide the criteria they cover (or OUROBOROS_CHECK_PACKAGE=decide, or boundary.check_package: decide in config); --no-check-package turns them off (or OUROBOROS_CHECK_PACKAGE=off, or boundary.check_package: off). The checks are model-written Python scripts. They run on throwaway copies of the project with the project's interpreter, a per-check timeout, and an allowlisted environment, confined by the execution sandbox: they can write only inside their copy and a scratch directory and have no network, but they can read files you can read. |
| `--auto-evaluate / --no-auto-evaluate` | boolean | 아니요 | After the run, enqueue formal evaluation (failed runs included) and follow it. Default: execution.auto_evaluate in config (on). |
| `--auto-evolve / --no-auto-evolve` | boolean | 아니요 | When formal evaluation is not approved, continue into a bounded Ralph loop and follow it. Default: execution.auto_evolve in config (on). |
| `--model / -m` | str | 아니요 | Model for every role in this command: auto (latest of each role's tier), frugal, standard, frontier, or a model id. Tier names work on every backend; Claude aliases such as opus only on Claude backends. Default: models.default in config. |
| `--pin-models / --no-pin-models` | boolean | 아니요 | Run the per-role model ids saved in config (research and reproducibility). Default: models.pin in config (off). |

### `run workflow` 선택과 우선순위

아래는 고정 소스의 선언·호출 분기 기준이다. 현재 버전의 `--help` 문구만으로 실행 방지나 비용 없는 동작을 추론하지 않는다. [구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [실행·평가 흐름](/docs/evaluation-evolution-detail/).

| 입력 | 생략 시 / 우선순위 | 사용 시 영향과 주의 |
| --- | --- | --- |
| `SEED_FILE` | 필수: 읽을 수 있는 파일 | 모델 호출·코드와 프로젝트 파일 변경이 뒤따를 수 있다. `ouroboros run SEED_FILE`은 이 하위 명령의 축약형이다. |
| `--orchestrator` / `--no-orchestrator`, `--dry-run` | orchestrator 기본 켜짐; dry-run 기본 꺼짐 | 위 경고처럼 기본 실행 경로는 `--dry-run`을 받지 않는다. `--no-orchestrator`만 사용한 경로는 실제 실행이 아닌 placeholder다. `--mcp-config`나 `--resume` 결합 시 orchestrator 경로로 바뀔 수 있다. |
| `--project-dir` | 명시값 > Seed metadata의 경로 > 유효한 brownfield 대상 등의 경로 해석; 전역 Seed는 다른 대상이 없을 때 현재 디렉터리 사용 | 실행·검증 작업 대상에 영향을 준다. 상대 경로와 task worktree 경계는 [기존 프로젝트](/docs/existing-project-detail/)에서 확인한다. |
| `--resume`, `--skip-completed` | 둘 다 없음 | 전자는 이전 orchestrator 세션 ID를 재개한다. 후자는 1부터 시작하는 완료 AC 번호의 YAML 파일을 사용하나 재개 시 무시된다. [복구](/docs/recovery-detail/). |
| `--mcp-config`, `--mcp-tool-prefix` | 서버 설정 없음, 접두사 빈 문자열 | 구성된 외부 서버를 연결하고 도구 이름에 접두사를 붙인다. 서버 프로세스·네트워크와 실패 시 계속 진행 조건을 [통합 안내](/docs/integration-detail/)에서 확인한다. |
| `--sequential`, `--runtime` | 독립 AC는 병렬; 런타임은 설정에서 결정 | sequential은 독립 AC를 순차 실행한다. runtime은 orchestrator 실행 런타임 선택이다. |
| `--no-qa` | 실행 후 QA 생략 안 함 | QA를 생략하는 스위치이며, formal evaluation이나 그 이후 evolve를 끄는 스위치와 별개다. |
| `--max-decomposition-depth` | CLI > `OUROBOROS_MAX_DECOMPOSITION_DEPTH` > Seed의 `orchestrator.max_decomposition_depth` > 기본 2 | 0은 분해 비활성화; 4 초과는 레거시 비재개 경로다. |
| `--check-package` / `--no-check-package` | CLI > 환경 변수 > 설정 > 기본 record | 명시 활성은 decide, 비활성은 off다. 모델 생성 검사 코드와 샌드박스의 실제 범위를 [검사 패키지](/docs/check-package-detail/)에서 확인한다. |
| `--auto-evaluate`, `--auto-evolve` 및 각각의 `--no-...` | 생략 시 각각 설정값(기본 켜짐) | 실행 후 formal evaluation, 미승인 시 bounded Ralph의 별도 제어다. 비용·시간과 추가 파일 변경이 발생할 수 있다. |
| `--model`, `--pin-models` / `--no-pin-models`, `--debug` | 각각 모델 설정·pin 설정 및 debug 꺼짐 | 이 명령의 모델 해석·자식 프로세스에 영향을 주며 debug는 상세 로그를 출력한다. |

표는 소스 대조와 격리 도움말의 옵션 존재 확인이며 모든 조합의 실제 실행·비용·부작용을 시험한 것이 아니다.

## `ouroboros run resume`

이 명령은 고정 source에서 `Would resume ...`만 출력하는 자리표시자이며 실제 재개하지 않는다. orchestrator 세션은 검토된 Seed와 실제 세션 ID로 `ouroboros run workflow --orchestrator --resume SESSION_ID /path/to/seed.yaml` 경로를 사용한다. [복구 안내](/docs/recovery-detail/).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `EXECUTION_ID` | str | 아니요 | Execution ID to resume. Uses latest if not specified. |

## `ouroboros job`

Inspect background Ouroboros jobs.

## `ouroboros job status`

Print the latest status for a background job.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `JOB_ID` | str | 예 | Job ID returned by a start tool. |
| `--view` | str | 아니요 | 'full' (default), 'summary', or 'compact'. |

## `ouroboros job wait`

Wait briefly for a background job update.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `JOB_ID` | str | 예 | Job ID returned by a start tool. |
| `--cursor` | int | 아니요 | Previous cursor from job status or job wait. |
| `--timeout-seconds` | int | 아니요 | Maximum seconds to wait for a change; defaults to an immediate snapshot. |
| `--view` | str | 아니요 | 'full' (default), 'summary', or 'compact'. |
| `--stream` | str | 아니요 | 'progress' (default) or 'linked'. |

## `ouroboros job result`

Print the terminal result for a completed background job.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `JOB_ID` | str | 예 | Job ID returned by a start tool. |

## `ouroboros job events`

Print read-only job EventStore events as cursor-paged JSON.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `JOB_ID` | str | 예 | Job ID returned by a start tool. |
| `--since` | int | 아니요 | Last seen EventStore rowid cursor. |
| `--limit` | int | 아니요 | Maximum job events to return. |
| `--db-path` | str | 아니요 | Path to ouroboros.db; defaults to the configured runtime database. |

## `ouroboros artifacts`

Fetch, replay, and conservatively prune Disposable Memory artifacts.

## `ouroboros artifacts prune`

List prune candidates by default; deletion requires ''--apply''.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--project-dir` | directory | 아니요 | Project containing .ouroboros/artifacts. |
| `--ttl` | str | 아니요 | Minimum artifact age; default 90d. |
| `--apply` | boolean | 아니요 | Write tombstones and delete listed bodies. |
| `--allow-replay-tombstone` | boolean | 아니요 | Allow pruning inactive contracts still inside replay retention. |

## `ouroboros artifacts fetch`

Explicitly fetch one artifact body.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `CONTRACT_ID` | str | 예 | Contract id the artifact is bound to. |
| `--project-dir` | directory | 아니요 |  |

## `ouroboros artifacts replay`

Replay by reading the stored body; this command never re-executes work.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `CONTRACT_ID` | str | 예 | Contract id to replay from storage. |
| `--project-dir` | directory | 아니요 |  |

### Artifact 명령 선택과 부작용

| 명령·옵션 | 기본값·조건과 영향 |
| --- | --- |
| `fetch CONTRACT_ID`, `replay CONTRACT_ID` | `--project-dir` 기본값은 현재 디렉터리(`.`). 둘 다 저장된 본문을 읽으며 `replay`는 작업을 재실행하지 않는다. ID가 없거나 본문이 정리된 경우 오류가 날 수 있다. |
| `prune --ttl` | 기본 `90d`; 숫자와 `s`, `m`, `h`, `d`, `w` 단위의 음수가 아닌 기간을 받는다. 기본 실행은 삭제 계획이지만 빈 프로젝트에서도 저장소 DB가 생성될 수 있다. |
| `prune --apply` | 기본 false. 지정하면 후보 본문을 삭제하고 tombstone을 기록한다. 실행 전 프로젝트와 후보·백업을 확인한다. |
| `prune --allow-replay-tombstone` | 기본 false. 지정하면 replay 보존 기간 안의 본문도 TTL을 넘었다면 후보가 될 수 있다. 별도의 `--apply` 없이는 계획만 출력한다. |

자세한 저장·보존·동시성 경계는 [Artifact 안내](/docs/artifacts-detail/)를 본다. [CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/artifacts.py).

## `ouroboros harness`

Inspect A2 interview traces (list/show/trace/diff/frontier).

## `ouroboros harness list`

List runs that have traces, plus persisted runs not yet exported. Columns are all data-derived: run_id, a persisted timestamp (never wall-clock at render), export status, terminal phase / grade, final ambiguity, and a provenance-histogram digest.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--traces-root` | path | 아니요 | Trace directory root (default: <cwd>/.ouroboros/traces). |
| `--data-root` | path | 아니요 | Auto-store data root (default: ~/.ouroboros/data). |

## `ouroboros harness show`

Render a run's ''summary.md'' plus key ''outcome.json'' fields. Exports the trace on-demand when it is missing on disk.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `RUN_ID` | str | 예 | Run id (auto_<hex>) to render. |
| `--traces-root` | path | 아니요 | Trace directory root (default: <cwd>/.ouroboros/traces). |
| `--data-root` | path | 아니요 | Auto-store data root (default: ~/.ouroboros/data). |
| `--db-path` | path | 아니요 | EventStore path for on-demand export (default: configured runtime database). |

## `ouroboros harness trace`

Grep across a run's JSONL streams; print ''file:line:'' matches. Deterministic: streams are scanned in a fixed order and lines in file order. Exports the trace on-demand when missing.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `RUN_ID` | str | 예 | Run id (auto_<hex>) to grep. |
| `--grep` | str | 예 | Regex (fallback: literal) to match stream lines. |
| `--stream` | str | 아니요 | Restrict to one stream: questions\|ambiguity\|lateral\|decisions\|flags. |
| `--traces-root` | path | 아니요 | Trace directory root (default: <cwd>/.ouroboros/traces). |
| `--data-root` | path | 아니요 | Auto-store data root (default: ~/.ouroboros/data). |
| `--db-path` | path | 아니요 | EventStore path for on-demand export (default: configured runtime database). |

## `ouroboros harness diff`

Side-by-side of two runs' key metrics + per-stream line deltas. Deterministic text. Exports either trace on-demand when missing.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `RUN_A` | str | 예 | First run id. |
| `RUN_B` | str | 예 | Second run id. |
| `--traces-root` | path | 아니요 | Trace directory root (default: <cwd>/.ouroboros/traces). |
| `--data-root` | path | 아니요 | Auto-store data root (default: ~/.ouroboros/data). |
| `--db-path` | path | 아니요 | EventStore path for on-demand export (default: configured runtime database). |

## `ouroboros harness frontier`

Rank all traced runs by a metric from ''outcome.json''. Ranks only runs already exported on disk (does not bulk-project every persisted run). Unknown metric → clean error listing the available ones.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--metric` | str | 예 | Metric to rank traced runs by. |
| `--traces-root` | path | 아니요 | Trace directory root (default: <cwd>/.ouroboros/traces). |

## `ouroboros config`

Manage Ouroboros configuration.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--web` | boolean | 아니요 | Force web mode even in an interactive terminal. |
| `--host` | str | 아니요 | Web-mode bind address. Use 0.0.0.0 to reach the GUI from another machine when this host runs a remote agent (e.g. hermes). |
| `--port` | int | 아니요 | Web-mode port (0 or omitted picks a free port). |
| `--no-browser` | boolean | 아니요 | Never auto-open a browser; just print the URL (remote/SSH hosts). |

## `ouroboros config show`

Display the effective configuration. Without arguments, renders the GUI-equivalent effective view: defaults, per-stage agents and models with resolved inheritance, value sources (env override / config / default), and CLI install status. Pass a section name for the raw section contents, or --json for a machine-readable effective view.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SECTION` | str | 아니요 | Configuration section to display (e.g., 'orchestrator'). |
| `--json` | boolean | 아니요 | Emit the effective view as JSON (for agents/scripts). |

## `ouroboros config backend`

Show or switch the runtime backend. Without arguments, shows the current backend. With an argument, switches to the specified backend. Delegates to the full setup flow to ensure all side effects (MCP registration, Codex artifacts) are applied consistently. [dim]Examples:[/dim] [dim] ouroboros config backend # show current[/dim] [dim] ouroboros config backend codex # switch to Codex[/dim] [dim] ouroboros config backend claude # switch to Claude Code[/dim] [dim] ouroboros config backend hermes # switch to Hermes[/dim] [dim] ouroboros config backend gemini # switch to Gemini CLI[/dim] [dim] ouroboros config backend gjc # switch to GJC[/dim] [dim] ouroboros config backend goose # switch to Goose[/dim] [dim] ouroboros config backend pi # switch to Pi CLI[/dim] [dim] ouroboros config backend omp # switch to Oh My Pi (omp)[/dim] [dim] ouroboros config backend zcode # switch to Zcode[/dim]

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `NEW_BACKEND` | str | 아니요 | Backend to switch to (claude, codex, gemini, zcode, hermes, goose, pi, omp, gjc, antigravity, grok, megacode). |

## `ouroboros config init`

Initialize Ouroboros configuration. Creates default configuration files if they don't exist. Only creates missing files — never overwrites existing ones.

## `ouroboros config set`

Set a configuration value. Use dot notation for nested keys (e.g., orchestrator.runtime_backend). Keys are validated against the config schema before writing. 이 고정 구현은 YAML 전체를 다시 쓰므로 주석·서식이 달라질 수 있고 성공 시 자동 백업을 만들지 않는다. [dim]Examples:[/dim] [dim] ouroboros config set logging.level debug[/dim] [dim] ouroboros config set models.default frontier[/dim] [dim] ouroboros config set models.pin true[/dim] [dim] ouroboros config set orchestrator.runtime_backend codex[/dim]

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `KEY` | str | 예 | Configuration key (dot notation). |
| `VALUE` | str | 예 | Value to set. |

**불리언 값의 판본 차이:** 키 검증과 값 해석은 별개입니다. 고정 release `0.59.9`의 불리언 변환은 `on`이나 오타를 false로 저장할 수 있고, 고정 main `592c667f`는 유효하지 않은 불리언 값을 거부합니다. 입력 전 [설정 안내의 main/release 경고](/docs/config-reference-guide/)를 확인하고 `true`/`false`를 사용한 뒤 같은 환경에서 저장값을 다시 확인하세요.

## `ouroboros config undo`

기존 `config.yaml.bak`과 현재 `config.yaml`을 교환한다. 도움말은 성공한 `config set`도 백업을 만든다고 설명하지만 이 고정 구현의 `config set`은 직접 YAML을 다시 쓰며 백업을 만들지 않는다. 따라서 이전 백업이 없으면 undo가 실패하고, 오래된 백업이 있으면 직전 변경 전 상태가 아닐 수 있다. 자세한 관찰과 변경 전 보존은 [설정 운영 안내](/docs/operations-detail/)를 확인한다.

## `ouroboros config validate`

Validate current configuration. Checks configuration files for errors and missing required values. Exits with status 1 if issues are found (scriptable).

## `ouroboros status`

Check Ouroboros system status.

## `ouroboros status auto`

Show unified auto + ralph status for an ''ooo auto'' session. Q00/ouroboros#782 — renders both the auto pipeline phase and the ralph sub-block in a single human-readable view.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `AUTO_SESSION_ID` | str | 예 | Auto session id to inspect (auto_<hex>). |

## `ouroboros status run`

Build a read-only Run/Stage/Step projection from persisted events. The CLI is a thin surface over ''ouroboros_query_projection'': the same run anchor returns byte-identical JSON between the MCP query and this command when ''--json'' is set. Exit codes follow the Wave-1 #946 S2 convention (''0'' ok, ''2'' unknown run, ''64'' malformed input).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `RUN_ID` | str | 아니요 | Optional run anchor (execution aggregate ID). Equivalent to passing --execution-id; mutually exclusive with --session-id. |
| `--session-id` | str | 아니요 | Optional orchestrator session ID to project. |
| `--execution-id` | str | 아니요 | Optional execution aggregate ID to project. |
| `--seed-id` | str | 아니요 | Optional seed ID override for projection labels. |
| `--limit` | int | 아니요 | Optional event count safety cap. |
| `--json` | boolean | 아니요 | Emit machine-readable projection JSON. |

## `ouroboros status project`

Show complete read-only run status for one project.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `PROJECT_DIR` | str | 아니요 | Project or workspace directory. Defaults to the current directory. |
| `--workspace` | str | 아니요 | Optional canonical project-relative workspace filter. |
| `--limit` | int | 아니요 | Complete-run safety cap; the command never truncates silently. |
| `--json` | boolean | 아니요 | Emit the exact MCP ProjectRecord JSON payload. |

## `ouroboros status executions`

List recent executions. Shows execution history with status information.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--limit / -n` | int | 아니요 | Number of executions to show. |
| `--all / -a` | boolean | 아니요 | Show all executions. |

## `ouroboros status execution`

Show details for a specific execution. Displays execution metadata, progress, and optionally events.

!!! note "도움말과 고정 구현의 표시 범위"
    위 영문은 CLI 도움말을 옮긴 것이다. 고정 구현의 상세 출력은 실행 ID·상태·최근 lifecycle 이벤트 유형·시각이며, `--events`는 시각·유형·상태의 요약 표다. 일반적인 metadata·단계별 progress 또는 이벤트 payload 전체를 표시한다고 가정하지 않는다. [실행 상태 조회와 검증 범위](/docs/progress-detail/)를 참고한다.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `EXECUTION_ID` | str | 예 | Execution ID to inspect. |
| `--events / -e` | boolean | 아니요 | Show execution events. |

## `ouroboros status health`

Check system health. Verifies configuration, database, runtime backend, and credentials.

## `ouroboros cancel`

Cancel stuck or orphaned executions.

## `ouroboros cancel execution`

Cancel a stuck or orphaned execution. Cancel a specific execution by session ID, or use --all to cancel every running/paused execution. When called without arguments, lists active executions and prompts you to pick one. This command interacts directly with the event store to emit cancellation events. Examples: # Interactive mode - list and pick ouroboros cancel execution # List active executions without prompting (scripts, agents) ouroboros cancel execution --list # Cancel a specific execution ouroboros cancel execution orch_abc123def456 # Cancel all running executions ouroboros cancel execution --all # Cancel with a custom reason ouroboros cancel execution orch_abc123 --reason "Stuck for 2 hours"

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `EXECUTION_ID` | str | 아니요 | Session/execution ID to cancel. |
| `--all / -a` | boolean | 아니요 | Cancel all running/paused executions. |
| `--reason / -r` | str | 아니요 | Reason for cancellation. |
| `--list / -l` | boolean | 아니요 | List active executions and exit without prompting or cancelling. |

**취소 ID와 결과 확인:** 위 help의 `EXECUTION_ID`라는 이름과 달리, 고정 main/release의 이 명령은 전달값을 실행 세션의 `session_id`로 복원합니다. `ouroboros cancel execution --list`에 표시된 세션 ID(예: `orch_...`)를 확인해 사용하고, 상태 조회용 `execution_id`·백그라운드 `job_id`·Interview 저장 ID를 그대로 대신 넣지 마세요. `--list`는 취소하지 않지만 EventStore 초기화가 일어날 수 있습니다. ID 지정과 `--all`은 대화형 선택·확인 경로를 거치지 않습니다. `Cancellation requested`는 요청 접수이며 완료가 아니므로 같은 세션 상태와 남은 작업·외부 효과를 다시 확인하세요. 종료 코드 0이나 취소 기록만으로 프로세스 종료·변경 되돌림을 판단하지 않습니다. [복구와 취소 경계](/docs/recovery-detail/) · [main 취소 ID 복원](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/cancel.py#L139-L145) · [release 세션 이벤트 복원](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/orchestrator/session.py#L1298-L1328).

## `ouroboros cleanup`

Prune leftover auto-session worktrees, branches, locks, and state files.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--dry-run` | boolean | 아니요 | Report what would be removed without removing anything. |
| `--force / -f` | boolean | 아니요 | Also remove clean worktrees whose branch is not merged yet. Unmerged branches themselves are kept. |
| `--state-all` | boolean | 아니요 | Prune state files of blocked/failed sessions too (default prunes only completed sessions). |

## `ouroboros codex`

Manage Ouroboros Codex CLI integration artifacts.

## `ouroboros codex refresh`

Refresh Codex rules and skills without changing MCP or Ouroboros config.

## `ouroboros codex doctor`

Verify installed Codex artifacts can route ''ooo auto'' to Ouroboros.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--codex-dir` | path | 아니요 | Codex configuration directory to inspect. Defaults to $CODEX_HOME or ~/.codex. |
| `--live-mcp` | boolean | 아니요 | Launch the configured stdio MCP server, run initialize/list_tools, and verify the official auto tools are exposed. |

## `ouroboros doctor`

Run read-only diagnostics for Ouroboros installations.

## `ouroboros doctor install`

Inspect package, plugin, and MCP install surfaces without mutating files.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--json` | boolean | 아니요 | Emit machine-readable JSON to stdout. |

## `ouroboros mcp`

MCP (Model Context Protocol) server commands.

## `ouroboros mcp doctor`

Run environment diagnostics for the MCP server. Checks Python version, the isolated MCP 2 profile, backend-specific dependencies, Codex OAuth readiness, EventStore health, and PID file liveness. Claude Agent SDK and MCP 2 are intentionally diagnosed as separate process profiles. Exit code 1 if any check fails. Examples: # Human-readable output ouroboros mcp doctor # Machine-readable (for bug reports) ouroboros mcp doctor --json # Opt-in local server startup and discovery probe ouroboros mcp doctor --probe-local-stdio

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--machine-snapshot` | boolean | 아니요 | Include an opt-in static, content-free machine snapshot. |
| `--json` | boolean | 아니요 | Emit machine-readable JSON to stdout. |
| `--probe-local-stdio` | boolean | 아니요 | Start this Ouroboros installation and probe MCP discovery over stdio. |

## `ouroboros mcp doctor-runtime`

Show bounded, read-only runtime facts for local MCP diagnostics.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--json` | boolean | 아니요 | Emit machine-readable JSON to stdout. |

## `ouroboros mcp serve`

Start the MCP server. Exposes Ouroboros functionality via Model Context Protocol, allowing Claude Desktop and other MCP clients to interact with Ouroboros. Available tools: - ouroboros_execute_seed: Execute a seed specification - ouroboros_session_status: Get session status - ouroboros_query_events: Query event history Examples: # Start with stdio transport (for Claude Desktop) ouroboros mcp serve --runtime claude-cli # Start with SSE transport on custom port ouroboros mcp serve --runtime claude-cli --transport sse --port 9000 # Start with streamable HTTP transport for Codex CLI --url clients ouroboros mcp serve --runtime claude-cli --transport streamable-http --port 9000 # Start with OpenCode runtime ouroboros mcp serve --runtime opencode # Use Codex CLI for LLM-only tools as well ouroboros mcp serve --runtime codex --llm-backend codex

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--host / -h` | str | 아니요 | Host to bind to. |
| `--port / -p` | int | 아니요 | Port to bind to. |
| `--transport / -t` | str | 아니요 | Transport type: stdio, sse, or streamable-http. |
| `--auth-token` | str | 아니요 | Shared secret clients must present as 'Authorization: Bearer <token>'. Required for network transports on a non-loopback host. Prefer the OUROBOROS_MCP_AUTH_TOKEN environment variable: a token on the command line is visible to every process on this machine via 'ps'. |
| `--allow-remote` | boolean | 아니요 | Acknowledge that a non-loopback bind exposes seed execution to everyone who can reach the port. Required alongside --auth-token to serve on a routable address. |
| `--allowed-host` | str | 아니요 | Host header value clients will use, e.g. 'ouroboros.internal:8080'. Repeatable. Required for wildcard binds (--host 0.0.0.0), whose reachable name cannot be inferred. A ':*' suffix allows any port. |
| `--allowed-origin` | str | 아니요 | Origin header value to permit. Repeatable. Empty by default, which rejects every browser-originated request. |
| `--workspace-root` | str | 아니요 | Restrict seed execution to directories under this path. Repeatable. Strongly recommended for network binds; unset means any existing directory on this machine may be used as a working directory. |
| `--db` | str | 아니요 | Override the shared EventStore path (default: persistence.database_path with legacy fallback). |
| `--idle-timeout` | float | 아니요 | Shut the server down after this many seconds without a tool call. Defaults to 7200 for network transports (sse, streamable-http) and disabled for stdio. Pass 0 to disable. |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Agent runtime backend for orchestrator-driven tools (claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, gjc, antigravity, grok, zcode, or host). |
| `--llm-backend` | choice: claude_code, litellm, codex, goose, copilot, opencode, gemini, kiro, pi, omp, zcode, dsh, megacode | 아니요 | LLM backend for interview/seed/evaluation tools (claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, zcode, or dsh). |

## `ouroboros mcp info`

Show MCP server information and available tools.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--runtime` | choice: claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, omp, gjc, antigravity, grok, zcode, megacode, host | 아니요 | Agent runtime backend for orchestrator-driven tools (claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, copilot, goose, kiro, pi, gjc, antigravity, grok, zcode, or host). |
| `--llm-backend` | choice: claude_code, litellm, codex, goose, copilot, opencode, gemini, kiro, pi, omp, zcode, dsh, megacode | 아니요 | LLM backend for interview/seed/evaluation tools (claude_code, litellm, codex, copilot, opencode, gemini, goose, kiro, pi, zcode, or dsh). |

## `ouroboros setup`

Set up Ouroboros for your environment.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--runtime / -r` | str | 아니요 | Runtime backend to configure (claude, claude-sdk, claude-cli, codex, opencode, hermes, gemini, goose, kiro, copilot, pi, omp, gjc, antigravity, grok, zcode, megacode, host). |
| `--non-interactive` | boolean | 아니요 | Skip interactive prompts (for scripted installs). |
| `--opencode-mode` | str | 아니요 | OpenCode integration mode (mutually exclusive): plugin (default) or subprocess. |
| `--mcp-mode` | str | 아니요 | Codex MCP config mode: auto preserves native-Windows safety and user entries; http explicitly writes the native-Windows loopback URL; preserve skips MCP changes; stdio replaces with the managed entry on supported hosts. |

## `ouroboros setup refresh`

Refresh artifacts installed by a previous setup.

## `ouroboros setup scan`

Re-scan a root directory and register new repos. Scans the requested root (up to a shallow depth) for valid seed git repos/worktrees and updates the brownfield registry. Each repo/worktree the walk reaches directly is registered self-only; Git worktree families are not expanded. Local repos and repos with any remote name are eligible. Existing repos are preserved (upsert).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SCAN_ROOT` | directory | 아니요 | Root directory for the brownfield scan. Defaults to the current user's home directory. |

## `ouroboros setup list`

List all registered brownfield repos.

## `ouroboros setup default`

Toggle default brownfield repos for PM interviews. Displays all registered repos and lets you toggle defaults (multi-default supported).

## `ouroboros detect`

Generate .ouroboros/mechanical.toml via one AI call.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `PATH` | path | 아니요 | Project directory to inspect. Defaults to cwd. |
| `--force / -f` | boolean | 아니요 | Re-detect and overwrite an existing .ouroboros/mechanical.toml. |
| `--backend` | str | 아니요 | LLM backend override (claude, codex, gemini, opencode, litellm). |

## `ouroboros tui`

Interactive TUI monitor for Ouroboros workflows.

## `ouroboros tui monitor`

Launch interactive TUI monitor. Starts a terminal UI that shows a list of all sessions found in the database. You can then select a session to monitor in real-time. The monitor attaches to the event store as an observer and does not own the running execution, so pause/resume controls are not offered on either backend. Use 'ouroboros cancel execution' to stop a run.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--db-path` | path | 아니요 | Path to the Ouroboros database file to monitor. |
| `--backend` | str | 아니요 | TUI backend to use: 'python' (default) or 'slt' (native binary). |

## `ouroboros tui open`

Open the TUI monitor in a new terminal window when possible.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--db-path` | path | 아니요 | Path to the Ouroboros database file to monitor. |
| `--cwd` | path | 아니요 | Working directory for the spawned TUI process. |

## `ouroboros pm`

Generate a Product Requirements Document through guided interview.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--resume / -r` | str | 아니요 | Resume an existing PM interview session by ID. |
| `--output / -o` | str | 아니요 | Output directory for the generated PM document (default: .ouroboros/). |
| `--model / -m` | str | 아니요 | Model for every role in this command: auto (latest of each role's tier), frugal, standard, frontier, or a model id. Tier names work on every backend; Claude aliases such as opus only on Claude backends. Default: models.default in config. |
| `--pin-models / --no-pin-models` | boolean | 아니요 | Run the per-role model ids saved in config (research and reproducibility). Default: models.pin in config (off). |
| `--debug` | boolean | 아니요 | Enable debug output. |

## `ouroboros plugin`

Manage UserLevel plugins (#725).

## `ouroboros plugin discover`

Inspect a manifest without registering or granting trust. 'discover' is the safest command in the manager — it neither writes to the lockfile nor reads the trust store.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `TARGET` | str | 예 | Path to a plugin directory or its ouroboros.plugin.json file. |

## `ouroboros plugin inspect`

Show installed plugin metadata + trust state. Unlike 'discover', this reads the lockfile and trust store. It still does not mutate any state.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `NAME` | str | 예 | Installed plugin name. |
| `--lockfile` | path | 아니요 | Override the lockfile path (default: ~/.ouroboros/plugins.lock). |
| `--trust-root` | path | 아니요 | Override the trust root (default: ~/.ouroboros/trust). |

## `ouroboros plugin list`

List installed plugins with their trust state.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--lockfile` | path | 아니요 | Override the lockfile path (default: ~/.ouroboros/plugins.lock). |
| `--trust-root` | path | 아니요 | Override the trust root (default: ~/.ouroboros/trust). |
| `--json` | boolean | 아니요 | Emit JSON for piping; suppresses table formatting. |

## `ouroboros plugin add`

Install one or more plugins from a repo URL or local path. Anti-pattern install strings (e.g. '#plugins/<name>') are rejected.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `TARGET` | str | 예 | Repository URL or local path. |
| `--plugin` | str | 아니요 | Non-interactive: name of a plugin in the repo catalog. Repeatable. |
| `--cache-root` | path | 아니요 | Where to clone repo URLs (default: ~/.ouroboros/cache). |
| `--plugin-home-root` | path | 아니요 | Where to install plugin homes (default: ~/.ouroboros/plugins). |
| `--lockfile` | path | 아니요 | Override the lockfile path. |
| `--trust-root` | path | 아니요 | Override the trust root (default: ~/.ouroboros/trust). Used to invalidate prior grants on a version bump. |
| `--catalog-state` | path | 아니요 | Override the known-catalog state path (default: ~/.ouroboros/plugin-catalogs.json). |

## `ouroboros plugin install`

Install one plugin. The RFC ("UX / 'add' vs 'install'") defines 'install' as the non-interactive primitive, with three resolution paths: - **Default form** — ''ooo plugin install <name>'' — succeeds only if exactly one known catalog exposes that name. Multi-source ambiguity raises an explicit error listing the candidates. - **Qualified form** — ''ooo plugin install <name> --from <url\|path>'' — selects an explicit source. For ''--from <local-path>'' this is ALSO the register-on-first-use verb for 'local_path' sources. - **Legacy direct-directory form** — ''ooo plugin install <plugin-dir>'' — kept for ergonomic parity with ''ooo plugin discover'' / pre-RFC scripts. The argument must be an existing directory containing ''ouroboros.plugin.json''.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `TARGET` | str | 예 | Either: a plugin name (resolves via the known-catalog registry — ambiguous names require --from), OR a local plugin directory containing ouroboros.plugin.json (legacy form). |
| `--from` | str | 아니요 | Qualify which source to install <name> from: a repo URL (plugin_home) or an absolute local path (local_path, register-on-first-use). |
| `--plugin-home-root` | path | 아니요 |  |
| `--lockfile` | path | 아니요 |  |
| `--trust-root` | path | 아니요 | Override the trust root (default: ~/.ouroboros/trust). Used to invalidate prior grants on a subject change. |
| `--cache-root` | path | 아니요 | Where to clone repo URLs for --from (default: ~/.ouroboros/cache). |
| `--catalog-state` | path | 아니요 | Override the known-catalog state path (default: ~/.ouroboros/plugin-catalogs.json). |

## `ouroboros plugin trust`

Grant one or more scopes to an installed plugin. Per Q00/ouroboros-plugins#9 Q3 lock: scopes are exact strings — '--scope github:pull_request' does NOT imply 'github:pull_request:write'. Per the locked RFC ("Disable records / Re-enabling"), 'trust' is also the re-enable path: it deletes any disable record bound to the install subject. Plugins whose manifest declares no permissions therefore accept an empty '--scope' set so they can be re-enabled after 'disable'. Plugins with declared permissions still require at least one '--scope' argument so the user has to make an explicit permission decision.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `NAME` | str | 예 | Installed plugin name. |
| `--scope` | str | 아니요 | Permission scope to grant. Repeatable. Exact-string match. Optional: omit to re-enable a disabled zero-permission plugin without granting any new scope. |
| `--granted-by` | str | 아니요 | User identity recorded in the audit trail. |
| `--lockfile` | path | 아니요 |  |
| `--trust-root` | path | 아니요 |  |
| `--audit-log` | path | 아니요 | Append plugin.trusted events here as JSON Lines (default: skip). |

## `ouroboros plugin disable`

Disable an installed plugin. Per the locked RFC ("Disable records"), 'disable' writes a record keyed by ''(name, source.type, source_identity)'' (no ''artifact_digest'') so the disable signal survives every digest change, including upgrades. The trust file is wiped at the same time. The lockfile entry remains so the user can re-enable with ''ooo plugin trust …'', which is the re-enable path.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `NAME` | str | 예 | Installed plugin name. |
| `--lockfile` | path | 아니요 |  |
| `--trust-root` | path | 아니요 | Override the trust root (default: ~/.ouroboros/trust). Required when the plugin was trusted under a non-default root. |

## `ouroboros plugin remove`

Remove an installed plugin (lockfile entry, trust file, plugin home).

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `NAME` | str | 예 | Installed plugin name. |
| `--lockfile` | path | 아니요 |  |
| `--trust-root` | path | 아니요 |  |
| `--plugin-home-root` | path | 아니요 |  |

## `ouroboros resume`

List in-flight sessions and re-attach after MCP disconnect.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--all / -a` | boolean | 아니요 | Show every in-flight session instead of the most recent 20. |
| `--list / -l` | boolean | 아니요 | List in-flight sessions and exit without prompting. |

## `ouroboros uninstall`

Cleanly remove Ouroboros from your system.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--keep-data` | boolean | 아니요 | Keep entire ~/.ouroboros/ directory (config, credentials, seeds, logs, DB). |
| `--dry-run` | boolean | 아니요 | Show what would be removed without actually deleting. |
| `--yes / -y` | boolean | 아니요 | Skip confirmation prompt. |

## `ouroboros update`

Update Ouroboros to the latest version.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `--check` | boolean | 아니요 | Only report installed vs latest version — change nothing. |
| `--yes / -y` | boolean | 아니요 | Skip confirmation prompt. |
| `--dry-run` | boolean | 아니요 | Show the commands that would run without executing them. |
| `--prerelease / --no-prerelease` | boolean | 아니요 | Include pre-releases (default: only when a pre-release is installed). |
| `--runtime / -r` | str | 아니요 | Runtime integration to refresh after upgrading (all refreshes Claude and Codex without changing the configured backend; auto preserves the configured backend; none skips refresh). |

### 설치·업데이트·제거 전 선택할 옵션

| 명령·입력 | 기본값과 동작 경계 |
| --- | --- |
| `setup --runtime/-r` | 생략하면 설치된 런타임을 탐색한다. 여러 개면 보통 선택을 요청한다. `--non-interactive`에서는 기존 백엔드가 탐색 결과에 있으면 우선하고, 그렇지 않으면 Claude, 그다음 탐색된 첫 런타임을 선택한다. 설정·호스트 통합 파일을 바꿀 수 있으므로 조회 전용 명령이 아니다. |
| `setup --non-interactive` | 기본 false. 질문을 건너뛰지만 설정 쓰기나 외부 프로그램 탐색을 건너뛰는 의미가 아니다. 런타임별 경로·실패 조건은 [호스트 설정](/docs/setup-host-detail/)을 확인한다. |
| `setup --opencode-mode`, `--mcp-mode` | 각각 기본 `plugin`, `auto`. OpenCode의 plugin/subprocess와 Codex MCP 등록 정책은 별개다. `preserve`는 MCP 변경을 생략하며 `stdio`·`http` 및 Windows 차이는 [호스트 설정](/docs/setup-host-detail/)에서 확인한다. |
| `setup scan [SCAN_ROOT]` | 인자를 생략하면 홈 디렉터리부터 얕게 탐색해 발견한 저장소를 brownfield 레지스트리에 등록한다. 조회만 하는 명령이 아니다. 목록은 `setup list`, 기본 선택은 `setup default`로 다룬다. |
| `update --check` | 기본 false. 지정하면 설치 버전과 최신 버전의 비교만 진행하지만 PyPI 조회를 위해 네트워크가 필요하다. 업데이트 자체는 하지 않는다. |
| `update --dry-run`, `--yes/-y` | 둘 다 기본 false. dry-run은 실행할 업데이트 명령의 미리보기이며 최신 버전 조회는 수행한다. `--yes`는 확인 질문만 건너뛰고 실제 업데이트를 막지 않는다. |
| `update --prerelease/--no-prerelease`, `--runtime/-r` | prerelease는 미지정 시 현재 버전이 사전 릴리스인 경우에 포함한다. runtime 기본은 `auto`; `all`은 Claude·Codex 통합을 갱신하고 `none`은 통합 갱신을 생략한다. 설치 방식·부분 실패는 [업데이트 안내](/docs/update-detail/)를 참조한다. |
| `uninstall --dry-run`, `--yes/-y` | 둘 다 기본 false. dry-run은 탐지한 제거 대상을 표시하고 삭제를 수행하지 않는다. `--yes`는 확인만 생략하며 삭제를 막지 않는다. 이 명령은 Python 패키지 자체를 제거하지 않는다. |
| `uninstall --keep-data` | 기본 false. 지정하면 홈 `~/.ouroboros/` 보존을 요청하지만 현재 작업 디렉터리의 `.ouroboros/`와 `CODEX_HOME`을 반영한 Codex home의 존재하는 관리 rules/skills는 별도 제거 대상이다. 삭제 실패 가능성, 홈에서 실행할 때의 경로 중복 및 관리 자산의 사용자 수정 보존은 [제거 전 보존 범위](/docs/operations-detail/)를 먼저 확인한다. |

이 표는 고정 소스의 옵션과 분기를 대조한 설명이며 모든 런타임·환경 조합을 실행한 결과는 아니다. [setup 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/setup.py), [update 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/update.py), [uninstall 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/uninstall.py).

## `ouroboros workflow-ir`

Inspect read-only Workflow IR projections.

## `ouroboros workflow-ir inspect`

Project a Seed file into Workflow IR without dispatching work.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SEED_FILE` | path | 예 | Seed YAML file to inspect. |
| `--json` | boolean | 아니요 | Emit machine-readable JSON. |

### Workflow IR 검사 입력과 결과

| 입력 | 기본값·조건과 영향 |
| --- | --- |
| `SEED_FILE` | 읽을 수 있는 YAML 매핑이어야 하며 Seed 모델과 IR 투영의 필수 조건을 만족해야 한다. 실패 시 종료 1. |
| `--json` | 기본 false. 지정하면 투영 결과와 validation을 JSON으로 출력한다. 검사는 작업을 dispatch하지 않는다. |
| 결과 해석 | 현재 CLI의 validation 출력은 투영 성공 후 구성한 값으로, 원래 검증기의 모든 경고를 전달하는 결과가 아니다. 생략된 Seed ID는 모델이 생성할 수 있다. 자세한 범위는 [Workflow IR](/docs/workflow-ir-detail/). |

[CLI 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/workflow_ir.py).

## `ouroboros zcode`

Convenience commands that use Zcode automatically.

## `ouroboros zcode start`

Start an interview using Zcode for authoring and workflow handoff.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `CONTEXT` | str | 아니요 | What you want to build, check, or turn into a Seed. |
| `--resume / -r` | str | 아니요 | Resume an existing interview by ID. |
| `--state-dir` | directory | 아니요 | Custom directory for interview state files. |
| `--debug / -d` | boolean | 아니요 | Show verbose logs. |

## `ouroboros zcode qa`

Evaluate text or a file with Zcode-backed Ouroboros QA.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `ARTIFACT` | str | 예 | Text or path to the file you want Zcode to evaluate. |
| `--quality-bar / -q` | str | 아니요 | Plain-language description of what PASS means. |
| `--artifact-type / -t` | str | 아니요 | Artifact type: code, document, api_response, screenshot, test_output, custom. |
| `--reference / -r` | str | 아니요 | Optional reference text or file path. |
| `--pass-threshold` | float range | 아니요 | Score threshold for PASS. |

## `ouroboros zcode run`

Run a Seed with Zcode as the execution runtime.

| 인자/옵션 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `SEED_FILE` | file | 예 | Path to a Seed YAML file. |
| `--project-dir` | directory | 아니요 | Project directory to run in. |
| `--resume / -r` | str | 아니요 | Resume a previous orchestrator session by ID. |
| `--no-qa` | boolean | 아니요 | Skip post-execution QA evaluation. |
| `--debug / -d` | boolean | 아니요 | Show verbose logs. |
| `--sequential / -s` | boolean | 아니요 | Execute acceptance criteria sequentially. |
| `--max-decomposition-depth` | int range | 아니요 | Maximum recursive split depth. Depths above 4 use legacy execution. |

`zcode run --no-qa`는 실행 후 QA만 생략하며 정식 자동 평가나 조건부 Ralph 후속을 끄지 않는다. 이 wrapper는 `--no-auto-evaluate`·`--no-auto-evolve` 옵션을 노출하지 않고 `run workflow`에 해당 override를 전달하지 않으므로 설정된 `execution.auto_evaluate`·`execution.auto_evolve` 정책이 적용된다. 기본 설정은 둘 다 켜져 있다. 실행 전 설정과 예상 후속 작업을 확인한다. 명령별 override가 필요하면 설치된 판본에서 일반 `run workflow`의 `--runtime zcode`와 자동 평가·진화 옵션을 확인한다. `zcode run`은 [런타임 안내](/docs/runtime-support-detail/)의 백엔드 차이도 따르므로 두 호출의 전체 환경이 자동으로 동일하다고 가정하지 않는다. 이는 [wrapper](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/zcode.py), [workflow](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run.py), [후속 정책](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/run_successors.py)의 정적 대조이며 실제 Zcode·모델·후속 작업은 시험하지 않았다.
