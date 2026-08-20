# MEDIA BETA Credential Attribution Correction

Version: 1.0
Status: CANONICAL_CORRECTION
Updated: 2026-08-20

## Purpose

Correct the credential attribution of the MEDIA BETA owner-operated acceptance tests without changing their technical results.

## User correction

The project owner confirmed that all prior MEDIA BETA live tests were executed by the owner/operator using the access code designated for `Tester 1`, not the separate owner-designated code.

Therefore:

- the technical results of A4, A5, A6 and the A7 EU Audio fallback live validation remain valid;
- the credential actually exercised in those live runs was the `Tester 1` code;
- the separate owner-designated beta code has not yet been independently live-validated;
- prior wording such as `owner code acceptance` or wording that could imply the owner-designated credential was used is incorrect;
- the correct description is `owner/operator acceptance performed using the Tester 1 credential`;
- these owner-operated runs do not count as independent external Tester 1 rollout evidence, because the human operator was still the owner;
- A7 therefore remains `READY_FOR_TESTER1`, not `COMPLETE`.

## Impact on acceptance status

No technical acceptance is revoked.

A5/A6 remain PASS because the Builder, Action, Helper, CriticProfile gate, approval transition, Research/Critic path and finalization were exercised successfully with a valid allowlisted tester credential.

The A7 EU Audio privacy gate remains PASS because provider routing, measured STT charge, provider cleanup and completion behavior are independent of whether the allowlisted credential was labeled owner or Tester 1.

## Credential-specific status

```text
Tester 1 credential:
- live-used extensively by owner/operator
- Action start: PASS
- captions-first: PASS
- Audio fallback: PASS
- EU AssemblyAI fallback: PASS

Owner-designated credential:
- live validation: NOT YET PERFORMED

Independent external Tester 1 human run:
- NOT YET PERFORMED
- required before A7 can be marked COMPLETE
```

## Canonical interpretation rule

Where older acceptance documents say `owner acceptance`, interpret `owner` as the human operator unless the text explicitly states which beta credential was used.

For credential identity, this correction supersedes ambiguous attribution in earlier A5/A6/A7 records.

No plaintext beta code is stored in this record.
