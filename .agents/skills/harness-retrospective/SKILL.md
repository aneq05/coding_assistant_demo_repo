---
name: harness-retrospective
description: Analyze real AI-assisted engineering evidence for repository-harness improvements; use for periodic read-only retrospectives, not implementation.
---

# Run a harness retrospective

Evaluate whether the repository harness should change, using only evidence that
is available in the current task. This is a read-only audit: do not modify
product files, harness files, GitHub state, permissions, or configuration, and
do not implement the recommendations.

Inspect relevant evidence from `AI_WORKLOG.md`, `AGENTS.md`, current repository
Skills and custom agents, `docs/IMPLEMENTATION_PLAN.md`, and, through GitHub MCP
when available, Issues, pull requests, review history, merge conflicts, and CI.
Also look for unavailable evidence, repeated human intervention or prompt
instructions, model-routing friction, and abandoned or resumed AI run state.
State which sources and time range were actually inspected.

For each candidate observation:

1. Label its confidence as `OBSERVED`, `INFERRED`, or
   `NOT ENOUGH EVIDENCE`. Never present inference as fact or invent a failure.
2. Classify it as one or more of: repeated friction, unnecessary manual
   repetition, unreliable agent behavior, missing repository context,
   duplicated capability, excessive context consumption, permission/tooling
   limitation, or unnecessary harness complexity.
3. Call it repeated only when multiple distinct occurrences support that
   conclusion; otherwise explicitly call it one-off.
4. Check whether an existing instruction, Skill, agent, document, deterministic
   command, or integration already addresses it. A command's existence alone
   does not justify a Skill.

Return only meaningful observations. For each, report:

- severity: `LOW`, `MEDIUM`, or `HIGH`
- confidence label
- category
- evidence, with concrete source references
- repeated or one-off
- cost or risk
- existing capability involved
- smallest recommended harness improvement

End with evidence gaps and an overall recommendation. `DO NOTHING` is an
explicitly valid recommendation when the current harness is sufficient or the
evidence does not justify added complexity. Never recommend broader permissions
without demonstrated need.
