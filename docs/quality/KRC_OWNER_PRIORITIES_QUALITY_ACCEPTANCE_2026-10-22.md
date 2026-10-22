# KRC Owner Task Priorities and Quality Acceptance Plan — 2026-10-22

Status: OWNER APPROVED PRIORITIES; execution of tasks 1-3 authorized, production/MEDIA/publication changes NOT authorized.

## Exact mapping to numbered debt list in status №65
ACTIVE FINISH: 1 full CriticProfile -> Research -> Critic -> Report cycle acceptance; 2 systematic source-origin independence checks; 3 confidence, contradictions, coverage and unsupported-claim standardization.
PAUSED: 4 public media access; 5 media E2E; 7 public security hardening; 8 external HTTPS MCP; 10 publication legal URLs; 11 With MCP submission; 12 independent Plus-user installation.
EXPLANATION REQUESTED, NO AUTOMATIC IMPLEMENTATION AUTHORIZATION: 6 deployed-code Git SHA/runtime attestation; 9 isolated negative tests/fault injection.
Maintain FREE_ONLY and separate Research MCP/Cobalt and private NO_MCP 0.19.8 unchanged.

## What a systematic quality test means
A frozen test corpus, explicitly sourced oracle/expected verdict for each claim, replay against the SAME instructions/model version and available sources, per-case deterministic checks and human cross-review.
Coverage matrix: true, false, partly true, misleading/quote out of context, unsupported, unverifiable, opinion; dependent syndication masquerading as independent evidence; time-sensitive/outdated primary data; contradictory sources; high-risk category.
Per-case acceptance:
1. profile gate really stops before approval, explicit approval recorded;
2. independent evidence origins are traceable and counted at claim level;
3. distinguish fact, inference and opinion, no fabricated citations;
4. abstain/SHORTFALL when cross-check floor unmet;
5. critic catches flaws and requires revision; score not treated as proven calibration;
6. final report aligns each material claim to evidence, exceptions and limitations.
Measure false verification rate, missing-source claims, duplicated-source misclassification, citation traceability, revision efficacy and profile-gate bypass. Never claim empirical rates until measured. Use offline reference texts where possible; current news tests require frozen snapshots and timestamp.

## Proposed implementation plan tasks 1-3
P1A: inventory source of truth in private plugin/Core Skill and create test cases + answer rubric.
P1B: offline deterministic validator/unit tests without production writes, then same-case prompt evaluations in private plugin when accessible.
P2: identify provenance using canonical publisher/source origin, source chain/republisher detection, DOI/document/original public statement identity, domain-level caution, source publication/access dates; URL diversity is not true independence. Unknown => cannot count as independent.
P3: traceable claim ledger with VERIFIED/PARTIAL/UNSUPPORTED/etc, evidence strength, conflicts, confidence calibration and mandatory limitations; score = reviewer assessment, not statistical probability without calibration.
Acceptance only after tests actually executed and evidence recorded. Skills behavioral guarantees cannot be verified from static source alone.

## Server current use
RDC krc-cobalt observed systemd research MCP service active pid 82373 no restarts, localhost:9013 LISTEN; separate Cobalt :9000 LISTEN. Research MCP is NOT referenced by the personal NO_MCP 0.19.8 plugin and has no public endpoint in this configuration, so normal NO_MCP chat doesn't use it. It consumes a small ongoing server footprint and serves localhost-protocol checks/tests only when explicitly invoked. Cobalt MEDIA remains separate, with provider work not established from listener status.

## Explanation requested
Task 6: Git commit/release SHA versus deployed server.py SHA256 and loaded interpreter code provenance; no .git checkout on server. This is a reproducibility/audit problem rather than evidence of compromise. Remedy: version-tagged immutable artifact manifest, SHA, owner controlled restart, compare installed/running service, rollback record. Avoid forcing intrusive process inspection.
Task 9: isolated negative tests (bad schema, duplicate evidence, missing evidence, malicious prompt-injection source text, invalid authorization, 16MiB overlimit upload, queue full, interrupted jobs, restart recovery, 10h TTL, rate limits and disk guard); fault injection on isolated test state/service only. Not a reason to send destructive tests against production.
