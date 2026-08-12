from pathlib import Path


REQUIRED_PATHS = (
    "README.md",
    ".env.example",
    "requirements.txt",
    "config/settings.yaml",
    "docs/PROJECT_FILE_STANDARD.md",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
    "docs/AGENT_INTERFACE.md",
    "docs/DATA_MODELS.md",
    "docs/RESEARCH_WORKFLOW.md",
    "docs/CONFIGURATION.md",
    "docs/TEST_PLAN.md",
    "agents",
    "supervisor",
    "tools",
    "models",
    "prompts",
    "config",
    "tests",
    "scripts",
    "output",
    "logs",
)


def test_required_repository_paths_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    assert not missing, f"Missing required repository paths: {missing}"


def test_real_env_file_is_not_tracked_fixture() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / ".env.example").is_file()
