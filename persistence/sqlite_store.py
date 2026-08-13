from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from models import (
    AgentResult,
    Artifact,
    Claim,
    CriticProfile,
    CriticReview,
    DomainAssessment,
    ResearchResult,
    Source,
    StateTransition,
    Task,
    UserApproval,
    WorkflowRun,
)

from .base import TaskAuditSnapshot

ModelT = TypeVar("ModelT", bound=BaseModel)


class SQLitePersistenceStore:
    """SQLite implementation that stores validated contracts as exact JSON snapshots."""

    SCHEMA_VERSION = "1"

    def __init__(self, path: str | Path = "runtime/k_supervisor.db") -> None:
        self.path = Path(path)
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self.path))
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS schema_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS workflow_runs (
                    workflow_run_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_state TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_workflow_runs_task
                    ON workflow_runs(task_id, started_at);

                CREATE TABLE IF NOT EXISTS state_transitions (
                    transition_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    workflow_run_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_state_transitions_workflow
                    ON state_transitions(workflow_run_id, created_at);

                CREATE TABLE IF NOT EXISTS agent_runs (
                    run_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    agent_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_agent_runs_task
                    ON agent_runs(task_id, started_at);

                CREATE TABLE IF NOT EXISTS domain_assessments (
                    assessment_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_domain_assessments_task
                    ON domain_assessments(task_id, created_at);

                CREATE TABLE IF NOT EXISTS critic_profiles (
                    profile_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_critic_profiles_task
                    ON critic_profiles(task_id, version, created_at);

                CREATE TABLE IF NOT EXISTS user_approvals (
                    approval_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_user_approvals_task
                    ON user_approvals(task_id, created_at);

                CREATE TABLE IF NOT EXISTS research_results (
                    research_result_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_research_results_task
                    ON research_results(task_id, iteration, created_at);

                CREATE TABLE IF NOT EXISTS claims (
                    claim_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_claims_task
                    ON claims(task_id, created_at);

                CREATE TABLE IF NOT EXISTS sources (
                    source_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_sources_task
                    ON sources(task_id, source_id);

                CREATE TABLE IF NOT EXISTS reviews (
                    review_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    iteration INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_reviews_task
                    ON reviews(task_id, iteration, created_at);

                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    workflow_run_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_artifacts_task
                    ON artifacts(task_id, created_at);
                """
            )
            connection.execute(
                """
                INSERT INTO schema_meta(key, value)
                VALUES('schema_version', ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (self.SCHEMA_VERSION,),
            )

    @staticmethod
    def _json(model: BaseModel) -> str:
        return model.model_dump_json()

    def save_task(self, task: Task) -> None:
        self._execute(
            """
            INSERT INTO tasks(task_id, status, updated_at, payload)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                status = excluded.status,
                updated_at = excluded.updated_at,
                payload = excluded.payload
            """,
            (task.task_id, task.status.value, task.updated_at.isoformat(), self._json(task)),
        )

    def save_workflow_run(self, workflow_run: WorkflowRun) -> None:
        self._execute(
            """
            INSERT INTO workflow_runs(
                workflow_run_id, task_id, status, current_state, started_at, payload
            ) VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(workflow_run_id) DO UPDATE SET
                task_id = excluded.task_id,
                status = excluded.status,
                current_state = excluded.current_state,
                started_at = excluded.started_at,
                payload = excluded.payload
            """,
            (
                workflow_run.workflow_run_id,
                workflow_run.task_id,
                workflow_run.status.value,
                workflow_run.current_state.value,
                workflow_run.started_at.isoformat(),
                self._json(workflow_run),
            ),
        )

    def save_state_transition(self, transition: StateTransition) -> None:
        self._execute(
            """
            INSERT INTO state_transitions(
                transition_id, task_id, workflow_run_id, created_at, payload
            ) VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(transition_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                transition.transition_id,
                transition.task_id,
                transition.workflow_run_id,
                transition.created_at.isoformat(),
                self._json(transition),
            ),
        )

    def save_agent_result(self, result: AgentResult) -> None:
        self._execute(
            """
            INSERT INTO agent_runs(run_id, task_id, agent_type, status, started_at, payload)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(run_id) DO UPDATE SET
                status = excluded.status,
                payload = excluded.payload
            """,
            (
                result.run_id,
                result.task_id,
                result.agent_type.value,
                result.status.value,
                result.started_at.isoformat(),
                self._json(result),
            ),
        )

    def save_domain_assessment(self, assessment: DomainAssessment) -> None:
        self._execute(
            """
            INSERT INTO domain_assessments(assessment_id, task_id, created_at, payload)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(assessment_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                assessment.assessment_id,
                assessment.task_id,
                assessment.created_at.isoformat(),
                self._json(assessment),
            ),
        )

    def save_critic_profile(self, profile: CriticProfile) -> None:
        self._execute(
            """
            INSERT INTO critic_profiles(profile_id, task_id, version, status, created_at, payload)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                version = excluded.version,
                status = excluded.status,
                payload = excluded.payload
            """,
            (
                profile.profile_id,
                profile.task_id,
                profile.version,
                profile.status.value,
                profile.created_at.isoformat(),
                self._json(profile),
            ),
        )

    def save_user_approval(self, approval: UserApproval) -> None:
        self._execute(
            """
            INSERT INTO user_approvals(approval_id, task_id, created_at, payload)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(approval_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                approval.approval_id,
                approval.task_id,
                approval.created_at.isoformat(),
                self._json(approval),
            ),
        )

    def save_research_result(self, result: ResearchResult) -> None:
        self._execute(
            """
            INSERT INTO research_results(
                research_result_id, task_id, run_id, iteration, created_at, payload
            ) VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(research_result_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                result.research_result_id,
                result.task_id,
                result.run_id,
                result.iteration,
                result.created_at.isoformat(),
                self._json(result),
            ),
        )
        for source in result.sources:
            self.save_source(source)
        for claim in result.claims:
            self.save_claim(claim)

    def save_claim(self, claim: Claim) -> None:
        self._execute(
            """
            INSERT INTO claims(claim_id, task_id, run_id, created_at, payload)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(claim_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                claim.claim_id,
                claim.task_id,
                claim.created_by_run_id,
                claim.created_at.isoformat(),
                self._json(claim),
            ),
        )

    def save_source(self, source: Source) -> None:
        self._execute(
            """
            INSERT INTO sources(source_id, task_id, payload)
            VALUES(?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET payload = excluded.payload
            """,
            (source.source_id, source.task_id, self._json(source)),
        )

    def save_critic_review(self, review: CriticReview) -> None:
        self._execute(
            """
            INSERT INTO reviews(review_id, task_id, run_id, iteration, created_at, payload)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(review_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                review.review_id,
                review.task_id,
                review.run_id,
                review.iteration,
                review.created_at.isoformat(),
                self._json(review),
            ),
        )

    def save_artifact(self, artifact: Artifact) -> None:
        self._execute(
            """
            INSERT INTO artifacts(
                artifact_id, task_id, workflow_run_id, created_at, payload
            ) VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET payload = excluded.payload
            """,
            (
                artifact.artifact_id,
                artifact.task_id,
                artifact.workflow_run_id,
                artifact.created_at.isoformat(),
                self._json(artifact),
            ),
        )

    def load_task(self, task_id: str) -> Task:
        return self._load_one("tasks", "task_id", task_id, Task)

    def load_workflow_run(self, workflow_run_id: str) -> WorkflowRun:
        return self._load_one(
            "workflow_runs", "workflow_run_id", workflow_run_id, WorkflowRun
        )

    def load_workflow_for_task(self, task_id: str) -> WorkflowRun | None:
        return self._load_latest(
            "workflow_runs", task_id, WorkflowRun, order_by="started_at"
        )

    def load_state_transitions(self, workflow_run_id: str) -> list[StateTransition]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM state_transitions
                WHERE workflow_run_id = ?
                ORDER BY created_at, transition_id
                """,
                (workflow_run_id,),
            ).fetchall()
        return [StateTransition.model_validate_json(row["payload"]) for row in rows]

    def load_agent_results(self, task_id: str) -> list[AgentResult]:
        return self._load_many("agent_runs", task_id, AgentResult, "started_at, run_id")

    def load_domain_assessments(self, task_id: str) -> list[DomainAssessment]:
        return self._load_many(
            "domain_assessments", task_id, DomainAssessment, "created_at, assessment_id"
        )

    def load_critic_profiles(self, task_id: str) -> list[CriticProfile]:
        return self._load_many(
            "critic_profiles", task_id, CriticProfile, "version, created_at, profile_id"
        )

    def load_user_approvals(self, task_id: str) -> list[UserApproval]:
        return self._load_many(
            "user_approvals", task_id, UserApproval, "created_at, approval_id"
        )

    def load_research_results(self, task_id: str) -> list[ResearchResult]:
        return self._load_many(
            "research_results", task_id, ResearchResult, "iteration, created_at, research_result_id"
        )

    def load_claims(self, task_id: str) -> list[Claim]:
        return self._load_many("claims", task_id, Claim, "created_at, claim_id")

    def load_sources(self, task_id: str) -> list[Source]:
        return self._load_many("sources", task_id, Source, "source_id")

    def load_reviews(self, task_id: str) -> list[CriticReview]:
        return self._load_many(
            "reviews", task_id, CriticReview, "iteration, created_at, review_id"
        )

    def load_artifacts(self, task_id: str) -> list[Artifact]:
        return self._load_many(
            "artifacts", task_id, Artifact, "created_at, artifact_id"
        )

    def load_task_audit(self, task_id: str) -> TaskAuditSnapshot:
        task = self.load_task(task_id)
        workflow = self.load_workflow_for_task(task_id)
        transitions = (
            tuple(self.load_state_transitions(workflow.workflow_run_id))
            if workflow is not None
            else ()
        )
        return TaskAuditSnapshot(
            task=task,
            workflow_run=workflow,
            transitions=transitions,
            domain_assessments=tuple(self.load_domain_assessments(task_id)),
            critic_profiles=tuple(self.load_critic_profiles(task_id)),
            user_approvals=tuple(self.load_user_approvals(task_id)),
            agent_results=tuple(self.load_agent_results(task_id)),
            research_results=tuple(self.load_research_results(task_id)),
            claims=tuple(self.load_claims(task_id)),
            sources=tuple(self.load_sources(task_id)),
            reviews=tuple(self.load_reviews(task_id)),
            artifacts=tuple(self.load_artifacts(task_id)),
        )

    def list_task_ids(self) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT task_id FROM tasks ORDER BY updated_at, task_id"
            ).fetchall()
        return [str(row["task_id"]) for row in rows]

    def table_names(self) -> list[str]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            ).fetchall()
        return [str(row["name"]) for row in rows]

    def count_records(self, table: str) -> int:
        allowed = {
            "tasks",
            "workflow_runs",
            "state_transitions",
            "agent_runs",
            "domain_assessments",
            "critic_profiles",
            "user_approvals",
            "research_results",
            "claims",
            "sources",
            "reviews",
            "artifacts",
        }
        if table not in allowed:
            raise ValueError(f"Unsupported persistence table: {table}")
        with self._connect() as connection:
            row = connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
        return int(row["count"])

    def schema_version(self) -> str:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT value FROM schema_meta WHERE key = 'schema_version'"
            ).fetchone()
        if row is None:
            raise RuntimeError("SQLite persistence schema version is missing")
        return str(row["value"])

    def _execute(self, sql: str, params: tuple[Any, ...]) -> None:
        with self._connect() as connection:
            connection.execute(sql, params)

    def _load_one(
        self,
        table: str,
        id_column: str,
        identifier: str,
        model: type[ModelT],
    ) -> ModelT:
        with self._connect() as connection:
            row = connection.execute(
                f"SELECT payload FROM {table} WHERE {id_column} = ?",
                (identifier,),
            ).fetchone()
        if row is None:
            raise KeyError(f"No persisted {table} record for {identifier}")
        return model.model_validate_json(row["payload"])

    def _load_latest(
        self,
        table: str,
        task_id: str,
        model: type[ModelT],
        *,
        order_by: str,
    ) -> ModelT | None:
        with self._connect() as connection:
            row = connection.execute(
                f"""
                SELECT payload FROM {table}
                WHERE task_id = ?
                ORDER BY {order_by} DESC
                LIMIT 1
                """,
                (task_id,),
            ).fetchone()
        return None if row is None else model.model_validate_json(row["payload"])

    def _load_many(
        self,
        table: str,
        task_id: str,
        model: type[ModelT],
        order_by: str,
    ) -> list[ModelT]:
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT payload FROM {table}
                WHERE task_id = ?
                ORDER BY {order_by}
                """,
                (task_id,),
            ).fetchall()
        return [model.model_validate_json(row["payload"]) for row in rows]
