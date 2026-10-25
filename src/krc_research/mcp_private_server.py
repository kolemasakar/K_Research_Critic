"""KRC private, loopback-only research MCP. No public listener or job mutations.

The server's tools check *provided* inspection provenance; they do not inspect science
or authenticate experimental data independently. Configuration defaults to loopback.
"""
import os
from mcp.server.fastmcp import FastMCP
from krc_research.offline_acceptance import evaluate_payload
from krc_research.public_metadata_adapters import reconcile_doi, crossref_editorial_updates
from krc_research.bibliography_audit import audit_bibliography
from krc_research.inspection_receipts import InspectionReceipt, audit_receipt
from krc_research.replay_registry import ReplayRegistry
from krc_research.science_dispatch import handle_science_request
from pathlib import Path

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
def krc_bibliography_audit(dois: list[str]) -> dict:
    """Bounded Crossref/EuropePMC/editorial DOI review. Metadata only; no retraction clearance."""
    return audit_bibliography(dois)

@mcp.tool()
def krc_inspection_receipt_review(receipt: dict) -> dict:
    """Review inspection evidence metadata; cannot authenticate paper content."""
    import json
    if not isinstance(receipt, dict) or len(json.dumps(receipt).encode()) > 32000:
        raise ValueError("Invalid receipt payload")
    return audit_receipt(InspectionReceipt(**receipt))


@mcp.tool()
def krc_science_signed_request(envelope: dict, signature: str) -> dict:
    """Sentinel-governed signed K_Science request. Closed until credentials are provisioned."""
    key_path=os.environ.get("KRC_SENTINEL_SCIENCE_KEY_FILE")
    if not key_path:
        return {"status":"NOT_CONFIGURED", "reason":"Sentinel service identity/key not provisioned"}
    key_file=Path(key_path)
    if key_file.is_symlink() or not key_file.is_file() or (key_file.stat().st_mode & 0o077):
        raise ValueError("Unsafe credential permissions")
    key=bytes.fromhex(key_file.read_text(encoding="ascii").strip())
    if len(key)<32:
        raise ValueError("Invalid Sentinel-issued key")
    replay=ReplayRegistry(os.environ.get("KRC_SCIENCE_REPLAY_DB",
                          "/home/krcops/krc-research-private/state/science_replay.sqlite3"))
    return handle_science_request(envelope,secret=key,signature=signature,
                    seen=replay,permitted={"research.evidence.preflight",
                         "research.bibliography.audit","research.inspection.review"})

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
