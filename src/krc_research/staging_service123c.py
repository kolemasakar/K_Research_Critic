"""Stage123-C composition factory: separate staging service, no automatic launch."""
from pathlib import Path
from .artifact_stage117 import HardenedExchange
from .request_ledger119 import RequestLedger
from .replay_registry import ReplayRegistry
from .research_boundary120 import ResearchBoundary
from .science_adapter122 import ScienceAdapter122
from .uds_verified123b import VerifiedStage123Server
from .science_signer127 import KRCInternalScienceSigner,ScienceAuthorizationDenied
from .consent_custody128 import ConsentCustody128

def make_staging_server(socket_path, state_root, *,peer_principals,uid_keys,claim_allowlist,science_secret,bibliography_fn=None,enable_internal_science_signing=False):
    root=Path(state_root)
    root.mkdir(mode=0o700,parents=True,exist_ok=True)
    if root.is_symlink():raise ValueError("Symlink state root rejected")
    science=ScienceAdapter122(secret=science_secret,allowed_principals=set(peer_principals.values()),bibliography_fn=bibliography_fn)
    science.seen=ReplayRegistry(root/"signed-science-replay.sqlite")
    if enable_internal_science_signing:
        custody=ConsentCustody128(root/'consent-approvals.sqlite')
        signer=KRCInternalScienceSigner(science_key=science_secret,authorizer=custody,
                dispatcher=science,bibliography_enabled=bibliography_fn is not None)
        class InternalAuthorizedDispatch:
            def execute_authorized(self,operation,payload,principal,*,request_id):
                if not isinstance(payload,dict) or set(payload)!={'task_id','profile_ref','evidence_refs','consent_ref','science_payload'}:
                    raise ScienceAuthorizationDenied('INVALID_REQUEST')
                return signer.execute(request_id=request_id,task_id=payload['task_id'],operation=operation,
                    payload=payload['science_payload'],principal=principal,
                    profile_ref=payload['profile_ref'],evidence_refs=payload['evidence_refs'],
                    consent_ref=payload['consent_ref'])
        active_dispatch=InternalAuthorizedDispatch()
    else:
        active_dispatch=science
    boundary=ResearchBoundary(
        ledger=RequestLedger(root/"request-ledger.sqlite"),
        exchange=HardenedExchange(root/"artifacts"),
        dispatch=active_dispatch)
    return VerifiedStage123Server(socket_path,boundary=boundary,peer_principals=peer_principals,
                                  uid_keys=uid_keys,claim_allowlist=claim_allowlist)
