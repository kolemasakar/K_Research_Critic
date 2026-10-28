# Stage131 hashed offline dependency lock checkpoint — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Completed
- Created platform-specific lock `locks/stage131-test-cp312-linux-x86_64.requirements.txt`, 19 exact pins and SHA-256 hashes matching existing private wheelhouse.
- File SHA-256: `3cc915ae902e69d1e311963854cdc4e447313f6f0f32085a10832a54330e24e8`. After GitHub commit `2d01972955f9f35b22eae6429faa84fb32d7958e`, verified on independent krc-cobalt checkout that repository lock hash equals generated lock and `cmp` = PASS.
- Fresh isolated venv `/home/krcops/stage131-hash-verify-venv` installed offline with `pip install --no-index --find-links=/home/krcops/stage131-wheelhouse --require-hashes -r /home/krcops/stage131-lock-candidate.txt`; process exit 0, `pip check` **No broken requirements found**.
- On this new hash-verified venv, targeted config, permission, private HTTP GET and PDF tests: **17/17 PASS (1.30 s)**.
- Stage127 active PID43261 NRestarts0 and Stage126 active PID37979 NRestarts0 after verification. No service modifications.

## Claims and limitations
This is a hash-locked **test dependency set for CPython 3.12 x86_64**, not a signed software supply-chain attestation, not a fully frozen production runtime environment, and not a cross-architecture ARM64 lock. Wheelhouse is host-local, not published or bundled in repo. Hashes alone do not establish independent provenance. Stage131 not installed or started. Consent and scientific E2E NOT_RUN, production NO-GO.

## Next
Review exact Stage131 immutable source release tree, check dependency CVEs and public-supply-chain provenance, prepare dry-run operator installation under dedicated /opt candidate, and independently attest runtime filesystem UID and config reading only after scoped approval.
