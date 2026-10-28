"""Stage123-C composition factory: separate staging service, no automatic launch."""
from pathlib import Path
from .artifact_stage117 import HardenedExchange
from .request_ledger119 import RequestLedger
from .replay_registry import ReplayRegistry
from .research_boundary120 import ResearchBoundary
from .science_adapter122 import ScienceAdapter122
from .uds_verified123b import VerifiedStage123Server

def make_staging_server(socket_path, state_root, *,peer_principals,uid_keys,claim_allowlist,science_secret,bibliography_fn=None):
    root=Path(state_root)
    root.mkdir(mode=0o700,parents=True,exist_ok=True)
    if root.is_symlink():raise ValueError("Symlink state root rejected")
    science=ScienceAdapter122(secret=science_secret,allowed_principals=set(peer_principals.values()),bibliography_fn=bibliography_fn)
    science.seen=ReplayRegistry(root/"signed-science-replay.sqlite")
    boundary=ResearchBoundary(
        ledger=RequestLedger(root/"request-ledger.sqlite"),
        exchange=HardenedExchange(root/"artifacts"),
        dispatch=science)
    return VerifiedStage123Server(socket_path,boundary=boundary,peer_principals=peer_principals,
                                  uid_keys=uid_keys,claim_allowlist=claim_allowlist)
