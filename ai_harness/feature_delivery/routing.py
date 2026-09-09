"""Pure deterministic routing decisions for feature delivery."""

from __future__ import annotations

from ai_harness.feature_delivery.config import GraphPolicy
from ai_harness.feature_delivery.state import (
    DeliveryState,
    ci_is_fresh,
    review_is_fresh,
)


def route_specification(state: DeliveryState, policy: GraphPolicy) -> str:
    status = state["specification_status"]
    if status == "CLEAR":
        return "quality_gate"
    if status == "MISMATCH":
        if state["retries"]["specification"] >= policy.retries.specification:
            return "human_gate"
        return "repair_specification"
    return "human_gate"


def route_quality_gate(state: DeliveryState, policy: GraphPolicy) -> str:
    if state["quality_gate_status"] == "PASS":
        return "prepare_pull_request" if state["pr_number"] is None else "inspect_pr"
    if state["retries"]["quality_gate"] >= policy.retries.quality_gate:
        return "human_gate"
    return "repair_quality_gate"


def route_pr_inspection(state: DeliveryState, policy: GraphPolicy) -> str:
    if state["mergeability"] == "CONFLICT":
        if state["retries"]["merge_conflict"] >= policy.retries.merge_conflict:
            return "human_gate"
        return "resolve_merge_conflict"

    if state["mergeability"] == "UNKNOWN":
        return "human_gate"

    if not ci_is_fresh(state):
        # Evidence for another SHA is stale, not a current failure.
        if state["ci_sha"] != state["head_sha"]:
            return "inspect_pr"
        if state["ci_status"] == "PENDING":
            return "inspect_pr"
        if state["ci_status"] == "FAIL":
            if state["retries"]["ci"] >= policy.retries.ci:
                return "human_gate"
            return "ci_triage"
        return "human_gate"

    if review_is_fresh(state):
        return "validate_pull_request"

    return "independent_review"


def route_independent_review(state: DeliveryState, policy: GraphPolicy) -> str:
    if state["review_status"] == "CLEAR":
        if not review_is_fresh(state):
            return "independent_review"
        return "validate_pull_request"

    if state["review_status"] == "FINDINGS":
        if state["retries"]["review"] >= policy.retries.review:
            return "human_gate"
        return "validate_review_feedback"

    if state["review_status"] == "PENDING":
        return "independent_review"

    return "human_gate"


def route_review_feedback(state: DeliveryState) -> str:
    if state["failure_reason"] is not None:
        return "human_gate"
    if state["actionable_review_findings"]:
        return "quality_gate"
    return "validate_pull_request"


def route_pull_request_validation(state: DeliveryState) -> str:
    if state["failure_reason"] is not None:
        return "human_gate"
    if state["mergeability"] != "CLEAN":
        return "inspect_pr"
    if not ci_is_fresh(state):
        return "inspect_pr"
    if not review_is_fresh(state):
        return "independent_review"
    return "ready_for_human_merge"


def route_human_decision(state: DeliveryState) -> str:
    if state["human_decision"] == "APPROVE":
        return state["human_resume_target"] or "blocked"
    if state["human_decision"] == "ABORT":
        return "aborted"
    return "blocked"


def route_checkpoint(state: DeliveryState) -> str:
    return state["checkpoint_next"] or "blocked"
