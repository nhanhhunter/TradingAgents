from contextlib import ExitStack
from unittest import mock

import pytest

from cli.models import AnalystType, AssetType

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def _clear_cli_selection_env(monkeypatch):
    for name in (
        "TRADINGAGENTS_OUTPUT_LANGUAGE",
        "TRADINGAGENTS_LLM_PROVIDER",
        "TRADINGAGENTS_LLM_BACKEND_URL",
        "TRADINGAGENTS_QUICK_THINK_LLM",
        "TRADINGAGENTS_DEEP_THINK_LLM",
    ):
        monkeypatch.delenv(name, raising=False)


class Answer:
    def __init__(self, value):
        self.value = value

    def ask(self):
        return self.value


@pytest.fixture
def cli_questionnaire():
    from cli import main

    def run(
        *,
        preferences=None,
        save_result=True,
        provider=("deepseek", "https://api.deepseek.com"),
        previous_provider_result=None,
        analysts=None,
        output_language="English",
        thinking_agents=("deepseek-chat", "deepseek-reasoner"),
    ):
        selected_analysts = (
            [AnalystType.MARKET, AnalystType.NEWS]
            if analysts is None
            else analysts
        )
        patches = {
            "load": mock.patch.object(
                main,
                "load_cli_preferences",
                return_value={} if preferences is None else preferences,
            ),
            "save": mock.patch.object(
                main,
                "save_cli_preferences",
                return_value=save_result,
            ),
            "fetch_announcements": mock.patch.object(
                main,
                "fetch_announcements",
                return_value=None,
            ),
            "display_announcements": mock.patch.object(
                main,
                "display_announcements",
            ),
            "get_ticker": mock.patch.object(
                main,
                "get_ticker",
                return_value="AAPL",
            ),
            "detect_asset_type": mock.patch.object(
                main,
                "detect_asset_type",
                return_value=AssetType.STOCK,
            ),
            "ensure_vnstock": mock.patch.object(
                main,
                "ensure_vnstock_api_key_for_symbol",
            ),
            "get_analysis_date": mock.patch.object(
                main,
                "get_analysis_date",
                return_value="2026-06-18",
            ),
            "ask_output_language": mock.patch.object(
                main,
                "ask_output_language",
                return_value=output_language,
            ),
            "select_analysts": mock.patch.object(
                main,
                "select_analysts",
                return_value=selected_analysts,
            ),
            "select_research_depth": mock.patch.object(
                main,
                "select_research_depth",
                return_value=2,
            ),
            "select_previous_provider": mock.patch.object(
                main,
                "select_previous_llm_provider",
                return_value=previous_provider_result,
            ),
            "select_provider": mock.patch.object(
                main,
                "select_llm_provider",
                return_value=provider,
            ),
            "select_thinking_agents": mock.patch.object(
                main,
                "select_thinking_agents",
                return_value=thinking_agents,
            ),
            "ask_qwen_region": mock.patch.object(
                main,
                "ask_qwen_region",
            ),
            "ask_gemini_thinking_config": mock.patch.object(
                main,
                "ask_gemini_thinking_config",
            ),
            "ask_openai_reasoning_effort": mock.patch.object(
                main,
                "ask_openai_reasoning_effort",
            ),
            "ask_anthropic_effort": mock.patch.object(
                main,
                "ask_anthropic_effort",
            ),
            "ensure_api_key": mock.patch.object(main, "ensure_api_key"),
        }
        with ExitStack() as stack:
            started = {
                name: stack.enter_context(patcher)
                for name, patcher in patches.items()
            }
            selections = main.get_user_selections()
        return selections, started

    return run


def test_first_run_orchestrates_preferences_and_saves_sparse_fields(
    cli_questionnaire,
):
    selections, calls = cli_questionnaire()

    calls["load"].assert_called_once_with()
    calls["ask_output_language"].assert_called_once_with(None)
    calls["select_analysts"].assert_called_once_with(
        AssetType.STOCK,
        default_analysts=None,
    )
    calls["select_previous_provider"].assert_called_once_with(None)
    calls["select_provider"].assert_called_once_with()
    calls["select_thinking_agents"].assert_called_once_with(
        "deepseek",
        previous_provider=None,
        previous_quick=None,
        previous_deep=None,
    )
    calls["save"].assert_called_once_with(
        {
            "analysts": ["market", "news"],
            "output_language": "English",
            "llm_provider": "deepseek",
            "thinking_provider": "deepseek",
            "quick_think_llm": "deepseek-chat",
            "deep_think_llm": "deepseek-reasoner",
        }
    )
    assert selections == {
        "ticker": "AAPL",
        "asset_type": "stock",
        "analysis_date": "2026-06-18",
        "analysts": [AnalystType.MARKET, AnalystType.NEWS],
        "research_depth": 2,
        "llm_provider": "deepseek",
        "backend_url": "https://api.deepseek.com",
        "shallow_thinker": "deepseek-chat",
        "deep_thinker": "deepseek-reasoner",
        "google_thinking_level": None,
        "openai_reasoning_effort": None,
        "anthropic_effort": None,
        "output_language": "English",
    }


def test_prior_regional_provider_reuse_skips_full_picker_and_region(
    cli_questionnaire,
):
    preferences = {
        "output_language": "Vietnamese",
        "analysts": ["social", "news"],
        "llm_provider": "qwen-cn",
        "thinking_provider": "qwen-cn",
        "quick_think_llm": "qwen-plus",
        "deep_think_llm": "qwen-max",
    }
    selections, calls = cli_questionnaire(
        preferences=preferences,
        previous_provider_result=(
            "qwen-cn",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        analysts=[AnalystType.SOCIAL, AnalystType.NEWS],
        output_language="Vietnamese",
        thinking_agents=("qwen-plus", "qwen-max"),
    )

    calls["ask_output_language"].assert_called_once_with("Vietnamese")
    calls["select_analysts"].assert_called_once_with(
        AssetType.STOCK,
        default_analysts=["social", "news"],
    )
    calls["select_previous_provider"].assert_called_once_with("qwen-cn")
    calls["select_provider"].assert_not_called()
    calls["ask_qwen_region"].assert_not_called()
    calls["select_thinking_agents"].assert_called_once_with(
        "qwen-cn",
        previous_provider="qwen-cn",
        previous_quick="qwen-plus",
        previous_deep="qwen-max",
    )
    calls["ensure_api_key"].assert_called_once_with("qwen-cn")
    assert selections["llm_provider"] == "qwen-cn"
    assert selections["backend_url"] == (
        "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )


def test_save_failure_warns_but_returns_current_selections(
    cli_questionnaire,
    capsys,
):
    selections, calls = cli_questionnaire(save_result=False)

    calls["save"].assert_called_once()
    assert selections["ticker"] == "AAPL"
    assert selections["llm_provider"] == "deepseek"
    assert "Warning: Could not save recent CLI selections." in capsys.readouterr().out


def test_env_provider_and_language_with_interactive_models_saves_pair_owner_only(
    cli_questionnaire,
    monkeypatch,
):
    from cli import main

    fake_config = dict(main.DEFAULT_CONFIG)
    fake_config.update(
        {
            "llm_provider": "openai",
            "backend_url": "https://api.openai.com/v1",
            "output_language": "Japanese",
        }
    )
    monkeypatch.setattr(main, "DEFAULT_CONFIG", fake_config)
    monkeypatch.setenv("TRADINGAGENTS_LLM_PROVIDER", "openai")
    monkeypatch.setenv("TRADINGAGENTS_OUTPUT_LANGUAGE", "Japanese")

    selections, calls = cli_questionnaire(
        preferences={
            "output_language": "Vietnamese",
            "llm_provider": "qwen-cn",
            "thinking_provider": "openai",
            "quick_think_llm": "gpt-5.4-mini",
            "deep_think_llm": "gpt-5.5",
        },
        thinking_agents=("gpt-5.4-mini", "gpt-5.5"),
    )

    calls["ask_output_language"].assert_not_called()
    calls["select_previous_provider"].assert_not_called()
    calls["select_provider"].assert_not_called()
    calls["select_thinking_agents"].assert_called_once_with(
        "openai",
        previous_provider="openai",
        previous_quick="gpt-5.4-mini",
        previous_deep="gpt-5.5",
    )
    calls["ask_openai_reasoning_effort"].assert_not_called()
    calls["save"].assert_called_once_with(
        {
            "analysts": ["market", "news"],
            "thinking_provider": "openai",
            "quick_think_llm": "gpt-5.4-mini",
            "deep_think_llm": "gpt-5.5",
        }
    )
    assert selections["output_language"] == "Japanese"
    assert selections["llm_provider"] == "openai"
    assert selections["shallow_thinker"] == "gpt-5.4-mini"
    assert selections["deep_thinker"] == "gpt-5.5"


def test_language_reuses_trimmed_previous_with_exact_choices():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select:
        assert utils.ask_output_language("  Vietnamese  ") == "Vietnamese"

    choices = select.call_args.kwargs["choices"]
    assert [(choice.title, choice.value) for choice in choices] == [
        ("Use previous: Vietnamese", "reuse"),
        ("Reselect", "reselect"),
    ]


def test_language_reselect_opens_existing_full_selector():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        side_effect=[Answer("reselect"), Answer("custom")],
    ) as select, mock.patch.object(
        utils.questionary,
        "text",
        return_value=Answer("  Vietnamese  "),
    ):
        assert utils.ask_output_language("Japanese") == "Vietnamese"

    assert select.call_count == 2


def test_language_cancel_opens_existing_full_selector():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        side_effect=[Answer(None), Answer("Korean")],
    ) as select:
        assert utils.ask_output_language("Japanese") == "Korean"

    assert select.call_count == 2


def test_analysts_checkbox_checks_only_valid_previous_wire_values():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "checkbox",
        return_value=Answer([AnalystType.MARKET, AnalystType.NEWS]),
    ) as checkbox:
        result = utils.select_analysts(
            AssetType.STOCK,
            default_analysts=["market", "news", "removed", "", None],
        )

    assert result == [AnalystType.MARKET, AnalystType.NEWS]
    choices = checkbox.call_args.kwargs["choices"]
    assert {
        choice.value
        for choice in choices
        if choice.checked
    } == {AnalystType.MARKET, AnalystType.NEWS}


def test_crypto_filters_fundamentals_from_choices_and_checked_defaults():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "checkbox",
        return_value=Answer([AnalystType.MARKET]),
    ) as checkbox:
        utils.select_analysts(
            AssetType.CRYPTO,
            default_analysts=["market", "fundamentals"],
        )

    choices = checkbox.call_args.kwargs["choices"]
    assert AnalystType.FUNDAMENTALS not in [choice.value for choice in choices]
    assert {
        choice.value
        for choice in choices
        if choice.checked
    } == {AnalystType.MARKET}


def test_previous_provider_reuses_current_display_and_endpoint():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select:
        assert utils.select_previous_llm_provider("MIMO") == (
            "mimo",
            "https://token-plan-sgp.xiaomimimo.com/v1",
        )

    choices = select.call_args.kwargs["choices"]
    assert [(choice.title, choice.value) for choice in choices] == [
        ("Use previous: Xiaomi Mimo", "reuse"),
        ("Reselect", "reselect"),
    ]


@pytest.mark.parametrize("previous", ["removed-provider", "", None, 123])
def test_unknown_or_non_string_previous_provider_skips_prompt(previous):
    from cli import utils

    with mock.patch.object(utils.questionary, "select") as select:
        assert utils.select_previous_llm_provider(previous) is None

    select.assert_not_called()


@pytest.mark.parametrize(
    ("provider", "endpoint"),
    [
        ("qwen", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        ("qwen-cn", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        ("glm", "https://api.z.ai/api/paas/v4/"),
        ("glm-cn", "https://open.bigmodel.cn/api/paas/v4/"),
        ("minimax", "https://api.minimax.io/v1"),
        ("minimax-cn", "https://api.minimaxi.com/v1"),
    ],
)
def test_regional_previous_provider_resolves_exact_current_endpoint(
    provider,
    endpoint,
):
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.select_previous_llm_provider(provider) == (provider, endpoint)


def test_previous_ollama_provider_uses_call_time_endpoint(monkeypatch):
    from cli import utils

    monkeypatch.setenv("OLLAMA_BASE_URL", "http://recent-ollama:11434/v1")
    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.select_previous_llm_provider("ollama") == (
            "ollama",
            "http://recent-ollama:11434/v1",
        )


def test_provider_reselect_returns_none_for_full_picker_fallback():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reselect"),
    ):
        assert utils.select_previous_llm_provider("mimo") is None


def test_thinking_agents_reuse_valid_catalog_pair_with_current_labels():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ) as select, mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
    ) as deep:
        result = utils.select_thinking_agents(
            "MIMO",
            previous_provider="mimo",
            previous_quick="  mimo-v2.5  ",
            previous_deep="  mimo-v2.5-pro  ",
        )

    assert result == ("mimo-v2.5", "mimo-v2.5-pro")
    choices = select.call_args.kwargs["choices"]
    assert choices[0].title == (
        "Use previous: Quick=Mimo v2.5; Deep=Mimo v2.5 Pro"
    )
    quick.assert_not_called()
    deep.assert_not_called()


def test_thinking_agents_provider_mismatch_opens_existing_selectors():
    from cli import utils

    with mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="deepseek-chat",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="deepseek-reasoner",
    ) as deep, mock.patch.object(utils.questionary, "select") as select:
        assert utils.select_thinking_agents(
            "deepseek",
            previous_provider="mimo",
            previous_quick="mimo-v2.5",
            previous_deep="mimo-v2.5-pro",
        ) == ("deepseek-chat", "deepseek-reasoner")

    select.assert_not_called()
    quick.assert_called_once_with("deepseek")
    deep.assert_called_once_with("deepseek")


def test_thinking_agents_reselect_opens_quick_then_deep_selectors():
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reselect"),
    ), mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="mimo-v2.5",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="mimo-v2.5-pro",
    ) as deep:
        assert utils.select_thinking_agents(
            "mimo",
            previous_provider="MIMO",
            previous_quick="mimo-v2.5",
            previous_deep="mimo-v2.5-pro",
        ) == ("mimo-v2.5", "mimo-v2.5-pro")

    quick.assert_called_once_with("mimo")
    deep.assert_called_once_with("mimo")


def test_thinking_agents_stale_mode_specific_catalog_pair_falls_back():
    from cli import utils

    with mock.patch.object(
        utils,
        "select_shallow_thinking_agent",
        return_value="gpt-5.4-mini",
    ) as quick, mock.patch.object(
        utils,
        "select_deep_thinking_agent",
        return_value="gpt-5.5",
    ) as deep, mock.patch.object(utils.questionary, "select") as select:
        assert utils.select_thinking_agents(
            "openai",
            previous_provider="openai",
            previous_quick="gpt-5.5-pro",
            previous_deep="gpt-5.5",
        ) == ("gpt-5.4-mini", "gpt-5.5")

    select.assert_not_called()
    quick.assert_called_once_with("openai")
    deep.assert_called_once_with("openai")


@pytest.mark.parametrize("provider", ["openrouter", "azure", "ollama"])
def test_thinking_agents_reuse_nonempty_custom_ids_for_supported_providers(
    provider,
):
    from cli import utils

    with mock.patch.object(
        utils.questionary,
        "select",
        return_value=Answer("reuse"),
    ):
        assert utils.select_thinking_agents(
            provider,
            previous_provider=provider.upper(),
            previous_quick="  custom-quick  ",
            previous_deep="  custom-deep  ",
        ) == ("custom-quick", "custom-deep")
