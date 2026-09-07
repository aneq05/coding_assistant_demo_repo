"""Read deterministic local Git activity for the current day."""

import subprocess
from dataclasses import dataclass
from datetime import datetime, time

from cdd.domain import LocalTimeConverter, git_activity_level


@dataclass(frozen=True)
class GitActivity:
    """Local Git activity for one local calendar day."""

    commits_today: int
    latest_commit: datetime | None

    @property
    def activity_level(self) -> str:
        """Return the level derived only from today's commit count."""
        return git_activity_level(self.commits_today)


def get_git_activity(
    *,
    now: datetime,
    to_local: LocalTimeConverter | None = None,
) -> GitActivity:
    """Return today's local Git activity, or an empty result outside Git."""
    local_now = _localize(now, to_local)
    start_of_day = datetime.combine(
        local_now.date(), time.min, tzinfo=local_now.tzinfo
    )
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--format=%cI",
                f"--since={start_of_day.isoformat()}",
                f"--until={local_now.isoformat()}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return GitActivity(commits_today=0, latest_commit=None)

    commits = [
        datetime.fromisoformat(line).astimezone(local_now.tzinfo)
        for line in result.stdout.splitlines()
        if line
    ]
    return GitActivity(
        commits_today=len(commits),
        latest_commit=max(commits) if commits else None,
    )


def _localize(
    timestamp: datetime,
    to_local: LocalTimeConverter | None,
) -> datetime:
    localized = to_local(timestamp) if to_local is not None else timestamp.astimezone()
    if localized.tzinfo is None or localized.utcoffset() is None:
        raise ValueError("local time must be timezone-aware")
    return localized
