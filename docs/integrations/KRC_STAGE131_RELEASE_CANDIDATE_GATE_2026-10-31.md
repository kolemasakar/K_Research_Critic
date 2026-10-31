# KRC Stage131 release-candidate gate — 2026-10-31

Status: RC_SOURCE_ONLY / RELEASE_NO_GO / STAGING ONLY / FREE_ONLY / Production NO-GO.

## Independent partner input
- K_Science 16280b403ad0b58e0518bfa532c93e4de60c61b8: 30 ACK / 2 MISMATCH in 32 isolated scenarios. M1 KRC dispatch mutable task ID. M2 K_Science consumer does not enforce TTL at equality. Stage117 committed TTL and expired/owner/tamper denials accepted.
- K_Sentinel Stage127 audit/design ACK only; no external GET HTTP or science dispatch enabled.

## KRC M1 remediation
- stage131_correlated_dispatch.py now pins expected_task_id before calling dispatch and passes a deep-copied payload, blocking downstream mutation of the admitted payload and false task correlation.
- tests/test_stage131_dispatch_mutation_regression.py demonstrates original task and nested payload unaffected; mutable dispatcher returned new task is denied.
- Focused gate tests: 12/12 PASS. Stage131 + related storage/consent/signer tests: 91/91 PASS.

## Regression and blocking issue
- Attempted full repository pytest with --maxfail=1: 103 PASS, 1 FAIL. tests/test_gpt_store_package.py:test_manifest_preserves_store_first_invariants because public Builder instructions exceed 8000-character hard limit.
- This is outside Stage131 but blocks a full KRC regression signoff. Do not silently truncate builder instructions or publish public GPT without dedicated review.

## Remaining release conditions
1. Independent K_Science replay of M1 at this exact source pin; separately change its TTL validator (M2) using trusted now >= expires_at_epoch denial, publish ACK/MISMATCH.
2. Final inner science response/errors and request correlation semantics agreed by K_Science; source-only test gate alone not a fully wired runtime entrypoint.
3. Bibliography provider remains off by default. Crossref/Europe PMC adapters tested in source; final handler integration, provider security/licensing budget tests still required.
4. Signer remains disabled. Requires real scoped user consent, reviewed signer-enabled entrypoint, custody ownership/replay review; no synthetic grants as real approval.
5. Sentinel authenticated external GET transport not enabled and needs versioned HTTP mapping, principal/repository/workflow scope, TTL/digest/replay/denial tests.
6. Release candidate cannot be installed until full regression, independent partner reviews, exact source-to-installed parity, rollback plan and separate user approval.

## Preservation
- Deployed Stage131 continues pinned at 49f8b857b46ebdf45636deffe90f8a4ee578bddf (last observed active). No service, key, consent, external port or dispatch changes in this session.
- 48 live scientific E2E NOT_RUN.