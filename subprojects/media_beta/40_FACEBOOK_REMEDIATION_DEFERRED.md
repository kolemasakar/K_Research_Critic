# A9.6 Facebook Remediation Deferred

Version: 1.0
Date: 2026-08-23
Status: DEFERRED_BY_OWNER / NOT_ACCEPTED

## Decision

The owner explicitly decided to skip A9.6 Facebook remediation for now.

This is a deferral, not an acceptance and not a closure of the Facebook adapter direction.

## Preserved technical state

The last separately authorized Facebook AI generate attempt failed with:
- `MANAGED_PROVIDER_TRANSCRIPT_INVALID`;
- `segments=0`;
- `credit_charge_uncertain=true`.

Therefore automatic retry or replay remains prohibited.

Nested async-result parser remediation exists in VoiceBridge commit:

`f6b32c2a03425deaecadd10fc902671d62eaab5d`

The latest recorded isolated deploy attempt of that remediation failed.

## No-action boundary while deferred

While this item remains deferred, do not:
- deploy the Facebook parser remediation solely for acceptance testing;
- request a new billable Facebook provider operation;
- replay the prior uncertain-charge operation;
- mark Facebook as accepted;
- expose Facebook as a live-supported MEDIA BETA adapter;
- change production VoiceBridge or repository `main` for this purpose.

## Resume sequence

If the owner later resumes Facebook work, continue from the preserved state:
1. deploy parser remediation without a billable provider call;
2. verify isolated service health/capability;
3. obtain a fresh credit quote;
4. require fresh explicit user authorization;
5. execute one fresh acceptance test;
6. only after backend PASS, run private GPT E2E.

The previous `credit_charge_uncertain=true` operation must never be replayed.

## Current disposition

`A9_6_FACEBOOK = DEFERRED_BY_OWNER_NOT_ACCEPTED`

No replacement next task is implied; the next project direction must be selected explicitly.
