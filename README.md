# Coffee-Driven Development

A deliberately over-serious coffee tracker built as a small product sandbox for
AI-assisted software engineering.

Coffee-Driven Development combines:

1. a typed Python CLI that tracks coffee, caffeine, developer state, statistics,
   and local Git activity;
2. an AI engineering harness built around repository-owned specifications,
   reusable Skills, specialist agents, LangGraph orchestration, CI, independent
   review, and human-controlled merge decisions.

<p align="center">
  <img
    src="docs/images/cdd-status.png"
    alt="Coffee-Driven Development status dashboard"
    width="100%"
  />
</p>

## Quick start

The project uses Python 3.12 and `uv`.

```console
uv sync --extra dev
uv run cdd status
```

Other commands:

```console
uv run cdd drink espresso
uv run cdd history --limit 10
uv run cdd stats --days 7
uv run cdd interactive
```

If the project's virtual environment is activated, the shorter `cdd ...`
commands are also available directly.

## Terminal experience

The CLI uses Rich for a terminal-native presentation layer while keeping domain
logic independent from rendering.

### Developer status

`cdd status` combines today's coffee telemetry with local Git activity.

<p align="center">
  <img
    src="docs/images/cdd-status.png"
    alt="CDD developer status dashboard with caffeine and Git activity"
    width="100%"
  />
</p>

Developer state remains deterministic:

```text
0 mg       -> NO SIGNAL
1-100 mg   -> BOOTING
101-250 mg -> PRODUCTIVE
251-399 mg -> TURBO MODE
400+ mg    -> ARCHITECTURE PRIVILEGES REVOKED
```

### Coffee statistics

`cdd stats --days N` shows aggregate metrics, a compact caffeine trend, and
per-day load.

<p align="center">
  <img
    src="docs/images/cdd-stats.png"
    alt="CDD seven-day coffee statistics and caffeine trend"
    width="100%"
  />
</p>

### Coffee history

`cdd history` renders recent events newest-first in local time.

<p align="center">
  <img
    src="docs/images/cdd-history.png"
    alt="CDD coffee history table"
    width="78%"
  />
</p>

### Interactive mode

`cdd interactive` exposes the same product behavior through a compact terminal
menu.

<p align="center">
  <img
    src="docs/images/cdd-interactive.png"
    alt="CDD interactive terminal menu"
    width="100%"
  />
</p>

## Product architecture

```text
CLI / orchestration
        |
        v
pure domain logic
        |
        v
local JSONL storage
```

The product runtime stays deliberately small:

```text
src/cdd/
├── cli.py
├── domain.py
├── git_activity.py
├── presentation.py
└── storage.py
```

- `cli.py` owns command orchestration and error boundaries.
- `domain.py` owns deterministic product rules.
- `storage.py` owns local JSONL persistence.
- `git_activity.py` reads deterministic local-day Git activity.
- `presentation.py` owns Rich terminal rendering.

The presentation layer can evolve visually without changing the product's
domain semantics.

## Why the product is intentionally small

The CLI is designed to be explainable in a few minutes. That keeps the product
easy to inspect while making the engineering workflow around it visible.

The repository is therefore deliberately asymmetric:

```text
small, deterministic product
        +
polished terminal presentation
        +
advanced AI engineering harness
```

The purpose is not to hide complexity inside the application. It is to make
the software-delivery system around a comprehensible application observable.

## AI engineering harness

The repository includes:

- persistent repository policy in [`AGENTS.md`](AGENTS.md);
- authoritative product requirements under [`spec/`](spec/README.md);
- reusable repository Skills under [`.agents/skills/`](.agents/skills/),
  including:
  - `create-feature-issue`
  - `develop-feature-tdd`
  - `manage-ai-run`
  - `prepare-pull-request`
  - `resolve-merge-conflict`
  - `sync-repository`
  - `validate-review-feedback`
  - `validate-pull-request`
  - `validate-specification`
- specialist agents under [`.github/agents/`](.github/agents/):
  - Feature Delivery Agent
  - CI Triage Agent
  - PR Autopilot Agent
- explicit LangGraph orchestration under
  [`ai_harness/feature_delivery/`](ai_harness/feature_delivery/);
- compact human-readable run state under [`.ai/runs/`](.ai/runs/);
- technical LangGraph SQLite checkpoints under `.ai/graph/`;
- deterministic quality gates and GitHub Actions CI;
- independent review and exact-HEAD evidence freshness;
- [`AI_WORKLOG.md`](AI_WORKLOG.md) for factual historical evidence.

Product runtime and AI orchestration are deliberately separated:

```text
src/cdd/       -> application
ai_harness/    -> explicit agent workflow orchestration
.agents/       -> reusable procedures
.github/agents -> specialist reasoning roles
spec/          -> intended product behavior
```

## Feature delivery workflow

The graph separates probabilistic engineering reasoning from deterministic
workflow control.

```text
User goal
   |
   v
GitHub Issue
   |
   v
Feature Delivery Agent
   |
   v
Feature Delivery Graph
   |
   +--> start / resume run
   |
   +--> validate scope
   |
   +--> claim Issue
   |
   +--> sync repository
   |
   +--> isolated worktree
   |
   +--> select relevant requirements from spec/
   |
   +--> TDD implementation
   |
   +--> validate specification
   |       |
   |       +--> mismatch -> bounded repair -> revalidate
   |       +--> ambiguity -> human gate
   |
   +--> local quality gate
   |       |
   |       +--> fail -> bounded repair -> rerun
   |
   +--> prepare pull request
   |
   +--> inspect current HEAD
   |
   +--> GitHub Actions CI
   |       |
   |       +--> fail -> CI triage -> correction -> quality gate -> CI
   |
   +--> mergeability check
   |       |
   |       +--> conflict -> resolve-merge-conflict -> full validation
   |
   +--> independent code review
   |       |
   |       +--> findings -> validate-review-feedback
   |                         |
   |                         +--> accepted fix
   |                              -> quality gate
   |                              -> CI
   |                              -> fresh review
   |
   +--> validate-pull-request
   |
   +--> verify current-HEAD evidence freshness
   |
   v
READY_FOR_HUMAN_MERGE
   |
   v
Human merge
```

The graph never performs the final merge and never enables auto-merge.

A HEAD-changing correction invalidates stale CI and review evidence. Final
readiness requires evidence for the same commit:

```text
current_head_sha == ci_sha == reviewed_sha
```

The implementation and reviewer models are also separated for independent
review.

For the detailed graph design, see
[`docs/ai/feature-delivery-graph.md`](docs/ai/feature-delivery-graph.md).

## Graph persistence

Two persistence layers intentionally serve different purposes:

```text
.ai/runs/
    -> compact, human-readable operational state

.ai/graph/*.sqlite3
    -> technical LangGraph checkpoints
```

The repository run record remains the human-readable operational source while
SQLite enables exact graph resumption.

## Validation

The product and harness are validated with:

```console
uv run --extra dev pytest
uv run --extra dev ruff check .
uv run --extra dev mypy
git diff --check
```

Production-code coverage is enforced at **>= 90%**.

## Evidence and documentation

- [`AI_WORKLOG.md`](AI_WORKLOG.md)
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md)
- [`docs/ai/feature-delivery-graph.md`](docs/ai/feature-delivery-graph.md)
- [`docs/ai/model-usage.md`](docs/ai/model-usage.md)
- [`docs/ai/github-integration-capabilities.md`](docs/ai/github-integration-capabilities.md)

## Product specification

[`spec/`](spec/README.md) is the authoritative repository-owned description of
intended product behavior and architecture constraints.

Implementation and tests are evidence of conformance, not replacements for the
specification.

Specification-aware delivery uses the
[`validate-specification`](.agents/skills/validate-specification/SKILL.md)
Skill before later quality and PR-readiness gates.

## Future end-to-end demo

**Late-Night Refactor Risk** is intentionally specified but not implemented.

The feature will use current local time, current-day caffeine, and current-day
local Git activity to calculate a deterministic, explainable refactor-risk
signal.

It is reserved for an end-to-end delivery demonstration:

```text
requirement
    -> Issue
    -> graph
    -> spec validation
    -> TDD implementation
    -> quality gate
    -> pull request
    -> CI
    -> independent review
    -> READY_FOR_HUMAN_MERGE
```

That keeps the final demo focused on the complete engineering workflow rather
than only on generating product code.
