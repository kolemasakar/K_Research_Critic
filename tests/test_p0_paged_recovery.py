import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from krc_research.paged_discovery import paged_discovery
from krc_research.paged_recovery import resume_search
import pytest
def response(url):
    from urllib.parse import urlsplit,parse_qs
    n=int(parse_qs(urlsplit(url).query)["offset"][0])
    return {"status":"ok","message":{"total-results":5,"items":[{"DOI":"10.1234/p"+str(i),"title":["Study "+str(i)]} for i in range(n,min(n+2,5))]}}
def broken(url):
    if "offset=2" in url:raise TimeoutError()
    return response(url)
def failed():
    return paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=4,fetch=broken)
def test_resume_exact_missing_pages():
    a=failed();b=resume_search(a,fetch=response)
    assert a["stopping_reason"]=="PROVIDER_FAILURE" and len(a["records"])==2
    assert b["stopping_reason"]=="REACHED_REPORTED_TOTAL" and len(b["records"])==5
    assert b["pages"][0]==a["pages"][0]
    assert b["resumed_from_sha256"]==a["manifest_sha256"]
def test_no_editing_provenance():
    a=failed();a["records"][0]["title"]="altered"
    with pytest.raises(ValueError):resume_search(a,fetch=response)
def test_no_resuming_success():
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=4,fetch=response)
    with pytest.raises(ValueError):resume_search(x,fetch=response)
def test_changed_total_fails_closed():
    a=failed()
    def moving(url):
        x=response(url);x["message"]["total-results"]=6;return x
    r=resume_search(a,fetch=moving)
    assert r["stopping_reason"]=="PROVIDER_FAILURE" and len(r["records"])==2
def test_retry_failure_retains_prior_records():
    r=resume_search(failed(),fetch=broken)
    assert len(r["records"])==2 and r["pages"][-1]["status"]=="FAIL"

def test_controlled_total_drift_is_partial_but_keeps_page():
    a=failed()
    def drift(url):
        x=response(url)
        x["message"]["total-results"]=6
        return x
    v=resume_search(a,fetch=drift,allow_total_drift=True)
    assert v["provider_total_drift_detected"]
    assert v["coverage_status"]=="PARTIAL_TOTAL_DRIFT"
    assert not v["complete_catalog_coverage"]
    assert len(v["records"])>=4
def test_transient_http_retry_is_bounded():
    from urllib.error import HTTPError
    attempts=[0]
    def sometimes(url):
        attempts[0]+=1
        if attempts[0]==1: raise HTTPError(url,429,"Too many requests",{},None)
        return response(url)
    r=resume_search(failed(),fetch=sometimes,retries=1,sleep=lambda _:None)
    assert r["retry_log"][0]["http_status"]==429
    assert len(r["records"])==5
def test_invalid_retry_limit_rejected():
    with pytest.raises(ValueError):resume_search(failed(),fetch=response,retries=8)
