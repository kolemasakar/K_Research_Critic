"""Bounded FREE_ONLY public metadata transport for Crossref and Europe PMC.

Public research may use this transport by default without owner approval per
DOI. This transport does not fetch PDFs or authorize scientific execution.
HTTPS/URL safety, response size, timeouts and retry controls remain mandatory.
Signed private science dispatch has its own independent authorization boundary.
"""
import json
import re
import time
from urllib.parse import parse_qsl, quote, unquote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

MAX_BODY=262144
MAX_URL=1024
MAX_RETRIES=3
_DOI=re.compile(r"^10\.[0-9]{4,9}/[^\s?#]{1,220}$",re.ASCII)

class ProviderHTTPError(OSError):
    def __init__(self, status):
        self.status=int(status)
        super().__init__("HTTP_"+str(self.status))

class _DenyRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def _safe_url(url):
    if not isinstance(url,str) or not (0<len(url)<=MAX_URL) or any(ord(c)<33 or ord(c)>126 for c in url):
        raise ValueError("PROVIDER_URL_DENIED")
    try:parts=urlsplit(url)
    except ValueError:raise ValueError("PROVIDER_URL_DENIED") from None
    if (parts.scheme!="https" or parts.username is not None or parts.password is not None
        or parts.port is not None or parts.fragment
        or parts.netloc not in ("api.crossref.org","www.ebi.ac.uk")):
        raise ValueError("PROVIDER_URL_DENIED")
    if parts.netloc=="api.crossref.org":
        if parts.query or not parts.path.startswith("/works/"):
            raise ValueError("PROVIDER_URL_DENIED")
        encoded=parts.path.removeprefix("/works/")
        doi=unquote(encoded)
        if (not _DOI.fullmatch(doi) or quote(doi,safe="")!=encoded
            or any(part in ("..",".") for part in doi.split("/"))):
            raise ValueError("PROVIDER_URL_DENIED")
        return "crossref"
    if parts.path!="/europepmc/webservices/rest/search":
        raise ValueError("PROVIDER_URL_DENIED")
    try:pairs=parse_qsl(parts.query,keep_blank_values=True,strict_parsing=True)
    except ValueError:raise ValueError("PROVIDER_URL_DENIED") from None
    if len(pairs)!=3 or {key for key,_ in pairs}!={"query","format","pageSize"}:
        raise ValueError("PROVIDER_URL_DENIED")
    args=dict(pairs)
    doi=args["query"][4:] if args["query"].startswith("DOI:") else ""
    if (not _DOI.fullmatch(doi) or args["format"]!="json"
        or args["pageSize"]!="1" or any(part in ("..",".") for part in doi.split("/"))):
        raise ValueError("PROVIDER_URL_DENIED")
    return "europe_pmc"

def _fetch_opener(request,*,timeout):
    # HTTPRedirectHandler defaults to following a Location target; disallow all
    # such redirects including redirects to a private-network destination.
    return build_opener(_DenyRedirect()).open(request,timeout=timeout)

def _read_json(response,url):
    final_url=response.geturl() if callable(getattr(response,"geturl",None)) else None
    if final_url is not None and final_url!=url:
        raise ValueError("PROVIDER_REDIRECT_DENIED")
    headers=getattr(response,"headers",None)
    if headers is None or not callable(getattr(headers,"get",None)):
        raise ValueError("PROVIDER_CONTENT_TYPE_REQUIRED")
    ctype=headers.get("Content-Type","").split(";",1)[0].strip().casefold()
    if ctype!="application/json" and not (ctype.startswith("application/") and ctype.endswith("+json")):
        raise ValueError("PROVIDER_CONTENT_TYPE_DENIED")
    encoding=headers.get("Content-Encoding","identity").strip().casefold()
    if encoding not in ("identity",""):
        raise ValueError("PROVIDER_CONTENT_ENCODING_DENIED")
    length=headers.get("Content-Length")
    if length is not None and (not str(length).isdecimal() or int(length)>MAX_BODY):
        raise ValueError("PROVIDER_RESPONSE_TOO_LARGE")
    data=response.read(MAX_BODY+1)
    if len(data)>MAX_BODY:
        raise ValueError("PROVIDER_RESPONSE_TOO_LARGE")
    payload=json.loads(data)
    if not isinstance(payload,dict):
        raise ValueError("INVALID_PROVIDER_RESPONSE")
    return payload

def fetch_json_metadata(url, timeout_seconds=5, *, opener=None, sleeper=time.sleep, max_attempts=2):
    _safe_url(url)
    if type(max_attempts) is not int or not 1<=max_attempts<=MAX_RETRIES:
        raise ValueError("INVALID_RETRY_LIMIT")
    if type(timeout_seconds) not in (int,float) or not 0<timeout_seconds<=10:
        raise ValueError("INVALID_TIMEOUT")
    if opener is None:
        opener=_fetch_opener
    request=Request(url,headers={
        "User-Agent":"KRC-Stage134-Research-Metadata/1 (metadata-only; no PDF)",
        "Accept":"application/json",
        "Accept-Encoding":"identity",
    })
    for attempt in range(max_attempts):
        try:
            with opener(request,timeout=timeout_seconds) as response:
                return _read_json(response,url)
        except HTTPError as exc:
            # Never follow Location, never retry non-transient or redirection codes.
            if exc.code not in (429,503) or attempt+1>=max_attempts:
                raise ProviderHTTPError(exc.code) from exc
        except URLError as exc:
            if attempt+1>=max_attempts:
                raise ConnectionError("PROVIDER_CONNECTION_FAILED") from exc
        except TimeoutError:
            if attempt+1>=max_attempts:
                raise
        sleeper(min(0.25*(2**attempt),1))
    raise RuntimeError("UNREACHABLE")
