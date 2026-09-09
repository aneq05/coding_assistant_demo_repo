---
name: manage-ai-run
description: Start or continue lightweight operational run state for engineering work likely to span sessions or meaningful stages; do not use for short tasks or permanent history.
---

# Manage resumable AI run state

Use `.ai/runs/<run-id>.md` only when the work is likely to cross sessions or
several meaningful stages. The file is disposable operational context, not
project history. Keep durable outcomes in `AI_WORKLOG.md` through the
repository's logging workflow; do not duplicate them here.

## Start a run

1. Inspect the current repository and any known Issue, PR, or branch before
   recording state. If the task is small enough to finish in one ordinary
   session, do not create a run file.
2. Choose a unique lowercase kebab-case identifier. Prefer
   `<issue-number>-<short-goal>` when an Issue is known; otherwise use
   `<yyyy-mm-dd>-<short-goal>`.
3. Create `.ai/runs/<run-id>.md` with the compact structure below. Record
   unknown links or branch values as `null`. Omit `commit_sha` entirely until
   a real commit exists and its SHA has been verified.
4. Seed an ordered checklist of meaningful, independently resumable steps.
   Mark a step complete only when repository or external evidence proves it.

```markdown
---
run_id: <run-id>
status: ACTIVE
goal: <one-sentence goal>
github_issue: null
pull_request: null
branch: null
---

## Progress

- [ ] <first meaningful step>
- [ ] <next meaningful step>

## Decisions

- decision: <decision needed to continue>; evidence: <repository path, command result, or external reference>

## Blocking state

- state: NONE
- detail: null

## Next action

<one concrete action>
```

Use `status: ACTIVE`, `BLOCKED`, or `COMPLETE`. Keep only decisions that affect
continuation, and attach specific evidence to each one. Do not record a
decision merely because it was proposed. Remove the example decision line when
there is no evidence-backed decision to preserve.

## Continue a run

1. Read the requested run file, then inspect current repository evidence and
   any recorded Issue, PR, branch, or commit before acting.
2. Compare that evidence with the recorded status, completed checklist items,
   decisions, and references. If they conflict, do not continue or rewrite the
   discrepancy; stop and report the exact conflict.
3. Resume from the first unchecked Progress item. Do not repeat completed work
   unless new evidence invalidates it, which is a conflict requiring a stop.
4. After each completed meaningful step, update Progress and the single next
   action. Update Issue, PR, branch, blocking state, and evidence-backed
   decisions only when their facts change.
5. If work cannot proceed, set `status: BLOCKED` and record the concrete
   blocker and its evidence. Return to `ACTIVE` only after evidence shows the
   blocker is resolved.
6. When the goal is achieved, mark all achieved steps, set `status: COMPLETE`,
   set the next action to `None`, and retain the file. Never silently delete a
   completed run.

Keep the file compact. Do not copy conversation transcripts, broad repository
context, validation logs, worklog prose, or speculative future work into it.
Never invent completed validation, commits, decisions, links, or progress.
