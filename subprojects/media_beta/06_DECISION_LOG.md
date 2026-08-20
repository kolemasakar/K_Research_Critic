# MEDIA BETA Decision Log
Реєстр затверджених рішень щодо архітектури, beta-обмежень і майбутнього безкоштовного медіарежиму.

Version: 1.3
Status: ACTIVE
Updated: 2026-08-20

## D001 - Media input is additive

Decision: APPROVED

The media workflow extends K-Research & Critic and does not replace the existing text workflow.

Reason:

Preserve production reliability and allow media failures to degrade only the optional media path.

## D002 - CriticProfile gate remains mandatory

Decision: APPROVED

Transcript acquisition and material-claim inventory may occur before approval. Independent claim research may not.

Reason:

Preserve the core K-Research & Critic contract:

`Supervisor proposes -> User approves/edits -> Critic executes`.

## D003 - Transcript is not independent evidence

Decision: APPROVED

A transcript is evidence of what was said, not evidence that the statement is true.

Reason:

Prevents self-corroboration and false confidence.

## D004 - Closed MEDIA BETA is first priority

Decision: APPROVED

Before public/free scaling work, deploy a controlled beta for the owner and up to three testers.

Reason:

Obtain real reliability and resource measurements with bounded exposure.

## D005 - Beta uses separate product identity

Decision: APPROVED

Create `K-Research & Critic - MEDIA BETA` separately from the published GPT.

Reason:

Avoid risking the public text product during media validation.

## D006 - Beta backend is isolated from production VoiceBridge

Decision: APPROVED

Use a dedicated Render service rather than deploy beta code over `voicebridge-cloud-us`.

Reason:

Media fetch/STT instability must not affect validated real-time VoiceBridge.

## D007 - Beta tester admission uses per-tester access codes

Decision: APPROVED

Target: owner + three testers.

Reason:

Personal Custom GPT sharing cannot be relied upon as a strict per-person access-control mechanism. Server-side beta admission provides revocable control over expensive media jobs.

## D008 - Subtitle-first

Decision: SUPERSEDED_FOR_CLIENT_HELPER_BY_D016

Original decision: try usable YouTube captions before STT fallback.

The principle remains valid when a reliable transcript/caption is directly available, but server-side YouTube acquisition from Render is blocked and the current A4.2 browser helper does not yet implement client-side caption extraction.

## D009 - AssemblyAI is beta fallback, not final public dependency

Decision: APPROVED

Use AssemblyAI Universal-2 during closed beta when transcript/caption intake is unavailable.

Reason:

It provides a practical reliable baseline for UK/RU/EN testing, but its free credits are finite and therefore unsuitable as the mandatory permanent public free path.

## D010 - Initial beta resource limits

Decision: APPROVED

- max video: 60 min;
- max concurrent media jobs: 1;
- global AssemblyAI budget: 7200 sec per UTC day;
- STT audio: mono 16 kHz approximately 32 kbps;
- transcript/job TTL: approximately one hour.

Reason:

Protect Render memory/bandwidth and AssemblyAI free credits during beta.

## D011 - User does not provide provider API keys

Decision: APPROVED

Developer/provider credentials remain server-side. Testers only provide their beta admission code.

Reason:

Better usability and security; preserves intended GPT Store experience.

## D012 - Do not store full transcript in checkpoint

Decision: APPROVED

Checkpoints may retain derived claims/source references but not the complete transcript or beta access code.

Reason:

Reduce persistence, privacy exposure, and checkpoint size.

## D013 - Target post-beta architecture is sustainable free hybrid

Decision: APPROVED_DIRECTION

Preferred target:

```text
YouTube captions
 -> Cloudflare Workers AI Whisper when required and quota available
 -> local Whisper fallback where practical
```

AssemblyAI may remain as comparator/emergency fallback but should not be required for the public free path.

Reason:

Remove the one-time external STT-credit exhaustion problem while keeping direct YouTube-link UX.

## D014 - "Unlimited free" is interpreted operationally

Decision: APPROVED_DIRECTION

The project cannot guarantee literally unlimited use. The target is to eliminate permanent paid/exhaustible external STT credits and make remaining limits renewable daily or dependent on owner-controlled local compute.

Reason:

All hosting, networks, source platforms, and ChatGPT plans have physical or policy limits.

## D015 - Changes to beta limits require explicit decision update

Decision: APPROVED

Do not silently raise tester count, duration, concurrency, or daily STT budget.

Reason:

These parameters directly affect cost/resource risk and reliability.

## D016 - Client/browser-assisted ingress replaces cloud YouTube acquisition for A4 beta

Decision: APPROVED

For the current closed beta, use a separate browser helper to capture the same active YouTube tab through the tester browser/network path and upload captured audio to the isolated beta backend.

The beta GPT creates `KRCC_...` jobs with `AWAITING_CLIENT`. The helper uses the tester beta code, but never receives the server-side Action bearer token or provider API key.

Direct reliable transcript/caption intake remains preferred when available. Client-side caption extraction is a planned optimization, not an implemented A4.2 capability.

Reason:

Three Render/cloud acquisition attempts, including a correctly wired current PO Token Provider, were blocked by YouTube datacenter-IP anti-bot enforcement. Client-assisted ingress avoids personal YouTube cookies, paid residential proxy infrastructure, and changes to the validated production VoiceBridge extension while preserving the Free Render beta target.

## D017 - Zero-client media router is public-only and multi-platform

Decision: APPROVED
Approved: 2026-08-20

The final zero-client media architecture is not limited to YouTube. It should use a platform-neutral MediaSourceRouter with adapters for explicitly validated public media URL types.

Initial target adapters:
- YouTube public videos;
- Instagram public Reels/posts containing video;
- Facebook public Video/Reels;
- Telegram public posts containing video.

Later public adapters may be added independently after validation.

Access boundary:
- public URLs only;
- no user logins, passwords, cookies, authenticated browser sessions, account tokens, or imported session state;
- no private/friends-only/group-only/account-gated content;
- do not ask the user for platform credentials;
- if access requires authentication, fail explicitly with `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

Support must be declared per public URL/content type, not as blanket support for an entire platform.

Reason:

The desired product UX is source-agnostic: paste a public media link, select the analysis mode, and receive the result in ChatGPT with no extra browser/media actions. A public-only boundary keeps the system simpler, safer, easier to operate from mobile, and avoids credential/session storage and private-content access risks.

## D018 - Local video/audio upload is an approved media ingress

Decision: APPROVED
Approved: 2026-08-20

The MediaSourceRouter should support a separate `local_upload` ingress for video/audio files explicitly attached by the owner from local/device storage.

Target behavior:
- accept local video and audio attachments through a future validated ChatGPT/Custom GPT file-ingest transport;
- validate file type, size, and duration before processing;
- prefer usable embedded subtitle/text tracks before STT;
- otherwise extract/normalize audio and use the accepted EU STT path during the current beta architecture;
- converge on the same normalized MediaAsset/transcript/job contract used by public URL adapters;
- do not require any platform login, cookies, browser session, or account token;
- do not durably retain the original media file after processing unless a future explicit retention decision changes this rule.

The public-only rule in D017 applies to remote platform URL adapters and does not block owner-supplied local files.

Initial local-upload scope is analysis of spoken/transcribed content. Visual-frame evidence extraction from video is a separate future capability and requires its own acceptance scope.

Implementation constraint:

Approval is architectural only. The actual ChatGPT attachment-to-Action/backend transport, supported file types, practical size limits, desktop/mobile behavior, and deletion guarantees must be live-validated before `local_upload` is marked supported.

Reason:

Local upload avoids source-platform anti-bot/authentication dependencies and provides a stable source path for media already available on the owner's device. Reusing the same MediaSourceRouter and normalized transcript contract prevents a separate analysis pipeline and keeps Research/Critic source-agnostic.
