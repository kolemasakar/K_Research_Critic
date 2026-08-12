from __future__ import annotations

from time import perf_counter
from typing import Any

from models import (
    AgentDefinition,
    AgentResult,
    AgentRunRequest,
    AgentType,
    Claim,
    ClaimType,
    ErrorRecord,
    ErrorType,
    ExecutionStatus,
    ImportanceLevel,
    Metrics,
    Source,
    VerificationStatus,
    WarningRecord,
    utc_now,
)
from models.research import ResearchResult
from tools import EvidenceToolkit, FetchedDocument, ResearchTools, SearchHit

from .base import Agent


class ResearchAgent(Agent):
    """Generic evidence-oriented ResearchAgent with injected provider-neutral tools."""

    def __init__(self, tools: ResearchTools, *, evidence: EvidenceToolkit | None = None) -> None:
        self.tools = tools
        self.evidence = evidence or EvidenceToolkit()
        self._definition = AgentDefinition(
            agent_type=AgentType.RESEARCH,
            name="ResearchAgent",
            version="1.1",
            capabilities=[
                "research_planning",
                "web_research",
                "source_collection",
                "source_normalization",
                "claim_extraction",
                "citation_management",
                "draft_generation",
                "revision_feedback",
            ],
            accepted_input_types=["research_task"],
            produced_output_types=["research_result"],
        )

    @property
    def definition(self) -> AgentDefinition:
        return self._definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        started_at = utc_now()
        timer = perf_counter()
        errors: list[ErrorRecord] = []
        warnings: list[WarningRecord] = []
        search_calls = 0
        fetch_calls = 0

        contract_error = self._validate_request(request)
        if contract_error is not None:
            return self._failed_result(
                request,
                started_at=started_at,
                timer=timer,
                error=contract_error,
            )

        topic = str(request.input.get("topic") or request.input.get("user_request") or "").strip()
        queries, changes_applied = self._build_queries(request, topic)
        max_queries = self._positive_limit(request.constraints.get("max_queries"), 12)
        max_sources = self._positive_limit(request.constraints.get("max_sources"), 30)
        max_sources_per_query = self._positive_limit(
            request.constraints.get("max_sources_per_query"), 8
        )
        queries = queries[:max_queries]

        hits: list[SearchHit] = []
        search_failures = 0
        for query in queries:
            try:
                search_calls += 1
                query_hits = self.tools.web_search(query, limit=max_sources_per_query)
            except Exception as exc:
                search_failures += 1
                errors.append(
                    ErrorRecord(
                        error_code="WEB_SEARCH_FAILED",
                        error_type=ErrorType.TOOL_ERROR,
                        message=str(exc) or "web_search failed",
                        recoverable=getattr(exc, "retryable", True),
                        component="web_search",
                        run_id=request.run_id,
                        details={
                            "query": query,
                            "tool_code": getattr(exc, "code", None),
                        },
                    )
                )
                continue
            hits.extend(query_hits)
            hits = self.evidence.deduplicate_hits(hits)[:max_sources]
            if len(hits) >= max_sources:
                break

        if queries and search_failures == len(queries):
            primary_error = errors[0] if errors else ErrorRecord(
                error_code="WEB_SEARCH_FAILED",
                error_type=ErrorType.TOOL_ERROR,
                message="All web_search calls failed",
                recoverable=True,
                component="web_search",
                run_id=request.run_id,
            )
            return self._failed_result(
                request,
                started_at=started_at,
                timer=timer,
                error=primary_error,
                metrics=Metrics(search_calls=search_calls, fetch_calls=fetch_calls),
            )

        documents: list[FetchedDocument] = []
        for hit in hits:
            try:
                fetch_calls += 1
                document = self.tools.web_fetch(hit.url)
                documents.append(document)
            except Exception as exc:
                errors.append(
                    ErrorRecord(
                        error_code="WEB_FETCH_FAILED",
                        error_type=ErrorType.TOOL_ERROR,
                        message=str(exc) or "web_fetch failed",
                        recoverable=getattr(exc, "retryable", True),
                        component="web_fetch",
                        run_id=request.run_id,
                        details={
                            "url": hit.url,
                            "title": hit.title,
                            "tool_code": getattr(exc, "code", None),
                        },
                    )
                )
                warnings.append(
                    WarningRecord(
                        warning_code="PARTIAL_TOOL_FAILURE",
                        message=f"Could not fetch source: {hit.url}",
                        component="ResearchAgent",
                        run_id=request.run_id,
                    )
                )
        documents = [item for item in self.evidence.deduplicate_hits(documents)]

        overrides = request.constraints.get("source_reliability_overrides")
        reliability_overrides = overrides if isinstance(overrides, dict) else None

        sources: list[Source] = []
        claims: list[Claim] = []
        for document in documents:
            source = self.evidence.source_from_document(
                request.task_id,
                document,
                reliability_overrides=reliability_overrides,
            )
            validation = self.evidence.validator.validate(source)
            if not validation.valid:
                warnings.append(
                    WarningRecord(
                        warning_code="SOURCE_VALIDATION_ISSUE",
                        message=f"Source {source.source_id} has validation issues: {', '.join(validation.issues)}",
                        component="source_validator",
                        run_id=request.run_id,
                        details={"source_id": source.source_id, "issues": validation.issues},
                    )
                )
            sources.append(source)

            claim_text = self._extract_claim_text(document)
            if not claim_text:
                continue
            claim = Claim(
                task_id=request.task_id,
                text=claim_text,
                claim_type=ClaimType.FACT,
                importance=ImportanceLevel.MEDIUM,
                source_ids=[],
                confidence=self.evidence.confidence_for(source.reliability_class),
                verification_status=VerificationStatus.UNVERIFIED,
                created_by_run_id=request.run_id,
            )
            self.evidence.linker.link(claim, [source])
            claims.append(claim)

        if not hits:
            warnings.append(
                WarningRecord(
                    warning_code="NO_SEARCH_RESULTS",
                    message="Research queries returned no sources.",
                    component="ResearchAgent",
                    run_id=request.run_id,
                )
            )
        elif not documents:
            warnings.append(
                WarningRecord(
                    warning_code="NO_FETCHED_SOURCES",
                    message="Search results were found but no source could be fetched.",
                    component="ResearchAgent",
                    run_id=request.run_id,
                )
            )
        elif not claims:
            warnings.append(
                WarningRecord(
                    warning_code="NO_EXTRACTABLE_CLAIMS",
                    message="Fetched sources contained no extractable text for the baseline MVP extractor.",
                    component="ResearchAgent",
                    run_id=request.run_id,
                )
            )

        findings = [claim.text for claim in claims]
        uncertainties = self._build_uncertainties(request, warnings)
        limitations = list(dict.fromkeys(warning.message for warning in warnings))
        summary = self._build_summary(topic, findings)
        draft_report = self._build_draft(
            topic=topic,
            summary=summary,
            claims=claims,
            sources=sources,
            uncertainties=uncertainties,
        )
        research_result = ResearchResult(
            task_id=request.task_id,
            run_id=request.run_id,
            iteration=request.iteration,
            summary=summary,
            findings=findings,
            claims=claims,
            sources=sources,
            uncertainties=uncertainties,
            limitations=limitations,
            draft_report=draft_report,
            changes_applied=changes_applied,
            search_queries=queries,
        )

        status = ExecutionStatus.SUCCEEDED
        if errors or warnings or not claims:
            status = ExecutionStatus.PARTIAL

        completed_at = utc_now()
        duration_ms = max(0, int((perf_counter() - timer) * 1000))
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.RESEARCH,
            status=status,
            result_type="research_result",
            payload=research_result.model_dump(mode="json"),
            warnings=warnings,
            errors=errors,
            metrics=Metrics(
                duration_ms=duration_ms,
                search_calls=search_calls,
                fetch_calls=fetch_calls,
                sources_examined=len(sources),
                claims_created=len(claims),
            ),
            started_at=started_at,
            completed_at=completed_at,
        )

    def _validate_request(self, request: AgentRunRequest) -> ErrorRecord | None:
        if request.agent_type != AgentType.RESEARCH:
            return ErrorRecord(
                error_code="INVALID_AGENT_TYPE",
                error_type=ErrorType.CONTRACT_ERROR,
                message="ResearchAgent requires agent_type RESEARCH",
                recoverable=False,
                component="ResearchAgent",
                run_id=request.run_id,
            )
        if request.agent_id != self.definition.agent_id:
            return ErrorRecord(
                error_code="AGENT_ID_MISMATCH",
                error_type=ErrorType.CONTRACT_ERROR,
                message="AgentRunRequest agent_id does not match ResearchAgent definition",
                recoverable=False,
                component="ResearchAgent",
                run_id=request.run_id,
            )
        topic = str(request.input.get("topic") or request.input.get("user_request") or "").strip()
        if not topic:
            return ErrorRecord(
                error_code="MISSING_RESEARCH_TOPIC",
                error_type=ErrorType.CONTRACT_ERROR,
                message="ResearchAgent input requires topic or user_request",
                recoverable=False,
                component="ResearchAgent",
                run_id=request.run_id,
            )
        return None

    @staticmethod
    def _build_queries(request: AgentRunRequest, topic: str) -> tuple[list[str], list[str]]:
        explicit = request.input.get("search_queries") or []
        questions = request.input.get("research_questions") or []
        requirements = request.input.get("requirements") or []
        previous_review = request.input.get("previous_review") or {}

        queries: list[str] = [str(item).strip() for item in explicit if str(item).strip()]
        if not queries:
            queries.append(topic)
            queries.extend(f"{topic} {item}" for item in questions if str(item).strip())
            queries.extend(f"{topic} {item}" for item in requirements if str(item).strip())

        feedback: list[str] = []
        if isinstance(previous_review, dict):
            for key in ("recommended_changes", "missing_topics"):
                values = previous_review.get(key) or []
                feedback.extend(str(item).strip() for item in values if str(item).strip())
        queries.extend(f"{topic} {item}" for item in feedback)
        changes_applied = [f"Research plan targeted critic feedback: {item}" for item in feedback]
        return list(dict.fromkeys(queries)), changes_applied

    @staticmethod
    def _extract_claim_text(document: FetchedDocument) -> str:
        candidate = (document.content or document.snippet or "").strip()
        if not candidate:
            return ""
        normalized = " ".join(candidate.split())
        for separator in (". ", "? ", "! "):
            if separator in normalized:
                head = normalized.split(separator, 1)[0].strip()
                if head:
                    return head + separator.strip()
        return normalized[:1200]

    @staticmethod
    def _build_uncertainties(
        request: AgentRunRequest, warnings: list[WarningRecord]
    ) -> list[str]:
        uncertainties = [str(item) for item in (request.input.get("uncertainties") or [])]
        uncertainties.extend(warning.message for warning in warnings)
        return list(dict.fromkeys(item for item in uncertainties if item.strip()))

    @staticmethod
    def _build_summary(topic: str, findings: list[str]) -> str:
        if not findings:
            return f"Research for '{topic}' produced no extractable claims."
        return " ".join(findings[:3])

    def _build_draft(
        self,
        *,
        topic: str,
        summary: str,
        claims: list[Claim],
        sources: list[Source],
        uncertainties: list[str],
    ) -> str:
        lines = ["# Draft Research", "", f"Topic: {topic}", "", "## Summary", "", summary]
        lines.extend(["", "## Findings", ""])
        source_map = {source.source_id: source for source in sources}
        if claims:
            for claim in claims:
                citation = self.evidence.citations.cite_claim(claim, source_map)
                lines.append(f"- {claim.text} {citation}".rstrip())
        else:
            lines.append("- No evidence-backed findings were produced.")
        lines.extend(["", "## Sources", ""])
        bibliography = self.evidence.citations.bibliography(sources)
        lines.append(bibliography or "- No sources collected.")
        if uncertainties:
            lines.extend(["", "## Uncertainties", ""])
            lines.extend(f"- {item}" for item in uncertainties)
        return "\n".join(lines)

    @staticmethod
    def _positive_limit(value: Any, default: int) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return default
        return parsed if parsed > 0 else default

    @staticmethod
    def _failed_result(
        request: AgentRunRequest,
        *,
        started_at,
        timer: float,
        error: ErrorRecord,
        metrics: Metrics | None = None,
    ) -> AgentResult:
        completed_at = utc_now()
        base_metrics = metrics or Metrics()
        if base_metrics.duration_ms is None:
            base_metrics.duration_ms = max(0, int((perf_counter() - timer) * 1000))
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=request.agent_type,
            status=ExecutionStatus.FAILED,
            result_type="research_result",
            payload={},
            errors=[error],
            metrics=base_metrics,
            started_at=started_at,
            completed_at=completed_at,
        )
