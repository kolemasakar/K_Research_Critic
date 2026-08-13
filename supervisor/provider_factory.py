from __future__ import annotations

from config import LoadedConfiguration
from models import DomainAssessment, Task
from providers import OpenAISemanticDomainProvider

from .domain_resolver import DomainResolver
from .hybrid_resolver import (
    DomainResolverProtocol,
    HybridResolver,
    LLMSemanticResolver,
)


class ProviderConfigurationError(RuntimeError):
    """Raised when configured model/provider wiring cannot be constructed safely."""


class SemanticOnlyDomainResolver:
    """Adapt validated semantic results to the stable DomainAssessment contract."""

    def __init__(self, semantic_resolver: LLMSemanticResolver) -> None:
        self.semantic_resolver = semantic_resolver

    def resolve(self, task: Task) -> DomainAssessment:
        semantic = self.semantic_resolver.resolve(task)
        return DomainAssessment(
            task_id=task.task_id,
            primary_domain=semantic.primary_domain,
            secondary_domains=semantic.secondary_domains,
            task_type=semantic.task_type,
            risk_level=semantic.risk_level,
            identified_standards=semantic.identified_standards,
            recommended_source_types=semantic.recommended_source_types,
            recommended_evaluation_criteria=semantic.recommended_evaluation_criteria,
            uncertainties=semantic.uncertainties,
        )


def build_domain_resolver(configuration: LoadedConfiguration) -> DomainResolverProtocol:
    """Build the configured resolver without embedding vendor code in Supervisor workflow logic."""

    settings = configuration.settings
    resolver = settings.resolver
    if resolver.mode == "rules":
        return DomainResolver()

    if not resolver.semantic_enabled:
        if resolver.mode == "semantic":
            raise ProviderConfigurationError(
                "resolver.mode=semantic requires resolver.semantic_enabled=true"
            )
        return HybridResolver(
            minimum_semantic_confidence=resolver.minimum_semantic_confidence,
            require_agreement_for_high_risk=resolver.require_agreement_for_high_risk,
            fallback_to_rules=resolver.fallback_to_rules,
        )

    role = settings.models.domain_resolver
    provider_name = (role.provider or "").strip().casefold()
    if provider_name != "openai":
        raise ProviderConfigurationError(
            f"Unsupported domain_resolver provider: {role.provider!r}; supported: openai"
        )
    if not role.model:
        raise ProviderConfigurationError("OpenAI domain_resolver requires a configured model")
    if configuration.secrets.openai_api_key is None:
        raise ProviderConfigurationError(
            "OpenAI domain_resolver requires OPENAI_API_KEY in the runtime environment"
        )

    retry = settings.retry
    provider = OpenAISemanticDomainProvider(
        api_key=configuration.secrets.openai_api_key.get_secret_value(),
        model=role.model,
        timeout_seconds=float(role.timeout_seconds or 30),
        max_output_tokens=int(role.max_output_tokens or 1200),
        reasoning_level=role.reasoning_level,
        temperature=role.temperature,
        max_attempts=retry.max_attempts,
        initial_delay_seconds=retry.initial_delay_seconds,
        max_delay_seconds=retry.max_delay_seconds,
        backoff_multiplier=retry.backoff_multiplier,
    )
    semantic = LLMSemanticResolver(provider)
    if resolver.mode == "semantic":
        return SemanticOnlyDomainResolver(semantic)
    return HybridResolver(
        semantic_resolver=semantic,
        minimum_semantic_confidence=resolver.minimum_semantic_confidence,
        require_agreement_for_high_risk=resolver.require_agreement_for_high_risk,
        fallback_to_rules=resolver.fallback_to_rules,
    )
