from pathlib import Path

PATCH = Path(__file__).with_name("a9_9_telegram_action_package_patch.py")
source = PATCH.read_text(encoding="utf-8")

bad = '''replace_once(
    VALIDATOR,
    '            "startManagedFacebookFallback",\\n',
    '            "startManagedFacebookFallback",\\n            "startManagedTelegramPublicTranscription",\\n',
)
'''

good = '''replace_once(
    VALIDATOR,
    '            "startManagedMediaAiTranscription",\\n',
    '            "startManagedMediaAiTranscription",\\n            "startManagedTelegramPublicTranscription",\\n',
)
'''

if bad not in source:
    raise SystemExit("A9.9 v2 patch could not find the obsolete Builder-token validator anchor")

source = source.replace(bad, good, 1)
exec(compile(source, str(PATCH), "exec"), {"__name__": "__main__", "__file__": str(PATCH)})
