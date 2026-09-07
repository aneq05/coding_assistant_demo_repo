"""Domain behavior for supported coffee drinks."""

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Drink:
    """Deterministic information about a supported drink."""

    kind: str
    name: str
    caffeine_mg: int


@dataclass(frozen=True)
class CoffeeEvent:
    """A supported coffee drink recorded at a specific time."""

    timestamp: datetime
    drink: str
    caffeine_mg: int


class UnsupportedDrinkError(ValueError):
    """Raised when a drink is not supported."""


_DRINKS = {
    "espresso": Drink(kind="espresso", name="Espresso", caffeine_mg=80),
    "americano": Drink(kind="americano", name="Americano", caffeine_mg=120),
    "cappuccino": Drink(kind="cappuccino", name="Cappuccino", caffeine_mg=75),
}


def get_drink(name: str) -> Drink:
    """Return deterministic information for a supported drink."""
    try:
        return _DRINKS[name]
    except KeyError as error:
        raise UnsupportedDrinkError(f"Unsupported drink: {name}") from error


def create_coffee_event(
    drink: Drink,
    *,
    timestamp: datetime | None = None,
) -> CoffeeEvent:
    """Create a coffee event for a supported drink."""
    return CoffeeEvent(
        timestamp=timestamp or datetime.now(UTC),
        drink=drink.kind,
        caffeine_mg=drink.caffeine_mg,
    )
