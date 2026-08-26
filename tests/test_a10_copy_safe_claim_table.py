from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_a10_builder_claim_table_is_rendered_and_copy_safe() -> None:
    manifest = yaml.safe_load((ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8"))
    instructions = manifest["instructions"]
    text = (ROOT / instructions["file"]).read_text(encoding="utf-8")

    assert len(text) <= instructions["builder_character_limit"]
    assert "| Твердження | Потрібно | Отримано незалежних | Виняток |" in text
    assert "| --- | ---: | ---: | --- |" in text
    assert "КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ" in text
    assert "fenced `text` code block" in text
    assert "exact header row, separator row and every claim row" in text
    assert "It MUST match the rendered table values exactly" in text


def test_a10_canonical_managed_reference_documents_copy_safe_fallback() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert "render the table correctly but serialize its header incorrectly" in text
    assert "КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ" in text
    assert "fenced `text` code block" in text
    assert "preserve literal `|` delimiters" in text
    assert "match the rendered table values exactly" in text
