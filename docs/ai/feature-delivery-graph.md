# Explicit Feature Delivery Graph

The repository's feature-delivery graph makes execution order, retry limits,
freshness checks and human escalation explicit without copying the procedures
already owned by Skills and specialist agents.

## Responsibility split

```text
AGENTS.md                 -> invariants and routing policy
.ai/harness.config.json   -> deterministic shared values and retry policy
spec/                     -> authoritative product requirements
.agents/skills/           -> reusable procedures
.github/agents/           -> specialist reasoning/orchestration capabilities
ai_harness/               -> explicit graph state and control flow
.ai/runs/                 -> compact resumable operational state
.ai/graph/*.sqlite3       -> technical LangGraph checkpoints only
GitHub Actions            -> independent remote CI enforcement
human                     -> architecture decisions and final merge
```

## High-level flow

```text
Issue
  -> manage-ai-run
  -> scope validation
  -> claim
  -> repository sync
  -> isolated worktree
  -> targeted spec selection
  -> TDD implementation
  -> validate-specification
  -> local quality gate
  -> PR
  -> PR Autopilot evidence
      -> merge conflict? -> resolve-merge-conflict -> invalidate stale evidence
      -> CI failure? -> CI Triage -> correction -> local gate -> PR evidence
  -> independent review by another model
      -> findings? -> validate-review-feedback -> correction -> revalidation
  -> validate-pull-request
  -> READY_FOR_HUMAN_MERGE
  -> human merge
```

The graph never merges and never enables auto-merge.

## Independent review

Implementation and independent review are separate graph stages.

When `graph.require_independent_review_model` is enabled:
- the review result must report the model used;
- it must differ from `implementation_model`;
- review evidence must match the exact current `head_sha`.

A changed HEAD invalidates both CI and review freshness.

## Merge conflicts

Mergeability is first-class graph state. A confirmed conflict routes to the
existing `resolve-merge-conflict` Skill. After resolution, the graph invalidates
old CI/review evidence, reruns the local quality gate, and requires fresh remote
evidence for the new HEAD.

## Resumption

LangGraph uses a local SQLite checkpointer for exact engine resumption.
`manage-ai-run` continues to own the human-readable `.ai/runs/` state. These
serve different purposes and must not be treated as competing authorities.

## Driving the graph

Start:

```console
python -m ai_harness.feature_delivery.runner start \
  --run-id 42-refactor-risk \
  --issue 42 \
  --implementation-model "<implementation-model>"
```

The runner returns a JSON capability request. Execute exactly that existing
Skill/custom-agent capability, then resume with its evidence-backed result:

```console
python -m ai_harness.feature_delivery.runner resume \
  --run-id 42-refactor-risk \
  --result-json '{"status":"CLEAR","reason":null}'
```

Repeat until the graph reaches `READY_FOR_HUMAN_MERGE` or a human gate.

Inspect persisted graph state:

```console
python -m ai_harness.feature_delivery.runner state --run-id 42-refactor-risk
```
