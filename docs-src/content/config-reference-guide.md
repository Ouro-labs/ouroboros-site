# 설정 참조

런타임, 모델, 실행·평가와 저장 설정을 확인하는 입구입니다. 이 페이지는 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)의 소스 기준이며 설치된 패키지와 호스트 서버의 설정·버전은 다를 수 있습니다. 현재 설치의 `ouroboros config --help`와 각 하위 명령 도움말을 먼저 확인하세요.

전체 필드와 환경 변수는 [고정 제품 설정 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/config-reference.md), 선언과 검증은 [설정 모델](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/models.py) 및 [로더](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/loader.py)를 참고합니다. 기본값·우선순위는 필드와 호출 경로에 따라 달라질 수 있으며 이 페이지는 모든 설정 조합의 실행 검증이 아닙니다.

| 알고 싶은 것 | 확인할 곳 | 사용 시 주의 |
| --- | --- | --- |
| 현재 설정과 유효성 | `ouroboros config show`, `ouroboros config validate` 및 각 `--help` | 출력에 경로 등 민감한 정보가 있을 수 있음. 검증 성공이 실제 인증·모델 호출 성공을 뜻하지 않음 |
| 실행 런타임 | 제품 설정 참조의 `orchestrator`와 런타임별 안내 | 호스트가 실행하는 MCP 서버와 독립 CLI는 다른 설정을 사용할 수 있음 |
| 인터뷰·평가 모델 | `llm`, `models`, `evaluation` 및 환경 변수 설명 | 인터뷰용 모델과 작업 실행 런타임은 별도. 적용 우선순위와 실제 선택을 확인 |
| 저장과 로그 | `persistence`, `logging`, 파일 구조 | 설정 선언만으로 모든 작업·호스트의 저장 또는 로그 부재를 보장하지 않음 |
| 실행과 권한 | `execution`, `boundary` 및 런타임 문서 | 특정 옵션이 모든 에이전트·외부 도구를 격리한다고 가정하지 않음 |
| 진단 | `ouroboros status health`, `ouroboros doctor install` | 각 행의 범위와 실패를 확인. 출력에 launcher 인자가 포함될 수 있음 |

예를 들어 독립 CLI 설정을 확인할 때는 다음처럼 먼저 도움말과 현재 상태를 읽습니다. 화면 출력은 실제 환경에 따라 다르며 비밀값·개인 경로를 가린 뒤 공유하세요.

```bash
ouroboros config show --help
ouroboros config show
ouroboros status health
```

불리언 설정은 입력 전에 기존 설정을 안전하게 보존하고 `true` 또는 `false`만 사용하세요. 같은 설치·설정 환경에서 저장된 값을 다시 확인합니다. 고정 release `0.59.9`는 기존 값, 또는 기존 값이 없거나 `null`일 때 참조하는 schema 기본값이 불리언인 경우 `true`·`1`·`yes` 외 입력을 false로 변환하므로 `on`이나 오타도 false가 될 수 있습니다. 고정 main `592c667f`는 불리언 입력을 Pydantic으로 검증해 유효하지 않은 값을 거부합니다. 이 설명은 해당 코드 경로의 정적 대조이며 설치판의 동작은 별도 확인하세요. [main 변환](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/config.py#L1147-L1168) · [release 변환](https://github.com/Q00/ouroboros/blob/5f5fca90662861201ff0a26f502edd22b272c4c6/src/ouroboros/cli/commands/config.py#L1147-L1171)

`config init`, `config set`, `setup`, refresh와 직접 파일 편집은 설정이나 파일을 바꿀 수 있습니다. 적용 대상과 기존 내용을 확인·보존하고, 변경 후 같은 환경에서 결과를 다시 검사하세요. 설정 검증 오류가 나면 다른 `ok` 행만 보고 전체가 정상이라고 판단하지 않습니다. 키·토큰을 문서나 채팅에 넣지 마세요.

[AI 진단 안내](/docs/ai-troubleshooting/)는 설정·인증 오류의 실무 순서입니다. [기존 설정 필드 색인](/docs/config-reference-detail/)은 이전 고정 소스 `722172ef`의 스키마를 추출한 것으로, 현재 main이나 공개 패키지의 동등성을 증명하지 않습니다. 이 페이지의 명령은 설명 예시이며 실제 사용자 설정을 변경하거나 모델을 호출해 검증한 결과가 아닙니다.
