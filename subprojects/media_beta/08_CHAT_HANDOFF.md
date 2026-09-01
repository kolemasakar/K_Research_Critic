# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.3
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3B_READY_FOR_AB
Checkpoint date: 2026-09-01

## Recovery command

`recover KRC MEDIA BETA M3B ready-for-A/B checkpoint 2026-09-01`

## Mandatory recovery order

1. `subprojects/media_beta/67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md`
2. `subprojects/media_beta/65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
3. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
4. `subprojects/media_beta/00_INDEX.md`
5. `subprojects/media_beta/61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md`
6. `subprojects/media_beta/60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md`
7. `subprojects/media_beta/03_CURRENT_STATE.md`
8. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`
9. `subprojects/media_beta/01_ARCHITECTURE.md`
10. `subprojects/media_beta/02_ROADMAP.md`
11. `subprojects/media_beta/06_DECISION_LOG.md`

Verify current GitHub heads and CI before any write, provider-consuming operation, merge, deployment, or activation decision.

## Product / repository context

```text
K-Research & Critic
 -> public Core
    repo: kolemasakar/K_Research_Critic
    branch: main
    state: published / maintenance

 -> K-Research & Critic - MEDIA BETA
    role: closed-beta module
    product/roadmap authority: K_Research_Critic
    branch: agent/video-url-research
    PR: #8
    release state: RELEASE_HOLD_OWNER_TESTING

VoiceBridge
 -> technology/backend implementation source
 -> main: accepted VoiceBridge project baseline
 -> agent/krc-media-gemini-migration: active KRC prerecorded migration / PR #45
```

VoiceBridge cannot independently authorize KRC product release gates.

## Current M3 state

First tranche:

```text
M3_FIRST_TRANCHE_AB                         COMPLETE 3/3
AssemblyAI token-weighted WER               3.23%
Gemini token-weighted WER                   6.45%
first-tranche preference                    ASSEMBLYAI_FOR_THIS_TRANCHE
Gemini prerecorded technical function       PASS
```

M3B expanded tranche:

```text
M3B_NEW_CASES                               4
M3B_ASSET_BYTES_CAPTURED                    TRUE 4/4
M3B_ASSET_SHA256_ACCEPTED                   TRUE 4/4
M3B_LOCAL_ASSET_SHA256_VERIFIED             TRUE 4/4
M3B_REFERENCE_INDEPENDENT_REVIEW            COMPLETE 4/4
M3B_FINAL_REFERENCE_SHA256_ACCEPTED         TRUE 4/4
M3B_READY_FOR_AB                            TRUE 4/4
M3B_PROVIDER_AB                             NOT_RUN
```

The owner independently listened to all four exact M3B assets after local SHA-256 verification. JACKHAMMER, VOSK NUMERIC, LIBRISPEECH, and HARVARD all passed without transcript correction.

## M3B final reference hashes

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

Transcript bodies remain outside GitHub.

VoiceBridge acceptance authority:

`docs/history/2026-09-01_KRC_MEDIA_M3B_REFERENCE_REVIEW_ACCEPTANCE.md`

## Provider separation

```text
VoiceBridge live streaming:
STT_PROVIDER=gemini
gemini-3.5-transcribe-live
accepted default

KRC prerecorded:
active provider: AssemblyAI universal-2
Gemini candidate: gemini-3.5-transcribe
Gemini active for normal jobs: FALSE
provider cutover: NOT_AUTHORIZED
```

## Critical policy recovery

- Facebook: Cobalt fail -> unavailable; no automatic paid fallback.
- Telegram: public-only, zero retrieval credits.
- Local attachment: trusted OpenAI file delivery, max 32 MiB, zero retrieval credits.
- AssemblyAI remains active for normal KRC prerecorded jobs.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 copy-safe summary remains mandatory.

## Release decision

```text
R1 merge: HOLD
R2 backend/production promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
M4 canary: NOT_STARTED
provider cutover: NOT_AUTHORIZED
```

## Exact continuation point

```text
M3B READY_FOR_AB / SECOND PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

Only after explicit owner authorization:

```text
4 exact accepted M3B assets
x 2 providers
= maximum 8 provider submissions

AssemblyAI universal-2
Gemini gemini-3.5-transcribe
 -> capture outputs
 -> deterministic comparison against final references
 -> manual factual/hallucination review
 -> seven-case evidence synthesis
 -> M3 closure or further-corpus decision
```

Do not infer provider-spend authorization from `READY_FOR_AB`. Do not activate Gemini for normal KRC jobs as part of the test.

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_3_M3B_READY_FOR_AB_PROVIDER_AUTHORIZATION`
