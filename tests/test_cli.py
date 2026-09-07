"""Tests for the initial CLI boundary."""

import json
from datetime import datetime
from pathlib import Path

import pytest

from cdd.cli import main


@pytest.mark.parametrize(
    ("drink", "display_name", "caffeine_mg"),
    [
        ("espresso", "Espresso", 80),
        ("americano", "Americano", 120),
        ("cappuccino", "Cappuccino", 75),
    ],
)
def test_drink_displays_supported_drink_information(
    drink: str,
    display_name: str,
    caffeine_mg: int,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """The drink command renders and persists deterministic drink information."""
    history_path = tmp_path / "history.jsonl"

    assert main(["drink", drink], history_path=history_path) == 0
    assert capsys.readouterr().out == (
        f"{display_name}\nEstimated caffeine: {caffeine_mg} mg\n"
    )
    records = [json.loads(line) for line in history_path.read_text().splitlines()]
    assert len(records) == 1
    assert records[0]["drink"] == drink
    assert records[0]["caffeine_mg"] == caffeine_mg
    assert datetime.fromisoformat(records[0]["timestamp"]).tzinfo is not None


def test_drink_rejects_unsupported_drink(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """The drink command exits unsuccessfully for an unknown drink."""
    history_path = tmp_path / "history.jsonl"

    with pytest.raises(SystemExit) as result:
        main(["drink", "latte"], history_path=history_path)

    assert result.value.code != 0
    assert "Unsupported drink: latte" in capsys.readouterr().err
    assert not history_path.exists()


def test_drink_reports_persistence_failure_without_traceback(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Filesystem failures remain a clean CLI error at the presentation boundary."""
    def fail_to_append(*args: object) -> None:
        raise OSError("read-only filesystem")

    monkeypatch.setattr("cdd.cli.append_event", fail_to_append)

    with pytest.raises(SystemExit) as result:
        main(["drink", "espresso"], history_path=tmp_path / "history.jsonl")

    assert result.value.code != 0
    assert "Could not persist coffee event" in capsys.readouterr().err


def test_help_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI exposes its initial help screen."""
    with pytest.raises(SystemExit) as result:
        main(["--help"])

    assert result.value.code == 0
    assert "Coffee-Driven Development" in capsys.readouterr().out
