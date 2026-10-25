"""Couple independent reviewer receipt-signatures, evidence preflight and rule Critic.

Reviewer credentials MUST come from trusted server configuration, never research JSON.
"""
from .integrated_research import execute_research
from .independent_critic import iterate_critic
from .inspection_receipts import InspectionReceipt, audit_receipt
from .reviewer_attestation import verify_attestation

def run_review_cycle(package, *, attestations=(), trusted_reviewer_keys=None,
                     researcher_id=None, now=None):
    verified_hashes=set()
    if attestations:
        if not trusted_reviewer_keys or not researcher_id:
            raise ValueError("Trusted external reviewer configuration required")
        receipt_lookup={}
        for raw in package.get("inspection_receipts",[]):
            receipt=InspectionReceipt(**raw)
            receipt_lookup[audit_receipt(receipt)["receipt_sha256"]]=receipt
        for entry in attestations:
            if set(entry)!={"body","signature"}:
                raise ValueError("Attestation envelope invalid")
            b=entry["body"]
            receipt=receipt_lookup.get(b.get("receipt_sha256"))
            if receipt is None:
                raise ValueError("Attestation for unknown receipt")
            verified=verify_attestation(
                b,entry["signature"],trusted_reviewer_keys=trusted_reviewer_keys,
                expected_receipt_sha256=b["receipt_sha256"],
                expected_document_sha256=receipt.document_sha256,
                researcher_id=researcher_id,now=now)
            if verified["verified"]:
                verified_hashes.add(verified["receipt_sha256"])
    research=execute_research(package,attested_receipt_hashes=frozenset(verified_hashes))
    critic=iterate_critic(research)
    passed=critic["history"][-1]["result"]["verdict"]!="REVISE"
    return {"schema":"KRC-RESEARCH-V2","research":research,"critic":critic,
            "verified_reviewer_attestations":len(verified_hashes),
            "attestation_limit":"REVIEWER_IDENTITY_AND_DOCUMENT_BINDING_NOT_SCIENTIFIC_TRUTH",
            "final_gate":"AWAIT_INDEPENDENT_SCIENTIFIC_REVIEW" if passed else "NO_GO",
            "publication_ready":False}
