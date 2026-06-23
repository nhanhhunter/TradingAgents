import json

import pytest

import cli.preferences as preferences
from cli.preferences import (
    PREFERENCES_PATH,
    load_cli_preferences,
    save_cli_preferences,
)

pytestmark = pytest.mark.unit


def test_default_preference_path_is_user_local():
    assert (
        preferences.Path.home()
        / ".tradingagents"
        / "cli_preferences.json"
    ) == PREFERENCES_PATH


def test_missing_preference_file_returns_empty_dict(tmp_path):
    assert load_cli_preferences(tmp_path / "missing.json") == {}


def test_valid_preferences_load_supported_fields_only(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": " Vietnamese ",
                "analysts": [
                    "market",
                    "social",
                    "market",
                    "unknown",
                    123,
                    "",
                ],
                "llm_provider": " mimo ",
                "thinking_provider": "mimo",
                "quick_think_llm": " mimo-v2.5 ",
                "deep_think_llm": "mimo-v2.5-pro",
                "api_key": "must-not-load",
                "backend_url": "https://secret.invalid",
                "ticker": "AAPL",
            }
        ),
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {
        "version": 1,
        "output_language": "Vietnamese",
        "analysts": ["market", "social"],
        "llm_provider": "mimo",
        "thinking_provider": "mimo",
        "quick_think_llm": "mimo-v2.5",
        "deep_think_llm": "mimo-v2.5-pro",
    }


@pytest.mark.parametrize(
    "payload",
    [
        "{not-json",
        json.dumps([]),
        json.dumps({"version": True, "output_language": "Vietnamese"}),
        json.dumps({"version": 2, "output_language": "Vietnamese"}),
    ],
)
def test_invalid_document_fails_open(tmp_path, payload):
    path = tmp_path / "preferences.json"
    path.write_text(payload, encoding="utf-8")

    assert load_cli_preferences(path) == {}


def test_oversized_integer_json_fails_open(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        '{"version": 1, "x": ' + ("9" * 5000) + "}",
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {}


def test_excessively_nested_json_fails_open(tmp_path):
    path = tmp_path / "preferences.json"
    depth = 10000
    path.write_text(
        '{"version": 1, "x": '
        + ("[" * depth)
        + "0"
        + ("]" * depth)
        + "}",
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {}


def test_unreadable_preference_path_fails_open(tmp_path):
    path = tmp_path / "preferences.json"
    path.mkdir()

    assert load_cli_preferences(path) == {}


def test_invalid_utf8_fails_open(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_bytes(b"\xff")

    assert load_cli_preferences(path) == {}


def test_wrong_field_types_are_discarded_independently(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": 123,
                "analysts": "market",
                "llm_provider": "mimo",
                "thinking_provider": None,
                "quick_think_llm": "",
                "deep_think_llm": "mimo-v2.5-pro",
            }
        ),
        encoding="utf-8",
    )

    assert load_cli_preferences(path) == {
        "version": 1,
        "llm_provider": "mimo",
        "deep_think_llm": "mimo-v2.5-pro",
    }


def test_save_creates_nested_directory_and_exact_non_secret_document(tmp_path):
    path = tmp_path / "nested" / "preferences.json"

    assert save_cli_preferences(
        {
            "output_language": " Vietnamese ",
            "analysts": [
                "market",
                "social",
                "market",
                "invalid",
            ],
            "llm_provider": " mimo ",
            "thinking_provider": "mimo",
            "quick_think_llm": "mimo-v2.5",
            "deep_think_llm": "mimo-v2.5-pro",
            "backend_url": "https://secret.invalid",
            "ticker": "AAPL",
            "api_key": "must-not-save",
        },
        path,
    )

    expected = {
        "version": 1,
        "output_language": "Vietnamese",
        "llm_provider": "mimo",
        "thinking_provider": "mimo",
        "quick_think_llm": "mimo-v2.5",
        "deep_think_llm": "mimo-v2.5-pro",
        "analysts": ["market", "social"],
    }
    assert path.read_text(encoding="utf-8") == (
        json.dumps(expected, indent=2) + "\n"
    )


def test_save_merge_preserves_supported_fields_omitted_from_update(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "output_language": "English",
                "analysts": ["market", "news"],
                "llm_provider": "openai",
                "thinking_provider": "openai",
                "quick_think_llm": "gpt-5-mini",
                "deep_think_llm": "gpt-5",
                "api_key": "old-secret",
            }
        ),
        encoding="utf-8",
    )

    assert save_cli_preferences(
        {
            "output_language": "Vietnamese",
            "backend_url": "https://secret.invalid",
        },
        path,
    )

    assert load_cli_preferences(path) == {
        "version": 1,
        "output_language": "Vietnamese",
        "analysts": ["market", "news"],
        "llm_provider": "openai",
        "thinking_provider": "openai",
        "quick_think_llm": "gpt-5-mini",
        "deep_think_llm": "gpt-5",
    }
    assert "old-secret" not in path.read_text(encoding="utf-8")
    assert "backend_url" not in path.read_text(encoding="utf-8")


def test_save_replaces_once_from_temporary_file_in_destination_directory(
    tmp_path, monkeypatch
):
    path = tmp_path / "nested" / "preferences.json"
    calls = []
    real_replace = preferences.os.replace

    def spy_replace(source, destination):
        calls.append((source, destination))
        real_replace(source, destination)

    monkeypatch.setattr(preferences.os, "replace", spy_replace)

    assert save_cli_preferences({"output_language": "English"}, path)

    assert len(calls) == 1
    source, destination = (preferences.Path(value) for value in calls[0])
    assert source.parent == path.parent
    assert destination == path


def test_replace_failure_returns_false_and_removes_temporary_file(
    tmp_path, monkeypatch
):
    path = tmp_path / "nested" / "preferences.json"

    def fail_replace(source, destination):
        raise OSError("replace failed")

    monkeypatch.setattr(preferences.os, "replace", fail_replace)

    assert not save_cli_preferences({"output_language": "English"}, path)
    assert not path.exists()
    assert path.parent.is_dir()
    assert list(path.parent.iterdir()) == []
