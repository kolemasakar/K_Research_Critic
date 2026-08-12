from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import Field, model_validator

from .contracts import Claim, ContractModel, NonEmptyText, RunId, Source, TaskId, utc_now
from .identifiers import generate_id

ResearchResultId = Annotated[str, Field(pattern=r"^RESEARCH_RESULT_[A-Z0-9]+$")]


class ResearchResult(ContractModel):
    """Structured ResearchAgent payload used across initial and revision runs."""

    research_result_id: ResearchResultId = Field(
        default_factory=lambda: generate_id("RESEARCH_RESULT"), frozen=True
    )
    task_id: TaskId = Field(frozen=True)
    run_id: RunId = Field(frozen=True)
    iteration: int = Field(ge=1)
    summary: NonEmptyText
    findings: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    draft_report: NonEmptyText
    change_log: list[str] = Field(default_factory=list)
    changes_applied: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_evidence_links(self) -> "ResearchResult":
        embedded_source_ids = [source.source_id for source in self.sources]
        embedded_claim_ids = [claim.claim_id for claim in self.claims]

        if self.source_ids and self.source_ids != embedded_source_ids:
            raise ValueError("source_ids must match embedded sources in order")
        if self.claim_ids and self.claim_ids != embedded_claim_ids:
            raise ValueError("claim_ids must match embedded claims in order")
        if not self.source_ids:
            self.source_ids = embedded_source_ids
        if not self.claim_ids:
            self.claim_ids = embedded_claim_ids

        source_id_set = set(self.source_ids)
        for source in self.sources:
            if source.task_id != self.task_id:
                raise ValueError("ResearchResult source task_id must match result task_id")
        for claim in self.claims:
            if claim.task_id != self.task_id:
                raise ValueError("ResearchResult claim task_id must match result task_id")
            if claim.created_by_run_id != self.run_id:
                raise ValueError("ResearchResult claim run_id must match result run_id")
            missing = set(claim.source_ids) - source_id_set
            if missing:
                raise ValueError(f"Claim references unknown source_ids: {sorted(missing)}")

        if self.change_log and self.changes_applied and self.change_log != self.changes_applied:
            raise ValueError("change_log and changes_applied must match when both are supplied")
        if not self.change_log and self.changes_applied:
            self.change_log = list(self.changes_applied)
        if not self.changes_applied and self.change_log:
            self.changes_applied = list(self.change_log)
        return self
