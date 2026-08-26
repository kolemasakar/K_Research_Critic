from pathlib import Path

PATCH = Path(__file__).with_name("a9_9_telegram_action_package_patch.py")
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
