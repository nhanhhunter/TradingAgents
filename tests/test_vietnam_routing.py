from unittest import mock

import pytest

from tradingagents.dataflows import interface


@pytest.mark.unit
def test_vietnam_ticker_routes_stock_data_to_vnstock_first():
    vn = mock.Mock(return_value="vn rows")
    with mock.patch.dict(interface.VENDOR_METHODS, {"get_stock_data": {"vnstock": vn, "yfinance": mock.Mock(return_value="yf rows")}}, clear=False):
        result = interface.route_to_vendor("get_stock_data", "VCB.VN", "2026-01-01", "2026-01-10")

    assert result == "vn rows"
    vn.assert_called_once_with("VCB.VN", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_non_vietnam_ticker_keeps_configured_vendor_chain():
    yf = mock.Mock(return_value="yf rows")
    with mock.patch.dict(interface.VENDOR_METHODS, {"get_stock_data": {"yfinance": yf}}, clear=False):
        result = interface.route_to_vendor("get_stock_data", "AAPL", "2026-01-01", "2026-01-10")

    assert result == "yf rows"
    yf.assert_called_once_with("AAPL", "2026-01-01", "2026-01-10")


@pytest.mark.unit
def test_vietnam_news_falls_back_to_yahoo_when_vietnam_sources_empty():
    vietnam = mock.Mock(return_value="No Vietnam news found for VCB.VN")
    yahoo = mock.Mock(return_value="## Yahoo fallback")
    with mock.patch.dict(interface.VENDOR_METHODS, {"get_news": {"vietnam_news": vietnam, "yfinance": yahoo}}, clear=False):
        result = interface.route_to_vendor("get_news", "VCB.VN", "2026-01-01", "2026-01-10")

    assert result == "## Yahoo fallback"
    yahoo.assert_called_once_with("VCB.VN", "2026-01-01", "2026-01-10")
