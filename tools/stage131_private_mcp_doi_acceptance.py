#!/usr/bin/env python3
"""Verify the real KRC scholarly MCP interface in staging over loopback only.

Manual operator use on authorized KRC VM:
  /opt/krc-public-mcp/venv/bin/python -B tools/stage131_private_mcp_doi_acceptance.py \
     --port 19147 --expect-tool [--live-doi]

For rollback:
  --expect-absent

Checks MCP initialize, list_tools, existing DOI tool preservation, new
FREE_ONLY public DOI method availability (or absence on baseline), and
fail-closed invalid input. Does not grant signed K_Science execution.
"""
from __future__ import annotations

import argparse
import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOOL = "krc_public_doi_check"
LEGACY = {"krc_doi_metadata", "krc_doi_updates", "krc_bibliography_audit"}
DOI = "10.1016/j.proeng.2013.03.022"


async def inspect(port: int, expect_tool: bool, live_doi: bool):
    url = f"http://127.0.0.1:{port}/mcp"
    async with streamablehttp_client(url, timeout=15, sse_read_timeout=45) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            names = {tool.name for tool in result.tools}
            assert LEGACY.issubset(names), f"Existing KRC legacy tools changed: {sorted(names)}"
            assert (TOOL in names) is expect_tool, sorted(names)
            print("MCP_INITIALIZE_AND_TOOL_REGISTRY_PASS", sorted(names), flush=True)
            if not expect_tool:
                print("BASELINE_NEW_DOI_TOOL_ABSENT_PASS", flush=True)
                return
            bad = await session.call_tool(TOOL, arguments={"doi": "10.1000/bad\x00doi"})
            assert bad.isError is True, bad
            print("INVALID_DOI_MCP_TOOL_DENIED_PASS", flush=True)
            if live_doi:
                checked = await session.call_tool(TOOL, arguments={"doi": DOI})
                assert checked.isError is False, checked
                body = checked.structuredContent
                if not isinstance(body, dict):
                    text_items = [i.text for i in checked.content if getattr(i, "type", None) == "text"]
                    assert text_items, checked
                    body = json.loads(text_items[0])
                assert body["schema"] == "KRC-PUBLIC-DOI-CHECK/1", body
                assert body["mode"] == "FREE_ONLY_PUBLIC_METADATA"
                assert body["scientific_approval"] is False
                assert body["experimental_independence_verified"] is False
                assert body["full_text_verified"] is False
                assert body["status"] in (
                    "COVERAGE_GAP_METADATA_ONLY",
                    "TWO_PROVIDER_DOI_MATCH_METADATA_ONLY",
                    "REVIEW_REQUIRED",
                )
                crossref = body["sources"]["crossref"]["status"]
                europe = body["sources"]["europe_pmc"]["status"]
                print("MCP_PUBLIC_DOI_LIVE_STATUS", body["status"],
                      "CROSSREF", crossref, "EUROPE_PMC", europe, flush=True)
                if crossref != "METADATA_ONLY":
                    print("PROVIDER_NETWORK_DEGRADED_NO_SCIENTIFIC_PROMOTION", flush=True)
                else:
                    print("FREE_ONLY_DOI_CROSSREF_LIVE_READ_PASS", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=19147)
    kind = parser.add_mutually_exclusive_group(required=True)
    kind.add_argument("--expect-tool", action="store_true")
    kind.add_argument("--expect-absent", action="store_true")
    parser.add_argument("--live-doi", action="store_true")
    opts = parser.parse_args()
    if not (1024 < opts.port < 65536):
        parser.error("Unprivileged port required")
    if opts.live_doi and opts.expect_absent:
        parser.error("Cannot call a tool expected to be absent")
    asyncio.run(inspect(opts.port, opts.expect_tool, opts.live_doi))


if __name__ == "__main__":
    main()
