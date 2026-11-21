# Stage133 private KRC project CLI pin and proposal registration
Date: 2026-11-21
Status: PRIVATE_CLI_STAGE133_PIN_PASS / TWO_PROPOSED / ZERO_APPROVED / NO_SCIENCE_SEND / STAGING_ONLY / PRODUCTION_NO_GO

## Root cause
Trusted KRC personal-project command /home/krcops/krc-project-n39-staging/krc-project (UID1002, mode0700) continued importing /home/krcops/krc-project-n39-staging/source/src after the root-installed Stage133 broker and gateway went live. Legacy research route SHA256 f55ff13505ac52aff12b8d235a874e088adebcc44335a64b467dc7f45dd5ef3f lacked the Stage133 external payload conversion and validation. An earlier propose attempt for preflight correctly failed INVALID_PAYLOAD, with zero grants and no dispatch.

## Correction
- New shell wrapper loads only the root-owned immutable Stage133 release as first PYTHONPATH component, with existing KRC private source as a secondary import source for unchanged dependencies; the full immutable release SHA256SUMS is checked on EACH CLI invocation, and the stable release SHA, owner UID1002 and state root custody are checked.
- Release location: /opt/krc-stage133-offline/d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6.
- New Stage133 route SHA256: 93dd1b42d399c06f7e51b61c3984e34fd5e0d6e217e571aee5cc73d572b65df9.
- Wrapper new SHA256: b2ed903043e9bbe31e7eeeeb84117bc263f381e90c46a089ea3b9533c72b912b; private file mode0700.
- Original wrapper SHA256 cfa9a54355f3797533710fc14143f7f7cd3aefd2e732c70854d3b6bc2824ed8c retained as owner-only mode0700 backup /home/krcops/krc-project-n39-staging/krc-project.stage131-backup-20261121.
- Replaced wrapper atomically as UID1002 with fsync; no sudo, no systemd unit file changes, no listener changes, no provider calls or new external ingress.
- Existing database files were NOT copied, edited manually, or opened through a new identity bypass; the only intended writes were two normal PROPOSE transactions through the trusted original state path.

## Pre-registration independent acceptance
- Exact profiles retrieved from K_Science main, original Git blobs 4a64a09cc441fd4187e8287e7969975cd220e35f (preflight) and 3d6b698854c81ba4f8e06b6c24ee29eed0762aa8 (inspection).
- Both canonical profile SHA256 matched the two documented immutable values.
- Actual root-installed Stage133 Python route and the existing private dependency tree validated both profiles against the Stage133 strict schema and existing engine schema.
- Each exact profile passed a source-isolated temporary-state propose/show check and reject-run-without-approval test; no live records written at that stage.
- Revised CLI --help invoked successfully under actual UID1002 through its exact stable path.

## Actual two proposals, NO APPROVAL
Preflight synthetic technical profile:
- operation research.evidence.preflight
- canonical profile SHA256 919f8ab8f73bdfe2f672aa962e5b8948a520d25e5229d6fef508a6fcecad7b8c
- status PROPOSED; exact private request_id stored in owner-only consent.sqlite. No public workflow input is granted by this record.
- all manuscript checks false; source, claim and search lists empty; scientific publication approval false by construction.

Inspection synthetic technical profile:
- operation research.inspection.review
- canonical profile SHA256 984164393ae8120da9ec46ee4fda222d5770311908d4405f85af0c4f40e5a98b
- status PROPOSED; exact private request_id stored in owner-only consent.sqlite. No public workflow input is granted by this record.
- synthetic fake DOI/document trace, trace_verified false. No scientific truth, paper assessment or independence claimed.

Independent post-write checks (2026-11-21):
- Exact CLI show of both records returns status PROPOSED and matching full profiles and SHA256.
- Live SQLite consent and request databases PRAGMA quick_check = ok.
- Exactly one proposed approval record per immutable SHA256; NO status APPROVED or COMPLETED for either; zero request ledger rows and zero artifact associations for both.
- Real four installed services remain ACTIVE with unchanged PIDs (broker19623, gateway19631, reader5267, Sentinel19642) and NRestarts0.
- Unauthorized Stage127 external GET returns expected HTTP401. Existing source and original wrapper untouched except atomic wrapper change.

## Outstanding explicit owner gates
- Owner must REVIEW each complete proposed immutable profile and separately give explicit approval of its exact private RID and SHA256; no approval is inferred from a registration, chat report, or previous spent Stage132 token.
- KRC trusted channel should update proposals to APPROVED using its normal owner-only route only after that approval.
- K_Science PR15 manual workflow remains DEFAULT_OFF; external authenticated E2E must be dispatched only with an exact separately approved profile, a new token, and independent ledger/GET-SHA/semantic check. No duplicate/retry dispatch on uncertainty.
- Prior accepted Science E2E stays 2/48. Production NO-GO. K_Sentinel only transports.

## Rollback
If necessary, an authorized KRC operator can atomically restore the exact original wrapper SHA from the private backup after confirming custody. Changing the CLI is not a reason to restart any live KRC service.
