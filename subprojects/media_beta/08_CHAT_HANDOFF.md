# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.4
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3B_AB_COMPLETE_OWNER_DECISION_PENDING
Checkpoint date: 2026-09-01

## Recovery command

`recover KRC MEDIA BETA M3B A/B complete owner decision checkpoint 2026-09-01`

## Mandatory recovery order

1. `subprojects/media_beta/68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
2. `subprojects/media_beta/67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md`
3. `subprojects/media_beta/65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
4. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
5. `subprojects/media_beta/00_INDEX.md`
6. `subprojects/media_beta/02_ROADMAP.md`
7. `subprojects/media_beta/03_CURRENT_STATE.md`
8. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`
9. `subprojects/media_beta/01_ARCHITECTURE.md`
10. `subprojects/media_beta/06_DECISION_LOG.md`

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
    PR: #8 draft/open/unmerged
    release state: RELEASE_HOLD_OWNER_TESTING

VoiceBridge
 -> technology/backend implementation source
 -> main: accepted shared baseline
 -> agent/krc-media-gemini-migration: active KRC prerecorded migration / PR #45
```

VoiceBridge cannot independently authorize KRC product release gates.

## Current M3 evidence

First provider tranche:

```text
M3_FIRST_TRANCHE_AB: COMPLETE
AssemblyAI token-weighted WER: 3.23%
Gemini token-weighted WER: 6.45%
first-tranche preference: ASSEMBLYAI_FOR_THIS_TRANCHE
```

Expanded M3B tranche:

```text
M3B_ASSET_SHA256_ACCEPTED: TRUE 4/4
M3B_REFERENCE_INDEPENDENT_REVIEW: COMPLETE 4/4
M3B_PROVIDER_AB: COMPLETE
M3B_PROVIDER_RESULTS: SUCCESS 8/8
M3B_LEXICAL_WER: TIE_FOR_THIS_TRANCHE
M3B_NUMERIC_SEQUENCE_FIDELITY: GEMINI_PREFERRED_FOR_THIS_FIXTURE
```

Execution authority:

```text
VoiceBridge workflow: KRC Media M3B Live A-B
run: 33545803364
source commit: 4f55dab95abe5518b9205cb5666ad457795416d7
result: SUCCESS
artifact id: 9815474860
artifact digest: sha256:27553dfea4c4b641f54cfd8113b9a91396f262a6d2b9dc4c928a57f72964e80f
raw media artifact: FALSE
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

Numeric interpretation is mixed: an earlier RU case favored AssemblyAI for numeric-format clarity; the M3B numeric sequence fixture favored Gemini for complete digit-sequence preservation.

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
M3B A/B COMPLETE / OWNER M3 CLOSURE DECISION
```

Owner decision options:

```text
1. RETAIN_ASSEMBLYAI_AND_CLOSE_M3
2. M3C_TARGETED_CORPUS
3. HOLD_WITHOUT_CUTOVER
```

A further provider-consuming run is not implied by the completed A/B and requires separate explicit authorization.

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_4_M3B_AB_COMPLETE_OWNER_DECISION`
