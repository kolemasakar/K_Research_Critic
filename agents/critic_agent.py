from __future__ import annotations

import re
from datetime import date
from time import perf_counter
from typing import Any

from pydantic import ValidationError

from models import (
    AgentDefinition,
    AgentResult,
    AgentRunRequest,
    AgentType,
    Claim,
    CriticReview,
    ErrorRecord,
    ErrorType,
    ExecutionStatus,
    ImportanceLevel,
    Metrics,
    ProfileStatus,
    ReliabilityClass,
    ReviewDecision,
    RiskLevel,
    Source,
    SourceType,
    WarningRecord,
    utc_now,
)
from models.research import ResearchResult
from tools import EvidenceToolkit, FetchedDocument, ResearchTools, normalize_url

from .base import Agent


class CriticAgent(Agent):
    """Generic profile-driven reviewer with independent web verification."""

    _QUALITY = {
        ReliabilityClass.A: 1.00,
        ReliabilityClass.B: 0.85,
        ReliabilityClass.C: 0.65,
        ReliabilityClass.D: 0.35,
    }
    _IMPORTANCE_WEIGHT = {
        ImportanceLevel.LOW: 1.0,
        ImportanceLevel.MEDIUM: 2.0,
        ImportanceLevel.HIGH: 3.0,
        ImportanceLevel.CRITICAL: 4.0,
    }
    _PRIMARY_LIKE_TYPES = {
        SourceType.OFFICIAL,
        SourceType.PRIMARY_DOCUMENT,
        SourceType.STANDARD,
        SourceType.GOVERNMENT,
    }
    _STOPWORDS = {
        "about",
        "after",
        "also",
        "been",
        "being",
        "between",
        "from",
        "have",
        "into",
        "more",
        "must",
        "that",
        "their",
        "there",
        "these",
        "this",
        "those",
        "through",
        "with",
        "without",
        "для",
        "який",
        "яка",
        "яке",
        "які",
        "цей",
        "ця",
        "це",
        "цих",
        "після",
        "через",
        "може",
        "повинен",
        "повинна",
        "було",
        "бути",
        "при",
        "про",
        "від",
        "або",
        "але",
    }
    _CONTRADICTION_MARKERS = (
        "contradicts",
        "contradictory",
        "is false",
        "is incorrect",
        "incorrect claim",
        "not supported",
        "no evidence",
        "does not support",
        "cannot support",
        "не підтвердж",
        "суперечить",
        "хибн",
        "неправильн",
        "немає доказ",
    )

    def __init__(self, tools: ResearchTools, *, evidence: EvidenceToolkit | None = None) -> None:
        self.tools = tools
        self.evidence = evidence or EvidenceToolkit()
        self._definition = AgentDefinition(
            agent_type=AgentType.CRITIC,
            name="CriticAgent",
            version="1.0",
            capabilities=[
                "profile_driven_review",
                "claim_verification",
                "independent_web_research",
                "source_quality_assessment",
                "freshness_assessment",
                "contradiction_detection",
                "coverage_assessment",
                "pass_revise_decision",
            ],
            accepted_input_types=["research_result"],
            produced_output_types=["critic_review"],
            supports_profile=True,
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
        verification_sources_examined = 0

        contract_error = self._validate_request(request)
        if contract_error is not None:
            return self._failed_result(request, started_at=started_at, timer=timer, error=contract_error)

        profile = request.profile
        assert profile is not None

        try:
            research = self._parse_research_result(request)
        except (ValidationError, TypeError, ValueError) as exc:
            return self._failed_result(
                request,
                started_at=started_at,
                timer=timer,
                error=ErrorRecord(
                    error_code="INVALID_RESEARCH_RESULT",
                    error_type=ErrorType.CONTRACT_ERROR,
                    message=str(exc),
                    recoverable=False,
                    component="CriticAgent",
                    run_id=request.run_id,
                ),
            )

        source_by_id = {source.source_id: source for source in research.sources}
        weak_source_ids: list[str] = []
        unsupported_claim_ids: list[str] = []
        verified_claim_ids: list[str] = []
        unresolved_claim_ids: list[str] = []
        contradictions: list[str] = []
        critical_issues: list[str] = []
        recommended_changes: list[str] = []
        claim_scores: list[tuple[float, float]] = []

        max_verification_queries = self._positive_limit(
            request.constraints.get("max_verification_queries"), 12
        )
        max_sources_per_claim = self._positive_limit(
            request.constraints.get("max_verification_sources_per_claim"), 4
        )
        require_independent_search = self._bool_constraint(
            request.constraints.get("require_independent_search"), True
        )
        freshness_relevant = self._freshness_relevant(request, profile.risk_level)
        max_source_age_days = self._max_source_age_days(request, profile.risk_level)

        for source in research.sources:
            source_issues = self.evidence.validator.validate(source).issues
            if source_issues:
                weak_source_ids.append(source.source_id)
                warnings.append(
                    WarningRecord(
                        warning_code="SOURCE_VALIDATION_ISSUE",
                        message=f"Source {source.source_id} has structural issues: {', '.join(source_issues)}",
                        component="CriticAgent",
                        run_id=request.run_id,
                        details={"source_id": source.source_id, "issues": source_issues},
                    )
                )
            if self._is_stale(source, freshness_relevant, max_source_age_days):
                weak_source_ids.append(source.source_id)
                warnings.append(
                    WarningRecord(
                        warning_code="STALE_SOURCE_DETECTED",
                        message=f"Source {source.source_id} may be too old for the approved freshness requirement.",
                        component="CriticAgent",
                        run_id=request.run_id,
                        details={"source_id": source.source_id},
                    )
                )
            if self._is_weak_for_profile(source, profile.minimum_evidence_level):
                weak_source_ids.append(source.source_id)

        for claim in research.claims:
            linked_sources = [source_by_id[source_id] for source_id in claim.source_ids if source_id in source_by_id]
            supporting_sources = list(linked_sources)
            verification_support: list[Source] = []
            verification_contradictions: list[Source] = []

            should_verify = require_independent_search and search_calls < max_verification_queries
            if should_verify:
                query = claim.text.strip()
                try:
                    search_calls += 1
                    hits = self.tools.web_search(query, limit=max_sources_per_claim)
                    hits = self.evidence.deduplicate_hits(hits)
                except Exception as exc:
                    errors.append(
                        ErrorRecord(
                            error_code="CRITIC_WEB_SEARCH_FAILED",
                            error_type=ErrorType.TOOL_ERROR,
                            message=str(exc) or "Critic independent web_search failed",
                            recoverable=getattr(exc, "retryable", True),
                            component="CriticAgent.web_search",
                            run_id=request.run_id,
                            details={"claim_id": claim.claim_id, "query": query},
                        )
                    )
                    warnings.append(
                        WarningRecord(
                            warning_code="INDEPENDENT_VERIFICATION_INCOMPLETE",
                            message=f"Independent verification search failed for {claim.claim_id}.",
                            component="CriticAgent",
                            run_id=request.run_id,
                            details={"claim_id": claim.claim_id},
                        )
                    )
                    hits = []

                known_urls = {normalize_url(source.url) for source in linked_sources if source.url}
                for hit in hits:
                    if normalize_url(hit.url) in known_urls:
                        continue
                    try:
                        fetch_calls += 1
                        document = self.tools.web_fetch(hit.url)
                    except Exception as exc:
                        errors.append(
                            ErrorRecord(
                                error_code="CRITIC_WEB_FETCH_FAILED",
                                error_type=ErrorType.TOOL_ERROR,
                                message=str(exc) or "Critic independent web_fetch failed",
                                recoverable=getattr(exc, "retryable", True),
                                component="CriticAgent.web_fetch",
                                run_id=request.run_id,
                                details={"claim_id": claim.claim_id, "url": hit.url},
                            )
                        )
                        continue

                    verification_sources_examined += 1
                    source = self.evidence.source_from_document(request.task_id, document)
                    relation = self._evidence_relation(claim.text, document)
                    if relation == "support":
                        source.supports_claim_ids = [claim.claim_id]
                        verification_support.append(source)
                        supporting_sources.append(source)
                    elif relation == "contradiction":
                        source.contradicts_claim_ids = [claim.claim_id]
                        verification_contradictions.append(source)

                    if self._is_stale(source, freshness_relevant, max_source_age_days):
                        warnings.append(
                            WarningRecord(
                                warning_code="STALE_VERIFICATION_SOURCE",
                                message=f"Independent source for {claim.claim_id} may be stale.",
                                component="CriticAgent",
                                run_id=request.run_id,
                                details={"claim_id": claim.claim_id, "url": source.url},
                            )
                        )

            evidence_ok = self._meets_evidence_requirement(
                profile.minimum_evidence_level,
                profile.preferred_source_types,
                profile.required_cross_checks,
                supporting_sources,
            )
            if require_independent_search and not verification_support:
                evidence_ok = False

            if not linked_sources or not evidence_ok:
                unsupported_claim_ids.append(claim.claim_id)
                unresolved_claim_ids.append(claim.claim_id)
                recommended_changes.append(
                    f"Strengthen evidence for claim {claim.claim_id} to satisfy the approved CriticProfile."
                )
            elif verification_contradictions:
                unresolved_claim_ids.append(claim.claim_id)
            else:
                verified_claim_ids.append(claim.claim_id)

            if verification_contradictions:
                urls = [source.url or source.title for source in verification_contradictions]
                contradictions.append(
                    f"Independent evidence conflicts with claim {claim.claim_id}: {', '.join(urls)}"
                )
                recommended_changes.append(
                    f"Resolve contradictory evidence for claim {claim.claim_id} before acceptance."
                )
                if claim.importance == ImportanceLevel.CRITICAL or profile.risk_level == RiskLevel.CRITICAL:
                    critical_issues.append(
                        f"Critical claim {claim.claim_id} has contradictory independent evidence."
                    )

            if claim.importance in {ImportanceLevel.HIGH, ImportanceLevel.CRITICAL}:
                if not self._claim_cited_in_draft(claim, research.draft_report):
                    critical_issues.append(
                        f"Important claim {claim.claim_id} is not source-cited in the draft report."
                    )
                    recommended_changes.append(
                        f"Add explicit source citation for important claim {claim.claim_id}."
                    )

            score = self._claim_reliability_score(
                claim,
                supporting_sources,
                evidence_ok=evidence_ok,
                contradicted=bool(verification_contradictions),
            )
            claim_scores.append((score, self._IMPORTANCE_WEIGHT[claim.importance]))

        missing_topics = self._missing_topics(request, research, profile.special_user_requirements)
        for topic in missing_topics:
            recommended_changes.append(f"Address missing required topic or requirement: {topic}")

        weak_source_ids = list(dict.fromkeys(weak_source_ids))
        unsupported_claim_ids = list(dict.fromkeys(unsupported_claim_ids))
        verified_claim_ids = list(dict.fromkeys(verified_claim_ids))
        unresolved_claim_ids = list(dict.fromkeys(unresolved_claim_ids))
        contradictions = list(dict.fromkeys(contradictions))
        critical_issues = list(dict.fromkeys(critical_issues))
        recommended_changes = list(dict.fromkeys(recommended_changes))

        reliability_score = self._weighted_score(claim_scores)
        if reliability_score < profile.confidence_threshold:
            recommended_changes.append(
                f"Raise evidence reliability from {reliability_score:.2f} to the approved threshold {profile.confidence_threshold:.2f}."
            )

        blockers = bool(
            critical_issues
            or unsupported_claim_ids
            or contradictions
            or missing_topics
            or unresolved_claim_ids
            or reliability_score < profile.confidence_threshold
        )
        decision = ReviewDecision.REVISE if blockers else ReviewDecision.PASS

        review = CriticReview(
            task_id=request.task_id,
            run_id=request.run_id,
            profile_id=profile.profile_id,
            iteration=request.iteration,
            decision=decision,
            reliability_score=reliability_score,
            critical_issues=critical_issues,
            unsupported_claim_ids=unsupported_claim_ids,
            weak_source_ids=weak_source_ids,
            contradictions=contradictions,
            missing_topics=missing_topics,
            recommended_changes=recommended_changes,
            verified_claim_ids=verified_claim_ids,
            unresolved_claim_ids=unresolved_claim_ids,
        )

        completed_at = utc_now()
        duration_ms = max(0, int((perf_counter() - timer) * 1000))
        status = ExecutionStatus.PARTIAL if errors else ExecutionStatus.SUCCEEDED
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.CRITIC,
            status=status,
            result_type="critic_review",
            payload=review.model_dump(mode="json"),
            warnings=warnings,
            errors=errors,
            metrics=Metrics(
                duration_ms=duration_ms,
                search_calls=search_calls,
                fetch_calls=fetch_calls,
                sources_examined=len(research.sources) + verification_sources_examined,
                claims_verified=len(verified_claim_ids),
            ),
            started_at=started_at,
            completed_at=completed_at,
        )

    def _validate_request(self, request: AgentRunRequest) -> ErrorRecord | None:
        if request.agent_type != AgentType.CRITIC:
            return ErrorRecord(
                error_code="INVALID_AGENT_TYPE",
                error_type=ErrorType.CONTRACT_ERROR,
                message="CriticAgent requires agent_type CRITIC",
                recoverable=False,
                component="CriticAgent",
                run_id=request.run_id,
            )
        if request.agent_id != self.definition.agent_id:
            return ErrorRecord(
                error_code="AGENT_ID_MISMATCH",
                error_type=ErrorType.CONTRACT_ERROR,
                message="AgentRunRequest agent_id does not match CriticAgent definition",
                recoverable=False,
                component="CriticAgent",
                run_id=request.run_id,
            )
        if request.profile is None or request.profile.status != ProfileStatus.APPROVED:
            return ErrorRecord(
                error_code="CRITIC_PROFILE_NOT_APPROVED",
                error_type=ErrorType.CONTRACT_ERROR,
                message="CriticAgent requires the approved CriticProfile for this task",
                recoverable=False,
                component="CriticAgent",
                run_id=request.run_id,
            )
        if request.profile.task_id != request.task_id:
            return ErrorRecord(
                error_code="CRITIC_PROFILE_TASK_MISMATCH",
                error_type=ErrorType.CONTRACT_ERROR,
                message="CriticProfile task_id must match AgentRunRequest task_id",
                recoverable=False,
                component="CriticAgent",
                run_id=request.run_id,
            )
        return None

    @staticmethod
    def _parse_research_result(request: AgentRunRequest) -> ResearchResult:
        raw = request.input.get("research_result")
        if raw is None:
            raise ValueError("CriticAgent input requires research_result")
        research = raw if isinstance(raw, ResearchResult) else ResearchResult.model_validate(raw)
        if research.task_id != request.task_id:
            raise ValueError("ResearchResult task_id must match CriticAgent request task_id")
        if research.iteration != request.iteration:
            raise ValueError("ResearchResult iteration must match CriticAgent request iteration")
        return research

    @classmethod
    def _meets_evidence_requirement(
        cls,
        minimum_evidence_level: str,
        preferred_source_types: list[str],
        required_cross_checks: list[str],
        sources: list[Source],
    ) -> bool:
        if not sources:
            return False

        minimum = minimum_evidence_level.casefold()
        if "primary_or_authoritative_cross_checked" in minimum:
            allowed = {ReliabilityClass.A, ReliabilityClass.B}
            required_groups = 2
            requires_primary_like = True
        elif "authoritative_cross_checked" in minimum:
            allowed = {ReliabilityClass.A, ReliabilityClass.B}
            required_groups = 2
            requires_primary_like = False
        elif "authoritative" in minimum:
            allowed = {ReliabilityClass.A, ReliabilityClass.B}
            required_groups = 1
            requires_primary_like = False
        else:
            allowed = {ReliabilityClass.A, ReliabilityClass.B, ReliabilityClass.C}
            required_groups = 1
            requires_primary_like = False

        cross_text = " ".join(required_cross_checks).casefold()
        if "two independent" in cross_text or "independent confirmation" in cross_text:
            required_groups = max(required_groups, 2)

        acceptable = [source for source in sources if source.reliability_class in allowed]
        if not acceptable:
            return False

        groups = {cls._independence_key(source) for source in acceptable}
        if len(groups) < required_groups:
            return False

        if requires_primary_like and not any(
            source.primary_source or source.source_type in cls._PRIMARY_LIKE_TYPES
            for source in acceptable
        ):
            return False

        preferred = {value.upper() for value in preferred_source_types}
        if preferred and not any(source.source_type.value.upper() in preferred for source in acceptable):
            return False
        return True

    @classmethod
    def _claim_reliability_score(
        cls,
        claim: Claim,
        sources: list[Source],
        *,
        evidence_ok: bool,
        contradicted: bool,
    ) -> float:
        if not sources:
            return 0.0
        best = max(cls._QUALITY[source.reliability_class] for source in sources)
        groups = len({cls._independence_key(source) for source in sources})
        source_score = min(1.0, best + (0.05 if groups >= 2 else 0.0))
        score = (source_score + claim.confidence) / 2.0
        if not evidence_ok:
            score = min(score, 0.69)
        if contradicted:
            score = min(score * 0.4, 0.40)
        return round(max(0.0, min(1.0, score)), 4)

    @staticmethod
    def _weighted_score(scores: list[tuple[float, float]]) -> float:
        if not scores:
            return 0.0
        total_weight = sum(weight for _, weight in scores)
        if total_weight <= 0:
            return 0.0
        value = sum(score * weight for score, weight in scores) / total_weight
        return round(max(0.0, min(1.0, value)), 4)

    @classmethod
    def _independence_key(cls, source: Source) -> str:
        if source.independence_group:
            return f"group:{source.independence_group.casefold()}"
        if source.url:
            return f"url:{normalize_url(source.url)}"
        publisher = (source.publisher or source.title).casefold()
        return f"publisher:{publisher}"

    @classmethod
    def _evidence_relation(cls, claim_text: str, document: FetchedDocument) -> str:
        evidence_text = " ".join(
            part for part in (document.title, document.snippet or "", document.content or "") if part
        )
        claim_tokens = cls._tokens(claim_text)
        evidence_tokens = cls._tokens(evidence_text)
        if not claim_tokens or not evidence_tokens:
            return "unrelated"
        overlap = len(claim_tokens & evidence_tokens) / max(1, len(claim_tokens))
        if overlap < 0.35:
            return "unrelated"
        lowered = evidence_text.casefold()
        if any(marker in lowered for marker in cls._CONTRADICTION_MARKERS):
            return "contradiction"
        return "support"

    @classmethod
    def _tokens(cls, text: str) -> set[str]:
        return {
            token.casefold()
            for token in re.findall(r"[\w-]+", text, flags=re.UNICODE)
            if len(token) >= 4 and token.casefold() not in cls._STOPWORDS
        }

    @classmethod
    def _topic_covered(cls, topic: str, corpus: str) -> bool:
        topic_tokens = cls._tokens(topic)
        if not topic_tokens:
            return True
        corpus_tokens = cls._tokens(corpus)
        overlap = len(topic_tokens & corpus_tokens) / len(topic_tokens)
        return overlap >= 0.35

    @classmethod
    def _missing_topics(
        cls,
        request: AgentRunRequest,
        research: ResearchResult,
        special_requirements: list[str],
    ) -> list[str]:
        required = [str(item).strip() for item in request.input.get("required_topics", []) if str(item).strip()]
        required.extend(str(item).strip() for item in special_requirements if str(item).strip())
        required = list(dict.fromkeys(required))
        corpus = " ".join(
            [research.summary, *research.findings, research.draft_report, *research.uncertainties]
        )
        return [topic for topic in required if not cls._topic_covered(topic, corpus)]

    @staticmethod
    def _claim_cited_in_draft(claim: Claim, draft_report: str) -> bool:
        return any(f"[{source_id}]" in draft_report for source_id in claim.source_ids)

    @staticmethod
    def _is_weak_for_profile(source: Source, minimum_evidence_level: str) -> bool:
        minimum = minimum_evidence_level.casefold()
        if "authoritative" in minimum or "primary_or_authoritative" in minimum:
            return source.reliability_class not in {ReliabilityClass.A, ReliabilityClass.B}
        return source.reliability_class == ReliabilityClass.D

    @staticmethod
    def _freshness_relevant(request: AgentRunRequest, risk_level: RiskLevel) -> bool:
        explicit = request.context.get("freshness_relevant")
        if explicit is not None:
            return bool(explicit)
        explicit = request.input.get("freshness_relevant")
        if explicit is not None:
            return bool(explicit)
        return risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    @staticmethod
    def _max_source_age_days(request: AgentRunRequest, risk_level: RiskLevel) -> int:
        raw = request.constraints.get("max_source_age_days")
        try:
            if raw is not None and int(raw) > 0:
                return int(raw)
        except (TypeError, ValueError):
            pass
        return {
            RiskLevel.LOW: 3650,
            RiskLevel.MEDIUM: 1825,
            RiskLevel.HIGH: 730,
            RiskLevel.CRITICAL: 365,
        }[risk_level]

    @staticmethod
    def _is_stale(source: Source, freshness_relevant: bool, max_age_days: int) -> bool:
        if not freshness_relevant or source.publication_date is None:
            return False
        age = date.today() - source.publication_date
        return age.days > max_age_days

    @staticmethod
    def _positive_limit(value: Any, default: int) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return default
        return parsed if parsed > 0 else default

    @staticmethod
    def _bool_constraint(value: Any, default: bool) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().casefold()
            if lowered in {"true", "1", "yes", "on"}:
                return True
            if lowered in {"false", "0", "no", "off"}:
                return False
        return bool(value)

    @staticmethod
    def _failed_result(
        request: AgentRunRequest,
        *,
        started_at,
        timer: float,
        error: ErrorRecord,
    ) -> AgentResult:
        completed_at = utc_now()
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=request.agent_type,
            status=ExecutionStatus.FAILED,
            result_type="critic_review",
            payload={},
            errors=[error],
            metrics=Metrics(duration_ms=max(0, int((perf_counter() - timer) * 1000))),
            started_at=started_at,
            completed_at=completed_at,
        )
