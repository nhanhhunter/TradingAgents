"""Vietnam-focused news collection for Vietnamese tickers and macro context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import unescape
import re
from typing import Iterable, Optional
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import requests

from .config import get_config
from .vietnam_symbols import to_vnstock_symbol


@dataclass(frozen=True)
class VietnamNewsArticle:
    title: str
    source: str
    link: str
    published_at: Optional[datetime]
    summary: str = ""


def _parse_date(value: str | None) -> Optional[datetime]:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).replace(tzinfo=None)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value[:19], fmt)
        except ValueError:
            continue
    return None


def _strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(text)).strip()


def _dedupe_articles(articles: Iterable[VietnamNewsArticle]) -> list[VietnamNewsArticle]:
    seen: set[str] = set()
    result: list[VietnamNewsArticle] = []
    for article in articles:
        key = article.link.strip().lower() if article.link else article.title.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(article)
    return result


def _filter_articles(
    articles: Iterable[VietnamNewsArticle],
    start_date: str,
    end_date: str,
    limit: int,
) -> list[VietnamNewsArticle]:
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    in_range = [
        article
        for article in articles
        if article.published_at is None or start_dt <= article.published_at <= end_dt.replace(hour=23, minute=59, second=59)
    ]
    in_range.sort(key=lambda item: item.published_at or datetime.min, reverse=True)
    return in_range[:limit]


def _format_articles(
    label: str,
    start_date: str,
    end_date: str,
    articles: list[VietnamNewsArticle],
) -> str:
    if not articles:
        return f"No Vietnam news found for {label} between {start_date} and {end_date}"
    body = ""
    for article in articles:
        body += f"### {article.title} (source: {article.source})\n"
        if article.summary:
            body += f"{article.summary}\n"
        if article.link:
            body += f"Link: {article.link}\n"
        body += "\n"
    return f"## {label} Vietnam News, from {start_date} to {end_date}:\n\n{body}"


def _fetch_rss(url: str, source: str) -> list[VietnamNewsArticle]:
    response = requests.get(
        url,
        timeout=10,
        headers={"User-Agent": "TradingAgents/0.2.5 (+https://github.com/TauricResearch/TradingAgents)"},
    )
    response.raise_for_status()
    root = ET.fromstring(response.content)
    articles: list[VietnamNewsArticle] = []
    for item in root.findall(".//item"):
        title = _strip_html(item.findtext("title") or "")
        link = (item.findtext("link") or "").strip()
        summary = _strip_html(item.findtext("description") or "")
        published_at = _parse_date(item.findtext("pubDate") or item.findtext("published"))
        if title:
            articles.append(VietnamNewsArticle(title, source, link, published_at, summary))
    return articles


def _google_news_rss(query: str) -> str:
    return (
        "https://news.google.com/rss/search?q="
        f"{quote_plus(query)}&hl=vi&gl=VN&ceid=VN:vi"
    )


def _vietnam_queries(ticker: str | None = None) -> list[str]:
    if ticker:
        symbol = to_vnstock_symbol(ticker)
        return [
            f"{symbol} cổ phiếu",
            f"{symbol} chứng khoán",
            f"{symbol} cafef OR vietstock OR vneconomy",
        ]
    return [
        "thị trường chứng khoán Việt Nam VNINDEX",
        "kinh tế vĩ mô Việt Nam lãi suất tỷ giá chứng khoán",
        "VNINDEX Vietstock CafeF VnEconomy",
    ]


def _source_search_queries(ticker: str | None) -> list[tuple[str, str]]:
    queries = []
    for query in _vietnam_queries(ticker):
        queries.append(("Google News RSS", _google_news_rss(query)))
    for domain in (
        "cafef.vn",
        "vneconomy.vn",
        "vietstock.vn",
        "tinnhanhchungkhoan.vn",
        "vietnambiz.vn/chung-khoan.htm",
        "vn.investing.com",
    ):
        scoped = _vietnam_queries(ticker)[0] + f" site:{domain}"
        queries.append((domain, _google_news_rss(scoped)))
    return queries


def _collect_articles(ticker: str | None = None) -> list[VietnamNewsArticle]:
    articles: list[VietnamNewsArticle] = []
    for source, url in _source_search_queries(ticker):
        try:
            articles.extend(_fetch_rss(url, source))
        except Exception:
            continue
    return _dedupe_articles(articles)


def get_news_vietnam(ticker: str, start_date: str, end_date: str) -> str:
    limit = get_config()["news_article_limit"]
    articles = _filter_articles(_collect_articles(ticker), start_date, end_date, limit)
    return _format_articles(ticker.upper(), start_date, end_date, articles)


def get_global_news_vietnam(
    curr_date: str,
    look_back_days: Optional[int] = None,
    limit: Optional[int] = None,
) -> str:
    from dateutil.relativedelta import relativedelta

    config = get_config()
    if look_back_days is None:
        look_back_days = config["global_news_lookback_days"]
    if limit is None:
        limit = config["global_news_article_limit"]

    curr_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    start_date = (curr_dt - relativedelta(days=look_back_days)).strftime("%Y-%m-%d")
    articles = _filter_articles(_collect_articles(None), start_date, curr_date, limit)
    return _format_articles("Vietnam Market", start_date, curr_date, articles)
