# Proxy peer diagnostic research prototype

Date: 2026-10-01. Research-only; no VoiceBridge or Render production changes.

## Added
- `plugins/krc_migration_candidate/mcp_canary/proxy_peer_diagnostics.py`: pure Python research prototype, not imported by live E2 or VoiceBridge. Normalizes IPv4/IPv6 socket peer, produces a 24-hex-character HMAC-SHA256 tag using caller-supplied ephemeral >=32-byte key; categorizes only whether an untrusted Forwarded-like header is absent/empty/single/multiple/oversize. It never returns the raw IP or header value. Header shape is explicitly not a verified client identity.
- `tests/test_proxy_peer_diagnostics.py`: isolated tests cover deterministic same-peer tagging, key rotation, peer changes, IPv6 normalization, untrusted header classification, weak key and invalid IP rejection.

## Test status and limits

An attempt to run the tests on the authorized remote `krc-cobalt` was blocked by the tool safety layer before execution. **Test result: NOT RUN / UNVERIFIED**, not PASS. Do not deploy or use the prototype for live decisions before a permitted isolated test and security review. No provider calls or paid resources were initiated.

## Security decisions

Do not substitute raw `X-Forwarded-For` for the TCP peer without verifying trusted proxy boundary and spoof resistance. The prototype is diagnostic only, not a new rate-limit algorithm; its temporary HMAC key must be generated and protected outside logs and rotated per observation period. It is not production-integrated.

## Next gate

Obtain successful isolated unit-test output and review privacy/threat model; only then consider a separately owner-approved, minimal VoiceBridge diagnostic design. Existing E2 stays probe-only and FREE_ONLY.

## Subsequent isolated validation and privacy review

An independent local isolated Python pytest run using the checked-in prototype logic and its 12 parameter-expanded test cases completed **12 passed in 0.06s**. This supersedes the earlier blocked remote execution for these isolated tests only. The blocked `krc-cobalt` attempt remains historical fact; no authorized remote test or VoiceBridge integration has been performed.

Privacy/security review: the code does not return raw peer IP or header content, uses an HMAC with a caller-supplied key of >=32 bytes, and treats forwarded headers as untrusted classification only. A stable tag still links observations within the same key period; if the ephemeral key leaks, low-entropy IP candidates may be tested offline. Operational integration must ensure fresh cryptographically random keys, no key/raw-IP logging, strict log access and retention, and explicit proxy trust-boundary review. The module currently has no runtime wiring and cannot establish the cause of earlier 429 responses. Full repository regression suite not rerun in this isolated test.

Decision: **isolated unit gate PASS; privacy review CONDITIONAL; production integration NOT APPROVED**.
