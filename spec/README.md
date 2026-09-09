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

This index is the entry point for task-scoped retrieval. Feature files should
list only the IDs they own and their status, so a future traceability graph can
read the relevant node without loading every specification file.

## Requirement conventions

`FR` identifies functional requirements, `AR` intentional architecture
requirements, `NFR` product-level non-functional requirements, and `RISK`
requirements for the named future feature. Each identifier is stable; retired
requirements should be marked as retired rather than reused.

## Change flow

```text
requirement → specification → implementation → tests → conformance validation
```

Behavior-changing work SHOULD identify affected requirement IDs. A code change
MUST NOT silently alter normative behavior, and a specification change MUST NOT
silently excuse nonconforming code. Conformance automation is intentionally not
part of this phase.

## Documents

- [Current product requirements](product.md)
- [Architecture requirements](architecture.md)
- [Late-Night Refactor Risk](features/late-night-refactor-risk.md)
