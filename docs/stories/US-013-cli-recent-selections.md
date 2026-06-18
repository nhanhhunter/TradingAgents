# US-013 CLI Recent Selections

## Status

implemented

## Lane

normal

## Product Contract

The interactive CLI remembers the most recent non-secret Output Language,
Analysts Team, LLM provider, and Quick/Deep Thinking Agent selections in
`~/.tradingagents/cli_preferences.json`. Repeat runs reuse valid values, while
environment configuration remains authoritative.

## Relevant Product Docs

- `README.md`
- `docs/superpowers/specs/2026-06-18-cli-recent-selections-design.md`
- `cli/main.py`
- `cli/utils.py`

## Acceptance Criteria

- A first run or wholly invalid preference document uses the current full
  selectors; individual invalid fields fall back independently while other
  valid fields remain reusable.
- Output Language, LLM provider, and the Quick/Deep Thinking Agent model pair
  offer `Use previous` and `Reselect` when valid prior values exist.
- Analysts Team remains the existing checkbox with valid prior analyst values
  prechecked.
- A prior regional provider reuses its exact provider key without showing the
  region prompt again; its endpoint is resolved from the current provider
  catalog and is not persisted.
- API keys, backend URLs, ticker symbols, and analysis dates are never
  persisted.
- Interactive selections are merged and written atomically once after the full
  questionnaire completes.
- Environment-controlled fields are excluded from preference updates, leaving
  prior interactive values for those fields unchanged.
- Preference load and save failures are non-fatal.

## Design Notes

- Commands: `tradingagents` / `python -m cli.main`.
- Domain rules: analyst wire values are `market`, `social`, `news`, and
  `fundamentals`; the Quick/Deep model pair belongs to `thinking_provider`.
- UI surfaces: Questionary interactive CLI.
- Persistence: versioned user-local JSON containing no secrets.

## Validation

When updating durable proof status, use numeric booleans:
`scripts/bin/harness-cli story update --id US-013 --unit 1 --integration 1 --e2e 0 --platform 1`.

| Layer | Expected proof |
| --- | --- |
| Unit | `python -m pytest tests/test_cli_preferences.py tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider` |
| Integration | `python -m pytest tests/test_cli_env_skip.py tests/test_api_key_env.py tests/test_ollama_base_url.py tests/test_model_validation.py -q --basetemp .pytest-tmp -p no:cacheprovider` |
| E2E | Not required |
| Platform | `python -m cli.main --help` |
| Release | README |

## Harness Delta

`scripts/bin/harness-cli` is absent in this checkout, so durable intake, story,
matrix, and trace records cannot be created or updated.

## Evidence

- Approved design:
  `docs/superpowers/specs/2026-06-18-cli-recent-selections-design.md`.
- Design commit: `38eb25c`.
- Observed TDD RED evidence during implementation:
  - Task 2, before implementation commit `bde1cdb`:
    `python -m pytest tests/test_cli_preferences.py -q --basetemp .pytest-tmp -p no:cacheprovider`
    first failed during collection with
    `ModuleNotFoundError: No module named 'cli.preferences'`. After the loader
    implementation and save tests were added, the same command entered a
    second RED phase because `save_cli_preferences` was not defined/importable.
  - Task 3, before implementation commit `3a91d9d`:
    `python -m pytest tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider`
    failed in successive RED phases because `ask_output_language` lacked the
    `previous` argument, `select_analysts` lacked `default_analysts`,
    `select_previous_llm_provider` was absent, and
    `select_thinking_agents` was absent.
  - Task 4, before implementation commit `4063454`:
    `python -m pytest tests/test_cli_recent_selections.py::test_questionnaire_loads_once_and_saves_interactive_fields_once -q --basetemp .pytest-tmp -p no:cacheprovider`
    failed because `cli.main` did not expose or call
    `load_cli_preferences`.
- Fresh final validation:
  - `python -m pytest tests/test_cli_preferences.py tests/test_cli_recent_selections.py -q --basetemp .pytest-tmp -p no:cacheprovider`
    - `43 passed in 1.45s`
  - `python -m pytest tests/test_cli_env_skip.py tests/test_api_key_env.py tests/test_ollama_base_url.py tests/test_model_validation.py tests/test_crypto_asset_mode.py -q --basetemp .pytest-tmp -p no:cacheprovider`
    - `56 passed in 1.96s`
  - `python -m cli.main --help`
    - Exit 0; displayed the CLI usage and options.
  - `env DEEPSEEK_API_KEY=placeholder python -m pytest -q --basetemp .pytest-tmp -p no:cacheprovider`
    - `384 passed, 1 skipped, 7 warnings in 8.50s`
    - Skip: `tests/test_deepseek_reasoning.py:210` skipped the live API call
      because `DEEPSEEK_API_KEY` was unset or a placeholder.
    - Warnings: seven expected `RuntimeWarning` entries from
      `tests/test_anthropic_effort.py` for intentionally unknown Anthropic
      model names.
  - `git diff --check`
    - Exit 0 with no output.
  - `git status --short`
    - Before this story update, reported only untracked `.pytest-tmp/`.
- `scripts/bin/harness-cli` is absent in this checkout, so durable story,
  matrix, and trace rows were not updated.
