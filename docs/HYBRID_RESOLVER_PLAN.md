# HYBRID_RESOLVER_PLAN
План після-MVP переходу від детермінованого DomainResolver до гібридного визначення домену.

Version: 1.0
Status: PLANNED

## 1. Purpose

This document schedules the HybridResolver enhancement after Phase 9 End-to-End MVP.

The enhancement is non-blocking for the initial MVP. The current deterministic DomainResolver remains the active implementation until the end-to-end workflow is stable.

## 2. Target Sequence

```text
Phase 9 - End-to-End MVP
        |
        v
HybridResolver enhancement
        |
        v
Phase 10+ post-MVP platform work
```

## 3. Target Architecture

```text
DomainResolver interface
        |
        +-- RuleBasedResolver
        +-- LLMSemanticResolver
        +-- HybridResolver
```

HybridResolver will combine deterministic evidence with semantic classification while preserving the existing DomainAssessment contract.

## 4. Components

### 4.1 RuleBasedResolver

The existing deterministic Phase 3 resolver will be extracted or adapted as the rule-based component.

Responsibilities:

- keyword and rule matching;
- deterministic risk floor;
- known domain hints;
- deterministic fallback;
- low-cost first-pass classification.

### 4.2 LLMSemanticResolver

A provider-neutral semantic resolver will analyze task meaning rather than only keyword matches.

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

The semantic resolver must return structured data validated before use.

### 4.3 HybridResolver

HybridResolver will combine both results.

Responsibilities:

- compare rule-based and semantic classifications;
- preserve deterministic risk floors for high-risk matches;
- resolve compatible domain results;
- detect material conflicts;
- calculate or normalize classification confidence;
- fall back to RuleBasedResolver when semantic resolution fails;
- record uncertainty when the two methods materially disagree.

## 5. Contract Boundary

The external contract remains:

```text
Task
  -> DomainResolver
  -> DomainAssessment
  -> CriticProfile
  -> USER APPROVAL
```

HybridResolver must not change the mandatory CriticProfile approval boundary.

No silent change to an approved CriticProfile is allowed.

## 6. Conflict Policy

Initial policy:

- deterministic high-risk classification may raise but not silently lower semantic risk;
- semantic analysis may add secondary domains and subdomain context;
- material disagreement must be represented in DomainAssessment.uncertainties;
- unresolved high-impact disagreement should be surfaced to Supervisor for user review;
- semantic failure must not block classification when the rule-based resolver can produce a valid result.

## 7. Configuration

Planned settings:

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

## 8. Testing

Required tests:

- rule and semantic agreement;
- compatible multi-domain merge;
- semantic-only domain discovery;
- deterministic high-risk floor preservation;
- material disagreement handling;
- malformed semantic output;
- semantic provider failure;
- deterministic fallback;
- unchanged DomainAssessment schema;
- unchanged CriticProfile user approval gate.

## 9. Exit Criteria

HybridResolver is complete when:

- it is provider-neutral;
- it preserves deterministic fallback;
- semantic output is schema validated;
- risk cannot be silently reduced by semantic classification;
- multi-domain classification is supported;
- material conflicts are auditable;
- existing Phase 3 approval behavior remains unchanged;
- the complete CI suite passes.

## 10. Scheduling Decision

Implementation is scheduled after Phase 9 End-to-End MVP.

Reason:

- the current RuleBasedResolver satisfies the MVP domain-resolution contract;
- ResearchAgent, Tools Layer, CriticAgent, autonomous iteration, report generation, and end-to-end validation provide higher immediate MVP value;
- the semantic resolver can later reuse the mature model/configuration and testing boundaries without expanding current MVP scope.
