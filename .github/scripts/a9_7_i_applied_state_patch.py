from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = [
    ROOT / "tests" / "test_media_beta_managed_package.py",
    ROOT / "tests" / "test_claim_level_cross_check_enforcement.py",
]

for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    old = 'assert release["gpt_builder_private_update_required"] is True'
    new = 'assert release["gpt_builder_private_update_required"] is False'
    if old not in text:
        raise SystemExit(f"expected assertion not found in {path}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

print("A9.7-I applied-state assertions patched")
