# CLI Recent Selections Design

## Goal

Reduce repeated input in the interactive CLI by remembering the most recent
user-selected values for:

- Output language
- Analysts Team
- LLM provider
- Quick- and Deep-Thinking agents

Preferences are local to the current user and machine. They are convenience
defaults only; environment-driven configuration remains authoritative.

## Scope

This change affects the interactive questionnaire in `cli/main.py` and the
selection helpers in `cli/utils.py`. It does not change analysis configuration
keys, report formats, result logs, API-key storage, non-interactive package
usage, or environment-variable behavior.

Research Depth, ticker, analysis date, and provider-specific thinking settings
remain unchanged.

## Persistence

Store preferences as JSON at:

```text
~/.tradingagents/cli_preferences.json
```

The file contains only non-secret questionnaire values:

```json
{
  "version": 1,
  "output_language": "Vietnamese",
  "analysts": ["market", "social", "news", "fundamentals"],
  "llm_provider": "mimo",
  "thinking_provider": "mimo",
  "quick_think_llm": "mimo-v2.5",
  "deep_think_llm": "mimo-v2.5-pro"
}
```

API keys, backend credentials, ticker symbols, and analysis dates must never be
stored in this file.

Preferences are written once, immediately after the full questionnaire has
completed successfully. The write creates the parent directory if needed and
uses a temporary file plus replacement so an interrupted write cannot leave
partially written JSON.

Environment-provided values are not copied into the preference file. Existing
interactive preferences remain unchanged for any field controlled by its
corresponding `TRADINGAGENTS_*` environment variable.

## Loading and Failure Handling

The questionnaire loads preferences once at startup.

Missing files, unreadable files, malformed JSON, unsupported versions, wrong
field types, or unknown values are treated as absent preferences. These
conditions must not prevent the CLI from starting.

Validation is field-specific. One invalid field does not discard other valid
fields. Unknown JSON fields are ignored to allow additive future versions.

If saving fails, the current analysis selections remain valid and the CLI emits
a non-fatal warning. Preference persistence must never block an analysis run.

## Interaction Design

### First Run or Missing Valid Preference

Each question behaves exactly as it does today and shows its full selector.

### Output Language

When a valid previous language exists, show a two-choice prompt:

```text
Select Output Language:
  Use previous: Vietnamese
  Reselect
```

Choosing the previous value returns it immediately. Choosing `Reselect` opens
the existing full language selector, including custom language entry.

Custom language names are valid previous values when they are non-empty
strings.

### Analysts Team

Always show the existing analyst checkbox. Do not add a `Use previous` or
`Reselect` prompt.

When previous analysts exist, mark the valid previous analysts as checked by
default. The user may confirm them with Enter or adjust the selection normally.
There are currently at most four analysts:

- Market Analyst
- Sentiment Analyst, stored with the existing wire value `social`
- News Analyst
- Fundamentals Analyst

Analysts unavailable for the current asset type are removed from the defaults.
For example, Fundamentals Analyst is not preselected for crypto. If none of the
previous analysts are valid for the current asset type, the checkbox opens with
no defaults and keeps the existing requirement that at least one analyst be
selected.

### LLM Provider

When a valid previous provider exists, show:

```text
Select your LLM Provider:
  Use previous: Xiaomi Mimo
  Reselect
```

The label uses the current provider display name while the stored value remains
the canonical provider key.

Choosing the previous provider reuses its current catalog endpoint, not a
persisted backend URL. Provider-specific follow-up behavior remains intact:

- Qwen, GLM, and MiniMax still resolve their regional provider variant.
- Ollama still resolves and displays the current `OLLAMA_BASE_URL` or default.
- The selected provider still passes through the existing API-key check.

If the stored provider no longer exists in the provider table, show the full
provider selector.

Regional provider variants are stored as the final canonical provider key
selected for the run, such as `qwen-cn`. Reuse must resolve that exact variant
and endpoint without asking for the region again. Selecting `Reselect` retains
the current main-provider-plus-region flow.

### Thinking Agents

Quick and Deep models are treated as one remembered pair because both depend on
the selected provider. `thinking_provider` records which provider the pair
belongs to independently of the most recent interactively selected provider.
This avoids mismatching models when the provider came from an environment
variable but model selection remained interactive.

When both previous models are valid for the currently selected provider, show:

```text
Select your Thinking Agents:
  Use previous: Quick=Mimo v2.5; Deep=Mimo v2.5 Pro
  Reselect
```

Choosing the previous pair returns both model IDs. Choosing `Reselect` runs the
existing Quick selector followed by the existing Deep selector.

The pair is reusable only when:

- the current provider matches `thinking_provider`; and
- both stored model IDs are valid for that provider and mode.

Catalog models are validated against the current model catalog. Custom model
IDs remain reusable for providers that already support custom IDs, including
OpenRouter, Ollama, and Azure. If the pair cannot be validated safely, skip the
reuse prompt and open both existing model selectors.

## Environment Precedence

Existing environment behavior is preserved:

- `TRADINGAGENTS_OUTPUT_LANGUAGE` skips the language prompt.
- `TRADINGAGENTS_LLM_PROVIDER` skips the provider prompt.
- Either `TRADINGAGENTS_QUICK_THINK_LLM` or
  `TRADINGAGENTS_DEEP_THINK_LLM` keeps the current environment-driven Thinking
  Agents behavior.

Environment-controlled fields are excluded from the preference update. Fields
that remain interactive in the same questionnaire are still updated. When
Thinking Agents remain interactive while the provider comes from the
environment, the selected model pair and its `thinking_provider` are saved
without replacing the prior interactive `llm_provider` preference.

## Components

### Preference Store

Add a small CLI-local module responsible for:

- resolving the user preference path;
- parsing and validating stored fields;
- returning an empty preference object on recoverable load failures; and
- atomically saving merged interactive selections.

The module has no dependency on Questionary or Rich, making persistence rules
independently testable.

### Selection Helpers

Extend the existing helpers without changing their returned domain values:

- language selection accepts an optional previous value;
- analyst selection accepts optional default analysts;
- provider selection accepts an optional previous provider;
- Thinking Agent selection accepts an optional previous provider/model pair.

Prompt presentation remains inside the CLI utility layer. Validation should
reuse the provider table and model catalog rather than duplicating provider or
model lists in the preference module.

### Questionnaire Orchestration

`get_user_selections()`:

1. loads preferences once;
2. passes applicable previous values into the four optimized questions;
3. preserves existing environment skips and provider follow-up prompts;
4. builds the existing selection result dictionary; and
5. merges and saves interactive fields once before returning the dictionary.

## Testing

### Preference Store Unit Tests

- Missing preference file returns empty preferences.
- Valid version-1 JSON loads supported fields.
- Malformed JSON and wrong field types fail open.
- Invalid fields are discarded independently.
- Saving creates the user directory and writes the expected non-secret fields.
- Saving preserves environment-controlled fields from the prior file.
- Atomic replacement leaves a complete JSON document.
- Save failure is non-fatal to questionnaire completion.

Tests inject a temporary preference path and never write to the real home
directory.

### Prompt Unit Tests

- Language uses a valid previous value or opens the full selector on
  `Reselect`.
- Custom language values can be reused.
- Analysts are prechecked from previous valid values.
- Crypto removes Fundamentals Analyst from prechecked values.
- Provider reuse resolves the current display label and endpoint.
- Unknown providers open the full selector.
- Regional provider variants reuse the exact variant without a region prompt.
- A valid provider/model pair can be reused.
- Provider mismatch or stale catalog models open the full model selectors.

### Questionnaire Integration Tests

- First run follows the current full questionnaire.
- A prior preference file reduces language, provider, and model selection to
  reuse/reselect prompts while Analysts Team remains the normal checkbox.
- The preference file is saved once after all questions complete.
- Environment-configured fields still skip prompts and are not overwritten in
  preferences.
- Existing returned selection keys and values remain unchanged.

### Regression Validation

Run focused CLI tests, then the full test suite. No live provider calls are
required.

## Harness Classification

Lane: normal.

Reason: this is a bounded user-visible CLI workflow change with existing
behavior and tests to preserve. It does not alter secrets, provider request
behavior, report contracts, or stored analysis data.

The required `scripts/bin/harness-cli` binary is absent from this checkout, so
the durable intake and matrix commands cannot currently be recorded.
