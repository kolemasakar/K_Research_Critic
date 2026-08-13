from __future__ import annotations

from pathlib import Path

from config import AppSettings, LoadedConfiguration, RuntimeSecrets, load_configuration
from persistence import SQLitePersistenceStore
from supervisor import KSupervisorApplication


ROOT = Path(__file__).resolve().parents[1]
TRACKED_SETTINGS = ROOT / "config" / "settings.yaml"


class NoopTools:
    def web_search(self, query: str, *, limit: int):
        return []

    def web_fetch(self, url: str):
        raise RuntimeError("not used")


def _changed_configuration() -> LoadedConfiguration:
    base = load_configuration(TRACKED_SETTINGS, env_path=None, environ={})
    raw = base.settings.model_dump(mode="python")
    raw["research"]["max_queries"] = 5
    raw["limits"]["max_search_calls"] = 12
    settings = AppSettings.model_validate(raw)
    return LoadedConfiguration(
        settings=settings,
        secrets=RuntimeSecrets(),
        settings_path=TRACKED_SETTINGS,
        env_path=None,
    )


def test_profile_amendment_after_restart_preserves_original_frozen_configuration(
    tmp_path: Path,
) -> None:
    database = tmp_path / "audit.db"
    original_configuration = load_configuration(
        TRACKED_SETTINGS,
        env_path=None,
        environ={},
    )
    first_app = KSupervisorApplication(
        NoopTools(),
        output_directory=tmp_path / "original-output",
        persistence=SQLitePersistenceStore(database),
        configuration=original_configuration,
    )
    prepared = first_app.prepare_task("Explain software architecture behavior.")
    first_profile, _ = first_app.approve_profile(
        prepared.task.task_id,
        approved_by="TEST_USER",
    )
    first_snapshot = first_app.configuration_snapshot(prepared.task.task_id)
    assert first_snapshot is not None

    changed_configuration = _changed_configuration()
    assert changed_configuration.fingerprint != original_configuration.fingerprint
    second_app = KSupervisorApplication(
        NoopTools(),
        output_directory=tmp_path / "changed-output",
        persistence=SQLitePersistenceStore(database),
        configuration=changed_configuration,
    )
    recovery = second_app.recover_task(prepared.task.task_id)
    assert recovery.resumable is True

    second_app.propose_profile_amendment(
        prepared.task.task_id,
        changes={"critic_role": "Independent post-restart architecture reviewer"},
        reason="Test frozen configuration continuity across restart",
    )
    second_profile, _ = second_app.approve_profile(
        prepared.task.task_id,
        approved_by="TEST_USER",
    )
    second_snapshot = second_app.configuration_snapshot(prepared.task.task_id)

    assert second_snapshot is not None
    assert second_profile.profile_id != first_profile.profile_id
    assert second_snapshot.supersedes_snapshot_id == first_snapshot.snapshot_id
    assert second_snapshot.approved_profile_id == second_profile.profile_id
    assert second_snapshot.effective_settings == first_snapshot.effective_settings
    assert second_snapshot.settings_fingerprint == first_snapshot.settings_fingerprint
    assert second_snapshot.environment == first_snapshot.environment
