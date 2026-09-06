# AI Engineering Worklog

This document records how AI tooling was used during
the development of Coffee-Driven Development.

For each meaningful AI-assisted task I record:
- tool and model
- reasoning level
- delegated task
- human decisions
- validation
- friction / failures
- harness improvements

## 2026-09-06 — Initial architecture exploration

### Harness

Tool: Codex
Model: GPT-5.6 Terra
Reasoning: Medium
Mode: Plan
Task type: architecture exploration
Risk level: low

### Model selection

The task was read-only, well-scoped and low-risk. GPT-5.6 Terra with Medium
reasoning was selected because it required structured architecture exploration
but did not justify a stronger and more expensive implementation model. The
model-routing principle was to use the lowest-cost model that can reliably
complete the task and escalate based on ambiguity, risk, or observed failure.

### Goal

Inspect the initial Coffee-Driven Development repository and propose the
smallest reasonable v0.1 architecture.

### AI responsibility

- Inspected repository documentation and structure.
- Proposed the minimal package structure and dependency strategy.
- Identified unnecessary abstractions; separated CLI, domain, and future
  storage responsibilities; and identified assumptions, open questions, and
  possible future Skill candidates without creating them.

### Human responsibility

The human remained responsible for final architecture approval, project scope,
accepting or rejecting abstractions, product decisions, permission-sensitive
actions, and deciding when implementation could begin.

### Outcome

The AI proposed Python 3.12+, a src-layout package with `cli.py`, `domain.py`,
and `storage.py`, focused tests, local JSONL-style persistence, argparse, zero
runtime dependencies where practical, pytest, ruff, and mypy. Service layers,
repository interfaces, and dependency-injection infrastructure were considered
unnecessary for the current scope. This architecture was proposed only; it had
not yet been implemented.

### Validation

No implementation occurred. No code validation was required.

### Friction / failure

Git inspection was affected by Git's safe-directory / dubious-ownership
protection.

### Harness change

None. This was still primarily a prompt-driven workflow.

### Lesson learned

The project should stay deliberately small and avoid abstractions justified
only by hypothetical future requirements.

## 2026-09-06 — Engineering foundation implementation

### Harness

Tool: Codex
Model: GPT-5.6 Sol
Reasoning: Medium
Mode: Implementation
Task type: engineering foundation implementation
Risk level: low-medium

### Model selection

GPT-5.6 Sol with Medium reasoning was selected because this was a normal
multi-file implementation task with clear acceptance criteria. It required
stronger coding capability than the earlier planning session but did not
justify the most expensive model.

### Goal

Create the minimal typed Python engineering foundation without implementing
actual coffee-tracking behavior.

### AI responsibility

- Inspected repository instructions and structure.
- Created the Python packaging foundation, initial CLI boundary, and initial
  CLI test.
- Configured Hatchling, pytest, ruff, mypy, and the `cdd` console entry point.
- Validated the foundation and verified that product functionality was absent.

### Files changed

- `pyproject.toml`
- `Makefile`
- `src/cdd/__init__.py`
- `src/cdd/cli.py`
- `tests/test_cli.py`

### Human responsibility

The human remained responsible for architecture, project scope, product
decisions, accepting generated changes, evaluating tooling choices, and final
merge.

### Outcome

The minimal typed Python engineering foundation was created without
coffee-tracking behavior.

### Validation

- `uv run --extra dev pytest` — passed, 1 test.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed.
- `uv run --extra dev cdd --help` — passed.

`make check` could not execute because GNU Make was not installed on the
Windows host. Its underlying test, lint, and type-check commands were executed
directly and passed.

### Friction / failure

- Git safe-directory / ownership issue.
- GNU Make was unavailable on the Windows host.
- The default uv cache path was unusable in the execution environment and
  required a repository-local workaround.

### Harness change

Initial repeatable quality checks, pytest / ruff / mypy configuration, and a
Makefile wrapper for the quality commands were introduced.

### Lesson learned

Host-level developer tools cannot be assumed to exist, so validation should
eventually become explicitly cross-platform.

## 2026-09-06 — Repository housekeeping and harness roadmap refinement

### Harness

Tool: ChatGPT
Model: GPT-5.6 Sol
Reasoning: not recorded
Mode: advisory
Task type: harness refinement
Risk level: low

### Model selection

The model was used for repository review, design discussion, and refinement of
the AI engineering workflow. Reasoning level was not explicitly recorded and
is not inferred.

### Goal

Review the early repository state after the first Codex implementation and
simplify the harness before introducing reusable Skills.

### AI responsibility

ChatGPT reviewed the repository through the GitHub integration; identified the
need to complete `.gitignore`; identified GNU Make as environment-specific
friction; recommended explicit cross-platform `uv` validation; distinguished
deterministic commands from reasoning-heavy Skills; helped restructure
`docs/IMPLEMENTATION_PLAN.md`; and recommended progressive Skill creation.
It provided analysis and recommendations, not the local edits in the commits.

### Human responsibility

The human evaluated those recommendations and chose to update `.gitignore`,
remove the Makefile, add validation commands to `AGENTS.md`, update
`docs/IMPLEMENTATION_PLAN.md`, and commit and push the changes.

### Outcome

GNU Make is no longer part of the canonical local workflow. Validation uses
direct cross-platform `uv` commands; local environments and caches are ignored;
the implementation plan is the repository roadmap; and only genuinely repeated
workflows should become Skills.

### Validation

This was primarily repository housekeeping and documentation work. No code
validation is recorded.

### Friction / failure

The previously observed GNU Make incompatibility motivated the simplification.

### Harness change

Validation moved from a Make-based wrapper to explicit `uv` commands,
`AGENTS.md` gained persistent validation instructions, repository hygiene
improved, and the project gained a structured implementation/harness roadmap.

### Lesson learned

Deterministic repeated commands belong in commands or scripts; reusable Skills
should encode workflows that benefit from agent reasoning or orchestration.

## 2026-09-06 — Harness baseline and reusable session logging

### Harness

Tool: Codex
Model: GPT-5.6 Terra
Reasoning: Medium
Mode: Implementation
Task type: harness improvement
Risk level: low

### Model selection

This task was primarily repository documentation and workflow configuration. It
required structured reasoning and careful preservation of project history, but
did not require complex product implementation or the strongest available
model.

### Goal

Backfill credible historical AI usage records and move repeated session logging
instructions into the first reusable repository Skill.

### AI responsibility

- Inspected repository state, Git history, relevant diffs, and Skill
  conventions.
- Backfilled the historical worklog entries.
- Created `record-ai-session` and minimally routed future sessions through it
  from `AGENTS.md`.
- Validated the Skill and verified the resulting changes.

### Human responsibility

The human decided to introduce the first Skill only after repeated logging
behavior was observed, selected the model and reasoning level, remains
responsible for accepting the harness design, and remains responsible for
committing or merging these changes unless explicitly delegated.

### Outcome

Historical AI-assisted sessions were backfilled; `record-ai-session` became
the first reusable repository Skill; `AGENTS.md` routes meaningful completed
work into the logging workflow; and application/product code remained
unchanged.

### Files changed

- `AI_WORKLOG.md`
- `AGENTS.md`
- `.agents/skills/record-ai-session/SKILL.md`

### Validation

The `record-ai-session` Skill passed its format validator. Git history and
diffs were inspected to verify the historical facts and resulting scope.

### Friction / failure

The Skill validator required elevated host-Python access because the sandbox
could not start the Python launcher.

### Harness change

Session logging moved from repeated task-prompt instructions into a reusable
repository capability. This marks the transition from primarily prompt-driven
behavior toward a workflow-aware harness.

### Lesson learned

Repeated instructions that represent stable, meaningful workflow behavior are
good candidates for extraction into reusable harness capabilities.

## 2026-09-06 — Safe Git delivery and pull-request automation

### Harness

Tool: Codex
Model: GPT-5.6 Terra
Reasoning: Medium
Mode: Implementation
Task type: Git delivery harness improvement
Risk level: low-medium

### Model selection

This task concerned repository workflow configuration, Git lifecycle,
pull-request preparation, and reusable agent instructions. It required careful
sequencing and safety checks but did not require complex product implementation
or the strongest available model.

### Goal

Introduce a reusable, safety-bounded workflow that converts completed
validated local changes into review-ready GitHub pull requests.

### AI responsibility

- Inspected repository state, Git history, remotes, and available GitHub
  capabilities.
- Created and validated the `prepare-pull-request` Skill.
- Updated repository routing and roadmap documentation.
- Created, committed, and pushed `chore/pr-automation`.
- Created draft PR #1 and verified that later commits were pushed to it.

### Human responsibility

The human decided to automate Git delivery, approved branch-based delivery,
retained final review and merge authority, and selected the model and
reasoning level.

### Outcome

The repository gained a dedicated-branch, validation-gated delivery workflow
with explicit staging, push, draft-PR creation, and one worklog update. Draft
PR #1 is open at
`https://github.com/aneq05/coding_assistant_demo_repo/pull/1`; it remains
human-controlled. Application and test code remained unchanged.

### Files changed

- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `.agents/skills/prepare-pull-request/SKILL.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py .agents/skills/prepare-pull-request` — passed.
- Complete and staged diffs were inspected.
- `git diff --check` — passed.
- The branch was pushed and draft PR #1 was created successfully.

No code validation was run because this session changed only harness and
documentation files.

### Friction / failure

The local GitHub CLI could not read its configuration in the sandbox. The
authenticated GitHub connector was available and completed draft-PR creation.

### Harness change

Git delivery moved from manual human commit/push steps into a reusable,
validation-gated repository workflow.

### Lesson learned

Automation is safer when delivery, review, and merge remain separate stages
with different permission boundaries.
