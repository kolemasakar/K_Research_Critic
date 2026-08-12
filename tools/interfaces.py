from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

from models import ReliabilityClass, SourceType


class ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SearchHit(ToolModel):
    url: str
    title: str = Field(min_length=1)
    publisher: str | None = None
    author: str | None = None
    snippet: str | None = None
    publication_date: date | None = None
    source_type: SourceType = SourceType.OTHER
    reliability_class: ReliabilityClass | None = None
    primary_source: bool = False
    independence_group: str | None = None


class FetchedDocument(SearchHit):
    content: str = ""


class WebSearchProvider(Protocol):
    """Raw provider contract wrapped by WebSearchTool."""

    def search(self, query: str, *, limit: int) -> Sequence[SearchHit | Mapping[str, Any]]:
        ...


class WebFetchProvider(Protocol):
    """Raw provider contract wrapped by WebFetchTool."""

    def fetch(self, url: str) -> FetchedDocument | Mapping[str, Any]:
        ...


class ResearchTools(Protocol):
    """Provider-neutral tool boundary consumed by ResearchAgent."""

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        ...

    def web_fetch(self, url: str) -> FetchedDocument:
        ...
