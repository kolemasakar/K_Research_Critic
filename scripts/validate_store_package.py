from __future__ import annotations

import json
from pathlib import Path

import yaml

from gpt_store import StoreCheckpoint


ROOT = Path(__file__).resolve().parents[1]
MEDIA_BETA_SERVER = "https://voicebridge-krc-media-beta-kolemasakar.onrender.com"
MEDIA_BETA_ASSEMBLYAI_EU = "https://api.eu.assemblyai.com"


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
    _require(isinstance(description, str), "Store description must be a string")
    _require(description.startswith("Користувач:"), "Store description must use the approved Ukrainian first line")
    _require(
        "\n(research supervisor for evidence-based planning" in description,
        "Store description must include the English parenthetical second line",
    )
    _require(product.get("default_language") == "uk-UA", "product.default_language must be uk-UA")
    _require(product.get("primary_channel") == "chatgpt_store", "primary channel must remain chatgpt_store")
    _require(product.get("publication_state") == "published", "publication state must remain published")
    _require(product.get("published_at") == "2026-08-14", "published_at must record the Store launch date")
    _require(product.get("store_category") == "Research & Analysis", "Store category must remain Research & Analysis")

    _require(model.get("policy") == "user_plan", "model policy must remain user_plan")
    _require(model.get("recommended_model") is None, "recommended model must remain unset")
    _require(model.get("allow_user_model_switch") is True, "user model switching must remain enabled")

    _require(capabilities.get("web_search") is True, "web search must be enabled in the Store package")
    _require(capabilities.get("code_interpreter_data_analysis") is True, "data analysis must be enabled")
    _require(capabilities.get("apps") is False, "Apps must remain disabled")
    _require(capabilities.get("actions") is True, "Actions must be enabled for optional media input")

    _require(release.get("developer_api_key_required") is False, "Core Store path must not require a developer API key")
    _require(release.get("external_backend_required") is False, "Core Store path must not require an external backend")
    _require(release.get("free_user_compatible") is True, "Store package must remain Free-user compatible")
    _require(release.get("privacy_policy_url_required_by_package") is True, "Public Action package must require a privacy policy URL")
    _require(release.get("production_smoke_test_passed") is True, "existing production smoke test must remain recorded")
    _require(release.get("production_smoke_tested_at") == "2026-08-14", "production smoke test date must remain 2026-08-14")

    _require(media_release.get("enabled") is True, "media input must be enabled")
    _require(media_release.get("rollout_state") == "PREVIEW_REQUIRED", "public media rollout must remain PREVIEW_REQUIRED")
    _require(media_release.get("external_backend_required") is True, "media mode must declare its external backend")
    _require(media_release.get("developer_provider_key_required") is True, "media mode must declare provider key requirement")
    _require(media_release.get("user_api_key_required") is False, "media mode must not ask users for API keys")
    _require(media_release.get("automatic_language_detection") is True, "media mode must keep language detection")
    _require(media_release.get("production_smoke_test_passed") is False, "media production smoke test must remain false")
    _require(set(media_release.get("supported_platforms", [])) == {"youtube"}, "initial public media platform set must remain youtube")
    _require(set(media_release.get("supported_languages", [])) == {"uk", "ru", "en"}, "initial media language set must remain uk/ru/en")

    _require(media_action.get("enabled") is True, "media transcript action must be enabled")
    _require(media_action.get("authentication") == "bearer_api_key", "media action must use bearer API-key auth")
    _require(media_action.get("server") == "https://voicebridge-cloud-us.onrender.com", "public preview server must remain production VoiceBridge until separately promoted")

    instruction_path = root / str(instructions.get("file", ""))
    instruction_text = instruction_path.read_text(encoding="utf-8")
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
            "On PASS produce normal user-facing output, NOT a checkpoint",
            "Create checkpoint ONLY when user explicitly requests",
            "K_SUPERVISOR_CHECKPOINT",
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
    _require(manifest.get("schema_version") == "0.6-beta", "media beta schema_version must be 0.6-beta")

    product = _mapping(manifest, "product")
    capabilities = _mapping(manifest, "capabilities")
    instructions = _mapping(manifest, "instructions")
    media_action = _mapping(_mapping(manifest, "actions"), "media_transcript")
    beta = _mapping(manifest, "beta")
    release = _mapping(manifest, "release")

    _require(product.get("name") == "K-Research & Critic - MEDIA BETA", "media beta product name must remain isolated")
    _require(product.get("publication_state") == "private_owner_only", "MEDIA BETA must remain private owner-only")
    _require(product.get("primary_channel") == "chatgpt_private_beta", "MEDIA BETA channel must remain private")
    _require(product.get("default_language") == "uk-UA", "media beta default language must remain Ukrainian")

    _require(capabilities.get("web_search") is True, "private media beta requires web search")
    _require(capabilities.get("code_interpreter_data_analysis") is True, "private media beta requires data analysis")
    _require(capabilities.get("image_generation") is False, "private media beta image generation must remain disabled")
    _require(capabilities.get("actions") is True, "private media beta requires Actions")
    _require(capabilities.get("apps") is False, "private media beta must not require Apps")

    _require(instructions.get("version") == "0.9-beta-a9.10", "A9.10 instruction version must be 0.9-beta-a9.10")
    _require(instructions.get("builder_package_version") == "0.9-beta-a9.10", "A9.10 Builder package version must be 0.9-beta-a9.10")
    _require(instructions.get("builder_runtime_applied") is False, "A9.10 Builder package must remain pending until the private GPT is updated")
    _require(instructions.get("builder_policy_fix_runtime_applied") is True, "A9.7-I corrected Builder policy must record runtime application")
    _require(instructions.get("builder_character_limit") == 8000, "Builder instruction limit must remain 8000")
    _require(instructions.get("canonical_reference") == "prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md", "managed instruction file must be canonical")
    _require(instructions.get("default_report_language") == "uk-UA", "default report language must remain uk-UA")
    _require(instructions.get("report_language_follows_source_language") is False, "source language must not control report language")
    _require(instructions.get("verdict_labels_localized_to_report_language") is True, "verdicts must be localized to report language")

    _require(beta.get("access_model") == "private_gpt_action_bearer_plus_server_owner_admission", "access model must keep owner admission server-side")
    _require(beta.get("intended_testers") == 1, "private beta must target owner only")
    _require(beta.get("owner_only") is True, "MEDIA BETA must remain owner-only")
    _require(beta.get("ingress_mode") == "managed_zero_client", "MEDIA BETA must use managed zero-client ingress")
    _require(beta.get("browser_helper_required") is False, "normal flow must not require Helper")
    _require(beta.get("browser_helper_normal_flow_allowed") is False, "normal flow must not use Helper")
    _require(beta.get("browser_assisted_a8_fallback_preserved") is True, "A8 fallback evidence must remain preserved")
    _require(beta.get("managed_job_prefix") == "KRCM_", "managed jobs must use KRCM_ prefix")
    _require(beta.get("public_platforms_live_accepted") == ["youtube", "instagram", "facebook", "telegram"], "YouTube, Instagram, Facebook and Telegram owner zero-client paths must be declared live accepted")
    _require(beta.get("public_platforms_in_progress") == [], "No public platform may remain in progress after Telegram private-GPT E2E acceptance")
    _require(beta.get("public_platforms_not_started") == [], "No public platform may remain not started after A9.9 backend acceptance")
    _require(beta.get("local_upload_live_accepted") is False, "local upload must remain unaccepted until full private-GPT E2E")
    _require(beta.get("managed_attachment_transport_live_accepted") is True, "A9.10 attachment transport runtime must be accepted")
    _require(beta.get("managed_attachment_backend_code_ready") is True, "A9.10 attachment backend must be code-ready")
    _require(beta.get("managed_attachment_backend_live_deployed") is True, "A9.10 attachment backend must be deployed to isolated beta")
    _require(beta.get("managed_attachment_retrieval_provider") == "openai_attachment", "A9.10 attachment retrieval provider must be openai_attachment")
    _require(beta.get("managed_attachment_retrieval_credits") == 0, "A9.10 attachment retrieval must cost zero credits")
    _require(beta.get("managed_attachment_stt_provider") == "assemblyai", "A9.10 attachment STT provider must be AssemblyAI")
    _require(beta.get("managed_attachment_action_schema_ready") is True, "A9.10 attachment Action schema must be ready")
    _require(beta.get("managed_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder update must remain pending")
    _require(beta.get("managed_attachment_ingestion_live_accepted") is False, "A9.10 full ingestion must remain pending until a real attachment STT run")
    _require(beta.get("managed_attachment_private_gpt_e2e_complete") is False, "A9.10 private-GPT E2E must remain pending")
    _require(beta.get("max_video_seconds") == 3600, "media beta max video must remain 60 minutes")
    _require(beta.get("managed_provider") == "supadata", "managed provider must remain Supadata for native-first paths")
    _require(beta.get("managed_provider_mode") == "native_first", "managed mode must remain native-first")
    _require(beta.get("managed_native_credit_cost") == 1, "native managed cost must remain one credit")
    _require(beta.get("managed_credit_preflight_required") is True, "credit preflight must remain mandatory")
    _require(beta.get("managed_explicit_user_consent_required") is True, "explicit user credit consent must remain mandatory")
    _require(beta.get("managed_automatic_ai_fallback") is False, "automatic managed AI fallback must remain disabled")
    _require(beta.get("managed_ai_requires_second_consent") is True, "AI fallback must require second consent")
    _require(beta.get("managed_instagram_ai_fallback_live_accepted") is True, "Instagram AI fallback must be live accepted")
    _require(beta.get("managed_instagram_ai_rate_credits_per_minute") == 2, "Instagram AI rate must remain 2 credits/min")
    _require(beta.get("managed_instagram_ai_hard_cap_credits") == 40, "Instagram AI consent cap must remain 40 credits")
    _require(beta.get("managed_facebook_retrieval_stt_code_ready") is True, "A9.7-C Facebook retrieval/STT must be code-ready")
    _require(beta.get("managed_facebook_free_retrieval_provider") == "cobalt", "Facebook free retrieval provider must be Cobalt")
    _require(beta.get("managed_facebook_free_path_live_accepted") is True, "Facebook Cobalt free path must be live accepted")
    _require(beta.get("managed_facebook_paid_retrieval_provider") == "scrapecreators", "Facebook paid retrieval provider must be ScrapeCreators")
    _require(beta.get("managed_facebook_paid_retrieval_configured") is False, "ScrapeCreators must remain unconfigured in this acceptance state")
    _require(beta.get("managed_facebook_paid_fallback_live_accepted") is False, "ScrapeCreators paid fallback must remain not live accepted")
    _require(beta.get("managed_facebook_paid_retrieval_max_credits") == 1, "Facebook paid retrieval hard cap must remain one credit")
    _require(beta.get("managed_facebook_paid_retrieval_requires_separate_consent") is True, "Facebook paid retrieval must require separate explicit consent")
    _require(beta.get("managed_facebook_automatic_paid_retrieval") is False, "Facebook paid retrieval must never run automatically")
    _require(beta.get("managed_facebook_stt_provider") == "assemblyai", "Facebook STT provider must be AssemblyAI")
    _require(beta.get("managed_facebook_live_accepted") is True, "Facebook free Cobalt path must be marked live accepted after H1 evidence")
    _require(beta.get("managed_telegram_code_ready") is True, "A9.9 Telegram managed path must be code-ready")
    _require(beta.get("managed_telegram_backend_live_accepted") is True, "A9.9 Telegram backend must record isolated live acceptance")
    _require(beta.get("managed_telegram_public_retrieval_provider") == "telegram_public_web", "Telegram retrieval provider must be public web")
    _require(beta.get("managed_telegram_retrieval_credits") == 0, "Telegram retrieval credits must remain zero")
    _require(beta.get("managed_telegram_stt_provider") == "assemblyai", "Telegram STT provider must be AssemblyAI")
    _require(beta.get("managed_telegram_action_schema_ready") is True, "Telegram Action schema must be package-ready")
    _require(beta.get("managed_telegram_builder_runtime_applied") is True, "Telegram Builder runtime must record actual application")
    _require(beta.get("managed_telegram_private_gpt_e2e_complete") is True, "Telegram private-GPT E2E must be accepted")

    _require(beta.get("managed_user_beta_access_code_required") is False, "owner must not be asked for a beta code")
    _require(beta.get("managed_owner_access_injected_server_side") is True, "owner admission must be injected server-side")
    _require(beta.get("managed_durable_store") == "postgres", "managed store must remain Postgres")
    _require(beta.get("managed_restart_resilient_jobs") is True, "managed jobs must remain restart resilient")
    _require(beta.get("managed_duplicate_start_reuses_job") is True, "duplicate managed start must reuse durable job")

    legacy = _mapping(beta, "legacy_browser_assisted")
    _require(legacy.get("job_prefix") == "KRCC_", "A8 fallback job prefix must remain KRCC_")
    _require(legacy.get("helper_version") == "0.2.2", "A8 fallback helper version must remain 0.2.2")
    _require(legacy.get("stt_endpoint") == MEDIA_BETA_ASSEMBLYAI_EU, "A8 fallback STT endpoint must remain AssemblyAI EU")
    _require(legacy.get("status") == "A8_ACCEPTED_FALLBACK_ONLY", "A8 must be fallback only")

    _require(release.get("rollout_state") == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING", "rollout state must record A9.10 attachment package ready / Builder pending")
    _require(release.get("production_core_unchanged") is True, "private beta must preserve production core")
    _require(release.get("public_store_gpt_unchanged") is True, "private beta must not modify public GPT")
    _require(release.get("user_api_key_required") is False, "private beta must not request user API keys")
    _require(release.get("user_beta_access_code_required") is False, "private owner flow must not request beta access code")
    _require(release.get("a9_2r_managed_native_complete") is True, "A9.2R must remain complete")
    _require(release.get("a9_3_durable_managed_complete") is True, "A9.3 must remain complete")
    _require(release.get("a9_5_private_gpt_integration_complete") is True, "A9.5 private GPT integration must remain complete")
    _require(release.get("a9_8_owner_zero_client_acceptance_complete") is True, "YouTube owner zero-client acceptance must remain complete")
    _require(release.get("a9_6_instagram_managed_complete") is True, "Instagram managed path must remain complete")
    _require(release.get("a9_6_facebook_complete") is False, "Historical A9.6 Supadata Facebook route must remain incomplete")
    _require(release.get("a9_7_c_facebook_runtime_code_ready") is True, "A9.7-C Facebook runtime contract must be recorded code-ready")
    _require(release.get("a9_7_c_facebook_live_acceptance_complete") is True, "A9.7 Facebook runtime contract must record live acceptance")
    _require(release.get("a9_7_h1_facebook_cobalt_live_acceptance_complete") is True, "A9.7-H1 Cobalt acceptance evidence must be recorded")
    _require(release.get("a9_7_i_builder_package_ready") is True, "A9.7-I Builder package must be ready")
    _require(release.get("a9_7_i_builder_runtime_applied") is True, "A9.7-I Builder runtime update must be recorded applied")
    _require(release.get("a9_7_i_builder_policy_fix_runtime_applied") is True, "A9.7-I corrected Builder policy must be applied")
    _require(release.get("a9_7_i_private_gpt_e2e_complete") is True, "A9.7-I owner private-GPT E2E must remain accepted")
    _require(release.get("a9_9_telegram_backend_complete") is True, "A9.9 Telegram backend acceptance must be complete")
    _require(release.get("a9_9_telegram_action_package_complete") is True, "A9.9 Telegram Action package must be complete")
    _require(release.get("a9_9_telegram_builder_runtime_applied") is True, "A9.9 Telegram Builder runtime must be applied")
    _require(release.get("a9_9_telegram_private_gpt_e2e_complete") is True, "A9.9 Telegram private-GPT E2E must be accepted")
    _require(release.get("a9_10_attachment_transport_runtime_accepted") is True, "A9.10 attachment transport runtime acceptance must be recorded")
    _require(release.get("a9_10_attachment_backend_code_ready") is True, "A9.10 attachment backend must be code-ready")
    _require(release.get("a9_10_attachment_backend_live_deployed") is True, "A9.10 attachment backend must be live on isolated beta")
    _require(release.get("a9_10_attachment_action_package_complete") is True, "A9.10 attachment Action package must be complete")
    _require(release.get("a9_10_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder application must remain pending")
    _require(release.get("a9_10_attachment_ingestion_live_accepted") is False, "A9.10 full attachment ingestion must remain pending")
    _require(release.get("a9_10_attachment_private_gpt_e2e_complete") is False, "A9.10 attachment private-GPT E2E must remain pending")
    _require(release.get("gpt_builder_private_update_required") is True, "A9.10 package requires a private Builder update")
    _require(release.get("external_tester_rollout_paused") is True, "external tester rollout must remain paused")
    _require(release.get("merge_to_public_product_allowed") is False, "private beta must not auto-promote to public product")

    _require(media_action.get("authentication") == "bearer_api_key", "private beta Action must use bearer authentication")
    _require(media_action.get("server") == MEDIA_BETA_SERVER, "private beta Action must use dedicated beta Render service")
    _require(media_action.get("schema") == "gpt_store/actions/media_managed_beta_openapi.yaml", "private beta must use managed Action schema")

    builder_path = root / str(instructions.get("file", ""))
    builder_text = builder_path.read_text(encoding="utf-8")
    _require(len(builder_text) <= 8000, "private beta Builder instructions must fit the 8000-character limit")
    _require_tokens(
        builder_text,
        [
            "K-Research & Critic - MEDIA BETA",
            "REPORT LANGUAGE INVARIANT",
            "Source/transcript language never controls report language",
            "OWNER-ONLY ZERO-CLIENT MEDIA",
            "preflightManagedMediaCredits",
            "startManagedMediaNativeTranscription",
            "getManagedMediaTranscriptionStatus",
            "getManagedMediaTranscriptSegments",
            "preflightManagedMediaAiCredits",
            "startManagedMediaAiTranscription",
            "startManagedTelegramPublicTranscription",
            "startManagedAttachmentTranscription",
            "Do NOT ask the user for beta access code",
            "Do not expose `KRCM_...` Job IDs",
            "Do not fall back to Helper in the normal owner flow",
            "1 - Так",
            "2 - Ні",
            "AWAITING_AI_CONSENT",
            "credit_charge_uncertain=true",
            "1=APPROVE, 2=EDIT, 3=REJECT",
        ],
        "A9.9 Builder instructions",
    )

    action_path = root / str(media_action.get("schema", ""))
    action_text = action_path.read_text(encoding="utf-8")
    action = _load_yaml(action_path, "managed media Action schema")
    _require(action.get("openapi") == "3.1.0", "managed media Action must use OpenAPI 3.1.0")
    servers = action.get("servers")
    _require(isinstance(servers, list) and bool(servers), "managed media Action must declare a server")
    _require(isinstance(servers[0], dict) and servers[0].get("url") == MEDIA_BETA_SERVER, "managed Action must use dedicated beta server")
    _require_tokens(
        action_text,
        [
            "version: 0.6.0-a9.10",
            "operationId: getManagedMediaCapability",
            "operationId: preflightManagedMediaCredits",
            "operationId: startManagedMediaNativeTranscription",
            "operationId: startManagedFacebookFallback",
            "operationId: startManagedTelegramPublicTranscription",
            "operationId: startManagedAttachmentTranscription",
            "operationId: preflightManagedFacebookRetrievalCredit",
            "operationId: continueManagedFacebookPaidRetrieval",
            "operationId: getManagedMediaTranscriptionStatus",
            "operationId: getManagedMediaTranscriptSegments",
            "operationId: preflightManagedMediaAiCredits",
            "operationId: startManagedMediaAiTranscription",
            "x-openai-isConsequential: true",
            "x-openai-isConsequential: false",
            "const: supadata",
            "const: native",
            "const: generate",
            "const: scrapecreators",
            "const: facebook_post",
            "const: cobalt",
            "const: assemblyai",
            "maximum: 1",
            "AWAITING_RETRIEVAL_CONSENT",
            "facebook_retrieval_stt",
            "telegram_public_retrieval_stt",
            "telegram_public_web",
            "attachment_upload_stt",
            "openai_attachment",
            "provider_balance_lookup_performed",
            "retrieval_credits_charged",
            "stt_seconds_charged",
            "credit_charge_uncertain",
            "reused",
            "bearerAuth",
        ],
        "A9.9 managed Action schema",
    )
    _require("beta_access_code" not in action_text, "user-facing Action schema must not expose beta_access_code")

    privacy_path = root / str(media_action.get("privacy_policy_document", ""))
    privacy_text = privacy_path.read_text(encoding="utf-8")
    _require_tokens(
        privacy_text,
        [
            "AssemblyAI",
            MEDIA_BETA_ASSEMBLYAI_EU,
            "files submitted through its European servers are not used for model training",
        ],
        "media beta privacy policy",
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
