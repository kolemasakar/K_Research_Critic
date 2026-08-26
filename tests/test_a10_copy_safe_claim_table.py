from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_a10_builder_claim_table_is_rendered_and_copy_safe() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8"))
    instructions = manifest["instructions"]
    text = (ROOT / instructions["file"]).read_text(encoding="utf-8")

    assert len(text) <= instructions["builder_character_limit"]
    assert instructions["builder_runtime_applied"] is True
    assert instructions["cross_check_copy_safe_table_required"] is True
    assert "| Твердження | Потрібно | Отримано незалежних | Виняток |" in text
    assert "| --- | ---: | ---: | --- |" in text
    assert "КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ" in text
    assert "fenced `text` code block" in text
    assert "exact header row, separator row and every claim row" in text
    assert "It MUST match the rendered table values exactly" in text

    release = manifest["release"]
    assert release["stabilization_state"] == "A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED"
    assert release["a10_claim_summary_table_runtime_accepted"] is True
    assert release["a10_copy_safe_claim_table_runtime_accepted"] is True
    assert release["gpt_builder_private_update_required"] is False


def test_a10_canonical_managed_reference_documents_copy_safe_fallback() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert "render the table correctly but serialize its header incorrectly" in text
    assert "КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ" in text
    assert "fenced `text` code block" in text
    assert "preserve literal `|` delimiters" in text
    assert "match the rendered table values exactly" in text


def test_a10_runtime_acceptance_record_preserves_real_shortfall_and_copy_safe_rows() -> None:
    text = (ROOT / "subprojects" / "media_beta" / "52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md").read_text(encoding="utf-8")

    assert "A10 runtime gate: **PASS**" in text
    assert "A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED" in text
    assert "| Твердження | Потрібно | Отримано незалежних | Виняток |" in text
    assert "| 4. Саморобна конструкція є працездатною та безпечною | 1 | 0 | SHORTFALL |" in text
    assert "53 s` media / `53 s` STT / `0` credits" in text
