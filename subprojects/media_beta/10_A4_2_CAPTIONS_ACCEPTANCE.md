# MEDIA BETA A4.2 Captions Acceptance
Живе підтвердження успішного captions-first отримання субтитрів через browser helper без використання STT.

Version: 1.2
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

The Action-facing status endpoint was read successfully for the same KRCC job and returned:

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

This confirms that the completed captions-first result is visible through the same GPT-facing contract that the closed-beta Action will use.

## GPT-facing segment pagination - page 1

The first Action-facing transcript segment page was read successfully:

```text
cursor=0
next_cursor=50
segment_count_on_page=50
segment_indices=0..49
status=COMPLETED
```

The returned segments include `index`, `start_ms`, `end_ms`, `text`, and nullable `confidence`. Timestamps are ordered and the cursor advances correctly to 50.

The Windows CMD `type` display showed mojibake for Ukrainian UTF-8 text because of the console code page. This is a local display/encoding issue and does not indicate backend transcript corruption.

## Acceptance conclusion

PASS for A4.2 captions-first browser-assisted ingestion, GPT-facing status readback, and first-page segment pagination on the owner acceptance video.

Confirmed properties:
- transcript acquired from YouTube captions through the tester browser path;
- timestamped segments returned;
- Ukrainian automatic captions detected;
- no AssemblyAI STT budget consumed;
- no provider cleanup required because no STT provider transcript was created;
- audio fallback was not used;
- completed job is readable through the Action-facing status endpoint;
- first segment page returns 50 ordered segments and `next_cursor=50`;
- production VoiceBridge and the published K-Research & Critic GPT were not modified.

## Remaining validation

This PASS does not close all MEDIA BETA release gates. Remaining work includes:
- Action-side pagination across remaining segments 50..226;
- additional UK/RU/EN/auto cases;
- audio fallback acceptance for a video with no usable captions;
- provider cleanup verification on the AssemblyAI fallback path;
- >60 minute, source mismatch, concurrency, and daily quota guard tests;
- GPT Builder closed-beta end-to-end test;
- privacy/public-release gates.

`A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS`

`A4_2_GPT_STATUS_READBACK_PASS`

`A4_2_SEGMENT_PAGE_1_PASS`
