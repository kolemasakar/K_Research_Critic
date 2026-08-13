from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from models import ProviderUsageRecord, Task

from .openai_semantic import OpenAISemanticDomainProvider


class MeteredOpenAISemanticDomainProvider(OpenAISemanticDomainProvider):
    """Optional standalone OpenAI adapter wrapper that captures response usage telemetry."""

    def __init__(
        self,
        *,
        input_cost_per_million_tokens: float | None = None,
        output_cost_per_million_tokens: float | None = None,
        **kwargs: Any,
    ) -> None:
        for name, value in (
            ("input_cost_per_million_tokens", input_cost_per_million_tokens),
            ("output_cost_per_million_tokens", output_cost_per_million_tokens),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} cannot be negative")
        super().__init__(**kwargs)
        self.input_cost_per_million_tokens = input_cost_per_million_tokens
        self.output_cost_per_million_tokens = output_cost_per_million_tokens
        self._delegate_transport = self.transport
        self.transport = self._metered_transport
        self._api_calls = 0
        self._last_usage: Mapping[str, Any] = {}
        self._usage_by_task: dict[str, ProviderUsageRecord] = {}

    def resolve(self, task: Task) -> Mapping[str, Any]:
        self._api_calls = 0
        self._last_usage = {}
        try:
            return super().resolve(task)
        finally:
            self._usage_by_task[task.task_id] = self._build_usage(task.task_id)

    def get_usage(self, task_id: str) -> ProviderUsageRecord | None:
        """Return captured telemetry without performing another provider request."""
        return self._usage_by_task.get(task_id)

    def _metered_transport(
        self,
        url: str,
        headers: dict[str, str],
        payload: bytes,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        self._api_calls += 1
        raw = self._delegate_transport(url, headers, payload, timeout_seconds)
        usage = raw.get("usage")
        self._last_usage = usage if isinstance(usage, Mapping) else {}
        return raw

    def _build_usage(self, task_id: str) -> ProviderUsageRecord:
        input_tokens = self._optional_int(self._last_usage.get("input_tokens"))
        output_tokens = self._optional_int(self._last_usage.get("output_tokens"))
        total_tokens = self._optional_int(self._last_usage.get("total_tokens"))
        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens

        estimated_cost_usd: float | None = None
        if (
            input_tokens is not None
            and output_tokens is not None
            and self.input_cost_per_million_tokens is not None
            and self.output_cost_per_million_tokens is not None
        ):
            estimated_cost_usd = round(
                (input_tokens / 1_000_000) * self.input_cost_per_million_tokens
                + (output_tokens / 1_000_000) * self.output_cost_per_million_tokens,
                8,
            )

        return ProviderUsageRecord(
            task_id=task_id,
            component="domain_resolver",
            provider="openai",
            model=self.model,
            api_calls=self._api_calls,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            metadata={"usage_reported": bool(self._last_usage)},
        )

    @staticmethod
    def _optional_int(value: Any) -> int | None:
        if isinstance(value, bool):
            return None
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None
        return parsed if parsed >= 0 else None
