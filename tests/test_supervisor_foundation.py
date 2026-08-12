import pytest

from models import ActorType, AgentDefinition, AgentStatus, AgentType, IdPrefix, TaskStatus, WorkflowStatus, generate_id
from supervisor import AgentRegistrationError, AgentRegistry, InvalidStateTransitionError, TaskManager, WorkflowAlreadyActiveError, WorkflowEngine


def make_engine(max_iterations: int = 3):
    manager = TaskManager()
    engine = WorkflowEngine(task_manager=manager)
    task = manager.create_task(user_request="Assess GNSS monitoring workflow", task_type="technical_research")
    run = engine.start_workflow(task.task_id, max_iterations=max_iterations)
    return manager, engine, task, run


def move_to_profile_review(manager, engine, task):
    engine.transition(task.task_id, TaskStatus.PROFILE_GENERATING, trigger="task_accepted")
    engine.transition(task.task_id, TaskStatus.PROFILE_REVIEW_REQUIRED, trigger="profile_draft_ready")
    manager.set_active_profile(task.task_id, generate_id(IdPrefix.PROFILE))
    engine.transition(task.task_id, TaskStatus.PROFILE_APPROVED, trigger="user_approved_profile", actor_type=ActorType.USER, actor_id="USER")


def test_happy_path_reaches_finalized_and_records_audit_history() -> None:
    manager, engine, task, run = make_engine()
    move_to_profile_review(manager, engine, task)
    iteration_transition = engine.start_research_iteration(task.task_id)
    assert iteration_transition.to_state == TaskStatus.RESEARCHING
    assert run.iteration == 1
    engine.transition(task.task_id, TaskStatus.DRAFT_READY, trigger="research_complete")
    engine.transition(task.task_id, TaskStatus.REVIEWING, trigger="critic_started")
    engine.transition(task.task_id, TaskStatus.APPROVED, trigger="critic_pass")
    engine.transition(task.task_id, TaskStatus.FINALIZING, trigger="finalization_started")
    engine.transition(task.task_id, TaskStatus.FINALIZED, trigger="artifacts_created")
    assert task.status == TaskStatus.FINALIZED
    assert run.status == WorkflowStatus.SUCCEEDED
    assert run.completed_at is not None
    transitions = engine.get_transitions(run.workflow_run_id)
    assert transitions[0].from_state == TaskStatus.NEW
    assert transitions[-1].to_state == TaskStatus.FINALIZED
    assert len({item.transition_id for item in transitions}) == len(transitions)


def test_invalid_transition_is_rejected_without_state_change() -> None:
    _, engine, task, _ = make_engine()
    with pytest.raises(InvalidStateTransitionError):
        engine.transition(task.task_id, TaskStatus.RESEARCHING, trigger="invalid")
    assert task.status == TaskStatus.NEW


def test_profile_approval_state_requires_active_profile_id() -> None:
    _, engine, task, _ = make_engine()
    engine.transition(task.task_id, TaskStatus.PROFILE_GENERATING, trigger="task_accepted")
    engine.transition(task.task_id, TaskStatus.PROFILE_REVIEW_REQUIRED, trigger="profile_draft_ready")
    with pytest.raises(InvalidStateTransitionError):
        engine.transition(task.task_id, TaskStatus.PROFILE_APPROVED, trigger="invalid_approval")


def test_waiting_for_user_status_is_explicit() -> None:
    _, engine, task, run = make_engine()
    engine.transition(task.task_id, TaskStatus.PROFILE_GENERATING, trigger="task_accepted")
    engine.transition(task.task_id, TaskStatus.PROFILE_REVIEW_REQUIRED, trigger="profile_draft_ready")
    assert run.status == WorkflowStatus.WAITING_FOR_USER


def test_iteration_limit_routes_to_completed_with_limitations() -> None:
    manager, engine, task, run = make_engine(max_iterations=1)
    move_to_profile_review(manager, engine, task)
    engine.start_research_iteration(task.task_id)
    engine.transition(task.task_id, TaskStatus.DRAFT_READY, trigger="research_complete")
    engine.transition(task.task_id, TaskStatus.REVIEWING, trigger="critic_started")
    engine.transition(task.task_id, TaskStatus.REVISE_REQUIRED, trigger="critic_revise")
    limit_transition = engine.start_research_iteration(task.task_id)
    assert limit_transition.to_state == TaskStatus.MAX_ITERATIONS_REACHED
    assert run.iteration == 1
    engine.complete_with_limitations(task.task_id, reason="Iteration limit reached")
    assert task.status == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert run.status == WorkflowStatus.COMPLETED_WITH_LIMITATIONS
    assert run.completed_at is not None


def test_failure_terminates_workflow() -> None:
    _, engine, task, run = make_engine()
    engine.transition(task.task_id, TaskStatus.PROFILE_GENERATING, trigger="task_accepted")
    engine.fail_task(task.task_id, reason="Unrecoverable profile generation error")
    assert task.status == TaskStatus.FAILED
    assert run.status == WorkflowStatus.FAILED
    assert run.completed_at is not None
    with pytest.raises(InvalidStateTransitionError):
        engine.transition(task.task_id, TaskStatus.PROFILE_GENERATING, trigger="retry")


def test_second_active_workflow_for_same_task_is_rejected() -> None:
    _, engine, task, _ = make_engine()
    with pytest.raises(WorkflowAlreadyActiveError):
        engine.start_workflow(task.task_id)


def test_agent_run_tracking_is_idempotent() -> None:
    _, engine, task, run = make_engine()
    agent_run_id = generate_id(IdPrefix.RUN)
    engine.record_agent_run(task.task_id, agent_run_id)
    engine.record_agent_run(task.task_id, agent_run_id)
    assert run.agent_run_ids == [agent_run_id]


def test_agent_registry_supports_capability_discovery() -> None:
    registry = AgentRegistry()
    research = AgentDefinition(agent_type=AgentType.RESEARCH, name="ResearchAgent", version="1.0", capabilities=["web_research", "claim_extraction"])
    disabled = AgentDefinition(agent_type=AgentType.CRITIC, name="DisabledCritic", version="1.0", capabilities=["web_research"], status=AgentStatus.DISABLED)
    registry.register(research)
    registry.register(disabled)
    matches = registry.find_by_capability("web_research")
    assert [agent.agent_id for agent in matches] == [research.agent_id]


def test_agent_registry_rejects_duplicate_name_and_version() -> None:
    registry = AgentRegistry()
    registry.register(AgentDefinition(agent_type=AgentType.RESEARCH, name="ResearchAgent", version="1.0"))
    with pytest.raises(AgentRegistrationError):
        registry.register(AgentDefinition(agent_type=AgentType.RESEARCH, name="ResearchAgent", version="1.0"))
