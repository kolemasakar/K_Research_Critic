# A9.7 Facebook Cobalt Live Acceptance

Status: LIVE_ACCEPTED_FREE_PATH
Date: 2026-08-23
Scope: isolated owner-only MEDIA BETA

## Accepted path

`Facebook public URL -> VoiceBridge -> Cobalt -> media asset -> AssemblyAI STT -> durable KRCM transcript`

The accepted scope is the free Cobalt retrieval path only. The ScrapeCreators paid fallback is not configured and is not live accepted. It remains a separately consent-gated maximum-one-credit contingency path.

## H1 evidence

Test URL: public Facebook Reel `1114235920664408`.

Observed result:
- HTTP start: 200;
- job: `KRCM_0d2a512d-c90d-4b41-87b7-3d3f47d258bd`;
- final status: `COMPLETED`;
- provider mode: `facebook_retrieval_stt`;
- retrieval provider: `cobalt`;
- retrieval credits charged: 0;
- STT provider: `assemblyai`;
- STT seconds charged: 23;
- durable segment count: 1;
- transcript characters: 101;
- durable job reread: `COMPLETED`;
- segments read: HTTP 200;
- terminal error: none.

The first H1 workflow attempt failed before the HTTP start because its PR-job Action token was empty. No Facebook, Cobalt, or AssemblyAI request occurred in that failed setup attempt. The corrected H1 run obtained the already configured Action token server-side from Render and performed the single real acceptance start.

## Safety and cost boundary

No ScrapeCreators request was made. No Supadata request was made. No paid Facebook continuation was invoked. AssemblyAI ran only because Cobalt returned media. Production VoiceBridge, repository main branches, and merge state were unchanged.

## Historical A9.6 distinction

The earlier A9.6 Supadata Facebook route remains not accepted. Its failed/empty transcript behavior and non-replay rules remain historical evidence. A9.7 does not retroactively mark A9.6 complete.

## Current product state

Facebook is live accepted for the isolated owner beta only through the free Cobalt path. The actual private Custom GPT Builder still requires the A9.7-C schema/instruction update before private-GPT Facebook E2E can be marked accepted.
