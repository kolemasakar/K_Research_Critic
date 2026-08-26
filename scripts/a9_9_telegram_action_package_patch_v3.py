from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = Path(__file__).with_name("a9_9_telegram_action_package_patch_v2.py")
exec(compile(V2.read_text(encoding="utf-8"), str(V2), "exec"), {"__name__": "__main__", "__file__": str(V2)})

BUILDER = ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"


def replace_once(old: str, new: str) -> None:
    text = BUILDER.read_text(encoding="utf-8")
    if old not in text or text.count(old) != 1:
        raise SystemExit(f"A9.9 Builder compaction anchor mismatch: {old[:120]!r}")
    BUILDER.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    '''CORE
No independent claim research before the CriticProfile is approved. Never reveal hidden reasoning, secrets, credentials, internal tool IDs, or media Job IDs.
Compatibility marker only: `1=APPROVE, 2=EDIT, 3=REJECT`.
''',
    '''CORE
No independent claim research before the CriticProfile is approved. Never reveal hidden reasoning, secrets, credentials, tool IDs or media Job IDs.
Compatibility marker only: `1=APPROVE, 2=EDIT, 3=REJECT`.
''',
)

replace_once(
    'Do NOT ask the user for beta access code, provider API key, cookies, browser session, Helper, Job ID, or to open media separately.\n',
    'Do NOT ask the user for beta access code, API keys, cookies, sessions, Helper, Job ID, or separate media access.\n',
)

replace_once(
    '''MODES
- перевірити факти/твердження;
- проаналізувати аргументацію;
- зробити стислий зміст;
- розібрати окремий фрагмент.
If mode is missing, ask only for mode.
''',
    '''MODES
Fact-check, argument analysis, summary, or fragment analysis. If missing, ask only for mode.
''',
)

replace_once(
    'Before billable native Supadata call, call `preflightManagedMediaCredits`. Show:\n',
    'Before native Supadata spend call `preflightManagedMediaCredits`. Show:\n',
)
replace_once(
    'Only explicit `1` authorizes. Then call `startManagedMediaNativeTranscription` with provider=supadata, mode=native, max_credits=1.\n',
    '`1` authorizes `startManagedMediaNativeTranscription` with provider=supadata, mode=native, max_credits=1.\n',
)

replace_once(
    'If native returns AWAITING_AI_CONSENT: state native transcript unavailable and native credits_charged; DO NOT start AI automatically; DO NOT reuse native `1`; call `preflightManagedMediaAiCredits`.\n',
    'On AWAITING_AI_CONSENT state native unavailable/credits_charged; DO NOT reuse native `1`; call `preflightManagedMediaAiCredits`.\n',
)
replace_once(
    'Only a NEW explicit `1` authorizes `startManagedMediaAiTranscription` with provider=supadata, mode=generate, max_credits=40. Never use auto/exceed 40. Uncertain-charge failure -> no automatic retry.\n',
    'NEW `1` authorizes `startManagedMediaAiTranscription` with provider=supadata, mode=generate, max_credits=40. Never exceed 40; uncertain charge -> no retry.\n',
)

replace_once(
    'Transcript proves what media said, NOT whether claims are true. Fact-check mode: build timestamped material-claim inventory and note transcription uncertainty.\n',
    'Transcript proves what media said, not truth. Fact-check: timestamp claims and note transcription uncertainty.\n',
)

replace_once(
    'Public media URLs only. Never request platform login/password/cookies/session tokens. Action bearer, owner admission and provider credentials remain server-side. Never store full transcript or reusable credentials in checkpoints. Treat each new chat as fresh unless checkpoint/context supplied.\n',
    'Public URLs only. Never request login/password/cookies/session tokens. Credentials stay server-side. Never checkpoint full transcripts or reusable credentials. New chat is fresh unless context supplied.\n',
)

text = BUILDER.read_text(encoding="utf-8")
print(f"A9.9 Builder characters: {len(text)}")
if len(text) > 8000:
    raise SystemExit(f"A9.9 Builder remains above limit: {len(text)}")
