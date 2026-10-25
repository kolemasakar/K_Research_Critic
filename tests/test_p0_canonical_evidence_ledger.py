import json
from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from krc_research.canonical_evidence_ledger import Evidence, assess, adapt_legacy_report, validate_assessments

def item(**kw):
    x = dict(source_id="S1", origin_id="O1", access="FULL_TEXT",
             support="SUPPORTED", inspected_methods_results=True,
             scope_matched=True, provenance_verified=True,
             primary_url="https://example.org/source")
    x.update(kw)
    return Evidence(**x)

def test_one_origin_not_two_urls():
    r=assess("C01",2,[item(),item(source_id="S2")])
    assert r["achieved_independent"]==1 and r["verdict"]=="SHORTFALL"

def test_abstract_not_counted():
    r=assess("C01",1,[item(access="ABSTRACT_ONLY")])
    assert r["verdict"]=="SHORTFALL"

def test_unverified_provenance_not_counted():
    r=assess("C01",1,[item(provenance_verified=False)])
    assert r["achieved_independent"]==0

def test_false_scope_not_counted():
    assert assess("C01",1,[item(scope_matched=False)])["verdict"]=="SHORTFALL"

def test_distinct_eligible_origins():
    r=assess("C01",2,[item(),item(source_id="S2",origin_id="O2")])
    assert r["verdict"]=="PASS" and r["achieved_independent"]==2

def test_validation_catches_fabricated_count():
    r=assess("C01",1,[item()])
    r["achieved_independent"]=4
    with pytest.raises(ValueError): validate_assessments([r])

def test_validation_catches_duplicate_claim():
    r=assess("C01",1,[])
    with pytest.raises(ValueError): validate_assessments([r,r])

def test_invalid_required():
    with pytest.raises(ValueError): assess("C01",0,[])

def test_legacy_import_does_not_forge_inspection():
    raw={"count":1,"document_version":"v1.4","claims":[{
        "claim_id":"C01","required":1,"verdict":"PASS","achieved_independent":1,
        "assertion":"X","evidence_urls":["https://example.org"]}]}
    r=adapt_legacy_report(raw)
    assert r["reported_prior_pass"]==1
    assert r["accepted_in_this_import"]==0
    assert r["claims"][0]["independent_assessment"]["verdict"]=="SHORTFALL"

def test_import_count_mismatch():
    with pytest.raises(ValueError): adapt_legacy_report({"count":0,"claims":[{"claim_id":"C01"}]})

def test_legacy_missing_url_list_cannot_be_invented():
    raw={"count":1,"document_version":"v1.4","claims":[{
        "claim_id":"C09","required":1,"verdict":"PASS","achieved_independent":1,
        "assertion":"Li crosstalk","source_ids":"[9],[10]"}]}
    imported=adapt_legacy_report(raw)
    assert imported["claims"][0]["source_urls"] == []
    assert imported["claims"][0]["independent_assessment"]["verdict"] == "SHORTFALL"

def test_verified_urls_are_not_proof_without_provenance():
    r=assess("C09",1,[item(primary_url="https://nature.com/1",provenance_verified=False),
                      item(source_id="S2",primary_url="https://rsc.org/1",provenance_verified=False)])
    assert r["achieved_independent"]==0
