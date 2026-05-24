import os
import sys
from pathlib import Path

from scraper import fetch_articles, fetch_article_body
from summarizer import summarize_articles
from generator import generate_html


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)

    print("1/4 記事一覧を取得中...")
    articles = fetch_articles(max_articles=10)
    print(f"    {len(articles)} 件取得")

    print("2/4 各記事の本文を取得中...")
    for i, article in enumerate(articles):
        print(f"    [{i+1}/{len(articles)}] {article.title[:50]}...")
        article.body = fetch_article_body(article.url)

    print("3/4 Claude API で日本語要約中...")
    articles = summarize_articles(articles, api_key)

    print("4/4 HTML を生成中...")
    html = generate_html(articles, api_key)

    out_path = Path(__file__).parent / "docs" / "index.html"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"    保存完了: {out_path}")
    print("完了!")


if __name__ == "__main__":
    main()
