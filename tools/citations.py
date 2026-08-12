from __future__ import annotations

from collections.abc import Iterable, Mapping

from models import Claim, Source


class CitationManager:
    """Create stable source-id citations without embedding provider-specific syntax."""

    @staticmethod
    def source_token(source_id: str) -> str:
        return f"[{source_id}]"

    def cite_claim(self, claim: Claim, sources: Mapping[str, Source]) -> str:
        missing = [source_id for source_id in claim.source_ids if source_id not in sources]
        if missing:
            raise ValueError(f"Claim references unknown source_ids: {missing}")
        return " ".join(self.source_token(source_id) for source_id in claim.source_ids)

    def bibliography(self, sources: Iterable[Source]) -> str:
        lines: list[str] = []
        seen: set[str] = set()
        for source in sources:
            if source.source_id in seen:
                continue
            seen.add(source.source_id)
            publisher = f"; {source.publisher}" if source.publisher else ""
            publication_date = (
                f"; {source.publication_date.isoformat()}" if source.publication_date else ""
            )
            location = source.url or "local source"
            lines.append(
                f"- {self.source_token(source.source_id)} {source.title}{publisher}{publication_date}; {location}"
            )
        return "\n".join(lines)
