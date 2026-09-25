# KRC MEDIA — Gemini failure diagnostics fix deployed; fresh retry authorization next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / FAILED_JOB_CONFIRMED / DIAGNOSTIC_FIX_VALIDATED / VOICEBRIDGE_DEPLOYED / FRESH_RETRY_AUTHORIZATION_REQUIRED / FREE_ONLY**

## Failed job evidence

Read-only `media_youtube_lookup` returned:

```text
job_id=KRCM_3d55d447-f32d-4d3b-8584-8030abc202e3
status=FAILED
provider=gemini
provider_mode=youtube_gemini_direct
provider_model=gemini-3.7-flash
error.code=GEMINI_YOUTUBE_FAILED
error.retryable=false
free_retrieval_error_code=GEMINI_YOUTUBE_FAILED
credits_charged=0
retrieval_credits_charged=0
stt_seconds_charged=0
segment_count=0
transcript_characters=0
reused=true
```

The old persisted `retryable=false` is not authoritative for the original Gemini response because the adapter previously forced failed jobs to `retryable=false`.

## Contract verification

Current Google documentation confirms:

```text
Interactions API supports gemini-3.7-flash
public YouTube video URL input is supported
video input shape: {type:"video", uri:"https://www.youtube.com/watch?v=..."}
```

Therefore the provider contract is structurally supported; exact upstream failure remains unknown.

## VoiceBridge fix

VoiceBridge PR #52:

```text
repo=kolemasakar/VoiceBridge
PR=52
title=Diag: preserve Gemini YouTube upstream failure metadata
base=agent/krc-media-gemini-migration
merged=true
merge_commit=1e729ad8a7efc3bd3710510574ba24dd777ebea6
```

Changes:

1. Preserve actual upstream Gemini HTTP status on failed jobs.
2. Preserve sanitized Gemini error status such as `RESOURCE_EXHAUSTED`, `PERMISSION_DENIED`, or `INVALID_ARGUMENT`.
3. Preserve real retryability instead of forcing `false`.
4. Canonicalize `youtu.be/<id>?...` to `https://www.youtube.com/watch?v=<id>` before Gemini Interactions calls.
5. Never persist Google's raw error message.

Canonicalization is compatibility hardening, not a proven root-cause fix.

## Validation

Local exact-branch validation on HP-OMEN:

```text
npm run build=PASS
tests=269
pass=269
fail=0
targeted public_gemini_youtube=8/8 PASS
```

Temporary validation clone was under a project subdirectory, not a drive root.

## Deployment

VoiceBridge Render:

```text
service=srv-da1kic5bedkc73d6fk60
deploy=dep-daqolgek1f9s73ctv8pg
commit=1e729ad8a7efc3bd3710510574ba24dd777ebea6
status=LIVE
health=200
```

No provider retry was executed after deployment.

## Next gate

A fresh provider attempt is required to observe the newly preserved upstream diagnostics.

Because the previous job FAILED and the free-tier contract requires explicit fresh consent for retry, no automatic retry is permitted.

On explicit user authorization:

1. use Work mode;
2. repeat the YouTube fact-check request;
3. approve CriticProfile;
4. explicitly consent to Gemini Free Tier;
5. approve the separate E1 consequential confirmation once;
6. if the job fails, immediately run read-only `media_youtube_lookup`;
7. inspect `provider_http_status`, `provider_error_status`, and `error.retryable`.

## Hard boundary

```text
AUTOMATIC_RETRY=NO
NEW_PROVIDER_WORK=REQUIRES_EXPLICIT_USER_AUTHORIZATION
PAID_FALLBACK=NO
PLUGIN_MUTATION=NO
APP_MAPPING_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_217_GEMINI_DIAGNOSTIC_FIX_DEPLOYED
NEXT_GATE=EXPLICIT_FRESH_E1_RETRY_AUTHORIZATION
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_217_GEMINI_FAILURE_DIAGNOSTIC_FIX_DEPLOYED_RETRY_AUTHORIZATION_NEXT_2026_09_24`
