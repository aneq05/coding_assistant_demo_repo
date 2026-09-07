---
name: validate-pull-request
description: Assess whether an open pull request is genuinely ready for human merge after delivery and review feedback; never merge or replace review-feedback validation.
---

# Validate pull request

Use after a PR has been prepared and review feedback processed, before human
merge. This is a quality gate, not a code reviewer, test-runner, delivery
workflow, or merge workflow.

1. Inspect PR metadata: open status, correct base, non-default head branch,
   ready-for-review state, unmerged status, auto-merge where detectable, and
   GitHub mergeability/conflict state. A confirmed unmergeable or conflicted PR
   is `BLOCKED`; when mergeability is unavailable or unknown, report that
   explicitly rather than treating the check as PASS.
2. Inspect title and body for concise, accurate scope, rationale, only actual
   validation evidence, excluded scope, and relevant review information.
3. Inspect the complete diff for unrelated files, generated artifacts, secrets,
   local configuration, and scope inconsistent with the PR description. Check
   against `AGENTS.md`, relevant engineering guidance, and roadmap state.
4. For code PRs, confirm the required local AGENTS.md quality gate passed, then
   inspect required GitHub Actions or check results for the current PR HEAD SHA.
   CI passes only when required validation for that exact SHA completed and all
   required checks succeeded. A completed failure or known broken workflow is
   `BLOCKED`. Pending, unavailable, absent, or indeterminate CI is
   `NEEDS_ATTENTION`, as is a successful run for only an older SHA. Never infer
   CI success from a PR description or treat local validation as independent CI.
   For harness or documentation PRs, apply required CI when repository policy
   requires it and confirm relevant Skill and diff validation occurred.
5. Read review submissions, comments, and threads. Compare the current PR HEAD
   with the latest relevant automated or required review using an exposed review
   commit SHA or explicit reviewed-commit evidence. Do not guess. A review shown
   to cover the current HEAD passes; a stale or unverifiable required review is
   `NEEDS_ATTENTION`, and a new review should be requested after HEAD changes.
6. Classify readiness as `BLOCKED` for a confirmed unmergeable or conflicted PR,
   failed required current-HEAD CI, unresolved actionable feedback, or failing
   required validation; `NEEDS_ATTENTION` for unknown mergeability, incomplete
   or stale CI/review evidence, or non-blocking metadata or consistency issues;
   otherwise `CLEAR` when all evidence aligns with the current HEAD.
7. Route unresolved actionable feedback to `validate-review-feedback`; do not
   reimplement it, resolve threads without verification, or alter code merely
   to satisfy this checklist. Return a concise PASS checklist and reasons for
   every non-PASS result. Never merge or enable auto-merge.
8. Use this quality flow without assuming CI and review finish serially:
   implementation, local validation, push, current-HEAD CI and automated review,
   feedback validation, this final gate, then human merge. Validate both CI and
   review freshness against the final current HEAD.
