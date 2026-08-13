from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from time import sleep
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from models import Task


Transport = Callable[[str, dict[str, str], bytes, float], Mapping[str, Any]]


class OpenAISemanticDomainProvider:
    """OpenAI Responses API adapter for structured semantic domain classification."""

    ENDPOINT = "https://api.openai.com/v1/responses"

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        timeout_seconds: float = 30.0,
        max_output_tokens: int = 1200,
        reasoning_level: str | None = None,
        temperature: float | None = None,
        max_attempts: int = 3,
        initial_delay_seconds: float = 1.0,
        max_delay_seconds: float = 8.0,
        backoff_multiplier: float = 2.0,
        transport: Transport | None = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("OpenAI semantic provider requires an API key")
        if not model.strip():
            raise ValueError("OpenAI semantic provider requires a model")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be greater than zero")
        if max_attempts <= 0:
            raise ValueError("max_attempts must be greater than zero")
        self.api_key = api_key.strip()
        self.model = model.strip()
        self.timeout_seconds = float(timeout_seconds)
        self.max_output_tokens = int(max_output_tokens)
        self.reasoning_level = reasoning_level
        self.temperature = temperature
        self.max_attempts = int(max_attempts)
        self.initial_delay_seconds = float(initial_delay_seconds)
        self.max_delay_seconds = float(max_delay_seconds)
        self.backoff_multiplier = float(backoff_multiplier)
        self.transport = transport or self._http_transport

    def resolve(self, task: Task) -> Mapping[str, Any]:
        body = self._request_body(task)
        raw = self._request_with_retry(body)
        text = self._extract_output_text(raw)
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"OpenAI semantic response was not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("OpenAI semantic response must decode to an object")
        return parsed

    def _request_body(self, task: Task) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": self.model,
            "store": False,
            "max_output_tokens": self.max_output_tokens,
            "input": [
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Classify the research task semantically. Return only the requested "
                                "structured data. Do not include private reasoning. Treat risk as the "
                                "consequence of a wrong or weakly supported answer, not as sentiment."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                f"User request: {task.user_request}\n"
                                f"Existing task type hint: {task.task_type}\n"
                                "Identify primary/secondary domains, task type, risk, relevant standards, "
                                "source classes, evaluation criteria, uncertainties, and confidence."
                            ),
                        }
                    ],
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "semantic_domain_result",
                    "strict": True,
                    "schema": self._json_schema(),
                }
            },
        }
        if self.reasoning_level:
            body["reasoning"] = {"effort": self.reasoning_level}
        if self.temperature is not None:
            body["temperature"] = self.temperature
        return body

    @staticmethod
    def _json_schema() -> dict[str, Any]:
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "primary_domain": {"type": "string", "minLength": 1},
                "secondary_domains": {"type": "array", "items": {"type": "string"}},
                "task_type": {"type": "string", "minLength": 1},
                "risk_level": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                },
                "identified_standards": {"type": "array", "items": {"type": "string"}},
                "recommended_source_types": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "recommended_evaluation_criteria": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "uncertainties": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            },
            "required": [
                "primary_domain",
                "secondary_domains",
                "task_type",
                "risk_level",
                "identified_standards",
                "recommended_source_types",
                "recommended_evaluation_criteria",
                "uncertainties",
                "confidence",
            ],
        }

    def _request_with_retry(self, body: dict[str, Any]) -> Mapping[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = json.dumps(body).encode("utf-8")
        delay = self.initial_delay_seconds
        last_error: Exception | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self.transport(self.ENDPOINT, headers, payload, self.timeout_seconds)
            except Exception as exc:
                last_error = exc
                retryable = self._retryable(exc)
                if not retryable or attempt >= self.max_attempts:
                    break
                if delay > 0:
                    sleep(delay)
                delay = min(self.max_delay_seconds, delay * self.backoff_multiplier)
        raise RuntimeError(f"OpenAI semantic provider request failed: {last_error}") from last_error

    @staticmethod
    def _retryable(exc: Exception) -> bool:
        if isinstance(exc, HTTPError):
            return exc.code == 429 or 500 <= exc.code <= 599
        if isinstance(exc, URLError):
            return True
        return bool(getattr(exc, "retryable", False))

    @staticmethod
    def _extract_output_text(raw: Mapping[str, Any]) -> str:
        direct = raw.get("output_text")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        output = raw.get("output")
        if isinstance(output, list):
            for item in output:
                if not isinstance(item, Mapping):
                    continue
                content = item.get("content")
                if not isinstance(content, list):
                    continue
                for part in content:
                    if (
                        isinstance(part, Mapping)
                        and part.get("type") == "output_text"
                        and isinstance(part.get("text"), str)
                        and str(part["text"]).strip()
                    ):
                        return str(part["text"]).strip()
        raise RuntimeError("OpenAI semantic response did not contain output text")

    @staticmethod
    def _http_transport(
        url: str,
        headers: dict[str, str],
        payload: bytes,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        request = Request(url, data=payload, headers=headers, method="POST")
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise RuntimeError("OpenAI API response root must be an object")
        return parsed
