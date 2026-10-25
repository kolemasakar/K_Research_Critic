import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.publication_date_screen import screen_publication_dates
def item(value="2024-03-09",provider="Crossref"):
    return {"source_id":"S1","doi":"10.3390/buildings14030720","published_date":value,"date_source":provider}
def test_inclusive_period():
    assert screen_publication_dates([item()],start="2024-03-09",end="2024-03-09")["in_period"]==1
def test_older_year_excluded():
    assert screen_publication_dates([item()],start="2013-01-01",end="2023-12-31")["out_of_period"]==1
def test_missing_date_unresolved():
    assert screen_publication_dates([item(None,None)],start="2000-01-01",end="2030-01-01")["unresolved"]==1
def test_missing_origin_fails_closed():
    with pytest.raises(ValueError):screen_publication_dates([item(None,"Crossref")],start="2000-01-01",end="2030-01-01")
def test_unattributed_date_fails_closed():
    with pytest.raises(ValueError):screen_publication_dates([item("2024-03-09",None)],start="2000-01-01",end="2030-01-01")
def test_backward_dates_denied():
    with pytest.raises(ValueError):screen_publication_dates([item()],start="2030-01-01",end="2020-01-01")
def test_bad_day_denied():
    with pytest.raises(ValueError):screen_publication_dates([item("2024-02-30")],start="2000-01-01",end="2030-01-01")
