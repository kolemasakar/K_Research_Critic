from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from models.identifiers import generate_id

from .loader import LoadedConfiguration
from .schema import AppSettings


class TaskConfigurationSnapshot(BaseModel):
    """Immutable, secret-free effective configuration frozen for one approved profile."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    snapshot_id: str = Field(default_factory=lambda: generate_id("CONFIG"))
    task_id: str = Field(min_length=1)
    configuration_schema_version: str = Field(min_length=1)
    environment: str = Field(min_length=1)
    settings_fingerprint: str = Field(min_length=64, max_length=64)
    effective_settings: AppSettings
    approved_profile_id: str = Field(min_length=1)
    approved_profile_version: int = Field(ge=1)
    supersedes_snapshot_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def create_task_configuration_snapshot(
    configuration: LoadedConfiguration,
    *,
    task_id: str,
    approved_profile_id: str,
    approved_profile_version: int,
    max_iterations: int | None = None,
    output_directory: str | None = None,
    persistence_path: str | None = None,
    supersedes_snapshot_id: str | None = None,
) -> TaskConfigurationSnapshot:
    """Freeze validated effective settings without copying runtime secrets."""

    raw: dict[str, Any] = configuration.settings.model_dump(mode="python")
    if max_iterations is not None:
        raw["workflow"]["max_iterations"] = max_iterations
    if output_directory is not None:
        raw["reports"]["output_directory"] = output_directory
    if persistence_path is not None:
        raw["persistence"]["path"] = persistence_path

    effective = AppSettings.model_validate(raw)
    minimum_agent_capacity = (effective.workflow.max_iterations * 2) + 1
    if minimum_agent_capacity > effective.limits.max_agent_runs:
        raise ValueError(
            "limits.max_agent_runs is too low for the effective workflow.max_iterations; "
            f"requires at least {minimum_agent_capacity}"
        )
    fingerprint = hashlib.sha256(
        effective.model_dump_json().encode("utf-8")
    ).hexdigest()

    return TaskConfigurationSnapshot(
        task_id=task_id,
        configuration_schema_version=effective.schema_version,
        environment=effective.environment,
        settings_fingerprint=fingerprint,
        effective_settings=effective,
        approved_profile_id=approved_profile_id,
        approved_profile_version=approved_profile_version,
        supersedes_snapshot_id=supersedes_snapshot_id,
    )


def snapshots_from_task_metadata(metadata: dict[str, Any]) -> tuple[TaskConfigurationSnapshot, ...]:
    raw = metadata.get("configuration_snapshots", [])
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise ValueError("Task metadata configuration_snapshots must be a list")
    return tuple(TaskConfigurationSnapshot.model_validate(item) for item in raw)


def latest_task_configuration_snapshot(
    metadata: dict[str, Any],
) -> TaskConfigurationSnapshot | None:
    snapshots = snapshots_from_task_metadata(metadata)
    return snapshots[-1] if snapshots else None
