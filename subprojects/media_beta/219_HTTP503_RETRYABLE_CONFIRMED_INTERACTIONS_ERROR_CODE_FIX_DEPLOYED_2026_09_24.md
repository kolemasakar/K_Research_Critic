# KRC MEDIA — HTTP 503 retryable confirmed; Interactions error-code diagnostics fix deployed

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / HTTP503_RETRYABLE_CONFIRMED / INTERACTIONS_ERROR_CODE_FIX_DEPLOYED / NO_NEW_PROVIDER_RETRY / FREE_ONLY**

## Read-only lookup of fresh failed job

```text
job_id=KRCM_d4545ce4-0971-408e-ae13-bcb01d4433ca
status=FAILED
provider=gemini
provider_mode=youtube_gemini_direct
provider_model=gemini-3.7-flash
provider_http_status=503
provider_error_status=null
error.code=GEMINI_YOUTUBE_FAILED
error.retryable=true
credits_charged=0
retrieval_credits_charged=0
stt_seconds_charged=0
segment_count=0
transcript_characters=0
source_url=https://www.youtube.com/watch?v=bu_DYQAKnuQ
```

This confirms the upstream failure is retryable HTTP 503 and that URL canonicalization is active.

## Diagnostic defect found

The current Gemini Interactions API error schema uses:

```json
{
  "error": {
    "code": "service_unavailable",
    "message": "..."
  }
}
```

The prior diagnostic patch inspected legacy `error.status`, so `provider_error_status=null` did not mean the provider returned no machine code; it meant the adapter inspected the wrong field for current Interactions API responses.

## VoiceBridge fix

VoiceBridge PR #53:

```text
repo=kolemasakar/VoiceBridge
PR=53
title=Diag: preserve Gemini Interactions API error code
merged=true
merge_commit=d3873bf13e60c4932ab08cae449c924051be4a37
```

Changes:

1. Add `provider_error_code` from current Interactions API `error.code`.
2. Retain `provider_error_status` only as legacy compatibility metadata.
3. Preserve existing upstream HTTP status and retryability behavior.
4. Do not persist raw provider error messages.

## Validation

```text
TypeScript build=PASS
targeted public_gemini_youtube tests=9/9 PASS
diff_files=2
provider_work_started_by_validation=0
```

A full-suite local run encountered the pre-existing open-handle stall after unrelated streaming tests; it was not counted as PASS.

## Deployment

```text
VoiceBridge service=srv-da1kic5bedkc73d6fk60
deploy=dep-daqp1iou01pc73fgjb00
commit=d3873bf13e60c4932ab08cae449c924051be4a37
status=LIVE
```

No new Gemini provider attempt was executed after this deployment.

## Current interpretation

```text
PLUGIN_WORK_MODE=PASS
R3C=PASS
E1=PASS
VOICEBRIDGE_ROUTING=PASS
UPSTREAM_RESULT=HTTP 503
RETRYABLE=true
PAID_FALLBACK=NO
CREDITS_CHARGED=0
ROOT_CAUSE_CLASS=TRANSIENT_GEMINI_SERVICE_UNAVAILABLE
```

The exact provider machine code for a future failure can now be persisted in `provider_error_code`.

## Next gate

No automatic retry.

A future retry requires new explicit Gemini Free Tier consent and a separate E1 consequential confirmation.

Recommended operational policy: wait before retrying; if retrying, use one controlled attempt only, then inspect read-only lookup.

## Resume

```text
RESUME_FROM=CHECKPOINT_219_HTTP503_RETRYABLE_CONFIRMED
NEXT_GATE=WAIT_OR_EXPLICIT_SINGLE_RETRY
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_219_HTTP503_RETRYABLE_CONFIRMED_INTERACTIONS_ERROR_CODE_FIX_DEPLOYED_2026_09_24`
