# Overview

## Current Behavior

TradingAgents defaults to yfinance for market data and Yahoo/global sources for
news. Vietnam tickers such as `VCB.VN` and `VNINDEX` do not have a dedicated
Vietnam data path. Xiaomi Mimo and 9router are not selectable LLM providers.

## Target Behavior

Vietnam equities entered with `.VN` and `VNINDEX` route to VNstock-backed price,
indicator, fundamentals, and Vietnam news adapters while non-Vietnam tickers keep
the existing provider chain. Xiaomi Mimo and 9router are available through the
existing OpenAI-compatible client.

## Affected Users

- CLI and package users analyzing Vietnamese market instruments.
- Users selecting OpenAI-compatible LLM providers.

## Affected Product Docs

- `README.md`
- `.env.example`

## Non-Goals

- No rewrite of yfinance adapters.
- No live API calls in default tests.
- No UI redesign.
