from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from tradingagents.env_config import (
    load_tradingagents_env,
    persist_env_value,
    resolve_env_file,
)


def _make_source_checkout(path: Path) -> None:
    (path / "pyproject.toml").write_text(
        '[project]\nname = "tradingagents"\n',
        encoding="utf-8",
    )
    (path / "tradingagents").mkdir()
    (path / "cli").mkdir()


def test_source_checkout_ignores_ancestor_env(tmp_path):
    ancestor_env = tmp_path / ".env"
    ancestor_env.write_text("DEEPSEEK_API_KEY=ancestor\n", encoding="utf-8")
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    _make_source_checkout(checkout)

    resolved = resolve_env_file(cwd=checkout, home=tmp_path / "home", environ={})

    assert resolved == checkout / ".env"
    assert resolved != ancestor_env


def test_existing_current_directory_env_wins_outside_source_checkout(tmp_path):
    working_dir = tmp_path / "analysis"
    working_dir.mkdir()
    local_env = working_dir / ".env"
    local_env.write_text("OPENAI_API_KEY=local\n", encoding="utf-8")

    resolved = resolve_env_file(
        cwd=working_dir,
        home=tmp_path / "home",
        environ={},
    )

    assert resolved == local_env


def test_installed_command_uses_per_user_config_when_cwd_has_no_env(tmp_path):
    working_dir = tmp_path / "analysis"
    working_dir.mkdir()
    home = tmp_path / "home"

    resolved = resolve_env_file(cwd=working_dir, home=home, environ={})

    assert resolved == home / ".tradingagents" / ".env"


def test_explicit_env_file_override_supports_relative_paths(tmp_path):
    working_dir = tmp_path / "analysis"
    working_dir.mkdir()

    resolved = resolve_env_file(
        cwd=working_dir,
        home=tmp_path / "home",
        environ={"TRADINGAGENTS_ENV_FILE": "config/keys.env"},
    )

    assert resolved == working_dir / "config" / "keys.env"


def test_loader_fills_blank_environment_values_from_persisted_file(
    monkeypatch, tmp_path
):
    env_file = tmp_path / "keys.env"
    env_file.write_text(
        "OPENAI_API_KEY=persisted\nDEEPSEEK_API_KEY=stored-deepseek\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TRADINGAGENTS_ENV_FILE", str(env_file))
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "process-wins")

    load_tradingagents_env()

    assert os.environ["OPENAI_API_KEY"] == "persisted"
    assert os.environ["DEEPSEEK_API_KEY"] == "process-wins"


def test_persist_round_trip_uses_resolved_file(monkeypatch, tmp_path):
    env_file = tmp_path / "nested" / "keys.env"
    monkeypatch.setenv("TRADINGAGENTS_ENV_FILE", str(env_file))
    monkeypatch.delenv("MIMO_API_KEY", raising=False)

    resolved = persist_env_value("MIMO_API_KEY", "placeholder-secret")
    monkeypatch.setenv("MIMO_API_KEY", "")
    load_tradingagents_env()

    assert resolved == env_file
    assert os.environ["MIMO_API_KEY"] == "placeholder-secret"
    assert "MIMO_API_KEY='placeholder-secret'" in env_file.read_text(encoding="utf-8")


def test_fresh_process_loads_persisted_value_when_inherited_value_is_blank(tmp_path):
    env_file = tmp_path / "keys.env"
    env_file.write_text("MIMO_API_KEY=fresh-process-value\n", encoding="utf-8")
    child_env = os.environ.copy()
    child_env["TRADINGAGENTS_ENV_FILE"] = str(env_file)
    child_env["MIMO_API_KEY"] = ""

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import os; import tradingagents; "
                "assert os.environ['MIMO_API_KEY'] == 'fresh-process-value'"
            ),
        ],
        cwd=tmp_path,
        env=child_env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(os.name == "nt", reason="POSIX mode bits are not Windows ACLs")
def test_new_credential_file_requests_owner_only_permissions(monkeypatch, tmp_path):
    env_file = tmp_path / "keys.env"
    monkeypatch.setenv("TRADINGAGENTS_ENV_FILE", str(env_file))

    persist_env_value("OPENROUTER_API_KEY", "placeholder-secret")

    assert stat.S_IMODE(env_file.stat().st_mode) == 0o600


def test_docker_runtime_uses_named_volume_backed_env_file():
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")
    compose = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert (
        "TRADINGAGENTS_ENV_FILE=/home/appuser/.tradingagents/.env"
        in dockerfile
    )
    assert (
        compose.count(
            "tradingagents_data:/home/appuser/.tradingagents"
        )
        == 2
    )
