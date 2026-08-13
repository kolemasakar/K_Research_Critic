from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

from config import LoadedConfiguration
from config.schema import LoggingSettings, RuntimeSecrets
from models import utc_now


_REDACTED = "[REDACTED]"
_REDACTED_PRIVATE_REASONING = "[REDACTED_PRIVATE_REASONING]"

_PRIVATE_REASONING_KEYS = {
    "chain_of_thought",
    "hidden_reasoning",
    "private_reasoning",
    "reasoning_trace",
    "scratchpad",
}

_SENSITIVE_KEYS = {
    "api_key",
    "authorization",
    "cookie",
    "credential",
    "credentials",
    "database_url",
    "password",
    "passwd",
    "private_key",
    "secret",
    "token",
}

_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_OPENAI_KEY_RE = re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b")
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
_URI_CREDENTIALS_RE = re.compile(
    r"(?i)([a-z][a-z0-9+.-]*://)([^/\s:@]+):([^@\s/]+)@"
)
_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)(\b(?:[\w-]*api[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token|"
    r"password|passwd|secret|authorization|database[_-]?url|connection[_-]?string)\b\s*[:=]\s*)"
    r"([^\s,;]+)"
)

_LEVEL_ORDER = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


@dataclass(frozen=True)
class OperationalLogContext:
    """Stable identifiers attached to structured operational events."""

    task_id: str | None = None
    workflow_run_id: str | None = None
    run_id: str | None = None
    agent_id: str | None = None
    request_id: str | None = None


class SensitiveDataRedactor:
    """Recursively redact configured secrets, secret-like fields, and private reasoning."""

    def __init__(self, secret_values: Iterable[str] = ()) -> None:
        values = {value for value in (str(item).strip() for item in secret_values) if value}
        self._secret_values = tuple(sorted(values, key=len, reverse=True))

    def redact(self, value: Any, *, key: str | None = None) -> Any:
        if key is not None:
            normalized_key = self._normalize_key(key)
            if normalized_key in _PRIVATE_REASONING_KEYS:
                return _REDACTED_PRIVATE_REASONING
            if self._is_sensitive_key(normalized_key):
                return _REDACTED

        if isinstance(value, Mapping):
            return {
                str(item_key): self.redact(item_value, key=str(item_key))
                for item_key, item_value in value.items()
            }
        if isinstance(value, (list, tuple, set, frozenset)):
            return [self.redact(item) for item in value]
        if isinstance(value, str):
            return self._redact_text(value)
        return value

    def _redact_text(self, text: str) -> str:
        result = text
        for secret in self._secret_values:
            result = result.replace(secret, _REDACTED)
        result = _BEARER_RE.sub("Bearer [REDACTED]", result)
        result = _OPENAI_KEY_RE.sub(_REDACTED, result)
        result = _JWT_RE.sub(_REDACTED, result)
        result = _URI_CREDENTIALS_RE.sub(r"\1[REDACTED]@", result)
        result = _SECRET_ASSIGNMENT_RE.sub(r"\1[REDACTED]", result)
        return result

    @staticmethod
    def _normalize_key(key: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", key.casefold()).strip("_")

    @staticmethod
    def _is_sensitive_key(normalized_key: str) -> bool:
        if normalized_key in _SENSITIVE_KEYS:
            return True
        return normalized_key.endswith(
            (
                "_api_key",
                "_access_token",
                "_refresh_token",
                "_auth_token",
                "_password",
                "_private_key",
                "_secret",
            )
        )


class OperationalLogger:
    """JSONL operational logger for the optional standalone/API runtime."""

    FILE_NAME = "k_supervisor.jsonl"

    def __init__(
        self,
        settings: LoggingSettings,
        *,
        secrets: RuntimeSecrets | None = None,
    ) -> None:
        self.settings = settings
        self.redactor = SensitiveDataRedactor(self._secret_values(secrets))
        self._lock = Lock()
        self._file_path = Path(settings.directory) / self.FILE_NAME
        if settings.file_enabled:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def file_path(self) -> Path:
        return self._file_path

    def debug(
        self,
        event: str,
        *,
        message: str = "",
        context: OperationalLogContext | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.log("DEBUG", event, message=message, context=context, details=details)

    def info(
        self,
        event: str,
        *,
        message: str = "",
        context: OperationalLogContext | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.log("INFO", event, message=message, context=context, details=details)

    def warning(
        self,
        event: str,
        *,
        message: str = "",
        context: OperationalLogContext | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.log("WARNING", event, message=message, context=context, details=details)

    def error(
        self,
        event: str,
        *,
        message: str = "",
        context: OperationalLogContext | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.log("ERROR", event, message=message, context=context, details=details)

    def log(
        self,
        level: str,
        event: str,
        *,
        message: str = "",
        context: OperationalLogContext | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        normalized_level = level.upper().strip()
        if normalized_level not in _LEVEL_ORDER:
            raise ValueError(f"Unsupported log level: {level}")
        if not event.strip():
            raise ValueError("Operational log event name cannot be empty")
        if _LEVEL_ORDER[normalized_level] < _LEVEL_ORDER[self.settings.level]:
            return

        context = context or OperationalLogContext()
        record: dict[str, Any] = {
            "timestamp": utc_now().isoformat(),
            "level": normalized_level,
            "event": event.strip(),
        }
        if message:
            record["message"] = message
        if self.settings.include_task_id and context.task_id:
            record["task_id"] = context.task_id
        if context.workflow_run_id:
            record["workflow_run_id"] = context.workflow_run_id
        if self.settings.include_run_id and context.run_id:
            record["run_id"] = context.run_id
        if context.agent_id:
            record["agent_id"] = context.agent_id
        if context.request_id:
            record["request_id"] = context.request_id
        if details:
            record["details"] = dict(details)

        sanitized = self.redactor.redact(record)
        line = json.dumps(
            sanitized,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        )
        with self._lock:
            if self.settings.file_enabled:
                with self._file_path.open("a", encoding="utf-8", newline="\n") as handle:
                    handle.write(line + "\n")
            if self.settings.console_enabled:
                print(line, file=sys.stderr)

    @staticmethod
    def _secret_values(secrets: RuntimeSecrets | None) -> tuple[str, ...]:
        if secrets is None:
            return ()
        values: list[str] = []
        for name in ("openai_api_key", "search_api_key", "database_url"):
            secret = getattr(secrets, name)
            if secret is not None:
                value = secret.get_secret_value().strip()
                if value:
                    values.append(value)
        return tuple(values)


def build_operational_logger(configuration: LoadedConfiguration) -> OperationalLogger:
    """Build a standalone logger from validated configuration without exposing secrets."""

    return OperationalLogger(
        configuration.settings.logging,
        secrets=configuration.secrets,
    )
