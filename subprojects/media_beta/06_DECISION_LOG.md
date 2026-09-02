# MEDIA BETA Decision Log
Реєстр чинних і історичних рішень MEDIA BETA з актуальними release-hold рішеннями.

Version: 2.1
Status: ACTIVE
Updated: 2026-09-02

This file is the compact current decision index. Detailed historical rationale remains available in Git history and the numbered phase/acceptance records.

## Historical Decisions D001-D022

`D001` Media input is additive to the KRC Core - APPROVED.

`D002` CriticProfile approval remains mandatory before independent research - APPROVED.

`D003` Transcript proves what was said, not truth - APPROVED.

`D004` Closed beta precedes public scaling - APPROVED; original multi-tester target is now operationally superseded by owner-only hold state.

`D005` MEDIA BETA uses separate private product identity - APPROVED.

`D006` MEDIA BETA backend is isolated from production VoiceBridge - APPROVED.

`D007` Historical multi-tester admission used per-tester codes - APPROVED_HISTORICAL; normal current owner flow no longer asks for a code.

`D008` Subtitle-first principle - retained where reliable, but historical browser-helper implementation decisions are not current normal UX.

`D009` AssemblyAI is a beta reliability/STT provider, not a permanent public-free commitment - APPROVED.

`D010` Bounded beta resource limits - APPROVED.

`D011` Users do not provide provider API keys - APPROVED.

`D012` Full transcript is excluded from KRC checkpoints - APPROVED.

`D013` Sustainable free hybrid is a future direction, not current active architecture - APPROVED_DIRECTION.

`D014` Unlimited-free is interpreted operationally, not literally - APPROVED_DIRECTION.

`D015` Resource limits change only by explicit decision - APPROVED.

`D016` Browser-assisted ingress was the A4 fallback architecture - APPROVED_HISTORICAL / FALLBACK_ONLY.

`D017` Zero-client media router is public-only for remote platforms and multi-platform - APPROVED.

`D018` Local audio/video upload is a separate approved ingress class - APPROVED; live acceptance later completed in A9.10.

`D019` Managed transcript provider became primary zero-client YouTube approach - APPROVED.

`D020` Billable managed-provider operations require explicit user consent - APPROVED.

`D021` Managed KRCM jobs are durable and duplicate starts are credit-safe - APPROVED / LIVE_ACCEPTED.

`D022` Private owner Action hides beta admission behind bearer authentication and server-side owner admission - APPROVED / LIVE_ACCEPTED.

## D023 - Facebook Active Route Is Free Cobalt Only

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-24

Active Facebook behavior:

```text
Cobalt success -> AssemblyAI -> durable KRCM
Cobalt failure -> unavailable -> STOP
```

ScrapeCreators remains reserve-only, unconfigured, inactive, and not offerable. Automatic or offered paid fallback after Cobalt failure is forbidden.

Reason: preserve zero-client owner UX and prevent silent/accidental paid retrieval.

## D024 - Telegram Public Adapter Is Zero-Credit and No-Auth

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

Supported public Telegram video posts use public web/embed retrieval, trusted Telegram media delivery, AssemblyAI STT, and durable KRCM. Retrieval credits are zero. No login, cookies, session, bot token, or paid fallback is allowed.

Reason: maintain a public-only, credential-free adapter with explicit terminal failure behavior.

## D025 - Local openaiFileIdRefs Attachment Ingestion Is Accepted

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

One current-conversation audio/video attachment may use ChatGPT `openaiFileIdRefs` transport to the isolated backend. The backend accepts trusted OpenAI temporary HTTPS delivery, validates media, limits attachment size to 32 MiB, normalizes audio/video, uses AssemblyAI STT, and stores durable KRCM segments. Retrieval credits are zero. File IDs/signed URLs are not user-visible.

Reason: provide a stable zero-client source path for owner-local media without platform authentication.

## D026 - Copy-Safe Fenced Claim Table Is the Accepted UI Mitigation

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

The normal four-column table remains required. Because ChatGPT whole-response Copy can collapse the rendered table header, the final report also includes an identical fenced `text` table with literal pipe delimiters.

The fenced duplicate passed owner copy testing and is the accepted mitigation. The external rendered-table Copy defect alone does not reopen A10.

## D027 - Release Hold Owner Testing

Decision: APPROVED
Date: 2026-08-27

After A9/A9.10/A10 acceptance, the owner chose continued private testing before release.

```text
merge to main = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Defects are fixed/revalidated in isolated feature branches during the hold.

## D028 - Release Gates Are Independent

Decision: APPROVED
Date: 2026-08-27

Merge, production promotion, external tester onboarding, and public rollout are separate decisions. Approval of one must never be inferred as approval of another.

Reason: repository integration, infrastructure deployment, audience expansion, and public publication carry different risks and controls.

## D029 - Post-AssemblyAI Free-Credit Hybrid C/D Is the Planned Free-First Direction

Decision: APPROVED_PLAN / NOT_IMPLEMENTED
Date: 2026-09-02

The owner selected the combined Hybrid C/D direction as the planned STT architecture **after AssemblyAI free credits are exhausted**.

Current runtime remains unchanged:

```text
active KRC prerecorded provider: AssemblyAI universal-2
Gemini normal prerecorded activation: FALSE
hybrid implementation now: FALSE
```

Planned future routing direction:

```text
Gemini 3.5 Transcribe Live
  -> preferred free route for eligible jobs without word timestamps/diarization

Gemini 3.5 Transcribe unary
  -> free feature route when timestamps and/or diarization are required and quota allows

AssemblyAI universal-2
  -> retained rollback/fallback technology
  -> billable fallback disabled by default after free credits expire
  -> paid use requires separate explicit owner authorization
```

No automatic paid provider fallback is authorized.

Before implementation, mutable assumptions must be revalidated: Gemini model availability, Free Tier limits, language coverage, Live session restrictions, privacy/data-use policy, and actual remaining AssemblyAI balance.

Targeted validation before cutover must cover code-switching, noisy Ukrainian/Russian, multi-speaker media, telephone-bandwidth speech, longer real-world media, numeric/date/name fidelity, and Gemini unary-versus-Live parity where applicable.

Detailed product plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

Technical implementation plan:

`kolemasakar/VoiceBridge` -> `docs/planning/2026-09-02_KRC_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_IMPLEMENTATION_PLAN.md`

This decision does not authorize code changes, provider activation, deployment, merge, external testing, public rollout, or provider-consuming validation now.
