"""Typed state for the explicit feature-delivery graph."""

from __future__ import annotations

import operator
from typing import Annotated, Literal, TypedDict


ClearStatus = Literal[
    "CLEAR",
    "MISMATCH",
    "UNKNOWN",
    "HUMAN_REVIEW_REQUIRED",
]
CheckStatus = Literal["PENDING", "PASS", "FAIL", "UNKNOWN"]
Mergeability = Literal["UNKNOWN", "CLEAN", "CONFLICT"]
ReviewStatus = Literal["PENDING", "CLEAR", "FINDINGS", "UNKNOWN"]
RunOutcome = Literal[
    "READY_FOR_HUMAN_MERGE",
    "HUMAN_REVIEW_REQUIRED",
    "ABORTED",
]
HumanDecision = Literal["APPROVE", "BLOCK", "ABORT"]


class RetryState(TypedDict):
    specification: int
    quality_gate: int
    ci: int
    review: int
    merge_conflict: int


class DeliveryState(TypedDict):
    run_id: str
    issue_number: int

    requirement_ids: list[str]

    branch: str | None
    worktree_path: str | None
    head_sha: str | None

    implementation_model: str | None
    review_model: str | None

    specification_status: ClearStatus | None

    quality_gate_status: CheckStatus | None
    coverage_percent: float | None

    pr_number: int | None

    ci_status: CheckStatus | None
    ci_sha: str | None

    mergeability: Mergeability

    review_status: ReviewStatus
    reviewed_sha: str | None
    actionable_review_findings: bool

    retries: RetryState

    ci_diagnosis: str | None
    failure_reason: str | None

    human_gate: str | None
    human_resume_target: str | None
    human_decision: HumanDecision | None

    checkpoint_next: str | None
    checkpoint_note: str | None

    outcome: RunOutcome | None

    events: Annotated[list[str], operator.add]


def initial_state(
    *,
    run_id: str,
    issue_number: int,
    implementation_model: str | None = None,
) -> DeliveryState:
    """Build a new graph state without inventing repository evidence."""
    return DeliveryState(
        run_id=run_id,
        issue_number=issue_number,
        requirement_ids=[],
        branch=None,
        worktree_path=None,
        head_sha=None,
        implementation_model=implementation_model,
        review_model=None,
        specification_status=None,
        quality_gate_status=None,
        coverage_percent=None,
        pr_number=None,
        ci_status=None,
        ci_sha=None,
        mergeability="UNKNOWN",
        review_status="PENDING",
        reviewed_sha=None,
        actionable_review_findings=False,
        retries=RetryState(
            specification=0,
            quality_gate=0,
            ci=0,
            review=0,
            merge_conflict=0,
        ),
        ci_diagnosis=None,
        failure_reason=None,
        human_gate=None,
        human_resume_target=None,
        human_decision=None,
        checkpoint_next=None,
        checkpoint_note=None,
        outcome=None,
        events=[],
    )


def ci_is_fresh(state: DeliveryState) -> bool:
    """Return true only for successful CI evidence tied to the current HEAD."""
    return (
        state["ci_status"] == "PASS"
        and state["head_sha"] is not None
        and state["ci_sha"] == state["head_sha"]
    )


def review_is_fresh(state: DeliveryState) -> bool:
    """Return true only for CLEAR review evidence tied to the current HEAD."""
    return (
        state["review_status"] == "CLEAR"
        and state["head_sha"] is not None
        and state["reviewed_sha"] == state["head_sha"]
    )


def invalidate_head_bound_evidence(
    state: DeliveryState,
    *,
    new_head_sha: str | None,
) -> dict[str, object]:
    """Invalidate CI/review evidence whenever the PR HEAD changes."""
    if new_head_sha is None or new_head_sha == state["head_sha"]:
        return {"head_sha": new_head_sha}

    return {
        "head_sha": new_head_sha,
        "ci_status": "PENDING",
        "ci_sha": None,
        "mergeability": "UNKNOWN",
        "review_status": "PENDING",
        "reviewed_sha": None,
        "review_model": None,
        "actionable_review_findings": False,
    }
