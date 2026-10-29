import io,json
from urllib.error import HTTPError
import pytest
from krc_research.stage131_bibliography_http import fetch_json_metadata,ProviderHTTPError

URL="https://api.crossref.org/works/10.1000%2Ftest"
class Response:
    def __init__(self,data):self.data=data
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,n):return self.data[:n]

def http_error(status):
    return HTTPError(URL,status,"error",{},io.BytesIO())

@pytest.mark.parametrize("status",[429,503])
def test_retry_then_success(status):
    calls=[]; sleeps=[]
    def opener(req,timeout):
        calls.append(timeout)
        if len(calls)==1:raise http_error(status)
        return Response(b'{"message":{"DOI":"10.1000/test"}}')
    result=fetch_json_metadata(URL,opener=opener,sleeper=sleeps.append)
    assert result["message"]["DOI"]=="10.1000/test"
    assert calls==[5,5] and sleeps==[0.25]

@pytest.mark.parametrize("status",[429,503,404])
def test_fail_closed_http(status):
    with pytest.raises(ProviderHTTPError) as err:
        fetch_json_metadata(URL,opener=lambda *a,**k:(_ for _ in ()).throw(http_error(status)),sleeper=lambda _:None)
    assert err.value.status==status

def test_timeout_retry_and_limit():
    calls=[]
    def fail(*args,**kwargs):
        calls.append(1);raise TimeoutError()
    with pytest.raises(TimeoutError):fetch_json_metadata(URL,opener=fail,sleeper=lambda _:None)
    assert len(calls)==2

def test_oversize_invalid_json_and_unapproved_url():
    with pytest.raises(ValueError,match="TOO_LARGE"):
        fetch_json_metadata(URL,opener=lambda *a,**k:Response(b"x"*262145))
    with pytest.raises(json.JSONDecodeError):
        fetch_json_metadata(URL,opener=lambda *a,**k:Response(b"invalid"))
    with pytest.raises(ValueError,match="DENIED"):
        fetch_json_metadata("https://example.org",opener=lambda *a,**k:None)
