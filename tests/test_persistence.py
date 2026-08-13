from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from models import ProfileStatus, TaskStatus, WorkflowStatus
from persistence import SQLitePersistenceStore
from scripts.audit_task import main as audit_cli_main
from supervisor import KSupervisorApplication, MVPStatus
from tools import JsonCorpusProvider, ResearchToolset, WebFetchTool, WebSearchTool


def _write_corpus(path: Path) -> Path:
    sentence = "Software architecture evidence supports deterministic workflow behavior."
    documents = []
    for index in range(2):
        documents.append(
            {
                "url": f"https://persistent-source-{index + 1}.example/evidence",
                "title": f"Persistent source {index + 1}",
                "publisher": f"Publisher {index + 1}",
                "snippet": sentence,
                "publication_date": date.today().isoformat(),
                "source_type": "OFFICIAL",
                "reliability_class": "A",
                "primary_source": True,
                "independence_group": f"persistent-group-{index + 1}",
                "content": f"{sentence} Independent detail {index + 1}.",
            }
        )
    path.write_text(json.dumps({"documents": documents}), encoding="utf-8")
    return path


def _tools(tmp_path: Path):
    corpus = _write_corpus(tmp_path / "persistence-corpus.json")
    provider = JsonCorpusProvider.from_file(corpus)
    return ResearchToolset(WebSearchTool(provider), WebFetchTool(provider))


def _app(tmp_path: Path, database: Path) -> KSupervisorApplication:
    return KSupervisorApplication(
        _tools(tmp_path),
        output_directory=tmp_path / "output",
        persistence=SQLitePersistenceStore(database),
    )


def test_sqlite_store_creates_phase10_schema(tmp_path: Path) -> None:
    store = SQLitePersistenceStore(tmp_path / "audit.db")

    assert store.schema_version() == "1"
    assert {
        "tasks",
        "workflow_runs",
        "state_transitions",
        "agent_runs",
        "domain_assessments",
        "critic_profiles",
        "user_approvals",
        "research_results",
        "claims",
        "sources",
        "reviews",
        "artifacts",
    }.issubset(set(store.table_names()))


def test_approved_profile_round_trips_exactly_after_restart(tmp_path: Path) -> None:
    database = tmp_path / "audit.db"
    app = _app(tmp_path, database)
    prepared = app.prepare_task("Explain software architecture behavior.")
    approved, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    reopened = SQLitePersistenceStore(database)
    restored_task = reopened.load_task(prepared.task.task_id)
    profiles = reopened.load_critic_profiles(prepared.task.task_id)
    restored_profile = next(item for item in profiles if item.profile_id == approved.profile_id)

    assert restored_task.active_profile_id == approved.profile_id
    assert restored_profile.status == ProfileStatus.APPROVED
    assert restored_profile.model_dump(mode="json") == approved.model_dump(mode="json")


def test_completed_task_is_fully_auditable_after_restart(tmp_path: Path) -> None:
    database = tmp_path / "audit.db"
    app = _app(tmp_path, database)
    prepared = app.prepare_task("Explain software architecture behavior.")
    app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    outcome = app.run_to_completion(prepared.task.task_id)
    assert outcome.status == MVPStatus.SUCCESS

    reopened = SQLitePersistenceStore(database)
    audit = reopened.load_task_audit(prepared.task.task_id)

    assert audit.task.status == TaskStatus.FINALIZED
    assert audit.workflow_run is not None
    assert audit.workflow_run.status == WorkflowStatus.SUCCEEDED
    assert len(audit.transitions) >= 8
    assert len(audit.critic_profiles) >= 1
    assert len(audit.user_approvals) == 1
    assert len(audit.agent_results) >= 3
    assert len(audit.research_results) >= 1
    assert len(audit.claims) >= 1
    assert len(audit.sources) >= 1
    assert len(audit.reviews) >= 1
    assert len(audit.artifacts) == 2


def test_recovery_restores_waiting_for_user_then_continues(tmp_path: Path) -> None:
    database = tmp_path / "audit.db"
    first = _app(tmp_path, database)
    prepared = first.prepare_task("Explain software architecture behavior.")

    second = _app(tmp_path, database)
    recovery = second.recover_task(prepared.task.task_id)

    assert recovery.resumable is True
    assert recovery.task.status == TaskStatus.PROFILE_REVIEW_REQUIRED
    pending = second.profile_workflow.profile_manager.get_pending_profile(prepared.task.task_id)
    assert pending.profile_id == prepared.critic_profile.profile_id

    second.approve_profile(prepared.task.task_id, approved_by="RECOVERED_USER")
    outcome = second.run_to_completion(prepared.task.task_id)

    assert outcome.status == MVPStatus.SUCCESS
    assert outcome.final_state == TaskStatus.FINALIZED


def test_recovery_restores_approved_task_then_continues(tmp_path: Path) -> None:
    database = tmp_path / "audit.db"
    first = _app(tmp_path, database)
    prepared = first.prepare_task("Explain software architecture behavior.")
    approved, _ = first.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    second = _app(tmp_path, database)
    recovery = second.recover_task(prepared.task.task_id)

    assert recovery.resumable is True
    assert recovery.task.status == TaskStatus.PROFILE_APPROVED
    restored = second.profile_workflow.profile_manager.get_profile(approved.profile_id)
    assert restored.model_dump(mode="json") == approved.model_dump(mode="json")

    outcome = second.run_to_completion(prepared.task.task_id)
    assert outcome.status == MVPStatus.SUCCESS


def test_persistence_upserts_are_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "audit.db"
    app = _app(tmp_path, database)
    prepared = app.prepare_task("Explain software architecture behavior.")
    store = SQLitePersistenceStore(database)

    task = store.load_task(prepared.task.task_id)
    store.save_task(task)
    store.save_task(task)

    assert store.count_records("tasks") == 1


def test_audit_cli_reads_completed_task_after_restart(tmp_path: Path, capsys) -> None:
    database = tmp_path / "audit.db"
    app = _app(tmp_path, database)
    prepared = app.prepare_task("Explain software architecture behavior.")
    app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")
    app.run_to_completion(prepared.task.task_id)

    exit_code = audit_cli_main(
        ["--task-id", prepared.task.task_id, "--database", str(database)]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Task state: FINALIZED" in output
    assert "Artifacts: 2" in output


def test_agent_business_logic_does_not_depend_on_sqlite(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    agent_files = sorted((root / "agents").glob("*.py"))
    assert agent_files
    for path in agent_files:
        assert "sqlite3" not in path.read_text(encoding="utf-8")
