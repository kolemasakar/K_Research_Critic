# MEDIA BETA A4.3 Audio Fallback Acceptance
Живе підтвердження browser-audio fallback через AssemblyAI з перевіркою квоти та видалення provider transcript.

Version: 1.0
Status: PASS
Acceptance date: 2026-08-18

## Acceptance URL

Canonical video ID:
`DZLzmQ2kwaA`

Fresh request URL used to avoid idempotent reuse of the prior captions job:
`https://youtu.be/DZLzmQ2kwaA?si=audio2`

## Accepted client job

`KRCC_07774204-5a71-4b79-8129-f73cf4dc164d`

## Helper

`KRC MEDIA BETA Helper 0.2.2`

Helper 0.2.2 was used because 0.2.1 retained the previous COMPLETED UI state when the tester entered a fresh Job ID. Version 0.2.2 persists Job ID changes immediately and allows the new job to start without reinstalling or resetting browser storage manually.

## Live browser flow

The controlled fallback test intentionally did not use the captions button.

Observed sequence:

```text
AWAITING_CLIENT
 -> CAPTURING
 -> UPLOADING
 -> TRANSCRIBING
 -> COMPLETED
```

The helper successfully captured active-tab audio, uploaded it to the dedicated MEDIA BETA backend, and waited for provider transcription.

## Final helper result

```text
status=COMPLETED
detected_language=uk
segment_count=2
stt_seconds_charged=98
provider_cleanup=deleted
```

The 98-second charge reflects the actual captured-audio duration measured after backend normalization. It was not hard-coded to the nominal 60-second operator target.

## Accepted backend path

```text
Edge active-tab audio
 -> MediaRecorder WebM/Opus
 -> browser-only /audio upload
 -> bounded ffmpeg normalization to mono 16 kHz MP3
 -> ffprobe duration measurement
 -> STT quota reservation using measured duration
 -> AssemblyAI universal-2 async transcription
 -> timestamped transcript segments
 -> AssemblyAI transcript DELETE request
 -> provider_data_deleted=true
 -> COMPLETED
```

## Provider cleanup

The helper displayed:

```text
Provider cleanup = deleted
```

This is accepted live evidence that the backend completed its provider transcript deletion request after successful transcription.

## Resource accounting

Before this fallback test, the accepted captions path had consumed zero STT seconds.

For this audio test:

```text
stt_seconds_charged=98
```

The charge is based on the normalized browser capture duration and therefore validates the intended quota-accounting boundary for the fallback path.

A separate Action-facing status readback should still be performed to record the exact post-test `beta_quota.used_seconds` and `remaining_seconds` values in the GPT-facing contract.

## Important restart finding

A previous controlled audio attempt reached browser `UPLOADING` and then failed with:

```text
MEDIA_TRANSCRIPT_NOT_FOUND
The client-assisted media job was not found or expired.
```

The job had not reached the configured 3600-second TTL. The failure occurred because client jobs currently live only in the backend process-memory `Map`; a Render process restart/spin cycle loses those jobs.

This is a known beta durability limitation and is not considered an AssemblyAI/audio-path failure.

Required post-A4 hardening:
- persist KRCC job state outside process RAM, or
- replace the waiting-job dependency with a signed stateless upload ticket/session design.

Until then, owner/tester fallback acceptance should create the KRCC job immediately before browser capture and avoid long idle gaps.

## Acceptance conclusion

PASS for A4.3 browser-audio fallback execution.

Confirmed:
- Helper 0.2.2 can switch from an old completed job to a fresh KRCC job;
- active-tab audio capture works;
- browser audio upload works;
- WebM/Opus normalization and duration probing work;
- AssemblyAI fallback reaches COMPLETED;
- Ukrainian language detection is returned;
- transcript segments are produced;
- measured STT duration is charged;
- provider transcript cleanup is reported as deleted;
- production VoiceBridge and the published K-Research & Critic GPT remain unchanged.

## Remaining A4 validation

This PASS does not close all MEDIA BETA release gates. Remaining work includes:
- Action-facing status readback for this audio job and exact quota readback;
- Action-facing audio segment pagination/readback;
- additional UK/RU/EN/auto cases;
- >60 minute rejection;
- source mismatch rejection;
- concurrency rejection;
- daily quota exhaustion simulation;
- AssemblyAI no-training/privacy verification;
- GPT Builder closed-beta end-to-end test;
- hosted public privacy policy URL;
- Free-plan/paid runtime checks before any public promotion;
- job-state durability across Render restart/spin-down.

`A4_3_AUDIO_FALLBACK_OWNER_ACCEPTANCE_PASS`

`A4_3_ASSEMBLYAI_PROVIDER_CLEANUP_PASS`

`A4_3_STT_DURATION_ACCOUNTING_PASS`
