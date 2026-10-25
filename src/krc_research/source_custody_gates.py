import hashlib
from pathlib import Path

def verify_source_bytes(path, expected_sha256):
    if not isinstance(expected_sha256,str) or len(expected_sha256)!=64:
        raise ValueError('Invalid digest')
    bytes.fromhex(expected_sha256)
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>20000000:
        raise ValueError('Invalid source file')
    data=p.read_bytes()
    return {'sha256':hashlib.sha256(data).hexdigest(), 'bytes':len(data), 'status':'PASS' if hashlib.sha256(data).hexdigest()==expected_sha256.lower() else 'HASH_MISMATCH', 'scientific_claim_verified':False}

def review_methods_novelty(package):
    if not isinstance(package,dict):raise ValueError('Object required')
    methods=('research_question','methods','sampling_plan','uncertainty_plan')
    novelty=('prior_art_search_log','novelty_claim','closest_prior_work')
    missing_m=[k for k in methods if not isinstance(package.get(k),str) or not package[k].strip()]
    missing_n=[k for k in novelty if not isinstance(package.get(k),str) or not package[k].strip()]
    return {'methodology':'SHORTFALL' if missing_m else 'DOCUMENTED_FOR_REVIEW', 'novelty':'SHORTFALL' if missing_n else 'DOCUMENTED_FOR_REVIEW', 'missing_methodology':missing_m, 'missing_novelty':missing_n, 'independent_novelty_established':False, 'publication_gate':'NO_GO'}
