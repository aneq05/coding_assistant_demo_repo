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

## AI session logging

After completed non-trivial AI-assisted work that materially changes the
repository, architecture, harness, validation, or external integrations, use
the `record-ai-session` Skill to append an accurate entry to `AI_WORKLOG.md`.
Do not log trivial interactions, invent missing metadata, or override explicit
user instructions.
