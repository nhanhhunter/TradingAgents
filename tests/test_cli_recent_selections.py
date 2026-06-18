from unittest import mock

import pytest

from cli.models import AnalystType, AssetType


pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def _clear_cli_selection_env(monkeypatch):
    for name in (
        "TRADINGAGENTS_OUTPUT_LANGUAGE",
        "TRADINGAGENTS_LLM_PROVIDER",
        "TRADINGAGENTS_QUICK_THINK_LLM",
        "TRADINGAGENTS_DEEP_THINK_LLM",
    ):
        monkeypatch.delenv(name, raising=False)


class Answer:
    def __init__(self, value):
        self.value = value

    def ask(self):
        return self.value


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
