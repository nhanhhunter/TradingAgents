import pytest

from tradingagents.dataflows.vietnam_symbols import (
    is_vietnam_symbol,
    to_vnstock_symbol,
)


@pytest.mark.unit
def test_detects_vietnam_equity_suffix_and_index():
    assert is_vietnam_symbol("VCB.VN") is True
    assert is_vietnam_symbol(" vcb.vn ") is True
    assert is_vietnam_symbol("VNINDEX") is True


@pytest.mark.unit
def test_does_not_treat_foreign_symbols_as_vietnamese():
    assert is_vietnam_symbol("AAPL") is False
    assert is_vietnam_symbol("0700.HK") is False
    assert is_vietnam_symbol("BTC-USD") is False


@pytest.mark.unit
def test_converts_to_vnstock_symbol():
    assert to_vnstock_symbol("VCB.VN") == "VCB"
    assert to_vnstock_symbol(" vcb.vn ") == "VCB"
    assert to_vnstock_symbol("VNINDEX") == "VNINDEX"
