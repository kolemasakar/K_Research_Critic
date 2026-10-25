"""Inventory embedded source-PDF figure images; no automatic curve digitization.

Requires original SHA and an approved directory, records exact extracted RGB
image bytes and dimensions, but does not claim that image index corresponds
to a particular figure until visually reviewed.
"""
from __future__ import annotations
from hashlib import sha256
from io import BytesIO
from pathlib import Path

def inventory_embedded_figures(*,path,approved_root,expected_sha256,page):
    root=Path(approved_root).resolve(strict=True)
    p=Path(path)
    if p.is_symlink():raise ValueError("PDF symlink forbidden")
    p=p.resolve(strict=True)
    if not p.is_relative_to(root) or p.suffix.lower()!=".pdf" or not p.is_file():
        raise ValueError("PDF must be inside approved root")
    if p.stat().st_size>8_000_000:raise ValueError("PDF exceeds size cap")
    actual=sha256(p.read_bytes()).hexdigest()
    if actual!=expected_sha256:
        return {"schema":"KRC-FIGURE-INVENTORY-1","status":"HASH_MISMATCH",
                "source_sha256":actual,"images":[],"figure_axes_verified":False}
    from pypdf import PdfReader
    from PIL import Image
    pdf=PdfReader(str(p),strict=True)
    if pdf.is_encrypted or not isinstance(page,int) or isinstance(page,bool) or not 1<=page<=len(pdf.pages):
        raise ValueError("Invalid page or encrypted source")
    images=[]
    for index,entry in enumerate(pdf.pages[page-1].images):
        if index>=20:raise ValueError("Too many embedded images")
        im=Image.open(BytesIO(entry.data))
        if im.width>10_000 or im.height>10_000:raise ValueError("Oversized figure")
        rgb=im.convert("RGB")
        encoded=BytesIO()
        rgb.save(encoded,format="PNG")
        data=encoded.getvalue()
        images.append({"image_index":index+1,"embedded_name":entry.name,
                       "width_px":rgb.width,"height_px":rgb.height,
                       "rgb_png_sha256":sha256(data).hexdigest(),
                       "bytes":len(data),
                       "axes_verified":False,"curve_coordinates_verified":False})
    return {"schema":"KRC-FIGURE-INVENTORY-1","status":"RASTER_ASSETS_INVENTORIED",
            "source_sha256":actual,"physical_pdf_page":page,"images":images,
            "figure_axes_verified":False,"scientific_graph_validation":False}
