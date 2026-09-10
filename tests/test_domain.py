"""Tests for deterministic drink information."""

from datetime import UTC, datetime, timedelta, timezone

import pytest

from cdd.domain import (
    CoffeeEvent,
    InvalidOccurrenceTimeError,
    UnsupportedDrinkError,
    calculate_stats,
    create_coffee_event,
    developer_state,
    get_drink,
    summarize_today,
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


def test_create_coffee_event_normalizes_aware_timestamp_to_utc() -> None:
    """Injected aware timestamps preserve the UTC storage invariant."""
    timestamp = datetime(
        2026,
        9,
        7,
        14,
        30,
        tzinfo=timezone(timedelta(hours=2)),
    )

    event = create_coffee_event(get_drink("espresso"), timestamp=timestamp)

    assert event.timestamp == datetime(2026, 9, 7, 12, 30, tzinfo=UTC)
    assert event.timestamp.tzinfo is UTC


def test_create_coffee_event_rejects_naive_timestamp() -> None:
    """A timestamp without timezone information cannot become a stored event."""
    timestamp = datetime(2026, 9, 7, 12, 30, tzinfo=UTC).replace(tzinfo=None)

    with pytest.raises(ValueError, match="timestamp must be timezone-aware"):
        create_coffee_event(get_drink("espresso"), timestamp=timestamp)


def test_create_historical_coffee_event_parses_and_normalizes_offset() -> None:
    event = create_coffee_event(
        get_drink("espresso"),
        timestamp="2026-09-05T14:30:00+02:00",
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
    )

    assert event.timestamp == datetime(2026, 9, 5, 12, 30, tzinfo=UTC)


@pytest.mark.parametrize(
    ("timestamp", "message"),
    [
        ("not-a-timestamp", "valid ISO 8601"),
        ("2026-09-05T14:30:00", "timezone-aware"),
        ("2026-09-08T12:00:00+00:00", "cannot be in the future"),
        ("0001-01-01T00:00:00+01:00", "cannot be represented in UTC"),
        ("9999-12-31T23:59:59-01:00", "cannot be represented in UTC"),
    ],
)
def test_create_historical_coffee_event_rejects_invalid_input(
    timestamp: str,
    message: str,
) -> None:
    with pytest.raises(InvalidOccurrenceTimeError, match=message):
        create_coffee_event(
            get_drink("espresso"),
            timestamp=timestamp,
            now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
        )


@pytest.mark.parametrize(
    ("caffeine_mg", "expected"),
    [
        (0, "NO SIGNAL"),
        (1, "BOOTING"),
        (100, "BOOTING"),
        (101, "PRODUCTIVE"),
        (250, "PRODUCTIVE"),
        (251, "TURBO MODE"),
        (399, "TURBO MODE"),
        (400, "ARCHITECTURE PRIVILEGES REVOKED"),
    ],
)
def test_developer_state_uses_exact_caffeine_boundaries(
    caffeine_mg: int,
    expected: str,
) -> None:
    assert developer_state(caffeine_mg) == expected


def test_summarize_today_uses_the_supplied_local_calendar_day() -> None:
    local_timezone = timezone(timedelta(hours=2))
    now = datetime(2026, 9, 7, 9, 0, tzinfo=local_timezone)
    events = [
        CoffeeEvent(datetime(2026, 9, 6, 21, 59, tzinfo=UTC), "espresso", 80),
        CoffeeEvent(datetime(2026, 9, 6, 22, 0, tzinfo=UTC), "americano", 120),
        CoffeeEvent(datetime(2026, 9, 7, 7, 0, tzinfo=UTC), "cappuccino", 75),
    ]

    summary = summarize_today(events, now=now)

    assert summary.coffees == 2
    assert summary.caffeine_mg == 195
    assert summary.developer_state == "PRODUCTIVE"


def test_summarize_today_has_explicit_empty_history_semantics() -> None:
    summary = summarize_today([], now=datetime(2026, 9, 7, tzinfo=UTC))

    assert summary.coffees == 0
    assert summary.caffeine_mg == 0
    assert summary.developer_state == "NO SIGNAL"


def test_summarize_today_uses_the_supplied_dst_aware_localizer() -> None:
    fixed_winter_offset = timezone(timedelta(hours=-5))
    now = datetime(2026, 7, 1, 12, 0, tzinfo=fixed_winter_offset)
    event = CoffeeEvent(
        datetime(2026, 7, 1, 4, 30, tzinfo=UTC),
        "espresso",
        80,
    )

    def summer_local_time(timestamp: datetime) -> datetime:
        return timestamp.astimezone(timezone(timedelta(hours=-4)))

    summary = summarize_today([event], now=now, to_local=summer_local_time)

    assert summary.coffees == 1
    assert summary.caffeine_mg == 80


def test_calculate_stats_includes_zero_days_and_excludes_older_events() -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=UTC)
    events = [
        CoffeeEvent(datetime(2026, 9, 4, 23, 59, tzinfo=UTC), "espresso", 80),
        CoffeeEvent(datetime(2026, 9, 5, 8, 0, tzinfo=UTC), "americano", 120),
        CoffeeEvent(datetime(2026, 9, 7, 8, 0, tzinfo=UTC), "espresso", 80),
    ]

    stats = calculate_stats(events, days=3, now=now)

    assert stats.total_coffees == 2
    assert stats.total_caffeine_mg == 200
    assert stats.average_caffeine_mg == pytest.approx(200 / 3)
    assert stats.favorite_drink == "americano"
    assert [(day.day.isoformat(), day.caffeine_mg) for day in stats.daily] == [
        ("2026-09-05", 120),
        ("2026-09-06", 0),
        ("2026-09-07", 80),
    ]


def test_calculate_stats_breaks_favorite_ties_alphabetically() -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=UTC)
    events = [
        CoffeeEvent(now, "espresso", 80),
        CoffeeEvent(now, "americano", 120),
    ]

    stats = calculate_stats(events, days=7, now=now)

    assert stats.favorite_drink == "americano"


def test_calculate_stats_has_explicit_no_data_semantics() -> None:
    stats = calculate_stats([], days=7, now=datetime(2026, 9, 7, tzinfo=UTC))

    assert stats.total_coffees == 0
    assert stats.total_caffeine_mg == 0
    assert stats.average_caffeine_mg == 0
    assert stats.favorite_drink is None
    assert len(stats.daily) == 7
