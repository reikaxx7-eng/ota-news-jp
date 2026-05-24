import anthropic
from scraper import Article


def summarize_articles(articles: list[Article], api_key: str) -> list[Article]:
    client = anthropic.Anthropic(api_key=api_key)

    for article in articles:
        source_text = article.body or article.excerpt or article.title

        prompt = f"""以下はOTA（Online Travel Agency）業界のニュース記事です。日本語で3〜5文の簡潔な要約を作成してください。

記事タイトル: {article.title}
カテゴリ: {article.category}
内容:
{source_text}

要約（箇条書き不要、自然な日本語の文章で）:"""

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        article.excerpt = response.content[0].text.strip()

    return articles


def translate_category(category: str, api_key: str) -> str:
    mapping = {
        "Tech Deep Dive": "技術解説",
        "Strategy": "戦略",
        "Market Pulse": "市場動向",
        "Travel Trends": "旅行トレンド",
        "General": "一般",
        "Analysis": "分析",
        "OTAs": "OTA",
    }
    return mapping.get(category, category)
