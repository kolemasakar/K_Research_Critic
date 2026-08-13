from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from agents import CriticAgent, ReportGenerator, ResearchAgent
from models import CriticProfile, DomainAssessment, ExecutionStatus, Task, TaskStatus, UserApproval
from persistence import PersistenceStore, TaskAuditSnapshot
from tools import ResearchTools

from .hybrid_resolver import DomainResolverProtocol
from .profile_workflow import ProfileWorkflow
from .recovery import RecoveryOutcome, RuntimeRecoveryService
from .report_workflow import ReportWorkflow, ReportWorkflowOutcome
from .research_critic_loop import ResearchCriticLoop, ResearchCriticLoopOutcome
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
        self.profile_workflow = ProfileWorkflow(
            self.workflow_engine,
            domain_resolver=domain_resolver,
        )
        self.research_agent = ResearchAgent(tools)
        self.critic_agent = CriticAgent(tools)
        self.report_generator = ReportGenerator(output_directory)
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
        task = self.workflow_engine.task_manager.create_task(
            user_request=user_request,
            task_type=task_type,
            metadata=metadata,
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
        return self.profile_workflow.approve_current_profile(
            task_id,
            approved_by=approved_by,
            edits=edits,
        )

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
        loop_outcome = self.research_critic_loop.run(
            task_id,
            research_input=research_input,
            critic_input=critic_input,
            research_constraints=research_constraints,
            critic_constraints=critic_constraints,
        )

        report_outcome: ReportWorkflowOutcome | None = None
        if loop_outcome.final_state in {TaskStatus.APPROVED, TaskStatus.COMPLETED_WITH_LIMITATIONS}:
            report_outcome = self.report_workflow.finalize(
                task_id,
                loop_outcome,
                extra_context=report_context,
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
