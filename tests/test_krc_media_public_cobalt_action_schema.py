from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"


def load_schema() -> dict:
    return yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_public_media_schema_exposes_only_accepted_public_routes() -> None:
    schema = load_schema()
    paths = set(schema["paths"])
    assert paths == {
        "/api/v1/media/managed",
        "/api/v1/media/managed/preflight",
        "/api/v1/media/managed/lookup",
        "/api/v1/media/managed/transcriptions",
        "/api/v1/media/managed/facebook-fallback",
        "/api/v1/media/managed/telegram",
        "/api/v1/media/managed/transcriptions/{job_id}",
        "/api/v1/media/managed/transcriptions/{job_id}/segments",
    }


def test_public_media_schema_has_no_legacy_paid_or_attachment_operations() -> None:
    text = SCHEMA_PATH.read_text(encoding="utf-8").lower()
    forbidden_operation_fragments = (
        "facebook-retrieval-preflight",
        "facebook-retrieval:",
        "/ai-preflight",
        "/ai:",
        "/attachment:",
        "/attachment-probe:",
        "startmanagedmedianativetranscription",
        "continuemanagedfacebookpaidretrieval",
        "startmanagedmediaaitranscription",
    )
    for fragment in forbidden_operation_fragments:
        assert fragment not in text


def test_public_youtube_instagram_schema_matches_cobalt_contract() -> None:
    schema = load_schema()
    paths = schema["paths"]

    assert paths["/api/v1/media/managed/preflight"]["post"]["operationId"] == "preflightPublicCobaltMedia"
    assert paths["/api/v1/media/managed/lookup"]["post"]["operationId"] == "lookupPublicCobaltMediaJob"
    assert (
        paths["/api/v1/media/managed/transcriptions"]["post"]["operationId"]
        == "startPublicCobaltMediaTranscription"
    )

    request = schema["components"]["schemas"]["PublicCobaltRequest"]
    assert request["required"] == ["url"]
    assert "credit_consent" not in request["properties"]

    preflight = schema["components"]["schemas"]["PublicCobaltPreflight"]["properties"]
    assert preflight["provider"]["const"] == "cobalt"
    assert preflight["estimated_retrieval_credits"]["const"] == 0
    assert preflight["stt_provider"]["const"] == "assemblyai"
    assert preflight["consent_required"]["const"] is False
    assert preflight["automatic_paid_fallback"]["const"] is False


def test_public_capability_declares_free_only_cobalt_routing() -> None:
    capability = load_schema()["components"]["schemas"]["ManagedCapability"]["properties"]

    assert capability["supadata_public_active"]["const"] is False
    assert capability["youtube_retrieval_provider"]["const"] == "cobalt"
    assert capability["youtube_retrieval_credits"]["const"] == 0
    assert capability["instagram_retrieval_provider"]["const"] == "cobalt"
    assert capability["instagram_retrieval_credits"]["const"] == 0
    assert capability["facebook_free_retrieval_provider"]["const"] == "cobalt"
    assert capability["facebook_paid_retrieval_configured"]["const"] is False
    assert capability["facebook_automatic_paid_retrieval"]["const"] is False
    assert capability["telegram_retrieval_provider"]["const"] == "telegram_public_web"
    assert capability["telegram_retrieval_credits"]["const"] == 0
    assert capability["paid_retrieval_fallback"]["const"] is False
    assert capability["paid_stt_fallback"]["const"] is False
