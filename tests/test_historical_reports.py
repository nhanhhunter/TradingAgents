"""Tests for bounded historical full-state report context."""

import json

import pytest

from tradingagents.agents.utils.historical_reports import build_historical_report_context


def _state(date_label: str) -> dict:
    return {
        "company_of_interest": "NVDA",
        "trade_date": date_label,
        "market_report": f"Market thesis {date_label}",
        "sentiment_report": f"Sentiment thesis {date_label}",
        "news_report": f"News thesis {date_label}",
        "fundamentals_report": f"Fundamentals thesis {date_label}",
        "final_trade_decision": f"Rating: Buy\nDecision thesis {date_label}",
        "investment_debate_state": {"history": "research history should not leak"},
        "risk_debate_state": {"history": "risk history should not leak"},
    }


def _write_state(tmp_path, ticker: str, date_label: str, payload: dict | None = None):
    logs_dir = tmp_path / ticker / "TradingAgentsStrategy_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / f"full_states_log_{date_label}.json"
    path.write_text(json.dumps(payload or _state(date_label)), encoding="utf-8")
    return path


def _config(tmp_path, **overrides):
    config = {
        "results_dir": str(tmp_path),
        "historical_report_context_enabled": True,
        "historical_report_context_max_runs": 3,
        "historical_report_context_max_chars_per_run": 4000,
    }
    config.update(overrides)
    return config


def test_loads_three_most_recent_prior_same_ticker_logs(tmp_path):
    for day in range(1, 7):
        _write_state(tmp_path, "NVDA", f"2026-01-0{day}")
    _write_state(tmp_path, "AAPL", "2026-01-04")

    ctx = build_historical_report_context(_config(tmp_path), "NVDA", "2026-01-05")

    assert "Prior analysis: 2026-01-04" in ctx
    assert "Prior analysis: 2026-01-03" in ctx
    assert "Prior analysis: 2026-01-02" in ctx
    assert "Prior analysis: 2026-01-01" not in ctx
    assert "Prior analysis: 2026-01-05" not in ctx
    assert "Prior analysis: 2026-01-06" not in ctx
    assert "AAPL" not in ctx


def test_skips_malformed_and_missing_field_logs(tmp_path):
    _write_state(tmp_path, "NVDA", "2026-01-04")
    malformed = _write_state(tmp_path, "NVDA", "2026-01-03")
    malformed.write_text("{not-json", encoding="utf-8")
    missing = _state("2026-01-02")
    del missing["fundamentals_report"]
    _write_state(tmp_path, "NVDA", "2026-01-02", missing)
    _write_state(tmp_path, "NVDA", "2026-01-01")

    ctx = build_historical_report_context(_config(tmp_path), "NVDA", "2026-01-05")

    assert "Prior analysis: 2026-01-04" in ctx
    assert "Prior analysis: 2026-01-01" in ctx
    assert "Prior analysis: 2026-01-03" not in ctx
    assert "Prior analysis: 2026-01-02" not in ctx


def test_summary_contains_only_expected_report_fields_and_outcome(tmp_path):
    _write_state(tmp_path, "NVDA", "2026-01-04")
    memory_entries = [
        {
            "ticker": "NVDA",
            "date": "2026-01-04",
            "rating": "Buy",
            "pending": False,
            "raw": "+5.0%",
            "alpha": "+2.0%",
            "holding": "5d",
            "reflection": "Momentum confirmed.",
        }
    ]

    ctx = build_historical_report_context(
        _config(tmp_path),
        "NVDA",
        "2026-01-05",
        memory_entries=memory_entries,
    )

    assert "Final decision:" in ctx
    assert "Market report:" in ctx
    assert "Sentiment report:" in ctx
    assert "News report:" in ctx
    assert "Fundamentals report:" in ctx
    assert "raw_return=+5.0%" in ctx
    assert "alpha=+2.0%" in ctx
    assert "Momentum confirmed." in ctx
    assert "research history should not leak" not in ctx
    assert "risk history should not leak" not in ctx


def test_summary_respects_per_run_char_limit(tmp_path):
    state = _state("2026-01-04")
    state["market_report"] = "market " * 1000
    _write_state(tmp_path, "NVDA", "2026-01-04", state)

    ctx = build_historical_report_context(
        _config(tmp_path, historical_report_context_max_chars_per_run=200),
        "NVDA",
        "2026-01-05",
    )

    assert len(ctx) <= 200
    assert "[truncated]" in ctx


def test_can_be_disabled(tmp_path):
    _write_state(tmp_path, "NVDA", "2026-01-04")

    ctx = build_historical_report_context(
        _config(tmp_path, historical_report_context_enabled=False),
        "NVDA",
        "2026-01-05",
    )

    assert ctx == ""


def test_unsafe_ticker_is_rejected_before_path_lookup(tmp_path):
    _write_state(tmp_path, "NVDA", "2026-01-04")

    with pytest.raises(ValueError):
        build_historical_report_context(_config(tmp_path), "../NVDA", "2026-01-05")
