# Python 공개 API 대응과 미검증 범위

!!! warning "판본과 검증 범위"
    이 대응표는 제품 소스 [`722172ef`](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2)를 2026-11-04에 정적으로 추출한 자료입니다. 제품 main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0), 공개 패키지 `0.59.9`, 현재 설치 환경은 서로 다를 수 있으며 최신 설치의 전체 심벌·호환성을 검증하지 않았습니다. 표에서 연결하는 고정 정의와 현재 설치 버전을 별도로 확인하세요. 일부 합성 시험의 재현 자료는 공개되지 않았고 실제 호스트·모델·운영 환경이나 모든 조합을 입증하지 않습니다.


기준: 2026-11-04. 고정 [Q00/ouroboros 722172ef](https://github.com/Q00/ouroboros/tree/722172ef096767583679d04aef5e847458fee6b2); 설치 패키지와 다른 판본일 수 있다. [Python 사용 예제](/docs/python-api-detail/), [MCP 연결](/docs/integration-detail/), [판본 차이](/docs/version-guide/#version-scope)와 함께 읽는다.

아래는 고정 소스의 `ouroboros.core`와 `ouroboros.mcp`의 `__all__` 및 공식 MCP API가 명시한 client/server 패키지 공개 표면을 정적 추출한 **탐색 목록**이다. tools/resources는 공식 API에 명시된 세 이름만 포함하며 이 패키지들의 나머지 export, 다른 Ouroboros 패키지의 전체 export 또는 내부 API 전체를 열거하지 않는다. 재내보내기 선언과 정의 위치를 표시하며, import·호출·호환성을 모두 실행 검증했다는 뜻이 아니다. 공식 [Core API](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/core.md), [MCP API](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/mcp.md)에도 소스와 차이가 있을 수 있으므로 고정 구현과 함께 확인한다.

**문서 언급**은 이 페이지의 설명 절과 다른 페이지에서 심벌 이름의 정확한 독립 문자열을 기계적으로 찾은 것일 뿐 해당 심벌의 모든 사용법이나 의미를 검증했다는 뜻이 아니다. 최대 세 페이지를 표시하며, `—`는 이 검색에서 찾지 못했다는 뜻이지 기능이 없거나 다른 이름으로 설명되지 않았다는 뜻이 아니다. 아래 정의 위치를 확인하고 설치 버전에서 재검증한다.

## `ouroboros.core` (66개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `Result` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py) | [python-api](/docs/python-api-detail/), [integration](/docs/integration-detail/), [mcp-inventory](/docs/mcp-reference-detail/) |
| `EventPayload` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py) | — |
| `CostUnits` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py) | — |
| `DriftScore` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/types.py) | — |
| `ControlContract` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/control_contract.py) | [이 문서 설명](#python-control-contract), [architecture](/docs/architecture-detail/) |
| `Directive` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/directive.py) | [이 문서 설명](#python-control-contract), [architecture](/docs/architecture-detail/) |
| `ConductorActorMode` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/conductor.py) | — |
| `ConductorDecisionPhase` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/conductor.py) | — |
| `ConductorDirective` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/conductor.py) | — |
| `ConductorEffect` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/conductor.py) | — |
| `EngineOwnershipState` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/conductor.py) | — |
| `EfficiencyMode` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py) | — |
| `FrugalityAssurance` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py) | — |
| `ResolvedExecutionPreferences` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py) | [이 문서 설명](#python-execution-preferences) |
| `resolve_execution_preferences` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py) | [이 문서 설명](#python-execution-preferences) |
| `SessionSignal` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | [이 문서 설명](#python-session-signal) |
| `SessionSignalCapabilities` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | [이 문서 설명](#python-session-signal) |
| `SessionSignalCapabilityError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | [이 문서 설명](#python-session-signal) |
| `SessionSignalContractEffect` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | — |
| `SessionSignalMode` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | — |
| `SessionSignalSource` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | — |
| `SessionSignalState` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | — |
| `resolve_session_signal_mode` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | [이 문서 설명](#python-session-signal) |
| `derive_session_signal_id` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py) | — |
| `OuroborosError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py) | [python-api](/docs/python-api-detail/) |
| `ProviderError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py) | [python-api](/docs/python-api-detail/) |
| `ConfigError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py) | — |
| `PersistenceError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py) | — |
| `ValidationError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/errors.py) | [python-api](/docs/python-api-detail/) |
| `Seed` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | [이 문서 설명](#python-workflow-context), [이 문서 설명](#python-requirement-candidates), [python-api](/docs/python-api-detail/) |
| `SeedMetadata` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | [python-api](/docs/python-api-detail/) |
| `InvestmentSpec` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | — |
| `OntologySchema` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | [python-api](/docs/python-api-detail/) |
| `OntologyField` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | — |
| `EvaluationPrinciple` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | — |
| `ExitCondition` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | — |
| `derive_semantic_ac_key` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed.py) | — |
| `OntologyConcept` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed_contract.py) | — |
| `OntologyLens` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed_contract.py) | — |
| `SeedContract` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/seed_contract.py) | [seed-format](/docs/seed-format-detail/) |
| `CandidateContentSource` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | — |
| `CandidateResolution` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | — |
| `ConfirmationAuthority` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | — |
| `RequirementCandidate` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | [이 문서 설명](#python-requirement-candidates) |
| `RequirementDistillation` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | [이 문서 설명](#python-requirement-candidates) |
| `RequirementEvidence` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | [이 문서 설명](#python-requirement-candidates) |
| `RequirementEvidenceKind` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | — |
| `RequirementSection` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | — |
| `evaluate_promotion` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py) | [이 문서 설명](#python-requirement-candidates) |
| `WorkflowContext` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | [이 문서 설명](#python-workflow-context) |
| `ContextMetrics` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | — |
| `CompressionResult` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | — |
| `FilteredContext` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | [이 문서 설명](#python-workflow-context) |
| `count_tokens` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | — |
| `count_context_tokens` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | — |
| `get_context_metrics` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | [이 문서 설명](#python-workflow-context) |
| `compress_context` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | [이 문서 설명](#python-workflow-context) |
| `compress_context_with_llm` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | — |
| `create_filtered_context` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) | [이 문서 설명](#python-workflow-context) |
| `GitWorkflowConfig` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/git_workflow.py) | [이 문서 설명](#python-git-workflow) |
| `detect_git_workflow` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/git_workflow.py) | [이 문서 설명](#python-git-workflow) |
| `is_on_protected_branch` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/git_workflow.py) | [이 문서 설명](#python-git-workflow) |
| `InputValidator` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/security.py) | [python-api](/docs/python-api-detail/) |
| `mask_api_key` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/security.py) | [python-api](/docs/python-api-detail/) |
| `validate_api_key_format` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/security.py) | [python-api](/docs/python-api-detail/) |
| `sanitize_for_logging` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/security.py) | [python-api](/docs/python-api-detail/) |

## `ouroboros.mcp` (34개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `MCPError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | [integration](/docs/integration-detail/), [mcp-inventory](/docs/mcp-reference-detail/) |
| `MCPClientError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | — |
| `MCPServerError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | [python-api](/docs/python-api-detail/) |
| `MCPAuthError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | — |
| `MCPTimeoutError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | — |
| `MCPConnectionError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | [integration](/docs/integration-detail/) |
| `MCPProtocolError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | — |
| `MCPResourceNotFoundError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | — |
| `MCPToolError` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/errors.py) | [python-api](/docs/python-api-detail/) |
| `TransportType` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `ContentType` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPCacheScope` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPServerConfig` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPToolDefinition` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPToolParameter` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPToolResult` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/), [integration](/docs/integration-detail/) |
| `MCPContentItem` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPResourceDefinition` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPResourceContent` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPResourceResult` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPPromptDefinition` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPPromptArgument` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | [python-api](/docs/python-api-detail/) |
| `MCPPromptMessage` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPPromptResult` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPPeerIdentity` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPCapabilities` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPServerInfo` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPServerSnapshot` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPRequest` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `MCPResponse` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `JSONScalar` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `JSONValue` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `JSONObject` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |
| `JSONSchema` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/types.py) | — |

## `ouroboros.mcp.client` (3개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `MCPClient` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/protocol.py) | — |
| `MCPClientAdapter` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/adapter.py) | [python-api](/docs/python-api-detail/) |
| `MCPClientManager` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/manager.py) | [python-api](/docs/python-api-detail/), [integration](/docs/integration-detail/) |

## `ouroboros.mcp.server` (4개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `MCPServer` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py) | [python-api](/docs/python-api-detail/) |
| `ToolHandler` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py) | — |
| `ResourceHandler` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/protocol.py) | — |
| `MCPServerAdapter` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py) | [python-api](/docs/python-api-detail/) |

## `ouroboros.mcp.tools` (2개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `OUROBOROS_TOOLS` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/definitions.py) | — |
| `ToolRegistry` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/tools/registry.py) | [python-api](/docs/python-api-detail/) |

## `ouroboros.mcp.resources` (1개)

| 심벌 | 고정 정의·재수출 근거 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `OUROBOROS_RESOURCES` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/resources/handlers.py) | — |

## 공식 MCP 참조의 추가 심벌

이 항목은 위 패키지 `__all__` 표와 별도로 공식 MCP 문서에 이름이 명시된 구현이다. 재수출 여부와 런타임 사용 가능성을 자동으로 뜻하지 않는다.

| 심벌 | 고정 구현 | 사이트 내 이름 언급 |
| --- | --- | --- |
| `create_mcp_client` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/client/adapter.py) | — |
| `create_ouroboros_server` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/mcp/server/adapter.py) | — |
| `MCPConnectionConfig` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_config.py) | — |
| `MCPClientConfig` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_config.py) | — |
| `load_mcp_config` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_config.py) | — |
| `ToolConflict` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_tools.py) | — |
| `MCPToolInfo` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_tools.py) | — |
| `MCPToolProvider` | [소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/orchestrator/mcp_tools.py) | [python-api](/docs/python-api-detail/), [integration](/docs/integration-detail/) |

## 다음 검증 우선순위

1. `MCPServerAdapter`는 [합성 stdio 서버 예제](/docs/python-api-detail/)에서 등록·연결·정상 및 오류 호출·종료를 시험했다. `MCPClientManager`와 `MCPToolProvider`는 [한 서버 합성 예제](/docs/python-api-detail/)에서 설정·연결·호출·정리를 시험했다. 여러 합성 stdio 서버의 충돌·종료 오류 사례는 [관찰 범위](/docs/python-api-detail/)에서 다룬다. 실제 서버 및 인증은 미검증이다. 실제 서버 인증·외부 도구 효과도 미검증이다.
2. `MCPToolProvider`, 설정 로딩, 리소스·프롬프트 타입 및 오류 계층은 [MCP API](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/docs/api/mcp.md)와 고정 구현을 대조한다. 공식 문서의 모든 메서드와 인자, 프로토콜 동작을 이 표만으로 다뤘다고 주장하지 않는다.
3. `ouroboros.core`의 control·requirement 관련 export는 이름과 정의 위치만 파악한 항목이 많다. context의 일부는 아래 사용 경계를 참고한다. 호출 계약·부작용·버전 호환성을 관련 테스트와 격리 예제로 확인하고, 공개 API 안정성은 명시된 근거가 있을 때만 주장한다.

표는 고정 Git 객체를 AST로 읽은 정적 인벤토리다. 생성에 사용한 내부 자료는 공개되지 않았다. 외부 서비스·모델·인증이나 모든 import 조합을 시험하지 않았다. 배포판, 선택 의존성 및 다른 호스트에서는 심벌이나 동작이 다를 수 있다.

<a id="python-workflow-context"></a>
## Python 워크플로 컨텍스트와 하위 작업 입력

고정 소스의 `ouroboros.core`는 `WorkflowContext`, `create_filtered_context`, `get_context_metrics`, `compress_context` 등을 내보낸다. 이들은 Python에서 구성 요소를 조합하기 위한 API이며 호스트 간 보안 격리나 자동 호출을 보장하지 않는다. 다음은 네트워크·모델 없이 입력을 구성하는 예다.

```python
from ouroboros.core import WorkflowContext, create_filtered_context

parent = WorkflowContext(
    seed_summary="문서 검색 개선",
    current_ac="전체 기준",
    key_facts=["검색은 로컬 인덱스를 사용", "배포는 승인 필요"],
    history=[{"step": "인덱스 확인"}],
)
child = create_filtered_context(parent, "검색 결과 검증", ["검색"])
assert child.current_ac == "검색 결과 검증"
assert child.relevant_facts == ["검색은 로컬 인덱스를 사용"]
```

키워드는 대소문자를 무시한 부분 문자열 OR 검색이다. 키워드가 없거나 빈 리스트이면 모든 사실을 새 리스트에 담는다. 최근 이력은 마지막 3개를 **리스트로만 얕게 복사**하므로, 이력 항목의 딕셔너리나 그 안의 객체를 수정하면 원본도 바뀔 수 있다. `FilteredContext`의 frozen 선언은 필드 재할당을 막을 뿐 내부 리스트·객체를 얼리지 않는다. 신뢰 경계나 변경 격리가 필요하면 전달 전에 중첩 자료를 복사하고 별도의 권한 경계를 적용한다. 반대로 사실 리스트 자체를 추가·삭제해도 원본의 사실 리스트는 바뀌지 않는다.

`get_context_metrics`는 토큰 수가 **100,000 초과** 또는 생성 후 **6시간 초과**일 때 `needs_compression`을 표시한다. 길이 기준은 추정치이며 LiteLLM을 불러올 수 없거나 계수에 실패하면 문자 수의 4분의 1을 사용한다. 직접 `compress_context`를 호출하면 모델 요약을 시도하므로 비용과 데이터 전송이 발생할 수 있다. 요약이 성공하면 Seed·현재 AC·모든 key facts와 최근 3개 이력을 포함하지만, 실패 시 반환되는 `method="truncate"` 결과에는 Seed·현재 AC와 앞의 사실 최대 5개만 남고 이력이 없다. 결과 객체와 실제 내용을 확인하고 원본 보존·복구 정책을 별도로 정해야 한다. 이 설명은 [고정 소스](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/context.py) 기준이며 모든 호출 경로의 자동 압축 여부를 뜻하지 않는다.

2026-11-04 합성 시험에서 대소문자 필터, 필드 재할당 차단, 중첩 이력의 원본 공유 및 토큰 100,000/100,001과 7시간 조건을 확인했다. 시간의 정확한 6시간 경계, 실제 토큰 계산기·모델 요약·다른 프로세스 전달은 시험하지 않았다. 재현 자료는 공개되지 않았다. 고정 소스 archive의 `context.py` Git blob이 `2eedd0d1e44f647e092c0e6511f7a334ae159323`으로 일치했고, 기존 가상환경을 사용했으므로 의존성 전체의 lock 일치는 미검증이다.

<a id="python-requirement-candidates"></a>
### 요구사항 후보의 출처와 Seed 반영 판정

`RequirementCandidate`와 `RequirementEvidence`는 인터뷰에서 파생된 **Seed 이전 후보**를 표현한다. 이것만으로 인터뷰 원문이나 사용자의 결정을 대체하거나 실행 가능한 Seed를 생성하지 않는다. 고정 소스의 [`evaluate_promotion`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/requirement_candidate.py)은 후보가 나열한 `evidence_ids`를 증거에 대조해 출처를 다시 결정하고, 각 후보의 `decisions`와 `promoted`·`omitted`·`blockers`를 반환한다. 호출자는 결과와 원본 근거를 함께 검토해야 한다.

- 증거가 없거나 ID가 누락된 계보는 필수 후보라면 차단하고 선택 후보라면 제외한다. 유효한 계보의 `conflicting`은 필수 여부와 관계없이 차단한다. `unknown` 또는 미확정 후보는 필수일 때 차단하고 선택일 때 제외한다.
- 사용자 진술·참조 유래·모델 추론은 승격에 사용자 확인이 필요하다. 저장소 증거 유래는 `context`나 `existing_constraint`에서 저장소 증거 확인 또는 사용자 확인으로 승격할 수 있지만, `goal` 등 다른 섹션은 사용자 확인이 필요하다. 여기의 확인 권한은 모델에 입력된 값이며 이 함수가 실제 사람의 확인이나 저장소 사실을 독립 증명하는 것은 아니다.
- `RequirementDistillation.is_current()`는 스키마 버전·입력 revision·fingerprint를 호출자가 제공한 값과 비교한다. `evaluate_promotion()` 자체가 최신 입력과 비교해 낡은 결과를 자동 거부하지는 않는다. 원본 입력을 바꾸면 fingerprint와 revision을 갱신하고 판정 전에 현재성을 검사한다. `is_ready_for_seed`는 **차단 항목이 없는지**만 나타내므로 목표·필수 항목의 완전성이나 실제 Seed 생성 성공을 보장하지 않는다.

2026-11-04 기준 고정 소스와 일치하는 파일 및 기존 가상환경에서 격리 합성 후보 5개를 평가해 저장소 증거 context 승격·goal 차단·선택 미확정 제외·충돌 차단·증거 누락 차단을 확인했다. 재현 자료는 공개되지 않았다. 처음 importlib 실행은 모듈 등록 누락으로 Pydantic 오류가 났으며 `sys.modules` 등록 후 수정·재시험했다. 실제 인터뷰·사용자 확인·Seed 생성·모든 후보 조합이나 의존성 lock 동등성은 검증하지 않았다.

<a id="python-control-contract"></a>
### Python 제어 결정의 형태와 멱등 범위

고정 소스의 [`ControlContract`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/control_contract.py)는 `control.directive.emitted`에 쓰는 결정 데이터의 형태를 검증한다. 이 객체의 생성이나 직렬화만으로 이벤트가 저장되거나 실제 실행이 중단되는 것은 아니다. `directive`에는 문자열이 아니라 `Directive` 열거값을 주며 `is_terminal`은 직접 지정하지 않고 그 열거값에서 유도한다. 이 판본에서 종료 지시는 `CANCEL`과 `CONVERGE`다.

```python
from ouroboros.core import ControlContract, Directive

contract = ControlContract(
    directive=Directive.CANCEL,
    target_type="execution", target_id="exec-example",
    emitted_by="operator", reason="사용자 요청",
    idempotency_key="example-decision-1",
)
assert contract.is_terminal
assert contract.effective_idempotency_key == (
    "execution", "exec-example", "cancel", "example-decision-1"
)
payload = contract.to_event_data()
```

필수 문자열은 앞뒤 공백을 제거하며 빈 값은 거부한다. `target_type`의 정식 권장 목록은 닫힌 허용 목록이 아니므로 임의의 비어 있지 않은 값도 생성 단계에서 허용된다. 키를 생략하면 `effective_idempotency_key`는 `None`이다. 이 튜플은 소비자가 중복을 식별할 때 쓸 수 있는 **계산된 키**로, 객체 자체가 저장·중복 제거·정확히 한 번 실행을 보장하지 않는다. 이벤트 전송과 소비자별 실패 정책은 [아키텍처](/docs/architecture-detail/)를 확인한다.

`extra`는 딕셔너리여야 하지만 중첩 값은 깊이 복사하거나 JSON 호환성을 검사하지 않는다. `to_event_data()`도 중첩 객체를 공유하므로 호출 후 수정이 원본에 반영될 수 있고, JSON으로 변환할 수 없는 값은 이후 직렬화에서 실패할 수 있다. 공유·직렬화 전에 호출자가 자료를 검증하고 필요하면 깊이 복사한다. 2026-11-04 고정 소스의 합성 시험에서 키·종료성·필수 타입과 얕은 복사 및 JSON 비호환 값을 확인했다. 재현 자료는 공개되지 않았다. 실제 이벤트 저장, 소비자 중복 처리 및 다른 버전은 시험하지 않았다.

<a id="python-git-workflow"></a>
### Git 워크플로 감지와 보호 브랜치 판정

[`detect_git_workflow(project_root)`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/git_workflow.py)는 고정 구현에서 지정 디렉터리의 `CLAUDE.md`를 먼저 읽고, 없거나 읽을 수 없을 때 `.claude/CLAUDE.md`를 확인한다. 원본 함수 설명에는 상위 디렉터리를 검색한다고 적혀 있지만 실제 목록은 이 두 경로뿐이다. 첫 파일이 비어 있지 않으면 두 번째 파일과 합치지 않는다. 인식은 자연어 전체의 의미 분석이 아니라 제한된 영어 정규식이다. 감지 결과의 `use_branches`·`auto_pr`은 설정값이며 이 함수 호출이 브랜치 생성·push·PR 생성을 실행하지 않는다. 자동 PR도 `auto`/`automatically`와 특정 표현이 있어야 인식되므로 일반적인 PR 지시만으로 활성화됐다고 가정하지 않는다.

보호 브랜치 추출은 `never commit to …` 등의 대상에 `\w+`를 사용하므로 슬래시나 하이픈이 있는 이름 전체를 보존하지 않을 수 있다. 예컨대 합성 문장 `never commit to release/v1`은 `release/v1`이 아니라 `release`로 추출됐다. 결과를 실제 브랜치 보호 정책으로 취급하지 말고, 복잡한 이름과 지침은 별도로 확인하거나 명시적으로 `GitWorkflowConfig(protected_branches=("release/v1", ...))`를 구성한다. 이 문자열 추출은 첫 파일 우선과 결합되므로 입력 파일과 반환된 `source`·`protected_branches`를 확인해야 한다.

`is_on_protected_branch(project_root, config)`는 실제 `git rev-parse --abbrev-ref HEAD` 결과를 설정된 이름과 비교한다. 브랜치를 확인할 수 없거나 detached HEAD면 **보호된 것으로 반환**한다. 다만 이것은 검사 함수의 결과이지 GitHub 브랜치 보호 규칙이나 다른 호출 경로에서의 강제 적용을 의미하지 않는다. 빈 저장소·비저장소·detached와 정상 feature 브랜치를 격리된 임시 Git 저장소로 시험했고, 상위 파일 무시·두 파일 우선순위 및 슬래시 이름의 부분 추출도 합성 입력으로 확인했다. 고정 commit의 `git_workflow.py` blob `7739ed1b6496760d3aa97390e164109ae691cada`와 시험 파일이 일치했다. 최초 시험은 임시 archive 경로를 잘못 지정해 파일을 열지 못했고 경로를 바로잡아 통과했다. 재현 자료는 공개되지 않았다. 실제 프로젝트·GitHub 보호 규칙·인코딩 오류와 모든 문구는 시험하지 않았다.

<a id="python-execution-preferences"></a>
## Python 실행 선호도 해석

[`resolve_execution_preferences`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/execution_preferences.py)는 전달된 실행 효율·검증 강도를 `ResolvedExecutionPreferences`로 정규화한다. **이 함수의 기본값은 실행 진입점의 기본값과 같다고 가정하지 않는다.** 함수에 `(None, None)`을 직접 주면 `adaptive`와 `observe`가 되고, `("quality_first", None)`이면 `quality_first`와 `off`가 된다. CLI·MCP 경로는 이 함수 전에 설정이나 자체 기본값을 적용할 수 있으므로 해당 [실행 정책](/docs/routing-detail/)과 실제 설정을 확인한다. 고정 MCP `ExecuteSeedHandler`의 합성 plugin 분기에서는 기본 정책을 `quality_first` 대역으로 고정했을 때 payload builder가 `quality_first/off`를, 명시 `adaptive/strict`에는 그 값을 받았고 재개 중 명시 mode 변경은 builder 전에 오류였다. 실제 설정 읽기·plugin·모델·CLI는 이 시험에서 사용하지 않았다. 재현 자료는 공개되지 않았다.

```python
from ouroboros.core import resolve_execution_preferences

prefs = resolve_execution_preferences("adaptive", "strict")
assert prefs.child_model_lowering_enabled
assert prefs.frugality_attention_enabled
assert prefs.strict_baseline_authorized
contract = prefs.to_contract_data()
```

`strict_baseline_authorized`는 강도가 `strict`이고 명시적으로 전달된 경우에만 참이며 추가 비용이 발생할 수 있는 baseline 작업을 허용하는 선호도를 나타낸다. 이것만으로 작업 실행, 비용 상한 또는 검증 통과를 보장하지 않는다. 지원하지 않는 문자열은 `ValueError`다. `to_contract_data()`는 값과 명시 여부를 직렬화한다. 같은 소스의 `execution_preferences_from_contract`는 정확한 세 키와 boolean 명시 여부가 필요하며 잘못된 객체를 `None`으로 반환한다. 저장된 값에 `strict`가 있더라도 명시 여부가 `False`면 `strict_baseline_authorized`는 거짓이다. 실제 호출자가 이 복원 함수를 쓰는지 별도로 확인한다.

2026-11-04 고정 Git 객체의 모듈을 외부 실행 없이 불러 합성 입력으로 기본값·명시 `strict`·`quality_first`·잘못된 모드와 복원된 미명시 `strict`를 확인했다. 실제 모델 선택, 호스트 설정 전달, 추가 비용 또는 모든 입력 조합은 시험하지 않았다.

<a id="python-session-signal"></a>
## Python 세션 신호 계약과 능력 판정

[`SessionSignal`](https://github.com/Q00/ouroboros/blob/722172ef096767583679d04aef5e847458fee6b2/src/ouroboros/core/session_signal.py)은 특정 실행·세션 범위·시도에 대한 신호의 **데이터 계약**이다. 객체를 만드는 것만으로 신호가 저장되거나 작업자에게 전달되지 않는다. `mode`, `source`, `contract_effect`에는 해당 열거값이 필요하며, 본문과 사유는 빈 값·비가시 문자만 있는 값·크기 초과·일부 비밀값 모양을 거부한다. 이 패턴 검사는 모든 비밀값을 찾는 보장이 아니므로 민감 정보를 넣지 않는다. `replace` 또는 명세 변경에는 `user_approval_event_id`가 필요하지만 문자열 존재가 실제 승인 여부를 증명하지는 않는다.

`effective_idempotency_key`는 실행 ID·세션 범위 ID·시도 ID·제공된 키의 튜플이다. 동일 키를 계산하는 것만으로 영속 저장이나 중복 처리가 보장되지는 않는다. `to_event_data()`는 기본적으로 메시지 본문을 포함하며 `from_event_data()`로 재구성할 수 있다. `include_message=False`는 본문 대신 digest만 남기므로 재구성할 수 없다. 본문 포함 데이터를 기록·공유할 때 보존 및 접근 정책을 따로 적용한다. 만료 시간은 시간대가 있어야 하며, 만료 시각과 같은 시점부터 만료다.

`SessionSignalCapabilities()`의 모든 능력은 기본적으로 거짓이다. `resolve_session_signal_mode`는 지원되지 않는 모드를 `SessionSignalCapabilityError`로 거부한다. `redirect`에 명시적으로 `after_turn` fallback이 있고 그 능력이 있을 때만 대체할 수 있으며, redirect 능력이 있으면 그것이 우선한다. `replace`는 abort와 replacement resume 능력을 모두 요구한다. 능력 객체의 선언 자체가 실제 런타임의 전달·중단을 증명하지 않는다. 실제 도구와 생명주기는 [Synapse 안내](/docs/synapse-detail/)를 참고한다.

2026-11-04 고정 Git 객체의 모듈을 격리 합성 입력으로 시험해 본문 포함 왕복, digest 전용 복원 거부, 기본 능력의 거부, 명시 fallback과 redirect 우선, 만료 시각 경계를 확인했다. 재현 자료는 공개되지 않았다. 실제 이벤트 저장·MCP 호출·작업자 전달·승인 및 모든 민감정보 패턴은 시험하지 않았다.
