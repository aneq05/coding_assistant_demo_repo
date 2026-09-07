"""Tests for deterministic drink information."""

from datetime import UTC, datetime

import pytest

from cdd.domain import (
    CoffeeEvent,
    UnsupportedDrinkError,
    create_coffee_event,
    get_drink,
)


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

    assert drink.kind == name
    assert drink.name == display_name
    assert drink.caffeine_mg == caffeine_mg


def test_get_drink_rejects_unsupported_drink() -> None:
    """Unknown drinks are rejected instead of being substituted."""
    with pytest.raises(UnsupportedDrinkError, match="Unsupported drink: latte"):
        get_drink("latte")


def test_create_coffee_event_captures_required_drink_data() -> None:
    """A coffee event contains its UTC time, drink type, and caffeine amount."""
    timestamp = datetime(2026, 9, 7, 12, 30, tzinfo=UTC)

    event = create_coffee_event(get_drink("espresso"), timestamp=timestamp)

    assert event == CoffeeEvent(
        timestamp=timestamp,
        drink="espresso",
        caffeine_mg=80,
    )
