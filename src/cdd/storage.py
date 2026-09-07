"""Local JSON Lines persistence for coffee events."""

import json
from datetime import UTC, datetime
from pathlib import Path

from cdd.domain import CoffeeEvent


class InvalidHistoryError(ValueError):
    """Raised when a persisted history line does not match the event schema."""


def default_history_path() -> Path:
    """Return the default per-user coffee history path."""
    return Path.home() / ".cdd" / "history.jsonl"


def append_event(event: CoffeeEvent, path: Path | None = None) -> None:
    """Append one coffee event as an independently parseable JSON line."""
    history_path = path or default_history_path()
    history_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": event.timestamp.isoformat(),
        "drink": event.drink,
        "caffeine_mg": event.caffeine_mg,
    }
    with history_path.open("a", encoding="utf-8") as history_file:
        json.dump(record, history_file, separators=(",", ":"))
        history_file.write("\n")


def read_events(path: Path | None = None) -> list[CoffeeEvent]:
    """Read valid nonempty JSONL records in persisted order."""
    history_path = path or default_history_path()
    if not history_path.exists():
        return []

    events: list[CoffeeEvent] = []
    try:
        with history_path.open("r", encoding="utf-8") as history_file:
            for line_number, line in enumerate(history_file, start=1):
                if not line.strip():
                    continue
                try:
                    events.append(_parse_event(line))
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
                    raise InvalidHistoryError(
                        f"Invalid coffee history at line {line_number}"
                    ) from error
    except UnicodeError as error:
        raise InvalidHistoryError("Invalid coffee history encoding") from error
    return events


def _parse_event(line: str) -> CoffeeEvent:
    record = json.loads(line)
    if not isinstance(record, dict):
        raise TypeError("history record must be an object")

    timestamp_value = record["timestamp"]
    drink = record["drink"]
    caffeine_mg = record["caffeine_mg"]
    if not isinstance(timestamp_value, str):
        raise TypeError("timestamp must be a string")
    if not isinstance(drink, str) or not drink:
        raise TypeError("drink must be a nonempty string")
    if isinstance(caffeine_mg, bool) or not isinstance(caffeine_mg, int):
        raise TypeError("caffeine_mg must be an integer")
    if caffeine_mg < 0:
        raise ValueError("caffeine_mg cannot be negative")

    timestamp = datetime.fromisoformat(timestamp_value)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return CoffeeEvent(
        timestamp=timestamp.astimezone(UTC),
        drink=drink,
        caffeine_mg=caffeine_mg,
    )
