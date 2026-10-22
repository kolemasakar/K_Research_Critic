import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from krc_research.doi_provenance import normalize_doi, extract_crossref, extract_datacite, deduplicate, ClaimEvidence, audit_claim

@pytest.mark.parametrize('value', [
    '10.1038/NATURE12373',
    'doi:10.1038/nature12373',
    'https://doi.org/10.1038/nature12373',
    'https://dx.doi.org/10.1038%2Fnature12373',
])
def test_normalize_variants(value):
    assert normalize_doi(value) == '10.1038/nature12373'

@pytest.mark.parametrize('value', ['', 'invalid', '10.12/a', '10.1234/has spaces', None])
def test_bad_doi(value):
    with pytest.raises(ValueError): normalize_doi(value)

def test_crossref_metadata_only():
    value = extract_crossref({'status':'ok', 'message': {
      'DOI':'10.1038/nature12373', 'title':['Nanometre-scale thermometry in a living cell'],
      'published': {'date-parts':[[2013,8]]}, 'author':[{'family':'Kucsko'}]}})
    assert value['year']==2013 and value['access_status']=='METADATA_ONLY'

def test_datacite_metadata_only():
    value = extract_datacite({'data':{'attributes':{
      'doi':'10.6084/m9.figshare.21545982', 'titles':[{'title':'Sample deposit'}],
      'creators':[{'name':'Example'}], 'publicationYear':2022}}})
    assert value['metadata_source']=='DataCite' and value['access_status']=='METADATA_ONLY'

def test_dedup_identity():
    works, mapping = deduplicate([{'doi':'doi:10.1038/nature12373','title':'Title'},
      {'doi':'https://doi.org/10.1038/NATURE12373','title':'Title'}])
    assert len(works)==1 and mapping[0]==mapping[1]

def test_metadata_conflict():
    with pytest.raises(ValueError):
        deduplicate([{'doi':'10.1038/nature12373','title':'A'},
                     {'doi':'10.1038/nature12373','title':'B'}])

def test_no_fake_source_independence():
    evidence = [
      ClaimEvidence('C1','one-paper','paper reference',True,'SUPPORTED'),
      ClaimEvidence('C1','one-paper','syndicated citation',True,'SUPPORTED'),
      ClaimEvidence('C1','two-paper','',True,'SUPPORTED'),
      ClaimEvidence('C1','three-paper','reference',False,'SUPPORTED')]
    assert audit_claim('C1',evidence,2)['status']=='SHORTFALL'

def test_two_independent_inspected_sources():
    evidence = [ClaimEvidence('C1','paper-a','reference A',True,'SUPPORTED'),
                ClaimEvidence('C1','paper-b','reference B',True,'SUPPORTED')]
    assert audit_claim('C1',evidence,2)['status']=='PASS'

def test_unrelated_claim_not_counted():
    assert audit_claim('C1',[ClaimEvidence('C2','origin','citation',True,'SUPPORTED')],1)['achieved_independent']==0
