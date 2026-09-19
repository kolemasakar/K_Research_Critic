from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.r3c import R3C_TOOL_NAMES
from plugins.krc_migration_candidate.mcp_canary.r3e1 import (
    R3E1_EXECUTION_TOOL_NAME,
    R3E1_TOOL_NAMES,
)
from plugins.krc_migration_candidate.mcp_canary.r3e2 import (
    R3E2_EXECUTION_TOOL_NAME,
    R3E2_TOOL_NAMES,
)
from plugins.krc_migration_candidate.mcp_canary.r3e3 import (
    R3E3_EXECUTION_TOOL_NAME,
    R3E3_TOOL_NAMES,
)
from plugins.krc_migration_candidate.mcp_canary.r3e4 import (
    R3E4_EXECUTION_TOOL_NAME,
    R3E4_TOOL_NAMES,
)

READ_TOOLS = {
    "media_get_capabilities",
    "media_youtube_preflight",
    "media_youtube_lookup",
    "media_youtube_status",
    "media_youtube_segments",
    "media_instagram_preflight",
    "media_instagram_lookup",
    "media_non_youtube_status",
    "media_non_youtube_segments",
}
EXECUTION_TOOLS = {
    "media_youtube_start",
    "media_instagram_start",
    "media_facebook_start",
    "media_telegram_start",
}
CANONICAL_TOOLS = READ_TOOLS | EXECUTION_TOOLS


def test_r3f_canonical_contract_remains_13_operations() -> None:
    assert len(READ_TOOLS) == 9
    assert len(EXECUTION_TOOLS) == 4
    assert len(CANONICAL_TOOLS) == 13
    assert set(R3C_TOOL_NAMES) == READ_TOOLS


def test_r3f_execution_surfaces_cover_all_four_starts_exactly_once() -> None:
    starts = {
        R3E1_EXECUTION_TOOL_NAME,
        R3E2_EXECUTION_TOOL_NAME,
        R3E3_EXECUTION_TOOL_NAME,
        R3E4_EXECUTION_TOOL_NAME,
    }
    assert starts == EXECUTION_TOOLS
    assert len(starts) == 4


def test_r3f_union_of_read_contract_and_execution_surfaces_is_complete() -> None:
    exposed = set(R3C_TOOL_NAMES)
    exposed.update(R3E1_TOOL_NAMES)
    exposed.update(R3E2_TOOL_NAMES)
    exposed.update(R3E3_TOOL_NAMES)
    exposed.update(R3E4_TOOL_NAMES)
    assert exposed == CANONICAL_TOOLS

def test_r3f_each_isolated_surface_exposes_only_its_own_start() -> None:
    surfaces = {
        "youtube": (set(R3E1_TOOL_NAMES), R3E1_EXECUTION_TOOL_NAME),
        "instagram": (set(R3E2_TOOL_NAMES), R3E2_EXECUTION_TOOL_NAME),
        "facebook": (set(R3E3_TOOL_NAMES), R3E3_EXECUTION_TOOL_NAME),
        "telegram": (set(R3E4_TOOL_NAMES), R3E4_EXECUTION_TOOL_NAME),
    }
    for _name, (tool_names, own_start) in surfaces.items():
        exposed_starts = tool_names & EXECUTION_TOOLS
        assert exposed_starts == {own_start}


def test_r3f_no_execution_tool_leaks_into_r3c_readonly_surface() -> None:
    assert set(R3C_TOOL_NAMES).isdisjoint(EXECUTION_TOOLS)


def test_r3f_all_execution_descriptors_keep_confirmation_annotations() -> None:
    from plugins.krc_migration_candidate.mcp_canary.r3e1 import tool_descriptors as e1_descriptors
    from plugins.krc_migration_candidate.mcp_canary.r3e2 import tool_descriptors as e2_descriptors
    from plugins.krc_migration_candidate.mcp_canary.r3e3 import tool_descriptors as e3_descriptors
    from plugins.krc_migration_candidate.mcp_canary.r3e4 import tool_descriptors as e4_descriptors

    surfaces = (
        (e1_descriptors(), R3E1_EXECUTION_TOOL_NAME),
        (e2_descriptors(), R3E2_EXECUTION_TOOL_NAME),
        (e3_descriptors(), R3E3_EXECUTION_TOOL_NAME),
        (e4_descriptors(), R3E4_EXECUTION_TOOL_NAME),
    )
    for descriptors, execution_name in surfaces:
        execution = [item for item in descriptors if item["name"] == execution_name]
        assert len(execution) == 1
        annotations = execution[0]["annotations"]
        assert annotations["readOnlyHint"] is False
        assert annotations["destructiveHint"] is False
        assert annotations["idempotentHint"] is False
        assert annotations["openWorldHint"] is True


def test_r3f_every_nonexecution_descriptor_remains_read_only() -> None:
    from plugins.krc_migration_candidate.mcp_canary.r3c import tool_descriptors as r3c_descriptors

    descriptors = r3c_descriptors()
    assert len(descriptors) == 9
    for descriptor in descriptors:
        assert descriptor["name"] in READ_TOOLS
        annotations = descriptor["annotations"]
        assert annotations["readOnlyHint"] is True
        assert annotations["destructiveHint"] is False
