from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "scripts" / "a9_10_attachment_ingestion_package_patch.py"), run_name="__main__")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"v2 anchor missing in {path}: {old[:160]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"v2 anchor not unique in {path}: {old[:160]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


validator = ROOT / "scripts" / "validate_store_package.py"
claim_test = ROOT / "tests" / "test_claim_level_cross_check_enforcement.py"
schema = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"

replace_once(
    validator,
    '_require(release.get("rollout_state") == "A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED", "rollout state must record accepted A9.9 owner private-GPT Telegram E2E")',
    '_require(release.get("rollout_state") == "A9_10_ATTACHMENT_PACKAGE_READY_BUILDER_PENDING", "rollout state must record A9.10 attachment package ready / Builder pending")',
)

replace_once(
    claim_test,
    '    assert release["gpt_builder_private_update_required"] is False\n',
    '    assert release["gpt_builder_private_update_required"] is True\n',
)

replace_once(
    schema,
    '''      description: >-\n        Use for exactly one audio/video file attached in the current ChatGPT\n        conversation. ChatGPT supplies the runtime openaiFileIdRefs object. The\n        isolated backend downloads the temporary trusted OpenAI attachment, enforces\n        media size/duration/type limits, normalizes audio, runs AssemblyAI STT and\n        persists durable KRCM segments. Retrieval credits are zero and no Helper,\n        cookies, session or user beta code is required.\n''',
    '''      description: >-\n        Transcribe one current-conversation audio/video attachment. ChatGPT supplies\n        openaiFileIdRefs; the isolated backend accepts only trusted OpenAI media,\n        enforces type/size/duration, runs AssemblyAI, and persists KRCM segments.\n        Retrieval credits are zero; no Helper, cookies, session, or user code.\n''',
)

builder_len = len((ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md").read_text(encoding="utf-8"))
print(f"A9.10 v2 Builder characters: {builder_len}")
print("A9.10 v2 validator/regression alignment applied")
