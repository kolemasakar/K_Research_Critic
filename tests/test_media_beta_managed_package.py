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
    assert manifest["beta"]["ingress_mode"] == "managed_zero_client"
    assert manifest["beta"]["browser_helper_required"] is False
    assert manifest["beta"]["managed_job_prefix"] == "KRCM_"
    assert manifest["beta"]["managed_credit_preflight_required"] is True
    assert manifest["beta"]["managed_explicit_user_consent_required"] is True
    assert manifest["beta"]["managed_automatic_ai_fallback"] is False
    assert manifest["beta"]["managed_user_beta_access_code_required"] is False
    assert manifest["release"]["a9_3_durable_managed_complete"] is True
    assert manifest["release"]["a9_5_private_gpt_integration_complete"] is False


def test_managed_action_schema_hides_owner_admission_and_preserves_credit_gate() -> None:
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
    }
    assert paths["/api/v1/media/managed/preflight"]["post"]["operationId"] == (
        "preflightManagedMediaCredits"
    )
    start = paths["/api/v1/media/managed/transcriptions"]["post"]
    assert start["operationId"] == "startManagedMediaNativeTranscription"
    assert start["x-openai-isConsequential"] is True

    preflight = schema["components"]["schemas"]["PreflightRequest"]
    assert preflight["required"] == ["url"]
    assert "beta_access_code" not in preflight["properties"]

    native = schema["components"]["schemas"]["NativeTranscriptRequest"]
    assert native["type"] == "object"
    assert "allOf" not in native
    assert set(native["required"]) == {"url", "credit_consent"}
    assert "beta_access_code" not in native["properties"]
    consent = native["properties"]["credit_consent"]["properties"]
    assert consent["provider"]["const"] == "supadata"
    assert consent["mode"]["const"] == "native"
    assert consent["max_credits"]["maximum"] == 1


def test_private_builder_instructions_fit_limit_and_forbid_legacy_normal_flow() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "preflightManagedMediaCredits" in text
    assert "startManagedMediaNativeTranscription" in text
    assert "getManagedMediaTranscriptSegments" in text
    assert "Do NOT ask the user for beta access code" in text
    assert "Do not expose `KRCM_...` Job IDs" in text
    assert "Do not fall back to Helper in the normal owner flow" in text
    assert "1 - Так" in text
    assert "2 - Ні" in text
