# TEST_PLAN
План перевірки функціональності, надійності, якості та відтворюваності K_Supervisor.

Version: 1.1
Status: ACTIVE

## 1. Purpose

This document defines the canonical test strategy for K_Supervisor.

The test program verifies that the system follows the architecture and contracts, preserves the mandatory CriticProfile approval boundary, runs the autonomous ResearchAgent-CriticAgent loop only after approval, persists an auditable task history, and produces stable final artifacts without exposing private reasoning.

## 2. Test Objectives

The suite must prove that K_Supervisor can:

- accept a valid user task;
- resolve task domains;
- generate a valid draft CriticProfile;
- block autonomous work before explicit approval;
- freeze the approved profile and effective task configuration;
- launch ResearchAgent and CriticAgent with valid structured context;
- route PASS and REVISE decisions correctly;
- enforce configured iterations, resource limits, timeouts, and retries;
- handle recoverable and unrecoverable failures explicitly;
- persist and reconstruct task audit information;
- produce FINAL_REPORT and REVIEW_PROTOCOL artifacts;
- preserve traceability through task_id, workflow/run identifiers, transitions, evidence, reviews, metrics, and artifacts.

## 3. Test Levels

### 3.1 Unit and Contract Tests

Unit and contract tests cover isolated deterministic behavior and canonical data structures.

Primary targets include:

```text
DomainResolver and HybridResolver
ProfileManager
StateMachine
AgentRegistry
configuration loader and schema
TaskConfigurationSnapshot
identifier generation
Claim and Source contracts
CriticReview
Metrics and usage records
logging and redaction
artifact naming and serialization
GPT Store checkpoint contracts
```

Invalid contracts must fail explicitly for missing fields, invalid identifiers or states, malformed values, and incompatible schema assumptions.

### 3.2 Integration and Workflow Tests

Integration tests cover component boundaries:

```text
Supervisor -> DomainResolver
Supervisor -> ProfileManager
Supervisor -> ResearchAgent
Supervisor -> CriticAgent
ResearchAgent -> Tools Layer
CriticAgent -> Tools Layer
Supervisor -> ReportGenerator
Supervisor -> Persistence Layer
Configuration -> runtime controls
Provider factory -> optional provider adapters
```

The primary workflow success path is:

```text
NEW
-> PROFILE_GENERATING
-> PROFILE_REVIEW_REQUIRED
-> PROFILE_APPROVED
-> RESEARCHING
-> DRAFT_READY
-> REVIEWING
-> APPROVED
-> FINALIZING
-> FINALIZED
```

Revision and exceptional paths include REVISE, FAILED, MAX_ITERATIONS_REACHED, and COMPLETED_WITH_LIMITATIONS.

### 3.3 End-to-End Tests

End-to-end tests validate the complete user-visible workflow from task preparation through final artifacts. Deterministic offline providers are preferred in repository CI. Live provider/UI checks are kept separate when they cannot be reproduced honestly in CI.

## 4. Critical Approval and Profile Tests

Required behavior:

- draft profile generation produces reviewable criteria, source requirements, and confidence settings;
- research is blocked before explicit approval;
- approval creates an auditable UserApproval record;
- the active profile is frozen for execution;
- CriticAgent cannot silently modify approved criteria;
- a material amendment requires another explicit review/approval boundary;
- recovery preserves the approved profile state exactly.

## 5. Domain Resolution Tests

Coverage includes single-domain, multi-domain, ambiguous, generic, and unknown-domain tasks.

Reference domains include:

```text
literary_analysis
medicine
geodesy
construction
military
finance
law
software_engineering
```

Hybrid resolution tests must also cover deterministic fallback, semantic-provider errors, confidence floors, risk floors, and material disagreement audit.

## 6. Research, Evidence, and Critic Tests

ResearchAgent tests verify task decomposition, query generation, source collection, duplicate handling, claim extraction, claim-source links, uncertainty capture, structured revision handling, and output contract compliance.

Evidence tests verify stable IDs, valid source references, contradictory evidence preservation, source reliability metadata, freshness metadata where relevant, and claim verification state changes across iterations.

CriticAgent tests verify approved-profile use, independent verification behavior, source quality assessment, freshness rules, unsupported-claim detection, contradictions, missing topics, evidence-conclusion consistency, PASS/REVISE output, reliability scores, and no silent profile modification.

ResearchAgent must not self-approve the final reliability of its own result.

## 7. Revision Loop and State Machine Tests

The suite covers:

```text
PASS on first review
one revision before PASS
multiple revisions
max_iterations reached
completed with limitations
agent failure
invalid transitions
recovery at safe checkpoints
```

Every valid transition requires positive coverage and prohibited transitions require negative coverage. No failure may silently disappear from the audit trail.

## 8. Configuration and Runtime-Control Tests

Configuration tests verify:

- YAML parsing and validation;
- environment precedence;
- secret separation;
- immutable effective task snapshots;
- exact snapshot persistence/recovery;
- runtime override inclusion in the effective snapshot;
- max_iterations and tool/resource budgets;
- timeout and retry behavior;
- provider/model selection isolation from agent business logic;
- Store-first distribution invariants;
- redaction cannot be disabled by normal configuration.

## 9. Persistence, Metrics, and Audit Tests

For completed and failed tasks, tests should be able to reconstruct:

```text
user task
approved CriticProfile
configuration snapshot
workflow states and transitions
agent runs
research iterations
critic reviews
claims and sources
usage and quality metrics
final artifacts
errors and warnings
```

Persistence tests require exact logical round-trip behavior, idempotent stable-ID writes, safe schema handling, and conservative restart recovery.

The audit trail must not require private chain-of-thought.

## 10. Failure, Idempotency, and Security Tests

Failure coverage includes provider/tool timeout, fetch/search failure, unavailable source, malformed agent output, schema failure, provider exception, persistence failure, artifact write failure, duplicate requests, and iteration/resource limits.

Security checks verify that:

- API keys are not tracked;
- `.env` remains ignored;
- RuntimeSecrets do not leak into snapshots, logs, errors, or artifacts;
- secret-like and private-reasoning fields are redacted before persistence/logging;
- test fixtures contain only synthetic values.

Idempotency tests verify repeated stable operations do not create conflicting logical work or corrupt task state.

## 11. Artifact Tests

Required artifacts:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Tests verify UTF-8 output, canonical filenames, correct task_id, evidence/limitations, iteration/review history, consistent final status, and explicit exclusion of hidden chain-of-thought/private model reasoning from REVIEW_PROTOCOL.

## 12. Determinism and Reproducibility

Testing separates structural reproducibility from content reproducibility.

Structural reproducibility requires stable control rules, contracts, state boundaries, evidence rules, and artifact behavior for equivalent inputs.

Live LLM/web content may vary and therefore must not be confused with deterministic repository regression fixtures.

## 13. Phase 12 Reference Benchmark

Phase 12 adds a deterministic offline benchmark:

```text
examples/reference_benchmark.json
tests/test_reference_benchmark.py
```

The fixture contains four reference tasks:

```text
REF_LITERARY_001  -> literary_analysis
REF_SOFTWARE_001  -> software_engineering
REF_MEDICINE_001  -> medicine
REF_GEODESY_001   -> geodesy
```

Each task uses synthetic local evidence and validates:

- expected domain resolution;
- explicit CriticProfile approval;
- autonomous completion to FINALIZED;
- expected iteration count;
- minimum source and claim presence;
- task-specific reliability floor;
- approved-profile confidence threshold;
- Critic decision PASS;
- absence of critical issues, unsupported claims, contradictions, and unresolved claims;
- FINAL_REPORT and REVIEW_PROTOCOL generation;
- task_id traceability;
- review-protocol audit note excluding hidden chain-of-thought/private reasoning.

The benchmark must remain offline and cost-free in CI. It is a regression baseline, not a substitute for real-world subject-matter validation.

Run only the benchmark with:

```text
python -m pytest -q tests/test_reference_benchmark.py
```

## 14. CI and Quality Gates

Every push and pull request runs the full deterministic suite on:

```text
Python 3.13
Python 3.14
```

The quality job also runs:

```text
python -m pip check
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
python -m pytest --cov --cov-report=term-missing --cov-fail-under=70
```

Provider-dependent, paid, or ChatGPT UI/account checks must not be represented as automated PASS conditions unless the CI environment can actually execute and verify them.

## 15. Validated Phase 12 Baseline

Validated implementation baseline:

```text
Python 3.13 full suite: 169 passed
Python 3.14 full suite: PASS
Quality gates: PASS
Dependency integrity: PASS
Ruff correctness gate: PASS
Mypy typed boundary gate: PASS
Repository policy validator: PASS
GPT Store package validator: PASS
Total coverage: 85 percent
Blocking coverage floor: 70 percent
Reference benchmark cases: 4
```

## 16. Regression Policy

Every confirmed defect should gain a regression test when technically practical.

Changes to ARCHITECTURE.md, AGENT_INTERFACE.md, DATA_MODELS.md, RESEARCH_WORKFLOW.md, CONFIGURATION.md, persistence contracts, runtime controls, or Store package invariants require review of affected tests.

The quality gate scope is a ratchet. It may expand or become stricter as coverage and typing improve; it should not be weakened merely to make CI green.

## 17. Test Data Rules

Test data must:

- avoid real secrets and unnecessary personal data;
- identify synthetic fixtures clearly;
- preserve stable IDs where deterministic fixtures require them;
- separate valid and invalid cases;
- support provider-independent execution through deterministic local providers, mocks, or stubs.

## 18. Exit Rule

A development phase may be marked complete only when:

- its critical automated tests exist;
- relevant regression and boundary tests pass;
- known limitations are documented;
- no unresolved critical defect is hidden by retries, skips, blanket ignores, or manual intervention;
- required artifacts and audit behavior remain stable.

Phase 12 satisfies this rule with the reference benchmark, cross-version pytest matrix, blocking quality gates, and documented manual boundaries for ChatGPT publication/account validation.
