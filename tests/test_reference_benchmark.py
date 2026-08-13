from __future__ import annotations

import json
from pathlib import Path

import pytest

from models import TaskStatus
from supervisor import KSupervisorApplication, MVPStatus
from tools import JsonCorpusProvider, ResearchToolset, WebFetchTool, WebSearchTool


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = ROOT / "examples" / "reference_benchmark.json"
BENCHMARK = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
REFERENCE_TASKS = BENCHMARK["tasks"]


def test_reference_benchmark_manifest_is_well_formed() -> None:
    assert BENCHMARK["schema_version"] == "1.0"
    assert len(REFERENCE_TASKS) >= 3
    assert len(BENCHMARK["documents"]) >= len(REFERENCE_TASKS) * 2

    benchmark_ids = [case["benchmark_id"] for case in REFERENCE_TASKS]
    assert len(benchmark_ids) == len(set(benchmark_ids))

    independence_groups = [document["independence_group"] for document in BENCHMARK["documents"]]
    assert len(independence_groups) == len(set(independence_groups))


@pytest.mark.parametrize("case", REFERENCE_TASKS, ids=lambda case: case["benchmark_id"])
def test_reference_benchmark_tasks_meet_regression_floor(tmp_path: Path, case: dict[str, object]) -> None:
    provider = JsonCorpusProvider.from_file(BENCHMARK_PATH)
    tools = ResearchToolset(WebSearchTool(provider), WebFetchTool(provider))
    max_iterations = int(case["max_iterations"])
    app = KSupervisorApplication(
        tools,
        output_directory=tmp_path / str(case["benchmark_id"]),
        default_max_iterations=max_iterations,
    )

    prepared = app.prepare_task(str(case["request"]), max_iterations=max_iterations)
    assert prepared.domain_assessment.primary_domain == case["expected_domain"]

    approved_profile, _ = app.approve_profile(prepared.task.task_id, approved_by="REFERENCE_BENCHMARK")
    outcome = app.run_to_completion(
        prepared.task.task_id,
        research_constraints=dict(case["research_constraints"]),
    )

    assert outcome.status == MVPStatus(str(case["expected_status"]))
    assert outcome.final_state == TaskStatus.FINALIZED
    assert len(outcome.loop_outcome.iterations) == int(case["expected_iterations"])

    research = outcome.loop_outcome.last_research_result
    review = outcome.loop_outcome.last_review
    assert research is not None
    assert review is not None
    assert len(research.sources) >= int(case["minimum_sources"])
    assert len(research.claims) >= int(case["minimum_claims"])
    assert review.reliability_score >= float(case["minimum_reliability_score"])
    assert review.reliability_score >= approved_profile.confidence_threshold
    assert review.decision.value == "PASS"
    assert not review.critical_issues
    assert not review.unsupported_claim_ids
    assert not review.contradictions
    assert not review.unresolved_claim_ids

    assert len(outcome.artifact_paths) == 2
    final_report_path = next(Path(path) for path in outcome.artifact_paths if path.endswith("_FINAL_REPORT.md"))
    review_protocol_path = next(
        Path(path) for path in outcome.artifact_paths if path.endswith("_REVIEW_PROTOCOL.md")
    )
    final_report = final_report_path.read_text(encoding="utf-8")
    review_protocol = review_protocol_path.read_text(encoding="utf-8")

    assert prepared.task.task_id in final_report
    assert "## Evidence-backed Claims" in final_report
    assert "## Sources" in final_report
    assert prepared.task.task_id in review_protocol
    assert "Critic decision: PASS" in review_protocol
    assert "## Audit Note" in review_protocol
    assert "Hidden chain-of-thought and private model reasoning are not included." in review_protocol
