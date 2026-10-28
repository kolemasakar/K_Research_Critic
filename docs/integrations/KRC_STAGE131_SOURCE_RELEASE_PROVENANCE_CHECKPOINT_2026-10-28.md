# KRC Stage131 immutable-source candidate & dependency provenance checkpoint — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO. No privileged installation or service activation.**

## Source candidate (host-local)
- Verified clean source git commit `45141cc0f0ceaa0fa9fcac267c9b5dba9f788df9`.
- Created unprivileged archive-extracted source under `/home/krcops/stage131-release-candidate-45141cc0f0ceaa0fa9fcac267c9b5dba9f788df9` using `git archive` at exact SHA.
- File count 845. SHA-256 manifest `/home/krcops/stage131-candidate-files.sha256`, digest `0eec944a8b2ca9789c6c600db1aabebc0fde1e57b781e5e56441edfa1d654b66`; `sha256sum -c` exit 0.
- On extracted candidate, hash-enforced offline venv and isolated Stage131 entrypoint/permissions/HTTP GET/response schema/PDF: **18/18 PASS** in 1.61s.

## Dependency provenance limitations
- CPython 3.12 x86_64 offline wheelhouse 19 SHA-256 pinned dependencies from `locks/stage131-test-cp312-linux-x86_64.requirements.txt`, pip `--require-hashes --no-index` earlier PASS.
- Installed distribution metadata count 19; no `direct_url.json` files. This is consistent with index/wheel resolution, but **does not independently prove trusted publisher identity, signed provenance, independent attestations, or vulnerability clearance**.
- Do not claim full supply-chain attestation or security-audit PASS; independent signature/provenance and vulnerability scan still outstanding.

## Review-only unit
Rendered SHA placeholder into temp `/tmp/krc-stage131-candidate.service`; `systemd-analyze verify` reported expected unavailable path `/opt/krc-stage131/<SHA>/.venv/bin/python`. Therefore **not installation-ready**, and no unit file installed or enabled.

## Blockers before K2
1. Root-owned immutable files and self-contained locked .venv at exact reviewed /opt SHA path (absent).
2. Service UID988 ability to read dedicated Stage131 operator-controlled secrets and config (none created).
3. No actual Stage131 socket, real consent or authorization; no production.
4. Joint Sentinel transport approval, T4 and scientific E2E acceptance remain separate.
