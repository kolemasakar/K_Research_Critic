# Stage132 first actual approved profile E2E acceptance
Date: 2026-11-20
Disposition: FIRST_ACTUAL_PROFILE_E2E_PASS / KRC_ACK / MATRIX_RECONCILIATION_PENDING / PRODUCTION_NO_GO.

## Actual consumer evidence
Owner supplied run44814230633, job136558284228, main workflow_dispatch attempt1, SUCCESS. Head1cc98aec66efc130cb2978460a8319db86be887e. Exact sender blob06791456d393fce797167494b53306fe29645eb1, receiver429895a96b0c17eed4abb9940a37bcf5c176fcf5 and workflow fff782e4416c2344724bdf6e2a6682920b399480 unchanged from reviewed main; intervening commit changes only unrelated standards work. Main/single attempt/exclusive mode, OIDC, Tailnet, checkout and pilot step all PASS; other probes skipped.
20:45:43.6434683Z STAGE132_POST_ATTEMPT request KS-2f5ca3707c62d707cbfb28fe4fc01a9d
20:45:44.7542740Z STAGE132_POST_DESCRIPTOR completed artifact;
20:45:45.0490880Z STAGE132_PILOT_RESULT_SHAPE_VERIFIED exact request/task/SHA, SCIENTIFIC_APPROVAL=false.
Elapsed client markers approximately1.406s for POST plus execution and GET verification, not a load benchmark or general latency guarantee.
Descriptor artifact aec98a70a2838c1a1a2e01e3848a0e73a0a2d9327c677837, research-result.json, application/json, 401 bytes, SHA256 7f629277afada8c375648fbd5eb47f090ee29afd656ca650936915dfb49d28c3, expiry1795812344.6922162.

## Independent KRC producer reconciliation
Actual host20:47:28Z active unchanged broker10179, gateway10271, Reader5267, Sentinel10278 all NRestarts0, no failed units. Trusted show COMPLETED for exact approved profile SHA95a78f606304733d216a632c12163811fe4854a204b285131e8ad60fe4ef2d0a; trusted read exact authoritative descriptor matches client descriptor. Inner result task KS-2f5ca3707c62d707cbfb28fe4fc01a9d-task, operation research.profile.validate, status PENDING, engine schema KRC-CRITICPROFILE-1, profile KS-STAGE127-PILOT-20261120 v1, protocol KRC Core, validation STRUCTURE_VALID, approval_claimed=false, approval_independently_verified=false, scientific_approval=false at both levels. Transport completion is not scientific approval.
Private RequestLedger COMPLETE for principal K_Science and exact RID with matching descriptor. Science replay 2 total from pre-run1, exactly one row for this task and client K_Science, created1795207544. Consent COMPLETED with approved_at1795207224 and consumed_at/completed_at1795207544, no cancellation. Private requests2, science2, consent2, relay nonce2, reader nonce2, all quick_check ok. Relay admission20:45:44.628771Z, reader admissions20:45:44.990252Z and20:45:44.998638Z correlate to descriptor and GET receipt. No new dispatch or repeat POST in reconciliation. Prior approved pilot grant is spent; do not rerun. Full external replay denial for spent grant remains a separate case; one observed execution is not proof of all adversarial scenarios.

## Matrix disposition
Reviewed exact Science draft matrix blob faf392d77dd6181f0f914cbf6a4fafeea44be46c, 48 cases. KRC accepts E2E-01-research.profile.validate-valid_scoped_consent as actual PASS. Prior run44812700859/job136553044875 with broker admission and unchanged science/consent supports E2E-02-research.profile.validate-missing_consent PASS as separately documented a8cbde4a1d43a9a6a6e7287ec0d4a9cfd6d06616. Request K_Science reconcile these two exact cases (2/48 supported, 46 remaining; draft not yet updated by this KRC report), retain scope and other gates. No blanket execution_allowed true. Remaining external profile cases, remaining three operations, bibliography/provider readiness, larger payload/fault tests and production authorization not established by this pilot. Sentinel delivery scope only. No new scientific research, external investigation or provider call authorized or observed. FREE_ONLY_OFFLINE.

Evidence: https://github.com/kolemasakar/K_Science/actions/runs/44814230633/job/136558284228
