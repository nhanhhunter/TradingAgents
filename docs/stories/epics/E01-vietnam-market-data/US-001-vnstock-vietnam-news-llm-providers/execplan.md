# Exec Plan

## Goal

Add Vietnam market data/news and two OpenAI-compatible LLM providers while
preserving existing TradingAgents contracts.

## Scope

In scope:

- VNstock adapters for Vietnam symbols.
- Vietnam news source normalization and fallback.
- Mimo and 9router provider registry support.
- Mocked tests and documentation updates.

Out of scope:

- Live provider certification.
- Broad yfinance refactors.
- User interface redesign.

## Risk Classification

Risk flags:

- External systems.
- Public contracts.
- Existing behavior.
- Weak proof.
- Multi-domain.

Hard gates:

- External provider behavior.

## Work Phases

1. Add failing tests.
2. Add isolated VN modules.
3. Add narrow routing and provider registry hooks.
4. Update docs.
5. Verify with focused and full tests.
6. Update graphify graph.

## Stop Conditions

Pause for human confirmation if:

- VNstock requires an incompatible public signature.
- Verification requires weakening existing tests.
- Provider behavior requires storing secrets in source-controlled files.
