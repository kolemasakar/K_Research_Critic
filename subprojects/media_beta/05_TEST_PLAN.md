# MEDIA BETA Test Plan
План автоматизованої та живої перевірки працездатності закритої beta-версії без ризику для production.

Version: 1.0
Status: ACTIVE
Updated: 2026-08-17

## 1. Test goals

Validate that:

- beta admission control works;
- transcript acquisition is reliable enough for claim research;
- captions are preferred over paid/exhaustible STT;
- AssemblyAI fallback is bounded;
- Ukrainian, Russian, and English media are usable;
- transcript source is never treated as independent proof;
- CriticProfile approval gate is preserved;
- production text workflow and VoiceBridge streaming workflow do not regress.

## 2. Automated CI gates

### VoiceBridge feature branch

Required:

- TypeScript build PASS;
- cloud tests PASS;
- media beta tests PASS;
- existing VoiceBridge streaming tests PASS;
- browser extension regression PASS;
- repository documentation/policy checks PASS.

### K-Research & Critic feature branch

Required:

- Python 3.13 full tests PASS;
- Python 3.14 full tests PASS;
- dependency integrity PASS;
- Ruff PASS;
- Mypy PASS;
- repository validation PASS;
- GPT Store/package validation PASS;
- coverage gate PASS.

Any red CI blocks merge/promotion.

## 3. Backend live acceptance matrix

### B01 - Health

Input:

beta `/api/v1/health`.

Pass:

- HTTP 200;
- media capability configured;
- expected beta limits visible/consistent.

### B02 - Production isolation

Input:

production VoiceBridge `/api/v1/health` before and after beta deploy.

Pass:

- production remains healthy and behavior/version baseline unchanged.

### B03 - Missing Action bearer

Pass:

- request rejected;
- no media job created.

### B04 - Invalid tester code

Pass:

- HTTP 403 / beta access denied;
- supplied code not returned in response.

### B05 - Caption-first success

Use short YouTube video with usable source-language captions.

Pass:

- completed transcript;
- `transcript_source=youtube_captions`;
- `stt_seconds_charged=0`;
- usable timestamp segments.

### B06 - AssemblyAI fallback success

Use short video without usable captions.

Pass:

- fallback runs;
- `transcript_source=assemblyai_stt`;
- STT seconds charged approximately equal reserved source duration policy;
- transcript segments returned;
- temporary media removed after processing.

### B07 - Provider cleanup

Pass:

- successful AssemblyAI case reports `provider_data_deleted=true` when provider deletion succeeds;
- if false, system does not claim cleanup succeeded.

### B08 - Ukrainian

Pass:

- subject and key claims intelligible;
- names/numbers checked manually against source;
- timestamps usable.

### B09 - Russian

Same acceptance as B08.

### B10 - English

Same acceptance as B08.

### B11 - Auto language detection

Pass:

- detected language is plausible;
- transcript quality comparable with explicit hint for representative sample.

### B12 - Duration limit

Input:

video >60 minutes.

Pass:

- rejected before costly STT processing.

### B13 - Concurrency

Input:

second fallback job while one is active.

Pass:

- second job rejected/bounded according to beta contract;
- no uncontrolled parallel STT.

### B14 - Daily STT quota

Pass:

- AssemblyAI fallback cannot exceed configured daily budget under normal process lifetime;
- captions remain usable when STT budget is exhausted.

### B15 - Duplicate request reuse

Pass:

- repeated same normalized URL/language does not unnecessarily repeat non-failed transcript work during TTL where reuse is supported.

## 4. GPT Builder beta acceptance matrix

### G01 - Separate identity

Pass:

- beta GPT is distinct from published K-Research & Critic.

### G02 - Missing tester code

Pass:

- GPT asks for beta access code;
- it does not call the Action first.

### G03 - Secret discipline

Pass:

- tester code is not echoed after use;
- no provider/developer secret is requested from tester.

### G04 - Transcript intake only before profile

Pass:

- system may obtain transcript and identify claims;
- no independent truth research occurs before CriticProfile approval.

### G05 - CriticProfile gate

Pass:

- profile is displayed;
- workflow stops for APPROVE/EDIT/REJECT.

### G06 - Full media research

After APPROVE:

- independent sources are used;
- video is not used as self-corroboration;
- material claims receive verdicts;
- timestamps link claims back to transcript;
- uncertainty is stated.

### G07 - Final output

Pass:

- FINAL REPORT present;
- CLAIM VERIFICATION present;
- REVIEW PROTOCOL present;
- beta code absent;
- hidden reasoning absent.

### G08 - Text workflow regression

Use an ordinary non-media research task.

Pass:

- existing CriticProfile -> Research -> Critic workflow works without beta code or media backend.

### G09 - Checkpoint regression

Pass:

- existing checkpoint schema 1.0 still validates;
- full transcript absent;
- beta access code absent.

## 5. Resource acceptance

During beta record real measurements for at least 10 representative media jobs:

- video duration;
- caption or STT path;
- downloaded/uploaded audio size if fallback;
- STT seconds charged;
- Render bandwidth change;
- AssemblyAI credit change;
- total elapsed transcription time;
- transcript quality notes.

No public rollout decision should be made without this measured sample.

## 6. Reliability scoring for transcript intake

For each language sample classify:

- names/proper nouns;
- numbers and units;
- dates;
- acronyms;
- technical terminology;
- sentence segmentation;
- timestamp alignment.

Use qualitative grades:

`GOOD / ACCEPTABLE_WITH_REVIEW / POOR`

A POOR transcript for material claims requires either alternate transcript acquisition or explicit limitation before research.

## 7. Beta exit criteria

Closed beta can be considered technically validated when:

- all critical B and G tests pass;
- no production regression exists;
- at least owner + one external tester complete representative media tasks;
- resource consumption is measured;
- no credential leakage is observed;
- transcript errors are bounded and surfaced;
- user explicitly approves moving to the next architecture/release phase.