"""Fail-closed mapping of image pixels to chart coordinates.

No curve coordinates are extracted from documents here. Calibration is valid
only when two distinct numeric ticks for EACH axis have been explicitly
verified by a human inspector from the original figure. Uncertainty bounds
are linearized local pixel-coordinate sensitivity, not measurement error.
"""
from __future__ import annotations
import hashlib,json,math

def _num(v):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):
        raise ValueError("A finite numeric coordinate is required")
    return float(v)

def calibrate_figure(record, points=()):
    required={"source_sha256","page","figure_id","image_width","image_height",
              "x_ticks","y_ticks","inspector_verified_ticks","pixel_uncertainty"}
    if not isinstance(record,dict) or set(record)!=required:
        raise ValueError("Incomplete figure calibration record")
    digest=record["source_sha256"]
    if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid source file checksum")
    page=record["page"]
    if not isinstance(page,int) or isinstance(page,bool) or page<1:
        raise ValueError("A physical PDF page is required")
    if not isinstance(record["figure_id"],str) or not record["figure_id"].strip():
        raise ValueError("Figure identifier required")
    w=_num(record["image_width"]);h=_num(record["image_height"])
    if w<8 or h<8:raise ValueError("Invalid pixel dimensions")
    uncertainty=_num(record["pixel_uncertainty"])
    if uncertainty<0 or uncertainty>10:raise ValueError("Unsupported pixel uncertainty")
    if not record["inspector_verified_ticks"]:
        return {"schema":"KRC-FIGURE-AXIS-1","status":"BLOCKED_UNVERIFIED_AXIS_TICKS",
                "figure_id":record["figure_id"],"source_sha256":digest,
                "scientific_plot_points_verified":False,"publication_ready":False}
    def axis(ticks,limit):
        if not isinstance(ticks,list) or len(ticks)!=2:raise ValueError("Exactly two anchor ticks required")
        if any(not isinstance(z,dict) or set(z)!={"pixel","value","unit"} for z in ticks):
            raise ValueError("Malformed anchor ticks")
        if ticks[0]["unit"]!=ticks[1]["unit"] or not isinstance(ticks[0]["unit"],str) or not ticks[0]["unit"]:
            raise ValueError("Axis unit mismatch")
        p0,p1=(_num(z["pixel"]) for z in ticks)
        v0,v1=(_num(z["value"]) for z in ticks)
        if not 0<=p0<=limit or not 0<=p1<=limit or p0==p1 or v0==v1:
            raise ValueError("Invalid or indistinguishable ticks")
        scale=(v1-v0)/(p1-p0)
        return p0,v0,scale,ticks[0]["unit"]
    x=axis(record["x_ticks"],w);y=axis(record["y_ticks"],h)
    if not isinstance(points,(list,tuple)) or len(points)>100:
        raise ValueError("Up to 100 selected image coordinates supported")
    mapped=[]
    for p in points:
        if not isinstance(p,dict) or set(p)!={"id","x_pixel","y_pixel"}:
            raise ValueError("Malformed figure point")
        px=_num(p["x_pixel"]);py=_num(p["y_pixel"])
        if not 0<=px<=w or not 0<=py<=h:raise ValueError("Point outside raster")
        mapped.append({"id":p["id"],"x":x[1]+(px-x[0])*x[2],
                       "y":y[1]+(py-y[0])*y[2],"x_unit":x[3],"y_unit":y[3],
                       "x_pixel_uncertainty_bound":abs(x[2])*uncertainty,
                       "y_pixel_uncertainty_bound":abs(y[2])*uncertainty})
    manifest={"source_sha256":digest,"page":page,"figure_id":record["figure_id"],
              "calibration":record,"mapped":mapped}
    return {"schema":"KRC-FIGURE-AXIS-1","status":"AXES_CALIBRATED_GEOMETRIC_ONLY",
            "figure_id":record["figure_id"],
            "manifest_sha256":hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
            "points":mapped,"scientific_plot_points_verified":False,"publication_ready":False}
