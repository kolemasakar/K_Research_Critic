import pytest

from tools import (
    FetchedDocument,
    ResearchToolset,
    SearchHit,
    ToolExecutionError,
    WebFetchTool,
    WebSearchTool,
)


class FakeSearchProvider:
    def __init__(self, results=None, error=None):
        self.results = results or []
        self.error = error
        self.calls = []

    def search(self, query: str, *, limit: int):
        self.calls.append((query, limit))
        if self.error:
            raise self.error
        return self.results


class FakeFetchProvider:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def fetch(self, url: str):
        self.calls.append(url)
        if self.error:
            raise self.error
        return self.result


def test_web_search_tool_normalizes_mapping_results() -> None:
    provider = FakeSearchProvider(
        results=[{"url": "https://example.test/a", "title": "A"}]
    )
    tool = WebSearchTool(provider)

    results = tool.web_search(" topic ", limit=3)

    assert results == [SearchHit(url="https://example.test/a", title="A")]
    assert provider.calls == [("topic", 3)]


def test_web_search_tool_normalizes_provider_failure() -> None:
    tool = WebSearchTool(FakeSearchProvider(error=RuntimeError("provider down")))

    with pytest.raises(ToolExecutionError) as exc_info:
        tool.web_search("topic", limit=3)

    assert exc_info.value.code == "SEARCH_PROVIDER_ERROR"
    assert exc_info.value.operation == "web_search"
    assert exc_info.value.retryable is True


def test_web_search_tool_rejects_invalid_provider_result() -> None:
    tool = WebSearchTool(FakeSearchProvider(results=[{"url": "https://example.test/a"}]))

    with pytest.raises(ToolExecutionError) as exc_info:
        tool.web_search("topic", limit=3)

    assert exc_info.value.code == "INVALID_SEARCH_RESULT"
    assert exc_info.value.retryable is False


def test_web_fetch_tool_normalizes_mapping_result() -> None:
    provider = FakeFetchProvider(
        result={
            "url": "https://example.test/a",
            "title": "A",
            "content": "Fetched evidence",
        }
    )
    tool = WebFetchTool(provider)

    document = tool.web_fetch(" https://example.test/a ")

    assert document == FetchedDocument(
        url="https://example.test/a",
        title="A",
        content="Fetched evidence",
    )
    assert provider.calls == ["https://example.test/a"]


def test_research_toolset_composes_search_and_fetch_adapters() -> None:
    search_provider = FakeSearchProvider(
        results=[{"url": "https://example.test/a", "title": "A"}]
    )
    fetch_provider = FakeFetchProvider(
        result={"url": "https://example.test/a", "title": "A", "content": "Evidence"}
    )
    tools = ResearchToolset(WebSearchTool(search_provider), WebFetchTool(fetch_provider))

    hits = tools.web_search("topic", limit=1)
    document = tools.web_fetch(hits[0].url)

    assert len(hits) == 1
    assert document.content == "Evidence"
