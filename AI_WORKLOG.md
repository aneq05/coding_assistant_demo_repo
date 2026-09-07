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

## 2026-09-06 — Engineering workflow, TDD and review-feedback automation

### Harness

Tool: Codex
Model: GPT-5.6 Sol
Reasoning: Medium
Mode: Implementation
Task type: engineering workflow and review-feedback automation
Risk level: medium

### Model selection

This task modified interacting engineering workflows, project-specific
guidance, and GitHub review feedback. It required stronger implementation and
integration reasoning than simple documentation work, but not the most
expensive model.

### Goal

Prepare the repository for Phase 4 with reusable test-first development and
critical review-feedback validation workflows.

### AI responsibility

- Inspected PR #1, its complete diff, Copilot review, and review thread.
- Refined `prepare-pull-request` for workflow-level delivery authorization and
  ready-for-review completion.
- Added Python and testing guidance plus `develop-feature-tdd` and
  `validate-review-feedback`.
- Classified and corrected the valid roadmap findings, replied to, and resolved
  the addressed Copilot thread.
- Validated the Skills and pushed the corrections to PR #1.

### Human responsibility

The human chose TDD as the development methodology, chose to automate normal
Git delivery, retained architecture, scope, and merge authority, and retains
the final PR merge decision.

### Outcome

The repository gained reusable test-first feature development and critical
review-feedback validation workflows. PR #1 now contains the justified
corrections; no Phase 4 product behavior was implemented.

### Files changed

- `.agents/skills/prepare-pull-request/SKILL.md`
- `.agents/skills/develop-feature-tdd/SKILL.md`
- `.agents/skills/validate-review-feedback/SKILL.md`
- `docs/engineering/python-guidelines.md`
- `docs/engineering/testing-strategy.md`
- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py` passed for `prepare-pull-request`,
  `develop-feature-tdd`, and `validate-review-feedback`.
- Complete and staged diffs were inspected.
- `git diff --check` passed.
- PR #1 review data and the final pushed branch were verified.

No code validation was run because this session changed only harness and
documentation files.

### Friction / failure

None observed.

### Harness change

The repository gained a reusable test-first development workflow and a
separate critical feedback-validation workflow.

### Lesson learned

Implementation, delivery, review, and review-feedback validation should remain
separate capabilities so one agent output is not treated as self-validating.

## 2026-09-07 — Pull-request quality gate

### Harness

Tool: Codex
Model: GPT-5.6 Terra
Reasoning: Medium
Mode: Implementation
Task type: pull-request quality-gate improvement
Risk level: low-medium

### Model selection

This task focused on repository workflow validation, review state, and PR
metadata consistency. It required structured reasoning and careful GitHub
inspection, but not product implementation or the strongest available model.

### Goal

Introduce a reusable final PR validation capability and clean up the current
harness PR before Phase 4.

### AI responsibility

- Inspected PR #1 metadata, complete diff, review submissions, and threads.
- Corrected delivery, roadmap, and future-phase terminology based on validated
  review findings.
- Updated PR #1 title and description to match its final scope.
- Created and validated `validate-pull-request` and applied its readiness
  checks to PR #1.

### Human responsibility

The human chose to add a pre-merge quality gate, retained final merge
authority, and approved the validation criteria through the task request.

### Outcome

PR #1 gained consistent metadata, resolved review findings, and a reusable
pre-merge readiness workflow. No Phase 4 product behavior was implemented.

### Files changed

- `.agents/skills/prepare-pull-request/SKILL.md`
- `.agents/skills/validate-pull-request/SKILL.md`
- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py` passed for `prepare-pull-request` and
  `validate-pull-request`.
- Complete and staged diffs were inspected.
- `git diff --check` passed.
- PR metadata and review-thread state were inspected directly through GitHub.

No code validation was run because this session changed only harness and
documentation files.

### Friction / failure

None observed.

### Harness change

Pull requests now have a reusable readiness check after delivery and
review-feedback processing.

### Lesson learned

Automation needs validation not only for code, but also for workflow state,
metadata, review resolution, and repository consistency.

## 2026-09-07 — Mergeability review-feedback correction

### Harness

Tool: Codex
Model: GPT-5
Reasoning: not recorded
Mode: Implementation
Task type: pull-request review-feedback validation
Risk level: low

### Model selection

Not recorded.

### Goal

Validate and address the latest Codex finding on PR #1 about the pull-request
quality gate's missing mergeability/conflict check.

### AI responsibility

- Read PR #1 metadata, review submissions, and review threads.
- Classified the finding as valid and made the minimal Skill correction.
- Validated the changed Skill and inspected its diff before delivery.

### Human responsibility

The human requested the feedback workflow and retains final merge authority.

### Outcome

The quality gate now blocks confirmed unmergeable or conflicted PRs, reports
unknown mergeability explicitly, and requires mergeability alignment for
`CLEAR`. No product behavior or Phase 4 work was added.

### Files changed

- `.agents/skills/validate-pull-request/SKILL.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py .agents/skills/validate-pull-request` passed.
- `git diff --check` passed.
- PR #1 metadata showed `mergeable: true` before the correction.

No code validation was run because this session changed only harness files.

### Friction / failure

None observed.

### Harness change

The pull-request quality gate now distinguishes confirmed merge conflicts from
unknown mergeability and cannot return `CLEAR` for a known unmergeable PR.

### Lesson learned

Final pull-request readiness must include GitHub's mergeability state, not
only branch, validation, and review metadata.

## 2026-09-07 — First product feature through TDD

### Harness

Tool: Codex
Model: GPT-5.6 Sol
Reasoning: Medium
Mode: Implementation
Task type: first TDD product feature
Risk level: medium

### Model selection

GPT-5.6 Sol with Medium reasoning matches the repository's routing for normal
implementation and the Phase 4 roadmap choice.

### Goal

Implement `cdd drink <drink>` for espresso, americano, and cappuccino with
deterministic caffeine values, clear unsupported-input behavior, and no
persistence.

### AI responsibility

- Synchronized from the latest merged `main` and created
  `feature/drink-command`.
- Derived observable CLI and domain acceptance criteria.
- Wrote domain and CLI tests before production behavior, confirmed RED, then
  implemented the minimal CLI-to-domain change and confirmed GREEN.
- Removed three ignored Python cache artifacts from Git tracking.
- Ran the complete local quality gate, inspected the diff, updated the roadmap,
  and created draft PR #2.

### Human responsibility

The human specified the supported drinks, caffeine constants, feature scope,
architecture boundary, and TDD/delivery workflows, and retains final merge
authority.

### Outcome

`cdd drink` now reports espresso at 80 mg, americano at 120 mg, and cappuccino
at 75 mg. Unsupported drinks exit unsuccessfully with a clear error. Phase 4
is complete and Phase 5 remains planned.

### Files changed

- `src/cdd/domain.py`
- `src/cdd/cli.py`
- `tests/test_domain.py`
- `tests/test_cli.py`
- `docs/IMPLEMENTATION_PLAN.md`
- `src/cdd/__pycache__/__init__.cpython-312.pyc` (removed from tracking)
- `src/cdd/__pycache__/cli.cpython-312.pyc` (removed from tracking)
- `tests/__pycache__/test_cli.cpython-312-pytest-9.1.1.pyc` (removed from tracking)
- `AI_WORKLOG.md`

### Validation

- RED: `tests/test_cli.py` produced four expected failures because `drink` was
  unrecognized or lacked the required unsupported-drink error; the existing
  help test passed.
- RED: `tests/test_domain.py` failed collection because the required
  `cdd.domain` module had not yet been implemented.
- GREEN: `uv run --extra dev pytest tests/test_domain.py tests/test_cli.py -q`
  passed with 9 tests.
- `uv run --extra dev pytest` passed with 9 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed with no issues in 5 source files.
- Supported-drink smoke tests printed the specified names and caffeine values;
  unsupported `latte` exited 2; `cdd --help` succeeded.
- `git diff --check` passed, and the complete staged diff was inspected.

### Friction / failure

The first targeted test attempt could not initialize uv's user cache under the
sandbox. The same commands ran successfully with the host environment; the
cache error was not counted as RED.

### Harness change

This was the first product feature implemented through `develop-feature-tdd`.
The Skill was sufficient, and no workflow changes were needed.

### Lesson learned

Separating domain and CLI tests made the RED evidence distinguish missing
business behavior from missing command parsing while preserving a small design.

## 2026-09-07 — CI and repository synchronization

### Harness

Tool: Codex
Model: GPT-5.6 Sol
Reasoning: Medium
Mode: Implementation
Task type: CI and repository synchronization harness improvement
Risk level: medium

### Model selection

GPT-5.6 Sol with Medium reasoning matched a multi-file workflow task requiring
Git safety, CI implementation, external validation, and evidence inspection.

### Goal

Add safe repository synchronization, independent current-HEAD GitHub Actions
validation, persistent CI report artifacts, a human-readable summary, and CI
and review freshness checks before Phase 5.

### AI responsibility

- Verified PR #2 was merged, no PR was open, synchronized local `main` to remote
  SHA `848b434`, and created `chore/ci-and-sync` without deleting old branches.
- Created `sync-repository`, composed it from `develop-feature-tdd`, and added a
  concise repository routing rule.
- Added the CI workflow and current-HEAD CI/review rules to
  `validate-pull-request`.
- Ran local validation, delivered draft PR #3, diagnosed the initial CI failure,
  applied the focused action-version correction, and inspected successful jobs
  and artifacts.

### Human responsibility

The human chose independent CI validation, retained architecture and final
merge authority, and chose CI artifacts instead of committed report files.

### Outcome

Phase 4.5 is complete. GitHub Actions independently runs pytest, ruff, and mypy,
publishes a validation summary, and uploads SHA-named reports. CI runs #2 and #3
passed for heads `4548558` and `4438fa4`; the worklog commit creates one final
HEAD that must be revalidated before PR clearance.

### Files changed

- `.agents/skills/sync-repository/SKILL.md`
- `.agents/skills/develop-feature-tdd/SKILL.md`
- `.agents/skills/validate-pull-request/SKILL.md`
- `.github/workflows/ci.yml`
- `.gitignore`
- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py` passed for `sync-repository`, `develop-feature-tdd`, and
  `validate-pull-request`.
- `uv run --extra dev pytest` passed with 9 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed with no issues in 5 source files.
- `git diff --check` passed and the complete diff was inspected.
- CI run #2 passed all required steps for SHA `4548558c67de8d14efc70817e2977be8da14a40f`.
- Its artifact `validation-reports-4548558c67de8d14efc70817e2977be8da14a40f`
  contained `pytest.xml`, `ruff.txt`, and `mypy.txt`; the reports showed 9
  passing tests, clean ruff, and clean mypy.
- CI run #3 passed all required steps and uploaded a current-SHA artifact for
  roadmap head `4438fa4f8362e3dacd3a0d843547147dd3d944fe`.

### Friction / failure

- `actionlint` was not installed, so no local actionlint result was claimed.
- CI run #1 failed during job setup because the initially selected floating
  `astral-sh/setup-uv@v9` ref did not exist. No validator ran and no artifact was
  produced. Live GitHub release data identified available exact action tags;
  the corrected workflow passed without weakening validation.

### Harness change

Validation is no longer only self-reported by the implementation agent. GitHub
now independently reruns deterministic checks in a clean CI environment.

### Lesson learned

Increasing agent autonomy should be paired with independent validation and
freshness checks.

## 2026-09-07 — Context-aware Copilot Code Review configuration

### Harness

Tool: Codex
Model: GPT-5.6 Terra
Reasoning: Medium
Mode: Implementation
Task type: GitHub Copilot review customization
Risk level: low-medium

### Model selection

GPT-5.6 Terra with Medium reasoning was selected for a bounded harness
configuration task requiring current GitHub documentation, repository context,
and careful separation from existing review-validation workflows.

### Goal

Configure repository-specific GitHub Copilot Code Review context without
changing product behavior or enabling broad credentials.

### AI responsibility

- Synchronized from merged Phase 4.5 on remote `main` at `a3802a7` and created
  `chore/context-aware-copilot-review`.
- Verified the supported Copilot instruction and review-Skill locations in
  current GitHub documentation.
- Added the review-finding Skill, concise Copilot instructions, and Phase 4.6
  roadmap entry; created draft PR #4.

### Human responsibility

The human authorized the scope and retains repository settings, review,
architecture, and final merge authority.

### Outcome

PR #4 is the dedicated Phase 4.6 delivery. It is intentionally limited to
review configuration and remains separate from `validate-review-feedback` and
`validate-pull-request`. No product behavior, GitHub MCP server configuration,
or broad personal access token was added.

### Files changed

- `.github/skills/code-review/SKILL.md`
- `.github/copilot-instructions.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`

### Validation

- Local Skill format validation passed for `.github/skills/code-review`.
- `git diff --check` passed.
- `uv run --extra dev pytest` passed with 9 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed.

Current-HEAD CI and the requested Copilot review will be evaluated after this
worklog commit creates the final review head; no outcome is recorded before it
exists.

### Friction / failure

The installed GitHub CLI does not provide the preview `gh skill` command, so
its `publish --dry-run` validation was unavailable.

### Harness change

The repository now has review-focused Copilot context that requests
current-HEAD evidence and avoids duplicate or speculative findings.

### Lesson learned

Review configuration should distinguish explicit tool evidence from assumptions
about what a reviewer used.

## 2026-09-07 — Phase 4.6 review-freshness finalization

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: pull-request review-freshness harness improvement
Risk level: low

### Goal

Finalize Phase 4.6 using evidence from PR #4 and make final-review freshness
reliable when GitHub omits a reviewed commit SHA.

### AI responsibility

- Synchronized the clean task branch and verified local `main` matched
  `origin/main` at `a3802a7`.
- Verified the post-head Copilot review, resolved review threads, and
  current-head CI evidence for the prior PR #4 head.
- Added an ordered exact-SHA and temporal fallback to
  `validate-pull-request`, preserving explicit-SHA preference and CI and
  actionable-feedback requirements.
- Recorded Phase 4.6 completion with configuration-exercised evidence and
  separate UNKNOWN attribution fields.

### Human responsibility

The human specified the temporal evidence policy, authorized Phase 4.6
completion criteria, and retains final merge authority.

### Outcome

PR #4 remains the existing, unmerged delivery. The readiness workflow can now
report `TEMPORAL` review-freshness evidence when GitHub omits a reviewed SHA;
it does not present that evidence as `EXACT_SHA`. Broad GitHub MCP integration
remains planned.

### Files changed

- `.agents/skills/validate-pull-request/SKILL.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`

### Validation

- `quick_validate.py .agents/skills/validate-pull-request` passed.
- `git diff --check` passed.
- `uv run --extra dev pytest` passed with 9 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed.

### Friction / failure

GitHub did not expose a reviewed-commit SHA for the Copilot review, requiring
the documented temporal fallback.

### Harness change

Final review freshness now has a conservative, evidence-labeled fallback for
review systems that expose timestamps but not reviewed commit SHAs.

### Lesson learned

When external systems omit exact provenance, a bounded temporal rule can
preserve safety only when it also proves the branch did not move afterward.
