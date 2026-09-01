# K-Research & Critic MEDIA BETA - M3 A/B Complete Owner Decision Checkpoint

Status: CANONICAL_RECOVERY_CHECKPOINT / M3_AB_COMPLETE / OWNER_DECISION_PENDING
Date: 2026-09-01
Release state: RELEASE_HOLD_OWNER_TESTING

## Purpose

Preserve the product-level state after the first controlled provider-consuming prerecorded M3 A/B run completed successfully. This checkpoint supersedes checkpoint 64 for current M3 continuation while preserving checkpoint 64 as the pre-A/B historical state.

## Product Boundary

```text
K-Research & Critic
  public Core: K_Research_Critic/main
  MEDIA BETA product/roadmap authority: K_Research_Critic/agent/video-url-research
  technology/backend evidence: VoiceBridge
```

VoiceBridge validates implementation and A/B evidence. It does not independently authorize KRC release, deployment, merge, or provider cutover.

## Accepted Runtime Boundary

```text
active KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini normal KRC activation: FALSE
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
RELEASE_HOLD_OWNER_TESTING: PRESERVED
```

No normal KRC provider selector, production deployment, Action URL, Neon state, Builder package, or release gate was changed by the M3 A/B run.

## Pre-A/B Evidence

```text
ASSET_SHA256_ACCEPTED: TRUE 3/3
FINAL_REFERENCE_SHA256_ACCEPTED: TRUE 3/3
REFERENCE_REVIEW_STATE: independent_reviewed 3/3
READY_FOR_AB: TRUE 3/3
```

## Live A/B Execution

VoiceBridge evidence:

```text
branch: agent/krc-media-gemini-migration
workflow: KRC Media M3 Live A-B
run: 33529742510
attempt: 2
execution source commit: acecda62b5c0c0958633f85fd13e5a38e522dbc7
result: SUCCESS
provider results: 6/6
provider failures: 0/6
provider cleanup confirmed: TRUE 6/6
raw media artifact: FALSE
```

Artifact:

```text
name: krc-media-m3-live-ab-results
artifact id: 9810164909
artifact digest: sha256:b8b170f23e94f1a4ca53a811b5463e07c1770d65c08bf1f838a1b12d749986e4
result JSON SHA-256: a9498149cd39abd333700c424255612c0ae93680d2d24a79d7fca6046e0d4127
```

VoiceBridge immutable acceptance record:

`docs/history/2026-09-01_KRC_MEDIA_M3_LIVE_AB_ACCEPTANCE.md`

VoiceBridge evidence commit after acceptance record:

`278203ac5f84d7a1488bdb91caf5e62f64de4e43`

VoiceBridge PR #45 remains OPEN / DRAFT / UNMERGED and Gemini remains inactive for normal KRC prerecorded jobs.

## Deterministic Results

| case | AssemblyAI WER | Gemini WER |
|---|---:|---:|
| UA clean | 0.00% | 0.00% |
| RU clean | 16.67% | 33.33% |
| EN clean | 0.00% | 0.00% |

Aggregate over 31 reviewed reference lexical tokens:

```text
AssemblyAI token-weighted WER: 3.23%
Gemini token-weighted WER: 6.45%
AssemblyAI macro-average WER: 5.56%
Gemini macro-average WER: 11.11%
AssemblyAI mean latency: 3514.3 ms
Gemini mean latency: 3764.7 ms
timestamp coverage: 100% for both providers in all cases
```

No actual currency billing evidence was collected, so no monetary cost comparison is asserted from this run.

## Manual Review

```text
UA: PASS_BOTH
EN: PASS_BOTH
RU: ASSEMBLYAI_PREFERRED / GEMINI_NUMERIC_FORMAT_AMBIGUITY
```

The RU Gemini output used a dotted numeric rendering and omitted the lexical magnitude word. It may be semantically interpretable as the intended amount in some formatting conventions, but it introduces avoidable ambiguity for research-oriented transcription.

## Derived M3 State

```text
M3_PROVIDER_AB: COMPLETE
M3_MANUAL_FACTUAL_REVIEW: COMPLETE
M3_MANUAL_HALLUCINATION_REVIEW: COMPLETE
M3_EVIDENCE_PREFERENCE: ASSEMBLYAI_FOR_THIS_TRANCHE
GEMINI_PRERECORDED_TECHNICAL_FUNCTION: PASS
GEMINI_PRERECORDED_ACTIVE: FALSE
PROVIDER_CUTOVER: NOT_AUTHORIZED
M3_CLOSURE_DECISION: OWNER_DECISION_PENDING
```

The three-case corpus is intentionally small and clean. It is sufficient to prove the controlled A/B path and provide initial provider evidence, but it is not sufficient to establish a universal provider winner.

## Release Gates

```text
R1 merge selected MEDIA BETA work toward main: HOLD
R2 backend/production promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
M4 new-infrastructure canary: NOT_STARTED
M5 provider/new-infrastructure cutover: NOT_AUTHORIZED
```

## Next Decision

Owner must choose one of these product-level paths:

```text
A. RETAIN_ASSEMBLYAI_AND_CLOSE_M3
B. BROADEN_REPRESENTATIVE_CORPUS_BEFORE_M3_CLOSURE
C. KEEP_M3_OPEN_WITHOUT_FURTHER_PROVIDER_SPEND
```

A Gemini provider cutover is not a valid implicit consequence of this A/B result and would require a separate explicit authorization gate.

## Recovery Command

`recover KRC MEDIA BETA M3 A-B complete owner decision checkpoint 2026-09-01`
