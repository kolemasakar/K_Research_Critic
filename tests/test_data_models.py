from datetime import timedelta

import pytest
from pydantic import ValidationError

from models import (
    AgentDefinition,
    AgentResult,
    AgentType,
    Claim,
    ClaimType,
    CriticProfile,
    ErrorRecord,
    ErrorType,
    ExecutionStatus,
    IdPrefix,
    ImportanceLevel,
    ProfileStatus,
    ReliabilityClass,
    RiskLevel,
    Source,
    SourceType,
    Task,
    VerificationStatus,
    generate_id,
    utc_now,
)


def make_task() -> Task:
    return Task(
        user_request="Assess GNSS accuracy for deformation monitoring",
        task_type="technical_research",
    )


def make_profile(task: Task, status: ProfileStatus = ProfileStatus.DRAFT) -> CriticProfile:
    values = {
        "task_id": task.task_id,
        "status": status,
        "domain": ["geodesy"],
        "subdomains": ["GNSS"],
        "task_type": "technical_research",
        "risk_level": RiskLevel.HIGH,
        "critic_role": "Independent geodesy technical reviewer",
        "evaluation_criteria": [
            "technical correctness",
            "measurement accuracy",
            "source reliability",
        ],
        "preferred_source_types": ["STANDARD", "OFFICIAL"],
        "required_cross_checks": ["two independent sources"],
        "standards": [],
        "minimum_evidence_level": "authoritative",
        "freshness_requirement": "current_where_relevant",
        "confidence_threshold": 0.9,
    }
    if status == ProfileStatus.APPROVED:
        values["approved_at"] = utc_now()
        values["approved_by"] = "USER"
    return CriticProfile(**values)


def test_task_generates_stable_prefixed_identifier() -> None:
    task = make_task()
    assert task.task_id.startswith("TASK_")
    assert task.model_dump(mode="json")["status"] == "NEW"


def test_identifier_generator_uses_requested_prefix() -> None:
    assert generate_id(IdPrefix.RUN).startswith("RUN_")
    assert generate_id(IdPrefix.WORKFLOW).startswith("WF_")


def test_extra_contract_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        Task(
            user_request="Test",
            task_type="research",
            unexpected_field=True,
        )


def test_task_identifier_is_immutable() -> None:
    task = make_task()
    with pytest.raises(ValidationError):
        task.task_id = generate_id(IdPrefix.TASK)


def test_approved_profile_requires_explicit_approval_metadata() -> None:
    task = make_task()
    with pytest.raises(ValidationError):
        CriticProfile(
            task_id=task.task_id,
            status=ProfileStatus.APPROVED,
            domain=["medicine"],
            task_type="research",
            risk_level=RiskLevel.HIGH,
            critic_role="Medical evidence reviewer",
            evaluation_criteria=["clinical evidence quality"],
            minimum_evidence_level="high",
            freshness_requirement="current",
            confidence_threshold=0.95,
        )


def test_approved_profile_is_valid_with_user_boundary() -> None:
    task = make_task()
    profile = make_profile(task, ProfileStatus.APPROVED)
    assert profile.status == ProfileStatus.APPROVED
    assert profile.approved_by == "USER"


def test_critic_profile_is_immutable() -> None:
    task = make_task()
    profile = make_profile(task, ProfileStatus.APPROVED)
    with pytest.raises(ValidationError):
        profile.confidence_threshold = 0.8


def test_claim_confidence_must_be_in_range() -> None:
    task = make_task()
    run_id = generate_id(IdPrefix.RUN)
    with pytest.raises(ValidationError):
        Claim(
            task_id=task.task_id,
            text="The receiver supports the required correction stream.",
            claim_type=ClaimType.FACT,
            importance=ImportanceLevel.HIGH,
            confidence=1.1,
            verification_status=VerificationStatus.UNVERIFIED,
            created_by_run_id=run_id,
        )


def test_web_source_requires_access_time() -> None:
    task = make_task()
    with pytest.raises(ValidationError):
        Source(
            task_id=task.task_id,
            url="https://example.com/reference",
            title="Reference",
            source_type=SourceType.REFERENCE,
            reliability_class=ReliabilityClass.C,
        )


def test_web_source_with_access_time_is_valid() -> None:
    task = make_task()
    source = Source(
        task_id=task.task_id,
        url="https://example.com/reference",
        title="Reference",
        accessed_at=utc_now(),
        source_type=SourceType.REFERENCE,
        reliability_class=ReliabilityClass.C,
    )
    assert source.source_id.startswith("SOURCE_")


def test_agent_result_rejects_invalid_time_order() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.RESEARCH,
        name="ResearchAgent",
        version="1.0",
    )
    started_at = utc_now()
    with pytest.raises(ValidationError):
        AgentResult(
            run_id=generate_id(IdPrefix.RUN),
            request_id=generate_id(IdPrefix.REQUEST),
            task_id=task.task_id,
            agent_id=agent.agent_id,
            agent_type=AgentType.RESEARCH,
            status=ExecutionStatus.SUCCEEDED,
            result_type="ResearchResult",
            started_at=started_at,
            completed_at=started_at - timedelta(seconds=1),
        )


def test_failed_agent_result_requires_error_record() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.RESEARCH,
        name="ResearchAgent",
        version="1.0",
    )
    now = utc_now()
    with pytest.raises(ValidationError):
        AgentResult(
            run_id=generate_id(IdPrefix.RUN),
            request_id=generate_id(IdPrefix.REQUEST),
            task_id=task.task_id,
            agent_id=agent.agent_id,
            agent_type=AgentType.RESEARCH,
            status=ExecutionStatus.FAILED,
            result_type="ResearchResult",
            started_at=now,
            completed_at=now,
        )

    error = ErrorRecord(
        error_code="TEST_FAILURE",
        error_type=ErrorType.CONTRACT_ERROR,
        message="Expected test error",
        recoverable=False,
        component="ResearchAgent",
    )
    result = AgentResult(
        run_id=generate_id(IdPrefix.RUN),
        request_id=generate_id(IdPrefix.REQUEST),
        task_id=task.task_id,
        agent_id=agent.agent_id,
        agent_type=AgentType.RESEARCH,
        status=ExecutionStatus.FAILED,
        result_type="ResearchResult",
        errors=[error],
        started_at=now,
        completed_at=now,
    )
    assert result.errors[0].error_code == "TEST_FAILURE"
