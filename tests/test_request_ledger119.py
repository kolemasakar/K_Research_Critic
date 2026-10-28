import pytest
from concurrent.futures import ThreadPoolExecutor
from krc_research.request_ledger119 import RequestLedger,LedgerError

def test_first_and_replay(tmp_path):
 a=RequestLedger(tmp_path/"l.db")
 assert a.admit(principal="p",request_id="r",operation="op",payload={"n":1})["decision"]=="EXECUTE"
 a.complete(principal="p",request_id="r",operation="op",payload={"n":1},result={"ok":True})
 assert a.admit(principal="p",request_id="r",operation="op",payload={"n":1})["result"]=={"ok":True}

def test_reboot_ambiguous_fail_closed(tmp_path):
 path=tmp_path/"l.db"
 a=RequestLedger(path)
 a.admit(principal="p",request_id="r",operation="op",payload={})
 b=RequestLedger(path)
 assert b.admit(principal="p",request_id="r",operation="op",payload={})["decision"]=="AMBIGUOUS"

def test_changed_body_conflict(tmp_path):
 l=RequestLedger(tmp_path/"l.db");l.admit(principal="p",request_id="r",operation="a",payload={})
 with pytest.raises(LedgerError,match="IDEMPOTENCY_CONFLICT"):
  l.admit(principal="p",request_id="r",operation="a",payload={"changed":True})

def test_principal_scoped(tmp_path):
 l=RequestLedger(tmp_path/"l.db")
 assert l.admit(principal="a",request_id="same",operation="op",payload={})["decision"]=="EXECUTE"
 assert l.admit(principal="b",request_id="same",operation="op",payload={})["decision"]=="EXECUTE"

def test_concurrent_at_most_one_admission(tmp_path):
 l=RequestLedger(tmp_path/"l.db")
 with ThreadPoolExecutor(max_workers=8) as e:
  results=list(e.map(lambda _:l.admit(principal="p",request_id="same",operation="op",payload={})["decision"],range(8)))
 assert results.count("EXECUTE")==1 and results.count("AMBIGUOUS")==7

def test_complete_requires_existing(tmp_path):
 l=RequestLedger(tmp_path/"l.db")
 with pytest.raises(LedgerError,match="IDEMPOTENCY_CONFLICT"):
  l.complete(principal="p",request_id="r",operation="op",payload={},result={})

def test_canonical_key_order(tmp_path):
 l=RequestLedger(tmp_path/"l.db")
 l.admit(principal="p",request_id="r",operation="op",payload={"b":2,"a":1})
 assert l.admit(principal="p",request_id="r",operation="op",payload={"a":1,"b":2})["decision"]=="AMBIGUOUS"

def test_invalid_principal(tmp_path):
 l=RequestLedger(tmp_path/"l.db")
 with pytest.raises(LedgerError,match="UNAUTHORIZED"):
  l.admit(principal="",request_id="r",operation="op",payload={})
