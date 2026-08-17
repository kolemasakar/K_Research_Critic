# MEDIA BETA Decision Log
Реєстр затверджених рішень щодо архітектури, beta-обмежень і майбутнього безкоштовного медіарежиму.

Version: 1.0
Status: ACTIVE
Updated: 2026-08-17

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

Decision: APPROVED

Try usable YouTube captions before any STT fallback.

Reason:

Captions dramatically reduce external STT usage, bandwidth, latency, and free-credit exhaustion.

## D009 - AssemblyAI is beta fallback, not final public dependency

Decision: APPROVED

Use AssemblyAI Universal-2 during closed beta when captions are unavailable.

Reason:

It provides a practical reliable baseline for UK/RU/EN testing, but its free credits are finite and therefore unsuitable as the mandatory permanent public free path.

## D010 - Initial beta resource limits

Decision: APPROVED

- max video: 60 min;
- max concurrent media jobs: 1;
- global AssemblyAI fallback budget: 7200 sec per UTC day;
- fallback audio: mono 16 kHz approximately 32 kbps;
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