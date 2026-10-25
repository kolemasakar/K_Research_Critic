import hashlib,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.figure_asset_inventory import inventory_embedded_figures
from pypdf import PdfWriter
def blank(tmp_path):
 p=tmp_path/"sample.pdf";w=PdfWriter();w.add_blank_page(width=595,height=842)
 with p.open("wb") as f:w.write(f)
 return p,hashlib.sha256(p.read_bytes()).hexdigest()
def test_pdf_blank_inventory_not_graph_pass(tmp_path):
 p,h=blank(tmp_path);x=inventory_embedded_figures(path=p,approved_root=tmp_path,expected_sha256=h,page=1)
 assert x["images"]==[] and not x["scientific_graph_validation"]
def test_wrong_hash_fails_closed(tmp_path):
 p,h=blank(tmp_path)
 x=inventory_embedded_figures(path=p,approved_root=tmp_path,expected_sha256="0"*64,page=1)
 assert x["status"]=="HASH_MISMATCH"
def test_unapproved_path_denied(tmp_path):
 p,h=blank(tmp_path);sub=tmp_path/"sub";sub.mkdir()
 with pytest.raises(ValueError):inventory_embedded_figures(path=p,approved_root=sub,expected_sha256=h,page=1)
def test_invalid_page_denied(tmp_path):
 p,h=blank(tmp_path)
 with pytest.raises(ValueError):inventory_embedded_figures(path=p,approved_root=tmp_path,expected_sha256=h,page=0)
