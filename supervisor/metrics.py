from __future__ import annotations

from collections.abc import Iterable

from models import AgentResult, CriticReview, ProviderUsageRecord, ResearchResult, TaskQualityMetrics, TaskStatus
from persistence import TaskAuditSnapshot


def collect_quality_metrics(
    *,
    task_id: str,
    final_state: TaskStatus,
    research_results: Iterable[ResearchResult],
    reviews: Iterable[CriticReview],
    agent_results: Iterable[AgentResult],
    provider_usage: Iterable[ProviderUsageRecord] = (),
) -> TaskQualityMetrics:
    """Build runtime-independent task quality metrics without causing new provider calls."""

    research = sorted(
        (item for item in research_results if item.task_id == task_id),
        key=lambda item: item.iteration,
    )
    critic_reviews = sorted(
        (item for item in reviews if item.task_id == task_id),
        key=lambda item: item.iteration,
    )
    runs = [item for item in agent_results if item.task_id == task_id]
    usage = [item for item in provider_usage if item.task_id == task_id]

    latest_research = research[-1] if research else None
    latest_review = critic_reviews[-1] if critic_reviews else None

    claims = list(latest_research.claims) if latest_research is not None else []
    sources = list(latest_research.sources) if latest_research is not None else []
    claims_total = len(claims)
    claims_with_sources = sum(1 for claim in claims if claim.source_ids)
    claims_verified = len(latest_review.verified_claim_ids) if latest_review is not None else 0
    claims_unresolved = len(latest_review.unresolved_claim_ids) if latest_review is not None else 0

    return TaskQualityMetrics(
        task_id=task_id,
        final_state=final_state,
        iteration_count=max(
            [item.iteration for item in research] + [item.iteration for item in critic_reviews],
            default=0,
        ),
        critic_decisions=[item.decision for item in critic_reviews],
        reliability_scores=[item.reliability_score for item in critic_reviews],
        final_reliability_score=(
            latest_review.reliability_score if latest_review is not None else None
        ),
        claims_total=claims_total,
        claims_with_sources=claims_with_sources,
        claims_verified=claims_verified,
        claims_unresolved=claims_unresolved,
        sources_total=len(sources),
        claim_source_coverage_ratio=_ratio(claims_with_sources, claims_total),
        claim_verification_ratio=_ratio(claims_verified, claims_total),
        critical_issue_count=(
            len(latest_review.critical_issues) if latest_review is not None else 0
        ),
        contradiction_count=(
            len(latest_review.contradictions) if latest_review is not None else 0
        ),
        missing_topic_count=(
            len(latest_review.missing_topics) if latest_review is not None else 0
        ),
        agent_run_count=len(runs),
        search_calls=sum(item.metrics.search_calls or 0 for item in runs),
        fetch_calls=sum(item.metrics.fetch_calls or 0 for item in runs),
        retry_count=sum(item.metrics.retry_count for item in runs),
        warning_count=sum(len(item.warnings) for item in runs),
        error_count=sum(len(item.errors) for item in runs),
        provider_usage=usage,
    )


def collect_quality_metrics_from_audit(
    audit: TaskAuditSnapshot,
    *,
    provider_usage: Iterable[ProviderUsageRecord] = (),
) -> TaskQualityMetrics:
    """Derive quality metrics from persisted audit data after restart."""

    return collect_quality_metrics(
        task_id=audit.task.task_id,
        final_state=audit.task.status,
        research_results=audit.research_results,
        reviews=audit.reviews,
        agent_results=audit.agent_results,
        provider_usage=provider_usage,
    )


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round(numerator / denominator, 4)
