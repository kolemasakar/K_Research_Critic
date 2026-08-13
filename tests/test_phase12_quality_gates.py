from pathlib import Path

import pytest

from scripts.validate_repository import RepositoryValidationError, validate_document, validate_repository


ROOT = Path(__file__).resolve().parents[1]


def test_repository_static_policy_passes() -> None:
    summary = validate_repository(ROOT)

    assert summary.tracked_files >= 70
    assert summary.documents_checked >= 10
    assert summary.secret_patterns_checked >= 40


def test_document_validator_rejects_non_ascii_after_description(tmp_path: Path) -> None:
    document = tmp_path / "BROKEN.md"
    document.write_text(
        "# BROKEN\n"
        "Короткий опис документа.\n\n"
        "This line is valid ASCII.\n"
        "А цей рядок вже не дозволений.\n",
        encoding="utf-8",
    )

    with pytest.raises(RepositoryValidationError, match="non-ASCII content"):
        validate_document(document)


def test_ci_declares_current_action_major_versions_and_quality_gates() -> None:
    workflow = (ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v6" in workflow
    assert "actions/setup-python@v6" in workflow
    assert 'python-version: ["3.13", "3.14"]' in workflow
    assert "python -m ruff check" in workflow
    assert "python -m mypy" in workflow
    assert "python -m scripts.validate_repository" in workflow
    assert "python -m scripts.validate_store_package" in workflow
    assert "--cov-fail-under=70" in workflow
    assert "pull_request:" in workflow


def test_phase12_development_dependencies_are_declared() -> None:
    dependencies = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")

    assert "mypy" in dependencies
    assert "pytest-cov" in dependencies
    assert "ruff" in dependencies
    assert "types-PyYAML" in dependencies


def test_dependabot_covers_python_and_github_actions() -> None:
    configuration = (ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8")

    assert 'package-ecosystem: "pip"' in configuration
    assert 'package-ecosystem: "github-actions"' in configuration
