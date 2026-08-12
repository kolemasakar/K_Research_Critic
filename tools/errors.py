from __future__ import annotations

from typing import Any


class ToolExecutionError(RuntimeError):
    """Normalized provider-neutral error raised by tool adapters."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        operation: str,
        retryable: bool = True,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.operation = operation
        self.retryable = retryable
        self.details = details or {}
