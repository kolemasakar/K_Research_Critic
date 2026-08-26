from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"
BUILDER = ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
MANIFEST = ROOT / "gpt_store" / "media_beta_manifest.yaml"
VALIDATOR = ROOT / "scripts" / "validate_store_package.py"
MANAGED_TEST = ROOT / "tests" / "test_media_beta_managed_package.py"
BUILDER_TEST = ROOT / "tests" / "test_media_beta_builder_a9_7_i.py"
PROBE_TEST = ROOT / "tests" / "test_media_attachment_probe_package.py"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:140]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:140]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Action schema: promote from transport probe package to full local attachment ingestion package.
replace_once(SCHEMA, "  version: 0.5.0-a9.9\n", "  version: 0.6.0-a9.10\n")
replace_once(
    SCHEMA,
    "    Facebook and supported public Telegram video posts, plus a non-billable A9.10\n    local-attachment transport probe. Existing Supadata native and consent-gated AI\n",
    "    Facebook and supported public Telegram video posts, plus owner-only local\n    audio/video attachments. Existing Supadata native and consent-gated AI\n",
)

attachment_path = '''  /api/v1/media/managed/attachment:\n    post:\n      operationId: startManagedAttachmentTranscription\n      summary: Transcribe one local audio or video attachment with AssemblyAI\n      description: >-\n        Use for exactly one audio/video file attached in the current ChatGPT\n        conversation. ChatGPT supplies the runtime openaiFileIdRefs object. The\n        isolated backend downloads the temporary trusted OpenAI attachment, enforces\n        media size/duration/type limits, normalizes audio, runs AssemblyAI STT and\n        persists durable KRCM segments. Retrieval credits are zero and no Helper,\n        cookies, session or user beta code is required.\n      x-openai-isConsequential: false\n      requestBody:\n        required: true\n        content:\n          application/json:\n            schema:\n              $ref: "#/components/schemas/AttachmentTranscriptRequest"\n      responses:\n        "200":\n          description: Local attachment job completed, failed, or reused from durable state.\n          content:\n            application/json:\n              schema:\n                $ref: "#/components/schemas/ManagedJob"\n        "400":\n          description: Missing, malformed, multiple, or untrusted runtime file reference.\n        "401":\n          description: Private GPT Action bearer authentication failed.\n        "413":\n          description: Attachment exceeds the isolated media size or duration limit.\n        "415":\n          description: Attachment type, extension, or downloaded MIME is unsupported or inconsistent.\n        "422":\n          description: Attachment media or resulting transcript is unusable.\n        "429":\n          description: Closed-beta STT quota is exhausted.\n        "502":\n          description: Temporary OpenAI download or STT provider could not be reached safely.\n        "503":\n          description: Managed local attachment transcription is not configured.\n'''
replace_once(
    SCHEMA,
    "  /api/v1/media/managed/attachment-probe:\n",
    attachment_path + "  /api/v1/media/managed/attachment-probe:\n",
)

replace_once(
    SCHEMA,
    "        telegram_stt_configured:\n          type: boolean\n",
    "        telegram_stt_configured:\n          type: boolean\n"
    "        local_attachment_transport:\n          type: boolean\n"
    "        local_attachment_transcription:\n          type: boolean\n"
    "        local_attachment_provider:\n          type: string\n          const: assemblyai\n"
    "        local_attachment_retrieval_provider:\n          type: string\n          const: openai_attachment\n"
    "        local_attachment_max_bytes:\n          type: integer\n          const: 33554432\n"
    "        local_attachment_max_duration_seconds:\n          type: integer\n          minimum: 60\n",
)

attachment_request = '''    AttachmentTranscriptRequest:\n      type: object\n      additionalProperties: false\n      required: [openaiFileIdRefs]\n      properties:\n        openaiFileIdRefs:\n          type: array\n          minItems: 1\n          maxItems: 1\n          items:\n            type: string\n          description: >-\n            Exactly one user-uploaded audio or video file from the current ChatGPT\n            conversation. ChatGPT replaces this string-array schema with the runtime\n            file-reference object containing name, id, mime_type and temporary\n            download_link. The backend never exposes those identifiers or URL.\n        language_hint:\n          type: string\n          enum: [auto, uk, ru, en]\n          default: auto\n'''
replace_once(
    SCHEMA,
    "    AttachmentProbeRequest:\n",
    attachment_request + "    AttachmentProbeRequest:\n",
)
replace_once(
    SCHEMA,
    "          enum: [native, generate, facebook_retrieval_stt, telegram_public_retrieval_stt]\n",
    "          enum: [native, generate, facebook_retrieval_stt, telegram_public_retrieval_stt, attachment_upload_stt]\n",
)
replace_once(
    SCHEMA,
    "              enum: [cobalt, scrapecreators, telegram_public_web]\n",
    "              enum: [cobalt, scrapecreators, telegram_public_web, openai_attachment]\n",
)

# Builder routing: compact enough to preserve the hard 8000-character limit.
replace_once(
    BUILDER,
    "Telegram public video post -> `startManagedTelegramPublicTranscription`; no credit preflight. COMPLETED -> segments. FAILED/unavailable -> report unavailable and STOP. Never request Telegram login/cookies/session or use paid fallback.\n",
    "Telegram public video post -> `startManagedTelegramPublicTranscription`; no credit preflight. COMPLETED -> segments. FAILED/unavailable -> report unavailable and STOP. Never request Telegram login/cookies/session or use paid fallback.\n"
    "Local audio/video attachment -> `startManagedAttachmentTranscription`; no retrieval-credit preflight or Helper. COMPLETED -> segments. FAILED -> report unavailable and STOP.\n",
)

# Manifest: package ready / Builder + full private-GPT ingestion E2E still pending.
replace_once(MANIFEST, '  version: "0.8-beta-a9.9"\n', '  version: "0.9-beta-a9.10"\n')
replace_once(MANIFEST, '  builder_package_version: "0.8-beta-a9.9"\n', '  builder_package_version: "0.9-beta-a9.10"\n')
replace_once(MANIFEST, '  builder_target_action_schema_version: "0.5.0-a9.9"\n', '  builder_target_action_schema_version: "0.6.0-a9.10"\n')
replace_once(MANIFEST, "  builder_runtime_applied: true\n", "  builder_runtime_applied: false\n")
replace_once(
    MANIFEST,
    "  local_upload_live_accepted: false\n",
    "  local_upload_live_accepted: false\n"
    "  managed_attachment_transport_live_accepted: true\n"
    "  managed_attachment_transport_provider: openai_file_refs\n"
    "  managed_attachment_backend_code_ready: true\n"
    "  managed_attachment_backend_live_deployed: true\n"
    "  managed_attachment_retrieval_provider: openai_attachment\n"
    "  managed_attachment_retrieval_credits: 0\n"
    "  managed_attachment_stt_provider: assemblyai\n"
    "  managed_attachment_max_bytes: 33554432\n"
    "  managed_attachment_action_schema_ready: true\n"
    "  managed_attachment_builder_runtime_applied: false\n"
    "  managed_attachment_ingestion_live_accepted: false\n"
    "  managed_attachment_private_gpt_e2e_complete: false\n",
)
replace_once(
    MANIFEST,
    "  rollout_state: A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED\n",
    "  rollout_state: A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING\n",
)
replace_once(
    MANIFEST,
    "  a9_9_telegram_private_gpt_e2e_complete: true\n",
    "  a9_9_telegram_private_gpt_e2e_complete: true\n"
    "  a9_10_attachment_transport_runtime_accepted: true\n"
    "  a9_10_attachment_backend_code_ready: true\n"
    "  a9_10_attachment_backend_live_deployed: true\n"
    "  a9_10_attachment_action_package_complete: true\n"
    "  a9_10_attachment_builder_runtime_applied: false\n"
    "  a9_10_attachment_ingestion_live_accepted: false\n"
    "  a9_10_attachment_private_gpt_e2e_complete: false\n",
)
replace_once(MANIFEST, "  gpt_builder_private_update_required: false\n", "  gpt_builder_private_update_required: true\n")

# Validator tracks the new package-ready / Builder-pending checkpoint while preserving A9.9 history.
replace_once(VALIDATOR, 'instructions.get("version") == "0.8-beta-a9.9"', 'instructions.get("version") == "0.9-beta-a9.10"')
replace_once(VALIDATOR, '"A9.9 instruction version must be 0.8-beta-a9.9"', '"A9.10 instruction version must be 0.9-beta-a9.10"')
replace_once(VALIDATOR, 'instructions.get("builder_package_version") == "0.8-beta-a9.9"', 'instructions.get("builder_package_version") == "0.9-beta-a9.10"')
replace_once(VALIDATOR, '"A9.9 Builder package version must be 0.8-beta-a9.9"', '"A9.10 Builder package version must be 0.9-beta-a9.10"')
replace_once(VALIDATOR, 'instructions.get("builder_runtime_applied") is True', 'instructions.get("builder_runtime_applied") is False')
replace_once(VALIDATOR, '"A9.9 Builder package must record actual private GPT runtime application"', '"A9.10 Builder package must remain pending until the private GPT is updated"')
replace_once(
    VALIDATOR,
    '_require(beta.get("local_upload_live_accepted") is False, "local upload must remain unaccepted")\n',
    '_require(beta.get("local_upload_live_accepted") is False, "local upload must remain unaccepted until full private-GPT E2E")\n'
    '    _require(beta.get("managed_attachment_transport_live_accepted") is True, "A9.10 attachment transport runtime must be accepted")\n'
    '    _require(beta.get("managed_attachment_backend_code_ready") is True, "A9.10 attachment backend must be code-ready")\n'
    '    _require(beta.get("managed_attachment_backend_live_deployed") is True, "A9.10 attachment backend must be deployed to isolated beta")\n'
    '    _require(beta.get("managed_attachment_retrieval_provider") == "openai_attachment", "A9.10 attachment retrieval provider must be openai_attachment")\n'
    '    _require(beta.get("managed_attachment_retrieval_credits") == 0, "A9.10 attachment retrieval must cost zero credits")\n'
    '    _require(beta.get("managed_attachment_stt_provider") == "assemblyai", "A9.10 attachment STT provider must be AssemblyAI")\n'
    '    _require(beta.get("managed_attachment_action_schema_ready") is True, "A9.10 attachment Action schema must be ready")\n'
    '    _require(beta.get("managed_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder update must remain pending")\n'
    '    _require(beta.get("managed_attachment_ingestion_live_accepted") is False, "A9.10 full ingestion must remain pending until a real attachment STT run")\n'
    '    _require(beta.get("managed_attachment_private_gpt_e2e_complete") is False, "A9.10 private-GPT E2E must remain pending")\n',
)
replace_once(
    VALIDATOR,
    '_require(release.get("gpt_builder_private_update_required") is False, "A9.9 accepted Builder runtime must not require another private Builder update")\n',
    '_require(release.get("a9_10_attachment_transport_runtime_accepted") is True, "A9.10 attachment transport runtime acceptance must be recorded")\n'
    '    _require(release.get("a9_10_attachment_backend_code_ready") is True, "A9.10 attachment backend must be code-ready")\n'
    '    _require(release.get("a9_10_attachment_backend_live_deployed") is True, "A9.10 attachment backend must be live on isolated beta")\n'
    '    _require(release.get("a9_10_attachment_action_package_complete") is True, "A9.10 attachment Action package must be complete")\n'
    '    _require(release.get("a9_10_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder application must remain pending")\n'
    '    _require(release.get("a9_10_attachment_ingestion_live_accepted") is False, "A9.10 full attachment ingestion must remain pending")\n'
    '    _require(release.get("a9_10_attachment_private_gpt_e2e_complete") is False, "A9.10 attachment private-GPT E2E must remain pending")\n'
    '    _require(release.get("gpt_builder_private_update_required") is True, "A9.10 package requires a private Builder update")\n',
)
replace_once(
    VALIDATOR,
    '            "startManagedTelegramPublicTranscription",\n',
    '            "startManagedTelegramPublicTranscription",\n            "startManagedAttachmentTranscription",\n',
)
replace_once(VALIDATOR, '            "version: 0.5.0-a9.9",\n', '            "version: 0.6.0-a9.10",\n')
replace_once(
    VALIDATOR,
    '            "operationId: startManagedTelegramPublicTranscription",\n',
    '            "operationId: startManagedTelegramPublicTranscription",\n            "operationId: startManagedAttachmentTranscription",\n',
)
replace_once(
    VALIDATOR,
    '            "telegram_public_retrieval_stt",\n            "telegram_public_web",\n',
    '            "telegram_public_retrieval_stt",\n            "telegram_public_web",\n            "attachment_upload_stt",\n            "openai_attachment",\n',
)

# Managed package regression expectations.
replace_once(MANAGED_TEST, '    assert release["gpt_builder_private_update_required"] is False\n', '    assert release["gpt_builder_private_update_required"] is True\n')
replace_once(
    MANAGED_TEST,
    '        "/api/v1/media/managed/attachment-probe",\n',
    '        "/api/v1/media/managed/attachment",\n        "/api/v1/media/managed/attachment-probe",\n',
)
replace_once(
    MANAGED_TEST,
    '    attachment_probe = paths["/api/v1/media/managed/attachment-probe"]["post"]\n',
    '    attachment = paths["/api/v1/media/managed/attachment"]["post"]\n'
    '    assert attachment["operationId"] == "startManagedAttachmentTranscription"\n'
    '    assert attachment["x-openai-isConsequential"] is False\n'
    '    attachment_probe = paths["/api/v1/media/managed/attachment-probe"]["post"]\n',
)
replace_once(
    MANAGED_TEST,
    '    attachment_request = schema["components"]["schemas"]["AttachmentProbeRequest"]\n',
    '    attachment_transcript_request = schema["components"]["schemas"]["AttachmentTranscriptRequest"]\n'
    '    assert attachment_transcript_request["required"] == ["openaiFileIdRefs"]\n'
    '    transcript_refs = attachment_transcript_request["properties"]["openaiFileIdRefs"]\n'
    '    assert transcript_refs["minItems"] == 1\n'
    '    assert transcript_refs["maxItems"] == 1\n'
    '    assert "beta_access_code" not in attachment_transcript_request["properties"]\n'
    '    assert "credit_consent" not in attachment_transcript_request["properties"]\n'
    '    attachment_request = schema["components"]["schemas"]["AttachmentProbeRequest"]\n',
)
replace_once(
    MANAGED_TEST,
    '        "telegram_public_retrieval_stt",\n    }\n',
    '        "telegram_public_retrieval_stt",\n        "attachment_upload_stt",\n    }\n',
)
replace_once(
    MANAGED_TEST,
    '    assert set(retrieval_provider["enum"]) == {"cobalt", "scrapecreators", "telegram_public_web"}\n',
    '    assert set(retrieval_provider["enum"]) == {"cobalt", "scrapecreators", "telegram_public_web", "openai_attachment"}\n',
)
replace_once(
    MANAGED_TEST,
    '    assert "startManagedMediaAiTranscription" in text\n',
    '    assert "startManagedMediaAiTranscription" in text\n    assert "startManagedAttachmentTranscription" in text\n',
)

# Historical A9.7/A9.9 test now distinguishes historical acceptance from current A9.10 Builder-pending package.
replace_once(BUILDER_TEST, '    assert instructions["version"] == "0.8-beta-a9.9"\n', '    assert instructions["version"] == "0.9-beta-a9.10"\n')
replace_once(BUILDER_TEST, '    assert instructions["builder_package_version"] == "0.8-beta-a9.9"\n', '    assert instructions["builder_package_version"] == "0.9-beta-a9.10"\n')
replace_once(BUILDER_TEST, '    assert instructions["builder_target_action_schema_version"] == "0.5.0-a9.9"\n', '    assert instructions["builder_target_action_schema_version"] == "0.6.0-a9.10"\n')
replace_once(BUILDER_TEST, '    assert instructions["builder_runtime_applied"] is True\n', '    assert instructions["builder_runtime_applied"] is False\n')
replace_once(BUILDER_TEST, '    assert release["rollout_state"] == "A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED"\n', '    assert release["rollout_state"] == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING"\n')
replace_once(BUILDER_TEST, '    assert release["gpt_builder_private_update_required"] is False\n', '    assert release["gpt_builder_private_update_required"] is True\n')

# Probe test now recognizes that Gate 2 passed, while the standalone probe contract remains non-billable.
probe_text = PROBE_TEST.read_text(encoding="utf-8")
probe_text = probe_text.replace(
    'AUDIT_PATH = ROOT / "subprojects" / "media_beta" / "47_A9_10_LOCAL_UPLOAD_TRANSPORT_AUDIT.md"\n',
    'ACCEPTANCE_PATH = ROOT / "subprojects" / "media_beta" / "49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md"\n'
)
probe_text = probe_text.replace(
    'def test_attachment_probe_audit_keeps_runtime_acceptance_pending() -> None:\n    text = AUDIT_PATH.read_text(encoding="utf-8")\n\n    assert "FEASIBILITY_CONFIRMED_IN_CONTRACT / LIVE_RUNTIME_PROBE_REQUIRED" in text\n    assert "probeManagedAttachmentTransport" in text\n    assert "zero credits and zero STT seconds" in text\n    assert "Only after this live probe passes" in text\n    assert "not yet runtime accepted" in text\n',
    'def test_attachment_transport_runtime_acceptance_is_recorded() -> None:\n    text = ACCEPTANCE_PATH.read_text(encoding="utf-8")\n\n    assert "LIVE_RUNTIME_TRANSPORT_ACCEPTED / FULL_INGESTION_PENDING" in text\n    assert "probeManagedAttachmentTransport" in text\n    assert "transport_available = true" in text\n    assert "retrieval_credits_charged = 0" in text\n    assert "stt_seconds_charged = 0" in text\n'
)
PROBE_TEST.write_text(probe_text, encoding="utf-8")

# Dedicated package-state test.
(ROOT / "tests" / "test_media_attachment_ingestion_package.py").write_text(r'''from __future__ import annotations

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
''', encoding="utf-8")

builder_len = len(BUILDER.read_text(encoding="utf-8"))
print(f"A9.10 Builder characters: {builder_len}")
if builder_len > 8000:
    raise SystemExit(f"Builder instructions exceed 8000 characters: {builder_len}")
print("A9.10 attachment ingestion Action package patch applied")
