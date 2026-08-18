# MEDIA BETA A4.3 Audio Fallback Acceptance
Живе підтвердження browser-audio fallback через AssemblyAI з перевіркою квоти, Action readback та видалення provider transcript.

Version: 1.2
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

## Action-facing status readback

The GPT-facing status endpoint returned the completed audio fallback result:

```text
status=COMPLETED
client_upload_required=false
transcript_source=assemblyai_stt
caption_type=null
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
detected_language=uk
language_confidence=0.7404
duration_seconds=97.056
transcript_characters=1141
segment_count=2
stt_seconds_charged=98
beta_quota.used_seconds=98
beta_quota.remaining_seconds=7102
error=null
```

This confirms that the browser-audio completion is visible through the same Action-facing contract used by the beta GPT.

## Action-facing segment readback

The GPT-facing segment route returned:

```text
status=COMPLETED
cursor=0
next_cursor=null
segment_count=2
indices=0..1
```

Segment timing readback:

```text
segment 0: start_ms=5347  end_ms=64032
segment 1: start_ms=64032 end_ms=96917
```

Both segments include text and confidence values. Timestamps are ordered and contiguous at the segment boundary. The final `next_cursor=null` is correct because all audio transcript segments fit in the first page.

Observed confidence values were approximately `0.8694` and `0.8469`.

Two replacement-character artifacts (`U+FFFD`) were visible in the returned transcript text. This does not invalidate transport/pagination acceptance, but it is recorded as an STT text-quality anomaly for later provider/pipeline quality investigation before public release.

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

The helper and Action status both confirmed successful provider cleanup:

```text
provider_data_deleted=true
Provider cleanup=deleted
```

This is accepted live evidence that the backend completed its provider transcript deletion request after successful transcription.

## Resource accounting

Before this fallback test, the accepted captions path had consumed zero STT seconds.

For this audio test:

```text
measured_duration_seconds=97.056
stt_seconds_charged=98
beta_quota.used_seconds=98
beta_quota.remaining_seconds=7102
```

The charge is based on the normalized browser capture duration and validates the intended quota-accounting boundary for the fallback path.

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

PASS for the complete A4.3 browser-audio fallback path, including GPT-facing status and segment readback.

Confirmed:
- Helper 0.2.2 can switch from an old completed job to a fresh KRCC job;
- active-tab audio capture works;
- browser audio upload works;
- WebM/Opus normalization and duration probing work;
- AssemblyAI fallback reaches COMPLETED;
- Ukrainian language detection is returned;
- transcript segments are produced and readable through the GPT-facing Action route;
- segment indices/timestamps and final pagination cursor are valid;
- measured STT duration is charged correctly;
- exact daily quota readback is correct;
- provider transcript cleanup is confirmed by the Action contract;
- production VoiceBridge and the published K-Research & Critic GPT remain unchanged.

## Remaining A4 validation

A4.3 transport/processing acceptance is complete. Remaining release gates include:
- additional UK/RU/EN/auto cases;
- >60 minute rejection;
- source mismatch rejection;
- concurrency rejection;
- daily quota exhaustion simulation;
- STT text-quality investigation for observed replacement-character artifacts;
- AssemblyAI no-training/privacy verification;
- GPT Builder closed-beta end-to-end test;
- hosted public privacy policy URL;
- Free-plan/paid runtime checks before any public promotion;
- job-state durability across Render restart/spin-down.

`A4_3_AUDIO_FALLBACK_OWNER_ACCEPTANCE_PASS`

`A4_3_ASSEMBLYAI_PROVIDER_CLEANUP_PASS`

`A4_3_STT_DURATION_ACCOUNTING_PASS`

`A4_3_GPT_STATUS_READBACK_PASS`

`A4_3_GPT_SEGMENT_READBACK_PASS`
