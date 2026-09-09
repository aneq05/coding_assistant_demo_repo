"""Tests for deterministic terminal presentation helpers."""

import pytest
from rich.console import Console

from cdd.domain import supported_drinks
from cdd.presentation import (
    _developer_state_style,
    _format_coffee_count,
    caffeine_bar,
    caffeine_gauge,
    caffeine_sparkline,
    developer_state_indicator,
    render_drink_picker,
)


def test_drink_picker_renders_numbers_icons_names_and_caffeine() -> None:
    console = Console(record=True, width=80)

    render_drink_picker(console, supported_drinks())

    output = console.export_text()
    expected_rows = [
        ("1", "☕", "Espresso", "80 mg"),
        ("2", "🖤", "Americano", "120 mg"),
        ("3", "🤎", "Cappuccino", "75 mg"),
        ("4", "🥛", "Latte", "75 mg"),
        ("5", "🤍", "Flat White", "130 mg"),
        ("6", "🍫", "Mocha", "90 mg"),
        ("7", "⚡", "Double Espresso", "160 mg"),
    ]
    for number, icon, name, caffeine in expected_rows:
        assert number in output
        assert icon in output
        assert name in output
        assert caffeine in output


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


@pytest.mark.parametrize(
    ("caffeine_mg", "expected_filled"),
    [
        (-10, 0),
        (0, 0),
        (1, 1),
        (200, 9),
        (400, 18),
        (800, 18),
    ],
)
def test_caffeine_gauge_is_bounded_and_keeps_a_fixed_width(
    caffeine_mg: int,
    expected_filled: int,
) -> None:
    gauge = caffeine_gauge(caffeine_mg)

    assert len(gauge) == 18
    assert gauge.count("█") == expected_filled
    assert gauge.count("░") == 18 - expected_filled


def test_caffeine_gauge_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="width"):
        caffeine_gauge(100, width=0)

    with pytest.raises(ValueError, match="maximum_mg"):
        caffeine_gauge(100, maximum_mg=0)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], ""),
        ([0, 0, 0], "· · ·"),
        ([0, 50, 100], "· ▅ █"),
        ([100, 100], "█ █"),
    ],
)
def test_caffeine_sparkline_scales_relative_values_and_preserves_zero_days(
    values: list[int],
    expected: str,
) -> None:
    assert caffeine_sparkline(values) == expected


@pytest.mark.parametrize(
    ("state", "indicator", "style"),
    [
        ("NO SIGNAL", "○ ○ ○ ○ ○", "dim"),
        ("BOOTING", "● ○ ○ ○ ○", "cyan"),
        ("PRODUCTIVE", "● ● ● ○ ○", "green"),
        ("TURBO MODE", "● ● ● ● ○", "yellow"),
        (
            "ARCHITECTURE PRIVILEGES REVOKED",
            "● ● ● ● ●",
            "bold red",
        ),
    ],
)
def test_developer_state_has_deterministic_visual_signal_and_style(
    state: str,
    indicator: str,
    style: str,
) -> None:
    assert developer_state_indicator(state) == indicator
    assert _developer_state_style(state) == style
