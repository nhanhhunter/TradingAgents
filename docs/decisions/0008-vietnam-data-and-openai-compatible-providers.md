# 0008 Vietnam Data and OpenAI-Compatible Providers

Date: 2026-06-12

## Status

Accepted

## Context

Vietnamese market instruments need local market data and news coverage, but the
upstream TradingAgents project still evolves around yfinance and provider
registries. The implementation should remain easy to merge with upstream.

## Decision

Add Vietnam-specific adapters as new modules and route `.VN`/`VNINDEX` through
them from the existing dataflow interface. Add Xiaomi Mimo and 9router through
the existing OpenAI-compatible client registry.

## Alternatives Considered

1. Replace yfinance globally. Rejected because it would change non-Vietnam
   behavior and create avoidable merge conflicts.
2. Fork LangGraph tools for Vietnam. Rejected because preserving tool
   signatures keeps existing agent calls stable.

## Consequences

Positive:

- Vietnam support is additive and isolated.
- Existing non-Vietnam behavior remains intact.
- New provider support follows current registry patterns.

Tradeoffs:

- VNstock live API shape is handled defensively because versions can differ.
- Default tests use mocks instead of proving live source availability.

## Follow-Up

- Add live opt-in smoke tests once stable VNstock credentials are available.
