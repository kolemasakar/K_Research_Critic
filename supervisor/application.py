from __future__ import annotations

from contextlib import nullcontext
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from agents import CriticAgent, ReportGenerator, ResearchAgent
from config import (
    LoadedConfiguration,
    TaskConfigurationSnapshot,
    create_task_configuration_snapshot,
    latest_task_configuration_snapshot,
)
from models import CriticProfile, DomainAssessment, ExecutionStatus, Task, TaskStatus, UserApproval
from persistence import PersistenceStore, TaskAuditSnapshot
from tools import (
    ResearchTools,
    RuntimeControlledResearchTools,
    RuntimeToolPolicy,
)

from .hybrid_resolver import DomainResolverProtocol
from .profile_workflow import ProfileWorkflow
from .provider_factory import build_domain_resolver
from .recovery import RecoveryOutcome, RuntimeRecoveryService
from .report_workflow import ReportWorkflow, ReportWorkflowOutcome
from .research_critic_loop import ResearchCriticLoop, ResearchCriticLoopOutcome
from .runtime_limits import OutputBoundedReportGenerator
from .workflow_engine import WorkflowEngine


class MVPStatus(StrEnum):
    SUCCESS = "SUCCESS"
    LIMITATION = "LIMITATION"
    FAILURE = "FAILURE"


@dataclass(frozen=True)
class PreparedTask:
    """User-review boundary produced before autonomous execution starts."""

    task: Task
    domain_assessment: DomainAssessment
    critic_profile: CriticProfile


@dataclass(frozen=True)
class MVPOutcome:
    """Structured end-to-end result exposed by the application layer."""

    task_id: str
    status: MVPStatus
    final_state: TaskStatus
    loop_outcome: ResearchCriticLoopOutcome
    report_outcome: ReportWorkflowOutcome | None

    @property
    def artifact_paths(self) -> tuple[str, ...]:
        if self.report_outcome is None:
            return ()
        return tuple(artifact.path for artifact in self.report_outcome.artifacts)


class KSupervisorApplication:
    """Compose the approved components into one end-to-end workflow."""

    def __init__(
        self,
        tools: ResearchTools,
        *,
        output_directory: str | Path = "output",
        default_max_iterations: int = 3,
        workflow_engine: WorkflowEngine | None = None,
        domain_resolver: DomainResolverProtocol | None = None,
        persistence: PersistenceStore | None = None,
        configuration: LoadedConfiguration | None = None,
    ) -> None:
        if default_max_iterations <= 0:
            raise ValueError("default_max_iterations must be greater than zero")

        if workflow_engine is None:
            workflow_engine = WorkflowEngine(persistence=persistence)
        elif (
            persistence is not None
            and workflow_engine.persistence is not None
            and workflow_engine.persistence is not persistence
        ):
            raise ValueError("Application and WorkflowEngine must use the same persistence store")
        elif persistence is not None and workflow_engine.persistence is None:
            workflow_engine.persistence = persistence
            workflow_engine.task_manager.persistence = persistence

        self.workflow_engine = workflow_engine
        self.persistence = persistence or workflow_engine.persistence
        self.configuration = configuration
        self._output_directory = Path(output_directory)

        if configuration is not None:
            self._validate_required_agents(configuration)
            if domain_resolver is None:
                domain_resolver = build_domain_resolver(configuration)
            self.runtime_tools: RuntimeControlledResearchTools | None = (
                RuntimeControlledResearchTools(tools)
            )
            agent_tools: ResearchTools = self.runtime_tools
        else:
            self.runtime_tools = None
            agent_tools = tools

        self.profile_workflow = ProfileWorkflow(
            self.workflow_engine,
            domain_resolver=domain_resolver,
        )
        self.research_agent = ResearchAgent(agent_tools)
        self.critic_agent = CriticAgent(agent_tools)
        base_report_generator = ReportGenerator(self._output_directory)
        self.report_generator = (
            OutputBoundedReportGenerator(base_report_generator)
            if configuration is not None
            else base_report_generator
        )
        self.research_critic_loop = ResearchCriticLoop(
            self.workflow_engine,
            self.profile_workflow.profile_manager,
            self.research_agent,
            self.critic_agent,
            persistence=self.persistence,
        )
        self.report_workflow = ReportWorkflow(
            self.workflow_engine,
            self.report_generator,
            persistence=self.persistence,
        )
        self.default_max_iterations = default_max_iterations
        self._register_agents()

    def prepare_task(
        self,
        user_request: str,
        *,
        task_type: str = "auto",
        max_iterations: int | None = None,
        special_user_requirements: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PreparedTask:
        iterations = self.default_max_iterations if max_iterations is None else max_iterations
        if iterations <= 0:
            raise ValueError("max_iterations must be greater than zero")

        task_metadata = dict(metadata or {})
        if self.configuration is not None:
            task_metadata.update(
                {
                    "configuration_schema_version": self.configuration.settings.schema_version,
                    "configuration_environment": self.configuration.settings.environment,
                    "configuration_source_fingerprint": self.configuration.fingerprint,
                }
            )
        task = self.workflow_engine.task_manager.create_task(
            user_request=user_request,
            task_type=task_type,
            metadata=task_metadata,
        )
        self.workflow_engine.start_workflow(task.task_id, max_iterations=iterations)
        assessment, profile = self.profile_workflow.generate_profile(
            task.task_id,
            special_user_requirements=special_user_requirements,
        )
        return PreparedTask(task=task, domain_assessment=assessment, critic_profile=profile)

    def approve_profile(
        self,
        task_id: str,
        *,
        approved_by: str = "USER",
        edits: dict[str, Any] | None = None,
    ) -> tuple[CriticProfile, UserApproval]:
        approved, approval = self.profile_workflow.approve_current_profile(
            task_id,
            approved_by=approved_by,
            edits=edits,
        )
        if self.configuration is not None:
            self._freeze_task_configuration(task_id, approved)
        return approved, approval

    def reject_profile(
        self,
        task_id: str,
        *,
        reason: str | None = None,
        actor_id: str = "USER",
    ) -> tuple[CriticProfile, UserApproval]:
        return self.profile_workflow.reject_current_profile(
            task_id,
            reason=reason,
            actor_id=actor_id,
        )

    def propose_profile_amendment(
        self,
        task_id: str,
        *,
        changes: dict[str, Any],
        reason: str,
    ) -> CriticProfile:
        return self.profile_workflow.propose_amendment(
            task_id,
            changes=changes,
            reason=reason,
        )

    def recover_task(self, task_id: str) -> RecoveryOutcome:
        if self.persistence is None:
            raise RuntimeError("Task recovery requires a configured persistence store")
        service = RuntimeRecoveryService(self.persistence)
        return service.restore(
            task_id,
            workflow_engine=self.workflow_engine,
            profile_manager=self.profile_workflow.profile_manager,
            research_critic_loop=self.research_critic_loop,
        )

    def audit_task(self, task_id: str) -> TaskAuditSnapshot:
        if self.persistence is None:
            raise RuntimeError("Task audit requires a configured persistence store")
        return self.persistence.load_task_audit(task_id)

    def configuration_snapshot(self, task_id: str) -> TaskConfigurationSnapshot | None:
        task = self.workflow_engine.task_manager.get_task(task_id)
        return latest_task_configuration_snapshot(task.metadata)

    def run_to_completion(
        self,
        task_id: str,
        *,
        research_input: dict[str, Any] | None = None,
        critic_input: dict[str, Any] | None = None,
        research_constraints: dict[str, Any] | None = None,
        critic_constraints: dict[str, Any] | None = None,
        report_context: dict[str, Any] | None = None,
    ) -> MVPOutcome:
        snapshot = self.configuration_snapshot(task_id)
        if self.configuration is not None and snapshot is None:
            raise RuntimeError(
                "Autonomous execution requires a frozen TaskConfigurationSnapshot after profile approval"
            )

        effective_research_constraints = dict(research_constraints or {})
        effective_critic_constraints = dict(critic_constraints or {})
        runtime_context = nullcontext()
        if snapshot is not None:
            settings = snapshot.effective_settings
            effective_research_constraints = self._apply_frozen_constraints(
                effective_research_constraints,
                {
                    "max_queries": settings.research.max_queries,
                    "max_sources": settings.research.max_sources,
                    "max_sources_per_query": settings.research.max_sources_per_query,
                },
            )
            effective_critic_constraints = self._apply_frozen_constraints(
                effective_critic_constraints,
                {
                    "max_verification_queries": settings.critic.max_verification_queries,
                    "max_verification_sources_per_claim": (
                        settings.critic.max_verification_sources_per_claim
                    ),
                    "require_independent_search": settings.critic.require_independent_search,
                },
            )
            if self.runtime_tools is not None:
                runtime_context = self.runtime_tools.scope(self._runtime_policy(snapshot))

        with runtime_context:
            loop_outcome = self.research_critic_loop.run(
                task_id,
                research_input=research_input,
                critic_input=critic_input,
                research_constraints=effective_research_constraints,
                critic_constraints=effective_critic_constraints,
            )

        report_outcome: ReportWorkflowOutcome | None = None
        if loop_outcome.final_state in {TaskStatus.APPROVED, TaskStatus.COMPLETED_WITH_LIMITATIONS}:
            effective_report_context = dict(report_context or {})
            if snapshot is not None:
                effective_report_context.update(
                    {
                        "configuration_snapshot_id": snapshot.snapshot_id,
                        "configuration_fingerprint": snapshot.settings_fingerprint,
                        "max_output_size_bytes": snapshot.effective_settings.limits.max_output_size_bytes,
                    }
                )
            report_outcome = self.report_workflow.finalize(
                task_id,
                loop_outcome,
                extra_context=effective_report_context,
            )

        final_state = self.workflow_engine.task_manager.get_task(task_id).status
        status = self._mvp_status(final_state, report_outcome)
        return MVPOutcome(
            task_id=task_id,
            status=status,
            final_state=final_state,
            loop_outcome=loop_outcome,
            report_outcome=report_outcome,
        )

    def _freeze_task_configuration(
        self,
        task_id: str,
        profile: CriticProfile,
    ) -> TaskConfigurationSnapshot:
        assert self.configuration is not None
        task = self.workflow_engine.task_manager.get_task(task_id)
        previous = latest_task_configuration_snapshot(task.metadata)
        workflow = self.workflow_engine.get_task_workflow(task_id)
        persistence_path = getattr(self.persistence, "path", None)
        snapshot = create_task_configuration_snapshot(
            self.configuration,
            task_id=task_id,
            approved_profile_id=profile.profile_id,
            approved_profile_version=profile.version,
            max_iterations=workflow.max_iterations,
            output_directory=str(self._output_directory),
            persistence_path=(str(persistence_path) if persistence_path is not None else None),
            supersedes_snapshot_id=(previous.snapshot_id if previous is not None else None),
        )
        self.workflow_engine.task_manager.append_configuration_snapshot(task_id, snapshot)
        return snapshot

    @staticmethod
    def _apply_frozen_constraints(
        provided: dict[str, Any],
        frozen: dict[str, Any],
    ) -> dict[str, Any]:
        result = dict(provided)
        for key, value in frozen.items():
            if key in result and result[key] != value:
                raise ValueError(
                    f"Constraint {key!r} is frozen for the active task and cannot be changed"
                )
            result[key] = value
        return result

    @staticmethod
    def _runtime_policy(snapshot: TaskConfigurationSnapshot) -> RuntimeToolPolicy:
        settings = snapshot.effective_settings
        return RuntimeToolPolicy(
            max_search_calls=settings.limits.max_search_calls,
            max_fetch_calls=settings.limits.max_fetch_calls,
            max_runtime_seconds=float(settings.limits.max_runtime_seconds),
            search_timeout_seconds=float(settings.tools.web_search.timeout_seconds),
            fetch_timeout_seconds=float(settings.tools.web_fetch.timeout_seconds),
            retry_max_attempts=settings.retry.max_attempts,
            retry_initial_delay_seconds=settings.retry.initial_delay_seconds,
            retry_max_delay_seconds=settings.retry.max_delay_seconds,
            retry_backoff_multiplier=settings.retry.backoff_multiplier,
            search_enabled=settings.tools.web_search.enabled,
            fetch_enabled=settings.tools.web_fetch.enabled,
        )

    @staticmethod
    def _validate_required_agents(configuration: LoadedConfiguration) -> None:
        agents = configuration.settings.agents
        disabled = [
            name
            for name, enabled in (
                ("research_agent", agents.research_agent.enabled),
                ("critic_agent", agents.critic_agent.enabled),
                ("report_generator", agents.report_generator.enabled),
            )
            if not enabled
        ]
        if disabled:
            raise ValueError(
                "The RESEARCH_CRITIC workflow requires these enabled agents: "
                + ", ".join(disabled)
            )

    def _register_agents(self) -> None:
        existing = {
            (definition.name, definition.version)
            for definition in self.workflow_engine.agent_registry.list_agents()
        }
        for definition in (
            self.research_agent.definition,
            self.critic_agent.definition,
            self.report_generator.definition,
        ):
            identity = (definition.name, definition.version)
            if identity not in existing:
                self.workflow_engine.agent_registry.register(definition)
                existing.add(identity)

    @staticmethod
    def _mvp_status(
        final_state: TaskStatus,
        report_outcome: ReportWorkflowOutcome | None,
    ) -> MVPStatus:
        if (
            final_state == TaskStatus.FINALIZED
            and report_outcome is not None
            and report_outcome.report_agent_result.status == ExecutionStatus.SUCCEEDED
            and len(report_outcome.artifacts) == 2
        ):
            return MVPStatus.SUCCESS
        if (
            final_state == TaskStatus.COMPLETED_WITH_LIMITATIONS
            and report_outcome is not None
            and report_outcome.report_agent_result.status == ExecutionStatus.SUCCEEDED
            and len(report_outcome.artifacts) == 2
        ):
            return MVPStatus.LIMITATION
        return MVPStatus.FAILURE
