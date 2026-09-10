# Interactive Project Mind Map

This folder contains an interactive mind map of the **Coffee-Driven Development** project.

The map is a standalone HTML page designed to provide a quick visual walkthrough of the project without requiring the viewer to browse the whole repository first. It can be used during a technical interview, project demo, or repository walkthrough.

## What is included

The map is organized around four main areas.

### 1. Product overview

This section presents the main CLI capabilities:

- `drink` — records a coffee event together with its caffeine value and timestamp,
- `history` — displays previously recorded coffee events,
- `status` — combines today's caffeine intake with the calculated developer state and local Git activity,
- `stats` — summarizes coffee consumption and daily trends,
- `interactive` — exposes the main commands through a terminal menu.

The section also includes screenshots of the CLI in action.

For the `status` view, the map additionally shows the deterministic levels used by the application:

**Developer state**

```text
0 mg       -> NO SIGNAL
1-100 mg   -> BOOTING
101-250 mg -> PRODUCTIVE
251-399 mg -> TURBO MODE
400+ mg    -> ARCHITECTURE PRIVILEGES REVOKED
```

**Git activity**

```text
0 commits -> QUIET
1-2       -> ACTIVE
3-5       -> SHIPPING
6+        -> DEEP WORK
```

### 2. Repository organization

This section explains the repository layout and why the AI-related parts are separated into different layers.

The goal of this structure is to create a lightweight framework for managing AI-assisted engineering work, where persistent rules, reusable procedures, agent roles, CI, runtime state, and historical evidence have clearly separated responsibilities.

The map includes short descriptions of:

**Specialist agents**

- **Feature Delivery Agent** — coordinates feature work from specification or issue to a validated Pull Request.
- **CI Triage Agent** — analyzes failed CI runs and supports controlled repair based on CI evidence.
- **PR Autopilot Agent** — coordinates final PR readiness, review feedback, validation, and evidence freshness.

**Reusable Skills**

- `create-feature-issue`
- `develop-feature-tdd`
- `harness-retrospective`
- `manage-ai-run`
- `prepare-pull-request`
- `record-ai-session`
- `resolve-merge-conflict`
- `sync-repository`
- `validate-pull-request`
- `validate-review-feedback`
- `validate-specification`

Each Skill represents a reusable engineering procedure rather than a one-off prompt.

**AI harness and runtime files**

- `.ai/harness.config.json` — shared harness policy and retry configuration,
- `.ai/runs/` — operational state for AI-assisted runs,
- `.ai/graph/checkpoints.sqlite3` — LangGraph checkpoints used for workflow persistence and resumption,
- `ai_harness/feature_delivery/` — deterministic feature-delivery orchestration,
- `AI_WORKLOG.md` — human-readable history of AI-assisted work and evidence.

**MCP integrations**

- **GitHub MCP** — gives AI tools structured access to repository context such as issues, Pull Requests, code, and CI-related information.
- **Figma MCP** — is used to work with visual project materials and presentation assets while keeping design context available to the AI workflow.

### 3. Engineering quality

This section summarizes the deterministic quality controls used around AI-assisted changes:

- Test-Driven Development,
- `pytest`,
- `Ruff`,
- `mypy`,
- coverage checks,
- `git diff --check`,
- evidence-driven validation,
- independent review,
- human gates,
- human-controlled final merge.

The core idea is that AI can perform engineering work, but readiness is determined by explicit validation evidence rather than by trusting the model output alone.

### 4. End-to-end workflow

The workflow section presents the complete feature-delivery path:

```text
USER PROMPT
   |
   v
FEATURE DELIVERY AGENT
   |
   v
READ SPEC
   |
   v
START / RESUME RUN
   |
   v
VALIDATE SCOPE
   |
   v
CLAIM ISSUE
   |
   v
SYNC REPOSITORY
   |
   v
CREATE ISOLATED WORKTREE
   |
   v
SELECT REQUIREMENTS
   |
   v
TDD IMPLEMENTATION
   |
   v
VALIDATE SPECIFICATION
   |
   v
LOCAL QUALITY GATE
pytest / ruff / mypy / coverage
   |
   v
PREPARE PR
   |
   v
PUSH
   |
   v
CURRENT HEAD SHA
   |
   v
GITHUB ACTIONS CI
   |
   v
MERGEABILITY CHECK
   |
   v
INDEPENDENT REVIEW
   |
   v
VALIDATE PR
   |
   v
VERIFY

HEAD == CI SHA == REVIEW SHA
   |
   v
READY_FOR_HUMAN_MERGE
   |
   v
HUMAN MERGES
```

The interactive diagram also shows the repair paths for:

- specification mismatches,
- local quality-gate failures,
- CI failures,
- merge conflicts,
- review findings.

The final merge remains a human decision.

## How to run the mind map

### Option 1 — open it directly

Open:

```text
docs/interactive-map/index.html
```

in a browser.

### Option 2 — run a local HTTP server

From the repository root:

```powershell
python -m http.server 8000 -d docs/interactive-map
```

Then open:

```text
http://localhost:8000
```

Running the local server is recommended when presenting the project.

## How to use it

- Click one of the four main tiles to expand its section.
- Click the same tile again to collapse it.
- Selecting another tile replaces the currently expanded section.
- Use **Presentation Mode** for a cleaner view.
- Press `F11` in the browser to enter fullscreen mode.

## Files

```text
docs/interactive-map/
├── index.html
└── README.md
```

The map is self-contained and does not require an additional frontend framework or build step.
