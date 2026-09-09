"""Small CLI for starting/resuming the repository feature-delivery graph.

The caller executes capability requests with the repository's existing
Skill/custom-agent system, then resumes with the returned JSON object.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from contextlib import closing
from typing import Any

os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from ai_harness.feature_delivery.config import load_graph_policy
from ai_harness.feature_delivery.graph import build_delivery_graph
from ai_harness.feature_delivery.state import initial_state


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Drive the feature-delivery graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("--run-id", required=True)
    start.add_argument("--issue", type=int, required=True)
    start.add_argument("--implementation-model")

    resume = sub.add_parser("resume")
    resume.add_argument("--run-id", required=True)
    resume.add_argument("--result-json", required=True)

    state = sub.add_parser("state")
    state.add_argument("--run-id", required=True)
    return parser


def _config(run_id: str) -> dict[str, dict[str, str]]:
    return {"configurable": {"thread_id": run_id}}


def _print_result(result: Any) -> None:
    interrupts = result.get("__interrupt__", ()) if isinstance(result, dict) else ()
    if interrupts:
        payload = interrupts[0].value
        print(json.dumps({"status": "INTERRUPTED", "request": payload}, indent=2))
        return

    if isinstance(result, dict):
        printable = {
            "status": "FINISHED",
            "outcome": result.get("outcome"),
            "head_sha": result.get("head_sha"),
            "pr_number": result.get("pr_number"),
            "events": result.get("events", []),
        }
        print(json.dumps(printable, indent=2))
        return

    print(json.dumps({"status": "UNKNOWN_RESULT", "repr": repr(result)}, indent=2))


def _open_graph() -> tuple[Any, sqlite3.Connection]:
    policy = load_graph_policy()
    policy.checkpoint_db.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(policy.checkpoint_db, check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    graph = build_delivery_graph(policy=policy, checkpointer=checkpointer)
    return graph, connection


def main() -> int:
    args = _parser().parse_args()
    graph, connection = _open_graph()

    with closing(connection):
        config = _config(args.run_id)

        if args.command == "start":
            result = graph.invoke(
                initial_state(
                    run_id=args.run_id,
                    issue_number=args.issue,
                    implementation_model=args.implementation_model,
                ),
                config=config,
            )
            _print_result(result)
            return 0

        if args.command == "resume":
            payload = json.loads(args.result_json)
            if not isinstance(payload, dict):
                raise ValueError("--result-json must decode to a JSON object")
            result = graph.invoke(Command(resume=payload), config=config)
            _print_result(result)
            return 0

        if args.command == "state":
            snapshot = graph.get_state(config)
            print(json.dumps(snapshot.values, indent=2, default=str))
            return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
