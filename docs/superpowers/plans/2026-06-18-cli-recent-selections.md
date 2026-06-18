# CLI Recent Selections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remember the latest interactive language, analyst team, provider, and Thinking Agent pair per user/machine so repeat CLI runs can reuse them with minimal input.

**Architecture:** Add a dependency-free `cli.preferences` module that validates and atomically stores non-secret JSON at `~/.tradingagents/cli_preferences.json`. Keep Questionary behavior in `cli.utils`: language/provider/model pairs get a `Use previous`/`Reselect` gate, while the existing Analysts Team checkbox receives checked defaults. `cli.main.get_user_selections()` loads once, preserves environment precedence, and merges interactive fields into the preference file once after the questionnaire succeeds.

**Tech Stack:** Python 3.10+, Questionary, Rich, pytest, `unittest.mock`, standard-library JSON/tempfile/path handling.

---

## File Map

- Create `cli/preferences.py`: preference path resolution, field-level validation, fail-open loading, merge-and-atomic-save.
- Modify `cli/utils.py`: previous-value prompts, analyst checkbox defaults, canonical provider lookup, reusable Thinking Agent pair validation.
- Modify `cli/main.py`: load preferences once, route them into prompts, preserve environment precedence, save once after Step 8.
- Create `tests/test_cli_preferences.py`: isolated persistence tests using `tmp_path`.
- Create `tests/test_cli_recent_selections.py`: prompt and questionnaire orchestration tests.
- Modify `tests/test_cli_env_skip.py`: patch preference I/O and assert environment values do not overwrite interactive history.
- Create `docs/stories/US-013-cli-recent-selections.md`: Harness story contract and validation evidence.
- Modify `README.md`: document the convenience behavior, storage path, and environment precedence.

### Task 1: Record the Normal-Lane Story

**Files:**
- Create: `docs/stories/US-013-cli-recent-selections.md`
- Reference: `docs/superpowers/specs/2026-06-18-cli-recent-selections-design.md`

- [ ] **Step 1: Create the story packet**

```markdown
# US-013 CLI Recent Selections

## Status

planned

## Lane

normal

## Product Contract

The interactive CLI remembers the most recent non-secret Output Language,
Analysts Team, LLM provider, and Quick/Deep Thinking Agent selections in
`~/.tradingagents/cli_preferences.json`. Repeat runs may reuse valid values,
while environment configuration remains authoritative.

## Relevant Product Docs

- `README.md`
- `docs/superpowers/specs/2026-06-18-cli-recent-selections-design.md`
- `cli/main.py`
- `cli/utils.py`

## Acceptance Criteria

- First runs and invalid preference files retain the current full selectors.
- Output Language, LLM Provider, and the Quick/Deep model pair offer
  `Use previous` and `Reselect` when the previous value is valid.
- Analysts Team always uses the existing checkbox and prechecks prior analysts
  that remain valid for the current asset type.
- Regional providers reuse their exact canonical provider and endpoint without
  asking for the region again.
- Preferences contain no API keys, backend URLs, ticker symbols, or dates.
- The preference file is merged and atomically written once after the
  questionnaire completes.
- Environment-controlled fields are not copied into or over the previous
  interactive preference.
- Preference load/save failures never prevent an analysis run.

## Design Notes

- Commands: `tradingagents` / `python -m cli.main`.
- Domain rules: stored analyst wire values remain `market`, `social`, `news`,
  and `fundamentals`; Thinking Agent pairs are owned by `thinking_provider`.
- UI surfaces: Questionary select and checkbox prompts.
- Persistence: versioned user-local JSON, no secrets.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python -m pytest tests/test_cli_preferences.py tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider` |
| Integration | `python -m pytest tests/test_cli_env_skip.py tests/test_api_key_env.py tests/test_ollama_base_url.py tests/test_model_validation.py -q --basetemp .pytest-tmp -p no:cacheprovider` |
| E2E | Not required; Questionary behavior is covered with prompt-boundary tests |
| Platform | `python -m cli.main --help` |
| Release | README documents the preference path and precedence |

## Harness Delta

`scripts/bin/harness-cli` is absent in this checkout, so durable intake,
matrix, and story rows cannot be recorded until the binary is restored.

## Evidence

- Approved design: `docs/superpowers/specs/2026-06-18-cli-recent-selections-design.md`.
- Design commit: `38eb25c`.
- Implementation and validation evidence will be appended by this story's
  execution tasks.
```

- [ ] **Step 2: Confirm the story is scoped to one product behavior**

Run:

```bash
rg -n "Output Language|Analysts Team|LLM provider|Thinking Agent|environment|atomic" docs/stories/US-013-cli-recent-selections.md
```

Expected: each acceptance area appears in the story and no unrelated CLI behavior is included.

- [ ] **Step 3: Commit the story**

```bash
git add docs/stories/US-013-cli-recent-selections.md
git commit -m "docs: add CLI recent selections story"
```

### Task 2: Build the Preference Store with TDD

**Files:**
- Create: `tests/test_cli_preferences.py`
- Create: `cli/preferences.py`

- [ ] **Step 1: Write failing load-validation tests**

```python
import json
import os

import pytest

from cli.preferences import load_cli_preferences


pytestmark = pytest.mark.unit


def test_missing_preference_file_returns_empty_dict(tmp_path):
    assert load_cli_preferences(tmp_path / "missing.json") == {}


def test_valid_preferences_load_supported_fields_only(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": "Vietnamese",
                "analysts": ["market", "social", "unknown"],
                "llm_provider": "mimo",
                "thinking_provider": "mimo",
                "quick_think_llm": "mimo-v2.5",
                "deep_think_llm": "mimo-v2.5-pro",
                "api_key": "must-not-load",
            }
        ),
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {
        "version": 1,
        "output_language": "Vietnamese",
        "analysts": ["market", "social"],
        "llm_provider": "mimo",
        "thinking_provider": "mimo",
        "quick_think_llm": "mimo-v2.5",
        "deep_think_llm": "mimo-v2.5-pro",
    }


@pytest.mark.parametrize(
    "payload",
    [
        "{not-json",
        json.dumps([]),
        json.dumps({"version": 2, "output_language": "Vietnamese"}),
    ],
)
def test_invalid_document_fails_open(tmp_path, payload):
    path = tmp_path / "preferences.json"
    path.write_text(payload, encoding="utf-8")

    assert load_cli_preferences(path) == {}


def test_wrong_field_types_are_discarded_independently(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": 123,
                "analysts": "market",
                "llm_provider": "mimo",
                "thinking_provider": None,
                "quick_think_llm": "",
                "deep_think_llm": "mimo-v2.5-pro",
            }
        ),
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {
        "version": 1,
        "llm_provider": "mimo",
        "deep_think_llm": "mimo-v2.5-pro",
    }
```

- [ ] **Step 2: Run the load tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_preferences.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: collection fails with `ModuleNotFoundError: No module named 'cli.preferences'`.

- [ ] **Step 3: Add the minimal fail-open loader**

Create `cli/preferences.py`:

```python
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping


PREFERENCES_VERSION = 1
PREFERENCES_PATH = Path.home() / ".tradingagents" / "cli_preferences.json"
ANALYST_VALUES = {"market", "social", "news", "fundamentals"}
STRING_FIELDS = {
    "output_language",
    "llm_provider",
    "thinking_provider",
    "quick_think_llm",
    "deep_think_llm",
}


def _nonempty_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _sanitize_preferences(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("version") != PREFERENCES_VERSION:
        return {}

    sanitized: dict[str, Any] = {"version": PREFERENCES_VERSION}
    for field in STRING_FIELDS:
        value = _nonempty_string(payload.get(field))
        if value is not None:
            sanitized[field] = value

    analysts = payload.get("analysts")
    if isinstance(analysts, list):
        valid = [
            value
            for value in analysts
            if isinstance(value, str) and value in ANALYST_VALUES
        ]
        if valid:
            sanitized["analysts"] = list(dict.fromkeys(valid))

    return sanitized


def load_cli_preferences(path: Path = PREFERENCES_PATH) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return _sanitize_preferences(json.load(handle))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return {}
```

- [ ] **Step 4: Run the load tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_preferences.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all four load test groups pass.

- [ ] **Step 5: Write failing merge-and-save tests**

Append to `tests/test_cli_preferences.py`:

```python
from unittest import mock

from cli.preferences import save_cli_preferences


def test_save_merges_updates_and_writes_only_supported_fields(tmp_path):
    path = tmp_path / "nested" / "preferences.json"

    assert save_cli_preferences(
        {
            "output_language": "Vietnamese",
            "analysts": ["market", "news"],
            "llm_provider": "mimo",
            "thinking_provider": "mimo",
            "quick_think_llm": "mimo-v2.5",
            "deep_think_llm": "mimo-v2.5-pro",
            "backend_url": "https://secret.example",
            "ticker": "XAUUSD",
        },
        path,
    )

    assert json.loads(path.read_text(encoding="utf-8")) == {
        "version": 1,
        "output_language": "Vietnamese",
        "analysts": ["market", "news"],
        "llm_provider": "mimo",
        "thinking_provider": "mimo",
        "quick_think_llm": "mimo-v2.5",
        "deep_think_llm": "mimo-v2.5-pro",
    }


def test_save_preserves_fields_excluded_from_updates(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": "Japanese",
                "llm_provider": "deepseek",
                "thinking_provider": "deepseek",
                "quick_think_llm": "deepseek-chat",
                "deep_think_llm": "deepseek-reasoner",
            }
        ),
        encoding="utf-8",
    )

    assert save_cli_preferences({"analysts": ["market"]}, path)
    stored = json.loads(path.read_text(encoding="utf-8"))

    assert stored["output_language"] == "Japanese"
    assert stored["llm_provider"] == "deepseek"
    assert stored["quick_think_llm"] == "deepseek-chat"
    assert stored["analysts"] == ["market"]


def test_save_uses_atomic_replace(tmp_path):
    path = tmp_path / "preferences.json"

    with mock.patch("cli.preferences.os.replace", wraps=os.replace) as replace:
        assert save_cli_preferences({"analysts": ["market"]}, path)

    replace.assert_called_once()
    source, destination = replace.call_args.args
    assert Path(destination) == path
    assert Path(source).parent == path.parent
    assert json.loads(path.read_text(encoding="utf-8"))["analysts"] == ["market"]


def test_save_failure_returns_false_and_removes_temp_file(tmp_path):
    path = tmp_path / "preferences.json"

    with mock.patch("cli.preferences.os.replace", side_effect=OSError("disk full")):
        assert save_cli_preferences({"analysts": ["market"]}, path) is False

    assert not path.exists()
    assert list(tmp_path.iterdir()) == []
```

- [ ] **Step 6: Run the save tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_preferences.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: import fails because `save_cli_preferences` does not exist.

- [ ] **Step 7: Implement merge-and-atomic-save**

Append to `cli/preferences.py`:

```python
def save_cli_preferences(
    updates: Mapping[str, Any],
    path: Path = PREFERENCES_PATH,
) -> bool:
    current = load_cli_preferences(path)
    merged = dict(current)
    merged.update(updates)
    merged["version"] = PREFERENCES_VERSION
    sanitized = _sanitize_preferences(merged)

    temp_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(sanitized, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        return True
    except OSError:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except OSError:
                pass
        return False
```

- [ ] **Step 8: Run preference tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_preferences.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all preference tests pass and no real home-directory file is created.

- [ ] **Step 9: Commit the preference store**

```bash
git add cli/preferences.py tests/test_cli_preferences.py
git commit -m "feat: add CLI preference store"
```

### Task 3: Add Previous-Selection Prompt Behavior with TDD

**Files:**
- Create: `tests/test_cli_recent_selections.py`
- Modify: `cli/utils.py:1-334`
- Modify: `cli/utils.py:591-622`

- [ ] **Step 1: Write a reusable fake prompt and failing language tests**

Create `tests/test_cli_recent_selections.py`:

```python
import os
from unittest import mock

import pytest

from cli.models import AnalystType, AssetType


pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def _clear_cli_selection_env(monkeypatch):
    for name in (
        "TRADINGAGENTS_OUTPUT_LANGUAGE",
        "TRADINGAGENTS_LLM_PROVIDER",
        "TRADINGAGENTS_QUICK_THINK_LLM",
        "TRADINGAGENTS_DEEP_THINK_LLM",
    ):
        monkeypatch.delenv(name, raising=False)


class Answer:
    def __init__(self, value):
        self.value = value

    def ask(self):
        return self.value


def test_language_reuses_previous_without_opening_full_selector():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select:
        assert utils.ask_output_language("Vietnamese") == "Vietnamese"

    choices = select.call_args.kwargs["choices"]
    assert [choice.title for choice in choices] == [
        "Use previous: Vietnamese",
        "Reselect",
    ]


def test_language_reselect_opens_existing_full_selector():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        side_effect=[Answer("reselect"), Answer("Japanese")],
    ) as select:
        assert utils.ask_output_language("Vietnamese") == "Japanese"

    assert select.call_count == 2


def test_custom_language_is_reusable():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.ask_output_language("Vietnamese") == "Vietnamese"
```

- [ ] **Step 2: Run language tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: tests fail because `ask_output_language()` does not accept a previous value.

- [ ] **Step 3: Split the full language selector and add the reuse gate**

Replace the current language function in `cli/utils.py` with:

```python
def _ask_output_language_full() -> str:
    choice = questionary.select(
        "Select Output Language:",
        choices=[
            questionary.Choice("English (default)", "English"),
            questionary.Choice("Chinese (中文)", "Chinese"),
            questionary.Choice("Japanese (日本語)", "Japanese"),
            questionary.Choice("Korean (한국어)", "Korean"),
            questionary.Choice("Hindi (हिन्दी)", "Hindi"),
            questionary.Choice("Spanish (Español)", "Spanish"),
            questionary.Choice("Portuguese (Português)", "Portuguese"),
            questionary.Choice("French (Français)", "French"),
            questionary.Choice("German (Deutsch)", "German"),
            questionary.Choice("Arabic (العربية)", "Arabic"),
            questionary.Choice("Russian (Русский)", "Russian"),
            questionary.Choice("Custom language", "custom"),
        ],
        style=questionary.Style([
            ("selected", "fg:yellow noinherit"),
            ("highlighted", "fg:yellow noinherit"),
            ("pointer", "fg:yellow noinherit"),
        ]),
    ).ask()
    if choice == "custom":
        return questionary.text(
            "Enter language name (e.g. Turkish, Vietnamese, Thai, Indonesian):",
            validate=lambda x: len(x.strip()) > 0 or "Please enter a language name.",
        ).ask().strip()
    return choice


def ask_output_language(previous_language: str | None = None) -> str:
    """Ask for report output language, optionally reusing the prior value."""
    if isinstance(previous_language, str) and previous_language.strip():
        action = questionary.select(
            "Select Output Language:",
            choices=[
                questionary.Choice(
                    f"Use previous: {previous_language.strip()}",
                    "reuse",
                ),
                questionary.Choice("Reselect", "reselect"),
            ],
            style=questionary.Style([
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]),
        ).ask()
        if action == "reuse":
            return previous_language.strip()
    return _ask_output_language_full()
```

- [ ] **Step 4: Run language tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: the three language tests pass.

- [ ] **Step 5: Write failing Analysts Team default tests**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_analysts_checkbox_prechecks_previous_values():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "checkbox",
        return_value=Answer([AnalystType.MARKET, AnalystType.NEWS]),
    ) as checkbox:
        result = utils.select_analysts(
            AssetType.STOCK,
            default_analysts=["market", "news"],
        )

    assert result == [AnalystType.MARKET, AnalystType.NEWS]
    checked = {
        choice.value
        for choice in checkbox.call_args.kwargs["choices"]
        if choice.checked
    }
    assert checked == {AnalystType.MARKET, AnalystType.NEWS}


def test_crypto_drops_fundamentals_from_checked_defaults():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "checkbox",
        return_value=Answer([AnalystType.MARKET]),
    ) as checkbox:
        utils.select_analysts(
            AssetType.CRYPTO,
            default_analysts=["market", "fundamentals"],
        )

    values = [choice.value for choice in checkbox.call_args.kwargs["choices"]]
    assert AnalystType.FUNDAMENTALS not in values
    assert all(
        choice.value != AnalystType.FUNDAMENTALS or not choice.checked
        for choice in checkbox.call_args.kwargs["choices"]
    )
```

- [ ] **Step 6: Run analyst tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: tests fail because `select_analysts()` has no `default_analysts` parameter.

- [ ] **Step 7: Add checked defaults to the existing checkbox**

Change `select_analysts()` in `cli/utils.py`:

```python
def select_analysts(
    asset_type: AssetType = AssetType.STOCK,
    default_analysts: List[str] | None = None,
) -> List[AnalystType]:
    """Select analysts, prechecking prior values valid for the asset type."""
    available_analysts = filter_analysts_for_asset_type(
        [value for _, value in ANALYST_ORDER],
        asset_type,
    )
    default_values = {
        value
        for value in (default_analysts or [])
        if value in {analyst.value for analyst in available_analysts}
    }
    choices = questionary.checkbox(
        "Select Your [Analysts Team]:",
        choices=[
            questionary.Choice(
                display,
                value=value,
                checked=value.value in default_values,
            )
            for display, value in ANALYST_ORDER
            if value in available_analysts
        ],
        instruction="\n- Press Space to select/unselect analysts\n- Press 'a' to select/unselect all\n- Press Enter when done",
        validate=lambda x: len(x) > 0 or "You must select at least one analyst.",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()
    if not choices:
        console.print("\n[red]No analysts selected. Exiting...[/red]")
        exit(1)
    return choices
```

- [ ] **Step 8: Run analyst tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: language and analyst tests pass.

- [ ] **Step 9: Write failing provider reuse tests**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_previous_provider_reuses_current_display_and_endpoint():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select:
        result = utils.select_previous_llm_provider("mimo")

    assert result == ("mimo", "https://token-plan-sgp.xiaomimimo.com/v1")
    assert select.call_args.kwargs["choices"][0].title == "Use previous: Xiaomi Mimo"


def test_unknown_previous_provider_skips_reuse_prompt():
    from cli import utils

    with mock.patch.object(utils.questionary, "select") as select:
        assert utils.select_previous_llm_provider("removed-provider") is None

    select.assert_not_called()


@pytest.mark.parametrize(
    ("provider", "endpoint"),
    [
        ("qwen", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        ("qwen-cn", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        ("glm", "https://api.z.ai/api/paas/v4/"),
        ("glm-cn", "https://open.bigmodel.cn/api/paas/v4/"),
        ("minimax", "https://api.minimax.io/v1"),
        ("minimax-cn", "https://api.minimaxi.com/v1"),
    ],
)
def test_regional_previous_provider_resolves_exact_endpoint(provider, endpoint):
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.select_previous_llm_provider(provider) == (provider, endpoint)


def test_provider_reselect_returns_none_for_full_picker_fallback():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reselect"),
    ):
        assert utils.select_previous_llm_provider("mimo") is None
```

- [ ] **Step 10: Run provider tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: tests fail because `select_previous_llm_provider` does not exist.

- [ ] **Step 11: Add canonical provider lookup and reuse prompt**

Add below `_llm_provider_table()` in `cli/utils.py`:

```python
def _provider_lookup() -> dict[str, tuple[str, str | None]]:
    lookup = {
        provider_key: (display, url)
        for display, provider_key, url in _llm_provider_table()
    }
    lookup.update(
        {
            "glm": (
                "GLM / Z.AI (International)",
                "https://api.z.ai/api/paas/v4/",
            ),
            "qwen-cn": (
                "Qwen (China)",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
            "glm-cn": (
                "GLM / BigModel (China)",
                "https://open.bigmodel.cn/api/paas/v4/",
            ),
            "minimax-cn": (
                "MiniMax (China)",
                "https://api.minimaxi.com/v1",
            ),
        }
    )
    return lookup


def select_previous_llm_provider(
    previous_provider: str | None,
) -> tuple[str, str | None] | None:
    """Offer reuse for a valid canonical provider, otherwise use the full picker."""
    if not isinstance(previous_provider, str):
        return None
    provider_key = previous_provider.lower()
    provider = _provider_lookup().get(provider_key)
    if provider is None:
        return None

    display, url = provider
    action = questionary.select(
        "Select your LLM Provider:",
        choices=[
            questionary.Choice(f"Use previous: {display}", "reuse"),
            questionary.Choice("Reselect", "reselect"),
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()
    if action == "reuse":
        return provider_key, url
    return None
```

Leave `provider_default_url()` unchanged. The new lookup is scoped to reuse and
overrides the final canonical `glm` variant to the Z.AI international endpoint;
this avoids changing existing environment-default behavior as part of this
feature.

- [ ] **Step 12: Run provider tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py tests/test_cli_env_skip.py::TestProviderDefaultUrl -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all selected tests pass, including existing default URL behavior.

- [ ] **Step 13: Write failing Thinking Agent pair tests**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_thinking_agents_reuse_valid_catalog_pair():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select, mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
    ) as deep:
        result = utils.select_thinking_agents(
            "mimo",
            previous_provider="mimo",
            previous_quick="mimo-v2.5",
            previous_deep="mimo-v2.5-pro",
        )

    assert result == ("mimo-v2.5", "mimo-v2.5-pro")
    assert "Quick=Mimo v2.5" in select.call_args.kwargs["choices"][0].title
    quick.assert_not_called()
    deep.assert_not_called()


def test_thinking_agents_provider_mismatch_opens_full_selectors():
    from cli import utils

    with mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="deepseek-chat",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="deepseek-reasoner",
    ) as deep, mock.patch.object(utils.questionary, "select") as select:
        result = utils.select_thinking_agents(
            "deepseek",
            previous_provider="mimo",
            previous_quick="mimo-v2.5",
            previous_deep="mimo-v2.5-pro",
        )

    assert result == ("deepseek-chat", "deepseek-reasoner")
    select.assert_not_called()
    quick.assert_called_once_with("deepseek")
    deep.assert_called_once_with("deepseek")


def test_thinking_agents_reselect_runs_both_existing_selectors():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reselect"),
    ), mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="mimo-v2.5",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="mimo-v2.5-pro",
    ) as deep:
        result = utils.select_thinking_agents(
            "mimo",
            previous_provider="mimo",
            previous_quick="mimo-v2.5",
            previous_deep="mimo-v2.5-pro",
        )

    assert result == ("mimo-v2.5", "mimo-v2.5-pro")
    quick.assert_called_once_with("mimo")
    deep.assert_called_once_with("mimo")


def test_stale_catalog_model_opens_full_selectors():
    from cli import utils

    with mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="gpt-5.4-mini",
    ), mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="gpt-5.5",
    ), mock.patch.object(utils.questionary, "select") as select:
        result = utils.select_thinking_agents(
            "openai",
            previous_provider="openai",
            previous_quick="removed-model",
            previous_deep="gpt-5.5",
        )

    assert result == ("gpt-5.4-mini", "gpt-5.5")
    select.assert_not_called()


@pytest.mark.parametrize("provider", ["openrouter", "azure", "ollama"])
def test_custom_model_pairs_are_reusable_for_custom_capable_providers(provider):
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.select_thinking_agents(
            provider,
            previous_provider=provider,
            previous_quick="custom-quick",
            previous_deep="custom-deep",
        ) == ("custom-quick", "custom-deep")
```

- [ ] **Step 14: Run Thinking Agent tests and verify RED**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: tests fail because `select_thinking_agents` does not exist.

- [ ] **Step 15: Implement pair validation, labels, and reuse/reselect**

Add after the individual Thinking Agent selectors in `cli/utils.py`:

```python
def _reusable_model_label(provider: str, mode: str, model: object) -> str | None:
    if not isinstance(model, str) or not model.strip():
        return None
    model_id = model.strip()
    provider_key = provider.lower()

    if provider_key in {"openrouter", "azure"}:
        return model_id

    try:
        options = get_model_options(provider_key, mode)
    except KeyError:
        return None

    labels = {value: display for display, value in options if value != "custom"}
    if model_id in labels:
        return labels[model_id].split(" - ", 1)[0]
    if any(value == "custom" for _, value in options):
        return model_id
    return None


def select_thinking_agents(
    provider: str,
    *,
    previous_provider: str | None = None,
    previous_quick: str | None = None,
    previous_deep: str | None = None,
) -> tuple[str, str]:
    """Reuse a valid provider-owned model pair or run both existing selectors."""
    provider_key = provider.lower()
    previous_key = (
        previous_provider.lower()
        if isinstance(previous_provider, str)
        else None
    )
    quick_label = _reusable_model_label(provider_key, "quick", previous_quick)
    deep_label = _reusable_model_label(provider_key, "deep", previous_deep)

    if previous_key == provider_key and quick_label and deep_label:
        action = questionary.select(
            "Select your Thinking Agents:",
            choices=[
                questionary.Choice(
                    f"Use previous: Quick={quick_label}; Deep={deep_label}",
                    "reuse",
                ),
                questionary.Choice("Reselect", "reselect"),
            ],
            instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
            style=questionary.Style(
                [
                    ("selected", "fg:magenta noinherit"),
                    ("highlighted", "fg:magenta noinherit"),
                    ("pointer", "fg:magenta noinherit"),
                ]
            ),
        ).ask()
        if action == "reuse":
            return previous_quick.strip(), previous_deep.strip()

    return (
        select_shallow_thinking_agent(provider_key),
        select_deep_thinking_agent(provider_key),
    )
```

- [ ] **Step 16: Run all prompt tests and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py tests/test_cli_env_skip.py::TestProviderDefaultUrl tests/test_ollama_base_url.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all selected tests pass.

- [ ] **Step 17: Commit prompt behavior**

```bash
git add cli/utils.py tests/test_cli_recent_selections.py
git commit -m "feat: reuse recent CLI selections"
```

### Task 4: Wire Preferences into the Questionnaire with TDD

**Files:**
- Modify: `tests/test_cli_recent_selections.py`
- Modify: `tests/test_cli_env_skip.py:35-121`
- Modify: `cli/main.py:1-34`
- Modify: `cli/main.py:476-677`

- [ ] **Step 1: Write a questionnaire fixture and failing first-run/save-once test**

Append to `tests/test_cli_recent_selections.py`:

```python
def _questionnaire_patches(main_module):
    return [
        mock.patch.object(main_module, "fetch_announcements", return_value=None),
        mock.patch.object(main_module, "display_announcements"),
        mock.patch.object(main_module, "get_ticker", return_value="AAPL"),
        mock.patch.object(main_module, "ensure_vnstock_api_key_for_symbol"),
        mock.patch.object(main_module, "get_analysis_date", return_value="2026-06-18"),
        mock.patch.object(main_module, "select_research_depth", return_value=1),
        mock.patch.object(main_module, "ensure_api_key"),
    ]


def test_questionnaire_loads_once_and_saves_interactive_fields_once():
    import cli.main as main

    patchers = _questionnaire_patches(main)
    entered = [patcher.start() for patcher in patchers]
    try:
        with mock.patch.object(main, "load_cli_preferences", return_value={}) as load, \
             mock.patch.object(main, "save_cli_preferences", return_value=True) as save, \
             mock.patch.object(main, "ask_output_language", return_value="Vietnamese") as language, \
             mock.patch.object(
                 main,
                 "select_analysts",
                 return_value=[AnalystType.MARKET, AnalystType.NEWS],
             ) as analysts, \
             mock.patch.object(
                 main,
                 "select_previous_llm_provider",
                 return_value=None,
             ) as previous_provider, \
             mock.patch.object(
                 main,
                 "select_llm_provider",
                 return_value=("mimo", "https://token-plan-sgp.xiaomimimo.com/v1"),
             ), \
             mock.patch.object(
                 main,
                 "select_thinking_agents",
                 return_value=("mimo-v2.5", "mimo-v2.5-pro"),
             ) as thinking:
            selections = main.get_user_selections()
    finally:
        for patcher in reversed(patchers):
            patcher.stop()

    load.assert_called_once_with()
    language.assert_called_once_with(None)
    analysts.assert_called_once_with(AssetType.STOCK, default_analysts=None)
    previous_provider.assert_called_once_with(None)
    thinking.assert_called_once_with(
        "mimo",
        previous_provider=None,
        previous_quick=None,
        previous_deep=None,
    )
    save.assert_called_once_with(
        {
            "output_language": "Vietnamese",
            "analysts": ["market", "news"],
            "llm_provider": "mimo",
            "thinking_provider": "mimo",
            "quick_think_llm": "mimo-v2.5",
            "deep_think_llm": "mimo-v2.5-pro",
        }
    )
    assert selections["output_language"] == "Vietnamese"
    assert selections["analysts"] == [AnalystType.MARKET, AnalystType.NEWS]
    assert selections["llm_provider"] == "mimo"
    assert selections["shallow_thinker"] == "mimo-v2.5"
    assert selections["deep_thinker"] == "mimo-v2.5-pro"
```

- [ ] **Step 2: Run the orchestration test and verify RED**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py::test_questionnaire_loads_once_and_saves_interactive_fields_once -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: test fails because `cli.main` does not import or call preference functions and still invokes the old prompt signatures.

- [ ] **Step 3: Import the preference store and load once**

Add to `cli/main.py` imports:

```python
from cli.preferences import load_cli_preferences, save_cli_preferences
from cli.models import AnalystType, AssetType
```

Remove the now-redundant single-type import:

```python
from cli.models import AnalystType
```

At the beginning of `get_user_selections()`, before rendering the welcome panel:

```python
    preferences = load_cli_preferences()
```

- [ ] **Step 4: Pass previous values into language and analysts**

Replace Step 3 and Step 4 prompt calls with:

```python
    language_from_env = bool(os.environ.get("TRADINGAGENTS_OUTPUT_LANGUAGE"))
    if language_from_env:
        output_language = DEFAULT_CONFIG["output_language"]
        console.print(
            f"[green]✓ Output language from environment:[/green] {output_language}"
        )
    else:
        console.print(
            create_question_box(
                "Step 3: Output Language",
                "Select the language for analyst reports and final decision",
            )
        )
        output_language = ask_output_language(
            preferences.get("output_language")
        )

    console.print(
        create_question_box(
            "Step 4: Analysts Team",
            "Select your LLM analyst agents for the analysis",
        )
    )
    selected_analysts = select_analysts(
        asset_type,
        default_analysts=preferences.get("analysts"),
    )
```

- [ ] **Step 5: Reuse exact providers without repeating region selection**

Replace the interactive branch of Step 6 with:

```python
    else:
        console.print(
            create_question_box(
                "Step 6: LLM Provider", "Select your LLM provider"
            )
        )
        reused_provider = select_previous_llm_provider(
            preferences.get("llm_provider")
        )
        if reused_provider is not None:
            selected_llm_provider, backend_url = reused_provider
        else:
            selected_llm_provider, backend_url = select_llm_provider()
            if selected_llm_provider == "qwen":
                selected_llm_provider, backend_url = ask_qwen_region()
            elif selected_llm_provider == "minimax":
                selected_llm_provider, backend_url = ask_minimax_region()
            elif selected_llm_provider == "glm":
                selected_llm_provider, backend_url = ask_glm_region()

        if selected_llm_provider == "ollama":
            confirm_ollama_endpoint(backend_url)
        ensure_api_key(selected_llm_provider)
```

- [ ] **Step 6: Select Thinking Agents as one provider-owned pair**

Replace Step 7 with:

```python
    models_from_env = bool(
        os.environ.get("TRADINGAGENTS_QUICK_THINK_LLM")
        or os.environ.get("TRADINGAGENTS_DEEP_THINK_LLM")
    )
    if models_from_env:
        selected_shallow_thinker = DEFAULT_CONFIG["quick_think_llm"]
        selected_deep_thinker = DEFAULT_CONFIG["deep_think_llm"]
        console.print(
            f"[green]✓ Thinking agents from environment:[/green] "
            f"quick={selected_shallow_thinker}, deep={selected_deep_thinker}"
        )
    else:
        console.print(
            create_question_box(
                "Step 7: Thinking Agents",
                "Select your thinking agents for analysis",
            )
        )
        (
            selected_shallow_thinker,
            selected_deep_thinker,
        ) = select_thinking_agents(
            selected_llm_provider,
            previous_provider=preferences.get("thinking_provider"),
            previous_quick=preferences.get("quick_think_llm"),
            previous_deep=preferences.get("deep_think_llm"),
        )
```

- [ ] **Step 7: Build the existing result, merge interactive fields, and save once**

Replace the direct return at the end of `get_user_selections()` with:

```python
    selections = {
        "ticker": selected_ticker,
        "asset_type": asset_type.value,
        "analysis_date": analysis_date,
        "analysts": selected_analysts,
        "research_depth": selected_research_depth,
        "llm_provider": selected_llm_provider.lower(),
        "backend_url": backend_url,
        "shallow_thinker": selected_shallow_thinker,
        "deep_thinker": selected_deep_thinker,
        "google_thinking_level": thinking_level,
        "openai_reasoning_effort": reasoning_effort,
        "anthropic_effort": anthropic_effort,
        "output_language": output_language,
    }

    preference_updates = {
        "analysts": [analyst.value for analyst in selected_analysts],
    }
    if not language_from_env:
        preference_updates["output_language"] = output_language
    if not provider_from_env:
        preference_updates["llm_provider"] = selected_llm_provider.lower()
    if not models_from_env:
        preference_updates.update(
            {
                "thinking_provider": selected_llm_provider.lower(),
                "quick_think_llm": selected_shallow_thinker,
                "deep_think_llm": selected_deep_thinker,
            }
        )

    if not save_cli_preferences(preference_updates):
        console.print(
            "[yellow]Could not save recent CLI selections; "
            "continuing with the current run.[/yellow]"
        )

    return selections
```

- [ ] **Step 8: Run the first-run/save-once test and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py::test_questionnaire_loads_once_and_saves_interactive_fields_once -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: test passes.

- [ ] **Step 9: Write failing prior-value and regional-reuse integration test**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_questionnaire_passes_prior_values_and_skips_region_prompt_on_reuse():
    import cli.main as main

    preferences = {
        "version": 1,
        "output_language": "Vietnamese",
        "analysts": ["market", "social", "news", "fundamentals"],
        "llm_provider": "qwen-cn",
        "thinking_provider": "qwen-cn",
        "quick_think_llm": "qwen3.6-flash",
        "deep_think_llm": "qwen3.7-max",
    }
    patchers = _questionnaire_patches(main)
    [patcher.start() for patcher in patchers]
    try:
        with mock.patch.object(main, "load_cli_preferences", return_value=preferences), \
             mock.patch.object(main, "save_cli_preferences", return_value=True), \
             mock.patch.object(main, "ask_output_language", return_value="Vietnamese") as language, \
             mock.patch.object(
                 main,
                 "select_analysts",
                 return_value=[AnalystType.MARKET, AnalystType.NEWS],
             ) as analysts, \
             mock.patch.object(
                 main,
                 "select_previous_llm_provider",
                 return_value=(
                     "qwen-cn",
                     "https://dashscope.aliyuncs.com/compatible-mode/v1",
                 ),
             ), \
             mock.patch.object(main, "select_llm_provider") as full_provider, \
             mock.patch.object(main, "ask_qwen_region") as region, \
             mock.patch.object(
                 main,
                 "select_thinking_agents",
                 return_value=("qwen3.6-flash", "qwen3.7-max"),
             ) as thinking:
            result = main.get_user_selections()
    finally:
        for patcher in reversed(patchers):
            patcher.stop()

    language.assert_called_once_with("Vietnamese")
    analysts.assert_called_once_with(
        AssetType.STOCK,
        default_analysts=["market", "social", "news", "fundamentals"],
    )
    full_provider.assert_not_called()
    region.assert_not_called()
    thinking.assert_called_once_with(
        "qwen-cn",
        previous_provider="qwen-cn",
        previous_quick="qwen3.6-flash",
        previous_deep="qwen3.7-max",
    )
    assert result["llm_provider"] == "qwen-cn"
```

- [ ] **Step 10: Run the prior-value test and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py::test_questionnaire_passes_prior_values_and_skips_region_prompt_on_reuse -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: test passes with no full provider or region prompt.

- [ ] **Step 11: Write failing save-failure test**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_preference_save_failure_warns_but_returns_current_selections():
    import cli.main as main

    patchers = _questionnaire_patches(main)
    [patcher.start() for patcher in patchers]
    try:
        with mock.patch.object(main, "load_cli_preferences", return_value={}), \
             mock.patch.object(main, "save_cli_preferences", return_value=False), \
             mock.patch.object(main, "ask_output_language", return_value="English"), \
             mock.patch.object(
                 main,
                 "select_analysts",
                 return_value=[AnalystType.MARKET],
             ), \
             mock.patch.object(main, "select_previous_llm_provider", return_value=None), \
             mock.patch.object(
                 main,
                 "select_llm_provider",
                 return_value=("mimo", "https://token-plan-sgp.xiaomimimo.com/v1"),
             ), \
             mock.patch.object(
                 main,
                 "select_thinking_agents",
                 return_value=("mimo-v2.5", "mimo-v2.5-pro"),
             ), \
             mock.patch.object(main.console, "print") as print_message:
            result = main.get_user_selections()
    finally:
        for patcher in reversed(patchers):
            patcher.stop()

    assert result["llm_provider"] == "mimo"
    assert any(
        "Could not save recent CLI selections" in str(call.args[0])
        for call in print_message.call_args_list
        if call.args
    )
```

- [ ] **Step 12: Run save-failure test and verify GREEN**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py::test_preference_save_failure_warns_but_returns_current_selections -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: test passes and the questionnaire result is returned.

- [ ] **Step 13: Update the existing environment-skip test**

In both `get_user_selections()` tests in `tests/test_cli_env_skip.py`:

1. Patch `load_cli_preferences` with an existing interactive history.
2. Patch `save_cli_preferences` and prevent real home-directory writes.
3. Replace patches of the two individual model selectors with
   `select_thinking_agents`.
4. Assert only the always-interactive analysts are updated.

Use this expectation in `test_env_config_skips_llm_prompts`:

```python
prior_preferences = {
    "version": 1,
    "output_language": "Vietnamese",
    "llm_provider": "mimo",
    "thinking_provider": "mimo",
    "quick_think_llm": "mimo-v2.5",
    "deep_think_llm": "mimo-v2.5-pro",
}

# Add to the existing with statement:
mock.patch.object(m, "load_cli_preferences", return_value=prior_preferences), \
mock.patch.object(m, "save_cli_preferences", return_value=True) as save_preferences, \
mock.patch.object(m, "select_previous_llm_provider") as previous_provider, \
mock.patch.object(m, "select_thinking_agents") as prompt_thinking:

# Replace the old quick/deep assertions:
previous_provider.assert_not_called()
prompt_thinking.assert_not_called()
save_preferences.assert_called_once_with({"analysts": []})
```

Apply the same preference I/O patches to
`test_cli_checks_vnstock_key_after_ticker_entry`; its assertions remain focused
on `ensure_vnstock_api_key_for_symbol("VCB.VN")`.

- [ ] **Step 14: Add mixed environment/interactivity coverage**

Append to `tests/test_cli_recent_selections.py`:

```python
def test_env_provider_with_interactive_models_saves_pair_not_provider(monkeypatch):
    import cli.main as main

    monkeypatch.setenv("TRADINGAGENTS_LLM_PROVIDER", "mimo")
    monkeypatch.setenv("TRADINGAGENTS_OUTPUT_LANGUAGE", "English")
    fake_config = dict(main.DEFAULT_CONFIG)
    fake_config.update(
        {
            "llm_provider": "mimo",
            "backend_url": "https://token-plan-sgp.xiaomimimo.com/v1",
            "output_language": "English",
        }
    )
    patchers = _questionnaire_patches(main)
    [patcher.start() for patcher in patchers]
    try:
        with mock.patch.object(main, "DEFAULT_CONFIG", fake_config), \
             mock.patch.object(
                 main,
                 "load_cli_preferences",
                 return_value={
                     "version": 1,
                     "output_language": "Vietnamese",
                     "llm_provider": "deepseek",
                 },
             ), \
             mock.patch.object(main, "save_cli_preferences", return_value=True) as save, \
             mock.patch.object(
                 main,
                 "select_analysts",
                 return_value=[AnalystType.MARKET],
             ), \
             mock.patch.object(
                 main,
                 "select_thinking_agents",
                 return_value=("mimo-v2.5", "mimo-v2.5-pro"),
             ):
            main.get_user_selections()
    finally:
        for patcher in reversed(patchers):
            patcher.stop()

    save.assert_called_once_with(
        {
            "analysts": ["market"],
            "thinking_provider": "mimo",
            "quick_think_llm": "mimo-v2.5",
            "deep_think_llm": "mimo-v2.5-pro",
        }
    )
```

This proves an environment provider can own a newly selected model pair without
overwriting the prior interactive `llm_provider` or `output_language`.

- [ ] **Step 15: Run orchestration and environment tests**

Run:

```bash
python -m pytest tests/test_cli_recent_selections.py tests/test_cli_env_skip.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all tests pass and no test writes `~/.tradingagents/cli_preferences.json`.

- [ ] **Step 16: Commit questionnaire integration**

```bash
git add cli/main.py tests/test_cli_recent_selections.py tests/test_cli_env_skip.py
git commit -m "feat: persist recent CLI questionnaire choices"
```

### Task 5: Document the User-Visible Behavior

**Files:**
- Modify: `README.md:236-246`
- Modify: `docs/stories/US-013-cli-recent-selections.md`

- [ ] **Step 1: Add the preference behavior under CLI Usage**

After the interactive CLI launch commands in `README.md`, add:

```markdown
### Reusing recent CLI selections

For interactive runs, TradingAgents remembers the latest Output Language, LLM
provider, and Quick/Deep Thinking Agent pair for the current user and offers
`Use previous` or `Reselect` on the next run. The Analysts Team checkbox is
always shown, with the previous valid analysts checked by default.

Preferences are stored locally at
`~/.tradingagents/cli_preferences.json`. The file contains no API keys,
backend URLs, ticker symbols, or analysis dates. `TRADINGAGENTS_*` environment
variables remain authoritative; environment-controlled values are not copied
over the prior interactive preference.
```

- [ ] **Step 2: Mark the story in progress**

In `docs/stories/US-013-cli-recent-selections.md`, change:

```markdown
## Status

in_progress
```

Keep the design evidence already recorded; validation commands are appended
only after they have actually run.

- [ ] **Step 3: Verify documentation wording and secret exclusions**

Run:

```bash
rg -n "cli_preferences.json|Use previous|Analysts Team|TRADINGAGENTS_\\*|API keys|backend URLs" README.md docs/stories/US-013-cli-recent-selections.md
```

Expected: README and story both describe the path, interaction, precedence, and non-secret contract.

- [ ] **Step 4: Commit documentation**

```bash
git add README.md docs/stories/US-013-cli-recent-selections.md
git commit -m "docs: explain recent CLI selections"
```

### Task 6: Run Regression Proof and Record Evidence

**Files:**
- Modify: `docs/stories/US-013-cli-recent-selections.md`

- [ ] **Step 1: Run focused preference and prompt tests**

Run:

```bash
python -m pytest tests/test_cli_preferences.py tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all new tests pass.

- [ ] **Step 2: Run related CLI/provider regressions**

Run:

```bash
python -m pytest tests/test_cli_env_skip.py tests/test_api_key_env.py tests/test_ollama_base_url.py tests/test_model_validation.py tests/test_crypto_asset_mode.py -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all selected tests pass with no network calls or live credentials.

- [ ] **Step 3: Run CLI help smoke**

Run:

```bash
python -m cli.main --help
```

Expected: exits 0 and displays the TradingAgents command help.

- [ ] **Step 4: Run the full suite**

Run:

```bash
env DEEPSEEK_API_KEY=placeholder python -m pytest -q --basetemp .pytest-tmp -p no:cacheprovider
```

Expected: all non-live tests pass; the credential-gated live integration test remains skipped.

- [ ] **Step 5: Record exact evidence**

Change the story status from `in_progress` to `implemented`. Under `Evidence`,
append each command from Steps 1-4 and its observed pytest summary line
verbatim. Also record the RED failures observed during Tasks 2-4 and the fact
that Harness durable rows were not updated because `scripts/bin/harness-cli`
is absent in this checkout.

- [ ] **Step 6: Review the complete diff**

Run:

```bash
git diff --check
git status --short
git diff -- cli/preferences.py cli/utils.py cli/main.py tests/test_cli_preferences.py tests/test_cli_recent_selections.py tests/test_cli_env_skip.py README.md docs/stories/US-013-cli-recent-selections.md
```

Expected: no whitespace errors; only the scoped preference feature, tests, story, README, spec, and plan are present.

- [ ] **Step 7: Commit validation evidence**

```bash
git add docs/stories/US-013-cli-recent-selections.md
git commit -m "test: record CLI preference validation"
```
