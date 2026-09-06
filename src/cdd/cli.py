"""Command-line interface for Coffee-Driven Development."""

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    return argparse.ArgumentParser(
        prog="cdd",
        description="Coffee-Driven Development: an over-serious coffee CLI.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return its exit status."""
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
