# MEDIA BETA Roadmap
Поточний roadmap приватного MEDIA BETA після завершення A9-A10 та під час M3 prerecorded provider-evidence migration track.

Version: 4.0
Status: RELEASE_HOLD_OWNER_TESTING / M3_READY_FOR_AB
Updated: 2026-09-01

## Product Position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main
closed-beta product branch: agent/video-url-research
technology/backend implementation source: kolemasakar/VoiceBridge
active KRC provider-migration branch: agent/krc-media-gemini-migration
```

VoiceBridge supplies reusable technology, backend implementation, and validation evidence. It is not the parent product and does not independently authorize KRC MEDIA BETA release decisions.

## Accepted Runtime Baseline

```text
A8 browser-assisted owner baseline                 COMPLETE / FALLBACK_ONLY
A9 owner zero-client media input                   COMPLETE / ACCEPTED
A9.10 local attachment                             COMPLETE / ACCEPTED
A10 copy-safe claim-summary stabilization           COMPLETE / ACCEPTED
Builder package                                     0.9.1-beta-a10
Action schema                                       0.6.0-a9.10
release state                                       RELEASE_HOLD_OWNER_TESTING
```

Accepted owner inputs remain YouTube, Instagram Reel, Facebook Video/Reel through free Cobalt, supported public Telegram video, and one current-conversation local audio/video attachment.

Accepted policy remains unchanged:

```text
Facebook Cobalt failure -> unavailable
NO automatic paid fallback
ScrapeCreators reserve only / inactive
Telegram public-only / zero retrieval credits
local attachment max 32 MiB / zero retrieval credits
```

## VoiceBridge Shared Baseline

VoiceBridge live streaming migration to Gemini is complete and separate from KRC prerecorded migration.

```text
VoiceBridge main                               a426ae331721dd36291874e45380faf603d854cf
VoiceBridge streaming default                  Gemini gemini-3.5-transcribe-live
VoiceBridge streaming rollback                 AssemblyAI universal-streaming-english
VoiceBridge Phase 2                            COMPLETE / CONTROLLED E2E VALIDATED
```

KRC prerecorded provider state remains:

```text
selector: KRC_MEDIA_STT_PROVIDER
active provider: AssemblyAI
active model: universal-2
Gemini candidate: gemini-3.5-transcribe
Gemini normal activation: FALSE
```

VoiceBridge live Gemini acceptance does not substitute for KRC prerecorded M3 evidence and does not activate Gemini for normal KRC jobs.

## Active Track: KRC Gemini Prerecorded Forward Migration

```text
M0 migration preflight                         COMPLETE
M1 provider abstraction                        PASS
M2 Gemini prerecorded adapter                  PASS / INACTIVE
M3 offline evaluator                           PASS
M3 same-asset execution contract               PASS
M3 corpus manifest/readiness contract          PASS
M3 byte-exact evidence helper                  PASS
M3 first clean-public asset tranche            ACCEPTED
M3 independent reference review                COMPLETE 3/3
M3 READY_FOR_AB clean tranche                  TRUE 3/3
M3 provider-consuming A/B                      NOT_RUN
M4 new-infrastructure canary                    NOT_STARTED
M5 provider/new-infrastructure cutover          NOT_AUTHORIZED
```

Technical authority:

```text
VoiceBridge branch: agent/krc-media-gemini-migration
current evidence head: 90ca4f354a466f7f5ffdba20de246eb033b369a8
VoiceBridge draft PR: #45
latest pre-acceptance validated head: 6dd00fefcf9f29de4af37ce5417dddec988d4562
Validate run: 33525309306 SUCCESS
final-reference exact-head Validate: 33527873644 running at roadmap write
```

The final-reference head adds evidence documentation only; it does not activate Gemini or change runtime provider behavior.

## M3 Accepted Clean-Public Evidence

### ua-clean-public-001

```text
asset SHA-256:
98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c

original candidate reference: REJECTED AFTER LISTENING REVIEW
corrected final reference SHA-256:
2ec614c71321a8747b6bb50fb57a7c341bcad9150a09c5cb2a1825ebfc0f828e
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

### ru-clean-public-001

```text
asset SHA-256:
d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5

final reference SHA-256:
1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

### en-clean-public-001

```text
asset SHA-256:
63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715

final reference SHA-256:
044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

Reference transcript bytes remain outside GitHub. GitHub stores only digests, provenance metadata, and review state.

The Ukrainian upstream candidate was correctly rejected after independent listening revealed a material lexical mismatch. The corrected local reference artifact was recreated using UTF-8, LF, exactly one terminal newline, no pre-hash normalization, then re-hashed. This evidence correction does not alter the accepted media asset hash.

## Current Evidence State

```text
REAL_ASSET_BYTES_CAPTURED                     TRUE
REAL_ASSETS_SELECTED                          TRUE
ASSET_SHA256_ACCEPTED                         TRUE / 3 OF 3
REFERENCE_LISTENING_REVIEW_COMPLETED           TRUE / 3 OF 3
FINAL_REFERENCE_SHA256_ACCEPTED                TRUE / 3 OF 3
REFERENCE_REVIEW_STATE                         independent_reviewed / 3 OF 3
READY_FOR_AB                                   TRUE / 3 OF 3
M3_PROVIDER_AB                                 NOT_RUN
ASSEMBLYAI_M3_CALLS                            NONE
GEMINI_M3_MEDIA_CALLS                          NONE
GEMINI_PRERECORDED_ACTIVE                      FALSE
```

## CURRENT ROADMAP POSITION

```text
M3 READY_FOR_AB / PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

Next transition:

```text
READY_FOR_AB
 -> explicit authorization for provider-consuming test
 -> same exact media asset to AssemblyAI universal-2
 -> same exact media asset to Gemini gemini-3.5-transcribe
 -> capture provider output + latency/cost metadata
 -> deterministic comparison against final reference
 -> manual factual/hallucination review
 -> M3 closure decision
```

Provider-consuming AssemblyAI/Gemini execution is a separate action. Reaching `READY_FOR_AB` does not itself authorize spending provider credits or activating Gemini for normal KRC jobs.

## M4 - New-Infrastructure Canary

Status: NOT STARTED.

M4 requires a KRC-specific deployment-image parity audit covering media retrieval, probing/transcoding, managed KRC HTTP routes, Neon/PostgreSQL tooling, quota ledger, retention/provider cleanup, privacy/log-redaction guards, and route isolation.

VoiceBridge Phase 2 completion is positive shared-infrastructure evidence but is not sufficient by itself to close this KRC-specific gate.

## M5 - Cutover Decision

Status: NOT AUTHORIZED.

Any KRC prerecorded provider or infrastructure cutover requires separate explicit owner approval and verified rollback to the accepted AssemblyAI path.

## Release Hold

All release gates remain closed and independent:

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 backend/production promotion                 HOLD
R3 external testers                             HOLD
R4 public sharing / Store rollout               HOLD
```

M3 completion, favorable Gemini evidence, successful CI, or VoiceBridge Phase 2 completion does not automatically authorize any release gate.

## Optional Future Sustainability Work

Cloudflare/local Whisper or other provider-neutral cost reductions remain optional future work. They are not prerequisites for private owner testing and must not silently replace the accepted beta route.
