# A4 Durable Quota Ledger Restart Acceptance
Фіксує live-перевірку відновлення денного STT quota ledger з durable Postgres після restart isolated MEDIA BETA.

Version: 1.0
Status: PASS
Updated: 2026-08-18

## Scope

This acceptance verifies that a real AssemblyAI STT charge is persisted durably and restored into the in-memory beta quota gate after an isolated backend restart.

It distinguishes two things:
- durable readback of the already completed charged job;
- runtime quota restoration demonstrated by a fresh job created only after the restart.

## Charged audio job before restart

Job:
`KRCC_493fcc82-adea-4de2-aee3-a671c0c54073`

Source:
`https://youtu.be/DZLzmQ2kwaA?si=quota-ledger-restart`

Final pre-restart state:

```text
status=COMPLETED
created_at=2026-08-18T05:17:36.573Z
updated_at=2026-08-18T05:20:37.757Z
language_hint=uk
detected_language=uk
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
duration_seconds=56.376
transcript_characters=555
segment_count=1
stt_seconds_charged=57
beta_quota.daily_limit_seconds=7200
beta_quota.used_seconds=57
beta_quota.remaining_seconds=7143
error=null
```

This is a real provider-backed STT charge, not a synthetic quota reservation.

## Isolated restart

A controlled deploy/restart was triggered only for:
`voicebridge-krc-media-beta-kolemasakar`

Restart commit:
`beebe6a638637e5d4d81a13826371810048d1407`

GitHub Actions / Render control reported the deploy as SUCCESS and ready for post-restart quota readback.

Production VoiceBridge was not targeted.

## Post-restart readback of charged job

The same external job remained readable after restart:

```text
job_id=KRCC_493fcc82-adea-4de2-aee3-a671c0c54073
status=COMPLETED
created_at=2026-08-18T05:17:36.573Z
updated_at=2026-08-18T05:20:37.757Z
transcript_source=assemblyai_stt
provider=assemblyai
provider_data_deleted=true
stt_seconds_charged=57
beta_quota.used_seconds=57
beta_quota.remaining_seconds=7143
segment_count=1
transcript_characters=555
error=null
```

This confirms durable completed-job preservation but by itself is not sufficient to prove runtime quota restoration.

## Fresh job created after restart

Fresh job:
`KRCC_adc4c232-d2df-4382-8bbd-72d7736142ac`

Source:
`https://youtu.be/DZLzmQ2kwaA?si=quota-ledger-after-restart`

Initial state created only after the isolated restart:

```text
status=AWAITING_CLIENT
created_at=2026-08-18T05:28:31.758Z
language_hint=auto
stt_seconds_charged=0
beta_quota.daily_limit_seconds=7200
beta_quota.used_seconds=57
beta_quota.remaining_seconds=7143
error=null
```

Because this new job was created after process replacement, its quota snapshot comes from the restarted runtime. `used_seconds=57` therefore demonstrates that startup restoration loaded the durable daily charge from Postgres into the active `MediaBetaGate`.

## Acceptance result

```text
pre_restart_real_stt_charge=57
post_restart_old_job_charge=57
fresh_post_restart_runtime_used_seconds=57
fresh_post_restart_runtime_remaining_seconds=7143
```

Acceptance marker:

`A4_DURABLE_QUOTA_LEDGER_RESTART_PASS`

## Boundary

This acceptance does not yet validate process replacement while an audio operation is actively uploading or transcribing. That remains a separate A4 edge case.

PR #8 and PR #28 remain draft and unmerged. Production VoiceBridge and the published K-Research & Critic remain unchanged.
