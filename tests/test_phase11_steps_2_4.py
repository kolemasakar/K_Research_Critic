from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents import Agent
from config import (
    AppSettings,
    LoadedConfiguration,
    RuntimeSecrets,
    latest_task_configuration_snapshot,
    load_configuration,
)
from models import (
    AgentDefinition,
    AgentResult,
    AgentRunRequest,
    AgentType,
    ExecutionStatus,
    Metrics,
    Task,
    utc_now,
)
from models.identifiers import generate_id
from persistence import SQLitePersistenceStore
from providers import OpenAISemanticDomainProvider
from supervisor import KSupervisorApplication, build_domain_resolver
from supervisor.hybrid_resolver import HybridResolver
from supervisor.runtime_limits import OutputBoundedReportGenerator
from tools import (
    RuntimeControlledResearchTools,
    RuntimeToolPolicy,
    SearchHit,
    ToolExecutionError,
)


ROOT = Path(__file__).resolve().parents[1]
TRACKED_SETTINGS = ROOT / "config" / "settings.yaml"


class NoopTools:
    def web_search(self, query: str, *, limit: int):
        return []

    def web_fetch(self, url: str):
        raise RuntimeError("not used")


class FlakyTools:
    def __init__(self) -> None:
        self.search_attempts = 0

    def web_search(self, query: str, *, limit: int):
        self.search_attempts += 1
        if self.search_attempts == 1:
            raise ToolExecutionError(
                "TRANSIENT",
                "temporary",
                operation="web_search",
                retryable=True,
            )
        return [SearchHit(url="https://example.org/source", title="Source")]

    def web_fetch(self, url: str):
        raise RuntimeError("not used")


class FakeReportAgent(Agent):
    def __init__(self, artifact_path: Path) -> None:
        self.artifact_path = artifact_path
        self._definition = AgentDefinition(
            agent_type=AgentType.REPORT_GENERATOR,
            name="FakeReportAgent",
            version="1.0",
            produced_output_types=["artifacts"],
        )

    @property
    def definition(self) -> AgentDefinition:
        return self._definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        started = utc_now()
        self.artifact_path.write_text("0123456789", encoding="utf-8")
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.REPORT_GENERATOR,
            status=ExecutionStatus.SUCCEEDED,
            result_type="artifacts",
            payload={"artifacts": [{"path": str(self.artifact_path)}]},
            metrics=Metrics(),
            started_at=started,
            completed_at=utc_now(),
        )


def _loaded_configuration(*, secret: str | None = None) -> LoadedConfiguration:
    environ = {"OPENAI_API_KEY": secret} if secret is not None else {}
    return load_configuration(TRACKED_SETTINGS, env_path=None, environ=environ)


def _semantic_configuration(*, with_secret: bool = True) -> LoadedConfiguration:
    base = _loaded_configuration()
    raw = base.settings.model_dump(mode="python")
    raw["resolver"]["semantic_enabled"] = True
    raw["models"]["domain_resolver"]["provider"] = "openai"
    raw["models"]["domain_resolver"]["model"] = "gpt-5-mini"
    raw["models"]["domain_resolver"]["reasoning_level"] = "low"
    settings = AppSettings.model_validate(raw)
    return LoadedConfiguration(
        settings=settings,
        secrets=RuntimeSecrets(openai_api_key="test-key" if with_secret else None),
        settings_path=TRACKED_SETTINGS,
        env_path=None,
    )


def test_configuration_snapshot_is_frozen_secret_free_and_restart_safe(tmp_path: Path) -> None:
    configuration = _loaded_configuration(secret="super-secret")
    database = tmp_path / "audit.db"
    app = KSupervisorApplication(
        NoopTools(),
        output_directory=tmp_path / "output",
        default_max_iterations=2,
        persistence=SQLitePersistenceStore(database),
        configuration=configuration,
    )
    prepared = app.prepare_task("Explain software architecture behavior.", max_iterations=2)
    approved, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")

    snapshot = app.configuration_snapshot(prepared.task.task_id)
    assert snapshot is not None
    assert snapshot.approved_profile_id == approved.profile_id
    assert snapshot.approved_profile_version == approved.version
    assert snapshot.effective_settings.workflow.max_iterations == 2
    assert str(tmp_path / "output") == snapshot.effective_settings.reports.output_directory
    assert "super-secret" not in snapshot.model_dump_json()

    with pytest.raises(Exception):
        snapshot.environment = "production"

    reopened_task = SQLitePersistenceStore(database).load_task(prepared.task.task_id)
    restored = latest_task_configuration_snapshot(reopened_task.metadata)
    assert restored == snapshot


def test_profile_amendment_creates_new_snapshot_without_changing_frozen_settings(tmp_path: Path) -> None:
    configuration = _loaded_configuration()
    app = KSupervisorApplication(
        NoopTools(),
        output_directory=tmp_path / "output",
        persistence=SQLitePersistenceStore(tmp_path / "audit.db"),
        configuration=configuration,
    )
    prepared = app.prepare_task("Explain software architecture behavior.")
    first_profile, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")
    first = app.configuration_snapshot(prepared.task.task_id)
    assert first is not None

    app.propose_profile_amendment(
        prepared.task.task_id,
        changes={"critic_role": "Independent architecture reviewer"},
        reason="Test explicit amendment",
    )
    second_profile, _ = app.approve_profile(prepared.task.task_id, approved_by="TEST_USER")
    second = app.configuration_snapshot(prepared.task.task_id)

    assert second is not None
    assert second.snapshot_id != first.snapshot_id
    assert second.supersedes_snapshot_id == first.snapshot_id
    assert second.approved_profile_id == second_profile.profile_id
    assert second_profile.profile_id != first_profile.profile_id
    assert second.effective_settings == first.effective_settings
    assert second.settings_fingerprint == first.settings_fingerprint


def test_openai_semantic_provider_uses_structured_responses_request_without_storage() -> None:
    captured: dict[str, object] = {}

    def transport(url, headers, payload, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["body"] = json.loads(payload.decode("utf-8"))
        captured["timeout"] = timeout
        result = {
            "primary_domain": "geodesy",
            "secondary_domains": ["construction"],
            "task_type": "technical_assessment",
            "risk_level": "HIGH",
            "identified_standards": ["ISO example"],
            "recommended_source_types": ["STANDARD"],
            "recommended_evaluation_criteria": ["accuracy"],
            "uncertainties": [],
            "confidence": 0.92,
        }
        return {
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": json.dumps(result)}],
                }
            ]
        }

    provider = OpenAISemanticDomainProvider(
        api_key="secret",
        model="gpt-5-mini",
        reasoning_level="low",
        max_attempts=1,
        transport=transport,
    )
    result = provider.resolve(Task(user_request="Assess GNSS RTK accuracy", task_type="auto"))

    assert result["primary_domain"] == "geodesy"
    body = captured["body"]
    assert isinstance(body, dict)
    assert body["store"] is False
    assert body["text"]["format"]["type"] == "json_schema"
    assert body["text"]["format"]["strict"] is True
    assert body["reasoning"] == {"effort": "low"}


def test_provider_factory_wires_openai_semantic_provider_and_requires_secret() -> None:
    resolver = build_domain_resolver(_semantic_configuration(with_secret=True))
    assert isinstance(resolver, HybridResolver)
    assert resolver.semantic_resolver is not None
    assert isinstance(resolver.semantic_resolver.provider, OpenAISemanticDomainProvider)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        build_domain_resolver(_semantic_configuration(with_secret=False))


def test_runtime_tool_controls_retry_and_enforce_call_budget() -> None:
    delegate = FlakyTools()
    tools = RuntimeControlledResearchTools(delegate)
    policy = RuntimeToolPolicy(
        max_search_calls=2,
        max_fetch_calls=1,
        max_runtime_seconds=5,
        search_timeout_seconds=1,
        fetch_timeout_seconds=1,
        retry_max_attempts=2,
        retry_initial_delay_seconds=0,
        retry_max_delay_seconds=0,
        retry_backoff_multiplier=1,
    )

    with tools.scope(policy) as usage:
        results = tools.web_search("architecture", limit=1)
        assert len(results) == 1
        assert usage.search_calls == 2
        assert usage.retries == 1
        with pytest.raises(ToolExecutionError, match="call limit"):
            tools.web_search("second", limit=1)


def test_output_size_limit_turns_report_result_into_explicit_failure(tmp_path: Path) -> None:
    artifact_path = tmp_path / "oversized.md"
    delegate = FakeReportAgent(artifact_path)
    bounded = OutputBoundedReportGenerator(delegate)
    request = AgentRunRequest(
        task_id=generate_id("TASK"),
        workflow_run_id=generate_id("WF"),
        agent_id=delegate.definition.agent_id,
        agent_type=AgentType.REPORT_GENERATOR,
        input={},
        context={"max_output_size_bytes": 5},
    )

    result = bounded.run(request)

    assert result.status == ExecutionStatus.FAILED
    assert result.errors[0].error_code == "MAX_OUTPUT_SIZE_EXCEEDED"
    assert not artifact_path.exists()
