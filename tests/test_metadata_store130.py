import tempfile,unittest
from pathlib import Path
from krc_research.metadata_store130 import MetadataStore130
from krc_research.bibliography_bounded129 import BoundedBibliography129
class StoreTests(unittest.TestCase):
 def test_cache_persists(self):
  with tempfile.TemporaryDirectory() as d:
   p=str(Path(d)/"meta.sqlite"); s=MetadataStore130(p)
   s.put("crossref","https://api.crossref.org/works/10.1000%2Ftest",{"a":1})
   self.assertEqual(MetadataStore130(p).load("crossref","https://api.crossref.org/works/10.1000%2Ftest"),{"a":1})
 def test_expired(self):
  with tempfile.TemporaryDirectory() as d:
   now=[100.]
   s=MetadataStore130(str(Path(d)/"m.db"),ttl_seconds=60,clock=lambda:now[0])
   s.put("p","u",{"ok":True});now[0]=161
   self.assertIsNone(s.load("p","u"))
 def test_adapter_uses_cache(self):
  with tempfile.TemporaryDirectory() as d:
   n=[0]
   def f(url):
    n[0]+=1
    if "europepmc" in url:return {"resultList":{"result":[{"doi":"10.1000/test","title":"test"}]}}
    if "filter=" in url:return {"status":"ok","message":{"items":[]}}
    return {"status":"ok","message":{"DOI":"10.1000/test","title":["test"]}}
   s=MetadataStore130(str(Path(d)/"m.db"))
   b=BoundedBibliography129(crossref_fetch=f,europepmc_fetch=f,updates_fetch=f,min_interval=0,metadata_store=s)
   self.assertEqual(b(["10.1000/test"])["evidence_level"],"METADATA_ONLY")
   self.assertEqual(b(["10.1000/test"])["evidence_level"],"METADATA_ONLY")
   self.assertEqual(n[0],3)
 def test_rate_rejects_unauthorized(self):
  with self.assertRaises(ValueError):MetadataStore130("relative")
if __name__=="__main__":unittest.main()
