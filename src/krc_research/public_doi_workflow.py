"""Public FREE_ONLY DOI checking, shared by KRC private MCP and staging tests.

This public read-only metadata workflow is separate from signed K_Science
research.bibliography.audit. It neither creates consent nor claims verified
scientific origins or publisher authentication.
"""
from __future__ import annotations

from .stage131_bibliography_adapter import lookup_doi_metadata

SCHEMA = "KRC-PUBLIC-DOI-CHECK/1"


def krc_public_doi_check(doi: str) -> dict:
    """Check DOI metadata through public Crossref and Europe PMC (FREE_ONLY)."""
    record = lookup_doi_metadata(doi)
    return {
        "schema": SCHEMA,
        "mode": "FREE_ONLY_PUBLIC_METADATA",
        "doi": record["doi"],
        "status": record["status"],
        "sources": record["sources"],
        "full_text_verified": False,
        "experimental_independence_verified": False,
        "scientific_approval": False,
        "publication_clearance": "NOT_ESTABLISHED",
    }
