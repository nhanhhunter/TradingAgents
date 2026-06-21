# Validation

## Proof Strategy

Use isolated temporary directories and placeholder keys. Prove both path
selection and a save/load round trip without making live API calls.

## Test Plan

| Layer | Cases |
| --- | --- |
| Unit | Path precedence, ancestor isolation, empty-variable loading, permissions |
| Integration | CLI provider and VNstock persistence through the shared resolver |
| E2E | Save in one process and load in a fresh process |
| Platform | Pathlib behavior plus Dockerfile destination |
| Performance | Not applicable |
| Logs/Audit | Confirm no key values are printed |

## Fixtures

- Temporary source checkout.
- Temporary installed-command directory.
- Temporary home directory.
- Placeholder API-key values only.

## Commands

```text
python -m pytest tests/test_env_config.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_vnstock_adapter.py -q
python -m pytest -q
git diff --check
```

## Acceptance Evidence

- RED: `python -m pytest tests/test_env_config.py -q` failed during collection
  with `ModuleNotFoundError: No module named 'tradingagents.env_config'`.
- Focused GREEN:
  `python -m pytest tests/test_env_config.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_vnstock_adapter.py -q`
  passed with 45 tests.
- Release suite: `python -m pytest -q` passed with 395 tests, one expected
  live-provider skip, and seven existing unknown-model warnings.
- Original repro: a source checkout nested below an ancestor `.env` wrote to
  the checkout `.env` and left the ancestor file unchanged.
