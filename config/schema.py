from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class FrozenSettingsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class RuntimeSettings(FrozenSettingsModel):
    timezone: str = "UTC"
    debug: bool = False


class WorkflowSettings(FrozenSettingsModel):
    max_iterations: int = Field(ge=1)
    allow_completed_with_limitations: bool = True
    require_profile_approval: bool = True
    freeze_task_configuration: bool = True
    freeze_critic_profile: bool = True


class AgentToggle(FrozenSettingsModel):
    enabled: bool = True


class AgentsSettings(FrozenSettingsModel):
    research_agent: AgentToggle
    critic_agent: AgentToggle
    report_generator: AgentToggle


class ModelRoleSettings(FrozenSettingsModel):
    provider: str | None = None
    model: str | None = None
    reasoning_level: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_output_tokens: int | None = Field(default=None, ge=1)
    timeout_seconds: int | None = Field(default=None, ge=1)


class ModelsSettings(FrozenSettingsModel):
    supervisor: ModelRoleSettings
    domain_resolver: ModelRoleSettings
    research_agent: ModelRoleSettings
    critic_agent: ModelRoleSettings
    report_generator: ModelRoleSettings


class ResolverSettings(FrozenSettingsModel):
    mode: Literal["rules", "semantic", "hybrid"] = "hybrid"
    semantic_enabled: bool = False
    minimum_semantic_confidence: float = Field(default=0.70, ge=0.0, le=1.0)
    require_agreement_for_high_risk: bool = True
    fallback_to_rules: bool = True


class WebToolSettings(FrozenSettingsModel):
    enabled: bool = True
    timeout_seconds: int = Field(ge=1)


class ToggleSettings(FrozenSettingsModel):
    enabled: bool = True


class ToolsSettings(FrozenSettingsModel):
    web_search: WebToolSettings
    web_fetch: WebToolSettings
    source_validator: ToggleSettings
    citation_manager: ToggleSettings


class ResearchSettings(FrozenSettingsModel):
    max_queries: int = Field(ge=1)
    max_sources: int = Field(ge=1)
    max_sources_per_query: int = Field(ge=1)
    prefer_primary_sources: bool = True
    enable_cross_source_comparison: bool = True
    capture_publication_date: bool = True
    capture_access_time: bool = True
    deduplicate_sources: bool = True


class CriticSettings(FrozenSettingsModel):
    max_verification_queries: int = Field(ge=1)
    require_independent_search: bool = True
    require_claim_level_review: bool = True
    default_minimum_cross_checks: int = Field(ge=0)
    default_confidence_threshold: float = Field(ge=0.0, le=1.0)
    stop_on_critical_issue: bool = False


class ReportsSettings(FrozenSettingsModel):
    output_directory: str
    final_report_suffix: str
    review_protocol_suffix: str


class PersistenceSettings(FrozenSettingsModel):
    backend: Literal["sqlite"]
    path: str
    schema_version: str


class LoggingSettings(FrozenSettingsModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    directory: str
    console_enabled: bool = True
    file_enabled: bool = True
    include_task_id: bool = True
    include_run_id: bool = True
    redact_secrets: bool = True


class RetrySettings(FrozenSettingsModel):
    max_attempts: int = Field(ge=1)
    initial_delay_seconds: float = Field(ge=0.0)
    max_delay_seconds: float = Field(ge=0.0)
    backoff_multiplier: float = Field(ge=1.0)

    @model_validator(mode="after")
    def validate_delay_order(self) -> "RetrySettings":
        if self.max_delay_seconds < self.initial_delay_seconds:
            raise ValueError("max_delay_seconds cannot be lower than initial_delay_seconds")
        return self


class LimitsSettings(FrozenSettingsModel):
    max_agent_runs: int = Field(ge=1)
    max_search_calls: int = Field(ge=1)
    max_fetch_calls: int = Field(ge=1)
    max_sources: int = Field(ge=1)
    max_runtime_seconds: int = Field(ge=1)
    max_output_size_bytes: int = Field(ge=1)


class AppSettings(FrozenSettingsModel):
    schema_version: str
    environment: Literal["development", "test", "production"]
    runtime: RuntimeSettings
    workflow: WorkflowSettings
    agents: AgentsSettings
    models: ModelsSettings
    resolver: ResolverSettings
    tools: ToolsSettings
    research: ResearchSettings
    critic: CriticSettings
    reports: ReportsSettings
    persistence: PersistenceSettings
    logging: LoggingSettings
    retry: RetrySettings
    limits: LimitsSettings

    @model_validator(mode="after")
    def validate_system_invariants(self) -> "AppSettings":
        if not self.workflow.require_profile_approval:
            raise ValueError("require_profile_approval is a system invariant and must remain true")
        if not self.workflow.freeze_task_configuration:
            raise ValueError("freeze_task_configuration is a system invariant and must remain true")
        if not self.workflow.freeze_critic_profile:
            raise ValueError("freeze_critic_profile is a system invariant and must remain true")
        if self.research.max_sources > self.limits.max_sources:
            raise ValueError("research.max_sources cannot exceed limits.max_sources")
        if self.resolver.semantic_enabled:
            role = self.models.domain_resolver
            if not role.provider or not role.model:
                raise ValueError(
                    "semantic resolver requires models.domain_resolver.provider and model"
                )
        return self


class RuntimeSecrets(FrozenSettingsModel):
    openai_api_key: SecretStr | None = None
    search_api_key: SecretStr | None = None
    database_url: SecretStr | None = None
