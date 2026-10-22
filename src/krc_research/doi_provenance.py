"""KRC P0.3: offline, fail-closed DOI and evidence metadata validation."""
import re
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import unquote

DOI_PATTERN = re.compile(r'^10\.\d{4,9}/\S+$', re.I)

def normalize_doi(raw: str) -> str:
    if not isinstance(raw, str): raise ValueError('DOI must be a string')
    value = re.sub(r'(?i)^doi:\s*', '', raw.strip())
    value = re.sub(r'(?i)^https?://(?:dx\.)?doi\.org/', '', value)
    value = unquote(value).strip().lower()
    if not DOI_PATTERN.fullmatch(value) or any(c.isspace() for c in value):
        raise ValueError('Invalid DOI syntax')
    return value

def extract_crossref(payload: Mapping) -> dict:
    if payload.get('status') != 'ok' or not isinstance(payload.get('message'), dict):
        raise ValueError('Invalid Crossref response')
    item = payload['message']
    title = item.get('title') or []
    if not item.get('DOI') or not title or not isinstance(title[0], str):
        raise ValueError('Missing DOI/title')
    return {'doi': normalize_doi(item['DOI']), 'title': title[0],
            'authors': [a.get('family', '') for a in item.get('author', [])],
            'venue': (item.get('container-title') or [''])[0],
            'year': _year(item.get('published') or item.get('published-print') or item.get('published-online')),
            'metadata_source': 'Crossref', 'access_status': 'METADATA_ONLY'}

def extract_datacite(payload: Mapping) -> dict:
    item = payload.get('data', {})
    attrs = item.get('attributes', {}) if isinstance(item, dict) else {}
    title = (attrs.get('titles') or [{}])[0].get('title')
    if not attrs.get('doi') or not title: raise ValueError('Invalid DataCite response')
    return {'doi': normalize_doi(attrs['doi']), 'title': title,
            'authors': [a.get('name','') for a in attrs.get('creators', [])],
            'venue': attrs.get('publisher') or '', 'year': attrs.get('publicationYear'),
            'metadata_source': 'DataCite', 'access_status': 'METADATA_ONLY'}

def _year(date_parts):
    try: return int(date_parts['date-parts'][0][0])
    except (TypeError, KeyError, IndexError, ValueError): return None

def deduplicate(works: list[dict]) -> tuple[dict, dict]:
    result, mapping = {}, {}
    for idx, work in enumerate(works):
        doi = normalize_doi(work['doi'])
        mapping[idx] = doi
        if doi in result:
            if result[doi].get('title', '').strip().casefold() != work.get('title', '').strip().casefold():
                raise ValueError('DOI metadata conflict: review required')
        else: result[doi] = dict(work, doi=doi)
    return result, mapping

@dataclass(frozen=True)
class ClaimEvidence:
    claim_id: str
    origin_id: str
    citation: str
    inspected: bool
    support: str

def audit_claim(claim_id: str, evidences: list[ClaimEvidence], required_independent: int) -> dict:
    if required_independent < 0: raise ValueError('required_independent must be nonnegative')
    accepted = [e for e in evidences if e.claim_id == claim_id and e.inspected and
                e.support == 'SUPPORTED' and e.origin_id and e.citation]
    origins = sorted({e.origin_id for e in accepted})
    achieved = len(origins)
    return {'claim_id': claim_id, 'required': required_independent,
            'achieved_independent': achieved, 'origins': origins,
            'status': 'PASS' if achieved >= required_independent else 'SHORTFALL'}
