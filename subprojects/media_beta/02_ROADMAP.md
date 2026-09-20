# MEDIA BETA Roadmap

Version: 7.3
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_COMPLETE / R3-E4_COMPLETE / R3-F_RUNTIME_ACCEPTANCE_NEXT / R3-G_OAUTH_RUNTIME_ACTIVE / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-20

## End state

Build a production-grade private MEDIA surface for K-Research & Critic while preserving the published public KRC core.

The finished system must provide:

- canonical 13 MEDIA operations;
- 9 read operations and 4 consequential start operations;
- isolated YouTube / Instagram / Facebook / Telegram execution surfaces;
- confirmation before each consequential start;
- server-side route-scoped credentials;
- restart-safe OAuth/DCR;
- Neon durable state;
- restart replay and duplicate-start idempotency;
- fail-closed FREE_ONLY provider policy;
- migration/publication readiness only after runtime parity and operational hardening.

## Current roadmap position

```text
R3-A Contract freeze/security baseline        PASS
R3-B Authentication/secret hardening          PASS
R3-C 9-tool read-only binding                 PASS
R3-D Consequential-action confirmation        PASS
R3-E1 YouTube execution                       PASS / COMPLETE
R3-E2 Instagram execution                     PASS / COMPLETE
R3-E3 Facebook execution                      PASS / COMPLETE
R3-E4 Telegram execution                      PASS / COMPLETE
R3-F Full 13-operation parity                 LOCAL+CI PASS / RUNTIME ACCEPTANCE NEXT
R3-G Private operational hardening            OAUTH ACTIVE / TOKEN RESTART ACCEPTANCE PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

## Accepted live evidence

```text
YouTube=COMPLETE
Instagram=COMPLETE

Facebook:
  job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
  status=COMPLETED
  retrieval_provider=cobalt
  charge=0
  restart_durability=PASS
  duplicate_start_idempotency=PASS

Telegram:
  completed_job_id=KRCM_c1cbb41b-497d-472c-b6c2-10d1128b4eda
  status=COMPLETED
  retrieval_provider=telegram_public_web
  charge=0
  restart_durability=PASS
  duplicate_start_idempotency=PASS
  failed_content_fixture=KRCM_59d7bdc2-9ea0-4028-b8c6-dfe3f39828f9
  failed_content_reason=no_spoken_audio
```

E3/E4 are returned to `CONFIRMATION_PROBE_ONLY=true`.

## Canonical contract

```text
TOTAL_OPERATIONS=13
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
```

Execution operations:

- `media_youtube_start`
- `media_instagram_start`
- `media_facebook_start`
- `media_telegram_start`

## CI state

```text
KRC_RUN=35466720921
KRC_PYTHON_3_13=PASS
KRC_PYTHON_3_14=PASS
KRC_QUALITY=PASS

VOICEBRIDGE_RUN=35466722002
VOICEBRIDGE_CLOUD=PASS
VOICEBRIDGE_IMAGE_PARITY=PASS
VOICEBRIDGE_BROWSER_EXTENSION=PASS
VOICEBRIDGE_REPOSITORY_DOCS=PASS
```

## Current safety invariant

```text
E3_CONFIRMATION_PROBE_ONLY=true
E4_CONFIRMATION_PROBE_ONLY=true
E3_PROVIDER_WORK_STARTED=false
E4_PROVIDER_WORK_STARTED=false
ADDITIONAL_LIVE_MEDIA_STARTS=NO
PROJECT_COST_POLICY=FREE_ONLY
AUTOMATIC_PAID_FALLBACK=DENIED
```

## Nearest tasks

1. Complete R3-F runtime parity across the read-only surface and four isolated execution surfaces.
2. Prove all 13 canonical operations are represented exactly as designed.
3. Prove no execution tool leaks into the 9-tool read-only surface.
4. Prove each E1/E2/E3/E4 surface exposes exactly its own start operation plus scoped non-execution support.
5. Complete R3-G OAuth token continuity across controlled restart.
6. Finish operational hardening evidence.
7. Enter R3-H migration/publication readiness.

## Infrastructure policy

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

## Storage policy

```text
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
LOCAL_WORKTREES=TRANSIENT_ONLY
```

Recovery authority: `CURRENT_HANDOFF.md` v19.2 + checkpoint 158.
