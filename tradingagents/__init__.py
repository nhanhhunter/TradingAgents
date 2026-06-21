import warnings

# Load deterministic .env files at package import so DEFAULT_CONFIG's env-var
# overlay (and every llm_clients consumer) sees persisted keys regardless of
# entry point. The resolver never walks into parent directories and never
# replaces a non-empty value already exported by the caller.
try:
    from tradingagents.env_config import load_tradingagents_env

    load_tradingagents_env()
except ImportError:
    pass

# langchain-core 1.3.3 calls surface_langchain_deprecation_warnings() in
# its own __init__, which prepends default-action filters for its
# subclassed warning categories. To suppress a specific warning we must
# install our filter AFTER langchain-core has installed its own, so import
# it first. The package is a guaranteed transitive dep via langgraph.
try:
    import langchain_core  # noqa: F401
except ImportError:
    pass

# langgraph-checkpoint 4.0.3 calls Reviver() at module load without an
# explicit allowed_objects, which triggers a noisy pending-deprecation
# warning from langchain-core 1.3.3 on every interpreter start. The fix
# is already merged upstream (langchain-ai/langgraph#7743, 2026-05-08)
# and will arrive in the next langgraph-checkpoint release. Remove this
# block (and the langchain_core preload above) when we bump past it.
warnings.filterwarnings(
    "ignore",
    message=r"The default value of `allowed_objects`.*",
    category=PendingDeprecationWarning,
)
