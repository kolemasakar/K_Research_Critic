from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "gpt_store" / "actions" / "media_attachment_probe_openapi.yaml"
ACCEPTANCE_PATH = ROOT / "subprojects" / "media_beta" / "49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md"


def test_attachment_probe_schema_is_non_billable_and_file_ref_only() -> None:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert schema["openapi"] == "3.1.0"
    assert schema["info"]["version"] == "0.1.0-a9.10-probe"
    assert schema["servers"] == [
        {"url": "https://voicebridge-krc-media-beta-kolemasakar.onrender.com"}
    ]

    paths = schema["paths"]
    assert set(paths) == {"/api/v1/media/managed/attachment-probe"}
    operation = paths["/api/v1/media/managed/attachment-probe"]["post"]
    assert operation["operationId"] == "probeManagedAttachmentTransport"
    assert operation["x-openai-isConsequential"] is False

    request = schema["components"]["schemas"]["AttachmentProbeRequest"]
    assert request["additionalProperties"] is False
    assert request["required"] == ["openaiFileIdRefs"]
    refs = request["properties"]["openaiFileIdRefs"]
    assert refs["type"] == "array"
    assert refs["minItems"] == 1
    assert refs["maxItems"] == 1
    assert refs["items"] == {"type": "string"}

    result = schema["components"]["schemas"]["AttachmentProbeResult"]["properties"]
    assert result["retrieval_credits_charged"]["const"] == 0
    assert result["stt_seconds_charged"]["const"] == 0
    assert result["probe_byte_limit"]["const"] == 65536

    serialized = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "AssemblyAI" in serialized
    assert "does not call AssemblyAI" in serialized
    assert "startManagedAttachmentTranscription" not in serialized
    assert "download_link:" not in serialized
    assert "file_id:" not in serialized


def test_attachment_transport_runtime_acceptance_is_recorded() -> None:
    text = ACCEPTANCE_PATH.read_text(encoding="utf-8")

    assert "LIVE_RUNTIME_TRANSPORT_ACCEPTED / FULL_INGESTION_PENDING" in text
    assert "probeManagedAttachmentTransport" in text
    assert "transport_available = true" in text
    assert "retrieval_credits_charged = 0" in text
    assert "stt_seconds_charged = 0" in text
