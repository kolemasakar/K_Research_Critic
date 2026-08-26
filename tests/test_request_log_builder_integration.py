from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_public_core_instructions_keep_request_logging_disabled() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")
    manifest = yaml.safe_load((ROOT / "gpt_store" / "manifest.yaml").read_text(encoding="utf-8"))

    assert len(text) <= 8000
    assert "REQUEST LOGGING" not in text
    assert "call `logRequest` exactly once" not in text
    assert manifest["capabilities"]["actions"] is False
    assert manifest["request_log_mvp"]["public_enabled_target"] is False
    assert manifest["request_log_mvp"]["builder_action_currently_configured"] is False
    assert manifest["release"]["request_log_public_enabled"] is False
    assert manifest["release"]["request_log_disablement_runtime_accepted"] is True
