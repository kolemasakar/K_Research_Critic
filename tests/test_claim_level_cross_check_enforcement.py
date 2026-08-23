from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_media_builder_requires_claim_level_cross_check_ledger() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "For EACH material factual claim create an internal cross-check ledger" in text
    assert "`required`, `achieved_independent`, `exception`" in text
    assert "If achieved<required, set exception=SHORTFALL" in text
    assert "Never report the requirement as met for that claim" in text
    assert "Critic checks the ledger claim-by-claim" in text
    assert "An unconditional PASS is forbidden" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text
    assert "per-claim required/achieved/exception summary" in text


def test_managed_reference_requires_claim_level_cross_check_ledger() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "For EACH material factual claim" in text
    assert "`achieved_independent`" in text
    assert "`exception`: `NONE` or `SHORTFALL`" in text
    assert "The system must never report the requirement as met for that claim" in text
    assert "claim-by-claim before `PASS`" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text


def test_manifest_declares_claim_level_runtime_acceptance() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    instructions = manifest["instructions"]
    release = manifest["release"]

    assert instructions["cross_check_claim_level_ledger_required"] is True
    assert instructions["cross_check_claim_level_output_required"] is True
    assert instructions["cross_check_unqualified_pass_on_shortfall_forbidden"] is True
    assert instructions["cross_check_ledger_fields"] == [
        "required",
        "achieved_independent",
        "exception",
    ]
    assert release["cross_check_claim_level_enforcement_hardened"] is True
    assert release["cross_check_claim_level_runtime_accepted"] is True
    assert release["gpt_builder_private_update_required"] is False
