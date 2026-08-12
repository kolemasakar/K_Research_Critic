from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from .errors import ToolExecutionError
from .interfaces import FetchedDocument, SearchHit, WebFetchProvider, WebSearchProvider


class WebSearchTool:
    """Validate and normalize raw search-provider responses."""

    def __init__(self, provider: WebSearchProvider) -> None:
        self.provider = provider

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        normalized_query = query.strip()
        if not normalized_query:
            raise ToolExecutionError(
                "INVALID_SEARCH_QUERY",
                "web_search requires a non-empty query",
                operation="web_search",
                retryable=False,
            )
        if limit <= 0:
            raise ToolExecutionError(
                "INVALID_SEARCH_LIMIT",
                "web_search limit must be greater than zero",
                operation="web_search",
                retryable=False,
                details={"limit": limit},
            )

        try:
            raw_results = self.provider.search(normalized_query, limit=limit)
        except ToolExecutionError:
            raise
        except Exception as exc:
            raise ToolExecutionError(
                "SEARCH_PROVIDER_ERROR",
                str(exc) or "Search provider failed",
                operation="web_search",
                details={"query": normalized_query, "limit": limit},
            ) from exc

        results: list[SearchHit] = []
        for index, raw in enumerate(raw_results):
            try:
                if isinstance(raw, SearchHit):
                    hit = raw
                elif isinstance(raw, Mapping):
                    hit = SearchHit.model_validate(dict(raw))
                else:
                    raise TypeError(f"Unsupported search result type: {type(raw).__name__}")
            except (ValidationError, TypeError, ValueError) as exc:
                raise ToolExecutionError(
                    "INVALID_SEARCH_RESULT",
                    str(exc),
                    operation="web_search",
                    retryable=False,
                    details={"query": normalized_query, "index": index},
                ) from exc
            results.append(hit)
            if len(results) >= limit:
                break
        return results


class WebFetchTool:
    """Validate and normalize raw fetch-provider responses."""

    def __init__(self, provider: WebFetchProvider) -> None:
        self.provider = provider

    def web_fetch(self, url: str) -> FetchedDocument:
        normalized_url = url.strip()
        if not normalized_url:
            raise ToolExecutionError(
                "INVALID_FETCH_URL",
                "web_fetch requires a non-empty URL",
                operation="web_fetch",
                retryable=False,
            )

        try:
            raw = self.provider.fetch(normalized_url)
        except ToolExecutionError:
            raise
        except Exception as exc:
            raise ToolExecutionError(
                "FETCH_PROVIDER_ERROR",
                str(exc) or "Fetch provider failed",
                operation="web_fetch",
                details={"url": normalized_url},
            ) from exc

        try:
            if isinstance(raw, FetchedDocument):
                document = raw
            elif isinstance(raw, Mapping):
                document = FetchedDocument.model_validate(dict(raw))
            else:
                raise TypeError(f"Unsupported fetched document type: {type(raw).__name__}")
        except (ValidationError, TypeError, ValueError) as exc:
            raise ToolExecutionError(
                "INVALID_FETCH_RESULT",
                str(exc),
                operation="web_fetch",
                retryable=False,
                details={"url": normalized_url},
            ) from exc
        return document


class ResearchToolset:
    """Composite ResearchTools implementation built from normalized adapters."""

    def __init__(self, search: WebSearchTool, fetch: WebFetchTool) -> None:
        self.search = search
        self.fetch = fetch

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        return self.search.web_search(query, limit=limit)

    def web_fetch(self, url: str) -> FetchedDocument:
        return self.fetch.web_fetch(url)
