from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "plugins"
    / "krc_migration_candidate"
    / "contracts"
    / "migration_acceptance.yaml"
)


def load_contract() -> dict:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


def test_migration_timing_is_plan_specific_and_fail_closed() -> None:
    contract = load_contract()
    timing = contract["plan_timing"]
    assert timing["enterprise_target_dates_are_universal_for_personal_plans"] is False
    assert timing["account_specific_notice_is_authoritative_for_execution_timing"] is True
    assert timing["do_not_assume_plus_cutoff_from_enterprise_calendar"] is True
    assert timing["dates_may_change"] is True


def test_core_is_model_agnostic_and_not_chat_history_dependent() -> None:
    portability = load_contract()["portability"]

    model = portability["selected_model"]
    assert model["transfer_guaranteed"] is False
    assert model["acceptance"]["model_agnostic_core_required"] is True
    assert model["acceptance"]["selected_model_must_not_be_runtime_dependency"] is True

    chats = portability["previous_chats"]
    assert chats["transfer_guaranteed"] is False
    assert chats["acceptance"]["required_state_must_not_exist_only_in_chat_history"] is True
    assert chats["acceptance"]["cross_chat_continuity_uses_explicit_checkpoint_artifacts"] is True


def test_starters_and_reference_assets_are_explicitly_revalidated() -> None:
    portability = load_contract()["portability"]

    starters = portability["conversation_starters"]
    assert starters["transfer_guaranteed"] is False
    assert starters["acceptance"]["starter_text_not_required_for_core_correctness"] is True
    assert starters["acceptance"]["representative_starters_must_exist_as_regression_fixtures"] is True
    assert starters["acceptance"]["replacement_starters_or_equivalent_entry_points_validated_after_migration"] is True

    assets = portability["reference_assets"]
    assert assets["transfer_guaranteed"] is False
    assert assets["acceptance"]["enumerate_required_reference_assets_before_cutover"] is True
    assert assets["acceptance"]["validate_access_and_behavior_after_migration"] is True


def test_custom_actions_are_not_assumed_to_migrate() -> None:
    actions = load_contract()["portability"]["custom_actions"]
    assert actions["transfer_guaranteed"] is False
    assert actions["acceptance"]["legacy_action_creation_default"] == "HOLD"
    assert actions["acceptance"]["media_rebuilt_through_supported_app_connector_or_mcp"] is True
    assert actions["acceptance"]["media_operation_parity_required"] == 13


def test_replacement_access_and_store_distribution_are_not_assumed() -> None:
    distribution = load_contract()["access_and_distribution"]
    assert distribution["replacement_plugin_initial_access"] == "PRIVATE"
    assert distribution["public_gpt_sharing_auto_inherited"] is False
    assert distribution["sharing_must_be_reconfigured_and_validated"] is True
    assert distribution["intended_user_access_must_be_tested_before_cutover"] is True

    metrics = distribution["store_metrics"]
    assert metrics["ratings_transfer_guaranteed"] is False
    assert metrics["reviews_transfer_guaranteed"] is False
    assert metrics["usage_counters_transfer_guaranteed"] is False
    assert metrics["ranking_transfer_guaranteed"] is False
    assert metrics["store_position_transfer_guaranteed"] is False
    assert metrics["acceptance_dependency_on_metric_transfer"] is False


def test_legacy_link_redirect_is_observed_not_assumed() -> None:
    link = load_contract()["legacy_link"]
    assert link["redirect_to_replacement_expected_when_supported_and_user_has_access"] is True
    assert link["redirect_guaranteed_for_acceptance"] is False
    assert link["verify_after_activation"] is True
    assert link["document_if_absent_or_inaccessible"] is True


def test_migration_is_state_changing_not_preview() -> None:
    migration = load_contract()["migration_state_change"]
    assert migration["migration_makes_original_gpt_read_only"] is True
    assert migration["migration_requires_separate_owner_approval"] is True
    assert migration["migration_is_not_preview"] is True
    assert migration["read_only_inspection_must_stop_before_migrate"] is True


def test_cutover_requires_regression_access_and_owner_approval() -> None:
    contract = load_contract()
    required = set(contract["post_migration_regression"]["required"])
    assert {
        "core_skill_semantic_parity",
        "checkpoint_recovery_without_chat_history_dependency",
        "model_agnostic_behavior",
        "reference_asset_access_if_any",
        "media_13_operation_semantic_parity",
        "sharing_and_intended_audience_access",
        "representative_entry_points_or_starters",
    } <= required
    assert contract["post_migration_regression"]["must_pass_before_user_switch"] is True

    cutover = contract["cutover_gate"]
    assert cutover["core_regression_pass_required"] is True
    assert cutover["media_regression_pass_required"] is True
    assert cutover["sharing_access_validation_required"] is True
    assert cutover["current_public_gpt_kept_until_replacement_accepted"] is True
    assert cutover["separate_owner_approval_required_for_activation_or_user_switch"] is True


def test_release_boundary_remains_non_mutating() -> None:
    boundary = load_contract()["release_boundary"]
    assert set(boundary.values()) == {"DENIED"}
