# LiteLLM 모델 라우팅과 reasoning sampling

기준 제품 판본은 [`Q00/ouroboros` main `592c667f076c3dad7ef68d7844e91480d80135d0`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0)이다. 이 안내는 LiteLLM 어댑터가 요청을 어떻게 구성하는지 설명한다. 모든 공급자 API가 같은 인자를 받아들이거나 같은 결과를 낸다고 보장하지 않으며, 실모델 API 호출로 검증하지 않았다.

## LLM 백엔드와 모델 선택

`llm.backend`는 인터뷰·QA·평가 등 LLM 전용 요청의 백엔드를 고른다. 실행 런타임의 `orchestrator.runtime_backend`와는 별개다. `llm_profiles`에 재사용할 설정을 두고 `llm_role_profiles`에서 논리 역할에 연결한다. 선택된 백엔드의 `providers.litellm.model`로 LiteLLM 모델 ID를 지정할 수 있다. 예를 들어 `openai/o3`는 LiteLLM의 OpenAI 라우트이고 `openrouter/openai/o3`는 OpenRouter 경로다. 두 ID를 같은 직접 OpenAI 요청으로 취급하지 않는다.

```yaml
llm_profiles:
  openai_reasoning:
    temperature: 0.2
    top_p: 0.7
    providers:
      litellm:
        model: openai/o3
        reasoning_effort: high

llm_role_profiles:
  semantic_evaluation: openai_reasoning
```

이 예시에서 `reasoning_effort`는 `low`, `medium`, `high` 중 하나를 지정한다. `xhigh`는 Codex provider profile에 한정되므로 LiteLLM profile에는 쓰지 않는다. 설정 필드와 YAML 구조는 [설정 참조](/docs/config-reference-guide/), 실행 정책과 비용은 [실행 정책 안내](/docs/routing-detail/)를 확인한다. 역할 매핑과 명시 profile의 실제 선택 순서는 아래 [Profile resolution and sampling](#profile-resolution-and-sampling) 절과 [기준 main의 구현](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/profiles.py#L86-L180)에 따른다.

### Profile resolution and sampling

**역할 매핑과 sampling 값 적용은 구분한다.** 이 예시처럼 `llm_role_profiles`로 profile을 연결하면 provider/model과 `reasoning_effort`는 역할 해석에 사용될 수 있지만, profile의 `temperature`와 `top_p`는 역할 매핑만으로 호출 설정에 덮어쓰지 않는다. 이때 요청을 만든 호출자의 `temperature`와 `top_p`가 유지된다. profile의 sampling 값을 명시적으로 적용하려면 호출에서 `CompletionConfig.profile`을 설정해야 한다. 그 경우 provider별 값, 공통 profile 값, 요청 설정값의 순서로 값을 고른다.

요청 model이 profile model보다 우선하는 것은 제한된 조건에서만이다. `role`이 지정되고 `CompletionConfig.profile`은 비어 있으며, 요청의 `model_is_explicit`이 참이고 model 값이 비어 있지 않고 `default`도 아닐 때 role 기반 profile model을 덮어쓴다. 그 조건을 충족하지 않으면 provider별 model, 공통 profile model, 요청 model의 순서로 선택한다. 따라서 `CompletionConfig.profile`을 명시한 경우에는 provider/profile model이 요청 model보다 우선할 수 있다. [`profiles.py`](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/profiles.py#L86-L95) [`resolve_completion_profile`](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/profiles.py#L134-L180)

## reasoning 모델에서 sampling 값이 전달되는 조건

LiteLLM 경로는 모델 ID와 설치된 LiteLLM 모델 메타데이터를 보고 직접 OpenAI reasoning 경로인지 판별한다. 이 판본은 reasoning 계열 ID(`o` 계열, `gpt-5` 계열)를 확인하고, `gpt-5` chat 계열과 OpenRouter 같은 다른 provider prefix는 제외한다. 모델 메타데이터가 `none` reasoning effort를 지원한다고 명시하지 않으면 보수적으로 판단한다.

판별 결과 sampling 제어를 생략해야 하는 요청에서는 adapter가 `temperature`와 `top_p`를 LiteLLM 호출 인자에서 빼고, 설정 파일의 값을 변경하지 않는다. 따라서 설정에 값이 있어도 해당 호출에서는 공급자 쪽 sampling 기본 동작을 따르게 된다. `reasoning_effort`가 지정된 경우 adapter는 이를 LiteLLM에 전달한다. 설정값이 계속 저장돼 있다는 사실만으로 매 요청에 실제 적용됐다고 판단하지 않는다.

main의 단위 사례에는 다음 차이가 있다.

- `openai/o3`, `openai/o4-mini`, `openai/gpt-5-mini`는 `reasoning_effort`가 없을 때도 `temperature`와 `top_p`를 생략한다.
- `openai/gpt-5.4`는 effort가 없거나 `none`이면 둘을 유지하고, `high`처럼 reasoning effort를 요청하면 둘을 생략한다.
- `openai/gpt-4o`, `openai/gpt-5-chat-latest`, `openrouter/openai/o3`는 이 직접 OpenAI reasoning 분기에 포함되지 않는다.

이것은 LiteLLM 어댑터의 요청 구성 조건이지, 해당 모델의 현재 API가 모든 sampling 인자를 거부한다거나 대체 설정이 동일한 출력을 낸다는 보편 규칙이 아니다. 판단에 사용하는 `litellm.model_cost` 메타데이터는 설치된 LiteLLM 버전에 따라 다를 수 있다. 이 main의 `litellm` extra는 Python 3.14 미만에서 LiteLLM `1.91.0`을 고정한다. 다른 판본·런타임은 별도 확인한다.

## Python API의 `json_schema` 형식

`response_format`은 현재 일반 `llm_profiles` YAML 필드가 아니라 Python `CompletionConfig` 요청 옵션이다. LiteLLM 어댑터에 다음처럼 bare schema를 넘기면:

```python
CompletionConfig(
    model="openai/gpt-4o",
    response_format={
        "type": "json_schema",
        "json_schema": {"type": "object", "properties": {"ok": {"type": "boolean"}}},
    },
)
```

Claude 5.5의 직접 Anthropic 경로는 예외다. LiteLLM 어댑터는 OpenRouter 경로가 아닌 Claude 5.5의 `json_object` 및 `json_schema` 요청을 `response_format`으로 보내는 대신 system 지시문으로 바꾼다. 따라서 이 경로는 아래 JSON schema 래퍼 정규화를 거치지 않는다. [`litellm_adapter.py`](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/litellm_adapter.py#L1196-L1212)

그 예외가 아닌 LiteLLM 경로에서는 bare schema를 `{"name": "response", "schema": <schema>}`로 감싼다. 이미 `json_schema.schema`가 dict인 입력은 그대로 둔다. 래퍼 판정은 `name`의 존재가 아니라 내부 `schema` 값이 dict인지에 달려 있다. 이 경우 `strict` 같은 기존 필드는 유지되고 호출자의 원본 dict는 수정되지 않는다. 이는 요청 모양을 맞추는 정규화다. 각 모델/API가 스키마를 강제 준수하거나 응답이 항상 유효하다는 보장은 아니다. [`_litellm_response_format`](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/litellm_adapter.py#L1496-L1517)

## 검증 경계

고정 소스에는 직접 OpenAI 라우트가 로컬 가짜 HTTP endpoint에 보낸 요청을 검사하는 테스트와 bare/already-wrapped `json_schema` 인자를 검사하는 단위 테스트가 있다. 이 페이지 작성 중 해당 테스트나 실제 공급자 API를 실행하지 않았다. 비용·품질·모델별 결과, 현재 계정에서의 접근 가능성은 확인되지 않았다.

참조: [LiteLLM 모델 판별](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/openai_sampling.py), [LiteLLM 요청 구성](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/providers/litellm_adapter.py), [profile 설정 모델](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config/models.py), [로컬 요청 테스트](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/tests/unit/providers/test_openai_reasoning_wire.py), [스키마 래퍼 테스트](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/tests/unit/providers/test_litellm_adapter.py).
