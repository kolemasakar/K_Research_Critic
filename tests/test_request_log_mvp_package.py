from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_request_log_manifest_contract() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "manifest.yaml").read_text(encoding="utf-8"))
    request_log = manifest["request_log_mvp"]

    assert request_log["status"] == "DISABLED_DUE_TO_USER_CONSENT_UX_PENDING_BUILDER_SYNC"
    assert request_log["public_enabled_target"] is False
    assert request_log["prototype_retained"] is True
    assert request_log["historical_runtime_acceptance_preserved"] is True
    assert request_log["selected_storage"] == "google_sheets"
    assert request_log["sheet_name"] == "Звернення"
    assert request_log["timezone"] == "Europe/Kyiv"
    assert request_log["authentication"] == "none"
    assert request_log["full_prompt_storage"] is False
    assert request_log["user_name_mode"] == "none"
    assert request_log["topic_max_length"] == 160
    assert request_log["logging_failure_blocks_core_workflow"] is False
    assert request_log["google_sheet_created"] is True
    assert request_log["apps_script_deployed"] is True
    assert request_log["builder_action_currently_configured"] is True
    assert request_log["builder_action_disable_pending_manual_step"] is True
    assert request_log["builder_action_test_passed"] is True
    assert request_log["google_sheet_write_test_passed"] is True
    assert request_log["runtime_new_chat_test_passed"] is True
    assert request_log["workflow_reply_dedup_verified"] is True
    assert request_log["runtime_accepted"] is True


def test_apps_script_prototype_is_retained() -> None:
    text = (ROOT / "integrations" / "request_log" / "google_apps_script" / "Code.gs").read_text(
        encoding="utf-8"
    )

    assert "LockService.getScriptLock" in text
    assert "Europe/Kyiv" in text
    assert "Utilities.formatDate" in text
    assert "'none'" in text
    assert ".slice(0, 160)" in text
    assert "appendRow" in text


def test_action_schema_prototype_is_retained() -> None:
    schema = yaml.safe_load((ROOT / "integrations" / "request_log" / "openapi.yaml").read_text(encoding="utf-8"))
    operation = schema["paths"]["/exec"]["post"]
    topic = operation["requestBody"]["content"]["application/json"]["schema"]["properties"]["topic"]
    response_schema = operation["responses"]["200"]["content"]["application/json"]["schema"]

    assert operation["operationId"] == "logRequest"
    assert operation["x-openai-isConsequential"] is False
    assert topic["maxLength"] == 160
    assert schema["components"]["schemas"] == {}
    assert response_schema["type"] == "object"
    assert "properties" in response_schema


def test_public_core_no_longer_contains_request_logging() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert "REQUEST LOGGING" not in text
    assert "logRequest" not in text


def test_request_log_addendum_is_retained_as_reference_only() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_REQUEST_LOG_ADDENDUM.md").read_text(encoding="utf-8")

    assert "exactly once" in text
    assert "Do not send the full prompt" in text
    assert "NON-BLOCKING" in text
