from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from models import DomainAssessment, RiskLevel, Task

from .domain_resolver import DomainResolver


class DomainResolverProtocol(Protocol):
    """Stable resolver boundary consumed by ProfileWorkflow."""

    def resolve(self, task: Task) -> DomainAssessment:
        ...


class SemanticDomainProvider(Protocol):
    """Provider-neutral semantic classification contract."""

    def resolve(self, task: Task) -> "SemanticDomainResult | Mapping[str, Any]":
        ...


class SemanticDomainResult(BaseModel):
    """Structured semantic classification validated before hybrid merge."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    primary_domain: str = Field(min_length=1)
    secondary_domains: list[str] = Field(default_factory=list)
    task_type: str = Field(min_length=1)
    risk_level: RiskLevel
    identified_standards: list[str] = Field(default_factory=list)
    recommended_source_types: list[str] = Field(default_factory=list)
    recommended_evaluation_criteria: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


class SemanticResolutionError(RuntimeError):
    """Normalized semantic resolver failure."""


class LLMSemanticResolver:
    """Validate provider-neutral semantic output without coupling to a vendor SDK."""

    def __init__(self, provider: SemanticDomainProvider) -> None:
        self.provider = provider

    def resolve(self, task: Task) -> SemanticDomainResult:
        try:
            raw = self.provider.resolve(task)
            if isinstance(raw, SemanticDomainResult):
                return raw
            if isinstance(raw, Mapping):
                return SemanticDomainResult.model_validate(dict(raw))
            raise TypeError(f"Unsupported semantic resolver result: {type(raw).__name__}")
        except SemanticResolutionError:
            raise
        except (ValidationError, TypeError, ValueError) as exc:
            raise SemanticResolutionError(f"Invalid semantic domain result: {exc}") from exc
        except Exception as exc:
            raise SemanticResolutionError(str(exc) or "Semantic domain provider failed") from exc


@dataclass(frozen=True)
class HybridResolutionAudit:
    """Auditable merge summary kept outside the stable DomainAssessment schema."""

    task_id: str
    rule_primary_domain: str
    semantic_primary_domain: str | None
    semantic_confidence: float | None
    semantic_used: bool
    fallback_used: bool
    material_conflict: bool
    risk_floor_applied: bool
    final_primary_domain: str
    final_risk_level: RiskLevel
    notes: tuple[str, ...] = ()


class HybridResolver:
    """Merge deterministic and semantic domain classification conservatively."""

    HIGH_RISK_LEVELS = frozenset({RiskLevel.HIGH, RiskLevel.CRITICAL})

    def __init__(
        self,
        *,
        rule_resolver: DomainResolverProtocol | None = None,
        semantic_resolver: LLMSemanticResolver | None = None,
        minimum_semantic_confidence: float = 0.70,
        require_agreement_for_high_risk: bool = True,
        fallback_to_rules: bool = True,
    ) -> None:
        if not 0.0 <= minimum_semantic_confidence <= 1.0:
            raise ValueError("minimum_semantic_confidence must be between 0 and 1")
        self.rule_resolver = rule_resolver or DomainResolver()
        self.semantic_resolver = semantic_resolver
        self.minimum_semantic_confidence = minimum_semantic_confidence
        self.require_agreement_for_high_risk = require_agreement_for_high_risk
        self.fallback_to_rules = fallback_to_rules
        self._audit_by_task: dict[str, HybridResolutionAudit] = {}

    def resolve(self, task: Task) -> DomainAssessment:
        rule = self.rule_resolver.resolve(task)
        if self.semantic_resolver is None:
            self._record_audit(
                task,
                rule,
                semantic=None,
                final=rule,
                semantic_used=False,
                fallback_used=False,
                material_conflict=False,
                risk_floor_applied=False,
                notes=("Semantic resolver is not configured; deterministic resolution used.",),
            )
            return rule

        try:
            semantic = self.semantic_resolver.resolve(task)
        except SemanticResolutionError as exc:
            if not self.fallback_to_rules:
                raise
            final = self._fallback(rule, f"Semantic resolution failed; deterministic fallback used: {exc}")
            self._record_audit(
                task,
                rule,
                semantic=None,
                final=final,
                semantic_used=False,
                fallback_used=True,
                material_conflict=False,
                risk_floor_applied=False,
                notes=(str(exc),),
            )
            return final

        if semantic.confidence < self.minimum_semantic_confidence:
            message = (
                "Semantic confidence below configured threshold; deterministic fallback used "
                f"({semantic.confidence:.3f} < {self.minimum_semantic_confidence:.3f})."
            )
            if not self.fallback_to_rules:
                raise SemanticResolutionError(message)
            final = self._fallback(rule, message)
            self._record_audit(
                task,
                rule,
                semantic=semantic,
                final=final,
                semantic_used=False,
                fallback_used=True,
                material_conflict=False,
                risk_floor_applied=False,
                notes=(message,),
            )
            return final

        final, material_conflict, risk_floor_applied, notes = self._merge(task, rule, semantic)
        self._record_audit(
            task,
            rule,
            semantic=semantic,
            final=final,
            semantic_used=True,
            fallback_used=False,
            material_conflict=material_conflict,
            risk_floor_applied=risk_floor_applied,
            notes=tuple(notes),
        )
        return final

    def get_audit(self, task_id: str) -> HybridResolutionAudit:
        try:
            return self._audit_by_task[task_id]
        except KeyError as exc:
            raise KeyError(f"No HybridResolver audit record for task: {task_id}") from exc

    def _merge(
        self,
        task: Task,
        rule: DomainAssessment,
        semantic: SemanticDomainResult,
    ) -> tuple[DomainAssessment, bool, bool, list[str]]:
        rule_specific = rule.primary_domain != "general_research"
        rule_domains = [rule.primary_domain, *rule.secondary_domains]
        semantic_domains = [semantic.primary_domain, *semantic.secondary_domains]
        overlap = bool(set(rule_domains) & set(semantic_domains))
        material_conflict = rule_specific and not overlap

        if rule_specific:
            primary_domain = rule.primary_domain
            secondary_domains = self._dedupe(
                [*rule.secondary_domains, semantic.primary_domain, *semantic.secondary_domains]
            )
        else:
            primary_domain = semantic.primary_domain
            secondary_domains = self._dedupe(
                [*semantic.secondary_domains, *rule.secondary_domains]
            )
        secondary_domains = [
            item
            for item in secondary_domains
            if item not in {primary_domain, "general_research"}
        ]

        semantic_rank = self._risk_rank(semantic.risk_level)
        rule_rank = self._risk_rank(rule.risk_level)
        if rule_specific:
            final_risk = rule.risk_level if rule_rank >= semantic_rank else semantic.risk_level
        else:
            final_risk = semantic.risk_level
        risk_floor_applied = rule_specific and rule_rank > semantic_rank

        if task.task_type.casefold() in DomainResolver.GENERIC_TASK_TYPES:
            task_type = semantic.task_type
        else:
            task_type = rule.task_type

        uncertainties = self._dedupe([*rule.uncertainties, *semantic.uncertainties])
        notes: list[str] = []
        if material_conflict:
            message = (
                "Material domain disagreement between deterministic and semantic resolution: "
                f"rules={rule.primary_domain}; semantic={semantic.primary_domain}."
            )
            uncertainties.append(message)
            notes.append(message)
        if risk_floor_applied:
            message = (
                "Deterministic risk floor preserved: "
                f"rules={rule.risk_level.value}; semantic={semantic.risk_level.value}."
            )
            uncertainties.append(message)
            notes.append(message)
        if (
            self.require_agreement_for_high_risk
            and rule_specific
            and rule.risk_level in self.HIGH_RISK_LEVELS
            and semantic.primary_domain != rule.primary_domain
        ):
            message = (
                "High-risk resolver agreement requirement not met; user review is required at the "
                "existing CriticProfile approval boundary."
            )
            uncertainties.append(message)
            notes.append(message)

        final = DomainAssessment(
            task_id=task.task_id,
            primary_domain=primary_domain,
            secondary_domains=secondary_domains,
            task_type=task_type,
            risk_level=final_risk,
            identified_standards=self._dedupe(
                [*rule.identified_standards, *semantic.identified_standards]
            ),
            recommended_source_types=self._dedupe(
                [*rule.recommended_source_types, *semantic.recommended_source_types]
            ),
            recommended_evaluation_criteria=self._dedupe(
                [
                    *rule.recommended_evaluation_criteria,
                    *semantic.recommended_evaluation_criteria,
                ]
            ),
            uncertainties=self._dedupe(uncertainties),
        )
        return final, material_conflict, risk_floor_applied, notes

    @staticmethod
    def _fallback(rule: DomainAssessment, message: str) -> DomainAssessment:
        values = rule.model_dump(exclude={"assessment_id", "created_at"})
        values["uncertainties"] = list(dict.fromkeys([*rule.uncertainties, message]))
        return DomainAssessment(**values)

    def _record_audit(
        self,
        task: Task,
        rule: DomainAssessment,
        *,
        semantic: SemanticDomainResult | None,
        final: DomainAssessment,
        semantic_used: bool,
        fallback_used: bool,
        material_conflict: bool,
        risk_floor_applied: bool,
        notes: tuple[str, ...],
    ) -> None:
        self._audit_by_task[task.task_id] = HybridResolutionAudit(
            task_id=task.task_id,
            rule_primary_domain=rule.primary_domain,
            semantic_primary_domain=semantic.primary_domain if semantic else None,
            semantic_confidence=semantic.confidence if semantic else None,
            semantic_used=semantic_used,
            fallback_used=fallback_used,
            material_conflict=material_conflict,
            risk_floor_applied=risk_floor_applied,
            final_primary_domain=final.primary_domain,
            final_risk_level=final.risk_level,
            notes=notes,
        )

    @staticmethod
    def _risk_rank(level: RiskLevel) -> int:
        return {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }[level]

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        return list(dict.fromkeys(item for item in values if str(item).strip()))
