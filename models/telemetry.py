from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .contracts import TaskId, utc_now
from .enums import ReviewDecision, TaskStatus


class TelemetryModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class ProviderUsageRecord(TelemetryModel):
    """Provider-neutral usage record for optional standalone/API telemetry."""

    task_id: TaskId
    component: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    api_calls: int = Field(default=1, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    estimated_cost_usd: float | None = Field(default=None, ge=0.0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class TaskQualityMetrics(TelemetryModel):
    """Runtime-independent quality/audit metrics derivable from workflow state."""

    task_id: TaskId
    final_state: TaskStatus
    iteration_count: int = Field(ge=0)
    critic_decisions: list[ReviewDecision] = Field(default_factory=list)
    reliability_scores: list[float] = Field(default_factory=list)
    final_reliability_score: float | None = Field(default=None, ge=0.0, le=1.0)
    claims_total: int = Field(default=0, ge=0)
    claims_with_sources: int = Field(default=0, ge=0)
    claims_verified: int = Field(default=0, ge=0)
    claims_unresolved: int = Field(default=0, ge=0)
    sources_total: int = Field(default=0, ge=0)
    claim_source_coverage_ratio: float | None = Field(default=None, ge=0.0, le=1.0)
    claim_verification_ratio: float | None = Field(default=None, ge=0.0, le=1.0)
    critical_issue_count: int = Field(default=0, ge=0)
    contradiction_count: int = Field(default=0, ge=0)
    missing_topic_count: int = Field(default=0, ge=0)
    agent_run_count: int = Field(default=0, ge=0)
    search_calls: int = Field(default=0, ge=0)
    fetch_calls: int = Field(default=0, ge=0)
    retry_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    provider_usage: list[ProviderUsageRecord] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=utc_now)
