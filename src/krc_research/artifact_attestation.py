"""Verify locally provided plaintext artifact bytes, not authorship or scientific truth."""
import hashlib
from pathlib import Path
def verify_plaintext_artifact(receipt,path,*,approved_root):
    root=Path(approved_root).resolve(strict=True);p=Path(path).resolve(strict=True)
    if not p.is_relative_to(root):raise ValueError("Path outside approved root")
    if not p.is_file() or p.stat().st_size>4194304:raise ValueError("Unsafe artifact")
    raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest();text=raw.decode('utf-8')
    loc=receipt.get('passage_locators',[])
    if not isinstance(loc,(list,tuple)) or not loc:raise ValueError("Locators required")
    present=all(isinstance(x,str) and len(x)>=4 and x in text for x in loc)
    matched=(digest==receipt.get('document_sha256') and present)
    return {"artifact_sha256":digest,"hash_match":digest==receipt.get('document_sha256'),
            "locators_present":present,"bytes_inspected":len(raw),"artifact_access":"LOCAL_PLAINTEXT",
            "verified_claim_science":False,"independent_attestation_granted":False,
            "status":"STRUCTURAL_MATCH" if matched else "SHORTFALL"}
