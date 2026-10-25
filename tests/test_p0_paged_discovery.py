import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.paged_discovery import paged_discovery,scoped_prisma_flow
def cross(url):
    from urllib.parse import parse_qs,urlsplit
    ofs=int(parse_qs(urlsplit(url).query)["offset"][0])
    rows=[{"DOI":f"10.1234/p{x}","title":[f"Paper {x}"]} for x in range(ofs,min(ofs+2,5))]
    return {"status":"ok","message":{"total-results":5,"items":rows}}
def alex(url):
    from urllib.parse import parse_qs,urlsplit
    page=int(parse_qs(urlsplit(url).query)["page"][0])
    start=(page-1)*2
    rows=[{"id":f"W{x}","doi":f"https://doi.org/10.1234/p{x}","display_name":f"Paper {x}"} for x in range(start,min(start+2,5))]
    return {"meta":{"count":5},"results":rows}
def test_crossref_reaches_reported_total():
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=4,fetch=cross)
    assert x["returned_unique_records"]==5 and len(x["pages"])==3
    assert x["stopping_reason"]=="REACHED_REPORTED_TOTAL"
def test_openalex_reaches_total():
    x=paged_discovery("ultrasonic concrete","OpenAlex",page_size=2,max_pages=4,fetch=alex)
    assert x["returned_unique_records"]==5 and x["complete_catalog_coverage"]
def test_cap_does_not_claim_complete():
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=1,fetch=cross)
    assert x["stopping_reason"]=="MAX_PAGES_REACHED" and not x["complete_catalog_coverage"]
def test_failure_preserves_first_page_and_reason():
    def failing(url):
        if "offset=2" in url:raise TimeoutError()
        return cross(url)
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=3,fetch=failing)
    assert x["stopping_reason"]=="PROVIDER_FAILURE" and x["returned_unique_records"]==2
def test_scoped_prisma_not_full_review():
    runs=[paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=4,fetch=cross),
          paged_discovery("ultrasonic concrete","OpenAlex",page_size=2,max_pages=4,fetch=alex)]
    y=scoped_prisma_flow(runs,selected_dois=["10.1234/p0"])
    assert y["records_identified"]==10 and y["duplicate_doi_records"]==5
    assert y["unique_doi_records_screened"]==5
    assert y["studies_included_in_synthesis"]==0
def test_unknown_inclusion_denied():
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=1,fetch=cross)
    with pytest.raises(ValueError):scoped_prisma_flow([x],selected_dois=["10.1234/not-found"])
def test_invalid_page_size_denied():
    with pytest.raises(ValueError):paged_discovery("ultrasonic concrete","OpenAlex",page_size=100,fetch=alex)
def test_provider_count_change_is_failure():
    def moving(url):
        r=cross(url)
        if "offset=2" in url:r["message"]["total-results"]=6
        return r
    x=paged_discovery("ultrasonic concrete","Crossref",page_size=2,max_pages=3,fetch=moving)
    assert x["stopping_reason"]=="PROVIDER_FAILURE"
