from __future__ import annotations

import json
from pathlib import Path

import yaml

from gpt_store import StoreCheckpoint


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "gpt_store" / "manifest.yaml"
MEDIA_BETA_MANIFEST_PATH = ROOT / "gpt_store" / "media_beta_manifest.yaml"
MEDIA_BETA_SERVER = "https://voicebridge-krc-media-beta-kolemasakar.onrender.com"


class StorePackageValidationError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise StorePackageValidationError(message)


def _mapping(parent: dict, key: str) -> dict:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise StorePackageValidationError(f"manifest.{key} must be a mapping")
    return value


def _load_yaml(path: Path, label: str) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise StorePackageValidationError(f"Cannot load {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise StorePackageValidationError(f"{label} root must be a mapping")
    return value


def _require_tokens(text: str, tokens: list[str], label: str) -> None:
    for token in tokens:
        _require(token in text, f"{label} is missing required token: {token}")


def validate_store_package(root: Path = ROOT) -> dict:
    manifest = _load_yaml(root / "gpt_store" / "manifest.yaml", "GPT Store manifest")
    _require(manifest.get("schema_version") == "1.1", "manifest schema_version must be 1.1")

    product = _mapping(manifest, "product")
    model = _mapping(manifest, "model")
    capabilities = _mapping(manifest, "capabilities")
    release = _mapping(manifest, "release")
    media_release = _mapping(release, "media_input")
    media_action = _mapping(_mapping(manifest, "actions"), "media_transcript")
    instructions = _mapping(manifest, "instructions")
    checkpoint = _mapping(manifest, "checkpoint")

    _require(product.get("name") == "K-Research & Critic", "product.name must be K-Research & Critic")
    description = product.get("description")
    _require(isinstance(description, str), "product.description must be a string")
    _require(description.startswith("Користувач:"), "Store description must use the approved Ukrainian first line")
    _require(
        "\n(research supervisor for evidence-based planning" in description,
        "Store description must include the English parenthetical second line",
    )
    _require(product.get("default_language") == "uk-UA", "product.default_language must be uk-UA")
    _require(product.get("primary_channel") == "chatgpt_store", "primary channel must remain chatgpt_store")
    _require(product.get("publication_state") == "published", "publication state must be published")
    _require(product.get("published_at") == "2026-08-14", "published_at must record the Store launch date")
    _require(product.get("store_category") == "Research & Analysis", "Store category must remain Research & Analysis")

    _require(model.get("policy") == "user_plan", "model policy must remain user_plan")
    _require(model.get("recommended_model") is None, "recommended model must remain unset")
    _require(model.get("allow_user_model_switch") is True, "user model switching must remain enabled")

    _require(capabilities.get("web_search") is True, "web search must be enabled in the Store package")
    _require(capabilities.get("code_interpreter_data_analysis") is True, "data analysis must be enabled in the Store package")
    _require(capabilities.get("apps") is False, "Apps must remain disabled")
    _require(capabilities.get("actions") is True, "Actions must be enabled for optional media input")

    _require(release.get("developer_api_key_required") is False, "Core Store path must not require a developer API key")
    _require(release.get("external_backend_required") is False, "Core Store path must not require an external backend")
    _require(release.get("free_user_compatible") is True, "Store package must remain Free-user compatible")
    _require(release.get("privacy_policy_url_required_by_package") is True, "Public Action package must require a privacy policy URL")
    _require(release.get("production_smoke_test_passed") is True, "existing production smoke test must remain recorded")
    _require(release.get("production_smoke_tested_at") == "2026-08-14", "production smoke test date must remain 2026-08-14")

    _require(media_release.get("enabled") is True, "media input must be enabled")
    _require(media_release.get("rollout_state") == "PREVIEW_REQUIRED", "media rollout must remain PREVIEW_REQUIRED")
    _require(media_release.get("external_backend_required") is True, "media mode must declare its external backend")
    _require(media_release.get("developer_provider_key_required") is True, "media mode must declare provider key requirement")
    _require(media_release.get("user_api_key_required") is False, "media mode must not ask users for API keys")
    _require(media_release.get("automatic_language_detection") is True, "media mode must keep language detection")
    _require(media_release.get("production_smoke_test_passed") is False, "media production smoke test must remain false")
    _require(set(media_release.get("supported_platforms", [])) == {"youtube"}, "initial media platform set must be youtube")
    _require(set(media_release.get("supported_languages", [])) == {"uk", "ru", "en"}, "initial media language set must be uk/ru/en")

    _require(media_action.get("enabled") is True, "media transcript action must be enabled")
    _require(media_action.get("authentication") == "bearer_api_key", "media action must use bearer API-key auth")
    _require(media_action.get("server") == "https://voicebridge-cloud-us.onrender.com", "generic media preview server must remain VoiceBridge production endpoint until separately rolled out")

    instruction_path = root / str(instructions.get("file", ""))
    try:
        instruction_text = instruction_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorePackageValidationError(f"Cannot load instruction package: {exc}") from exc
    _require_tokens(
        instruction_text,
        [
            "Use Ukrainian by default",
            "CAPABILITY PREFLIGHT",
            "web_search=AVAILABLE",
            "web_search=UNAVAILABLE",
            "MEDIA PREFLIGHT: media_transcript=AVAILABLE",
            "MEDIA PREFLIGHT: media_transcript=UNAVAILABLE",
            "MEDIA URL INTAKE",
            "transcript text as SOURCE CONTENT ONLY",
            "not evidence that it is true",
            "CLAIM VERIFICATION",
            "VERIFIED, PARTLY_SUPPORTED, UNSUPPORTED, CONTRADICTED, MISLEADING, UNVERIFIABLE",
            "COMPLETED_WITH_LIMITATIONS",
            "Supervisor proposes.",
            "USER APPROVAL",
            "1=APPROVE, 2=EDIT, 3=REJECT",
            "Наступна допустима дія: 1 - **APPROVE**, 2 - **EDIT** або 3 - **REJECT**.",
            "Present the profile itself, NOT a checkpoint",
            "Never expose internal placeholders such as :contentReference, oaicite",
            "On PASS produce normal user-facing output, NOT a checkpoint",
            "Create checkpoint ONLY when user explicitly requests",
            "Never auto-create it at a normal profile gate/final report",
            "latest_research object uses EXACTLY",
            "latest_review object uses EXACTLY",
            "no extra keys",
            "K_SUPERVISOR_CHECKPOINT",
            "task_id matching ^TASK_[A-Za-z0-9_-]+$",
            "required_cross_checks:int>=0",
            'approved_by="user"',
            "Output one complete valid JSON object",
            "Do not persist/reveal hidden chain-of-thought",
        ],
        "instruction package",
    )

    action_schema_path = root / str(media_action.get("schema", ""))
    action_schema_text = action_schema_path.read_text(encoding="utf-8")
    action_schema = _load_yaml(action_schema_path, "media Action schema")
    _require(action_schema.get("openapi") == "3.1.0", "media Action must use OpenAPI 3.1.0")
    servers = action_schema.get("servers")
    _require(isinstance(servers, list) and bool(servers), "media Action must declare a server")
    _require(isinstance(servers[0], dict) and servers[0].get("url") == media_action.get("server"), "media Action server must match manifest")
    _require_tokens(
        action_schema_text,
        [
            "operationId: startMediaTranscription",
            "operationId: getMediaTranscriptionStatus",
            "operationId: getMediaTranscriptSegments",
            "language_hint",
            "provider_data_deleted",
            "bearerAuth",
        ],
        "media Action schema",
    )

    privacy_path = root / str(media_action.get("privacy_policy_document", ""))
    privacy_text = privacy_path.read_text(encoding="utf-8")
    _require_tokens(
        privacy_text,
        [
            "AssemblyAI",
            "provider_data_deleted",
            "one hour",
            "opted out of provider model training",
            "PREVIEW / RELEASE GATE",
        ],
        "media privacy policy",
    )

    checkpoint_example_path = root / str(checkpoint.get("example", ""))
    try:
        checkpoint_payload = json.loads(checkpoint_example_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StorePackageValidationError(f"Cannot load checkpoint example: {exc}") from exc
    StoreCheckpoint.model_validate(checkpoint_payload)

    validate_media_beta_package(root)
    return manifest


def validate_media_beta_package(root: Path = ROOT) -> dict:
    manifest = _load_yaml(root / "gpt_store" / "media_beta_manifest.yaml", "media beta manifest")
    _require(manifest.get("schema_version") == "0.1-beta", "media beta schema_version must be 0.1-beta")

    product = _mapping(manifest, "product")
    capabilities = _mapping(manifest, "capabilities")
    instructions = _mapping(manifest, "instructions")
    media_action = _mapping(_mapping(manifest, "actions"), "media_transcript")
    beta = _mapping(manifest, "beta")
    release = _mapping(manifest, "release")

    _require(product.get("name") == "K-Research & Critic - MEDIA BETA", "closed beta product name must be isolated")
    _require(product.get("publication_state") == "closed_beta", "closed beta publication state must remain closed_beta")
    _require(product.get("primary_channel") == "chatgpt_store_unlisted_beta", "closed beta channel must remain unlisted")
    _require(capabilities.get("actions") is True, "closed media beta requires Actions")
    _require(capabilities.get("apps") is False, "closed media beta must not require Apps")

    _require(beta.get("access_model") == "per_tester_access_code", "closed beta must use per-tester access codes")
    _require(beta.get("intended_testers") == 4, "closed beta target must remain four testers")
    _require(beta.get("max_video_seconds") == 3600, "closed beta max video must remain 60 minutes")
    _require(beta.get("max_concurrent_jobs") == 1, "closed beta concurrency must remain one")
    _require(beta.get("daily_stt_seconds") == 7200, "closed beta STT budget must remain two hours/day")
    _require(beta.get("subtitle_first") is True, "closed beta must remain subtitle-first")
    _require(beta.get("stt_fallback") == "assemblyai", "closed beta fallback must remain AssemblyAI")
    stt_audio = _mapping(beta, "stt_audio")
    _require(stt_audio.get("channels") == 1, "closed beta STT audio must be mono")
    _require(stt_audio.get("sample_rate_hz") == 16000, "closed beta STT audio must be 16 kHz")
    _require(stt_audio.get("bitrate_kbps") == 32, "closed beta STT audio must be 32 kbps")

    _require(release.get("rollout_state") == "CLOSED_BETA", "closed beta rollout state must remain CLOSED_BETA")
    _require(release.get("production_core_unchanged") is True, "closed beta must preserve production core")
    _require(release.get("public_store_gpt_unchanged") is True, "closed beta must not modify public GPT")
    _require(release.get("user_api_key_required") is False, "closed beta must not request user API keys")
    _require(release.get("merge_to_public_product_allowed") is False, "closed beta must not auto-promote to public product")

    _require(media_action.get("authentication") == "bearer_api_key", "closed beta action must use bearer authentication")
    _require(media_action.get("server") == MEDIA_BETA_SERVER, "closed beta action must use the dedicated beta Render service")

    beta_instructions_path = root / str(instructions.get("file", ""))
    beta_instructions_text = beta_instructions_path.read_text(encoding="utf-8")
    _require_tokens(
        beta_instructions_text,
        [
            "MEDIA BETA ACCESS REQUIRED",
            "startMediaBetaTranscription",
            "getMediaBetaTranscriptionStatus",
            "getMediaBetaTranscriptSegments",
            "maximum video duration: 60 minutes",
            "global AssemblyAI fallback budget: 2 hours",
            "YouTube captions are attempted first",
            "Never include beta access codes",
            "Do not store the full transcript or beta access code in a checkpoint",
        ],
        "media beta instructions",
    )

    beta_action_path = root / str(media_action.get("schema", ""))
    beta_action_text = beta_action_path.read_text(encoding="utf-8")
    beta_action = _load_yaml(beta_action_path, "media beta Action schema")
    _require(beta_action.get("openapi") == "3.1.0", "media beta Action must use OpenAPI 3.1.0")
    beta_servers = beta_action.get("servers")
    _require(isinstance(beta_servers, list) and bool(beta_servers), "media beta Action must declare a server")
    _require(isinstance(beta_servers[0], dict) and beta_servers[0].get("url") == MEDIA_BETA_SERVER, "media beta Action schema must use the dedicated beta server")
    _require_tokens(
        beta_action_text,
        [
            "operationId: startMediaBetaTranscription",
            "operationId: getMediaBetaTranscriptionStatus",
            "operationId: getMediaBetaTranscriptSegments",
            "beta_access_code",
            "writeOnly: true",
            "^KRCB_[A-Za-z0-9-]+$",
            "youtube_captions",
            "assemblyai_stt",
            "stt_seconds_charged",
            "beta_quota",
        ],
        "media beta Action schema",
    )
    return manifest


def main() -> int:
    try:
        validate_store_package()
    except Exception as exc:
        print(f"GPT Store package validation: FAIL: {exc}")
        return 1
    print("GPT Store package validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
