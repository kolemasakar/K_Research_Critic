# MEDIA BETA Roadmap
Поточний roadmap приватного K-Research & Critic MEDIA BETA.

Version: 4.1
Status: RELEASE_HOLD_OWNER_TESTING / M3B_AB_COMPLETE_OWNER_DECISION_PENDING
Updated: 2026-09-01

## Product position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main
closed-beta product branch: agent/video-url-research
technology/backend implementation source: kolemasakar/VoiceBridge
active KRC provider-migration branch: agent/krc-media-gemini-migration
```

VoiceBridge supplies technology, implementation, and validation evidence. It does not independently authorize KRC product release gates.

## Accepted runtime baseline

```text
A8 browser-assisted owner baseline                 COMPLETE / FALLBACK_ONLY
A9 owner zero-client media input                   COMPLETE / ACCEPTED
A9.10 local attachment                             COMPLETE / ACCEPTED
A10 copy-safe claim-summary stabilization           COMPLETE / ACCEPTED
Builder package                                     0.9.1-beta-a10
Action schema                                       0.6.0-a9.10
release state                                       RELEASE_HOLD_OWNER_TESTING
```

Accepted policy remains unchanged:

```text
Facebook Cobalt failure -> unavailable
NO automatic paid fallback
ScrapeCreators reserve only / inactive
Telegram public-only / zero retrieval credits
local attachment max 32 MiB / zero retrieval credits
```

## Provider boundary

VoiceBridge live streaming and KRC prerecorded STT remain separate domains.

```text
VoiceBridge live default: Gemini gemini-3.5-transcribe-live
KRC prerecorded selector: KRC_MEDIA_STT_PROVIDER
KRC prerecorded active provider: AssemblyAI
KRC prerecorded active model: universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini normal activation: FALSE
provider cutover: NOT_AUTHORIZED
```

## M3 provider-evidence track

```text
M0 migration preflight                         COMPLETE
M1 provider abstraction                        PASS
M2 Gemini prerecorded adapter                  PASS / INACTIVE
M3 offline evaluator                           PASS
M3 first clean-public reference review         COMPLETE 3/3
M3 first provider A/B                          COMPLETE 3/3 x 2
M3B expanded corpus byte acceptance            COMPLETE 4/4
M3B independent reference review               COMPLETE 4/4
M3B second provider A/B                        COMPLETE 4/4 x 2
M3 manual factual/hallucination review          COMPLETE
M3 closure decision                            OWNER_DECISION_PENDING
M4 new-infrastructure canary                    NOT_STARTED
M5 provider/new-infrastructure cutover          NOT_AUTHORIZED
```

## First M3 tranche

```text
cases: 3
AssemblyAI token-weighted WER: 3.23%
Gemini token-weighted WER: 6.45%
first-tranche evidence preference: ASSEMBLYAI_FOR_THIS_TRANCHE
Gemini prerecorded technical function: PASS
```

The first tranche was too small to justify a provider cutover, so the corpus was expanded.

## M3B expanded tranche

Workflow evidence:

```text
workflow: KRC Media M3B Live A-B
run: 33545803364
source commit: 4f55dab95abe5518b9205cb5666ad457795416d7
result: SUCCESS
provider result records: 8/8 SUCCESS
provider failure observed: FALSE
raw media artifact: FALSE
artifact id: 9815474860
artifact digest: sha256:27553dfea4c4b641f54cfd8113b9a91396f262a6d2b9dc4c928a57f72964e80f
```

Deterministic lexical WER:

| M3B case | AssemblyAI | Gemini |
|---|---:|---:|
| longer Harvard speech | 0.00% | 0.00% |
| jackhammer noise | 0.00% | 0.00% |
| numeric Vosk fixture | 100.00% | 100.00% |
| LibriSpeech test-other | 0.00% | 0.00% |

M3B aggregate over 86 reviewed reference tokens:

```text
AssemblyAI token-weighted WER: 17.44%
Gemini token-weighted WER: 17.44%
AssemblyAI mean latency: 3220.5 ms
Gemini mean latency: 3399.25 ms
```

The numeric case dominates lexical WER because both providers render spoken number words as digit strings. Manual semantic review therefore remains mandatory.

Numeric factual review:

```text
reviewed digit sequence: 100019021001803
AssemblyAI: 1000190210018
AssemblyAI numeric sequence error rate: 13.33%
AssemblyAI omission: final 03
Gemini: 100019021001803
Gemini numeric sequence error rate: 0.00%
zero-versus-oh lexical preservation: FAIL_BOTH
numeric sequence factual completeness: GEMINI_PREFERRED_FOR_THIS_FIXTURE
```

## Combined seven-case evidence

```text
total reviewed reference tokens: 117
AssemblyAI token-weighted lexical WER: 13.68%
Gemini token-weighted lexical WER: 14.53%
AssemblyAI mean provider latency: 3346.43 ms
Gemini mean provider latency: 3555.86 ms
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

Interpretation is mixed: the first RU numeric-format case favored AssemblyAI for clarity, while the new numeric sequence case favored Gemini for exact factual completeness. Three new non-numeric English cases were exact for both providers, including the loud-noise case.

## Current roadmap position

```text
M3B A/B COMPLETE / OWNER M3 CLOSURE DECISION
```

Canonical recovery checkpoint:

`68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`

Owner decision options:

```text
1. RETAIN_ASSEMBLYAI_AND_CLOSE_M3
2. M3C_TARGETED_CORPUS
3. HOLD_WITHOUT_CUTOVER
```

No option is implied by CI or evidence. Any further provider-consuming run requires separate explicit authorization.

## Remaining evidence gaps

The seven-case corpus does not materially cover:

- real multi-speaker conversation;
- code-switching;
- telephone-bandwidth speech;
- noisy Ukrainian;
- noisy Russian;
- longer real-world geopolitical media recordings.

## M4 - New-infrastructure canary

Status: NOT_STARTED.

M4 requires a KRC-specific deployment-image parity audit before any canary. M3 completion alone does not authorize M4.

## M5 - Cutover decision

Status: NOT_AUTHORIZED.

Any KRC prerecorded provider or infrastructure cutover requires separate explicit owner approval and verified rollback to the accepted AssemblyAI path.

## Release hold

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 backend/production promotion                 HOLD
R3 external testers                             HOLD
R4 public sharing / Store rollout               HOLD
```

Provider evidence, successful CI, or VoiceBridge Phase 2 completion does not automatically authorize any release gate.
