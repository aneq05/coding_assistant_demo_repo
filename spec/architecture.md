# Architecture requirements

## Intent

The runtime remains deliberately small, local, and deterministic. The intended
responsibility direction is:

```text
CLI / orchestration
        ↓
domain logic
        ↓
storage / external systems
```

Orchestration may coordinate the domain with storage or local Git at the
boundary; this diagram expresses responsibility, not a requirement that the
domain call external systems.

## Requirements

### CDD-AR-001 — Responsibility boundaries

CLI orchestration MUST parse requests, coordinate use cases, and translate
expected failures at the user boundary. Domain logic MUST own deterministic
product calculations. Storage and external-system access MUST remain at their
respective boundaries.

### CDD-AR-002 — Presentation separation

Presentation MUST format domain and external results for the terminal without
owning business rules. Changes to terminal rendering MUST NOT require changing
deterministic domain rules solely for display purposes.

### CDD-AR-003 — Framework-independent domain

Domain logic MUST NOT depend on Rich or `argparse`. It MUST remain usable and
independently testable without command-line parsing or terminal rendering.

### CDD-AR-004 — Storage isolation

Storage serialization, filesystem behavior, and malformed-record handling MUST
NOT leak into domain calculations. Domain calculations MUST consume product
events, not filesystem records.

### CDD-AR-005 — External-system isolation

Local Git invocation and its availability failures MUST remain outside the
domain calculations. Deterministic mapping from a commit count to an activity
level MAY reside in the domain.

### CDD-AR-006 — No runtime AI

Runtime product behavior MUST NOT use AI or LLM inference unless a future
requirement explicitly authorizes it.

### CDD-AR-007 — Justified simplicity

The product MUST NOT add service layers, repository abstractions, dependency
injection frameworks, plugins, ORMs, remote infrastructure, or runtime
dependencies without a concrete product requirement and justification.
