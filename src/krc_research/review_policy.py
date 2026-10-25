"""Owner-approved combined Critic policy.

Automated audit is allowed during research development. A genuinely independent
external reviewer remains mandatory for final scientific acceptance. This
component does not issue reviewer signatures or assert academic validity.
"""
from __future__ import annotations

POLICY_ID="KRC-REVIEW-COMBINED-V1"
PHASES={"DEVELOPMENT","INTERNAL_VALIDATION","FINAL_SCIENTIFIC_ACCEPTANCE"}

def evaluate_review_policy(*, phase: str, automatic_critic: dict,
                           external_reviewer_attested: bool = False,
                           author_approved: bool = False) -> dict:
    if phase not in PHASES:
        raise ValueError("Unknown review phase")
    if not isinstance(automatic_critic, dict):
        raise ValueError("Automatic Critic report required")
    verdict=automatic_critic.get("verdict")
    if verdict not in {"REVISE","CONDITIONAL_RULE_CHECK_PASS"}:
        raise ValueError("Unsupported executed Critic verdict")
    scientific_pass=verdict=="CONDITIONAL_RULE_CHECK_PASS"
    if phase!="FINAL_SCIENTIFIC_ACCEPTANCE":
        status="INTERNAL_REVIEW_PASS" if scientific_pass else "REVISE"
    elif not scientific_pass:
        status="REVISE"
    elif not external_reviewer_attested:
        status="AWAIT_EXTERNAL_REVIEWER"
    elif not author_approved:
        status="AWAIT_AUTHOR_APPROVAL"
    else:
        status="REVIEW_GATES_COMPLETE_NOT_PUBLICATION_APPROVAL"
    return {"schema":POLICY_ID,"phase":phase,"automatic_critic_executed":True,
            "automatic_critic_verdict":verdict,
            "external_reviewer_required_at_final":True,
            "external_reviewer_attested":bool(external_reviewer_attested),
            "author_approved":bool(author_approved),
            "status":status,"journal_acceptance_guaranteed":False,
            "scientific_truth_verified":False,"publication_ready":False}
