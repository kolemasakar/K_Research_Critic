"""Stage131 opt-in metadata-only DOI adapter. Does not dispatch network by default.

Caller must explicitly pass a fetch_json(url, timeout_seconds) function and allow_network=True.
No scientific execution, no full-text download, no provider credentials.
"""
import re
from urllib.parse import quote
from .stage131_bibliography_probe import classify_crossref, classify_europe_pmc, europe_pmc_query_url

_DOI = re.compile(r"^10\.[0-9]{4,9}/[^\s?#]{1,220}$", re.ASCII)
def lookup_doi_metadata(doi, *, fetch_json=None, allow_network=False, timeout_seconds=5):
    if not isinstance(doi,str) or not _DOI.fullmatch(doi):
        raise ValueError("INVALID_DOI")
    if not allow_network or fetch_json is None:
        return {"status":"PROVIDER_DISABLED","doi":doi,"sources":{}}
    if not isinstance(timeout_seconds,(int,float)) or not (0 < timeout_seconds <= 10):
        raise ValueError("INVALID_TIMEOUT")
    urls = {
        "crossref":"https://api.crossref.org/works/"+quote(doi,safe=""),
        "europe_pmc":europe_pmc_query_url(doi),
    }
    sources={}
    for provider,url in urls.items():
        try:
            payload=fetch_json(url, timeout_seconds)
            sources[provider]=(classify_crossref if provider=="crossref" else classify_europe_pmc)(doi,payload)
        except (TimeoutError,ConnectionError,OSError) as exc:
            sources[provider]={"status":"PROVIDER_UNAVAILABLE","error_type":type(exc).__name__}
        except ValueError as exc:
            sources[provider]={"status":"INVALID_PROVIDER_RESPONSE","error_type":type(exc).__name__}
    if any(v["status"] not in ("METADATA_ONLY",) for v in sources.values()):
        verdict="REVIEW_REQUIRED"
    else:
        verdict="TWO_PROVIDER_DOI_MATCH_METADATA_ONLY"
    return {"status":verdict,"doi":doi,"sources":sources,"full_text_verified":False,"experimental_independence_verified":False}
