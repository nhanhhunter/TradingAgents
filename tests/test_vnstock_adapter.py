import inspect
from pathlib import Path
from unittest import mock

import pandas as pd
import pytest

from tradingagents.dataflows import vnstock_adapter
from tradingagents.dataflows.vendors.yahoo import fundamentals as yahoo_fundamentals


@pytest.mark.unit
def test_financial_adapter_signatures_match_yfinance_contract():
    for name in ("get_fundamentals", "get_balance_sheet", "get_cashflow", "get_income_statement"):
        assert inspect.signature(getattr(vnstock_adapter, name)) == inspect.signature(getattr(yahoo_fundamentals, name))


@pytest.mark.unit
def test_stock_history_formats_vnstock_ohlcv():
    history = pd.DataFrame(
        {
            "time": ["2026-01-02"],
            "open": [1000],
            "high": [1100],
            "low": [900],
            "close": [1050],
            "volume": [123456],
        }
    )
    with mock.patch.object(vnstock_adapter, "_history_frame", return_value=history):
        result = vnstock_adapter.get_vnstock_data_online("VCB.VN", "2026-01-01", "2026-01-03")

    assert "# Stock data for VCB.VN (VNstock: VCB)" in result
    assert "Open,High,Low,Close,Volume" in result
    assert "2026-01-02" in result


@pytest.mark.unit
def test_vnindex_financial_statement_returns_explicit_no_data():
    result = vnstock_adapter.get_balance_sheet("VNINDEX", as_of_date="2026-01-10")
    assert "VNINDEX" in result
    assert "does not have company financial statements" in result


@pytest.mark.unit
def test_registers_api_key_when_env_set_and_key_file_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("VNSTOCK_API_KEY", "secret-token")
    key_path = tmp_path / ".vnstock" / "api_key.json"

    with mock.patch.object(vnstock_adapter, "VNSTOCK_API_KEY_PATH", key_path), \
         mock.patch.object(Path, "home", return_value=tmp_path), \
         mock.patch.object(vnstock_adapter, "_vnstock_register_user") as register:
        vnstock_adapter.ensure_vnstock_credentials()

    register.assert_called_once_with(api_key="secret-token")
