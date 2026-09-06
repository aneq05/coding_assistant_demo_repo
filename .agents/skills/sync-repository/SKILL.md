---
name: sync-repository
description: Safely verify and synchronize repository state before new repository-changing work without discarding, rewriting, or publishing local work.
---

# Synchronize repository

Use before starting repository-changing work when freshness has not already
been verified in the current session, especially after a previous pull request
was merged. This is a synchronization workflow, not cleanup or delivery.

1. Inspect the current branch, working tree including untracked files,
   configured remotes, default branch, and remote repository identity. Verify
   that the expected repository and remote are in use.
2. If switching or updating could overwrite or lose local work, stop and report
   the exact affected state. Never discard changes, stash user work, reset hard,
   clean files, overwrite branches, or delete an old task branch.
3. Fetch the configured remote and determine whether the local default branch
   is behind, ahead, diverged, or current relative to its remote counterpart.
4. When preparing for new work after the previous task PR was merged, switch to
   the default branch only when safe and update it with fast-forward-only
   behavior. Never merge remote changes or rebase user work automatically.
5. When the current task branch has an open PR, preserve it: fetch and report
   its relationship to the default branch and PR, but do not switch, merge, or
   rebase merely to synchronize.
6. Before declaring success, verify the local default HEAD equals the remote
   default HEAD. Return `Repository synchronization: CURRENT` or
   `Repository synchronization: NEEDS_ATTENTION` with the current branch,
   both default-branch SHAs, ahead/behind state, and any local-work warnings.

Do not commit, push, or create a pull request. Those actions belong to the
delivery workflow.
