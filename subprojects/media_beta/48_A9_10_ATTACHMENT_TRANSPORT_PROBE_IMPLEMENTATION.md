# A9.10 Attachment Transport Probe Implementation

Status: CODE_READY / LIVE_RUNTIME_PROBE_PENDING
Date: 2026-08-26
Scope: isolated owner-only MEDIA BETA

## Purpose

Implement the smallest non-billable runtime probe needed to determine whether the
current private Custom GPT can pass one locally attached audio/video file to the
isolated VoiceBridge backend through the documented GPT Actions
`openaiFileIdRefs` transport.

This record does not mark local attachment transcription as accepted.

## VoiceBridge implementation

Repository: `kolemasakar/VoiceBridge`
Branch: `agent/krc-media-transcript`

Feature-branch implementation head at this checkpoint:

`c1a27ceef4320cba57a558490cfcb5f33f5e8ade`

Added:
- `src/cloud/src/managed_attachment_probe.ts`;
- `src/cloud/src/managed_attachment_probe_http.ts`;
- `src/cloud/tests/managed_attachment_probe.test.ts`;
- `.github/workflows/a9-10-attachment-probe-validate.yml`.

Updated:
- `src/cloud/src/managed_server.ts`.

Endpoint:

`POST /api/v1/media/managed/attachment-probe`

The endpoint is wired only into the isolated managed server path.

## Security boundary

The probe:
- requires the existing private Action bearer;
- requires server-side owner admission to be configured;
- accepts exactly one runtime `openaiFileIdRefs` object;
- rejects the schema-placeholder string form at backend runtime;
- accepts supported audio/video MIME classes only;
- cross-checks filename extension against the declared media class;
- accepts only HTTPS temporary downloads on exact host `files.oaiusercontent.com`;
- requires an OpenAI-style `/file-...` path;
- rejects credentials, non-default ports and arbitrary download hosts;
- uses `redirect: manual` and rejects redirects;
- requests only the first 65536 bytes using HTTP Range;
- independently bounds body reading to 65536 bytes even if Range is ignored;
- applies an 8-second download timeout;
- verifies the downloaded MIME class against the declared audio/video class;
- immediately discards probe bytes;
- does not return file id, filename or signed download URL.

## Cost boundary

The probe does not call AssemblyAI or Supadata and does not create a transcript.

Successful response records:
- `retrieval_credits_charged = 0`;
- `stt_seconds_charged = 0`.

The dedicated validation workflow also rejects accidental STT/full-transcription
references in the probe implementation.

## KRC Action probe package

Repository: `kolemasakar/K_Research_Critic`
Branch: `agent/video-url-research`

Added:
- `gpt_store/actions/media_attachment_probe_openapi.yaml`;
- `tests/test_media_attachment_probe_package.py`.

Probe schema version:

`0.1.0-a9.10-probe`

Operation:

`probeManagedAttachmentTransport`

The OpenAPI schema deliberately follows the documented GPT Actions convention:
`openaiFileIdRefs` is declared as an array of strings in the schema, while the
backend requires the runtime array to contain the OpenAI file-reference object.

The probe schema is a temporary isolated add-on for the feasibility gate. It does
not replace the accepted `media_managed_beta_openapi.yaml` package and does not add
full attachment transcription to the active product contract.

## Required live gate

The next gate requires the actual private owner GPT Builder/runtime:

1. add the isolated probe Action schema while preserving the current managed media Action;
2. upload one small local audio or video file in a fresh GPT conversation;
3. invoke `probeManagedAttachmentTransport` without STT or analysis;
4. require `transport_available=true`;
5. require audio/video MIME consistency;
6. require `retrieval_credits_charged=0`;
7. require `stt_seconds_charged=0`;
8. confirm no Helper, local path, cookie/session, file id or signed URL is exposed.

Only after this live gate passes may A9.10 proceed to full attachment ingestion,
normalization/STT and durable KRCM transcript integration.

## Production boundary

Repository `main`, production VoiceBridge, public GPT sharing, external tester
rollout and legacy Helper behavior remain unchanged. No production deployment or
merge is authorized by this checkpoint.
