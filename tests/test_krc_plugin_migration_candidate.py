from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "plugins" / "krc_migration_candidate"
CORE = ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md"
SKILL = CANDIDATE / "skills" / "krc_core" / "SKILL.md"
CONTRACT = CANDIDATE / "contracts" / "media_tools.yaml"
OPENAPI = ROOT / "gpt_store" / "actions" / "media_public_r3_openapi.yaml"
README = CANDIDATE / "README.md"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def openapi_operations() -> dict[str, tuple[str, str]]:
    schema = load_yaml(OPENAPI)
    operations: dict[str, tuple[str, str]] = {}
    for route, path_item in schema["paths"].items():
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if operation and operation.get("operationId"):
                operations[operation["operationId"]] = (method.upper(), route)
    return operations


def test_core_skill_snapshot_is_exact_canonical_core() -> None:
    text = SKILL.read_text(encoding="utf-8")
    begin = "<!-- BEGIN KRC CORE EXACT SNAPSHOT -->\n"
    end = "\n<!-- END KRC CORE EXACT SNAPSHOT -->"
    assert begin in text
    assert end in text
    snapshot = text.split(begin, 1)[1].split(end, 1)[0].rstrip("\n")
    canonical = CORE.read_text(encoding="utf-8").rstrip("\n")
    assert snapshot == canonical


def test_media_candidate_has_exact_13_operation_parity() -> None:
    contract = load_yaml(CONTRACT)
    expected = openapi_operations()
    tools = contract["tools"]

    assert contract["operation_count"] == 13
    assert len(tools) == 13
    assert len(expected) == 13

    actual = {
        tool["source_operation_id"]: (tool["method"], tool["path"])
        for tool in tools
    }
    assert actual == expected
    assert len({tool["candidate_name"] for tool in tools}) == 13


def test_media_candidate_preserves_free_only_fail_closed_policy() -> None:
    contract = load_yaml(CONTRACT)
    policy = contract["policy"]
    assert policy["paid_retrieval_fallback"] is False
    assert policy["paid_stt_fallback"] is False
    assert policy["paid_proxy_fallback"] is False
    assert policy["supadata_public_active"] is False
    assert policy["scrapecreators_public_active"] is False
    assert policy["cookie_login_fallback"] is False
    assert policy["automatic_retry_loop"] is False
    assert policy["failed_free_only_retry"] == "fresh_deterministic_job_on_new_explicit_retry_request"
    assert policy["failed_paid_or_charge_uncertain_retry"] == "blocked"


def test_youtube_consent_and_provider_boundary_are_preserved() -> None:
    contract = load_yaml(CONTRACT)
    consent = contract["youtube_consent"]
    assert consent == {
        "preflight_calls_provider": False,
        "provider": "google_gemini",
        "tier": "free",
        "data_use_acknowledged": True,
        "required_before_start": True,
    }

    tools = {tool["source_operation_id"]: tool for tool in contract["tools"]}
    assert tools["startPublicGeminiYoutubeTranscription"]["requires_explicit_user_consent"] is True
    assert contract["routes"]["youtube"] == "Gemini Developer API Free Tier direct URL"


def test_platform_specific_media_guards_are_preserved() -> None:
    contract = load_yaml(CONTRACT)
    guards = contract["hard_guards"]
    assert "cobalt_fallback" in guards["youtube"]["forbid"]
    assert "assemblyai_fallback" in guards["youtube"]["forbid"]
    assert guards["facebook"]["canonical_retrieval"] == "cobalt_video_plus_audio"
    assert guards["facebook"]["normalization"] == "mono_pcm_wav_16khz"
    assert guards["telegram"]["canonical_retrieval"] == "telegram_public_web"
    assert guards["instagram"]["canonical_retrieval"] == "cobalt"


def test_candidate_does_not_guess_final_plugin_or_mcp_packaging() -> None:
    readme = README.read_text(encoding="utf-8")
    assert "DESIGN_ONLY / NOT_INSTALLABLE / NOT_DEPLOYED" in readme
    assert not (CANDIDATE / "mcp.json").exists()
    assert not (CANDIDATE / ".mcp.json").exists()
    assert not (CANDIDATE / ".app.json").exists()


def test_candidate_contains_no_concrete_browser_profile_or_common_secret_prefix() -> None:
    candidate_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    )
    lowered = candidate_text.lower()
    assert "prof_" not in candidate_text
    assert "sk-proj-" not in lowered
    assert "sk-live-" not in lowered
    assert "bearer eyj" not in lowered


def test_authentication_is_explicitly_unfinalized_and_server_side_only() -> None:
    auth = load_yaml(CONTRACT)["authentication"]
    assert auth["final_strategy"] == "TBD_AFTER_ACCOUNT_MIGRATION_SURFACE_INSPECTION"
    assert auth["secret_visibility"] == "SERVER_SIDE_ONLY"
    assert auth["model_visible_secret"] is False
    assert auth["repository_secret"] is False
