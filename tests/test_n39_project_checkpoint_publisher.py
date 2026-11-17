import base64, copy, importlib.util, json
from pathlib import Path
import pytest

spec=importlib.util.spec_from_file_location("publisher",Path(__file__).resolve().parents[1]/"tools/n39_project_checkpoint_publisher.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
M={"schema_version":"KRC_N39_PROJECT_CHECKPOINT_V1","phase":"STATE_CHECKPOINT",
   "journal_id":"project-"+"1"*32,"sequence":1,"chain_head_sha256":"2"*64,
   "previous_chain_head_sha256":"0"*64,"previous_anchor_commit_sha":"a"*40,
   "source_commit_sha":"b"*40,"recorded_at_utc":"2026-11-17T20:00:00Z"}
class API:
 def __init__(self,m):
  self.m=m;self.path=mod.validate(m);self.tip="a"*40;self.b=None;self.blob=None;self.merged=False;self.writes=[];self.rules_ok=True;self.added_only=True
 def __call__(self,method,p,b=None):
  if method!="GET":self.writes.append((method,p))
  if p=="rulesets/27332825":return {"enforcement":"active" if self.rules_ok else "disabled","conditions":{"ref_name":{"include":["refs/heads/"+mod.BASE]}},"bypass_actors":[],"rules":[{"type":v} for v in ("deletion","non_fast_forward","required_linear_history","pull_request")]}
  if p=="git/ref/heads/"+mod.BASE:return {"object":{"sha":self.tip}}
  if p.startswith("git/ref/heads/"):return {"object":{"sha":self.b}} if self.b else None
  if p=="git/commits/"+"b"*40:return {}
  if p.startswith("compare/"):return {"status":"ahead","behind_by":0,"files":[{"filename":self.path,"status":"added" if self.added_only else "modified"}]}
  if method=="GET" and p.startswith("contents/"):
   name,rev=p[9:].split("?ref=")
   filled=rev==self.b and self.blob is not None or rev==self.tip and self.merged
   if name==self.path:
    return {"type":"file","encoding":"base64","content":base64.b64encode(json.dumps(self.blob).encode()).decode()} if filled else None
   if name==self.path.rsplit("/",1)[0]:
    return [{"type":"file","name":self.path.rsplit("/",1)[1],"path":self.path}] if filled else None
  if method=="POST" and p=="git/refs":self.b=self.tip;return {}
  if method=="PUT" and p.startswith("contents/"):
   self.blob=json.loads(base64.b64decode(b["content"]));self.b="c"*40;return {}
  if method=="GET" and p.startswith("pulls?"):return []
  if method=="POST" and p=="pulls":return {"number":1,"head":{"sha":self.b},"base":{"ref":mod.BASE}}
  if method=="PUT" and p=="pulls/1/merge":
   assert b=={"sha":self.b,"merge_method":"rebase"};self.tip="d"*40;self.merged=True;return {"merged":True}
  raise AssertionError((method,p,b))

def test_publish_and_restart_are_idempotent():
 api=API(M)
 r=mod.publish(M,api=api)
 assert r["status"]=="PUBLISHED" and r["commit"]=="d"*40 and r["pr"]==1
 writes=api.writes[:]
 assert mod.publish(M,api=api)["commit"]==r["commit"]
 assert api.writes==writes

def test_no_private_fields_or_invalid_parent():
 with pytest.raises(ValueError,match="INVALID_MANIFEST_FIELDS"):
  mod.validate(dict(M,owner="private"))
 with pytest.raises(ValueError,match="INVALID_PREFIX"):
  mod.validate(dict(M,previous_chain_head_sha256="3"*64))
 api=API(M);api.tip="e"*40
 with pytest.raises(ValueError,match="BASE_MOVED_RECONCILE"):mod.publish(M,api=api)
 assert not api.writes

def test_protection_and_append_only_checks():
 api=API(M);api.rules_ok=False
 with pytest.raises(ValueError,match="RULESET_MISMATCH"):mod.publish(M,api=api)
 assert not api.writes
 api=API(M);api.added_only=False
 with pytest.raises(ValueError,match="NON_APPEND_ONLY_PR"):mod.publish(M,api=api)
 assert not any(p.startswith("pulls") for method,p in api.writes)

def test_conflicting_existing_checkpoint_denied():
 api=API(M);mod.publish(M,api=api);api.blob=dict(M,source_commit_sha="e"*40);before=api.writes[:]
 with pytest.raises(ValueError,match="REMOTE_FILE_CONFLICT"):mod.publish(M,api=api)
 assert api.writes==before
