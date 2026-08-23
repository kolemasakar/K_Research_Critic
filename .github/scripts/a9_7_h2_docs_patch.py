from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"missing anchor in {path}: {old[:80]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"non-unique anchor in {path}: {old[:80]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Manifest: accept only the tested free Cobalt path. Keep the historical A9.6
# Supadata Facebook route incomplete and keep the paid ScrapeCreators path unaccepted.
replace_once(
    "gpt_store/media_beta_manifest.yaml",
    "  public_platforms_live_accepted:\n    - youtube\n    - instagram\n  public_platforms_in_progress:\n    - facebook\n",
    "  public_platforms_live_accepted:\n    - youtube\n    - instagram\n    - facebook\n  public_platforms_in_progress: []\n",
)
replace_once(
    "gpt_store/media_beta_manifest.yaml",
    "  managed_facebook_free_retrieval_provider: cobalt\n  managed_facebook_paid_retrieval_provider: scrapecreators\n",
    "  managed_facebook_free_retrieval_provider: cobalt\n  managed_facebook_free_path_live_accepted: true\n  managed_facebook_paid_retrieval_provider: scrapecreators\n  managed_facebook_paid_retrieval_configured: false\n  managed_facebook_paid_fallback_live_accepted: false\n",
)
replace_once(
    "gpt_store/media_beta_manifest.yaml",
    "  managed_facebook_live_accepted: false\n",
    "  managed_facebook_live_accepted: true\n",
)
replace_once(
    "gpt_store/media_beta_manifest.yaml",
    "  rollout_state: A9_6_INSTAGRAM_COMPLETE_FACEBOOK_IN_PROGRESS\n",
    "  rollout_state: A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED\n",
)
replace_once(
    "gpt_store/media_beta_manifest.yaml",
    "  a9_7_c_facebook_live_acceptance_complete: false\n",
    "  a9_7_c_facebook_live_acceptance_complete: true\n  a9_7_h1_facebook_cobalt_live_acceptance_complete: true\n",
)

# Validator expectations.
replace_once(
    "scripts/validate_store_package.py",
    '_require(beta.get("public_platforms_live_accepted") == ["youtube", "instagram"], "YouTube and Instagram must be declared live accepted")',
    '_require(beta.get("public_platforms_live_accepted") == ["youtube", "instagram", "facebook"], "YouTube, Instagram, and the accepted Facebook free path must be declared live accepted")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(beta.get("public_platforms_in_progress") == ["facebook"], "Facebook must remain in progress until isolated live acceptance")',
    '_require(beta.get("public_platforms_in_progress") == [], "No public platform may remain in progress after Facebook Cobalt live acceptance")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(beta.get("managed_facebook_free_retrieval_provider") == "cobalt", "Facebook free retrieval provider must be Cobalt")\n    _require(beta.get("managed_facebook_paid_retrieval_provider") == "scrapecreators", "Facebook paid retrieval provider must be ScrapeCreators")',
    '_require(beta.get("managed_facebook_free_retrieval_provider") == "cobalt", "Facebook free retrieval provider must be Cobalt")\n    _require(beta.get("managed_facebook_free_path_live_accepted") is True, "Facebook Cobalt free path must be live accepted")\n    _require(beta.get("managed_facebook_paid_retrieval_provider") == "scrapecreators", "Facebook paid retrieval provider must be ScrapeCreators")\n    _require(beta.get("managed_facebook_paid_retrieval_configured") is False, "ScrapeCreators must remain unconfigured in this acceptance state")\n    _require(beta.get("managed_facebook_paid_fallback_live_accepted") is False, "ScrapeCreators paid fallback must remain not live accepted")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(beta.get("managed_facebook_live_accepted") is False, "Facebook must not be marked live accepted before isolated deployment evidence")',
    '_require(beta.get("managed_facebook_live_accepted") is True, "Facebook free Cobalt path must be marked live accepted after H1 evidence")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(release.get("rollout_state") == "A9_6_INSTAGRAM_COMPLETE_FACEBOOK_IN_PROGRESS", "live rollout state must remain pre-Facebook-acceptance")',
    '_require(release.get("rollout_state") == "A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED", "rollout state must record the accepted Facebook Cobalt free path")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(release.get("a9_6_facebook_complete") is False, "Facebook must not be pre-declared complete")',
    '_require(release.get("a9_6_facebook_complete") is False, "Historical A9.6 Supadata Facebook route must remain incomplete")',
)
replace_once(
    "scripts/validate_store_package.py",
    '_require(release.get("a9_7_c_facebook_live_acceptance_complete") is False, "A9.7-C must not pre-declare live acceptance")',
    '_require(release.get("a9_7_c_facebook_live_acceptance_complete") is True, "A9.7 Facebook runtime contract must record live acceptance")\n    _require(release.get("a9_7_h1_facebook_cobalt_live_acceptance_complete") is True, "A9.7-H1 Cobalt acceptance evidence must be recorded")',
)

# Regression expectations.
replace_once(
    "tests/test_media_beta_managed_package.py",
    '    assert beta["public_platforms_live_accepted"] == ["youtube", "instagram"]\n    assert beta["public_platforms_in_progress"] == ["facebook"]\n',
    '    assert beta["public_platforms_live_accepted"] == ["youtube", "instagram", "facebook"]\n    assert beta["public_platforms_in_progress"] == []\n',
)
replace_once(
    "tests/test_media_beta_managed_package.py",
    '    assert beta["managed_facebook_free_retrieval_provider"] == "cobalt"\n    assert beta["managed_facebook_paid_retrieval_provider"] == "scrapecreators"\n',
    '    assert beta["managed_facebook_free_retrieval_provider"] == "cobalt"\n    assert beta["managed_facebook_free_path_live_accepted"] is True\n    assert beta["managed_facebook_paid_retrieval_provider"] == "scrapecreators"\n    assert beta["managed_facebook_paid_retrieval_configured"] is False\n    assert beta["managed_facebook_paid_fallback_live_accepted"] is False\n',
)
replace_once(
    "tests/test_media_beta_managed_package.py",
    '    assert beta["managed_facebook_live_accepted"] is False\n',
    '    assert beta["managed_facebook_live_accepted"] is True\n',
)
replace_once(
    "tests/test_media_beta_managed_package.py",
    '    assert release["a9_7_c_facebook_live_acceptance_complete"] is False\n',
    '    assert release["a9_7_c_facebook_live_acceptance_complete"] is True\n    assert release["a9_7_h1_facebook_cobalt_live_acceptance_complete"] is True\n',
)

# Canonical index/current-state updates. The A9.6 deferral remains historical.
replace_once("subprojects/media_beta/00_INDEX.md", "Version: 3.3\n", "Version: 3.4\n")
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "21. `40_FACEBOOK_REMEDIATION_DEFERRED.md` - owner decision to defer A9.6 Facebook remediation while preserving the non-replay safety boundary.\n",
    "21. `40_FACEBOOK_REMEDIATION_DEFERRED.md` - historical owner decision to defer the failed A9.6 Supadata route.\n22. `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md` - live acceptance of the free Facebook Cobalt -> AssemblyAI -> durable KRCM path.\n",
)
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "3. `40_FACEBOOK_REMEDIATION_DEFERRED.md` for the current Facebook work disposition;\n",
    "3. `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md` for the current Facebook live-acceptance boundary;\n",
)
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_DEFERRED_NOT_ACCEPTED",
    "A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_SUPADATA_NOT_ACCEPTED / A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED",
)
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "- `gpt_builder_private_update_required = false`.\n",
    "- `gpt_builder_private_update_required = true`.\n",
)
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "- live-accepted zero-client adapters: YouTube and Instagram Reel;\n- Facebook is deferred by owner and remains not accepted;\n",
    "- live-accepted zero-client adapters: YouTube, Instagram Reel, and Facebook through the free Cobalt -> AssemblyAI path;\n- ScrapeCreators remains an unconfigured, not-live-accepted paid fallback requiring a separate one-credit consent;\n",
)
replace_once(
    "subprojects/media_beta/00_INDEX.md",
    "Facebook remediation is intentionally skipped for now. No substitute task is implied; choose the next project direction explicitly.\n",
    "Backend Facebook free-path acceptance is complete. The next media gate is the private GPT Builder update and owner new-chat Facebook E2E; this documentation update does not perform that Builder change.\n",
)

replace_once("subprojects/media_beta/03_CURRENT_STATE.md", "Version: 5.4\n", "Version: 5.5\n")
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    "A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_DEFERRED_NOT_ACCEPTED",
    "A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_SUPADATA_NOT_ACCEPTED / A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED",
)
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    "Accepted owner-only zero-client adapters:\n- public prerecorded YouTube;\n- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable.\n\nDeferred / not accepted:\n- Facebook public Video/Reels — remediation explicitly deferred by owner on 2026-08-23;\n- Telegram public video posts;\n- local audio/video attachment.\n",
    "Accepted owner-only zero-client adapters:\n- public prerecorded YouTube;\n- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable;\n- public Facebook Video/Reels through the free Cobalt retrieval path followed by AssemblyAI STT and durable KRCM persistence.\n\nDeferred / not accepted:\n- ScrapeCreators paid Facebook fallback (unconfigured and not live accepted);\n- Telegram public video posts;\n- local audio/video attachment.\n",
)
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    "`gpt_builder_private_update_required = false`\n",
    "`gpt_builder_private_update_required = true`\n",
)
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    " -> Instagram only: if native unavailable, separate AI preflight + separate explicit consent\n -> CriticProfile gate\n",
    " -> Instagram only: if native unavailable, separate AI preflight + separate explicit consent\n -> Facebook: free Cobalt retrieval first; AssemblyAI only after media retrieval; paid ScrapeCreators continuation never automatic\n -> CriticProfile gate\n",
)
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    "### A9.6 - Facebook\n\nDEFERRED BY OWNER / NOT_ACCEPTED.\n",
    "### A9.6 - Facebook Supadata route\n\nHISTORICAL / NOT_ACCEPTED.\n",
)
replace_once(
    "subprojects/media_beta/03_CURRENT_STATE.md",
    "## Next task\n\nFacebook remediation is intentionally skipped for now. No replacement engineering task is implied by this checkpoint; select the next project direction explicitly.\n\nThese markers do NOT authorize repository merge, external tester rollout, production VoiceBridge changes, private/authenticated media, automatic AI fallback, Facebook acceptance, Telegram, or local upload.\n",
    "### A9.7 - Facebook Cobalt free path\n\nLIVE ACCEPTED for the isolated owner beta. H1 evidence: job `KRCM_0d2a512d-c90d-4b41-87b7-3d3f47d258bd` completed through `retrieval_provider=cobalt` and `provider=assemblyai`, with 0 retrieval credits, 23 STT seconds, 1 durable segment, 101 transcript characters, and a successful durable reread/segments read. ScrapeCreators and Supadata were not called.\n\nCanonical acceptance record: `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md`.\n\n## Next task\n\nBackend Facebook free-path acceptance is complete. The next media gate is to apply the A9.7-C Action schema/instructions to the actual private Custom GPT Builder and run one owner new-chat Facebook zero-client E2E. ScrapeCreators remains outside live acceptance and still requires a fresh explicit one-credit approval before any real call.\n\nThese markers do NOT authorize repository merge, external tester rollout, production VoiceBridge changes, private/authenticated media, automatic AI fallback, ScrapeCreators paid-fallback acceptance, Telegram, or local upload.\n",
)

acceptance = ROOT / "subprojects/media_beta/41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md"
acceptance.write_text(
    """# A9.7 Facebook Cobalt Live Acceptance\n\nStatus: LIVE_ACCEPTED_FREE_PATH\nDate: 2026-08-23\nScope: isolated owner-only MEDIA BETA\n\n## Accepted path\n\n`Facebook public URL -> VoiceBridge -> Cobalt -> media asset -> AssemblyAI STT -> durable KRCM transcript`\n\nThe accepted scope is the free Cobalt retrieval path only. The ScrapeCreators paid fallback is not configured and is not live accepted. It remains a separately consent-gated maximum-one-credit contingency path.\n\n## H1 evidence\n\nTest URL: public Facebook Reel `1114235920664408`.\n\nObserved result:\n- HTTP start: 200;\n- job: `KRCM_0d2a512d-c90d-4b41-87b7-3d3f47d258bd`;\n- final status: `COMPLETED`;\n- provider mode: `facebook_retrieval_stt`;\n- retrieval provider: `cobalt`;\n- retrieval credits charged: 0;\n- STT provider: `assemblyai`;\n- STT seconds charged: 23;\n- durable segment count: 1;\n- transcript characters: 101;\n- durable job reread: `COMPLETED`;\n- segments read: HTTP 200;\n- terminal error: none.\n\nThe first H1 workflow attempt failed before the HTTP start because its PR-job Action token was empty. No Facebook, Cobalt, or AssemblyAI request occurred in that failed setup attempt. The corrected H1 run obtained the already configured Action token server-side from Render and performed the single real acceptance start.\n\n## Safety and cost boundary\n\nNo ScrapeCreators request was made. No Supadata request was made. No paid Facebook continuation was invoked. AssemblyAI ran only because Cobalt returned media. Production VoiceBridge, repository main branches, and merge state were unchanged.\n\n## Historical A9.6 distinction\n\nThe earlier A9.6 Supadata Facebook route remains not accepted. Its failed/empty transcript behavior and non-replay rules remain historical evidence. A9.7 does not retroactively mark A9.6 complete.\n\n## Current product state\n\nFacebook is live accepted for the isolated owner beta only through the free Cobalt path. The actual private Custom GPT Builder still requires the A9.7-C schema/instruction update before private-GPT Facebook E2E can be marked accepted.\n""",
    encoding="ascii",
)
