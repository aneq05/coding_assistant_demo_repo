"""Command-line interface for Coffee-Driven Development."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from cdd.domain import UnsupportedDrinkError, create_coffee_event, get_drink
from cdd.storage import append_event


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
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    history_path: Path | None = None,
) -> int:
    """Run the CLI and return its exit status."""
    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "drink":
        try:
            drink = get_drink(arguments.drink)
        except UnsupportedDrinkError as error:
            parser.error(str(error))

        try:
            append_event(create_coffee_event(drink), history_path)
        except OSError as error:
            parser.error(f"Could not persist coffee event: {error}")

        print(drink.name)
        print(f"Estimated caffeine: {drink.caffeine_mg} mg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
