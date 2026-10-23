# KRC 0.19.12 — M01–M07 owner-observed acceptance baseline
Date: 2026-10-23. Status: ACCEPTANCE SNAPSHOT; NO RELEASE CHANGE.
Plugin: PRIVATE USER `0.19.12`, release `pluginrel_6ada5b660e188191a65080aa5762eeef`. Source: owner-supplied screenshots, response texts and exported Markdown/DOCX/PDF. GitHub canonical rules: `prompts/GPT_STORE_INSTRUCTIONS.md`.

## Observed matrix
| Test | Outcome | Evidence summary |
|---|---|---|
| M01 | PASS | Four-item compact menu, no full CriticProfile by default, no automatic research. |
| M02 | PARTIAL | Option 1 starts Core; evidence provenance/ledger improved on repeat, but approval-event timestamp provenance lacks independent execution log; actual implementation not independently attested. |
| M03 | PARTIAL | Option 2 activates Scholarly Research, manual route reflected; produced critical literature review, not full reproducible manuscript; novelty/search and publication gate incomplete. |
| M04 | PASS | Option 3 displays full CriticProfile REVIEW_REQUIRED without research. |
| M05 | PASS | Option 4 cancels without initiating research. |
| M06 | PASS | Explicit demand for full CriticProfile bypasses compact menu, remains REVIEW_REQUIRED. |
| M07 | PASS | Manual CORE to SCHOLARLY edit increments profile v1.0 to v1.1, retains topic, keeps REVIEW_REQUIRED, no research. |

Overall: **5 PASS / 2 PARTIAL / 0 FAIL** for the scoped user-observed scenarios. This is not a general accuracy guarantee. M03 reference review has not been independently reproduced from every primary text.

## Outstanding issues
1. Evidence independence is inferred from described methods/papers; raw lab data/reproduction not independently audited.
2. `approved_at` is shown with a plausible tool-origin claim, but there is no independently auditable per-event log to prove exact selection time.
3. P0 scholarly manuscript acceptance not achieved: full search protocol, novelty check, journal policy, manuscript/revision history and authorized AI-detector outputs still needed.
4. Export: Markdown/DOCX/PDF with tables tested, prototype graphic export tested off-plugin; full in-plugin figure parity not established.

## Engineering decision
Freeze this as test baseline, not P0 acceptance. Keep FREE_ONLY, NO_MCP private and no Public/MEDIA/deploy changes. Proceed P0.4–P0.7 separately. Formal PZ isolated destructive/fault-injection/negative campaign LAST per canonical roadmap; ordinary bounded unit negative fixtures may occur during P0.
