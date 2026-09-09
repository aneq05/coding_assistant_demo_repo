---
name: validate-specification
description: Validate a scoped implementation, diff, pull request, or feature against the authoritative product specification under spec/; use when conformance, traceability, requirement coverage, or specification mismatch must be assessed before delivery or graph progression.
---

# Validate specification conformance

Use the repository-owned specification as the authority for intended product behavior and architecture. Read the configured specification index first, then load only the requirement documents relevant to the current task.

Do not treat implementation or tests as automatically authoritative when they conflict with normative requirements. Do not rewrite the specification merely to make current code appear compliant.

## Validate

1. Determine the validation scope from the available Issue, requirement IDs, diff, branch, pull request, or current implementation context.
2. Read `.ai/harness.config.json` and use the configured specification index and root. Prefer targeted retrieval from `spec/README.md`; do not load the full specification when a smaller requirement subset is sufficient.
3. Identify the relevant normative requirement IDs and any architecture constraints affected by the change.
4. Compare each relevant requirement against available evidence from implementation, tests, and the current diff or PR.
5. Distinguish clearly between:
   - implementation defect,
   - missing or inadequate test evidence,
   - specification ambiguity or contradiction,
   - intentionally specified but not-yet-implemented future behavior.
6. Do not classify future requirements as mismatches merely because their documented status is `specified, not implemented`.
7. Return one overall result:
   - `CLEAR` — relevant implementation and evidence conform to the applicable specification;
   - `MISMATCH` — a concrete actionable discrepancy exists;
   - `UNKNOWN` — available evidence is insufficient to establish conformance;
   - `HUMAN_REVIEW_REQUIRED` — product intent, architecture, scope, or conflicting evidence requires a human decision.
8. For `MISMATCH`, identify the exact requirement IDs and whether the defect is in implementation, tests, or both. Prefer correcting implementation/tests rather than weakening the specification when correction is within the authorized scope.
9. For ambiguous or conflicting normative intent, stop and route to the repository's human architecture/product decision gate instead of choosing an interpretation.
10. After an authorized correction, re-run specification validation against the affected requirements before treating the change as conforming.

## Traceability

Keep output scoped and concise. For each relevant requirement, report evidence in this form:

```text
CDD-FR-012
specification: found
implementation: found
tests: found
status: CLEAR
```

or:

```text
CDD-FR-014
specification: found
implementation: inconsistent
tests: missing expected behavior
status: MISMATCH
```

Do not generate repository-wide traceability matrices when the task affects only a small requirement subset.

## Run-state integration

For meaningful multi-stage or resumable work, use the existing `manage-ai-run` capability and `.ai/runs/` state rather than creating another persistence mechanism.

Persist only compact continuation state when useful, such as:

```text
relevant_requirement_ids
specification_status
mismatched_requirement_ids
unresolved_requirement_ids
```

Do not copy full specification documents, prompts, transcripts, or long analysis into run state.

## Routing boundaries

- Let the graph or caller own retry limits, global orchestration, and cross-workflow state transitions.
- Use existing implementation, TDD, validation, PR, review-feedback, merge-conflict, and delivery capabilities instead of reproducing them here.
- The repository quality gate remains authoritative for pytest, coverage, ruff, and mypy.
- A `CLEAR` result does not authorize merge or architecture changes.
- Material product-scope, architecture, dependency, permission, or specification changes remain human-controlled.

Return a concise conformance result containing:

```text
scope
relevant requirement IDs
overall status
requirement-level findings
mismatches
unresolved items
human gate, if any
recommended next action
```
