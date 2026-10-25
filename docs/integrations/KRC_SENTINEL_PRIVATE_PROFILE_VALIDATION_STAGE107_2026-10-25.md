# KRC №107 — private CriticProfile shape validation

2026-10-25. Isolated KRC research checkout on krc-cobalt.

`research.profile.validate` now has a bounded offline handler in `science_dispatch.py`, supported by `profile_validator.py`. Payload requires `critic_profile` object with non-empty `profile_id`, `version`, `protocol`, `topic`. Allowed protocols: `KRC Core`, `Scholarly Research`. Optional `user_profile_approved` is a claimed boolean, NOT independently verified owner consent. Result: `{schema:'KRC-CRITICPROFILE-1',profile_id,profile_version,protocol,validation:'STRUCTURE_VALID',approval_claimed,approval_independently_verified:false,scientific_approval:false}` wrapped in dispatcher `{task_id,operation,status,engine_result,scientific_approval:false}`.

Signed envelope `krc-science/1`, ACL, time and replay are enforced by preexisting dispatcher. Seven added tests: valid shape, absent profile, unsupported protocol, denied permission, invalid signature, replay denial, unclaimed approval. Full isolated suite **295/295 PASS** (2.89s, exit 0). Source and tests committed to KRC branch.

Operation matrix: `research.profile.validate`, `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review` all have OFFLINE_DISPATCH implementations, **0/4 live network route accepted**. Bibliography operation can call external metadata providers and must be disabled in a zero-test. Strict owner profile approval proof and standardized JSON outputSchema/error envelope remain TODO. Public FIFO `research_profile_validate` is unrelated. K_Sentinel route WAITING_FOR_SENTINEL_READY. No production/MEDIA/public changes; FREE_ONLY.
