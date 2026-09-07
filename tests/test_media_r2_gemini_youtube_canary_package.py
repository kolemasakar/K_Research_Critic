from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / "prompts" / "GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md"
MANIFEST = ROOT / "gpt_store" / "media_r2_gemini_youtube_canary_manifest.yaml"


def test_canary_manifest_points_to_mixed_free_public_schema() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["instructions"]["file"].endswith(
        "GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md"
    )
    assert manifest["instructions"]["builder_runtime_applied"] is True
    assert manifest["instructions"]["builder_update_required"] is False
    assert manifest["actions"]["media_transcript"]["schema"] == (
        "gpt_store/actions/media_public_free_openapi.yaml"
    )
    assert manifest["actions"]["media_transcript"]["builder_runtime_applied"] is True
    assert manifest["routing"]["youtube"] == "gemini_free_direct_public_url"
    assert manifest["routing"]["instagram"] == "cobalt_to_assemblyai_free"
    assert manifest["routing"]["facebook"] == "cobalt_to_assemblyai_free"
    assert manifest["routing"]["telegram"] == "telegram_public_web_to_assemblyai_free"


def test_canary_manifest_records_checkpoint_87_without_r3_release() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    acceptance = manifest["acceptance"]
    release = manifest["release"]
    cobalt = manifest["cobalt_infrastructure"]

    assert acceptance["capability_read"] == "PASS"
    assert acceptance["youtube_consent_gate"] == "PASS"
    assert acceptance["youtube_provider_execution"] == "PASS"
    assert acceptance["youtube_durable_neon_completion"] == "PASS"
    assert acceptance["youtube_duplicate_reuse"] == "PASS"
    assert acceptance["youtube_new_provider_call_on_reuse"] is False
    assert acceptance["youtube_retrieval_credits_charged"] == 0
    assert acceptance["youtube_stt_seconds_charged"] == 0
    assert acceptance["instagram_live_canary"] == "FAIL_CLOSED_BLOCKED"
    assert acceptance["instagram_retrieval_provider"] == "cobalt"
    assert acceptance["instagram_retrieval_credits_charged"] == 0
    assert acceptance["instagram_stt_seconds_charged"] == 0
    assert acceptance["instagram_assemblyai_started"] is False
    assert acceptance["facebook_live_canary"] == "PENDING"
    assert acceptance["telegram_live_canary"] == "PENDING"
    assert acceptance["core_isolation_regression"] == "PENDING"

    assert cobalt["current_host"] == "render_free"
    assert cobalt["acceptance_state"] == "EDGE_429_BLOCKED"
    assert cobalt["blocker"] == "edge_http_429_non_json"
    assert cobalt["instagram_probe_reproduced"] is True
    assert cobalt["youtube_control_reproduced"] is True
    assert cobalt["paid_hosting_remediation"] == "excluded"
    assert cobalt["approved_migration_target"] == "oci_always_free"
    assert cobalt["endpoint_change_pending"] is True

    assert release["r2_youtube_live_acceptance_pass"] is True
    assert release["r2_instagram_infrastructure_remediation_pending"] is True
    assert release["r2_full_pass"] is False
    assert release["r3_ready"] is False
    assert release["r3_public_gpt_hold"] is True


def test_canary_policy_requires_one_gemini_data_use_consent_and_no_generic_media_confirmation() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    policy = manifest["policy"]

    assert policy["youtube_gemini_free_tier_only"] is True
    assert policy["youtube_gemini_data_use_consent_required"] is True
    assert policy["youtube_generic_media_start_confirmation"] is False
    assert policy["youtube_duplicate_confirmation_forbidden"] is True
    assert policy["paid_retrieval_fallback"] is False
    assert policy["paid_stt_fallback"] is False
    assert policy["paid_proxy_fallback"] is False
    assert policy["paid_cobalt_hosting_considered"] is False
    assert policy["user_cookies_forbidden"] is True
    assert policy["user_login_forbidden"] is True


def test_canary_instructions_encode_consent_payload_and_forbid_old_supadata_credit_ui() -> None:
    text = INSTRUCTIONS.read_text(encoding="utf-8")
    lower = text.lower()

    assert "preflightPublicGeminiYoutube" in text
    assert "startPublicGeminiYoutubeTranscription" in text
    assert '"provider": "google_gemini"' in text
    assert '"tier": "free"' in text
    assert '"data_use_acknowledged": true' in text
    assert "may be used" in lower or "можуть використовуватися" in lower
    assert "do not add a generic media-start confirmation" in lower
    assert "do not call `startpublicgeminiyoutubetranscription`" in lower
    assert "no cobalt, assemblyai, paid gemini" in lower
    assert "supadata-style credit balances" in lower
