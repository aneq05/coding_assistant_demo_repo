# Feature-delivery graph runtime state

`spec/`, repository Skills, custom agents, and `.ai/runs/` remain the human-readable
sources of product/workflow truth.

The SQLite database created in this directory is only a LangGraph technical
checkpoint store. It exists so an interrupted graph thread can resume after the
Python process exits.

Do not commit checkpoint database files. The graph `thread_id` must equal the
matching `.ai/runs/<run-id>.md` run identifier.

`.ai/runs/` remains the canonical compact operational run record:
- meaningful completed stages,
- evidence-backed decisions,
- blocker,
- next action.

The SQLite checkpoint may contain lower-level engine state and is disposable
after the run no longer needs technical resumption.
