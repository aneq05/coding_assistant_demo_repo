"""Tests for the initial CLI boundary."""

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
) -> None:
    """The drink command renders deterministic caffeine information."""
    assert main(["drink", drink]) == 0
    assert capsys.readouterr().out == (
        f"{display_name}\nEstimated caffeine: {caffeine_mg} mg\n"
    )


def test_drink_rejects_unsupported_drink(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The drink command exits unsuccessfully for an unknown drink."""
    with pytest.raises(SystemExit) as result:
        main(["drink", "latte"])

    assert result.value.code != 0
    assert "Unsupported drink: latte" in capsys.readouterr().err


def test_help_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI exposes its initial help screen."""
    with pytest.raises(SystemExit) as result:
        main(["--help"])

    assert result.value.code == 0
    assert "Coffee-Driven Development" in capsys.readouterr().out
