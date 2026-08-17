from __future__ import annotations

import json
from pathlib import Path

import yaml

from gpt_store import StoreCheckpoint


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "gpt_store" / "manifest.yaml"


class StorePackageValidationError(RuntimeError):
    pass


def validate_store_package(root: Path = ROOT) -> dict:
    manifest_path = root / "gpt_store" / "manifest.yaml"
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise StorePackageValidationError(f"Cannot load GPT Store manifest: {exc}") from exc

    if not isinstance(manifest, dict):
        raise StorePackageValidationError("GPT Store manifest root must be a mapping")

    _require(manifest.get("schema_version") == "1.1", "manifest schema_version must be 1.1")
    product = _mapping(manifest, "product")
    model = _mapping(manifest, "model")
    capabilities = _mapping(manifest, "capabilities")
    release = _mapping(manifest, "release")
    media_release = _mapping(release, "media_input")
    actions = _mapping(manifest, "actions")
    media_action = _mapping(actions, "media_transcript")
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
    _require(
        capabilities.get("code_interpreter_data_analysis") is True,
        "data analysis must be enabled in the Store package",
    )
    _require(capabilities.get("apps") is False, "Apps must remain disabled")
    _require(capabilities.get("actions") is True, "Actions must be enabled for optional media input")

    # Core text mode remains backend-free. Media URL ingestion is explicitly scoped below.
    _require(release.get("developer_api_key_required") is False, "Core Store path must not require a developer API key")
    _require(release.get("external_backend_required") is False, "Core Store path must not require an external backend")
    _require(release.get("free_user_compatible") is True, "Store package must remain Free-user compatible")
    _require(release.get("privacy_policy_url_required_by_package") is True, "Public Action package must require a privacy policy URL")
    _require(release.get("production_smoke_test_passed") is True, "existing production smoke test must remain recorded")
    _require(
        release.get("production_smoke_tested_at") == "2026-08-14",
        "production smoke test date must preserve the launch verification date",
    )

    _require(media_release.get("enabled") is True, "media input must be enabled")
    _require(media_release.get("rollout_state") == "PREVIEW_REQUIRED", "media rollout must remain PREVIEW_REQUIRED until live validation")
    _require(media_release.get("external_backend_required") is True, "media mode must declare its external backend")
    _require(media_release.get("developer_provider_key_required") is True, "media mode must declare provider key requirement")
    _require(media_release.get("user_api_key_required") is False, "media mode must not ask users for API keys")
    _require(media_release.get("automatic_language_detection") is True, "media mode must keep language detection")
    _require(media_release.get("production_smoke_test_passed") is False, "media production smoke test must remain false before rollout")
    _require(
        set(media_release.get("supported_platforms", [])) == {"youtube"},
        "initial media platform set must be youtube",
    )
    _require(
        set(media_release.get("supported_languages", [])) == {"uk", "ru", "en"},
        "initial media language set must be uk/ru/en",
    )

    _require(media_action.get("enabled") is True, "media transcript action must be enabled")
    _require(media_action.get("authentication") == "bearer_api_key", "media action must use bearer API-key auth")
    _require(
        media_action.get("server") == "https://voicebridge-cloud-us.onrender.com",
        "media action server must match the approved VoiceBridge endpoint",
    )

    instruction_path = root / str(instructions.get("file", ""))
    try:
        instruction_text = instruction_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorePackageValidationError(f"Cannot load instruction package: {exc}") from exc

    required_instruction_tokens = [
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
        "approved_by=\"user\"",
        "Output one complete valid JSON object",
        "Do not persist/reveal hidden chain-of-thought",
    ]
    for token in required_instruction_tokens:
        _require(token in instruction_text, f"instruction package is missing required token: {token}")

    action_schema_path = root / str(media_action.get("schema", ""))
    try:
        action_schema_text = action_schema_path.read_text(encoding="utf-8")
        action_schema = yaml.safe_load(action_schema_text)
    except (OSError, yaml.YAMLError) as exc:
        raise StorePackageValidationError(f"Cannot load media Action schema: {exc}") from exc
    _require(isinstance(action_schema, dict), "media Action schema root must be a mapping")
    _require(action_schema.get("openapi") == "3.1.0", "media Action must use OpenAPI 3.1.0")
    servers = action_schema.get("servers")
    _require(isinstance(servers, list) and servers, "media Action must declare a server")
    _require(
        isinstance(servers[0], dict) and servers[0].get("url") == media_action.get("server"),
        "media Action server must match manifest",
    )
    for token in [
        "operationId: startMediaTranscription",
        "operationId: getMediaTranscriptionStatus",
        "operationId: getMediaTranscriptSegments",
        "language_hint",
        "provider_data_deleted",
        "bearerAuth",
    ]:
        _require(token in action_schema_text, f"media Action schema is missing required token: {token}")

    privacy_path = root / str(media_action.get("privacy_policy_document", ""))
    try:
        privacy_text = privacy_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorePackageValidationError(f"Cannot load media privacy policy: {exc}") from exc
    for token in [
        "AssemblyAI",
        "provider_data_deleted",
        "one hour",
        "opted out of provider model training",
        "PREVIEW / RELEASE GATE",
    ]:
        _require(token in privacy_text, f"media privacy policy is missing required token: {token}")

    checkpoint_example_path = root / str(checkpoint.get("example", ""))
    try:
        checkpoint_payload = json.loads(checkpoint_example_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StorePackageValidationError(f"Cannot load checkpoint example: {exc}") from exc
    StoreCheckpoint.model_validate(checkpoint_payload)

    return manifest


def main() -> int:
    try:
        validate_store_package()
    except Exception as exc:
        print(f"GPT Store package validation: FAIL: {exc}")
        return 1
    print("GPT Store package validation: PASS")
    return 0


def _mapping(parent: dict, key: str) -> dict:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise StorePackageValidationError(f"manifest.{key} must be a mapping")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise StorePackageValidationError(message)


if __name__ == "__main__":
    raise SystemExit(main())
