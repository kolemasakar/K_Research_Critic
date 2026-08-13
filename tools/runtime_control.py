from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from contextlib import contextmanager
from dataclasses import dataclass
from time import monotonic, sleep
from typing import Callable, Iterator, TypeVar

from .errors import ToolExecutionError
from .interfaces import FetchedDocument, ResearchTools, SearchHit

T = TypeVar("T")


@dataclass(frozen=True)
class RuntimeToolPolicy:
    max_search_calls: int
    max_fetch_calls: int
    max_runtime_seconds: float
    search_timeout_seconds: float
    fetch_timeout_seconds: float
    retry_max_attempts: int
    retry_initial_delay_seconds: float
    retry_max_delay_seconds: float
    retry_backoff_multiplier: float
    search_enabled: bool = True
    fetch_enabled: bool = True

    def __post_init__(self) -> None:
        positive = {
            "max_search_calls": self.max_search_calls,
            "max_fetch_calls": self.max_fetch_calls,
            "max_runtime_seconds": self.max_runtime_seconds,
            "search_timeout_seconds": self.search_timeout_seconds,
            "fetch_timeout_seconds": self.fetch_timeout_seconds,
            "retry_max_attempts": self.retry_max_attempts,
        }
        if any(value <= 0 for value in positive.values()):
            raise ValueError("Runtime tool limits and timeouts must be greater than zero")
        if self.retry_initial_delay_seconds < 0 or self.retry_max_delay_seconds < 0:
            raise ValueError("Retry delays cannot be negative")
        if self.retry_backoff_multiplier < 1:
            raise ValueError("Retry backoff multiplier must be at least 1")


@dataclass
class RuntimeToolUsage:
    search_calls: int = 0
    fetch_calls: int = 0
    retries: int = 0
    timeouts: int = 0


@dataclass
class _RuntimeScope:
    policy: RuntimeToolPolicy
    started_at: float
    usage: RuntimeToolUsage


class RuntimeControlledResearchTools:
    """Apply task-scoped call limits, retries, timeouts, and runtime ceilings."""

    def __init__(self, delegate: ResearchTools) -> None:
        self.delegate = delegate
        self._scope: _RuntimeScope | None = None
        self._last_usage = RuntimeToolUsage()

    @contextmanager
    def scope(self, policy: RuntimeToolPolicy) -> Iterator[RuntimeToolUsage]:
        if self._scope is not None:
            raise RuntimeError("A runtime tool scope is already active")
        usage = RuntimeToolUsage()
        self._scope = _RuntimeScope(policy=policy, started_at=monotonic(), usage=usage)
        try:
            yield usage
        finally:
            self._last_usage = RuntimeToolUsage(
                search_calls=usage.search_calls,
                fetch_calls=usage.fetch_calls,
                retries=usage.retries,
                timeouts=usage.timeouts,
            )
            self._scope = None

    @property
    def last_usage(self) -> RuntimeToolUsage:
        return RuntimeToolUsage(
            search_calls=self._last_usage.search_calls,
            fetch_calls=self._last_usage.fetch_calls,
            retries=self._last_usage.retries,
            timeouts=self._last_usage.timeouts,
        )

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        scope = self._require_scope()
        return self._execute(
            scope,
            operation="web_search",
            timeout_seconds=scope.policy.search_timeout_seconds,
            call=lambda: self.delegate.web_search(query, limit=limit),
        )

    def web_fetch(self, url: str) -> FetchedDocument:
        scope = self._require_scope()
        return self._execute(
            scope,
            operation="web_fetch",
            timeout_seconds=scope.policy.fetch_timeout_seconds,
            call=lambda: self.delegate.web_fetch(url),
        )

    def _require_scope(self) -> _RuntimeScope:
        if self._scope is None:
            raise ToolExecutionError(
                "RUNTIME_SCOPE_REQUIRED",
                "Runtime-controlled tools require an active task scope",
                operation="runtime_control",
                retryable=False,
            )
        return self._scope

    def _execute(
        self,
        scope: _RuntimeScope,
        *,
        operation: str,
        timeout_seconds: float,
        call: Callable[[], T],
    ) -> T:
        policy = scope.policy
        delay = policy.retry_initial_delay_seconds
        last_error: Exception | None = None
        for attempt in range(1, policy.retry_max_attempts + 1):
            self._check_runtime(scope)
            self._consume_call(scope, operation)
            try:
                return self._call_with_timeout(call, timeout_seconds)
            except FutureTimeoutError:
                scope.usage.timeouts += 1
                last_error = ToolExecutionError(
                    "TOOL_TIMEOUT",
                    f"{operation} exceeded {timeout_seconds:.3f} seconds",
                    operation=operation,
                    retryable=True,
                )
            except ToolExecutionError as exc:
                last_error = exc
                if not exc.retryable:
                    raise
            except Exception as exc:
                last_error = ToolExecutionError(
                    "RUNTIME_TOOL_ERROR",
                    str(exc) or f"{operation} failed",
                    operation=operation,
                    retryable=True,
                )

            if attempt >= policy.retry_max_attempts:
                break
            scope.usage.retries += 1
            if delay > 0:
                sleep(delay)
            delay = min(policy.retry_max_delay_seconds, delay * policy.retry_backoff_multiplier)

        if isinstance(last_error, Exception):
            raise last_error
        raise ToolExecutionError(
            "RUNTIME_TOOL_ERROR",
            f"{operation} failed without an error record",
            operation=operation,
        )

    @staticmethod
    def _call_with_timeout(call: Callable[[], T], timeout_seconds: float) -> T:
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="k_supervisor_tool")
        future = executor.submit(call)
        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError:
            future.cancel()
            raise
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    @staticmethod
    def _check_runtime(scope: _RuntimeScope) -> None:
        elapsed = monotonic() - scope.started_at
        if elapsed > scope.policy.max_runtime_seconds:
            raise ToolExecutionError(
                "MAX_RUNTIME_EXCEEDED",
                "Configured task runtime limit was exceeded",
                operation="runtime_control",
                retryable=False,
                details={
                    "elapsed_seconds": elapsed,
                    "max_runtime_seconds": scope.policy.max_runtime_seconds,
                },
            )

    @staticmethod
    def _consume_call(scope: _RuntimeScope, operation: str) -> None:
        if operation == "web_search":
            if not scope.policy.search_enabled:
                raise ToolExecutionError(
                    "WEB_SEARCH_DISABLED",
                    "web_search is disabled by the frozen task configuration",
                    operation=operation,
                    retryable=False,
                )
            if scope.usage.search_calls >= scope.policy.max_search_calls:
                raise ToolExecutionError(
                    "MAX_SEARCH_CALLS_EXCEEDED",
                    "Configured web_search call limit was reached",
                    operation=operation,
                    retryable=False,
                )
            scope.usage.search_calls += 1
            return
        if not scope.policy.fetch_enabled:
            raise ToolExecutionError(
                "WEB_FETCH_DISABLED",
                "web_fetch is disabled by the frozen task configuration",
                operation=operation,
                retryable=False,
            )
        if scope.usage.fetch_calls >= scope.policy.max_fetch_calls:
            raise ToolExecutionError(
                "MAX_FETCH_CALLS_EXCEEDED",
                "Configured web_fetch call limit was reached",
                operation=operation,
                retryable=False,
            )
        scope.usage.fetch_calls += 1
