from __future__ import annotations

from models import (
    ActorType,
    StateTransition,
    TaskStatus,
    WorkflowRun,
    WorkflowStatus,
    WorkflowType,
    utc_now,
)

from .agent_registry import AgentRegistry
from .exceptions import WorkflowAlreadyActiveError, WorkflowNotFoundError
from .state_machine import StateMachine
from .task_manager import TaskManager


class WorkflowEngine:
    """Phase 2 orchestration skeleton with auditable in-memory run tracking."""

    def __init__(self, *, task_manager: TaskManager | None = None, state_machine: StateMachine | None = None, agent_registry: AgentRegistry | None = None) -> None:
        self.task_manager = task_manager or TaskManager()
        self.state_machine = state_machine or StateMachine()
        self.agent_registry = agent_registry or AgentRegistry()
        self._runs: dict[str, WorkflowRun] = {}
        self._transitions: dict[str, StateTransition] = {}

    def start_workflow(self, task_id: str, *, max_iterations: int = 3, workflow_type: WorkflowType = WorkflowType.RESEARCH_CRITIC) -> WorkflowRun:
        task = self.task_manager.get_task(task_id)
        if task.current_workflow_run_id is not None:
            existing = self._runs.get(task.current_workflow_run_id)
            if existing is not None and existing.status in {WorkflowStatus.RUNNING, WorkflowStatus.WAITING_FOR_USER}:
                raise WorkflowAlreadyActiveError(f"Task already has active workflow: {existing.workflow_run_id}")
        run = WorkflowRun(task_id=task.task_id, workflow_type=workflow_type, current_state=task.status, max_iterations=max_iterations)
        self._runs[run.workflow_run_id] = run
        self.task_manager.attach_workflow(task.task_id, run.workflow_run_id)
        return run

    def get_workflow(self, workflow_run_id: str) -> WorkflowRun:
        try:
            return self._runs[workflow_run_id]
        except KeyError as exc:
            raise WorkflowNotFoundError(f"Unknown workflow_run_id: {workflow_run_id}") from exc

    def get_task_workflow(self, task_id: str) -> WorkflowRun:
        task = self.task_manager.get_task(task_id)
        if task.current_workflow_run_id is None:
            raise WorkflowNotFoundError(f"Task has no workflow: {task_id}")
        return self.get_workflow(task.current_workflow_run_id)

    def get_transitions(self, workflow_run_id: str) -> list[StateTransition]:
        run = self.get_workflow(workflow_run_id)
        return [self._transitions[item] for item in run.transition_ids]

    def transition(self, task_id: str, to_state: TaskStatus, *, trigger: str, reason: str | None = None, actor_type: ActorType = ActorType.SUPERVISOR, actor_id: str | None = "SUPERVISOR") -> StateTransition:
        task = self.task_manager.get_task(task_id)
        run = self.get_task_workflow(task_id)
        from_state, applied_state = self.state_machine.transition(task, to_state)
        record = StateTransition(task_id=task.task_id, workflow_run_id=run.workflow_run_id, from_state=from_state, to_state=applied_state, trigger=trigger, reason=reason, actor_type=actor_type, actor_id=actor_id)
        self._transitions[record.transition_id] = record
        run.transition_ids = [*run.transition_ids, record.transition_id]
        run.current_state = applied_state
        self._sync_workflow_status(run, applied_state)
        return record

    def start_research_iteration(self, task_id: str, *, actor_type: ActorType = ActorType.SUPERVISOR, actor_id: str | None = "SUPERVISOR") -> StateTransition:
        task = self.task_manager.get_task(task_id)
        run = self.get_task_workflow(task_id)
        if task.status not in {TaskStatus.PROFILE_APPROVED, TaskStatus.REVISE_REQUIRED}:
            return self.transition(task_id, TaskStatus.RESEARCHING, trigger="research_iteration_requested", reason="Research iteration requested from current workflow state", actor_type=actor_type, actor_id=actor_id)
        if run.iteration >= run.max_iterations:
            return self.transition(task_id, TaskStatus.MAX_ITERATIONS_REACHED, trigger="iteration_limit_reached", reason=f"Maximum iterations reached: {run.max_iterations}", actor_type=actor_type, actor_id=actor_id)
        run.iteration += 1
        return self.transition(task_id, TaskStatus.RESEARCHING, trigger="research_iteration_started", reason=f"Starting research iteration {run.iteration}", actor_type=actor_type, actor_id=actor_id)

    def record_agent_run(self, task_id: str, run_id: str) -> WorkflowRun:
        run = self.get_task_workflow(task_id)
        if run_id not in run.agent_run_ids:
            run.agent_run_ids = [*run.agent_run_ids, run_id]
        return run

    def fail_task(self, task_id: str, *, reason: str, actor_type: ActorType = ActorType.SYSTEM, actor_id: str | None = "SYSTEM") -> StateTransition:
        return self.transition(task_id, TaskStatus.FAILED, trigger="workflow_failure", reason=reason, actor_type=actor_type, actor_id=actor_id)

    def complete_with_limitations(self, task_id: str, *, reason: str) -> StateTransition:
        return self.transition(task_id, TaskStatus.COMPLETED_WITH_LIMITATIONS, trigger="completed_with_limitations", reason=reason, actor_type=ActorType.SUPERVISOR, actor_id="SUPERVISOR")

    @staticmethod
    def _sync_workflow_status(run: WorkflowRun, state: TaskStatus) -> None:
        if state == TaskStatus.PROFILE_REVIEW_REQUIRED:
            run.status = WorkflowStatus.WAITING_FOR_USER
            return
        if state == TaskStatus.FINALIZED:
            run.completed_at = utc_now()
            run.final_decision = TaskStatus.FINALIZED.value
            run.status = WorkflowStatus.SUCCEEDED
            return
        if state == TaskStatus.FAILED:
            run.completed_at = utc_now()
            run.final_decision = TaskStatus.FAILED.value
            run.status = WorkflowStatus.FAILED
            return
        if state == TaskStatus.COMPLETED_WITH_LIMITATIONS:
            run.completed_at = utc_now()
            run.final_decision = TaskStatus.COMPLETED_WITH_LIMITATIONS.value
            run.status = WorkflowStatus.COMPLETED_WITH_LIMITATIONS
            return
        run.status = WorkflowStatus.RUNNING
