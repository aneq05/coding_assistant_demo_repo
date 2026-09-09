# Interactive Drink Picker

**Status:** specified for a future feature; not implemented.

## Goal and boundaries

The feature will replace the interactive mode's free-form primary drink prompt
with a polished numbered drink picker and expand the deterministic drink
catalog.

The direct `cdd drink <drink>` command remains supported. The interactive picker
is a presentation and selection surface over the same domain-owned drink
catalog; it MUST NOT create a separate catalog or caffeine mapping.

## Requirements

### CDD-PICK-001 — Expanded supported drink catalog

When this feature is implemented, the product MUST support the following
canonical drinks and deterministic caffeine values:

| Canonical identifier | Display name | Caffeine |
| --- | --- | ---: |
| `espresso` | Espresso | 80 mg |
| `americano` | Americano | 120 mg |
| `cappuccino` | Cappuccino | 75 mg |
| `latte` | Latte | 75 mg |
| `flat-white` | Flat White | 130 mg |
| `mocha` | Mocha | 90 mg |
| `double-espresso` | Double Espresso | 160 mg |

These values are deterministic product estimates, not medical measurements.

This requirement intentionally supersedes the exact three-drink catalog in
`CDD-FR-001` when the feature becomes implemented.

### CDD-PICK-002 — Domain-owned catalog

Canonical drink identifiers, display names, and caffeine amounts MUST have one
domain-owned source of truth.

Direct CLI recording and the interactive picker MUST resolve drinks through that
same catalog.

The implementation MUST NOT duplicate caffeine values in CLI or presentation
code.

### CDD-PICK-003 — Numbered interactive selection

Choosing `Record coffee` in interactive mode MUST display a numbered list of
available drinks.

A user MUST be able to select a drink by entering its displayed number.

The picker order MUST be deterministic and stable.

The intended order is the table order in `CDD-PICK-001`.

### CDD-PICK-004 — Visual drink identity

The interactive picker MUST present each drink with a compact visual icon.

The intended presentation mapping is:

| Drink | Icon |
| --- | --- |
| Espresso | ☕ |
| Americano | 🖤 |
| Cappuccino | 🤎 |
| Latte | 🥛 |
| Flat White | 🤍 |
| Mocha | 🍫 |
| Double Espresso | ⚡ |

Icons are presentation metadata only. They MUST NOT be persisted in history and
MUST NOT become part of the domain event schema.

### CDD-PICK-005 — Rich terminal presentation

The picker MUST use the existing Rich presentation boundary and SHOULD display
at least:

- numeric selection;
- icon;
- display name;
- deterministic caffeine amount.

A representative layout is:

```text
╭──────────── Choose your coffee ────────────╮
│ [1]  ☕  Espresso            80 mg         │
│ [2]  🖤  Americano          120 mg         │
│ [3]  🤎  Cappuccino          75 mg         │
│ [4]  🥛  Latte               75 mg         │
│ [5]  🤍  Flat White         130 mg         │
│ [6]  🍫  Mocha               90 mg         │
│ [7]  ⚡  Double Espresso    160 mg         │
╰────────────────────────────────────────────╯
```

Exact spacing and terminal width behavior are presentation details, not
normative requirements.

### CDD-PICK-006 — Backward-compatible aliases

Interactive numeric selection MUST be the primary documented path.

Canonical textual identifiers MAY remain accepted as interactive aliases for
backward compatibility, but the user MUST NOT be required to type a drink name.

The direct command MUST continue to accept canonical drink identifiers.

### CDD-PICK-007 — Invalid selection recovery

An invalid numeric or textual interactive selection MUST be reported cleanly
without a traceback and MUST allow the interactive session to recover.

It MUST NOT create a coffee event.

### CDD-PICK-008 — Same recording semantics

After a drink is selected, recording MUST use the existing coffee-event creation
and persistence semantics.

The picker MUST NOT change:

- UTC normalization;
- JSONL storage;
- daily status calculations;
- statistics calculations;
- history ordering.

If Backdated Coffee Recording is also implemented, the drink picker MUST feed
the selected drink into that same shared current/historical recording flow.

### CDD-PICK-009 — Deterministic tests

At minimum, tests MUST cover:

- the complete catalog and exact caffeine values;
- stable picker ordering;
- numeric selection for every supported drink;
- preservation of canonical direct-command identifiers;
- invalid selection recovery;
- persisted canonical drink identifier;
- no presentation icon stored in history;
- rendering of drink names, caffeine amounts, numbers, and icons.

## Affected existing requirements

This feature changes the implemented drink catalog defined by `CDD-FR-001` and
extends interactive behavior under `CDD-FR-011`.

It also preserves:

- `CDD-FR-002` — event recording;
- `CDD-FR-003` — JSONL persistence;
- `CDD-FR-005` — history;
- `CDD-FR-006` — daily status;
- `CDD-FR-007` and `CDD-FR-008` — statistics;
- `CDD-FR-012` — clean failures.

When this feature becomes implemented, `spec/product.md` MUST be updated in the
same delivery change. In particular, `CDD-FR-001` MUST no longer state that
exactly three drinks are supported.

## Architecture constraints

The feature MUST preserve the current responsibility boundaries:

```text
domain
    -> canonical drink catalog and caffeine values

presentation
    -> icons and Rich drink-picker rendering

CLI/orchestration
    -> user selection and recording flow
```

It MUST NOT add a new runtime dependency, a second drink catalog, a database,
remote API, or runtime AI.

## Out of scope

This feature does not provide:

- user-defined drinks;
- configurable caffeine amounts;
- serving-size selection;
- nutritional data;
- image assets;
- remote drink catalogs;
- fuzzy AI-based drink matching.
