from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "gpt_store" / "actions" / "media_public_free_openapi.yaml"


def load_schema() -> dict:
    return yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_public_free_schema_routes_youtube_only_through_gemini_direct() -> None:
    schema = load_schema()
    paths = schema["paths"]

    assert "/api/v1/media/youtube-gemini/preflight" in paths
    assert "/api/v1/media/youtube-gemini/lookup" in paths
    assert "/api/v1/media/youtube-gemini/transcriptions" in paths
    assert "/api/v1/media/youtube-gemini/transcriptions/{job_id}" in paths
    assert "/api/v1/media/youtube-gemini/transcriptions/{job_id}/segments" in paths

    assert (
        paths["/api/v1/media/youtube-gemini/preflight"]["post"]["operationId"]
        == "preflightPublicGeminiYoutube"
    )
    assert (
        paths["/api/v1/media/youtube-gemini/transcriptions"]["post"]["operationId"]
        == "startPublicGeminiYoutubeTranscription"
    )
    assert (
        paths["/api/v1/media/youtube-gemini/transcriptions"]["post"]["x-openai-isConsequential"]
        is False
    )

    instagram_request = schema["components"]["schemas"]["InstagramRequest"]
    assert "YouTube" not in instagram_request["properties"]["url"]["description"]


def test_youtube_start_requires_explicit_gemini_free_data_use_consent() -> None:
    schema = load_schema()
    request = schema["components"]["schemas"]["YoutubeGeminiStartRequest"]
    consent = schema["components"]["schemas"]["GeminiFreeConsent"]

    assert request["required"] == ["url", "gemini_free_consent"]
    assert request["properties"]["gemini_free_consent"]["$ref"] == "#/components/schemas/GeminiFreeConsent"
    assert consent["required"] == ["provider", "tier", "data_use_acknowledged"]
    assert consent["properties"]["provider"]["const"] == "google_gemini"
    assert consent["properties"]["tier"]["const"] == "free"
    assert consent["properties"]["data_use_acknowledged"]["const"] is True

    preflight = schema["components"]["schemas"]["GeminiYoutubePreflight"]["properties"]
    assert preflight["provider"]["const"] == "gemini"
    assert preflight["mode"]["const"] == "youtube_direct"
    assert preflight["retrieval_provider"]["const"] == "gemini_youtube_url"
    assert preflight["consent_required"]["const"] is True
    assert preflight["consent_provider"]["const"] == "google_gemini"
    assert preflight["consent_tier"]["const"] == "free"
    assert preflight["automatic_paid_fallback"]["const"] is False


def test_public_capabilities_declare_mixed_free_only_routing() -> None:
    capability = load_schema()["components"]["schemas"]["PublicCapabilities"]["properties"]

    assert capability["supadata_public_active"]["const"] is False
    assert capability["automatic_paid_fallback"]["const"] is False
    assert capability["paid_retrieval_fallback"]["const"] is False
    assert capability["paid_stt_fallback"]["const"] is False

    assert capability["youtube_retrieval_provider"]["const"] == "gemini_youtube_url"
    assert capability["youtube_retrieval_credits"]["const"] == 0
    assert capability["youtube_stt_provider"]["const"] == "gemini"
    assert capability["youtube_gemini_free_tier_only"]["const"] is True
    assert capability["youtube_gemini_consent_required"]["const"] is True

    assert capability["instagram_retrieval_provider"]["const"] == "cobalt"
    assert capability["instagram_retrieval_credits"]["const"] == 0
    assert capability["instagram_stt_provider"]["const"] == "assemblyai"
    assert capability["facebook_free_retrieval_provider"]["const"] == "cobalt"
    assert capability["facebook_stt_provider"]["const"] == "assemblyai"
    assert capability["telegram_retrieval_provider"]["const"] == "telegram_public_web"
    assert capability["telegram_retrieval_credits"]["const"] == 0
    assert capability["telegram_stt_provider"]["const"] == "assemblyai"


def test_public_free_schema_exposes_no_paid_legacy_or_cookie_routes() -> None:
    text = SCHEMA_PATH.read_text(encoding="utf-8").lower()
    forbidden_operation_fragments = (
        "facebook-retrieval-preflight",
        "continuemanagedfacebookpaidretrieval",
        "startmanagedmedianativetranscription",
        "startmanagedmediaaitranscription",
        "/ai-preflight",
        "/attachment-probe",
    )
    for fragment in forbidden_operation_fragments:
        assert fragment not in text

    assert "paid_retrieval_fallback: false" in text
    assert "paid_stt_fallback: false" in text
    assert "paid_proxy_fallback: false" in text
    assert "supadata_public_active: false" in text
    assert "scrapecreators_public_active: false" in text
    assert "user cookies" in text
    assert "user login" in text


def test_public_free_builder_job_id_parameters_remain_inline() -> None:
    schema = load_schema()
    paths = (
        "/api/v1/media/youtube-gemini/transcriptions/{job_id}",
        "/api/v1/media/youtube-gemini/transcriptions/{job_id}/segments",
        "/api/v1/media/managed/transcriptions/{job_id}",
        "/api/v1/media/managed/transcriptions/{job_id}/segments",
    )
    for path in paths:
        operation = schema["paths"][path]["get"]
        job = next((item for item in operation["parameters"] if item.get("name") == "job_id"), None)
        assert job is not None
        assert "$ref" not in job
        assert job["in"] == "path"
        assert job["required"] is True
        assert job["schema"]["pattern"] == "^KRCM_[A-Za-z0-9-]+$"
