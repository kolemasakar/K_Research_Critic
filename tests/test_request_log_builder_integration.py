from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_core_instructions_include_non_blocking_request_logging() -> None:
    text = (ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "REQUEST LOGGING" in text
    assert "call `logRequest` exactly once" in text
    assert "short generalized topic <=160 characters" in text
    assert "Do not log standalone `1`, `2`, `3`" in text
    assert "NON-BLOCKING" in text
    assert "do not repeatedly retry" in text
    assert "logger records `none`" in text
