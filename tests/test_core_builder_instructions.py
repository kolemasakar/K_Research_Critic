from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "prompts" / "GPT_STORE_CORE_BUILDER_INSTRUCTIONS.md"

FIRST_GATE = (
    "Профіль збору і критики успішно створено.\n"
    "1 - виконати аналіз одразу.\n"
    "2 - переглянути і відредагувати профіль збору і критики.\n"
    "3 - скасувати дослідження."
)

DISPLAYED_GATE = (
    "1 - прийняти профіль, виконати дослідження.\n"
    "2 - редагувати профіль.\n"
    "3 - скасувати дослідження."
)


def _text() -> str:
    return CORE.read_text(encoding="utf-8")


def test_core_builder_fits_builder_limit_and_keeps_two_stage_gate() -> None:
    text = _text()
    assert len(text) <= 8000
    assert FIRST_GATE in text
    assert DISPLAYED_GATE in text
    assert "DO NOT display the profile immediately" in text
    assert "approved_at=current ISO-8601 timestamp" in text


def test_core_builder_enforces_claim_level_cross_checks() -> None:
    text = _text()
    assert "LOW>=0, MEDIUM>=1, HIGH>=2, CRITICAL>=3" in text
    assert "CLAIM-LEVEL CROSS-CHECK LEDGER" in text
    assert "`required`: approved required_cross_checks" in text
    assert "`achieved_independent`" in text
    assert "`exception`: NONE | SHORTFALL" in text
    assert "An unconditional PASS is forbidden" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text


def test_core_builder_requires_traceable_pass_counts() -> None:
    text = _text()
    assert "TRACEABILITY INVARIANT" in text
    assert "Every evidence origin counted in `achieved_independent` MUST be traceable" in text
    assert "PASS count greater than the number of visibly traceable independent origins" in text
    assert "systematic review/meta-analysis counts as one evidence origin" in text
    assert "untraceable PASS count" in text
    assert "equals the number of valid, visibly traceable independent evidence origins" in text


def test_core_builder_requires_localized_claim_protocol_table() -> None:
    text = _text()
    assert "`ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`" in text
    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text
    assert "Include EVERY material factual claim" in text
    assert "Values must match visible claim blocks and traceable evidence origins" in text
    assert "localize equivalents for another selected report language" in text


def test_core_builder_localizes_all_user_visible_labels() -> None:
    text = _text()
    assert "headings, table titles/columns, field labels" in text
    assert "Canonical English keys may remain internal only" in text
    assert "`ФІНАЛЬНИЙ ЗВІТ`" in text
    assert "`ПЕРЕВІРКА ТВЕРДЖЕНЬ`" in text
    assert "`ПРОТОКОЛ ПЕРЕВІРКИ`" in text
    assert "Do not show English labels such as `Claim-level summary`" in text
    assert "raw keys such as `profile_id`, `risk_level`, `required_cross_checks`, `approved_at` remain internal" in text


def test_core_builder_is_clean_of_media_beta_operational_logic() -> None:
    text = _text()
    forbidden = (
        "Supadata",
        "KRCM_",
        "Instagram",
        "Facebook",
        "AI-транскрипція",
        "credits_available",
        "max_credits",
        "preflightManagedMediaCredits",
        "startManagedMediaNativeTranscription",
        "startManagedMediaAiTranscription",
    )
    for token in forbidden:
        assert token not in text


def test_core_builder_keeps_ukrainian_report_and_verdict_contract() -> None:
    text = _text()
    assert "ALWAYS reply in Ukrainian" in text
    assert "Source language never changes report language" in text
    assert "ПІДТВЕРДЖЕНО" in text
    assert "ЧАСТКОВО ПІДТВЕРДЖЕНО" in text
    assert "НЕ ПІДТВЕРДЖЕНО" in text
    assert "СУПЕРЕЧИТЬ ДЖЕРЕЛАМ" in text
    assert "ВВОДИТЬ В ОМАНУ" in text
    assert "НЕМОЖЛИВО ПЕРЕВІРИТИ" in text
    assert "ДУМКА" in text
