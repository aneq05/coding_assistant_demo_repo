"""Tests for local JSON Lines coffee-event persistence."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from cdd import storage
from cdd.domain import CoffeeEvent
from cdd.storage import InvalidHistoryError, append_event, read_events


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
    monkeypatch.setattr(storage, "_REPOSITORY_ROOT", tmp_path)

    append_event(make_event())

    assert (tmp_path / ".cdd" / "history.jsonl").is_file()


def test_read_events_returns_empty_for_missing_history(tmp_path: Path) -> None:
    assert read_events(tmp_path / "missing.jsonl") == []


def test_read_events_parses_nonempty_lines_in_persisted_order(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"
    history_path.write_text(
        "\n"
        '{"timestamp":"2026-09-07T14:30:00+02:00","drink":"espresso",'
        '"caffeine_mg":80}\n'
        "   \n"
        '{"timestamp":"2026-09-07T13:00:00+00:00","drink":"americano",'
        '"caffeine_mg":120}\n',
        encoding="utf-8",
    )

    events = read_events(history_path)

    assert events == [
        CoffeeEvent(datetime(2026, 9, 7, 12, 30, tzinfo=UTC), "espresso", 80),
        CoffeeEvent(datetime(2026, 9, 7, 13, 0, tzinfo=UTC), "americano", 120),
    ]


@pytest.mark.parametrize(
    "line",
    [
        "not json",
        '{}',
        '{"timestamp":"not-a-time","drink":"espresso","caffeine_mg":80}',
        (
            '{"timestamp":"2026-09-07T12:30:00","drink":"espresso",'
            '"caffeine_mg":80}'
        ),
        (
            '{"timestamp":"2026-09-07T12:30:00+00:00","drink":7,'
            '"caffeine_mg":80}'
        ),
        (
            '{"timestamp":"2026-09-07T12:30:00+00:00","drink":"espresso",'
            '"caffeine_mg":true}'
        ),
    ],
)
def test_read_events_rejects_malformed_nonempty_lines(
    line: str,
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    history_path.write_text(f"\n{line}\n", encoding="utf-8")

    with pytest.raises(InvalidHistoryError, match="line 2"):
        read_events(history_path)
