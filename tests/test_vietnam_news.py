from datetime import datetime

import pytest

from tradingagents.dataflows.vietnam_news import (
    VietnamNewsArticle,
    _dedupe_articles,
    _filter_articles,
    _format_articles,
)


@pytest.mark.unit
def test_dedupes_by_link_then_title():
    articles = [
        VietnamNewsArticle("VCB profit rises", "CafeF", "https://example.com/a", datetime(2026, 1, 2), "A"),
        VietnamNewsArticle("VCB profit rises", "CafeF", "https://example.com/a", datetime(2026, 1, 2), "B"),
        VietnamNewsArticle("VCB profit rises", "VnEconomy", "", datetime(2026, 1, 3), ""),
        VietnamNewsArticle("VCB profit rises", "Vietstock", "", datetime(2026, 1, 4), ""),
    ]

    deduped = _dedupe_articles(articles)

    assert len(deduped) == 2
    assert deduped[0].summary == "A"


@pytest.mark.unit
def test_filters_by_date_and_limit():
    articles = [
        VietnamNewsArticle("old", "CafeF", "1", datetime(2025, 12, 31), ""),
        VietnamNewsArticle("in range 1", "CafeF", "2", datetime(2026, 1, 2), ""),
        VietnamNewsArticle("in range 2", "CafeF", "3", datetime(2026, 1, 3), ""),
    ]

    filtered = _filter_articles(articles, "2026-01-01", "2026-01-03", limit=1)

    assert [article.title for article in filtered] == ["in range 2"]


@pytest.mark.unit
def test_formats_articles_like_news_tool_output():
    articles = [
        VietnamNewsArticle("Headline", "CafeF", "https://example.com", datetime(2026, 1, 2), "Summary"),
    ]

    formatted = _format_articles("VCB.VN", "2026-01-01", "2026-01-03", articles)

    assert formatted.startswith("## VCB.VN Vietnam News")
    assert "### Headline (source: CafeF)" in formatted
    assert "Summary" in formatted
    assert "Link: https://example.com" in formatted
