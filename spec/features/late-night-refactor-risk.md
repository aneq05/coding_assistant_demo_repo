# Late-Night Refactor Risk

**Status:** specified for a future feature; not implemented.

## Goal and boundaries

The feature will extend developer status with an explainable deterministic
assessment of refactor risk using only current local time, current-day caffeine,
and current-day local Git activity. It is intentionally local: no network,
remote GitHub data, runtime AI, or LLM inference is in scope.

## Requirements

### CDD-RISK-001 — Inputs

The assessment MUST use an injected timezone-aware current local time, the
current local-day caffeine total, and current local-day Git activity. Tests
MUST be able to supply fixed values for all inputs.

### CDD-RISK-002 — Bounded score

The assessment MUST return an integer score from 0 through 100 inclusive. The
score MUST be the capped sum of the contributions in `CDD-RISK-003` through
`CDD-RISK-006`.

### CDD-RISK-003 — Caffeine contribution

Current-day caffeine of 251 mg or more MUST add 40 points; 250 mg or less MUST
add 0 points.

### CDD-RISK-004 — Current-time contribution

A current local time from 22:00 inclusive through 23:59 inclusive MUST add 20
points. Any other local time MUST add 0 points.

### CDD-RISK-005 — Git-volume contribution

Current-day commits MUST add 0 points for 0 commits, 10 points for 1–2, 20
points for 3–5, and 30 points for 6 or more commits.

### CDD-RISK-006 — Late-commit contribution

One or more current-day local commits timestamped from 22:00 inclusive through
23:59 inclusive MUST add 30 points; otherwise they MUST add 0 points.

### CDD-RISK-007 — Categories and explanation

Scores of 0–24 MUST be `LOW`, 25–49 `MODERATE`, 50–74 `HIGH`, and 75–100
`CRITICAL`. The result MUST identify every nonzero contributing factor so the
score is explainable.

### CDD-RISK-008 — Git unavailability

When local Git data is unavailable, the assessment MUST remain successful and
calculate with zero Git-volume and late-commit contributions. It MUST identify
Git activity as unavailable rather than infer remote activity.

### CDD-RISK-009 — Deterministic local implementation

Scoring MUST be deterministic and independently testable. It MUST NOT invoke
an LLM, network service, or remote GitHub API.

## Out of scope

This feature does not diagnose developer wellbeing, predict code quality,
inspect source code or diffs, infer intent, collect remote activity, persist
risk scores, or prescribe automated engineering actions. Its category is a
local, explainable signal only.
