from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_media_beta_manifest_uses_zero_client_managed_action() -> None:
    manifest = yaml.safe_load(
        (ROOT / "gpt_store" / "media_beta_manifest.yaml").read_text(encoding="utf-8")
    )

    assert manifest["product"]["publication_state"] == "private_owner_only"
    assert manifest["actions"]["media_transcript"]["schema"] == (
        "gpt_store/actions/media_managed_beta_openapi.yaml"
    )
    instructions = manifest["instructions"]
    assert instructions["profile_gate_mode"] == "two_stage_direct_or_review"
    assert instructions["profile_auto_display"] is False
    assert instructions["profile_direct_run_approves_profile"] is True
    assert instructions["profile_review_option"] == 2
    assert instructions["profile_cancel_option"] == 3
    assert instructions["recovered_review_required_uses_same_gate"] is True
    assert instructions["required_cross_checks_enforced"] is True
    assert instructions["cross_check_independence_required"] is True
    assert instructions["cross_check_shortfall_must_be_reported"] is True
    assert instructions["cross_check_protocol_summary_required"] is True
    assert instructions["cross_check_claim_level_ledger_required"] is True
    assert instructions["cross_check_claim_level_output_required"] is True
    assert instructions["cross_check_unqualified_pass_on_shortfall_forbidden"] is True
    assert instructions["cross_check_traceability_required"] is True
    assert instructions["cross_check_achieved_cannot_exceed_visible_origins"] is True
    assert instructions["cross_check_systematic_review_counts_as_one_origin"] is True
    assert instructions["cross_check_protocol_table_required"] is True
    assert instructions["user_visible_labels_localized_to_report_language"] is True
    assert instructions["criticprofile_field_labels_localized_to_report_language"] is True
    assert instructions["ukrainian_required_headings"] == [
        "ФІНАЛЬНИЙ ЗВІТ",
        "ПЕРЕВІРКА ТВЕРДЖЕНЬ",
        "ПРОТОКОЛ ПЕРЕВІРКИ",
        "ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ",
    ]
    assert instructions["cross_check_protocol_table_columns"] == [
        "Твердження",
        "Потрібно",
        "Отримано незалежних",
        "Виняток",
    ]
    assert instructions["cross_check_floor_by_risk"] == {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }
    beta = manifest["beta"]
    assert beta["ingress_mode"] == "managed_zero_client"
    assert beta["browser_helper_required"] is False
    assert beta["managed_job_prefix"] == "KRCM_"
    assert beta["managed_credit_preflight_required"] is True
    assert beta["managed_explicit_user_consent_required"] is True
    assert beta["managed_automatic_ai_fallback"] is False
    assert beta["managed_user_beta_access_code_required"] is False
    assert beta["public_platforms_live_accepted"] == ["youtube", "instagram", "facebook"]
    assert beta["public_platforms_in_progress"] == []
    assert beta["managed_instagram_ai_fallback_live_accepted"] is True
    assert beta["managed_facebook_retrieval_stt_code_ready"] is True
    assert beta["managed_facebook_free_retrieval_provider"] == "cobalt"
    assert beta["managed_facebook_free_path_live_accepted"] is True
    assert beta["managed_facebook_paid_retrieval_provider"] == "scrapecreators"
    assert beta["managed_facebook_paid_retrieval_configured"] is False
    assert beta["managed_facebook_paid_fallback_live_accepted"] is False
    assert beta["managed_facebook_paid_retrieval_max_credits"] == 1
    assert beta["managed_facebook_paid_retrieval_requires_separate_consent"] is True
    assert beta["managed_facebook_automatic_paid_retrieval"] is False
    assert beta["managed_facebook_stt_provider"] == "assemblyai"
    assert beta["managed_facebook_live_accepted"] is True

    release = manifest["release"]
    assert release["a9_3_durable_managed_complete"] is True
    assert release["a9_5_private_gpt_integration_complete"] is True
    assert release["a9_8_owner_zero_client_acceptance_complete"] is True
    assert release["a9_6_instagram_managed_complete"] is True
    assert release["a9_6_facebook_complete"] is False
    assert release["a9_7_c_facebook_runtime_code_ready"] is True
    assert release["a9_7_c_facebook_live_acceptance_complete"] is True
    assert release["a9_7_h1_facebook_cobalt_live_acceptance_complete"] is True
    assert release["criticprofile_gate_runtime_accepted"] is True
    assert release["cross_check_enforcement_hardened"] is True
    assert release["cross_check_claim_level_enforcement_hardened"] is True
    assert release["cross_check_claim_level_runtime_accepted"] is True
    assert release["cross_check_traceability_hardened"] is True
    assert release["cross_check_traceability_runtime_accepted"] is True
    assert release["report_label_localization_hardened"] is True
    assert release["report_label_localization_runtime_accepted"] is True
    assert release["gpt_builder_private_update_required"] is False


def test_managed_action_schema_hides_owner_admission_and_preserves_credit_gates() -> None:
    schema = yaml.safe_load(
        (ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml").read_text(
            encoding="utf-8"
        )
    )
    paths = schema["paths"]

    assert set(paths) == {
        "/api/v1/media/managed",
        "/api/v1/media/managed/preflight",
        "/api/v1/media/managed/transcriptions",
        "/api/v1/media/managed/facebook-fallback",
        "/api/v1/media/managed/transcriptions/{job_id}",
        "/api/v1/media/managed/transcriptions/{job_id}/segments",
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval-preflight",
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval",
        "/api/v1/media/managed/transcriptions/{job_id}/ai-preflight",
        "/api/v1/media/managed/transcriptions/{job_id}/ai",
    }
    assert paths["/api/v1/media/managed"]["get"]["operationId"] == (
        "getManagedMediaCapability"
    )
    assert paths["/api/v1/media/managed/preflight"]["post"]["operationId"] == (
        "preflightManagedMediaCredits"
    )
    start = paths["/api/v1/media/managed/transcriptions"]["post"]
    assert start["operationId"] == "startManagedMediaNativeTranscription"
    assert start["x-openai-isConsequential"] is True
    facebook_free = paths["/api/v1/media/managed/facebook-fallback"]["post"]
    assert facebook_free["operationId"] == "startManagedFacebookFallback"
    assert facebook_free["x-openai-isConsequential"] is False

    retrieval_preflight = paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval-preflight"
    ]["get"]
    assert retrieval_preflight["operationId"] == "preflightManagedFacebookRetrievalCredit"
    assert retrieval_preflight["x-openai-isConsequential"] is False

    retrieval_start = paths[
        "/api/v1/media/managed/transcriptions/{job_id}/facebook-retrieval"
    ]["post"]
    assert retrieval_start["operationId"] == "continueManagedFacebookPaidRetrieval"
    assert retrieval_start["x-openai-isConsequential"] is True

    ai_preflight = paths[
        "/api/v1/media/managed/transcriptions/{job_id}/ai-preflight"
    ]["get"]
    assert ai_preflight["operationId"] == "preflightManagedMediaAiCredits"
    assert ai_preflight["x-openai-isConsequential"] is False

    ai_start = paths["/api/v1/media/managed/transcriptions/{job_id}/ai"]["post"]
    assert ai_start["operationId"] == "startManagedMediaAiTranscription"
    assert ai_start["x-openai-isConsequential"] is True

    job_operations = [
        paths["/api/v1/media/managed/transcriptions/{job_id}"]["get"],
        paths["/api/v1/media/managed/transcriptions/{job_id}/segments"]["get"],
        retrieval_preflight,
        retrieval_start,
        ai_preflight,
        ai_start,
    ]
    for operation in job_operations:
        job_id = operation["parameters"][0]
        assert job_id["name"] == "job_id"
        assert job_id["in"] == "path"
        assert job_id["required"] is True
        assert job_id["schema"]["type"] == "string"
        assert job_id["schema"]["pattern"] == "^KRCM_[A-Za-z0-9-]+$"
        assert "$ref" not in job_id

    preflight = schema["components"]["schemas"]["PreflightRequest"]
    assert preflight["required"] == ["url"]
    assert "beta_access_code" not in preflight["properties"]

    facebook_request = schema["components"]["schemas"]["FacebookFallbackRequest"]
    assert facebook_request["required"] == ["url"]
    assert "credit_consent" not in facebook_request["properties"]
    assert "beta_access_code" not in facebook_request["properties"]

    native = schema["components"]["schemas"]["NativeTranscriptRequest"]
    assert native["type"] == "object"
    assert "allOf" not in native
    assert set(native["required"]) == {"url", "credit_consent"}
    assert "beta_access_code" not in native["properties"]
    native_consent = native["properties"]["credit_consent"]["properties"]
    assert native_consent["provider"]["const"] == "supadata"
    assert native_consent["mode"]["const"] == "native"
    assert native_consent["max_credits"]["minimum"] == 1
    assert native_consent["max_credits"]["maximum"] == 1

    retrieval_request = schema["components"]["schemas"]["FacebookRetrievalConsentRequest"]
    assert retrieval_request["required"] == ["credit_consent"]
    retrieval_consent = retrieval_request["properties"]["credit_consent"]["properties"]
    assert retrieval_consent["provider"]["const"] == "scrapecreators"
    assert retrieval_consent["mode"]["const"] == "facebook_post"
    assert retrieval_consent["max_credits"]["minimum"] == 1
    assert retrieval_consent["max_credits"]["maximum"] == 1

    retrieval_quote = schema["components"]["schemas"][
        "FacebookRetrievalCreditPreflight"
    ]["properties"]
    assert retrieval_quote["provider"]["const"] == "scrapecreators"
    assert retrieval_quote["mode"]["const"] == "facebook_post"
    assert retrieval_quote["estimated_credits"]["const"] == 1
    assert retrieval_quote["maximum_credits"]["const"] == 1
    assert retrieval_quote["provider_balance_lookup_performed"]["const"] is False
    assert retrieval_quote["consent_required"]["const"] is True

    ai_request = schema["components"]["schemas"]["AiTranscriptRequest"]
    assert ai_request["type"] == "object"
    assert "allOf" not in ai_request
    assert ai_request["required"] == ["credit_consent"]
    assert "beta_access_code" not in ai_request["properties"]
    ai_consent = ai_request["properties"]["credit_consent"]["properties"]
    assert ai_consent["provider"]["const"] == "supadata"
    assert ai_consent["mode"]["const"] == "generate"
    assert ai_consent["max_credits"]["const"] == 40

    ai_quote = schema["components"]["schemas"]["AiCreditPreflight"]["properties"]
    assert ai_quote["estimated_credits"]["minimum"] == 1
    assert ai_quote["maximum_credits"]["minimum"] == 1
    assert ai_quote["credits_per_minute"]["minimum"] == 0
    assert ai_quote["maximum_duration_minutes"]["minimum"] == 0
    assert "const" not in ai_quote["estimated_credits"]
    assert "const" not in ai_quote["maximum_credits"]

    job = schema["components"]["schemas"]["ManagedJob"]["properties"]
    assert set(job["status"]["enum"]) == {
        "PROCESSING",
        "COMPLETED",
        "AWAITING_AI_CONSENT",
        "AWAITING_RETRIEVAL_CONSENT",
        "FAILED",
    }
    assert set(job["provider_mode"]["enum"]) == {
        "native",
        "generate",
        "facebook_retrieval_stt",
    }
    retrieval_provider = job["retrieval_provider"]["anyOf"][0]
    assert set(retrieval_provider["enum"]) == {"cobalt", "scrapecreators"}


def test_private_builder_instructions_fit_limit_and_use_two_stage_profile_gate() -> None:
    text = (
        ROOT / "prompts" / "GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
    ).read_text(encoding="utf-8")

    assert len(text) <= 8000
    assert "REPORT LANGUAGE INVARIANT" in text
    assert "Source/transcript language never controls report language" in text
    assert "Canonical English keys stay internal" in text
    assert "`ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`" in text
    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text
    assert "raw CriticProfile keys such as `profile_id`, `risk_level`, `required_cross_checks`, `approved_at`" in text
    assert "preflightManagedMediaCredits" in text
    assert "startManagedMediaNativeTranscription" in text
    assert "preflightManagedMediaAiCredits" in text
    assert "startManagedMediaAiTranscription" in text
    assert "mode=generate, max_credits=40" in text
    assert "DO NOT reuse native `1`" in text
    assert "Do NOT ask the user for beta access code" in text
    assert "Do not expose `KRCM_...` Job IDs" in text
    assert "Do not fall back to Helper in the normal owner flow" in text
    assert "1 - Так" in text
    assert "2 - Ні" in text
    assert "DO NOT display the profile immediately" in text
    assert "Профіль збору і критики успішно створено." in text
    assert "1 - виконати аналіз одразу." in text
    assert "2 - переглянути і відредагувати профіль збору і критики." in text
    assert "1 - прийняти профіль, виконати дослідження." in text
    assert "2 - редагувати профіль." in text
    assert "Never claim approval before `1`" in text
    assert "CRITICAL>=3, HIGH>=2, MEDIUM>=1, LOW>=0" in text
    assert "For EACH material factual claim" in text
    assert "`required`, `achieved_independent`, `exception`" in text
    assert "If achieved<required, set exception=SHORTFALL" in text
    assert "Critic checks the ledger claim-by-claim and verifies traceability" in text
    assert "An unconditional PASS is forbidden" in text
    assert "Cross-check: achieved/required - PASS|SHORTFALL" in text
    assert "TRACEABILITY:" in text
    assert "A systematic review/meta-analysis counts as one evidence origin" in text
