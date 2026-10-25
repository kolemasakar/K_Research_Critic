"""No-network P0 scholarly cycle with injectable transport and fail-closed evidence."""
from .local_research_stages import execute_local_stage
from .workflow_readiness import inspect_workflow

STAGES = ("source_search", "source_verify", "critic_review", "research_export")

def run_offline_cycle(package: dict, transport) -> dict:
    """Transport must be explicitly injected; no implicit network or mutations."""
    gate = inspect_workflow(package)
    if not callable(transport):
        raise ValueError("Authorized transport callback required")
    outcomes = {}
    for stage in STAGES:
        request = {"stage": stage, "input_sha256": gate["input_sha256"]}
        acknowledgement = transport(request)
        if not isinstance(acknowledgement, dict) or acknowledgement.get("stage") != stage or acknowledgement.get("accepted") is not True:
            raise ValueError("Transport acknowledgement missing/mismatched")
        outcomes[stage] = execute_local_stage(stage, package)
    return {"schema": "KRC-P0-LOCAL-CYCLE-1", "input_sha256": gate["input_sha256"],
            "stages": outcomes, "transport": "INJECTED_TEST_ONLY",
            "critic_verdict": "REVISE", "scientific_approval": False,
            "publication_gate": "NO_GO", "network_tested": False}
