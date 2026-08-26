# A9.10 Local Attachment Transport Audit

Feasibility audit for zero-client local audio/video attachment transport from a Custom GPT conversation to the isolated MEDIA BETA backend.

Status: FEASIBILITY_CONFIRMED_IN_CONTRACT / LIVE_RUNTIME_PROBE_REQUIRED
Date: 2026-08-26
Scope: private owner-only MEDIA BETA only

## Key finding

The Custom GPT Actions contract has a documented zero-client file-transfer mechanism. A POST Action may declare a request property named exactly:

`openaiFileIdRefs`

OpenAI documents that files already present in the conversation can then be supplied to the Action as temporary file-reference objects containing:
- `name`;
- `id`;
- `mime_type`;
- `download_link`.

The download URL is documented as valid for five minutes. GPT Actions may include user-uploaded files, DALL-E-generated images, and files created by Code Interpreter.

Official source:
`https://developers.openai.com/api/docs/actions/sending-files`

This removes the architectural need for the A8 browser Helper as the only possible attachment transport.

## Current VoiceBridge state

VoiceBridge already contains a browser-assisted raw-audio ingestion path under:

`/api/v1/media/client-transcriptions/.../audio`

The existing handler:
- reads binary request bodies;
- enforces `MAX_CLIENT_AUDIO_BYTES`;
- uses AssemblyAI through the accepted MEDIA BETA pipeline;
- persists client transcript jobs;
- explicitly reports `requires_browser_helper: true`.

Therefore existing A8 ingestion logic is reusable as processing evidence, but its transport is not the desired A9.10 zero-client boundary.

## Recommended A9.10 transport

Add a dedicated managed Action endpoint, separate from the legacy KRCC browser-client route:

`POST /api/v1/media/managed/attachment`

Recommended operation ID:

`startManagedAttachmentTranscription`

Request shape:

```yaml
type: object
required:
  - openaiFileIdRefs
properties:
  openaiFileIdRefs:
    type: array
    minItems: 1
    maxItems: 1
    items:
      type: string
    description: Exactly one user-uploaded audio or video file from the current ChatGPT conversation.
  language_hint:
    type: string
```

At runtime ChatGPT is expected to replace the declared string item with the documented file-reference object.

## Backend download boundary

The backend must never trust an arbitrary user-supplied URL field.

For the live probe and implementation:
- accept exactly one runtime `openaiFileIdRefs` object;
- require HTTPS;
- require a short-lived OpenAI attachment download URL from the expected OpenAI file-delivery host family;
- do not follow redirects to arbitrary external hosts;
- enforce strict timeout and byte limits while downloading;
- validate MIME type and extension independently;
- never log the signed download URL;
- do not persist the original media file after processing;
- persist only the durable transcript/job metadata required by KRCM;
- do not expose the file ID or signed URL in user-visible output.

## Media processing target

First accepted media classes should be limited to common audio/video containers that the isolated processing path can safely normalize.

Target flow:

```text
user attaches local audio/video in private GPT
 -> Action receives openaiFileIdRefs
 -> VoiceBridge downloads temporary signed attachment
 -> validate size/type
 -> inspect for directly usable text/subtitles when practical
 -> otherwise normalize/extract audio
 -> AssemblyAI EU
 -> durable KRCM transcript
 -> CriticProfile gate
 -> Research/Critic
```

No browser Helper is part of this target flow.

## Current runtime risk

Although the official Actions documentation specifies `openaiFileIdRefs`, OpenAI Developer Community reports in 2026 describe intermittent/current issues where file-reference injection or externally usable signed `download_link` values may fail in some Custom GPT flows. OpenAI Support acknowledged a known issue affecting some file-upload/download Action flows and recommends a fresh reproduction for affected workspaces.

This means architecture is supported by contract, but **current owner runtime must be probed before A9.10 is marked implementable/accepted**.

The probe must distinguish:
1. schema accepted by Builder;
2. Action invocation actually contains non-empty `openaiFileIdRefs`;
3. backend receives a runtime object rather than a literal/local path;
4. `download_link` is externally fetchable by isolated VoiceBridge;
5. audio/video MIME survives the transfer;
6. no credential/session/helper requirement appears.

## Minimal feasibility probe

Implement a non-billable isolated endpoint first:

`POST /api/v1/media/managed/attachment-probe`

Recommended operation ID:

`probeManagedAttachmentTransport`

The probe should:
- accept exactly one `openaiFileIdRefs` item;
- download only a bounded prefix or use a bounded GET sufficient to verify external reachability and MIME/size;
- perform no AssemblyAI submission;
- charge zero credits and zero STT seconds;
- return only safe metadata such as `transport_available`, accepted MIME, byte-bound status, and normalized file class;
- immediately discard downloaded probe bytes.

Only after this live probe passes should the full attachment-transcription operation be added.

## Acceptance gates

### Gate 1 - Builder schema
PASS when the Action editor recognizes `probeManagedAttachmentTransport` with `openaiFileIdRefs`.

### Gate 2 - Current Custom GPT runtime
PASS when a fresh owner conversation with one local audio/video attachment causes a real Action request containing a usable file reference and the isolated backend can download it.

### Gate 3 - processing
PASS when the full attachment route produces AssemblyAI/durable KRCM transcript evidence without Helper/client software.

### Gate 4 - private GPT Research/Critic E2E
PASS when attachment -> transcript -> CriticProfile -> explicit approval -> Research/Critic -> localized final report completes in one conversation.

## Decision

A9.10 transport feasibility is **supported by the documented GPT Actions contract** and should proceed with an isolated live transport probe.

It is not yet runtime accepted because current `openaiFileIdRefs` behavior must be verified in this specific private GPT/account/runtime before processing code or Builder claims are promoted.

Production, public sharing, repository `main`, and legacy Helper behavior remain unchanged.
