"""Stage134 schema, DOI, provenance, independence and fail-closed tests: OFFLINE."""
import copy
import hashlib
import json
from urllib.parse import quote

import pytest
from jsonschema import Draft202012Validator

from krc_research.stage134_bibliography_provenance import (
    Stage134Denied, audit_stage134_provenance, normalize_stage134_doi,
)

DOI = "10.1000/demo"
HASH = "0" * 64


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def capture(provider, payload):
    url = ("https://api.crossref.org/works/" + quote(DOI, safe="")
           if provider == "crossref" else
           "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
           + quote("DOI:" + DOI, safe="") + "&format=json&pageSize=1")
    return {"provider": provider, "url": url,
            "captured_at": "2026-11-21T12:00:00Z", "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def crossref(doi=DOI, title="Concrete methods", year=2024):
    return {"message": {"DOI": doi, "title": [title],
                        "published": {"date-parts": [[year]]}}}


def pmc(doi=DOI, title="Concrete methods", year="2024"):
    return {"resultList": {"result": [{"doi": doi, "title": title, "pubYear": year}]}}


def source(sid="S01", origin="O01", access="FULL_TEXT", derived=()):
    return {"source_id": sid, "origin_id": origin,
            "document_sha256": HASH, "access": access,
            "derived_from": list(derived)}


def bundle(captures=None, sources=None):
    return {"version": "KRC-STAGE134-BIBLIOGRAPHY-PROVENANCE/1",
            "policy": "FREE_ONLY_OFFLINE", "doi": DOI,
            "captures": captures if captures is not None else [
                capture("crossref", crossref()), capture("europe_pmc", pmc())],
            "sources": sources if sources is not None else []}


def audit(value):
    return audit_stage134_provenance(value)


def test_clean_two_provider_match_only_metadata():
    result = audit(bundle())
    assert result["metadata_status"] == "TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY"
    assert result["metadata_field_checks"] == {"title": "MATCH", "year": "MATCH"}
    assert result["provenance_status"] == "PROVIDER_ORIGIN_NOT_AUTHENTICATED"
    assert result["scientific_independence"]["verified_origin_count"] == 0
    assert result["scientific_independence"]["scientific_truth_verified"] is False
    assert result["scientific_independence"]["full_text_verified"] is False
    assert result["decision"] == "HUMAN_EVIDENCE_REVIEW_REQUIRED"
    assert all(p["integrity_status"] == "CANONICAL_PAYLOAD_HASH_MATCH_ONLY"
               for p in result["provider_snapshots"])


def test_order_independent_capture_digest_canonical():
    value = bundle()
    shuffled = copy.deepcopy(value)
    shuffled["captures"].reverse()
    result = audit(shuffled)
    assert result["metadata_status"] == "TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY"
    assert [p["provider"] for p in result["provider_snapshots"]] == [
        "crossref", "europe_pmc"]


@pytest.mark.parametrize("raw,expected",[
    ("10.1234/a.b", "10.1234/a.b"),
    ("10.1088/1757-899X/365/3/032058", "10.1088/1757-899x/365/3/032058"),
    ("10.1000/(a);b", "10.1000/(a);b"),
])
def test_restricted_valid_doi(raw, expected):
    assert normalize_stage134_doi(raw) == expected


@pytest.mark.parametrize("raw",[
    "doi:10.1000/demo", "https://doi.org/10.1000/demo",
    "10.1000/../secret", "10.1000/%2Fsecret",
    "10.1000/unsafe?x=1", "10.1000/a#x", "10.1000/a\\evil",
    "10.1000/a b", "10.1000/\n", "10.abc/demo",
    "10.1000/", "", None, 123, "10.1000/a\u00a0b",
])
def test_reject_ambiguous_or_unsafe_doi(raw):
    with pytest.raises(Stage134Denied, match="INVALID_DOI"):
        normalize_stage134_doi(raw)


def test_crossref_doi_mismatch_cannot_be_promoted():
    r = audit(bundle([capture("crossref", crossref(doi="10.1000/other"))]))
    assert r["metadata_status"] == "DOI_MISMATCH"
    assert r["provider_snapshots"][0]["doi_status"] == "MISMATCH"


def test_europe_pmc_absence_is_coverage_gap():
    r = audit(bundle([capture("crossref", crossref()),
                      capture("europe_pmc", {"resultList": {"result": []}})]))
    assert r["metadata_status"] == "COVERAGE_GAP_METADATA_ONLY"
    assert r["provider_snapshots"][1]["doi_status"] == "NOT_FOUND"


def test_europe_pmc_wrong_existing_doi_is_mismatch():
    r = audit(bundle([capture("crossref", crossref()),
                      capture("europe_pmc", pmc(doi="10.1000/other"))]))
    assert r["metadata_status"] == "DOI_MISMATCH"


def test_single_provider_is_partial():
    r = audit(bundle([capture("crossref", crossref())]))
    assert r["metadata_status"] == "PARTIAL_METADATA_ONLY"


@pytest.mark.parametrize("provider_payload",[
    pmc(title="Other methods"), pmc(year="2023"),
])
def test_conflicting_fields_require_review(provider_payload):
    r = audit(bundle([capture("crossref", crossref()),
                      capture("europe_pmc", provider_payload)]))
    assert r["metadata_status"] == "METADATA_CONFLICT_REVIEW"


def test_missing_comparison_field_not_mismatch():
    r = audit(bundle([capture("crossref", crossref(title="")),
                      capture("europe_pmc", pmc())]))
    assert r["metadata_status"] == "INCOMPLETE_METADATA_REVIEW"


def test_capture_hash_tampering_rejected_before_analysis():
    value = bundle()
    value["captures"][0]["payload"]["message"]["title"][0] = "Tampered"
    with pytest.raises(Stage134Denied, match="CAPTURE_HASH_MISMATCH"):
        audit(value)


def test_network_not_called_even_when_valid(monkeypatch):
    import urllib.request
    def forbidden(*args, **kwargs):
        raise AssertionError("NETWORK_UNEXPECTED")
    monkeypatch.setattr(urllib.request, "urlopen", forbidden)
    audit(bundle())


@pytest.mark.parametrize("mutate", [
    lambda c: c.update(url="http://api.crossref.org/works/10.1000%2Fdemo"),
    lambda c: c.update(url="https://api.crossref.org.evil.invalid/works/10.1000%2Fdemo"),
    lambda c: c.update(url="https://api.crossref.org/works/10.1000%252Fdemo"),
    lambda c: c.update(url="https://api.crossref.org/works/10.1000%2Fother"),
])
def test_capture_url_exact_allowlist(mutate):
    value = bundle()
    mutate(value["captures"][0])
    with pytest.raises(Stage134Denied):
        audit(value)


def test_bad_datetime_rejected():
    value = bundle()
    value["captures"][0]["captured_at"] = "2026-11-22T00:00:00"
    with pytest.raises(Stage134Denied):
        audit(value)


def test_duplicate_provider_rejected():
    cap = capture("crossref", crossref())
    with pytest.raises(Stage134Denied, match="DUPLICATE_PROVIDER"):
        audit(bundle([cap, cap]))


def test_duplicate_result_in_europe_pmc_fails_closed():
    p = pmc()
    p["resultList"]["result"].append(copy.deepcopy(p["resultList"]["result"][0]))
    with pytest.raises(Stage134Denied, match="DUPLICATE_PROVIDER_RECORD"):
        audit(bundle([capture("europe_pmc", p)]))


def test_bounded_provider_payload_rejected():
    large = crossref(title="a" * 262145)
    with pytest.raises(Stage134Denied, match="CAPTURE_TOO_LARGE"):
        audit(bundle([capture("crossref", large)]))


@pytest.mark.parametrize("changes", [
    {"policy": "FREE_ONLY_METADATA"},
    {"version": "stage134-other"},
    {"extra": True},
    {"captures": []},
    {"doi": "10.1000/../invalid"},
])
def test_input_schema_or_doi_fails_closed(changes):
    value = bundle()
    value.update(changes)
    with pytest.raises(Stage134Denied):
        audit(value)


def test_lineage_merges_derived_and_same_origin_without_verified_claim():
    srcs = [source("S01", "O01"),
            source("S02", "O02", derived=["S01"]),
            source("S03", "O02", access="METHODS_RESULTS_EXCERPT"),
            source("S04", "O04")]
    out = audit(bundle(sources=srcs))
    assert len(out["lineage_groups"]) == 2
    assert out["lineage_groups"][0]["source_ids"] == ["S01", "S02", "S03"]
    assert out["lineage_groups"][0]["origin_ids"] == ["O01", "O02"]
    assert out["lineage_groups"][0]["claimed_inspected_sources"] == 3
    assert out["scientific_independence"]["verified_origin_count"] == 0
    assert out["scientific_independence"]["scientific_truth_verified"] is False


def test_unrelated_claimed_sources_still_unverified():
    out = audit(bundle(sources=[source("A", "ORA"), source("B", "ORB")]))
    assert len(out["lineage_groups"]) == 2
    assert out["scientific_independence"]["verified_origin_count"] == 0


@pytest.mark.parametrize("sources,reason", [
    ([source("S01"), source("S01")], "DUPLICATE_SOURCE_ID"),
    ([source("S01", derived=["UNKNOWN"])], "UNKNOWN_PARENT_SOURCE"),
    ([source("S01", derived=["S01"])], "LINEAGE_CYCLE"),
    ([source("S01", derived=["S02"]), source("S02", derived=["S01"])], "LINEAGE_CYCLE"),
])
def test_lineage_invalid_structure(sources, reason):
    with pytest.raises(Stage134Denied, match=reason):
        audit(bundle(sources=sources))


def test_canonical_input_hash_and_output_schema():
    inp = bundle(sources=[source()])
    out = audit(inp)
    assert out["input_sha256"] == hashlib.sha256(canonical(inp)).hexdigest()
    from krc_research.stage134_bibliography_provenance import _schema
    result_schema = _schema("bibliography_provenance_result_v1.schema.json")
    Draft202012Validator.check_schema(result_schema)
    assert Draft202012Validator(result_schema).is_valid(out)


def test_malformed_crossref_response_denied():
    with pytest.raises(Stage134Denied, match="INVALID_CROSSREF_RESPONSE"):
        audit(bundle([capture("crossref", {"message": []})]))


def test_metadata_only_records_never_count_as_scientific_confirmation():
    src = source(access="METADATA_ONLY")
    out = audit(bundle(sources=[src]))
    assert out["lineage_groups"][0]["claimed_inspected_sources"] == 0
    assert not out["scientific_independence"]["full_text_verified"]


def test_empty_citation_origin_is_never_accepted():
    src = source()
    src["origin_id"] = ""
    with pytest.raises(Stage134Denied, match="INVALID_BUNDLE_SCHEMA"):
        audit(bundle(sources=[src]))


def test_adapter_offline_entrypoint_consistent():
    from krc_research.stage131_bibliography_adapter import audit_doi_provenance_offline
    value = bundle()
    assert audit_doi_provenance_offline(value) == audit_stage134_provenance(value)


def test_casefold_duplicate_source_rejected():
    with pytest.raises(Stage134Denied, match="DUPLICATE_SOURCE_ID"):
        audit(bundle(sources=[source("SAME", "A"), source("same", "B")]))


def test_casefold_origin_group_collapses_claims():
    out = audit(bundle(sources=[source("A", "Origin1"), source("B", "origin1")]))
    assert len(out["lineage_groups"]) == 1
    assert out["scientific_independence"]["verified_origin_count"] == 0

