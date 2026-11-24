"""KRC public FREE_ONLY DOI workflow and main private MCP source wiring."""
import ast
from pathlib import Path

import pytest

from krc_research import public_doi_workflow as workflow


def test_public_doi_result_preserves_metadata_only(monkeypatch):
    calls = []
    def fake(doi):
        calls.append(doi)
        return {
            "status": "COVERAGE_GAP_METADATA_ONLY",
            "doi": doi,
            "sources": {
                "crossref": {"status": "METADATA_ONLY", "access": "UNVERIFIED"},
                "europe_pmc": {"status": "NOT_FOUND"},
            },
            "full_text_verified": False,
            "experimental_independence_verified": False,
        }
    monkeypatch.setattr(workflow, "lookup_doi_metadata", fake)
    got = workflow.krc_public_doi_check("10.1016/j.proeng.2013.03.022")
    assert calls == ["10.1016/j.proeng.2013.03.022"]
    assert got == {
        "schema": "KRC-PUBLIC-DOI-CHECK/1",
        "mode": "FREE_ONLY_PUBLIC_METADATA",
        "doi": calls[0],
        "status": "COVERAGE_GAP_METADATA_ONLY",
        "sources": {
            "crossref": {"status": "METADATA_ONLY", "access": "UNVERIFIED"},
            "europe_pmc": {"status": "NOT_FOUND"},
        },
        "full_text_verified": False,
        "experimental_independence_verified": False,
        "scientific_approval": False,
        "publication_clearance": "NOT_ESTABLISHED",
    }


def test_public_doi_invalid_does_not_trigger_provider(monkeypatch):
    def fail(*_args, **_kwargs):
        raise AssertionError("PROVIDER_REQUEST_MUST_NOT_EXECUTE")
    from krc_research import stage131_bibliography_adapter as adapter
    monkeypatch.setattr(adapter, "fetch_json_metadata", fail)
    with pytest.raises(ValueError, match="INVALID_DOI"):
        workflow.krc_public_doi_check("10.1000/bad\x00doi")


def test_mcp_primary_tool_registered_without_mutating_legacy_tools():
    source = Path(__file__).resolve().parents[1] / "src/krc_research/mcp_private_server.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    functions = {node.name: node for node in tree.body
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for name in ("krc_doi_metadata", "krc_doi_updates", "krc_bibliography_audit",
                 "krc_scholarly_preflight", "krc_public_doi_check"):
        assert name in functions
        fn = functions[name]
        assert any(isinstance(dec, ast.Call)
                   and isinstance(dec.func, ast.Attribute)
                   and isinstance(dec.func.value, ast.Name)
                   and dec.func.value.id == "mcp"
                   and dec.func.attr == "tool"
                   for dec in fn.decorator_list)
    new_tool = functions["krc_public_doi_check"]
    calls = [node for node in ast.walk(new_tool) if isinstance(node, ast.Call)]
    assert any(isinstance(node.func, ast.Name)
               and node.func.id == "_krc_public_doi_check"
               for node in calls)
