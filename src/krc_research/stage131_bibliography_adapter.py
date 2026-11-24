"""Stage131 public bibliography lookup: READ-ONLY INTERNET RESEARCH BY DEFAULT.

Public FREE_ONLY metadata lookup does not require separate owner approval per DOI.
Only signed scientific execution requires a separate immutable approved profile.
No paid fallback, source-content publishing or scientific truth attestation.
For deterministic/offline callers, explicitly set allow_network=False or inject a fake.
"""
import re
from urllib.parse import quote
from .stage131_bibliography_probe import classify_crossref, classify_europe_pmc, europe_pmc_query_url
from .stage131_bibliography_http import ProviderHTTPError, fetch_json_metadata

_DOI = re.compile(r"^10\.[0-9]{4,9}/[^\s?#]{1,220}$", re.ASCII)
def lookup_doi_metadata(doi, *, fetch_json=None, allow_network=True, timeout_seconds=5):
    if not isinstance(doi,str) or not _DOI.fullmatch(doi) or any(ch.isspace() or ord(ch)<32 or ord(ch)==127 for ch in doi):
        raise ValueError("INVALID_DOI")
    if allow_network is False:
        return {"status":"PROVIDER_DISABLED","doi":doi,"sources":{}}
    if allow_network is not True:
        raise ValueError("INVALID_NETWORK_MODE")
    if not isinstance(timeout_seconds,(int,float)) or isinstance(timeout_seconds,bool) or not (0 < timeout_seconds <= 10):
        raise ValueError("INVALID_TIMEOUT")
    if fetch_json is None:
        fetch_json = fetch_json_metadata
    urls = {
        "crossref":"https://api.crossref.org/works/"+quote(doi,safe=""),
        "europe_pmc":europe_pmc_query_url(doi),
    }
    sources={}
    for provider,url in urls.items():
        try:
            payload=fetch_json(url, timeout_seconds)
            sources[provider]=(classify_crossref if provider=="crossref" else classify_europe_pmc)(doi,payload)
        except ProviderHTTPError as exc:
            sources[provider]={
                "status":("PROVIDER_RATE_LIMITED" if exc.status==429
                          else "PROVIDER_NOT_FOUND" if exc.status==404
                          else "PROVIDER_UNAVAILABLE"),
                "http_status":exc.status,
            }
        except (TimeoutError,ConnectionError,OSError) as exc:
            sources[provider]={"status":"PROVIDER_UNAVAILABLE","error_type":type(exc).__name__}
        except ValueError as exc:
            sources[provider]={"status":"INVALID_PROVIDER_RESPONSE","error_type":type(exc).__name__}
    crossref=sources["crossref"]["status"]
    epmc=sources["europe_pmc"]["status"]
    if crossref=="METADATA_ONLY" and epmc=="METADATA_ONLY":
        verdict="TWO_PROVIDER_DOI_MATCH_METADATA_ONLY"
    elif crossref=="METADATA_ONLY" and epmc in ("NOT_FOUND","PROVIDER_NOT_FOUND"):
        # Europe PMC is not a comprehensive engineering publication index.
        verdict="COVERAGE_GAP_METADATA_ONLY"
    else:
        verdict="REVIEW_REQUIRED"
    return {"status":verdict,"doi":doi,"sources":sources,"full_text_verified":False,"experimental_independence_verified":False}

