from datetime import date, datetime, timezone

import pytest

from models import (
    Claim,
    ClaimType,
    IdPrefix,
    ImportanceLevel,
    ReliabilityClass,
    Source,
    SourceType,
    VerificationStatus,
    generate_id,
)
from tools import (
    CitationManager,
    EvidenceLinker,
    EvidenceToolkit,
    FetchedDocument,
    SourceDeduplicator,
    SourceMetadataExtractor,
    SourceReliabilityClassifier,
    SourceValidator,
    normalize_url,
)


def make_source(task_id: str, *, url: str, reliability: ReliabilityClass) -> Source:
    return Source(
        task_id=task_id,
        url=url,
        title="Source",
        publisher="Publisher",
        accessed_at=datetime(2026, 8, 12, tzinfo=timezone.utc),
        source_type=SourceType.NEWS,
        reliability_class=reliability,
    )


def test_normalize_url_removes_tracking_fragment_and_sorts_query() -> None:
    url = "HTTPS://Example.COM/path?utm_source=x&b=2&a=1#section"
    assert normalize_url(url) == "https://example.com/path?a=1&b=2"


def test_metadata_extractor_classifies_official_source_and_preserves_dates() -> None:
    task_id = generate_id(IdPrefix.TASK)
    document = FetchedDocument(
        url="https://example.test/official",
        title="Official bulletin",
        publisher="Agency",
        author="Office",
        publication_date=date(2026, 8, 1),
        source_type=SourceType.OFFICIAL,
        content="Evidence",
    )
    accessed_at = datetime(2026, 8, 12, tzinfo=timezone.utc)

    source = SourceMetadataExtractor().to_source(task_id, document, accessed_at=accessed_at)

    assert source.reliability_class == ReliabilityClass.A
    assert source.publication_date == date(2026, 8, 1)
    assert source.accessed_at == accessed_at
    assert source.author == "Office"


def test_reliability_classifier_supports_explicit_profile_driven_override() -> None:
    classifier = SourceReliabilityClassifier()
    result = classifier.classify(
        SourceType.NEWS,
        overrides={SourceType.NEWS: ReliabilityClass.B},
    )
    assert result == ReliabilityClass.B


def test_source_deduplicator_merges_tracking_variants_and_keeps_stronger_metadata() -> None:
    task_id = generate_id(IdPrefix.TASK)
    first = make_source(
        task_id,
        url="https://example.test/report?utm_source=newsletter&id=7",
        reliability=ReliabilityClass.C,
    )
    second = make_source(
        task_id,
        url="https://example.test/report?id=7#details",
        reliability=ReliabilityClass.A,
    )
    second.primary_source = True
    second.author = "Author"

    merged = SourceDeduplicator().deduplicate([first, second])

    assert len(merged) == 1
    assert merged[0].reliability_class == ReliabilityClass.A
    assert merged[0].primary_source is True
    assert merged[0].author == "Author"


def test_evidence_linker_creates_bidirectional_links_and_rejects_task_mismatch() -> None:
    task_id = generate_id(IdPrefix.TASK)
    run_id = generate_id(IdPrefix.RUN)
    source = make_source(task_id, url="https://example.test/source", reliability=ReliabilityClass.B)
    claim = Claim(
        task_id=task_id,
        text="Linked claim",
        claim_type=ClaimType.FACT,
        importance=ImportanceLevel.HIGH,
        source_ids=[],
        confidence=0.8,
        verification_status=VerificationStatus.UNVERIFIED,
        created_by_run_id=run_id,
    )

    EvidenceLinker().link(claim, [source])

    assert claim.source_ids == [source.source_id]
    assert source.supports_claim_ids == [claim.claim_id]

    other = make_source(
        generate_id(IdPrefix.TASK),
        url="https://example.test/other",
        reliability=ReliabilityClass.B,
    )
    with pytest.raises(ValueError):
        EvidenceLinker().link(claim, [other])


def test_citation_manager_validates_claim_references_and_builds_bibliography() -> None:
    task_id = generate_id(IdPrefix.TASK)
    run_id = generate_id(IdPrefix.RUN)
    source = make_source(task_id, url="https://example.test/source", reliability=ReliabilityClass.A)
    claim = Claim(
        task_id=task_id,
        text="Claim",
        claim_type=ClaimType.FACT,
        importance=ImportanceLevel.MEDIUM,
        source_ids=[source.source_id],
        confidence=0.9,
        verification_status=VerificationStatus.UNVERIFIED,
        created_by_run_id=run_id,
    )
    manager = CitationManager()

    assert manager.cite_claim(claim, {source.source_id: source}) == f"[{source.source_id}]"
    assert f"[{source.source_id}] Source" in manager.bibliography([source])

    with pytest.raises(ValueError):
        manager.cite_claim(claim, {})


def test_source_validator_detects_invalid_url_and_future_publication_date() -> None:
    task_id = generate_id(IdPrefix.TASK)
    source = Source(
        task_id=task_id,
        url="ftp://example.test/file",
        title="Invalid web source",
        publication_date=date(2026, 8, 13),
        accessed_at=datetime(2026, 8, 12, tzinfo=timezone.utc),
        source_type=SourceType.OTHER,
        reliability_class=ReliabilityClass.D,
    )

    result = SourceValidator().validate(source)

    assert result.valid is False
    assert "invalid_web_url" in result.issues
    assert "publication_date_after_access_date" in result.issues


def test_evidence_toolkit_deduplicates_search_hits_by_normalized_url() -> None:
    toolkit = EvidenceToolkit()
    hits = [
        FetchedDocument(url="https://example.test/a?utm_medium=x", title="A"),
        FetchedDocument(url="https://example.test/a#fragment", title="A copy"),
    ]

    assert len(toolkit.deduplicate_hits(hits)) == 1
