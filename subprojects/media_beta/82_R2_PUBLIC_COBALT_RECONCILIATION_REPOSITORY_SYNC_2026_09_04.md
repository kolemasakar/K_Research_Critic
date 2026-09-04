# K-Research & Critic / MEDIA BETA - R2 Public Cobalt Reconciliation Repository Sync Checkpoint 82

Date: 2026-09-04
Status: R2_LIVE_BASELINE / PUBLIC_COBALT_CANDIDATE_REPOSITORY_PASS / DEPLOYMENT_PENDING / CANARY_PENDING / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 81 as the canonical recovery point after the failed YouTube Supadata canary sequence, architecture reconciliation, and repository-only migration of public YouTube/Instagram retrieval to self-hosted Cobalt.

No Render deployment, Render environment mutation, Neon mutation, ChatGPT Builder update, public GPT change, PR merge, Gemini activation, or provider-consuming canary was performed while creating this checkpoint.

## Current live backend baseline

Read-only Render recheck on 2026-09-04 confirms the currently live MEDIA deployment is:

```text
Render service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live deploy: dep-dadfu1mq1p3s73dgv5m0
live commit: 7c8806713ea75b0809b638f102e31d8d3af86150
status: live
autoDeploy: no
```

This live commit still contains the Supadata public path and the temporary free-plan label remediation. It is the immediate rollback target for the next Cobalt candidate deployment.

Historical original R2 rollback baseline remains:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

## Canary sequence and finding

The private MEDIA BETA YouTube canary was attempted through the authenticated GPT Action path.

Observed sequence:

```text
attempt 1 -> fail closed before provider processing because required public/free-only runtime flags were absent
runtime flags -> applied
attempt 2 -> fail closed on Supadata free-tier/account classification
Supadata Basic/free-label guard -> patched and deployed
attempt 3 -> still fail closed on Supadata account/free-tier requirement
```

No successful YouTube transcript was produced by these attempts. The failures did not justify weakening the free-only policy or enabling paid fallback.

## Architecture reconciliation

Repository/history review established:

- Supadata was genuinely implemented and accepted for earlier owner/private zero-client beta work.
- Facebook had already moved to `Cobalt -> AssemblyAI` with no automatic paid fallback.
- Telegram had already moved to `public web -> AssemblyAI` with zero retrieval credits.
- Permanent public YouTube/Instagram reliance on Supadata had not been independently validated as the final free-only architecture.

The accepted public candidate architecture is now:

```text
YouTube   -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 -> durable KRCM/Neon
```

Supadata remains only as historical/private compatibility code. It is not required by `KRC_MEDIA_PUBLIC_MODE` in the new repository candidate.

No paid retrieval fallback is authorized. ScrapeCreators remains forbidden in public free-only mode.

## VoiceBridge repository candidate

Repository:

`kolemasakar/VoiceBridge`

Branch:

`agent/krc-media-gemini-migration`

Repository candidate:

`4384b8dc8ef949ded7859495808b7f138eb8244d`

Commit message:

`R2 public media: route YouTube and Instagram through Cobalt`

Validate workflow:

```text
run: 33916332270
conclusion: SUCCESS
cloud tests: 239 passed / 0 failed
repository-docs: PASS
browser-extension: PASS
krc-image-parity: PASS
```

Repository behavior verified by tests:

```text
public MEDIA does not require SUPADATA_API_KEY
YouTube Cobalt audio retrieval path exists
Instagram Cobalt audio retrieval path exists
Cobalt request uses downloadMode=audio and audioFormat=mp3
retrieval_credits_charged=0
Cobalt failure stops before STT and fails closed
duplicate public job is reused without second retrieval/STT
YouTube public start no longer requires Supadata credit consent
```

VoiceBridge PR #45 remains:

```text
OPEN
DRAFT
UNMERGED
mergeable=true
```

## Public Cobalt release boundary

The repository candidate is not live yet.

Current divergence:

```text
LIVE Render:              7c8806713ea75b0809b638f102e31d8d3af86150
REPOSITORY CANDIDATE:     4384b8dc8ef949ded7859495808b7f138eb8244d
NEXT IMMEDIATE ROLLBACK:  7c8806713ea75b0809b638f102e31d8d3af86150
HISTORICAL R2 ROLLBACK:   2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The next state-changing release step must deploy the exact repository candidate, not an unspecified branch head.

## Provider policy retained

```text
KRC prerecorded current provider: AssemblyAI universal-2
AssemblyAI use: Free balance only
paid AssemblyAI continuation: forbidden
post-AssemblyAI target: Gemini prerecorded
Gemini automatic cutover: not implemented
Gemini public Free activation: requires separate disclosure + explicit user consent
paid Gemini fallback: none
```

## Administrative cleanup

The accidental temporary Render service `noop` was manually deleted by the owner and its deletion was rechecked through the Render connector. No cleanup item remains for that service.

## KRC public boundary

The existing published `K-Research & Critic` GPT remains unchanged and still has no public MEDIA Action attached.

Therefore the current live VoiceBridge changes affect the isolated MEDIA backend/private MEDIA BETA path only. R3 remains the separate gate where the existing public GPT Builder configuration would be updated.

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   LIVE BASELINE / COBALT REPOSITORY CANDIDATE PASS / DEPLOYMENT + CANARY PENDING
R3   HOLD
R4   HOLD
```

R2 must not be marked complete until the exact Cobalt candidate is deployed and bounded Action canaries for YouTube, Instagram, Facebook and Telegram plus Core-isolation checks pass.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Recovery instruction

Recovery must start from this checkpoint 82, then re-read:

1. KRC `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. VoiceBridge branch `agent/krc-media-gemini-migration` exact head and Validate state;
3. Render current live deployment for `srv-da1kic5bedkc73d6fk60`;
4. VoiceBridge `docs/history/2026-09-04_KRC_MEDIA_PUBLIC_COBALT_ROUTING_RECONCILIATION.md`;
5. PR #45 state.

Do not deploy, mutate Render/Neon, merge PR #45, activate Gemini, or edit the public GPT Builder without a fresh explicit owner authorization for that state-changing gate.
