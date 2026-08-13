from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
import yaml

from config import ConfigurationError, RuntimeSecrets, load_configuration
from observability import OperationalLogContext, OperationalLogger, SensitiveDataRedactor
from scripts.run_research import main as cli_main


ROOT = Path(__file__).resolve().parents[1]
TRACKED_SETTINGS = ROOT / "config" / "settings.yaml"


def test_redactor_removes_configured_secrets_sensitive_fields_and_private_reasoning() -> None:
    redactor = SensitiveDataRedactor(
        [
            "configured-secret-value",
            "postgresql://db-user:db-pass@example.test/db",
        ]
    )
    payload = {
        "safe": "visible",
        "openai_api_key": "sk-should-never-appear",
        "input_tokens": 123,
        "nested": {
            "authorization": "Bearer very-secret-token",
            "chain_of_thought": "private reasoning text",
        },
        "message": (
            "configured-secret-value password=hunter2 "
            "https://alice:secret@example.test/path sk-abcdefghijk12345"
        ),
    }

    redacted = redactor.redact(payload)
    serialized = json.dumps(redacted)

    assert redacted["safe"] == "visible"
    assert redacted["input_tokens"] == 123
    assert redacted["openai_api_key"] == "[REDACTED]"
    assert redacted["nested"]["authorization"] == "[REDACTED]"
    assert redacted["nested"]["chain_of_thought"] == "[REDACTED_PRIVATE_REASONING]"
    assert "configured-secret-value" not in serialized
    assert "hunter2" not in serialized
    assert "alice:secret" not in serialized
    assert "sk-abcdefghijk12345" not in serialized
    assert "private reasoning text" not in serialized


def test_operational_logger_writes_jsonl_with_stable_context_and_redaction(tmp_path: Path) -> None:
    configuration = load_configuration(TRACKED_SETTINGS, env_path=None, environ={})
    settings = configuration.settings.logging.model_copy(
        update={"directory": str(tmp_path), "console_enabled": False}
    )
    secrets = RuntimeSecrets(
        openai_api_key="configured-secret-value",
        search_api_key="search-secret-value",
    )
    logger = OperationalLogger(settings, secrets=secrets)

    logger.info(
        "agent_run_completed",
        context=OperationalLogContext(
            task_id="TASK_ABC123",
            workflow_run_id="WF_ABC123",
            run_id="RUN_ABC123",
            agent_id="AGENT_ABC123",
            request_id="REQUEST_ABC123",
        ),
        details={
            "execution_status": "SUCCEEDED",
            "input_tokens": 100,
            "error": "OPENAI_API_KEY=configured-secret-value",
            "scratchpad": "never persist this",
        },
    )

    lines = logger.file_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["event"] == "agent_run_completed"
    assert record["task_id"] == "TASK_ABC123"
    assert record["workflow_run_id"] == "WF_ABC123"
    assert record["run_id"] == "RUN_ABC123"
    assert record["agent_id"] == "AGENT_ABC123"
    assert record["request_id"] == "REQUEST_ABC123"
    assert record["details"]["input_tokens"] == 100
    assert record["details"]["scratchpad"] == "[REDACTED_PRIVATE_REASONING]"
    assert "configured-secret-value" not in lines[0]
    assert "search-secret-value" not in lines[0]
    assert "never persist this" not in lines[0]


def test_log_level_filter_suppresses_lower_priority_events(tmp_path: Path) -> None:
    configuration = load_configuration(TRACKED_SETTINGS, env_path=None, environ={})
    settings = configuration.settings.logging.model_copy(
        update={
            "directory": str(tmp_path),
            "console_enabled": False,
            "level": "WARNING",
        }
    )
    logger = OperationalLogger(settings)

    logger.info("suppressed")
    logger.warning("written")

    records = [
        json.loads(line)
        for line in logger.file_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [record["event"] for record in records] == ["written"]


def test_logging_redaction_is_a_system_invariant(tmp_path: Path) -> None:
    data = yaml.safe_load(TRACKED_SETTINGS.read_text(encoding="utf-8"))
    data["logging"]["redact_secrets"] = False
    path = tmp_path / "settings.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(ConfigurationError, match="logging.redact_secrets"):
        load_configuration(path, env_path=None, environ={})


def test_cli_emits_structured_operational_log_without_task_content(tmp_path: Path) -> None:
    sentence = "Software architecture evidence supports deterministic workflow behavior."
    corpus = tmp_path / "corpus.json"
    documents = []
    for index in range(2):
        documents.append(
            {
                "url": f"https://source-{index + 1}.example/evidence",
                "title": f"Evidence source {index + 1}",
                "publisher": f"Publisher {index + 1}",
                "snippet": sentence,
                "publication_date": date.today().isoformat(),
                "source_type": "OFFICIAL",
                "reliability_class": "A",
                "primary_source": True,
                "independence_group": f"group-{index + 1}",
                "content": f"{sentence} Independent details {index + 1}.",
            }
        )
    corpus.write_text(json.dumps({"documents": documents}), encoding="utf-8")

    data = yaml.safe_load(TRACKED_SETTINGS.read_text(encoding="utf-8"))
    data["logging"]["directory"] = str(tmp_path / "logs")
    data["logging"]["console_enabled"] = False
    data["reports"]["output_directory"] = str(tmp_path / "output")
    data["persistence"]["path"] = str(tmp_path / "runtime.db")
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    task_text = "Explain software architecture behavior."
    exit_code = cli_main(
        [
            "--task",
            task_text,
            "--corpus",
            str(corpus),
            "--settings",
            str(settings_path),
            "--env-file",
            str(tmp_path / "missing.env"),
            "--approve-profile",
        ]
    )

    assert exit_code == 0
    log_path = tmp_path / "logs" / "k_supervisor.jsonl"
    records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    events = [record["event"] for record in records]
    assert "task_prepared" in events
    assert "profile_approved" in events
    assert "autonomous_execution_started" in events
    assert "agent_run_completed" in events
    assert "workflow_completed" in events
    assert task_text not in log_path.read_text(encoding="utf-8")

    agent_records = [record for record in records if record["event"] == "agent_run_completed"]
    assert agent_records
    for record in agent_records:
        assert record["task_id"].startswith("TASK_")
        assert record["workflow_run_id"].startswith("WF_")
        assert record["run_id"].startswith("RUN_")
        assert record["agent_id"].startswith("AGENT_")
        assert record["request_id"].startswith("REQUEST_")
