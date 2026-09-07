---
name: create-feature-issue
description: Turn a short feature goal into one scoped GitHub Issue; do not use for implementation or multi-Issue planning.
---

# Create feature Issue

Turn the user's feature goal into one concise, actionable GitHub Issue. Do not
begin implementation, edit product code, or create more than one Issue unless
the user explicitly requests multiple Issues.

1. Read `AGENTS.md`, the relevant roadmap sections in
   `docs/IMPLEMENTATION_PLAN.md`, and any repository guidance needed to define
   the feature's boundaries.
2. Use the available GitHub integration or MCP to search open Issues for an
   equivalent or substantially overlapping request. If one exists, return its
   number and URL, explain the overlap briefly, and do not create a duplicate.
3. Derive the smallest clear requirement supported by the user's goal and
   repository context. Do not make architectural, scope, or product decisions
   that require human approval; ask for direction when one is necessary.
4. Prepare an Issue with exactly these sections:

   ```markdown
   ## Goal
   ## Requirements
   ## Acceptance criteria
   ## Constraints
   ## Out of scope
   ```

5. Create that single Issue through the available GitHub integration or MCP
   only when its write capability is available and authorized. Return the Issue
   number and URL after creation.
6. If GitHub Issue write capability is unavailable, return the prepared title
   and body instead. State that no Issue was created; never imply otherwise.
