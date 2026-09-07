"""Tests for local Git activity reporting."""

from datetime import UTC, datetime, timedelta, timezone

import pytest

from cdd.domain import git_activity_level
from cdd.git_activity import GitActivity, get_git_activity


@pytest.mark.parametrize(
    ("commits", "expected"),
    [
        (0, "QUIET"),
        (1, "ACTIVE"),
        (2, "ACTIVE"),
        (3, "SHIPPING"),
        (5, "SHIPPING"),
        (6, "DEEP WORK"),
    ],
)
def test_git_activity_level_uses_commit_count_boundaries(
    commits: int,
    expected: str,
) -> None:
    assert git_activity_level(commits) == expected


def test_get_git_activity_reports_today_and_latest_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=timezone(timedelta(hours=2)))

    def fake_run(*args: object, **kwargs: object) -> object:
        class Result:
            stdout = "2026-09-07T09:00:00+00:00\n2026-09-07T10:30:00+00:00\n"

        return Result()

    monkeypatch.setattr("cdd.git_activity.subprocess.run", fake_run)

    assert get_git_activity(now=now) == GitActivity(
        commits_today=2,
        latest_commit=datetime(2026, 9, 7, 12, 30, tzinfo=now.tzinfo),
    )


def test_get_git_activity_is_empty_outside_a_git_repository(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run(*args: object, **kwargs: object) -> object:
        raise OSError("not a repository")

    monkeypatch.setattr("cdd.git_activity.subprocess.run", fake_run)

    assert get_git_activity(now=datetime(2026, 9, 7, tzinfo=UTC)) == GitActivity(
        commits_today=0,
        latest_commit=None,
    )
