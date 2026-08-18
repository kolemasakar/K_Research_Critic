# MEDIA BETA A4.2 Captions Acceptance
Живе підтвердження успішного captions-first отримання субтитрів через browser helper без використання STT.

Version: 1.0
Status: PASS
Acceptance date: 2026-08-18

## Acceptance URL

`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

## Accepted client job

`KRCC_c4d0b996-9500-4a39-a47c-0a873049cfea`

## Helper

`KRC MEDIA BETA Helper 0.2.1`

The direct timed-text route did not provide usable caption data, so the helper used the YouTube transcript-panel fallback through the tester browser.

## Live result

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected/source language=uk
segment_count=227
stt_seconds_charged=0
provider_cleanup=not applicable
```

## Acceptance conclusion

PASS for A4.2 captions-first browser-assisted ingestion on the owner acceptance video.

Confirmed properties:
- transcript acquired from YouTube captions through the tester browser path;
- timestamped segments returned;
- Ukrainian automatic captions detected;
- no AssemblyAI STT budget consumed;
- no provider cleanup required because no STT provider transcript was created;
- audio fallback was not used;
- production VoiceBridge and the published K-Research & Critic GPT were not modified.

## Remaining validation

This PASS does not close all MEDIA BETA release gates. Remaining work includes:
- Action-side readback of completed job and segment pagination;
- additional UK/RU/EN/auto cases;
- audio fallback acceptance for a video with no usable captions;
- provider cleanup verification on the AssemblyAI fallback path;
- >60 minute, source mismatch, concurrency, and daily quota guard tests;
- GPT Builder closed-beta end-to-end test;
- privacy/public-release gates.

`A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS`
