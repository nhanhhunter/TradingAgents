"""Helpers for Vietnamese market symbols.

TradingAgents keeps Yahoo Finance as the default global path. These helpers
only identify the Vietnam-specific shapes that should use VNstock instead:
equities entered with a ``.VN`` suffix and the market index ``VNINDEX``.
"""

from __future__ import annotations


VNINDEX_SYMBOL = "VNINDEX"


def normalize_vietnam_symbol(symbol: str) -> str:
    """Return a trimmed, upper-case symbol for Vietnam routing checks."""
    return symbol.strip().upper() if isinstance(symbol, str) else symbol


def is_vietnam_symbol(symbol: str) -> bool:
    """True for symbols that should use Vietnam-specific data sources."""
    normalized = normalize_vietnam_symbol(symbol)
    if not normalized:
        return False
    return normalized == VNINDEX_SYMBOL or normalized.endswith(".VN")


def is_vietnam_index(symbol: str) -> bool:
    """True when the symbol represents the broad Vietnam index."""
    return normalize_vietnam_symbol(symbol) == VNINDEX_SYMBOL


def to_vnstock_symbol(symbol: str) -> str:
    """Convert TradingAgents/Yahoo-style Vietnam symbols to VNstock symbols."""
    normalized = normalize_vietnam_symbol(symbol)
    if normalized.endswith(".VN"):
        return normalized[:-3]
    return normalized
