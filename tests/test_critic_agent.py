from __future__ import annotations

from datetime import date

from agents import CriticAgent
from models import (
    AgentRunRequest,
    AgentType,
    Claim,
    ClaimType,
    CriticProfile,
    CriticReview,
    ExecutionStatus,
    IdPrefix,
    ImportanceLevel,
    ProfileStatus,
    ReliabilityClass,
    ReviewDecision,
    RiskLevel,
    Source,
    SourceType,
    VerificationStatus,
    generate_id,
    utc_now,
)
from models.research import ResearchResult
from tools import FetchedDocument, SearchHit


class FakeCriticTools:
    def __init__(self, *, search_results=None, documents=None, search_error=None, fetch_errors=None):
        self.search_results = search_results or {}
        self.documents = documents or {}
        self.search_error = search_error
        self.fetch_errors = set(fetch_errors or [])
        self.search_calls: list[tuple[str, int]] = []
        self.fetch_calls: list[str] = []

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        self.search_calls.append((query, limit))
        if self.search_error is not None:
            raise self.search_error
        return list(self.search_results.get(query, []))[:limit]

    def web_fetch(self, url: str) -> FetchedDocument:
        self.fetch_calls.append(url)
        if url in self.fetch_errors:
            raise RuntimeError(f"fetch failed for {url}")
        return self.documents[url]


def make_profile(
    task_id: str,
    *,
    domains: list[str],
    risk: RiskLevel,
    minimum_evidence_level: str,
    confidence_threshold: float,
    preferred_source_types: list[str],
    required_cross_checks: list[str] | None = None,
    special_user_requirements: list[str] | None = None,
) -> CriticProfile:
    return CriticProfile(
        task_id=task_id,
        status=ProfileStatus.APPROVED,
        domain=domains,
        task_type="research",
        risk_level=risk,
        critic_role="Independent reviewer",
        evaluation_criteria=["claim support", "source quality"],
        preferred_source_types=preferred_source_types,
        required_cross_checks=list(required_cross_checks or []),
        standards=["task-relevant authoritative sources"],
        minimum_evidence_level=minimum_evidence_level,
        freshness_requirement="current_where_relevant",
        confidence_threshold=confidence_threshold,
        special_user_requirements=list(special_user_requirements or []),
        approved_at=utc_now(),
        approved_by="user",
    )


def make_research(
    task_id: str,
    *,
    claim_text: str,
    source_type: SourceType,
    reliability: ReliabilityClass,
    importance: ImportanceLevel = ImportanceLevel.MEDIUM,
    confidence: float = 0.9,
) -> ResearchResult:
    research_run_id = generate_id(IdPrefix.RUN)
    source = Source(
        task_id=task_id,
        url="https://research.example/source",
        title="Research source",
        publisher="Research Publisher",
        publication_date=date.today(),
        accessed_at=utc_now(),
        source_type=source_type,
        reliability_class=reliability,
        primary_source=source_type in {SourceType.OFFICIAL, SourceType.PRIMARY_DOCUMENT, SourceType.STANDARD},
        independence_group="research-source",
    )
    claim = Claim(
        task_id=task_id,
        text=claim_text,
        claim_type=ClaimType.FACT,
        importance=importance,
        source_ids=[source.source_id],
        confidence=confidence,
        verification_status=VerificationStatus.UNVERIFIED,
        created_by_run_id=research_run_id,
    )
    source.supports_claim_ids = [claim.claim_id]
    return ResearchResult(
        task_id=task_id,
        run_id=research_run_id,
        iteration=1,
        summary=claim_text,
        findings=[claim_text],
        claims=[claim],
        sources=[source],
        draft_report=f"# Draft\n\n{claim_text} [{source.source_id}]",
    )


def make_verification(
    claim_text: str,
    *,
    url: str,
    source_type: SourceType,
    reliability: ReliabilityClass,
    content: str | None = None,
) -> tuple[SearchHit, FetchedDocument]:
    hit = SearchHit(
        url=url,
        title="Independent verification",
        publisher="Independent Publisher",
        snippet=claim_text,
        publication_date=date.today(),
        source_type=source_type,
        reliability_class=reliability,
        primary_source=source_type in {SourceType.OFFICIAL, SourceType.PRIMARY_DOCUMENT, SourceType.STANDARD},
        independence_group=url,
    )
    document = FetchedDocument(
        **hit.model_dump(),
        content=content or claim_text,
    )
    return hit, document


def make_request(agent: CriticAgent, profile: CriticProfile, research: ResearchResult, *, required_topics=None) -> AgentRunRequest:
    return AgentRunRequest(
        task_id=profile.task_id,
        workflow_run_id=generate_id(IdPrefix.WORKFLOW),
        agent_id=agent.definition.agent_id,
        agent_type=AgentType.CRITIC,
        iteration=research.iteration,
        input={
            "research_result": research.model_dump(mode="json"),
            "required_topics": list(required_topics or []),
        },
        profile=profile,
    )


def run_with_independent_support(
    *,
    profile: CriticProfile,
    research: ResearchResult,
    verification_type: SourceType,
    verification_reliability: ReliabilityClass,
) -> tuple[CriticAgent, CriticReview, ExecutionStatus]:
    claim = research.claims[0]
    url = "https://verify.example/independent"
    hit, document = make_verification(
        claim.text,
        url=url,
        source_type=verification_type,
        reliability=verification_reliability,
    )
    tools = FakeCriticTools(search_results={claim.text: [hit]}, documents={url: document})
    agent = CriticAgent(tools)
    result = agent.run(make_request(agent, profile, research))
    return agent, CriticReview.model_validate(result.payload), result.status


def test_literary_profile_uses_same_generic_agent_and_can_pass() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "The primary text explicitly uses a first-person narrator."
    profile = make_profile(
        task_id,
        domains=["literary_analysis"],
        risk=RiskLevel.LOW,
        minimum_evidence_level="credible",
        confidence_threshold=0.75,
        preferred_source_types=["PRIMARY_DOCUMENT", "ACADEMIC", "REFERENCE"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.PRIMARY_DOCUMENT,
        reliability=ReliabilityClass.A,
    )

    _, review, status = run_with_independent_support(
        profile=profile,
        research=research,
        verification_type=SourceType.ACADEMIC,
        verification_reliability=ReliabilityClass.B,
    )

    assert status == ExecutionStatus.SUCCEEDED
    assert review.decision == ReviewDecision.PASS
    assert review.reliability_score >= profile.confidence_threshold
    assert review.verified_claim_ids == [research.claims[0].claim_id]


def test_medical_profile_requires_authoritative_cross_checked_evidence() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "The current guideline recommends this intervention for the defined indication."
    profile = make_profile(
        task_id,
        domains=["medicine"],
        risk=RiskLevel.CRITICAL,
        minimum_evidence_level="primary_or_authoritative_cross_checked",
        confidence_threshold=0.95,
        preferred_source_types=["OFFICIAL", "PEER_REVIEWED", "PRIMARY_DOCUMENT", "GOVERNMENT"],
        required_cross_checks=["two independent confirmations for critical claims"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.OFFICIAL,
        reliability=ReliabilityClass.A,
        importance=ImportanceLevel.CRITICAL,
    )

    _, review, status = run_with_independent_support(
        profile=profile,
        research=research,
        verification_type=SourceType.GOVERNMENT,
        verification_reliability=ReliabilityClass.A,
    )

    assert status == ExecutionStatus.SUCCEEDED
    assert review.decision == ReviewDecision.PASS
    assert review.reliability_score >= 0.95


def test_technical_profile_revises_when_only_weak_evidence_exists() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "GNSS deformation monitoring requires a stable reference frame."
    profile = make_profile(
        task_id,
        domains=["geodesy"],
        risk=RiskLevel.HIGH,
        minimum_evidence_level="authoritative_cross_checked",
        confidence_threshold=0.90,
        preferred_source_types=["STANDARD", "OFFICIAL", "PRIMARY_DOCUMENT", "ACADEMIC"],
        required_cross_checks=["two independent confirmations for high-impact claims"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
        importance=ImportanceLevel.HIGH,
    )
    tools = FakeCriticTools(search_results={claim_text: []})
    agent = CriticAgent(tools)

    result = agent.run(make_request(agent, profile, research))
    review = CriticReview.model_validate(result.payload)

    assert result.status == ExecutionStatus.SUCCEEDED
    assert review.decision == ReviewDecision.REVISE
    assert research.claims[0].claim_id in review.unsupported_claim_ids
    assert research.sources[0].source_id in review.weak_source_ids


def test_multi_domain_profile_uses_same_critic_implementation() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "Structural displacement interpretation depends on the geodetic reference system."
    profile = make_profile(
        task_id,
        domains=["construction", "geodesy"],
        risk=RiskLevel.HIGH,
        minimum_evidence_level="authoritative_cross_checked",
        confidence_threshold=0.90,
        preferred_source_types=["STANDARD", "OFFICIAL", "PRIMARY_DOCUMENT", "ACADEMIC"],
        required_cross_checks=["two independent confirmations for high-impact claims"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.STANDARD,
        reliability=ReliabilityClass.A,
        importance=ImportanceLevel.HIGH,
    )

    _, review, status = run_with_independent_support(
        profile=profile,
        research=research,
        verification_type=SourceType.ACADEMIC,
        verification_reliability=ReliabilityClass.B,
    )

    assert status == ExecutionStatus.SUCCEEDED
    assert review.decision == ReviewDecision.PASS


def test_same_evidence_can_pass_low_risk_profile_and_fail_high_risk_profile() -> None:
    claim_text = "The documented interface accepts structured JSON input."

    low_task = generate_id(IdPrefix.TASK)
    low_profile = make_profile(
        low_task,
        domains=["general_research"],
        risk=RiskLevel.LOW,
        minimum_evidence_level="credible",
        confidence_threshold=0.75,
        preferred_source_types=["REFERENCE"],
    )
    low_research = make_research(
        low_task,
        claim_text=claim_text,
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
        confidence=0.8,
    )
    low_hit, low_doc = make_verification(
        claim_text,
        url="https://verify.example/low",
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
    )
    low_agent = CriticAgent(FakeCriticTools(search_results={claim_text: [low_hit]}, documents={low_hit.url: low_doc}))
    low_review = CriticReview.model_validate(low_agent.run(make_request(low_agent, low_profile, low_research)).payload)

    high_task = generate_id(IdPrefix.TASK)
    high_profile = make_profile(
        high_task,
        domains=["software_engineering"],
        risk=RiskLevel.HIGH,
        minimum_evidence_level="authoritative_cross_checked",
        confidence_threshold=0.90,
        preferred_source_types=["OFFICIAL", "PRIMARY_DOCUMENT"],
        required_cross_checks=["two independent confirmations for high-impact claims"],
    )
    high_research = make_research(
        high_task,
        claim_text=claim_text,
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
        confidence=0.8,
    )
    high_hit, high_doc = make_verification(
        claim_text,
        url="https://verify.example/high",
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
    )
    high_agent = CriticAgent(FakeCriticTools(search_results={claim_text: [high_hit]}, documents={high_hit.url: high_doc}))
    high_review = CriticReview.model_validate(high_agent.run(make_request(high_agent, high_profile, high_research)).payload)

    assert low_review.decision == ReviewDecision.PASS
    assert high_review.decision == ReviewDecision.REVISE


def test_independent_contradiction_forces_revise() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "GNSS monitoring requires a stable reference frame."
    profile = make_profile(
        task_id,
        domains=["geodesy"],
        risk=RiskLevel.LOW,
        minimum_evidence_level="credible",
        confidence_threshold=0.75,
        preferred_source_types=["OFFICIAL", "REFERENCE"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.OFFICIAL,
        reliability=ReliabilityClass.A,
    )
    url = "https://verify.example/conflict"
    hit, document = make_verification(
        claim_text,
        url=url,
        source_type=SourceType.OFFICIAL,
        reliability=ReliabilityClass.A,
        content=f"{claim_text} This claim is incorrect according to the independent evidence.",
    )
    agent = CriticAgent(FakeCriticTools(search_results={claim_text: [hit]}, documents={url: document}))

    review = CriticReview.model_validate(agent.run(make_request(agent, profile, research)).payload)

    assert review.decision == ReviewDecision.REVISE
    assert review.contradictions
    assert research.claims[0].claim_id in review.unresolved_claim_ids


def test_special_profile_requirement_can_create_missing_topic() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "GNSS monitoring requires a stable reference frame."
    profile = make_profile(
        task_id,
        domains=["geodesy"],
        risk=RiskLevel.LOW,
        minimum_evidence_level="credible",
        confidence_threshold=0.75,
        preferred_source_types=["OFFICIAL", "ACADEMIC"],
        special_user_requirements=["atmospheric error budget"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.OFFICIAL,
        reliability=ReliabilityClass.A,
    )
    url = "https://verify.example/support"
    hit, document = make_verification(
        claim_text,
        url=url,
        source_type=SourceType.ACADEMIC,
        reliability=ReliabilityClass.B,
    )
    agent = CriticAgent(FakeCriticTools(search_results={claim_text: [hit]}, documents={url: document}))

    review = CriticReview.model_validate(agent.run(make_request(agent, profile, research)).payload)

    assert review.decision == ReviewDecision.REVISE
    assert "atmospheric error budget" in review.missing_topics


def test_search_failure_returns_partial_review_instead_of_false_pass() -> None:
    task_id = generate_id(IdPrefix.TASK)
    claim_text = "The interface is documented by an official source."
    profile = make_profile(
        task_id,
        domains=["software_engineering"],
        risk=RiskLevel.MEDIUM,
        minimum_evidence_level="authoritative",
        confidence_threshold=0.80,
        preferred_source_types=["OFFICIAL", "PRIMARY_DOCUMENT"],
    )
    research = make_research(
        task_id,
        claim_text=claim_text,
        source_type=SourceType.OFFICIAL,
        reliability=ReliabilityClass.A,
    )
    agent = CriticAgent(FakeCriticTools(search_error=RuntimeError("search unavailable")))

    result = agent.run(make_request(agent, profile, research))
    review = CriticReview.model_validate(result.payload)

    assert result.status == ExecutionStatus.PARTIAL
    assert review.decision == ReviewDecision.REVISE
    assert result.errors[0].error_code == "CRITIC_WEB_SEARCH_FAILED"


def test_research_result_task_mismatch_is_failed_contract_execution() -> None:
    profile_task = generate_id(IdPrefix.TASK)
    other_task = generate_id(IdPrefix.TASK)
    profile = make_profile(
        profile_task,
        domains=["general_research"],
        risk=RiskLevel.LOW,
        minimum_evidence_level="credible",
        confidence_threshold=0.75,
        preferred_source_types=["REFERENCE"],
    )
    research = make_research(
        other_task,
        claim_text="A claim from another task.",
        source_type=SourceType.REFERENCE,
        reliability=ReliabilityClass.C,
    )
    agent = CriticAgent(FakeCriticTools())

    result = agent.run(make_request(agent, profile, research))

    assert result.status == ExecutionStatus.FAILED
    assert result.errors[0].error_code == "INVALID_RESEARCH_RESULT"
    assert result.payload == {}
