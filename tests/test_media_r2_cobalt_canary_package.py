from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_r2_cobalt_canary_manifest_uses_public_schema() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_r2_cobalt_canary_manifest.yaml").read_text(encoding="utf-8")
    )
    assert manifest["actions"]["media_transcript"]["schema"] == (
        "gpt_store/actions/media_public_cobalt_openapi.yaml"
    )
    assert manifest["policy"]["supadata_active"] is False
    assert manifest["policy"]["paid_retrieval_fallback"] is False
    assert manifest["policy"]["paid_stt_fallback"] is False
    assert manifest["policy"]["media_start_confirmation_for_zero_credit_routes"] is False
    assert manifest["policy"]["duplicate_media_confirmation_forbidden"] is True


def test_r2_cobalt_canary_builder_forbids_legacy_credit_gate() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_R2_COBALT_CANARY_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")
    assert "preflightPublicCobaltMedia" in text
    assert "startPublicCobaltMediaTranscription" in text
    assert "Never ask twice for the same MEDIA operation." in text
    assert "Supadata is NOT active in this canary." in text
    assert "Do NOT display a Supadata credit quote" in text


def test_public_cobalt_action_start_is_non_consequential() -> None:
    schema = yaml.safe_load(
        (ROOT / "gpt_store" / "actions" / "media_public_cobalt_openapi.yaml").read_text(
            encoding="utf-8"
        )
    )
    start = schema["paths"]["/api/v1/media/managed/transcriptions"]["post"]
    assert start["operationId"] == "startPublicCobaltMediaTranscription"
    assert start["x-openai-isConsequential"] is False
