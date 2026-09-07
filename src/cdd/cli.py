"""Command-line interface for Coffee-Driven Development."""

import argparse
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, datetime, tzinfo
from pathlib import Path

from rich.console import Console

from cdd.domain import (
    InvalidStatsPeriodError,
    LocalTimeConverter,
    UnsupportedDrinkError,
    calculate_stats,
    create_coffee_event,
    get_drink,
    summarize_today,
)
from cdd.git_activity import get_git_activity
from cdd.presentation import (
    render_drink,
    render_history,
    render_interactive_menu,
    render_stats,
    render_status,
)
from cdd.storage import InvalidHistoryError, append_event, read_events

InputFunction = Callable[[str], str]
Clock = Callable[[], datetime]


def _configure_stdio() -> None:
    """Prefer UTF-8 terminal output when the platform supports reconfiguration."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _default_console() -> Console:
    """Build a presentation console with UTF-8-friendly terminal settings."""
    _configure_stdio()
    return Console(highlight=False, legacy_windows=False)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="cdd",
        description="Coffee-Driven Development: an over-serious coffee CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")
    drink_parser = subparsers.add_parser(
        "drink",
        help="Show deterministic caffeine information for a drink.",
    )
    drink_parser.add_argument("drink")
    history_parser = subparsers.add_parser(
        "history",
        help="Show recent coffee history.",
    )
    history_parser.add_argument("--limit", type=_positive_integer, default=20)
    subparsers.add_parser("status", help="Show today's coffee status.")
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show coffee statistics for recent calendar days.",
    )
    stats_parser.add_argument("--days", type=_positive_integer, default=7)
    subparsers.add_parser("interactive", help="Start the interactive menu.")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    history_path: Path | None = None,
    now: datetime | None = None,
    clock: Clock | None = None,
    to_local: LocalTimeConverter | None = None,
    console: Console | None = None,
    input_fn: InputFunction = input,
) -> int:
    """Run the CLI and return its exit status."""
    parser = build_parser()
    arguments = parser.parse_args(argv)
    output = console or _default_console()
    current_time, localize = _time_context(now, clock, to_local)

    if arguments.command == "drink":
        try:
            drink = get_drink(arguments.drink)
        except UnsupportedDrinkError as error:
            parser.error(str(error))

        try:
            append_event(
                create_coffee_event(drink, timestamp=current_time()),
                history_path,
            )
        except OSError as error:
            parser.error(f"Could not persist coffee event: {error}")

        render_drink(output, drink)
    elif arguments.command == "interactive":
        _run_interactive(
            output,
            history_path=history_path,
            clock=current_time,
            to_local=localize,
            input_fn=input_fn,
        )
    elif arguments.command is not None:
        try:
            if arguments.command == "history":
                _show_history(
                    output,
                    history_path=history_path,
                    limit=arguments.limit,
                    to_local=localize,
                )
            elif arguments.command == "status":
                _show_status(
                    output,
                    history_path=history_path,
                    now=current_time(),
                    to_local=localize,
                )
            elif arguments.command == "stats":
                try:
                    _show_stats(
                        output,
                        history_path=history_path,
                        days=arguments.days,
                        now=current_time(),
                        to_local=localize,
                    )
                except InvalidStatsPeriodError as error:
                    parser.error(f"Invalid statistics period: {error}")
        except (InvalidHistoryError, OSError) as error:
            parser.error(f"Could not read coffee history: {error}")

    return 0


def _positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _show_history(
    console: Console,
    *,
    history_path: Path | None,
    limit: int,
    to_local: LocalTimeConverter,
) -> None:
    events = read_events(history_path)
    render_history(
        console,
        list(reversed(events[-limit:])),
        to_local=to_local,
    )


def _show_status(
    console: Console,
    *,
    history_path: Path | None,
    now: datetime,
    to_local: LocalTimeConverter,
) -> None:
    render_status(
        console,
        summarize_today(read_events(history_path), now=now, to_local=to_local),
        get_git_activity(now=now, to_local=to_local),
    )


def _show_stats(
    console: Console,
    *,
    history_path: Path | None,
    days: int,
    now: datetime,
    to_local: LocalTimeConverter,
) -> None:
    render_stats(
        console,
        calculate_stats(
            read_events(history_path),
            days=days,
            now=now,
            to_local=to_local,
        ),
    )


def _run_interactive(
    console: Console,
    *,
    history_path: Path | None,
    clock: Clock,
    to_local: LocalTimeConverter,
    input_fn: InputFunction,
) -> None:
    while True:
        render_interactive_menu(console)
        try:
            selection = input_fn("Choose an option: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye.")
            return

        if selection in {"5", "exit", "quit"}:
            console.print("Goodbye.")
            return
        if selection in {"1", "add", "drink"}:
            if not _interactive_add(
                console,
                history_path,
                clock,
                input_fn,
            ):
                console.print("Goodbye.")
                return
            continue

        try:
            if selection in {"2", "status"}:
                _show_status(
                    console,
                    history_path=history_path,
                    now=clock(),
                    to_local=to_local,
                )
            elif selection in {"3", "history"}:
                _show_history(
                    console,
                    history_path=history_path,
                    limit=20,
                    to_local=to_local,
                )
            elif selection in {"4", "stats"}:
                _show_stats(
                    console,
                    history_path=history_path,
                    days=7,
                    now=clock(),
                    to_local=to_local,
                )
            else:
                console.print("Invalid selection. Choose 1–5.")
        except InvalidStatsPeriodError as error:
            console.print(f"Invalid statistics period: {error}")
        except (InvalidHistoryError, OSError) as error:
            console.print(f"Could not read coffee history: {error}")


def _interactive_add(
    console: Console,
    history_path: Path | None,
    clock: Clock,
    input_fn: InputFunction,
) -> bool:
    console.print("Choose espresso, americano, or cappuccino.")
    try:
        name = input_fn("Drink: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False

    try:
        drink = get_drink(name)
        append_event(
            create_coffee_event(drink, timestamp=clock()),
            history_path,
        )
    except UnsupportedDrinkError as error:
        console.print(str(error))
        return True
    except OSError as error:
        console.print(f"Could not persist coffee event: {error}")
        return True
    render_drink(console, drink, recorded=True)
    return True


def _aware_timezone(timestamp: datetime) -> tzinfo:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    return timestamp.tzinfo


def _system_clock() -> datetime:
    return datetime.now(UTC)


def _system_local_time(timestamp: datetime) -> datetime:
    return timestamp.astimezone()


def _time_context(
    now: datetime | None,
    clock: Clock | None,
    to_local: LocalTimeConverter | None,
) -> tuple[Clock, LocalTimeConverter]:
    if now is None:
        return clock or _system_clock, to_local or _system_local_time
    if clock is not None:
        raise ValueError("now and clock cannot both be supplied")

    local_timezone = _aware_timezone(now)

    def fixed_clock() -> datetime:
        return now

    def fixed_local_time(timestamp: datetime) -> datetime:
        return timestamp.astimezone(local_timezone)

    return fixed_clock, to_local or fixed_local_time


if __name__ == "__main__":
    raise SystemExit(main())
