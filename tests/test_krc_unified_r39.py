from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md"
ADDENDUM = ROOT / "prompts" / "GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md"
ROUTING = ROOT / "contracts" / "krc_unified_media_routing.yaml"
STAGING = ROOT / "gpt_store" / "unified_r39_manifest.yaml"
TOOLS = ROOT / "plugins" / "krc_migration_candidate" / "contracts" / "media_tools.yaml"
R4_APPS = ROOT / "plugins" / "krc_r4_candidate" / ".app.json"
R39_OPENAPI = ROOT / "gpt_store" / "actions" / "media_public_r39_openapi.yaml"
UNIFIED = ROOT / "prompts" / "GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_r39_keeps_core_authoritative_and_media_as_evidence_layer() -> None:
    routing = load_yaml(ROUTING)
    assert routing["architecture"]["core_authority"] == "prompts/GPT_STORE_INSTRUCTIONS.md"
    assert routing["architecture"]["media_role"] == "evidence_acquisition_layer"
    assert routing["architecture"]["final_verdict_owner"] == "core_critic_workflow"
    assert routing["architecture"]["media_backend_merge_required"] is False
    assert routing["future_plugin_parity"]["custom_action_is_transport_adapter_not_business_logic"] is True


def test_r39_preserves_criticprofile_before_research_or_media_content() -> None:
    routing = load_yaml(ROUTING)
    order = routing["routing_order"]
    assert order.index("obtain_explicit_criticprofile_approval") < order.index("perform_read_only_media_preflight_or_lookup_when_relevant")
    forbidden = set(routing["pre_approval_boundary"]["forbidden"])
    assert "transcript_content_retrieval" in forbidden
    assert "provider_work" in forbidden
    assert "media_execution_start" in forbidden


def test_r39_preserves_exact_13_operation_split() -> None:
    routing = load_yaml(ROUTING)
    counts = routing["operation_counts"]
    assert counts == {
        "read_only": 9,
        "execution": 4,
        "total": 13,
        "read_only_execution_leakage": 0,
    }
    tools = load_yaml(TOOLS)
    assert tools["operation_count"] == 13
    assert tools["non_execution_count"] == 9
    assert tools["execution_count"] == 4
    assert set(routing["post_approval_read_only_tools"]) == {
        tool["candidate_name"]
        for tool in tools["tools"]
        if tool["classification"] == "non_execution"
    }
    assert set(routing["execution_tools"]) == {
        tool["candidate_name"]
        for tool in tools["tools"]
        if tool["classification"] == "execution"
    }


def test_r39_preserves_free_only_fail_closed_policy() -> None:
    free = load_yaml(ROUTING)["free_only"]
    assert free["required"] is True
    assert free["paid_retrieval_fallback"] is False
    assert free["paid_stt_fallback"] is False
    assert free["paid_proxy_fallback"] is False
    assert free["automatic_paid_retry"] is False
    assert free["supadata_public_active"] is False
    assert free["scrapecreators_public_active"] is False
    assert free["cookie_or_login_fallback"] is False


def test_r39_media_evidence_does_not_bypass_cross_check() -> None:
    evidence = load_yaml(ROUTING)["evidence_semantics"]
    assert evidence["transcript_proves"] == "what_the_media_source_says"
    assert evidence["transcript_does_not_prove"] == "external_factual_truth"
    assert evidence["one_media_item_counts_as_at_most_one_underlying_evidence_origin"] is True
    assert evidence["material_external_claims_follow_core_cross_check_floor"] is True
    assert evidence["traceability_invariant_required"] is True


def test_r39_current_gpt_addendum_and_future_plugin_use_same_semantics() -> None:
    staging = load_yaml(STAGING)
    assert staging["instructions"]["core"] == "prompts/GPT_STORE_INSTRUCTIONS.md"
    assert staging["instructions"]["media_addendum"] == "prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md"
    assert staging["future_plugin_mapping"]["semantic_parity_required"] is True
    addendum = ADDENDUM.read_text(encoding="utf-8")
    assert "MEDIA failure never blocks Core" in addendum
    assert "CriticProfile gate" in addendum
    assert "Never use paid/Supadata/ScrapeCreators/cookies/login fallback." in addendum


def test_r39_r4_candidate_retains_exact_five_app_ids() -> None:
    apps = json.loads(R4_APPS.read_text(encoding="utf-8"))["apps"]
    assert apps == {
        "krc-media-readonly": {"id": "asdk_app_6aaaf8ca113c8191a4ac53f8793833a4"},
        "krc-youtube": {"id": "asdk_app_6ab26b061fb4819180fa096638f1e4df"},
        "krc-instagram": {"id": "asdk_app_6aaeae197c9081918b90e46f5bb09615"},
        "krc-facebook": {"id": "asdk_app_6aaf262767d8819199146dc84b8e1ee8"},
        "krc-telegram": {"id": "asdk_app_6aaf292e653481918c75767dea004c5c"},
    }


def test_r39_staging_does_not_authorize_public_mutation_or_resume_r4c() -> None:
    staging = load_yaml(STAGING)
    assert staging["release_boundary"]["current_public_gpt_update"] == "NOT_YET_AUTHORIZED"
    assert staging["release_boundary"]["r4_c"] == "PAUSED_PENDING_SUPPORTED_CHATGPT_DISTRIBUTION"
    routing = load_yaml(ROUTING)["release_boundary"]
    assert routing["public_gpt_mutation"] == "HOLD_UNTIL_R39_REPOSITORY_ACCEPTANCE"
    assert routing["r4_c_resume"] == "DENIED"


def test_r39_builder_artifact_is_exact_core_plus_media_addendum() -> None:
    expected = CORE.read_text(encoding="utf-8").rstrip() + "\n\n" + ADDENDUM.read_text(encoding="utf-8").strip() + "\n"
    actual = UNIFIED.read_text(encoding="utf-8")
    assert actual == expected
    assert len(actual.rstrip()) <= 8000


def test_r39_action_schema_has_exact_confirmation_boundary() -> None:
    schema = load_yaml(R39_OPENAPI)
    operations = {}
    for route, path_item in schema["paths"].items():
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if operation and operation.get("operationId"):
                operations[operation["operationId"]] = operation["x-openai-isConsequential"]

    expected_execution = {
        "startPublicGeminiYoutubeTranscription",
        "startPublicInstagramCobaltTranscription",
        "startPublicFacebookCobaltTranscription",
        "startPublicTelegramTranscription",
    }
    assert len(operations) == 13
    assert {op for op, consequential in operations.items() if consequential is True} == expected_execution
    assert sum(value is False for value in operations.values()) == 9

    tools = load_yaml(TOOLS)["tools"]
    assert set(operations) == {tool["source_operation_id"] for tool in tools}


def test_r39_action_schema_preserves_bearer_auth_and_free_only_server() -> None:
    schema = load_yaml(R39_OPENAPI)
    assert schema["security"] == [{"bearerAuth": []}]
    auth = schema["components"]["securitySchemes"]["bearerAuth"]
    assert auth == {"type": "http", "scheme": "bearer"}
    assert schema["servers"] == [{"url": "https://voicebridge-krc-media-beta-kolemasakar.onrender.com"}]
    policy = schema["x-krc-free-only-policy"]
    assert policy["paid_retrieval_fallback"] is False
    assert policy["paid_stt_fallback"] is False
    assert policy["paid_proxy_fallback"] is False
