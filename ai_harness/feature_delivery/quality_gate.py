"""Deterministic execution of the repository's configured local quality gate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ai_harness.feature_delivery.config import GraphPolicy
from ai_harness.feature_delivery.state import DeliveryState


def _coverage_percent(worktree: Path) -> float | None:
    report = worktree / "reports" / "coverage.json"
    if not report.is_file():
        return None

    try:
        data = json.loads(report.read_text(encoding="utf-8"))
        value = data["totals"]["percent_covered"]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None

    if isinstance(value, int | float):
        return float(value)
    return None


def run_quality_gate(
    state: DeliveryState,
    policy: GraphPolicy,
) -> dict[str, object]:
    """Run canonical commands in the selected task worktree."""
    worktree_value = state["worktree_path"]
    if worktree_value is None:
        return {
            "quality_gate_status": "FAIL",
            "failure_reason": "quality gate has no verified worktree",
            "events": ["quality_gate:FAIL:no-worktree"],
        }

    worktree = Path(worktree_value).resolve()
    if not worktree.is_dir():
        return {
            "quality_gate_status": "FAIL",
            "failure_reason": f"worktree does not exist: {worktree}",
            "events": ["quality_gate:FAIL:missing-worktree"],
        }

    for command in policy.quality_gate_commands:
        completed = subprocess.run(
            command,
            cwd=worktree,
            shell=True,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            tail = (completed.stdout + "\n" + completed.stderr)[-2000:].strip()
            return {
                "quality_gate_status": "FAIL",
                "coverage_percent": _coverage_percent(worktree),
                "failure_reason": (
                    f"quality gate command failed ({completed.returncode}): "
                    f"{command}\n{tail}"
                ),
                "events": [f"quality_gate:FAIL:{command}"],
            }

    return {
        "quality_gate_status": "PASS",
        "coverage_percent": _coverage_percent(worktree),
        "failure_reason": None,
        "events": ["quality_gate:PASS"],
    }
