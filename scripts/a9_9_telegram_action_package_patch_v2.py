from pathlib import Path

PATCH = Path(__file__).with_name("a9_9_telegram_action_package_patch.py")
ROOT = PATCH.parents[1]
source = PATCH.read_text(encoding="utf-8")

bad_builder_token = '''replace_once(
    VALIDATOR,
    '            "startManagedFacebookFallback",\\n',
    '            "startManagedFacebookFallback",\\n            "startManagedTelegramPublicTranscription",\\n',
)
'''

good_builder_token = '''replace_once(
    VALIDATOR,
    '            "startManagedMediaAiTranscription",\\n',
    '            "startManagedMediaAiTranscription",\\n            "startManagedTelegramPublicTranscription",\\n',
)
'''

bad_builder_label = '''replace_once(
    VALIDATOR,
    '            "A9.7-I Builder instructions",\\n',
    '            "A9.9 Builder instructions",\\n',
)
'''

good_builder_label = '''replace_once(
    VALIDATOR,
    '        "A9.7-I Builder instructions",\\n',
    '        "A9.9 Builder instructions",\\n',
)
'''

for old, new, label in [
    (bad_builder_token, good_builder_token, "Builder token"),
    (bad_builder_label, good_builder_label, "Builder label"),
]:
    if old not in source:
        raise SystemExit(f"A9.9 v2 patch could not find obsolete {label} validator anchor")
    source = source.replace(old, new, 1)

exec(compile(source, str(PATCH), "exec"), {"__name__": "__main__", "__file__": str(PATCH)})


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text or text.count(old) != 1:
        raise SystemExit(f"A9.9 v2 post-patch anchor mismatch in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Keep GPT Builder operation descriptions within the repository's 300-char parser limit.
action = ROOT / "gpt_store/actions/media_managed_beta_openapi.yaml"
replace_once(
    action,
    '''        Use only for a supported public Telegram post URL. Retrieval uses the public
        Telegram embed surface and costs zero retrieval credits. No Telegram account,
        cookies, session, bot token or paid fallback is used. AssemblyAI STT may consume
        the isolated beta STT quota. Terminal unavailable jobs are not retried automatically.
''',
    '''        Use only for a supported public Telegram post URL. Retrieval uses the public
        Telegram embed surface with zero retrieval credits and no Telegram account, cookies,
        session, bot token or paid fallback. AssemblyAI STT may use isolated beta quota.
        Terminal unavailable jobs are not retried automatically.
''',
)

# Preserve the already accepted A9.7-I Facebook wording while adding Telegram routing.
builder = ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
replace_once(
    builder,
    'Live accepted in current GPT: YouTube, Instagram Reel, Facebook Video/Reel. Telegram backend is live accepted; this package adds public Telegram video routing.\n',
    'Live accepted: YouTube, Instagram Reel, Facebook Video/Reel.\nTelegram backend is live accepted; this package adds public Telegram video routing.\n',
)
replace_once(
    builder,
    '''ROUTING
YouTube/Instagram -> native managed flow first. Facebook -> `startManagedFacebookFallback`; 0 ScrapeCreators credits. COMPLETED -> segments. Cobalt failure, including `AWAITING_RETRIEVAL_CONSENT`, means unavailable; STOP. Never call paid Facebook continuation or Supadata generate fallback.
Telegram public video post -> `startManagedTelegramPublicTranscription`; no credit preflight. COMPLETED -> segments. FAILED/unavailable -> report unavailable and STOP. Never request Telegram login/cookies/session or use paid fallback.
''',
    '''ROUTING
YouTube/Instagram -> native managed flow first. Facebook -> `startManagedFacebookFallback`; 0 ScrapeCreators credits. COMPLETED -> segments. If free Cobalt retrieval fails, including `AWAITING_RETRIEVAL_CONSENT`, report that Facebook media retrieval is unavailable and STOP media intake. Do NOT call `preflightManagedFacebookRetrievalCredit` or `continueManagedFacebookPaidRetrieval`. Do not route Facebook through Supadata generate fallback.
Telegram public video post -> `startManagedTelegramPublicTranscription`; no credit preflight. COMPLETED -> segments. FAILED/unavailable -> report unavailable and STOP. Never request Telegram login/cookies/session or use paid fallback.
''',
)
replace_once(
    builder,
    'JOB HANDLING\nDo not expose `KRCM_...` Job IDs. PROCESSING -> bounded `getManagedMediaTranscriptionStatus` checks. COMPLETED -> retrieve ALL `getManagedMediaTranscriptSegments` pages, cursor=0, limit=50 until next_cursor=null. reused=true -> reuse. FAILED + credit_charge_uncertain=true -> no retry. Action/auth unavailable -> report unavailable. Facebook free failure and Telegram unavailable are terminal: no paid fallback. Do not fall back to Helper in the normal owner flow. Never invent it.\n',
    'JOB HANDLING\nDo not expose `KRCM_...` Job IDs. PROCESSING -> bounded `getManagedMediaTranscriptionStatus` checks. COMPLETED -> retrieve ALL `getManagedMediaTranscriptSegments` pages, cursor=0, limit=50 until next_cursor=null. reused=true -> reuse. FAILED + credit_charge_uncertain=true -> no retry. Action/auth unavailable -> report unavailable. For Facebook, free retrieval failure is terminal for the active MEDIA BETA flow: do not offer any paid retrieval fallback. Telegram unavailable is also terminal with no paid fallback. Do not fall back to Helper in the normal owner flow. Never invent it.\n',
)

# Advance regression expectations to the explicit A9.9 package-ready / Builder-pending state.
claim_test = ROOT / "tests/test_claim_level_cross_check_enforcement.py"
replace_once(
    claim_test,
    '    assert release["gpt_builder_private_update_required"] is False\n',
    '    assert release["gpt_builder_private_update_required"] is True\n',
)

builder_test = ROOT / "tests/test_media_beta_builder_a9_7_i.py"
replace_once(
    builder_test,
    'def test_a9_7_i_corrected_builder_policy_fix_is_runtime_accepted() -> None:\n',
    'def test_a9_9_package_preserves_a9_7_i_acceptance_and_marks_builder_pending() -> None:\n',
)
replace_once(builder_test, '    assert instructions["version"] == "0.7-beta-a9.7-i"\n', '    assert instructions["version"] == "0.8-beta-a9.9"\n')
replace_once(builder_test, '    assert instructions["builder_package_version"] == "0.7-beta-a9.7-i"\n', '    assert instructions["builder_package_version"] == "0.8-beta-a9.9"\n')
replace_once(builder_test, '    assert instructions["builder_target_action_schema_version"] == "0.4.0-a9.7-c"\n', '    assert instructions["builder_target_action_schema_version"] == "0.5.0-a9.9"\n')
replace_once(builder_test, '    assert instructions["builder_runtime_applied"] is True\n', '    assert instructions["builder_runtime_applied"] is False\n')
replace_once(builder_test, '    assert release["rollout_state"] == "A9_7_I_PRIVATE_GPT_E2E_ACCEPTED"\n', '    assert release["rollout_state"] == "A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING"\n')
replace_once(
    builder_test,
    '    assert release["a9_7_i_private_gpt_e2e_complete"] is True\n',
    '''    assert release["a9_7_i_private_gpt_e2e_complete"] is True
    assert release["a9_9_telegram_backend_complete"] is True
    assert release["a9_9_telegram_action_package_complete"] is True
    assert release["a9_9_telegram_builder_runtime_applied"] is False
    assert release["a9_9_telegram_private_gpt_e2e_complete"] is False
''',
)
replace_once(builder_test, '    assert release["gpt_builder_private_update_required"] is False\n', '    assert release["gpt_builder_private_update_required"] is True\n')

managed_test = ROOT / "tests/test_media_beta_managed_package.py"
replace_once(managed_test, '    assert beta["public_platforms_in_progress"] == []\n', '    assert beta["public_platforms_in_progress"] == ["telegram"]\n    assert beta["public_platforms_not_started"] == []\n')
replace_once(
    managed_test,
    '    assert beta["managed_facebook_live_accepted"] is True\n',
    '''    assert beta["managed_facebook_live_accepted"] is True
    assert beta["managed_telegram_code_ready"] is True
    assert beta["managed_telegram_backend_live_accepted"] is True
    assert beta["managed_telegram_public_retrieval_provider"] == "telegram_public_web"
    assert beta["managed_telegram_retrieval_credits"] == 0
    assert beta["managed_telegram_stt_provider"] == "assemblyai"
    assert beta["managed_telegram_action_schema_ready"] is True
    assert beta["managed_telegram_builder_runtime_applied"] is False
    assert beta["managed_telegram_private_gpt_e2e_complete"] is False
''',
)
replace_once(managed_test, '    assert release["gpt_builder_private_update_required"] is False\n', '    assert release["gpt_builder_private_update_required"] is True\n')
replace_once(
    managed_test,
    '        "/api/v1/media/managed/facebook-fallback",\n',
    '        "/api/v1/media/managed/facebook-fallback",\n        "/api/v1/media/managed/telegram",\n',
)
replace_once(
    managed_test,
    '    assert facebook_free["x-openai-isConsequential"] is False\n',
    '''    assert facebook_free["x-openai-isConsequential"] is False
    telegram = paths["/api/v1/media/managed/telegram"]["post"]
    assert telegram["operationId"] == "startManagedTelegramPublicTranscription"
    assert telegram["x-openai-isConsequential"] is False
''',
)
replace_once(
    managed_test,
    '    native = schema["components"]["schemas"]["NativeTranscriptRequest"]\n',
    '''    telegram_request = schema["components"]["schemas"]["TelegramPublicRequest"]
    assert telegram_request["required"] == ["url"]
    assert "credit_consent" not in telegram_request["properties"]
    assert "beta_access_code" not in telegram_request["properties"]

    native = schema["components"]["schemas"]["NativeTranscriptRequest"]
''',
)
replace_once(
    managed_test,
    '''    assert set(job["provider_mode"]["enum"]) == {
        "native",
        "generate",
        "facebook_retrieval_stt",
    }
''',
    '''    assert set(job["provider_mode"]["enum"]) == {
        "native",
        "generate",
        "facebook_retrieval_stt",
        "telegram_public_retrieval_stt",
    }
''',
)
replace_once(
    managed_test,
    '    assert set(retrieval_provider["enum"]) == {"cobalt", "scrapecreators"}\n',
    '    assert set(retrieval_provider["enum"]) == {"cobalt", "scrapecreators", "telegram_public_web"}\n',
)

print("A9.9 package regression expectations aligned")
