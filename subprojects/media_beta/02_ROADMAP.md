# MEDIA BETA Roadmap

Roadmap for the closed MEDIA BETA and later optional public/sustainable media work.

Version: 2.9
Status: ACTIVE
Updated: 2026-08-20

## Phase A - Closed MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Delivered:
- separate MEDIA BETA GPT identity;
- separate GPT Action contract;
- separate VoiceBridge media backend path;
- dedicated Render beta target;
- production VoiceBridge unchanged;
- published K-Research & Critic unchanged.

### A2. Resource protection

Status: COMPLETE_IN_CODE_AND_PRIMARY_LIVE_GUARDS

Accepted controls:
- max source/capture duration 60 min;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec per UTC day;
- captions path STT charge 0;
- helper audio upload guard 32 MiB;
- mono 16 kHz speech normalization at about 32 kbps;
- provider delete request on normal AssemblyAI completion;
- access-code guard;
- durable Postgres job state and STT quota ledger;
- negative-path guards for invalid code, wrong source, >60 min, concurrency, and quota exhaustion.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- isolated from production VoiceBridge.

### A4. Live transcript validation

Status: COMPLETE

Accepted:
- captions-first browser-assisted ingestion;
- UK/RU/EN/AUTO language/source cases;
- zero STT charge for captions;
- Audio fallback through AssemblyAI Universal-2;
- duration/quota accounting;
- provider cleanup on normal completion;
- Action status/segment readback;
- durable restart/resume behavior;
- durable quota-ledger restoration;
- forced active-audio process loss -> retry-safe deterministic failure;
- no duplicate STT charge after process replacement;
- U+FFFD anomaly dispositioned as non-reproducible/non-blocking.

Canonical records: `10_...` through `17_...` in this directory.

### A5. Separate GPT Builder beta

Status: COMPLETE

Accepted:
- separate `K-Research & Critic - MEDIA BETA` GPT;
- Builder-safe instructions under the 8000-character limit;
- web search enabled;
- image generation disabled;
- code interpreter/data analysis enabled;
- API Key/Bearer Action auth;
- isolated beta Action server;
- privacy policy URL configured;
- all three GPT-facing operations recognized and manually tested;
- manual transcript pagination 227/227 segments confirmed;
- Builder-created KRCC job interoperates with Helper 0.2.2;
- CriticProfile approval gate blocks independent research before approval.

Canonical acceptance: `18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md`.

### A6. Owner/operator end-to-end acceptance

Status: COMPLETE

Accepted owner-operated flow:

```text
YouTube URL
 -> valid allowlisted credential
 -> Builder Action
 -> Helper captions-first completion
 -> GPT status/segments
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> independent web research
 -> Critic/revision
 -> finalization
```

Historical live tests were performed by the owner/operator using the credential designated for Tester 1. This does not invalidate the technical acceptance. Canonical correction: `21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`.

### A7. Controlled external tester rollout

Status: PAUSED_BY_OWNER

Previously accepted readiness gates remain valid:
- captions-first READY;
- Helper 0.2.2 onboarding READY;
- AssemblyAI Audio fallback routed through `https://api.eu.assemblyai.com`;
- EU Audio fallback live acceptance PASS;
- normal provider deletion and exact STT quota accounting confirmed.

External Tester 1/2/3 onboarding, GPT link sharing, public sharing restriction investigation, and appeal work are paused by explicit owner decision on 2026-08-20.

A7 is not required for the current owner-only completion target.

### A8. Owner-only product finalization

Status: IN_PROGRESS

Target state: private `K-Research & Critic - MEDIA BETA` usable only by the owner.

Required before `OWNER_ONLY_COMPLETE`:
- GPT remains `Only me`;
- one post-create end-to-end smoke test through the actual private GPT (not only Builder Preview);
- preferably use the separately designated owner credential for semantic cleanup;
- verify KRCC creation, Helper 0.2.2, captions-first completion, complete transcript retrieval, CriticProfile gate, owner approval, Research/Critic, and final output;
- keep the accepted EU Audio fallback available for captions-unavailable cases;
- active KRC feature-branch CI remains green.

Canonical plan: `22_OWNER_ONLY_COMPLETION_PLAN.md`.

On PASS create owner-only acceptance and set:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_OWNER_ONLY_COMPLETE`

## Phase B - Sustainable Free Media

Status: DEFERRED

Potential future work:
- caption-path hardening;
- Cloudflare Whisper proof of concept;
- provider-neutral transcript router;
- local Media Node / residential ingress proof of concept;
- remove permanent AssemblyAI dependency from any future public free path.

None of Phase B blocks owner-only completion.

## Phase C - Public media release

Status: PAUSED / FUTURE

Would require a new explicit owner decision plus sharing/publication resolution, sustainable resource architecture, privacy re-validation, runtime-plan compatibility, stable public privacy-policy delivery, production smoke tests, and explicit promotion approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation/acceptance evidence exists. READY/IN_PROGRESS/PAUSED/BLOCKED/PLANNED must never be described as already validated.
