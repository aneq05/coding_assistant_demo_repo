# Backdated Coffee Recording

**Status:** implemented.

## Goal and boundaries

The feature will allow a user to record a supported coffee at an explicit past
occurrence time instead of always using the current clock.

The feature extends the existing coffee-event recording flow. It does not
introduce a second event type, a second persistence format, remote storage,
calendar synchronization, or retrospective editing of an already persisted
event.

The existing behavior remains the default: when no explicit occurrence time is
provided, a coffee is recorded at the current injected/system time.

## Requirements

### CDD-HIST-001 — Optional explicit occurrence time

The direct `drink` command MUST accept an optional explicit occurrence time in
addition to the existing drink identifier.

The intended command surface is:

```text
cdd drink <drink> [--at <timestamp>]
```

Omitting `--at` MUST preserve the existing current-time behavior.

### CDD-HIST-002 — Aware ISO 8601 input

`--at` MUST accept a timezone-aware ISO 8601 timestamp, for example:

```text
2026-09-05T14:30:00+02:00
```

A malformed timestamp or a timezone-naive timestamp MUST be rejected as clean
user input error rather than silently interpreted in an assumed timezone.

### CDD-HIST-003 — Historical-only recording

An explicitly supplied occurrence time MUST NOT be later than the current
injected/system time used by the command.

A future timestamp MUST be rejected and MUST NOT create a history record.

An occurrence time equal to the current time MAY be accepted.

### CDD-HIST-004 — Existing event contract

A backdated coffee MUST use the existing `CoffeeEvent` contract and the same
supported-drink lookup as a current-time coffee.

The persisted timestamp MUST continue to be timezone-aware and normalized to
UTC before storage.

The JSONL schema and default history path MUST NOT change.

### CDD-HIST-005 — Interactive time choice

The interactive add-coffee flow MUST allow the user to choose whether the
selected coffee should be recorded:

1. now; or
2. at an explicit historical occurrence time.

The default and shortest path MUST remain `now`.

The custom-time path MUST use the same timestamp parsing and validation rules as
the direct `--at` option.

### CDD-HIST-006 — Shared behavior

Direct and interactive recording MUST reuse the same timestamp-validation and
event-creation behavior. They MUST NOT implement separate rules for historical
recording.

### CDD-HIST-007 — Downstream behavior

A successfully recorded historical event MUST participate in existing history,
daily status, and statistics calculations according to its persisted occurrence
timestamp.

Recording a historical event MUST NOT alter Git activity or infer any Git
activity for that historical date.

### CDD-HIST-008 — Failure behavior

Invalid explicit timestamps, timezone-naive timestamps, future timestamps, and
event-persistence failures MUST produce clean user-facing errors without a
traceback.

A rejected historical input MUST NOT append a partial or fallback event.

### CDD-HIST-009 — Deterministic testability

Tests MUST be able to inject the current clock and explicit occurrence timestamp
so boundary behavior can be validated without relying on the machine's real
clock.

At minimum, tests MUST cover:

- omitted `--at` preserving current behavior;
- a valid timestamp in a non-UTC offset being persisted as UTC;
- invalid ISO input;
- timezone-naive input;
- a future timestamp;
- interactive `now`;
- interactive historical recording;
- downstream history/statistics inclusion.

## Affected existing requirements

This feature extends:

- `CDD-FR-002` — Coffee-event recording;
- `CDD-FR-010` — Command interface;
- `CDD-FR-011` — Interactive mode;
- `CDD-FR-012` — User-facing failures;
- `CDD-NFR-002` — Testable time boundaries.

It MUST preserve `CDD-FR-003` and `CDD-FR-004` storage/history integrity.

When implementation becomes current product behavior, `spec/product.md` MUST be
updated in the same delivery change so these extensions are represented there.

## Architecture constraints

The feature MUST preserve `CDD-AR-001` through `CDD-AR-007`.

Timestamp parsing/validation may be introduced as a small deterministic helper,
but no framework, service layer, database, network dependency, or runtime AI is
justified by this feature.

## Out of scope

This feature does not provide:

- editing or deleting existing events;
- future/scheduled coffee events;
- timezone inference from geographic names;
- calendar integration;
- bulk history import;
- remote synchronization;
- Git activity reconstruction for historical dates.
