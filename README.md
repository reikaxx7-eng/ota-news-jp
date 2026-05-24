# OTA News 日本語まとめサイト

OTA News (ota-news.com) の最新記事を Claude AI で日本語要約し、GitHub Pages で自動公開するツールです。

## 仕組み

```
ota-news.com をスクレイピング
    ↓
Claude API で日本語要約
    ↓
静的 HTML を生成 (docs/index.html)
    ↓
GitHub Actions が 6 時間ごとに自動実行
    ↓
GitHub Pages で公開
```

## セットアップ手順

### 1. GitHubリポジトリを作成

1. [github.com](https://github.com) にログイン
2. 右上「+」→「New repository」
3. Repository name: `ota-news-jp`
4. Public を選択（GitHub Pages 無料枠）
5. 「Create repository」

### 2. このフォルダをGitHubにプッシュ

```powershell
cd "C:\Villaria\05.Claude Code\ota-news-jp"
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/あなたのユーザー名/ota-news-jp.git
git push -u origin main
```

### 3. Anthropic API キーを GitHub Secret に登録

1. GitHubリポジトリ → 「Settings」タブ
2. 左メニュー「Secrets and variables」→「Actions」
3. 「New repository secret」
4. Name: `ANTHROPIC_API_KEY`
5. Secret: あなたのAPIキー（`sk-ant-...`）を貼り付け
6. 「Add secret」

### 4. GitHub Pages を有効化

1. GitHubリポジトリ → 「Settings」タブ
2. 左メニュー「Pages」
3. Source: 「Deploy from a branch」
4. Branch: `main` / `docs` フォルダを選択
5. 「Save」

### 5. 初回手動実行

1. GitHubリポジトリ → 「Actions」タブ
2. 「Update OTA News Summary」→「Run workflow」→「Run workflow」
3. 数分後にサイトが更新される

### 6. 公開URL

```
https://あなたのユーザー名.github.io/ota-news-jp/
```

## ローカルでのテスト

```powershell
cd "C:\Villaria\05.Claude Code\ota-news-jp"
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "sk-ant-あなたのAPIキー"
python main.py
# docs/index.html をブラウザで開いて確認
```

## 更新スケジュール

日本時間で毎日 **6:00 / 12:00 / 18:00 / 24:00** に自動更新します。
`.github/workflows/update.yml` の `cron` を編集すれば変更できます。
