from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .evidence import normalize_url
from .interfaces import FetchedDocument, SearchHit


class JsonCorpusProvider:
    """Deterministic local search/fetch provider for the Phase 9 runnable MVP and tests."""

    def __init__(self, documents: list[FetchedDocument]) -> None:
        if not documents:
            raise ValueError("JsonCorpusProvider requires at least one document")
        self._documents = list(documents)
        self._by_url: dict[str, FetchedDocument] = {}
        for document in self._documents:
            key = normalize_url(document.url)
            if key in self._by_url:
                raise ValueError(f"Duplicate corpus URL: {document.url}")
            self._by_url[key] = document

    @classmethod
    def from_file(cls, path: str | Path) -> "JsonCorpusProvider":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw_documents = raw.get("documents")
        else:
            raw_documents = raw
        if not isinstance(raw_documents, list):
            raise ValueError("Corpus JSON must be a list or an object with a documents list")
        documents = [FetchedDocument.model_validate(item) for item in raw_documents]
        return cls(documents)

    def search(self, query: str, *, limit: int) -> list[SearchHit]:
        if limit <= 0:
            return []
        query_tokens = self._tokens(query)
        scored: list[tuple[int, int, FetchedDocument]] = []
        for index, document in enumerate(self._documents):
            haystack = " ".join(
                part
                for part in (
                    document.title,
                    document.publisher or "",
                    document.snippet or "",
                    document.content or "",
                )
                if part
            )
            score = len(query_tokens & self._tokens(haystack))
            scored.append((score, index, document))

        matching = [item for item in scored if item[0] > 0]
        ranked = matching if matching else scored
        ranked.sort(key=lambda item: (-item[0], item[1]))
        return [self._to_hit(item[2]) for item in ranked[:limit]]

    def fetch(self, url: str) -> FetchedDocument:
        key = normalize_url(url)
        try:
            return self._by_url[key].model_copy(deep=True)
        except KeyError as exc:
            raise KeyError(f"URL not found in corpus: {url}") from exc

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token.casefold()
            for token in re.findall(r"[\w-]+", text, flags=re.UNICODE)
            if len(token) >= 3
        }

    @staticmethod
    def _to_hit(document: FetchedDocument) -> SearchHit:
        values: dict[str, Any] = document.model_dump(exclude={"content"})
        return SearchHit.model_validate(values)
