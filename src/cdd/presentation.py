"""Rich terminal presentation for Coffee-Driven Development."""

from math import ceil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cdd.domain import (
    CoffeeEvent,
    CoffeeStats,
    Drink,
    LocalTimeConverter,
    TodaySummary,
)
from cdd.git_activity import GitActivity


def caffeine_bar(caffeine_mg: int) -> str:
    """Return a deterministic, capped one-block-per-40-mg bar."""
    if caffeine_mg <= 0:
        return ""
    return "█" * min(20, max(1, ceil(caffeine_mg / 40)))


def render_drink(console: Console, drink: Drink, *, recorded: bool = False) -> None:
    """Render one supported drink."""
    console.print(drink.name)
    console.print(f"Estimated caffeine: {drink.caffeine_mg} mg")
    if recorded:
        console.print("Coffee recorded.")


def _format_coffee_count(count: int) -> str:
    """Return a numeric zero or one emoji per coffee consumed today."""
    if count == 0:
        return "0"
    return " ".join("☕" for _ in range(count))


def render_history(
    console: Console,
    events: list[CoffeeEvent],
    *,
    to_local: LocalTimeConverter,
) -> None:
    """Render coffee events in their supplied display order."""
    if not events:
        console.print("No coffee recorded yet.")
        return

    table = Table(title="Coffee history")
    table.add_column("Local time")
    table.add_column("Drink")
    table.add_column("Caffeine", justify="right")
    for event in events:
        local_time = to_local(event.timestamp)
        table.add_row(
            local_time.strftime("%Y-%m-%d %H:%M"),
            event.drink.title(),
            f"{event.caffeine_mg} mg",
        )
    console.print(table)


def render_status(
    console: Console,
    summary: TodaySummary,
    git_activity: GitActivity,
) -> None:
    """Render coffee and local Git status in one compact report."""
    report = Table.grid(expand=True, padding=(0, 1))
    report.add_column(style="bold")
    report.add_column(justify="right")
    report.add_row("[bold]Coffee[/bold]", "")
    report.add_row("Coffees today", _format_coffee_count(summary.coffees))
    report.add_row("Caffeine today", f"{summary.caffeine_mg} mg")
    report.add_row("Developer state", summary.developer_state)
    report.add_row("", "")
    report.add_row("[bold]Git activity[/bold]", "")
    report.add_row("Commits today", str(git_activity.commits_today))
    latest_commit = (
        git_activity.latest_commit.strftime("%Y-%m-%d %H:%M")
        if git_activity.latest_commit is not None
        else "None"
    )
    report.add_row("Latest commit", latest_commit)
    report.add_row("Activity level", git_activity.activity_level)
    console.print(Panel(report, title="Coffee-Driven Development"))


def render_stats(console: Console, stats: CoffeeStats) -> None:
    """Render summary statistics and a per-day caffeine chart."""
    if stats.total_coffees == 0:
        console.print(f"No data in the last {stats.days} days.")

    summary = Table(
        title=f"Coffee Statistics — last {stats.days} days",
        show_header=False,
    )
    summary.add_column("Metric")
    summary.add_column("Value", justify="right")
    summary.add_row("Total coffees", str(stats.total_coffees))
    summary.add_row("Total caffeine", f"{stats.total_caffeine_mg} mg")
    summary.add_row("Average per day", f"{round(stats.average_caffeine_mg)} mg")
    favorite = stats.favorite_drink.title() if stats.favorite_drink else "None"
    summary.add_row("Favorite drink", favorite)
    console.print(summary)

    daily = Table(title="Daily caffeine")
    daily.add_column("Date")
    daily.add_column("Caffeine", justify="right")
    daily.add_column("Chart")
    for total in stats.daily:
        daily.add_row(
            total.day.strftime("%a  %b %d"),
            f"{total.caffeine_mg} mg",
            caffeine_bar(total.caffeine_mg),
        )
    console.print(daily)


def render_interactive_menu(console: Console) -> None:
    """Render the interactive command menu."""
    console.print("\nCoffee-Driven Development")
    console.print("1. Add coffee")
    console.print("2. Show status")
    console.print("3. Show history")
    console.print("4. Show stats")
    console.print("5. Exit")
