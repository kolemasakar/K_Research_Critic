from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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


def test_core_instructions_use_two_stage_criticprofile_gate() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )

    assert "Do NOT display the profile immediately" in text
    assert FIRST_GATE in text
    assert DISPLAYED_GATE in text
    assert "approve the current undisplayed profile" in text
    assert "Never claim approval before explicit 1" in text
    assert "PROFILE_REVIEW_REQUIRED: do not display the profile immediately" in text


def test_media_builder_uses_two_stage_criticprofile_gate() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "DO NOT display the profile immediately" in text
    assert FIRST_GATE in text
    assert DISPLAYED_GATE in text
    assert "approve the current undisplayed profile" in text
    assert "Never claim approval before `1`" in text


def test_profile_gate_does_not_bypass_research_approval() -> None:
    core = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    media = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "No independent claim research before the CriticProfile is approved" in media
    assert "MANDATORY GATE: USER APPROVAL before research" in core
    assert 'status=APPROVED, approved_by="user"' in core
    assert "status=APPROVED, approved_by=user" in media


def test_required_cross_checks_are_enforced_and_auditable() -> None:
    core = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    media = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert "LOW>=0, MEDIUM>=1, HIGH>=2, CRITICAL>=3" in core
    assert "CRITICAL>=3, HIGH>=2, MEDIUM>=1, LOW>=0" in media
    assert "independent underlying evidence sources" in core
    assert "independent underlying evidence" in media
    assert "state the shortfall" in core
    assert "set exception=SHORTFALL" in media
    assert "cross-check compliance" in core
    assert "claim-by-claim" in media
    assert "required versus achieved cross-checks" in core
    assert "per-claim required/achieved/exception summary" in media
