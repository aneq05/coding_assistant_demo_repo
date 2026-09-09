"""External capability contracts used by the graph.

The graph owns ordering and state. Repository Skills/custom agents remain the
authority for the procedures named in these requests.
"""

from __future__ import annotations

from typing import Any

from langgraph.types import interrupt

from ai_harness.feature_delivery.state import DeliveryState

CAPABILITY_OWNERS: dict[str, str] = {
    "manage-ai-run": ".agents/skills/manage-ai-run/SKILL.md",
    "validate-scope": ".github/agents/feature-delivery.agent.md",
    "claim-issue": ".github/agents/feature-delivery.agent.md",
    "sync-repository": ".agents/skills/sync-repository/SKILL.md",
    "prepare-worktree": ".github/agents/feature-delivery.agent.md",
    "select-requirements": "spec/README.md",
    "develop-feature-tdd": ".agents/skills/develop-feature-tdd/SKILL.md",
    "validate-specification": ".agents/skills/validate-specification/SKILL.md",
    "prepare-pull-request": ".agents/skills/prepare-pull-request/SKILL.md",
    "inspect-pr": ".github/agents/pr-autopilot.agent.md",
    "ci-triage": ".github/agents/ci-triage.agent.md",
    "apply-ci-correction": ".github/agents/feature-delivery.agent.md",
    "resolve-merge-conflict": ".agents/skills/resolve-merge-conflict/SKILL.md",
    "independent-code-review": "independent reviewer model",
    "validate-review-feedback": ".agents/skills/validate-review-feedback/SKILL.md",
    "validate-pull-request": ".agents/skills/validate-pull-request/SKILL.md",
}


def compact_state(state: DeliveryState) -> dict[str, Any]:
    """Expose only resumable operational state, never full prompts or logs."""
    return {
        "run_id": state["run_id"],
        "issue_number": state["issue_number"],
        "requirements": state["requirement_ids"],
        "branch": state["branch"],
        "worktree_path": state["worktree_path"],
        "head_sha": state["head_sha"],
        "pr_number": state["pr_number"],
        "specification_status": state["specification_status"],
        "quality_gate_status": state["quality_gate_status"],
        "coverage_percent": state["coverage_percent"],
        "ci_status": state["ci_status"],
        "ci_sha": state["ci_sha"],
        "mergeability": state["mergeability"],
        "review_status": state["review_status"],
        "reviewed_sha": state["reviewed_sha"],
        "implementation_model": state["implementation_model"],
        "review_model": state["review_model"],
        "retries": dict(state["retries"]),
        "failure_reason": state["failure_reason"],
        "human_gate": state["human_gate"],
        "outcome": state["outcome"],
    }


def request_capability(
    state: DeliveryState,
    *,
    capability: str,
    action: str,
    instructions: str,
    expected_result: dict[str, str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Pause for the existing repository capability and return its result."""
    payload: dict[str, Any] = {
        "type": "repository_capability",
        "capability": capability,
        "owner": CAPABILITY_OWNERS[capability],
        "action": action,
        "instructions": instructions,
        "expected_result": expected_result,
        "graph_state": compact_state(state),
    }
    if extra:
        payload["extra"] = extra

    result = interrupt(payload)
    if not isinstance(result, dict):
        raise TypeError(f"{capability} result must be a JSON object")
    return result


def string_result(
    result: dict[str, Any],
    key: str,
    *,
    allowed: set[str] | None = None,
) -> str:
    value = result.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"capability result requires non-empty string '{key}'")
    if allowed is not None and value not in allowed:
        raise ValueError(f"unsupported {key}: {value}")
    return value


def optional_string(result: dict[str, Any], key: str) -> str | None:
    value = result.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"'{key}' must be a string or null")
    return value
