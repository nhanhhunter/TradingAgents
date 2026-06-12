"""VNstock-backed market data adapter.

The public functions intentionally mirror the yfinance adapter signatures so
LangGraph tool calls can route Vietnamese tickers here without changing the
tool schemas exposed to LLMs.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any

import pandas as pd

from .stockstats_utils import _clean_dataframe, filter_financials_by_date
from .symbol_utils import NoMarketDataError
from .vietnam_symbols import is_vietnam_index, to_vnstock_symbol

logger = logging.getLogger(__name__)

VNSTOCK_API_KEY_PATH = Path.home() / ".vnstock" / "api_key.json"


def _vnstock_register_user(*, api_key: str) -> None:
    """Register a VNstock API key without importing vnstock at module import."""
    from vnstock import register_user

    register_user(api_key=api_key)


def ensure_vnstock_credentials() -> None:
    """Initialize VNstock credentials from ``VNSTOCK_API_KEY`` when needed.

    VNstock reads credentials from ``~/.vnstock/api_key.json``. If that file is
    already present, this is a no-op. If not, and ``VNSTOCK_API_KEY`` is set,
    delegate creation to VNstock's registration helper. The key is never
    logged or written by this module directly.
    """
    if VNSTOCK_API_KEY_PATH.exists():
        return
    api_key = os.environ.get("VNSTOCK_API_KEY")
    if not api_key:
        logger.info(
            "VNSTOCK_API_KEY is not set; VNstock will run with its configured guest tier."
        )
        return
    _vnstock_register_user(api_key=api_key)


def _stock_client(symbol: str) -> Any:
    """Return a VNstock stock client across supported VNstock versions."""
    ensure_vnstock_credentials()
    vn_symbol = to_vnstock_symbol(symbol)

    try:
        from vnstock import Vnstock

        return Vnstock().stock(symbol=vn_symbol, source="VCI")
    except Exception:
        from vnstock import stock

        return stock(symbol=vn_symbol, source="VCI")


def _quote_client(symbol: str) -> Any:
    client = _stock_client(symbol)
    quote = getattr(client, "quote", None)
    return quote if quote is not None else client


def _company_client(symbol: str) -> Any:
    client = _stock_client(symbol)
    company = getattr(client, "company", None)
    return company if company is not None else client


def _finance_client(symbol: str) -> Any:
    client = _stock_client(symbol)
    finance = getattr(client, "finance", None)
    return finance if finance is not None else client


def _history_frame(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    quote = _quote_client(symbol)
    if hasattr(quote, "history"):
        return quote.history(start=start_date, end=end_date, interval="1D")
    if hasattr(quote, "historical_data"):
        return quote.historical_data(start_date=start_date, end_date=end_date)
    raise RuntimeError("VNstock quote client does not expose a history method")


def get_price_history_frame(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Return normalized VNstock OHLCV rows for internal calculations."""
    return _normalize_ohlcv(_history_frame(symbol, start_date, end_date))


def _normalize_ohlcv(data: pd.DataFrame) -> pd.DataFrame:
    if data is None or data.empty:
        return pd.DataFrame()

    frame = data.copy()
    rename = {
        "time": "Date",
        "date": "Date",
        "tradingDate": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
    frame = frame.rename(columns={c: rename.get(c, c) for c in frame.columns})
    if "Date" not in frame.columns:
        frame = frame.reset_index().rename(columns={"index": "Date"})
    wanted = [c for c in ["Date", "Open", "High", "Low", "Close", "Volume"] if c in frame.columns]
    frame = frame[wanted]
    frame = _clean_dataframe(frame)
    for col in ["Open", "High", "Low", "Close"]:
        if col in frame.columns:
            frame[col] = frame[col].round(2)
    return frame


def _statement_frame(symbol: str, statement: str, freq: str) -> pd.DataFrame:
    finance = _finance_client(symbol)
    period = "quarter" if freq.lower() == "quarterly" else "year"
    candidates = {
        "balance_sheet": ("balance_sheet", "balance_sheet_report"),
        "cash_flow": ("cash_flow", "cashflow", "cash_flow_report"),
        "income_statement": ("income_statement", "income_statement_report"),
    }[statement]
    for name in candidates:
        method = getattr(finance, name, None)
        if method is None:
            continue
        try:
            return method(period=period)
        except TypeError:
            return method(freq=period)
    raise RuntimeError(f"VNstock finance client does not expose {statement}")


def _format_statement(
    ticker: str,
    statement_title: str,
    data: pd.DataFrame,
    freq: str,
    curr_date: str | None,
) -> str:
    if data is None or data.empty:
        raise NoMarketDataError(ticker, to_vnstock_symbol(ticker), f"no {statement_title} data")
    filtered = filter_financials_by_date(data, curr_date)
    if filtered.empty:
        filtered = data
    header = f"# {statement_title} data for {ticker.upper()} (VNstock: {to_vnstock_symbol(ticker)}, {freq})\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    return header + filtered.to_csv(index=True)


def _index_no_statement(ticker: str) -> str:
    return (
        f"NO_DATA_AVAILABLE: {ticker.upper()} is a Vietnam market index and does not "
        "have company financial statements. Do not estimate or fabricate company "
        "fundamental values for this index."
    )


def get_vnstock_data_online(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")
    data = get_price_history_frame(symbol, start_date, end_date)
    if data.empty:
        raise NoMarketDataError(symbol, to_vnstock_symbol(symbol), "VNstock returned no rows")

    header = f"# Stock data for {symbol.upper()} (VNstock: {to_vnstock_symbol(symbol)}) from {start_date} to {end_date}\n"
    header += f"# Total records: {len(data)}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    return header + data.to_csv(index=False)


def get_stock_stats_indicators_window(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    from dateutil.relativedelta import relativedelta
    from stockstats import wrap

    curr_date_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    before = curr_date_dt - relativedelta(days=max(look_back_days, 30) + 260)
    data = _normalize_ohlcv(
        _history_frame(symbol, before.strftime("%Y-%m-%d"), curr_date)
    )
    if data.empty:
        raise NoMarketDataError(symbol, to_vnstock_symbol(symbol), "no OHLCV rows for indicators")

    df = wrap(data)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df[indicator]

    start = curr_date_dt - relativedelta(days=look_back_days)
    values = []
    current = curr_date_dt
    while current >= start:
        date_str = current.strftime("%Y-%m-%d")
        match = df[df["Date"] == date_str]
        if match.empty:
            value = "N/A: Not a trading day (weekend or holiday)"
        else:
            raw = match[indicator].iloc[0]
            value = "N/A" if pd.isna(raw) else str(raw)
        values.append(f"{date_str}: {value}")
        current = current - relativedelta(days=1)

    return (
        f"## {indicator} values from {start.strftime('%Y-%m-%d')} to {curr_date} "
        f"for {symbol.upper()} (VNstock):\n\n" + "\n".join(values)
    )


def get_fundamentals(
    ticker: Annotated[str, "ticker symbol of the company"],
    curr_date: Annotated[str, "current date (not used for yfinance)"] = None
):
    if is_vietnam_index(ticker):
        return _index_no_statement(ticker)

    lines = []
    try:
        company = _company_client(ticker)
        overview_method = getattr(company, "overview", None)
        overview = overview_method() if overview_method else None
        if isinstance(overview, pd.DataFrame) and not overview.empty:
            row = overview.iloc[0].to_dict()
        elif isinstance(overview, dict):
            row = overview
        else:
            row = {}
        for key, value in row.items():
            if pd.notna(value) and value != "":
                lines.append(f"{key}: {value}")
    except Exception as exc:
        logger.debug("VNstock company overview failed for %s: %s", ticker, exc)

    try:
        finance = _finance_client(ticker)
        ratio_method = getattr(finance, "ratio", None)
        ratios = ratio_method(period="quarter") if ratio_method else None
        if isinstance(ratios, pd.DataFrame) and not ratios.empty:
            latest = ratios.iloc[0].to_dict()
            for key, value in latest.items():
                if pd.notna(value) and value != "":
                    lines.append(f"{key}: {value}")
    except Exception as exc:
        logger.debug("VNstock ratios failed for %s: %s", ticker, exc)

    if not lines:
        raise NoMarketDataError(ticker, to_vnstock_symbol(ticker), "no fundamentals returned")

    header = f"# Company Fundamentals for {ticker.upper()} (VNstock: {to_vnstock_symbol(ticker)})\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    return header + "\n".join(lines)


def get_balance_sheet(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[str, "current date in YYYY-MM-DD format"] = None
):
    if is_vietnam_index(ticker):
        return _index_no_statement(ticker)
    data = _statement_frame(ticker, "balance_sheet", freq)
    return _format_statement(ticker, "Balance Sheet", data, freq, curr_date)


def get_cashflow(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[str, "current date in YYYY-MM-DD format"] = None
):
    if is_vietnam_index(ticker):
        return _index_no_statement(ticker)
    data = _statement_frame(ticker, "cash_flow", freq)
    return _format_statement(ticker, "Cash Flow", data, freq, curr_date)


def get_income_statement(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[str, "current date in YYYY-MM-DD format"] = None
):
    if is_vietnam_index(ticker):
        return _index_no_statement(ticker)
    data = _statement_frame(ticker, "income_statement", freq)
    return _format_statement(ticker, "Income Statement", data, freq, curr_date)


def get_company_news(ticker: str, start_date: str, end_date: str) -> str:
    """Best-effort VNstock company news, falling back to no-news text."""
    if is_vietnam_index(ticker):
        return f"No VNstock company news found for {ticker.upper()}"
    try:
        company = _company_client(ticker)
        for method_name in ("news", "events"):
            method = getattr(company, method_name, None)
            if method is None:
                continue
            data = method()
            if isinstance(data, pd.DataFrame) and not data.empty:
                return (
                    f"## {ticker.upper()} VNstock Company News, from {start_date} to {end_date}:\n\n"
                    + data.to_csv(index=False)
                )
    except Exception as exc:
        logger.debug("VNstock company news failed for %s: %s", ticker, exc)
    return f"No VNstock company news found for {ticker.upper()} between {start_date} and {end_date}"
