# K-Research & Critic - MEDIA BETA
## M3B Ready-for-A/B Checkpoint

Date: 2026-09-01
Status: CANONICAL_RECOVERY_CHECKPOINT / RELEASE_HOLD_OWNER_TESTING / M3B_READY_FOR_AB
Supersedes for current continuation: `66_M3B_CORPUS_EXPANSION_REVIEW_CHECKPOINT_2026_09_01.md`

## Owner review outcome

The owner completed independent full-file listening for all four M3B expanded-corpus assets after local SHA-256 verification.

```text
JACKHAMMER   PASS
VOSK NUMERIC PASS
LIBRISPEECH  PASS
HARVARD      PASS
```

No correction to any candidate reference was required.

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

The public Core runtime is unchanged by this checkpoint.

## M3B exact assets

| case | accepted asset SHA-256 | local owner SHA verification | listening |
|---|---|---|---|
| `en-long-harvard-001` | `971b4163670445c415c6b0fb6813c38093409ecac2f6b4d429ae3574d24ad470` | MATCH | PASS |
| `en-noisy-jackhammer-001` | `a9484bb0ec40468683ebe6a064f6b4b579bfa800ac8b360a15ae3d225c5037e2` | MATCH | PASS |
| `en-numeric-vosk-001` | `dcfea5712c43a43ba7ae8083afb39d36993e5a69c46e88b68aaa72b65cb615bb` | MATCH | PASS |
| `en-hard-librispeech-001` | `078553534e86b6c32eb0d3e30a75be8a4546735a910e14ab924c0b9f51367f4d` | MATCH | PASS |

VoiceBridge byte-capture workflow:

```text
run: 33536967546
result: SUCCESS
new assets captured: 4/4
provider calls: NONE
provider credentials used: NONE
raw media artifact: NONE
```

## Final accepted reference hashes

Reference byte convention: UTF-8, LF, exactly one terminal newline. Transcript bodies remain outside GitHub.

```text
en-long-harvard-001
FINAL_REFERENCE_SHA256=f9e9eddbd0130ab1505d877a18cb29a26492114ecda86b9e7da92ec29b78b211

en-noisy-jackhammer-001
FINAL_REFERENCE_SHA256=cf62ebe3e7e89f77272a5f6fdf296d2860af8e738799d939a672c08fe4484724

en-numeric-vosk-001
FINAL_REFERENCE_SHA256=cc73ecc627780d8b6ef02fd5d8b093d85f21420a9a646b871e3ce0a0934eb1f4

en-hard-librispeech-001
FINAL_REFERENCE_SHA256=a5bbd76f41e8929020cacf75c98208b7d6a42d6b669c95a8e8303f27ac97ec49
```

VoiceBridge acceptance record:

`docs/history/2026-09-01_KRC_MEDIA_M3B_REFERENCE_REVIEW_ACCEPTANCE.md`

## Retained first-tranche evidence

```text
M3_FIRST_TRANCHE_AB                          COMPLETE 3/3
AssemblyAI token-weighted WER                3.23%
Gemini token-weighted WER                    6.45%
first-tranche evidence preference            ASSEMBLYAI_FOR_THIS_TRANCHE
Gemini prerecorded technical function        PASS
Gemini prerecorded normal activation          FALSE
provider cutover                              NOT_AUTHORIZED
```

## Current state

```text
M3_FIRST_TRANCHE_AB                         COMPLETE 3/3
M3B_CORPUS_EXPANSION_SELECTED               TRUE
M3B_NEW_CASES                               4
M3B_ASSET_BYTES_CAPTURED                    TRUE 4/4
M3B_ASSET_SHA256_ACCEPTED                   TRUE 4/4
M3B_LOCAL_ASSET_SHA256_VERIFIED             TRUE 4/4
M3B_REFERENCE_INDEPENDENT_REVIEW            COMPLETE 4/4
M3B_FINAL_REFERENCE_SHA256_ACCEPTED          TRUE 4/4
M3B_READY_FOR_AB                            TRUE 4/4
M3B_PROVIDER_AB                             NOT_RUN
M3B_PROVIDER_CALLS                          NONE
GEMINI_PRERECORDED_ACTIVE                   FALSE
PROVIDER_CUTOVER                            NOT_AUTHORIZED
R1 / R2 / R3 / R4                           HOLD
```

## Exact continuation point

The next action is a separately authorized, bounded, same-asset M3B provider A/B:

```text
4 exact accepted assets
x
2 prerecorded providers
=
maximum 8 provider submissions

AssemblyAI: universal-2
Gemini: gemini-3.5-transcribe
```

No automatic retries/resubmissions should be introduced. Normal KRC provider selection must remain AssemblyAI unless a later separate cutover gate is explicitly approved.

The owner decision `BROADEN CORPUS` did not itself authorize this second provider-consuming run. Explicit authorization is still required.

## Recovery command

`recover KRC MEDIA BETA M3B ready-for-A/B checkpoint 2026-09-01`
