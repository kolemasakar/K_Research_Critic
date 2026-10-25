import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.figure_axis_calibration import calibrate_figure
def rec():
 return {"source_sha256":"a"*64,"page":4,"figure_id":"FIG1",
   "image_width":1000,"image_height":800,
   "x_ticks":[{"pixel":100,"value":0,"unit":"%"},{"pixel":900,"value":8,"unit":"%"}],
   "y_ticks":[{"pixel":700,"value":4000,"unit":"m/s"},{"pixel":100,"value":5000,"unit":"m/s"}],
   "inspector_verified_ticks":True,"pixel_uncertainty":2}
def test_synthetic_geometry_mapping_not_scientific_result():
 r=calibrate_figure(rec(),[{"id":"p","x_pixel":500,"y_pixel":400}])
 p=r["points"][0]
 assert p["x"]==4 and p["y"]==4500
 assert p["x_pixel_uncertainty_bound"]==0.02
 assert not r["scientific_plot_points_verified"]
def test_unverified_ticks_block_even_with_points():
 x=rec();x["inspector_verified_ticks"]=False
 assert calibrate_figure(x,[{"id":"x","x_pixel":500,"y_pixel":400}])["status"]=="BLOCKED_UNVERIFIED_AXIS_TICKS"
def test_swapped_axis_or_undefined_units_denied():
 x=rec();x["x_ticks"][1]["unit"]="m/s"
 with pytest.raises(ValueError):calibrate_figure(x)
def test_out_of_image_point_denied():
 with pytest.raises(ValueError):calibrate_figure(rec(),[{"id":"p","x_pixel":1001,"y_pixel":400}])
def test_degenerate_axis_denied():
 x=rec();x["y_ticks"][1]["pixel"]=700
 with pytest.raises(ValueError):calibrate_figure(x)
def test_digest_mandatory():
 x=rec();x["source_sha256"]="short"
 with pytest.raises(ValueError):calibrate_figure(x)
