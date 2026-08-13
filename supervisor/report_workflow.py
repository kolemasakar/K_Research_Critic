from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agents import Agent
from models import AgentResult, AgentRunRequest, AgentType, Artifact, ExecutionStatus, TaskStatus

from .exceptions import ProfileStateError
from .research_critic_loop import ResearchCriticLoopOutcome
from .workflow_engine import WorkflowEngine


@dataclass(frozen=True)
class ReportWorkflowOutcome:
    """Structured result of Phase 8 artifact generation and finalization."""

    task_id: str
    final_state: TaskStatus
    report_agent_result: AgentResult
    artifacts: tuple[Artifact, ...]


class ReportWorkflow:
    """Supervisor-owned finalization boundary around ReportGenerator."""

    def __init__(self, workflow_engine: WorkflowEngine, report_generator: Agent) -> None:
        if report_generator.definition.agent_type != AgentType.REPORT_GENERATOR:
            raise ValueError("report_generator must expose AgentType.REPORT_GENERATOR")
        self.workflow_engine = workflow_engine
        self.report_generator = report_generator

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

        artifacts = tuple(Artifact.model_validate(item) for item in result.payload.get("artifacts", []))
        if len(artifacts) != 2:
            if task.status == TaskStatus.FINALIZING:
                self.workflow_engine.fail_task(task_id, reason="ReportGenerator did not return both required artifacts")
            return ReportWorkflowOutcome(
                task_id=task_id,
                final_state=self.workflow_engine.task_manager.get_task(task_id).status,
                report_agent_result=result,
                artifacts=artifacts,
            )

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
