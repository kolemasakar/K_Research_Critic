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

    product = _mapping(manifest, "product")
    model = _mapping(manifest, "model")
    capabilities = _mapping(manifest, "capabilities")
    release = _mapping(manifest, "release")
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
    _require(capabilities.get("apps") is False, "Apps must remain disabled for the core package")
    _require(capabilities.get("actions") is False, "Actions must remain disabled for the core package")
    _require(release.get("developer_api_key_required") is False, "Store package must not require a developer API key")
    _require(release.get("external_backend_required") is False, "Store package must not require an external backend")
    _require(release.get("free_user_compatible") is True, "Store package must remain Free-user compatible")
    _require(release.get("production_smoke_test_passed") is True, "production smoke test must be recorded as passed")
    _require(release.get("production_smoke_tested_at") == "2026-08-14", "launch smoke-test date must remain recorded")
    _require(release.get("latest_core_runtime_regression_passed_at") == "2026-08-23", "latest Core runtime regression must be recorded")
    _require(release.get("criticprofile_two_stage_gate_runtime_accepted") is True, "two-stage CriticProfile gate must be accepted")
    _require(release.get("cross_check_claim_level_runtime_accepted") is True, "claim-level cross-check runtime must be accepted")
    _require(release.get("cross_check_traceability_runtime_accepted") is True, "traceability runtime must be accepted")
    _require(release.get("report_label_localization_runtime_accepted") is True, "report-label localization runtime must be accepted")
    _require(release.get("repository_matches_current_public_builder") is True, "repository must match the accepted public Builder")

    _require(instructions.get("builder_character_limit") == 8000, "Builder character limit must be 8000")
    _require(instructions.get("default_report_language") == "uk-UA", "default report language must be uk-UA")
    _require(instructions.get("profile_gate_mode") == "two_stage_direct_or_review", "two-stage profile gate must be declared")
    _require(instructions.get("profile_auto_display") is False, "profile must not auto-display")
    _require(instructions.get("cross_check_traceability_required") is True, "traceability must be required")
    _require(
        instructions.get("cross_check_achieved_cannot_exceed_visible_origins") is True,
        "achieved cross-check count cannot exceed visible origins",
    )
    _require(
        instructions.get("cross_check_protocol_table_columns")
        == ["Твердження", "Потрібно", "Отримано незалежних", "Виняток"],
        "Ukrainian claim-summary columns must match the accepted runtime",
    )

    instruction_path = root / str(instructions.get("file", ""))
    try:
        instruction_text = instruction_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorePackageValidationError(f"Cannot load instruction package: {exc}") from exc

    _require(len(instruction_text) <= 8000, "public Builder instructions must fit the 8000-character limit")
    required_instruction_tokens = [
        "ALWAYS reply in Ukrainian",
        "Профіль збору і критики успішно створено.",
        "1 - виконати аналіз одразу.",
        "2 - переглянути і відредагувати профіль збору і критики.",
        "Cross-check floors: LOW>=0, MEDIUM>=1, HIGH>=2, CRITICAL>=3",
        "For EACH material factual claim",
        "A systematic review/meta-analysis counts as one evidence origin",
        "TRACEABILITY INVARIANT",
        "Critic must inspect each material claim ledger",
        "Cross-check: achieved/required - PASS|SHORTFALL",
        "ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ",
        "Твердження | Потрібно | Отримано незалежних | Виняток",
        "Localize CriticProfile field labels",
        "COMPLETED_WITH_LIMITATIONS",
        "Only when explicitly asked to save/resume across chats",
    ]
    for token in required_instruction_tokens:
        _require(token in instruction_text, f"instruction package is missing required token: {token}")

    forbidden_instruction_tokens = [
        "CAPABILITY PREFLIGHT",
        "Наступна допустима дія: 1 - **APPROVE**",
        "Present the profile itself, NOT a checkpoint",
    ]
    for token in forbidden_instruction_tokens:
        _require(token not in instruction_text, f"obsolete public Builder behavior remains: {token}")

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
