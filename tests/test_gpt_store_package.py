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
    assert manifest["release"]["developer_api_key_required"] is False
    assert manifest["release"]["external_backend_required"] is False
    assert manifest["release"]["production_smoke_test_passed"] is True
    assert manifest["release"]["production_smoke_tested_at"] == "2026-08-14"


def test_instruction_package_contains_required_workflow_boundaries() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert "Use Ukrainian by default" in text
    assert "CAPABILITY PREFLIGHT" in text
    assert "web_search=AVAILABLE" in text
    assert "web_search=UNAVAILABLE" in text
    assert "Supervisor proposes." in text
    assert "USER APPROVAL" in text
    assert "1=APPROVE, 2=EDIT, 3=REJECT" in text
    assert "Наступна допустима дія: 1 - **APPROVE**, 2 - **EDIT** або 3 - **REJECT**." in text
    assert "Present the profile itself, NOT a checkpoint" in text
    assert "Never expose internal placeholders such as :contentReference, oaicite" in text
    assert "On PASS produce normal user-facing output, NOT a checkpoint" in text
    assert "Create checkpoint ONLY when user explicitly requests" in text
    assert "Never auto-create it at a normal profile gate/final report" in text
    assert "latest_research object uses EXACTLY" in text
    assert "latest_review object uses EXACTLY" in text
    assert "K_SUPERVISOR_CHECKPOINT" in text
    assert "task_id matching ^TASK_[A-Za-z0-9_-]+$" in text
    assert "required_cross_checks:int>=0" in text
    assert 'approved_by="user"' in text
    assert "Output one complete valid JSON object" in text
    assert "Do not persist/reveal hidden chain-of-thought" in text


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


def test_manifest_can_be_parsed_without_secrets_or_external_actions() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "manifest.yaml").read_text(encoding="utf-8"))
    serialized = json.dumps(manifest, sort_keys=True)
    secret_name = "OPENAI" + "_API_KEY"

    assert secret_name not in serialized
    assert manifest["capabilities"]["actions"] is False
    assert manifest["capabilities"]["apps"] is False
    assert manifest["knowledge"]["required"] is False


def test_store_package_validation_cli_passes() -> None:
    assert validate_main() == 0
