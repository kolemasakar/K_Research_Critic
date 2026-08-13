from __future__ import annotations

import json
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenStoreModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class StoreDistributionSnapshot(FrozenStoreModel):
    channel: Literal["chatgpt_store"] = "chatgpt_store"
    model_policy: Literal["user_plan"] = "user_plan"
    developer_api_key_required: Literal[False] = False
    external_backend_required: Literal[False] = False


class StoreCheckpointSource(FrozenStoreModel):
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: str | None = None
    reliability: str | None = None


class StoreCheckpointClaim(FrozenStoreModel):
    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    verification_status: str | None = None
    source_ids: list[str] = Field(default_factory=list)


class StoreCheckpointResearch(FrozenStoreModel):
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
    claims: list[StoreCheckpointClaim] = Field(default_factory=list)
    sources: list[StoreCheckpointSource] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class StoreCheckpointReview(FrozenStoreModel):
    decision: Literal["PASS", "REVISE"]
    reliability_score: float = Field(ge=0.0, le=1.0)
    critical_issues: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    weak_sources: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    missing_topics: list[str] = Field(default_factory=list)
    recommended_changes: list[str] = Field(default_factory=list)


class StoreCheckpointProfile(FrozenStoreModel):
    profile_id: str = Field(min_length=1)
    version: int = Field(ge=1)
    status: Literal["REVIEW_REQUIRED", "APPROVED"]
    domain: str = Field(min_length=1)
    subdomains: list[str] = Field(default_factory=list)
    task_type: str = Field(min_length=1)
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    critic_role: str = Field(min_length=1)
    evaluation_criteria: list[str] = Field(min_length=1)
    preferred_source_types: list[str] = Field(min_length=1)
    required_cross_checks: int = Field(ge=0)
    standards: list[str] = Field(default_factory=list)
    minimum_evidence_level: str = Field(min_length=1)
    freshness_requirement: str = Field(min_length=1)
    confidence_threshold: float = Field(ge=0.0, le=1.0)
    special_user_requirements: list[str] = Field(default_factory=list)
    approved_by: str | None = None
    approved_at: datetime | None = None

    @model_validator(mode="after")
    def validate_approval_metadata(self) -> "StoreCheckpointProfile":
        if self.status == "APPROVED":
            if not self.approved_by or self.approved_at is None:
                raise ValueError("APPROVED checkpoint profile requires approval metadata")
        return self


SafeStoreState = Literal[
    "PROFILE_REVIEW_REQUIRED",
    "PROFILE_APPROVED",
    "REVISE_REQUIRED",
    "APPROVED",
    "FINALIZED",
    "COMPLETED_WITH_LIMITATIONS",
    "FAILED",
]

ResumePolicy = Literal["REQUIRE_PROFILE_APPROVAL", "CONFIRM_RESUME", "TERMINAL"]


class StoreCheckpoint(FrozenStoreModel):
    marker: Literal["K_SUPERVISOR_CHECKPOINT"] = "K_SUPERVISOR_CHECKPOINT"
    schema_version: Literal["1.0"] = "1.0"
    task_id: str = Field(pattern=r"^TASK_[A-Za-z0-9_-]+$")
    task_summary: str = Field(min_length=1)
    workflow_state: SafeStoreState
    resume_policy: ResumePolicy
    iteration: int = Field(ge=0)
    critic_profile: StoreCheckpointProfile
    latest_research: StoreCheckpointResearch | None = None
    latest_review: StoreCheckpointReview | None = None
    limitations: list[str] = Field(default_factory=list)
    distribution: StoreDistributionSnapshot = Field(default_factory=StoreDistributionSnapshot)
    created_at: datetime

    @model_validator(mode="after")
    def validate_resume_boundary(self) -> "StoreCheckpoint":
        if self.workflow_state == "PROFILE_REVIEW_REQUIRED":
            if self.critic_profile.status != "REVIEW_REQUIRED":
                raise ValueError("PROFILE_REVIEW_REQUIRED requires REVIEW_REQUIRED profile")
            if self.resume_policy != "REQUIRE_PROFILE_APPROVAL":
                raise ValueError("profile review checkpoint requires REQUIRE_PROFILE_APPROVAL")
            return self

        if self.critic_profile.status != "APPROVED":
            raise ValueError("safe post-approval checkpoint states require APPROVED profile")

        terminal = {"FINALIZED", "COMPLETED_WITH_LIMITATIONS", "FAILED"}
        expected_policy = "TERMINAL" if self.workflow_state in terminal else "CONFIRM_RESUME"
        if self.resume_policy != expected_policy:
            raise ValueError(f"{self.workflow_state} requires resume_policy={expected_policy}")
        return self


def checkpoint_schema() -> dict:
    return StoreCheckpoint.model_json_schema()


def load_checkpoint_json(text: str) -> StoreCheckpoint:
    payload = json.loads(text)
    return StoreCheckpoint.model_validate(payload)
