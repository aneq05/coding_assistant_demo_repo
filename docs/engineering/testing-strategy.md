# Testing strategy

## Test philosophy

- Test externally meaningful, deterministic behavior rather than incidental
  implementation details.
- New behavior normally has tests; regressions receive regression tests.
- Filesystem tests use isolated temporary locations and never modify the real
  user home directory.

## TDD cycle

For suitable product behavior: requirement → observable behavior → test first
→ RED → minimal implementation → GREEN → justified refactor → full validation.

Run each new test before production implementation. A valid RED failure is
expected and demonstrates the missing intended behavior. Investigate an
unexpected pass; fix test setup or unrelated failures without calling them RED.

Implement the smallest reasonable change for GREEN. Do not weaken a test merely
to pass it. After targeted tests are green, run the validation commands in
`AGENTS.md`.

## Coverage quality gate

The test suite measures branch coverage for production code in `src/cdd` only.
Total coverage must be at least 90%; `uv run --extra dev pytest` fails below
that threshold. Coverage gains must come from meaningful, behavior-focused
tests, not artificial exclusions or assertions that merely execute lines.

Pytest writes a terminal missing-lines report plus machine-readable XML and JSON
reports and a human-readable HTML report under `reports/`. CI uploads those
outputs with the existing validation reports and publishes the required 90%
threshold, actual measured coverage, and coverage result in its job summary.
Pytest, coverage, ruff, and mypy are all required CI outcomes.
