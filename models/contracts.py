from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .enums import (
    AgentStatus,
    AgentType,
    ApprovalDecision,
    ApprovalType,
    ArtifactStatus,
    ArtifactType,
    ClaimType,
    ErrorType,
    ExecutionStatus,
    ImportanceLevel,
    ProfileStatus,
    ReliabilityClass,
    ReviewDecision,
    RiskLevel,
    SourceType,
    TaskStatus,
    VerificationStatus,
)
from .identifiers import IdPrefix, generate_id


TaskId = Annotated[str, Field(pattern=r"^TASK_[A-Z0-9]+$")]
RunId = Annotated[str, Field(pattern=r"^RUN_[A-Z0-9]+$")]
WorkflowRunId = Annotated[str, Field(pattern=r"^WF_[A-Z0-9]+$")]
ProfileId = Annotated[str, Field(pattern=r"^PROFILE_[A-Z0-9]+$")]
ClaimId = Annotated[str, Field(pattern=r"^CLAIM_[A-Z0-9]+$")]
SourceId = Annotated[str, Field(pattern=r"^SOURCE_[A-Z0-9]+$")]
ReviewId = Annotated[str, Field(pattern=r"^REVIEW_[A-Z0-9]+$")]
ArtifactId = Annotated[str, Field(pattern=r"^ARTIFACT_[A-Z0-9]+$")]
AssessmentId = Annotated[str, Field(pattern=r"^ASSESSMENT_[A-Z0-9]+$")]
ApprovalId = Annotated[str, Field(pattern=r"^APPROVAL_[A-Z0-9]+$")]
RequestId = Annotated[str, Field(pattern=r"^REQUEST_[A-Z0-9]+$")]
AgentId = Annotated[str, Field(pattern=r"^AGENT_[A-Z0-9]+$")]
Confidence = Annotated[float, Field(ge=0.0, le=1.0)]
NonEmptyText = Annotated[str, Field(min_length=1)]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ContractModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    @field_validator("*", mode="after")
    @classmethod
    def normalize_datetime_to_utc(cls, value: Any) -> Any:
        if not isinstance(value, datetime):
            return value
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime values must be timezone-aware")
        if value.utcoffset() != timedelta(0):
            return value.astimezone(timezone.utc)
        return value


class Task(ContractModel):
    task_id: TaskId = Field(default_factory=lambda: generate_id(IdPrefix.TASK), frozen=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    status: TaskStatus = TaskStatus.NEW
    user_request: NonEmptyText
    task_type: NonEmptyText
    primary_domain: str | None = None
    secondary_domains: list[str] = Field(default_factory=list)
    risk_level: RiskLevel | None = None
    active_profile_id: ProfileId | None = None
    current_workflow_run_id: WorkflowRunId | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_task_times(self) -> "Task":
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot be earlier than created_at")
        return self


class DomainAssessment(ContractModel):
    assessment_id: AssessmentId = Field(
        default_factory=lambda: generate_id(IdPrefix.ASSESSMENT), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    primary_domain: NonEmptyText
    secondary_domains: list[str] = Field(default_factory=list)
    task_type: NonEmptyText
    risk_level: RiskLevel
    identified_standards: list[str] = Field(default_factory=list)
    recommended_source_types: list[str] = Field(default_factory=list)
    recommended_evaluation_criteria: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class CriticProfile(ContractModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        frozen=True,
    )

    profile_id: ProfileId = Field(
        default_factory=lambda: generate_id(IdPrefix.PROFILE), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    version: int = Field(default=1, ge=1)
    status: ProfileStatus = ProfileStatus.DRAFT
    domain: list[str] = Field(min_length=1)
    subdomains: list[str] = Field(default_factory=list)
    task_type: NonEmptyText
    risk_level: RiskLevel
    critic_role: NonEmptyText
    evaluation_criteria: list[str] = Field(min_length=1)
    preferred_source_types: list[str] = Field(default_factory=list)
    required_cross_checks: list[str] = Field(default_factory=list)
    standards: list[str] = Field(default_factory=list)
    minimum_evidence_level: NonEmptyText
    freshness_requirement: NonEmptyText
    confidence_threshold: Confidence
    special_user_requirements: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    approved_at: datetime | None = None
    approved_by: str | None = None
    supersedes_profile_id: ProfileId | None = None

    @model_validator(mode="after")
    def validate_approval_boundary(self) -> "CriticProfile":
        if self.status == ProfileStatus.APPROVED:
            if self.approved_at is None or not self.approved_by:
                raise ValueError(
                    "APPROVED CriticProfile requires approved_at and approved_by"
                )
        return self


class UserApproval(ContractModel):
    approval_id: ApprovalId = Field(
        default_factory=lambda: generate_id(IdPrefix.APPROVAL), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    approval_type: ApprovalType
    target_id: NonEmptyText
    decision: ApprovalDecision
    user_changes: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class AgentDefinition(ContractModel):
    agent_id: AgentId = Field(default_factory=lambda: generate_id(IdPrefix.AGENT), frozen=True)
    agent_type: AgentType
    name: NonEmptyText
    version: NonEmptyText
    capabilities: list[str] = Field(default_factory=list)
    accepted_input_types: list[str] = Field(default_factory=list)
    produced_output_types: list[str] = Field(default_factory=list)
    supports_profile: bool = False
    status: AgentStatus = AgentStatus.ACTIVE
    metadata: dict[str, Any] = Field(default_factory=dict)


class ErrorRecord(ContractModel):
    error_code: NonEmptyText
    error_type: ErrorType
    message: NonEmptyText
    recoverable: bool
    component: NonEmptyText
    run_id: RunId | None = None
    retry_count: int = Field(default=0, ge=0)
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class WarningRecord(ContractModel):
    warning_code: NonEmptyText
    message: NonEmptyText
    component: NonEmptyText
    run_id: RunId | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class Metrics(ContractModel):
    duration_ms: int | None = Field(default=None, ge=0)
    llm_calls: int | None = Field(default=None, ge=0)
    search_calls: int | None = Field(default=None, ge=0)
    fetch_calls: int | None = Field(default=None, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    estimated_cost: float | None = Field(default=None, ge=0.0)
    sources_examined: int | None = Field(default=None, ge=0)
    claims_created: int | None = Field(default=None, ge=0)
    claims_verified: int | None = Field(default=None, ge=0)
    retry_count: int = Field(default=0, ge=0)


class AgentRunRequest(ContractModel):
    request_id: RequestId = Field(
        default_factory=lambda: generate_id(IdPrefix.REQUEST), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    workflow_run_id: WorkflowRunId = Field(frozen=True)
    run_id: RunId = Field(default_factory=lambda: generate_id(IdPrefix.RUN), frozen=True)
    agent_id: AgentId = Field(frozen=True)
    agent_type: AgentType
    iteration: int = Field(default=1, ge=1)
    input: dict[str, Any]
    context: dict[str, Any] = Field(default_factory=dict)
    profile: CriticProfile | None = None
    constraints: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def enforce_critic_profile_gate(self) -> "AgentRunRequest":
        if self.agent_type == AgentType.CRITIC:
            if self.profile is None:
                raise ValueError("CriticAgent execution requires a CriticProfile")
            if self.profile.status != ProfileStatus.APPROVED:
                raise ValueError("CriticAgent execution requires an APPROVED CriticProfile")
            if self.profile.task_id != self.task_id:
                raise ValueError("CriticProfile task_id must match request task_id")
        return self


class AgentResult(ContractModel):
    run_id: RunId = Field(frozen=True)
    request_id: RequestId = Field(frozen=True)
    task_id: TaskId = Field(frozen=True)
    agent_id: AgentId = Field(frozen=True)
    agent_type: AgentType
    status: ExecutionStatus
    result_type: NonEmptyText
    payload: dict[str, Any] = Field(default_factory=dict)
    warnings: list[WarningRecord] = Field(default_factory=list)
    errors: list[ErrorRecord] = Field(default_factory=list)
    metrics: Metrics = Field(default_factory=Metrics)
    started_at: datetime
    completed_at: datetime

    @model_validator(mode="after")
    def validate_execution_times(self) -> "AgentResult":
        if self.completed_at < self.started_at:
            raise ValueError("completed_at cannot be earlier than started_at")
        if self.status == ExecutionStatus.FAILED and not self.errors:
            raise ValueError("FAILED AgentResult requires at least one ErrorRecord")
        return self


class Claim(ContractModel):
    claim_id: ClaimId = Field(default_factory=lambda: generate_id(IdPrefix.CLAIM), frozen=True)
    task_id: TaskId = Field(frozen=True)
    text: NonEmptyText
    claim_type: ClaimType
    importance: ImportanceLevel
    source_ids: list[SourceId] = Field(default_factory=list)
    confidence: Confidence
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    created_by_run_id: RunId = Field(frozen=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_claim_times(self) -> "Claim":
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot be earlier than created_at")
        return self


class Source(ContractModel):
    source_id: SourceId = Field(
        default_factory=lambda: generate_id(IdPrefix.SOURCE), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    url: str | None = None
    title: NonEmptyText
    publisher: str | None = None
    author: str | None = None
    publication_date: date | None = None
    accessed_at: datetime | None = None
    source_type: SourceType
    reliability_class: ReliabilityClass
    primary_source: bool = False
    independence_group: str | None = None
    supports_claim_ids: list[ClaimId] = Field(default_factory=list)
    contradicts_claim_ids: list[ClaimId] = Field(default_factory=list)
    notes: str | None = None

    @model_validator(mode="after")
    def require_access_time_for_web_source(self) -> "Source":
        if self.url and self.accessed_at is None:
            raise ValueError("Web sources with a URL require accessed_at")
        return self


class CriticReview(ContractModel):
    review_id: ReviewId = Field(
        default_factory=lambda: generate_id(IdPrefix.REVIEW), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    run_id: RunId = Field(frozen=True)
    profile_id: ProfileId = Field(frozen=True)
    iteration: int = Field(ge=1)
    decision: ReviewDecision
    reliability_score: Confidence
    critical_issues: list[str] = Field(default_factory=list)
    unsupported_claim_ids: list[ClaimId] = Field(default_factory=list)
    weak_source_ids: list[SourceId] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    missing_topics: list[str] = Field(default_factory=list)
    recommended_changes: list[str] = Field(default_factory=list)
    verified_claim_ids: list[ClaimId] = Field(default_factory=list)
    unresolved_claim_ids: list[ClaimId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class Artifact(ContractModel):
    artifact_id: ArtifactId = Field(
        default_factory=lambda: generate_id(IdPrefix.ARTIFACT), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    workflow_run_id: WorkflowRunId = Field(frozen=True)
    artifact_type: ArtifactType
    path: NonEmptyText
    encoding: NonEmptyText
    status: ArtifactStatus
    created_by_run_id: RunId | None = Field(default=None, frozen=True)
    created_at: datetime = Field(default_factory=utc_now)
    checksum: NonEmptyText
    metadata: dict[str, Any] = Field(default_factory=dict)


ReviewResult = CriticReview
