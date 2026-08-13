from __future__ import annotations

from dataclasses import dataclass

from models import Task, TaskStatus, WorkflowRun
from persistence import PersistenceStore, TaskAuditSnapshot

from .profile_manager import ProfileManager
from .research_critic_loop import ResearchCriticLoop
from .workflow_engine import WorkflowEngine


@dataclass(frozen=True)
class RecoveryOutcome:
    """Result of restoring persisted orchestration state into a fresh runtime."""

    task: Task
    workflow_run: WorkflowRun | None
    audit: TaskAuditSnapshot
    resumable: bool
    resume_reason: str


class RuntimeRecoveryService:
    """Restore persisted Supervisor state without exposing SQLite to agents."""

    RESUMABLE_STATES = frozenset(
        {
            TaskStatus.PROFILE_REVIEW_REQUIRED,
            TaskStatus.PROFILE_APPROVED,
            TaskStatus.REVISE_REQUIRED,
        }
    )

    def __init__(self, persistence: PersistenceStore) -> None:
        self.persistence = persistence

    def restore(
        self,
        task_id: str,
        *,
        workflow_engine: WorkflowEngine,
        profile_manager: ProfileManager,
        research_critic_loop: ResearchCriticLoop | None = None,
    ) -> RecoveryOutcome:
        audit = self.persistence.load_task_audit(task_id)
        workflow_engine.task_manager.restore_task(audit.task)

        if audit.workflow_run is not None:
            workflow_engine.restore_workflow(
                audit.workflow_run,
                transitions=list(audit.transitions),
            )

        profile_manager.restore_records(
            assessments=list(audit.domain_assessments),
            profiles=list(audit.critic_profiles),
            approvals=list(audit.user_approvals),
        )

        if research_critic_loop is not None:
            research_critic_loop.restore_history(
                task_id,
                agent_results=list(audit.agent_results),
                research_results=list(audit.research_results),
                reviews=list(audit.reviews),
            )

        state = audit.task.status
        if state in self.RESUMABLE_STATES:
            resumable = True
            reason = f"Task can resume from {state.value}"
        elif state in {
            TaskStatus.FINALIZED,
            TaskStatus.FAILED,
            TaskStatus.COMPLETED_WITH_LIMITATIONS,
        }:
            resumable = False
            reason = f"Task is terminal at {state.value}; audit remains fully available"
        else:
            resumable = False
            reason = (
                f"Task was interrupted at {state.value}; automatic mid-step replay is not "
                "performed because the last agent-side effect may be ambiguous"
            )

        return RecoveryOutcome(
            task=audit.task,
            workflow_run=audit.workflow_run,
            audit=audit,
            resumable=resumable,
            resume_reason=reason,
        )
