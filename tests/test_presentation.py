"""Tests for deterministic terminal presentation helpers."""

import pytest

from cdd.presentation import _format_coffee_count, caffeine_bar


@pytest.mark.parametrize(
    ("count", "expected"),
    [(0, "0"), (1, "☕"), (3, "☕ ☕ ☕")],
)
def test_format_coffee_count_uses_numeric_zero_or_emoji_per_drink(
    count: int,
    expected: str,
) -> None:
    assert _format_coffee_count(count) == expected


@pytest.mark.parametrize(
    ("caffeine_mg", "blocks"),
    [(0, 0), (1, 1), (40, 1), (41, 2), (800, 20), (900, 20)],
)
def test_caffeine_bar_uses_a_capped_one_block_per_40_mg_scale(
    caffeine_mg: int,
    blocks: int,
) -> None:
    assert caffeine_bar(caffeine_mg) == "█" * blocks
