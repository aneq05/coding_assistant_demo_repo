"""LangGraph orchestration for repository feature delivery.

The graph deliberately does not duplicate Skills. External action nodes pause
with a structured capability request; the Feature Delivery Agent (or another
caller) executes the named existing capability and resumes the same graph run.
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from ai_harness.feature_delivery.capabilities import (
    optional_string,
    request_capability,
    string_result,
)
from ai_harness.feature_delivery.config import GraphPolicy, load_graph_policy
from ai_harness.feature_delivery.quality_gate import run_quality_gate
from ai_harness.feature_delivery.routing import (
    route_checkpoint,
    route_human_decision,
    route_independent_review,
    route_pr_inspection,
    route_pull_request_validation,
    route_quality_gate,
    route_review_feedback,
    route_specification,
)
from ai_harness.feature_delivery.state import (
    DeliveryState,
    invalidate_head_bound_evidence,
)


def _retry(state: DeliveryState, key: str) -> dict[str, int]:
    retries = dict(state["retries"])
    retries[key] += 1
    return retries


def _human(
    *,
    reason: str,
    resume_target: str,
    gate: str = "architecture-decision",
) -> dict[str, object]:
    return {
        "human_gate": gate,
        "human_resume_target": resume_target,
        "failure_reason": reason,
        "events": [f"human_gate:{gate}:{reason}"],
    }


def build_delivery_graph(
    *,
    policy: GraphPolicy | None = None,
    checkpointer: Any | None = None,
) -> Any:
    """Compile the explicit delivery graph."""
    graph_policy = policy or load_graph_policy()
    builder = StateGraph(DeliveryState)

    def start_run(state: DeliveryState) -> dict[str, object]:
        request_capability(
            state,
            capability="manage-ai-run",
            action="start-or-resume",
            instructions=(
                "Create or reconcile the matching .ai/runs state using the "
                "existing manage-ai-run Skill. The run file is canonical "
                "operational context; do not copy graph checkpoints into it."
            ),
            expected_result={"status": "ACTIVE | BLOCKED", "detail": "string"},
        )
        return {"events": ["run_state:started-or-resumed"]}

    def validate_scope(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="validate-scope",
            action="validate-issue-scope",
            instructions=(
                "Inspect the Issue and repository evidence. Do not expand product "
                "requirements. Return CLEAR only when the Issue is adequately scoped."
            ),
            expected_result={
                "status": "CLEAR | HUMAN_REVIEW_REQUIRED",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "HUMAN_REVIEW_REQUIRED"}
        )
        if status == "CLEAR":
            return {"failure_reason": None, "events": ["scope:CLEAR"]}
        return _human(
            reason=optional_string(result, "reason") or "Issue scope needs human input",
            resume_target="validate_scope",
        )

    def claim_issue(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="claim-issue",
            action="claim-target-issue",
            instructions=(
                "Apply the existing conservative ai-in-progress ownership rules. "
                "Resume only matching ownership; never steal or overwrite a claim."
            ),
            expected_result={
                "status": "ACQUIRED | RESUMED | HUMAN_REVIEW_REQUIRED",
                "reason": "string or null",
            },
        )
        status = string_result(
            result,
            "status",
            allowed={"ACQUIRED", "RESUMED", "HUMAN_REVIEW_REQUIRED"},
        )
        if status == "HUMAN_REVIEW_REQUIRED":
            return _human(
                reason=optional_string(result, "reason") or "Issue claim is ambiguous",
                resume_target="claim_issue",
                gate="claim-ownership-ambiguity",
            )
        return {
            "checkpoint_next": "sync_repository",
            "checkpoint_note": f"Issue claim {status.lower()}",
            "failure_reason": None,
            "events": [f"claim:{status}"],
        }

    def sync_repository(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="sync-repository",
            action="verify-fresh-repository-state",
            instructions="Use the existing Skill; preserve unrelated user work.",
            expected_result={
                "status": "CLEAR | HUMAN_REVIEW_REQUIRED",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "CLEAR":
            return _human(
                reason=optional_string(result, "reason") or "Repository state is unsafe",
                resume_target="sync_repository",
            )
        return {"failure_reason": None, "events": ["repository_sync:CLEAR"]}

    def prepare_worktree(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="prepare-worktree",
            action="prepare-isolated-task-worktree",
            instructions=(
                "Use Feature Delivery Agent worktree safety rules. Verify branch, "
                "base ancestry, path identity and clean task state."
            ),
            expected_result={
                "status": "CLEAR | HUMAN_REVIEW_REQUIRED",
                "branch": "string",
                "worktree_path": "string",
                "head_sha": "string",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "CLEAR":
            return _human(
                reason=optional_string(result, "reason") or "Worktree setup is ambiguous",
                resume_target="prepare_worktree",
            )
        return {
            "branch": string_result(result, "branch"),
            "worktree_path": string_result(result, "worktree_path"),
            "head_sha": string_result(result, "head_sha"),
            "failure_reason": None,
            "events": ["worktree:CLEAR"],
        }

    def select_requirements(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="select-requirements",
            action="select-relevant-specification",
            instructions=(
                "Start from configured spec/README.md and load only task-relevant "
                "requirements. Do not load the entire specification unnecessarily."
            ),
            expected_result={
                "status": "CLEAR | HUMAN_REVIEW_REQUIRED",
                "requirement_ids": "list[str]",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "CLEAR":
            return _human(
                reason=optional_string(result, "reason")
                or "Relevant requirements are ambiguous",
                resume_target="select_requirements",
            )
        raw_ids = result.get("requirement_ids")
        if not isinstance(raw_ids, list) or not all(
            isinstance(value, str) for value in raw_ids
        ):
            return _human(
                reason="Requirement selection did not return requirement_ids",
                resume_target="select_requirements",
            )
        return {
            "requirement_ids": list(raw_ids),
            "failure_reason": None,
            "events": ["requirements:selected"],
        }

    def implement(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="develop-feature-tdd",
            action="implement-scoped-feature",
            instructions=(
                "Use the existing TDD Skill for scoped behavioral work and preserve "
                "the selected specification requirements."
            ),
            expected_result={
                "status": "COMPLETE | HUMAN_REVIEW_REQUIRED",
                "implementation_model": "string",
                "head_sha": "string or null",
                "reason": "string or null",
            },
            extra={"requirement_ids": state["requirement_ids"]},
        )
        status = string_result(
            result, "status", allowed={"COMPLETE", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "COMPLETE":
            return _human(
                reason=optional_string(result, "reason")
                or "Implementation requires a human decision",
                resume_target="implement",
            )

        model = string_result(result, "implementation_model")
        head = optional_string(result, "head_sha")
        updates = invalidate_head_bound_evidence(state, new_head_sha=head)
        updates.update(
            {
                "implementation_model": model,
                "checkpoint_next": "validate_specification",
                "checkpoint_note": "Implementation completed; validate specification",
                "failure_reason": None,
                "events": ["implementation:COMPLETE"],
            }
        )
        return updates

    def validate_specification(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="validate-specification",
            action="validate-current-change",
            instructions=(
                "Validate only relevant requirements against implementation, tests "
                "and the current change. Do not rewrite spec to excuse code."
            ),
            expected_result={
                "status": "CLEAR | MISMATCH | UNKNOWN | HUMAN_REVIEW_REQUIRED",
                "reason": "string or null",
            },
            extra={"requirement_ids": state["requirement_ids"]},
        )
        status = string_result(
            result,
            "status",
            allowed={"CLEAR", "MISMATCH", "UNKNOWN", "HUMAN_REVIEW_REQUIRED"},
        )
        updates: dict[str, object] = {
            "specification_status": status,
            "failure_reason": optional_string(result, "reason"),
            "events": [f"specification:{status}"],
        }
        if status in {"UNKNOWN", "HUMAN_REVIEW_REQUIRED"}:
            updates.update(
                _human(
                    reason=optional_string(result, "reason")
                    or "Specification conformance is unresolved",
                    resume_target="validate_specification",
                )
            )
        return updates

    def repair_specification(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="develop-feature-tdd",
            action="correct-specification-mismatch",
            instructions=(
                "Correct implementation/tests for the validated mismatch. Do not "
                "weaken or silently edit normative specification."
            ),
            expected_result={
                "status": "COMPLETE | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string or null",
                "reason": "string or null",
            },
            extra={"requirement_ids": state["requirement_ids"]},
        )
        retries = _retry(state, "specification")
        if string_result(
            result, "status", allowed={"COMPLETE", "HUMAN_REVIEW_REQUIRED"}
        ) != "COMPLETE":
            updates = _human(
                reason=optional_string(result, "reason")
                or "Specification mismatch correction needs human input",
                resume_target="repair_specification",
            )
            updates["retries"] = retries
            return updates

        updates = invalidate_head_bound_evidence(
            state, new_head_sha=optional_string(result, "head_sha")
        )
        updates.update(
            {
                "retries": retries,
                "specification_status": None,
                "failure_reason": None,
                "events": ["specification:repaired"],
            }
        )
        return updates

    def quality_gate(state: DeliveryState) -> dict[str, object]:
        return run_quality_gate(state, graph_policy)

    def repair_quality_gate(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="develop-feature-tdd",
            action="repair-local-quality-gate",
            instructions=(
                "Diagnose the failing local gate and apply the smallest justified "
                "correction without weakening tests, coverage, linting or typing."
            ),
            expected_result={
                "status": "COMPLETE | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string or null",
                "reason": "string or null",
            },
            extra={"failure_reason": state["failure_reason"]},
        )
        retries = _retry(state, "quality_gate")
        if string_result(
            result, "status", allowed={"COMPLETE", "HUMAN_REVIEW_REQUIRED"}
        ) != "COMPLETE":
            updates = _human(
                reason=optional_string(result, "reason")
                or "Local quality-gate correction needs human input",
                resume_target="repair_quality_gate",
            )
            updates["retries"] = retries
            return updates
        updates = invalidate_head_bound_evidence(
            state, new_head_sha=optional_string(result, "head_sha")
        )
        updates.update(
            {
                "retries": retries,
                "quality_gate_status": None,
                "failure_reason": None,
                "events": ["quality_gate:repaired"],
            }
        )
        return updates

    def prepare_pull_request(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="prepare-pull-request",
            action="deliver-review-ready-pr",
            instructions=(
                "Use the existing Skill and preserve human-controlled final merge. "
                "Do not auto-merge."
            ),
            expected_result={
                "status": "COMPLETE | HUMAN_REVIEW_REQUIRED",
                "pr_number": "integer",
                "head_sha": "string",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"COMPLETE", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "COMPLETE":
            return _human(
                reason=optional_string(result, "reason") or "PR delivery needs human input",
                resume_target="prepare_pull_request",
            )

        pr_number = result.get("pr_number")
        if isinstance(pr_number, bool) or not isinstance(pr_number, int):
            return _human(
                reason="PR delivery did not provide a valid pr_number",
                resume_target="prepare_pull_request",
            )
        head = string_result(result, "head_sha")
        updates = invalidate_head_bound_evidence(state, new_head_sha=head)
        updates.update(
            {
                "pr_number": pr_number,
                "checkpoint_next": "inspect_pr",
                "checkpoint_note": f"PR #{pr_number} created; inspect current HEAD",
                "failure_reason": None,
                "events": [f"pull_request:#{pr_number}"],
            }
        )
        return updates

    def inspect_pr(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="inspect-pr",
            action="inspect-current-pr-state",
            instructions=(
                "Use PR Autopilot only for evidence/diagnosis. Return current HEAD, "
                "mergeability and current-HEAD CI evidence; do not merge."
            ),
            expected_result={
                "status": "CLEAR | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string",
                "mergeability": "CLEAN | CONFLICT | UNKNOWN",
                "ci_status": "PENDING | PASS | FAIL | UNKNOWN",
                "ci_sha": "string or null",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "CLEAR":
            return _human(
                reason=optional_string(result, "reason") or "PR state is ambiguous",
                resume_target="inspect_pr",
            )

        head = string_result(result, "head_sha")
        updates = invalidate_head_bound_evidence(state, new_head_sha=head)
        updates.update(
            {
                "mergeability": string_result(
                    result, "mergeability", allowed={"CLEAN", "CONFLICT", "UNKNOWN"}
                ),
                "ci_status": string_result(
                    result, "ci_status", allowed={"PENDING", "PASS", "FAIL", "UNKNOWN"}
                ),
                "ci_sha": optional_string(result, "ci_sha"),
                "failure_reason": optional_string(result, "reason"),
                "events": ["pr:inspected"],
            }
        )
        return updates

    def ci_triage(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="ci-triage",
            action="diagnose-current-head-ci-failure",
            instructions=(
                "Diagnose the current-HEAD failure first. Do not weaken safeguards."
            ),
            expected_result={
                "status": "DIAGNOSED | HUMAN_REVIEW_REQUIRED",
                "classification": "string",
                "correction": "string or null",
                "reason": "string or null",
            },
        )
        retries = _retry(state, "ci")
        status = string_result(
            result, "status", allowed={"DIAGNOSED", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "DIAGNOSED":
            updates = _human(
                reason=optional_string(result, "reason") or "CI diagnosis is ambiguous",
                resume_target="ci_triage",
            )
            updates["retries"] = retries
            return updates

        return {
            "retries": retries,
            "ci_diagnosis": (
                f"{string_result(result, 'classification')}: "
                f"{optional_string(result, 'correction') or 'no correction proposed'}"
            ),
            "failure_reason": None,
            "events": ["ci:diagnosed"],
        }

    def apply_ci_correction(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="apply-ci-correction",
            action="apply-diagnosed-ci-correction",
            instructions=(
                "Apply only the justified diagnosed correction on the existing PR "
                "branch, validate locally and push without force. Stop for product, "
                "architecture, dependency or permission ambiguity."
            ),
            expected_result={
                "status": "COMPLETE | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string",
                "reason": "string or null",
            },
            extra={"diagnosis": state["ci_diagnosis"]},
        )
        status = string_result(
            result, "status", allowed={"COMPLETE", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "COMPLETE":
            return _human(
                reason=optional_string(result, "reason")
                or "CI correction requires human input",
                resume_target="apply_ci_correction",
            )
        updates = invalidate_head_bound_evidence(
            state, new_head_sha=string_result(result, "head_sha")
        )
        updates.update(
            {
                "ci_diagnosis": None,
                "quality_gate_status": None,
                "failure_reason": None,
                "events": ["ci:correction-applied"],
            }
        )
        return updates

    def resolve_merge_conflict(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="resolve-merge-conflict",
            action="resolve-current-pr-conflict",
            instructions=(
                "Use the existing Skill. Automatically resolve only clearly "
                "TRIVIAL/COMPOSABLE conflicts; escalate semantic/architectural intent."
            ),
            expected_result={
                "status": "RESOLVED | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string or null",
                "reason": "string or null",
            },
        )
        retries = _retry(state, "merge_conflict")
        status = string_result(
            result, "status", allowed={"RESOLVED", "HUMAN_REVIEW_REQUIRED"}
        )
        if status != "RESOLVED":
            updates = _human(
                reason=optional_string(result, "reason")
                or "Merge conflict requires human resolution",
                resume_target="resolve_merge_conflict",
            )
            updates["retries"] = retries
            return updates

        updates = invalidate_head_bound_evidence(
            state, new_head_sha=optional_string(result, "head_sha")
        )
        updates.update(
            {
                "retries": retries,
                "mergeability": "UNKNOWN",
                "quality_gate_status": None,
                "checkpoint_next": "quality_gate",
                "checkpoint_note": "Merge conflict resolved; all HEAD-bound evidence invalidated",
                "failure_reason": None,
                "events": ["merge_conflict:RESOLVED"],
            }
        )
        return updates

    def independent_review(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="independent-code-review",
            action="review-current-head",
            instructions=(
                "Perform an independent code review of the exact current HEAD. "
                "The reviewer model must differ from the implementation model."
            ),
            expected_result={
                "status": "CLEAR | FINDINGS | HUMAN_REVIEW_REQUIRED",
                "review_model": "string",
                "reviewed_sha": "string",
                "reason": "string or null",
            },
            extra={
                "implementation_model": state["implementation_model"],
                "required_head_sha": state["head_sha"],
                "model_must_differ": graph_policy.require_independent_review_model,
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "FINDINGS", "HUMAN_REVIEW_REQUIRED"}
        )
        review_model = string_result(result, "review_model")
        reviewed_sha = string_result(result, "reviewed_sha")

        if (
            graph_policy.require_independent_review_model
            and state["implementation_model"] is not None
            and review_model == state["implementation_model"]
        ):
            return _human(
                reason="Independent review used the implementation model",
                resume_target="independent_review",
            )

        if reviewed_sha != state["head_sha"]:
            return {
                "review_model": review_model,
                "review_status": "PENDING",
                "reviewed_sha": reviewed_sha,
                "failure_reason": "Review evidence is stale for the current HEAD",
                "events": ["review:STALE"],
            }

        if status == "HUMAN_REVIEW_REQUIRED":
            updates = _human(
                reason=optional_string(result, "reason") or "Review needs human input",
                resume_target="independent_review",
            )
            updates.update(
                {
                    "review_model": review_model,
                    "reviewed_sha": reviewed_sha,
                    "review_status": "UNKNOWN",
                }
            )
            return updates

        return {
            "review_model": review_model,
            "reviewed_sha": reviewed_sha,
            "review_status": "CLEAR" if status == "CLEAR" else "FINDINGS",
            "actionable_review_findings": status == "FINDINGS",
            "failure_reason": optional_string(result, "reason"),
            "events": [f"review:{status}:{review_model}"],
        }

    def validate_review_feedback(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="validate-review-feedback",
            action="validate-and-process-review-findings",
            instructions=(
                "Treat reviewer findings as evidence, not authority. Apply only "
                "justified corrections using the existing Skill."
            ),
            expected_result={
                "status": "NO_CHANGE | CORRECTED | HUMAN_REVIEW_REQUIRED",
                "head_sha": "string or null",
                "reason": "string or null",
            },
        )
        retries = _retry(state, "review")
        status = string_result(
            result,
            "status",
            allowed={"NO_CHANGE", "CORRECTED", "HUMAN_REVIEW_REQUIRED"},
        )
        if status == "HUMAN_REVIEW_REQUIRED":
            updates = _human(
                reason=optional_string(result, "reason")
                or "Review feedback requires human decision",
                resume_target="validate_review_feedback",
            )
            updates["retries"] = retries
            return updates

        if status == "CORRECTED":
            updates = invalidate_head_bound_evidence(
                state, new_head_sha=optional_string(result, "head_sha")
            )
            updates.update(
                {
                    "retries": retries,
                    "quality_gate_status": None,
                    "failure_reason": None,
                    "actionable_review_findings": True,
                    "checkpoint_next": "quality_gate",
                    "checkpoint_note": "Review correction changed HEAD; CI/review freshness invalidated",
                    "events": ["review_feedback:CORRECTED"],
                }
            )
            return updates

        return {
            "retries": retries,
            "actionable_review_findings": False,
            "review_status": "CLEAR",
            "failure_reason": None,
            "events": ["review_feedback:NO_CHANGE"],
        }

    def validate_pull_request(state: DeliveryState) -> dict[str, object]:
        result = request_capability(
            state,
            capability="validate-pull-request",
            action="final-current-head-readiness-gate",
            instructions=(
                "Validate mergeability, exact-current-HEAD CI and review freshness. "
                "CLEAR is readiness evidence, never authorization to merge."
            ),
            expected_result={
                "status": "CLEAR | BLOCKED | NEEDS_ATTENTION",
                "reason": "string or null",
            },
        )
        status = string_result(
            result, "status", allowed={"CLEAR", "BLOCKED", "NEEDS_ATTENTION"}
        )
        if status != "CLEAR":
            return _human(
                reason=optional_string(result, "reason")
                or f"Final PR validation returned {status}",
                resume_target="validate_pull_request",
            )
        return {"failure_reason": None, "events": ["pull_request_validation:CLEAR"]}

    def checkpoint_run(state: DeliveryState) -> dict[str, object]:
        request_capability(
            state,
            capability="manage-ai-run",
            action="update-progress",
            instructions=(
                "Update the existing .ai/runs record with only compact evidence-backed "
                "progress and next action. Do not copy graph checkpoint data or logs."
            ),
            expected_result={"status": "ACTIVE | BLOCKED | COMPLETE"},
            extra={"checkpoint_note": state["checkpoint_note"]},
        )
        return {"events": ["run_state:checkpointed"]}

    def human_gate(state: DeliveryState) -> dict[str, object]:
        answer = interrupt(
            {
                "type": "human_gate",
                "gate": state["human_gate"] or "architecture-decision",
                "reason": state["failure_reason"] or "Human decision required",
                "resume_target": state["human_resume_target"],
                "allowed_decisions": ["APPROVE", "BLOCK", "ABORT"],
            }
        )
        if not isinstance(answer, dict):
            raise ValueError("human gate response must be a JSON object")
        decision = answer.get("decision")
        if decision not in {"APPROVE", "BLOCK", "ABORT"}:
            raise ValueError("human decision must be APPROVE, BLOCK, or ABORT")
        return {
            "human_decision": decision,
            "human_gate": None if decision == "APPROVE" else state["human_gate"],
            "failure_reason": None if decision == "APPROVE" else state["failure_reason"],
            "events": [f"human_decision:{decision}"],
        }

    def ready_for_human_merge(state: DeliveryState) -> dict[str, object]:
        return {
            "outcome": "READY_FOR_HUMAN_MERGE",
            "checkpoint_next": "terminal_checkpoint",
            "checkpoint_note": "All graph gates clear; final merge remains human-controlled",
            "failure_reason": None,
            "events": ["outcome:READY_FOR_HUMAN_MERGE"],
        }

    def blocked(state: DeliveryState) -> dict[str, object]:
        return {
            "outcome": "HUMAN_REVIEW_REQUIRED",
            "checkpoint_next": "terminal_checkpoint",
            "checkpoint_note": state["failure_reason"] or "Run blocked for human review",
            "events": ["outcome:HUMAN_REVIEW_REQUIRED"],
        }

    def aborted(state: DeliveryState) -> dict[str, object]:
        return {
            "outcome": "ABORTED",
            "checkpoint_next": "terminal_checkpoint",
            "checkpoint_note": "Run aborted by human decision",
            "events": ["outcome:ABORTED"],
        }

    def terminal_checkpoint(state: DeliveryState) -> dict[str, object]:
        request_capability(
            state,
            capability="manage-ai-run",
            action="finalize-or-block-run",
            instructions=(
                "Reconcile .ai/runs with current repository/GitHub evidence. Mark "
                "COMPLETE only for READY_FOR_HUMAN_MERGE or ABORTED; otherwise BLOCKED."
            ),
            expected_result={"status": "COMPLETE | BLOCKED"},
            extra={"outcome": state["outcome"]},
        )
        return {"events": ["run_state:terminal-checkpoint"]}

    # Nodes
    builder.add_node("start_run", start_run)
    builder.add_node("validate_scope", validate_scope)
    builder.add_node("claim_issue", claim_issue)
    builder.add_node("sync_repository", sync_repository)
    builder.add_node("prepare_worktree", prepare_worktree)
    builder.add_node("select_requirements", select_requirements)
    builder.add_node("implement", implement)
    builder.add_node("validate_specification", validate_specification)
    builder.add_node("repair_specification", repair_specification)
    builder.add_node("quality_gate", quality_gate)
    builder.add_node("repair_quality_gate", repair_quality_gate)
    builder.add_node("prepare_pull_request", prepare_pull_request)
    builder.add_node("inspect_pr", inspect_pr)
    builder.add_node("ci_triage", ci_triage)
    builder.add_node("apply_ci_correction", apply_ci_correction)
    builder.add_node("resolve_merge_conflict", resolve_merge_conflict)
    builder.add_node("independent_review", independent_review)
    builder.add_node("validate_review_feedback", validate_review_feedback)
    builder.add_node("validate_pull_request", validate_pull_request)
    builder.add_node("checkpoint_run", checkpoint_run)
    builder.add_node("human_gate", human_gate)
    builder.add_node("ready_for_human_merge", ready_for_human_merge)
    builder.add_node("blocked", blocked)
    builder.add_node("aborted", aborted)
    builder.add_node("terminal_checkpoint", terminal_checkpoint)

    # Main path
    builder.add_edge(START, "start_run")
    builder.add_edge("start_run", "validate_scope")
    builder.add_conditional_edges(
        "validate_scope",
        lambda state: "human_gate" if state["human_gate"] else "claim_issue",
    )
    builder.add_conditional_edges(
        "claim_issue",
        lambda state: "human_gate" if state["human_gate"] else "checkpoint_run",
    )
    builder.add_conditional_edges(
        "checkpoint_run",
        route_checkpoint,
        {
            "sync_repository": "sync_repository",
            "validate_specification": "validate_specification",
            "inspect_pr": "inspect_pr",
            "quality_gate": "quality_gate",
            "terminal_checkpoint": "terminal_checkpoint",
            "blocked": "blocked",
        },
    )
    builder.add_conditional_edges(
        "sync_repository",
        lambda state: "human_gate" if state["human_gate"] else "prepare_worktree",
    )
    builder.add_conditional_edges(
        "prepare_worktree",
        lambda state: "human_gate" if state["human_gate"] else "select_requirements",
    )
    builder.add_conditional_edges(
        "select_requirements",
        lambda state: "human_gate" if state["human_gate"] else "implement",
    )
    builder.add_conditional_edges(
        "implement",
        lambda state: "human_gate" if state["human_gate"] else "checkpoint_run",
    )

    # Specification and local validation loops
    builder.add_conditional_edges(
        "validate_specification",
        lambda state: (
            "human_gate"
            if state["human_gate"]
            else route_specification(state, graph_policy)
        ),
    )
    builder.add_conditional_edges(
        "repair_specification",
        lambda state: "human_gate" if state["human_gate"] else "validate_specification",
    )
    builder.add_conditional_edges(
        "quality_gate",
        lambda state: (
            "human_gate"
            if state["human_gate"]
            else route_quality_gate(state, graph_policy)
        ),
    )
    builder.add_conditional_edges(
        "repair_quality_gate",
        lambda state: "human_gate" if state["human_gate"] else "validate_specification",
    )

    # PR and remote-state routing
    builder.add_conditional_edges(
        "prepare_pull_request",
        lambda state: "human_gate" if state["human_gate"] else "checkpoint_run",
    )
    builder.add_conditional_edges(
        "inspect_pr",
        lambda state: (
            "human_gate"
            if state["human_gate"]
            else route_pr_inspection(state, graph_policy)
        ),
    )
    builder.add_conditional_edges(
        "ci_triage",
        lambda state: "human_gate" if state["human_gate"] else "apply_ci_correction",
    )
    builder.add_conditional_edges(
        "apply_ci_correction",
        lambda state: "human_gate" if state["human_gate"] else "quality_gate",
    )
    builder.add_conditional_edges(
        "resolve_merge_conflict",
        lambda state: "human_gate" if state["human_gate"] else "checkpoint_run",
    )

    # Independent model review and feedback
    builder.add_conditional_edges(
        "independent_review",
        lambda state: (
            "human_gate"
            if state["human_gate"]
            else route_independent_review(state, graph_policy)
        ),
    )
    builder.add_conditional_edges(
        "validate_review_feedback",
        lambda state: (
            "human_gate" if state["human_gate"] else route_review_feedback(state)
        ),
    )
    builder.add_conditional_edges(
        "validate_pull_request",
        lambda state: (
            "human_gate"
            if state["human_gate"]
            else route_pull_request_validation(state)
        ),
    )

    # Human-in-the-loop and terminal states
    builder.add_conditional_edges(
        "human_gate",
        route_human_decision,
        {
            "validate_scope": "validate_scope",
            "claim_issue": "claim_issue",
            "sync_repository": "sync_repository",
            "prepare_worktree": "prepare_worktree",
            "select_requirements": "select_requirements",
            "implement": "implement",
            "validate_specification": "validate_specification",
            "repair_specification": "repair_specification",
            "repair_quality_gate": "repair_quality_gate",
            "prepare_pull_request": "prepare_pull_request",
            "inspect_pr": "inspect_pr",
            "ci_triage": "ci_triage",
            "apply_ci_correction": "apply_ci_correction",
            "resolve_merge_conflict": "resolve_merge_conflict",
            "independent_review": "independent_review",
            "validate_review_feedback": "validate_review_feedback",
            "validate_pull_request": "validate_pull_request",
            "blocked": "blocked",
            "aborted": "aborted",
        },
    )
    builder.add_edge("ready_for_human_merge", "terminal_checkpoint")
    builder.add_edge("blocked", "terminal_checkpoint")
    builder.add_edge("aborted", "terminal_checkpoint")
    builder.add_edge("terminal_checkpoint", END)

    return builder.compile(checkpointer=checkpointer)
