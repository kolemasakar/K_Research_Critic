# A9 Managed Provider Credit Consent

Version: 1.0
Status: APPROVED
Approved: 2026-08-20

## Purpose

Restore the zero-client public media flow when direct Render-to-YouTube access is blocked by datacenter anti-bot enforcement.

Primary managed provider for the closed beta: Supadata.

Initial provider mode: `native` only.

## Credit consent rule

No transcript-credit operation may start without explicit user approval.

Required user-facing preflight fields:

- available provider credits;
- estimated credits for the requested operation;
- estimated remaining credits after the operation;
- explicit options `1 - YES`, `2 - NO`.

Example:

```text
Available: 100 credits
Expected cost: 1 credit
Expected balance after processing: 99 credits
Continue?
1 - YES
2 - NO
```

The backend must treat the user approval as a hard maximum credit budget for that operation.

## Native transcript gate

Supadata `mode=native` is the first managed operation.

Current pricing contract verified on 2026-08-20:

- native transcript request: 1 credit;
- a `transcript-unavailable` result also costs 1 credit;
- response header `x-billable-requests` reports the billed amount.

The first consent may authorize at most 1 credit.

## AI fallback gate

Automatic fallback from `native` to managed AI transcription is prohibited.

If native transcript is unavailable:

```text
native request
 -> 1 credit consumed
 -> STOP
 -> calculate/obtain AI cost estimate
 -> show current balance and estimated AI cost
 -> request a second explicit consent
 -> only then may AI generation start
```

Managed AI generation currently costs 2 credits per video minute. The AI fallback contract must be implemented and accepted separately before use.

## Provider boundary

- provider API key remains server-side;
- testers never provide provider API keys;
- public media URLs only;
- no YouTube cookies, authenticated browser sessions, personal account tokens, or paid residential proxy are introduced by this decision;
- provider usage is isolated to MEDIA BETA until acceptance is complete.

## A9.2R implementation sequence

```text
A9.2R.1 Supadata provider + native credit consent contract
A9.2R.2 isolated HTTP/Action integration
A9.2R.3 exact blocked-video live acceptance
A9.2R.4 explicit AI fallback consent decision/implementation
```

Acceptance video for the managed-provider proof:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

The same URL previously failed on direct Render ingestion with the YouTube bot/login challenge and zero STT charge.

## Acceptance conditions for A9.2R.3

- no Helper;
- no user-side video opening;
- no cookies/login/session import;
- preflight reports current provider credit balance;
- no transcript request before explicit consent;
- `mode=native` is enforced for the first request;
- billed credits are captured from the provider response;
- timestamped transcript segments are returned;
- no automatic AI fallback;
- production VoiceBridge is not modified.
