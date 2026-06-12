# Validation

## Proof Strategy

Use mocked unit tests for provider routing, VNstock formatting, Vietnam news
normalization, and LLM provider registries. Live APIs remain opt-in.

## Test Plan

| Layer | Cases |
| --- | --- |
| Unit | Vietnam symbol detection, VNstock adapter signatures, routing, news filtering, provider env/model/base URLs |
| Integration | Existing dataflow and CLI provider tests |
| E2E | Not required for this provider adapter change |
| Platform | Git status review after code changes |
| Performance | Source limits and dedupe keep news prompts bounded |
| Logs/Audit | No secret values in logs |

## Fixtures

Mocked VNstock DataFrames, mocked provider functions, and deterministic Vietnam
news article records.

## Commands

```text
python -m pytest tests/test_dataflows_config.py tests/test_symbol_utils.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_model_validation.py
python -m pytest tests/test_vnstock_adapter.py tests/test_vietnam_news.py tests/test_vietnam_routing.py
python -m pytest
```

## Acceptance Evidence

- `python -m pytest tests/test_dataflows_config.py tests/test_symbol_utils.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_model_validation.py --basetemp .pytest-tmp -p no:cacheprovider`: 49 passed.
- `python -m pytest tests/test_vnstock_adapter.py tests/test_vietnam_news.py tests/test_vietnam_routing.py --basetemp .pytest-tmp -p no:cacheprovider`: 10 passed.
- `$env:DEEPSEEK_API_KEY='placeholder'; python -m pytest --basetemp .pytest-tmp -p no:cacheprovider`: 326 passed, 1 skipped, 7 warnings. The skipped test is the existing live DeepSeek integration guard.
