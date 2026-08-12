import pytest
from pydantic import ValidationError

from models import (
    AgentDefinition,
    AgentRunRequest,
    AgentType,
    IdPrefix,
    ProfileStatus,
    RiskLevel,
    Task,
    CriticProfile,
    generate_id,
    utc_now,
)


def make_task() -> Task:
    return Task(
        user_request="Evaluate a technical research result",
        task_type="technical_research",
    )


def make_profile(task: Task, status: ProfileStatus) -> CriticProfile:
    values = {
        "task_id": task.task_id,
        "status": status,
        "domain": ["construction"],
        "task_type": "technical_research",
        "risk_level": RiskLevel.HIGH,
        "critic_role": "Independent construction reviewer",
        "evaluation_criteria": ["technical correctness", "applicable standards"],
        "minimum_evidence_level": "authoritative",
        "freshness_requirement": "current_where_relevant",
        "confidence_threshold": 0.9,
    }
    if status == ProfileStatus.APPROVED:
        values["approved_at"] = utc_now()
        values["approved_by"] = "USER"
    return CriticProfile(**values)


def test_research_agent_does_not_require_critic_profile() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.RESEARCH,
        name="ResearchAgent",
        version="1.0",
    )
    request = AgentRunRequest(
        task_id=task.task_id,
        workflow_run_id=generate_id(IdPrefix.WORKFLOW),
        agent_id=agent.agent_id,
        agent_type=AgentType.RESEARCH,
        input={"task": task.user_request},
    )
    assert request.profile is None


def test_critic_agent_rejects_missing_profile() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.CRITIC,
        name="CriticAgent",
        version="1.0",
        supports_profile=True,
    )
    with pytest.raises(ValidationError):
        AgentRunRequest(
            task_id=task.task_id,
            workflow_run_id=generate_id(IdPrefix.WORKFLOW),
            agent_id=agent.agent_id,
            agent_type=AgentType.CRITIC,
            input={"draft": "Draft result"},
        )


def test_critic_agent_rejects_unapproved_profile() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.CRITIC,
        name="CriticAgent",
        version="1.0",
        supports_profile=True,
    )
    profile = make_profile(task, ProfileStatus.REVIEW_REQUIRED)
    with pytest.raises(ValidationError):
        AgentRunRequest(
            task_id=task.task_id,
            workflow_run_id=generate_id(IdPrefix.WORKFLOW),
            agent_id=agent.agent_id,
            agent_type=AgentType.CRITIC,
            input={"draft": "Draft result"},
            profile=profile,
        )


def test_critic_agent_accepts_approved_profile_for_same_task() -> None:
    task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.CRITIC,
        name="CriticAgent",
        version="1.0",
        supports_profile=True,
    )
    profile = make_profile(task, ProfileStatus.APPROVED)
    request = AgentRunRequest(
        task_id=task.task_id,
        workflow_run_id=generate_id(IdPrefix.WORKFLOW),
        agent_id=agent.agent_id,
        agent_type=AgentType.CRITIC,
        input={"draft": "Draft result"},
        profile=profile,
    )
    assert request.profile is not None
    assert request.profile.profile_id == profile.profile_id


def test_critic_agent_rejects_profile_from_another_task() -> None:
    task = make_task()
    other_task = make_task()
    agent = AgentDefinition(
        agent_type=AgentType.CRITIC,
        name="CriticAgent",
        version="1.0",
        supports_profile=True,
    )
    profile = make_profile(other_task, ProfileStatus.APPROVED)
    with pytest.raises(ValidationError):
        AgentRunRequest(
            task_id=task.task_id,
            workflow_run_id=generate_id(IdPrefix.WORKFLOW),
            agent_id=agent.agent_id,
            agent_type=AgentType.CRITIC,
            input={"draft": "Draft result"},
            profile=profile,
        )
