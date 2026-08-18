# MEDIA BETA A4.2 Captions Acceptance
Живе підтвердження успішного captions-first отримання субтитрів через browser helper без використання STT.

Version: 1.3
Status: PASS
Acceptance date: 2026-08-18

## Acceptance URL

`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

## Accepted client job

`KRCC_c4d0b996-9500-4a39-a47c-0a873049cfea`

## Helper

`KRC MEDIA BETA Helper 0.2.1`

The direct timed-text route did not provide usable caption data, so the helper used the YouTube transcript-panel fallback through the tester browser.

## Live helper result

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected/source language=uk
segment_count=227
stt_seconds_charged=0
provider_cleanup=not applicable
```

## GPT-facing status API readback

The Action-facing status endpoint returned:

```text
status=COMPLETED
client_upload_required=false
transcript_source=youtube_captions
caption_type=auto_generated
provider=youtube
detected_language=uk
duration_seconds=663
transcript_characters=8235
segment_count=227
stt_seconds_charged=0
beta_quota.used_seconds=0
beta_quota.remaining_seconds=7200
error=null
```

This confirms that the completed captions-first result is visible through the GPT-facing Action contract.

## Full GPT-facing segment pagination

All 227 transcript segments were read through the Action-facing pagination endpoint with `limit=50`:

```text
page 1: cursor=0   next_cursor=50   count=50 indices=0..49
page 2: cursor=50  next_cursor=100  count=50 indices=50..99
page 3: cursor=100 next_cursor=150  count=50 indices=100..149
page 4: cursor=150 next_cursor=200  count=50 indices=150..199
page 5: cursor=200 next_cursor=null count=27 indices=200..226
```

Acceptance properties:
- total segments read: 227/227;
- no index gaps;
- no duplicate page ranges;
- cursor progression correct;
- final `next_cursor=null` correct;
- each segment contains `index`, `start_ms`, `end_ms`, `text`, and nullable `confidence`;
- timestamps are ordered.

The Windows CMD `type` command initially displayed Ukrainian UTF-8 text as mojibake because of the local console code page. This was a local display issue, not backend transcript corruption.

## Acceptance conclusion

PASS for A4.2 captions-first browser-assisted ingestion, GPT-facing status readback, and complete Action-side segment pagination on the owner acceptance video.

Confirmed:
- transcript acquired from YouTube captions through the tester browser path;
- transcript-panel fallback works when direct timed-text is unusable;
- Ukrainian automatic captions detected;
- 227 timestamped segments exposed through the Action API;
- no AssemblyAI STT budget consumed;
- no provider cleanup required because no STT provider transcript was created;
- audio fallback was not used;
- production VoiceBridge and the published K-Research & Critic GPT were not modified.

## Remaining validation

This PASS does not close all MEDIA BETA release gates. Remaining work includes:
- additional UK/RU/EN/auto cases;
- audio fallback acceptance for a video with no usable captions;
- provider cleanup verification on the AssemblyAI fallback path;
- >60 minute, source mismatch, concurrency, and daily quota guard tests;
- GPT Builder closed-beta end-to-end test;
- privacy/public-release gates.

`A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS`

`A4_2_GPT_STATUS_READBACK_PASS`

`A4_2_SEGMENT_PAGINATION_227_OF_227_PASS`
