from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "plugins" / "krc_migration_candidate"
CORE = ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md"
SKILL = CANDIDATE / "skills" / "krc_core" / "SKILL.md"
CONTRACT = CANDIDATE / "contracts" / "media_tools.yaml"
ADAPTER = CANDIDATE / "contracts" / "media_adapter.yaml"
CORE_CASES = CANDIDATE / "regression" / "core_cases.yaml"
MEDIA_NEGATIVE_CASES = CANDIDATE / "regression" / "media_negative_cases.yaml"
OPENAPI = ROOT / "gpt_store" / "actions" / "media_public_r3_openapi.yaml"
README = CANDIDATE / "README.md"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def openapi_operations() -> dict[str, tuple[str, str]]:
    schema = load_yaml(OPENAPI)
    operations: dict[str, tuple[str, str]] = {}
    for route, path_item in schema["paths"].items():
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if operation and operation.get("operationId"):
                operations[operation["operationId"]] = (method.upper(), route)
    return operations


def test_core_skill_snapshot_is_exact_canonical_core() -> None:
    text = SKILL.read_text(encoding="utf-8")
    begin = "<!-- BEGIN KRC CORE EXACT SNAPSHOT -->\n"
    end = "\n<!-- END KRC CORE EXACT SNAPSHOT -->"
    assert begin in text
    assert end in text
    snapshot = text.split(begin, 1)[1].split(end, 1)[0].rstrip("\n")
    canonical = CORE.read_text(encoding="utf-8").rstrip("\n")
    assert snapshot == canonical


def test_media_candidate_has_exact_13_operation_parity() -> None:
    contract = load_yaml(CONTRACT)
    expected = openapi_operations()
    tools = contract["tools"]

    assert contract["operation_count"] == 13
    assert len(tools) == 13
    assert len(expected) == 13

    actual = {
        tool["source_operation_id"]: (tool["method"], tool["path"])
        for tool in tools
    }
    assert actual == expected
    assert len({tool["candidate_name"] for tool in tools}) == 13


def test_media_candidate_preserves_free_only_fail_closed_policy() -> None:
    contract = load_yaml(CONTRACT)
    policy = contract["policy"]
    assert policy["paid_retrieval_fallback"] is False
    assert policy["paid_stt_fallback"] is False
    assert policy["paid_proxy_fallback"] is False
    assert policy["supadata_public_active"] is False
    assert policy["scrapecreators_public_active"] is False
    assert policy["cookie_login_fallback"] is False
    assert policy["automatic_retry_loop"] is False
    assert policy["failed_free_only_retry"] == "fresh_deterministic_job_on_new_explicit_retry_request"
    assert policy["failed_paid_or_charge_uncertain_retry"] == "blocked"


def test_youtube_consent_and_provider_boundary_are_preserved() -> None:
    contract = load_yaml(CONTRACT)
    consent = contract["youtube_consent"]
    assert consent == {
        "preflight_calls_provider": False,
        "provider": "google_gemini",
        "tier": "free",
        "data_use_acknowledged": True,
        "required_before_start": True,
    }

    tools = {tool["source_operation_id"]: tool for tool in contract["tools"]}
    assert tools["startPublicGeminiYoutubeTranscription"]["requires_explicit_user_consent"] is True
    assert contract["routes"]["youtube"] == "Gemini Developer API Free Tier direct URL"


def test_platform_specific_media_guards_are_preserved() -> None:
    contract = load_yaml(CONTRACT)
    guards = contract["hard_guards"]
    assert "cobalt_fallback" in guards["youtube"]["forbid"]
    assert "assemblyai_fallback" in guards["youtube"]["forbid"]
    assert guards["facebook"]["canonical_retrieval"] == "cobalt_video_plus_audio"
    assert guards["facebook"]["normalization"] == "mono_pcm_wav_16khz"
    assert guards["telegram"]["canonical_retrieval"] == "telegram_public_web"
    assert guards["instagram"]["canonical_retrieval"] == "cobalt"


def test_core_regression_pack_covers_required_behavioral_dimensions() -> None:
    fixtures = load_yaml(CORE_CASES)
    cases = fixtures["cases"]
    ids = {case["id"] for case in cases}
    categories = {case["category"] for case in cases}

    assert len(cases) >= 8
    assert len(ids) == len(cases)
    assert set(fixtures["required_categories"]) <= categories
    assert {
        "core_criticprofile_direct_run_uk",
        "core_criticprofile_review_edit_uk",
        "core_crosscheck_shortfall_high_risk_uk",
        "core_checkpoint_recovery_review_required_uk",
        "core_media_failure_isolation_uk",
        "core_report_language_english",
        "core_ukrainian_protocol_table",
    } <= ids

    forbidden = set(fixtures["forbidden_regressions"])
    assert "independent_research_before_criticprofile_approval" in forbidden
    assert "hidden_unqualified_shortfall" in forbidden
    assert "untraceable_pass_count" in forbidden
    assert "request_log_silently_reenabled" in forbidden
    assert "media_failure_blocks_core" in forbidden
    assert "hidden_reasoning_exposed" in forbidden


def test_core_regression_pack_preserves_ukrainian_protocol_contract() -> None:
    fixtures = load_yaml(CORE_CASES)
    case = next(case for case in fixtures["cases"] if case["id"] == "core_ukrainian_protocol_table")
    assert case["expected_heading"] == "ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ"
    assert case["expected_columns"] == [
        "Твердження",
        "Потрібно",
        "Отримано незалежних",
        "Виняток",
    ]


def test_media_negative_pack_covers_hard_failure_boundaries() -> None:
    fixtures = load_yaml(MEDIA_NEGATIVE_CASES)
    cases = fixtures["cases"]
    ids = {case["id"] for case in cases}

    assert len(cases) >= 14
    assert len(ids) == len(cases)
    assert {
        "media_wrong_platform_on_instagram_route",
        "media_youtube_start_without_consent",
        "media_youtube_preflight_is_non_provider",
        "media_paid_fallback_forbidden",
        "media_failed_free_only_retry_requires_new_explicit_request",
        "media_credit_uncertain_replay_blocked",
        "media_completed_reused",
        "media_processing_reused",
        "media_facebook_only_audio_not_canonical",
        "media_telegram_login_fallback_forbidden",
        "media_malformed_job_id",
        "media_segments_pagination_bounds",
        "media_secret_leakage_forbidden",
        "media_failure_isolated_from_core",
    } <= ids

    required_dimensions = set(fixtures["required_negative_dimensions"])
    assert {
        "platform_validation",
        "explicit_consent",
        "paid_fallback_prohibition",
        "retry_semantics",
        "charge_uncertain_block",
        "durable_reuse",
        "concurrency_protection",
        "facebook_normalization",
        "telegram_public_only",
        "identifier_validation",
        "pagination_validation",
        "secret_sanitization",
        "core_isolation",
    } <= required_dimensions


def test_negative_pack_blocks_charge_uncertain_and_automatic_paid_fallback() -> None:
    cases = {case["id"]: case for case in load_yaml(MEDIA_NEGATIVE_CASES)["cases"]}
    charge = cases["media_credit_uncertain_replay_blocked"]
    assert charge["expected"]["outcome"] == "BLOCK_REPLAY"
    assert "no_fresh_retry" in charge["invariants"]

    paid = cases["media_paid_fallback_forbidden"]
    assert paid["expected"]["outcome"] == "FAIL_CLOSED"
    assert "paid_retrieval_fallback_false" in paid["invariants"]
    assert "paid_stt_fallback_false" in paid["invariants"]
    assert "paid_proxy_fallback_false" in paid["invariants"]


def test_adapter_has_exact_operation_binding_parity() -> None:
    adapter = load_yaml(ADAPTER)
    expected = set(openapi_operations())
    bindings = adapter["operation_bindings"]
    assert len(bindings) == 13
    assert set(bindings) == expected
    assert len({binding["adapter_method"] for binding in bindings.values()}) == 13


def test_adapter_preserves_request_validation_and_pagination_bounds() -> None:
    request = load_yaml(ADAPTER)["canonical_request_envelope"]
    assert request["job_id_pattern"] == "^KRCM_[A-Za-z0-9-]+$"
    assert request["language_hint_allowed"] == ["auto", "uk", "ru", "en"]
    assert request["pagination"] == {
        "cursor_minimum": 0,
        "limit_minimum": 1,
        "limit_maximum": 50,
    }


def test_adapter_preserves_consent_retry_and_core_isolation() -> None:
    adapter = load_yaml(ADAPTER)
    consent = adapter["consent_contract"]
    assert consent["youtube_start"] == {
        "required": True,
        "provider": "google_gemini",
        "tier": "free",
        "data_use_acknowledged": True,
    }
    assert consent["youtube_preflight"]["provider_work_allowed"] is False

    retry = adapter["retry_contract"]
    assert retry["COMPLETED"] == "REUSE"
    assert retry["PROCESSING"] == "REUSE_INFLIGHT"
    assert retry["FAILED_FREE_ONLY"]["requires_new_explicit_retry_request"] is True
    assert retry["FAILED_PAID_OR_CHARGE_UNCERTAIN"]["action"] == "BLOCK_REPLAY"
    assert retry["automatic_retry_loop"] is False

    isolation = adapter["core_isolation"]
    assert isolation["media_failure_blocks_core"] is False
    assert isolation["media_transcript_is_evidence_not_final_fact_verdict"] is True
    assert isolation["fact_check_still_uses_criticprofile_gate"] is True


def test_adapter_auth_and_error_boundary_are_fail_closed() -> None:
    adapter = load_yaml(ADAPTER)
    auth = adapter["authentication"]
    assert auth["final_strategy"] == "TBD_AFTER_ACCOUNT_MIGRATION_SURFACE_INSPECTION"
    assert auth["secret_placement"] == "SERVER_SIDE_ONLY"
    assert auth["model_receives_secret"] is False
    assert auth["repository_contains_secret"] is False
    assert auth["skill_contains_secret"] is False
    assert auth["evidence_contains_secret"] is False

    errors = adapter["error_taxonomy"]
    assert errors["CONSENT_REQUIRED"]["provider_call_allowed_before_resolution"] is False
    assert errors["FREE_PROVIDER_QUOTA"]["paid_fallback_allowed"] is False
    assert errors["FREE_PROVIDER_UNAVAILABLE"]["paid_fallback_allowed"] is False
    assert errors["CHARGE_UNCERTAIN"]["replay_allowed"] is False
    assert errors["SECRET_SANITIZATION"]["expose_raw_backend_error"] is False


def test_adapter_is_transport_neutral_and_requires_no_backend_mutation() -> None:
    adapter = load_yaml(ADAPTER)
    transport = adapter["transport"]
    backend = adapter["backend"]
    assert transport["final_surface"] == "TBD_AFTER_ACCOUNT_MIGRATION_SURFACE_INSPECTION"
    assert transport["protocol_binding"] == "TBD"
    assert transport["installable"] is False
    assert transport["deployed"] is False
    assert transport["live_mcp_server"] is False
    assert transport["backend_mutation_required"] is False
    assert backend["preserve_existing_api"] is True
    assert backend["render_change_required_for_design_candidate"] is False


def test_candidate_does_not_guess_final_plugin_or_mcp_packaging() -> None:
    readme = README.read_text(encoding="utf-8")
    assert "DESIGN_ONLY / NOT_INSTALLABLE / NOT_DEPLOYED" in readme
    assert not (CANDIDATE / "mcp.json").exists()
    assert not (CANDIDATE / ".mcp.json").exists()
    assert not (CANDIDATE / ".app.json").exists()


def test_candidate_contains_no_concrete_browser_profile_or_common_secret_prefix() -> None:
    candidate_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    )
    lowered = candidate_text.lower()
    assert "prof_" not in candidate_text
    assert "sk-proj-" not in lowered
    assert "sk-live-" not in lowered
    assert "bearer eyj" not in lowered


def test_authentication_is_explicitly_unfinalized_and_server_side_only() -> None:
    auth = load_yaml(CONTRACT)["authentication"]
    assert auth["final_strategy"] == "TBD_AFTER_ACCOUNT_MIGRATION_SURFACE_INSPECTION"
    assert auth["secret_visibility"] == "SERVER_SIDE_ONLY"
    assert auth["model_visible_secret"] is False
    assert auth["repository_secret"] is False
