from models import Claim, ClaimType, IdPrefix, ImportanceLevel, ResearchResult, VerificationStatus, generate_id


def test_research_result_populates_canonical_ids_and_change_log() -> None:
    task_id = generate_id(IdPrefix.TASK)
    run_id = generate_id(IdPrefix.RUN)
    result = ResearchResult(
        task_id=task_id,
        run_id=run_id,
        iteration=2,
        summary="Updated summary",
        findings=["Updated finding"],
        draft_report="Draft report",
        changes_applied=["Research plan targeted critic feedback: verify evidence"],
    )

    assert result.research_result_id.startswith("RESEARCH_RESULT_")
    assert result.claim_ids == []
    assert result.source_ids == []
    assert result.change_log == result.changes_applied
    assert result.limitations == []
    assert result.created_at.tzinfo is not None


def test_research_result_derives_claim_ids_from_embedded_claims() -> None:
    task_id = generate_id(IdPrefix.TASK)
    run_id = generate_id(IdPrefix.RUN)
    claim = Claim(
        task_id=task_id,
        text="A source-independent draft claim",
        claim_type=ClaimType.INTERPRETATION,
        importance=ImportanceLevel.LOW,
        source_ids=[],
        confidence=0.4,
        verification_status=VerificationStatus.UNVERIFIED,
        created_by_run_id=run_id,
    )

    result = ResearchResult(
        task_id=task_id,
        run_id=run_id,
        iteration=1,
        summary="Summary",
        claims=[claim],
        draft_report="Draft report",
    )

    assert result.claim_ids == [claim.claim_id]
