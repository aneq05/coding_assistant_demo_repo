# Coffee-Driven Development — Implementation Plan

## Purpose

Coffee-Driven Development (CDD) is intentionally a small and slightly
ridiculous Python CLI.

The product itself is deliberately simple.

The primary purpose of this repository is to progressively build,
test and demonstrate an AI-assisted engineering harness suitable for
a Forward Deployed Engineer workflow.

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
- CI validation,
- bounded autonomous execution,
- human approval at important decision boundaries.

The harness should evolve based on observed repetition, friction and
real project needs rather than being fully designed upfront.

---

# AI model routing policy

Do not use the strongest model by default.

Choose the lowest-cost model that can reliably perform the task.

Escalate based on:

- ambiguity,
- architectural impact,
- difficulty,
- risk,
- observed failure of a cheaper model.

Current available models:

- GPT-6 Astra
- GPT-5.6 Sol
- GPT-5.6 Terra
- GPT-5.6 Luna
- GPT-5.5
- GPT-5.4 Mini

Default project routing:

| Task type | Preferred model | Reasoning |
| --- | --- | --- |
| Simple documentation / worklog | GPT-5.6 Luna | Low |
| Planning / lightweight harness configuration | GPT-5.6 Terra | Medium |
| Normal implementation | GPT-5.6 Sol | Medium |
| Architecture / difficult implementation | GPT-5.6 Sol | High |
| Independent critical review | GPT-6 Astra | High |
| Final whole-repository audit | GPT-6 Astra | Highest useful setting |

Model selection should be recorded in `AI_WORKLOG.md`.

---

# Current status

Current phase:

**Phase 3 — Harness baseline and reusable session logging**

The repository currently contains only the engineering foundation.
The core product functionality and most of the AI harness are still intentionally
not implemented.

## Completed

- [x] Phase 0 — Repository initialization
- [x] Phase 1 — Initial architecture exploration
- [x] Phase 2 — Engineering foundation
- [x] Create project implementation roadmap

Current repository capabilities:

- [x] Python 3.12+ project configured
- [x] `src` package layout
- [x] `cdd` CLI entry point
- [x] `cdd --help`
- [x] pytest configured
- [x] ruff configured
- [x] mypy configured
- [x] initial `AGENTS.md`
- [x] initial `AI_WORKLOG.md`
- [x] model-selection strategy started

Product functionality implemented so far:

- [ ] coffee tracking
- [ ] persistent history
- [ ] developer status
- [ ] Git activity
- [ ] refactor-risk scoring

AI harness capabilities implemented so far:

- [x] repository-level agent instructions
- [x] model/reasoning selection recorded manually
- [ ] automatic AI session logging
- [ ] repository Skills
- [ ] engineering knowledge base
- [ ] testing workflow Skill
- [ ] feature-development workflow
- [ ] GitHub MCP
- [ ] independent AI PR review
- [ ] Figma MCP
- [ ] Goal-based delegation
- [ ] presentation-generation workflow

---

# Immediate next steps

## Phase 3 — Harness baseline

- [ ] Backfill the two historical `AI_WORKLOG.md` entries
- [ ] Create first repository Skill: `record-ai-session`
- [ ] Add a minimal routing rule to `AGENTS.md`
- [ ] Verify that the Skill records the current session correctly
- [ ] Ensure future meaningful AI sessions are logged automatically
- [ ] Decide whether the current Make-based quality gate should remain
      or be replaced/supplemented with a cross-platform command

## Phase 4 — First actual product feature

- [ ] Implement `cdd drink <drink>`
- [ ] Add espresso
- [ ] Add americano
- [ ] Add cappuccino
- [ ] Keep caffeine calculation independent from CLI rendering
- [ ] Add first meaningful domain tests
- [ ] Observe whether testing instructions start becoming repetitive

## Phase 5 — Persistence

- [ ] Add drink-event model
- [ ] Persist timestamp, drink type and caffeine amount
- [ ] Implement JSON/JSONL local storage
- [ ] Make storage path injectable
- [ ] Add filesystem-isolated tests
- [ ] Ensure tests never modify the real user home directory

## Phase 6 — Status and history

- [ ] Implement `cdd history`
- [ ] Implement `cdd status`
- [ ] Calculate caffeine consumed today
- [ ] Add deterministic developer states
- [ ] Keep status calculation as pure domain logic
- [ ] Add humorous terminal presentation

---

# Roadmap at a glance

## Foundation

- [x] Phase 0 — Repository initialization
- [x] Phase 1 — Architecture exploration
- [x] Phase 2 — Engineering foundation
- [ ] Phase 3 — Reusable AI session logging

## Product MVP

- [ ] Phase 4 — `cdd drink`
- [ ] Phase 5 — Local persistence
- [ ] Phase 6 — `cdd status` and `cdd history`

## Harness evolution

- [ ] Phase 7 — Harness retrospective
- [ ] Phase 8 — Repository engineering knowledge
- [ ] Phase 9 — Unit-testing Skill

## GitHub engineering workflow

- [ ] Phase 10 — GitHub Actions CI
- [ ] Phase 11 — GitHub MCP integration
- [ ] Phase 12 — Git activity feature through a GitHub Issue
- [ ] Phase 13 — Independent AI pull-request review
- [ ] Phase 14 — AI review-feedback validation

## Knowledge work and increased autonomy

- [ ] Phase 15 — Figma MCP workflow documentation
- [ ] Phase 16 — Bounded Goal-based delegation

## Interview preparation

- [ ] Phase 17 — Reserved live-demo feature: Late-Night Refactor Risk
- [ ] Phase 18 — Generate interview presentation from project evidence
- [ ] Phase 19 — Final critical harness audit

## Goal

Create the initial repository manually before delegating meaningful work
to AI.

## Human-created files

- `README.md`
- `AGENTS.md`
- `AI_WORKLOG.md`
- `.gitignore`

## Repository purpose

The application was deliberately defined as a small Python CLI so that
the engineering workflow around it remains the main focus.

Initial intended product capabilities:

```text
cdd drink espresso
cdd status
cdd history