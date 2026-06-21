"""Deterministic loading and persistence for TradingAgents environment files."""

from __future__ import annotations

import os
from collections.abc import Mapping, MutableMapping
from pathlib import Path

from dotenv import dotenv_values, set_key


ENV_FILE_OVERRIDE = "TRADINGAGENTS_ENV_FILE"


def _is_source_checkout(path: Path) -> bool:
    """Return whether ``path`` looks like the TradingAgents repository root."""
    return (
        (path / "pyproject.toml").is_file()
        and (path / "tradingagents").is_dir()
        and (path / "cli").is_dir()
    )


def _absolute_path(path: Path, *, cwd: Path) -> Path:
    path = path.expanduser()
    if not path.is_absolute():
        path = cwd / path
    return path.resolve()


def resolve_env_file(
    *,
    cwd: Path | None = None,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Select the primary dotenv file without searching parent directories."""
    cwd = (cwd or Path.cwd()).resolve()
    home = (home or Path.home()).expanduser().resolve()
    environ = os.environ if environ is None else environ

    explicit = environ.get(ENV_FILE_OVERRIDE, "").strip()
    if explicit:
        return _absolute_path(Path(explicit), cwd=cwd)

    local_env = cwd / ".env"
    if local_env.is_file() or _is_source_checkout(cwd):
        return local_env

    return home / ".tradingagents" / ".env"


def _load_file(path: Path, environ: MutableMapping[str, str]) -> None:
    if not path.is_file():
        return

    for name, value in dotenv_values(path).items():
        if value is not None and not environ.get(name):
            environ[name] = value


def load_tradingagents_env(
    *,
    cwd: Path | None = None,
    home: Path | None = None,
    environ: MutableMapping[str, str] | None = None,
) -> None:
    """Load TradingAgents dotenv files while preserving non-empty env values."""
    cwd = (cwd or Path.cwd()).resolve()
    home = (home or Path.home()).expanduser().resolve()
    environ = os.environ if environ is None else environ

    primary = resolve_env_file(cwd=cwd, home=home, environ=environ)
    candidates = [primary]

    enterprise = cwd / ".env.enterprise"
    if enterprise != primary:
        candidates.append(enterprise)

    if not environ.get(ENV_FILE_OVERRIDE):
        user_env = home / ".tradingagents" / ".env"
        if user_env not in candidates:
            candidates.append(user_env)

    for path in candidates:
        _load_file(path, environ)


def persist_env_value(
    name: str,
    value: str,
    *,
    cwd: Path | None = None,
    home: Path | None = None,
    environ: MutableMapping[str, str] | None = None,
) -> Path:
    """Persist one value to the resolved dotenv file and current environment."""
    environ = os.environ if environ is None else environ
    env_path = resolve_env_file(cwd=cwd, home=home, environ=environ)
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.touch(mode=0o600, exist_ok=True)
    set_key(str(env_path), name, value)

    try:
        env_path.chmod(0o600)
    except OSError:
        # Windows ACLs and some mounted filesystems do not expose POSIX modes.
        pass

    environ[name] = value
    return env_path
