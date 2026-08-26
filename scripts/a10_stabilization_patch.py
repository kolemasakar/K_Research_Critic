from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one match, got {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_after(path: Path, anchor: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(anchor)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, got {count}: {anchor!r}")
    path.write_text(text.replace(anchor, anchor + addition, 1), encoding="utf-8")


validator = ROOT / "scripts" / "validate_store_package.py"
replace_once(
    validator,
    '_require(instructions.get("version") == "0.9-beta-a9.10", "A9.10 instruction version must be 0.9-beta-a9.10")',
    '_require(instructions.get("version") == "0.9.1-beta-a10", "A10 stabilization instruction version must be 0.9.1-beta-a10")',
)
replace_once(
    validator,
    '_require(instructions.get("builder_package_version") == "0.9-beta-a9.10", "A9.10 Builder package version must be 0.9-beta-a9.10")',
    '_require(instructions.get("builder_package_version") == "0.9.1-beta-a10", "A10 stabilization Builder package version must be 0.9.1-beta-a10")',
)
replace_once(
    validator,
    '_require(instructions.get("builder_runtime_applied") is True, "A9.10 Builder package must record actual private GPT application")',
    '_require(instructions.get("builder_runtime_applied") is False, "A10 stabilization Builder package must remain pending until owner runtime application")',
)
insert_after(
    validator,
    '    _require(instructions.get("verdict_labels_localized_to_report_language") is True, "verdicts must be localized to report language")\n',
    '    _require(instructions.get("cross_check_protocol_markdown_table_strict") is True, "claim summary must require strict Markdown table rendering")\n'
    '    _require(instructions.get("cross_check_protocol_header_merge_forbidden") is True, "claim summary header merging must be forbidden")\n'
    '    _require(instructions.get("cross_check_protocol_table_header_row_uk") == "| Твердження | Потрібно | Отримано незалежних | Виняток |", "Ukrainian claim-summary header row must remain exact")\n'
    '    _require(instructions.get("cross_check_protocol_table_separator_row") == "| --- | ---: | ---: | --- |", "claim-summary separator row must remain exact")\n',
)
insert_after(
    validator,
    '    _require(beta.get("managed_attachment_private_gpt_e2e_complete") is True, "A9.10 attachment private-GPT E2E must be accepted")\n',
    '    _require(beta.get("stabilization_phase") == "A10", "stabilization phase must be A10")\n'
    '    _require(beta.get("claim_summary_table_hardening_package_ready") is True, "A10 claim-summary hardening package must be ready")\n'
    '    _require(beta.get("claim_summary_table_hardening_runtime_applied") is False, "A10 claim-summary runtime hardening must remain pending before owner Builder update")\n',
)
insert_after(
    validator,
    '    _require(release.get("rollout_state") == "A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED", "rollout state must record accepted A9.10 local attachment private-GPT E2E")\n',
    '    _require(release.get("stabilization_state") == "A10_CLAIM_TABLE_HARDENING_PACKAGE_READY_RUNTIME_PENDING", "A10 stabilization state must remain runtime-pending")\n',
)
insert_after(
    validator,
    '    _require(release.get("a9_10_attachment_private_gpt_e2e_complete") is True, "A9.10 attachment private-GPT E2E must be accepted")\n',
    '    _require(release.get("a10_claim_summary_table_hardening_ready") is True, "A10 claim-summary hardening must be package-ready")\n'
    '    _require(release.get("a10_claim_summary_table_runtime_accepted") is False, "A10 claim-summary runtime acceptance must remain pending")\n',
)
replace_once(
    validator,
    '    _require(release.get("gpt_builder_private_update_required") is False, "accepted A9.10 Builder runtime must not require another private update")',
    '    _require(release.get("gpt_builder_private_update_required") is True, "A10 stabilization package must require a private Builder update")',
)
insert_after(
    validator,
    '            "startManagedAttachmentTranscription",\n',
    '            "| Твердження | Потрібно | Отримано незалежних | Виняток |",\n'
    '            "| --- | ---: | ---: | --- |",\n'
    '            "Never merge/concatenate header labels",\n',
)

builder_test = ROOT / "tests" / "test_media_beta_builder_a9_7_i.py"
replace_once(builder_test, 'assert instructions["version"] == "0.9-beta-a9.10"', 'assert instructions["version"] == "0.9.1-beta-a10"')
replace_once(builder_test, 'assert instructions["builder_package_version"] == "0.9-beta-a9.10"', 'assert instructions["builder_package_version"] == "0.9.1-beta-a10"')
replace_once(builder_test, 'assert instructions["builder_runtime_applied"] is True', 'assert instructions["builder_runtime_applied"] is False')
replace_once(builder_test, 'assert release["gpt_builder_private_update_required"] is False', 'assert release["gpt_builder_private_update_required"] is True')
insert_after(
    builder_test,
    '    assert instructions["builder_policy_fix_runtime_applied"] is True\n',
    '    assert instructions["cross_check_protocol_markdown_table_strict"] is True\n'
    '    assert instructions["cross_check_protocol_header_merge_forbidden"] is True\n',
)

attachment_test = ROOT / "tests" / "test_media_attachment_ingestion_package.py"
replace_once(attachment_test, 'assert instructions["version"] == "0.9-beta-a9.10"', 'assert instructions["version"] == "0.9.1-beta-a10"')
replace_once(attachment_test, 'assert instructions["builder_runtime_applied"] is True', 'assert instructions["builder_runtime_applied"] is False')
replace_once(attachment_test, 'assert release["gpt_builder_private_update_required"] is False', 'assert release["gpt_builder_private_update_required"] is True')

managed_test = ROOT / "tests" / "test_media_beta_managed_package.py"
insert_after(
    managed_test,
    '    assert instructions["cross_check_protocol_table_required"] is True\n',
    '    assert instructions["cross_check_protocol_markdown_table_strict"] is True\n'
    '    assert instructions["cross_check_protocol_header_merge_forbidden"] is True\n'
    '    assert instructions["cross_check_protocol_table_header_row_uk"] == "| Твердження | Потрібно | Отримано незалежних | Виняток |"\n'
    '    assert instructions["cross_check_protocol_table_separator_row"] == "| --- | ---: | ---: | --- |"\n',
)
replace_once(managed_test, 'assert release["gpt_builder_private_update_required"] is False', 'assert release["gpt_builder_private_update_required"] is True')

crosscheck_test = ROOT / "tests" / "test_claim_level_cross_check_enforcement.py"
replace_once(
    crosscheck_test,
    '    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text\n    assert "Values must match visible claim blocks and traceable evidence origins" in text',
    '    assert "`| Твердження | Потрібно | Отримано незалежних | Виняток |`" in text\n'
    '    assert "`| --- | ---: | ---: | --- |`" in text\n'
    '    assert "Never merge/concatenate header labels" in text\n'
    '    assert "Values must match visible claim blocks and traceable evidence origins" in text',
)
replace_once(
    crosscheck_test,
    '    assert "`Твердження | Потрібно | Отримано незалежних | Виняток`" in text\n    assert "Do not expose English labels such as `Claim-level summary`" in text',
    '    assert "`| Твердження | Потрібно | Отримано незалежних | Виняток |`" in text\n'
    '    assert "`| --- | ---: | ---: | --- |`" in text\n'
    '    assert "Never merge or concatenate the four header labels" in text\n'
    '    assert "Do not expose English labels such as `Claim-level summary`" in text',
)
insert_after(
    crosscheck_test,
    '    assert instructions["cross_check_protocol_table_required"] is True\n',
    '    assert instructions["cross_check_protocol_markdown_table_strict"] is True\n'
    '    assert instructions["cross_check_protocol_header_merge_forbidden"] is True\n'
    '    assert instructions["cross_check_protocol_table_header_row_uk"] == "| Твердження | Потрібно | Отримано незалежних | Виняток |"\n'
    '    assert instructions["cross_check_protocol_table_separator_row"] == "| --- | ---: | ---: | --- |"\n',
)
replace_once(crosscheck_test, 'assert release["gpt_builder_private_update_required"] is False', 'assert release["gpt_builder_private_update_required"] is True')

print("A10 stabilization patch applied")
