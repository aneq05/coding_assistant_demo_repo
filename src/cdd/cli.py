"""Command-line interface for Coffee-Driven Development."""

import argparse
from collections.abc import Sequence

from cdd.domain import UnsupportedDrinkError, get_drink


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


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return its exit status."""
    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "drink":
        try:
            drink = get_drink(arguments.drink)
        except UnsupportedDrinkError as error:
            parser.error(str(error))

        print(drink.name)
        print(f"Estimated caffeine: {drink.caffeine_mg} mg")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
