"""KRC P0 read-only JSON execution boundary for external orchestration.

Usage: python -m krc_research.offline_acceptance <input.json> <output.json>
No provider request or broker/service operation occurs here.
"""
from __future__ import annotations
import json
from pathlib import Path
from .canonical_evidence_ledger import Evidence, assess, adapt_legacy_report
from .manuscript_gates import ManuscriptGateInput
from .scholarly_preflight import scholarly_preflight
from .source_search_ledger import SearchRun

def evaluate_payload(payload: dict) -> dict:
    if "legacy_report" in payload:
        migrated=adapt_legacy_report(payload["legacy_report"])
        claims=[c["independent_assessment"] for c in migrated["claims"]]
        historical={"reported_pass":migrated["reported_prior_pass"],
                    "reported_shortfall":migrated["count"]-migrated["reported_prior_pass"],
                    "status":"IMPORTED_UNVERIFIED"}
    else:
        claim_rows=payload.get("claims",[])
        claims=[assess(c["claim_id"],c["required"],
                       [Evidence(**e) for e in c.get("evidence",[])]) for c in claim_rows]
        historical=None
    manuscript=ManuscriptGateInput(**payload["manuscript_gate"])
    searches=[SearchRun(**s) for s in payload.get("search_runs",[])]
    result=scholarly_preflight(claims=claims,searches=searches,manuscript=manuscript)
    return {"schema":"KRC-P0D-1", "result":result,
            "historical_report":historical,
            "final_publication_status":"NO_GO" if result["status"]=="REVISE" else "AWAIT_AUTHOR_JOURNAL_SIGNOFF"}

def main() -> None:
    import argparse
    cli=argparse.ArgumentParser()
    cli.add_argument("input",type=Path)
    cli.add_argument("output",type=Path)
    args=cli.parse_args()
    payload=json.loads(args.input.read_text(encoding="utf-8"))
    result=evaluate_payload(payload)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
