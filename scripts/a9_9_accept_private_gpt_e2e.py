from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "gpt_store/media_beta_manifest.yaml"
VALIDATOR = ROOT / "scripts/validate_store_package.py"
TEST = ROOT / "tests/test_media_beta_builder_a9_7_i.py"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"A9.9 acceptance anchor mismatch in {path}: count={count} anchor={old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Manifest: actual Builder + owner NEW-chat Telegram positive-path E2E accepted.
replace_once(
    MANIFEST,
    "Приватне owner-only тестування zero-client аналізу публічних YouTube-відео, Instagram Reel та Facebook media.",
    "Приватне owner-only тестування zero-client аналізу публічних YouTube-відео, Instagram Reel, Facebook та Telegram media.",
)
replace_once(MANIFEST, "  builder_runtime_applied: false\n", "  builder_runtime_applied: true\n")
replace_once(
    MANIFEST,
    "  public_platforms_live_accepted:\n    - youtube\n    - instagram\n    - facebook\n  public_platforms_in_progress:\n    - telegram\n",
    "  public_platforms_live_accepted:\n    - youtube\n    - instagram\n    - facebook\n    - telegram\n  public_platforms_in_progress: []\n",
)
replace_once(
    MANIFEST,
    "  managed_telegram_builder_runtime_applied: false\n",
    "  managed_telegram_builder_runtime_applied: true\n",
)
replace_once(
    MANIFEST,
    "  managed_telegram_private_gpt_e2e_complete: false\n",
    "  managed_telegram_private_gpt_e2e_complete: true\n",
)
replace_once(
    MANIFEST,
    "  rollout_state: A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING\n",
    "  rollout_state: A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED\n",
)
replace_once(
    MANIFEST,
    "  a9_9_telegram_builder_runtime_applied: false\n",
    "  a9_9_telegram_builder_runtime_applied: true\n",
)
replace_once(
    MANIFEST,
    "  a9_9_telegram_private_gpt_e2e_complete: false\n",
    "  a9_9_telegram_private_gpt_e2e_complete: true\n",
)
replace_once(
    MANIFEST,
    "  gpt_builder_private_update_required: true\n",
    "  gpt_builder_private_update_required: false\n",
)

# Validator: accepted-state invariants.
replace_once(
    VALIDATOR,
    '_require(instructions.get("builder_runtime_applied") is False, "A9.9 Builder package must remain pending until private GPT Builder is updated")',
    '_require(instructions.get("builder_runtime_applied") is True, "A9.9 Builder package must record actual private GPT runtime application")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("public_platforms_live_accepted") == ["youtube", "instagram", "facebook"], "YouTube, Instagram, and the accepted Facebook free path must be declared live accepted")',
    '_require(beta.get("public_platforms_live_accepted") == ["youtube", "instagram", "facebook", "telegram"], "YouTube, Instagram, Facebook and Telegram owner zero-client paths must be declared live accepted")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("public_platforms_in_progress") == ["telegram"], "Telegram must remain in progress until private-GPT E2E acceptance")',
    '_require(beta.get("public_platforms_in_progress") == [], "No public platform may remain in progress after Telegram private-GPT E2E acceptance")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("managed_telegram_builder_runtime_applied") is False, "Telegram Builder runtime must remain pending")',
    '_require(beta.get("managed_telegram_builder_runtime_applied") is True, "Telegram Builder runtime must record actual application")',
)
replace_once(
    VALIDATOR,
    '_require(beta.get("managed_telegram_private_gpt_e2e_complete") is False, "Telegram private-GPT E2E must remain pending")',
    '_require(beta.get("managed_telegram_private_gpt_e2e_complete") is True, "Telegram private-GPT E2E must be accepted")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("rollout_state") == "A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING", "rollout state must record A9.9 package-ready Builder-pending state")',
    '_require(release.get("rollout_state") == "A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED", "rollout state must record accepted A9.9 owner private-GPT Telegram E2E")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("a9_9_telegram_builder_runtime_applied") is False, "A9.9 Telegram Builder runtime must remain pending")',
    '_require(release.get("a9_9_telegram_builder_runtime_applied") is True, "A9.9 Telegram Builder runtime must be applied")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("a9_9_telegram_private_gpt_e2e_complete") is False, "A9.9 Telegram private-GPT E2E must remain pending")',
    '_require(release.get("a9_9_telegram_private_gpt_e2e_complete") is True, "A9.9 Telegram private-GPT E2E must be accepted")',
)
replace_once(
    VALIDATOR,
    '_require(release.get("gpt_builder_private_update_required") is True, "A9.9 must require private Builder package update")',
    '_require(release.get("gpt_builder_private_update_required") is False, "A9.9 accepted Builder runtime must not require another private Builder update")',
)

# Regression tests: package-ready -> actual-runtime accepted state.
replace_once(
    TEST,
    "def test_a9_9_package_preserves_a9_7_i_acceptance_and_marks_builder_pending() -> None:\n",
    "def test_a9_9_package_preserves_a9_7_i_acceptance_and_records_private_gpt_e2e() -> None:\n",
)
replace_once(TEST, '    assert instructions["builder_runtime_applied"] is False\n', '    assert instructions["builder_runtime_applied"] is True\n')
replace_once(
    TEST,
    '    assert release["rollout_state"] == "A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING"\n',
    '    assert release["rollout_state"] == "A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED"\n',
)
replace_once(
    TEST,
    '    assert release["a9_9_telegram_builder_runtime_applied"] is False\n',
    '    assert release["a9_9_telegram_builder_runtime_applied"] is True\n',
)
replace_once(
    TEST,
    '    assert release["a9_9_telegram_private_gpt_e2e_complete"] is False\n',
    '    assert release["a9_9_telegram_private_gpt_e2e_complete"] is True\n',
)
replace_once(
    TEST,
    '    assert release["gpt_builder_private_update_required"] is True\n',
    '    assert release["gpt_builder_private_update_required"] is False\n',
)

print("A9.9 private GPT Telegram E2E acceptance state applied")
