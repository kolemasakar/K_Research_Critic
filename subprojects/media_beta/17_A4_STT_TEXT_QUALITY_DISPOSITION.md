# MEDIA BETA A4 STT Text-Quality Disposition
Live disposition of the previously observed `U+FFFD` replacement-character anomaly in AssemblyAI audio-fallback transcript text.

Version: 1.0
Status: PASS_NON_REPRODUCIBLE_ANOMALY
Disposition date: 2026-08-20

## Scope

A4.3 owner acceptance on 2026-08-18 recorded two `U+FFFD` replacement characters in the returned AssemblyAI transcript text. Transport, quota, pagination, timestamps, provider cleanup, and Action readback otherwise passed.

This validation determines whether the replacement characters are reproducible in the current audio-fallback pipeline and whether they should block A4 exit.

## Original observation

Original A4.3 job:
`KRCC_07774204-5a71-4b79-8129-f73cf4dc164d`

Canonical earlier observation:

```text
segment_count=2
U+FFFD observed=2
```

The complete original transcript is intentionally not stored in the checkpoint documentation.

On 2026-08-20 the original job could no longer be re-read from the Action API because it had expired:

```text
MEDIA_TRANSCRIPT_NOT_FOUND
The client-assisted media job was not found or expired.
```

Therefore the original provider payload cannot be re-inspected and root-cause attribution for that historical sample is not possible.

## Fresh control jobs

Two later independent successful AssemblyAI audio-fallback jobs were read through the Action-facing segment endpoint and scanned for Unicode replacement character `U+FFFD`.

Control job 1:
`KRCC_62dedd79-a1db-4e4d-84b8-e28ad44a6a78`

Result:

```text
segments=2
U+FFFD=0
```

Control job 2:
`KRCC_8b256d21-f190-4b45-a59a-8d092e0fbb43`

Result:

```text
segments=2
U+FFFD=0
```

Combined fresh result:

```text
successful_control_jobs=2
returned_segments=4
U+FFFD_total=0
```

## Pipeline review

Current VoiceBridge audio-fallback code reads the AssemblyAI HTTP response as text and parses JSON with the platform JSON parser. The transcript text and AssemblyAI word text are then copied into transcript fields/segments without an explicit lossy character-set conversion.

The available evidence therefore does not show a deterministic encoding/transcoding defect in the current VoiceBridge transport, segmentation, persistence, or Action-readback path.

This does not prove that the historical two replacement characters originated inside AssemblyAI: the original raw provider response has expired and was not retained. Root cause remains unconfirmed.

## Disposition

Status: NON_REPRODUCIBLE QUALITY ANOMALY / NOT AN A4 BLOCKER.

Accepted rationale:
- the anomaly was real and remains documented;
- two fresh successful AssemblyAI jobs independently returned zero `U+FFFD` artifacts;
- the anomaly is not reproducible in the current pipeline;
- no deterministic VoiceBridge encoding defect is supported by current evidence;
- original raw provider data is unavailable, so provider attribution is not asserted;
- continued closed-beta monitoring remains appropriate.

A future recurrence should capture a bounded diagnostic signal before provider cleanup, sufficient to distinguish provider-output corruption from downstream transport/persistence without storing the full transcript in project checkpoints.

## A4 conclusion

The STT replacement-character investigation is dispositioned and no longer blocks A4 exit.

Acceptance markers:

`A4_STT_REPLACEMENT_CHARACTER_INVESTIGATION_PASS`

`A4_STT_U_FFFD_NON_REPRODUCIBLE`

`A4_STT_TEXT_QUALITY_DISPOSITION_PASS`
