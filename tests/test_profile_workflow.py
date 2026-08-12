import pytest
from pydantic import ValidationError

from models import (
    ApprovalDecision,
    ApprovalType,
    ProfileStatus,
    RiskLevel,
    TaskStatus,
    WorkflowStatus,
)
from supervisor import (
    DomainResolver,
    InvalidStateTransitionError,
    ProfileManager,
    ProfileStateError,
    ProfileWorkflow,
    TaskManager,
    WorkflowEngine,
)


def make_profile_workflow(user_request: str, *, task_type: str = "auto"):
    manager = TaskManager()
    engine = WorkflowEngine(task_manager=manager)
    task = manager.create_task(user_request=user_request, task_type=task_type)
    run = engine.start_workflow(task.task_id)
    profiles = ProfileManager()
    workflow = ProfileWorkflow(engine, profile_manager=profiles)
    return manager, engine, profiles, workflow, task, run


def test_domain_resolver_detects_geodesy_and_task_type() -> None:
    manager = TaskManager()
    task = manager.create_task(
        user_request="Assess GNSS RTK accuracy for deformation monitoring",
        task_type="auto",
    )
    assessment = DomainResolver().resolve(task)
    assert assessment.primary_domain == "geodesy"
    assert assessment.task_type == "assessment"
    assert assessment.risk_level == RiskLevel.HIGH
    assert "STANDARD" in assessment.recommended_source_types


def test_domain_resolver_supports_multi_domain_tasks() -> None:
    manager = TaskManager()
    task = manager.create_task(
        user_request="Evaluate GNSS monitoring for structural deformation of a concrete building",
        task_type="technical_research",
    )
    assessment = DomainResolver().resolve(task)
    assert assessment.primary_domain == "construction"
    assert "geodesy" in assessment.secondary_domains
    assert assessment.risk_level == RiskLevel.HIGH


def test_domain_resolver_falls_back_to_general_research() -> None:
    manager = TaskManager()
    task = manager.create_task(user_request="Investigate an unusual historical topic", task_type="auto")
    assessment = DomainResolver().resolve(task)
    assert assessment.primary_domain == "general_research"
    assert assessment.risk_level == RiskLevel.MEDIUM
    assert assessment.uncertainties


def test_profile_generation_stops_at_explicit_user_gate() -> None:
    _, _, profiles, workflow, task, run = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    assessment, profile = workflow.generate_profile(task.task_id)
    assert assessment.task_id == task.task_id
    assert profile.status == ProfileStatus.REVIEW_REQUIRED
    assert task.status == TaskStatus.PROFILE_REVIEW_REQUIRED
    assert task.active_profile_id is None
    assert run.status == WorkflowStatus.WAITING_FOR_USER
    assert profiles.get_pending_profile(task.task_id).profile_id == profile.profile_id


def test_autonomous_research_cannot_start_before_profile_approval() -> None:
    _, engine, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    with pytest.raises(InvalidStateTransitionError):
        engine.start_research_iteration(task.task_id)
    assert task.status == TaskStatus.PROFILE_REVIEW_REQUIRED


def test_user_approval_activates_profile_and_is_auditable() -> None:
    _, _, profiles, workflow, task, run = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    _, pending = workflow.generate_profile(task.task_id)
    approved, approval = workflow.approve_current_profile(task.task_id)
    assert approved.profile_id == pending.profile_id
    assert approved.status == ProfileStatus.APPROVED
    assert approved.approved_by == "USER"
    assert task.active_profile_id == approved.profile_id
    assert task.status == TaskStatus.PROFILE_APPROVED
    assert run.status == WorkflowStatus.RUNNING
    assert approval.decision == ApprovalDecision.APPROVED
    assert approval.approval_type == ApprovalType.CRITIC_PROFILE
    assert profiles.get_approvals(task.task_id) == [approval]


def test_user_can_edit_and_approve_profile_in_one_explicit_action() -> None:
    _, _, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    approved, approval = workflow.approve_current_profile(
        task.task_id,
        edits={
            "confidence_threshold": 0.95,
            "special_user_requirements": ["Verify receiver specifications against primary documentation"],
        },
    )
    assert approved.confidence_threshold == 0.95
    assert approved.special_user_requirements
    assert approval.decision == ApprovalDecision.EDITED_AND_APPROVED
    assert approval.user_changes["confidence_threshold"] == 0.95


def test_initial_profile_rejection_returns_to_profile_generation() -> None:
    _, _, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    rejected, approval = workflow.reject_current_profile(
        task.task_id,
        reason="Add a construction review dimension",
    )
    assert rejected.status == ProfileStatus.REJECTED
    assert approval.decision == ApprovalDecision.REJECTED
    assert task.status == TaskStatus.PROFILE_GENERATING
    assert task.active_profile_id is None


def test_approved_profile_remains_immutable() -> None:
    _, _, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    approved, _ = workflow.approve_current_profile(task.task_id)
    with pytest.raises(ValidationError):
        approved.confidence_threshold = 0.50


def test_material_amendment_during_research_returns_to_user_gate() -> None:
    _, engine, profiles, workflow, task, run = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    approved, _ = workflow.approve_current_profile(task.task_id)
    engine.start_research_iteration(task.task_id)
    old_profile_id = task.active_profile_id

    amendment = workflow.propose_amendment(
        task.task_id,
        changes={
            "domain": ["geodesy", "construction"],
            "evaluation_criteria": [
                *approved.evaluation_criteria,
                "structural monitoring suitability",
            ],
        },
        reason="Research exposed a material structural-engineering review requirement",
    )

    assert amendment.status == ProfileStatus.REVIEW_REQUIRED
    assert amendment.version == approved.version + 1
    assert amendment.supersedes_profile_id == approved.profile_id
    assert task.active_profile_id == old_profile_id
    assert task.status == TaskStatus.PROFILE_REVIEW_REQUIRED
    assert run.status == WorkflowStatus.WAITING_FOR_USER
    assert profiles.get_pending_profile(task.task_id).profile_id == amendment.profile_id


def test_approved_amendment_replaces_active_profile_only_after_user_approval() -> None:
    _, engine, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    first, _ = workflow.approve_current_profile(task.task_id)
    engine.start_research_iteration(task.task_id)
    amendment = workflow.propose_amendment(
        task.task_id,
        changes={"domain": ["geodesy", "construction"]},
        reason="Structural review is now required",
    )
    assert task.active_profile_id == first.profile_id

    approved_amendment, approval = workflow.approve_current_profile(task.task_id)
    assert approved_amendment.profile_id == amendment.profile_id
    assert approved_amendment.supersedes_profile_id == first.profile_id
    assert task.active_profile_id == approved_amendment.profile_id
    assert task.status == TaskStatus.PROFILE_APPROVED
    assert approval.approval_type == ApprovalType.CRITIC_PROFILE_AMENDMENT


def test_rejected_amendment_keeps_previous_approved_profile_active() -> None:
    _, engine, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    first, _ = workflow.approve_current_profile(task.task_id)
    engine.start_research_iteration(task.task_id)
    workflow.propose_amendment(
        task.task_id,
        changes={"domain": ["geodesy", "construction"]},
        reason="Potential structural review requirement",
    )
    rejected, _ = workflow.reject_current_profile(task.task_id, reason="Keep original review scope")
    assert rejected.status == ProfileStatus.REJECTED
    assert task.active_profile_id == first.profile_id
    assert task.status == TaskStatus.PROFILE_APPROVED


def test_noop_amendment_is_rejected_before_state_change() -> None:
    _, engine, _, workflow, task, _ = make_profile_workflow(
        "Assess GNSS RTK accuracy for deformation monitoring"
    )
    workflow.generate_profile(task.task_id)
    approved, _ = workflow.approve_current_profile(task.task_id)
    engine.start_research_iteration(task.task_id)
    with pytest.raises(ProfileStateError):
        workflow.propose_amendment(
            task.task_id,
            changes={"confidence_threshold": approved.confidence_threshold},
            reason="No effective change",
        )
    assert task.status == TaskStatus.RESEARCHING
