---
name: record-ai-session
description: Append a concise, factually grounded AI engineering-session entry to AI_WORKLOG.md after meaningful work; do not use for trivial interactions.
---

# Record AI session

Use after meaningful AI-assisted engineering work: repository changes,
architecture or harness decisions, meaningful validation or debugging, code
review, external integrations, or a project decision that changes future work.
Do not use for casual discussion, simple explanations, or clarifications with
no meaningful outcome.

1. Inspect the current session, changed files, relevant validation, and Git
   history where needed. Treat user statements as facts only when explicit.
2. Record date, tool, model, reasoning, mode, task type, and risk when known.
   Write `not recorded` for unknown model metadata; never infer it.
3. Append—never overwrite—an entry in chronological order. Keep it concise and
   distinguish AI recommendations, AI execution, and human decisions/actions.
4. Include applicable sections: Harness, Model selection, Goal, AI
   responsibility, Human responsibility, Outcome, Files changed, Validation,
   Friction / failure, Harness change, and Lesson learned.
5. Record only supported facts. Do not invent validation, failures, metadata,
   decisions, actions, harness changes, or lessons.
6. Inspect the resulting `AI_WORKLOG.md` diff, verify earlier entries were not
   changed unintentionally, and summarize the appended entry.
