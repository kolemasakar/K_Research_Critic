import pytest

from models import DomainAssessment, ProfileStatus, RiskLevel, TaskStatus
from supervisor import (
    HybridResolver,
    LLMSemanticResolver,
    ProfileWorkflow,
    RuleBasedResolver,
    SemanticDomainResult,
    SemanticResolutionError,
    TaskManager,
    WorkflowEngine,
)


class StaticSemanticProvider:
    def __init__(self, result):
        self.result = result

    def resolve(self, task):
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def semantic_result(
    *,
    primary_domain: str,
    secondary_domains: list[str] | None = None,
    task_type: str = "research",
    risk_level: RiskLevel = RiskLevel.MEDIUM,
    confidence: float = 0.90,
    source_types: list[str] | None = None,
) -> SemanticDomainResult:
    return SemanticDomainResult(
        primary_domain=primary_domain,
        secondary_domains=list(secondary_domains or []),
        task_type=task_type,
        risk_level=risk_level,
        identified_standards=["semantic task-relevant standards"],
        recommended_source_types=list(source_types or ["ACADEMIC"]),
        recommended_evaluation_criteria=["semantic evidence consistency"],
        uncertainties=[],
        confidence=confidence,
    )


def make_task(user_request: str, *, task_type: str = "auto"):
    manager = TaskManager()
    return manager.create_task(user_request=user_request, task_type=task_type)


def make_hybrid(result, **kwargs) -> HybridResolver:
    return HybridResolver(
        semantic_resolver=LLMSemanticResolver(StaticSemanticProvider(result)),
        **kwargs,
    )


def test_rule_and_semantic_agreement_merges_evidence_requirements() -> None:
    task = make_task("Assess GNSS RTK coordinate accuracy for geodetic surveying")
    resolver = make_hybrid(
        semantic_result(
            primary_domain="geodesy",
            task_type="technical_assessment",
            risk_level=RiskLevel.HIGH,
            source_types=["ACADEMIC", "STANDARD"],
        )
    )

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "geodesy"
    assert assessment.task_type == "technical_assessment"
    assert assessment.risk_level == RiskLevel.HIGH
    assert "STANDARD" in assessment.recommended_source_types
    assert "ACADEMIC" in assessment.recommended_source_types
    audit = resolver.get_audit(task.task_id)
    assert audit.semantic_used is True
    assert audit.material_conflict is False


def test_compatible_multi_domain_merge_preserves_rule_primary_and_adds_semantic_domains() -> None:
    task = make_task("Assess structural building deformation monitoring with GNSS RTK coordinates")
    resolver = make_hybrid(
        semantic_result(
            primary_domain="geodesy",
            secondary_domains=["construction", "structural_monitoring"],
            task_type="engineering_assessment",
            risk_level=RiskLevel.HIGH,
        )
    )

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "construction"
    assert "geodesy" in assessment.secondary_domains
    assert "structural_monitoring" in assessment.secondary_domains
    assert resolver.get_audit(task.task_id).material_conflict is False


def test_semantic_only_domain_discovery_replaces_general_fallback() -> None:
    task = make_task("Analyze archaeological pottery symbolism from a newly catalogued collection")
    resolver = make_hybrid(
        semantic_result(
            primary_domain="archaeology",
            secondary_domains=["material_culture"],
            task_type="interpretive_analysis",
            risk_level=RiskLevel.LOW,
        )
    )

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "archaeology"
    assert assessment.secondary_domains == ["material_culture"]
    assert assessment.risk_level == RiskLevel.LOW
    assert assessment.task_type == "interpretive_analysis"


def test_deterministic_high_risk_floor_cannot_be_lowered_by_semantic_result() -> None:
    task = make_task("Explain current medical treatment evidence for a patient")
    resolver = make_hybrid(
        semantic_result(
            primary_domain="medicine",
            task_type="medical_research",
            risk_level=RiskLevel.MEDIUM,
        )
    )

    assessment = resolver.resolve(task)

    assert assessment.risk_level == RiskLevel.CRITICAL
    assert any("risk floor" in item.casefold() for item in assessment.uncertainties)
    assert resolver.get_audit(task.task_id).risk_floor_applied is True


def test_material_domain_disagreement_is_auditable_and_surfaces_user_review_uncertainty() -> None:
    task = make_task("Explain current medical treatment evidence for a patient")
    resolver = make_hybrid(
        semantic_result(
            primary_domain="literary_analysis",
            task_type="interpretive_analysis",
            risk_level=RiskLevel.LOW,
        )
    )

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "medicine"
    assert "literary_analysis" in assessment.secondary_domains
    assert any("material domain disagreement" in item.casefold() for item in assessment.uncertainties)
    assert any("user review is required" in item.casefold() for item in assessment.uncertainties)
    audit = resolver.get_audit(task.task_id)
    assert audit.material_conflict is True
    assert audit.risk_floor_applied is True


def test_malformed_semantic_output_falls_back_to_rules_with_explicit_uncertainty() -> None:
    task = make_task("Assess GNSS RTK coordinate accuracy")
    resolver = make_hybrid({"primary_domain": "geodesy"})

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "geodesy"
    assert any("semantic resolution failed" in item.casefold() for item in assessment.uncertainties)
    audit = resolver.get_audit(task.task_id)
    assert audit.fallback_used is True
    assert audit.semantic_used is False


def test_semantic_provider_failure_uses_deterministic_fallback() -> None:
    task = make_task("Assess GNSS RTK coordinate accuracy")
    resolver = make_hybrid(RuntimeError("provider unavailable"))

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "geodesy"
    assert resolver.get_audit(task.task_id).fallback_used is True


def test_low_semantic_confidence_uses_configured_fallback_threshold() -> None:
    task = make_task("Analyze archaeological pottery symbolism")
    resolver = make_hybrid(
        semantic_result(primary_domain="archaeology", confidence=0.40),
        minimum_semantic_confidence=0.70,
    )

    assessment = resolver.resolve(task)

    assert assessment.primary_domain == "general_research"
    assert any("confidence below" in item.casefold() for item in assessment.uncertainties)


def test_semantic_failure_can_be_configured_to_fail_closed() -> None:
    task = make_task("Assess GNSS RTK coordinate accuracy")
    resolver = make_hybrid(RuntimeError("provider unavailable"), fallback_to_rules=False)

    with pytest.raises(SemanticResolutionError):
        resolver.resolve(task)


def test_domain_assessment_contract_schema_remains_unchanged() -> None:
    expected = {
        "assessment_id",
        "task_id",
        "primary_domain",
        "secondary_domains",
        "task_type",
        "risk_level",
        "identified_standards",
        "recommended_source_types",
        "recommended_evaluation_criteria",
        "uncertainties",
        "created_at",
    }
    assert set(DomainAssessment.model_fields) == expected


def test_rule_based_resolver_alias_preserves_phase3_behavior() -> None:
    task = make_task("Assess GNSS RTK coordinate accuracy")
    assessment = RuleBasedResolver().resolve(task)
    assert assessment.primary_domain == "geodesy"
    assert assessment.risk_level == RiskLevel.HIGH


def test_hybrid_profile_generation_preserves_explicit_user_approval_gate() -> None:
    manager = TaskManager()
    engine = WorkflowEngine(task_manager=manager)
    task = manager.create_task(
        user_request="Analyze archaeological pottery symbolism",
        task_type="auto",
    )
    engine.start_workflow(task.task_id)
    resolver = make_hybrid(
        semantic_result(
            primary_domain="archaeology",
            task_type="interpretive_analysis",
            risk_level=RiskLevel.LOW,
        )
    )
    workflow = ProfileWorkflow(engine, domain_resolver=resolver)

    assessment, profile = workflow.generate_profile(task.task_id)

    assert assessment.primary_domain == "archaeology"
    assert profile.status == ProfileStatus.REVIEW_REQUIRED
    assert task.status == TaskStatus.PROFILE_REVIEW_REQUIRED
    assert task.active_profile_id is None

    approved, _ = workflow.approve_current_profile(task.task_id, approved_by="USER")
    assert approved.status == ProfileStatus.APPROVED
    assert task.status == TaskStatus.PROFILE_APPROVED
    assert task.active_profile_id == approved.profile_id
