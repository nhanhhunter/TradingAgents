# First-Run API Key Prompts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure first-run CLI users are prompted for missing required API keys and document installation from `nhanhhunter/TradingAgents`.

**Architecture:** Reuse the existing `ensure_api_key(provider)` flow for LLM providers. Add a focused VNstock helper in `cli/utils.py` that only prompts for Vietnam-market tickers when `VNSTOCK_API_KEY` and the VNstock credential file are both missing, then call it immediately after ticker entry.

**Tech Stack:** Python, Typer, Questionary, python-dotenv, pytest, Harness.

---

### Task 1: VNstock First-Run Prompt

**Files:**
- Modify: `tests/test_api_key_env.py`
- Modify: `tests/test_cli_env_skip.py`
- Modify: `cli/utils.py`
- Modify: `cli/main.py`

- [x] **Step 1: Write failing tests**

Tests added:
- `test_ensure_vnstock_api_key_for_vietnam_symbol_prompts_and_writes`
- `test_ensure_vnstock_api_key_skips_non_vietnam_symbols`
- `test_cli_checks_vnstock_key_after_ticker_entry`

- [x] **Step 2: Run tests to verify failure**

Run:
```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_api_key_env.py::test_ensure_vnstock_api_key_for_vietnam_symbol_prompts_and_writes tests\test_api_key_env.py::test_ensure_vnstock_api_key_skips_non_vietnam_symbols tests\test_cli_env_skip.py::TestCliSkipsPromptsFromEnv::test_cli_checks_vnstock_key_after_ticker_entry -q
```

Expected: FAIL because the helper is missing.

- [x] **Step 3: Implement helper and CLI call**

Add `ensure_vnstock_api_key_for_symbol(symbol)` to `cli/utils.py`. Call it from `get_user_selections()` after ticker entry.

- [x] **Step 4: Verify tests pass**

Run:
```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_api_key_env.py tests\test_cli_env_skip.py tests\test_vnstock_adapter.py -q
```

Expected: all tests pass.

### Task 2: README Install Docs

**Files:**
- Modify: `README.md`
- Verify: `.env.example`

- [x] **Step 1: Replace installation instructions**

Update the clone URL to `https://github.com/nhanhhunter/TradingAgents.git`, add macOS/Linux and Windows venv setup, explain first-run key prompts, and keep manual `.env` configuration as optional advanced usage.

- [x] **Step 2: Verify docs and examples**

Run:
```powershell
rg "TauricResearch/TradingAgents.git|DEEPSEEK_API_KEY=sk-|MIMO_API_KEY=tp-|9ROUTER_API_KEY=sk-|VNSTOCK_API_KEY=vnstock_" README.md .env.example
```

Expected: no output.
