---
name: validate-pull-request
description: Assess whether an open pull request is genuinely ready for human merge after delivery and review feedback; never merge or replace review-feedback validation.
---

# Validate pull request

Use after a PR has been prepared and review feedback processed, before human
merge. This is a quality gate, not a code reviewer, test-runner, delivery
workflow, or merge workflow.

1. Inspect PR metadata: open status, correct base, non-default head branch,
   ready-for-review state, unmerged status, and auto-merge where detectable.
2. Inspect title and body for concise, accurate scope, rationale, only actual
   validation evidence, excluded scope, and relevant review information.
3. Inspect the complete diff for unrelated files, generated artifacts, secrets,
   local configuration, and scope inconsistent with the PR description. Check
   against `AGENTS.md`, relevant engineering guidance, and roadmap state.
4. For code PRs, confirm the required AGENTS.md quality gate passed. For harness
   or documentation PRs, confirm relevant Skill and diff validation actually
   occurred. Never fabricate validation.
5. Read review submissions, comments, and threads. Classify readiness as
   `BLOCKED` for unresolved actionable feedback or failing required validation;
   `NEEDS_ATTENTION` for non-blocking metadata or consistency issues; otherwise
   `CLEAR` when metadata, scope, validation, and review state align.
6. Route unresolved actionable feedback to `validate-review-feedback`; do not
   reimplement it, resolve threads without verification, or alter code merely
   to satisfy this checklist. Return a concise PASS checklist and reasons for
   every non-PASS result. Never merge or enable auto-merge.
