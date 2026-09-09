"""Deterministic routing tests for the feature-delivery graph."""

from pathlib import Path

from ai_harness.feature_delivery.config import GraphPolicy, RetryPolicy
from ai_harness.feature_delivery.routing import (
    route_independent_review,
    route_pr_inspection,
    route_pull_request_validation,
    route_quality_gate,
    route_specification,
)
from ai_harness.feature_delivery.state import initial_state


def policy() -> GraphPolicy:
    return GraphPolicy(
        repository_root=Path("."),
        checkpoint_db=Path(".ai/graph/checkpoints.sqlite3"),
        quality_gate_commands=("pytest",),
        retries=RetryPolicy(
            specification=2,
            quality_gate=2,
            ci=2,
            review=2,
            merge_conflict=1,
        ),
        require_independent_review_model=True,
    )


def test_specification_clear_routes_to_quality_gate() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["specification_status"] = "CLEAR"

    assert route_specification(state, policy()) == "quality_gate"


def test_specification_retry_exhaustion_routes_to_human() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["specification_status"] = "MISMATCH"
    state["retries"]["specification"] = 2

    assert route_specification(state, policy()) == "human_gate"


def test_quality_gate_pass_routes_to_pr_before_pr_exists() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["quality_gate_status"] = "PASS"

    assert route_quality_gate(state, policy()) == "prepare_pull_request"


def test_quality_gate_pass_routes_to_pr_inspection_after_pr_exists() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["quality_gate_status"] = "PASS"
    state["pr_number"] = 99

    assert route_quality_gate(state, policy()) == "inspect_pr"


def test_merge_conflict_routes_to_conflict_skill() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["mergeability"] = "CONFLICT"

    assert route_pr_inspection(state, policy()) == "resolve_merge_conflict"


def test_current_head_ci_failure_routes_to_triage() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["mergeability"] = "CLEAN"
    state["head_sha"] = "abc"
    state["ci_status"] = "FAIL"
    state["ci_sha"] = "abc"

    assert route_pr_inspection(state, policy()) == "ci_triage"


def test_stale_ci_cannot_reach_review() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["mergeability"] = "CLEAN"
    state["head_sha"] = "new"
    state["ci_status"] = "PASS"
    state["ci_sha"] = "old"

    assert route_pr_inspection(state, policy()) == "inspect_pr"


def test_fresh_ci_requires_independent_review() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["mergeability"] = "CLEAN"
    state["head_sha"] = "abc"
    state["ci_status"] = "PASS"
    state["ci_sha"] = "abc"

    assert route_pr_inspection(state, policy()) == "independent_review"


def test_review_findings_route_to_feedback_validation() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["head_sha"] = "abc"
    state["review_status"] = "FINDINGS"
    state["reviewed_sha"] = "abc"

    assert route_independent_review(state, policy()) == "validate_review_feedback"


def test_stale_review_is_repeated() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["head_sha"] = "new"
    state["review_status"] = "CLEAR"
    state["reviewed_sha"] = "old"

    assert route_independent_review(state, policy()) == "independent_review"


def test_final_readiness_requires_fresh_ci_and_review() -> None:
    state = initial_state(run_id="12-test", issue_number=12)
    state["head_sha"] = "abc"
    state["mergeability"] = "CLEAN"
    state["ci_status"] = "PASS"
    state["ci_sha"] = "abc"
    state["review_status"] = "CLEAR"
    state["reviewed_sha"] = "abc"
    state["failure_reason"] = None

    assert route_pull_request_validation(state) == "ready_for_human_merge"
