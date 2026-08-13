from __future__ import annotations

from typing import Any

from models import (
    ApprovalDecision,
    ApprovalType,
    CriticProfile,
    DomainAssessment,
    ProfileStatus,
    RiskLevel,
    UserApproval,
    utc_now,
)
from persistence import PersistenceStore

from .exceptions import ProfileNotFoundError, ProfileStateError


class ProfileManager:
    """CriticProfile lifecycle manager with optional write-through persistence."""

    MATERIAL_FIELDS = frozenset(
        {
            "domain",
            "subdomains",
            "task_type",
            "risk_level",
            "critic_role",
            "evaluation_criteria",
            "preferred_source_types",
            "required_cross_checks",
            "standards",
            "minimum_evidence_level",
            "freshness_requirement",
            "confidence_threshold",
            "special_user_requirements",
        }
    )

    def __init__(self, persistence: PersistenceStore | None = None) -> None:
        self.persistence = persistence
        self._profiles: dict[str, CriticProfile] = {}
        self._pending_profile_by_task: dict[str, str] = {}
        self._approvals: list[UserApproval] = []
        self._assessments: dict[str, DomainAssessment] = {}
        self._latest_assessment_by_task: dict[str, str] = {}

    def record_assessment(self, assessment: DomainAssessment) -> None:
        self._assessments[assessment.assessment_id] = assessment
        self._latest_assessment_by_task[assessment.task_id] = assessment.assessment_id
        if self.persistence is not None:
            self.persistence.save_domain_assessment(assessment)

    def get_latest_assessment(self, task_id: str) -> DomainAssessment:
        assessment_id = self._latest_assessment_by_task.get(task_id)
        if assessment_id is None:
            raise ProfileNotFoundError(f"No DomainAssessment for task: {task_id}")
        return self._assessments[assessment_id]

    def create_draft(
        self,
        assessment: DomainAssessment,
        *,
        special_user_requirements: list[str] | None = None,
    ) -> CriticProfile:
        domains = [assessment.primary_domain, *assessment.secondary_domains]
        profile = CriticProfile(
            task_id=assessment.task_id,
            status=ProfileStatus.DRAFT,
            domain=domains,
            subdomains=[],
            task_type=assessment.task_type,
            risk_level=assessment.risk_level,
            critic_role=self._critic_role(domains),
            evaluation_criteria=list(assessment.recommended_evaluation_criteria),
            preferred_source_types=list(assessment.recommended_source_types),
            required_cross_checks=self._cross_checks(assessment.risk_level),
            standards=list(assessment.identified_standards),
            minimum_evidence_level=self._minimum_evidence_level(assessment.risk_level),
            freshness_requirement=self._freshness_requirement(assessment.risk_level),
            confidence_threshold=self._confidence_threshold(assessment.risk_level),
            special_user_requirements=list(special_user_requirements or []),
        )
        self._profiles[profile.profile_id] = profile
        self._pending_profile_by_task[profile.task_id] = profile.profile_id
        self._persist_profile(profile)
        return profile

    def get_profile(self, profile_id: str) -> CriticProfile:
        try:
            return self._profiles[profile_id]
        except KeyError as exc:
            raise ProfileNotFoundError(f"Unknown profile_id: {profile_id}") from exc

    def get_pending_profile(self, task_id: str) -> CriticProfile:
        profile_id = self._pending_profile_by_task.get(task_id)
        if profile_id is None:
            raise ProfileNotFoundError(f"No pending CriticProfile for task: {task_id}")
        return self.get_profile(profile_id)

    def submit_for_review(self, profile_id: str) -> CriticProfile:
        profile = self.get_profile(profile_id)
        if profile.status not in {ProfileStatus.DRAFT, ProfileStatus.REVIEW_REQUIRED}:
            raise ProfileStateError(f"Profile cannot enter review from status {profile.status}")
        reviewed = self._rebuild(profile, status=ProfileStatus.REVIEW_REQUIRED)
        self._profiles[profile_id] = reviewed
        self._pending_profile_by_task[reviewed.task_id] = reviewed.profile_id
        self._persist_profile(reviewed)
        return reviewed

    def edit_pending(self, profile_id: str, changes: dict[str, Any]) -> CriticProfile:
        profile = self.get_profile(profile_id)
        if profile.status not in {ProfileStatus.DRAFT, ProfileStatus.REVIEW_REQUIRED}:
            raise ProfileStateError("Only a draft or review-required profile can be edited")
        unknown = set(changes) - self.MATERIAL_FIELDS
        if unknown:
            raise ProfileStateError(f"Unsupported profile fields: {sorted(unknown)}")
        edited = self._rebuild(profile, **changes)
        self._profiles[profile_id] = edited
        self._persist_profile(edited)
        return edited

    def approve(
        self,
        profile_id: str,
        *,
        approved_by: str,
        decision: ApprovalDecision = ApprovalDecision.APPROVED,
        user_changes: dict[str, Any] | None = None,
    ) -> tuple[CriticProfile, UserApproval]:
        profile = self.get_profile(profile_id)
        if profile.status != ProfileStatus.REVIEW_REQUIRED:
            raise ProfileStateError("CriticProfile must be REVIEW_REQUIRED before approval")
        approved = self._rebuild(
            profile,
            status=ProfileStatus.APPROVED,
            approved_at=utc_now(),
            approved_by=approved_by,
        )
        approval_type = (
            ApprovalType.CRITIC_PROFILE_AMENDMENT
            if approved.supersedes_profile_id is not None
            else ApprovalType.CRITIC_PROFILE
        )
        approval = UserApproval(
            task_id=approved.task_id,
            approval_type=approval_type,
            target_id=approved.profile_id,
            decision=decision,
            user_changes=dict(user_changes or {}),
        )
        self._profiles[profile_id] = approved
        self._approvals.append(approval)
        self._pending_profile_by_task.pop(approved.task_id, None)
        self._persist_profile(approved)
        self._persist_approval(approval)
        return approved, approval

    def reject(
        self,
        profile_id: str,
        *,
        reason: str | None = None,
    ) -> tuple[CriticProfile, UserApproval]:
        profile = self.get_profile(profile_id)
        if profile.status != ProfileStatus.REVIEW_REQUIRED:
            raise ProfileStateError("CriticProfile must be REVIEW_REQUIRED before rejection")
        rejected = self._rebuild(profile, status=ProfileStatus.REJECTED)
        approval_type = (
            ApprovalType.CRITIC_PROFILE_AMENDMENT
            if rejected.supersedes_profile_id is not None
            else ApprovalType.CRITIC_PROFILE
        )
        approval = UserApproval(
            task_id=rejected.task_id,
            approval_type=approval_type,
            target_id=rejected.profile_id,
            decision=ApprovalDecision.REJECTED,
            user_changes={"reason": reason} if reason else {},
        )
        self._profiles[profile_id] = rejected
        self._approvals.append(approval)
        self._pending_profile_by_task.pop(rejected.task_id, None)
        self._persist_profile(rejected)
        self._persist_approval(approval)
        return rejected, approval

    def propose_amendment(
        self,
        approved_profile_id: str,
        changes: dict[str, Any],
    ) -> CriticProfile:
        current = self.get_profile(approved_profile_id)
        if current.status != ProfileStatus.APPROVED:
            raise ProfileStateError("Only an APPROVED profile can be amended")
        if not self.is_material_change(current, changes):
            raise ProfileStateError("Amendment does not contain a material profile change")
        unknown = set(changes) - self.MATERIAL_FIELDS
        if unknown:
            raise ProfileStateError(f"Unsupported profile fields: {sorted(unknown)}")

        values = current.model_dump()
        values.pop("profile_id", None)
        values.update(changes)
        values.update(
            {
                "version": current.version + 1,
                "status": ProfileStatus.DRAFT,
                "approved_at": None,
                "approved_by": None,
                "supersedes_profile_id": current.profile_id,
                "created_at": utc_now(),
            }
        )
        amendment = CriticProfile(**values)
        self._profiles[amendment.profile_id] = amendment
        self._pending_profile_by_task[amendment.task_id] = amendment.profile_id
        self._persist_profile(amendment)
        return amendment

    def restore_records(
        self,
        *,
        assessments: list[DomainAssessment],
        profiles: list[CriticProfile],
        approvals: list[UserApproval],
    ) -> None:
        """Restore persisted profile state without creating new lifecycle events."""
        for assessment in sorted(assessments, key=lambda item: item.created_at):
            self._assessments[assessment.assessment_id] = assessment
            self._latest_assessment_by_task[assessment.task_id] = assessment.assessment_id

        for profile in sorted(
            profiles,
            key=lambda item: (item.task_id, item.version, item.created_at),
        ):
            self._profiles[profile.profile_id] = profile

        existing_approval_ids = {item.approval_id for item in self._approvals}
        for approval in sorted(approvals, key=lambda item: item.created_at):
            if approval.approval_id not in existing_approval_ids:
                self._approvals.append(approval)
                existing_approval_ids.add(approval.approval_id)

        by_task: dict[str, list[CriticProfile]] = {}
        for profile in profiles:
            if profile.status in {ProfileStatus.DRAFT, ProfileStatus.REVIEW_REQUIRED}:
                by_task.setdefault(profile.task_id, []).append(profile)
        for task_id, pending in by_task.items():
            latest = max(pending, key=lambda item: (item.version, item.created_at))
            self._pending_profile_by_task[task_id] = latest.profile_id

    def is_material_change(self, profile: CriticProfile, changes: dict[str, Any]) -> bool:
        for field, value in changes.items():
            if field in self.MATERIAL_FIELDS and getattr(profile, field) != value:
                return True
        return False

    def get_approvals(self, task_id: str) -> list[UserApproval]:
        return [approval for approval in self._approvals if approval.task_id == task_id]

    def _persist_profile(self, profile: CriticProfile) -> None:
        if self.persistence is not None:
            self.persistence.save_critic_profile(profile)

    def _persist_approval(self, approval: UserApproval) -> None:
        if self.persistence is not None:
            self.persistence.save_user_approval(approval)

    @staticmethod
    def _rebuild(profile: CriticProfile, **changes: Any) -> CriticProfile:
        values = profile.model_dump()
        values.update(changes)
        return CriticProfile(**values)

    @staticmethod
    def _critic_role(domains: list[str]) -> str:
        if len(domains) == 1:
            return f"Independent {domains[0]} reviewer"
        return f"Independent multi-domain reviewer for {', '.join(domains)}"

    @staticmethod
    def _cross_checks(risk: RiskLevel) -> list[str]:
        if risk == RiskLevel.CRITICAL:
            return [
                "primary or official source where available",
                "two independent confirmations for critical claims",
            ]
        if risk == RiskLevel.HIGH:
            return ["two independent confirmations for high-impact claims"]
        if risk == RiskLevel.MEDIUM:
            return ["independent confirmation for important factual claims"]
        return []

    @staticmethod
    def _minimum_evidence_level(risk: RiskLevel) -> str:
        return {
            RiskLevel.LOW: "credible",
            RiskLevel.MEDIUM: "authoritative",
            RiskLevel.HIGH: "authoritative_cross_checked",
            RiskLevel.CRITICAL: "primary_or_authoritative_cross_checked",
        }[risk]

    @staticmethod
    def _freshness_requirement(risk: RiskLevel) -> str:
        if risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return "current_where_relevant_and_verified"
        return "current_where_relevant"

    @staticmethod
    def _confidence_threshold(risk: RiskLevel) -> float:
        return {
            RiskLevel.LOW: 0.75,
            RiskLevel.MEDIUM: 0.80,
            RiskLevel.HIGH: 0.90,
            RiskLevel.CRITICAL: 0.95,
        }[risk]
