# 런타임별 설치·권한·재개 차이

> **판본과 검증 범위:** 이 안내는 2026-11-04에 조사한 Ouroboros 고정 소스 [`722172ef096767583679d04aef5e847458fee6b2`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)를 기준으로 한다. 2026-11-06에 확인한 upstream `main` (`592c667f076c3dad7ef68d7844e91480d80135d0`) 및 2026-11-07에 기록된 공개 릴리스 `v0.59.9`와 이 본문의 동등성은 확인하지 않았다. 설치된 호스트 플러그인·MCP 서버의 실제 동작도 미검증이다. 설치판의 도움말·설정·도구 스키마를 먼저 확인하고, 아래 시험 사례를 운영 성공이나 현재판 보장으로 일반화하지 않는다.

기준: 2026-11-04, Ouroboros [722172ef096767583679d04aef5e847458fee6b2](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2). 이 페이지의 표는 고정 소스의 백엔드 등록과 해당 판본의 **문서상 계약**을 요약한다. 각 호스트에서 실제 설치·인증·호출을 시험했다는 뜻이 아니다. 외부 제품의 현재 요금, 로그인 방식, OS 지원은 달라질 수 있다. 이 조사에서는 모델 호출이나 원격 실행을 하지 않았다.

## 배포 패키지 0.59.9와 고정 소스의 차이

별도 Python 3.13 환경의 `ouroboros-ai[mcp]==0.59.9`(해결된 MCP 2.2.0)과 위 고정 소스를 비교했다. **이 페이지는 고정 소스를 기준으로 하므로 아래 런타임이 설치된 0.59.9 패키지에도 있다고 가정하지 않는다.** 패키지의 `ouroboros setup --help`에 `megacode`는 없었고 패키지의 백엔드 등록·설정 모델과 런타임 파일에서도 해당 항목을 찾지 못했다. 같은 패키지에는 고정 소스의 `copilot_acp_runtime.py`도 없었다. 따라서 아래 `megacode`와 실험적 Copilot ACP 설명은 **고정 소스에 대한 안내**이며, 이 패키지에서 실행 가능한 기능으로 확인되지 않았다. 설치한 버전의 도움말과 실제 배포물을 확인한다. [source 등록](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/backends/capabilities.py), [source ACP 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/copilot_acp_runtime.py).

이는 해당 help와 파일을 정적으로 비교한 관찰이다. 각 런타임 실행·인증·다른 패키지 빌드나 호스트 플러그인은 시험하지 않았고, 나머지 기능이 두 판본에서 동등하다는 뜻도 아니다. MCP 도구 스키마 차이는 [MCP 색인](/docs/mcp-reference-detail/#package-source-differences)에 따로 기록했다.

## 선택 전에 구분할 것

호스트는 사용자와 MCP 서버를 연결하고, **작업 런타임**은 작업을 수행하며, **LLM 백엔드**는 작성·평가 등에 사용된다. 이름이 같아도 세 연결은 별개다. `orchestrator.runtime_backend`, `OUROBOROS_AGENT_RUNTIME`, 진입점의 `--runtime`과 실행 단계 프로필이 선택에 관여한다. `ooo auto`의 작성 단계는 서버 내 핸들러에서 실행하고 RUN 인계 단계에 실행 런타임을 사용한다. 설정 경로와 우선순위는 [호스트와 MCP 연결](/docs/integration-detail/), [구성 색인](/docs/config-reference-detail/), [원본 auto 계약](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/auto-runtime-semantics.md)을 확인한다.

다음은 소스의 [백엔드 등록](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/backends/capabilities.py)에서 런타임으로 등록된 이름이다. 실행 가능 바이너리, 설치 성공, 계정 권한, 모든 기능의 동일한 동작까지 보장하는 목록은 아니다.

| 런타임 | 문서상 준비와 특히 확인할 점 |
| --- | --- |
| `claude` | in-process Claude Agent SDK 어댑터다. 독립 실행 환경에 `[claude]` 또는 `[claude-sdk]` extra와 해당 인증이 필요하다. MCP 2용 `[mcp]`와 같은 Python 환경에 섞지 않는다. SDK가 사용하는 CLI 경로는 선택적으로 지정할 수 있다. [팩토리](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/runtime_factory.py), [SDK 어댑터](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/adapter.py) |
| `claude_mcp` | 별도 Claude CLI의 headless worker 경로다. 실행 파일과 인증을 확인한다. SDK 어댑터와 동일한 in-process 경로가 아니다. 플러그인은 격리된 MCP 2 서버와 CLI 워커를 사용한다. [워커 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/claude_worker_runtime.py), [안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/claude-code.md) |
| `codex`, `codex_mcp` | Codex CLI·인증이 필요하다. 기본 패키지에 실행 어댑터가 있지만 Ouroboros의 Codex 호스트 MCP 등록에는 별도의 실행 가능한 런처(`uvx`, MCP extra 설치 또는 MCP가 있는 Python 환경)가 필요하다. `codex_mcp` 작업자는 같은 Codex 바이너리의 `mcp-server`를 사용한다. [안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/codex.md) |
| `copilot` | `copilot` 실행 파일·인증이 필요하며 원본 표는 MCP extra와 모델 검색용 `gh`도 명시한다. 기본 CLI 외 실험적 ACP 전송은 별도 선택이다. [안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/copilot.md), [ACP](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/copilot-acp.md) |
| `gemini`, `opencode`, `hermes`, `goose`, `kiro` | 각각 대응 CLI와 그 CLI의 인증·프로바이더 설정이 필요하다. Kiro 바이너리는 `kiro-cli`다. 설치 및 MCP 설정은 [각 런타임 안내](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides)를 따르고, 모델·도구 권한이 같다고 가정하지 않는다. |
| `pi`, `omp`, `gjc` | 각각 `pi`, `omp`, `gjc`가 필요하다. `gjc`의 원본 표는 MCP extra도 명시한다. OMP와 Pi의 도구 제한 적용 여부는 아래 권한 항목을 확인한다. [안내](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides) |
| `antigravity`, `grok`, `zcode` | 각각 `agy`, `grok`, `zcode` 실행 파일을 사용하는 별도 어댑터다. 이 커밋에서 Antigravity와 Grok은 실행 런타임이지만 LLM 백엔드로 등록돼 있지 않다. Zcode는 양쪽에 등록돼 있다. [안내](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides) |
| `megacode` | `harness`, 해당 인증, MCP 실행용 `uv`가 필요하다. setup은 harness 설정 경로에 관리 블록을 쓴다. headless 호출은 세션 재개를 지원하지 않으며 중첩 호출마다 MCP 시작 비용이 발생할 수 있다. [안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/megacode.md) |
| `host` | 외부 CLI 대신 호출 MCP 호스트가 작업을 받아 하위 에이전트를 실행하고 결과를 제출해야 한다. 터미널 `ouroboros run`, 직접 `ouroboros_execute_seed`, evolve와 Ralph는 이 경로를 지원하지 않는다. 호스트의 `ouroboros_job_wait` 및 결과 제출 계약이 필수다. [안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/host.md) |

같은 등록에서 `ourocode`, `dsh`, `litellm`은 LLM 백엔드로 나타나지만 작업 런타임으로 등록돼 있지 않다. `dsh` 호스트가 `host` 실행 런타임을 사용하는 경로와 혼동하지 않는다. 등록 정보는 각 커맨드가 해당 이름을 모두 받는다는 보장은 아니다. 각 진입점의 도움말과 해당 안내를 확인한다.

## DSH(DeepSeek Harness)를 LLM 백엔드로 사용할 때 {#dsh-llm-backend}

이 별도 안내는 제품 main `592c667f`와 release `v0.59.9`의 DSH 경로를 설명합니다. 제품 client 소스가 대조한 upstream은 `deepseek-harness@0.1.0-rc.5`, commit `47f9438`입니다. 이 판본 표시는 현재 upstream/package 상태를 보증하지 않습니다. `dsh`는 interview·Seed·QA 등의 **LLM 백엔드**이고 agent 작업을 실행하는 runtime은 아닙니다. `dsh-acp-demo`를 별도 child process로 실행하며, 작업 runtime도 따로 지정해야 합니다. [main backend 등록](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/backends/capabilities.py#L714-L728) · [release 등록](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/backends/capabilities.py#L702-L710).

### 먼저 실행 파일을 확인하기 {#dsh-executable-check}

`ouroboros mcp serve`를 실행할 **같은 터미널·환경**에서 다음을 확인합니다. 이 명령은 `PATH`에서 찾은 경로만 출력하며, Ouroboros가 실제로 선택하는 경로와 다를 수 있습니다. 실행 결과를 공유할 때는 개인 경로를 가리세요.

```sh
command -v dsh-acp-demo
```

별도 경로를 설정했다면 `command -v` 결과 대신 선택된 절대 경로를 직접 확인합니다. 예를 들어 경로가 `/absolute/path/to/dsh-acp-demo`라면:

```sh
test -x /absolute/path/to/dsh-acp-demo
```

실행 파일을 찾지 못했다면 제품 문서가 고정한 DeepSeek Harness source commit `47f9438`과 Node.js `>= 22` 조건, `pnpm install && pnpm run build` source-build 절차를 검토한 뒤 실행하세요. 제품 문서는 대조한 `@0.1.0-rc.5` 호환 경로에서 published `@deepseek-ai/dsh-acp-demo` 설치의 peer-dependency 문제를 기록합니다. 이 상태는 문서가 대조한 버전의 관찰이며 현재 registry 상태나 설치 성공을 보증하지 않습니다. 의존성 설치와 build는 네트워크·실행 스크립트를 사용할 수 있습니다. [main DSH client](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/dsh_acp_client.py#L1-L13) · [main launch/validation](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/dsh_acp_client.py#L47-L137) · [release DSH client](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/dsh_acp_client.py#L1-L13) · [release launch/validation](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/dsh_acp_client.py#L47-L137) · [main guide](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/guides/deepseek-harness.md#L96-L103) · [release guide](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/docs/guides/deepseek-harness.md#L96-L103).

CLI 경로 우선순위는 호출자의 명시적 `cli_path` → `OUROBOROS_DSH_CLI_PATH` → 신뢰된 `~/.ouroboros/config.yaml`의 `orchestrator.dsh_cli_path` → `PATH`의 `dsh-acp-demo`입니다. `command -v`는 마지막 경로만 확인합니다. [main factory](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/factory.py#L297-L305) · [main 설정 우선순위](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/loader.py#L1416-L1438) · [release factory](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/factory.py#L297-L305) · [release 설정 우선순위](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/config/loader.py#L1412-L1434).

### 신뢰한 composition과 인증을 지정하기 {#dsh-composition-auth}

`dsh-acp-demo`에는 Cordis composition 파일이 필수입니다. 경로는 `OUROBOROS_DSH_CONFIG_PATH` → 신뢰된 `~/.ouroboros/config.yaml`의 `orchestrator.dsh_config_path` 순으로 선택되며, 둘 다 없으면 child process를 시작하지 않고 fail-closed 합니다. Composition 경로는 **절대 경로**여야 하며, 그 파일과 파일 위치에서 해석되는 plugin/package를 신뢰해야 합니다. 이 composition은 Node process에 어떤 plugins를 로드할지 고르며 그 plugin 코드를 실행할 수 있습니다. 상대 경로는 `invalid_config`로 process 시작 전에 거절됩니다. Composition이 있는 곳에서 dsh의 `node_modules` 또는 workspace가 해석 가능한지도 확인하세요. [main 설정 우선순위](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/loader.py#L1441-L1463) · [main 필수 경로 검사](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/dsh_acp_client.py#L105-L123) · [release 설정 우선순위](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/config/loader.py#L1437-L1459) · [release 필수 경로 검사](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/dsh_acp_client.py#L105-L123).

환경 변수는 `dsh-acp-demo`를 포함한 Ouroboros 시작 환경에서 지정합니다. 예를 들어 trusted shell에서 다음 변수를 설정할 수 있습니다. 두 경로는 절대 경로로 지정하고, 실제 파일 위치로 바꾸세요.

```sh
export OUROBOROS_DSH_CLI_PATH=/absolute/path/to/dsh-acp-demo
export OUROBOROS_DSH_CONFIG_PATH=/absolute/path/to/cordis.yml
```

대신 경로는 `~/.ouroboros/config.yaml`의 다음 키에 지정할 수 있습니다. 기존 YAML 전체를 덮어쓰지 말고 신뢰된 설정에 필요한 키만 병합하세요.

```yaml
llm:
  backend: dsh
orchestrator:
  dsh_cli_path: /absolute/path/to/dsh-acp-demo
  dsh_config_path: /absolute/path/to/cordis.yml
```

두 `OUROBOROS_DSH_*_PATH` 값은 project `.env`에서 신뢰하지 않는 입력으로 차단됩니다. Composition 경로는 실행할 plugin tree를 선택하므로 repository가 실행 파일이나 composition을 바꾸게 두지 마세요. [main denylist](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/untrusted_env.py#L98-L111) · [release denylist](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/config/untrusted_env.py#L95-L108).

Composition이 지정한 provider 인증 정보도 같은 Ouroboros 시작 환경에서 접근 가능해야 합니다. 일반적인 예는 `DEEPSEEK_API_KEY`지만 실제 변수 이름은 trusted composition이 정합니다. 값을 출력하지 말고 해당 프로세스가 읽을 수 있는지 presence만 확인하세요. 예를 들어 composition이 `DEEPSEEK_API_KEY`를 요구할 때는 다음처럼 값 없이 확인할 수 있습니다.

```sh
test -n "${DEEPSEEK_API_KEY:-}" && echo "DEEPSEEK_API_KEY is set" || echo "DEEPSEEK_API_KEY is missing"
```

Ouroboros는 일반 환경을 child에 넘기면서 자체 runtime/backend selector 일부만 제거합니다. DSH에서 키가 없거나 거부되면 전용 `auth failed` 분류가 아니라 보통 ACP/RPC model 오류로 나타날 수 있으므로, 오류 문구 하나로 원인을 단정하지 마세요. [main child environment/오류 처리](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/dsh_acp_client.py#L95-L108) · [release](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/providers/dsh_acp_client.py#L95-L108).

### 별도 runtime과 함께 선택하기

MCP 서버를 시작하는 경우 제품 문서의 예시는 다음과 같습니다. `claude-cli`가 설치·인증된 executable runtime이 아닐 경우 실제 환경에서 지원되는 runtime(예: `codex`, `opencode`)을 선택합니다. `--runtime`은 별도 작업 실행 경로이며 `dsh`로 바꾸지 않습니다.

```sh
ouroboros mcp serve --runtime claude-cli --llm-backend dsh
```

같은 backend는 trusted user config의 `llm.backend: dsh` 또는 시작 process의 `OUROBOROS_LLM_BACKEND=dsh`로 지정할 수도 있습니다. CLI와 config에는 runtime 해석 alias `deepseek_harness` 대신 `dsh`를 사용합니다. 이 예시는 설정 위치와 명령 형태만 보여 주며 실제 실행·연결·모델 호출의 성공 출력은 아닙니다. [main guide: backend/runtime](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/guides/deepseek-harness.md#L131-L159) · [release guide](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/docs/guides/deepseek-harness.md#L131-L159).

### 오류가 나면 처음 확인할 것 {#dsh-first-checks}

- `dsh-acp-demo` spawn/command not found: 위의 `command -v`를 **서버를 실제로 띄우는 같은 환경**에서 확인하세요. `orchestrator.dsh_cli_path`를 썼다면 사용자 설정의 값이 실행 가능한 절대 경로인지 검토하되, 경로 전체를 공유하지 않습니다.
- `invalid_config` 또는 composition 오류: `OUROBOROS_DSH_CONFIG_PATH`가 absolute/readable인지, 또는 trusted user config의 `orchestrator.dsh_config_path`가 그 composition을 가리키는지 확인하세요. Project `.env`에 넣지 마세요. composition의 plugin/package resolution 경로도 그 파일 기준으로 점검합니다.
- ACP/RPC model 오류: 같은 실행 환경에서 composition의 provider와 credential 변수 이름을 확인하고 해당 값이 process에 설정됐는지만 확인합니다. 키 값, composition 전체, 환경 전체를 출력하거나 붙여넣지 마세요.

DSH composition이 provider와 model을 고릅니다. ACP 응답은 model 이름과 token count를 제공하지 않아 Ouroboros가 `dsh-composition` 및 0-token usage를 표시할 수 있습니다. 이를 호출 없음이나 비용 없음으로 해석하지 마세요. 실제 사용량·요금은 composition이 연결한 provider의 기록에서 확인해야 하며, 여기서는 모델 호출이나 비용을 측정하지 않았습니다. main과 release `0.59.9`에서 소스·문서 계약을 대조했을 뿐, 이 환경의 DSH binary 설치, composition, credential, host 연결, 모델·청구 동작은 시험하지 않았습니다. [main model/usage note](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/guides/deepseek-harness.md#L161-L166) · [release guide](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/docs/guides/deepseek-harness.md#L161-L166).

## Zcode로 시작·평가·실행하기

고정 소스의 [Zcode 안내](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-guides/zcode.ko.md) 기준으로 ZCode 앱 또는 실행 가능한 `zcode`, 해당 공급자 인증 및 유효한 `~/.zcode/cli/config.json`의 문자열 `model.main`이 필요하다. 데스크톱에서 모델을 선택했다고 CLI용 설정이 자동 생성되는 것은 아니다. 독립 `.cjs`에는 호환되는 Node가 필요하고 공식 macOS 앱 번들은 포함된 Electron/Node를 사용한다. 이 요구사항은 원본 안내의 계약이며 이 환경에서 Zcode 설치·인증을 확인한 것은 아니다. 자격증명을 명령·문서·로그에 적지 않는다. `ouroboros setup --runtime zcode`는 설정을 변경할 수 있으므로 실행 전에 [호스트 설정](/docs/setup-host-detail/)을 확인한다.

다음 명령은 연결 검사나 dry-run이 아니라 모델 사용과 작업 실행으로 이어질 수 있다. 실제 사용 전에 실행 위치와 권한·비용을 확인한다.

```bash
ouroboros zcode start "작은 CLI를 만들고 테스트하기"
ouroboros zcode qa ./draft.md --artifact-type document --quality-bar "명확하고 정확하면 PASS"
ouroboros zcode run ./seed.yaml --project-dir /path/to/project
```

| 명령 | 입력과 실제 위임 | 결과와 경계 |
| --- | --- | --- |
| `start` | 선택적 과제 설명 또는 `--resume INTERVIEW_ID`, 존재하는 `--state-dir`. 인터뷰 LLM 백엔드와 후속 작업 런타임을 모두 Zcode로 지정한다. | 인터뷰·Seed와 실행 인계는 [첫 실행](/docs/first-run-detail/)의 확인 절차를 따른다. `ouroboros zcode "과제"` 축약도 지원하지만 `start`를 명시하면 하위 명령명과 혼동을 피한다. |
| `qa` | 텍스트 또는 파일 경로, 선택적인 `--quality-bar`, `--artifact-type`, `--reference`, `--pass-threshold`. 이 프로세스에서 LLM 백엔드를 Zcode로 지정해 일반 QA에 위임한다. | 결과의 PASS 여부·근거·점수를 확인한다. [QA 안내](/docs/qa-detail/)의 종료 코드와 검증 범위가 적용되며 모델 평가가 실행·보안의 증거는 아니다. |
| `run` | 존재하고 읽을 수 있는 Seed YAML, 선택적인 `--project-dir`, `--resume`, `--no-qa`, `--sequential`, `--max-decomposition-depth`. 실행 런타임을 Zcode로 지정한다. | orchestrator 실행으로 위임하며 프로젝트 변경이 생길 수 있다. `--no-qa`는 실행 후 QA를 생략한다. 이 wrapper는 `start`·`qa`와 달리 LLM 백엔드를 Zcode로 강제하지 않으므로 평가·작성 백엔드도 같다고 가정하지 않는다. 진행과 재개는 [상태](/docs/progress-detail/)·[복구](/docs/recovery-detail/)를 따른다. |

`ozo`는 같은 앱을 가리키는 별도 콘솔 진입점으로 소스에 선언돼 있으나 설치한 패키지에서 제공되는지 확인한다. 일반 경로 해석은 생성자 경로, 환경 변수, 저장된 `orchestrator.zcode_cli_path`, macOS 앱 기본 경로, PATH 순이다. **다만 위 `zcode`·`ozo` 편의 명령은 환경 변수가 비어 있고 macOS 기본 앱 경로가 존재하면, 저장된 설정을 확인하기 전에 그 기본 경로를 환경 변수로 채운다.** 유효한 기본 경로는 따라서 저장된 다른 CLI 경로보다 먼저 선택될 수 있다. 원하는 경로가 있다면 실행 전 `OUROBOROS_ZCODE_CLI_PATH`를 명시하고, 경로와 선택된 바이너리를 확인한다. 실제 해석에서는 읽기 불가능하거나 실행할 수 없는 경로를 제외할 수 있다([경로 설정 로더](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/config/loader.py)). 공급업체의 CLI 출력 계약은 안정적으로 공개된 것이 아니며 원본 안내가 관찰한 버전에 한정된다. 위 설명은 [wrapper 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/cli/commands/zcode.py) 및 기존 대역 단위 테스트 14개 통과를 근거로 한다. 실제 Zcode 바이너리·인증·인터뷰·QA·작업 실행은 시험하지 않았다.

## 권한과 재개는 기능별로 다르다

원본 [기능표](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/runtime-capability-matrix.md)는 실행 인자의 전달 수준을 `native`(직접 적용), `translated`(다른 방식으로 변환), `ignored`(적용하지 않음)로 구분한다. 표는 일부 신규 백엔드를 열에 포함하지 않으므로 개별 안내와 구현을 함께 봐야 한다.

- Codex, Gemini, Goose, 기본 Copilot CLI, OpenCode, Hermes의 도구 허용 목록은 표에서 일부 프롬프트 안내로 변환된다. 이는 강제적인 샌드박스나 보안 경계가 아니다. 실제 호스트·OS·런타임의 권한을 따로 설정한다.
- 고정 CLI 어댑터의 빈 목록 처리도 같지 않다. Codex CLI는 `tools=[]`를 받으면 도구를 사용하지 말라는 **프롬프트 안내**를 넣지만, OpenCode CLI는 빈 목록이면 도구 안내를 추가하지 않는다. `tools=None`과 빈 목록도 구별되는 경로이므로 목록만 보고 도구가 운영체제 수준에서 차단됐다고 판단하지 않는다. 이는 [Codex 프롬프트 구성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/codex_cli_runtime.py), [안내 생성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/tooling_guidance.py), [OpenCode 프롬프트 구성](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/opencode_runtime.py)의 정적 대조이며 실제 호스트 권한과 도구 호출을 시험하지 않았다.
- OMP는 문서상 도구 제한을 네이티브 인자로 전달하지만 승인 모드는 메타데이터로만 보존한다. Pi는 바이너리 기능 탐지에 따라 네이티브 제한을 사용하며, 빈 목록에 필요한 `--no-tools`를 사용할 수 없으면 작업을 시작하지 않고 실패하도록 문서화돼 있다. 모든 버전의 바이너리가 동일하다고 가정하지 않는다.
- 원본 표는 Claude·Codex·OpenCode·Hermes·Pi·OMP의 네이티브 재개를 기술하지만 Gemini·Copilot은 제공하지 않고 Kiro는 호출자가 세션 ID를 제공해야 하는 부분 지원으로 설명한다. 이 표의 Codex 설명을 `codex_mcp` 작업자에 일반화하면 안 된다. `codex_mcp`의 세션은 서버 프로세스에 묶여 있어 해당 연결이 닫힌 뒤에는 재개할 수 없다. [작업자 구현](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/codex_mcp_runtime.py) Ouroboros 수준의 체크포인트와 런타임의 네이티브 세션 재개는 다르다. GJC에 관한 원본 표의 재개 행과 능력 설명은 서로 일치하지 않으므로 해당 판본 구현을 확인하기 전 보장하지 않는다.
- ACP Copilot은 실험적이며 기본 CLI와 도구 제한·권한 처리 및 이벤트 계약이 다르다. 기능표에서 ACP의 `structured_output`은 구조화 이벤트를 뜻하며 출력 JSON 스키마 강제와 같지 않다.

## 설치와 점검

1. [설치와 첫 실행](/docs/first-run-detail/)을 읽고 독립 CLI와 호스트 플러그인 중 사용할 경로를 선택한다. `setup`은 호스트 설정과 파일을 변경할 수 있으므로 해당 안내에서 대상 경로를 확인한다.
2. 각 실행 파일의 `--version`, `ouroboros --help`, 사용 진입점의 `--help`로 로컬 설치를 확인한다. 이는 계정 인증이나 작업 성공을 증명하지 않는다. 자격 증명 값을 출력하거나 문서에 기록하지 않는다.
3. 사용할 워크스페이스·샌드박스·네트워크·도구 승인 경계를 확인하고, 필요하면 작은 읽기 전용 실행으로 연결과 권한을 검증한다. 이 실행도 모델 사용과 비용을 발생시킬 수 있다.
4. 중단된 작업은 [복구 안내](/docs/recovery-detail/)에 따라 세션·런타임·작업 디렉터리를 확인한다. 도구별 네이티브 재개가 불가능하면 이어진 대화 문맥이 있다고 추정하지 않는다.

**검증 범위:** 고정 커밋의 백엔드 등록, 런타임 기능표와 Claude·Codex·host·Megacode 안내를 정적으로 대조했다. 각 바이너리 설치, 실제 인증, 모델 호출, 플랫폼별 성공과 보안 격리는 이번 페이지 작성 중 검증하지 않았다. 원본 표의 dry-run 관련 일반화는 [첫 실행 안내](/docs/first-run-detail/)의 제한과 대조한다.
