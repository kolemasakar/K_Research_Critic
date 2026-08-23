from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_media_beta_manifest_uses_zero_client_managed_action() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )

    assert manifest["product"]["publication_state"] == "private_owner_only"
    assert manifest["actions"]["media_transcript"]["schema"] == (
        "gpt_store/actions/media_managed_beta_openapi.yaml"
    )
    assert manifest["instructions"]["profile_gate_mode"] == "two_stage_direct_or_review"
    assert manifest["instructions"]["profile_auto_display"] is False
    assert manifest["instructions"]["profile_direct_run_approves_profile"] is True
    assert manifest["instructions"]["profile_review_option"] == 2
    assert manifest["instructions"]["profile_cancel_option"] == 3
    assert manifest["instructions"]["recovered_review_required_uses_same_gate"] is True
    assert manifest["instructions"]["required_cross_checks_enforced"] is True
    assert manifest["instructions"]["cross_check_independence_required"] is True
    assert manifest["instructions"]["cross_check_shortfall_must_be_reported"] is True
    assert manifest["instructions"]["cross_check_protocol_summary_required"] is True
    assert manifest["instructions"]["cross_check_floor_by_risk"] == {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }
    assert manifest["beta"]["ingress_mode"] == "managed_zero_client"
    assert manifest["beta"]["browser_helper_required"] is False
    assert manifest["beta"]["managed_job_prefix"] == "KRCM_"
    assert manifest["beta"]["managed_credit_preflight_required"] is True
    assert manifest["beta"]["managed_explicit_user_consent_required"] is True
    assert manifest["beta"]["managed_automatic_ai_fallback"] is False
    assert manifest["beta"]["managed_user_beta_access_code_required"] is False
    assert manifest["beta"]["public_platforms_live_accepted"] == [
        "youtube",
        "instagram",
    ]
    assert manifest["beta"]["managed_instagram_ai_fallback_live_accepted"] is True
    assert manifest["release"]["a9_3_durable_managed_complete"] is True
    assert manifest["release"]["a9_5_private_gpt_integration_complete"] is True
    assert manifest["release"]["a9_8_owner_zero_client_acceptance_complete"] is True
    assert manifest["release"]["a9_6_instagram_managed_complete"] is True
    assert manifest["release"]["a9_6_facebook_complete"] is False
    assert manifest["release"]["criticprofile_gate_runtime_accepted"] is True
    assert manifest["release"]["cross_check_enforcement_hardened"] is True


def test_managed_action_schema_hides_owner_admission_and_preserves_credit_gates() -> None:
    schema = yaml.safe_load(
        (ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml").read_text(
            encoding="utf-8"
        )
    )
    paths = schema["paths"]

    assert set(paths) == {
        "/api/v1/media/managed/preflight",
        "/api/v1/media/managed/transcriptions",
        "/api/v1/media/managed/transcriptions/{job_id}",
        "/api/v1/media/managed/transcriptions/{job_id}/segments",
        "/api/v1/media/managed/transcriptions/{job_id}/ai-preflight",
        "/api/v1/media/managed/transcriptions/{job_id}/ai",
    }
    assert paths["/api/v1/media/managed/preflight"]["post"]["operationId"] == (
        "preflightManagedMediaCredits"
    )
    start = paths["/api/v1/media/managed/transcriptions"]["post"]
    assert start["operationId"] == "startManagedMediaNativeTranscription"
    assert start["x-openai-isConsequential"] is True

    ai_preflight = paths[
        "/api/v1/media/managed/transcriptions/{job_id}/ai-preflight"
    ]["get"]
    assert ai_preflight["operationId"] == "preflightManagedMediaAiCredits"
    assert ai_preflight["x-openai-isConsequential"] is False

    ai_start = paths["/api/v1/media/managed/transcriptions/{job_id}/ai"]["post"]
    assert ai_start["operationId"] == "startManagedMediaAiTranscription"
    assert ai_start["x-openai-isConsequential"] is True

    job_operations = [
        paths["/api/v1/media/managed/transcriptions/{job_id}"]["get"],
        paths["/api/v1/media/managed/transcriptions/{job_id}/segments"]["get"],
        ai_preflight,
        ai_start,
    ]
    for operation in job_operations:
        parameter = operation["parameters"][0]
        assert "$ref" not in parameter
        assert parameter["name"] == "job_id"
        assert parameter["in"] == "path"
        assert parameter["required"] is True

    preflight = schema["components"]["schemas"]["PreflightRequest"]
    assert preflight["required"] == ["url"]
    assert "beta_access_code" not in preflight["properties"]

    native = schema["components"]["schemas"]["NativeTranscriptRequest"]
    assert native["type"] == "object"
    assert "allOf" not in native
    assert set(native["required"]) == {"url", "credit_consent"}
    assert "beta_access_code" not in native["properties"]
    native_consent = native["properties"]["credit_consent"]["properties"]
    assert native_consent["provider"]["const"] == "supadata"
    assert native_consent["mode"]["const"] == "native"
    assert native_consent["max_credits"]["const"] == 1

    ai_request = schema["components"]["schemas"]["AiTranscriptRequest"]
    assert ai_request["type"] == "object"
    assert "allOf" not in ai_request
    assert ai_request["required"] == ["credit_consent"]
    assert "beta_access_code" not in ai_request["properties"]
    ai_consent = ai_request["properties"]["credit_consent"]["properties"]
    assert ai_consent["provider"]["const"] == "supadata"
    assert ai_consent["mode"]["const"] == "generate"
    assert ai_consent["max_credits"]["const"] == 40

    ai_quote = schema["components"]["schemas"]["AiCreditPreflight"]["properties"]
    assert ai_quote["estimated_credits"]["const"] == 40
    assert ai_quote["maximum_credits"]["const"] == 40
    assert ai_quote["credits_per_minute"]["const"] == 2
    assert ai_quote["maximum_duration_minutes"]["const"] == 20
    assert ai_quote["conservative_maximum"]["const"] is True

    job = schema["components"]["schemas"]["ManagedJob"]["properties"]
    assert set(job["provider_mode"]["enum"]) == {"native", "generate"}


def test_private_builder_instructions_fit_limit_and_use_two_stage_profile_gate() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "REPORT LANGUAGE INVARIANT" in text
    assert "Source/transcript language never controls report language" in text
    assert "preflightManagedMediaCredits" in text
    assert "startManagedMediaNativeTranscription" in text
    assert "preflightManagedMediaAiCredits" in text
    assert "startManagedMediaAiTranscription" in text
    assert "mode=generate, max_credits=40" in text
    assert "DO NOT reuse native `1`" in text
    assert "Do NOT ask the user for beta access code" in text
    assert "Do not expose `KRCM_...` Job IDs" in text
    assert "Do not fall back to Helper in the normal owner flow" in text
    assert "1 - Так" in text
    assert "2 - Ні" in text
    assert "DO NOT display the profile immediately" in text
    assert "Профіль збору і критики успішно створено." in text
    assert "1 - виконати аналіз одразу." in text
    assert "2 - переглянути і відредагувати профіль збору і критики." in text
    assert "1 - прийняти профіль, виконати дослідження." in text
    assert "2 - редагувати профіль." in text
    assert "Never claim approval before `1`" in text
    assert "CRITICAL>=3, HIGH>=2, MEDIUM>=1, LOW>=0" in text
    assert "satisfy approved `required_cross_checks`" in text
    assert "Count independent underlying sources" in text
    assert "state the shortfall, lower confidence, and record a limitation" in text
    assert "Protocol reports required/achieved cross-checks and exceptions" in text
