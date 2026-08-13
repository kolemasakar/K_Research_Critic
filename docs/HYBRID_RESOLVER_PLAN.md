# HYBRID_RESOLVER_PLAN
План після-MVP переходу від детермінованого DomainResolver до гібридного визначення домену.

Version: 1.0
Status: COMPLETE

## 1. Purpose

This document defines and records the HybridResolver enhancement implemented after Phase 9 End-to-End MVP.

The enhancement preserves the stable DomainAssessment and CriticProfile approval contracts while adding optional provider-neutral semantic classification on top of the deterministic Phase 3 resolver.

## 2. Target Sequence

```text
Phase 9 - End-to-End MVP             COMPLETE
        |
        v
HybridResolver enhancement           COMPLETE
        |
        v
Phase 10+ post-MVP platform work
```

## 3. Target Architecture

```text
DomainResolverProtocol
        |
        +-- RuleBasedResolver
        +-- LLMSemanticResolver
        +-- HybridResolver
```

HybridResolver combines deterministic evidence with semantic classification while preserving the existing DomainAssessment contract.

## 4. Components

### 4.1 RuleBasedResolver

The existing deterministic Phase 3 DomainResolver remains available and is exported as RuleBasedResolver for the hybrid architecture.

Responsibilities:

- keyword and rule matching;
- deterministic risk floor;
- known domain hints;
- deterministic fallback;
- low-cost first-pass classification.

### 4.2 LLMSemanticResolver

A provider-neutral semantic resolver validates structured semantic output before it can participate in the hybrid merge.

Required output:

```text
primary_domain
secondary_domains
task_type
risk_level
identified_standards
recommended_source_types
recommended_evaluation_criteria
uncertainties
confidence
```

The implementation accepts any provider satisfying SemanticDomainProvider. No vendor SDK is embedded in Supervisor.

### 4.3 HybridResolver

HybridResolver combines both results.

Responsibilities:

- compare rule-based and semantic classifications;
- preserve deterministic risk floors for matched rule domains;
- resolve compatible multi-domain results;
- detect material conflicts;
- enforce minimum semantic confidence;
- fall back to RuleBasedResolver when semantic resolution fails or confidence is insufficient;
- record uncertainty when the two methods materially disagree;
- expose HybridResolutionAudit without changing DomainAssessment.

## 5. Contract Boundary

The external contract remains:

```text
Task
  -> DomainResolverProtocol
  -> DomainAssessment
  -> CriticProfile
  -> USER APPROVAL
```

HybridResolver does not change the mandatory CriticProfile approval boundary.

No silent change to an approved CriticProfile is allowed.

## 6. Conflict Policy

Implemented policy:

- deterministic matched-domain risk may raise but cannot be silently reduced by semantic risk;
- semantic analysis may add secondary domains and additional source, standard, and evaluation requirements;
- semantic-only discovery can replace the generic general_research fallback;
- material disagreement is represented in DomainAssessment.uncertainties;
- high-risk disagreement explicitly states that user review is required at the existing CriticProfile approval boundary;
- semantic failure does not block classification when deterministic fallback is enabled;
- fallback can be disabled to fail closed when required.

## 7. Configuration

Tracked settings now include:

```text
models.domain_resolver.provider
models.domain_resolver.model
resolver.mode = hybrid
resolver.semantic_enabled
resolver.minimum_semantic_confidence
resolver.require_agreement_for_high_risk
resolver.fallback_to_rules
```

Secrets remain outside tracked configuration.

The current application supports resolver injection directly. Central provider/model factory wiring from configuration remains part of the later configuration-control work rather than being hard-coded into the resolver.

## 8. Testing

Implemented tests cover:

- rule and semantic agreement;
- compatible multi-domain merge;
- semantic-only domain discovery;
- deterministic high-risk floor preservation;
- material disagreement handling;
- malformed semantic output;
- semantic provider failure;
- low-confidence fallback;
- configurable fail-closed behavior;
- unchanged DomainAssessment schema;
- RuleBasedResolver compatibility;
- unchanged CriticProfile user approval gate.

## 9. Exit Criteria

HybridResolver is complete because:

- it is provider-neutral;
- it preserves deterministic fallback;
- semantic output is schema validated;
- risk cannot be silently reduced for deterministic matched domains;
- multi-domain classification is supported;
- material conflicts are auditable;
- existing Phase 3 approval behavior remains unchanged;
- the complete CI suite passes.

## 10. Implementation Result

Implementation commit:

```text
ec25b7443ffda8e1d64f82e2f7d764b9051b6f42
```

Validation result:

```text
GitHub Actions run 31657407690
111 tests passed
```

ProfileWorkflow now uses HybridResolver as its default resolver boundary. When no semantic provider is configured, HybridResolver returns the deterministic DomainResolver result unchanged. A semantic provider can be injected through LLMSemanticResolver without modifying ProfileWorkflow or the CriticProfile approval contract.

Semantic confidence and merge diagnostics are intentionally kept outside DomainAssessment through HybridResolutionAudit so the stable DomainAssessment schema remains unchanged.

## 11. Scheduling Decision

The scheduled post-MVP enhancement is complete. The next roadmap phase is Phase 10 - Persistence and Audit.
