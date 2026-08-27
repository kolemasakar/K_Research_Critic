# Sustainable Free Media Target
Майбутній опційний напрям зниження залежності від платних або вичерпних STT ресурсів.

Version: 1.1
Status: FUTURE_OPTIONAL / NOT_ACTIVE_DURING_RELEASE_HOLD
Updated: 2026-08-27

## Objective

Explore a later provider-neutral architecture that reduces recurring external STT cost while preserving the accepted KRC workflow and source traceability.

This document is not the current MEDIA BETA architecture and does not authorize provider replacement during the owner-testing hold.

## Current Accepted Baseline

The owner beta currently has accepted managed routes for YouTube/Instagram and accepted AssemblyAI-backed STT after safe retrieval for Facebook, Telegram, and local attachment.

That baseline remains frozen unless a real defect requires a validated change.

## Future Candidate Layers

Potential later architecture may include:

```text
usable captions/transcript
 -> renewable free cloud STT when needed and available
 -> owner-controlled local Whisper fallback where practical
```

Possible cloud/local technologies remain candidates, not commitments. Quotas, file limits, timestamp support, data handling, quality, and provider terms must be re-evaluated when this work is actually opened.

## Provider-Neutral Contract Goal

Any future provider should converge on the same durable transcript abstraction:

```text
status
source metadata
transcript source/provider
detected language/confidence
media duration
segment count
resource/quota diagnostics
error/limitation state
```

Segments retain index, timestamps, text, and confidence where available.

## Migration Rule

Do not replace the accepted current provider path merely because a free alternative exists. A future migration requires:
1. explicit owner decision to open the work;
2. same-sample quality/latency/resource comparison;
3. privacy/security review;
4. provider-neutral persistence compatibility;
5. full media and Research/Critic regression;
6. private owner E2E acceptance.

## Release-Hold Boundary

Current work is `RELEASE_HOLD_OWNER_TESTING`. Sustainable-free redesign is deferred and is not a prerequisite for continued owner testing or for a later release decision unless the owner explicitly makes it one.
