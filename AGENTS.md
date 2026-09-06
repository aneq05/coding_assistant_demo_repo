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