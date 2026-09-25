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


def test_surface_matrix_records_selected_canary_proven_remote_mcp() -> None:
    matrix = load_yaml(MATRIX)
    selection = matrix["selection"]
    assert selection == {
        "selected_media_surface": "custom_remote_mcp",
        "selected_transport": "remote_mcp_http",
        "protocol_version": "2026-07-28",
        "selection_evidence": "bounded_remote_mcp_canary_closed_pass",
        "full_binding_authorized": False,
    }
    mcp = next(surface for surface in matrix["surfaces"] if surface["id"] == "custom_remote_mcp")
    assert mcp["binding_status"] == "SELECTED_CANDIDATE_CANARY_PROVEN"
    assert "one_read_only_invocation" in mcp["proven"]
    assert "execution_confirmation_semantics" in mcp["unproven_until_later_gates"]


def test_surface_matrix_has_fail_closed_release_boundary() -> None:
    boundary = load_yaml(MATRIX)["release_boundary"]
    assert set(boundary.values()) == {"DENIED"}
    assert boundary["public_gpt_mutation"] == "DENIED"
    assert boundary["migration_execution"] == "DENIED"
    assert boundary["plugin_publication"] == "DENIED"
    assert boundary["full_media_mcp_creation"] == "DENIED"
    assert boundary["voicebridge_credential_binding"] == "DENIED"
    assert boundary["render_change"] == "DENIED"
    assert boundary["main_mutation"] == "DENIED"
    assert boundary["pr22_merge"] == "DENIED"
    assert boundary["pr45_merge"] == "DENIED"


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
    assert execution["non_execution_operation_count"] == 9
    assert execution["execution_operation_count"] == 4
    assert execution["execution_tools_exposed_in_r3a"] is False


def test_auth_binding_selects_remote_mcp_and_preserves_secret_boundary() -> None:
    binding = load_yaml(AUTH_BINDING)
    transport = binding["transport_contract"]
    assert transport["final_transport"] == "remote_mcp_http"
    assert transport["protocol_version"] == "2026-07-28"
    assert transport["selected_surface"] == "custom_remote_mcp"
    assert transport["account_surface_proven"] is True
    assert transport["web_surface_proven"] is True
    assert transport["live_read_only_canary_proven"] is True
    assert transport["current_canary_reusable_for_voicebridge_binding"] is False
    assert transport["local_mcp_direct_dependency"] is False
    assert transport["client_desktop_dependency_allowed_by_default"] is False
    assert transport["automatic_transport_retry"] is False

    credentials = binding["credentials"]
    assert credentials["final_auth_method"] == "R3_B_REQUIRED_BEFORE_VOICEBRIDGE_BINDING"
    assert credentials["inbound_no_auth_allowed_for_full_binding"] is False
    assert credentials["canary_no_auth_is_evidence_only"] is True
    assert credentials["voicebridge_bearer_server_side_only"] is True
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
    assert consent["consent_must_not_be_inferred_from_plugin_connection"] is True

    retry = binding["retry_idempotency"]
    assert retry["completed"] == "REUSE"
    assert retry["processing"] == "REUSE_AND_CONCURRENCY_PROTECT"
    assert retry["failed_free_only"] == "FRESH_DETERMINISTIC_JOB_ON_NEW_EXPLICIT_RETRY_REQUEST"
    assert retry["failed_paid_or_charge_uncertain"] == "BLOCK"
    assert retry["automatic_retry_loop"] is False

    errors = binding["errors"]
    assert errors["structured_error_required"] is True
    assert errors["credential_sanitization_required"] is True
    assert errors["raw_voicebridge_authorization_header_exposed"] is False
    assert errors["media_failure_blocks_core"] is False


def test_r3a_auth_binding_only_authorizes_repository_contract_changes() -> None:
    boundary = load_yaml(AUTH_BINDING)["release_boundary"]
    assert boundary["r3a_contract_changes"] == "AUTHORIZED"
    denied = {key: value for key, value in boundary.items() if key != "r3a_contract_changes"}
    assert set(denied.values()) == {"DENIED"}


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
