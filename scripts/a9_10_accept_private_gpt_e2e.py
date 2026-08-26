from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "gpt_store" / "media_beta_manifest.yaml"
VALIDATOR = ROOT / "scripts" / "validate_store_package.py"
ATTACH_TEST = ROOT / "tests" / "test_media_attachment_ingestion_package.py"
BUILDER_TEST = ROOT / "tests" / "test_media_beta_builder_a9_7_i.py"
MANAGED_TEST = ROOT / "tests" / "test_media_beta_managed_package.py"
CLAIM_TEST = ROOT / "tests" / "test_claim_level_cross_check_enforcement.py"
ACCEPTANCE = ROOT / "subprojects" / "media_beta" / "50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


if not ACCEPTANCE.exists():
    raise SystemExit("A9.10 private GPT acceptance record is missing")

# Manifest: actual Builder application + real local attachment E2E are now accepted.
replace_once(
    MANIFEST,
    "    Приватне owner-only тестування zero-client аналізу публічних YouTube-відео, Instagram Reel, Facebook та Telegram media.\n",
    "    Приватне owner-only тестування zero-client аналізу публічних YouTube-відео, Instagram Reel, Facebook, Telegram media та локальних audio/video вкладень.\n",
)
replace_once(MANIFEST, "  builder_runtime_applied: false\n", "  builder_runtime_applied: true\n")
replace_once(MANIFEST, "  local_upload_live_accepted: false\n", "  local_upload_live_accepted: true\n")
replace_once(MANIFEST, "  managed_attachment_builder_runtime_applied: false\n", "  managed_attachment_builder_runtime_applied: true\n")
replace_once(MANIFEST, "  managed_attachment_ingestion_live_accepted: false\n", "  managed_attachment_ingestion_live_accepted: true\n")
replace_once(MANIFEST, "  managed_attachment_private_gpt_e2e_complete: false\n", "  managed_attachment_private_gpt_e2e_complete: true\n")
replace_once(MANIFEST, "  rollout_state: A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING\n", "  rollout_state: A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED\n")
replace_once(MANIFEST, "  a9_10_attachment_builder_runtime_applied: false\n", "  a9_10_attachment_builder_runtime_applied: true\n")
replace_once(MANIFEST, "  a9_10_attachment_ingestion_live_accepted: false\n", "  a9_10_attachment_ingestion_live_accepted: true\n")
replace_once(MANIFEST, "  a9_10_attachment_private_gpt_e2e_complete: false\n", "  a9_10_attachment_private_gpt_e2e_complete: true\n")
replace_once(MANIFEST, "  gpt_builder_private_update_required: true\n", "  gpt_builder_private_update_required: false\n")

# Validator: accepted A9.10 runtime state.
replace_once(
    VALIDATOR,
    '_require(instructions.get("builder_runtime_applied") is False, "A9.10 Builder package must remain pending until the private GPT is updated")',
    '_require(instructions.get("builder_runtime_applied") is True, "A9.10 Builder package must record actual private GPT application")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("local_upload_live_accepted") is False, "local upload must remain unaccepted until full private-GPT E2E")',
    '_require(beta.get("local_upload_live_accepted") is True, "local upload must be live accepted after A9.10 private-GPT E2E")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("managed_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder update must remain pending")',
    '_require(beta.get("managed_attachment_builder_runtime_applied") is True, "A9.10 attachment Builder update must record runtime application")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("managed_attachment_ingestion_live_accepted") is False, "A9.10 full ingestion must remain pending until a real attachment STT run")',
    '_require(beta.get("managed_attachment_ingestion_live_accepted") is True, "A9.10 full attachment ingestion must be live accepted")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("managed_attachment_private_gpt_e2e_complete") is False, "A9.10 private-GPT E2E must remain pending")',
    '_require(beta.get("managed_attachment_private_gpt_e2e_complete") is True, "A9.10 attachment private-GPT E2E must be accepted")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("rollout_state") == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING", "rollout state must record A9.10 attachment package ready / Builder pending")',
    '_require(release.get("rollout_state") == "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED", "rollout state must record accepted A9.10 local attachment private-GPT E2E")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("a9_10_attachment_builder_runtime_applied") is False, "A9.10 attachment Builder application must remain pending")',
    '_require(release.get("a9_10_attachment_builder_runtime_applied") is True, "A9.10 attachment Builder application must be recorded")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("a9_10_attachment_ingestion_live_accepted") is False, "A9.10 full attachment ingestion must remain pending")',
    '_require(release.get("a9_10_attachment_ingestion_live_accepted") is True, "A9.10 full attachment ingestion must be accepted")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("a9_10_attachment_private_gpt_e2e_complete") is False, "A9.10 attachment private-GPT E2E must remain pending")',
    '_require(release.get("a9_10_attachment_private_gpt_e2e_complete") is True, "A9.10 attachment private-GPT E2E must be accepted")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("gpt_builder_private_update_required") is True, "A9.10 package requires a private Builder update")',
    '_require(release.get("gpt_builder_private_update_required") is False, "accepted A9.10 Builder runtime must not require another private update")',
)

# Dedicated A9.10 test now records accepted runtime state and verifies the acceptance record.
replace_once(ATTACH_TEST, "def test_a9_10_attachment_action_package_is_builder_pending() -> None:\n", "def test_a9_10_attachment_private_gpt_e2e_is_accepted() -> None:\n")
replace_once(ATTACH_TEST, '    assert instructions["builder_runtime_applied"] is False\n', '    assert instructions["builder_runtime_applied"] is True\n')
replace_once(ATTACH_TEST, '    assert beta["managed_attachment_builder_runtime_applied"] is False\n', '    assert beta["managed_attachment_builder_runtime_applied"] is True\n')
replace_once(ATTACH_TEST, '    assert beta["managed_attachment_ingestion_live_accepted"] is False\n', '    assert beta["managed_attachment_ingestion_live_accepted"] is True\n')
replace_once(ATTACH_TEST, '    assert beta["managed_attachment_private_gpt_e2e_complete"] is False\n', '    assert beta["managed_attachment_private_gpt_e2e_complete"] is True\n')
replace_once(ATTACH_TEST, '    assert release["rollout_state"] == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING"\n', '    assert release["rollout_state"] == "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED"\n')
replace_once(ATTACH_TEST, '    assert release["gpt_builder_private_update_required"] is True\n', '    assert release["gpt_builder_private_update_required"] is False\n')
with ATTACH_TEST.open("a", encoding="utf-8") as fh:
    fh.write('\n\ndef test_a9_10_private_gpt_acceptance_record_contains_runtime_evidence() -> None:\n')
    fh.write('    text = (ROOT / "subprojects" / "media_beta" / "50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md").read_text(encoding="utf-8")\n')
    fh.write('    assert "PRIVATE_GPT_E2E_ACCEPTED" in text\n')
    fh.write('    assert "startManagedAttachmentTranscription" in text\n')
    fh.write('    assert "STT accounting: `71 s`" in text\n')
    fh.write('    assert "retrieval/provider credits reported: `0`" in text\n')
    fh.write('    assert "0/1 - SHORTFALL" in text\n')
    fh.write('    assert "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED" in text\n')

# Historical A9.7/A9.9 regression test follows current A9.10 accepted checkpoint.
replace_once(BUILDER_TEST, '    assert instructions["builder_runtime_applied"] is False\n', '    assert instructions["builder_runtime_applied"] is True\n')
replace_once(BUILDER_TEST, '    assert release["rollout_state"] == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING"\n', '    assert release["rollout_state"] == "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED"\n')
replace_once(BUILDER_TEST, '    assert release["gpt_builder_private_update_required"] is True\n', '    assert release["gpt_builder_private_update_required"] is False\n')

replace_once(MANAGED_TEST, '    assert release["gpt_builder_private_update_required"] is True\n', '    assert release["gpt_builder_private_update_required"] is False\n')
replace_once(CLAIM_TEST, '    assert release["gpt_builder_private_update_required"] is True\n', '    assert release["gpt_builder_private_update_required"] is False\n')

print("A9.10 private GPT local attachment E2E acceptance patch applied")
