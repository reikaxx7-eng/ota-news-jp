from datetime import datetime, timezone, timedelta
from scraper import Article
from summarizer import translate_category

JST = timezone(timedelta(hours=9))


def generate_html(articles: list[Article], api_key: str = "") -> str:
    now = datetime.now(JST).strftime("%Y年%m月%d日 %H:%M JST")
    cards = ""

    for a in articles:
        cat_ja = translate_category(a.category, api_key)
        date_str = a.date or "日付不明"
        summary = a.excerpt or "（要約なし）"

        cards += f"""
        <article class="card">
          <div class="card-meta">
            <span class="category">{cat_ja}</span>
            <span class="date">{date_str}</span>
          </div>
          <h2 class="card-title">
            <a href="{a.url}" target="_blank" rel="noopener">{a.title}</a>
          </h2>
          <p class="summary">{summary}</p>
          <a class="read-more" href="{a.url}" target="_blank" rel="noopener">原文を読む →</a>
        </article>
"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OTA News 日本語まとめ</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif;
      background: #f5f6fa;
      color: #2c2c2c;
      line-height: 1.7;
    }}
    header {{
      background: linear-gradient(135deg, #1a3a5c 0%, #2563ab 100%);
      color: #fff;
      padding: 32px 20px 24px;
      text-align: center;
    }}
    header h1 {{ font-size: 1.8rem; letter-spacing: 0.05em; }}
    header p {{ font-size: 0.85rem; margin-top: 6px; opacity: 0.8; }}
    .update-time {{
      background: #e8f0fe;
      text-align: center;
      font-size: 0.8rem;
      color: #555;
      padding: 8px;
      border-bottom: 1px solid #d0daf0;
    }}
    main {{
      max-width: 860px;
      margin: 32px auto;
      padding: 0 16px;
      display: grid;
      gap: 20px;
    }}
    .card {{
      background: #fff;
      border-radius: 10px;
      padding: 22px 26px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.07);
      border-left: 4px solid #2563ab;
      transition: transform 0.15s, box-shadow 0.15s;
    }}
    .card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.11); }}
    .card-meta {{ display: flex; gap: 12px; align-items: center; margin-bottom: 10px; }}
    .category {{
      background: #2563ab;
      color: #fff;
      font-size: 0.72rem;
      padding: 3px 10px;
      border-radius: 20px;
      font-weight: 600;
      letter-spacing: 0.03em;
    }}
    .date {{ color: #888; font-size: 0.8rem; }}
    .card-title {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 10px; }}
    .card-title a {{ color: #1a3a5c; text-decoration: none; }}
    .card-title a:hover {{ text-decoration: underline; color: #2563ab; }}
    .summary {{ font-size: 0.92rem; color: #444; margin-bottom: 14px; }}
    .read-more {{ font-size: 0.82rem; color: #2563ab; text-decoration: none; font-weight: 600; }}
    .read-more:hover {{ text-decoration: underline; }}
    footer {{
      text-align: center;
      padding: 28px;
      font-size: 0.78rem;
      color: #aaa;
    }}
    footer a {{ color: #2563ab; text-decoration: none; }}
  </style>
</head>
<body>
  <header>
    <h1>OTA News 日本語まとめ</h1>
    <p>Online Travel Agency 業界の最新ニュースを日本語で</p>
  </header>
  <div class="update-time">最終更新: {now}</div>
  <main>
    {cards}
  </main>
  <footer>
    情報ソース: <a href="https://www.ota-news.com/" target="_blank">OTA News</a> &nbsp;|&nbsp;
    Claude AI による日本語要約
  </footer>
</body>
</html>"""
