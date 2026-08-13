from __future__ import annotations

import os
import tempfile
from hashlib import sha256
from pathlib import Path
from time import perf_counter
from typing import Any

from pydantic import ValidationError

from models import (
    AgentDefinition,
    AgentResult,
    AgentRunRequest,
    AgentType,
    Artifact,
    ArtifactStatus,
    ArtifactType,
    CriticReview,
    ErrorRecord,
    ErrorType,
    ExecutionStatus,
    Metrics,
    ResearchResult,
    TaskStatus,
    utc_now,
)
from tools import CitationManager

from .base import Agent


class ReportGenerator(Agent):
    """Generate final user-facing Markdown artifacts from structured workflow results."""

    def __init__(self, output_directory: str | Path = "output") -> None:
        self.output_directory = Path(output_directory)
        self.citations = CitationManager()
        self._definition = AgentDefinition(
            agent_type=AgentType.REPORT_GENERATOR,
            name="ReportGenerator",
            version="1.0",
            capabilities=["final_report_generation", "review_protocol_generation"],
            accepted_input_types=["research_result", "critic_review_history"],
            produced_output_types=["artifacts"],
            supports_profile=False,
        )

    @property
    def definition(self) -> AgentDefinition:
        return self._definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        started_at = utc_now()
        timer = perf_counter()
        validation_error = self._validate_request(request)
        if validation_error is not None:
            return self._failed_result(request, started_at, timer, validation_error)

        try:
            research = ResearchResult.model_validate(request.input["final_research_result"])
            research_history = [
                ResearchResult.model_validate(item)
                for item in request.input.get("research_history", [request.input["final_research_result"]])
            ]
            review_history = [
                CriticReview.model_validate(item) for item in request.input.get("review_history", [])
            ]
            final_status = TaskStatus(str(request.input["final_status"]))
            self._validate_payload(request, research, research_history, review_history, final_status)
        except (KeyError, TypeError, ValueError, ValidationError) as exc:
            return self._failed_result(
                request,
                started_at,
                timer,
                ErrorRecord(
                    error_code="INVALID_REPORT_INPUT",
                    error_type=ErrorType.CONTRACT_ERROR,
                    message=str(exc),
                    recoverable=False,
                    component="ReportGenerator",
                    run_id=request.run_id,
                ),
            )

        try:
            self.output_directory.mkdir(parents=True, exist_ok=True)
            final_path = self.output_directory / f"{request.task_id}_FINAL_REPORT.md"
            protocol_path = self.output_directory / f"{request.task_id}_REVIEW_PROTOCOL.md"
            final_content = self._render_final_report(research, final_status)
            protocol_content = self._render_review_protocol(
                request,
                research_history,
                review_history,
                final_status,
            )
            artifacts = [
                self._artifact(request, final_path, final_content, ArtifactType.FINAL_REPORT, final_status),
                self._artifact(request, protocol_path, protocol_content, ArtifactType.REVIEW_PROTOCOL, final_status),
            ]
            self._write_artifact_pair(
                (
                    (final_path, final_content),
                    (protocol_path, protocol_content),
                )
            )
        except OSError as exc:
            return self._failed_result(
                request,
                started_at,
                timer,
                ErrorRecord(
                    error_code="ARTIFACT_WRITE_FAILED",
                    error_type=ErrorType.INTERNAL_ERROR,
                    message=str(exc),
                    recoverable=False,
                    component="ReportGenerator",
                    run_id=request.run_id,
                ),
            )

        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.REPORT_GENERATOR,
            status=ExecutionStatus.SUCCEEDED,
            result_type="artifacts",
            payload={
                "artifacts": [artifact.model_dump(mode="json") for artifact in artifacts],
                "final_status": final_status.value,
            },
            metrics=Metrics(duration_ms=max(0, int((perf_counter() - timer) * 1000))),
            started_at=started_at,
            completed_at=utc_now(),
        )

    def _write_artifact_pair(self, outputs: tuple[tuple[Path, str], tuple[Path, str]]) -> None:
        """Stage both files before commit and restore the previous pair if commit fails."""
        staged: dict[Path, Path] = {}
        backups: dict[Path, Path] = {}
        existed: dict[Path, bool] = {}

        try:
            for target, content in outputs:
                staged[target] = self._stage_text(target, content)

            for target, _ in outputs:
                existed[target] = target.exists()
                if existed[target]:
                    backup = self._reserve_temp_path(target, "backup")
                    os.replace(target, backup)
                    backups[target] = backup

            for target, _ in outputs:
                os.replace(staged[target], target)
        except OSError:
            self._rollback_artifact_pair(outputs, backups, existed)
            raise
        finally:
            for path in [*staged.values(), *backups.values()]:
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass

    def _stage_text(self, target: Path, content: str) -> Path:
        file_descriptor, name = tempfile.mkstemp(
            dir=self.output_directory,
            prefix=f".{target.name}.",
            suffix=".tmp",
        )
        os.close(file_descriptor)
        staged = Path(name)
        try:
            staged.write_text(content, encoding="utf-8")
        except OSError:
            staged.unlink(missing_ok=True)
            raise
        return staged

    def _reserve_temp_path(self, target: Path, purpose: str) -> Path:
        file_descriptor, name = tempfile.mkstemp(
            dir=self.output_directory,
            prefix=f".{target.name}.{purpose}.",
            suffix=".tmp",
        )
        os.close(file_descriptor)
        path = Path(name)
        path.unlink(missing_ok=True)
        return path

    @staticmethod
    def _rollback_artifact_pair(
        outputs: tuple[tuple[Path, str], tuple[Path, str]],
        backups: dict[Path, Path],
        existed: dict[Path, bool],
    ) -> None:
        for target, _ in reversed(outputs):
            backup = backups.get(target)
            try:
                if backup is not None and backup.exists():
                    os.replace(backup, target)
                elif not existed.get(target, False):
                    target.unlink(missing_ok=True)
            except OSError:
                pass

    def _validate_request(self, request: AgentRunRequest) -> ErrorRecord | None:
        if request.agent_type != AgentType.REPORT_GENERATOR:
            return self._contract_error(request, "INVALID_AGENT_TYPE", "ReportGenerator requires REPORT_GENERATOR")
        if request.agent_id != self.definition.agent_id:
            return self._contract_error(request, "AGENT_ID_MISMATCH", "AgentRunRequest agent_id does not match ReportGenerator")
        return None

    @staticmethod
    def _validate_payload(
        request: AgentRunRequest,
        research: ResearchResult,
        research_history: list[ResearchResult],
        review_history: list[CriticReview],
        final_status: TaskStatus,
    ) -> None:
        if final_status not in {TaskStatus.FINALIZED, TaskStatus.COMPLETED_WITH_LIMITATIONS}:
            raise ValueError("ReportGenerator final_status must be FINALIZED or COMPLETED_WITH_LIMITATIONS")
        if research.task_id != request.task_id:
            raise ValueError("Final ResearchResult task_id must match request task_id")
        if any(item.task_id != request.task_id for item in research_history):
            raise ValueError("Research history contains a different task_id")
        if any(item.task_id != request.task_id for item in review_history):
            raise ValueError("Review history contains a different task_id")
        iterations = [item.iteration for item in research_history]
        if iterations != sorted(iterations) or len(iterations) != len(set(iterations)):
            raise ValueError("Research history iterations must be unique and ordered")
        review_iterations = [item.iteration for item in review_history]
        if review_iterations != sorted(review_iterations) or len(review_iterations) != len(set(review_iterations)):
            raise ValueError("Review history iterations must be unique and ordered")

    def _render_final_report(self, research: ResearchResult, final_status: TaskStatus) -> str:
        lines = [
            f"# {research.task_id} FINAL REPORT",
            "",
            f"Status: {final_status.value}",
            f"Research iteration: {research.iteration}",
            "",
            "## Summary",
            "",
            research.summary,
            "",
            "## Findings",
            "",
        ]
        lines.extend(self._bullet_lines(research.findings, "No separate findings were recorded."))
        lines.extend(["", "## Evidence-backed Claims", ""])
        source_map = {source.source_id: source for source in research.sources}
        if research.claims:
            for claim in research.claims:
                citation = self.citations.cite_claim(claim, source_map)
                suffix = f" {citation}" if citation else ""
                lines.append(f"- {claim.text}{suffix}")
        else:
            lines.append("- No structured claims were recorded.")
        lines.extend(["", "## Uncertainty and Limitations", ""])
        uncertainty = [*research.uncertainties, *research.limitations]
        lines.extend(self._bullet_lines(uncertainty, "No explicit limitations were recorded."))
        lines.extend(["", "## Sources", ""])
        bibliography = self.citations.bibliography(research.sources)
        lines.append(bibliography or "No sources were recorded.")
        lines.extend(["", "## Approved Draft", "", research.draft_report, ""])
        return "\n".join(lines)

    def _render_review_protocol(
        self,
        request: AgentRunRequest,
        research_history: list[ResearchResult],
        review_history: list[CriticReview],
        final_status: TaskStatus,
    ) -> str:
        reviews = {item.iteration: item for item in review_history}
        lines = [
            f"# {request.task_id} REVIEW PROTOCOL",
            "",
            f"Workflow run: {request.workflow_run_id}",
            f"Final status: {final_status.value}",
            f"Completed research iterations: {len(research_history)}",
            "",
            "## Iteration History",
            "",
        ]
        for research in research_history:
            review = reviews.get(research.iteration)
            lines.extend([f"### Iteration {research.iteration}", ""])
            if review is None:
                lines.append("Critic decision: NOT_RECORDED")
            else:
                lines.extend(
                    [
                        f"Critic decision: {review.decision.value}",
                        f"Reliability score: {review.reliability_score:.4f}",
                        "",
                        "Critical issues:",
                        *self._bullet_lines(review.critical_issues, "None."),
                        "",
                        "Recommended changes:",
                        *self._bullet_lines(review.recommended_changes, "None."),
                        "",
                        "Unresolved items:",
                        *self._bullet_lines(
                            [
                                *review.contradictions,
                                *review.missing_topics,
                                *[f"Unsupported claim: {item}" for item in review.unsupported_claim_ids],
                                *[f"Unresolved claim: {item}" for item in review.unresolved_claim_ids],
                            ],
                            "None.",
                        ),
                    ]
                )
            lines.extend(["", "Changes applied by ResearchAgent:"])
            lines.extend(self._bullet_lines(research.changes_applied, "None recorded."))
            lines.append("")
        final_research = research_history[-1]
        final_limitations = [*final_research.uncertainties, *final_research.limitations]
        lines.extend(["## Final Limitations", ""])
        lines.extend(self._bullet_lines(final_limitations, "No explicit final limitations were recorded."))
        lines.extend(
            [
                "",
                "## Audit Note",
                "",
                "This protocol records structured workflow outcomes only. Hidden chain-of-thought and private model reasoning are not included.",
                "",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _bullet_lines(items: list[str], empty_text: str) -> list[str]:
        clean = [str(item).strip() for item in items if str(item).strip()]
        return [f"- {item}" for item in clean] if clean else [f"- {empty_text}"]

    @staticmethod
    def _artifact(
        request: AgentRunRequest,
        path: Path,
        content: str,
        artifact_type: ArtifactType,
        final_status: TaskStatus,
    ) -> Artifact:
        return Artifact(
            task_id=request.task_id,
            workflow_run_id=request.workflow_run_id,
            artifact_type=artifact_type,
            path=str(path),
            encoding="UTF-8",
            status=ArtifactStatus.APPROVED if final_status == TaskStatus.FINALIZED else ArtifactStatus.GENERATED,
            created_by_run_id=request.run_id,
            checksum=sha256(content.encode("utf-8")).hexdigest(),
            metadata={"final_task_status": final_status.value},
        )

    @staticmethod
    def _contract_error(request: AgentRunRequest, code: str, message: str) -> ErrorRecord:
        return ErrorRecord(
            error_code=code,
            error_type=ErrorType.CONTRACT_ERROR,
            message=message,
            recoverable=False,
            component="ReportGenerator",
            run_id=request.run_id,
        )

    @staticmethod
    def _failed_result(
        request: AgentRunRequest,
        started_at,
        timer: float,
        error: ErrorRecord,
    ) -> AgentResult:
        return AgentResult(
            run_id=request.run_id,
            request_id=request.request_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            agent_type=AgentType.REPORT_GENERATOR,
            status=ExecutionStatus.FAILED,
            result_type="artifacts",
            errors=[error],
            metrics=Metrics(duration_ms=max(0, int((perf_counter() - timer) * 1000))),
            started_at=started_at,
            completed_at=utc_now(),
        )
