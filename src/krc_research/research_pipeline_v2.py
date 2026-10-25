"""Couple a fail-closed research assessment to a separately executed rule-based Critic."""
from .integrated_research import execute_research
from .independent_critic import iterate_critic
def run_review_cycle(package):
    research=execute_research(package)
    critic=iterate_critic(research)
    passed=critic['history'][-1]['result']['verdict']!="REVISE"
    return {"schema":"KRC-RESEARCH-V2","research":research,"critic":critic,
            "final_gate":"AWAIT_INDEPENDENT_SCIENTIFIC_REVIEW" if passed else "NO_GO",
            "publication_ready":False}
