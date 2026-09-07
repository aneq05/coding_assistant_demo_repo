# Coffee-Driven Development

This repository is intentionally small.

## Core rules

- Prefer the simplest implementation that satisfies the current requirement.
- Keep domain logic independent from CLI presentation.
- Use typed Python.
- Do not add dependencies without justification.
- Do not modify files when explicitly asked only to plan or analyze.
- For non-trivial changes, inspect the repository and propose a plan first.
- Human approval is required for architectural decisions and final merge.

## Validation

Before completing a code change, run:

1. `uv run --extra dev pytest`
2. `uv run --extra dev ruff check .`
3. `uv run --extra dev mypy`

All checks must pass.

## Repository context

- Project roadmap: `docs/IMPLEMENTATION_PLAN.md`
- AI-assisted development history: `AI_WORKLOG.md`

## Repository synchronization

Before new repository-changing work, or after a merged PR before subsequent
work, use `sync-repository` unless freshness was already verified during the
current session.

## AI session logging

After completed non-trivial AI-assisted work that materially changes the
repository, architecture, harness, validation, or external integrations, use
the `record-ai-session` Skill to append an accurate entry to `AI_WORKLOG.md`.
Do not log trivial interactions, invent missing metadata, or override explicit
user instructions.

## Git delivery

Completed validated changes that should be published for review must use the
`prepare-pull-request` Skill. Do not commit task changes directly to the
default branch; pull requests remain human-controlled and must not be
automatically merged. A successful PR should finish ready for review. When this Skill is used, let it invoke
`record-ai-session` after the PR exists so the session is logged once with the
actual Git and PR outcome.

## Engineering guidance

- Python conventions: `docs/engineering/python-guidelines.md`
- Testing strategy: `docs/engineering/testing-strategy.md`

For scoped product features or behavioral changes, use `develop-feature-tdd`
when appropriate. For actionable PR review feedback, use
`validate-review-feedback` before applying reviewer suggestions.

When current-head CI fails and its root cause is not obvious, manually select
the repository's `ci-triage` custom agent before applying a correction.

## Pull request validation

Before a pull request is considered ready for human merge, use
`validate-pull-request`. Use `validate-review-feedback` first when actionable
review feedback remains unresolved. A CLEAR result does not merge the PR;
final merge remains a human decision.
