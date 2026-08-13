from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from agents import Agent
from models import (
    AgentResult,
    AgentRunRequest,
    AgentType,
    Artifact,
    ArtifactStatus,
    ArtifactType,
    ExecutionStatus,
    TaskStatus,
)
from persistence import PersistenceStore

from .exceptions import ProfileStateError
from .research_critic_loop import ResearchCriticLoopOutcome
from .workflow_engine import WorkflowEngine


@dataclass(frozen=True)
class ReportWorkflowOutcome:
    """Structured result of final artifact generation and finalization."""

    task_id: str
    final_state: TaskStatus
    report_agent_result: AgentResult
    artifacts: tuple[Artifact, ...]


class ReportWorkflow:
    """Supervisor-owned finalization boundary around ReportGenerator."""

    def __init__(
        self,
        workflow_engine: WorkflowEngine,
        report_generator: Agent,
        *,
        persistence: PersistenceStore | None = None,
    ) -> None:
        if report_generator.definition.agent_type != AgentType.REPORT_GENERATOR:
            raise ValueError("report_generator must expose AgentType.REPORT_GENERATOR")
        self.workflow_engine = workflow_engine
        self.report_generator = report_generator
        self.persistence = persistence or workflow_engine.persistence

    def finalize(
        self,
        task_id: str,
        loop_outcome: ResearchCriticLoopOutcome,
        *,
        extra_context: dict[str, Any] | None = None,
    ) -> ReportWorkflowOutcome:
        task = self.workflow_engine.task_manager.get_task(task_id)
        workflow = self.workflow_engine.get_task_workflow(task_id)
        if loop_outcome.task_id != task_id or loop_outcome.workflow_run_id != workflow.workflow_run_id:
            raise ValueError("ResearchCriticLoopOutcome does not belong to the active task workflow")
        if loop_outcome.last_research_result is None:
            raise ProfileStateError("Report generation requires at least one completed research iteration")
        if task.status not in {TaskStatus.APPROVED, TaskStatus.COMPLETED_WITH_LIMITATIONS}:
            raise ProfileStateError(
                "Report generation requires APPROVED or COMPLETED_WITH_LIMITATIONS task state"
            )

        target_status = (
            TaskStatus.FINALIZED
            if task.status == TaskStatus.APPROVED
            else TaskStatus.COMPLETED_WITH_LIMITATIONS
        )
        if task.status == TaskStatus.APPROVED:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.FINALIZING,
                trigger="report_generation_started",
                reason="ReportGenerator started final artifact generation",
            )

        research_history = [item.research_result for item in loop_outcome.iterations]
        review_history = [item.critic_review for item in loop_outcome.iterations]
        request = AgentRunRequest(
            task_id=task_id,
            workflow_run_id=workflow.workflow_run_id,
            agent_id=self.report_generator.definition.agent_id,
            agent_type=AgentType.REPORT_GENERATOR,
            iteration=max(1, workflow.iteration),
            input={
                "final_research_result": loop_outcome.last_research_result.model_dump(mode="json"),
                "research_history": [item.model_dump(mode="json") for item in research_history],
                "review_history": [item.model_dump(mode="json") for item in review_history],
                "final_status": target_status.value,
            },
            context={
                "workflow_state": task.status.value,
                "prior_run_ids": list(workflow.agent_run_ids),
                **dict(extra_context or {}),
            },
        )
        result = self.report_generator.run(request)
        self.workflow_engine.record_agent_run(task_id, result.run_id)
        if self.persistence is not None:
            self.persistence.save_agent_result(result)

        if result.status == ExecutionStatus.FAILED:
            if task.status == TaskStatus.FINALIZING:
                reason = result.errors[0].message if result.errors else "ReportGenerator failed"
                self.workflow_engine.fail_task(task_id, reason=reason)
            return ReportWorkflowOutcome(
                task_id=task_id,
                final_state=self.workflow_engine.task_manager.get_task(task_id).status,
                report_agent_result=result,
                artifacts=(),
            )

        try:
            artifacts = tuple(Artifact.model_validate(item) for item in result.payload.get("artifacts", []))
        except (TypeError, ValueError, ValidationError) as exc:
            return self._invalid_artifact_outcome(
                task_id,
                task.status,
                result,
                (),
                f"ReportGenerator returned invalid artifact metadata: {exc}",
            )

        validation_error = self._validate_artifact_set(
            artifacts,
            task_id=task_id,
            workflow_run_id=workflow.workflow_run_id,
            report_run_id=result.run_id,
            target_status=target_status,
        )
        if validation_error is not None:
            return self._invalid_artifact_outcome(
                task_id,
                task.status,
                result,
                artifacts,
                validation_error,
            )

        if self.persistence is not None:
            for artifact in artifacts:
                self.persistence.save_artifact(artifact)

        if task.status == TaskStatus.FINALIZING:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.FINALIZED,
                trigger="final_artifacts_generated",
                reason="FINAL_REPORT and REVIEW_PROTOCOL generated successfully",
            )

        return ReportWorkflowOutcome(
            task_id=task_id,
            final_state=self.workflow_engine.task_manager.get_task(task_id).status,
            report_agent_result=result,
            artifacts=artifacts,
        )

    @staticmethod
    def _validate_artifact_set(
        artifacts: tuple[Artifact, ...],
        *,
        task_id: str,
        workflow_run_id: str,
        report_run_id: str,
        target_status: TaskStatus,
    ) -> str | None:
        required_types = {ArtifactType.FINAL_REPORT, ArtifactType.REVIEW_PROTOCOL}
        if len(artifacts) != 2 or {artifact.artifact_type for artifact in artifacts} != required_types:
            return "ReportGenerator must return exactly one FINAL_REPORT and one REVIEW_PROTOCOL"
        if any(artifact.task_id != task_id for artifact in artifacts):
            return "ReportGenerator artifact task_id does not match the finalized task"
        if any(artifact.workflow_run_id != workflow_run_id for artifact in artifacts):
            return "ReportGenerator artifact workflow_run_id does not match the active workflow"
        if any(artifact.created_by_run_id != report_run_id for artifact in artifacts):
            return "ReportGenerator artifact created_by_run_id does not match the report run"
        expected_status = (
            ArtifactStatus.APPROVED
            if target_status == TaskStatus.FINALIZED
            else ArtifactStatus.GENERATED
        )
        if any(artifact.status != expected_status for artifact in artifacts):
            return "ReportGenerator artifact status does not match the final task status"
        if len({artifact.path for artifact in artifacts}) != 2:
            return "ReportGenerator artifacts must use distinct paths"
        return None

    def _invalid_artifact_outcome(
        self,
        task_id: str,
        task_status: TaskStatus,
        result: AgentResult,
        artifacts: tuple[Artifact, ...],
        reason: str,
    ) -> ReportWorkflowOutcome:
        if task_status == TaskStatus.FINALIZING:
            self.workflow_engine.fail_task(task_id, reason=reason)
        return ReportWorkflowOutcome(
            task_id=task_id,
            final_state=self.workflow_engine.task_manager.get_task(task_id).status,
            report_agent_result=result,
            artifacts=artifacts,
        )
