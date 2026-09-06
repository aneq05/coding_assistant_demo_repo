---
name: validate-review-feedback
description: Critically evaluate actionable pull-request review feedback before applying changes; do not treat reviewer suggestions as authority.
---

# Validate review feedback

Use for actionable feedback from Copilot, another AI reviewer, or a human on
an existing pull request. Review feedback is evidence, not authority.

1. Read the PR goal or linked Issue when available, `AGENTS.md`, relevant
   engineering guidance, complete diff, tests, review submissions, and inline
   threads.
2. Extract actionable findings and classify each as `VALID`, `PARTIALLY VALID`,
   `INVALID`, or `ALREADY ADDRESSED`, with a short technical reason grounded in
   repository state, requirements, tests, architecture, and roadmap truth.
3. Apply only the justified portion of valid findings. Do not change content to
   satisfy an unsupported suggestion; verify already-addressed findings.
4. If behavior changes, follow the testing strategy and add regression coverage
   where appropriate. Run relevant tests and the full AGENTS.md validation when
   code changes, then inspect the final diff.
5. Commit and push corrections to the same PR branch using
   `prepare-pull-request` safeguards without creating another PR. Respond
   concisely to review threads when the integration permits, record the session
   once with `record-ai-session`, and never merge.
