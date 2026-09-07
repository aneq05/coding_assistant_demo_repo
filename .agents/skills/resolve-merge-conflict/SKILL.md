---
name: resolve-merge-conflict
description: Safely inspect and resolve a real Git merge conflict while preserving both sides and validating the resulting branch.
---

# Resolve a merge conflict

Use this workflow when a branch must incorporate another branch's changes.

1. Inspect repository identity, current branch, remotes, worktree status,
   untracked files, and recent history before modifying anything. Preserve
   unrelated user work. Never use `reset --hard`, `clean`, destructive
   checkout, history rewriting, or force-push.
2. Prefer merging the latest base branch into the topic branch so existing
   history is preserved. Identify every unmerged path with Git; do not infer
   the conflict set from visible markers alone. If repository or PR context is
   available through GitHub tooling, inspect base/head refs, mergeability,
   changed files, and relevant commits before resolving.
3. For each conflicted file, inspect both stages and the surrounding changes,
   then classify it as `TRIVIAL`, `COMPOSABLE`, `SEMANTIC`, or
   `ARCHITECTURAL`:
   - `TRIVIAL`: formatting or mechanically equivalent text.
   - `COMPOSABLE`: independent compatible additions that can both be retained.
   - `SEMANTIC`: overlapping behavior or content requiring a product decision.
   - `ARCHITECTURAL`: incompatible structure, ownership, or system direction.
4. Automatically resolve only `TRIVIAL` or `COMPOSABLE` conflicts when the
   repository evidence clearly supports the result. Never blindly choose ours
   or theirs. Stop and request human direction for ambiguous semantic or
   architectural intent; do not manufacture a compromise.
5. Resolve only the actual conflicts. Preserve unrelated work and the intent
   of both sides where compatible. Inspect the final diff for accidental loss
   from either parent, remove all conflict markers, and verify no unmerged
   paths remain.
6. Run focused validation for affected behavior, then the repository's full
   quality gate and `git diff --check`. Do not weaken tests or validation to
   make the merge pass.
7. Commit the merge resolution with a clear message and push the existing
   topic branch without force. Re-check the remote PR's current head and
   mergeability when GitHub tooling is available. Update its description only
   with truthful, relevant facts. Human approval remains required for
   ambiguous intent and final merge.
