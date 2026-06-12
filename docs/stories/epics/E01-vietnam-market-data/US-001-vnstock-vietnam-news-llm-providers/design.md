# Design

## Domain Model

Vietnam symbols are detected by `.VN` suffix or exact `VNINDEX`. VNstock symbols
strip `.VN` before provider calls. `VNINDEX` is an index and has no company
financial statements.

## Application Flow

`tradingagents.dataflows.interface.route_to_vendor` prepends Vietnam-specific
vendors for Vietnam symbols, then falls back to configured vendors. Non-Vietnam
symbols keep the current routing behavior.

## Interface Contract

Existing LangGraph tool signatures remain unchanged. New provider keys are:
`mimo` and `9router`. New environment variables are `MIMO_API_KEY`,
`9ROUTER_API_KEY`, and optional `VNSTOCK_API_KEY`.

## Data Model

No persistent schema changes. VNstock credentials are delegated to VNstock's own
`~/.vnstock/api_key.json` mechanism.

## UI / Platform Impact

The CLI provider dropdown adds Xiaomi Mimo and 9router. README and `.env.example`
document the new configuration.

## Observability

VNstock guest-tier credential absence is logged without exposing secrets.

## Alternatives Considered

1. Replace yfinance globally: rejected because it would increase upstream merge
   conflicts and change non-Vietnam behavior.
2. Require users to set `data_vendors`: rejected because `.VN`/`VNINDEX` are
   deterministic enough for automatic routing.
