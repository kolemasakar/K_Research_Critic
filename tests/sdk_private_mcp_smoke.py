"""SDK smoke test for owner-authorized *private, loopback-only* KRC MCP.
Run with `PYTHONPATH=src python tests/sdk_private_mcp_smoke.py` on the KRC host.
This is not an external ChatGPT app binding acceptance test.
"""
import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("KRC_PRIVATE_MCP_URL", "http://127.0.0.1:19014/mcp")

async def main():
    if not URL.startswith("http://127.0.0.1:"):
        raise ValueError("Private smoke only permits loopback")
    async with streamablehttp_client(URL) as (read,write,_):
        async with ClientSession(read,write) as session:
            await session.initialize()
            names={t.name for t in (await session.list_tools()).tools}
            expected={"krc_capabilities","krc_scholarly_preflight",
                      "krc_doi_metadata","krc_doi_updates"}
            assert expected <= names
            capabilities=await session.call_tool("krc_capabilities",{})
            raw=capabilities.structuredContent or json.loads(capabilities.content[0].text)
            assert raw["public_exposure"] is False
            assert raw["plugin_mapped"] is False
            payload={"claims":[{"claim_id":"C01","required":1,"evidence":[]}],
                     "search_runs":[],
                     "manuscript_gate":{k:False for k in (
                         "journal_policy_checked","search_audit_reproducible",
                         "primary_sources_inspected","novelty_reviewed",
                         "citations_validated","scientific_methods_audited",
                         "rights_and_ai_disclosure_done","human_author_approved")}}
            check=await session.call_tool("krc_scholarly_preflight",{"payload":payload})
            result=check.structuredContent or json.loads(check.content[0].text)
            assert result["final_publication_status"]=="NO_GO"
            print("PRIVATE_MCP_SDK_SMOKE=PASS TOOLS="+str(len(expected))+" NO_GO=PASS")

if __name__=="__main__":
    asyncio.run(main())
