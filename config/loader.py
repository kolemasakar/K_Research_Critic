from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml
from dotenv import dotenv_values
from pydantic import SecretStr, ValidationError

from .schema import AppSettings, RuntimeSecrets


class ConfigurationError(RuntimeError):
    """Raised when tracked or environment configuration cannot be validated."""


@dataclass(frozen=True)
class LoadedConfiguration:
    settings: AppSettings
    secrets: RuntimeSecrets
    settings_path: Path
    env_path: Path | None

    @property
    def fingerprint(self) -> str:
        payload = self.settings.model_dump_json()
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_configuration(
    settings_path: str | Path = "config/settings.yaml",
    *,
    env_path: str | Path | None = ".env",
    environ: Mapping[str, str] | None = None,
) -> LoadedConfiguration:
    path = Path(settings_path)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigurationError(f"Cannot read settings file {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Invalid YAML in settings file {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigurationError("Settings root must be a YAML mapping")

    env_file_path = Path(env_path) if env_path is not None else None
    environment_values: dict[str, str] = {}
    if env_file_path is not None and env_file_path.exists():
        parsed = dotenv_values(env_file_path)
        environment_values.update(
            {key: value for key, value in parsed.items() if key and value is not None}
        )

    runtime_environment = dict(os.environ if environ is None else environ)
    environment_values.update(runtime_environment)

    selected_environment = environment_values.get("K_SUPERVISOR_ENV")
    if selected_environment:
        raw = dict(raw)
        raw["environment"] = selected_environment.strip()

    try:
        settings = AppSettings.model_validate(raw)
        secrets = RuntimeSecrets(
            openai_api_key=_secret_or_none(environment_values.get("OPENAI_API_KEY")),
            search_api_key=_secret_or_none(environment_values.get("SEARCH_API_KEY")),
            database_url=_secret_or_none(environment_values.get("DATABASE_URL")),
        )
    except ValidationError as exc:
        raise ConfigurationError(f"Configuration validation failed: {exc}") from exc

    return LoadedConfiguration(
        settings=settings,
        secrets=secrets,
        settings_path=path,
        env_path=env_file_path if env_file_path is not None and env_file_path.exists() else None,
    )


def _secret_or_none(value: str | None) -> SecretStr | None:
    if value is None:
        return None
    stripped = value.strip()
    return SecretStr(stripped) if stripped else None
