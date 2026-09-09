"""Rich terminal presentation for Coffee-Driven Development."""

from collections.abc import Sequence
from math import ceil

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cdd.domain import (
    CoffeeEvent,
    CoffeeStats,
    Drink,
    LocalTimeConverter,
    TodaySummary,
)
from cdd.git_activity import GitActivity

_STATE_STYLES = {
    "NO SIGNAL": "dim",
    "BOOTING": "cyan",
    "PRODUCTIVE": "green",
    "TURBO MODE": "yellow",
    "ARCHITECTURE PRIVILEGES REVOKED": "bold red",
}

_STATE_LEVELS = {
    "NO SIGNAL": 0,
    "BOOTING": 1,
    "PRODUCTIVE": 3,
    "TURBO MODE": 4,
    "ARCHITECTURE PRIVILEGES REVOKED": 5,
}

_ACTIVITY_STYLES = {
    "QUIET": "dim",
    "ACTIVE": "cyan",
    "SHIPPING": "green",
    "DEEP WORK": "bold magenta",
}

_SPARK_LEVELS = "▂▃▄▅▆▇█"

_DRINK_ICONS = {
    "espresso": "☕",
    "americano": "🖤",
    "cappuccino": "🤎",
    "latte": "🥛",
    "flat-white": "🤍",
    "mocha": "🍫",
    "double-espresso": "⚡",
}


def caffeine_bar(caffeine_mg: int) -> str:
    """Return a deterministic, capped one-block-per-40-mg bar."""
    if caffeine_mg <= 0:
        return ""
    return "█" * min(20, max(1, ceil(caffeine_mg / 40)))


def caffeine_gauge(
    caffeine_mg: int,
    *,
    width: int = 18,
    maximum_mg: int = 400,
) -> str:
    """Return a bounded filled/empty caffeine gauge."""
    if width <= 0:
        raise ValueError("width must be positive")
    if maximum_mg <= 0:
        raise ValueError("maximum_mg must be positive")

    bounded = min(max(caffeine_mg, 0), maximum_mg)
    if bounded == 0:
        filled = 0
    else:
        filled = max(1, ceil((bounded / maximum_mg) * width))

    filled = min(width, filled)
    return "█" * filled + "░" * (width - filled)


def caffeine_sparkline(values: Sequence[int]) -> str:
    """Return a compact deterministic sparkline with visible zero values."""
    if not values:
        return ""

    maximum = max(values)
    if maximum <= 0:
        return " ".join("·" for _ in values)

    points: list[str] = []
    for value in values:
        if value <= 0:
            points.append("·")
            continue

        scaled = ceil((value / maximum) * len(_SPARK_LEVELS))
        index = min(len(_SPARK_LEVELS) - 1, max(0, scaled - 1))
        points.append(_SPARK_LEVELS[index])

    return " ".join(points)


def developer_state_indicator(state: str) -> str:
    """Return a five-step visual signal for the developer state."""
    active = _STATE_LEVELS.get(state, 0)
    return " ".join(["●"] * active + ["○"] * (5 - active))


def _developer_state_style(state: str) -> str:
    """Return semantic Rich styling for a developer state."""
    return _STATE_STYLES.get(state, "white")


def _activity_style(activity_level: str) -> str:
    """Return semantic Rich styling for a Git activity level."""
    return _ACTIVITY_STYLES.get(activity_level, "white")


def render_drink(console: Console, drink: Drink, *, recorded: bool = False) -> None:
    """Render one supported drink without changing its textual contract."""
    console.print(Text(drink.name, style="bold cyan"))
    console.print(
        Text(
            f"Estimated caffeine: {drink.caffeine_mg} mg",
            style="bright_black",
        )
    )
    if recorded:
        console.print(Text("Coffee recorded.", style="bold green"))


def render_drink_picker(console: Console, drinks: Sequence[Drink]) -> None:
    """Render the domain-owned drink catalog as a numbered Rich picker."""
    choices = Table.grid(padding=(0, 1))
    choices.add_column(style="bold cyan", justify="right")
    choices.add_column(justify="center")
    choices.add_column(min_width=18)
    choices.add_column(style="bright_black", justify="right")

    for number, drink in enumerate(drinks, start=1):
        choices.add_row(
            f"[{number}]",
            _DRINK_ICONS[drink.kind],
            drink.name,
            f"{drink.caffeine_mg} mg",
        )

    console.print()
    console.print(
        Panel(
            choices,
            title="Choose your coffee",
            border_style="cyan",
            padding=(1, 2),
        )
    )


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
        console.print(Text("No coffee recorded yet.", style="dim"))
        return

    table = Table(
        title="☕ Coffee history",
        title_style="bold cyan",
        header_style="bold",
        border_style="bright_black",
        row_styles=("", "dim"),
    )
    table.add_column("#", justify="right", style="bright_black", width=3)
    table.add_column("Time", min_width=16)
    table.add_column("Drink", min_width=12)
    table.add_column("Caffeine", justify="right", min_width=10)

    for index, event in enumerate(events, start=1):
        local_time = to_local(event.timestamp)
        table.add_row(
            str(index),
            local_time.strftime("%Y-%m-%d %H:%M"),
            event.drink.title(),
            f"{event.caffeine_mg} mg",
        )

    console.print(table)


def _coffee_status_panel(summary: TodaySummary) -> Panel:
    """Build the coffee half of the status dashboard."""
    style = _developer_state_style(summary.developer_state)

    report = Table.grid(expand=True, padding=(0, 1))
    report.add_column(style="bright_black")
    report.add_column(justify="right")

    report.add_row("Coffees today", _format_coffee_count(summary.coffees))
    report.add_row("Caffeine today", f"[bold]{summary.caffeine_mg} mg[/bold]")
    report.add_row(
        "Caffeine load",
        f"[cyan]{caffeine_gauge(summary.caffeine_mg)}[/cyan]",
    )
    report.add_row("", "")
    report.add_row("Developer state", f"[{style}]{summary.developer_state}[/{style}]")
    report.add_row(
        "State signal",
        f"[{style}]{developer_state_indicator(summary.developer_state)}[/{style}]",
    )

    return Panel(
        report,
        title="☕ Coffee today",
        title_align="left",
        border_style="cyan",
        padding=(1, 1),
    )


def _git_status_panel(git_activity: GitActivity) -> Panel:
    """Build the Git half of the status dashboard."""
    activity_style = _activity_style(git_activity.activity_level)

    latest_commit = (
        git_activity.latest_commit.strftime("%Y-%m-%d %H:%M")
        if git_activity.latest_commit is not None
        else "None"
    )

    report = Table.grid(expand=True, padding=(0, 1))
    report.add_column(style="bright_black")
    report.add_column(justify="right")

    report.add_row("Commits today", f"[bold]{git_activity.commits_today}[/bold]")
    report.add_row("Latest commit", latest_commit)
    report.add_row(
        "Activity level",
        f"[{activity_style}]{git_activity.activity_level}[/{activity_style}]",
    )
    report.add_row("", "")
    report.add_row(
        "Local signal",
        "[dim]git log · current local day[/dim]",
    )

    return Panel(
        report,
        title="Git activity",
        title_align="left",
        border_style="magenta",
        padding=(1, 1),
    )


def render_status(
    console: Console,
    summary: TodaySummary,
    git_activity: GitActivity,
) -> None:
    """Render coffee and local Git status as a terminal dashboard."""
    heading = Text(justify="center")
    heading.append("☕ Coffee-Driven Development", style="bold")
    heading.append("\ndeveloper telemetry", style="bright_black")

    console.print(
        Panel(
            Align.center(heading),
            border_style="bright_blue",
            padding=(0, 2),
        )
    )

    panels = [
        _coffee_status_panel(summary),
        _git_status_panel(git_activity),
    ]
    console.print(
        Columns(
            panels,
            equal=True,
            expand=True,
            padding=(0, 1),
        )
    )


def _trend_panel(stats: CoffeeStats) -> Panel:
    """Build a compact recent caffeine trend panel."""
    visible_days = stats.daily[-min(14, len(stats.daily)) :]
    labels = " ".join(total.day.strftime("%a")[0] for total in visible_days)
    values = [total.caffeine_mg for total in visible_days]
    sparkline = caffeine_sparkline(values)
    peak = max(values, default=0)

    body = Text()
    body.append(f"{labels}\n", style="bright_black")
    body.append(f"{sparkline}\n", style="bold cyan")
    body.append(f"Peak {peak} mg", style="bright_black")

    return Panel(
        body,
        title=f"Recent caffeine trend · {len(visible_days)} days",
        title_align="left",
        border_style="cyan",
        padding=(0, 1),
    )


def render_stats(console: Console, stats: CoffeeStats) -> None:
    """Render summary statistics and a compact caffeine trend."""
    if stats.total_coffees == 0:
        console.print(
            Text(
                f"No data in the last {stats.days} days.",
                style="dim",
            )
        )

    summary = Table(
        title=f"Coffee Statistics — last {stats.days} days",
        title_style="bold cyan",
        show_header=False,
        border_style="bright_black",
        padding=(0, 1),
    )
    summary.add_column("Metric", style="bright_black")
    summary.add_column("Value", justify="right", style="bold")
    summary.add_row("Total coffees", str(stats.total_coffees))
    summary.add_row("Total caffeine", f"{stats.total_caffeine_mg} mg")
    summary.add_row("Average per day", f"{round(stats.average_caffeine_mg)} mg")
    favorite = stats.favorite_drink.title() if stats.favorite_drink else "None"
    summary.add_row("Favorite drink", favorite)

    console.print(summary)
    console.print(_trend_panel(stats))

    daily = Table(
        title="Daily caffeine",
        title_style="bold",
        header_style="bold",
        border_style="bright_black",
    )
    daily.add_column("Date", min_width=12)
    daily.add_column("Caffeine", justify="right", min_width=10)
    daily.add_column("Load", min_width=8)

    for total in stats.daily:
        daily.add_row(
            total.day.strftime("%a  %b %d"),
            f"{total.caffeine_mg} mg",
            caffeine_bar(total.caffeine_mg) or "·",
        )

    console.print(daily)


def render_interactive_menu(console: Console) -> None:
    """Render the interactive command menu as a compact Rich panel."""
    menu = Table.grid(padding=(0, 1))
    menu.add_column(style="bold cyan", width=4)
    menu.add_column()

    menu.add_row("[1]", "☕  Record coffee")
    menu.add_row("[2]", "⚡  Developer status")
    menu.add_row("[3]", "🕒  Coffee history")
    menu.add_row("[4]", "📊  Statistics")
    menu.add_row("[5]", "×   Exit")

    console.print()
    console.print(
        Panel(
            menu,
            title="☕ Coffee-Driven Development",
            subtitle="What are we doing?",
            border_style="bright_blue",
            padding=(1, 2),
        )
    )
