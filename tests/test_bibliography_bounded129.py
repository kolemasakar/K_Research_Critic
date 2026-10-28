import unittest
from krc_research.bibliography_bounded129 import BoundedBibliography129

def provider(_):return {"status":"ok","message":{"DOI":"10.1000/test","title":["test"],"items":[]}}
class Tests(unittest.TestCase):
 def test_no_providers(self):
  with self.assertRaises(ValueError):BoundedBibliography129(crossref_fetch=None,europepmc_fetch=provider,updates_fetch=provider)
 def test_invalid_batch(self):
  b=BoundedBibliography129(crossref_fetch=provider,europepmc_fetch=provider,updates_fetch=provider,min_interval=0)
  with self.assertRaises(ValueError):b([])
 def test_duplicate_doi(self):
  b=BoundedBibliography129(crossref_fetch=provider,europepmc_fetch=provider,updates_fetch=provider,min_interval=0)
  with self.assertRaises(ValueError):b(["10.1000/test","10.1000/test"])
 def test_metadata_never_scientific_approval(self):
  b=BoundedBibliography129(crossref_fetch=provider,europepmc_fetch=provider,updates_fetch=provider,min_interval=0)
  r=b(["10.1000/test"])
  self.assertEqual(r["evidence_level"],"METADATA_ONLY")
  self.assertFalse(r["scientific_approval"])
if __name__=="__main__":unittest.main()
