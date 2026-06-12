# Graph Report - TradingAgents  (2026-06-12)

## Corpus Check
- 156 files · ~243,483 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1621 nodes · 2753 edges · 106 communities (98 shown, 8 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `263d0569`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 101|Community 101]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]

## God Nodes (most connected - your core abstractions)
1. `make_log()` - 40 edges
2. `TradingAgentsGraph` - 38 edges
3. `TestTradingMemoryLogCore` - 37 edges
4. `get_instrument_context_from_state()` - 32 edges
5. `BaseLLMClient` - 32 edges
6. `TradingMemoryLog` - 31 edges
7. `TestDeferredReflection` - 29 edges
8. `get_capabilities()` - 28 edges
9. `get_language_instruction()` - 27 edges
10. `Glossary` - 27 edges

## Surprising Connections (you probably didn't know these)
- `MessageBuffer` --uses--> `AnalystWallTimeTracker`  [INFERRED]
  cli/main.py → tradingagents/graph/analyst_execution.py
- `MessageBuffer` --uses--> `TradingAgentsGraph`  [INFERRED]
  cli/main.py → tradingagents/graph/trading_graph.py
- `Path` --uses--> `AnalystWallTimeTracker`  [INFERRED]
  cli/main.py → tradingagents/graph/analyst_execution.py
- `Path` --uses--> `TradingAgentsGraph`  [INFERRED]
  cli/main.py → tradingagents/graph/trading_graph.py
- `CryptoAssetModeTests` --uses--> `Propagator`  [INFERRED]
  tests/test_crypto_asset_mode.py → tradingagents/graph/propagation.py

## Import Cycles
- None detected.

## Communities (106 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (34): ChatOpenAI, DeepSeekChatOpenAI, _input_to_messages(), MinimaxChatOpenAI, NormalizedChatOpenAI, MiniMax-specific overrides on top of the OpenAI-compatible client.      M2.x r, ChatOpenAI with normalized content output and capability-aware binding.      T, Normalise a langchain LLM input to a list of message objects.      Accepts a l (+26 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (37): Validate ``value`` is safe to interpolate into a filesystem path.      Tickers, safe_ticker_component(), save_output(), checkpoint_step(), clear_checkpoint(), _db_path(), get_checkpointer(), has_checkpoint() (+29 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (36): get_category_for_method(), Get the category that contains the specified method., Route method calls to appropriate vendor implementation with fallback support., route_to_vendor(), Resolve ticker identity once and return the full instrument context., BuildInstrumentContextTests, ContextAnchoredPlaceholderTests, Tests for deterministic instrument-identity resolution (#814) and the context-a (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (15): make_log(), Calling store_decision twice with same (ticker, date) stores only one entry., batch_update_with_outcomes resolves multiple pending entries in one write., Rating: X' label wins even when an opposing rating word appears earlier in prose, LLM decision containing '---' must not corrupt the entry., Only the n_same most recent same-ticker entries are included., Only the n_cross most recent cross-ticker entries are included., Without max_entries, all resolved entries are kept. (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (34): AlphaVantageNotConfiguredError, AlphaVantageRateLimitError, _filter_csv_by_date_range(), format_datetime_for_api(), get_api_key(), _make_api_request(), Filter CSV data to include only rows within the specified date range.      Arg, Raised when Alpha Vantage is selected but no API key is configured.      Subcl (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (37): [0.1.0] — 2025-06-05, [0.1.1] — 2025-06-07, [0.2.0] — 2026-02-04, [0.2.1] — 2026-03-15, [0.2.2] — 2026-03-22, [0.2.3] — 2026-03-29, [0.2.4] — 2026-04-25, [0.2.5] — 2026-05-11 (+29 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (16): get_capabilities(), ModelCapabilities, Declarative per-model capability table for OpenAI-compatible providers.  This, Resolve capabilities by exact ID, then pattern, then default., What an OpenAI-compatible model accepts at the API level., Unit tests for the LLM capability table., deepseek-chat must NOT match the v\\d regex., Capability rows are immutable so they can be safely shared. (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (14): Only the matching entry is modified; all other entries remain unchanged., A pre-existing .tmp file is overwritten; the log is correctly updated., All fields intact and blank line between tag and DECISION preserved after update, Empty DataFrame → returns (None, None, None), no crash., SPY having fewer rows than the stock must not raise IndexError., config['benchmark_ticker'] wins for every ticker., Known suffixes route to their regional index., A-share tickers route to their exchange composite (uses the real         defaul (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (26): analyze(), classify_message_type(), create_layout(), display_complete_report(), extract_content_string(), format_tokens(), format_tool_args(), MessageBuffer (+18 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (29): get_model_options(), Return shared model options for a provider and selection mode., ModelOption, Tests for OLLAMA_BASE_URL env-var override across CLI and client paths., Restore module state after this file's importlib.reload() calls.      Several, If user sets OLLAMA_BASE_URL=0.0.0.128, advise on the expected shape., A remote host with no :11434 gets a soft hint about port mismatch., Local host without port shouldn't trigger the remote-port hint. (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (12): PortfolioDecision, Structured output produced by the Portfolio Manager.      The model fills ever, _make_pm_state(), Tests for TradingMemoryLog — storage, deferred reflection, PM injection, legacy, Minimal AgentState dict for portfolio_manager_node., PM prompt omits the lessons section entirely when past_context is empty., The structured PortfolioDecision is rendered to markdown that         downstrea, If a provider does not support with_structured_output, the agent         falls (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (17): fetch_reddit_posts(), _fetch_subreddit(), _fetch_subreddit_rss(), _iso_to_timestamp(), Reddit search fetcher for ticker-specific discussion posts.  Primary path is R, Fetch recent Reddit posts mentioning ``ticker`` across finance     subreddits a, Parse an Atom ``published`` timestamp to a UTC epoch, or None., Reduce the HTML body Reddit embeds in an Atom entry to plain text. (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (27): Agent, Backlog Outcome Loop, Component Taxonomy, Context Phase, Context Score, Context Score, Durable Layer, Entropy Score (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.07
Nodes (45): create_fundamentals_analyst(), create_market_analyst(), create_news_analyst(), _build_system_message(), create_sentiment_analyst(), create_social_media_analyst(), Sentiment analyst — multi-source sentiment analysis for a target ticker.  Prev, Assemble the sentiment-analyst system message with structured data blocks. (+37 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (19): AgentState, ConditionalLogic, ConditionalLogic, Initialize with configuration parameters., Determine if market analysis should continue., Determine if sentiment-analyst tool round should continue.          Method nam, Determine if news analysis should continue., Determine if fundamentals analysis should continue. (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.14
Nodes (27): install-harness.sh script, agent_shim_block(), append_or_replace_agent_harness_block(), backup_agent_file(), backup_claude_file(), can_prompt(), check_protected_target_paths(), claude_shim_block() (+19 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (24): get_analysis_date(), get_user_selections(), Get all user selections before starting the analysis display., Get the analysis date from user input., ask_anthropic_effort(), ask_gemini_thinking_config(), ask_glm_region(), ask_minimax_region() (+16 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (8): AnalystExecutionPlan, AnalystNodeSpec, AnalystWallTimeTracker, build_analyst_execution_plan(), get_initial_analyst_node(), sync_analyst_tracker_from_chunk(), AnalystExecutionPlanTests, AnalystWallTimeTrackerTests

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (10): Propagator, Handles state initialization and propagation through the graph., Initialize with configuration parameters., Create the initial state for the agent graph.          ``instrument_context``, Get arguments for the graph invocation.          Args:             callbacks:, PortfolioDecision, Any, TypedDict (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (23): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+15 more)

### Community 20 - "Community 20"
Cohesion: 0.13
Nodes (14): build_verified_market_snapshot(), _fmt(), Deterministic market-data verification snapshot.  The market analyst is an LLM, OHLCV on or before curr_date, date-sorted. Raises if nothing usable.      ``lo, Render a ground-truth snapshot: latest OHLCV row, indicators, recent closes., _verified_rows(), DataFrame, Tests for the deterministic market-data verification snapshot (#830/#881). (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.10
Nodes (18): get_api_key_env(), Canonical provider -> API-key env-var mapping.  A single source of truth for w, Return the env var name for `provider`'s API key, or None if not applicable., cli_utils(), Tests for the canonical provider->env-var mapping and the CLI key-prompt helper., When key is missing, user-pasted value must be written to .env AND os.environ., Empty prompt response (user cancelled) must not write to .env., An existing .env with other keys must be preserved on writeback. (+10 more)

### Community 22 - "Community 22"
Cohesion: 0.09
Nodes (22): Analyst Team, Checkpoint resume, Citation, CLI Usage, Contributing, Decision log, Docker, Implementation Details (+14 more)

### Community 23 - "Community 23"
Cohesion: 0.15
Nodes (8): Replace pending tag and append REFLECTION section using atomic write., Append-only markdown log of trading decisions and reflections., Apply multiple outcome updates in a single read + atomic write.          Each, Drop oldest resolved blocks when their count exceeds max_entries.          Pen, Parse all entries from log. Returns list of dicts., Return entries with outcome:pending (for Phase B)., Return formatted past context string for agent prompt injection., TradingMemoryLog

### Community 24 - "Community 24"
Cohesion: 0.08
Nodes (43): PortfolioRating, Pydantic schemas used by agents that produce structured output.  The framework, Structured transaction proposal produced by the Trader.      The trader reads, Render a TraderProposal to markdown.      The trailing ``FINAL TRANSACTION PRO, Render a PortfolioDecision back to the markdown shape the rest of the system exp, Discrete sentiment direction produced by the Sentiment Analyst.      Six tiers, Structured sentiment report produced by the Sentiment Analyst.      Replaces t, Render a SentimentReport to the markdown shape the rest of the system expects. (+35 more)

### Community 25 - "Community 25"
Cohesion: 0.16
Nodes (12): get_config(), initialize_config(), Initialize the configuration with default values., Update the configuration with custom values.      Dict-valued keys (e.g. ``dat, Get the current configuration., set_config(), DataflowsConfigIsolationTests, Config isolation: get/set must not leak nested-dict references. (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (6): TestParseRating, Append-only markdown decision log for TradingAgents., Append pending entry at end of propagate(). No LLM call., parse_rating(), Shared 5-tier rating vocabulary and a deterministic heuristic parser.  The sam, Heuristically extract a 5-tier rating from prose text.      Two-pass strategy:

### Community 27 - "Community 27"
Cohesion: 0.26
Nodes (11): Copy-HarnessFile(), Get-AgentShimBlock(), Get-DefaultCliBaseUrl(), Install-HarnessCliBinary(), Fail(), Merge-Gitignore(), Read-CliReleaseTag(), Read-RemoteText() (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.23
Nodes (11): AnalystType, AssetType, AnalystType, AssetType, detect_asset_type(), filter_analysts_for_asset_type(), get_analysis_date(), Select analysts using an interactive checkbox. (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.19
Nodes (15): _clean_dataframe(), _ensure_date_column(), filter_financials_by_date(), load_ohlcv(), Drop financial statement columns (fiscal period timestamps) after curr_date., Normalize the date column to ``Date``.      Some yfinance builds leave the ind, Normalize a stock DataFrame for stockstats: parse dates, drop invalid rows, fill, Fetch OHLCV data with caching, filtered to prevent look-ahead bias.      Downl (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.22
Nodes (5): FinancialSituationMemory must not be importable from the memory module., rank_bm25 must not be present in the memory module namespace., TradingAgentsGraph must not expose reflect_and_remember., propagate() completes and stores the decision after the redesign., TestLegacyRemoval

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (7): is_yahoo_safe(), normalize_symbol(), True when ``symbol`` only contains characters Yahoo symbols use., Map a user/broker symbol to its canonical Yahoo Finance symbol.      Resolutio, Tests for symbol normalization and the no-data routing sentinel., TestIsYahooSafe, TestNormalizeSymbol

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (10): BaseCallbackHandler, Any, Callback handler that tracks LLM calls, tool calls, and token usage., Increment LLM call counter when an LLM starts., Increment LLM call counter when a chat model starts., Extract token usage from LLM response., Increment tool call counter when a tool starts., Return current statistics. (+2 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (15): get_vendor(), Get the configured vendor for a data category or specific tool method.     Tool, Execute a yfinance call with exponential backoff on rate limits.      yfinance, yf_retry(), get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement() (+7 more)

### Community 34 - "Community 34"
Cohesion: 0.18
Nodes (9): Get provider-specific kwargs for LLM client creation., Create tool nodes for different data sources using abstract methods., Pick the benchmark ticker for alpha calculation against ``ticker``.          `, Fetch raw and alpha return for ticker over holding_days from trade_date., Resolve pending log entries for ticker at the start of a new run.          Fet, Main class that orchestrates the trading agents framework., Initialize the trading agents graph and components.          Args:, TradingAgentsGraph (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.12
Nodes (9): When max_entries is set and exceeded, oldest resolved entries are pruned., Pending entries (unresolved) are kept regardless of the cap., No rotation when resolved count <= max_entries., Store a decision then immediately resolve it via the API., Same-ticker entries in same-ticker section; cross-ticker entries in cross-ticker, Cross-ticker entries show only the REFLECTION text, not the full DECISION., More than 5 same-ticker completed entries → only 5 injected., More than 3 cross-ticker completed entries → only 3 injected. (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (8): _ohlcv(), DataFrame, Tests for tolerating a non-`Date` index column in stockstats_utils (#890).  Gu, OHLCV frame whose date column is named `date_col`., A frame with `index` instead of `Date` must still clean to a         usable, da, stockstats must compute indicators on a frame whose date column         arrived, TestCleanDataframeAcrossVersions, TestEnsureDateColumn

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (10): ChatAnthropic, AnthropicClient, NormalizedChatAnthropic, Whether Anthropic accepts the ``effort`` parameter for this model., ChatAnthropic with normalized content output.      Claude models with extended, Client for Anthropic Claude models., Return configured ChatAnthropic instance., Validate model for Anthropic. (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.17
Nodes (6): NoMarketDataError, Raised when a vendor returns no rows/records for a symbol.      Carries both t, Tests that empty vendor results never become fabricated data.  Covers two syst, TestLoadOhlcvNoPoison, TestRouteToVendorSentinel, TestNoMarketDataError

### Community 39 - "Community 39"
Cohesion: 0.13
Nodes (14): Decision Records, Done Definition, Durable Layer, Future Validation Ladder, Growth Rule, Harness, Harness Change Policy, Harness v0 Scope (+6 more)

### Community 40 - "Community 40"
Cohesion: 0.22
Nodes (6): ABC, BaseLLMClient, Abstract base class for LLM clients., Return the provider name used in warning messages., Warn when the model is outside the known list for the provider., Validate that the model is supported by this client.

### Community 41 - "Community 41"
Cohesion: 0.18
Nodes (9): _llm_provider_table(), provider_default_url(), (display_name, provider_key, base_url) for every supported provider.      Shar, Return the default backend URL for a provider key, or None if unknown., Select the LLM provider and its API endpoint., select_llm_provider(), Tests for env-driven CLI behavior (#897, #873).  The config-layer override (TR, TestCliSkipsPromptsFromEnv (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.14
Nodes (13): Current Assessment, H0 - Bare Environment, H1 - Scaffolding And Policy, H2 - Durable State And Observability, H3 - Active Observability And Evolution, H4 - Automated Verification, H5 - Self-Improving Harness, Harness Maturity Ladder (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (13): Adequate Trace (Standard), Detailed (score: 3), Examples, Field Reference, Friction Capture Protocol, Good Trace (Detailed), Insufficient Trace, Lane Mapping (+5 more)

### Community 44 - "Community 44"
Cohesion: 0.21
Nodes (13): Tests for TRADINGAGENTS_* env-var overlay onto DEFAULT_CONFIG., Set/clear env vars then reload default_config to re-evaluate DEFAULT_CONFIG., Empty TRADINGAGENTS_* values must not clobber the built-in default., Garbage int values should surface a ValueError at import, not silently misconfig, Env vars outside _ENV_OVERRIDES must not bleed into DEFAULT_CONFIG., _reload_with_env(), test_bool_coercion(), test_empty_env_value_is_passthrough() (+5 more)

### Community 45 - "Community 45"
Cohesion: 0.23
Nodes (6): _capture_kwargs(), Tests for Anthropic effort-parameter gating (#831).  Haiku 4.5 (and current Ha, Forward-compat: new Opus/Sonnet versions don't need a code change., Default is conservative — unknown models don't get effort to avoid 400s., Skipping effort must not break other passthrough kwargs., TestEffortGate

### Community 46 - "Community 46"
Cohesion: 0.83
Nodes (3): build-harness-cli-release.sh script, fail(), usage()

### Community 47 - "Community 47"
Cohesion: 0.17
Nodes (12): _fetch_openrouter_models(), _prompt_custom_model_id(), Fetch available models from the OpenRouter API., Select an OpenRouter model from the newest available, or enter a custom ID., Prompt user to type a custom model ID., Select a model for the given provider and mode (quick/deep)., Select shallow thinking llm engine using an interactive selection., Select deep thinking llm engine using an interactive selection. (+4 more)

### Community 48 - "Community 48"
Cohesion: 0.17
Nodes (11): Additive Behavior, Context Engineering Rules, Context Phases, Implementation Phase, Intake Phase, Planning Phase, Retrieval Triggers, Review Checklist (+3 more)

### Community 49 - "Community 49"
Cohesion: 0.20
Nodes (7): GoogleClient, Client for Google Gemini models., Return configured ChatGoogleGenerativeAI instance., Validate model for Google., Verify GoogleClient accepts unified api_key parameter., TestGoogleApiKeyStandardization, Any

### Community 50 - "Community 50"
Cohesion: 0.23
Nodes (4): Tests for the configurable sampling temperature (#178/#168).  Temperature is a, _get_provider_kwargs float-coerces and forwards temperature, or omits it., TestProviderKwargsTemperature, TestTemperatureEnvOverlay

### Community 51 - "Community 51"
Cohesion: 0.18
Nodes (10): Classification, Feature Intake, High-Risk, Input Types, Intake Flow, Lanes, Normal, Output (+2 more)

### Community 52 - "Community 52"
Cohesion: 0.21
Nodes (7): Read the 5-tier rating out of a Portfolio Manager decision., Return one of Buy / Overweight / Hold / Underweight / Sell., SignalProcessor, Tests for the shared rating heuristic and the SignalProcessor adapter.  The Po, SignalProcessor must not invoke the LLM it was constructed with —         the r, TestSignalProcessor, Any

### Community 54 - "Community 54"
Cohesion: 0.16
Nodes (9): create_llm_client(), Create an LLM client for the specified provider.      Provider modules are imp, OpenAIClient, Client for OpenAI, Ollama, OpenRouter, and xAI providers.      For native Open, Return configured ChatOpenAI instance., Validate model for the provider., TestTemperatureForwarding, BaseLLMClient (+1 more)

### Community 55 - "Community 55"
Cohesion: 0.18
Nodes (10): Architecture Questions, Candidate Epics, Candidate Product Docs, First Story Candidates, Harness Delta, Open Decisions, Project Summary, Source (+2 more)

### Community 56 - "Community 56"
Cohesion: 0.18
Nodes (10): Acceptance Criteria, Design Notes, Evidence, Harness Delta, Lane, Product Contract, Relevant Product Docs, Status (+2 more)

### Community 58 - "Community 58"
Cohesion: 0.33
Nodes (3): BaseLLMClient, DummyLLMClient, ModelValidationTests

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (5): get_ticker(), normalize_ticker_symbol(), Prompt the user to enter a ticker symbol, preserving exchange suffixes.      U, Normalize ticker input while preserving exchange suffixes., TickerSymbolHandlingTests

### Community 60 - "Community 60"
Cohesion: 0.22
Nodes (8): Architecture, Candidate Structure, Command/Query Boundary, Default Layering, Dependency Rule, Discovery Before Shape, Observability Contract, Parse-First Boundary Rule

### Community 61 - "Community 61"
Cohesion: 0.22
Nodes (8): Alternatives Considered, Application Flow, Data Model, Design, Domain Model, Interface Contract, Observability, UI / Platform Impact

### Community 62 - "Community 62"
Cohesion: 0.21
Nodes (8): get_known_models(), Shared model catalog for CLI selections and validation., Build known model names from the shared CLI catalog., Default base URL for ``provider``, with env-var overrides where defined., _resolve_provider_base_url(), Model name validators for each provider., Check if model name is valid for the given provider.      For ollama, openrout, validate_model()

### Community 63 - "Community 63"
Cohesion: 0.32
Nodes (7): _extract_article_data(), get_global_news_yfinance(), get_news_yfinance(), yfinance-based news data fetching functions., Retrieve global/macro economic news using yfinance Search.      Args:, Extract article data from yfinance news format (handles nested 'content' structu, Retrieve news for a specific stock ticker using yfinance.      Args:

### Community 64 - "Community 64"
Cohesion: 0.25
Nodes (7): 0003 Generic Spec Intake Harness, Alternatives Considered, Consequences, Context, Decision, Follow-Up, Status

### Community 65 - "Community 65"
Cohesion: 0.25
Nodes (7): 0004 SQLite Durable Layer, Alternatives Considered, Consequences, Context, Decision, Follow-Up, Status

### Community 66 - "Community 66"
Cohesion: 0.25
Nodes (7): 0005 Prebuilt Rust Harness CLI, Alternatives Considered, Consequences, Context, Decision, Follow-Up, Status

### Community 67 - "Community 67"
Cohesion: 0.25
Nodes (7): 0006 Phase 4 Benchmark Triage, Alternatives Considered, Consequences, Context, Decision, Follow-Up, Status

### Community 68 - "Community 68"
Cohesion: 0.25
Nodes (7): 0007 Improvement Proposal Rules, Alternatives Considered, Consequences, Context, Decision, Follow-Up, Status

### Community 69 - "Community 69"
Cohesion: 0.25
Nodes (7): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 70 - "Community 70"
Cohesion: 0.25
Nodes (7): Future Command Contract, Harness CLI, Installer, Release Packaging, Rust CLI Commands, Schema Migrations, Scripts

### Community 71 - "Community 71"
Cohesion: 0.25
Nodes (7): Alternatives Considered, Consequences, Context, Decision, Follow-Up, NNNN Decision Title, Status

### Community 72 - "Community 72"
Cohesion: 0.17
Nodes (8): AzureChatOpenAI, AzureOpenAIClient, NormalizedAzureChatOpenAI, AzureChatOpenAI with normalized content output., Client for Azure OpenAI deployments.      Requires environment variables:, Return configured AzureChatOpenAI instance., Azure accepts any deployed model name., Any

### Community 73 - "Community 73"
Cohesion: 0.33
Nodes (5): ChatGoogleGenerativeAI, normalize_content(), Normalize LLM response content to a plain string.      Multiple providers (Ope, NormalizedChatGoogleGenerativeAI, ChatGoogleGenerativeAI with normalized content output.      Gemini 3 models re

### Community 74 - "Community 74"
Cohesion: 0.29
Nodes (5): display_announcements(), fetch_announcements(), Fetch announcements from endpoint. Returns dict with announcements and settings., Display announcements panel. Prompts for Enter if require_attention is True., Console

### Community 75 - "Community 75"
Cohesion: 0.29
Nodes (6): Exec Plan, Goal, Risk Classification, Scope, Stop Conditions, Work Phases

### Community 76 - "Community 76"
Cohesion: 0.29
Nodes (6): Affected Product Docs, Affected Users, Current Behavior, Non-Goals, Overview, Target Behavior

### Community 77 - "Community 77"
Cohesion: 0.29
Nodes (6): Acceptance Evidence, Commands, Fixtures, Proof Strategy, Test Plan, Validation

### Community 78 - "Community 78"
Cohesion: 0.29
Nodes (6): Commands Run, Evidence, Gaps, Results, Scope, Validation Report

### Community 79 - "Community 79"
Cohesion: 0.33
Nodes (5): 0001 Harness-First Development, Consequences, Context, Decision, Status

### Community 80 - "Community 80"
Cohesion: 0.33
Nodes (5): 0002 Seed Specification Product Lifecycle, Consequences, Context, Decision, Status

### Community 81 - "Community 81"
Cohesion: 0.33
Nodes (5): Coverage Summary, File Inventory, Harness Components, NexAU Cross-Reference, Responsibility Map

### Community 82 - "Community 82"
Cohesion: 0.33
Nodes (5): Commit Proposals, Generate Proposals, Improvement Protocol, Review Rules, Validation

### Community 83 - "Community 83"
Cohesion: 0.40
Nodes (4): Current State, Documentation Map, Folders, Main Files

### Community 84 - "Community 84"
Cohesion: 0.40
Nodes (4): Evidence Rules, Matrix, Status Values, Test Matrix

### Community 85 - "Community 85"
Cohesion: 0.12
Nodes (10): Initialize the reflector with an LLM., Concise prompt for reflect_on_final_decision (Phase B log entries).          P, Single reflection call on the final trade decision with outcome context., Handles reflection on trading decisions., Reflector, Extract the 5-tier portfolio rating from the Portfolio Manager's decision.  Th, Return figures are present in the human message sent to the LLM., benchmark_name appears in the prompt label, not 'SPY' hardcoded. (+2 more)

### Community 86 - "Community 86"
Cohesion: 0.40
Nodes (4): High-Risk Story, Normal Story, Status Flow, Stories

### Community 88 - "Community 88"
Cohesion: 0.50
Nodes (3): Agent Instructions, graphify, Harness

### Community 89 - "Community 89"
Cohesion: 0.50
Nodes (3): Checks, Harness Audit, Score

### Community 90 - "Community 90"
Cohesion: 0.50
Nodes (3): Harness Backlog, Items, Template

### Community 91 - "Community 91"
Cohesion: 0.50
Nodes (3): Compiled Harness Commands, Tool Registry, Validation Rules

### Community 92 - "Community 92"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 93 - "Community 93"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 94 - "Community 94"
Cohesion: 0.50
Nodes (3): For /graphify explain, For /graphify path, graphify reference: query, path, explain

### Community 95 - "Community 95"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 96 - "Community 96"
Cohesion: 0.50
Nodes (3): _price_df(), Only 1 data point available → returns (None, None, None), no crash., Minimal DataFrame matching yfinance .history() output shape.

## Knowledge Gaps
- **299 isolated node(s):** `Console`, `LLMResult`, `DataFrame`, `DataFrame`, `SavePathType` (+294 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_llm_client()` connect `Community 54` to `Community 34`, `Community 4`, `Community 37`, `Community 40`, `Community 72`, `Community 13`, `Community 49`, `Community 50`, `Community 85`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `TradingAgentsGraph` connect `Community 34` to `Community 1`, `Community 2`, `Community 3`, `Community 7`, `Community 8`, `Community 10`, `Community 14`, `Community 18`, `Community 50`, `Community 52`, `Community 85`, `Community 54`, `Community 23`, `Community 25`, `Community 30`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `get_api_key_env()` connect `Community 21` to `Community 16`, `Community 54`, `Community 28`, `Community 62`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `TradingAgentsGraph` (e.g. with `MessageBuffer` and `Path`) actually correct?**
  _`TradingAgentsGraph` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TestTradingMemoryLogCore` (e.g. with `PortfolioDecision` and `PortfolioRating`) actually correct?**
  _`TestTradingMemoryLogCore` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `BaseLLMClient` (e.g. with `AnthropicClient` and `NormalizedChatAnthropic`) actually correct?**
  _`BaseLLMClient` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Console`, `Fetch announcements from endpoint. Returns dict with announcements and settings.`, `Display announcements panel. Prompts for Enter if require_attention is True.` to the rest of the system?**
  _650 weakly-connected nodes found - possible documentation gaps or missing edges._