# KRC Plus-first NO_MCP distribution — implementation checkpoint
Date: 2026-10-19

## Scope and owner authorization
Owner requested steps 1–5: sync core, verify pre-existing KRC GPT reachability, choose one-time distribution path, second independent Plus account test, prepare publication. Owner-approved NO_MCP policy, no Cobalt/MEDIA changes.

## Actions executed and sources
1. Canonical source `prompts/GPT_STORE_INSTRUCTIONS.md` fetched and retained. It already defines CriticProfile approval, risk floors, evidence ledger, source-independence and visible final report. Added explicit NO_MCP Plus distribution policy, without removing research methodology. New commit `87c2a8671b063e82878e1e68fd2a22c350df5d8f`.
2. Current Plugin Creator metadata inspected: `plugins_6acef8a60d708191bf37778f71e4562d`, R4 limited private v0.1.1, `scope=USER`, `discoverability=PRIVATE`, includes MEDIA applications. Keep untouched; do NOT treat as publicly shareable Plus plugin.
3. OpenAI Help Center: GPTs in ChatGPT, Creating and editing GPTs, Sharing and publishing GPTs. Personal Plus accounts cannot create/publish new GPTs; pre-existing GPTs can be used and edited with permission. Sharing options for pre-existing GPTs depend on account/editor controls. September 11, 2026 release notes: planned GPT retirement/migration to plugins; rollout varies.
4. OpenAI Plugins documentation: plugin directory across plans, but personal plugin sharing/public availability not automatically established; workspace plugin sharing and publishing permission details apply to managed workspaces. Sites hosting MCP is optional and does NOT satisfy approved no-MCP baseline.
5. Pre-existing candidate GPT URL supplied previously by owner: `https://chatgpt.com/g/g-6a7ed4905f5c81918190d12ec5f27e9b-k-research-critic`. Direct browser retrieval unavailable in current environment; cannot verify current visibility/owner sharing settings.

## Preferred eligible path
- Prefer **existing KRC GPT shared by link** if the existing GPT editor exposes a sharing option usable by separate Plus user.
- GPT access via ChatGPT; no KRC registration, local installation, or private MCP.
- Since public GPT retirement is planned, treat as bridge, preserve Core Skill as durable source, review migration when available.
- If existing GPT sharing is blocked, no verified public PLUS distribution is yet established. Do not claim launch achieved. Optional alternative public Site is a website, not plugin within ChatGPT.

## Recipient-side acceptance protocol (not yet executed)
Owner opens https://chatgpt.com/gpts -> My GPTs -> pre-existing KRC -> Edit GPT.
- Verify edit permission, instruction sync with canonical Core Skill, and Save/Update.
- Select Share and inspect options. If 'Anyone with link' (or equivalent) is available, enable and copy URL without exposing editable rights. If not, record the actual option and stop distribution.
- Different Plus account, not the author, open the link in signed-in ChatGPT; verify it opens, permits independent chat and has no provider authorization prompt.
- Test a short low/medium-risk user query: CriticProfile created, 1/2/3 gate works, after explicit '1' research begins, final output contains claim-level cross-check and evidence traceability, no MCP/login prompt.
- Second account must not see owner's chat or private files. Verify no unexpected sharing of private knowledge/actions.
- Record screenshots or concise PASS/FAIL for: link open, permission, gate, report quality, privacy, installation/login.
- Only then declare PLUS distribution PASS or present a publication/share link as confirmed.

## Status
Step 1 COMPLETE: repo instructions synchronized.
Step 2 PARTIAL: plugin metadata verified, existing GPT sharing state not independently inspectable.
Step 3 DESIGN DECIDED: pre-existing GPT by link is preferred if allowed.
Step 4 BLOCKED on a real independent Plus account test and owner-accessible GPT Share panel.
Step 5 PREPARED, NOT PUBLISHED: acceptance protocol ready; no public release action taken.

No source code was deployed, modified, or exposed on OCI.
