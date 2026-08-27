# MEDIA BETA Release Hold Owner Testing Checkpoint

Frozen project-state checkpoint for resuming MEDIA BETA without reconstructing prior work.

Checkpoint date: 2026-08-27
Status: RELEASE_HOLD_OWNER_TESTING
Scope: isolated private owner-only K-Research & Critic MEDIA BETA

## Decision captured

The owner has explicitly decided not to merge or promote the MEDIA BETA yet.

Current release decision:

```text
merge KRC feature branch to main = HOLD
production VoiceBridge promotion = HOLD
external tester onboarding = HOLD
public sharing / Store rollout = HOLD
```

The intended operating mode is continued private owner testing for a period of time. Release decisions will be reconsidered later from this checkpoint.

## Repository state baseline

KRC implementation state immediately before this checkpoint record:
- repository: `kolemasakar/K_Research_Critic`;
- active feature branch: `agent/video-url-research`;
- implementation head: `c8588ec1f13c3c576d3f307a001c1d8964b5128e`;
- draft PR: `#8`;
- PR state: open, draft, unmerged;
- base branch: `main`;
- `main` has not been changed by the MEDIA BETA release decision.

VoiceBridge implementation state:
- repository: `kolemasakar/VoiceBridge`;
- active feature branch: `agent/krc-media-transcript`;
- implementation head: `20afd2e54b87b4a2a8858961a03e22f78a565189`;
- draft PR: `#28`;
- PR state: open, draft, unmerged;
- base branch: `main`;
- production VoiceBridge is not targeted by this checkpoint.

Checkpoint/documentation commits after the KRC implementation head above are metadata-only unless explicitly stated otherwise.

## Last verified KRC CI

Workflow: `Tests`
Run: `33010660835`
Head: `c8588ec1f13c3c576d3f307a001c1d8964b5128e`
Conclusion: `SUCCESS`

Verified gates include:
- Quality gates;
- Python 3.13 tests;
- Python 3.14 tests;
- dependency integrity;
- Ruff;
- mypy;
- repository policy validation;
- GPT Store package validation;
- coverage gate.

## Accepted functional state

A9 owner zero-client media input: ACCEPTED.

Accepted owner-only ingress:
- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel through free Cobalt retrieval, then AssemblyAI, then durable KRCM;
- supported public Telegram video posts through public Telegram web/embed retrieval, then trusted Telegram CDN, then AssemblyAI, then durable KRCM;
- one current-conversation local audio/video attachment through `openaiFileIdRefs`, trusted OpenAI attachment delivery, AssemblyAI, then durable KRCM.

A9.10 local attachment: ACCEPTED.

Accepted local attachment evidence includes:
- real approximately 5 MB MP4;
- full private-GPT attachment ingestion;
- AssemblyAI STT;
- durable KRCM transcript/segments;
- CriticProfile gate;
- explicit owner approval;
- Research/Critic final report;
- retrieval/provider credits `0`;
- real SHORTFALL preserved;
- no KRCM Job ID, OpenAI file ID, signed URL or provider credential exposed.

A10 stabilization: ACCEPTED.

Accepted A10 state:
- Builder package `0.9.1-beta-a10`;
- Action schema `0.6.0-a9.10`;
- visible four-column claim-summary table runtime accepted;
- fenced copy-safe duplicate runtime accepted;
- whole-response Copy preserves the fenced pipe-delimited duplicate;
- real SHORTFALL remains visible and qualifies final status;
- no backend/VoiceBridge change required for A10.

Authoritative marker:

`A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED`

## Accepted Research/Critic contract

- two-stage CriticProfile gate is runtime accepted;
- profile is created before independent research;
- option `1` approves/direct-runs;
- option `2` reviews/edits;
- option `3` cancels;
- material profile changes require re-approval;
- claim-level cross-check floors are `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim tracks `required / achieved_independent / exception`;
- achieved counts independent evidence origins, not URLs;
- achieved cannot exceed visible traceable origins;
- an unqualified PASS is forbidden when a required cross-check is missing;
- report language defaults to Ukrainian unless explicitly changed by the user.

## Active media policy invariants

Facebook:
- active retrieval is free Cobalt only;
- Cobalt success -> AssemblyAI -> durable KRCM;
- Cobalt failure -> media unavailable -> STOP;
- ScrapeCreators remains reserve-only, unconfigured, inactive and not offerable;
- no automatic or active paid Facebook fallback.

Telegram:
- public Telegram posts only;
- no account/session/cookies/bot token;
- public web/embed -> trusted Telegram CDN -> AssemblyAI -> durable KRCM;
- retrieval credits `0`;
- no paid Telegram fallback.

Local attachment:
- one supported current-conversation audio/video attachment;
- `startManagedAttachmentTranscription`;
- trusted `*.oaiusercontent.com` delivery boundary;
- maximum attachment size `32 MiB`;
- retrieval provider `openai_attachment`;
- retrieval credits `0`;
- no Helper, file token, signed URL or credential exposed.

General:
- private Action bearer remains required;
- automatic managed AI fallback is prohibited;
- billable Supadata paths retain explicit consent gates;
- uncertain-charge operations are never automatically retried;
- A8 Helper remains fallback evidence only and is not normal owner UX.

## Isolated runtime boundary

Private GPT: `K-Research & Critic - MEDIA BETA`.

VoiceBridge beta service: `voicebridge-krc-media-beta-kolemasakar`.

The current testing period is owner-only. No external tester or public rollout is authorized.

## Known accepted limitation

ChatGPT whole-response Copy can collapse the header of a visually correct rendered Markdown table.

Accepted mitigation:
- render the normal four-column table;
- immediately provide `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ` as a fenced `text` table with literal `|` delimiters.

The copy-safe duplicate has passed owner runtime testing. This UI serialization defect is not treated as a KRC claim-accounting failure.

## Release hold boundary

During the owner-testing hold:
- do not merge PR #8;
- do not merge PR #28;
- do not change KRC `main` for MEDIA release;
- do not deploy/promote MEDIA changes to production VoiceBridge;
- do not enable external tester access;
- do not make the MEDIA GPT public or publish it to the Store;
- do not enable ScrapeCreators or paid Telegram retrieval;
- do not weaken existing credit, privacy, fallback or traceability gates.

Defects found during owner testing should be fixed only in the isolated feature branches and revalidated there unless the owner explicitly changes the release decision.

## Resume procedure

When resuming work from this checkpoint:
1. read `00_INDEX.md`;
2. read `03_CURRENT_STATE.md`;
3. read this checkpoint;
4. verify current heads of KRC `agent/video-url-research` and VoiceBridge `agent/krc-media-transcript`;
5. inspect draft PR #8 and draft PR #28;
6. if heads differ from this checkpoint, review only the delta before continuing;
7. keep RELEASE_HOLD_OWNER_TESTING unless the owner explicitly authorizes a release transition.

A later release decision should separately decide each gate:
- merge to `main`;
- production promotion;
- external testers;
- public rollout.

Do not infer authorization for one gate from authorization for another.

## Final checkpoint marker

`MEDIA_BETA_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT_2026_08_27`
