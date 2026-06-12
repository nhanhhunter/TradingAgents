# US-012 Historical Report Context for Portfolio Manager

## Status

implemented

## Lane

normal

## Product Contract

When prior same-ticker full-state JSON logs exist, the Portfolio Manager receives
a bounded structured summary of up to three prior analyses as hindsight context.
The feature does not change the decision log format, JSON log format, or analyst
pipeline inputs.

## Relevant Product Docs

- `README.md`

## Acceptance Criteria

- Prior report context is sourced from `full_states_log_<date>.json` files only.
- Only same-ticker logs before the current trade date are included, newest first,
  capped by config.
- Malformed or incomplete logs are skipped.
- Context includes analyst report summaries, prior final decision, and resolved
  decision-log outcome/reflection when available.
- Portfolio Manager prompt includes a guard that current analyst evidence takes
  priority over historical reports.

## Design Notes

- Commands: none.
- Queries: file reads from `results_dir/<safe_ticker>/TradingAgentsStrategy_logs`.
- API: `historical_report_context` added to graph state.
- Tables: none.
- Domain rules: historical reports are hindsight context, not current evidence.
- UI surfaces: none.

## Validation

When updating durable proof status, use numeric booleans:
`scripts/bin/harness-cli story update --id <id> --unit 1 --integration 1 --e2e 0 --platform 0`.

| Layer | Expected proof |
| --- | --- |
| Unit | `pytest tests/test_historical_reports.py tests/test_memory_log.py` |
| Integration | Existing graph/memory regression in `tests/test_memory_log.py` |
| E2E | Not required |
| Platform | Not required |
| Release | README and changelog updated |

## Harness Delta

`scripts/bin/harness-cli` is absent in this checkout, so durable story rows could
not be created or updated.

## Evidence

- `python -m py_compile tradingagents/agents/utils/historical_reports.py tradingagents/default_config.py tradingagents/graph/propagation.py tradingagents/agents/utils/agent_states.py tradingagents/graph/trading_graph.py tradingagents/agents/managers/portfolio_manager.py tests/test_historical_reports.py tests/test_memory_log.py`
- `pytest tests/test_historical_reports.py tests/test_memory_log.py` — 78 passed.
- `pytest` — 339 passed, 1 skipped.
