# Coffee-Driven Development — Implementation Plan

## Purpose

Coffee-Driven Development (CDD) is intentionally a small and slightly ridiculous Python CLI.

The product itself is deliberately simple.

Its primary purpose is to serve as a controlled sandbox for building, testing and demonstrating an AI-assisted engineering harness suitable for Forward Deployed Engineer workflows.

The repository should demonstrate how AI is used for:

- planning,
- repository exploration,
- implementation,
- testing,
- documentation,
- reusable workflows / Skills,
- GitHub integration,
- pull-request review,
- external knowledge work through MCP,
- deterministic validation,
- CI,
- bounded autonomous execution,
- human approval at important decision boundaries.

The application should remain small enough that its product behavior can be explained in approximately two minutes.

The interesting part of the project is the engineering workflow around it.

The harness should evolve based on observed repetition, friction and actual project needs rather than being fully designed upfront.

---

# Core project principles

## Keep the product small

Do not expand the application merely to make the repository look more complex.

Product complexity should only be introduced when it creates a useful engineering scenario for demonstrating the harness.

## Prefer deterministic behavior

Business rules should be deterministic and independently testable.

AI is primarily part of the development workflow, not the application runtime.

## Avoid premature abstractions

Do not introduce:

- service layers,
- repository interfaces,
- dependency injection frameworks,
- plugin systems,
- ORMs,
- distributed infrastructure,

unless a concrete requirement justifies them.

## Separate responsibilities

Maintain clear boundaries between:

```text
CLI / presentation
        ↓
domain logic
        ↓
storage / external systems
```

## Human decisions remain explicit

AI may:

- inspect,
- recommend,
- implement,
- test,
- review,
- document.

Humans remain responsible for:

- product scope,
- architecture approval,
- significant dependency changes,
- permission-sensitive actions,
- disputed review findings,
- final pull-request merge.

---

# AI model routing policy

Do not use the strongest available model by default.

Prefer the lowest-cost model that can reliably complete the task.

Escalate based on:

- ambiguity,
- architectural impact,
- implementation difficulty,
- risk,
- cross-cutting reasoning requirements,
- observed failure of a cheaper model.

Current available models:

- GPT-6 Astra
- GPT-5.6 Sol
- GPT-5.6 Terra
- GPT-5.6 Luna
- GPT-5.5
- GPT-5.4 Mini

Default routing:

| Task type | Preferred model | Reasoning |
| --- | --- | --- |
| Worklog / simple documentation | GPT-5.6 Luna | Low |
| Lightweight planning / harness configuration | GPT-5.6 Terra | Medium |
| Normal implementation | GPT-5.6 Sol | Medium |
| Architecture / difficult engineering | GPT-5.6 Sol | High |
| Independent critical review | GPT-6 Astra | High |
| Final whole-repository audit | GPT-6 Astra | Highest useful setting |

Model selection should be recorded in `AI_WORKLOG.md`.

The goal is not to demonstrate that the strongest model can solve every task.

The goal is to demonstrate deliberate model routing.

---

# Validation strategy

Canonical local validation is cross-platform and uses `uv` directly.

Before completing meaningful code changes, run:

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
uv run --extra dev mypy
```

These commands are intentionally explicit.

The project does not depend on GNU Make.

A future reusable validation Skill may orchestrate these commands together with higher-level reasoning such as:

- selecting relevant targeted tests,
- inspecting the diff,
- identifying unrelated changes,
- detecting regressions,
- summarizing remaining risks.

A Skill should not exist merely as an alias for deterministic commands.

---

# Current status

Current product phase:

**Phase 6 — `cdd status` and `cdd history` (not started)**

Current harness phase:

**Phase 4.7 — GitHub CI Triage Agent (configuration implemented; operational
exercise pending)**

Current harness maturity:

**Level 2 — Workflow-aware**

The repository contains a minimal Python engineering foundation and a
deterministic `cdd drink` command that appends coffee events to local JSONL
history. Status and history presentation have not been implemented yet.

## Completed

- [x] Phase 0 — Repository initialization
- [x] Phase 1 — Initial architecture exploration
- [x] Phase 2 — Engineering foundation
- [x] Project implementation roadmap
- [x] Python 3.12+ environment
- [x] `src` package layout
- [x] `cdd` console entry point
- [x] `cdd --help`
- [x] pytest configuration
- [x] ruff configuration
- [x] mypy configuration
- [x] initial `AGENTS.md`
- [x] explicit validation rules in `AGENTS.md`
- [x] initial `AI_WORKLOG.md`
- [x] initial model-routing policy
- [x] cross-platform validation strategy
- [x] Phase 4 — `cdd drink`
- [x] Phase 5 — Local persistence

## Product functionality implemented

- [x] deterministic drink information
- [x] coffee tracking
- [x] persistent coffee history
- [ ] developer status
- [ ] Git activity
- [ ] refactor-risk scoring

## AI harness capabilities implemented

- [x] repository-level agent instructions
- [x] explicit model / reasoning selection
- [x] human architecture approval
- [x] deterministic validation commands
- [ ] automatic AI session logging
- [x] repository Skills
- [x] safe Git delivery and ready-for-review pull-request workflow
- [x] Python engineering guidance
- [x] testing strategy
- [ ] reusable validation workflow
- [x] reusable TDD feature-development workflow
- [x] review-feedback validation workflow
- [x] safe repository synchronization workflow
- [x] authenticated GitHub PR delivery
- [ ] GitHub MCP
- [x] GitHub Actions CI
- [x] Context-aware Copilot Code Review
- [x] repository CI-triage agent configuration (operational exercise pending)
- [ ] independent AI pull-request review
- [ ] Figma MCP
- [ ] Goal-based delegation
- [ ] presentation-generation workflow

---

# Roadmap at a glance

## Foundation

- [x] Phase 0 — Repository initialization
- [x] Phase 1 — Initial architecture exploration
- [x] Phase 2 — Engineering foundation
- [x] Phase 3 — Reusable AI session logging
- [x] Phase 3.5 — Safe Git delivery and pull-request automation
- [x] Phase 3.75 — Engineering workflow and review-feedback automation
- [x] Phase 3.8 — Pull-request quality gate

## Product MVP

- [x] Phase 4 — `cdd drink`
- [x] Phase 5 — Local persistence
- [ ] Phase 6 — `cdd status` and `cdd history`

## Harness evolution

- [ ] Phase 7 — Harness retrospective
- [ ] Phase 8 — Repository engineering knowledge
- [ ] Phase 9 — Reusable engineering Skills

## GitHub engineering workflow

- [x] Phase 4.5 — CI and repository synchronization
- [x] Phase 4.6 — Context-aware Copilot Code Review
- [ ] Phase 4.7 — GitHub CI Triage Agent operational exercise
- [ ] Phase 10 — GitHub Actions CI
- [ ] Phase 11 — GitHub MCP integration
- [ ] Phase 12 — Git activity feature through GitHub Issue
- [ ] Phase 13 — Independent AI pull-request review
- [ ] Phase 14 — AI review-feedback validation

## Knowledge work and increased autonomy

- [ ] Phase 15 — Figma MCP workflow documentation
- [ ] Phase 16 — Bounded Goal-based delegation

## Interview preparation

- [ ] Phase 17 — Reserved live-demo feature
- [ ] Phase 18 — Generate interview presentation
- [ ] Phase 19 — Final critical harness audit

---

# Phase 0 — Repository initialization

Status: **COMPLETE**

## Goal

Create the repository manually before delegating meaningful work to AI.

## Initial files

- `README.md`
- `AGENTS.md`
- `AI_WORKLOG.md`
- `.gitignore`

## Human decision

The application was deliberately chosen to be small and memorable.

The initial product concept:

```text
cdd drink espresso
cdd status
cdd history
```

The application acts as a sandbox for AI engineering workflows rather than being the primary technical achievement.

---

# Phase 1 — Initial architecture exploration

Status: **COMPLETE**

## AI setup

Tool: Codex  
Model: GPT-5.6 Terra  
Reasoning: Medium  
Mode: Plan

## Goal

Propose the smallest reasonable v0.1 architecture without implementing code.

## Architecture direction

```text
src/
└── cdd/
    ├── __init__.py
    ├── cli.py
    ├── domain.py
    └── storage.py

tests/
```

## Decisions

- Python 3.12+
- `src` layout
- standard-library CLI
- zero runtime dependencies where practical
- typed Python
- pure domain logic
- local persistence
- pytest
- ruff
- mypy

## Explicit non-goals

Do not introduce:

- web API
- frontend
- Docker
- cloud infrastructure
- database server
- ORM
- service layer
- repository interface
- plugin architecture

## Human gate

Architecture was proposed by AI.

Final acceptance remained a human decision.

Historical session details belong in `AI_WORKLOG.md`.

---

# Phase 2 — Engineering foundation

Status: **COMPLETE**

## AI setup

Tool: Codex  
Model: GPT-5.6 Sol  
Reasoning: Medium  
Mode: Implementation

## Goal

Create the minimal Python engineering foundation without implementing product functionality.

## Implemented

- `pyproject.toml`
- `src/cdd/__init__.py`
- `src/cdd/cli.py`
- `tests/test_cli.py`
- `uv.lock`

## CLI capability

```bash
cdd --help
```

## Tooling

- Hatchling
- uv
- pytest
- ruff
- mypy
- argparse

Runtime dependencies:

```text
none
```

## Validation

Canonical validation:

```bash
uv run --extra dev pytest
uv run --extra dev ruff check .
uv run --extra dev mypy
```

## Current architecture

```text
CLI boundary
     ↓
future domain logic
     ↓
future local storage
```

No product behavior is implemented yet.

Historical friction and environment-specific issues belong in `AI_WORKLOG.md`, not in the roadmap.

---

# Phase 3 — Harness baseline and reusable session logging

Status: **COMPLETE**

## AI setup

Preferred model:

GPT-5.6 Terra

Reasoning:

Medium

## Goal

Introduce the first reusable harness capability based on an actually observed repeated workflow.

The repeated workflow is AI session documentation.

## Why now

The first two meaningful Codex sessions both required manually specified AI worklog instructions.

This repetition is sufficient to justify extracting the behavior from task prompts.

## Planned work

- [x] backfill the architecture-planning session
- [x] backfill the engineering-foundation session
- [x] create `record-ai-session`
- [x] add a minimal routing rule to `AGENTS.md`
- [x] use the new Skill to record the session in which it was created
- [x] verify existing historical worklog entries remain unchanged
- [x] ensure future meaningful sessions can be logged consistently

## Planned Skill

```text
.agents/
└── skills/
    └── record-ai-session/
        └── SKILL.md
```

## Skill responsibility

The Skill should:

- record actual session metadata
- distinguish AI execution from human decisions
- record validation actually performed
- record actual friction
- record actual harness changes
- append instead of overwrite
- preserve chronological history
- never invent missing metadata

Unknown metadata should be recorded as:

```text
not recorded
```

## Human gate

The human may decide that an interaction is too trivial to log.

Explicit user instructions override automatic logging behavior.

## Acceptance criteria

- [x] two historical sessions are accurately recorded
- [x] `record-ai-session` was established as the first repository Skill
- [x] `AGENTS.md` contains only a concise routing rule
- [x] detailed logging behavior lives in the Skill
- [x] the Skill successfully logs its own creation session
- [x] no product code changes occurred during this phase

---

# Phase 3.5 — Safe Git delivery and pull-request automation

Status: **COMPLETE**

## Goal

Create `prepare-pull-request`, the second repository Skill, to safely deliver
completed validated changes through a dedicated branch, explicit staging,
commit, push, ready-for-review pull request, and one factual session-log update.

## Requirements

- never commit task changes directly to the default branch
- validate before committing and stage only intended files
- create a ready-for-review PR with review-ready scope and validation evidence
- never auto-merge, force-push, or rewrite history
- keep independent AI review as a future separate workflow

## Future review direction

```text
implementation agent → prepare-pull-request → ready-for-review PR → independent review
agent → finding validation → human merge
```

---

# Phase 3.75 — Engineering workflow and review-feedback automation

Status: **COMPLETE**

## Goal

Add concise Python and testing knowledge, test-first feature development,
critical review-feedback validation, and ready-for-review Git delivery.

## Delivered

- `docs/engineering/python-guidelines.md`
- `docs/engineering/testing-strategy.md`
- `develop-feature-tdd`
- `validate-review-feedback`
- ready-for-review delivery after the final worklog commit

Independent first-pass AI review remains a future, separate capability.

---

# Phase 3.8 — Pull-request quality gate

Status: **COMPLETE**

## Goal

Add `validate-pull-request` to check PR metadata, diff scope, validation
evidence, review-thread state, and final pre-merge readiness.

---

# Phase 4 — First product feature: drink

Status: **COMPLETE**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

Medium

## Goal

Implement:

```bash
cdd drink <drink>
```

Initial drinks:

- espresso
- americano
- cappuccino

Example:

```text
$ cdd drink espresso

Espresso
Estimated caffeine: 80 mg
```

## Architecture

Introduce domain logic only when required.

Expected direction:

```text
CLI
 ↓
domain logic
```

Persistence is not introduced yet.

## Requirements

- typed domain model
- deterministic caffeine values
- domain independent from CLI rendering
- clear unsupported-drink behavior
- meaningful unit tests
- no new runtime dependency unless justified

## Harness observation

During implementation, observe whether the following become repetitive:

- test instructions
- validation sequence
- implementation workflow
- diff inspection

Do not create additional Skills solely after one occurrence.

---

# Phase 4.5 — CI and repository synchronization

Status: **COMPLETE**

## Goal

Strengthen the harness before Phase 5 with safe repository synchronization and
independent GitHub Actions validation for the current pull-request HEAD.

## Scope

- `sync-repository` verifies repository identity, local work, and default-branch
  freshness without destructive Git operations or delivery actions.
- GitHub Actions runs pytest, ruff, and mypy on pull requests and pushes to
  `main` using the locked development environment.
- CI preserves JUnit, ruff, and mypy reports as finite-retention artifacts and
  publishes a compact step summary even when validation fails.
- `validate-pull-request` requires CI and automated-review evidence for the
  current PR HEAD instead of accepting stale results.

## Acceptance criteria

- [x] repository synchronization workflow exists and is routed from new work
- [x] TDD composes with repository synchronization
- [x] CI workflow is defined without weakening required validation
- [x] pull-request validation checks current-HEAD CI and review freshness
- [x] local pytest, ruff, and mypy validation passes
- [x] CI succeeds for the current PR HEAD
- [x] CI step-summary generation is verified
- [x] `pytest.xml`, `ruff.txt`, and `mypy.txt` are verified in the uploaded artifact

Phase 5 remains planned and has not started.

---

# Phase 4.6 — Context-aware Copilot Code Review

Status: **COMPLETE**

## Goal

Configure repository-specific GitHub Copilot Code Review context without
changing Coffee-Driven Development product behavior.

## Scope

- A review-focused GitHub Copilot Skill generates concrete, repository-aware
  findings and remains separate from `validate-review-feedback` and
  `validate-pull-request`.
- Concise repository Copilot instructions route review work to the Skill and
  existing engineering guidance.
- Reviews compare CI evidence to the current pull-request HEAD and may use
  relevant GitHub or MCP context when available.
- Any actual Skill, instruction, or MCP usage is recorded only from explicit
  review attribution or session evidence; this phase does not broadly mark
  GitHub MCP complete.

## Completion criteria

- [x] A repository-specific review configuration was exercised by a real
      Copilot pull-request review.
- [x] Evidence is recorded separately: repository configuration exercised: YES;
      code-review Skill usage: UNKNOWN; Copilot instruction usage: UNKNOWN;
      GitHub MCP usage: UNKNOWN; current-head CI-context usage: UNKNOWN.
- [x] Actionable review feedback was handled through
      `validate-review-feedback`.
- [x] Review freshness is assessed through `validate-pull-request`, preferring
      exact reviewed-SHA evidence and otherwise reporting the documented
      temporal fallback separately.

GitHub MCP integration remains planned; this phase did not establish broad MCP
usage or attribution.

---

# Phase 4.7 — GitHub CI Triage Agent

Status: **CONFIGURATION IMPLEMENTED — OPERATIONAL EXERCISE PENDING**

## Goal

Provide a manually selected, repository-scoped custom agent for diagnosing a
real failing GitHub Actions run from current-head evidence.

## Implemented configuration

- `.github/agents/ci-triage.agent.md` uses GitHub's documented custom-agent
  location, filename suffix, YAML frontmatter, and tool aliases.
- Automatic model invocation is disabled; a human must select the agent.
- The agent classifies the primary failure, reports evidence, and recommends
  only the smallest justified correction.
- The agent cannot weaken validation, merge, force-push, or silently choose
  among ambiguous or materially different fixes.

## Remaining operational evidence

The configuration is not available on the default branch until this pull
request is merged. Exercise it only against a naturally occurring CI failure;
do not manufacture a failure to claim completion.

---

# Phase 5 — Local persistence

Status: **COMPLETE**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

Medium

## Goal

Persist coffee events locally.

Each event should contain:

```text
timestamp
drink type
caffeine amount
```

## Persistence direction

Use JSONL unless implementation reveals a concrete reason to reconsider.

Expected production location:

```text
~/.cdd/
```

Tests must use temporary paths.

Tests must never modify the real user home directory.

Production appends one JSON object per line to `~/.cdd/history.jsonl`. Tests
inject an explicit path through the internal CLI entry point, avoiding both a
dependency-injection framework and environment-variable mutation.

## Architecture

```text
CLI
 ↓
domain
 ↓
storage
```

Storage must not contain business logic.

Domain calculations must not read files directly.

## Human gate

Changing the persistence strategy requires explicit approval.

## Completion evidence

- successful espresso, americano, and cappuccino commands append typed coffee
  events with UTC ISO timestamps, drink types, and caffeine amounts
- unsupported drinks do not append events
- existing CLI output is preserved
- parent directories are created when absent
- storage tests use temporary paths and independently parse every JSON line

---

# Phase 6 — Status and history

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

Medium

## Commands

```bash
cdd history
cdd status
```

## Status output

Should include:

- drinks today
- caffeine today
- developer state

Initial deterministic states:

```text
0 mg
NO SIGNAL

1–100 mg
BOOTING

101–250 mg
PRODUCTIVE

251–400 mg
TURBO MODE

400+ mg
ARCHITECTURE PRIVILEGES REVOKED
```

## Architecture

Developer-state calculation must be pure domain logic.

It must not depend on:

- CLI rendering
- filesystem
- terminal formatting

---

# Milestone A — Product MVP

Reached when:

- [x] `cdd drink` works
- [ ] coffee history persists locally
- [ ] `cdd history` works
- [ ] `cdd status` works
- [ ] meaningful domain tests exist
- [ ] pytest passes
- [ ] ruff passes
- [ ] mypy passes

At this point the application itself is considered sufficient.

Further work should primarily improve the AI engineering harness rather than expand product scope.

---

# Phase 7 — Harness retrospective

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

High

Escalation:

GPT-6 Astra / High only if analysis becomes genuinely difficult or ambiguous.

## Goal

Evaluate the actual development history before introducing additional harness complexity.

Analyze:

- instructions repeatedly included in prompts
- repeated validation behavior
- repeated test expectations
- recurring friction
- inconsistent agent decisions
- missing persistent repository context
- unnecessary instructions

Classify each finding into:

1. `AGENTS.md`
2. repository engineering knowledge
3. reusable Skill candidate
4. deterministic command / script
5. task-specific information that should remain outside the harness

Do not implement changes during the first retrospective pass.

---

# Phase 8 — Repository engineering knowledge

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

High

## Prerequisite

Phase 3.75 already established Python and testing guidance based on observed
need. Phase 7 should evaluate whether the remaining guidance would improve
agent behavior before adding it.

Possible structure:

```text
docs/
└── engineering/
    ├── python-guidelines.md
    ├── testing-strategy.md
    ├── architecture-guidelines.md
    └── review-guidelines.md
```

## Python guidelines

Potential topics:

- typing
- dependency policy
- error handling
- module boundaries
- avoiding unnecessary abstraction

## Testing strategy

Potential topics:

- behavioral testing
- happy paths
- boundary conditions
- invalid input
- regression tests
- filesystem isolation
- deterministic tests

## Architecture guidelines

Potential topics:

- CLI/domain separation
- storage/domain separation
- simplicity constraint

## Review guidelines

Potential topics:

- correctness
- requirements
- regressions
- edge cases
- tests
- unrelated changes

## AGENTS.md role

After engineering documentation exists, `AGENTS.md` should primarily route agents to relevant knowledge instead of duplicating it.

---

# Phase 9 — Reusable engineering workflows

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Terra or GPT-5.6 Sol

Reasoning:

Medium

## Rule

Create only workflows justified by actual repetition observed during earlier phases.

Possible candidates:

```text
validate-change
write-unit-tests
implement-feature
investigate-bug
```

Not all candidates must be implemented.

## Example: validate-change

A useful Skill may:

```text
inspect changed files
        ↓
identify affected scope
        ↓
run targeted tests
        ↓
run full pytest
        ↓
run ruff
        ↓
run mypy
        ↓
inspect diff
        ↓
identify unrelated changes
        ↓
report validation status
```

The Skill must add reasoning around validation.

It must not merely alias deterministic commands.

## Example: write-unit-tests

Potential workflow:

```text
read testing strategy
↓
inspect behavior
↓
identify cases
↓
write tests
↓
run targeted tests
↓
run full quality gate
↓
summarize gaps
```

## Example: implement-feature

Potential workflow:

```text
read requirement
↓
inspect repository
↓
plan
↓
human approval when needed
↓
implement
↓
test
↓
validate
↓
inspect diff
```

---

# Phase 10 — GitHub Actions CI evolution

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Terra

Reasoning:

Medium

## Goal

The baseline GitHub Actions workflow is introduced in Phase 4.5. Revisit CI
here only when later repository evidence justifies hardening or expansion;
do not recreate the baseline workflow.

The scope and acceptance criteria for any later CI work should be derived from
observed limitations in the Phase 4.5 workflow rather than specified in
advance.

---

# Phase 11 — GitHub MCP integration

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Terra

Reasoning:

Medium

## First step

Verify integration in read-only mode.

The agent should:

- inspect repository
- inspect issues
- inspect pull requests
- inspect available GitHub capabilities
- distinguish read operations from write operations

Do not create or modify anything during the initial verification.

## Goal

Move real engineering context into the harness.

Instead of:

```text
copy GitHub Issue
↓
paste into prompt
```

prefer:

```text
GitHub Issue
↓
GitHub MCP
↓
Codex
```

---

# Phase 12 — Git activity feature through GitHub workflow

Status: **PLANNED**

## Feature

Add local Git activity to developer status.

Report:

- number of commits today
- latest commit time

Outside a Git repository:

fail gracefully.

## AI setup

Planning:

GPT-5.6 Sol / High

Implementation:

GPT-5.6 Sol / Medium

## Workflow

```text
GitHub Issue
↓
Codex reads requirement
↓
repository inspection
↓
implementation plan
↓
human approval
↓
implementation
↓
tests
↓
validation
↓
self-review
↓
pull request
```

## Human gate

Do not merge automatically.

---

# Phase 13 — Independent AI pull-request review

Status: **PLANNED**

## AI setup

Preferred model:

GPT-6 Astra

Reasoning:

High

## Goal

Use a separate Codex session as an independent reviewer.

Reviewer reads:

- original issue
- PR description
- complete diff
- repository guidelines
- tests

Reviewer must not modify code.

Focus on:

- requirement compliance
- correctness
- boundary conditions
- regressions
- test quality
- architecture consistency
- unnecessary complexity

Do not invent findings merely to produce review output.

---

# Phase 14 — Independent review feedback validation

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

High

Escalate to GPT-6 Astra only for genuinely difficult disagreements.

## Goal

Prevent automation bias.

The generic `validate-review-feedback` capability was introduced in Phase 3.75
and validated against GitHub Copilot feedback. This phase applies that
established workflow specifically to the independent AI reviewer from Phase 13.

For every review finding classify:

```text
valid
partially valid
not valid
```

Verify against:

- original issue
- implementation
- repository guidelines
- tests

Only then modify the implementation.

## Principle

AI review is evidence, not authority.

---

# Phase 15 — Figma MCP knowledge workflow

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Terra

Reasoning:

Medium

## Goal

Use Figma for knowledge work and workflow documentation.

Do not build unnecessary product UI.

Create a simple harness diagram showing:

```text
GitHub Issue
↓
Codex analysis
↓
implementation plan
↓
human approval
↓
implementation
↓
validation
↓
GitHub pull request
↓
independent AI review
↓
CI
↓
human merge
```

Also show persistent harness context:

- `AGENTS.md`
- repository engineering documentation
- Skills
- `AI_WORKLOG.md`
- GitHub MCP
- Figma MCP

The diagram should be explainable in under one minute.

---

# Phase 16 — Bounded Goal-based delegation

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Sol

Reasoning:

Medium or High depending on the task.

## Prerequisites

Only introduce Goal-based delegation after:

- repository instructions are stable
- useful Skills exist
- CI works
- GitHub MCP works
- validation is reliable
- human permission boundaries are explicit

Example bounded goal:

```text
Take GitHub issue #X from requirement analysis to a review-ready pull request.

Run repository validation.

Do not merge.
```

## Human gate

Final merge remains human-controlled.

---

# Phase 17 — Reserved interview demo feature

Status: **RESERVED**

Do not implement until the interview demo is being prepared.

## Feature

Late-Night Refactor Risk

Example:

```text
Refactor risk: 82%

Contributing factors:
☕ High caffeine
🌙 Late-night commits

Recommendation:
DO NOT TOUCH THE ARCHITECTURE.
```

## Rules

Risk increases when:

- caffeine > 250 mg
- commits occur after 22:00
- both conditions occur together

## Requirements

- deterministic score
- score between 0 and 100
- contributing factors shown
- exact boundaries documented
- tests
- no additional runtime dependency

## Live-demo model

GPT-5.6 Sol

Reasoning:

Medium

## Why

By this point the feature should be well-scoped.

The mature harness should already provide:

- repository context
- engineering instructions
- Skills
- validation
- GitHub access

The live prompt should therefore be intentionally short.

Example:

```text
Use GitHub MCP to read issue #X.

Use the repository's standard feature-development workflow.

Start with requirement analysis and an implementation plan.

Stop for my approval before editing.
```

The short prompt is part of the demonstration.

---

# Phase 18 — Interview presentation generation

Status: **PLANNED**

## AI setup

Preferred model:

GPT-5.6 Terra

Reasoning:

Medium

## Goal

Generate a concise interview presentation from actual project evidence.

Inputs should include:

- `README.md`
- `IMPLEMENTATION_PLAN.md`
- `AI_WORKLOG.md`
- `AGENTS.md`
- repository Skills
- model-usage history
- GitHub Issues
- pull requests
- review history
- CI evidence
- Figma workflow diagram

## Presentation focus

The presentation should emphasize:

1. how the harness started,
2. how repeated problems were identified,
3. how persistent instructions were introduced,
4. how repeated workflows became Skills,
5. how models were routed deliberately,
6. how GitHub and Figma were connected,
7. how validation became deterministic,
8. where human approval remains necessary,
9. how the mature harness reduces prompt length.

The Coffee-Driven Development application remains the memorable but secondary element.

---

# Phase 19 — Final harness audit

Status: **PLANNED**

## AI setup

Preferred model:

GPT-6 Astra

Reasoning:

Highest useful setting available.

## Goal

Perform a critical read-only audit before the interview.

Evaluate:

- `AGENTS.md`
- repository engineering knowledge
- Skill justification
- model-routing decisions
- human/AI responsibility boundaries
- GitHub permissions
- independent review quality
- CI
- worklog credibility
- unnecessary complexity
- presentation theatre
- likely interviewer challenges

Return:

- five strongest aspects
- five weakest aspects
- likely interview questions
- concrete cleanup recommendations

Do not modify files during the first audit pass.

---

# Continuous process — AI worklog

Status:

**ACTIVE AFTER PHASE 3**

Meaningful AI-assisted work should be recorded through:

```text
record-ai-session
```

Log entries should record:

- date
- tool
- model
- reasoning level
- mode
- task type
- goal
- AI responsibility
- human responsibility
- outcome
- files changed
- validation
- actual friction
- actual harness changes
- lesson learned

Do not invent missing metadata.

If metadata is unavailable:

```text
not recorded
```

Do not log trivial interactions.

---

# Harness maturity model

## Level 0 — Prompt-driven

Most behavior is described repeatedly in task prompts.

## Level 1 — Repository-aware

Persistent project rules live in `AGENTS.md`.

## Level 2 — Workflow-aware

Repeated engineering behavior is extracted into reusable Skills.

## Level 3 — Tool-connected

Codex accesses real external context through systems such as:

- GitHub MCP
- Figma MCP

## Level 4 — Self-validating

The workflow receives deterministic feedback from:

- pytest
- ruff
- mypy
- GitHub Actions

## Level 5 — Bounded autonomous

Goal-based execution can carry work across multiple steps while respecting explicit human approval boundaries.

Current level:

```text
Level 2 — Workflow-aware
```

---

# Human approval gates

AI should not independently decide:

- project-scope expansion
- architecture changes
- significant dependency additions
- persistence-strategy changes
- acceptance of disputed review feedback
- destructive external operations
- final pull-request merge

The purpose of the harness is not unlimited autonomy.

The goal is useful, inspectable and bounded autonomy.

---

# Target final harness

```text
                         HUMAN
                           │
              intent / decisions / gates
                           │
                           ▼
                        CODEX
                           │
          ┌────────────────┼────────────────┐
          │                │                │
      AGENTS.md          Skills       repository docs
          │                │                │
          └────────────────┼────────────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
             GitHub MCP          Figma MCP
                 │                   │
          Issues / PRs / CI     knowledge work
                 │                   │
                 └─────────┬─────────┘
                           │
                     implementation
                           │
                 deterministic validation
                           │
                pytest / ruff / mypy
                           │
                          CI
                           │
                 independent review
                           │
                     human merge
```

The model is only one component of the harness.

The complete harness consists of:

- model selection,
- persistent repository context,
- reusable workflows,
- tools and integrations,
- deterministic validation,
- permission boundaries,
- human decisions,
- evidence of what actually happened.
