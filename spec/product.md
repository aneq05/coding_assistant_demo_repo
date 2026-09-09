# Current product requirements

## Context

Coffee-Driven Development is a local command-line coffee tracker that presents
deterministic coffee and local developer-activity signals. The requirements in
this document describe currently implemented product behavior.

## Functional requirements

### CDD-FR-001 — Supported drinks

The product MUST support exactly `espresso` (80 mg), `americano` (120 mg), and
`cappuccino` (75 mg) as named drink choices. Each choice MUST have its stated,
deterministic caffeine value. An unsupported choice MUST be rejected rather
than substituted.

### CDD-FR-002 — Coffee-event recording

A successful drink action MUST record the selected drink, its caffeine amount,
and a timezone-aware occurrence time. Stored event times MUST be normalized to
UTC; a timezone-naive time MUST be rejected. A successful command MUST confirm
the drink and its estimated caffeine amount.

### CDD-FR-003 — Local history persistence

Coffee history MUST persist locally at the repository-local
`.cdd/history.jsonl` path by default.

The runtime data directory MUST remain excluded from version control.

Each event MUST be appended as one independently parseable JSON object line,
and a new event MUST preserve existing events.

### CDD-FR-004 — History integrity

Reading a missing history MUST produce an empty history. Empty lines MAY be
ignored. A malformed nonempty record or invalid history encoding MUST be
reported as a history error; it MUST NOT be silently skipped or partially used.

### CDD-FR-005 — Recent history

`cdd history` MUST show recorded events newest first, with timestamps displayed
in local time. It MUST default to the 20 most recent events and accept only a
positive `--limit`. An empty history MUST be explicit to the user.

### CDD-FR-006 — Daily coffee status

`cdd status` MUST calculate coffee count and caffeine from events on the
current local calendar day only. It MUST derive developer state as: 0 mg = `NO
SIGNAL`; 1–100 = `BOOTING`; 101–250 = `PRODUCTIVE`; 251–399 = `TURBO MODE`;
400 mg or more = `ARCHITECTURE PRIVILEGES REVOKED`.

### CDD-FR-007 — Recent statistics

`cdd stats` MUST report a requested positive number of local calendar days,
including today. It MUST include zero-consumption days, exclude older events,
and reject a period that cannot be represented before the minimum calendar
date.

### CDD-FR-008 — Statistics calculations

Statistics MUST report total coffees, total caffeine, average caffeine per day
including zero days, a daily caffeine total for every day in the window, and a
favorite drink. The favorite is the most frequently recorded drink in the
window; ties MUST resolve alphabetically. With no events, favorite drink MUST
be absent and the product MUST state that no data exists.

### CDD-FR-009 — Local Git activity

`cdd status` MUST also report the number of commits on the current local
calendar day, the latest such commit time when present, and an activity level.
Levels are: 0 = `QUIET`; 1–2 = `ACTIVE`; 3–5 = `SHIPPING`; 6 or more = `DEEP
WORK`. Outside a Git repository, or when local Git cannot be queried, status
MUST remain successful with zero commits and no latest commit.

### CDD-FR-010 — Command interface

The CLI MUST provide `drink <drink>`, `history [--limit N]`, `status`, `stats
[--days N]`, and `interactive`. Help MUST be available successfully. Invalid
numeric options MUST be rejected unless they are positive integers.

### CDD-FR-011 — Interactive mode

Interactive mode MUST provide add-drink, status, history, statistics, and exit
paths over the same product behavior as direct commands. It MUST not create a
separate set of business rules or persistence semantics.

### CDD-FR-012 — User-facing failures

Expected invalid input, history read failures, and event-persistence failures
MUST be presented as clean user-facing errors without a traceback. Interactive
invalid selections and EOF or interruption at a menu or drink prompt MUST exit
or recover gracefully.

## Non-functional requirements

### CDD-NFR-001 — Deterministic local operation

For fixed events, local-time conversion, clock, and Git-command results, the
product MUST produce deterministic business results. It MUST require no network
access for normal operation.

### CDD-NFR-002 — Testable time boundaries

Time-sensitive behavior MUST permit controlled, timezone-aware clock and local
time inputs so local-day and daylight-saving boundaries can be tested without
using a developer's real history or clock.
