# MEDIA BETA Owner-Only Completion Plan

Version: 1.0
Status: IN_PROGRESS
Updated: 2026-08-20

## Decision

The owner has paused investigation of GPT public/link sharing and paused the external Tester 1 rollout.

The immediate project target is now a fully usable private owner-only MEDIA BETA product with ChatGPT access set to `Only me`.

External sharing, appeal/review of the sharing restriction, independent tester rollout, Free-plan compatibility, and public Store promotion are outside the current completion boundary.

## Owner-only completion boundary

The owner-only product is considered COMPLETE when all of the following are true:

1. The separate `K-Research & Critic - MEDIA BETA` GPT exists as a created private GPT and remains accessible only to the owner.
2. The GPT-facing Actions remain configured to the isolated MEDIA BETA Render backend.
3. A post-create owner smoke test is completed through the private GPT itself, not only Builder Preview.
4. That smoke test proves the normal private workflow:

```text
private GPT
 -> public YouTube URL
 -> valid owner-authorized beta credential
 -> KRCC job
 -> Helper 0.2.2
 -> captions-first when usable
 -> GPT status + complete segment retrieval
 -> DRAFT CriticProfile
 -> explicit owner approval
 -> independent Research
 -> Critic
 -> final output
```

5. The accepted EU Audio fallback remains available for owner use when captions are unavailable/unusable:

```text
AssemblyAI base URL=https://api.eu.assemblyai.com
provider=assemblyai
provider_model=universal-2
normal completion requires provider_data_deleted=true
```

6. CI for the active KRC feature branch is green after synchronization of the media-beta package and privacy contract.

## Credential note

Historical live acceptance was performed by the owner/operator using the credential designated for `Tester 1`.

For semantic cleanup of the owner-only product, the final private smoke test should preferably use the separately designated owner credential. This is a credential-attribution cleanup, not a prerequisite for the already accepted technical A4/A5/A6 results.

No plaintext credential is to be stored in project documentation.

## Not required for owner-only completion

The following are explicitly deferred and do not block `OWNER_ONLY_COMPLETE`:

- `Anyone with the link` sharing;
- GPT public sharing / Store publishing;
- appeal or investigation of the current sharing restriction;
- external Tester 1/2/3 onboarding;
- Free-plan compatibility testing;
- public-production promotion of the media feature;
- merge of KRC PR #8 or VoiceBridge PR #28 into production `main`;
- sustainable public free-media architecture Phase B/C work.

## Residual operational hardening

The following remain documented limitations for the private owner-only beta unless separately closed:

- hard process loss during active AssemblyAI transcription can leave provider cleanup unconfirmed (`provider_data_deleted=null`);
- Free Postgres is temporary beta infrastructure and may require lifecycle/migration work later;
- AssemblyAI fallback quota is finite;
- YouTube browser caption interfaces can change;
- captions remain preferred and should be used before Audio fallback.

These limitations do not prevent private owner operation because retry-safe failure, durable job state, durable quota accounting, EU provider routing, normal provider deletion, and captions-first zero-STT operation have already been live validated.

## Final acceptance record

After the post-create private GPT smoke test passes, create a dedicated owner-only acceptance record and set the canonical state to:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_OWNER_ONLY_COMPLETE`

Do not resume external sharing/tester rollout without a new explicit owner decision.
