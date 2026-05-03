# Rakuten EAA Supplement Analyzer / 楽天EAAサプリメント解析スクレイパー

[English](#english) | [日本語](#japanese)

---

<a name="english"></a>
## English

A tool to automatically collect EAA supplement information from Rakuten Ichiba, extract component data (amino acid content), and summarize it in an Excel file.

### Features
- **Login Support**: Uses Playwright to handle login-required pages, member prices, and detailed info.
- **Auto Search & Analysis**: Automatically navigates up to 20 items based on specified keywords.
- **Component Extraction**: Analyzes essential amino acid content (Leucine, Valine, Isoleucine, etc.) from product descriptions.
- **Excel Output**: Saves results in a structured Excel sheet (`eaa_analysis_results.xlsx`).

### Setup
#### Requirements
- Python 3.8 or higher
- Google Chrome (Used automatically by Playwright)

#### Library Installation
```powershell
pip install playwright pandas openpyxl requests
playwright install chromium
```

### Usage
1. Double-click `run_scraper.bat` to start.
2. A browser will open. Log in to Rakuten if necessary.
3. Return to the terminal and press **Enter** to start analysis.
4. Once finished, `eaa_analysis_results.xlsx` will be generated in the same folder.

---

<a name="japanese"></a>
## 日本語

楽天市場からEAAサプリメントの商品情報を自動で収集し、成分量（アミノ酸含有量）を抽出してExcelファイルにまとめるツールです。

### 特徴
- **ログイン対応**: Playwrightを使用し、ログインが必要なページや会員価格、詳細情報にも対応。
- **自動検索 & 解析**: キーワードを指定して検索結果から最大20件の商品を自動巡回。
- **成分抽出**: 商品説明文からロイシン、バリン、イソロイシンなどの必須アミノ酸含有量を自動解析。
- **Excel出力**: 抽出結果を整理されたExcelシート（`eaa_analysis_results.xlsx`）として保存。

### セットアップ
#### 必要条件
- Python 3.8以上
- Google Chrome（Playwrightが自動で使用）

#### ライブラリのインストール
```powershell
pip install playwright pandas openpyxl requests
playwright install chromium
```

### 使い方
1. `run_scraper.bat` をダブルクリックして実行します。
2. ブラウザが起動するので、必要に応じて楽天市場にログインしてください。
3. ターミナル（黒い画面）に戻り、**Enterキー**を押すと解析が始まります。
4. 完了後、同フォルダ内に `eaa_analysis_results.xlsx` が生成されます。

---

## Security Note / セキュリティに関する注意
- `rakuten_user_data/` contains session info. **DO NOT upload this folder to GitHub.** / `rakuten_user_data/` にはセッション情報が含まれています。**このフォルダは絶対にGitHubにアップロードしないでください。**

## License / ライセンス
MIT License
