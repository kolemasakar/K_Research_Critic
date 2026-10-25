"""Second-path deterministic Critic of pipeline records, not scientific peer review."""
import hashlib,json
REQUIRED=('claim_verdicts','inspection_audit','preflight','critic_iterations')
def run_critic(pipeline):
    if not isinstance(pipeline,dict) or any(k not in pipeline for k in REQUIRED):raise ValueError("Incomplete artifact")
    issues=[];seen=set()
    if not pipeline['claim_verdicts']:issues.append("CLAIMS_MISSING")
    for row in pipeline['claim_verdicts']:
        cid=row.get('claim_id')
        if not cid or cid in seen:issues.append("CLAIM_ID_DUPLICATE")
        seen.add(cid)
        origins=row.get('counted_origins',[])
        if row.get('achieved_independent')!=len(set(origins)):issues.append("ACCOUNTING_MISMATCH:"+str(cid))
        if row.get('verdict')!="PASS" or row.get('achieved_independent',0)<row.get('required',1):issues.append("CLAIM_SHORTFALL:"+str(cid))
    for receipt in pipeline['inspection_audit']:
        if not receipt.get('usable') or not receipt.get('external_attestation'):issues.append("SOURCE_UNVERIFIED:"+str(receipt.get('source_id')))
    p=pipeline['preflight']
    if p.get('search_reproducibility')!="PASS":issues.append("SEARCH_NOT_REPRODUCIBLE")
    if p.get('manuscript_gate',{}).get('status')!="READY_FOR_AUTHOR_REVIEW":issues.append("MANUSCRIPT_GATES_INCOMPLETE")
    if not pipeline['critic_iterations']:issues.append("CRITIC_ITERATIONS_MISSING")
    if pipeline.get('critic_independently_executed'):issues.append("UNSUPPORTED_INDEPENDENCE_CLAIM")
    digest=hashlib.sha256(json.dumps(pipeline,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return {"schema":"KRC-CRITIC-EXEC-1","input_sha256":digest,"engine":"DETERMINISTIC_RULE_CRITIC",
            "verdict":"REVISE" if issues else "CONDITIONAL_RULE_CHECK_PASS","issues":sorted(set(issues)),
            "independent_from_reported_verdict":True,"scientific_peer_review_completed":False,"publication_ready":False}
def iterate_critic(pipeline,max_rounds=3):
    if not 1<=max_rounds<=5:raise ValueError("Invalid rounds")
    result=run_critic(pipeline)
    return {"rounds_executed":1,"history":[{"iteration":1,"revision":"INPUT_UNCHANGED","result":result}],
            "requires_new_research_revision":result["verdict"]=="REVISE"}
