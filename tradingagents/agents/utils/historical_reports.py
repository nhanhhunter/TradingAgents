"""Bounded historical full-state report context for the Portfolio Manager."""

from __future__ import annotations

import json
import logging
import re
from datetime import date
from pathlib import Path
from typing import Any

from tradingagents.dataflows.utils import safe_ticker_component

logger = logging.getLogger(__name__)

_LOG_PREFIX = "full_states_log_"
_LOG_SUFFIX = ".json"
_WHITESPACE_RE = re.compile(r"\s+")


def build_historical_report_context(
    config: dict[str, Any],
    ticker: str,
    trade_date: str,
    memory_entries: list[dict] | None = None,
) -> str:
    """Return structured summaries from prior same-ticker full-state logs.

    The context is intentionally bounded and source-selective. It gives the
    Portfolio Manager enough hindsight to compare prior theses without
    re-injecting entire historical reports into the prompt.
    """
    if not config.get("historical_report_context_enabled", True):
        return ""

    max_runs = int(config.get("historical_report_context_max_runs", 3) or 0)
    max_chars_per_run = int(
        config.get("historical_report_context_max_chars_per_run", 4000) or 0
    )
    if max_runs <= 0 or max_chars_per_run <= 0:
        return ""

    try:
        current_date = date.fromisoformat(str(trade_date))
    except ValueError:
        logger.warning("Invalid trade_date for historical report context: %s", trade_date)
        return ""

    results_dir = config.get("results_dir")
    if not results_dir:
        return ""

    safe_ticker = safe_ticker_component(ticker)
    logs_dir = Path(results_dir).expanduser() / safe_ticker / "TradingAgentsStrategy_logs"
    outcome_by_date = _memory_outcomes_by_date(ticker, memory_entries or [])

    summaries = []
    for log_date, path in _iter_prior_log_paths(logs_dir, current_date):
        state = _read_state_log(path)
        if not _has_required_fields(state):
            continue
        summaries.append(
            _format_run_summary(
                log_date=log_date,
                state=state,
                outcome=outcome_by_date.get(log_date.isoformat()),
                max_chars=max_chars_per_run,
            )
        )
        if len(summaries) >= max_runs:
            break

    if not summaries:
        return ""

    return "\n\n".join(summaries)


def _iter_prior_log_paths(logs_dir: Path, current_date: date) -> list[tuple[date, Path]]:
    if not logs_dir.exists() or not logs_dir.is_dir():
        return []

    candidates: list[tuple[date, Path]] = []
    for path in logs_dir.glob(f"{_LOG_PREFIX}*{_LOG_SUFFIX}"):
        stem = path.name[len(_LOG_PREFIX) : -len(_LOG_SUFFIX)]
        try:
            log_date = date.fromisoformat(stem)
        except ValueError:
            continue
        if log_date < current_date:
            candidates.append((log_date, path))

    return sorted(candidates, key=lambda item: item[0], reverse=True)


def _read_state_log(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Skipping historical report log %s: %s", path, exc)
        return {}
    return data if isinstance(data, dict) else {}


def _has_required_fields(state: dict[str, Any]) -> bool:
    required = (
        "market_report",
        "sentiment_report",
        "news_report",
        "fundamentals_report",
        "final_trade_decision",
    )
    return all(isinstance(state.get(key), str) for key in required)


def _memory_outcomes_by_date(ticker: str, entries: list[dict]) -> dict[str, dict]:
    outcomes = {}
    for entry in entries:
        if entry.get("ticker") != ticker or entry.get("pending"):
            continue
        entry_date = entry.get("date")
        if entry_date:
            outcomes[entry_date] = entry
    return outcomes


def _format_run_summary(
    log_date: date,
    state: dict[str, Any],
    outcome: dict | None,
    max_chars: int,
) -> str:
    sections = [
        f"### Prior analysis: {log_date.isoformat()}",
        f"Final decision:\n{_compact_text(state['final_trade_decision'])}",
    ]

    if outcome:
        outcome_bits = [
            f"rating={outcome.get('rating') or 'n/a'}",
            f"raw_return={outcome.get('raw') or 'n/a'}",
            f"alpha={outcome.get('alpha') or 'n/a'}",
            f"holding={outcome.get('holding') or 'n/a'}",
        ]
        sections.append(f"Outcome: {', '.join(outcome_bits)}")
        reflection = outcome.get("reflection")
        if reflection:
            sections.append(f"Reflection:\n{_compact_text(reflection)}")

    report_fields = (
        ("Market report", "market_report"),
        ("Sentiment report", "sentiment_report"),
        ("News report", "news_report"),
        ("Fundamentals report", "fundamentals_report"),
    )
    for label, key in report_fields:
        sections.append(f"{label}:\n{_compact_text(state[key])}")

    return _truncate("\n\n".join(sections), max_chars)


def _compact_text(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", str(text)).strip()


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    if max_chars <= 14:
        return text[:max_chars]
    return text[: max_chars - 14].rstrip() + "\n[truncated]"
