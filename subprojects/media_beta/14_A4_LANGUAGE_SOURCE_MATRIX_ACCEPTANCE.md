# A4 Language/Source Matrix Acceptance
Фіксує live-перевірки мов, типів субтитрів і великих caption payload у MEDIA BETA.

Version: 1.0
Status: IN_PROGRESS
Updated: 2026-08-18

## Scope

This record covers the remaining A4 language/source matrix after the primary Ukrainian captions, audio fallback, durability, and negative guard acceptance.

Matrix targets:
- Russian captions;
- English captions;
- explicit auto language/track selection beyond the accepted Ukrainian sample;
- manual-caption classification.

It also records defects discovered while executing those cases when the defect is directly relevant to transcript persistence or readback.

## Russian captions case

Status: PASS

Source URL:
`https://www.youtube.com/watch?v=j_R7sBXyRyE`

Job:
`KRCC_eabd86f0-5205-4311-b063-2bb04d4fe1c5`

Initial job state:

```text
status=AWAITING_CLIENT
created_at=2026-08-18T04:20:08.793Z
language_hint=ru
stt_seconds_charged=0
beta_quota.daily_limit_seconds=7200
beta_quota.used_seconds=0
```

Helper path:

```text
Use subtitles
 -> direct caption path not used for final completion
 -> YouTube transcript-panel fallback
 -> auto_generated / ru
 -> POST /captions
 -> COMPLETED
```

Helper-side completion:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=ru
segment_count=524
stt_seconds_charged=0
provider_cleanup=not applicable
```

Final Action-facing durable readback:

```text
status=COMPLETED
created_at=2026-08-18T04:20:08.793Z
updated_at=2026-08-18T04:40:48.824Z
language_hint=ru
detected_language=ru
transcript_source=youtube_captions
caption_type=auto_generated
provider=youtube
duration_seconds=1381
transcript_characters=19206
segment_count=524
stt_seconds_charged=0
beta_quota.used_seconds=0
beta_quota.remaining_seconds=7200
error=null
```

Acceptance result:

`A4_RU_CAPTIONS_PASS`

## Large-payload persistence defect discovered during Russian case

Status: CLOSED

Observed failure before remediation:
- Helper caption submission produced a generic client-assisted request failure;
- Action GET for the new Russian job returned HTTP 500 / `MEDIA_CLIENT_REQUEST_FAILED`;
- an older completed durable control job remained readable;
- the Russian durable row itself remained recoverable as `AWAITING_CLIENT` after remediation deployment.

Root-cause assessment:
- durable persistence serialized job and segment JSON to hex;
- the complete SQL statement, including large hex payload, was passed to `psql` via the `-c` command-line argument;
- sufficiently large caption payloads can exceed the operating-system per-argument length limit and cause process spawn/command failure before Postgres receives the SQL.

Remediation:
- VoiceBridge durable-store SQL is now supplied to `psql` through stdin instead of as one `-c` argument;
- regression coverage was added for the persistence invocation boundary;
- VoiceBridge validation completed successfully;
- isolated MEDIA BETA deployment completed successfully;
- production VoiceBridge was not targeted.

Validated VoiceBridge code commit:
`8962a323abd2d549ad372c51a054f9f5371e9ada`

Post-remediation evidence:
- the same external Russian Job ID remained readable as `AWAITING_CLIENT`;
- original `created_at` remained unchanged;
- retrying `Use subtitles` completed the same job;
- 524 segments / 19206 transcript characters persisted and were readable through the Action API;
- STT charge remained zero.

Closure marker:

`A4_LARGE_CAPTION_PAYLOAD_PERSISTENCE_DEFECT_CLOSED`

## Remaining matrix

Pending:
- English captions case;
- explicit `auto` language/track-selection case beyond the accepted Ukrainian sample;
- manual-caption classification case.

## Boundary

Caption text remains evidence of what the video represents as being said. It is not independent evidence that any material claim in the video is true.

PR #8 and PR #28 remain draft and unmerged. Public K-Research & Critic and production VoiceBridge remain unchanged.
