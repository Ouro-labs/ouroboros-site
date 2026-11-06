# MCP 도구 참조

MCP 도구는 호스트 또는 MCP 클라이언트가 서버에 호출합니다. `ooo`는 지원 호스트의 대화 요청이고 `ouroboros`는 독립 터미널 CLI입니다. 아래의 JSON은 **MCP 도구 인자 예시**이며 셸 명령이 아닙니다. 제공되는 도구와 입력 스키마는 서버·런타임·버전에 따라 다르므로 연결된 서버의 도구 목록과 스키마를 우선 확인하세요.

기준 소스는 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)입니다. 전체 도구의 상세 입력은 실제 서버의 도구 발견 결과와 [도구 등록·구현](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools)을 대조합니다. [제품 MCP API 참조](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/api/mcp.md)는 Python API와 일부 도구 계약을 설명하지만 서버의 전체 실시간 스키마를 대체하지 않습니다.

| 목적 | 도구와 입력 | 출력·오류를 읽는 법 | 영향 |
| --- | --- | --- | --- |
| 목표에서 자동 시작 | `ouroboros_start_auto`에 `{"goal": "작업 관리 CLI 만들기"}` | 반환된 job 및 auto session 식별자를 보존하고 이어서 조회. 오류·차단과 최종 실행 결과를 구분 | 인터뷰·모델 호출과 후속 실행이 발생할 수 있음. 대상과 비용을 확인 |
| 백그라운드 상태 | `ouroboros_job_status`에 `{"job_id": "실제 job ID"}` | 같은 job의 상태를 읽고 종료 후 제공되는 `ouroboros_job_result` 확인 | 응답이 지연돼도 중복 실행하지 않음 |
| 세션 상태 | `ouroboros_session_status`의 실제 서버 스키마에 맞는 세션 ID | 관련 상태와 오류·연결된 작업을 확인 | 저장된 상태가 현재 프로세스 생존이나 완료 검증을 증명하지 않음 |
| 설치·연결 진단 | 호스트의 MCP 상태와 오류 확인; 독립 CLI가 있다면 `ouroboros mcp doctor` | 호스트 연결과 별도 CLI 진단을 구분 | 선택적 live probe는 자식 서버를 시작하므로 실행 전 영향 확인 |

예시 ID와 목표는 실제 호출 결과가 아닙니다. 도구 미발견, 스키마 오류 또는 인증 실패가 나면 임의 인자를 추측하지 말고 연결된 서버의 오류와 버전을 확인하세요. `ouroboros_start_auto`의 접수는 Seed 검토·실행·평가 전체의 성공을 뜻하지 않습니다. 자세한 반환과 상태 경계는 [auto 핸들러](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/auto_handler.py), [job 핸들러](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/job_handlers.py), [세션 조회](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/mcp/tools/query_handlers.py)를 참고하세요.

[AI 진단 안내](/docs/ai-troubleshooting/)에는 MCP 실패와 복구 순서가 있습니다. [기존 MCP 색인](/docs/mcp-reference-detail/)과 [스키마 캡처](/docs/mcp-schema-snapshot-detail/)는 이전 고정 소스 `722172ef` 및 특정 환경 기준입니다. 현재 서버의 도구 목록이나 전체 호스트의 실사용 검증으로 취급하지 마세요.
