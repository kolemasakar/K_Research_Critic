from __future__ import annotations

import argparse

from persistence import SQLitePersistenceStore
from supervisor.metrics import collect_quality_metrics_from_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect a persisted K_Supervisor task audit.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--database", default="runtime/k_supervisor.db")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        store = SQLitePersistenceStore(args.database)
        audit = store.load_task_audit(args.task_id)
    except (KeyError, OSError, ValueError) as exc:
        print(f"ERROR: cannot load task audit: {exc}")
        return 1

    workflow = audit.workflow_run
    quality = collect_quality_metrics_from_audit(audit)
    print(f"Task ID: {audit.task.task_id}")
    print(f"Task state: {audit.task.status.value}")
    print(f"Workflow: {workflow.workflow_run_id if workflow else 'NONE'}")
    print(f"Workflow status: {workflow.status.value if workflow else 'NONE'}")
    print(f"Transitions: {len(audit.transitions)}")
    print(f"CriticProfiles: {len(audit.critic_profiles)}")
    print(f"Approvals: {len(audit.user_approvals)}")
    print(f"Agent runs: {len(audit.agent_results)}")
    print(f"Research results: {len(audit.research_results)}")
    print(f"Claims: {len(audit.claims)}")
    print(f"Sources: {len(audit.sources)}")
    print(f"Reviews: {len(audit.reviews)}")
    print(f"Artifacts: {len(audit.artifacts)}")
    print(f"Quality iterations: {quality.iteration_count}")
    print(
        "Quality critic decisions: "
        + (", ".join(item.value for item in quality.critic_decisions) or "NONE")
    )
    print(
        "Quality final reliability: "
        + (
            f"{quality.final_reliability_score:.4f}"
            if quality.final_reliability_score is not None
            else "NONE"
        )
    )
    print(
        "Quality claim source coverage: "
        + (
            f"{quality.claim_source_coverage_ratio:.4f}"
            if quality.claim_source_coverage_ratio is not None
            else "NONE"
        )
    )
    print(
        "Quality claim verification: "
        + (
            f"{quality.claim_verification_ratio:.4f}"
            if quality.claim_verification_ratio is not None
            else "NONE"
        )
    )
    print(f"Quality unresolved claims: {quality.claims_unresolved}")
    print(f"Quality critical issues: {quality.critical_issue_count}")
    print(f"Quality contradictions: {quality.contradiction_count}")
    print(f"Quality missing topics: {quality.missing_topic_count}")
    print(f"Tool search calls: {quality.search_calls}")
    print(f"Tool fetch calls: {quality.fetch_calls}")
    for artifact in audit.artifacts:
        print(f"Artifact: {artifact.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
