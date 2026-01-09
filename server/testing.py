import feedparser
import json
import requests
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from newspaper import Article
import ssl
import pandas as pd
import re

# Configuration
RSS_SOURCES = {
    "CNBC Market": "https://www.cnbcindonesia.com/market/rss",
    "Kontan": "https://investasi.kontan.co.id/rss",
    "Antara Ekonomi": "https://www.antaranews.com/rss/ekonomi.xml",
    "Republika Ekonomi": "https://republika.co.id/rss/ekonomi/",
    "Okezone Saham": "https://economy.okezone.com/rss/saham",
    "Detik Finance": "finance.detik.com/bursa-valas/rss"
}

KEYWORDS = {
    "korporasi": ["akuisisi", "merger", "konsolidasi", "takeover", "pemegang saham pengendali", "right issue", "private placement", "divestasi", "stock split", "reverse stock split", "buyback"], 
    "insider": ["laporan kepemilikan saham", "direksi membeli", 'komisaris menjual', "divestasi pemilik", "pengendali baru", "perubahan kepemilikan", "pembelian saham oleh manajemen"],
    "fundamental": ["laba bersih naik", "pendapatan melonjak", "rugi bersih menyusut", "all-time high laba", "dividen interim", "rekor pendapatan", "efisiensi beban", "kinerja keuangan"],
    "eksternal": ["harga komoditas", "kenaikan suku bunga", "insentif pajak", "kebijakan pemerintah", "kurs rupiah", "import", "ekspor", "harga CPO", "harga batu bara", "harga nikel"],
    "warning": ["PKPU", "gagal bayar", "wanprestasi", "gugatan hukum", "suspensi saham", "delisting", "penurunan rating utang", "pailit", "dispute", "skandal", "pemeriksaan ojk"]
}

# Global variable to store stock data
STOCK_DATA = None

def load_stock_data(json_path="stocks_data.json"):
    """Load stock data from JSON file"""
    global STOCK_DATA
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            STOCK_DATA = json.load(f)
        print(f"✅ Loaded {STOCK_DATA['total_stocks']} stocks from {json_path}")
        return STOCK_DATA
    except Exception as e:
        print(f"⚠️ Failed to load stock data: {e}")
        return None

def detect_stocks_in_text(title, content):
    """
    Detect which stocks are mentioned in the title or content
    Returns list of stock objects with their codes
    """
    if not STOCK_DATA:
        return []
    
    detected_stocks = []
    text_combined = (title + " " + content).lower()
    
    for stock in STOCK_DATA['stocks']:
        code = stock['code']
        name = stock['name'].lower()
        
        # Check for stock code (with word boundaries to avoid false positives)
        # Match patterns like: "BBCA", "$BBCA", "BBCA)", "(BBCA", etc.
        code_pattern = r'\b' + re.escape(code) + r'\b'
        
        # Check for company name (must be substantial match, at least 3 words or 15 chars)
        name_words = name.split()
        
        code_found = bool(re.search(code_pattern, text_combined, re.IGNORECASE))
        name_found = False
        
        # For company name, check if significant portion appears
        if len(name) >= 10:  # Only check substantial names
            # Check if at least 70% of the name appears
            name_found = name in text_combined
        
        if code_found or name_found:
            detected_stocks.append({
                "code": code,
                "name": stock['name'],
                "sector": stock['sector'],
                "matched_by": "code" if code_found else "name"
            })
    
    return detected_stocks

def get_full_content(url):
    """Fetches full article content using newspaper3k."""
    try:
        if not url.startswith('http'):
            url = 'https://' + url
            
        article = Article(url, language='id')
        article.download()
        article.parse()
        return " ".join(article.text.split())
    except Exception as e:
        # Silently fail for parallel workers to keep logs clean
        return ""

def calculate_relevance(title, content, keywords_dict):
    """Calculates relevance score based on keyword matches in title and content."""
    score = 0
    found_categories = []
    
    title_lower = title.lower()
    content_lower = content.lower()
    
    for category, keys in keywords_dict.items():
        cat_match = False
        for k in keys:
            # Title matches are weighted higher (x5)
            if k in title_lower:
                score += 5
                cat_match = True
            # Content matches (x1)
            hits = content_lower.count(k)
            if hits > 0:
                score += hits
                cat_match = True
        
        if cat_match:
            found_categories.append(category)
            
    return score, list(set(found_categories))

def news_accumulator(sources, keywords, duration_days=3, limit=30):
    all_entries = []
    seen_links = set()
    cutoff_date = datetime.now() - timedelta(days=duration_days)
    
    # Load stock data if not already loaded
    if not STOCK_DATA:
        load_stock_data()
    
    print(f"[*] Starting news accumulation for the last {duration_days} days...")
    
    # 1. Collect and Initial Filter (Deduplication included)
    for name, url in sources.items():
        print(f"Mendapatkan data dari: {name}")
        url_to_fetch = url if url.startswith('http') else 'https://' + url
        feed = feedparser.parse(url_to_fetch)
        
        for entry in feed.entries:
            try:
                if entry.published_parsed:
                    entry_date = datetime(*entry.published_parsed[:6])
                else: continue
                
                if entry_date > cutoff_date and entry.link not in seen_links:
                    seen_links.add(entry.link)
                    all_entries.append({
                        "source": name,
                        "title": entry.title,
                        "link": entry.link,
                        "date": entry_date.strftime("%Y-%m-%d %H:%M"),
                        "raw_entry": entry
                    })
            except Exception: continue
        # print(f"Data raw: {json.dumps(feed.entries[0], indent=2)}")
    # 2. Parallel Content Fetching (Concurrency)
    print(f"[*] Fetching full content for {len(all_entries)} candidate articles in parallel...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        links = [e['link'] for e in all_entries]
        contents = list(executor.map(get_full_content, links))
    
    # 3. Relevance Scoring & Stock Detection
    final_results = []
    for entry, content in zip(all_entries, contents):
        score, categories = calculate_relevance(entry['title'], content, keywords)
        
        # Detect stocks mentioned in the article
        detected_stocks = detect_stocks_in_text(entry['title'], content)
        
        # Boost score if stocks are detected
        if detected_stocks:
            score += len(detected_stocks) * 3  # Add 3 points per stock mentioned
        
        if score > 0 or detected_stocks:  # Include if relevant OR mentions stocks
            final_results.append({
                "source": entry['source'],
                "title": entry['title'],
                "link": entry['link'],
                "date": entry['date'],
                "categories": categories,
                "stocks": detected_stocks,  # NEW: List of detected stocks
                "stock_count": len(detected_stocks),  # NEW: Number of stocks mentioned
                "relevance_score": score,
                "content": content if content else "Content extraction failed."
            })

    # 4. Sort by relevance
    final_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    final_results = final_results[:limit]
    
    # 5. Auto-Export (JSON)
    output_file = f"news_accumulator_latest.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_results, f, indent=2, ensure_ascii=False)
        print(f"[*] Exported {len(final_results)} articles to {output_file}")
        
        # Print summary statistics
        total_stocks_mentioned = sum(1 for r in final_results if r['stock_count'] > 0)
        print(f"[*] Articles mentioning stocks: {total_stocks_mentioned}/{len(final_results)}")
        
    except Exception as e:
        print(f"[!] Export error: {e}")

    return final_results

def scrape_from_wikipedia():
    """Scrape stock data from Wikipedia"""
    url = "https://id.wikipedia.org/wiki/Daftar_perusahaan_yang_tercatat_di_Bursa_Efek_Indonesia"
    
    try:
        # Bypass SSL verification error
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Add User-Agent header to avoid 403 Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        dfs = pd.read_html(url, header=0, storage_options={'User-Agent': headers['User-Agent']})

        print(f"DFS: {dfs}")
        
        target_df = None
        for df in dfs:
            if 'Kode' in df.columns and 'Sektor' in df.columns:
                target_df = df
                break
        
        if target_df is None:
            print("⚠️ Gagal menemukan tabel saham di Wikipedia")
            return None
            
        # Process DataFrame to Dictionary
        new_map = {}
        
        for index, row in target_df.iterrows():
            ticker = str(row['Kode']).strip()
            sector_raw = str(row['Sektor']).strip()
            
            if sector_raw not in new_map:
                new_map[sector_raw] = []
            
            new_map[sector_raw].append(ticker)
            
        print(f"✅ Scraped {len(target_df)} stocks from Wikipedia!")
        return new_map

    except Exception as e:
        print(f"⚠️ Error scraping Wikipedia: {e}")
        return None


if __name__ == "__main__":
    # Load stock data first
    load_stock_data()
    
    start_time = time.time()
    results = news_accumulator(RSS_SOURCES, KEYWORDS, duration_days=3, limit=20)
    end_time = time.time()
    
    print("\n" + "="*60)
    print(f"TOP RELEVANT NEWS (Execution Time: {end_time - start_time:.2f}s)")
    print("="*60)
    
    for i, b in enumerate(results):
        print(f"\n[{i+1}] {b['title']} (Score: {b['relevance_score']})")
        print(f"Source: {b['source']} | Categories: {', '.join(b['categories'])} | Date: {b['date']}")
        
        # Display detected stocks
        if b['stocks']:
            stock_codes = [f"{s['code']} ({s['sector']})" for s in b['stocks']]
            print(f"📊 Stocks: {', '.join(stock_codes)}")
        
        print(f"Snippet: {b['content'][:150]}...")
        print("-" * 40)

    # print("\n" + "="*60)
    # print(f"SCRAPE STOCK WIKI")
    # print("="*60)
    # scrape_from_wikipedia()