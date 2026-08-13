from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from config import ConfigurationError, load_configuration
from observability import OperationalLogContext, OperationalLogger, build_operational_logger
from persistence import SQLitePersistenceStore
from supervisor import KSupervisorApplication, MVPStatus
from tools import JsonCorpusProvider, ResearchToolset, WebFetchTool, WebSearchTool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the K_Supervisor end-to-end workflow.")
    parser.add_argument("--task", help="Research task. If omitted, it is requested interactively.")
    parser.add_argument("--task-type", default="auto")
    parser.add_argument(
        "--corpus",
        required=True,
        help="UTF-8 JSON evidence corpus used by the local MVP provider.",
    )
    parser.add_argument("--settings", default="config/settings.yaml")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--output-directory")
    parser.add_argument("--database")
    parser.add_argument("--max-iterations", type=int)
    parser.add_argument(
        "--approve-profile",
        action="store_true",
        help="Treat this command invocation as explicit profile approval.",
    )
    parser.add_argument(
        "--profile-edits",
        help="JSON object of CriticProfile edits applied before explicit approval.",
    )
    parser.add_argument("--special-requirement", action="append", default=[])
    parser.add_argument("--required-topic", action="append", default=[])
    parser.add_argument("--search-query", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        configuration = load_configuration(args.settings, env_path=args.env_file)
    except ConfigurationError as exc:
        print(f"ERROR: cannot load configuration: {exc}")
        return 1

    try:
        logger = build_operational_logger(configuration)
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot initialize operational logging: {exc}")
        return 1

    settings = configuration.settings
    logger.info(
        "runtime_initialized",
        message="Standalone/API reference runtime initialized.",
        details={
            "environment": settings.environment,
            "configuration_fingerprint": configuration.fingerprint,
            "distribution_channel": settings.distribution.primary_channel,
        },
    )

    max_iterations = (
        settings.workflow.max_iterations if args.max_iterations is None else args.max_iterations
    )
    output_directory = args.output_directory or settings.reports.output_directory
    database = args.database or settings.persistence.path

    if max_iterations <= 0:
        logger.error(
            "invalid_runtime_argument",
            message="max_iterations must be greater than zero.",
            details={"argument": "max_iterations", "value": max_iterations},
        )
        print("ERROR: --max-iterations must be greater than zero.")
        return 1

    task_text = (args.task or "").strip()
    if not task_text:
        try:
            task_text = input("Research task: ").strip()
        except EOFError:
            logger.error(
                "missing_task_input",
                message="Research task was not provided in non-interactive mode.",
            )
            print("ERROR: --task is required in non-interactive mode.")
            return 1
    if not task_text:
        logger.error("empty_task_input", message="Research task cannot be empty.")
        print("ERROR: research task cannot be empty.")
        return 1

    try:
        provider = JsonCorpusProvider.from_file(args.corpus)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        logger.error(
            "corpus_load_failed",
            message="Local evidence corpus could not be loaded.",
            details={"error": str(exc)},
        )
        print(f"ERROR: cannot load corpus: {exc}")
        return 1

    try:
        persistence = SQLitePersistenceStore(database)
    except (OSError, ValueError) as exc:
        logger.error(
            "persistence_initialization_failed",
            message="Standalone persistence could not be initialized.",
            details={"error": str(exc)},
        )
        print(f"ERROR: cannot initialize persistence: {exc}")
        return 1

    tools = ResearchToolset(WebSearchTool(provider), WebFetchTool(provider))
    try:
        app = KSupervisorApplication(
            tools,
            output_directory=Path(output_directory),
            default_max_iterations=max_iterations,
            persistence=persistence,
            configuration=configuration,
        )
        prepared = app.prepare_task(
            task_text,
            task_type=args.task_type,
            max_iterations=max_iterations,
            special_user_requirements=list(args.special_requirement),
        )
    except (RuntimeError, ValueError) as exc:
        logger.error(
            "workflow_prepare_failed",
            message="Configured workflow preparation failed.",
            details={"error": str(exc)},
        )
        print(f"ERROR: cannot prepare configured workflow: {exc}")
        return 1

    task_context = _workflow_context(app, prepared.task.task_id)
    logger.info(
        "task_prepared",
        message="Task reached the CriticProfile user-review boundary.",
        context=task_context,
        details={
            "task_type": prepared.task.task_type,
            "primary_domain": prepared.domain_assessment.primary_domain,
            "risk_level": prepared.domain_assessment.risk_level.value,
            "critic_profile_id": prepared.critic_profile.profile_id,
            "task_state": prepared.task.status.value,
        },
    )

    print(f"Environment: {settings.environment}")
    print(f"Configuration source fingerprint: {configuration.fingerprint}")
    print(f"Task ID: {prepared.task.task_id}")
    print("Domain assessment:")
    print(prepared.domain_assessment.model_dump_json(indent=2))
    print("CriticProfile proposal:")
    print(prepared.critic_profile.model_dump_json(indent=2))

    edits = _parse_edits(args.profile_edits)
    if edits is None and args.profile_edits is not None:
        logger.error(
            "profile_edits_invalid",
            message="CriticProfile edits could not be parsed.",
            context=task_context,
        )
        return 1

    try:
        if args.approve_profile:
            app.approve_profile(prepared.task.task_id, approved_by="CLI_USER", edits=edits)
        else:
            approval = _interactive_profile_gate(app, prepared.task.task_id, edits)
            if not approval:
                logger.warning(
                    "profile_gate_stopped",
                    message="Autonomous execution did not start because the profile was not approved.",
                    context=task_context,
                    details={
                        "task_state": app.workflow_engine.task_manager.get_task(
                            prepared.task.task_id
                        ).status.value
                    },
                )
                return 4
    except (RuntimeError, ValueError) as exc:
        logger.error(
            "profile_approval_failed",
            message="Profile approval or task configuration freeze failed.",
            context=task_context,
            details={"error": str(exc)},
        )
        print(f"ERROR: profile approval/configuration freeze failed: {exc}")
        return 1

    active_task = app.workflow_engine.task_manager.get_task(prepared.task.task_id)
    logger.info(
        "profile_approved",
        message="CriticProfile was explicitly approved and autonomous execution is permitted.",
        context=task_context,
        details={
            "critic_profile_id": active_task.active_profile_id,
            "task_state": active_task.status.value,
            "edits_applied": bool(edits),
        },
    )

    snapshot = app.configuration_snapshot(prepared.task.task_id)
    if snapshot is not None:
        logger.info(
            "configuration_snapshot_frozen",
            message="Effective task configuration was frozen before autonomous execution.",
            context=task_context,
            details={
                "snapshot_id": snapshot.snapshot_id,
                "settings_fingerprint": snapshot.settings_fingerprint,
                "approved_profile_id": snapshot.approved_profile_id,
                "approved_profile_version": snapshot.approved_profile_version,
            },
        )
        print(f"Configuration snapshot: {snapshot.snapshot_id}")
        print(f"Effective configuration fingerprint: {snapshot.settings_fingerprint}")

    research_input: dict[str, Any] = {}
    if args.search_query:
        research_input["search_queries"] = list(args.search_query)
    if args.required_topic:
        research_input["requirements"] = list(args.required_topic)
    critic_input = {"required_topics": list(args.required_topic)} if args.required_topic else None

    logger.info(
        "autonomous_execution_started",
        message="Research-Critic autonomous execution started.",
        context=task_context,
    )
    try:
        outcome = app.run_to_completion(
            prepared.task.task_id,
            research_input=research_input or None,
            critic_input=critic_input,
        )
    except (RuntimeError, ValueError) as exc:
        logger.error(
            "workflow_execution_failed",
            message="Configured workflow execution raised an explicit failure.",
            context=task_context,
            details={"error": str(exc)},
        )
        print(f"ERROR: configured workflow execution failed: {exc}")
        return 1

    _log_agent_results(logger, task_context, outcome)
    logger.info(
        "workflow_completed",
        message="End-to-end workflow reached a terminal outcome.",
        context=task_context,
        details={
            "mvp_status": outcome.status.value,
            "final_task_state": outcome.final_state.value,
            "completed_iterations": len(outcome.loop_outcome.iterations),
            "artifact_count": len(outcome.artifact_paths),
        },
    )

    print(f"MVP status: {outcome.status.value}")
    print(f"Final task state: {outcome.final_state.value}")
    print(f"Audit database: {database}")
    if settings.logging.file_enabled:
        print(f"Operational log: {logger.file_path}")
    for path in outcome.artifact_paths:
        print(f"Artifact: {path}")

    if outcome.status == MVPStatus.SUCCESS:
        return 0
    if outcome.status == MVPStatus.LIMITATION:
        return 2
    return 1


def _workflow_context(
    app: KSupervisorApplication,
    task_id: str,
    *,
    run_id: str | None = None,
    agent_id: str | None = None,
    request_id: str | None = None,
) -> OperationalLogContext:
    workflow = app.workflow_engine.get_task_workflow(task_id)
    return OperationalLogContext(
        task_id=task_id,
        workflow_run_id=workflow.workflow_run_id,
        run_id=run_id,
        agent_id=agent_id,
        request_id=request_id,
    )


def _log_agent_results(
    logger: OperationalLogger,
    task_context: OperationalLogContext,
    outcome,
) -> None:
    results = list(outcome.loop_outcome.agent_results)
    if outcome.report_outcome is not None:
        results.append(outcome.report_outcome.report_agent_result)
    for result in results:
        logger.info(
            "agent_run_completed",
            message="Agent execution result recorded.",
            context=OperationalLogContext(
                task_id=task_context.task_id,
                workflow_run_id=task_context.workflow_run_id,
                run_id=result.run_id,
                agent_id=result.agent_id,
                request_id=result.request_id,
            ),
            details={
                "agent_type": result.agent_type.value,
                "execution_status": result.status.value,
                "result_type": result.result_type,
                "warning_count": len(result.warnings),
                "error_count": len(result.errors),
                "search_calls": result.metrics.search_calls,
                "fetch_calls": result.metrics.fetch_calls,
            },
        )


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
            print(
                "ERROR: explicit CriticProfile approval is required. "
                "Use --approve-profile for non-interactive runs."
            )
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
