# AI model usage

This table summarizes recorded AI-assisted repository work. It is derived from
`AI_WORKLOG.md` and the documented Phase 6 handoff. Missing metadata is kept as
`not recorded` rather than inferred.

| Task | Tool / model | Reasoning | Why | Phase |
| --- | --- | --- | --- | --- |
| Initial architecture exploration | Codex / GPT-5.6 Terra | Medium | Read-only, structured architecture exploration did not require a stronger implementation model. | 1 |
| Engineering foundation | Codex / GPT-5.6 Sol | Medium | A clear multi-file implementation needed reliable coding capability. | 2 |
| Repository housekeeping and roadmap refinement | ChatGPT / GPT-5.6 Sol | not recorded | Repository review and advisory workflow refinement. | 2–3 |
| Session-logging Skill | Codex / GPT-5.6 Terra | Medium | Bounded documentation and workflow configuration. | 3 |
| Pull-request delivery Skill | Codex / GPT-5.6 Terra | Medium | Git lifecycle work needed careful sequencing rather than complex product coding. | 3.5 |
| TDD and review-feedback workflows | Codex / GPT-5.6 Sol | Medium | Interacting engineering workflows and live review feedback needed stronger implementation reasoning. | 3.75 |
| Pull-request quality gate | Codex / GPT-5.6 Terra | Medium | Bounded PR metadata and review-state validation. | 3.8 |
| Mergeability feedback correction | Codex / GPT-5 | not recorded | not recorded | 3.8 |
| First product feature | Codex / GPT-5.6 Sol | Medium | A scoped behavioral feature was implemented through TDD. | 4 |
| CI and repository synchronization | Codex / GPT-5.6 Sol | Medium | Multi-file workflow work combined Git safety, CI, and external evidence. | 4.5 |
| Copilot review configuration | Codex / GPT-5.6 Terra | Medium | A bounded, documentation-sensitive harness configuration task. | 4.6 |
| Review-freshness finalization | Codex / not recorded | not recorded | not recorded | 4.6 |
| Persistence and CI-triage foundation | Codex / GPT-5.6 Sol | Medium | A typed product feature and bounded agent configuration required normal implementation strength. | 5 / 4.7 |
| Product MVP completion | Codex / GPT-5.6 Sol; Cursor / not recorded | Medium for Codex; not recorded for Cursor | The feature began as a clear multi-file product task in Codex; work continued in Cursor after Codex usage limits were reached while retaining the same validation and PR workflow. | 6 / 6.5 |

Tool changes are recorded as execution facts, not as evidence that one tool or
model produced better results than another.
