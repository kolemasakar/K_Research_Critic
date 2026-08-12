from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from agents import Agent
from models import (
    AgentResult,
    AgentRunRequest,
    AgentType,
    CriticProfile,
    CriticReview,
    ExecutionStatus,
    ProfileStatus,
    ResearchResult,
    ReviewDecision,
    TaskStatus,
)

from .exceptions import ProfileStateError
from .profile_manager import ProfileManager
from .workflow_engine import WorkflowEngine


@dataclass(frozen=True)
class ResearchCriticIteration:
    """Auditable record of one completed ResearchAgent-CriticAgent iteration."""

    iteration: int
    research_agent_result: AgentResult
    research_result: ResearchResult
    critic_agent_result: AgentResult
    critic_review: CriticReview


@dataclass(frozen=True)
class ResearchCriticLoopOutcome:
    """Structured Phase 7 outcome returned when the autonomous loop stops."""

    task_id: str
    workflow_run_id: str
    final_state: TaskStatus
    iterations: tuple[ResearchCriticIteration, ...]
    agent_results: tuple[AgentResult, ...]

    @property
    def last_research_result(self) -> ResearchResult | None:
        return self.iterations[-1].research_result if self.iterations else None

    @property
    def last_review(self) -> CriticReview | None:
        return self.iterations[-1].critic_review if self.iterations else None


class ResearchCriticLoop:
    """Supervisor-owned autonomous ResearchAgent-CriticAgent revision loop."""

    def __init__(
        self,
        workflow_engine: WorkflowEngine,
        profile_manager: ProfileManager,
        research_agent: Agent,
        critic_agent: Agent,
    ) -> None:
        if research_agent.definition.agent_type != AgentType.RESEARCH:
            raise ValueError("research_agent must expose AgentType.RESEARCH")
        if critic_agent.definition.agent_type != AgentType.CRITIC:
            raise ValueError("critic_agent must expose AgentType.CRITIC")
        self.workflow_engine = workflow_engine
        self.profile_manager = profile_manager
        self.research_agent = research_agent
        self.critic_agent = critic_agent
        self._iterations: dict[str, list[ResearchCriticIteration]] = {}
        self._agent_results: dict[str, AgentResult] = {}

    def run(
        self,
        task_id: str,
        *,
        research_input: dict[str, Any] | None = None,
        critic_input: dict[str, Any] | None = None,
        research_constraints: dict[str, Any] | None = None,
        critic_constraints: dict[str, Any] | None = None,
    ) -> ResearchCriticLoopOutcome:
        task = self.workflow_engine.task_manager.get_task(task_id)
        workflow = self.workflow_engine.get_task_workflow(task_id)
        if task.status not in {TaskStatus.PROFILE_APPROVED, TaskStatus.REVISE_REQUIRED}:
            raise ProfileStateError(
                "Autonomous Research-Critic execution requires PROFILE_APPROVED "
                "or a resumable REVISE_REQUIRED state"
            )

        profile = self._active_profile(task_id)
        previous_review = self._last_review(task_id)

        while True:
            if task.status == TaskStatus.REVISE_REQUIRED and workflow.iteration >= workflow.max_iterations:
                self._finish_iteration_limit(task_id, workflow.max_iterations)
                return self._outcome(task_id)

            self.workflow_engine.start_research_iteration(task_id)
            workflow = self.workflow_engine.get_task_workflow(task_id)
            iteration = workflow.iteration

            research_request = AgentRunRequest(
                task_id=task.task_id,
                workflow_run_id=workflow.workflow_run_id,
                agent_id=self.research_agent.definition.agent_id,
                agent_type=AgentType.RESEARCH,
                iteration=iteration,
                input=self._research_payload(
                    task.user_request,
                    research_input or {},
                    previous_review,
                ),
                context=self._context(task_id),
                constraints=dict(research_constraints or {}),
            )
            research_agent_result = self.research_agent.run(research_request)
            self._record_agent_result(task_id, research_agent_result)

            if research_agent_result.status == ExecutionStatus.FAILED:
                self._fail_from_agent(task_id, research_agent_result, "ResearchAgent")
                return self._outcome(task_id)

            research_result = self._parse_research_result(
                task_id,
                iteration,
                research_request.run_id,
                research_agent_result,
            )
            if research_result is None:
                return self._outcome(task_id)

            self.workflow_engine.transition(
                task_id,
                TaskStatus.DRAFT_READY,
                trigger="research_draft_ready",
                reason=f"Research iteration {iteration} produced a structured draft",
            )
            self.workflow_engine.transition(
                task_id,
                TaskStatus.REVIEWING,
                trigger="critic_review_started",
                reason=f"CriticAgent review started for iteration {iteration}",
            )

            critic_request = AgentRunRequest(
                task_id=task.task_id,
                workflow_run_id=workflow.workflow_run_id,
                agent_id=self.critic_agent.definition.agent_id,
                agent_type=AgentType.CRITIC,
                iteration=iteration,
                input=self._critic_payload(research_result, critic_input or {}),
                context=self._context(task_id),
                profile=profile,
                constraints=dict(critic_constraints or {}),
            )
            critic_agent_result = self.critic_agent.run(critic_request)
            self._record_agent_result(task_id, critic_agent_result)

            if critic_agent_result.status == ExecutionStatus.FAILED:
                self._fail_from_agent(task_id, critic_agent_result, "CriticAgent")
                return self._outcome(task_id)

            critic_review = self._parse_critic_review(
                task_id,
                iteration,
                critic_request.run_id,
                profile,
                critic_agent_result,
            )
            if critic_review is None:
                return self._outcome(task_id)

            iteration_record = ResearchCriticIteration(
                iteration=iteration,
                research_agent_result=research_agent_result,
                research_result=research_result,
                critic_agent_result=critic_agent_result,
                critic_review=critic_review,
            )
            self._iterations.setdefault(task_id, []).append(iteration_record)

            if self._review_is_accepted(critic_agent_result, critic_review, profile):
                self.workflow_engine.transition(
                    task_id,
                    TaskStatus.APPROVED,
                    trigger="critic_passed_research",
                    reason=(
                        f"CriticAgent PASS at reliability {critic_review.reliability_score:.4f}; "
                        f"required threshold {profile.confidence_threshold:.4f}"
                    ),
                )
                return self._outcome(task_id)

            self.workflow_engine.transition(
                task_id,
                TaskStatus.REVISE_REQUIRED,
                trigger="critic_requested_revision",
                reason=self._revision_reason(critic_agent_result, critic_review, profile),
            )

            if workflow.iteration >= workflow.max_iterations:
                self._finish_iteration_limit(task_id, workflow.max_iterations)
                return self._outcome(task_id)

            previous_review = critic_review

    def get_iterations(self, task_id: str) -> list[ResearchCriticIteration]:
        return list(self._iterations.get(task_id, []))

    def get_agent_result(self, run_id: str) -> AgentResult:
        return self._agent_results[run_id]

    def _active_profile(self, task_id: str) -> CriticProfile:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.active_profile_id is None:
            raise ProfileStateError("Autonomous Research-Critic execution requires an active profile")
        profile = self.profile_manager.get_profile(task.active_profile_id)
        if profile.status != ProfileStatus.APPROVED:
            raise ProfileStateError("Active CriticProfile must be APPROVED")
        if profile.task_id != task.task_id:
            raise ProfileStateError("Active CriticProfile task_id does not match the task")
        return profile

    def _last_review(self, task_id: str) -> CriticReview | None:
        history = self._iterations.get(task_id, [])
        return history[-1].critic_review if history else None

    @staticmethod
    def _research_payload(
        user_request: str,
        extra: dict[str, Any],
        previous_review: CriticReview | None,
    ) -> dict[str, Any]:
        payload = {"topic": user_request, "user_request": user_request, **extra}
        if previous_review is not None:
            payload["previous_review"] = previous_review.model_dump(mode="json")
        return payload

    @staticmethod
    def _critic_payload(
        research_result: ResearchResult,
        extra: dict[str, Any],
    ) -> dict[str, Any]:
        payload = dict(extra)
        payload["research_result"] = research_result.model_dump(mode="json")
        return payload

    def _context(self, task_id: str) -> dict[str, Any]:
        workflow = self.workflow_engine.get_task_workflow(task_id)
        return {
            "iteration": workflow.iteration,
            "workflow_state": workflow.current_state.value,
            "prior_run_ids": list(workflow.agent_run_ids),
        }

    def _record_agent_result(self, task_id: str, result: AgentResult) -> None:
        self._agent_results[result.run_id] = result
        self.workflow_engine.record_agent_run(task_id, result.run_id)

    def _parse_research_result(
        self,
        task_id: str,
        iteration: int,
        request_run_id: str,
        result: AgentResult,
    ) -> ResearchResult | None:
        try:
            research = ResearchResult.model_validate(result.payload)
            if research.task_id != task_id:
                raise ValueError("ResearchResult task_id does not match workflow task_id")
            if research.run_id != request_run_id or result.run_id != request_run_id:
                raise ValueError("ResearchResult run_id does not match ResearchAgent request run_id")
            if research.iteration != iteration:
                raise ValueError("ResearchResult iteration does not match workflow iteration")
            return research
        except (ValidationError, TypeError, ValueError) as exc:
            self.workflow_engine.fail_task(
                task_id,
                reason=f"Invalid ResearchAgent payload: {exc}",
            )
            return None

    def _parse_critic_review(
        self,
        task_id: str,
        iteration: int,
        request_run_id: str,
        profile: CriticProfile,
        result: AgentResult,
    ) -> CriticReview | None:
        try:
            review = CriticReview.model_validate(result.payload)
            if review.task_id != task_id:
                raise ValueError("CriticReview task_id does not match workflow task_id")
            if review.run_id != request_run_id or result.run_id != request_run_id:
                raise ValueError("CriticReview run_id does not match CriticAgent request run_id")
            if review.profile_id != profile.profile_id:
                raise ValueError("CriticReview profile_id does not match active CriticProfile")
            if review.iteration != iteration:
                raise ValueError("CriticReview iteration does not match workflow iteration")
            return review
        except (ValidationError, TypeError, ValueError) as exc:
            self.workflow_engine.fail_task(
                task_id,
                reason=f"Invalid CriticAgent payload: {exc}",
            )
            return None

    @staticmethod
    def _review_is_accepted(
        agent_result: AgentResult,
        review: CriticReview,
        profile: CriticProfile,
    ) -> bool:
        return (
            agent_result.status == ExecutionStatus.SUCCEEDED
            and review.decision == ReviewDecision.PASS
            and review.reliability_score >= profile.confidence_threshold
        )

    @staticmethod
    def _revision_reason(
        agent_result: AgentResult,
        review: CriticReview,
        profile: CriticProfile,
    ) -> str:
        if agent_result.status == ExecutionStatus.PARTIAL:
            return "CriticAgent execution was PARTIAL; incomplete verification cannot be accepted"
        if review.reliability_score < profile.confidence_threshold:
            return (
                f"Critic reliability {review.reliability_score:.4f} is below "
                f"required threshold {profile.confidence_threshold:.4f}"
            )
        return "CriticAgent returned REVISE"

    def _finish_iteration_limit(self, task_id: str, max_iterations: int) -> None:
        task = self.workflow_engine.task_manager.get_task(task_id)
        if task.status == TaskStatus.REVISE_REQUIRED:
            self.workflow_engine.transition(
                task_id,
                TaskStatus.MAX_ITERATIONS_REACHED,
                trigger="iteration_limit_reached",
                reason=f"Maximum autonomous iterations reached: {max_iterations}",
            )
        self.workflow_engine.complete_with_limitations(
            task_id,
            reason=(
                f"Useful research output exists, but acceptance criteria were not met "
                f"within {max_iterations} iterations"
            ),
        )

    def _fail_from_agent(
        self,
        task_id: str,
        result: AgentResult,
        agent_name: str,
    ) -> None:
        detail = result.errors[0].message if result.errors else "agent execution failed"
        self.workflow_engine.fail_task(
            task_id,
            reason=f"{agent_name} failed: {detail}",
        )

    def _outcome(self, task_id: str) -> ResearchCriticLoopOutcome:
        task = self.workflow_engine.task_manager.get_task(task_id)
        workflow = self.workflow_engine.get_task_workflow(task_id)
        agent_results = tuple(
            self._agent_results[run_id]
            for run_id in workflow.agent_run_ids
            if run_id in self._agent_results
        )
        return ResearchCriticLoopOutcome(
            task_id=task.task_id,
            workflow_run_id=workflow.workflow_run_id,
            final_state=task.status,
            iterations=tuple(self._iterations.get(task_id, [])),
            agent_results=agent_results,
        )
