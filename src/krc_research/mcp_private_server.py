"""KRC private, loopback-only research MCP. No public listener or job mutations.

The server's tools check *provided* inspection provenance; they do not inspect science
or authenticate experimental data independently. Configuration defaults to loopback.
"""
import os
from mcp.server.fastmcp import FastMCP
from krc_research.offline_acceptance import evaluate_payload
from krc_research.public_metadata_adapters import reconcile_doi, crossref_editorial_updates

HOST = "127.0.0.1"
PORT = int(os.environ.get("KRC_PRIVATE_RESEARCH_PORT", "19014"))
if not 1024 < PORT < 65536:
    raise ValueError("Invalid private port")

mcp = FastMCP("KRC Private Scientific Evidence", host=HOST, port=PORT,
              stateless_http=True, json_response=True)

@mcp.tool()
def krc_scholarly_preflight(payload: dict) -> dict:
    """Fail-closed standalone audit. Not a publication or source-authentication approval."""
    import json
    if not isinstance(payload, dict) or len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) > 262144:
        raise ValueError("Payload must be object <=256 KiB")
    return evaluate_payload(payload)

@mcp.tool()
def krc_doi_metadata(doi: str) -> dict:
    """Crossref/EuropePMC metadata only. Never implies full-text inspection."""
    return reconcile_doi(doi)

@mcp.tool()
def krc_doi_updates(doi: str) -> dict:
    """Find Crossref editorial corrections; no guarantee of no retractions."""
    return crossref_editorial_updates(doi)

@mcp.tool()
def krc_capabilities() -> dict:
    """Describe local-only private execution boundaries."""
    return {"transport":"streamable-http", "host":"127.0.0.1",
            "runtime":"isolated", "authorization":"loopback-only",
            "public_exposure":False, "provider_payments":False,
            "plugin_mapped":False,
            "claim_provenance_verified_by_server":False}

if __name__=="__main__":
    mcp.run(transport="streamable-http")
