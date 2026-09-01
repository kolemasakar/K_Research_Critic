# K-Research & Critic - MEDIA BETA
## M3B A/B Complete Owner Decision Checkpoint

Date: 2026-09-01
Status: CANONICAL_RECOVERY_CHECKPOINT / RELEASE_HOLD_OWNER_TESTING / M3B_AB_COMPLETE_OWNER_DECISION_PENDING
Supersedes for current continuation: `67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md`

## Owner authorization executed

The owner explicitly authorized the second provider-consuming M3B A/B run for four independently reviewed exact assets against two prerecorded providers.

```text
cases: 4
providers: 2
maximum provider submissions: 8
automatic retry/resubmit: FALSE
```

Providers:

- active KRC prerecorded baseline: AssemblyAI `universal-2`
- inactive candidate: Gemini `gemini-3.5-transcribe`

This authorization applied only to the bounded evidence run. It did not authorize normal Gemini activation, merge, deployment, external testers, or public release.

## M3B execution evidence

VoiceBridge workflow:

```text
KRC Media M3B Live A-B
run: 33545803364
source commit: 4f55dab95abe5518b9205cb5666ad457795416d7
result: SUCCESS
provider result records: 8/8 SUCCESS
provider failure observed: FALSE
raw media artifact: FALSE
artifact id: 9815474860
artifact digest: sha256:27553dfea4c4b641f54cfd8113b9a91396f262a6d2b9dc4c928a57f72964e80f
```

VoiceBridge acceptance record:

`docs/history/2026-09-01_KRC_MEDIA_M3B_LIVE_AB_ACCEPTANCE.md`

## M3B deterministic lexical WER

| case | AssemblyAI | Gemini |
|---|---:|---:|
| longer clean Harvard speech | 0.00% | 0.00% |
| loud jackhammer noise | 0.00% | 0.00% |
| numeric Vosk fixture | 100.00% | 100.00% |
| LibriSpeech test-other | 0.00% | 0.00% |

M3B aggregate over 86 reviewed reference tokens:

```text
AssemblyAI token-weighted WER: 17.44%
Gemini token-weighted WER: 17.44%
AssemblyAI mean latency: 3220.5 ms
Gemini mean latency: 3399.25 ms
```

The numeric fixture dominates lexical WER because both providers convert spoken number words into compact digit strings rather than preserving lexical `zero` / `oh` tokens.

## Numeric factual review

Independently reviewed spoken number sequence maps to:

`100019021001803`

```text
AssemblyAI digit sequence: 1000190210018
numeric sequence error rate: 13.33%
final digits omitted: 03

Gemini digit sequence: 100019021001803
numeric sequence error rate: 0.00%
```

Manual interpretation:

```text
zero-versus-oh lexical preservation: FAIL_BOTH
numeric sequence factual completeness: GEMINI_PREFERRED_FOR_THIS_FIXTURE
```

## Seven-case combined evidence

The original M3 three-case tranche plus M3B now total seven independently reviewed cases and 117 reference tokens under lexical-WER accounting.

```text
AssemblyAI token-weighted WER: 13.68%
Gemini token-weighted WER: 14.53%
AssemblyAI mean provider latency: 3346.43 ms
Gemini mean provider latency: 3555.86 ms
```

This is not a decisive provider ranking. The first RU fixture favored AssemblyAI for numeric-format clarity, while the new numeric sequence fixture favors Gemini for exact sequence completeness. Three new non-numeric English cases were exact for both providers, including the loud-noise case.

## Current interpretation

```text
M3_FIRST_TRANCHE_AB: COMPLETE
M3B_PROVIDER_AB: COMPLETE
M3B_PROVIDER_RESULTS: SUCCESS 8/8
M3B_MANUAL_FACTUAL_REVIEW: COMPLETE
M3B_MANUAL_HALLUCINATION_REVIEW: COMPLETE
M3B_LEXICAL_WER: TIE_FOR_THIS_TRANCHE
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
GEMINI_PRERECORDED_TECHNICAL_FUNCTION: PASS
ACTIVE_KRC_PRERECORDED_PROVIDER: ASSEMBLYAI universal-2
GEMINI_PRERECORDED_ACTIVE: FALSE
PROVIDER_CUTOVER: NOT_AUTHORIZED
M3_CLOSURE_DECISION: OWNER_DECISION_PENDING
R1 / R2 / R3 / R4: HOLD
```

## Remaining coverage gaps

The seven-case corpus still does not materially cover:

- real multi-speaker conversation;
- code-switching;
- telephone-bandwidth speech;
- noisy Ukrainian;
- noisy Russian;
- longer real-world geopolitical media recordings.

A further M3C tranche should be justified only if the owner wants a stronger evidence basis for provider cutover. If the immediate product goal is stability rather than migration, retaining AssemblyAI remains a valid conservative choice because it is already the active accepted provider and the evidence does not establish a clear global Gemini advantage.

## Exact continuation point

Owner decision required:

```text
1. RETAIN_ASSEMBLYAI_AND_CLOSE_M3
2. M3C_TARGETED_CORPUS
3. HOLD_WITHOUT_CUTOVER
```

No option is implied by this checkpoint. A new provider-consuming run requires separate explicit authorization.

## Recovery command

`recover KRC MEDIA BETA M3B A/B complete owner decision checkpoint 2026-09-01`
