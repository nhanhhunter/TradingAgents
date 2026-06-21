# Cross-Platform API Key Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist prompted API keys to a deterministic, reusable location on Linux, Windows, macOS, Docker, and Docker Compose.

**Architecture:** Add a side-effect-light environment-file module that owns path resolution, loading, and secure updates. Route package startup and both CLI credential prompts through it, then pin Docker to the named-volume-backed user configuration path.

**Tech Stack:** Python 3.10+, `pathlib`, `python-dotenv`, pytest, Docker/Compose.

---

### Task 1: Specify deterministic environment-file resolution

**Files:**
- Create: `tradingagents/env_config.py`
- Create: `tests/test_env_config.py`

- [ ] Write tests proving that an ancestor `.env` is ignored, a source checkout
  uses its own `.env`, installed usage falls back to
  `~/.tradingagents/.env`, and `TRADINGAGENTS_ENV_FILE` wins.
- [ ] Run `python -m pytest tests/test_env_config.py -q` and confirm the tests
  fail because `tradingagents.env_config` does not exist.
- [ ] Implement `resolve_env_file`, `load_tradingagents_env`, and
  `persist_env_value` with `pathlib`, exact-path lookup, non-empty environment
  precedence, and best-effort owner-only permissions.
- [ ] Re-run `python -m pytest tests/test_env_config.py -q` and confirm it
  passes.

### Task 2: Route CLI loading and saving through the shared module

**Files:**
- Modify: `tradingagents/__init__.py`
- Modify: `cli/utils.py`
- Modify: `tests/test_api_key_env.py`

- [ ] Add regression tests proving both provider and VNstock prompts use the
  resolved destination and a subsequent load restores the saved value.
- [ ] Run the focused tests and confirm failure against the current
  `find_dotenv` implementation.
- [ ] Replace package-level parent searching and both duplicated `set_key`
  blocks with the shared module.
- [ ] Run
  `python -m pytest tests/test_env_config.py tests/test_api_key_env.py tests/test_cli_env_skip.py tests/test_vnstock_adapter.py -q`.

### Task 3: Make Docker persistence durable

**Files:**
- Modify: `Dockerfile`
- Modify: `tests/test_env_config.py`

- [ ] Add a test asserting that Docker sets `TRADINGAGENTS_ENV_FILE` to the
  existing named-volume-backed directory.
- [ ] Run the test and confirm it fails before the Dockerfile change.
- [ ] Set
  `TRADINGAGENTS_ENV_FILE=/home/appuser/.tradingagents/.env` in the runtime
  image.
- [ ] Re-run the focused tests.

### Task 4: Update contracts and verify

**Files:**
- Modify: `README.md`
- Modify: `docs/stories/US-002-first-run-api-key-prompts.md`
- Create: `docs/stories/epics/E02-credential-persistence/US-014-cross-platform-api-key-persistence/overview.md`
- Create: `docs/stories/epics/E02-credential-persistence/US-014-cross-platform-api-key-persistence/design.md`
- Create: `docs/stories/epics/E02-credential-persistence/US-014-cross-platform-api-key-persistence/execplan.md`
- Create: `docs/stories/epics/E02-credential-persistence/US-014-cross-platform-api-key-persistence/validation.md`

- [ ] Document resolution order, override behavior, installed-package path,
  and Docker named-volume persistence.
- [ ] Run the focused credential suite.
- [ ] Run `python -m pytest -q`.
- [ ] Inspect `git diff --check`, `git status --short`, and scan changed files
  for accidental credential values.
