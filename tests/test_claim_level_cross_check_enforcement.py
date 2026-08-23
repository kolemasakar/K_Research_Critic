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


def test_media_builder_requires_traceable_evidence_origins_and_localized_protocol() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "A systematic review/meta-analysis counts as one evidence origin" in text
    assert "TRACEABILITY:" in text
    assert "every evidence origin counted in `achieved_independent` MUST be visible" in text
    assert "`achieved_independent` cannot exceed the number of visibly traceable" in text
    assert "Critic checks the ledger claim-by-claim and verifies traceability" in text
    assert "untraceable PASS count" in text
    assert "`ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`" in text
    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text
    assert "Values must match visible claim blocks and traceable evidence origins" in text


def test_media_builder_localizes_user_visible_labels() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "headings, table titles/columns, CriticProfile field labels" in text
    assert "Canonical English keys stay internal" in text
    assert "Do not show `Claim-level summary`" in text
    assert "raw CriticProfile keys such as `profile_id`, `risk_level`, `required_cross_checks`, `approved_at`" in text


def test_managed_reference_requires_claim_level_cross_check_ledger() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "For EACH material factual claim" in text
    assert "`achieved_independent`" in text
    assert "`exception`: `NONE` or `SHORTFALL`" in text
    assert "The system must never report the requirement as met for that claim" in text
    assert "ledger and evidence-origin traceability claim-by-claim before `PASS`" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text
    assert "A systematic review/meta-analysis counts as one evidence origin" in text
    assert "must be visible and traceable in the final user-facing report" in text
    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text
    assert "Do not expose English labels such as `Claim-level summary`" in text


def test_manifest_declares_claim_level_traceability_and_localization_contract() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )
    instructions = manifest["instructions"]
    release = manifest["release"]

    assert instructions["cross_check_claim_level_ledger_required"] is True
    assert instructions["cross_check_claim_level_output_required"] is True
    assert instructions["cross_check_unqualified_pass_on_shortfall_forbidden"] is True
    assert instructions["cross_check_traceability_required"] is True
    assert instructions["cross_check_achieved_cannot_exceed_visible_origins"] is True
    assert instructions["cross_check_systematic_review_counts_as_one_origin"] is True
    assert instructions["cross_check_protocol_table_required"] is True
    assert instructions["user_visible_labels_localized_to_report_language"] is True
    assert instructions["criticprofile_field_labels_localized_to_report_language"] is True
    assert instructions["cross_check_protocol_table_heading_uk"] == "ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ"
    assert instructions["cross_check_protocol_table_columns"] == [
        "Твердження",
        "Потрібно",
        "Отримано незалежних",
        "Виняток",
    ]
    assert instructions["cross_check_ledger_fields"] == [
        "required",
        "achieved_independent",
        "exception",
    ]
    assert release["cross_check_claim_level_enforcement_hardened"] is True
    assert release["cross_check_claim_level_runtime_accepted"] is True
    assert release["cross_check_traceability_hardened"] is True
    assert release["cross_check_traceability_runtime_accepted"] is False
    assert release["report_label_localization_hardened"] is True
    assert release["report_label_localization_runtime_accepted"] is False
    assert release["gpt_builder_private_update_required"] is True
