from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_a9_9_package_preserves_a9_7_i_acceptance_and_records_private_gpt_e2e() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    instructions = manifest["instructions"]
    beta = manifest["beta"]
    release = manifest["release"]

    assert instructions["version"] == "0.9.1-beta-a10"
    assert instructions["builder_package_version"] == "0.9.1-beta-a10"
    assert instructions["builder_target_action_schema_version"] == "0.6.0-a9.10"
    assert instructions["builder_package_ready"] is True
    assert instructions["builder_runtime_applied"] is False
    assert instructions["builder_policy_fix_runtime_applied"] is True
    assert instructions["cross_check_protocol_markdown_table_strict"] is True
    assert instructions["cross_check_protocol_header_merge_forbidden"] is True

    assert beta["public_platforms_live_accepted"] == [
        "youtube",
        "instagram",
        "facebook",
        "telegram",
    ]
    assert beta["public_platforms_in_progress"] == []
    assert beta["managed_telegram_builder_runtime_applied"] is True
    assert beta["managed_telegram_private_gpt_e2e_complete"] is True

    assert release["rollout_state"] == "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED"
    assert release["a9_7_i_builder_package_ready"] is True
    assert release["a9_7_i_builder_runtime_applied"] is True
    assert release["a9_7_i_builder_policy_fix_runtime_applied"] is True
    assert release["a9_7_i_private_gpt_e2e_complete"] is True
    assert release["a9_9_telegram_backend_complete"] is True
    assert release["a9_9_telegram_action_package_complete"] is True
    assert release["a9_9_telegram_builder_runtime_applied"] is True
    assert release["a9_9_telegram_private_gpt_e2e_complete"] is True
    assert release["gpt_builder_private_update_required"] is True


def test_a9_7_i_builder_enforces_cobalt_fail_unavailable_without_paid_offer() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "Live accepted: YouTube, Instagram Reel, Facebook Video/Reel." in text
    assert "Facebook path: FREE `Cobalt -> AssemblyAI -> durable KRCM`." in text
    assert "startManagedFacebookFallback" in text
    assert "Cobalt failure means media retrieval is unavailable" in text
    assert "AWAITING_RETRIEVAL_CONSENT" in text
    assert "report that Facebook media retrieval is unavailable and STOP media intake" in text
    assert "Do NOT call `preflightManagedFacebookRetrievalCredit`" in text
    assert "or `continueManagedFacebookPaidRetrieval`" in text
    assert "do not offer any paid retrieval fallback" in text
    assert "Do not route Facebook through Supadata generate fallback." in text
    assert "provider=scrapecreators, mode=facebook_post, max_credits=1" not in text
    assert "Only a NEW explicit `1` authorizes `continueManagedFacebookPaidRetrieval`" not in text


def test_a9_7_i_manifest_records_facebook_paid_path_inactive() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    beta = manifest["beta"]
    assert beta["managed_facebook_free_failure_behavior"] == "unavailable"
    assert beta["managed_facebook_paid_retrieval_configured"] is False
    assert beta["managed_facebook_paid_fallback_live_accepted"] is False
    assert beta["managed_facebook_paid_retrieval_active"] is False
    assert beta["managed_facebook_paid_offer_allowed"] is False
    assert beta["managed_facebook_automatic_paid_retrieval"] is False


def test_a9_7_i_target_action_schema_keeps_reserved_paid_operations_compatible() -> None:
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
    action_text = (
        ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"
    ).read_text(encoding="utf-8")
    assert "ScrapeCreators is reserved compatibility" in action_text
    assert "treat Facebook retrieval as terminal unavailable" in action_text
    assert "Builder must not call this operation after Cobalt failure" in action_text
    assert "separate local preflight and a new explicit" not in action_text
    assert "stop at AWAITING_RETRIEVAL_CONSENT" not in action_text

    paths = schema["paths"]
    assert paths["/api/v1/media/managed/facebook-fallback"]["post"]["operationId"] == (
        "startManagedFacebookFallback"
    )
    # Reserved compatibility operations remain in the schema, but active Builder
    # instructions explicitly forbid calling or offering them after Cobalt failure.
    assert paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval-preflight"
    ]["get"]["operationId"] == "preflightManagedFacebookRetrievalCredit"
    assert paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval"
    ]["post"]["operationId"] == "continueManagedFacebookPaidRetrieval"
