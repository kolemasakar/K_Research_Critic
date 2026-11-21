"""Stage134 offline provider-security and scientific-status negative matrix.

Only injected fake responses, no live provider API or network calls.
"""
import io
import pytest
from urllib.error import HTTPError
from krc_research.stage131_bibliography_http import (
    _safe_url, _DenyRedirect, fetch_json_metadata, ProviderHTTPError,
)
from krc_research.stage131_bibliography_adapter import lookup_doi_metadata
from krc_research.stage131_bibliography_reconcile import reconcile_metadata

GOOD="https://api.crossref.org/works/10.1000%2Fdemo"
EP="https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&format=json&pageSize=1"
BAD_URLS=[
    "http://api.crossref.org/works/10.1000%2Fdemo",
    "https://api.crossref.org.evil.invalid/works/10.1000%2Fdemo",
    "https://api.crossref.org@127.0.0.1/works/10.1000%2Fdemo",
    "https://api.crossref.org:444/works/10.1000%2Fdemo",
    "https://api.crossref.org/works/10.1000%2Fdemo?format=fulltext",
    "https://api.crossref.org/works/10.1000%2Fdemo#unsafe",
    "https://api.crossref.org/works/10.1000%252Fdemo",
    "https://api.crossref.org/works/10.1000%2F..%2Fmetadata",
    "https://api.crossref.org/works/../../../metadata",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=x&format=json&pageSize=1",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&format=xml&pageSize=1",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&format=json&pageSize=50",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&query=evil&format=json&pageSize=1",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&format=json&pageSize=1&extra=1",
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1000%2Fdemo&format=json&pageSize=1#fragment",
]
class Fake:
    def __init__(self,body=b'{"message":{"DOI":"10.1000/demo"}}',headers=None,url=GOOD):
        self.body=body
        self.headers=({"Content-Type":"application/json","Content-Encoding":"identity"}
                      if headers is None else headers)
        self.url=url
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def read(self,n):return self.body[:n]
    def geturl(self):return self.url

@pytest.mark.parametrize("value",BAD_URLS)
def test_provider_url_rejected_before_opener(value):
    calls=[]
    def unexpected(*a,**kw):
        calls.append(1)
        raise AssertionError("UNSAFE_NETWORK_ATTEMPT")
    with pytest.raises(ValueError,match="PROVIDER_URL_DENIED"):
        fetch_json_metadata(value,opener=unexpected)
    assert not calls

@pytest.mark.parametrize("url,expected",[(GOOD,"crossref"),(EP,"europe_pmc")])
def test_exact_provider_url_only(url,expected):
    assert _safe_url(url)==expected

def test_redirect_is_never_followed():
    assert _DenyRedirect().redirect_request(None,None,302,"Found",{},"http://127.0.0.1/") is None
    def redirected(*a,**kw):return Fake(url="http://127.0.0.1/private")
    with pytest.raises(ValueError,match="PROVIDER_REDIRECT_DENIED"):
        fetch_json_metadata(GOOD,opener=redirected)

@pytest.mark.parametrize("headers",[
    {},{"Content-Type":"text/html"},
    {"Content-Type":"application/pdf"},
    {"Content-Type":"application/json","Content-Encoding":"gzip"},
    {"Content-Type":"application/json","Content-Length":"262145"},
])
def test_disallowed_response_is_not_parsed(headers):
    with pytest.raises(ValueError):
        fetch_json_metadata(GOOD,opener=lambda *_a,**_kw:Fake(headers=headers))

def test_json_array_and_oversize_denied():
    for body in (b'[]',b'{"x":"'+b"a"*262145+b'"}'):
        with pytest.raises(ValueError):
            fetch_json_metadata(GOOD,opener=lambda *_a,**_kw:Fake(body=body))

def test_404_429_503_differ_in_adapter():
    for status,expected in ((404,"PROVIDER_NOT_FOUND"),(429,"PROVIDER_RATE_LIMITED"),(503,"PROVIDER_UNAVAILABLE")):
        def fail(url,timeout):
            if "crossref" in url:raise ProviderHTTPError(status)
            return {"resultList":{"result":[]}}
        out=lookup_doi_metadata("10.1000/demo",fetch_json=fail,allow_network=True)
        assert out["sources"]["crossref"]=={"status":expected,"http_status":status}
        assert out["status"]=="REVIEW_REQUIRED"
        assert not out["full_text_verified"]

def test_absence_from_europe_pmc_is_coverage_gap_not_disproof():
    doi="10.1000/demo"
    def fake(url,timeout):
        if "crossref" in url:return {"message":{"DOI":doi,"title":["Concrete"]}}
        return {"resultList":{"result":[]}}
    out=lookup_doi_metadata(doi,fetch_json=fake,allow_network=True)
    assert out["status"]=="COVERAGE_GAP_METADATA_ONLY"
    assert out["sources"]["europe_pmc"]["status"]=="NOT_FOUND"
    assert out["experimental_independence_verified"] is False
    reconcile=reconcile_metadata(doi,{"message":{"DOI":doi,"title":["Concrete"]}},
                                 {"resultList":{"result":[]}})
    assert reconcile["status"]=="COVERAGE_GAP_METADATA_ONLY"
    assert reconcile["field_checks"]["title"]=="NOT_CHECKED"

def test_network_disabled_before_injected_callback():
    def forbidden(*a,**kw):raise AssertionError("PROVIDER_CALLED")
    assert lookup_doi_metadata("10.1000/demo",fetch_json=forbidden)["status"]=="PROVIDER_DISABLED"
