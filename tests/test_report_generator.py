from __future__ import annotations

import importlib
from datetime import date

from agents import ReportGenerator
from models import (
    AgentResult,
    AgentRunRequest,
    AgentType,
    Artifact,
    ArtifactStatus,
    ArtifactType,
    Claim,
    ClaimType,
    CriticReview,
    ExecutionStatus,
    IdPrefix,
    ImportanceLevel,
    Metrics,
    ReliabilityClass,
    ResearchResult,
    ReviewDecision,
    Source,
    SourceType,
    TaskStatus,
    VerificationStatus,
    generate_id,
    utc_now,
)
from supervisor import (
    ProfileWorkflow,
    ReportWorkflow,
    ResearchCriticIteration,
    ResearchCriticLoopOutcome,
    WorkflowEngine,
)


def make_research(task_id: str, *, iteration: int = 1, unicode_text: bool = False) -> ResearchResult:
    run_id = generate_id(IdPrefix.RUN)
    source = Source(
        task_id=task_id,
        url="https://official.example/evidence",
        title="Official evidence",
        publisher="Official Authority",
        publication_date=date.today(),
        accessed_at=utc_now(),
        source_type=SourceType.OFFICIAL,
        reliability_class=ReliabilityClass.A,
        primary_source=True,
        independence_group="official",
    )
    claim_text = "Перевірений висновок" if unicode_text else "Verified conclusion"
    claim = Claim(
        task_id=task_id,
        text=claim_text,
        claim_type=ClaimType.FACT,
        importance=ImportanceLevel.HIGH,
        source_ids=[source.source_id],
        confidence=0.95,
        verification_status=VerificationStatus.VERIFIED,
        created_by_run_id=run_id,
    )
    source.supports_claim_ids = [claim.claim_id]
    return ResearchResult(
        task_id=task_id,
        run_id=run_id,
        iteration=iteration,
        summary="Підсумок дослідження" if unicode_text else "Research summary",
        findings=[claim_text],
        claims=[claim],
        sources=[source],
        uncertainties=["Залишається обмеження даних" if unicode_text else "Residual data limitation"],
        limitations=["Sample limitation"],
        draft_report=f"{claim_text} [{source.source_id}]",
        changes_applied=["Applied critic feedback"] if iteration > 1 else [],
    )


def make_review(task_id: str, profile_id: str, *, iteration: int = 1) -> CriticReview:
    return CriticReview(
        task_id=task_id,
        run_id=generate_id(IdPrefix.RUN),
        profile_id=profile_id,
        iteration=iteration,
        decision=ReviewDecision.PASS,
        reliability_score=0.95,
        recommended_changes=[] if iteration == 1 else ["Prior change resolved"],
        verified_claim_ids=[],
    )


def make_request(
    generator: ReportGenerator,
    task_id: str,
    workflow_run_id: str,
    research: ResearchResult,
    review: CriticReview,
    final_status: TaskStatus,
) -> AgentRunRequest:
    return AgentRunRequest(
        task_id=task_id,
        workflow_run_id=workflow_run_id,
        agent_id=generator.definition.agent_id,
        agent_type=AgentType.REPORT_GENERATOR,
        iteration=research.iteration,
        input={
            "final_research_result": research.model_dump(mode="json"),
            "research_history": [research.model_dump(mode="json")],
            "review_history": [review.model_dump(mode="json")],
            "final_status": final_status.value,
        },
    )


def make_approved_loop(engine: WorkflowEngine) -> tuple[object, object, ResearchCriticLoopOutcome]:
    task = engine.task_manager.create_task(user_request="Research a final report", task_type="research")
    workflow = engine.start_workflow(task.task_id)
    profile_workflow = ProfileWorkflow(engine)
    profile_workflow.generate_profile(task.task_id)
    profile, _ = profile_workflow.approve_current_profile(task.task_id, approved_by="TEST_USER")
    engine.start_research_iteration(task.task_id)
    engine.transition(task.task_id, TaskStatus.DRAFT_READY, trigger="test_draft")
    engine.transition(task.task_id, TaskStatus.REVIEWING, trigger="test_review")
    engine.transition(task.task_id, TaskStatus.APPROVED, trigger="test_pass")

    research = make_research(task.task_id)
    review = make_review(task.task_id, profile.profile_id)
    research_result_envelope = AgentResult(
        run_id=research.run_id,
        request_id=generate_id(IdPrefix.REQUEST),
        task_id=task.task_id,
        agent_id=generate_id(IdPrefix.AGENT),
        agent_type=AgentType.RESEARCH,
        status=ExecutionStatus.SUCCEEDED,
        result_type="research_result",
        payload=research.model_dump(mode="json"),
        metrics=Metrics(),
        started_at=utc_now(),
        completed_at=utc_now(),
    )
    critic_result_envelope = AgentResult(
        run_id=review.run_id,
        request_id=generate_id(IdPrefix.REQUEST),
        task_id=task.task_id,
        agent_id=generate_id(IdPrefix.AGENT),
        agent_type=AgentType.CRITIC,
        status=ExecutionStatus.SUCCEEDED,
        result_type="critic_review",
        payload=review.model_dump(mode="json"),
        metrics=Metrics(),
        started_at=utc_now(),
        completed_at=utc_now(),
    )
    iteration = ResearchCriticIteration(1, research_result_envelope, research, critic_result_envelope, review)
    loop_outcome = ResearchCriticLoopOutcome(
        task_id=task.task_id,
        workflow_run_id=workflow.workflow_run_id,
        final_state=TaskStatus.APPROVED,
        iterations=(iteration,),
        agent_results=(research_result_envelope, critic_result_envelope),
    )
    return task, workflow, loop_outcome


def test_report_generator_writes_both_utf8_artifacts_with_required_content(tmp_path) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id, unicode_text=True)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))

    result = generator.run(make_request(generator, task_id, workflow_id, research, review, TaskStatus.FINALIZED))

    assert result.status == ExecutionStatus.SUCCEEDED
    artifacts = [Artifact.model_validate(item) for item in result.payload["artifacts"]]
    assert {item.artifact_type for item in artifacts} == {ArtifactType.FINAL_REPORT, ArtifactType.REVIEW_PROTOCOL}
    final_path = tmp_path / f"{task_id}_FINAL_REPORT.md"
    protocol_path = tmp_path / f"{task_id}_REVIEW_PROTOCOL.md"
    assert final_path.exists() and protocol_path.exists()
    final_text = final_path.read_text(encoding="utf-8")
    protocol_text = protocol_path.read_text(encoding="utf-8")
    assert "Підсумок дослідження" in final_text
    assert "Залишається обмеження даних" in final_text
    assert f"[{research.sources[0].source_id}]" in final_text
    assert "Critic decision: PASS" in protocol_text
    assert "Hidden chain-of-thought and private model reasoning are not included." in protocol_text


def test_artifact_metadata_records_final_status_checksum_and_encoding(tmp_path) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))

    result = generator.run(make_request(generator, task_id, workflow_id, research, review, TaskStatus.FINALIZED))
    artifacts = [Artifact.model_validate(item) for item in result.payload["artifacts"]]

    assert all(item.encoding == "UTF-8" for item in artifacts)
    assert all(item.metadata["final_task_status"] == TaskStatus.FINALIZED.value for item in artifacts)
    assert all(len(item.checksum) == 64 for item in artifacts)
    assert all(item.status == ArtifactStatus.APPROVED for item in artifacts)


def test_completed_with_limitations_is_explicit_in_both_artifacts(tmp_path) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))

    result = generator.run(
        make_request(generator, task_id, workflow_id, research, review, TaskStatus.COMPLETED_WITH_LIMITATIONS)
    )

    assert result.status == ExecutionStatus.SUCCEEDED
    assert "COMPLETED_WITH_LIMITATIONS" in (tmp_path / f"{task_id}_FINAL_REPORT.md").read_text(encoding="utf-8")
    assert "COMPLETED_WITH_LIMITATIONS" in (tmp_path / f"{task_id}_REVIEW_PROTOCOL.md").read_text(encoding="utf-8")


def test_report_generator_rejects_non_final_status(tmp_path) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))

    result = generator.run(make_request(generator, task_id, workflow_id, research, review, TaskStatus.APPROVED))

    assert result.status == ExecutionStatus.FAILED
    assert result.errors[0].error_code == "INVALID_REPORT_INPUT"


def test_report_generator_second_stage_failure_leaves_no_partial_visible_pair(tmp_path, monkeypatch) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))
    original_stage = generator._stage_text
    calls = 0

    def fail_second_stage(target, content):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated second staging failure")
        return original_stage(target, content)

    monkeypatch.setattr(generator, "_stage_text", fail_second_stage)

    result = generator.run(make_request(generator, task_id, workflow_id, research, review, TaskStatus.FINALIZED))

    assert result.status == ExecutionStatus.FAILED
    assert result.errors[0].error_code == "ARTIFACT_WRITE_FAILED"
    assert not (tmp_path / f"{task_id}_FINAL_REPORT.md").exists()
    assert not (tmp_path / f"{task_id}_REVIEW_PROTOCOL.md").exists()
    assert not list(tmp_path.glob("*.tmp"))


def test_report_generator_commit_failure_restores_existing_artifact_pair(tmp_path, monkeypatch) -> None:
    generator = ReportGenerator(tmp_path)
    task_id = generate_id(IdPrefix.TASK)
    workflow_id = generate_id(IdPrefix.WORKFLOW)
    research = make_research(task_id)
    review = make_review(task_id, generate_id(IdPrefix.PROFILE))
    final_path = tmp_path / f"{task_id}_FINAL_REPORT.md"
    protocol_path = tmp_path / f"{task_id}_REVIEW_PROTOCOL.md"
    final_path.write_text("previous final", encoding="utf-8")
    protocol_path.write_text("previous protocol", encoding="utf-8")

    module = importlib.import_module("agents.report_generator")
    original_replace = module.os.replace
    calls = 0

    def fail_second_commit(source, destination):
        nonlocal calls
        calls += 1
        if calls == 4:
            raise OSError("simulated second commit failure")
        return original_replace(source, destination)

    monkeypatch.setattr(module.os, "replace", fail_second_commit)

    result = generator.run(make_request(generator, task_id, workflow_id, research, review, TaskStatus.FINALIZED))

    assert result.status == ExecutionStatus.FAILED
    assert final_path.read_text(encoding="utf-8") == "previous final"
    assert protocol_path.read_text(encoding="utf-8") == "previous protocol"
    assert not list(tmp_path.glob("*.tmp"))


def test_report_workflow_transitions_approved_task_to_finalized_and_tracks_run(tmp_path) -> None:
    engine = WorkflowEngine()
    task, workflow, loop_outcome = make_approved_loop(engine)

    outcome = ReportWorkflow(engine, ReportGenerator(tmp_path)).finalize(task.task_id, loop_outcome)

    assert outcome.final_state == TaskStatus.FINALIZED
    assert len(outcome.artifacts) == 2
    assert outcome.report_agent_result.run_id in engine.get_task_workflow(task.task_id).agent_run_ids
    states = [item.to_state for item in engine.get_transitions(workflow.workflow_run_id)]
    assert states[-2:] == [TaskStatus.FINALIZING, TaskStatus.FINALIZED]


def test_report_workflow_rejects_duplicate_artifact_types_and_fails_finalization(tmp_path) -> None:
    class DuplicateArtifactGenerator(ReportGenerator):
        def run(self, request: AgentRunRequest) -> AgentResult:
            artifacts = [
                Artifact(
                    task_id=request.task_id,
                    workflow_run_id=request.workflow_run_id,
                    artifact_type=ArtifactType.FINAL_REPORT,
                    path=str(tmp_path / "one.md"),
                    status=ArtifactStatus.APPROVED,
                    encoding="UTF-8",
                    checksum="a" * 64,
                    created_by_run_id=request.run_id,
                ),
                Artifact(
                    task_id=request.task_id,
                    workflow_run_id=request.workflow_run_id,
                    artifact_type=ArtifactType.FINAL_REPORT,
                    path=str(tmp_path / "two.md"),
                    status=ArtifactStatus.APPROVED,
                    encoding="UTF-8",
                    checksum="b" * 64,
                    created_by_run_id=request.run_id,
                ),
            ]
            return AgentResult(
                run_id=request.run_id,
                request_id=request.request_id,
                task_id=request.task_id,
                agent_id=request.agent_id,
                agent_type=AgentType.REPORT_GENERATOR,
                status=ExecutionStatus.SUCCEEDED,
                result_type="artifacts",
                payload={"artifacts": [item.model_dump(mode="json") for item in artifacts]},
                metrics=Metrics(),
                started_at=utc_now(),
                completed_at=utc_now(),
            )

    engine = WorkflowEngine()
    task, workflow, loop_outcome = make_approved_loop(engine)

    outcome = ReportWorkflow(engine, DuplicateArtifactGenerator(tmp_path)).finalize(task.task_id, loop_outcome)

    assert outcome.final_state == TaskStatus.FAILED
    assert {item.artifact_type for item in outcome.artifacts} == {ArtifactType.FINAL_REPORT}
    states = [item.to_state for item in engine.get_transitions(workflow.workflow_run_id)]
    assert states[-2:] == [TaskStatus.FINALIZING, TaskStatus.FAILED]
