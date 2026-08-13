from __future__ import annotations

from models import (
    AgentResult,
    AgentType,
    Claim,
    ClaimType,
    CriticReview,
    ExecutionStatus,
    ImportanceLevel,
    Metrics,
    ReliabilityClass,
    ResearchResult,
    ReviewDecision,
    Source,
    SourceType,
    Task,
    TaskStatus,
    VerificationStatus,
    generate_id,
    utc_now,
)
from persistence import TaskAuditSnapshot
from providers.telemetry import MeteredOpenAISemanticDomainProvider
from supervisor.metrics import collect_quality_metrics, collect_quality_metrics_from_audit


def _quality_fixture():
    task_id = generate_id("TASK")
    research_run = generate_id("RUN")
    critic_run = generate_id("RUN")
    source = Source(
        task_id=task_id,
        url="https://example.org/source",
        title="Official source",
        publisher="Example",
        accessed_at=utc_now(),
        source_type=SourceType.OFFICIAL,
        reliability_class=ReliabilityClass.A,
        primary_source=True,
    )
    claim = Claim(
        task_id=task_id,
        text="Evidence supports the conclusion.",
        claim_type=ClaimType.FACT,
        importance=ImportanceLevel.HIGH,
        source_ids=[source.source_id],
        confidence=0.95,
        verification_status=VerificationStatus.VERIFIED,
        created_by_run_id=research_run,
    )
    research = ResearchResult(
        task_id=task_id,
        run_id=research_run,
        iteration=1,
        summary="Evidence supports the conclusion.",
        findings=[claim.text],
        claims=[claim],
        sources=[source],
        draft_report="# Draft\n\nEvidence supports the conclusion.",
    )
    review = CriticReview(
        task_id=task_id,
        run_id=critic_run,
        profile_id=generate_id("PROFILE"),
        iteration=1,
        decision=ReviewDecision.PASS,
        reliability_score=0.93,
        verified_claim_ids=[claim.claim_id],
    )
    research_agent = AgentResult(
        run_id=research_run,
        request_id=generate_id("REQUEST"),
        task_id=task_id,
        agent_id=generate_id("AGENT"),
        agent_type=AgentType.RESEARCH,
        status=ExecutionStatus.SUCCEEDED,
        result_type="research_result",
        payload=research.model_dump(mode="json"),
        metrics=Metrics(search_calls=2, fetch_calls=1, sources_examined=1, claims_created=1),
        started_at=utc_now(),
        completed_at=utc_now(),
    )
    critic_agent = AgentResult(
        run_id=critic_run,
        request_id=generate_id("REQUEST"),
        task_id=task_id,
        agent_id=generate_id("AGENT"),
        agent_type=AgentType.CRITIC,
        status=ExecutionStatus.SUCCEEDED,
        result_type="critic_review",
        payload=review.model_dump(mode="json"),
        metrics=Metrics(search_calls=1, fetch_calls=1, claims_verified=1),
        started_at=utc_now(),
        completed_at=utc_now(),
    )
    return task_id, research, review, research_agent, critic_agent


def test_quality_metrics_cover_final_evidence_without_provider_calls() -> None:
    task_id, research, review, research_agent, critic_agent = _quality_fixture()

    metrics = collect_quality_metrics(
        task_id=task_id,
        final_state=TaskStatus.FINALIZED,
        research_results=[research],
        reviews=[review],
        agent_results=[research_agent, critic_agent],
    )

    assert metrics.iteration_count == 1
    assert metrics.critic_decisions == [ReviewDecision.PASS]
    assert metrics.final_reliability_score == 0.93
    assert metrics.claims_total == 1
    assert metrics.claims_with_sources == 1
    assert metrics.claims_verified == 1
    assert metrics.claims_unresolved == 0
    assert metrics.sources_total == 1
    assert metrics.claim_source_coverage_ratio == 1.0
    assert metrics.claim_verification_ratio == 1.0
    assert metrics.search_calls == 3
    assert metrics.fetch_calls == 2


def test_quality_metrics_reconstruct_from_restart_safe_audit() -> None:
    task_id, research, review, research_agent, critic_agent = _quality_fixture()
    task = Task(
        task_id=task_id,
        user_request="Assess evidence.",
        task_type="research",
        status=TaskStatus.FINALIZED,
    )
    audit = TaskAuditSnapshot(
        task=task,
        agent_results=(research_agent, critic_agent),
        research_results=(research,),
        reviews=(review,),
    )

    metrics = collect_quality_metrics_from_audit(audit)

    assert metrics.task_id == task_id
    assert metrics.final_state == TaskStatus.FINALIZED
    assert metrics.final_reliability_score == 0.93
    assert metrics.claim_verification_ratio == 1.0


def test_optional_provider_usage_can_estimate_cost_when_pricing_is_supplied() -> None:
    provider = object.__new__(MeteredOpenAISemanticDomainProvider)
    provider.model = "test-model"
    provider._api_calls = 2
    provider._last_usage = {"input_tokens": 1000, "output_tokens": 500, "total_tokens": 1500}
    provider.input_cost_per_million_tokens = 2.0
    provider.output_cost_per_million_tokens = 8.0

    usage = provider._build_usage(generate_id("TASK"))

    assert usage.api_calls == 2
    assert usage.input_tokens == 1000
    assert usage.output_tokens == 500
    assert usage.total_tokens == 1500
    assert usage.estimated_cost_usd == 0.006
