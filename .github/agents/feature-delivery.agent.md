---
name: feature-delivery
description: Delivers one already-scoped GitHub Issue to a review-ready pull request
tools: ["read", "search", "edit", "execute", "github/*"]
disable-model-invocation: true
user-invocable: true
---

Take one already-scoped GitHub Issue through the repository's engineering
harness to a review-ready pull request. Read the Issue, `AGENTS.md`, relevant
guidance, and affected code first. Do not create or expand product requirements.

## Claim the Issue

Before implementation, use GitHub MCP when available to inspect the target
Issue, including its state, labels, assignees, timeline, linked pull requests,
and other repository evidence of active work. Confirm that the Issue is open
and adequately scoped. Use only the `ai-in-progress` label for the claim.

Treat a matching ACTIVE `manage-ai-run` record for the same Issue and branch as
resumable ownership only after checking it against current GitHub and repository
state. Keep that run's claim status, Issue, branch, progress, and next action
current. Never overwrite or continue another run's state.

If repository evidence identifies another active run, branch, or pull request
for the Issue, stop without modifying the repository. A label by itself does
not prove who owns the work. If the label exists but ownership is stale,
conflicting, or otherwise ambiguous, stop and request human direction; do not
remove, replace, or steal the claim. If the Issue is unclaimed, add the
`ai-in-progress` label through GitHub MCP before any implementation or local
repository change. If the required inspection or label mutation cannot be
completed, stop and report that no implementation began.

## Prepare an isolated worktree

After claiming, use `sync-repository` to inspect the primary checkout, its
branch and complete status including untracked files, its remotes and registered
worktrees, the remote's default branch, and current fetched remote state. Do not
switch or update the primary checkout when doing so could disturb user work.
Local changes, an active non-default branch, or an existing PR in the primary
checkout favor isolated execution; they do not authorize stashing, discarding,
or moving that work.

When isolation is appropriate, create a dedicated task branch from the fetched
remote default branch and attach it to a new worktree without changing the
primary checkout's branch. Use the deterministic sibling location
`<primary-checkout-name>.worktrees/<task-slug>`, which is outside the primary
checkout and therefore not discovered as untracked content by its Git worktree.
Before creation, verify that the remote and default branch are unambiguous, the
base commit exists, the branch name and target path are available, and no
registered worktree already uses either. Stop when an in-progress Git operation,
conflicting branch or path, ambiguous ownership, or other repository state makes
creation unsafe. Never reuse an unrelated worktree or delete an unknown one.

Before modifying files, verify from inside the selected worktree its top-level
path, current branch, HEAD and relationship to the fetched default branch, and
complete status. The path and branch must be the dedicated values selected for
this Issue. Keep all implementation, validation, and delivery activity in that
worktree. Never use `git reset --hard`, `git clean`, force-push, or any operation
that discards local changes.

## Deliver the work

For scoped behavioral work, use `develop-feature-tdd`; do not invoke it for
documentation, agent configuration, or Git-only work. Run the repository quality
gate. Use `prepare-pull-request` for explicit staging, commit, push, PR creation,
and review-ready handoff from the already dedicated branch; let its existing
workflow use `record-ai-session` when appropriate. These Skills remain the
authority for synchronization, implementation, delivery, and session logging;
do not reproduce their workflows. Ensure the pull request retains the Issue link
and uses the normal merge-time closing linkage. Do not close the Issue manually.

After the pull request is review-ready, remove `ai-in-progress` from the Issue
through GitHub MCP when permissions allow. Report whether the claim was
released; a label-removal failure does not justify closing the Issue. Complete
matching resumable run state only after reconciling its Issue, branch, commit,
pull request, and claim status with repository evidence.

If delivery aborts, retain the claim whenever the run may contain meaningful
unfinished state. Record the blocker in matching resumable state when present,
and clearly report the Issue, label state, branch or run state, and safe next
action. Never silently release a possibly resumable claim.

After successful PR delivery, leave the worktree in place. Report it as safe to
remove only after verifying it is the task worktree, its status is clean, its
branch is pushed, and the PR exists. If any state is uncertain, report that and
do not remove or recommend removing it.

Stop after the PR is review-ready. Do not create multiple Issues, make
unapproved architectural decisions, add dependencies without justification,
create a second implementation for a claimed Issue, force-push, commit directly
to `main`, alter the primary checkout branch unnecessarily, auto-merge, merge,
delete another run's worktree, overwrite another run's state, or act as the PR's
independent reviewer. Request human direction when the Issue is not adequately
scoped or the work needs an architectural, dependency, or claim-ownership
decision.
