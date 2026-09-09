# Coffee-Driven Development

This repository is intentionally small.

## Project invariants

- Prefer the simplest implementation that satisfies the current requirement.
- Keep domain logic independent from CLI presentation.
- Use typed Python.
- Do not add dependencies without justification.
- Do not modify files when explicitly asked only to plan or analyze.
- For non-trivial changes, inspect the repository and propose a plan first.
- Human approval is required for architectural decisions and final merge.

## Human and Git gates

- Do not commit task changes directly to the default branch.
- Pull requests remain human-controlled. Never merge or enable auto-merge; a
  `CLEAR` validation result is not approval to merge.

## Validation

Before completing a code change, run:

1. `uv run --extra dev pytest`
2. `uv run --extra dev ruff check .`
3. `uv run --extra dev mypy`

All checks must pass.

## Repository context

- Project roadmap: `docs/IMPLEMENTATION_PLAN.md`
- AI-assisted development history: `AI_WORKLOG.md`
- Python conventions: `docs/engineering/python-guidelines.md`
- Testing strategy: `docs/engineering/testing-strategy.md`

## Task Router

| Situation | Use |
| --- | --- |
| Before repository-changing work, or after a merged PR before subsequent work, unless freshness was already verified in the current session | `sync-repository` |
| A short feature goal needs to become one scoped GitHub Issue, without implementation or multi-Issue planning | `create-feature-issue` |
| A scoped behavioral product change needs implementation; not documentation, Skills, or Git-only work | `develop-feature-tdd` |
| A completed, validated change is ready to be delivered on a dedicated branch as a review-ready PR | `prepare-pull-request` |
| Meaningful AI-assisted work changes the repository, architecture, harness, validation, or external integrations, and is not already being logged by `prepare-pull-request` | `record-ai-session` |
| A real Git merge conflict must be inspected and resolved while preserving both sides | `resolve-merge-conflict` |
| An existing PR has actionable human or automated review feedback | `validate-review-feedback` |
| A delivered PR has had review feedback processed and needs the final readiness assessment before human merge | `validate-pull-request` |
| One already-scoped GitHub Issue should be delivered end to end as a review-ready PR | Manually select the Feature Delivery Agent |
| Current-head GitHub Actions CI is failing and the root cause is not obvious | Manually select the CI Triage Agent before applying a correction |
| One existing PR needs evidence-based diagnosis and routing across repository capabilities | Manually select the PR Autopilot Agent |

Keep detailed procedures inside the selected Skill or agent. When
`prepare-pull-request` is used, let it invoke `record-ai-session` after the PR
exists so the session is logged once with the actual Git and PR outcome.
