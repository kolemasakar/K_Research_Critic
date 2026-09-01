# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.9
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3B_AB_COMPLETE_OWNER_DECISION_PENDING
Updated: 2026-09-01

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical reading order

1. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - current recovery authority after completed expanded-corpus provider A/B and seven-case synthesis.
2. `67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md` - immediately preceding M3B ready-for-A/B checkpoint.
3. `65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - first three-case provider A/B result.
4. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline.
5. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` - VoiceBridge live versus KRC prerecorded interpretation.
6. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - cross-repository migration overlay.
7. `03_CURRENT_STATE.md` - accepted operational runtime baseline.
8. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - release authority.
9. `01_ARCHITECTURE.md`, `02_ROADMAP.md`, `04_OPERATIONS_RUNBOOK.md`, `05_TEST_PLAN.md`, `06_DECISION_LOG.md` - architecture, roadmap, operations, tests, and decisions.
10. `08_CHAT_HANDOFF.md` - fresh-chat recovery.

## Current M3 evidence state

First tranche:

```text
cases: 3
provider A/B: COMPLETE
AssemblyAI token-weighted WER: 3.23%
Gemini token-weighted WER: 6.45%
first-tranche preference: ASSEMBLYAI_FOR_THIS_TRANCHE
```

Expanded M3B tranche:

```text
new cases: 4
byte and SHA-256 acceptance: COMPLETE 4/4
independent listening review: COMPLETE 4/4
provider A/B: COMPLETE 8/8 provider results
M3B lexical WER: TIE_FOR_THIS_TRANCHE
numeric sequence factual completeness: GEMINI_PREFERRED_FOR_THIS_FIXTURE
```

Seven-case synthesis:

```text
reviewed reference tokens: 117
AssemblyAI lexical WER: 13.68%
Gemini lexical WER: 14.53%
AssemblyAI mean latency: 3346.43 ms
Gemini mean latency: 3555.86 ms
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

## VoiceBridge current evidence authority

```text
docs/history/2026-09-01_KRC_MEDIA_M3_LIVE_AB_ACCEPTANCE.md
docs/history/2026-09-01_KRC_MEDIA_M3B_CORPUS_EXPANSION_BYTE_ACCEPTANCE.md
docs/history/2026-09-01_KRC_MEDIA_M3B_REFERENCE_REVIEW_ACCEPTANCE.md
docs/history/2026-09-01_KRC_MEDIA_M3B_LIVE_AB_ACCEPTANCE.md
```

M3B execution:

```text
workflow run: 33545803364
result: SUCCESS
provider results: 8/8 SUCCESS
artifact: 9815474860
artifact digest: sha256:27553dfea4c4b641f54cfd8113b9a91396f262a6d2b9dc4c928a57f72964e80f
raw media artifact: FALSE
```

## Active provider boundary

```text
KRC prerecorded active provider: AssemblyAI universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini prerecorded active for normal KRC jobs: FALSE
VoiceBridge live Gemini: separate accepted streaming domain
provider cutover: NOT_AUTHORIZED
```

## Release boundary

```text
R1 merge: HOLD
R2 backend promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
RELEASE_HOLD_OWNER_TESTING: PRESERVED
```

## Exact continuation point

```text
M3B A/B COMPLETE / OWNER M3 CLOSURE DECISION
```

Owner decision options:

```text
1. RETAIN_ASSEMBLYAI_AND_CLOSE_M3
2. M3C_TARGETED_CORPUS
3. HOLD_WITHOUT_CUTOVER
```

Any new provider-consuming work requires separate explicit authorization.

## Recovery command

`recover KRC MEDIA BETA M3B A/B complete owner decision checkpoint 2026-09-01`

Always read `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` first and verify current GitHub heads/CI before any write, provider-consuming work, merge, deployment, or activation decision.
