from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from contextlib import suppress
from pathlib import Path
from typing import Any

PREFERENCES_VERSION = 1
PREFERENCES_PATH = (
    Path.home() / ".tradingagents" / "cli_preferences.json"
)

_STRING_FIELDS = (
    "output_language",
    "llm_provider",
    "thinking_provider",
    "quick_think_llm",
    "deep_think_llm",
)
_ANALYST_VALUES = frozenset(
    {"market", "social", "news", "fundamentals"}
)


def _sanitize_preferences(payload: Any) -> dict[str, Any]:
    if (
        not isinstance(payload, dict)
        or type(payload.get("version")) is not int
        or payload.get("version") != PREFERENCES_VERSION
    ):
        return {}

    sanitized: dict[str, Any] = {"version": PREFERENCES_VERSION}

    for field in _STRING_FIELDS:
        value = payload.get(field)
        if isinstance(value, str):
            value = value.strip()
            if value:
                sanitized[field] = value

    analysts = payload.get("analysts")
    if isinstance(analysts, list):
        valid_analysts = []
        for analyst in analysts:
            if (
                isinstance(analyst, str)
                and analyst in _ANALYST_VALUES
                and analyst not in valid_analysts
            ):
                valid_analysts.append(analyst)
        if valid_analysts:
            sanitized["analysts"] = valid_analysts

    return sanitized


def load_cli_preferences(
    path: Path = PREFERENCES_PATH,
) -> dict[str, Any]:
    path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, RecursionError):
        return {}

    return _sanitize_preferences(payload)


def save_cli_preferences(
    updates: Mapping[str, Any],
    path: Path = PREFERENCES_PATH,
) -> bool:
    path = Path(path)
    temporary_path: Path | None = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        merged = load_cli_preferences(path)
        merged.update(updates)
        merged["version"] = PREFERENCES_VERSION
        sanitized = _sanitize_preferences(merged)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(
                sanitized,
                temporary_file,
                ensure_ascii=False,
                indent=2,
            )
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)
        temporary_path = None
        return True
    except OSError:
        if temporary_path is not None:
            with suppress(OSError):
                temporary_path.unlink(missing_ok=True)
        return False
