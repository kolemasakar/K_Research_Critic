# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.8
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3B_READY_FOR_AB
Updated: 2026-09-01

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical reading order

1. `67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md` - current recovery authority after expanded-corpus byte verification and independent listening review 4/4.
2. `66_M3B_CORPUS_EXPANSION_REVIEW_CHECKPOINT_2026_09_01.md` - immediately preceding M3B review-pending checkpoint.
3. `65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - first three-case provider A/B result and owner decision gate.
4. `64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md` - first clean-public tranche ready-for-A/B checkpoint.
5. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline.
6. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` - VoiceBridge live versus KRC prerecorded interpretation.
7. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - cross-repository migration overlay.
8. `03_CURRENT_STATE.md` - accepted operational runtime baseline.
9. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - release authority.
10. `01_ARCHITECTURE.md`, `02_ROADMAP.md`, `04_OPERATIONS_RUNBOOK.md`, `05_TEST_PLAN.md`, `06_DECISION_LOG.md` - architecture, roadmap, operations, tests, and decisions.
11. `08_CHAT_HANDOFF.md` - fresh-chat recovery.

## Current M3 evidence state

First tranche:

```text
cases                                      3
provider A/B                               COMPLETE
AssemblyAI token-weighted WER              3.23%
Gemini token-weighted WER                  6.45%
first-tranche evidence preference          ASSEMBLYAI_FOR_THIS_TRANCHE
Gemini prerecorded technical function      PASS
```

Expanded M3B tranche:

```text
new cases                                  4
asset bytes captured                       TRUE 4/4
asset SHA-256 accepted                     TRUE 4/4
local owner SHA-256 verification           MATCH 4/4
independent listening review               COMPLETE 4/4
final reference SHA-256 accepted           TRUE 4/4
M3B READY_FOR_AB                           TRUE 4/4
M3B provider A/B                           NOT_RUN
```

The seven-case corpus now consists of the original UA/RU/EN clean-public tranche plus four expanded English dimensions: longer clean speech, severe background noise, spoken numeric sequences, and LibriSpeech test-other challenging speech.

## M3B final reference hashes

Transcript bodies remain outside GitHub. Reference byte convention: UTF-8, LF, exactly one terminal newline.

```text
en-long-harvard-001
f9e9eddbd0130ab1505d877a18cb29a26492114ecda86b9e7da92ec29b78b211

en-noisy-jackhammer-001
cf62ebe3e7e89f77272a5f6fdf296d2860af8e738799d939a672c08fe4484724

en-numeric-vosk-001
cc73ecc627780d8b6ef02fd5d8b093d85f21420a9a646b871e3ce0a0934eb1f4

en-hard-librispeech-001
a5bbd76f41e8929020cacf75c98208b7d6a42d6b669c95a8e8303f27ac97ec49
```

VoiceBridge current M3B evidence authority:

```text
docs/history/2026-09-01_KRC_MEDIA_M3B_CORPUS_EXPANSION_BYTE_ACCEPTANCE.md
docs/history/2026-09-01_KRC_MEDIA_M3B_REFERENCE_REVIEW_ACCEPTANCE.md
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

No M3/M3B evidence checkpoint independently authorizes provider cutover, merge, deployment, external testing, or public release.

## Exact continuation point

```text
M3B READY_FOR_AB / SECOND PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

A second bounded same-asset comparison may run only after separate explicit owner authorization:

```text
4 accepted M3B assets x 2 providers = maximum 8 provider submissions
AssemblyAI universal-2
Gemini gemini-3.5-transcribe
```

## Recovery command

`recover KRC MEDIA BETA M3B ready-for-A/B checkpoint 2026-09-01`

Always read `67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md` first and verify current GitHub heads/CI before provider-consuming work.
