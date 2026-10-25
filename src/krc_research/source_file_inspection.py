"""Inspect permitted source files, preserve page/section provenance; no scientific truth claims.

PDF extraction is text-only via pypdf when installed, with a strict byte/page cap.
No OCR, no web downloads, no arbitrary local file discovery.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
MAX_PAGES = 100

def inspect_source_file(*, path, approved_root, expected_sha256, passages, access):
    root=Path(approved_root).resolve(strict=True)
    candidate=Path(path)
    if candidate.is_symlink():
        raise ValueError("Symlink input denied")
    p=candidate.resolve(strict=True)
    if not p.is_relative_to(root) or not p.is_file():
        raise ValueError("Source outside approved directory")
    if p.stat().st_size > MAX_BYTES:
        raise ValueError("Source too large")
    raw=p.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        return {"status":"HASH_MISMATCH","sha256":digest,"access":"UNKNOWN",
                "inspections":[],"scientific_truth_verified":False}
    if access not in {"FULL_TEXT","METHODS_RESULTS_EXCERPT"}:
        raise ValueError("Access level insufficient")
    if not isinstance(passages,list) or not passages or len(passages)>20:
        raise ValueError("1..20 passage descriptors required")
    if p.suffix.lower()==".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("pypdf unavailable; fail closed") from exc
        reader=PdfReader(str(p),strict=True)
        if reader.is_encrypted or len(reader.pages)>MAX_PAGES:
            raise ValueError("Encrypted or oversized PDF")
        pages=[page.extract_text() or "" for page in reader.pages]
        kind="PDF_TEXT_EXTRACTED"
    elif p.suffix.lower() in {".txt",".md"}:
        pages=[raw.decode("utf-8")]
        kind="UTF8_TEXT"
    else:
        raise ValueError("Unsupported file type")
    inspected=[]
    for item in passages:
        if not isinstance(item,dict) or set(item)!={"page","section","exact_quote"}:
            raise ValueError("Passage descriptor requires page, section, exact_quote")
        number=item["page"]
        section=item["section"]
        quote=item["exact_quote"]
        if not isinstance(number,int) or isinstance(number,bool) or not 1<=number<=len(pages):
            raise ValueError("Invalid 1-based page number")
        if section not in {"METHODS","RESULTS","LIMITATIONS","OTHER"}:
            raise ValueError("Invalid section label")
        if not isinstance(quote,str) or len(quote)<8 or len(quote)>500:
            raise ValueError("Invalid quoted passage")
        inspected.append({"page":number,"section":section,
            "exact_quote_sha256":hashlib.sha256(quote.encode("utf-8")).hexdigest(),
            "found":quote in pages[number-1]})
    sections={x["section"] for x in inspected if x["found"]}
    verified=all(x["found"] for x in inspected) and {"METHODS","RESULTS"}.issubset(sections)
    return {"status":"TEXT_MATCH_WITH_METHODS_RESULTS" if verified else "INSPECTION_SHORTFALL",
            "sha256":digest,"access":kind,"page_count":len(pages),
            "inspections":inspected,"scientific_truth_verified":False,
            "independent_reviewer_attestation":False}
