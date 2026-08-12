from __future__ import annotations

from datetime import date

import pytest

from agents import Agent, CriticAgent, ResearchAgent
from models import (
    AgentDefinition,
    AgentResult,
    AgentRunRequest,
    AgentType,
    Claim,
    ClaimType,
    CriticReview,
    ErrorRecord,
    ErrorType,
    ExecutionStatus,
    ImportanceLevel,
    Metrics,
    ReliabilityClass,
    ResearchResult,
    ReviewDecision,
    Source,
    SourceType,
    TaskStatus,
    VerificationStatus,
    WorkflowStatus,
    utc_now,
)
from supervisor import ProfileStateError, ProfileWorkflow, ResearchCriticLoop, WorkflowEngine
from tools import FetchedDocument, SearchHit


class ScriptedResearchAgent(Agent):
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.requests: list[AgentRunRequest] = []
        self._definition = AgentDefinition(
            agent_type=AgentType.RESEARCH,
            name="ScriptedResearchAgent",
            version="1.0",
            capabilities=["research_planning"],
            accepted_input_types=["research_task"],
            produced_output_types=["research_result"],
        )

    @property
    def definition(self) -> AgentDefinition:
        return self._definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        self.requests.append(request)
        started_at = utc_now()
        if self.fail:
            return AgentResult(
                run_id=request.run_id,
                request_id=request.request_id,
                task_id=request.task_id,
                agent_id=request.agent_id,
                agent_type=AgentType.RESEARCH,
                status=ExecutionStatus.FAILED,
                result_type="research_result",
                payload={},
                errors=[
                    ErrorRecord(
                        error_code="SCRIPTED_RESEARCH_FAILURE",
                        error_type=ErrorType.INTERNAL_ERROR,
                        message="scripted research failure",
                        recoverable=False,
                        component="ScriptedResearchAgent",
                        run_id=request.run_id,
                    )
                ],
                metrics=Metrics(),
                started_at=started_at,
                completed_at=utc_now(),
            )

        source = Source(
            task_id=request.task_id,
            url=f"https://research.example/iteration-{request.iteration}",
            title=f"Research source {request.iteration}",
            publisher="Research Publisher",
            publication_date=date.today(),
            accessed_at=utc_now(),
            source_type=SourceType.OFFICIAL,
            reliability_class=ReliabilityClass.A,
            primary_source=True,
            independence_group=f"research-{request.iteration}",
        )
        claim = Claim(
            task_id=request.task_id,
            text=f"Iteration {request.iteration} evidence-backed finding",
            claim_type=ClaimType.FACT,
            importance=ImportanceLevel.MEDIUM,
            source_ids=[source.source_id],
            confidence=0.95,
            verification_status=VerificationStatus.UNVERIFIED,
            created_by_run_id=request.run_id,
        )
        source.supports_claim_ids = [claim.claim_id]
        research = ResearchResult(
            task_id=request.task_id,
            run_id=request.run_id,
            iteration=request.iteration,
            summary=claim.text,
            findings=[claim.text],
            claims=[claim],
            sources=[source],
            draft_report=f"# Draft\n\n- {claim.text} [{source.source_id}]",
            changes_applied=(
                ["Applied prior critic feedback"] if request.input.get("previous_review") else []
            ),
        )
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.RESEARCH,
            status=ExecutionStatus.SUCCEEDED,
            result_type="research_result",
            payload=research.model_dump(mode="json"),
            metrics=Metrics(claims_created=1, sources_examined=1),
            started_at=started_at,
            completed_at=utc_now(),
        )


class ScriptedCriticAgent(Agent):
    def __init__(self, steps: list[tuple[ReviewDecision, float, ExecutionStatus]]) -> None:
        self.steps = steps
        self.requests: list[AgentRunRequest] = []
        self._definition = AgentDefinition(
            agent_type=AgentType.CRITIC,
            name="ScriptedCriticAgent",
            version="1.0",
            capabilities=["claim_verification"],
            accepted_input_types=["research_result"],
            produced_output_types=["critic_review"],
            supports_profile=True,
        )

    @property
    def definition(self) -> AgentDefinition:
        return self._definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        self.requests.append(request)
        index = min(len(self.requests) - 1, len(self.steps) - 1)
        decision, score, status = self.steps[index]
        assert request.profile is not None
        research = ResearchResult.model_validate(request.input["research_result"])
        recommended = ["Add independent confirmation"] if decision == ReviewDecision.REVISE else []
        missing = ["coverage requirement"] if decision == ReviewDecision.REVISE else []
        review = CriticReview(
            task_id=request.task_id,
            run_id=request.run_id,
            profile_id=request.profile.profile_id,
            iteration=request.iteration,
            decision=decision,
            reliability_score=score,
            unsupported_claim_ids=(
                [research.claims[0].claim_id] if decision == ReviewDecision.REVISE else []
            ),
            missing_topics=missing,
            recommended_changes=recommended,
            verified_claim_ids=(
                [research.claims[0].claim_id] if decision == ReviewDecision.PASS else []
            ),
            unresolved_claim_ids=(
                [research.claims[0].claim_id] if decision == ReviewDecision.REVISE else []
            ),
        )
        started_at = utc_now()
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.CRITIC,
            status=status,
            result_type="critic_review",
            payload=review.model_dump(mode="json"),
            metrics=Metrics(claims_verified=len(review.verified_claim_ids)),
            started_at=started_at,
            completed_at=utc_now(),
        )


def build_scripted_loop(
    *,
    max_iterations: int,
    critic_steps: list[tuple[ReviewDecision, float, ExecutionStatus]],
    research_fail: bool = False,
):
    engine = WorkflowEngine()
    task = engine.task_manager.create_task(
        user_request="Research an auditable orchestration workflow",
        task_type="research",
    )
    engine.start_workflow(task.task_id, max_iterations=max_iterations)
    profile_workflow = ProfileWorkflow(engine)
    profile_workflow.generate_profile(task.task_id)
    profile, _ = profile_workflow.approve_current_profile(task.task_id, approved_by="TEST_USER")
    research = ScriptedResearchAgent(fail=research_fail)
    critic = ScriptedCriticAgent(critic_steps)
    loop = ResearchCriticLoop(
        engine,
        profile_workflow.profile_manager,
        research,
        critic,
    )
    return engine, task, profile, research, critic, loop


def test_first_pass_stops_loop_at_approved() -> None:
    engine, task, profile, research, critic, loop = build_scripted_loop(
        max_iterations=3,
        critic_steps=[(ReviewDecision.PASS, 0.95, ExecutionStatus.SUCCEEDED)],
    )

    outcome = loop.run(task.task_id)

    assert outcome.final_state == TaskStatus.APPROVED
    assert engine.get_task_workflow(task.task_id).iteration == 1
    assert len(outcome.iterations) == 1
    assert len(outcome.agent_results) == 2
    assert outcome.last_review is not None
    assert outcome.last_review.profile_id == profile.profile_id
    assert outcome.last_review.decision == ReviewDecision.PASS
    assert len(research.requests) == 1
    assert len(critic.requests) == 1


def test_revise_feedback_is_passed_to_next_research_iteration() -> None:
    engine, task, _, research, _, loop = build_scripted_loop(
        max_iterations=3,
        critic_steps=[
            (ReviewDecision.REVISE, 0.60, ExecutionStatus.SUCCEEDED),
            (ReviewDecision.PASS, 0.95, ExecutionStatus.SUCCEEDED),
        ],
    )

    outcome = loop.run(task.task_id)

    assert outcome.final_state == TaskStatus.APPROVED
    assert engine.get_task_workflow(task.task_id).iteration == 2
    assert len(outcome.iterations) == 2
    assert outcome.iterations[0].research_result.research_result_id != outcome.iterations[1].research_result.research_result_id
    previous_review = research.requests[1].input["previous_review"]
    assert previous_review["recommended_changes"] == ["Add independent confirmation"]
    assert previous_review["missing_topics"] == ["coverage requirement"]
    assert outcome.iterations[1].research_result.changes_applied == ["Applied prior critic feedback"]


def test_max_iterations_terminates_with_explicit_limitations() -> None:
    engine, task, _, _, _, loop = build_scripted_loop(
        max_iterations=2,
        critic_steps=[
            (ReviewDecision.REVISE, 0.55, ExecutionStatus.SUCCEEDED),
            (ReviewDecision.REVISE, 0.65, ExecutionStatus.SUCCEEDED),
        ],
    )

    outcome = loop.run(task.task_id)
    workflow = engine.get_task_workflow(task.task_id)
    states = [transition.to_state for transition in engine.get_transitions(workflow.workflow_run_id)]

    assert outcome.final_state == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert workflow.status == WorkflowStatus.COMPLETED_WITH_LIMITATIONS
    assert workflow.iteration == 2
    assert TaskStatus.MAX_ITERATIONS_REACHED in states
    assert states[-1] == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert len(outcome.iterations) == 2


def test_workflow_enforces_profile_threshold_even_if_critic_returns_pass() -> None:
    engine, task, profile, _, _, loop = build_scripted_loop(
        max_iterations=1,
        critic_steps=[(ReviewDecision.PASS, 0.10, ExecutionStatus.SUCCEEDED)],
    )

    outcome = loop.run(task.task_id)

    assert profile.confidence_threshold > 0.10
    assert outcome.final_state == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert engine.get_task_workflow(task.task_id).iteration == 1


def test_partial_critic_execution_cannot_produce_accepted_pass() -> None:
    _, task, _, _, _, loop = build_scripted_loop(
        max_iterations=1,
        critic_steps=[(ReviewDecision.PASS, 0.99, ExecutionStatus.PARTIAL)],
    )

    outcome = loop.run(task.task_id)

    assert outcome.final_state == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert outcome.last_review is not None
    assert outcome.last_review.decision == ReviewDecision.PASS
    assert outcome.iterations[0].critic_agent_result.status == ExecutionStatus.PARTIAL


def test_failed_research_terminates_workflow_explicitly() -> None:
    engine, task, _, _, critic, loop = build_scripted_loop(
        max_iterations=3,
        critic_steps=[(ReviewDecision.PASS, 0.99, ExecutionStatus.SUCCEEDED)],
        research_fail=True,
    )

    outcome = loop.run(task.task_id)

    assert outcome.final_state == TaskStatus.FAILED
    assert engine.get_task_workflow(task.task_id).status == WorkflowStatus.FAILED
    assert len(critic.requests) == 0
    assert len(outcome.agent_results) == 1
    assert outcome.iterations == ()


def test_loop_exposes_auditable_iteration_and_agent_run_history() -> None:
    engine, task, _, _, _, loop = build_scripted_loop(
        max_iterations=2,
        critic_steps=[
            (ReviewDecision.REVISE, 0.60, ExecutionStatus.SUCCEEDED),
            (ReviewDecision.PASS, 0.95, ExecutionStatus.SUCCEEDED),
        ],
    )

    outcome = loop.run(task.task_id)
    workflow = engine.get_task_workflow(task.task_id)

    assert [item.iteration for item in loop.get_iterations(task.task_id)] == [1, 2]
    assert len(workflow.agent_run_ids) == 4
    assert [result.run_id for result in outcome.agent_results] == workflow.agent_run_ids
    for run_id in workflow.agent_run_ids:
        assert loop.get_agent_result(run_id).run_id == run_id


def test_loop_cannot_start_before_profile_approval() -> None:
    engine = WorkflowEngine()
    task = engine.task_manager.create_task(user_request="Research topic", task_type="research")
    engine.start_workflow(task.task_id)
    profile_workflow = ProfileWorkflow(engine)
    profile_workflow.generate_profile(task.task_id)
    research = ScriptedResearchAgent()
    critic = ScriptedCriticAgent([(ReviewDecision.PASS, 0.95, ExecutionStatus.SUCCEEDED)])
    loop = ResearchCriticLoop(engine, profile_workflow.profile_manager, research, critic)

    with pytest.raises(ProfileStateError):
        loop.run(task.task_id)


class StaticResearchTools:
    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        return [
            SearchHit(
                url="https://official.example/research",
                title="Official research evidence",
                publisher="Official Publisher",
                publication_date=date.today(),
                source_type=SourceType.OFFICIAL,
                primary_source=True,
                independence_group="research-official",
            )
        ][:limit]

    def web_fetch(self, url: str) -> FetchedDocument:
        return FetchedDocument(
            url=url,
            title="Official research evidence",
            publisher="Official Publisher",
            publication_date=date.today(),
            source_type=SourceType.OFFICIAL,
            primary_source=True,
            independence_group="research-official",
            content="Phase seven orchestration provides deterministic iteration control. Additional detail follows.",
        )


class StaticCriticTools:
    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        return [
            SearchHit(
                url="https://independent.example/verification",
                title="Independent verification",
                publisher="Independent Authority",
                publication_date=date.today(),
                source_type=SourceType.OFFICIAL,
                primary_source=True,
                independence_group="critic-independent",
            )
        ][:limit]

    def web_fetch(self, url: str) -> FetchedDocument:
        return FetchedDocument(
            url=url,
            title="Independent verification",
            publisher="Independent Authority",
            publication_date=date.today(),
            source_type=SourceType.OFFICIAL,
            primary_source=True,
            independence_group="critic-independent",
            content="Phase seven orchestration provides deterministic iteration control. Independent evidence supports the claim.",
        )


def test_real_research_and_critic_agents_are_connected_by_supervisor_loop() -> None:
    engine = WorkflowEngine()
    task = engine.task_manager.create_task(
        user_request="Explain phase seven orchestration",
        task_type="research",
    )
    engine.start_workflow(task.task_id, max_iterations=2)
    profile_workflow = ProfileWorkflow(engine)
    profile_workflow.generate_profile(task.task_id)
    profile_workflow.approve_current_profile(task.task_id, approved_by="TEST_USER")

    loop = ResearchCriticLoop(
        engine,
        profile_workflow.profile_manager,
        ResearchAgent(StaticResearchTools()),
        CriticAgent(StaticCriticTools()),
    )
    outcome = loop.run(task.task_id)

    assert outcome.final_state == TaskStatus.APPROVED
    assert len(outcome.iterations) == 1
    assert outcome.iterations[0].research_agent_result.agent_type == AgentType.RESEARCH
    assert outcome.iterations[0].critic_agent_result.agent_type == AgentType.CRITIC
    assert outcome.last_review is not None
    assert outcome.last_review.decision == ReviewDecision.PASS
