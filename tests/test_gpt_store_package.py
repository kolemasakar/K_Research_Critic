from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from gpt_store import StoreCheckpoint
from scripts.validate_store_package import main as validate_main, validate_store_package


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_preserves_store_first_invariants() -> None:
    manifest = validate_store_package(ROOT)

    assert manifest["product"]["name"] == "K-Research & Critic"
    description = manifest["product"]["description"]
    assert description.startswith("Користувач:")
    assert "\n(research supervisor for evidence-based planning" in description
    assert manifest["product"]["default_language"] == "uk-UA"
    assert manifest["product"]["primary_channel"] == "chatgpt_store"
    assert manifest["product"]["publication_state"] == "published"
    assert manifest["product"]["published_at"] == "2026-08-14"
    assert manifest["product"]["store_category"] == "Research & Analysis"
    assert manifest["model"]["policy"] == "user_plan"
    assert manifest["model"]["recommended_model"] is None
    assert manifest["model"]["allow_user_model_switch"] is True
    assert manifest["capabilities"]["web_search"] is True
    assert manifest["capabilities"]["code_interpreter_data_analysis"] is True
    assert manifest["capabilities"]["apps"] is False
    assert manifest["capabilities"]["actions"] is False
    release = manifest["release"]
    assert release["developer_api_key_required"] is False
    assert release["external_backend_required"] is False
    assert release["privacy_policy_url_required_by_package"] is False
    assert release["production_smoke_test_passed"] is True
    assert release["latest_core_runtime_regression_passed_at"] == "2026-08-23"
    assert release["criticprofile_two_stage_gate_runtime_accepted"] is True
    assert release["cross_check_claim_level_runtime_accepted"] is True
    assert release["cross_check_traceability_runtime_accepted"] is True
    assert release["report_label_localization_runtime_accepted"] is True
    assert release["request_log_runtime_accepted"] is True
    assert release["request_log_public_enabled"] is False
    assert release["request_log_disablement_runtime_accepted"] is True
    assert release["repository_matches_current_public_builder"] is True


def test_instruction_package_matches_accepted_public_core_runtime() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "ALWAYS reply in Ukrainian" in text
    assert "Профіль збору і критики успішно створено." in text
    assert "1 - виконати аналіз одразу." in text
    assert "2 - переглянути і відредагувати профіль збору і критики." in text
    assert "1 - прийняти профіль, виконати дослідження." in text
    assert "Cross-check floors: LOW>=0, MEDIUM>=1, HIGH>=2, CRITICAL>=3" in text
    assert "For EACH material factual claim" in text
    assert "A systematic review/meta-analysis counts as one evidence origin" in text
    assert "TRACEABILITY INVARIANT" in text
    assert "Critic must inspect each material claim ledger" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text
    assert "`ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`" in text
    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text
    assert "COMPLETED_WITH_LIMITATIONS" in text
    assert "Only when explicitly asked to save/resume across chats" in text
    assert "REQUEST LOGGING" not in text
    assert "logRequest" not in text
    assert "CAPABILITY PREFLIGHT" not in text
    assert "Наступна допустима дія: 1 - **APPROVE**" not in text


def test_manifest_declares_accepted_core_contract() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "manifest.yaml").read_text(encoding="utf-8"))
    instructions = manifest["instructions"]

    assert instructions["version"] == "2.2-request-log-disabled-runtime-accepted"
    assert instructions["builder_character_limit"] == 8000
    assert instructions["default_report_language"] == "uk-UA"
    assert instructions["report_language_follows_source_language"] is False
    assert instructions["user_visible_labels_localized_to_report_language"] is True
    assert instructions["criticprofile_field_labels_localized_to_report_language"] is True
    assert instructions["profile_gate_mode"] == "two_stage_direct_or_review"
    assert instructions["profile_auto_display"] is False
    assert instructions["profile_direct_run_approves_profile"] is True
    assert instructions["profile_review_option"] == 2
    assert instructions["profile_cancel_option"] == 3
    assert instructions["cross_check_claim_level_ledger_required"] is True
    assert instructions["cross_check_claim_level_output_required"] is True
    assert instructions["cross_check_traceability_required"] is True
    assert instructions["cross_check_achieved_cannot_exceed_visible_origins"] is True
    assert instructions["cross_check_systematic_review_counts_as_one_origin"] is True
    assert instructions["cross_check_protocol_table_required"] is True
    assert instructions["cross_check_protocol_table_columns"] == [
        "Твердження",
        "Потрібно",
        "Отримано незалежних",
        "Виняток",
    ]
    assert instructions["cross_check_floor_by_risk"] == {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }


def test_checkpoint_example_validates_and_round_trips() -> None:
    payload = json.loads((ROOT / "gpt_store" / "checkpoint_example.json").read_text(encoding="utf-8"))

    checkpoint = StoreCheckpoint.model_validate(payload)
    restored = StoreCheckpoint.model_validate_json(checkpoint.model_dump_json())

    assert restored == checkpoint
    assert restored.workflow_state == "PROFILE_APPROVED"
    assert restored.resume_policy == "CONFIRM_RESUME"
    assert restored.distribution.developer_api_key_required is False


def test_checkpoint_rejects_unsafe_mid_agent_state() -> None:
    payload = json.loads((ROOT / "gpt_store" / "checkpoint_example.json").read_text(encoding="utf-8"))
    payload["workflow_state"] = "RESEARCHING"

    with pytest.raises(ValidationError):
        StoreCheckpoint.model_validate(payload)


def test_checkpoint_rejects_resume_policy_mismatch() -> None:
    payload = json.loads((ROOT / "gpt_store" / "checkpoint_example.json").read_text(encoding="utf-8"))
    payload["resume_policy"] = "TERMINAL"

    with pytest.raises(ValidationError, match="CONFIRM_RESUME"):
        StoreCheckpoint.model_validate(payload)


def test_checkpoint_rejects_extra_research_keys() -> None:
    payload = json.loads((ROOT / "gpt_store" / "checkpoint_example.json").read_text(encoding="utf-8"))
    payload["latest_research"] = {
        "summary": "Research summary",
        "findings": [],
        "claims": [],
        "sources": [],
        "uncertainties": [],
        "limitations": [],
        "capability_preflight": "web_search=AVAILABLE",
    }

    with pytest.raises(ValidationError):
        StoreCheckpoint.model_validate(payload)


def test_checkpoint_rejects_extra_review_keys() -> None:
    payload = json.loads((ROOT / "gpt_store" / "checkpoint_example.json").read_text(encoding="utf-8"))
    payload["latest_review"] = {
        "decision": "PASS",
        "reliability_score": 0.9,
        "critical_issues": [],
        "unsupported_claims": [],
        "weak_sources": [],
        "contradictions": [],
        "missing_topics": [],
        "recommended_changes": [],
        "verification_sources": [],
    }

    with pytest.raises(ValidationError):
        StoreCheckpoint.model_validate(payload)


def test_manifest_can_be_parsed_without_secrets_or_active_actions() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "manifest.yaml").read_text(encoding="utf-8"))
    serialized = json.dumps(manifest, sort_keys=True)
    secret_name = "OPENAI" + "_API_KEY"

    assert secret_name not in serialized
    assert manifest["capabilities"]["actions"] is False
    assert manifest["capabilities"]["apps"] is False
    assert manifest["knowledge"]["required"] is False
    assert manifest["request_log_mvp"]["prototype_retained"] is True
    assert manifest["request_log_mvp"]["public_enabled_target"] is False
    assert manifest["request_log_mvp"]["disablement_runtime_accepted"] is True


def test_store_package_validation_cli_passes() -> None:
    assert validate_main() == 0
