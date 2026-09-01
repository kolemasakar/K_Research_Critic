# K-Research & Critic - MEDIA BETA
## M3B Corpus Expansion Review Checkpoint

Date: 2026-09-01
Status: CANONICAL_RECOVERY_CHECKPOINT / RELEASE_HOLD_OWNER_TESTING / M3B_REFERENCE_REVIEW_PENDING
Supersedes for current continuation: `65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`

## Owner decision

After the first controlled three-case provider A/B, the owner selected:

`BROADEN CORPUS`

This decision does not authorize a second provider-consuming A/B run. The next gate is evidence preparation and independent listening review.

## Product boundary

```text
K-Research & Critic
 -> public Core: K_Research_Critic/main / published / maintenance
 -> MEDIA BETA: K_Research_Critic/agent/video-url-research
    product/roadmap authority

VoiceBridge
 -> technology/backend implementation and M3 evidence authority
 -> active KRC branch: agent/krc-media-gemini-migration
```

The public Core runtime is not changed by this checkpoint.

## First M3 tranche retained

```text
first clean-public cases                     3
first provider A/B                            COMPLETE
AssemblyAI token-weighted WER                 3.23%
Gemini token-weighted WER                     6.45%
first-tranche evidence preference             ASSEMBLYAI_FOR_THIS_TRANCHE
Gemini prerecorded technical function         PASS
Gemini prerecorded normal activation          FALSE
provider cutover                              NOT_AUTHORIZED
```

The first tranche is too small to justify a global provider cutover.

## M3B expanded tranche

Four additional real public, byte-stable cases are accepted for pre-provider review:

| case | dimension | asset SHA-256 |
|---|---|---|
| `en-long-harvard-001` | longer multi-sentence clean English | `971b4163670445c415c6b0fb6813c38093409ecac2f6b4d429ae3574d24ad470` |
| `en-noisy-jackhammer-001` | loud jackhammer background noise | `a9484bb0ec40468683ebe6a064f6b4b579bfa800ac8b360a15ae3d225c5037e2` |
| `en-numeric-vosk-001` | digit sequences / zero versus oh | `dcfea5712c43a43ba7ae8083afb39d36993e5a69c46e88b68aaa72b65cb615bb` |
| `en-hard-librispeech-001` | LibriSpeech test-other challenging speech | `078553534e86b6c32eb0d3e30a75be8a4546735a910e14ab924c0b9f51367f4d` |

VoiceBridge byte capture:

```text
workflow: KRC Media M3B Expanded Corpus Byte Capture
run: 33536967546
result: SUCCESS
new assets captured: 4/4
provider calls: NONE
provider credentials used: NONE
raw media artifact: NONE
```

VoiceBridge evidence record:

`docs/history/2026-09-01_KRC_MEDIA_M3B_CORPUS_EXPANSION_BYTE_ACCEPTANCE.md`

## Candidate reference state

Candidate transcript artifacts are created outside GitHub using UTF-8, LF, exactly one terminal newline.

```text
en-long-harvard-001
candidate reference SHA-256:
f9e9eddbd0130ab1505d877a18cb29a26492114ecda86b9e7da92ec29b78b211

en-noisy-jackhammer-001
candidate reference SHA-256:
cf62ebe3e7e89f77272a5f6fdf296d2860af8e738799d939a672c08fe4484724

en-numeric-vosk-001
candidate reference SHA-256:
cc73ecc627780d8b6ef02fd5d8b093d85f21420a9a646b871e3ce0a0934eb1f4

en-hard-librispeech-001
candidate reference SHA-256:
a5bbd76f41e8929020cacf75c98208b7d6a42d6b669c95a8e8303f27ac97ec49
```

These are `CANDIDATE / REVIEW_PENDING`; none is a final accepted reference until reconciled by independent listening to the exact accepted audio.

## Current state

```text
M3_FIRST_TRANCHE_AB                         COMPLETE
M3B_CORPUS_EXPANSION_SELECTED               TRUE
M3B_NEW_CASES                               4
M3B_ASSET_BYTES_CAPTURED                    TRUE 4/4
M3B_ASSET_SHA256_ACCEPTED                   TRUE 4/4
M3B_REFERENCE_CANDIDATES_CREATED            TRUE 4/4 (outside GitHub)
M3B_REFERENCE_INDEPENDENT_REVIEW            PENDING 4/4
M3B_FINAL_REFERENCE_SHA256_ACCEPTED          FALSE
M3B_READY_FOR_AB                            FALSE
M3B_PROVIDER_CALLS                          NONE
GEMINI_PRERECORDED_ACTIVE                   FALSE
PROVIDER_CUTOVER                            NOT_AUTHORIZED
R1 / R2 / R3 / R4                           HOLD
```

## Coverage added

M3B adds:

- longer clean speech;
- severe background noise;
- numeric wording and `zero` / `oh` distinction;
- a harder `test-other` audiobook case.

Still not covered by this tranche:

- real multi-speaker conversation;
- code-switching;
- telephone-bandwidth speech;
- noisy Ukrainian;
- noisy Russian.

These dimensions are deferred to a possible M3C only if the seven-case evidence remains insufficient or contradictory.

## Exact continuation point

```text
M3B EXACT AUDIO DOWNLOAD
 -> local SHA-256 verification
 -> independent full-file listening 4/4
 -> final reference corrections if needed
 -> final reference SHA-256 acceptance
 -> M3B READY_FOR_AB
 -> separate owner authorization for provider-consuming A/B
```

Do not use AssemblyAI or Gemini output to establish ground truth.
Do not activate Gemini prerecorded for normal KRC jobs as part of this evidence track.

## Recovery command

`recover KRC MEDIA BETA M3B corpus expansion review checkpoint 2026-09-01`
