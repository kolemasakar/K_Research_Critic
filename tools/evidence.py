from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, Field

from models import Claim, ReliabilityClass, Source, SourceType, utc_now

from .citations import CitationManager
from .interfaces import FetchedDocument, SearchHit

_TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
_RELIABILITY_RANK = {
    ReliabilityClass.A: 0,
    ReliabilityClass.B: 1,
    ReliabilityClass.C: 2,
    ReliabilityClass.D: 3,
}


def normalize_url(url: str) -> str:
    """Return a deterministic URL key for source deduplication."""

    raw = url.strip()
    if not raw:
        return raw
    parsed = urlsplit(raw)
    if not parsed.scheme or not parsed.netloc:
        return raw

    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()
    port = parsed.port
    if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname

    if parsed.username:
        credentials = parsed.username
        if parsed.password:
            credentials += f":{parsed.password}"
        netloc = f"{credentials}@{netloc}"

    query_items = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower.startswith("utm_") or key_lower in _TRACKING_KEYS:
            continue
        query_items.append((key, value))
    query_items.sort()
    query = urlencode(query_items, doseq=True)
    path = parsed.path or "/"
    return urlunsplit((scheme, netloc, path, query, ""))


class SourceReliabilityClassifier:
    """Context-neutral baseline classification with explicit override support."""

    DEFAULTS: dict[SourceType, ReliabilityClass] = {
        SourceType.OFFICIAL: ReliabilityClass.A,
        SourceType.PRIMARY_DOCUMENT: ReliabilityClass.A,
        SourceType.STANDARD: ReliabilityClass.A,
        SourceType.GOVERNMENT: ReliabilityClass.A,
        SourceType.PEER_REVIEWED: ReliabilityClass.B,
        SourceType.ACADEMIC: ReliabilityClass.B,
        SourceType.MANUFACTURER: ReliabilityClass.B,
        SourceType.PROFESSIONAL_PUBLICATION: ReliabilityClass.B,
        SourceType.NEWS: ReliabilityClass.C,
        SourceType.REFERENCE: ReliabilityClass.C,
        SourceType.USER_PROVIDED: ReliabilityClass.C,
        SourceType.OTHER: ReliabilityClass.D,
    }

    def classify(
        self,
        source_type: SourceType,
        *,
        primary_source: bool = False,
        declared: ReliabilityClass | None = None,
        overrides: Mapping[SourceType | str, ReliabilityClass | str] | None = None,
    ) -> ReliabilityClass:
        override = self._lookup_override(source_type, overrides)
        if override is not None:
            return override
        if primary_source:
            return ReliabilityClass.A
        if declared is not None:
            return declared
        return self.DEFAULTS[source_type]

    @staticmethod
    def _lookup_override(
        source_type: SourceType,
        overrides: Mapping[SourceType | str, ReliabilityClass | str] | None,
    ) -> ReliabilityClass | None:
        if not overrides:
            return None
        for key in (source_type, source_type.value):
            if key in overrides:
                value = overrides[key]
                return value if isinstance(value, ReliabilityClass) else ReliabilityClass(value)
        return None


class SourceMetadataExtractor:
    """Convert provider-neutral search/fetch metadata into the canonical Source model."""

    def __init__(self, classifier: SourceReliabilityClassifier | None = None) -> None:
        self.classifier = classifier or SourceReliabilityClassifier()

    def to_source(
        self,
        task_id: str,
        document: SearchHit | FetchedDocument,
        *,
        accessed_at: datetime | None = None,
        reliability_overrides: Mapping[SourceType | str, ReliabilityClass | str] | None = None,
    ) -> Source:
        reliability = self.classifier.classify(
            document.source_type,
            primary_source=document.primary_source,
            declared=document.reliability_class,
            overrides=reliability_overrides,
        )
        return Source(
            task_id=task_id,
            url=document.url,
            title=document.title,
            publisher=document.publisher,
            author=document.author,
            publication_date=document.publication_date,
            accessed_at=accessed_at or utc_now(),
            source_type=document.source_type,
            reliability_class=reliability,
            primary_source=document.primary_source,
            independence_group=document.independence_group,
            notes=document.snippet,
        )


class SourceValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    valid: bool
    issues: list[str] = Field(default_factory=list)


class SourceValidator:
    """Perform deterministic structural checks that are independent of source content."""

    def validate(self, source: Source) -> SourceValidationResult:
        issues: list[str] = []
        if source.url:
            parsed = urlsplit(source.url)
            if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
                issues.append("invalid_web_url")
            if source.accessed_at is None:
                issues.append("missing_access_time")
        if source.publication_date and source.accessed_at:
            if source.publication_date > source.accessed_at.date():
                issues.append("publication_date_after_access_date")
        return SourceValidationResult(valid=not issues, issues=issues)


class SourceDeduplicator:
    """Normalize duplicate source records while preserving the strongest metadata."""

    def deduplicate(self, sources: Iterable[Source]) -> list[Source]:
        merged: dict[str, Source] = {}
        order: list[str] = []
        for source in sources:
            key = self._key(source)
            if key not in merged:
                merged[key] = source.model_copy(deep=True)
                order.append(key)
                continue
            merged[key] = self._merge(merged[key], source)
        return [merged[key] for key in order]

    @staticmethod
    def _key(source: Source) -> str:
        if source.url:
            return f"url:{normalize_url(source.url)}"
        publisher = (source.publisher or "").casefold()
        publication_date = source.publication_date.isoformat() if source.publication_date else ""
        return f"local:{source.title.casefold()}|{publisher}|{publication_date}"

    @staticmethod
    def _merge(current: Source, incoming: Source) -> Source:
        if current.task_id != incoming.task_id:
            raise ValueError("Cannot deduplicate sources from different tasks")
        result = current.model_copy(deep=True)
        for field in ("publisher", "author", "publication_date", "accessed_at", "independence_group", "notes"):
            if getattr(result, field) is None and getattr(incoming, field) is not None:
                setattr(result, field, getattr(incoming, field))
        if _RELIABILITY_RANK[incoming.reliability_class] < _RELIABILITY_RANK[result.reliability_class]:
            result.reliability_class = incoming.reliability_class
        result.primary_source = result.primary_source or incoming.primary_source
        result.supports_claim_ids = list(
            dict.fromkeys([*result.supports_claim_ids, *incoming.supports_claim_ids])
        )
        result.contradicts_claim_ids = list(
            dict.fromkeys([*result.contradicts_claim_ids, *incoming.contradicts_claim_ids])
        )
        return result


class EvidenceLinker:
    """Maintain bidirectional Claim-to-Source links."""

    def link(self, claim: Claim, sources: Iterable[Source]) -> tuple[Claim, list[Source]]:
        linked_sources = list(sources)
        if any(source.task_id != claim.task_id for source in linked_sources):
            raise ValueError("Claim and Source task_id values must match")
        claim.source_ids = list(
            dict.fromkeys([*claim.source_ids, *(source.source_id for source in linked_sources)])
        )
        for source in linked_sources:
            source.supports_claim_ids = list(
                dict.fromkeys([*source.supports_claim_ids, claim.claim_id])
            )
        return claim, linked_sources


class EvidenceToolkit:
    """Facade used by agents for Phase 5 evidence normalization operations."""

    def __init__(
        self,
        *,
        reliability_overrides: Mapping[SourceType | str, ReliabilityClass | str] | None = None,
    ) -> None:
        self.classifier = SourceReliabilityClassifier()
        self.metadata = SourceMetadataExtractor(self.classifier)
        self.validator = SourceValidator()
        self.deduplicator = SourceDeduplicator()
        self.linker = EvidenceLinker()
        self.citations = CitationManager()
        self.reliability_overrides = reliability_overrides or {}

    def deduplicate_hits(self, hits: Iterable[SearchHit]) -> list[SearchHit]:
        result: list[SearchHit] = []
        seen: set[str] = set()
        for hit in hits:
            key = normalize_url(hit.url)
            if key in seen:
                continue
            seen.add(key)
            result.append(hit)
        return result

    def source_from_document(self, task_id: str, document: FetchedDocument) -> Source:
        return self.metadata.to_source(
            task_id,
            document,
            reliability_overrides=self.reliability_overrides,
        )

    @staticmethod
    def confidence_for(reliability: ReliabilityClass) -> float:
        return {
            ReliabilityClass.A: 0.90,
            ReliabilityClass.B: 0.80,
            ReliabilityClass.C: 0.65,
            ReliabilityClass.D: 0.40,
        }[reliability]
