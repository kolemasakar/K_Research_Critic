# KRC MEDIA — Fresh retry COMPLETED; transcript ready; fact-check next

Date: 2026-09-25  
Status: **AUTHORITATIVE CHECKPOINT / FRESH_RETRY_COMPLETED / TRANSCRIPT_READY / ZERO_CREDITS / FACTCHECK_NEXT / FREE_ONLY**

## Durable job status

Read-only `media_youtube_status` for the fresh retry job returned:

```text
job_id=KRCM_a01a95b5-b91a-47b4-9d2d-5323fa36c8a4
status=COMPLETED
provider=gemini
provider_mode=youtube_gemini_direct
provider_model=gemini-3.7-flash
source_url=https://www.youtube.com/watch?v=bu_DYQAKnuQ
segment_count=30
transcript_characters=47289
credits_charged=0
retrieval_credits_charged=0
stt_seconds_charged=0
error=null
provider_http_status=null
provider_error_code=null
provider_error_status=null
```

The provider work completed successfully after the prior retryable HTTP 503 failures.

## Transcript acquisition

Read-only `media_youtube_segments` returned all 30 transcript segments.

The transcript contains the video's full sequence of 42 numbered culinary claims, beginning with potato boiling and ending with the general time/temperature conclusion.

No new provider work was started while reading status or segments.

## Acceptance

```text
WORK_MODE_MEDIA_ACQUISITION=PASS
E1_EXECUTION=PASS
DURABLE_JOB=PASS
RESTART_SAFE_READBACK=PASS
TRANSCRIPT_SEGMENTS=30
TRANSCRIPT_CHARACTERS=47289
CREDITS_CHARGED=0
PAID_FALLBACK=NO
FREE_ONLY=PASS
```

## Next gate

Continue the already-approved research workflow using the obtained transcript only as evidence of what the video says.

Next step:

1. Extract the 42 material factual claims from the transcript.
2. Independently verify each claim according to the approved CriticProfile.
3. Maintain claim-level cross-check ledger.
4. Run Critic review.
5. Produce the Ukrainian final report with the mandatory `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` table.

No new MEDIA provider execution is required.

## Hard boundary

```text
NEW_MEDIA_PROVIDER_WORK=NO
PAID_FALLBACK=NO
PLUGIN_MUTATION=NO
APP_MAPPING_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_220_FRESH_RETRY_COMPLETED
NEXT_GATE=FACTCHECK_42_TRANSCRIPT_CLAIMS
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_220_FRESH_RETRY_COMPLETED_TRANSCRIPT_READY_FACTCHECK_NEXT_2026_09_25`
