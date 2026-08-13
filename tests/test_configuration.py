from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from config import ConfigurationError, load_configuration


ROOT = Path(__file__).resolve().parents[1]
TRACKED_SETTINGS = ROOT / "config" / "settings.yaml"


def write_settings(tmp_path: Path, mutate=None) -> Path:
    data = yaml.safe_load(TRACKED_SETTINGS.read_text(encoding="utf-8"))
    if mutate is not None:
        mutate(data)
    path = tmp_path / "settings.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_tracked_settings_load_into_frozen_validated_schema() -> None:
    loaded = load_configuration(TRACKED_SETTINGS, env_path=None, environ={})

    assert loaded.settings.schema_version == "1.0"
    assert loaded.settings.environment == "development"
    assert loaded.settings.workflow.max_iterations == 3
    assert loaded.settings.persistence.backend == "sqlite"
    assert loaded.settings.persistence.path == "runtime/k_supervisor.db"
    assert loaded.settings.distribution.primary_channel == "chatgpt_store"
    assert loaded.settings.distribution.free_user_compatible is True
    assert loaded.settings.distribution.developer_api_key_required is False
    assert loaded.settings.distribution.model_policy == "user_plan"
    assert loaded.settings.distribution.recommended_model is None
    assert loaded.settings.distribution.allow_user_model_switch is True
    assert loaded.settings.distribution.external_backend_required is False
    assert len(loaded.fingerprint) == 64

    with pytest.raises(Exception):
        loaded.settings.workflow.max_iterations = 4


def test_environment_selection_overrides_tracked_default_without_mutating_file() -> None:
    loaded = load_configuration(
        TRACKED_SETTINGS,
        env_path=None,
        environ={"K_SUPERVISOR_ENV": "test"},
    )

    assert loaded.settings.environment == "test"
    assert yaml.safe_load(TRACKED_SETTINGS.read_text(encoding="utf-8"))["environment"] == "development"


def test_env_file_secrets_load_and_process_environment_has_precedence(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "K_SUPERVISOR_ENV=production\nOPENAI_API_KEY=file-secret\nSEARCH_API_KEY=file-search\n",
        encoding="utf-8",
    )

    loaded = load_configuration(
        TRACKED_SETTINGS,
        env_path=env_file,
        environ={"K_SUPERVISOR_ENV": "test", "OPENAI_API_KEY": "process-secret"},
    )

    assert loaded.settings.environment == "test"
    assert loaded.secrets.openai_api_key is not None
    assert loaded.secrets.openai_api_key.get_secret_value() == "process-secret"
    assert loaded.secrets.search_api_key is not None
    assert loaded.secrets.search_api_key.get_secret_value() == "file-search"
    assert "process-secret" not in loaded.secrets.model_dump_json()
    assert "file-search" not in loaded.secrets.model_dump_json()


def test_gpt_store_defaults_need_no_runtime_secret() -> None:
    loaded = load_configuration(TRACKED_SETTINGS, env_path=None, environ={})

    assert loaded.settings.distribution.primary_channel == "chatgpt_store"
    assert loaded.secrets.openai_api_key is None
    assert loaded.secrets.search_api_key is None
    assert loaded.secrets.database_url is None


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("free_user_compatible", False, "free_user_compatible"),
        ("developer_api_key_required", True, "developer API key"),
        ("model_policy", "configured_api", "model_policy=user_plan"),
        ("recommended_model", "pinned-model", "must not pin"),
        ("allow_user_model_switch", False, "allow user model switching"),
        ("external_backend_required", True, "external backend"),
    ],
)
def test_gpt_store_distribution_invariants_are_enforced(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    def mutate(data):
        data["distribution"][field] = value

    path = write_settings(tmp_path, mutate)

    with pytest.raises(ConfigurationError, match=message):
        load_configuration(path, env_path=None, environ={})


def test_unknown_configuration_fields_are_rejected(tmp_path: Path) -> None:
    path = write_settings(tmp_path, lambda data: data.__setitem__("unexpected", True))

    with pytest.raises(ConfigurationError, match="Configuration validation failed"):
        load_configuration(path, env_path=None, environ={})


def test_system_approval_invariants_cannot_be_disabled(tmp_path: Path) -> None:
    def mutate(data):
        data["workflow"]["require_profile_approval"] = False

    path = write_settings(tmp_path, mutate)

    with pytest.raises(ConfigurationError, match="require_profile_approval"):
        load_configuration(path, env_path=None, environ={})


def test_semantic_resolver_requires_configured_provider_and_model(tmp_path: Path) -> None:
    def mutate(data):
        data["resolver"]["semantic_enabled"] = True

    path = write_settings(tmp_path, mutate)

    with pytest.raises(ConfigurationError, match="semantic resolver requires"):
        load_configuration(path, env_path=None, environ={})


def test_research_source_limit_cannot_exceed_global_limit(tmp_path: Path) -> None:
    def mutate(data):
        data["research"]["max_sources"] = data["limits"]["max_sources"] + 1

    path = write_settings(tmp_path, mutate)

    with pytest.raises(ConfigurationError, match="research.max_sources"):
        load_configuration(path, env_path=None, environ={})


def test_missing_or_non_mapping_settings_fail_explicitly(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError, match="Cannot read settings file"):
        load_configuration(tmp_path / "missing.yaml", env_path=None, environ={})

    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="Settings root must be a YAML mapping"):
        load_configuration(invalid, env_path=None, environ={})
