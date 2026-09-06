"""Domain behavior for supported coffee drinks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Drink:
    """Deterministic information about a supported drink."""

    name: str
    caffeine_mg: int


class UnsupportedDrinkError(ValueError):
    """Raised when a drink is not supported."""


_DRINKS = {
    "espresso": Drink(name="Espresso", caffeine_mg=80),
    "americano": Drink(name="Americano", caffeine_mg=120),
    "cappuccino": Drink(name="Cappuccino", caffeine_mg=75),
}


def get_drink(name: str) -> Drink:
    """Return deterministic information for a supported drink."""
    try:
        return _DRINKS[name]
    except KeyError as error:
        raise UnsupportedDrinkError(f"Unsupported drink: {name}") from error
