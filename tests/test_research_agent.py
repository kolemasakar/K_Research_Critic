from __future__ import annotations

import pytest
from pydantic import ValidationError

from agents import ResearchAgent
from models import (
    AgentRunRequest,
    AgentType,
    Claim,
    ClaimType,
    ExecutionStatus,
    IdPrefix,
    ImportanceLevel,
    ReliabilityClass,
    ResearchResult,
    SourceType,
    VerificationStatus,
    generate_id,
)
from tools import FetchedDocument, SearchHit


class FakeResearchTools:
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


def make_request(agent: ResearchAgent, *, input_data=None, constraints=None, iteration=1) -> AgentRunRequest:
    return AgentRunRequest(
        task_id=generate_id(IdPrefix.TASK),
        workflow_run_id=generate_id(IdPrefix.WORKFLOW),
        agent_id=agent.definition.agent_id,
        agent_type=AgentType.RESEARCH,
        iteration=iteration,
        input=input_data or {"topic": "GNSS deformation monitoring"},
        constraints=constraints or {},
    )


def make_hit(url: str, title: str = "Official GNSS Guide") -> SearchHit:
    return SearchHit(
        url=url,
        title=title,
        publisher="Example Authority",
        snippet="GNSS monitoring requires a stable reference frame.",
        source_type=SourceType.OFFICIAL,
        reliability_class=ReliabilityClass.A,
        primary_source=True,
    )


def make_document(url: str, title: str = "Official GNSS Guide") -> FetchedDocument:
    return FetchedDocument(
        url=url,
        title=title,
        publisher="Example Authority",
        snippet="GNSS monitoring requires a stable reference frame.",
        content="GNSS deformation monitoring requires a stable reference frame. Network geometry also affects uncertainty.",
        source_type=SourceType.OFFICIAL,
        reliability_class=ReliabilityClass.A,
        primary_source=True,
    )


def test_research_agent_returns_structured_evidence_and_draft() -> None:
    url = "https://example.test/gnss"
    tools = FakeResearchTools(
        search_results={"GNSS deformation monitoring": [make_hit(url)]},
        documents={url: make_document(url)},
    )
    agent = ResearchAgent(tools)
    request = make_request(agent)

    result = agent.run(request)

    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.agent_id == agent.definition.agent_id
    assert result.run_id == request.run_id
    research = ResearchResult.model_validate(result.payload)
    assert research.task_id == request.task_id
    assert research.iteration == 1
    assert len(research.sources) == 1
    assert len(research.claims) == 1
    assert research.claims[0].source_ids == [research.sources[0].source_id]
    assert research.sources[0].supports_claim_ids == [research.claims[0].claim_id]
    assert "# Draft Research" in research.draft_report
    assert result.metrics.search_calls == 1
    assert result.metrics.fetch_calls == 1


def test_research_agent_deduplicates_urls_and_respects_source_limit() -> None:
    first = "https://example.test/a"
    second = "https://example.test/b"
    tools = FakeResearchTools(
        search_results={
            "q1": [make_hit(first, "A"), make_hit(first, "A duplicate"), make_hit(second, "B")]
        },
        documents={first: make_document(first, "A"), second: make_document(second, "B")},
    )
    agent = ResearchAgent(tools)
    request = make_request(
        agent,
        input_data={"topic": "test", "search_queries": ["q1"]},
        constraints={"max_sources": 1, "max_sources_per_query": 8},
    )

    result = agent.run(request)
    research = ResearchResult.model_validate(result.payload)

    assert result.status == ExecutionStatus.SUCCEEDED
    assert len(research.sources) == 1
    assert tools.fetch_calls == [first]


def test_revision_feedback_expands_plan_and_records_actions() -> None:
    topic = "GNSS monitoring"
    query1 = topic
    query2 = f"{topic} verify reference frame"
    query3 = f"{topic} atmospheric error budget"
    urls = ["https://example.test/1", "https://example.test/2", "https://example.test/3"]
    tools = FakeResearchTools(
        search_results={
            query1: [make_hit(urls[0])],
            query2: [make_hit(urls[1])],
            query3: [make_hit(urls[2])],
        },
        documents={url: make_document(url) for url in urls},
    )
    agent = ResearchAgent(tools)
    request = make_request(
        agent,
        iteration=2,
        input_data={
            "topic": topic,
            "previous_review": {
                "recommended_changes": ["verify reference frame"],
                "missing_topics": ["atmospheric error budget"],
            },
        },
    )

    result = agent.run(request)
    research = ResearchResult.model_validate(result.payload)

    assert research.iteration == 2
    assert research.search_queries == [query1, query2, query3]
    assert len(research.changes_applied) == 2
    assert all("Research plan targeted critic feedback" in item for item in research.changes_applied)


def test_partial_fetch_failure_preserves_useful_evidence() -> None:
    good = "https://example.test/good"
    bad = "https://example.test/bad"
    tools = FakeResearchTools(
        search_results={"GNSS deformation monitoring": [make_hit(good), make_hit(bad)]},
        documents={good: make_document(good)},
        fetch_errors={bad},
    )
    agent = ResearchAgent(tools)
    request = make_request(agent)

    result = agent.run(request)
    research = ResearchResult.model_validate(result.payload)

    assert result.status == ExecutionStatus.PARTIAL
    assert len(research.sources) == 1
    assert len(research.claims) == 1
    assert result.errors[0].error_code == "WEB_FETCH_FAILED"
    assert any(item.warning_code == "PARTIAL_TOOL_FAILURE" for item in result.warnings)


def test_no_search_results_returns_partial_result_not_false_success() -> None:
    tools = FakeResearchTools(search_results={"GNSS deformation monitoring": []})
    agent = ResearchAgent(tools)
    request = make_request(agent)

    result = agent.run(request)
    research = ResearchResult.model_validate(result.payload)

    assert result.status == ExecutionStatus.PARTIAL
    assert research.sources == []
    assert research.claims == []
    assert any(item.warning_code == "NO_SEARCH_RESULTS" for item in result.warnings)


def test_all_search_failures_return_failed_agent_result() -> None:
    tools = FakeResearchTools(search_error=RuntimeError("search unavailable"))
    agent = ResearchAgent(tools)
    request = make_request(agent)

    result = agent.run(request)

    assert result.status == ExecutionStatus.FAILED
    assert result.payload == {}
    assert result.errors[0].error_code == "WEB_SEARCH_FAILED"


def test_agent_id_mismatch_is_rejected_without_tool_calls() -> None:
    tools = FakeResearchTools()
    agent = ResearchAgent(tools)
    request = AgentRunRequest(
        task_id=generate_id(IdPrefix.TASK),
        workflow_run_id=generate_id(IdPrefix.WORKFLOW),
        agent_id=generate_id(IdPrefix.AGENT),
        agent_type=AgentType.RESEARCH,
        input={"topic": "GNSS"},
    )

    result = agent.run(request)

    assert result.status == ExecutionStatus.FAILED
    assert result.errors[0].error_code == "AGENT_ID_MISMATCH"
    assert tools.search_calls == []


def test_research_result_rejects_claim_with_unknown_source_reference() -> None:
    task_id = generate_id(IdPrefix.TASK)
    run_id = generate_id(IdPrefix.RUN)
    claim = Claim(
        task_id=task_id,
        text="Unsupported link",
        claim_type=ClaimType.FACT,
        importance=ImportanceLevel.MEDIUM,
        source_ids=[generate_id(IdPrefix.SOURCE)],
        confidence=0.5,
        verification_status=VerificationStatus.UNVERIFIED,
        created_by_run_id=run_id,
    )

    with pytest.raises(ValidationError):
        ResearchResult(
            task_id=task_id,
            run_id=run_id,
            iteration=1,
            summary="Summary",
            claims=[claim],
            sources=[],
            draft_report="Draft",
        )
