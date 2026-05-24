import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Article:
    title: str
    url: str
    category: str
    date: str
    author: str
    read_time: str
    excerpt: Optional[str] = None
    body: Optional[str] = None


def fetch_articles(max_articles: int = 10) -> list[Article]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get("https://www.ota-news.com/", headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []

    for card in soup.select("article, [class*='post'], [class*='card'], [class*='article']"):
        title_el = card.find(["h1", "h2", "h3"])
        link_el = card.find("a", href=True)
        if not title_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        href = link_el["href"]
        if not href.startswith("http"):
            href = "https://www.ota-news.com" + href

        # Skip navigation/header links
        if len(title) < 10:
            continue

        # Category
        cat_el = card.find(class_=re.compile(r"categ|label|tag", re.I))
        category = cat_el.get_text(strip=True) if cat_el else "General"

        # Date — try <time> tag first, then class-based, then text pattern
        date_el = card.find("time")
        if date_el:
            date = date_el.get("datetime", "") or date_el.get_text(strip=True)
        else:
            date_el = card.find(class_=re.compile(r"date|publish|time", re.I))
            if date_el:
                date = date_el.get_text(strip=True)
            else:
                # Fallback: scan all text for date patterns like "May 18, 2026"
                text_content = card.get_text(" ", strip=True)
                m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}", text_content)
                date = m.group(0) if m else ""

        # Author
        author_el = card.find(class_=re.compile(r"author|byline", re.I))
        author = author_el.get_text(strip=True) if author_el else ""

        # Read time
        read_el = card.find(string=re.compile(r"min read", re.I))
        read_time = read_el.strip() if read_el else ""

        # Excerpt
        p_el = card.find("p")
        excerpt = p_el.get_text(strip=True) if p_el else ""

        articles.append(Article(
            title=title,
            url=href,
            category=category,
            date=date,
            author=author,
            read_time=read_time,
            excerpt=excerpt,
        ))

        if len(articles) >= max_articles:
            break

    return articles


def fetch_article_body(url: str) -> tuple[str, str]:
    """Returns (body_text, date_string)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract date from article page
        date = ""
        time_el = soup.find("time")
        if time_el:
            date = time_el.get("datetime", "") or time_el.get_text(strip=True)
        if not date:
            date_el = soup.find(class_=re.compile(r"date|publish|posted", re.I))
            if date_el:
                date = date_el.get_text(strip=True)
        if not date:
            text_all = soup.get_text(" ", strip=True)
            m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}", text_all)
            date = m.group(0) if m else ""

        # Remove nav, footer, sidebar
        for el in soup.select("nav, footer, aside, [class*='sidebar'], [class*='related'], script, style"):
            el.decompose()

        # Try to find main article body
        body_el = soup.find(["article", "main"])
        if not body_el:
            body_el = soup.find(class_=re.compile(r"content|body|post", re.I))
        if not body_el:
            body_el = soup

        text = body_el.get_text(separator="\n", strip=True)
        return text[:3000], date
    except Exception:
        return "", ""
