from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "gpt_store" / "actions" / "media_public_r3_openapi.yaml"
CORE = ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md"
ADDENDUM = ROOT / "prompts" / "GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md"


def load_schema() -> dict:
    return yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))


def test_r3_schema_is_checkpoint_89_free_only_candidate() -> None:
    schema = load_schema()
    assert schema["x-krc-release-state"] == "R3_REPOSITORY_CANDIDATE_BUILDER_HOLD"
    assert schema["x-krc-canonical-checkpoint"].startswith("89_R2_FULL_ACCEPTANCE")
    policy = schema["x-krc-free-only-policy"]
    assert policy["paid_retrieval_fallback"] is False
    assert policy["paid_stt_fallback"] is False
    assert policy["paid_proxy_fallback"] is False
    assert policy["supadata_public_active"] is False
    assert policy["scrapecreators_public_active"] is False
    assert policy["cookie_login_fallback"] is False
    assert policy["failed_free_only_retry"] == "fresh_deterministic_job"
    assert policy["failed_paid_or_charge_uncertain_retry"] == "blocked"


def test_r3_routes_preserve_accepted_provider_split() -> None:
    schema = load_schema()
    paths = schema["paths"]
    assert paths["/api/v1/media/youtube-gemini/transcriptions"]["post"]["operationId"] == "startPublicGeminiYoutubeTranscription"
    assert paths["/api/v1/media/managed/transcriptions"]["post"]["operationId"] == "startPublicInstagramCobaltTranscription"
    assert paths["/api/v1/media/managed/facebook-fallback"]["post"]["operationId"] == "startPublicFacebookCobaltTranscription"
    assert paths["/api/v1/media/managed/telegram"]["post"]["operationId"] == "startPublicTelegramTranscription"

    instagram = schema["components"]["schemas"]["InstagramRequest"]["properties"]["url"]["description"]
    assert "Instagram" in instagram
    assert "YouTube" not in instagram

    facebook = paths["/api/v1/media/managed/facebook-fallback"]["post"]["description"]
    assert "video+audio" in facebook
    assert "ffmpeg" in facebook
    assert "16 kHz" in facebook


def test_r3_youtube_requires_gemini_free_consent() -> None:
    schema = load_schema()
    request = schema["components"]["schemas"]["YoutubeGeminiStartRequest"]
    assert request["required"] == ["url", "gemini_free_consent"]
    consent = schema["components"]["schemas"]["GeminiFreeConsent"]
    assert consent["properties"]["provider"]["const"] == "google_gemini"
    assert consent["properties"]["tier"]["const"] == "free"
    assert consent["properties"]["data_use_acknowledged"]["const"] is True


def test_r3_schema_exposes_no_paid_or_legacy_start_routes() -> None:
    text = SCHEMA.read_text(encoding="utf-8").lower()
    forbidden = (
        "facebook-retrieval-preflight",
        "continuemanagedfacebookpaidretrieval",
        "startmanagedmedianativetranscription",
        "startmanagedmediaaitranscription",
        "/ai-preflight",
        "/attachment-probe",
    )
    for value in forbidden:
        assert value not in text


def test_core_plus_media_addendum_fits_builder_limit_and_keeps_isolation() -> None:
    core = CORE.read_text(encoding="utf-8").rstrip()
    addendum = ADDENDUM.read_text(encoding="utf-8").strip()
    combined = core + "\n\n" + addendum
    assert len(combined) <= 8000
    assert "MEDIA failure never blocks Core" in addendum
    assert "YouTube=Gemini Free direct" in addendum
    assert "FAILED free-only may be freshly retried" in addendum
    assert "new explicit retry request" in addendum
    assert "once only" not in addendum
    assert "CriticProfile gate" in addendum
