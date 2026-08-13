from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from models import ApprovalDecision, ProfileStatus, TaskStatus
from scripts.run_research import main as cli_main
from supervisor import KSupervisorApplication, MVPStatus, ProfileStateError
from tools import JsonCorpusProvider, ResearchToolset, WebFetchTool, WebSearchTool


def write_corpus(
    root: Path,
    *,
    source_type: str,
    sentence: str,
    count: int = 2,
) -> Path:
    documents = []
    for index in range(count):
        documents.append(
            {
                "url": f"https://source-{index + 1}.example/evidence",
                "title": f"Evidence source {index + 1}",
                "publisher": f"Publisher {index + 1}",
                "snippet": sentence,
                "publication_date": date.today().isoformat(),
                "source_type": source_type,
                "reliability_class": "A",
                "primary_source": True,
                "independence_group": f"group-{index + 1}",
                "content": f"{sentence} Supporting details from independent source {index + 1}.",
            }
        )
    path = root / f"corpus-{source_type.lower()}-{count}.json"
    path.write_text(json.dumps({"documents": documents}), encoding="utf-8")
    return path


def build_app(
    tmp_path: Path,
    *,
    source_type: str = "OFFICIAL",
    sentence: str = "Independent evidence supports the requested research conclusion.",
    count: int = 2,
    max_iterations: int = 3,
) -> tuple[KSupervisorApplication, Path]:
    corpus = write_corpus(
        tmp_path,
        source_type=source_type,
        sentence=sentence,
        count=count,
    )
    provider = JsonCorpusProvider.from_file(corpus)
    tools = ResearchToolset(WebSearchTool(provider), WebFetchTool(provider))
    app = KSupervisorApplication(
        tools,
        output_directory=tmp_path / "output",
        default_max_iterations=max_iterations,
    )
    return app, corpus


@pytest.mark.parametrize(
    ("task_text", "source_type", "sentence", "primary_domain", "secondary_domains"),
    [
        (
            "Analyze the literary novel and its central theme.",
            "PRIMARY_DOCUMENT",
            "Literary novel evidence supports the central theme interpretation.",
            "literary_analysis",
            [],
        ),
        (
            "Explain current medical treatment evidence for a patient.",
            "OFFICIAL",
            "Current medical treatment evidence supports the stated patient-care conclusion.",
            "medicine",
            [],
        ),
        (
            "Assess GNSS RTK coordinate accuracy for geodetic surveying.",
            "STANDARD",
            "GNSS RTK coordinate accuracy evidence supports the geodetic surveying conclusion.",
            "geodesy",
            [],
        ),
        (
            "Assess structural building deformation monitoring with GNSS RTK coordinates.",
            "STANDARD",
            "Structural building deformation monitoring with GNSS RTK coordinates is supported by the evidence.",
            "construction",
            ["geodesy"],
        ),
    ],
)
def test_primary_phase9_scenarios_reach_finalized_artifacts(
    tmp_path: Path,
    task_text: str,
    source_type: str,
    sentence: str,
    primary_domain: str,
    secondary_domains: list[str],
) -> None:
    app, _ = build_app(tmp_path, source_type=source_type, sentence=sentence)
    prepared = app.prepare_task(task_text)

    assert prepared.domain_assessment.primary_domain == primary_domain
    assert prepared.domain_assessment.secondary_domains == secondary_domains
    assert prepared.task.status == TaskStatus.PROFILE_REVIEW_REQUIRED

    app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")
    outcome = app.run_to_completion(prepared.task.task_id)

    assert outcome.status == MVPStatus.SUCCESS
    assert outcome.final_state == TaskStatus.FINALIZED
    assert len(outcome.artifact_paths) == 2
    for artifact_path in outcome.artifact_paths:
        assert Path(artifact_path).exists()
        text = Path(artifact_path).read_text(encoding="utf-8")
        assert prepared.task.task_id in text


def test_autonomous_execution_is_blocked_until_explicit_profile_approval(tmp_path: Path) -> None:
    app, _ = build_app(tmp_path)
    prepared = app.prepare_task("Explain software architecture behavior.")

    with pytest.raises(ProfileStateError):
        app.run_to_completion(prepared.task.task_id)

    assert prepared.task.status == TaskStatus.PROFILE_REVIEW_REQUIRED


def test_user_can_edit_and_approve_profile_at_the_defined_boundary(tmp_path: Path) -> None:
    app, _ = build_app(tmp_path)
    prepared = app.prepare_task("Explain software architecture behavior.")

    profile, approval = app.approve_profile(
        prepared.task.task_id,
        approved_by="TEST_USER",
        edits={"critic_role": "Independent edited software reviewer"},
    )

    assert profile.status == ProfileStatus.APPROVED
    assert profile.critic_role == "Independent edited software reviewer"
    assert approval.decision == ApprovalDecision.EDITED_AND_APPROVED


def test_forced_max_iterations_produces_explicit_limitation_artifacts(tmp_path: Path) -> None:
    app, _ = build_app(
        tmp_path,
        source_type="OFFICIAL",
        sentence="Software architecture evidence supports the requested conclusion.",
        count=1,
        max_iterations=1,
    )
    prepared = app.prepare_task("Explain software architecture.", max_iterations=1)
    app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    outcome = app.run_to_completion(prepared.task.task_id)

    assert outcome.status == MVPStatus.LIMITATION
    assert outcome.final_state == TaskStatus.COMPLETED_WITH_LIMITATIONS
    assert len(outcome.artifact_paths) == 2
    for artifact_path in outcome.artifact_paths:
        text = Path(artifact_path).read_text(encoding="utf-8")
        assert "COMPLETED_WITH_LIMITATIONS" in text


class FailingTools:
    def web_search(self, query: str, *, limit: int):
        raise RuntimeError("forced search failure")

    def web_fetch(self, url: str):
        raise AssertionError("fetch must not be called after total search failure")


def test_tool_failure_terminates_end_to_end_workflow_explicitly(tmp_path: Path) -> None:
    app = KSupervisorApplication(FailingTools(), output_directory=tmp_path / "output")
    prepared = app.prepare_task("Explain software architecture failure handling.")
    app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    outcome = app.run_to_completion(prepared.task.task_id)

    assert outcome.status == MVPStatus.FAILURE
    assert outcome.final_state == TaskStatus.FAILED
    assert outcome.report_outcome is None
    assert outcome.artifact_paths == ()


def test_material_profile_amendment_returns_to_user_gate_then_resumes(tmp_path: Path) -> None:
    app, _ = build_app(
        tmp_path,
        source_type="STANDARD",
        sentence="GNSS RTK coordinate accuracy evidence supports the geodetic conclusion.",
    )
    prepared = app.prepare_task("Assess GNSS RTK coordinate accuracy for geodetic surveying.")
    original, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    amendment = app.propose_profile_amendment(
        prepared.task.task_id,
        changes={"critic_role": "Independent amended geodesy reviewer"},
        reason="Material reviewer-role clarification discovered before autonomous execution",
    )

    assert amendment.status == ProfileStatus.REVIEW_REQUIRED
    assert amendment.version == original.version + 1
    assert amendment.supersedes_profile_id == original.profile_id
    assert prepared.task.status == TaskStatus.PROFILE_REVIEW_REQUIRED
    assert prepared.task.active_profile_id == original.profile_id

    approved_amendment, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")
    assert prepared.task.active_profile_id == approved_amendment.profile_id

    outcome = app.run_to_completion(prepared.task.task_id)
    assert outcome.status == MVPStatus.SUCCESS
    assert outcome.final_state == TaskStatus.FINALIZED


def test_json_corpus_search_order_is_repeatable(tmp_path: Path) -> None:
    corpus = write_corpus(
        tmp_path,
        source_type="OFFICIAL",
        sentence="Software architecture evidence supports deterministic workflow behavior.",
    )
    provider = JsonCorpusProvider.from_file(corpus)

    first = [item.url for item in provider.search("software architecture", limit=10)]
    second = [item.url for item in provider.search("software architecture", limit=10)]

    assert first == second


def test_cli_non_interactive_explicit_approval_runs_complete_mvp(tmp_path: Path) -> None:
    corpus = write_corpus(
        tmp_path,
        source_type="OFFICIAL",
        sentence="Software architecture evidence supports deterministic workflow behavior.",
    )
    output = tmp_path / "cli-output"

    exit_code = cli_main(
        [
            "--task",
            "Explain software architecture behavior.",
            "--corpus",
            str(corpus),
            "--output-directory",
            str(output),
            "--approve-profile",
        ]
    )

    assert exit_code == 0
    assert len(list(output.glob("*_FINAL_REPORT.md"))) == 1
    assert len(list(output.glob("*_REVIEW_PROTOCOL.md"))) == 1
