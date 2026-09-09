---
name: prepare-pull-request
description: Safely deliver a completed, validated repository change on a dedicated branch as a ready-for-review pull request; never use it to merge or bypass validation.
---

# Prepare pull request

Use after a meaningful completed change is ready for GitHub review. Do not use
for unfinished or failing work, unresolved conflicts, inseparable unrelated
changes, or potential secrets.

Invoking this Skill pre-authorizes normal delivery actions: branch creation or
switching, explicit staging, committing, pushing, creating or updating a PR,
recording the session, pushing its worklog commit, and marking the PR ready for
review. Do not request conversational confirmation for those actions. Stop for
validation failure, secrets, ambiguous remotes, unrelated branch conflicts,
architecture or significant dependency decisions, destructive Git behavior, or
an environment-enforced approval prompt. Final merge remains human-controlled.

1. Read the default branch and shared paths from `.ai/harness.config.json`.
   Inspect the branch, status, complete diff, and remotes. Never commit task
   changes directly to the configured default branch. From that branch, create
   a lowercase, hyphenated branch using `feature/`, `fix/`, `chore/`, or
   `docs/`; inspect an existing candidate branch before reuse.
2. Identify intended files, generated files, caches, secrets, and unrelated
   changes. Stop if intended changes cannot be safely separated. Stage files
   explicitly; never blindly use `git add .`.
3. Run the configured quality-gate commands required by `AGENTS.md` for code
   changes. For documentation or harness work, run relevant inexpensive checks
   and validate Skills where applicable. Stop on known validation failure
   unless the user explicitly requests preservation of a failing state.
4. Inspect the staged diff, create a specific conventional-style commit, and
   record its SHA. Do not amend unrelated commits or rewrite history.
5. Push only the current task branch (`git push -u origin <branch>` when no
   upstream exists; otherwise `git push`). Never force-push. Verify the remote
   branch exists.
6. Create a draft PR to the default branch when an authenticated mechanism is
   available. Include Summary, Why, Validation, Scope, AI-assisted workflow,
   and Review notes; state human review is required. Do not invent issue
   references. If a PR for the branch already exists, update it rather than
   creating another. If drafts are unsupported, create a normal PR with that
   review requirement stated. Never merge, enable auto-merge, or approve the PR.
7. After the PR exists, use `record-ai-session` once with actual branch,
   commit, validation, and PR facts. Inspect its diff, commit only
   the configured AI worklog separately, push it to the same branch, and verify
   the PR includes it. Do not duplicate its logging workflow here.
8. Mark a successfully completed PR ready for review after the final worklog
   commit is pushed. Leave it draft only when work remains incomplete,
   validation is incomplete, or the user explicitly requests a draft.

If authenticated push or PR creation is unavailable, report the limitation
after recording any material local commit or delivery attempt through
`record-ai-session`. Do not claim end-to-end delivery.
