"""State freshness semantics for graph evidence."""

from ai_harness.feature_delivery.state import (
    ci_is_fresh,
    initial_state,
    invalidate_head_bound_evidence,
    review_is_fresh,
)


def test_head_change_invalidates_ci_and_review() -> None:
    state = initial_state(run_id="42-risk", issue_number=42)
    state["head_sha"] = "old"
    state["ci_status"] = "PASS"
    state["ci_sha"] = "old"
    state["review_status"] = "CLEAR"
    state["reviewed_sha"] = "old"
    state["review_model"] = "reviewer"

    updates = invalidate_head_bound_evidence(state, new_head_sha="new")

    assert updates["ci_status"] == "PENDING"
    assert updates["ci_sha"] is None
    assert updates["review_status"] == "PENDING"
    assert updates["reviewed_sha"] is None


def test_freshness_requires_exact_head_sha() -> None:
    state = initial_state(run_id="42-risk", issue_number=42)
    state["head_sha"] = "head"
    state["ci_status"] = "PASS"
    state["ci_sha"] = "head"
    state["review_status"] = "CLEAR"
    state["reviewed_sha"] = "head"

    assert ci_is_fresh(state)
    assert review_is_fresh(state)
