from __future__ import annotations

from typing import Any

from models import ActorType, ApprovalDecision, CriticProfile, DomainAssessment, TaskStatus, UserApproval

from .domain_resolver import DomainResolver
from .exceptions import ProfileStateError
from .profile_manager import ProfileManager
from .workflow_engine import WorkflowEngine


class ProfileWorkflow:
    """Coordinates domain resolution, CriticProfile review, and user approval gates."""

    AMENDMENT_STATES = frozenset(
        {
            TaskStatus.PROFILE_APPROVED,
            TaskStatus.RESEARCHING,
            TaskStatus.DRAFT_READY,
            TaskStatus.REVIEWING,
            TaskStatus.REVISE_REQUIRED,
            TaskStatus.APPROVED,
        }
    )

    def __init__(
        self,
        workflow_engine: WorkflowEngine,
        *,
        domain_resolver: DomainResolver | None = None,
        profile_manager: ProfileManager | None = None,
    ) -> None:
        self.workflow_engine = workflow_engine
        self.domain_resolver = domain_resolver or DomainResolver()
        self.profile_manager = profile_manager or ProfileManager()

    def generate_profile(
        self,
        task_id: str,
        *,
        special_user_requirements: list[str] | None = None,
    ) -> tuple[DomainAssessment, CriticProfile]:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.status == TaskStatus.NEW:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.PROFILE_GENERATING,
                trigger="profile_generation_started",
                reason="Domain analysis and critic profile generation started",
            )
        elif task.status != TaskStatus.PROFILE_GENERATING:
            raise ProfileStateError(
                f"Profile generation is not allowed from task state {task.status}"
            )

        assessment = self.domain_resolver.resolve(task)
        self.profile_manager.record_assessment(assessment)
        self.workflow_engine.task_manager.apply_domain_assessment(task_id, assessment)

        draft = self.profile_manager.create_draft(
            assessment,
            special_user_requirements=special_user_requirements,
        )
        review_profile = self.profile_manager.submit_for_review(draft.profile_id)
        self.workflow_engine.transition(
            task_id,
            TaskStatus.PROFILE_REVIEW_REQUIRED,
            trigger="critic_profile_ready_for_user_review",
            reason=f"CriticProfile {review_profile.profile_id} requires explicit user approval",
        )
        return assessment, review_profile

    def approve_current_profile(
        self,
        task_id: str,
        *,
        approved_by: str = "USER",
        edits: dict[str, Any] | None = None,
    ) -> tuple[CriticProfile, UserApproval]:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.status != TaskStatus.PROFILE_REVIEW_REQUIRED:
            raise ProfileStateError("Task must be PROFILE_REVIEW_REQUIRED before profile approval")

        pending = self.profile_manager.get_pending_profile(task_id)
        decision = ApprovalDecision.APPROVED
        user_changes: dict[str, Any] = {}
        if edits:
            pending = self.profile_manager.edit_pending(pending.profile_id, edits)
            decision = ApprovalDecision.EDITED_AND_APPROVED
            user_changes = dict(edits)

        approved, approval = self.profile_manager.approve(
            pending.profile_id,
            approved_by=approved_by,
            decision=decision,
            user_changes=user_changes,
        )
        self.workflow_engine.task_manager.set_active_profile(task_id, approved.profile_id)
        self.workflow_engine.transition(
            task_id,
            TaskStatus.PROFILE_APPROVED,
            trigger="user_approved_critic_profile",
            reason=f"User approved CriticProfile {approved.profile_id} version {approved.version}",
            actor_type=ActorType.USER,
            actor_id=approved_by,
        )
        return approved, approval

    def reject_current_profile(
        self,
        task_id: str,
        *,
        reason: str | None = None,
        actor_id: str = "USER",
    ) -> tuple[CriticProfile, UserApproval]:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.status != TaskStatus.PROFILE_REVIEW_REQUIRED:
            raise ProfileStateError("Task must be PROFILE_REVIEW_REQUIRED before profile rejection")

        pending = self.profile_manager.get_pending_profile(task_id)
        rejected, approval = self.profile_manager.reject(pending.profile_id, reason=reason)

        if rejected.supersedes_profile_id is not None and task.active_profile_id is not None:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.PROFILE_APPROVED,
                trigger="user_rejected_profile_amendment",
                reason="Amendment rejected; previous approved profile remains active",
                actor_type=ActorType.USER,
                actor_id=actor_id,
            )
        else:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.PROFILE_GENERATING,
                trigger="user_rejected_critic_profile",
                reason=reason or "User requested a new critic profile proposal",
                actor_type=ActorType.USER,
                actor_id=actor_id,
            )
        return rejected, approval

    def propose_amendment(
        self,
        task_id: str,
        *,
        changes: dict[str, Any],
        reason: str,
    ) -> CriticProfile:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.status not in self.AMENDMENT_STATES:
            raise ProfileStateError(
                f"CriticProfile amendment is not allowed from task state {task.status}"
            )
        if task.active_profile_id is None:
            raise ProfileStateError("A material amendment requires an active approved profile")

        active = self.profile_manager.get_profile(task.active_profile_id)
        if not self.profile_manager.is_material_change(active, changes):
            raise ProfileStateError("No material CriticProfile change detected")

        self.workflow_engine.transition(
            task_id,
            TaskStatus.PROFILE_GENERATING,
            trigger="material_profile_change_detected",
            reason=reason,
        )
        amendment = self.profile_manager.propose_amendment(active.profile_id, changes)
        review_profile = self.profile_manager.submit_for_review(amendment.profile_id)
        self.workflow_engine.transition(
            task_id,
            TaskStatus.PROFILE_REVIEW_REQUIRED,
            trigger="profile_amendment_ready_for_user_review",
            reason=f"CriticProfile amendment {review_profile.profile_id} requires user approval",
        )
        return review_profile
