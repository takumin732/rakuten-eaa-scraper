import os
import re
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# --- 設定 ---
SEARCH_KEYWORD = 'EAA'
OUTPUT_FILE = 'eaa_analysis_results.xlsx'
USER_DATA_DIR = os.path.join(os.getcwd(), 'rakuten_user_data')
MAX_ITEMS = 20  # 解析する最大商品数

# 抽出したいアミノ酸リスト
COMPONENTS = {
    'ロイシン': 'L-ロイシン',
    'リジン': 'L-リジン',
    'イソロイシン': 'L-イソロイシン',
    'バリン': 'L-バリン',
    'スレオニン': 'L-スレオニン',
    'フェニルアラニン': 'L-フェニルアラニン',
    'トリプトファン': 'L-トリプトファン',
    'メチオニン': 'L-メチオニン',
    'ヒスチジン': 'L-ヒスチジン'
}

def extract_value(text, component_name):
    """テキストから成分量(mg)を抽出する"""
    pattern = rf'{component_name}\D*(\d+(?:\.\d+)?)\s*(mg|g|グラム)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        val = float(match.group(1))
        unit = match.group(2).lower()
        if unit in ['g', 'グラム']:
            return val * 1000
        return val
    return None

def extract_serving_size(text):
    """基準となる摂取量を抽出する"""
    patterns = [
        r'(?:1日|1回|1食|当たり|あたり)\s*(\d+(?:\.\d+)?)\s*(g|グラム)',
        r'(\d+(?:\.\d+)?)\s*(g|グラム)\s*(?:あたり|当たり)'
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return float(match.group(1))
    return None

def run_scraper():
    results = []

    with sync_playwright() as p:
        print("ブラウザを起動しています...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            slow_mo=500
        )
        page = context.new_page()

        # 楽天検索ページへ直接移動
        search_url = f"https://search.rakuten.co.jp/search/mall/{SEARCH_KEYWORD.replace(' ', '+')}/"
        page.goto(search_url)

        print("\n" + "="*50)
        print("【ログイン待機】")
        print("1. 必要であればブラウザで楽天にログインしてください。")
        print("2. 検索結果が表示されていることを確認してください。")
        print("3. 準備ができたら、この画面で Enter キーを押してください。")
        print("="*50)
        input("Enterキーを押して解析を開始...")

        # 検索結果から商品リンクを取得
        # 楽天の検索結果セレクタは変更される可能性があるため、広めに取得
        print("商品リストを取得中...")
        items = page.query_selector_all("div.item--2S_X1, div.searchresultitem") # 一般的なクラス名
        
        # クラス名が取れない場合、リンクから推測
        if not items:
            links = page.query_selector_all("a")
            product_links = []
            for l in links:
                href = l.get_attribute("href")
                if href and "item.rakuten.co.jp" in href and href not in product_links:
                    product_links.append(href)
        else:
            product_links = []
            for item in items:
                link_element = item.query_selector("a")
                if link_element:
                    href = link_element.get_attribute("href")
                    if href and href not in product_links:
                        product_links.append(href)

        # 重複削除と件数制限
        product_links = list(dict.fromkeys(product_links))[:MAX_ITEMS]
        print(f"{len(product_links)} 件の商品が見つかりました。順次解析します。")

        for idx, url in enumerate(product_links, 1):
            print(f"[{idx}/{len(product_links)}] 解析中: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded")
                time.sleep(2) # 読み込み待ち

                title = page.title().split("|")[0].strip()
                content = page.inner_text("body")
                
                # 価格の取得（セレクタは変動するため、正規表現で補助）
                price_text = page.query_selector(".price2, .item_price, #price-box")
                price = price_text.inner_text() if price_text else "不明"

                serving_size = extract_serving_size(content)
                if not serving_size:
                    serving_size = 1.0

                item_data = {
                    '商品名': title[:50],
                    '価格': price.replace("\n", "").replace(" ", ""),
                    '基準量(g)': serving_size,
                    'URL': url
                }

                for key, display_name in COMPONENTS.items():
                    mg = extract_value(content, key)
                    if mg is not None:
                        item_data[f'{display_name}(mg/1g)'] = round(mg / serving_size, 2)
                    else:
                        item_data[f'{display_name}(mg/1g)'] = None
                
                results.append(item_data)
                
            except Exception as e:
                print(f"エラー: {e}")

        context.close()

    # データをExcelに保存
    if results:
        df = pd.DataFrame(results)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"\n完了。 データを {OUTPUT_FILE} に保存しました。")
    else:
        print("データが抽出されませんでした。")

if __name__ == "__main__":
    run_scraper()
