---
name: develop-feature-tdd
description: Implement a scoped behavioral product change through the repository's test-first workflow; do not use for documentation, Skills, or Git-only work.
---

# Develop feature with TDD

Use for a scoped product behavior where test-first development is appropriate.
Read `AGENTS.md`, the relevant requirement or Issue, related source and tests,
and [Python guidelines](../../../docs/engineering/python-guidelines.md) plus
[testing strategy](../../../docs/engineering/testing-strategy.md).

1. Identify observable acceptance criteria and the smallest useful tests.
   Stop for human input if the work changes architecture or scope, needs a
   significant dependency, or contains an ambiguous product decision.
2. Write tests first and run targeted tests before production code. Confirm RED
   is an expected missing-behavior failure; do not count setup failures or
   unexpected passes as RED.
3. Implement the smallest reasonable change, rerun targeted tests, and confirm
   GREEN. Refactor only for local clarity or obvious duplication.
4. Run the AGENTS.md quality gate, inspect the complete diff for weakened tests,
   debug code, unrelated changes, and scope expansion, then summarize RED,
   GREEN, validation, and remaining risks.
5. When complete and validated, use `prepare-pull-request` for delivery. Do not
   reproduce its Git workflow or merge the PR.
