from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_a9_7_i_builder_package_is_ready_but_not_runtime_applied() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    instructions = manifest["instructions"]
    release = manifest["release"]

    assert instructions["version"] == "0.6-beta-a9.6"
    assert instructions["builder_package_version"] == "0.7-beta-a9.7-i"
    assert instructions["builder_target_action_schema_version"] == "0.4.0-a9.7-c"
    assert instructions["builder_package_ready"] is True
    assert instructions["builder_runtime_applied"] is False

    assert release["a9_7_i_builder_package_ready"] is True
    assert release["a9_7_i_builder_runtime_applied"] is False
    assert release["a9_7_i_private_gpt_e2e_complete"] is False
    assert release["gpt_builder_private_update_required"] is True


def test_a9_7_i_builder_contains_facebook_free_and_paid_gate_contracts() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "Live accepted: YouTube, Instagram Reel, Facebook Video/Reel." in text
    assert "Facebook path: FREE `Cobalt -> AssemblyAI -> durable KRCM`." in text
    assert "startManagedFacebookFallback" in text
    assert "AWAITING_RETRIEVAL_CONSENT" in text
    assert "preflightManagedFacebookRetrievalCredit" in text
    assert "continueManagedFacebookPaidRetrieval" in text
    assert "provider=scrapecreators, mode=facebook_post, max_credits=1" in text
    assert "Do NOT reuse any earlier `1`" in text
    assert "Exactly one paid attempt. Never retry automatically." in text
    assert "Do not route Facebook through Supadata generate fallback." in text


def test_a9_7_i_target_action_schema_matches_package() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    schema = yaml.safe_load(
        (ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert schema["info"]["version"] == manifest["instructions"][
        "builder_target_action_schema_version"
    ]
    paths = schema["paths"]
    assert paths["/api/v1/media/managed/facebook-fallback"]["post"]["operationId"] == (
        "startManagedFacebookFallback"
    )
    assert paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval-preflight"
    ]["get"]["operationId"] == "preflightManagedFacebookRetrievalCredit"
    assert paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval"
    ]["post"]["operationId"] == "continueManagedFacebookPaidRetrieval"
