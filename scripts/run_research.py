from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from supervisor import KSupervisorApplication, MVPStatus
from tools import JsonCorpusProvider, ResearchToolset, WebFetchTool, WebSearchTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the K_Supervisor Phase 9 end-to-end MVP.")
    parser.add_argument("--task", help="Research task. If omitted, it is requested interactively.")
    parser.add_argument("--task-type", default="auto")
    parser.add_argument("--corpus", required=True, help="UTF-8 JSON evidence corpus used by the local MVP provider.")
    parser.add_argument("--output-directory", default="output")
    parser.add_argument("--max-iterations", type=int, default=3)
    parser.add_argument("--approve-profile", action="store_true", help="Treat this command invocation as explicit profile approval.")
    parser.add_argument("--profile-edits", help="JSON object of CriticProfile edits applied before explicit approval.")
    parser.add_argument("--special-requirement", action="append", default=[])
    parser.add_argument("--required-topic", action="append", default=[])
    parser.add_argument("--search-query", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    task_text = (args.task or "").strip()
    if not task_text:
        try:
            task_text = input("Research task: ").strip()
        except EOFError:
            print("ERROR: --task is required in non-interactive mode.")
            return 1
    if not task_text:
        print("ERROR: research task cannot be empty.")
        return 1

    try:
        provider = JsonCorpusProvider.from_file(args.corpus)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load corpus: {exc}")
        return 1

    tools = ResearchToolset(WebSearchTool(provider), WebFetchTool(provider))
    app = KSupervisorApplication(
        tools,
        output_directory=Path(args.output_directory),
        default_max_iterations=args.max_iterations,
    )
    prepared = app.prepare_task(
        task_text,
        task_type=args.task_type,
        max_iterations=args.max_iterations,
        special_user_requirements=list(args.special_requirement),
    )

    print(f"Task ID: {prepared.task.task_id}")
    print("Domain assessment:")
    print(prepared.domain_assessment.model_dump_json(indent=2))
    print("CriticProfile proposal:")
    print(prepared.critic_profile.model_dump_json(indent=2))

    edits = _parse_edits(args.profile_edits)
    if edits is None and args.profile_edits is not None:
        return 1

    if args.approve_profile:
        app.approve_profile(prepared.task.task_id, approved_by="CLI_USER", edits=edits)
    else:
        approval = _interactive_profile_gate(app, prepared.task.task_id, edits)
        if not approval:
            return 4

    research_input: dict[str, Any] = {}
    if args.search_query:
        research_input["search_queries"] = list(args.search_query)
    if args.required_topic:
        research_input["requirements"] = list(args.required_topic)
    critic_input = {"required_topics": list(args.required_topic)} if args.required_topic else None

    outcome = app.run_to_completion(
        prepared.task.task_id,
        research_input=research_input or None,
        critic_input=critic_input,
    )
    print(f"MVP status: {outcome.status.value}")
    print(f"Final task state: {outcome.final_state.value}")
    for path in outcome.artifact_paths:
        print(f"Artifact: {path}")

    if outcome.status == MVPStatus.SUCCESS:
        return 0
    if outcome.status == MVPStatus.LIMITATION:
        return 2
    return 1


def _parse_edits(raw: str | None) -> dict[str, Any] | None:
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --profile-edits must be valid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        print("ERROR: --profile-edits must decode to a JSON object.")
        return None
    return value


def _interactive_profile_gate(
    app: KSupervisorApplication,
    task_id: str,
    initial_edits: dict[str, Any] | None,
) -> bool:
    while True:
        try:
            action = input("CriticProfile action [approve/edit/reject]: ").strip().casefold()
        except EOFError:
            print("ERROR: explicit CriticProfile approval is required. Use --approve-profile for non-interactive runs.")
            return False
        if action in {"approve", "a"}:
            app.approve_profile(task_id, approved_by="CLI_USER", edits=initial_edits)
            return True
        if action in {"edit", "e"}:
            edits = initial_edits
            if edits is None:
                try:
                    raw = input("CriticProfile edits as JSON object: ").strip()
                except EOFError:
                    print("ERROR: profile edits were not provided.")
                    continue
                edits = _parse_edits(raw)
            if edits is None:
                continue
            app.approve_profile(task_id, approved_by="CLI_USER", edits=edits)
            return True
        if action in {"reject", "r"}:
            app.reject_profile(task_id, reason="Rejected from CLI", actor_id="CLI_USER")
            print("CriticProfile rejected. Autonomous execution was not started.")
            return False
        print("Choose approve, edit, or reject.")


if __name__ == "__main__":
    raise SystemExit(main())
