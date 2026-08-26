from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_a9_10_attachment_action_package_is_builder_pending() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8"))
    beta = manifest["beta"]
    release = manifest["release"]
    instructions = manifest["instructions"]

    assert instructions["version"] == "0.9-beta-a9.10"
    assert instructions["builder_target_action_schema_version"] == "0.6.0-a9.10"
    assert instructions["builder_package_ready"] is True
    assert instructions["builder_runtime_applied"] is False
    assert beta["managed_attachment_transport_live_accepted"] is True
    assert beta["managed_attachment_backend_code_ready"] is True
    assert beta["managed_attachment_backend_live_deployed"] is True
    assert beta["managed_attachment_retrieval_provider"] == "openai_attachment"
    assert beta["managed_attachment_retrieval_credits"] == 0
    assert beta["managed_attachment_stt_provider"] == "assemblyai"
    assert beta["managed_attachment_action_schema_ready"] is True
    assert beta["managed_attachment_builder_runtime_applied"] is False
    assert beta["managed_attachment_ingestion_live_accepted"] is False
    assert beta["managed_attachment_private_gpt_e2e_complete"] is False
    assert release["rollout_state"] == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING"
    assert release["gpt_builder_private_update_required"] is True


def test_a9_10_attachment_schema_is_zero_retrieval_credit_and_file_ref_only() -> None:
    schema = yaml.safe_load((ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml").read_text(encoding="utf-8"))
    operation = schema["paths"]["/api/v1/media/managed/attachment"]["post"]
    assert operation["operationId"] == "startManagedAttachmentTranscription"
    assert operation["x-openai-isConsequential"] is False
    request = schema["components"]["schemas"]["AttachmentTranscriptRequest"]
    assert request["required"] == ["openaiFileIdRefs"]
    refs = request["properties"]["openaiFileIdRefs"]
    assert refs["type"] == "array"
    assert refs["minItems"] == 1
    assert refs["maxItems"] == 1
    assert refs["items"] == {"type": "string"}
    assert "beta_access_code" not in request["properties"]
    assert "credit_consent" not in request["properties"]
    job = schema["components"]["schemas"]["ManagedJob"]["properties"]
    assert "attachment_upload_stt" in job["provider_mode"]["enum"]
    assert "openai_attachment" in job["retrieval_provider"]["anyOf"][0]["enum"]


def test_a9_10_builder_routes_local_attachment_without_helper_or_retrieval_credit_gate() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert len(text) <= 8000
    assert "Local audio/video attachment -> `startManagedAttachmentTranscription`" in text
    assert "no retrieval-credit preflight or Helper" in text
