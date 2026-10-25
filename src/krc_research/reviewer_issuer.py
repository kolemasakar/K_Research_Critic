"""Reviewer-owned local issuance boundary; never auto-approves a scientific claim.

The independent reviewer supplies explicit inspection findings, and the signing key
must be provisioned out-of-band with filesystem permissions, not in research JSON.
"""
from __future__ import annotations
import hashlib
import json
import os
import stat
from pathlib import Path
from .reviewer_attestation import attestation_body, sign_attestation
from .inspection_receipts import InspectionReceipt, audit_receipt

def read_reviewer_key(path: str | Path) -> bytes:
    p=Path(path)
    if p.is_symlink() or not p.is_file():
        raise ValueError("Reviewer key must be a regular, non-symlink file")
    mode=p.stat().st_mode
    if stat.S_IMODE(mode) != 0o600 or p.stat().st_uid != os.geteuid():
        raise ValueError("Unsafe reviewer key ownership or mode")
    key=p.read_bytes()
    if len(key)<32 or len(key)>4096:
        raise ValueError("Invalid reviewer key length")
    return key

def issue_review_attestation(receipt: dict, *, reviewer_id: str,
                             researcher_id: str, inspection_record: dict,
                             key_path: str | Path) -> dict:
    if not isinstance(inspection_record,dict):
        raise ValueError("Independent inspection record required")
    if reviewer_id==researcher_id or not researcher_id:
        raise ValueError("Self review prohibited")
    if inspection_record.get("explicit_reviewer_approval") is not True:
        raise ValueError("Independent reviewer must explicitly approve")
    if inspection_record.get("reviewer_id")!=reviewer_id:
        raise ValueError("Inspection reviewer mismatch")
    if inspection_record.get("document_sha256")!=receipt.get("document_sha256"):
        raise ValueError("Inspected document digest mismatch")
    if inspection_record.get("source_id")!=receipt.get("source_id"):
        raise ValueError("Inspected source mismatch")
    if not inspection_record.get("methods_notes") or not inspection_record.get("results_notes"):
        raise ValueError("Methods and results inspection notes required")
    observed=InspectionReceipt(**receipt)
    structural=audit_receipt(observed)
    if not structural["eligible_for_independent_claim_review"]:
        raise ValueError("Receipt fails inspection structure")
    body=attestation_body(receipt_sha256=structural["receipt_sha256"],
                           document_sha256=observed.document_sha256,
                           reviewer_id=reviewer_id,checked_at=observed.checked_at)
    signature=sign_attestation(body,read_reviewer_key(key_path))
    inspection_digest=hashlib.sha256(json.dumps(inspection_record,
                         ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"body":body,"signature":signature,"inspection_record_sha256":inspection_digest,
            "scope":"SIGNED_REVIEWER_DECLARATION_NOT_SCIENTIFIC_FACT_PROOF",
            "scientific_truth_verified":False}
