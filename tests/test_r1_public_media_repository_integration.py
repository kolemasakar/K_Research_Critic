from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_r1_public_core_package_remains_unchanged_and_action_free() -> None:
    manifest = _load_yaml("gpt_store/manifest.yaml")

    assert manifest["product"]["name"] == "K-Research & Critic"
    assert manifest["product"]["publication_state"] == "published"
    assert manifest["capabilities"]["web_search"] is True
    assert manifest["capabilities"]["code_interpreter_data_analysis"] is True
    assert manifest["capabilities"]["image_generation"] is False
    assert manifest["capabilities"]["apps"] is False
    assert manifest["capabilities"]["actions"] is False
    assert manifest["knowledge"]["files"] == []
    assert manifest["instructions"]["file"] == "prompts/GPT_STORE_INSTRUCTIONS.md"
    assert manifest["release"]["external_backend_required"] is False


def test_r1_media_package_is_additive_private_staging() -> None:
    media = _load_yaml("gpt_store/media_beta_manifest.yaml")

    assert media["product"]["name"] == "K-Research & Critic - MEDIA BETA"
    assert media["product"]["publication_state"] == "private_owner_only"
    assert media["capabilities"]["actions"] is True
    assert media["actions"]["media_transcript"]["schema"] == (
        "gpt_store/actions/media_managed_beta_openapi.yaml"
    )
    assert media["actions"]["media_transcript"]["server"] == (
        "https://voicebridge-krc-media-beta-kolemasakar.onrender.com"
    )
    assert media["release"]["production_core_unchanged"] is True
    assert media["release"]["public_store_gpt_unchanged"] is True
    assert media["release"]["merge_to_public_product_allowed"] is False

    assert (ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md").is_file()
    assert (ROOT / "prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md").is_file()
    assert (ROOT / "gpt_store/actions/media_managed_beta_openapi.yaml").is_file()
    assert (ROOT / "docs/PRIVACY_POLICY.md").is_file()


def test_r1_media_fail_closed_policy_is_preserved() -> None:
    media = _load_yaml("gpt_store/media_beta_manifest.yaml")
    beta = media["beta"]
    builder = (ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )

    assert beta["managed_facebook_free_retrieval_provider"] == "cobalt"
    assert beta["managed_facebook_free_failure_behavior"] == "unavailable"
    assert beta["managed_facebook_paid_retrieval_configured"] is False
    assert beta["managed_facebook_paid_retrieval_active"] is False
    assert beta["managed_facebook_paid_offer_allowed"] is False
    assert beta["managed_facebook_automatic_paid_retrieval"] is False
    assert beta["managed_telegram_retrieval_credits"] == 0
    assert beta["managed_attachment_retrieval_credits"] == 0

    assert "Cobalt failure means media retrieval is unavailable" in builder
    assert "do not offer any paid retrieval fallback" in builder
    assert "Do NOT call `preflightManagedFacebookRetrievalCredit`" in builder
    assert "or `continueManagedFacebookPaidRetrieval`" in builder


def test_r1_public_and_media_instructions_are_separate_files() -> None:
    public_text = (ROOT / "prompts/GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")
    media_text = (ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )

    assert public_text != media_text
    assert "K-Research & Critic - MEDIA BETA" not in public_text
    assert "OWNER-ONLY ZERO-CLIENT MEDIA" in media_text
