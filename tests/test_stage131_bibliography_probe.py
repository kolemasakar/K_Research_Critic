from urllib.parse import unquote
import pytest
from krc_research.stage131_bibliography_probe import europe_pmc_query_url,classify_europe_pmc,classify_crossref

def test_doi_query_uses_doi_field_not_ext_id():
    url=europe_pmc_query_url("10.1038/nature12373")
    assert "DOI%3A" in url and "EXT_ID" not in url
    assert "DOI:10.1038/nature12373" in unquote(url)

def test_metadata_not_promoted_to_fulltext():
    assert classify_europe_pmc("10.1038/nature12373",{"resultList":{"result":[{"doi":"10.1038/nature12373","isOpenAccess":"N"}]}})=={"status":"METADATA_ONLY","access":"OA_NOT_INDICATED","doi":"10.1038/nature12373"}
    x=classify_europe_pmc("10.1038/s41586-020-2649-2",{"resultList":{"result":[{"doi":"10.1038/s41586-020-2649-2","isOpenAccess":"Y"}]}})
    assert x["status"]=="METADATA_ONLY" and x["access"]=="OA_INDICATED"

def test_doi_mismatch_fail_closed():
    assert classify_crossref("10.1038/nature12373",{"message":{"DOI":"10.1038/other"}})["status"]=="DOI_MISMATCH"
    assert classify_europe_pmc("10.1038/nature12373",{"resultList":{"result":[{"doi":"10.1038/other"}]}})["status"]=="NOT_FOUND"

def test_malformed_provider_data_denied():
    with pytest.raises(ValueError):classify_crossref("10.1038/nature12373",{"message":None})
    with pytest.raises(ValueError):classify_europe_pmc("10.1038/nature12373",{})
    with pytest.raises(ValueError):europe_pmc_query_url("bad")
