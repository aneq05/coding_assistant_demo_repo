# Coffee-Driven Development

Coffee-Driven Development is two things:

1. A deliberately small, typed Python CLI for tracking coffee and developer
   activity.
2. An AI-assisted engineering harness sandbox: the product stays small so the
   repository workflow remains easy to inspect and demonstrate.

The application estimates when software engineering decisions start becoming
questionable. The interesting engineering exercise is the harness around it.

## Usage

```console
cdd drink espresso
cdd status
cdd history --limit 10
cdd stats --days 7
cdd interactive
```

For example, status after a productive morning:

```text
Coffee-Driven Development
──────────────────────────
Coffees today:      ☕ ☕
Caffeine today:     200 mg
Developer state:    PRODUCTIVE
```

Statistics over the last seven local calendar days:

```text
Coffee Statistics — last 7 days

Total coffees       9
Total caffeine      1,320 mg
Average per day     189 mg
Favorite drink      Espresso

Daily caffeine

Mon  Sep 01   █████         200 mg
Tue  Sep 02   ███████       280 mg
```

An empty day has explicit status:

```text
Coffees today:      0
Caffeine today:     0 mg
Developer state:    NO SIGNAL
```

## Why this project exists

The product is intentionally small and explainable in a couple of minutes.
That leaves room to explore how an AI-assisted engineering workflow can be
made persistent, repeatable, validated, reviewable, and human-controlled.

## Architecture

```text
CLI / orchestration
        ↓
pure domain logic
        ↓
local JSONL storage
```

Presentation is the terminal boundary: it formats domain results for the CLI,
while domain rules remain independent of command-line rendering.

## AI engineering harness

The repository contains the building blocks of a small, inspectable harness:

- persistent instructions in [`AGENTS.md`](AGENTS.md)
- reusable repository [Skills](.agents/skills/), including
  [`create-feature-issue`](.agents/skills/create-feature-issue/SKILL.md),
  [`develop-feature-tdd`](.agents/skills/develop-feature-tdd/SKILL.md),
  [`validate-review-feedback`](.agents/skills/validate-review-feedback/SKILL.md),
  and [`validate-pull-request`](.agents/skills/validate-pull-request/SKILL.md)
- a [Feature Issue template](.github/ISSUE_TEMPLATE/feature.yml)
- a [Feature Delivery Agent](.github/agents/feature-delivery.agent.md)
- a [CI Triage Agent](.github/agents/ci-triage.agent.md), configured for a
  human-selected operational exercise
- [GitHub Actions](.github/workflows/ci.yml) for deterministic validation
- context-aware AI code-review configuration in
  [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
- [`AI_WORKLOG.md`](AI_WORKLOG.md) for factual session history
- documented [model-routing evidence](docs/ai/model-usage.md)

The repository does not claim a connected GitHub MCP or Figma MCP integration:
those tool surfaces are not connected yet. GitHub capabilities documented in
[`docs/ai/github-integration-capabilities.md`](docs/ai/github-integration-capabilities.md)
are based on the evidence and boundaries recorded there.

## Engineering workflow

```text
Human goal
    → GitHub Issue
    → AI planning / TDD
    → implementation
    → local validation
    → PR
    → CI + AI review
    → feedback validation
    → human merge
```

Human approval remains required for important scope, architecture, and merge
decisions.

## Evidence

- [`AI_WORKLOG.md`](AI_WORKLOG.md)
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md)
- [`docs/ai/model-usage.md`](docs/ai/model-usage.md)
- [`docs/ai/github-integration-capabilities.md`](docs/ai/github-integration-capabilities.md)

## Product specification

[`spec/`](spec/README.md) is the authoritative, repository-owned description
of intended product behavior and architecture constraints. The implementation,
tests, roadmap, and worklog are evidence, not replacements for the
specification.

## Future demo

**Late-Night Refactor Risk** is intentionally specified but reserved for the
live demo; it is not implemented.
