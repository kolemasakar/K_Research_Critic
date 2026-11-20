# KRC N39 joint Artifact GET STAGING release candidate and audit checkpoint
Date: 2026-11-17 (UTC); owner policy remains single-owner ChatGPT Project.
Disposition: KRC SOURCE+ISOLATED ACK / PRIVATE AUDIT CHECKPOINT PUBLISHED /
AUTHENTICATED PUBLISHER SOURCE READY / JOINT RUNTIME INSTALLATION HOLD /
EXTERNAL N01-N40 0/40 FULL PASS / PRODUCTION NO-GO.

Response to Sentinel PR #29 comment 6959810604. No live service installation,
activation, owner consent mutation, provider execution or key provisioning.

## 1. Exact pins and files
- KRC package pin: 46aebfcd52117d564624fd708709a097bb533362.
- Full regression pin: a58921dea463d9ef6a3beeb552d1e73cc49b3314; package delta adds
  only the contract schema. 1203 PASS / 18 SKIP / 0 FAIL in 70.09s on isolated
  krc-cobalt, UID1002. No independent full partner rerun claimed.
- Runtime-state producer remains original installed pin
  1de17e2dda51a2fbb155632778c425d86fe152d9; no migration or rewrite.
- Source archive SHA256 (exact command below):
  75895401f582d65868109a7c3d5d7510aa9303090429a1e37eb2ae6bd104795b
- Source and package SHA256:

| File | SHA256 |
|---|---|
| src/krc_research/stage131_project_signed_read.py | e0300c8a948916b0b54117cb74275f9d5e1738adbe031acf7f3f7cc678516614 |
| src/krc_research/stage131_project_descriptor_client.py | 377c1c986af8e44138d0a70d417bcff79056156fef3d00fab3344aa90436c4f0 |
| src/krc_research/stage131_signed_artifact_read.py | 834cb3934d7c7ec5b6d2b2933dc4a59a3709be11f2c118be5b924530f7c6f7f2 |
| src/krc_research/stage131_signed_artifact_uds.py | c8db333d289bb90aa90b9a1c064752570917490c59a2541699bf5b74d78df375 |
| src/krc_research/stage131_artifact_nonce_registry.py | c3b9f9e3d26792fdef61f1cc74dd106aea3e799b7340fc06ed6f752bf46cb1ec |
| src/krc_research/stage131_project_audit_outbox.py | b71ea1b8344330e2a76e44e41f94e42f8081283c07776389635db04b6f7cf7dd |
| tools/n39_project_checkpoint_publisher.py | b2589efe9b66bcf903566ac426f7b651b40b3a4f3f5cb1e5014eee0941f37488 |
| deploy/stage131/krc-project-n39-read.service.example | e46d43f62b1b2bfd45dd4a81c86656fb6a4d963db9365045bdf87c104b84c571 |
| deploy/stage131/project_read_release_config.example.json | 0d4e486df67f5922bac9a3707a29d66834333bc11706885d8700475a097835fb |
| deploy/stage131/project_read_contract.schema.json | b8cd7bf82ba76bcce08ddb41d27bac4fd521bcbd209de7ce37403564e91880b2 |
| docs/integrations/fixtures/stage131_n39_project_read_wire_2026-11-17.json | cd7909ca49c25b3234e493de08ffc0de8192dd05a9532543ecff6a84b96c9ee0 |

Build command (read-only; no activation):
```sh
PIN=46aebfcd52117d564624fd708709a097bb533362
git archive "$PIN" src/krc_research deploy/stage131/krc-project-n39-read.service.example deploy/stage131/project_read_release_config.example.json deploy/stage131/project_read_contract.schema.json | sha256sum
```

## 2. Exact private interface
- Separate restricted AF_UNIX endpoint /run/krc-project-n39-read/backend.sock.
  Directory 0750 UID1002 GID984, socket 0660 UID1002 GID984. No TCP listener.
  Existing Stage127/Stage131/Research v2 sockets and POST services unchanged.
- Service owner krcops UID1002, effective group krc-sentinel-ipc GID984, not
  krcresearch UID988. This resolves private producer custody without chmod/chown
  or adding krcsentinel to krcops group. Producer state remains 0700/0600, only
  existing owner can access. SQL uses mode=ro and query_only. The unit protects
  DB files and object directory read-only and gives the existing owner access
  to the private directory for SQLite WAL/SHM sidecars. Actual mount namespace,
  sidecar creation/concurrency and service startup need installed parity test.
- Sentinel allowed kernel SO_PEERCRED UID987. Sentinel client verifies server
  UID1002 GID984. Kernel UID/GID mappings verified on host; isolated wire tests
  used actual UID/GID1002 and synthetic keys, not the installed Sentinel peer.
- Root-provisioned distinct retrieval-only 32-byte key, id
  stage131-project-read-v1, /etc/krc-project-n39-read/retrieval.key,
  root:984 0440; directory root:984 0750. Group is existing machine IPC group.
  No key material written. Compare separation from execution/transport keys
  privately only during approved install; never print secrets.
- Dedicated nonce database /var/lib/krc-project-n39-read/nonce.sqlite, private
  state directory 0700. Durable unique key/nonce/principal, 900s retention,
  signed clock skew <=300s, shared by read and describe. Four bounded workers;
  20s absolute connection deadline, 5s per socket timeout; bounded 200MiB spool.
- Envelope schema deploy/stage131/project_read_contract.schema.json. Exact
  server-derived identity K_Science / kolemasakar/K_Science / refs/heads/main.
  Both endpoints require HMAC + trusted peer + fresh nonce, exact request/artifact
  selectors. /v1/artifacts/describe uses artifact.describe; /v1/artifacts/read
  uses artifact.read. Both use POST and krc-artifact-get/1. Client must half-close
  write side, server sends strict length/hash/EOF with Connection: close.
- Authority: read-only COMPLETE RequestLedger record; exact artifact ID
  association in owner consent ledger; current COMPLETED consent; authoritative
  index metadata must equal producer descriptor; trusted server retention clock.
  No caller consent flag, principal override, execution signer or science
  dispatcher exposed. Cancellation before final authorization denies read;
  previously authorized bytes cannot be retracted. The N25 isolated test proves
  verified private spool does not stream later tampered source bytes.
- Trusted descriptor returned as JSON: request_id, artifact_id, filename,
  media_type, size_bytes, sha256, expires_at_epoch. K_Sentinel uses
  stage131_project_descriptor_client.fetch_descriptor() with already admitted
  signed read envelope to derive a DISTINCT nonce and independently signed
  describe call. Reference client checks peer, bounded header/length/EOF,
  scope/hash format and retention. Then Sentinel verified_spool validates actual
  read against this descriptor. Do NOT trust caller-supplied digest/download
  header as authoritative descriptor. K_Science must retain original scoped
  producer descriptor independently from received bytes.
- No new separate human consent or identity checks. 24h execution cap remains
  the producer's policy; read retention is independent of execution expiry.

## 3. Definitive candidate mapping and observed results
| Internal status | Meaning | Expected external mapping |
|---|---|---|
| 200 JSON | authoritative descriptor, no payload bytes | internal only |
| 200 binary | fully verified private spool, exact length and SHA, no-store/nosniff, EOF | 200 |
| 400 | malformed signed envelope/framing; no authorization | 400 for malformed external request, otherwise 502 for invalid backend request |
| 403 | wrong peer/key/signature/identity/replay/cancelled or missing scope association | 403 |
| 404 | disabled, missing COMPLETE ledger/different request or artifact/principal | 404 |
| 410 | still-authorized artifact expired | 410 |
| 413 | trusted descriptor over bound | 413 |
| 415 | malformed content type | 502 for invalid backend request |
| 502 | conflicted producer descriptor, corruption/truncation or invalid response | 502 |
| 503 | unavailable backend DB/worker saturation/socket unavailable | 503 |
| 504 | client-observed upstream deadline timeout; socket may close without a body | 504 |
No HTTP-504 wire emitted by the UDS on hard deadline shutdown; the reference
descriptor client and Sentinel timeout map to 504. No forwarding arbitrary
upstream error text. The actual fixture shows 503 JSON and 21 JSON responses
validated against schema, all 23 response lengths/hashes verified. All fixture
data synthetic, never the live owner's artifact.

Fault matrix: 21 PASS / 0 FAIL in 14.25s (wire test pin
139bd1902e979883cc33641a080f9169c6af2339). N12 400; N15/N18/N19/N20 missing 404;
N20 conflict 502; N21 410; N22/N23/N24 502; N25 verified spool 200 unchanged
original bytes then subsequent corrupted read 502; N26 413 at reduced test
limit (full 200MiB load owner-waived); N27-N30 403; N39 cancellation or missing
association 403; DB unavailable 503; describe/read 200 and durable nonce restart
403. Client missing socket 503 and controlled timeout 504. No repeat science
dispatch in read/revoke path. Existing 19 focused tests passed (publisher, outbox,
project read and hardening). Static systemd-analyze verify passed for candidate
unit in /tmp; /usr/bin/python3 source import/help passed; no new actual socket.
Actual fixture file:
docs/integrations/fixtures/stage131_n39_project_read_wire_2026-11-17.json.

Cross-project KRC-coordinated isolated interoperability: copied exact Sentinel
commit 3f9f45eac82ba0199b1c29b3251f3953a638a759 files
artifact_get_verified_spool127.py (blob 4bb0d4d9003364c158a220024499ec5a1232f01d)
and artifact_get_uds_client127.py (blob f2a8a8b0c5502ea2f5faf4b9e04a56ee885dbfe2).
KRC descriptor -> real AF_UNIX -> actual Sentinel verified_spool 386 bytes,
exact trusted descriptor SHA and EOF PASS. Replay 403 PASS, cancel between
describe/read 403 PASS, single original science dispatch PASS. Not independent
Sentinel ACK, not external ephemeral runner evidence.

Reproduce (isolated, synthetic):
```sh
PYTHONPATH=src python -m pytest -q tests/test_stage131_project_signed_read.py tests/test_stage131_project_read_joint_fault_matrix.py tests/test_stage131_signed_get_http_hardening.py tests/test_stage131_project_audit_outbox.py tests/test_n39_project_checkpoint_publisher.py
KRC_N39_FIXTURE_OUTPUT=/tmp/new-synthetic-fixtures.jsonl PYTHONPATH=src python -m pytest -q tests/test_stage131_project_read_joint_fault_matrix.py
PYTHONPATH=src python -m pytest -q
```

## 4. Audit publication (real observed state, not a grant)
Existing protected branch audit/n39-anchor-ledger accepted; ruleset 27332825.
Separate private SQLite outbox (0700 dir/0600 file) on krc-cobalt:
 /home/krcops/krc-project-n39-staging/audit/outbox.sqlite.
Observed actual persisted private state; canonical salted hash chain, no raw
profile, consent refs, artifact contents or secrets published. Prepared first
checkpoint with source pin 594a0d872de045c79841c710e766fedeb0b27a98, no retroactive
event grant. SHA256 022279467911c9a0b3b60c8b629ac673c5c1e0838ee043fe6437058013b70110.
GitHub PR #34 merged through protected rebase flow to
f8fa78c0e7bdbc457a0521f0e53b661845bf390e; compared ancestor
17dea84013392c0efda6bdb09f12d6f287283842, verified only new checkpoint + new schema +
README amendment, old anchors preserved. Exact file read back and local
receipt ACK PUBLISHED; repeated prepare returned UNCHANGED. Format
audit/n39/PROJECT_CHECKPOINT_FORMAT.json on protected branch. Independent-admin
custody deferred and NOT a gate.

Reusable publisher tools/n39_project_checkpoint_publisher.py validates strict
hash-only manifest, ruleset, prior branch ancestry, remote journal prefix and
append-only change, creates pinned rebase PR, verifies merged exact file and
prefix, returns receipt. 4 mocked API tests pass. Server gh CLI is installed
but not authenticated; no credentials provisioned. Real actual publishing
completed via authorized ChatGPT GitHub connector, NOT via authenticated
standalone gh invocation; autonomous scheduled publication of new checkpoints
not installed. For on-demand workflow remotely prepare outbox, publish returned
payload using already authorized GitHub connector (or trusted client with
existing gh auth and --publish), verify exact merged file+ancestry, then ACK
outbox. If unchanged no PR; if pending retry same hash; base changes require
reconciliation, never overwrite/delete or reexecute science. Source tests
validate tamper, prefix, cancellation checkpoint, duplicate and privacy.
Operational update hooks/continuous invocation still to be integrated; no
claim that every transition is continuously anchored.

## 5. Reviewed-only deployment and rollback manifest
Gate A: independent KRC/Sentinel/Science source ACK and verify fixture/schema,
candidate unit, hash manifest and descriptor mapping. Confirm key and UID/GID
custody, systemd runtime state, separate nonce registry, cancellation ordering.
No production or external activation.
Gate B (separate owner release decision required):
- Record exact prior service source pins/config flags, active sockets and
  permissions; preserve existing Stage127 :19017 POST and installed Stage131.
- Materialize exact verified archive to new root-owned /opt/krc-project-n39-read/
  <pin> directory, read-only code, verify SHA; point current symlink only in this
  new component. Stage unit under its distinct name with no Install/autostart.
  Keep enable-reviewed-staging marker absent; no service start, no new sockets.
- Provision key through existing authorized admin channel, separate from other
  keys, root:984 directory/file modes 0750/0440. Verify expected UID/GID and
  read-only private DB paths, key separation and nonce ownership without
  changing producer permissions. Do not copy actual DBs or live artifact bytes.
- Review and install Sentinel combined-handler package default GET OFF under
  existing Stage127 service only; no additional listener. Verify disabled GET
  404 with zero UDS, existing POST T3 and rollback before enabling.
Gate C (explicit temporary STAGING activation after B acceptance):
- Only then enable marker/start separate Unix read unit; confirm actual systemd
  namespace and DB WAL/SHM behavior with isolated test rows / reviewed fixtures,
  peer credentials, socket modes, no privileged data access and signed describe/
  read. No active new TCP port. Sentinel key and source pin match.
- Only reviewed owner-approved temporary external GET enable on canonical Stage127
  port; real OIDC and Tailnet runner, fresh JTI, approved artifacts, no new
  scientific dispatch. Run agreed N01-N40 evidence and K_Science receiver tests.
- Disable GET afterward, verify 404/zero UDS and POST unchanged. Review
  independent ACK/MISMATCH, no automatic production enable.
Rollback: disable Sentinel GET first and verify 404/zero UDS and POST regression;
restore prior reviewed Sentinel release/config if necessary. Stop only the new
read unit; remove its enable marker, preserve nonce DB, audit and producer data,
retain prior installed Stage127/Stage131/Research v2 unchanged. Verify new Unix
socket absent and original services responsive. Do not delete/reissue consent
or keys, replay research or force-update protected GitHub ledger.

Remaining: independent Sentinel/Science source review and actual installed parity,
joint external 0/40, formal release decision before any activation, authenticated
recurring audit publishing (on-demand checkpoint flow PASS), real science E2E not
authorized/executed. All current live owner approval and completed artifact state
left unchanged. No new human identification requirement.
