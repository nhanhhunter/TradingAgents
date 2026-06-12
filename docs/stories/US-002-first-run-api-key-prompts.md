# US-002 First-Run API Key Prompts

## Status

implemented

## Lane

normal

## Product Contract

When a first-run CLI user selects a provider whose API key is missing, TradingAgents prompts for that key, saves it to the project `.env`, and uses it for the current run. Vietnam tickers (`*.VN` and `VNINDEX`) also prompt for `VNSTOCK_API_KEY` when no environment value or VNstock credential file exists.

## Relevant Product Docs

- `README.md`
- `.env.example`
- `cli/main.py`
- `cli/utils.py`

## Acceptance Criteria

- LLM provider API keys are not hardcoded in examples.
- Missing provider keys are requested interactively and persisted to `.env`.
- Vietnam-market runs request `VNSTOCK_API_KEY` on first use when needed.
- README installation instructions target `nhanhhunter/TradingAgents` and cover macOS/Linux plus Windows.

## Design Notes

- Commands: `tradingagents` / `python -m cli.main`.
- Domain rules: VNstock credential prompting only applies to `*.VN` and `VNINDEX`; non-Vietnam symbols must not prompt for `VNSTOCK_API_KEY`.
- UI surfaces: interactive CLI password prompts.

## Validation

When updating durable proof status, use numeric booleans:
`scripts/bin/harness-cli story update --id US-002 --unit 1 --integration 0 --e2e 0 --platform 1`.

| Layer | Expected proof |
| --- | --- |
| Unit | `python -m pytest tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_vnstock_adapter.py -q` |
| Integration | Not required for this scoped change |
| E2E | Not run to avoid consuming live API quota |
| Platform | `tradingagents --help` smoke from installed environment |
| Release | Not required |

## Harness Delta

No harness rule changes required.

## Evidence

- RED before implementation: three new tests failed because `ensure_vnstock_api_key_for_symbol` did not exist.
- GREEN after implementation: `.\.venv\Scripts\python.exe -m pytest tests\test_api_key_env.py tests\test_cli_env_skip.py tests\test_vnstock_adapter.py -q` passed with 36 tests.
- Docs check: `rg "TauricResearch/TradingAgents.git|DEEPSEEK_API_KEY=sk-|MIMO_API_KEY=tp-|9ROUTER_API_KEY=sk-|VNSTOCK_API_KEY=vnstock_" README.md .env.example` returned no matches.
