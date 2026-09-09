# Coffee-Driven Development

This repository is intentionally small.

## Project invariants

- Prefer the simplest implementation that satisfies the current requirement.
- Keep domain logic independent from CLI presentation.
- Use typed Python.
- Do not add dependencies without justification.
- Do not modify files when explicitly asked only to plan or analyze.
- For non-trivial changes, inspect the repository and propose a plan first.
- Human approval is required at the architecture-decision and final-merge gates.

## Harness configuration

Read `.ai/harness.config.json` for deterministic shared harness values. Its
versioned schema contains the default branch, canonical quality-gate commands,
shared repository paths, graph retry policy, GitHub claim label, and human-gate
identifiers.

Keep rules and invariants here, reusable procedures in Skills, specialist
reasoning in custom agents, explicit delivery orchestration and state
transitions in the Feature Delivery Graph, historical evidence in
`AI_WORKLOG.md`, and resumable operational state in `.ai/runs/`.

LangGraph technical checkpoints are execution-engine persistence only and do
not replace `.ai/runs/` as the canonical compact operational record.

## Human and Git gates

- Do not commit task changes directly to the default branch.
- Pull requests remain human-controlled.
- Never merge or enable auto-merge.
- A `CLEAR` validation result is not approval to merge.
- `READY_FOR_HUMAN_MERGE` is a readiness state, not merge authorization.
- Material product, architecture, dependency, permission, and unresolved
  semantic-conflict decisions remain human-controlled.

## Validation

Before completing a code change, run every command in the configured
`quality_gate_commands` list.

The configured pytest command enforces at least 90% branch coverage across
production code. All checks must pass. Do not meet the coverage threshold
through artificial exclusions or tests that do not assert meaningful behavior.

For graph-driven delivery, CI and independent-review evidence are valid only
for the exact current HEAD. Any HEAD change invalidates stale evidence and
requires the graph to obtain fresh validation before final readiness.

## Repository context

- Project roadmap: configured `paths.implementation_plan`
- Authoritative product specification: configured `paths.specification_index`
- AI-assisted development history: configured `paths.ai_worklog`
- Resumable operational state: configured `paths.resumable_runs`
- Graph technical checkpoints: configured `paths.graph_checkpoints`
- Feature Delivery Graph documentation:
  `docs/ai/feature-delivery-graph.md`
- Python conventions: `docs/engineering/python-guidelines.md`
- Testing strategy: `docs/engineering/testing-strategy.md`

## Task Router

| Situation | Use |
| --- | --- |
| Before repository-changing work, or after a merged PR before subsequent work, unless freshness was already verified in the current session | `sync-repository` |
| Work likely to span sessions or meaningful stages needs operational state under `.ai/runs/` while permanent history remains in `AI_WORKLOG.md` | `manage-ai-run` |
| A short feature goal needs to become one scoped GitHub Issue, without implementation or multi-Issue planning | `create-feature-issue` |
| A scoped behavioral product change needs implementation; not documentation, Skills, or Git-only work | `develop-feature-tdd` |
| A scoped implementation, diff, pull request, or feature needs conformance validation against the authoritative product specification | `validate-specification` |
| A completed, validated change is ready to be delivered on a dedicated branch as a review-ready PR | `prepare-pull-request` |
| Meaningful AI-assisted work changes the repository, architecture, harness, validation, or external integrations, and is not already being logged by `prepare-pull-request` | `record-ai-session` |
| Periodic read-only evaluation is needed to determine whether real engineering evidence justifies changing the repository harness | `harness-retrospective` |
| A real Git merge conflict must be inspected and resolved while preserving both sides | `resolve-merge-conflict` |
| An existing PR has actionable human or automated review feedback | `validate-review-feedback` |
| A delivered PR has had review feedback processed and needs the final readiness assessment before human merge | `validate-pull-request` |
| One already-scoped GitHub Issue should be delivered end to end through explicit resumable orchestration with specification validation, bounded retries, current-HEAD CI/review freshness, conflict routing, independent review, and final human merge | Manually select the Feature Delivery Agent; it drives the Feature Delivery Graph |
| Current-head GitHub Actions CI is failing and the root cause is not obvious | Manually select the CI Triage Agent before applying a correction |
| One existing PR needs evidence-based diagnosis and routing across repository capabilities | Manually select the PR Autopilot Agent |

Keep detailed procedures inside the selected Skill, specialist agent, or graph.

The Feature Delivery Graph owns end-to-end execution order, retry bounds,
state transitions, freshness enforcement, and human-gate routing. Skills remain
the authority for reusable procedures, and specialist agents remain responsible
for bounded reasoning within their defined scopes.

When the Feature Delivery Agent is selected for end-to-end Issue delivery, it
must start or resume the matching graph thread and execute only the capability
requested by the graph at each interrupt. It must not bypass graph retry limits,
specification validation, current-HEAD freshness checks, merge-conflict routing,
independent-review separation, or human gates.

When `prepare-pull-request` is used, let it invoke `record-ai-session` after the
PR exists so the session is logged once with the actual Git and PR outcome.
