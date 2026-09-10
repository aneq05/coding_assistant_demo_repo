# Coffee-Driven Development product specification

## Authority and scope

`spec/` is the repository-owned, authoritative description of intended
product behavior and intentional product architecture constraints. It is
separate from:

- `AGENTS.md`, which governs agent operation;
- `docs/engineering/`, which records engineering practices; and
- `docs/IMPLEMENTATION_PLAN.md` and `AI_WORKLOG.md`, which preserve roadmap
  and historical evidence.

Implementation and tests are evidence of the current state, not an automatic
replacement for this specification. Conversely, a reconstructed requirement
must not be treated as settled authority when repository evidence genuinely
conflicts. Record the conflict here and obtain human resolution before changing
normative behavior or silently rewriting the specification to fit code.

Material product scope and architecture changes remain human-controlled.

## Retrieval index

| Area | Requirement IDs | Status | Unresolved ambiguities |
| --- | --- | --- | --- |
| Current product behavior | `CDD-FR-001`–`CDD-FR-012`, `CDD-NFR-001`–`CDD-NFR-002` | implemented | none recorded |
| Product architecture | `CDD-AR-001`–`CDD-AR-007` | current constraint | none recorded |
| Late-Night Refactor Risk | `CDD-RISK-001`–`CDD-RISK-009` | specified, not implemented | none recorded |
| Backdated Coffee Recording | `CDD-HIST-001`–`CDD-HIST-009` | implemented | none recorded |
| Interactive Drink Picker | `CDD-PICK-001`–`CDD-PICK-009` | specified, not implemented | none recorded |

This index is the entry point for task-scoped retrieval. Feature files should
list only the IDs they own and their status, so a future traceability graph can
read the relevant node without loading every specification file.

A feature marked `specified, not implemented` describes intended future
behavior. It is not evidence that the current implementation is nonconforming.
When such a feature is implemented, the same delivery change MUST update this
index and any affected current-product requirements so that `product.md`
describes the newly implemented state without leaving contradictory normative
requirements behind.

## Requirement conventions

`FR` identifies functional requirements, `AR` intentional architecture
requirements, `NFR` product-level non-functional requirements, `RISK`
requirements for Late-Night Refactor Risk, `HIST` requirements for Backdated
Coffee Recording, and `PICK` requirements for the Interactive Drink Picker.

Each identifier is stable; retired requirements should be marked as retired
rather than reused.

## Change flow

```text
requirement → specification → implementation → tests → conformance validation
```

Behavior-changing work SHOULD identify affected requirement IDs. A code change
MUST NOT silently alter normative behavior, and a specification change MUST NOT
silently excuse nonconforming code.

## Documents

- [Current product requirements](product.md)
- [Architecture requirements](architecture.md)
- [Late-Night Refactor Risk](features/late-night-refactor-risk.md)
- [Backdated Coffee Recording](features/backdated-coffee-recording.md)
- [Interactive Drink Picker](features/interactive-drink-picker.md)
