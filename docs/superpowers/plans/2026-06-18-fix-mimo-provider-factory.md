# Fix MIMO Provider Factory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the MIMO and 9router providers selectable end-to-end through the existing OpenAI-compatible client factory.

**Architecture:** Keep the current provider registry design. Add a regression test at the factory boundary, then register the two already-catalogued provider keys in `_OPENAI_COMPATIBLE`; do not change endpoints, credentials, models, or request behavior.

**Tech Stack:** Python, pytest, LangChain OpenAI-compatible client wrapper.

---

### Task 1: Add Factory Regression Coverage

**Files:**
- Create: `tests/test_llm_client_factory.py`
- Test: `tests/test_llm_client_factory.py`

- [x] **Step 1: Write the failing test**

```python
import pytest

from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.openai_client import OpenAIClient


@pytest.mark.unit
@pytest.mark.parametrize("provider", ["mimo", "9router"])
def test_openai_compatible_provider_is_dispatched(provider):
    client = create_llm_client(provider, "test-model")

    assert isinstance(client, OpenAIClient)
    assert client.provider == provider
```

- [x] **Step 2: Run the test to verify it fails**

Run:

```text
python -m pytest tests/test_llm_client_factory.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: both cases fail with `ValueError: Unsupported LLM provider`.

### Task 2: Register the Providers

**Files:**
- Modify: `tradingagents/llm_clients/factory.py:6-12`
- Test: `tests/test_llm_client_factory.py`

- [x] **Step 1: Write the minimal implementation**

Add the existing provider keys to the OpenAI-compatible tuple:

```python
_OPENAI_COMPATIBLE = (
    "openai", "xai", "deepseek",
    "qwen", "qwen-cn",
    "glm", "glm-cn",
    "minimax", "minimax-cn",
    "mimo", "9router",
    "ollama", "openrouter",
)
```

- [x] **Step 2: Run the regression test to verify it passes**

Run:

```text
python -m pytest tests/test_llm_client_factory.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: `2 passed`.

### Task 3: Verify Related Contracts

**Files:**
- Modify: `docs/stories/epics/E01-vietnam-market-data/US-001-vnstock-vietnam-news-llm-providers/validation.md`

- [x] **Step 1: Run focused provider tests**

Run:

```text
python -m pytest tests/test_llm_client_factory.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_model_validation.py tests/test_ollama_base_url.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all selected tests pass.

- [x] **Step 2: Run the full test suite**

Run:

```text
python -m pytest -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all non-live tests pass; any credential-gated live test remains skipped.

- [x] **Step 3: Record fresh acceptance evidence**

Append the exact focused and full-suite results to the existing story validation file without removing historical evidence.

- [x] **Step 4: Review the final diff**

Run:

```text
git diff --check
git status --short
git diff -- tradingagents/llm_clients/factory.py tests/test_llm_client_factory.py docs/stories/epics/E01-vietnam-market-data/US-001-vnstock-vietnam-news-llm-providers/validation.md
```

Expected: no whitespace errors and only the scoped fix, regression test, plan, and validation evidence are changed.
