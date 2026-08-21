# A9.3 Durable Managed Media Acceptance

Version: 1.0
Status: PASS / COMPLETE
Accepted: 2026-08-21

## Scope

This record closes A9.3 for the owner-only managed zero-client media path.

Acceptance target:

```text
one approved managed native transcript request
 -> durable KRCM job and timestamped segments
 -> backend process replacement
 -> same job and segments remain readable
 -> duplicate start reuses the same job
 -> duplicate path cannot spend a second provider credit
 -> valid provider configuration restored
```

Production VoiceBridge and both repositories' `main` branches were out of scope and were not modified.

## Accepted runtime

Isolated service:

`voicebridge-krc-media-beta-kolemasakar`

Accepted live VoiceBridge code:

`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`

Acceptance workflow:

`Render MEDIA BETA A9.3 Final Durable Acceptance`

GitHub Actions run:

`32438525793`

Job:

`96644421906`

## Acceptance source

Canonical public video:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

The final durability run used the same public video with a benign query marker to create a clean idempotency key after earlier failed reservation experiments:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg&krc_a93=ru-final-3`

Language hint:

`ru`

## Live result

Managed job:

`KRCM_6f359971-b061-4db8-b4a2-9f6422f351b6`

Result:

```text
start_http: 200
status: COMPLETED
detected_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 99
provider_balance_after: 98
```

No managed AI fallback was authorized.

## Durability and idempotency evidence

All acceptance stages passed:

- isolated runtime identity and exact live code check;
- valid managed capability and Postgres durability flags;
- one explicitly approved Supadata native request;
- durable job read before restart;
- durable timestamped-segment read before restart;
- replacement of the runtime provider key with an intentionally invalid guard value;
- isolated service restart on the exact accepted code;
- durable read of the same job after restart;
- durable read of timestamped segments after restart;
- duplicate start while the provider key was intentionally invalid;
- duplicate returned the existing completed job rather than requiring a new provider call;
- valid provider key restored;
- isolated service restarted on the accepted code after restoration;
- final provider balance changed by exactly one credit: `99 -> 98`.

The invalid-provider duplicate guard is the decisive no-double-spend check: a second real provider request could not have succeeded during that step, yet the duplicate operation succeeded by reusing durable state.

## Reservation parser remediation

Earlier live managed starts returned HTTP 500 before provider credit consumption. The durable reservation implementation used PostgreSQL `INSERT ... ON CONFLICT ... RETURNING`, while the parser previously selected the final non-empty `psql` stdout line unconditionally.

The accepted remediation hardened the parser to select the actual seven-field returned row and ignore unrelated `psql` command-tag lines. A regression test covers a returned row followed by `INSERT 0 1`.

After this parser remediation passed VoiceBridge CI and was deployed to the isolated beta, the final live A9.3 acceptance passed end to end.

## Credit-safety conclusion

A9.3 acceptance demonstrates:

- managed job state is durable across process replacement;
- completed transcript segments are durable across process replacement;
- request idempotency survives process replacement;
- a duplicate request reuses durable state;
- the accepted duplicate path does not require a second provider call;
- the live acceptance consumed exactly the single explicitly approved native credit.

Therefore:

`A9.3 = PASS / COMPLETE`

## Remaining zero-client work

A9.3 does not itself complete the owner product UX.

Next active task:

`A9.5 - Private GPT Action zero-client integration`

The private GPT must use the managed preflight/start/status/segments contract automatically and hide Helper/Job-ID mechanics from the normal user flow.

Final owner acceptance remains separate and requires the real private GPT to complete:

```text
public media URL
 -> analysis choice / required credit approval
 -> no separate media opening
 -> no Helper
 -> no manual Job ID
 -> transcript retrieval
 -> requested Research/Critic workflow
 -> result in the same ChatGPT conversation
```
