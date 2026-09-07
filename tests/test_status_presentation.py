"""Tests for the cohesive status report."""

from datetime import UTC, datetime
from io import StringIO

from rich.console import Console

from cdd.domain import TodaySummary
from cdd.git_activity import GitActivity
from cdd.presentation import render_status


def test_render_status_uses_one_panel_with_coffee_and_git_sections() -> None:
    output = StringIO()
    console = Console(file=output, force_terminal=False, color_system=None)

    render_status(
        console,
        TodaySummary(coffees=2, caffeine_mg=200, developer_state="PRODUCTIVE"),
        GitActivity(
            commits_today=3,
            latest_commit=datetime(2026, 9, 7, 11, 30, tzinfo=UTC),
        ),
    )

    rendered = output.getvalue()
    assert "Coffee-Driven Development" in rendered
    assert "Coffee" in rendered
    assert "Git activity" in rendered
    assert "Coffees today" in rendered
    assert "Caffeine today" in rendered
    assert "Developer state" in rendered
    assert "Commits today" in rendered
    assert "Latest commit" in rendered
    assert "Activity level" in rendered
    assert "SHIPPING" in rendered
