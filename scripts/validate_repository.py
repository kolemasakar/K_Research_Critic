from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


class RepositoryValidationError(RuntimeError):
    """Raised when a repository-level quality invariant is violated."""


@dataclass(frozen=True)
class RepositoryValidationSummary:
    tracked_files: int
    documents_checked: int
    gitkeep_files_checked: int
    secret_patterns_checked: int


_FORBIDDEN_STABLE_SUFFIXES = ("_NEW", "_LATEST", "_FIXED", "_COPY", "FINAL2")
_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)
_TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".txt",
    ".example",
}
_CANONICAL_STANDARD_WITH_UNICODE_EXAMPLE = "PROJECT_FILE_STANDARD.md"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RepositoryValidationError(message)


def discover_tracked_files(root: Path) -> tuple[Path, ...]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    entries = completed.stdout.decode("utf-8").split("\0")
    return tuple(root / entry for entry in entries if entry)


def _is_ascii(value: str) -> bool:
    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def validate_document(path: Path, *, allow_additional_unicode: bool = False) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    relative = path.as_posix()

    _require(len(lines) >= 2, f"documentation file is too short: {relative}")
    _require(lines[0].startswith("# "), f"documentation title is missing: {relative}")
    _require(not _is_ascii(lines[1]), f"Ukrainian description line is missing after title: {relative}")

    if allow_additional_unicode:
        return

    for line_number, line in enumerate(lines[2:], start=3):
        _require(
            _is_ascii(line),
            f"non-ASCII content outside approved description line: {relative}:{line_number}",
        )


def _validate_gitkeep_files(root: Path, tracked: tuple[Path, ...]) -> int:
    relative_paths = {path.relative_to(root).as_posix() for path in tracked}
    checked = 0
    for relative in sorted(relative_paths):
        if not relative.endswith("/.gitkeep"):
            continue
        checked += 1
        parent = relative.rsplit("/", 1)[0]
        real_siblings = [
            item
            for item in relative_paths
            if item.startswith(f"{parent}/") and item != relative and not item.endswith("/.gitkeep")
        ]
        _require(
            not real_siblings,
            f"remove stale .gitkeep because directory has tracked content: {relative}",
        )
    return checked


def _validate_secret_patterns(root: Path, tracked: tuple[Path, ...]) -> int:
    checked = 0
    for path in tracked:
        relative = path.relative_to(root)
        if relative.name == ".env":
            raise RepositoryValidationError("tracked .env file is prohibited")
        if not path.is_file():
            continue
        if path.suffix.lower() not in _TEXT_SUFFIXES and path.name != ".env.example":
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        checked += 1
        for pattern in _SECRET_PATTERNS:
            match = pattern.search(text)
            _require(
                match is None,
                f"possible tracked secret detected in {relative.as_posix()}",
            )
    return checked


def validate_repository(root: Path) -> RepositoryValidationSummary:
    root = root.resolve()
    tracked = discover_tracked_files(root)
    _require(bool(tracked), "repository contains no tracked files")

    documents: list[Path] = []
    readme = root / "README.md"
    if readme in tracked:
        documents.append(readme)
    documents.extend(sorted(path for path in tracked if path.parent == root / "docs" and path.suffix == ".md"))

    for path in tracked:
        relative = path.relative_to(root).as_posix()
        _require(_is_ascii(relative), f"tracked filename must be ASCII: {relative}")
        upper_name = path.name.upper()
        if path.suffix == ".md":
            _require(
                not any(marker in upper_name for marker in _FORBIDDEN_STABLE_SUFFIXES),
                f"ambiguous documentation revision suffix: {relative}",
            )

    for document in documents:
        validate_document(
            document,
            allow_additional_unicode=document.name == _CANONICAL_STANDARD_WITH_UNICODE_EXAMPLE,
        )

    gitkeep_count = _validate_gitkeep_files(root, tracked)
    secret_count = _validate_secret_patterns(root, tracked)

    _require((root / "prompts" / "GPT_STORE_INSTRUCTIONS.md") in tracked, "Store instruction package must be tracked")
    _require((root / "gpt_store" / "manifest.yaml") in tracked, "Store manifest must be tracked")

    return RepositoryValidationSummary(
        tracked_files=len(tracked),
        documents_checked=len(documents),
        gitkeep_files_checked=gitkeep_count,
        secret_patterns_checked=secret_count,
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        summary = validate_repository(root)
    except (RepositoryValidationError, OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print(f"Repository validation: FAIL: {exc}")
        return 1

    print(
        "Repository validation: PASS "
        f"({summary.tracked_files} tracked files, "
        f"{summary.documents_checked} documents, "
        f"{summary.gitkeep_files_checked} .gitkeep files, "
        f"{summary.secret_patterns_checked} text files scanned)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
