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
    _require(product.get("default_language") == "uk-UA", "product.default_language must be uk-UA")
    _require(product.get("primary_channel") == "chatgpt_store", "primary channel must remain chatgpt_store")
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
        "actually exposed in the current runtime",
        "COMPLETED_WITH_LIMITATIONS",
        "Supervisor proposes.",
        "USER APPROVAL",
        "APPROVE",
        "EDIT",
        "REJECT",
        "PASS",
        "REVISE",
        "K_SUPERVISOR_CHECKPOINT",
        "task_id matching ^TASK_[A-Za-z0-9_-]+$",
        "required_cross_checks:int >=0",
        "approved_by=\"user\"",
        "Output one complete valid JSON object",
        "Do not persist or reveal hidden chain-of-thought",
    ]
    for token in required_instruction_tokens:
        _require(token in instruction_text, f"instruction package is missing required token: {token}")

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
