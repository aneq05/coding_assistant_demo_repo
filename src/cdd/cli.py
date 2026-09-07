"""Command-line interface for Coffee-Driven Development."""

import argparse
import sys
from collections.abc import Callable, Sequence
from datetime import datetime, tzinfo
from pathlib import Path

from rich.console import Console

from cdd.domain import (
    UnsupportedDrinkError,
    calculate_stats,
    create_coffee_event,
    get_drink,
    summarize_today,
)
from cdd.presentation import (
    render_drink,
    render_history,
    render_interactive_menu,
    render_stats,
    render_status,
)
from cdd.storage import InvalidHistoryError, append_event, read_events

InputFunction = Callable[[str], str]


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
    console: Console | None = None,
    input_fn: InputFunction = input,
) -> int:
    """Run the CLI and return its exit status."""
    parser = build_parser()
    arguments = parser.parse_args(argv)
    output = console or _default_console()
    local_now = now or datetime.now().astimezone()

    if arguments.command == "drink":
        try:
            drink = get_drink(arguments.drink)
        except UnsupportedDrinkError as error:
            parser.error(str(error))

        try:
            append_event(
                create_coffee_event(drink, timestamp=local_now),
                history_path,
            )
        except OSError as error:
            parser.error(f"Could not persist coffee event: {error}")

        render_drink(output, drink)
    elif arguments.command == "interactive":
        _run_interactive(
            output,
            history_path=history_path,
            now=local_now,
            input_fn=input_fn,
        )
    elif arguments.command is not None:
        try:
            if arguments.command == "history":
                _show_history(
                    output,
                    history_path=history_path,
                    limit=arguments.limit,
                    now=local_now,
                )
            elif arguments.command == "status":
                _show_status(output, history_path=history_path, now=local_now)
            elif arguments.command == "stats":
                _show_stats(
                    output,
                    history_path=history_path,
                    days=arguments.days,
                    now=local_now,
                )
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
    now: datetime,
) -> None:
    events = read_events(history_path)
    local_timezone = _aware_timezone(now)
    render_history(
        console,
        list(reversed(events[-limit:])),
        local_timezone=local_timezone,
    )


def _show_status(
    console: Console,
    *,
    history_path: Path | None,
    now: datetime,
) -> None:
    render_status(console, summarize_today(read_events(history_path), now=now))


def _show_stats(
    console: Console,
    *,
    history_path: Path | None,
    days: int,
    now: datetime,
) -> None:
    render_stats(
        console,
        calculate_stats(read_events(history_path), days=days, now=now),
    )


def _run_interactive(
    console: Console,
    *,
    history_path: Path | None,
    now: datetime,
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
            if not _interactive_add(console, history_path, now, input_fn):
                console.print("Goodbye.")
                return
            continue

        try:
            if selection in {"2", "status"}:
                _show_status(console, history_path=history_path, now=now)
            elif selection in {"3", "history"}:
                _show_history(console, history_path=history_path, limit=20, now=now)
            elif selection in {"4", "stats"}:
                _show_stats(console, history_path=history_path, days=7, now=now)
            else:
                console.print("Invalid selection. Choose 1–5.")
        except (InvalidHistoryError, OSError) as error:
            console.print(f"Could not read coffee history: {error}")


def _interactive_add(
    console: Console,
    history_path: Path | None,
    now: datetime,
    input_fn: InputFunction,
) -> bool:
    console.print("Choose espresso, americano, or cappuccino.")
    try:
        name = input_fn("Drink: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False

    try:
        drink = get_drink(name)
        append_event(create_coffee_event(drink, timestamp=now), history_path)
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


if __name__ == "__main__":
    raise SystemExit(main())
