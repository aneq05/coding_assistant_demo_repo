---
name: prepare-pull-request
description: Safely deliver a completed, validated repository change on a dedicated branch as a draft pull request; never use it to merge or bypass validation.
---

# Prepare pull request

Use after a meaningful completed change is ready for GitHub review. Do not use
for unfinished or failing work, unresolved conflicts, inseparable unrelated
changes, or potential secrets.

1. Inspect the branch, status, complete diff, remotes, and default branch.
   Never commit task changes directly to `main` or `master`. From a default
   branch, create a lowercase, hyphenated branch using `feature/`, `fix/`,
   `chore/`, or `docs/`; inspect an existing candidate branch before reuse.
2. Identify intended files, generated files, caches, secrets, and unrelated
   changes. Stop if intended changes cannot be safely separated. Stage files
   explicitly; never blindly use `git add .`.
3. Run validation required by `AGENTS.md` for code changes. For documentation
   or harness work, run relevant inexpensive checks and validate Skills where
   applicable. Stop on known validation failure unless the user explicitly
   requests preservation of a failing state.
4. Inspect the staged diff, create a specific conventional-style commit, and
   record its SHA. Do not amend unrelated commits or rewrite history.
5. Push only the current task branch (`git push -u origin <branch>` when no
   upstream exists; otherwise `git push`). Never force-push. Verify the remote
   branch exists.
6. Create a draft PR to the default branch when an authenticated mechanism is
   available. Include Summary, Why, Validation, Scope, AI-assisted workflow,
   and Review notes; state human review is required. Do not invent issue
   references. If drafts are unsupported, create a normal PR with that review
   requirement stated. Never merge, enable auto-merge, or approve the PR.
7. After the PR exists, use `record-ai-session` once with actual branch,
   commit, validation, and PR facts. Inspect its diff, commit only
   `AI_WORKLOG.md` separately, push it to the same branch, and verify the PR
   includes it. Do not duplicate its logging workflow here.

If authenticated push or PR creation is unavailable, report the limitation
after completing only the safe local steps. Do not claim end-to-end delivery.
