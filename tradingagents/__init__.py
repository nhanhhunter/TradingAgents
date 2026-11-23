"""TradingAgents: multi-agent LLM financial trading framework."""

__version__ = "0.7.1"

# Load deterministic .env files at package import so DEFAULT_CONFIG's env-var
# overlay (and every llm_clients consumer) sees persisted keys regardless of
# entry point. The resolver never walks into parent directories and never
# replaces a non-empty value already exported by the caller.
try:
    from tradingagents.env_config import load_tradingagents_env

    load_tradingagents_env()
except ImportError:
    pass
