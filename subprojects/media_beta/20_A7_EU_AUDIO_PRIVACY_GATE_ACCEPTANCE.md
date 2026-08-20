# A7 EU Audio Privacy Gate Acceptance

Version: 1.0
Status: PASS
Acceptance date: 2026-08-20

## Purpose

Close the controlled-rollout privacy gate for the client-assisted Audio fallback path before external tester use.

The captions-first path was already accepted and does not invoke AssemblyAI. This record covers only the browser Audio fallback path.

## Provider boundary

The isolated MEDIA BETA runtime was configured with:

`KRC_MEDIA_ASSEMBLYAI_BASE_URL=https://api.eu.assemblyai.com`

The deployed VoiceBridge beta commit was:

`7a61790221b6f75c14293360002794208efd813f`

Render deploy:

`dep-da3f2te417fc73e600ng`

Final deploy status:

`live`

Production VoiceBridge and the VoiceBridge `main` branch were not targeted.

## Runtime health

After deployment, the isolated beta health endpoint returned:

- `status=ok`;
- service version `0.6.0`;
- `media_client_ingest.configured=true`;
- `durable_store=postgres`;
- `restart_resilient_waiting_jobs=true`;
- `durable_quota_ledger=true`.

## Live EU Audio fallback job

Accepted Job ID:

`KRCC_a79ad701-d5a0-40ca-91f8-6fbdfc6c3bc6`

Source marker:

`https://youtu.be/DZLzmQ2kwaA?si=a7-eu-audio-20260820`

Initial state:

```text
status=AWAITING_CLIENT
stt_seconds_charged=0
quota used=422
quota remaining=6778
```

The owner invoked Helper Audio fallback rather than captions.

Final Action-facing state:

```text
status=COMPLETED
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
detected_language=uk
language_confidence=0.695
duration_seconds=122.292
stt_seconds_charged=123
transcript_characters=1608
segment_count=3
error=null
quota used=545
quota remaining=6655
```

## Quota validation

```text
used before=422
used after=545
delta=123
stt_seconds_charged=123
ceil(122.292)=123
```

The durable quota increment exactly matched the measured rounded-up audio duration.

## Privacy disposition

Current AssemblyAI documentation states that files submitted through its European servers are not used for model training. The isolated MEDIA BETA client-assisted Audio fallback is now configured to the documented EU Async STT base endpoint and the live job above completed successfully through that configuration.

Therefore the A7 AssemblyAI EU/no-training deployment gate is accepted for controlled beta tester use.

This acceptance does not remove the requirement to re-check provider terms/configuration before any future public production promotion.

## Acceptance result

`A7_EU_AUDIO_FALLBACK_PRIVACY_GATE_PASS`

External tester Audio fallback may now be enabled within the controlled beta limits.

Remaining A7 work is operational tester rollout and observation, not provider-routing validation.

## Boundaries

- Captions remain the preferred path and consume zero AssemblyAI STT seconds.
- Audio fallback remains limited to 7200 seconds per UTC day and one concurrent client media job.
- Normal provider deletion must continue to report `provider_data_deleted=true` for accepted normal-completion cases.
- Hard process loss may still leave provider cleanup unconfirmed; that remains separate release hardening.
- No tester code, Action bearer secret, Render API key, or AssemblyAI API key is stored in this record.
