import hashlib
import pytest
from krc_research.artifact_exchange import ExchangeError
from krc_research.artifact_stream116 import StreamExchange

def test_stream_roundtrip(tmp_path):
 s=StreamExchange(tmp_path/'store')
 v=s.store_stream(iter([b'a'*1000,b'b'*1000]),principal='trusted',request_id='r',filename='a.pdf')
 assert v['sha256']==hashlib.sha256(b'a'*1000+b'b'*1000).hexdigest()
 assert b''.join(s.read_stream(v['artifact_id'],principal='trusted',request_id='r',chunk_size=128))==b'a'*1000+b'b'*1000

def test_cross_principal(tmp_path):
 s=StreamExchange(tmp_path/'store')
 v=s.store_stream([b'x'],principal='p',request_id='r',filename='a')
 with pytest.raises(ExchangeError,match='NOT_FOUND'):
  list(s.read_stream(v['artifact_id'],principal='q',request_id='r'))

def test_file_limit_and_cleanup(tmp_path):
 s=StreamExchange(tmp_path/'store',max_artifact=5)
 with pytest.raises(ExchangeError,match='ARTIFACT_TOO_LARGE'):
  s.store_stream([b'123',b'456'],principal='p',request_id='r',filename='a')
 assert not list(s.data.iterdir())

def test_tamper_detected(tmp_path):
 s=StreamExchange(tmp_path/'store')
 v=s.store_stream([b'abc'],principal='p',request_id='r',filename='a')
 (s.data/v['artifact_id']).write_bytes(b'abd')
 with pytest.raises(ExchangeError,match='ARTIFACT_CORRUPTED'):
  list(s.read_stream(v['artifact_id'],principal='p',request_id='r'))

def test_concurrent_quota(tmp_path):
 from concurrent.futures import ThreadPoolExecutor
 s=StreamExchange(tmp_path/'store',max_artifact=9,max_total=12)
 def go(i):
  try:return s.store_stream([b'x'*8],principal='p',request_id=str(i),filename='a')['artifact_id']
  except ExchangeError as e:return e.code
 with ThreadPoolExecutor(max_workers=2) as ex:
  results=list(ex.map(go,range(2)))
 assert len([r for r in results if r!='STORAGE_QUOTA_EXCEEDED'])==1

def test_recover_pending(tmp_path):
 s=StreamExchange(tmp_path/'store')
 (s.data/'.pending-abc').write_bytes(b'junk')
 assert s.reconcile_staging()==1
 assert not list(s.data.iterdir())
