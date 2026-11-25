# Confidential prepared-request delivery proposal - 2026-11-25

Status: PROPOSED FOR THREE-PARTY REVIEW. Not approved for live rollout.

## Selected approach

Reuse Stage127 Tailnet, existing GitHub OIDC identity verification and
authenticated local IPC. No new external host, listener, public storage,
credential or per-research-operation workflow. Candidate generic GET
/staging/v2/requests/<request_id>/prepared returns exact KRC-prepared
request bytes to the authorized consumer. Route spelling subject to
Sentinel review. A KRC-owned retrieval authority reads a private registry
and spools verified bytes; Sentinel forwards opaque data only.
The caller supplies RID, not path, operation, payload or approval claim.

Existing ProjectArtifactAuthority cannot be reused unchanged: descriptor()
requires requests.state=COMPLETE and consent.status=COMPLETED, whereas a
prepared request exists before execution. Do NOT relax these result GET
checks, fake a completed result or reuse result artifact IDs as request IDs.
Reuse signed read patterns, bounded spool, peer identity and nonce protection
with separate request-delivery purpose and scope. No direct filesystem ACL
grant to Sentinel or GitHub runner.

## Proposed contract and security

- KRC registry binds RID, intended principal/repository/workflow, immutable
  profile digest, byte digest, size, purpose, expiry, revocation and delivery
  authorization. Internal path determined by KRC, never user input.
- Delivery authorization is distinct from one-shot execution authorization.
  Owner approves verified design and real disclosure before enabling real
  retrieval. Preparation alone grants neither delivery nor execution.
- Existing OIDC and Tailnet admission; signed internal purpose
  prepared_request.read, bound RID, audience, issuer, nonce and expiry.
  Distinct signature context from artifact.read; reject cross-purpose reuse.
- Owner-only file, no symlinks, regular file, size <=262144 bytes, verify
  exact immutable bytes and profile correspondence before return. Recheck
  authorization at final release boundary. Already transmitted bytes
  cannot be recalled; document this limitation.
- 200 application/json, exact Content-Length and SHA256 digest header;
  Cache-Control: no-store. No redirects or body logging. Generic sanitized
  denial/error; exact status mapping agreed with Sentinel. No authorization
  inferred from knowledge of RID or digest.
- Runner obtains short-lived existing OIDC credential, validates response
  byte size/digest against pinned KRC descriptor, uses memory or protected
  temporary file, forwards exact bytes to existing POST /staging/v2/execute
  and verifies result via existing signed artifact GET. No public repository,
  workflow input, output, log, cache or Actions artifact containing raw
  request. Separate authenticated requests and no blind execution retries.
- Preserve existing Stage127 POST and result GET behavior. Default disabled,
  bounded timeout/concurrency, durable replay checks, explicit rollback.
  No live Stage134 retrieval until owner accepts design and synthetic tests.

## Acceptance and assignments

KRC: implement private retrieval authority and scoped read contract after
joint review, without rebuilding research profile/consent machinery.
Sentinel PR39: review threat model and route/IPC binding, implement generic
opaque forwarding through existing Stage127, prove synthetic admission,
confidentiality, wrong principal/scope, expiry, replay, revoke, tampered
bytes, oversized data, traversal, disconnect, no logs, rollback and
preserved existing routes. No permission expansion without review.
Science PR17: demonstrate existing authorized runner generic invocation,
exact digest validation, private byte handling and cleanup; retain
independent result validator. Owner: approve tested design before real run.

Real request stays owner-only, 66287 bytes, SHA256
44cd9db1315903082062732cf314f71a42ab7356c8e9ca8d8d4062093e8510f6.
Execution grant remains PROPOSED per last read. No execution or disclosure
performed by this proposal. Production NO_GO.
