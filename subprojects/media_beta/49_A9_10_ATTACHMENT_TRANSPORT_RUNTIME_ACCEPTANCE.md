# A9.10 Attachment Transport Runtime Acceptance

Status: LIVE_RUNTIME_TRANSPORT_ACCEPTED / FULL_INGESTION_PENDING
Date: 2026-08-26
Scope: private owner-only MEDIA BETA only

## Result

The zero-client local attachment transport boundary is accepted in the actual private Custom GPT runtime.

A fresh owner conversation attached one local MP4 file of approximately 5 MB and invoked:

`probeManagedAttachmentTransport`

The Action passed a runtime `openaiFileIdRefs` object to the isolated VoiceBridge backend. VoiceBridge successfully reached the temporary OpenAI attachment URL, validated the file as video, verified MIME consistency, and completed the bounded probe without transcription or analysis.

Observed successful result:
- `transport_available = true`;
- `file_class = video`;
- declared/downloaded MIME class: `video/mp4`;
- `mime_consistent = true`;
- `probe_bytes_received = 65536`;
- Range request support confirmed;
- `retrieval_credits_charged = 0`;
- `stt_seconds_charged = 0`.

The source file itself was approximately 5 MB. The 65536-byte result is intentional: the probe requests and reads only the first 64 KiB to prove external reachability and MIME/type integrity while remaining non-STT and non-billable. It is not a file-size truncation or upload failure.

## Runtime host correction

Initial live attempts showed that current ChatGPT runtime uses a regional OpenAI attachment host rather than only the historical exact host documented in older examples.

Observed sanitized runtime host:

`sdmntprcacentral.oaiusercontent.com`

The isolated backend was hardened to accept HTTPS hosts strictly within the `*.oaiusercontent.com` suffix family while continuing to reject lookalike/external hosts, credentials, non-default ports, fragments and redirects. Opaque CDN paths are accepted without echoing file IDs, paths or signed query values.

VoiceBridge isolated deployment validating this boundary:
- branch: `agent/krc-media-transcript`;
- accepted live-gate run: `32993540357`;
- deployment commit family includes regional OpenAI attachment host support;
- validation and isolated Render deployment completed successfully.

## Acceptance gates

### Gate 1 - Builder schema
PASS.

The active managed MEDIA Action exposes:

`POST /api/v1/media/managed/attachment-probe`

operation ID:

`probeManagedAttachmentTransport`

### Gate 2 - current private GPT runtime
PASS.

Confirmed in a fresh owner conversation with a real local MP4 attachment. No Helper, local client, browser extension, platform login, cookies or session was required.

### Gate 3 - processing
PENDING.

The transport probe intentionally downloads only a bounded prefix. The full attachment-ingestion route must now safely download the complete media file, enforce size/duration/type limits, submit the accepted audio stream to AssemblyAI, persist durable KRCM transcript data, and delete temporary media/provider data according to the existing MEDIA BETA privacy contract.

### Gate 4 - private GPT Research/Critic E2E
PENDING.

Required flow:

```text
local attachment
 -> startManagedAttachmentTranscription
 -> complete file download on trusted OpenAI attachment host
 -> AssemblyAI
 -> durable KRCM transcript/segments
 -> CriticProfile gate
 -> explicit user approval
 -> Research/Critic
 -> localized final report
```

## Decision

A9.10 attachment transport feasibility is no longer provisional. The actual private GPT runtime has proven zero-client local audio/video attachment transfer to isolated VoiceBridge.

Proceed to full local attachment ingestion and durable transcription implementation on the isolated feature branches.

Production, public sharing, repository `main`, external tester rollout and the legacy Helper baseline remain unchanged until separately authorized.
