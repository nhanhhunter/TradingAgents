# US-013 CLI Recent Selections

## Status

planned

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
- Implementation and validation evidence will be appended as later tasks
  complete.
