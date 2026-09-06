"""Tests for deterministic drink information."""

import pytest

from cdd.domain import UnsupportedDrinkError, get_drink


@pytest.mark.parametrize(
    ("name", "display_name", "caffeine_mg"),
    [
        ("espresso", "Espresso", 80),
        ("americano", "Americano", 120),
        ("cappuccino", "Cappuccino", 75),
    ],
)
def test_get_drink_returns_supported_drink_information(
    name: str,
    display_name: str,
    caffeine_mg: int,
) -> None:
    """Supported drinks have stable display names and caffeine amounts."""
    drink = get_drink(name)

    assert drink.name == display_name
    assert drink.caffeine_mg == caffeine_mg


def test_get_drink_rejects_unsupported_drink() -> None:
    """Unknown drinks are rejected instead of being substituted."""
    with pytest.raises(UnsupportedDrinkError, match="Unsupported drink: latte"):
        get_drink("latte")
