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

## 2026-09-07 — Local persistence and CI triage-agent foundation

### Harness

Tool: Codex
Model: GPT-5.6 Sol
Reasoning: Medium
Mode: Implementation
Task type: product development + bounded harness extension
Risk level: medium

### Model selection

GPT-5.6 Sol with Medium reasoning was selected because the iteration combined
a normal typed Python feature with a bounded, documentation-sensitive GitHub
agent configuration and did not require an architecture change.

### Goal

Complete Phase 5 with append-only local JSONL coffee-event persistence and add
the Phase 4.7 repository CI-triage agent configuration for future natural CI
failures.

### AI responsibility

- Verified Phase 4.6 was merged, synchronized local and remote `main` at
  `c15b8b6`, and created `feature/local-persistence-and-ci-triage`.
- Verified the current GitHub custom-agent profile format and built-in
  least-privilege repository context from official GitHub documentation.
- Added a manually selected CI-triage profile without broad credentials or
  merge authority.
- Drove Phase 5 through a real test-first cycle, then added the typed event,
  JSONL storage, CLI orchestration, tests, and roadmap updates.
- Created draft PR #5 from feature commit `c253286`.

### Human responsibility

The human approved JSONL and the CLI/domain/storage boundaries, defined the
agent safety and scope constraints, retains authority over architecture,
dependencies, disputed review feedback, and final merge, and must merge the
PR before the custom agent can become available from the default branch.

### Outcome

Successful drink commands append one event to `~/.cdd/history.jsonl` with an
aware UTC ISO 8601 timestamp, drink type, and caffeine amount. Unsupported
drinks append nothing and the existing human-readable output is unchanged.
The CI-triage configuration is created and schema-checked but was not exercised
or claimed available on the default branch.

### Files changed

- `.github/agents/ci-triage.agent.md`
- `AGENTS.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `src/cdd/cli.py`
- `src/cdd/domain.py`
- `src/cdd/storage.py`
- `tests/test_cli.py`
- `tests/test_domain.py`
- `tests/test_storage.py`
- `AI_WORKLOG.md`

### Validation

- RED: the focused suite failed to collect because the not-yet-implemented
  `CoffeeEvent` persistence contract was absent.
- GREEN: the focused suite passed all 14 domain, storage, and CLI tests.
- `uv run --extra dev pytest --basetemp=.pytest-phase5-full` passed with 14
  tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed with no issues in 7 source files.
- `git diff --check` passed.
- An isolated-path CLI smoke test produced three independently parseable JSON
  lines for espresso, americano, and cappuccino; unsupported latte appended no
  event.
- Official-schema inspection passed for the custom-agent path, suffix,
  frontmatter, and tool aliases; no supported local automated validator was
  available.

Current-head CI and review evidence remain to be collected after this worklog
commit creates the final PR head.

### Friction / failure

The exact pytest command could not access the workstation's pre-existing
`%TEMP%\pytest-of-ankap` directory. A task-scoped `--basetemp` changed only
pytest temporary-file placement and allowed the complete suite to pass.

### Harness change

The repository now includes a manually invoked, narrowly bounded CI-failure
diagnostic profile. It uses built-in read-only GitHub MCP repository access and
explicitly preserves tests, linting, typing, workflow safeguards, and human
merge control.

### Lesson learned

A custom CI agent can be installed safely before its first real use when its
availability and exercise status are recorded separately from format evidence.

## 2026-09-07 — Product MVP completion

### Harness

Tool: Codex and Cursor
Model: GPT-5.6 Sol for Codex; not recorded for Cursor
Reasoning: Medium for Codex; not recorded for Cursor
Mode: Implementation
Task type: product MVP completion
Risk level: medium

### Model selection

GPT-5.6 Sol with Medium reasoning was selected for a clear multi-file product
implementation with deterministic acceptance criteria. After Codex usage limits
were reached, part of the work continued through Cursor; its model and reasoning
level were not recorded. The same repository validation and pull-request
workflow remained in use across the tool handoff.

### Goal

Complete the Coffee-Driven Development MVP with persisted history reading,
local-day status, recent statistics, Rich terminal presentation, and an
interactive mode over the same product behavior.

### AI responsibility

- Synchronized from merged PR #5, created `feature/status-history-stats`, and
  translated Phase 6 and 6.5 into focused storage, domain, CLI, presentation,
  and interaction tests.
- Implemented the typed JSONL reader, pure status/statistics calculations,
  Rich presentation, direct commands, and interactive orchestration. Work was
  split between Codex and Cursor after the Codex usage limit was reached.
- Audited PR #6, classified four Codex review findings as valid, and added
  post-prompt clock refresh plus rule-aware per-timestamp local conversion with
  deterministic injection seams.
- Completed the README, roadmap, and model-usage evidence and ran local
  validation, package build, and isolated command smoke tests.

### Human responsibility

The human specified the product behavior, approved Rich as the only new runtime
dependency, directed the tool handoff and finalization, retained architecture
and scope authority, and retains the final merge decision.

### Outcome

`cdd history`, `cdd status`, `cdd stats`, and `cdd interactive` now reuse the
existing JSONL history and pure domain calculations. Phase 6, Phase 6.5, and
Milestone A are complete. Git activity, Refactor Risk, MCP/Figma work, and the
independent-review phase remain incomplete.

### Files changed

- `.gitignore`
- `README.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/ai/model-usage.md`
- `pyproject.toml`
- `uv.lock`
- `src/cdd/cli.py`
- `src/cdd/domain.py`
- `src/cdd/presentation.py`
- `src/cdd/storage.py`
- `tests/test_cli.py`
- `tests/test_domain.py`
- `tests/test_presentation.py`
- `tests/test_storage.py`
- `AI_WORKLOG.md`

### Validation

- Initial RED: domain/storage tests failed collection because `calculate_stats`
  and `InvalidHistoryError` did not exist; presentation tests failed collection
  because `cdd.presentation` did not exist.
- Review RED: focused DST-localization and interactive-clock tests failed with
  unsupported `to_local` and `clock` arguments on reviewed head `2ba3fe3`; a
  later post-prompt clock regression reproduced a finding on head `4655c60`.
- Review GREEN: all focused regression tests passed after the corrections.
- `uv run --extra dev pytest` passed with 65 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed with no issues in 9 source files.
- `git diff --check` passed.
- `uv build` produced and inspected a source distribution and wheel containing
  all five package modules and the `cdd` entry point.
- An isolated temporary-history smoke test passed for all three drinks, status,
  history, seven-day stats, and interactive add/status/history/stats/exit.
- GitHub Actions passed for the pre-finalization PR head `2ba3fe3`; the final
  correction head did not yet exist when this entry was written, so no later CI
  result is claimed here.

### Friction / failure

- Codex usage limits required a handoff to Cursor during implementation.
- The workstation's default pytest temporary root was inaccessible; the
  repository-local pytest base directory avoided real-home access.
- An early Windows CP1250 smoke test could not encode Unicode chart blocks. The
  UTF-8 console configuration corrected it, and the final smoke test passed.
- Copilot could not review PR #6 because the requesting user had reached its
  review quota.

### Harness change

No Skill was added or changed. Pytest now uses a repository-local ignored base
directory, temporary Phase 6 paths are ignored, and `docs/ai/model-usage.md`
summarizes recorded tool/model routing. The CI Triage Agent was not needed
because current-head CI was green before the final corrections.

### Lesson learned

Time-sensitive local-calendar behavior needs both an injectable clock and an
injectable local-time conversion boundary: one prevents stale interactive time,
and the other preserves operating-system DST rules without adding a dependency.

## 2026-09-07 â€” Feature Issue creation Skill

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: repository Skill creation
Risk level: low

### Goal

Add one repository Skill that turns a short human feature goal into one scoped
GitHub Issue without beginning implementation.

### AI responsibility

- Synchronized repository state, inspected existing Skill conventions and the
  implementation roadmap, and added `create-feature-issue`.
- Validated the Skill structure, created branch `docs/create-feature-issue-skill`,
  and opened PR #7 without creating a GitHub Issue.

### Human responsibility

The human specified the Skill's required Issue structure and boundaries, and
retains review and final-merge authority.

### Outcome

The new Skill searches open Issues before creating one Issue, returns a
prepared body when Issue write access is unavailable, and prohibits
implementation or implicit multi-Issue creation.

### Files changed

- `.agents/skills/create-feature-issue/SKILL.md`
- `AI_WORKLOG.md`

### Validation

- `C:\\Users\\ankap\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py .agents/skills/create-feature-issue` passed.
- `git diff --check` passed for the Skill change.

### Friction / failure

Git fetch initially could not write `.git/FETCH_HEAD` in the sandbox; the
required freshness check succeeded after approved escalation.

### Harness change

Added `create-feature-issue` as a concise, bounded GitHub Issue-authoring
workflow. No product code or GitHub Issue was created.

### Lesson learned

A truthful no-write fallback lets an Issue-authoring workflow remain useful
without assuming external mutation capability.

## 2026-09-07 â€” Feature Issue template

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: GitHub Issue template
Risk level: low

### Goal

Add one concise GitHub Issue Form for scoped feature requests that matches the
repository's feature-Issue workflow.

### AI responsibility

- Synchronized after merged PR #7, reviewed the roadmap and GitHub's Issue
  Form syntax, and added `feature.yml`.
- Validated the YAML with a temporary parser, opened PR #8, and did not create
  a GitHub Issue.

### Human responsibility

The human specified the fields, prohibited product and Skill changes, and
retains review and final-merge authority.

### Outcome

The form requires a short description plus Goal, Requirements, Acceptance
criteria, Constraints, and Out of scope; implementation notes are optional.

### Files changed

- `.github/ISSUE_TEMPLATE/feature.yml`
- `AI_WORKLOG.md`

### Validation

- `npx.cmd --yes js-yaml .github/ISSUE_TEMPLATE/feature.yml` parsed the YAML successfully.
- GitHub's official Issue Form syntax documentation was reviewed.
- `git diff --check` passed for the template change.

### Friction / failure

The local `uv` cache could not initialize because of a Windows cache-path
collision, and the configured Python environment was unavailable. A temporary
non-project YAML parser provided the required validation without changing
dependencies.

### Harness change

Added the repository's first feature Issue Form. No product code, repository
Skill, or GitHub Issue was created.

### Lesson learned

Issue Forms can enforce concise feature scope for humans while preserving the
same headings used by an automation workflow.

## 2026-09-07 — Git activity roadmap clarification

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: roadmap documentation
Risk level: low

### Goal

Define the planned Git activity feature precisely and reconcile roadmap status
with current repository evidence, without implementing product behavior.

### AI responsibility

- Synchronized the default branch, inspected the roadmap, GitHub Actions
  workflow, repository Skills, feature Issue Form, and GitHub capability audit.
- Updated only `docs/IMPLEMENTATION_PLAN.md`, committed `41755e8`, and opened
  draft PR #9.

### Human responsibility

The human defined the Git activity requirements and scope boundaries, and
retains review and final-merge authority.

### Outcome

The roadmap now defines Git activity in `cdd status` as commits today and the
latest commit time, specifies graceful non-repository behavior, prohibits
GitPython, requires Git-history-independent tests, and keeps Refactor Risk out
of scope. It also records completed CI, feature-Issue workflow/template, and
GitHub capability-audit evidence.

### Files changed

- `docs/IMPLEMENTATION_PLAN.md`
- `git diff --check` passed for the roadmap change.
- The relevant repository files were manually inspected; no product code was
  changed.

### Friction / failure

The sandbox initially prevented `git fetch` from writing `.git/FETCH_HEAD`;
the required freshness check completed after approved escalation.

### Harness change

No harness or product-code behavior changed; this was a documentation-only
roadmap clarification.

### Lesson learned

Feature planning is more reliable when implementation constraints and test
isolation are explicit before an Issue is used to begin delivery.

## 2026-09-07 — Feature delivery custom agent

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: GitHub custom-agent configuration
Risk level: low

### Goal

Add one manually invocable custom agent that takes an already-scoped GitHub
Issue through the repository harness to a review-ready pull request.

### AI responsibility

- Synchronized the repository, inspected the existing custom-agent format, and
  added the concise `feature-delivery` profile.
- Validated its frontmatter, required workflow references, safeguards, and
  whitespace; created PR #11 from `chore/feature-delivery-agent`.

### Human responsibility

The human specified the agent's purpose, workflow boundaries, and final-review
authority.

### Outcome

PR #11 contains the new profile at commit `6e09ac0`; no product code changed.

### Files changed

- `.github/agents/feature-delivery.agent.md`
- `AI_WORKLOG.md`

### Validation

- Custom-agent frontmatter and required workflow/safeguard references passed
  the local configuration check.
- `git diff --check` passed.

### Friction / failure

The shared working tree was switched to other local branches during delivery;
the dedicated task branch was restored before staging and publication.

### Harness change

Added a manually invocable GitHub custom agent that delegates synchronization,
TDD, delivery, and session logging to the repository Skills.

### Lesson learned

A compact custom-agent profile can preserve workflow authority by referencing
the existing Skills instead of duplicating their operational instructions.

## 2026-09-07 â€” Git activity status feature delivery

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: Scoped product feature delivery from GitHub Issue #12
Risk level: not recorded

### Goal

Take Issue #12 through implementation and validation to a review-ready pull
request, including the clarified cohesive Rich status report.

### AI responsibility

- Synchronized `main`, created `feature/git-activity-status`, and implemented
  local Git activity collection, deterministic activity levels, and the Rich
  panel presentation.
- Added focused tests, ran the repository quality gate, committed as `b0a4c3e`,
  and created PR #13.

### Human responsibility

The human defined the feature scope, presentation requirements, exclusions,
and retained final review and merge authority.

### Outcome

PR #13 is open and ready for review; it is not merged. Refactor Risk, numeric
scoring, late-night behavior, and remote GitHub activity remain out of scope.

### Files changed

- `src/cdd/cli.py`
- `src/cdd/domain.py`
- `src/cdd/git_activity.py`
- `src/cdd/presentation.py`
- `tests/test_git_activity.py`
- `tests/test_status_presentation.py`
- `AI_WORKLOG.md`

### Validation

- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed.
- `git diff --check` — passed.

### Friction / failure

The sandbox initially blocked Git metadata writes and the local `uv` cache;
approved escalation was required for synchronization, delivery, and the final
quality gate.

### Harness change

No harness behavior changed.

### Lesson learned

Keeping Git collection, deterministic level mapping, and Rich rendering in
separate responsibilities supports a small implementation with independently
testable boundaries.

## 2026-09-07 â€” README product and harness overview

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: documentation
Risk level: low

### Goal

Make the README present Coffee-Driven Development as both a small Python CLI
and an AI-assisted engineering harness sandbox while preserving product usage
examples.

### AI responsibility

- Synchronized the repository and inspected the current product and harness
  evidence.
- Updated the README with the requested purpose, architecture, workflow,
  capabilities, evidence links, and future-demo boundary.
- Created and pushed branch `docs/readme-harness-overview`, commit `0346618`,
  and pull request #10.

### Human responsibility

The human specified the README scope, required truthful MCP boundaries, and
retains review and final-merge authority.

### Outcome

The README is concise and skimmable, distinguishes terminal presentation from
the CLI/domain/storage path, and does not claim GitHub MCP or Figma MCP is
connected.

### Files changed

- `README.md`
- `AI_WORKLOG.md`

### Validation

- `git diff --check` passed.
- `uv run --extra dev pytest` passed: 65 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed.
- PR #10 was created for human review; no merge was performed.

### Friction / failure

The sandbox initially blocked Git fetch and uv cache/Python-environment access;
approved escalation completed synchronization and validation. An unrelated
untracked Feature Delivery Agent file was preserved and excluded from the PR.

### Harness change

No harness behavior changed; the README now provides a concise entry point to
the existing harness evidence.

### Lesson learned

README claims about integrations should follow the repository's recorded
evidence and explicitly separate authenticated CLI/API capability from an
unconnected MCP tool surface.

## 2026-09-07 — merge-conflict Skill and PR #10 resolution

### Harness

Tool: Codex with GitHub MCP and local Git
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: repository Skill and merge-conflict resolution
Risk level: medium

### Goal

Create and exercise `resolve-merge-conflict` on the real PR #10 conflict while
preserving the PR and current `main` changes.

### AI responsibility

- Inspected PR #10 metadata, base/head refs, changed files, mergeability,
  current `main`, and recent commits through GitHub MCP.
- Merged current `main` into the PR head in an isolated worktree, identified
  `AI_WORKLOG.md` as the only conflicted file, classified it as COMPOSABLE,
  and retained both independent worklog histories.
- Added the reusable conflict-resolution Skill and ran its workflow on this
  real conflict without force-pushing or merging the PR.

### Human responsibility

The human requested the Skill and conflict exercise and retains authority for
ambiguous product or architectural decisions and final PR merge.

### Outcome

PR #10's README work, current-main changes, both worklog histories, and the
new conflict-resolution Skill are present on the resolved branch.

### Files changed

- `.agents/skills/resolve-merge-conflict/SKILL.md`
- `AI_WORKLOG.md`
- Current-main files merged from `main` into PR #10.

### Validation

- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed.
- `git diff --check` — passed.
- No conflict markers or unmerged paths remain.

### Friction / failure

Initial sandbox restrictions blocked Git metadata and uv cache access; approved
escalation was used. The bundled Skill validator could not run because `python`
was unavailable, so the Skill was checked directly and the repository gate ran
successfully.

### Harness change

Added `.agents/skills/resolve-merge-conflict/SKILL.md`, covering safe discovery,
conflict classification, evidence-based composition, human escalation, and
post-resolution validation.

### Lesson learned

Worklog conflicts can be resolved compositionally when both sides are
independent chronological records; merge intent should still be established
from branch history and changed files rather than markers alone.

## 2026-09-09 — isolated Feature Delivery Agent worktrees

### Harness

Tool: Codex with local Git and GitHub CLI
Model: GPT-5
Reasoning: not recorded
Mode: Implementation
Task type: custom-agent configuration and Git delivery safety
Risk level: medium

### Goal

Allow the existing Feature Delivery Agent to perform bounded Issue-to-PR work
in an isolated Git worktree without disturbing the primary checkout.

### AI responsibility

- Inspected the primary checkout, remotes, default branch, fetched state, and
  registered worktrees before creating task state.
- Created `chore/feature-delivery-worktrees` from fetched `origin/main` in the
  deterministic sibling worktree `ai_coding_assistant.worktrees/feature-delivery-worktrees`.
- Updated the existing agent with conservative worktree creation, identity
  verification, cleanup-reporting, and Git safety boundaries while composing
  with the existing repository Skills.
- Created draft pull request #16 after validation.

### Human responsibility

The human specified the isolation and safety requirements and retains review
and final-merge authority.

### Outcome

The Feature Delivery Agent now supports isolated delivery when primary-checkout
state favors it. The primary branch and its existing user change were preserved,
and unrelated registered worktrees were neither reused nor removed.

### Files changed

- `.github/agents/feature-delivery.agent.md`
- `AI_WORKLOG.md`

### Validation

- Agent frontmatter, required safety instructions, and prompt length passed a
  focused configuration check against the documented GitHub profile shape.
- The task worktree path, branch, base ancestry, and separation from the primary
  checkout were verified.
- `uv run --extra dev pytest` passed: 74 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed.
- `git diff --check` passed for the agent change.

### Friction / failure

The host-created sibling worktree required a command-scoped Git safe-directory
setting for sandboxed read-only checks. Existing unrelated worktrees were left
untouched, including one nested under the primary checkout.

### Harness change

The existing Feature Delivery Agent gained isolated worktree setup and safety
checks. No new Skill was added and no existing Skill workflow was duplicated.

### Lesson learned

A deterministic sibling worktree avoids surfacing task files as untracked
content in the primary checkout and lets delivery proceed without switching its
branch or moving user changes.

## 2026-09-09 — resumable AI run-state Skill

### Harness

Tool: Codex
Model: not recorded
Reasoning: not recorded
Mode: Implementation
Task type: repository Skill and harness guidance
Risk level: low

### Goal

Add lightweight operational state for meaningful AI engineering work that may
span sessions or stages without duplicating permanent project history.

### AI responsibility

- Preserved an unrelated local test change by working from `origin/main` in an
  isolated `feature/manage-ai-run` worktree.
- Added and validated `manage-ai-run`, introduced `.ai/runs/`, and added
  concise repository routing.
- Committed the harness change as `cf72207` and created PR #15.

### Human responsibility

The human specified the run-state content and safety rules and retains review
and final-merge authority.

### Outcome

PR #15 contains a compact start-or-continue workflow that reconciles recorded
state with repository evidence, resumes from the first incomplete step, and
keeps `AI_WORKLOG.md` as the historical record. No product code changed, and
no merge was performed.

### Files changed

- `.agents/skills/manage-ai-run/SKILL.md`
- `.ai/runs/.gitkeep`
- `AGENTS.md`
- `AI_WORKLOG.md`

### Validation

- Skill Creator `quick_validate.py` — passed.
- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed.
- Staged diff check — passed.

### Friction / failure

The current merged feature branch contained an unrelated uncommitted test
change, so delivery used an isolated worktree. The Skill validator required an
ephemeral PyYAML installation because it is not a project dependency.

### Harness change

Added a repository Skill for evidence-backed resumable run state and minimal
`AGENTS.md` routing to it.

### Lesson learned

Operational continuation state stays useful and compact when it records only
the next-step checklist and supporting evidence while durable outcomes remain
in the chronological worklog.

## 2026-09-09 — PR autopilot custom agent

### Harness

Tool: Codex with GitHub CLI and local Git
Model: GPT-5
Reasoning: not recorded
Mode: Default
Task type: custom-agent harness
Risk level: low

### Goal

Add one manually invocable custom agent that diagnoses an existing pull
request and routes each blocking state to the smallest existing repository
capability without duplicating its procedure.

### AI responsibility

- Preserved unrelated local work by creating an isolated worktree from current
  `origin/main` on `chore/pr-autopilot-agent`.
- Added and validated `.github/agents/pr-autopilot.agent.md` against the
  repository conventions and GitHub's documented custom-agent configuration.
- Created task commit `3e08292`, pushed the branch, and created PR #14 for
  human review.

### Human responsibility

The human specified the routing, evidence, safety, validation, and delivery
requirements and retains final review and merge authority.

### Outcome

PR #14 contains a concise manual orchestrator for conflict, CI, review,
synchronization, and final PR-validation routing. No product code or dependency
changed, and no merge, auto-merge, self-approval, or force-push occurred.

### Files changed

- `.github/agents/pr-autopilot.agent.md`
- `AI_WORKLOG.md`

### Validation

- Custom-agent location, suffix, frontmatter, supported tool aliases, prompt
  length, and required routes — passed.
- `git diff --check` — passed.
- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed.

### Friction / failure

The starting branch contained an unrelated modification to
`tests/test_presentation.py`, so the task was isolated in a separate worktree.
Sandbox approval was required for remote Git and GitHub operations.

### Harness change

Added a manually invocable `pr-autopilot` agent with read-only GitHub MCP
access and routing to the existing conflict, CI, review, synchronization, and
PR-validation capabilities.

### Lesson learned

An orchestrator stays small when it owns state diagnosis and dependency order
while repository Skills and specialist agents continue to own corrections and
validation details.

## 2026-09-09 — merge-conflict resolution for PRs #15, #16, and #17

### Harness

Tool: Codex with local Git and GitHub CLI
Model: GPT-5
Reasoning: not recorded
Mode: Default
Task type: multi-PR merge-conflict resolution
Risk level: medium

### Goal

Resolve current merge conflicts against `main` for PRs #15, #16, and #17
without disturbing unrelated work in the primary checkout.

### AI responsibility

- Verified local and remote default-branch freshness and inspected all three PRs.
- Used isolated worktrees, merged `origin/main`, and preserved both independent
  `AI_WORKLOG.md` entries on each branch.
- Created and pushed merge commits `283973c`, `b96bfdf`, and `e502379`.

### Human responsibility

The human requested resolution of the three PR conflicts and retains review and
final-merge authority.

### Outcome

PRs #15, #16, and #17 were updated without force-pushing or changing their
feature intent. The unrelated primary-checkout modification remained untouched.

### Files changed

- `.github/agents/pr-autopilot.agent.md` (merged from `main`)
- `AI_WORKLOG.md`

### Validation

- `uv run --extra dev pytest` — 74 passed on each branch.
- `uv run --extra dev ruff check .` — passed on each branch.
- `uv run --extra dev mypy` — passed on each branch.
- Staged diff checks and conflict-marker checks — passed on each branch.

### Friction / failure

Windows retained stale absolute paths in PR #16's moved virtual environment; a
fresh environment was created and the full validation gate then passed.

### Harness change

No new harness behavior was introduced; each branch only incorporated the
already-reviewed mainline agent and retained its own feature changes.

### Lesson learned

Independent chronological worklog entries should be composed rather than
selected, and moved Windows virtual environments should be recreated before
validation.

## 2026-09-09 — AGENTS.md task router

### Harness

Tool: Codex with GitHub CLI and local Git
Model: GPT-5
Reasoning: not recorded
Mode: Default
Task type: repository guidance documentation
Risk level: low

### Goal

Refactor `AGENTS.md` into a lightweight task router while preserving project
invariants, validation requirements, human approval boundaries, and Git safety
rules.

### AI responsibility

- Inspected the capabilities present on current `origin/main` and their
  trigger boundaries.
- Preserved unrelated local work by using an isolated worktree on
  `docs/agents-task-router`.
- Consolidated repeated workflow prose into one task router and created task
  commit `7dc8eb6` and PR #18 for human review.

### Human responsibility

The human defined the documentation scope and policy-preservation constraints
and retains review and final-merge authority.

### Outcome

`AGENTS.md` now keeps persistent policy concise and routes tasks to all eight
Skills and three custom agents present on the base branch. The unmerged
`manage-ai-run` capability was not advertised. No product behavior or
repository policy changed, and no merge or auto-merge was performed.

### Files changed

- `AGENTS.md`
- `AI_WORKLOG.md`

### Validation

- `git diff --check` passed.
- The router inventory was checked against `origin/main`.
- PR #18 was created for human review.

### Friction / failure

The starting worktree contained an unrelated modified test and untracked
worktree directory, and local `main` was behind `origin/main`. The task used a
fresh isolated worktree so that existing user work remained untouched.

### Harness change

Reorganized `AGENTS.md` as a compact control plane for invariants, human gates,
validation, and capability routing; detailed procedures remain in their Skills
and agents.

### Lesson learned

Capability triggers can remain explicit without duplicating workflow details
when the repository control plane names situations and delegates procedures to
the owning Skill or agent.

## 2026-09-09 — central AI harness configuration

### Harness

Tool: Codex with GitHub CLI and local Git
Model: GPT-5
Reasoning: not recorded
Mode: Default
Task type: harness configuration
Risk level: low

### Goal

Centralize the repository's small deterministic AI workflow values without
introducing a configuration framework or moving policy into JSON.

### AI responsibility

- Synchronized `main` with `origin/main` and preserved unrelated work by using
  the isolated `chore/central-harness-config` worktree.
- Inspected current workflow guidance and review-ready resumable-run and
  claim-locking PRs before selecting the minimal shared values.
- Added the configuration, updated only direct Skill consumers, created task
  commit `1e1f69e`, pushed the branch, and opened PR #20.
- Merged the concurrently advanced `origin/main` and compositionally retained
  both the task-router guidance and chronological worklog entries.

### Human responsibility

The human specified the configuration boundaries and retains architecture,
review, and final merge authority.

### Outcome

PR #20 centralizes the default branch, quality-gate commands, shared paths,
claim label, and human-gate identifiers. No product behavior, Python runtime
code, dependency, parser, or configuration framework changed.

### Files changed

- `.ai/harness.config.json`
- `AGENTS.md`
- `.agents/skills/create-feature-issue/SKILL.md`
- `.agents/skills/prepare-pull-request/SKILL.md`
- `.agents/skills/record-ai-session/SKILL.md`
- `.agents/skills/sync-repository/SKILL.md`
- `.github/skills/code-review/SKILL.md`
- `AI_WORKLOG.md`

### Validation

- JSON parsing and minimal schema-shape assertions — passed.
- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed with no issues in 12 source files.
- `git diff --check` — passed after base-branch reconciliation.

### Friction / failure

The starting checkout contained unrelated user work, so the task used an
isolated worktree. While PR #20 was being prepared, PR #18 advanced `main` and
created composable conflicts in `AGENTS.md` and `AI_WORKLOG.md`. Sandbox
approval was required for remote Git and GitHub operations. The sandboxed
quality-gate attempt could not initialize uv's cache; the approved run passed.

### Harness change

Added one versioned JSON source for deterministic shared values and kept
persistent rules, procedures, orchestration, history, and resumable state in
their existing layers.

### Lesson learned

A small declarative value file removes drift when consumers remain explicit
and procedural policy stays in repository instructions and Skills.

## 2026-09-09 — PR #16 conflict resolution after PR #15 merge

### Harness

Tool: Codex with local Git and GitHub CLI
Model: GPT-5
Reasoning: not recorded
Mode: Default
Task type: merge-conflict resolution
Risk level: low

### Goal

Resolve PR #16 against the current `main` without altering its isolated
Feature Delivery Agent worktree behavior.

### AI responsibility

- Verified the PR branch and remote base in its isolated worktree.
- Merged `origin/main` and compositionally retained the independent PR #16 and
  merged PR #15 worklog entries.
- Created and pushed merge commit `0431038` without rewriting history.

### Human responsibility

The human narrowed the requested scope to PR #16 and retains final merge
authority.

### Outcome

PR #16 incorporates current mainline harness changes while its intended agent
worktree changes remain intact.

### Files changed

- Mainline harness files incorporated by the merge
- `AI_WORKLOG.md`

### Validation

- `uv run --extra dev pytest` — 74 passed.
- `uv run --extra dev ruff check .` — passed.
- `uv run --extra dev mypy` — passed with no issues in 12 source files.
- Conflict-marker, unmerged-path, and staged-diff checks — passed.

### Friction / failure

The local default branch was behind the remote base, so the current
`origin/main` was merged directly into the isolated PR worktree.

### Harness change

No new harness behavior was introduced by the resolution.

### Lesson learned

Rechecking the remote base immediately before resolution avoids treating a
previously mergeable PR as current after another PR advances `main`.

## 2026-09-09 — Feature Delivery Issue claiming

### Harness

Tool: Codex with authenticated GitHub CLI and local Git
Model: GPT-5
Reasoning: not recorded
Mode: Implementation
Task type: agent configuration and documentation
Risk level: medium

### Goal

Prevent concurrent Feature Delivery sessions from independently implementing
the same GitHub Issue with a conservative, lightweight claim lifecycle.

### AI responsibility

- Inspected repository, branch, worktree, pull request, Issue, and existing
  `manage-ai-run` branch state before editing.
- Updated the Feature Delivery Agent with `ai-in-progress` claim inspection,
  acquisition, release, abort, resumable-state, and Issue-linkage rules.
- Preserved unrelated modified files and existing worktrees by using isolated
  branch `chore/feature-delivery-claiming`.
- Created commit `6bc5a79` and draft pull request #17.

### Human responsibility

The human specified the claim policy and retains authority over ambiguous
claims, architectural decisions, review, and final merge.

### Outcome

The Feature Delivery Agent now stops before repository changes when an Issue
is owned or ownership is ambiguous, claims unowned work before implementation,
coordinates matching resumable state, and releases successful claims without
manually closing Issues.

### Files changed

- `.github/agents/feature-delivery.agent.md`
- `docs/ai/github-integration-capabilities.md`
- `AI_WORKLOG.md`

### Validation

- Agent frontmatter and required tool scope structure check passed.
- `uv run --extra dev pytest` passed: 74 tests.
- `uv run --extra dev ruff check .` passed.
- `uv run --extra dev mypy` passed.
- `git diff --check` passed.
- PR #17 was created for human review; no merge was performed.

### Friction / failure

The primary checkout contained an unrelated modified test and existing
worktrees, and local `main` was behind `origin/main`; an isolated worktree based
on the fetched remote default branch preserved that state. Sandbox restrictions
initially blocked the uv cache, so validation used approved escalation.

### Harness change

Added conservative GitHub Issue claim coordination directly to the existing
Feature Delivery Agent without adding a separate Skill or changing product
code.

### Lesson learned

A shared label prevents duplicate starts only when it is reconciled with active
GitHub, repository, and resumable-run evidence; the label alone cannot safely
establish or transfer ownership.
