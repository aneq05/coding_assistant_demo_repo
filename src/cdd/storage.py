"""Local JSON Lines persistence for coffee events."""

import json
from pathlib import Path

from cdd.domain import CoffeeEvent


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
