"""Publish an outbox manifest through the accepted protected GitHub PR flow.

Run ONLY on an already authenticated, trusted publishing client with gh CLI.
Inputs and outputs are public hash-only manifests/receipts; no private DB,
profile or secret is accepted. The server need not have a GitHub credential.
No direct protected branch writes, force push, delete or consent changes.
"""
import argparse
import base64
import datetime
import json
import re
import subprocess
from urllib.parse import quote

REPO="kolemasakar/K_Research_Critic"
BASE="audit/n39-anchor-ledger"
RULESET=27332825
ZERO="0"*64
FIELDS={"schema_version","journal_id","sequence","chain_head_sha256",
        "previous_chain_head_sha256","previous_anchor_commit_sha","source_commit_sha",
        "recorded_at_utc","phase"}

def require(ok,code):
    if not ok:raise ValueError(code)

def hexstr(v,n):
    return isinstance(v,str) and bool(re.fullmatch("[a-f0-9]{"+str(n)+"}",v))

def validate(m):
    require(type(m) is dict and set(m)==FIELDS,"INVALID_MANIFEST_FIELDS")
    require(m["schema_version"]=="KRC_N39_PROJECT_CHECKPOINT_V1" and m["phase"]=="STATE_CHECKPOINT","INVALID_SCHEMA")
    require(isinstance(m["journal_id"],str) and bool(re.fullmatch(r"project-[a-f0-9]{32}",m["journal_id"])),"INVALID_JOURNAL")
    require(type(m["sequence"]) is int and 1<=m["sequence"]<=99999999,"INVALID_SEQUENCE")
    require(all(hexstr(m[k],64) for k in ("chain_head_sha256","previous_chain_head_sha256")) and
            all(hexstr(m[k],40) for k in ("previous_anchor_commit_sha","source_commit_sha")),"INVALID_HASH")
    require((m["sequence"]==1)==(m["previous_chain_head_sha256"]==ZERO),"INVALID_PREFIX")
    require(isinstance(m["recorded_at_utc"],str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",m["recorded_at_utc"])),"INVALID_TIMESTAMP")
    datetime.datetime.strptime(m["recorded_at_utc"],"%Y-%m-%dT%H:%M:%SZ")
    return f'audit/n39/anchors/{m["journal_id"]}/{m["sequence"]:08d}-{m["chain_head_sha256"]}.json'

class Github:
    """Uses existing gh authentication; never prints auth or subprocess stderr."""
    def __call__(self,method,path,body=None):
        args=["gh","api","--method",method,"repos/"+REPO+"/"+path]
        kw={}
        if body is not None:
            args.extend(["--input","-"]);kw["input"]=json.dumps(body)
        r=subprocess.run(args,text=True,capture_output=True,timeout=45,**kw)
        if r.returncode:
            if "[HTTP 404]" in r.stderr or "(HTTP 404)" in r.stderr:return None
            raise ValueError("GITHUB_API_FAILED")
        return json.loads(r.stdout) if r.stdout.strip() else {}

def publish(m,*,api):
    path=validate(m)
    key=m["chain_head_sha256"]
    short=f'{m["journal_id"]}-{m["sequence"]:08d}-{key}'
    branch="audit/publish-"+short
    def get(p):return api("GET",p)
    def ref(b):
        r=get("git/ref/heads/"+b)
        return None if r is None else r["object"]["sha"]
    def file(p,rev):
        r=get("contents/"+p+"?ref="+quote(rev,safe=""))
        if r is None:return None
        require(r.get("type")=="file" and r.get("encoding")=="base64","INVALID_REMOTE_FILE")
        return json.loads(base64.b64decode(r["content"],validate=False))
    def ancestor(a,b):
        if a==b:return True
        r=get("compare/"+a+"..."+b)
        return r is not None and r.get("status")=="ahead" and r.get("behind_by")==0
    def verify_prefix(rev,include_current=False):
        directory=path.rsplit("/",1)[0]
        listed=get("contents/"+directory+"?ref="+quote(rev,safe=""))
        values=[] if listed is None else listed
        require(isinstance(values,list),"INVALID_REMOTE_DIRECTORY")
        expected=m["sequence"] if include_current else m["sequence"]-1
        # API contents has a 1000-entry ceiling: fail closed rather than
        # silently accepting an unverified long journal.
        require(len(values)==expected and expected<1000,"REMOTE_PREFIX_COUNT")
        previous=ZERO
        for i,v in enumerate(sorted(values,key=lambda x:x["name"]),1):
            require(v.get("type")=="file","REMOTE_PREFIX_TYPE")
            a=file(v["path"],rev)
            require(a is not None and validate(a)==v["path"] and a["sequence"]==i
                    and a["journal_id"]==m["journal_id"] and a["previous_chain_head_sha256"]==previous,
                    "REMOTE_PREFIX_MISMATCH")
            previous=a["chain_head_sha256"]
        require(previous==(key if include_current else m["previous_chain_head_sha256"]),"REMOTE_HEAD_MISMATCH")
    rules=get("rulesets/"+str(RULESET))
    require(rules is not None and rules.get("enforcement")=="active" and
      rules.get("conditions",{}).get("ref_name",{}).get("include")==["refs/heads/"+BASE] and
      not rules.get("bypass_actors") and {"deletion","non_fast_forward","required_linear_history","pull_request"}.issubset(
       {x["type"] for x in rules.get("rules",[])}),"RULESET_MISMATCH")
    tip=ref(BASE)
    require(hexstr(tip,40) and ancestor(m["previous_anchor_commit_sha"],tip),"BASE_ANCESTRY_MISMATCH")
    require(get("git/commits/"+m["source_commit_sha"]) is not None,"UNKNOWN_SOURCE_PIN")
    existing=file(path,tip)
    if existing is not None:
        require(existing==m,"REMOTE_FILE_CONFLICT")
        verify_prefix(tip,True)
        return {"status":"PUBLISHED","sequence":m["sequence"],"head":key,"commit":tip}
    require(tip==m["previous_anchor_commit_sha"],"BASE_MOVED_RECONCILE")
    verify_prefix(tip)
    b=ref(branch)
    if b is None:
        api("POST","git/refs",{"ref":"refs/heads/"+branch,"sha":tip})
        b=ref(branch)
    require(hexstr(b,40),"PUBLISH_BRANCH_MISSING")
    if b==tip:
        api("PUT","contents/"+path,{"branch":branch,
            "message":"Append observed N39 project checkpoint",
            "content":base64.b64encode((json.dumps(m,sort_keys=True,indent=2)+"\n").encode()).decode()})
        b=ref(branch)
    require(file(path,b)==m,"PUBLISH_BRANCH_CONFLICT")
    delta=get("compare/"+tip+"..."+b)
    require(delta and delta.get("status")=="ahead" and delta.get("behind_by")==0 and
            [(x["filename"],x["status"]) for x in delta.get("files",[])]==[(path,"added")],
            "NON_APPEND_ONLY_PR")
    prs=get("pulls?state=open&head="+quote("kolemasakar:"+branch,safe="")+"&base="+quote(BASE,safe=""))
    require(isinstance(prs,list) and len(prs)<=1,"PR_CONFLICT")
    if prs:pr=prs[0]
    else:pr=api("POST","pulls",{"head":branch,"base":BASE,"title":"Append N39 state checkpoint "+str(m["sequence"]),
          "body":"Hash-only observed private state; no consent or service changes.","draft":False})
    require(pr["head"]["sha"]==b and pr["base"]["ref"]==BASE,"PR_PIN_MISMATCH")
    require(ref(BASE)==tip,"BASE_MOVED_RECONCILE")
    result=api("PUT","pulls/"+str(pr["number"])+"/merge",{"sha":b,"merge_method":"rebase"})
    require(result and result.get("merged") is True,"MERGE_NOT_CONFIRMED")
    merged=ref(BASE)
    require(ancestor(tip,merged) and file(path,merged)==m,"MERGE_VERIFICATION_FAILED")
    verify_prefix(merged,True)
    return {"status":"PUBLISHED","sequence":m["sequence"],"head":key,"commit":merged,"pr":pr["number"]}

def main():
    p=argparse.ArgumentParser();p.add_argument("manifest");p.add_argument("--publish",action="store_true")
    a=p.parse_args()
    with open(a.manifest,encoding="utf-8") as f:m=json.load(f)
    path=validate(m)
    if not a.publish:
        print(json.dumps({"status":"VALIDATED_ONLY","path":path}));return
    print(json.dumps(publish(m,api=Github()),sort_keys=True))

if __name__=="__main__":main()
