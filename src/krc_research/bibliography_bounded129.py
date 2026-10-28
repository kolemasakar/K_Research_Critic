"""Bounded bibliography metadata adapter for an explicitly approved staging backend.

This adapter does NOT assert scientific evidence or retraction clearance.
A host-provided callback must enforce outbound policy; no network is opened here.
"""
import json,time
from .bibliography_audit import audit_bibliography
from .doi_provenance import normalize_doi

class BibliographyUnavailable(RuntimeError):pass

class BoundedBibliography129:
    def __init__(self, *, crossref_fetch, europepmc_fetch, updates_fetch,
                 min_interval=1.0, clock=None, sleeper=None, metadata_store=None):
        if not all(callable(x) for x in (crossref_fetch,europepmc_fetch,updates_fetch)):
            raise ValueError("PROVIDERS_NOT_CONFIGURED")
        if not 0<=min_interval<=60:raise ValueError("INVALID_RATE")
        self.transports=(crossref_fetch,europepmc_fetch,updates_fetch)
        self.interval=min_interval
        self.clock=clock or time.monotonic
        self.sleep=sleeper or time.sleep
        self.next_slot=0.0
        self.store=metadata_store
    def _bounded(self,fn,provider):
        def invoke(url):
            if self.store is not None:
                cached=self.store.load(provider,url)
                if cached is not None:return cached
            now=self.clock()
            if now<self.next_slot:self.sleep(self.next_slot-now)
            self.next_slot=self.clock()+self.interval
            try:result=fn(url)
            except Exception:
                if self.store is not None:self.store.error(provider,url)
                raise
            if not isinstance(result,dict):raise BibliographyUnavailable("INVALID_PROVIDER_RESPONSE")
            if len(json.dumps(result,ensure_ascii=False).encode("utf-8"))>2_000_000:
                raise BibliographyUnavailable("OVERSIZED_METADATA")
            if self.store is not None:self.store.put(provider,url,result)
            return result
        return invoke
    def __call__(self,dois):
        if not isinstance(dois,list) or not 1<=len(dois)<=24:
            raise ValueError("INVALID_DOI_BATCH")
        normalized=[normalize_doi(d) for d in dois]
        if len(set(normalized))!=len(normalized):raise ValueError("DUPLICATE_DOI")
        # cache only for same adapter lifetime; no persistent personal data.
        result=audit_bibliography(normalized,
            crossref_fetch=self._bounded(self.transports[0],'crossref'),
            europepmc_fetch=self._bounded(self.transports[1],'europepmc'),
            updates_fetch=self._bounded(self.transports[2],'editorial_updates'))
        result["evidence_level"]="METADATA_ONLY"
        result["scientific_approval"]=False
        return result
