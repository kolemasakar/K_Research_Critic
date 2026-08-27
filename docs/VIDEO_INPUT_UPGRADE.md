# VIDEO_INPUT_UPGRADE
Архітектура поточного приватного zero-client медіавходу без зміни public Core workflow.

Version: 1.0
Status: PRIVATE_BETA_ACCEPTED / RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## 1. Objective

Add reliable media source acquisition to K-Research & Critic while preserving the existing CriticProfile -> Research -> Critic workflow.

Current accepted input set is broader than the original YouTube-only preview:

```text
YouTube
Instagram Reel
Facebook Video/Reel
supported public Telegram video post
one local audio/video attachment
```

## 2. Non-Regression Rule

The public text Core remains independent of media ingestion. A media failure must not weaken or replace the standard research workflow.

## 3. Current Architecture

```text
MEDIA INPUT
 -> private MEDIA BETA GPT
 -> managed Action
 -> isolated VoiceBridge MEDIA BETA
 -> source-specific acquisition
 -> normalized durable KRCM transcript
 -> claim inventory
 -> CriticProfile approval gate
 -> independent Research
 -> Critic
 -> final report
```

## 4. Route Matrix

### YouTube / Instagram

Managed transcript provider path. Billable operations require explicit preflight and user approval. Instagram AI generation requires a separate second approval.

### Facebook

```text
free Cobalt retrieval
 -> success: AssemblyAI -> durable KRCM
 -> failure: unavailable -> STOP
```

No automatic or offered paid Facebook fallback is active. ScrapeCreators remains reserve-only compatibility code.

### Telegram

```text
public Telegram web/embed
 -> trusted Telegram CDN
 -> AssemblyAI
 -> durable KRCM
```

Retrieval credits are zero. No Telegram account, cookies, session, bot token, or paid fallback is used.

### Local attachment

```text
one current-conversation attachment
 -> openaiFileIdRefs
 -> trusted *.oaiusercontent.com delivery
 -> bounded download/type/duration checks
 -> media normalization
 -> AssemblyAI
 -> durable KRCM
```

Maximum accepted attachment size is 32 MiB. Retrieval credits are zero. File IDs and signed URLs are not user-visible.

## 5. Evidence Boundary

A transcript proves what the source said. It does not independently establish truth. Material factual claims must be independently checked after CriticProfile approval.

## 6. CriticProfile and Cross-Check Boundary

No independent claim research starts before explicit approval. Cross-check floors remain risk-based and each material factual claim must expose a traceable required/achieved result with SHORTFALL when applicable.

## 7. Durable Media State

Managed media state uses durable `KRCM_` jobs and paged transcript segments. Completed jobs remain reusable where the backend contract defines idempotent reuse. Uncertain-charge provider work is never automatically replayed.

## 8. Security and Privacy

- remote adapters support public content only;
- no platform passwords/cookies/sessions/account tokens;
- Action bearer, owner admission, and provider keys remain server-side;
- temporary source media is not intended as durable storage;
- full transcripts are excluded from KRC checkpoints;
- local attachment transport is accepted only through the current-conversation OpenAI file-reference boundary.

## 9. A10 Output Stabilization

The final claim-summary table is rendered normally and duplicated in a fenced `text` block for reliable whole-response copying. This is an accepted mitigation for a ChatGPT UI serialization defect.

## 10. Current Release State

All intended owner-only media inputs and A10 output stabilization are accepted. The feature is nevertheless held in private owner testing.

```text
merge = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

The next step is not another mandatory media adapter. It is a future release decision after the owner testing period.
