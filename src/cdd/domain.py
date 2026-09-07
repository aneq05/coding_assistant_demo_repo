"""Domain behavior for supported coffee drinks."""

from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, tzinfo

LocalTimeConverter = Callable[[datetime], datetime]


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


@dataclass(frozen=True)
class TodaySummary:
    """Coffee activity for one local calendar day."""

    coffees: int
    caffeine_mg: int
    developer_state: str


@dataclass(frozen=True)
class DailyCaffeine:
    """Caffeine consumed on one local calendar day."""

    day: date
    caffeine_mg: int


@dataclass(frozen=True)
class CoffeeStats:
    """Coffee statistics over a fixed local-calendar window."""

    days: int
    total_coffees: int
    total_caffeine_mg: int
    average_caffeine_mg: float
    favorite_drink: str | None
    daily: tuple[DailyCaffeine, ...]


class UnsupportedDrinkError(ValueError):
    """Raised when a drink is not supported."""


class InvalidStatsPeriodError(ValueError):
    """Raised when a statistics window cannot be represented."""


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
    event_timestamp = timestamp or datetime.now(UTC)
    if event_timestamp.tzinfo is None or event_timestamp.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")

    return CoffeeEvent(
        timestamp=event_timestamp.astimezone(UTC),
        drink=drink.kind,
        caffeine_mg=drink.caffeine_mg,
    )


def developer_state(caffeine_mg: int) -> str:
    """Return the developer state for a caffeine amount."""
    if caffeine_mg < 0:
        raise ValueError("caffeine_mg cannot be negative")
    if caffeine_mg == 0:
        return "NO SIGNAL"
    if caffeine_mg <= 100:
        return "BOOTING"
    if caffeine_mg <= 250:
        return "PRODUCTIVE"
    if caffeine_mg <= 399:
        return "TURBO MODE"
    return "ARCHITECTURE PRIVILEGES REVOKED"


def summarize_today(
    events: Sequence[CoffeeEvent],
    *,
    now: datetime,
    to_local: LocalTimeConverter | None = None,
) -> TodaySummary:
    """Summarize events occurring on the supplied local date."""
    local_timezone = _timezone_from(now)
    today = _localize(now, to_local, local_timezone).date()
    today_events = [
        event
        for event in events
        if _localize(event.timestamp, to_local, local_timezone).date() == today
    ]
    caffeine_mg = sum(event.caffeine_mg for event in today_events)
    return TodaySummary(
        coffees=len(today_events),
        caffeine_mg=caffeine_mg,
        developer_state=developer_state(caffeine_mg),
    )


def calculate_stats(
    events: Sequence[CoffeeEvent],
    *,
    days: int,
    now: datetime,
    to_local: LocalTimeConverter | None = None,
) -> CoffeeStats:
    """Calculate coffee statistics for recent local calendar days."""
    if days <= 0:
        raise ValueError("days must be positive")

    local_timezone = _timezone_from(now)
    local_now = _localize(now, to_local, local_timezone)
    if days > local_now.date().toordinal():
        raise InvalidStatsPeriodError("days extend before the minimum date")
    first_day = local_now.date() - timedelta(days=days - 1)
    daily_totals = {first_day + timedelta(days=offset): 0 for offset in range(days)}
    included_events: list[CoffeeEvent] = []

    for event in events:
        event_day = _localize(event.timestamp, to_local, local_timezone).date()
        if event_day in daily_totals:
            daily_totals[event_day] += event.caffeine_mg
            included_events.append(event)

    total_caffeine_mg = sum(daily_totals.values())
    drink_counts = Counter(event.drink for event in included_events)
    favorite_drink = None
    if drink_counts:
        highest_count = max(drink_counts.values())
        favorite_drink = min(
            drink for drink, count in drink_counts.items() if count == highest_count
        )

    return CoffeeStats(
        days=days,
        total_coffees=len(included_events),
        total_caffeine_mg=total_caffeine_mg,
        average_caffeine_mg=total_caffeine_mg / days,
        favorite_drink=favorite_drink,
        daily=tuple(
            DailyCaffeine(day=day, caffeine_mg=caffeine_mg)
            for day, caffeine_mg in daily_totals.items()
        ),
    )


def _timezone_from(timestamp: datetime) -> tzinfo:
    """Return timezone information after enforcing an aware timestamp."""
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    return timestamp.tzinfo


def _localize(
    timestamp: datetime,
    to_local: LocalTimeConverter | None,
    fallback_timezone: tzinfo,
) -> datetime:
    localized = (
        to_local(timestamp)
        if to_local is not None
        else timestamp.astimezone(fallback_timezone)
    )
    _timezone_from(localized)
    return localized
