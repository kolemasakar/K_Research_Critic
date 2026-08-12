from __future__ import annotations

from models import Task, TaskStatus, utc_now

from .exceptions import InvalidStateTransitionError


class StateMachine:
    """Strict task-state transition controller."""

    TERMINAL_STATES = frozenset({TaskStatus.FINALIZED, TaskStatus.FAILED, TaskStatus.COMPLETED_WITH_LIMITATIONS})

    ALLOWED_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
        TaskStatus.NEW: frozenset({TaskStatus.PROFILE_GENERATING, TaskStatus.FAILED}),
        TaskStatus.PROFILE_GENERATING: frozenset({TaskStatus.PROFILE_REVIEW_REQUIRED, TaskStatus.FAILED}),
        TaskStatus.PROFILE_REVIEW_REQUIRED: frozenset({TaskStatus.PROFILE_GENERATING, TaskStatus.PROFILE_APPROVED, TaskStatus.FAILED}),
        TaskStatus.PROFILE_APPROVED: frozenset({TaskStatus.RESEARCHING, TaskStatus.FAILED}),
        TaskStatus.RESEARCHING: frozenset({TaskStatus.DRAFT_READY, TaskStatus.FAILED}),
        TaskStatus.DRAFT_READY: frozenset({TaskStatus.REVIEWING, TaskStatus.FAILED}),
        TaskStatus.REVIEWING: frozenset({TaskStatus.REVISE_REQUIRED, TaskStatus.APPROVED, TaskStatus.FAILED}),
        TaskStatus.REVISE_REQUIRED: frozenset({TaskStatus.RESEARCHING, TaskStatus.MAX_ITERATIONS_REACHED, TaskStatus.FAILED}),
        TaskStatus.APPROVED: frozenset({TaskStatus.FINALIZING, TaskStatus.FAILED}),
        TaskStatus.FINALIZING: frozenset({TaskStatus.FINALIZED, TaskStatus.COMPLETED_WITH_LIMITATIONS, TaskStatus.FAILED}),
        TaskStatus.MAX_ITERATIONS_REACHED: frozenset({TaskStatus.COMPLETED_WITH_LIMITATIONS, TaskStatus.FAILED}),
        TaskStatus.FINALIZED: frozenset(),
        TaskStatus.FAILED: frozenset(),
        TaskStatus.COMPLETED_WITH_LIMITATIONS: frozenset(),
    }

    def can_transition(self, from_state: TaskStatus, to_state: TaskStatus) -> bool:
        return to_state in self.ALLOWED_TRANSITIONS.get(from_state, frozenset())

    def transition(self, task: Task, to_state: TaskStatus) -> tuple[TaskStatus, TaskStatus]:
        from_state = task.status
        if from_state in self.TERMINAL_STATES:
            raise InvalidStateTransitionError(f"Terminal state {from_state} cannot transition to {to_state}")
        if not self.can_transition(from_state, to_state):
            raise InvalidStateTransitionError(f"Invalid transition: {from_state} -> {to_state}")
        if to_state == TaskStatus.PROFILE_APPROVED and task.active_profile_id is None:
            raise InvalidStateTransitionError("PROFILE_APPROVED requires task.active_profile_id")
        task.status = to_state
        task.updated_at = utc_now()
        return from_state, to_state
