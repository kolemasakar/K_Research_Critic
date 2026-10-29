from krc_research.stage131_bibliography_reconcile import reconcile_metadata
DOI="10.1088/1757-899X/365/3/032058"
def crossref(title="Concrete testing",year=2018):
    return {"message":{"DOI":DOI,"title":[title],"published":{"date-parts":[[year]]}}}
def pmc(title="Concrete testing",year="2018"):
    return {"resultList":{"result":[{"doi":DOI,"title":title,"pubYear":year}]}}
def test_field_match_metadata_only():
    x=reconcile_metadata(DOI,crossref(),pmc())
    assert x["status"]=="FIELDS_MATCH_METADATA_ONLY"
    assert x["field_checks"]=={"title":"MATCH","year":"MATCH"}
    assert not x["full_text_verified"] and not x["experimental_independence_verified"]
def test_title_mismatch_review():
    assert reconcile_metadata(DOI,crossref(),pmc(title="Different"))["field_checks"]["title"]=="MISMATCH"
def test_year_mismatch_review():
    assert reconcile_metadata(DOI,crossref(),pmc(year="2017"))["status"]=="REVIEW_REQUIRED"
def test_no_claim_on_missing_fields():
    assert reconcile_metadata(DOI,crossref(title=""),pmc())["field_checks"]["title"]=="MISSING"
def test_invalid_and_doi_mismatch():
    assert reconcile_metadata(DOI,{},pmc())["status"]=="DOI_MISMATCH_OR_ABSENT"
    assert reconcile_metadata(DOI,crossref(),{"resultList":{"result":[]}})["status"]=="DOI_MISMATCH_OR_ABSENT"
