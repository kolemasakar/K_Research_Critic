from __future__ import annotations

from datetime import date
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from models import ReliabilityClass, SourceType


class ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SearchHit(ToolModel):
    url: str
    title: str = Field(min_length=1)
    publisher: str | None = None
    snippet: str | None = None
    publication_date: date | None = None
    source_type: SourceType = SourceType.OTHER
    reliability_class: ReliabilityClass = ReliabilityClass.C
    primary_source: bool = False
    independence_group: str | None = None


class FetchedDocument(SearchHit):
    content: str = ""


class ResearchTools(Protocol):
    """Provider-neutral tool boundary consumed by ResearchAgent."""

    def web_search(self, query: str, *, limit: int) -> list[SearchHit]:
        ...

    def web_fetch(self, url: str) -> FetchedDocument:
        ...
