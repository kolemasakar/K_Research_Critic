from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "plugins" / "krc_migration_candidate"
MATRIX = CANDIDATE / "contracts" / "surface_decision_matrix.yaml"
AUTH_BINDING = CANDIDATE / "contracts" / "auth_transport_binding.yaml"
INSPECTION = (
    ROOT
    / "subprojects"
    / "media_beta"
    / "100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md"
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_surface_matrix_treats_migration_as_state_changing() -> None:
    matrix = load_yaml(MATRIX)
    principles = matrix["principles"]
    assert principles["migration_button_is_state_changing"] is True
    assert principles["migrate_requires_separate_owner_approval"] is True
    assert principles["preserve_public_gpt_until_replacement_regression_accepted"] is True
    assert principles["fail_closed_on_unknown_permissions"] is True

    observations = matrix["migration_observations"]
    assert observations["custom_actions_auto_transfer"] is False
    assert observations["original_gpt_after_migration"] == "READ_ONLY_UNTIL_RETIREMENT"
    assert observations["replacement_plugin_initial_access"] == "PRIVATE_UNTIL_SHARED"


def test_surface_matrix_requires_execution_capability_for_full_media_parity() -> None:
    matrix = load_yaml(MATRIX)
    required = matrix["required_krc_capabilities"]
    assert required["media_operation_count"] == 13
    assert required["media_execution_required"] is True

    assert set(required["execution_operations"]) == {
        "startPublicGeminiYoutubeTranscription",
        "startPublicInstagramCobaltTranscription",
        "startPublicFacebookCobaltTranscription",
        "startPublicTelegramTranscription",
    }

    principles = matrix["principles"]
    assert principles["read_fetch_only_is_insufficient_for_full_media_parity"] is True

    mcp = next(surface for surface in matrix["surfaces"] if surface["id"] == "custom_remote_mcp")
    assert "account only permits read_fetch MCP" in mcp["reject_if_any"]


def test_surface_matrix_has_fail_closed_release_boundary() -> None:
    boundary = load_yaml(MATRIX)["release_boundary"]
    assert boundary == {
        "public_gpt_mutation": "DENIED",
        "migration_execution": "DENIED",
        "plugin_installation": "DENIED",
        "plugin_publication": "DENIED",
        "live_mcp_creation": "DENIED",
        "render_change": "DENIED",
        "main_mutation": "DENIED",
        "pr22_merge": "DENIED",
        "pr45_merge": "DENIED",
    }


def test_auth_binding_preserves_13_operation_and_four_execution_boundary() -> None:
    binding = load_yaml(AUTH_BINDING)
    assert binding["backend"]["operation_count"] == 13
    assert binding["backend"]["backend_api_change_required_for_design"] is False
    assert binding["backend"]["render_change_required_for_design"] is False

    execution = binding["execution_boundary"]
    assert execution["execution_required"] is True
    assert execution["read_fetch_only_surface_accepted_for_full_binding"] is False
    assert len(execution["execution_operations"]) == 4
    assert len(execution["read_only_operations"]) == 7
    assert len(execution["preflight_operations"]) == 2


def test_auth_binding_is_transport_neutral_and_server_side_secret_only() -> None:
    binding = load_yaml(AUTH_BINDING)
    transport = binding["transport_contract"]
    assert transport["final_transport"] == "TBD_AFTER_SURFACE_INSPECTION"
    assert transport["local_mcp_direct_dependency"] is False
    assert transport["client_desktop_dependency_allowed_by_default"] is False
    assert transport["automatic_transport_retry"] is False

    credentials = binding["credentials"]
    assert credentials["final_auth_method"] == "TBD_AFTER_SURFACE_INSPECTION"
    assert credentials["model_visible_secret"] is False
    assert credentials["repository_secret"] is False
    assert "secret_in_skill_text" in credentials["forbidden_patterns"]
    assert "secret_in_model_visible_arguments" in credentials["forbidden_patterns"]
    assert "secret_in_non_secret_sentinel_evidence" in credentials["forbidden_patterns"]


def test_auth_binding_preserves_consent_retry_and_error_safety() -> None:
    binding = load_yaml(AUTH_BINDING)
    consent = binding["consent"]
    assert consent["youtube_preflight_must_not_call_provider"] is True
    assert consent["youtube_execution_requires_explicit_user_acknowledgement"] is True
    assert consent["consent_must_not_be_inferred_from_plugin_installation"] is True

    retry = binding["retry_idempotency"]
    assert retry["completed"] == "REUSE"
    assert retry["processing"] == "REUSE_AND_CONCURRENCY_PROTECT"
    assert retry["failed_free_only"] == "FRESH_DETERMINISTIC_JOB_ON_NEW_EXPLICIT_RETRY_REQUEST"
    assert retry["failed_paid_or_charge_uncertain"] == "BLOCK"
    assert retry["automatic_retry_loop"] is False

    errors = binding["errors"]
    assert errors["structured_error_required"] is True
    assert errors["credential_sanitization_required"] is True
    assert errors["media_failure_blocks_core"] is False


def test_sentinel_package_is_strictly_read_only() -> None:
    text = INSPECTION.read_text(encoding="utf-8")
    required_denials = [
        "CLICK_MIGRATE=DENIED",
        "CONFIRM_MIGRATION=DENIED",
        "PLUGIN_INSTALL=DENIED",
        "APP_CONNECT=DENIED",
        "CUSTOM_MCP_UPLOAD=DENIED",
        "CREDENTIAL_CREATE=DENIED",
        "PLUGIN_SHARE_CHANGE=DENIED",
        "PLUGIN_PUBLICATION=DENIED",
        "PUBLIC_GPT_UPDATE=DENIED",
        "RENDER_CHANGE=DENIED",
    ]
    for denial in required_denials:
        assert denial in text

    assert "MIGRATION_EXECUTED=NO" in text
    assert "PLUGIN_INSTALLED=NO" in text
    assert "APP_CONNECTED=NO" in text
    assert "MCP_UPLOADED=NO" in text
    assert "CREDENTIAL_MUTATION=NO" in text
    assert "PUBLIC_GPT_MUTATION=NO" in text


def test_sentinel_package_requires_surface_capability_evidence() -> None:
    text = INSPECTION.read_text(encoding="utf-8")
    required_fields = [
        "MIGRATION_CONTROL_PRESENT=",
        "PLUGIN_SURFACE_PRESENT=",
        "CONNECTED_APP_OPTION=",
        "CUSTOM_MCP_OPTION=",
        "MCP_CAPABILITY=",
        "REMOTE_MCP_SUPPORTED=",
        "AUTH_OPTIONS=",
        "ACTION_CONFIRMATION_MODEL=",
        "WEB_AVAILABILITY=",
        "DESKTOP_ONLY_LIMITATION=",
        "INSTALL_PERMISSION=",
        "SHARE_PERMISSION=",
        "PUBLISH_PERMISSION=",
    ]
    for field in required_fields:
        assert field in text


def test_p100_candidate_contains_no_concrete_profile_or_common_secret_prefix() -> None:
    files = [MATRIX, AUTH_BINDING, INSPECTION]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    lowered = text.lower()
    assert "prof_" not in text
    assert "sk-proj-" not in lowered
    assert "sk-live-" not in lowered
    assert "bearer eyj" not in lowered
