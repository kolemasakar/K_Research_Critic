from __future__ import annotations

from pydantic import Field, model_validator

from .contracts import Claim, ContractModel, NonEmptyText, RunId, Source, TaskId


class ResearchResult(ContractModel):
    """Structured ResearchAgent payload used across initial and revision runs."""

    task_id: TaskId = Field(frozen=True)
    run_id: RunId = Field(frozen=True)
    iteration: int = Field(ge=1)
    summary: NonEmptyText
    findings: list[str] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    draft_report: NonEmptyText
    changes_applied: list[str] = Field(default_factory=list)
    search_queries: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_evidence_links(self) -> "ResearchResult":
        source_ids = {source.source_id for source in self.sources}
        for source in self.sources:
            if source.task_id != self.task_id:
                raise ValueError("ResearchResult source task_id must match result task_id")
        for claim in self.claims:
            if claim.task_id != self.task_id:
                raise ValueError("ResearchResult claim task_id must match result task_id")
            if claim.created_by_run_id != self.run_id:
                raise ValueError("ResearchResult claim run_id must match result run_id")
            missing = set(claim.source_ids) - source_ids
            if missing:
                raise ValueError(f"Claim references unknown source_ids: {sorted(missing)}")
        return self
