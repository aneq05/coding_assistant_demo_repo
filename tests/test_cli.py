"""Tests for the initial CLI boundary."""

import json
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from cdd.cli import main
from cdd.domain import CoffeeEvent
from cdd.storage import append_event, read_events


@pytest.mark.parametrize(
    ("drink", "display_name", "caffeine_mg"),
    [
        ("espresso", "Espresso", 80),
        ("americano", "Americano", 120),
        ("cappuccino", "Cappuccino", 75),
    ],
)
def test_drink_displays_supported_drink_information(
    drink: str,
    display_name: str,
    caffeine_mg: int,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """The drink command renders and persists deterministic drink information."""
    history_path = tmp_path / "history.jsonl"

    assert main(["drink", drink], history_path=history_path) == 0
    assert capsys.readouterr().out == (
        f"{display_name}\nEstimated caffeine: {caffeine_mg} mg\n"
    )
    records = [json.loads(line) for line in history_path.read_text().splitlines()]
    assert len(records) == 1
    assert records[0]["drink"] == drink
    assert records[0]["caffeine_mg"] == caffeine_mg
    assert datetime.fromisoformat(records[0]["timestamp"]).tzinfo is not None


def test_drink_rejects_unsupported_drink(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """The drink command exits unsuccessfully for an unknown drink."""
    history_path = tmp_path / "history.jsonl"

    with pytest.raises(SystemExit) as result:
        main(["drink", "latte"], history_path=history_path)

    assert result.value.code != 0
    assert "Unsupported drink: latte" in capsys.readouterr().err
    assert not history_path.exists()


def test_drink_records_an_explicit_historical_time_as_utc(
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"

    assert main(
        ["drink", "espresso", "--at", "2026-09-05T14:30:00+02:00"],
        history_path=history_path,
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
    ) == 0

    assert read_events(history_path)[0].timestamp == datetime(
        2026, 9, 5, 12, 30, tzinfo=UTC
    )


def test_drink_without_at_uses_the_injected_current_time(tmp_path: Path) -> None:
    history_path = tmp_path / "history.jsonl"
    now = datetime(2026, 9, 7, 12, 0, tzinfo=UTC)

    assert main(["drink", "espresso"], history_path=history_path, now=now) == 0

    assert read_events(history_path)[0].timestamp == now


@pytest.mark.parametrize(
    "timestamp",
    [
        "not-a-timestamp",
        "",
        "2026-09-05T14:30:00",
        "2026-09-08T12:00:00+00:00",
    ],
)
def test_drink_rejects_invalid_explicit_time_without_writing(
    timestamp: str,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"

    with pytest.raises(SystemExit) as result:
        main(
            ["drink", "espresso", "--at", timestamp],
            history_path=history_path,
            now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
        )

    assert result.value.code != 0
    assert "occurrence time" in capsys.readouterr().err
    assert not history_path.exists()


def test_drink_reports_persistence_failure_without_traceback(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Filesystem failures remain a clean CLI error at the presentation boundary."""
    def fail_to_append(*args: object) -> None:
        raise OSError("read-only filesystem")

    monkeypatch.setattr("cdd.cli.append_event", fail_to_append)

    with pytest.raises(SystemExit) as result:
        main(["drink", "espresso"], history_path=tmp_path / "history.jsonl")

    assert result.value.code != 0
    assert "Could not persist coffee event" in capsys.readouterr().err


def test_help_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI exposes its initial help screen."""
    with pytest.raises(SystemExit) as result:
        main(["--help"])

    assert result.value.code == 0
    assert "Coffee-Driven Development" in capsys.readouterr().out


def test_history_displays_newest_events_first_in_local_time(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    append_event(
        CoffeeEvent(datetime(2026, 9, 7, 10, 0, tzinfo=UTC), "espresso", 80),
        history_path,
    )
    append_event(
        CoffeeEvent(datetime(2026, 9, 7, 12, 30, tzinfo=UTC), "americano", 120),
        history_path,
    )
    local_now = datetime(
        2026,
        9,
        7,
        15,
        0,
        tzinfo=timezone(timedelta(hours=2)),
    )

    assert main(["history"], history_path=history_path, now=local_now) == 0

    output = capsys.readouterr().out
    assert output.index("Americano") < output.index("Espresso")
    assert "2026-09-07 14:30" in output


def test_history_limit_and_empty_history_are_explicit(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    append_event(
        CoffeeEvent(datetime(2026, 9, 7, 10, 0, tzinfo=UTC), "espresso", 80),
        history_path,
    )
    append_event(
        CoffeeEvent(datetime(2026, 9, 7, 11, 0, tzinfo=UTC), "americano", 120),
        history_path,
    )

    assert main(["history", "--limit", "1"], history_path=history_path) == 0
    output = capsys.readouterr().out
    assert "Americano" in output
    assert "Espresso" not in output

    assert main(["history"], history_path=tmp_path / "missing.jsonl") == 0
    assert "No coffee recorded yet." in capsys.readouterr().out


@pytest.mark.parametrize(
    "command",
    [
        ["history", "--limit", "0"],
        ["stats", "--days", "-1"],
        ["stats", "--days", "coffee"],
    ],
)
def test_numeric_options_require_positive_integers(
    command: list[str],
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    with pytest.raises(SystemExit) as result:
        main(command, history_path=tmp_path / "history.jsonl")

    assert result.value.code != 0
    assert "positive integer" in capsys.readouterr().err


def test_status_reports_explicit_empty_history_semantics(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=UTC)

    assert main(["status"], history_path=tmp_path / "missing.jsonl", now=now) == 0

    output = capsys.readouterr().out
    assert "Coffee-Driven Development" in output
    assert "Coffees today" in output and "0" in output
    assert "Caffeine today" in output and "0 mg" in output
    assert "NO SIGNAL" in output


def test_status_uses_only_events_on_the_local_day(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    append_event(
        CoffeeEvent(datetime(2026, 9, 6, 21, 0, tzinfo=UTC), "espresso", 80),
        history_path,
    )
    append_event(
        CoffeeEvent(datetime(2026, 9, 6, 22, 0, tzinfo=UTC), "americano", 120),
        history_path,
    )
    now = datetime(2026, 9, 7, 8, 0, tzinfo=timezone(timedelta(hours=2)))

    assert main(["status"], history_path=history_path, now=now) == 0

    output = capsys.readouterr().out
    assert "1" in output
    assert "120 mg" in output
    assert "PRODUCTIVE" in output


def test_stats_reports_numeric_results_favorite_and_daily_bars(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    events = [
        CoffeeEvent(datetime(2026, 9, 5, 9, 0, tzinfo=UTC), "espresso", 80),
        CoffeeEvent(datetime(2026, 9, 7, 9, 0, tzinfo=UTC), "americano", 120),
    ]
    for event in events:
        append_event(event, history_path)

    assert main(
        ["stats", "--days", "3"],
        history_path=history_path,
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
    ) == 0

    output = capsys.readouterr().out
    assert "Total coffees" in output and "2" in output
    assert "Total caffeine" in output and "200 mg" in output
    assert "Average per day" in output and "67 mg" in output
    assert "Favorite drink" in output and "Americano" in output
    assert "Sep 06" in output and "0 mg" in output
    assert "█" in output


def test_stats_empty_history_has_no_favorite(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    assert main(
        ["stats"],
        history_path=tmp_path / "missing.jsonl",
        now=datetime(2026, 9, 7, tzinfo=UTC),
    ) == 0

    output = capsys.readouterr().out
    assert "No data" in output
    assert "Favorite drink" in output and "None" in output


def test_stats_rejects_a_window_before_the_minimum_date(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    with pytest.raises(SystemExit) as result:
        main(
            ["stats", "--days", "2"],
            history_path=tmp_path / "missing.jsonl",
            now=datetime(1, 1, 1, tzinfo=UTC),
        )

    assert result.value.code != 0
    assert "statistics period" in capsys.readouterr().err


def test_malformed_history_is_a_clean_cli_error(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    history_path.write_text("not json\n", encoding="utf-8")

    with pytest.raises(SystemExit) as result:
        main(["status"], history_path=history_path)

    assert result.value.code != 0
    assert "Could not read coffee history" in capsys.readouterr().err


def test_interactive_reuses_add_now_and_status_behavior(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    responses: Iterator[str] = iter(["1", "espresso", "", "2", "5"])

    assert main(
        ["interactive"],
        history_path=tmp_path / "history.jsonl",
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
        input_fn=lambda _prompt: next(responses),
    ) == 0

    output = capsys.readouterr().out
    assert "Coffee recorded" in output
    assert "80 mg" in output
    assert "BOOTING" in output
    assert "Goodbye" in output


def test_interactive_records_historical_time_and_includes_it_in_stats(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    responses: Iterator[str] = iter(
        ["1", "americano", "historical", "2026-09-05T14:30:00+02:00", "4", "5"]
    )

    assert main(
        ["interactive"],
        history_path=history_path,
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
        input_fn=lambda _prompt: next(responses),
    ) == 0

    assert read_events(history_path)[0].timestamp == datetime(
        2026, 9, 5, 12, 30, tzinfo=UTC
    )
    output = capsys.readouterr().out
    assert "Total coffees" in output and "1" in output
    assert "120 mg" in output


def test_interactive_rejects_future_time_without_writing(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    responses: Iterator[str] = iter(
        ["1", "espresso", "historical", "2026-09-08T12:00:00+00:00", "5"]
    )

    assert main(
        ["interactive"],
        history_path=history_path,
        now=datetime(2026, 9, 7, 12, 0, tzinfo=UTC),
        input_fn=lambda _prompt: next(responses),
    ) == 0

    assert "Invalid occurrence time" in capsys.readouterr().out
    assert not history_path.exists()


def test_interactive_handles_invalid_input_and_keyboard_interrupt(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    responses: Iterator[str] = iter(["invalid", "5"])
    assert main(
        ["interactive"],
        history_path=tmp_path / "history.jsonl",
        input_fn=lambda _prompt: next(responses),
    ) == 0
    assert "Invalid selection" in capsys.readouterr().out

    def interrupt(_prompt: str) -> str:
        raise KeyboardInterrupt

    assert main(
        ["interactive"],
        history_path=tmp_path / "history.jsonl",
        input_fn=interrupt,
    ) == 0
    assert "Goodbye" in capsys.readouterr().out


def test_interactive_exposes_history_and_stats(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    responses: Iterator[str] = iter(["3", "4", "5"])

    assert main(
        ["interactive"],
        history_path=tmp_path / "missing.jsonl",
        now=datetime(2026, 9, 7, tzinfo=UTC),
        input_fn=lambda _prompt: next(responses),
    ) == 0

    output = capsys.readouterr().out
    assert "No coffee recorded yet." in output
    assert "Coffee Statistics" in output
    assert "Goodbye" in output


def test_interactive_exits_cleanly_when_drink_prompt_reaches_eof(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    calls = iter(["1"])

    def respond(_prompt: str) -> str:
        try:
            return next(calls)
        except StopIteration as error:
            raise EOFError from error

    assert main(
        ["interactive"],
        history_path=tmp_path / "history.jsonl",
        input_fn=respond,
    ) == 0
    assert "Goodbye" in capsys.readouterr().out


def test_interactive_refreshes_the_clock_for_each_added_drink(
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    responses: Iterator[str] = iter(
        ["1", "espresso", "", "1", "americano", "", "5"]
    )
    times: Iterator[datetime] = iter(
        [
            datetime(2026, 9, 7, 23, 59, tzinfo=UTC),
            datetime(2026, 9, 8, 0, 1, tzinfo=UTC),
        ]
    )

    assert main(
        ["interactive"],
        history_path=history_path,
        clock=lambda: next(times),
        to_local=lambda timestamp: timestamp,
        input_fn=lambda _prompt: next(responses),
    ) == 0

    assert [event.timestamp for event in read_events(history_path)] == [
        datetime(2026, 9, 7, 23, 59, tzinfo=UTC),
        datetime(2026, 9, 8, 0, 1, tzinfo=UTC),
    ]


def test_interactive_samples_the_clock_after_the_drink_prompt(
    tmp_path: Path,
) -> None:
    history_path = tmp_path / "history.jsonl"
    current_time = [datetime(2026, 9, 7, 23, 59, tzinfo=UTC)]
    responses: Iterator[str] = iter(["1", "espresso", "", "5"])

    def respond(prompt: str) -> str:
        if prompt == "Drink: ":
            current_time[0] = datetime(2026, 9, 8, 0, 1, tzinfo=UTC)
        return next(responses)

    assert main(
        ["interactive"],
        history_path=history_path,
        clock=lambda: current_time[0],
        to_local=lambda timestamp: timestamp,
        input_fn=respond,
    ) == 0

    assert read_events(history_path)[0].timestamp == datetime(
        2026,
        9,
        8,
        0,
        1,
        tzinfo=UTC,
    )
