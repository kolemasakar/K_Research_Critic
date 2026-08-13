from __future__ import annotations

from typing import Any

from config import TaskConfigurationSnapshot, snapshots_from_task_metadata
from models import DomainAssessment, Task, utc_now
from persistence import PersistenceStore

from .exceptions import DuplicateTaskError, TaskNotFoundError


class TaskManager:
    """Task registry with optional write-through persistence."""

    def __init__(self, persistence: PersistenceStore | None = None) -> None:
        self.persistence = persistence
        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        *,
        user_request: str,
        task_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> Task:
        task = Task(user_request=user_request, task_type=task_type, metadata=metadata or {})
        self.add_task(task)
        return task

    def add_task(self, task: Task) -> None:
        if task.task_id in self._tasks:
            raise DuplicateTaskError(f"Task already exists: {task.task_id}")
        self._tasks[task.task_id] = task
        self.persist_task(task.task_id)

    def restore_task(self, task: Task) -> Task:
        """Restore an exact persisted task without changing its timestamps or state."""
        existing = self._tasks.get(task.task_id)
        if existing is not None and existing.model_dump(mode="json") != task.model_dump(mode="json"):
            raise DuplicateTaskError(f"Task already exists with different state: {task.task_id}")
        self._tasks[task.task_id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise TaskNotFoundError(f"Unknown task_id: {task_id}") from exc

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def set_active_profile(self, task_id: str, profile_id: str) -> Task:
        task = self.get_task(task_id)
        task.active_profile_id = profile_id
        task.updated_at = utc_now()
        self.persist_task(task_id)
        return task

    def attach_workflow(self, task_id: str, workflow_run_id: str) -> Task:
        task = self.get_task(task_id)
        task.current_workflow_run_id = workflow_run_id
        task.updated_at = utc_now()
        self.persist_task(task_id)
        return task

    def apply_domain_assessment(self, task_id: str, assessment: DomainAssessment) -> Task:
        task = self.get_task(task_id)
        if assessment.task_id != task.task_id:
            raise ValueError("DomainAssessment task_id must match Task task_id")
        task.primary_domain = assessment.primary_domain
        task.secondary_domains = list(assessment.secondary_domains)
        task.task_type = assessment.task_type
        task.risk_level = assessment.risk_level
        task.updated_at = utc_now()
        self.persist_task(task_id)
        return task

    def append_configuration_snapshot(
        self,
        task_id: str,
        snapshot: TaskConfigurationSnapshot,
    ) -> Task:
        """Append a profile-linked snapshot while preserving the task's frozen settings."""
        task = self.get_task(task_id)
        if snapshot.task_id != task_id:
            raise ValueError("TaskConfigurationSnapshot task_id must match Task task_id")

        existing = list(snapshots_from_task_metadata(task.metadata))
        for item in existing:
            if item.snapshot_id == snapshot.snapshot_id:
                if item != snapshot:
                    raise ValueError("Configuration snapshot ID already exists with different content")
                return task

        latest = existing[-1] if existing else None
        if latest is None and snapshot.supersedes_snapshot_id is not None:
            raise ValueError("Initial configuration snapshot cannot supersede another snapshot")
        if latest is not None:
            if snapshot.supersedes_snapshot_id != latest.snapshot_id:
                raise ValueError("New configuration snapshot must supersede the current snapshot")
            snapshot = TaskConfigurationSnapshot(
                task_id=task_id,
                configuration_schema_version=latest.configuration_schema_version,
                environment=latest.environment,
                settings_fingerprint=latest.settings_fingerprint,
                effective_settings=latest.effective_settings,
                approved_profile_id=snapshot.approved_profile_id,
                approved_profile_version=snapshot.approved_profile_version,
                supersedes_snapshot_id=latest.snapshot_id,
            )

        serialized = [item.model_dump(mode="json") for item in existing]
        serialized.append(snapshot.model_dump(mode="json"))
        task.metadata = {
            **task.metadata,
            "configuration_snapshots": serialized,
            "active_configuration_snapshot_id": snapshot.snapshot_id,
        }
        task.updated_at = utc_now()
        self.persist_task(task_id)
        return task

    def persist_task(self, task_id: str) -> None:
        if self.persistence is not None:
            self.persistence.save_task(self.get_task(task_id))
