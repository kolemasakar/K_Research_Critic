"""Bounded HTTPS metadata fetcher for Stage131, opt-in only.

Inject opener and sleep for deterministic offline tests. Never fetch article PDFs.
"""
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ALLOWED_HOSTS = ("https://api.crossref.org/works/", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?")
class ProviderHTTPError(OSError):
    def __init__(self, status):
        self.status=status
        super().__init__("HTTP_"+str(status))

def fetch_json_metadata(url, timeout_seconds=5, *, opener=urlopen, sleeper=time.sleep, max_attempts=2):
    if not isinstance(url,str) or not any(url.startswith(x) for x in ALLOWED_HOSTS):
        raise ValueError("PROVIDER_URL_DENIED")
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError("INVALID_RETRY_LIMIT")
    if not isinstance(timeout_seconds,(int,float)) or not 0 < timeout_seconds <= 10:
        raise ValueError("INVALID_TIMEOUT")
    request=Request(url,headers={"User-Agent":"KRC-Stage131-Research-Metadata/1 (metadata-only)","Accept":"application/json"})
    for attempt in range(max_attempts):
        try:
            with opener(request,timeout=timeout_seconds) as response:
                data=response.read(262145)
                if len(data)>262144:
                    raise ValueError("PROVIDER_RESPONSE_TOO_LARGE")
                return json.loads(data)
        except HTTPError as exc:
            if exc.code not in (429,503) or attempt+1>=max_attempts:
                raise ProviderHTTPError(exc.code) from exc
        except URLError as exc:
            if attempt+1>=max_attempts:
                raise ConnectionError("PROVIDER_CONNECTION_FAILED") from exc
        except TimeoutError:
            if attempt+1>=max_attempts: raise
        sleeper(min(0.25*(2**attempt),1))
    raise RuntimeError("UNREACHABLE")
