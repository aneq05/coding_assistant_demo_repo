"""Load version-controlled graph policy from the shared harness config."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RetryPolicy:
    specification: int
    quality_gate: int
    ci: int
    review: int
    merge_conflict: int


@dataclass(frozen=True)
class GraphPolicy:
    repository_root: Path
    checkpoint_db: Path
    quality_gate_commands: tuple[str, ...]
    retries: RetryPolicy
    require_independent_review_model: bool


def _require_dict(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _require_positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


def load_graph_policy(repository_root: Path | None = None) -> GraphPolicy:
    """Load graph settings without introducing a second policy source."""
    root = (repository_root or Path.cwd()).resolve()
    config_path = root / ".ai" / "harness.config.json"
    data = _require_dict(json.loads(config_path.read_text(encoding="utf-8")), "config")
    paths = _require_dict(data.get("paths"), "paths")
    graph = _require_dict(data.get("graph"), "graph")
    retries = _require_dict(graph.get("max_retries"), "graph.max_retries")

    commands = data.get("quality_gate_commands")
    if not isinstance(commands, list) or not all(
        isinstance(command, str) and command.strip() for command in commands
    ):
        raise ValueError("quality_gate_commands must be a non-empty string list")

    checkpoint_value = paths.get("graph_checkpoints")
    if not isinstance(checkpoint_value, str) or not checkpoint_value:
        raise ValueError("paths.graph_checkpoints must be configured")

    require_independent = graph.get("require_independent_review_model")
    if not isinstance(require_independent, bool):
        raise ValueError("graph.require_independent_review_model must be boolean")

    return GraphPolicy(
        repository_root=root,
        checkpoint_db=root / checkpoint_value,
        quality_gate_commands=tuple(commands),
        retries=RetryPolicy(
            specification=_require_positive_int(
                retries.get("specification"), "max_retries.specification"
            ),
            quality_gate=_require_positive_int(
                retries.get("quality_gate"), "max_retries.quality_gate"
            ),
            ci=_require_positive_int(retries.get("ci"), "max_retries.ci"),
            review=_require_positive_int(retries.get("review"), "max_retries.review"),
            merge_conflict=_require_positive_int(
                retries.get("merge_conflict"), "max_retries.merge_conflict"
            ),
        ),
        require_independent_review_model=require_independent,
    )
