from __future__ import annotations

from pathlib import Path

from agents import Agent
from models import AgentResult, AgentRunRequest, ErrorRecord, ErrorType, ExecutionStatus


class OutputBoundedReportGenerator(Agent):
    """Fail report generation if generated artifacts exceed the task output budget."""

    def __init__(
        self,
        delegate: Agent,
        *,
        default_max_output_size_bytes: int | None = None,
    ) -> None:
        if default_max_output_size_bytes is not None and default_max_output_size_bytes <= 0:
            raise ValueError("default_max_output_size_bytes must be greater than zero")
        self.delegate = delegate
        self.default_max_output_size_bytes = default_max_output_size_bytes

    @property
    def definition(self):
        return self.delegate.definition

    def run(self, request: AgentRunRequest) -> AgentResult:
        result = self.delegate.run(request)
        if result.status != ExecutionStatus.SUCCEEDED:
            return result

        raw_limit = request.context.get(
            "max_output_size_bytes", self.default_max_output_size_bytes
        )
        if raw_limit is None:
            return result
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError):
            return self._failed_for_invalid_limit(result, raw_limit)
        if limit <= 0:
            return self._failed_for_invalid_limit(result, raw_limit)

        paths: list[Path] = []
        total_bytes = 0
        for raw in result.payload.get("artifacts", []):
            path_value = raw.get("path") if isinstance(raw, dict) else None
            if not isinstance(path_value, str):
                continue
            path = Path(path_value)
            paths.append(path)
            try:
                total_bytes += path.stat().st_size
            except OSError:
                continue

        if total_bytes <= limit:
            return result

        for path in paths:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass

        error = ErrorRecord(
            error_code="MAX_OUTPUT_SIZE_EXCEEDED",
            error_type=ErrorType.INTERNAL_ERROR,
            message=(
                f"Generated artifacts used {total_bytes} bytes; configured maximum is "
                f"{limit} bytes"
            ),
            recoverable=False,
            component="ReportGenerator",
            run_id=result.run_id,
            details={"actual_bytes": total_bytes, "max_output_size_bytes": limit},
        )
        return self._failed(result, error)

    @staticmethod
    def _failed_for_invalid_limit(result: AgentResult, raw_limit: object) -> AgentResult:
        error = ErrorRecord(
            error_code="INVALID_OUTPUT_SIZE_LIMIT",
            error_type=ErrorType.CONTRACT_ERROR,
            message=f"Invalid max_output_size_bytes: {raw_limit!r}",
            recoverable=False,
            component="ReportGenerator",
            run_id=result.run_id,
        )
        return OutputBoundedReportGenerator._failed(result, error)

    @staticmethod
    def _failed(result: AgentResult, error: ErrorRecord) -> AgentResult:
        values = result.model_dump(mode="python")
        values.update(
            status=ExecutionStatus.FAILED,
            payload={},
            errors=[*result.errors, error],
        )
        return AgentResult.model_validate(values)
