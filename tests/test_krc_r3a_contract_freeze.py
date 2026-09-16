from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "plugins" / "krc_migration_candidate" / "contracts"
MEDIA = CONTRACTS / "media_tools.yaml"
ADAPTER = CONTRACTS / "media_adapter.yaml"
AUTH = CONTRACTS / "auth_transport_binding.yaml"
MIGRATION = CONTRACTS / "migration_acceptance.yaml"
MATRIX = CONTRACTS / "surface_decision_matrix.yaml"


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_r3a_contract_set_is_versioned_and_frozen() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    auth = load(AUTH)
    migration = load(MIGRATION)
    matrix = load(MATRIX)

    assert media["schema_version"] == "0.2"
    assert media["status"] == "R3A_FROZEN_REMOTE_MCP_CONTRACT"
    assert adapter["schema_version"] == "0.2"
    assert adapter["status"] == "R3A_FROZEN_REMOTE_MCP_ADAPTER_CONTRACT"
    assert auth["schema_version"] == "0.2"
    assert auth["status"] == "R3A_FROZEN_AUTH_TRANSPORT_REQUIREMENTS"
    assert migration["schema_version"] == "0.2"
    assert migration["status"] == "R3A_RECONCILED_MIGRATION_ACCEPTANCE_CONTRACT"
    assert matrix["schema_version"] == "0.2"
    assert matrix["status"] == "R3A_REMOTE_MCP_SURFACE_SELECTED"


def test_selected_remote_mcp_surface_is_consistent_across_contracts() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    auth = load(AUTH)
    migration = load(MIGRATION)
    matrix = load(MATRIX)

    assert media["surface_evidence"]["selected_surface"] == "custom_remote_mcp"
    assert media["surface_evidence"]["transport"] == "remote_mcp_http"
    assert media["surface_evidence"]["protocol_version"] == "2026-07-28"
    assert adapter["transport"]["final_surface"] == "custom_remote_mcp"
    assert adapter["transport"]["protocol_binding"] == "remote_mcp_http_2026_07_28"
    assert auth["transport_contract"]["selected_surface"] == "custom_remote_mcp"
    assert auth["transport_contract"]["final_transport"] == "remote_mcp_http"
    assert auth["transport_contract"]["protocol_version"] == "2026-07-28"
    assert migration["selected_replacement_surface"]["media_binding"] == "custom_remote_mcp"
    assert matrix["selection"]["selected_media_surface"] == "custom_remote_mcp"
    assert matrix["selection"]["full_binding_authorized"] is False


def test_tool_identity_classification_and_adapter_mapping_are_frozen() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    tools = media["tools"]
    bindings = adapter["operation_bindings"]

    assert media["operation_count"] == 13
    assert media["non_execution_count"] == 9
    assert media["execution_count"] == 4
    assert len(tools) == 13
    assert len(bindings) == 13

    contract_map = {tool["source_operation_id"]: tool["candidate_name"] for tool in tools}
    adapter_map = {operation: binding["mcp_tool_name"] for operation, binding in bindings.items()}
    assert contract_map == adapter_map

    execution = {tool["candidate_name"] for tool in tools if tool["classification"] == "execution"}
    assert execution == {
        "media_youtube_start",
        "media_instagram_start",
        "media_facebook_start",
        "media_telegram_start",
    }

    for operation, binding in bindings.items():
        if binding["classification"] == "execution":
            assert binding["execution_not_exposed_in_r3a"] is True, operation
        else:
            assert binding["provider_work_allowed"] is False, operation


def test_secret_boundary_requires_r3b_before_voicebridge_binding() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    auth = load(AUTH)

    assert media["authentication"]["inbound_strategy"] == "R3_B_REQUIRED_BEFORE_VOICEBRIDGE_BINDING"
    assert media["authentication"]["canary_no_auth_allowed_for_full_binding"] is False
    assert adapter["authentication"]["final_strategy"] == "R3_B_REQUIRED_BEFORE_VOICEBRIDGE_BINDING"
    assert adapter["authentication"]["inbound_no_auth_allowed_for_full_binding"] is False
    assert auth["credentials"]["final_auth_method"] == "R3_B_REQUIRED_BEFORE_VOICEBRIDGE_BINDING"
    assert auth["credentials"]["canary_no_auth_is_evidence_only"] is True
    assert auth["credentials"]["voicebridge_bearer_server_side_only"] is True

    forbidden_flags = [
        media["authentication"]["model_visible_secret"],
        media["authentication"]["repository_secret"],
        adapter["authentication"]["model_receives_secret"],
        adapter["authentication"]["repository_contains_secret"],
        adapter["authentication"]["skill_contains_secret"],
        adapter["authentication"]["evidence_contains_secret"],
        adapter["authentication"]["tool_arguments_contain_secret"],
        auth["credentials"]["model_visible_secret"],
        auth["credentials"]["repository_secret"],
    ]
    assert forbidden_flags == [False] * len(forbidden_flags)


def test_consent_retry_audit_and_core_isolation_are_cross_contract_consistent() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    auth = load(AUTH)

    assert media["youtube_consent"]["required_before_start"] is True
    assert adapter["consent_contract"]["youtube_start"]["required"] is True
    assert auth["consent"]["youtube_execution_requires_explicit_user_acknowledgement"] is True
    assert auth["consent"]["consent_must_not_be_inferred_from_plugin_connection"] is True

    assert media["policy"]["automatic_retry_loop"] is False
    assert adapter["retry_contract"]["automatic_retry_loop"] is False
    assert auth["retry_idempotency"]["automatic_retry_loop"] is False
    assert adapter["retry_contract"]["FAILED_PAID_OR_CHARGE_UNCERTAIN"]["action"] == "BLOCK_REPLAY"
    assert auth["retry_idempotency"]["failed_paid_or_charge_uncertain"] == "BLOCK"

    assert set(media["audit_fields_required"]) == set(adapter["canonical_response_envelope"]["required_audit_fields"])
    assert adapter["core_isolation"]["media_failure_blocks_core"] is False
    assert auth["errors"]["media_failure_blocks_core"] is False


def test_r3a_does_not_authorize_runtime_expansion_or_cutover() -> None:
    media = load(MEDIA)
    adapter = load(ADAPTER)
    auth = load(AUTH)
    migration = load(MIGRATION)
    matrix = load(MATRIX)

    assert set(media["release_boundary"].values()) == {"DENIED"}
    assert set(adapter["release_boundary"].values()) == {"DENIED"}
    assert auth["release_boundary"]["r3a_contract_changes"] == "AUTHORIZED"
    assert set(
        value
        for key, value in auth["release_boundary"].items()
        if key != "r3a_contract_changes"
    ) == {"DENIED"}
    assert set(migration["release_boundary"].values()) == {"DENIED"}
    assert set(matrix["release_boundary"].values()) == {"DENIED"}
