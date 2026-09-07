"""Tests for local JSON Lines coffee-event persistence."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from cdd.domain import CoffeeEvent
from cdd.storage import append_event


def make_event(drink: str = "espresso", caffeine_mg: int = 80) -> CoffeeEvent:
    """Create a deterministic event for storage tests."""
    return CoffeeEvent(
        timestamp=datetime(2026, 9, 7, 12, 30, tzinfo=UTC),
        drink=drink,
        caffeine_mg=caffeine_mg,
    )


def test_append_event_writes_one_valid_json_line(tmp_path: Path) -> None:
    """A stored event has the complete JSONL schema and an aware timestamp."""
    history_path = tmp_path / "history.jsonl"

    append_event(make_event(), history_path)

    lines = history_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record == {
        "timestamp": "2026-09-07T12:30:00+00:00",
        "drink": "espresso",
        "caffeine_mg": 80,
    }
    assert datetime.fromisoformat(record["timestamp"]).tzinfo is not None


def test_append_event_preserves_existing_events(tmp_path: Path) -> None:
    """Each new event is appended as an independently parseable JSON line."""
    history_path = tmp_path / "history.jsonl"

    append_event(make_event(), history_path)
    append_event(make_event("americano", 120), history_path)

    records = [json.loads(line) for line in history_path.read_text().splitlines()]
    assert [record["drink"] for record in records] == ["espresso", "americano"]


def test_append_event_creates_parent_directory(tmp_path: Path) -> None:
    """The default-style parent directory need not already exist."""
    history_path = tmp_path / ".cdd" / "history.jsonl"

    append_event(make_event(), history_path)

    assert history_path.is_file()


def test_append_event_uses_default_history_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The production default is the history file beneath the user's home."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    append_event(make_event())

    assert (tmp_path / ".cdd" / "history.jsonl").is_file()
