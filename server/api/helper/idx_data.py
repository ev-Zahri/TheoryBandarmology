import pandas as pd
import ssl
import json
import os
from pathlib import Path

# --- BACKUP MANUAL (Jika Scraping dan JSON Cache Gagal) ---
TOP_CAPS_MAP = {
    "Financials": ["BBCA", "BBRI", "BMRI", "BBNI", "ARTO", "BRIS", "BBTN", "MEGA"],
    "Consumer Non-Cyclicals": ["ICBP", "INDF", "MYOR", "UNVR", "GGRM", "HMSP", "KLBF", "SIDO", "CPIN", "JPFA"],
    "Basic Materials": ["MDKA", "ANTM", "INCO", "TINS", "BRMS", "MBMA", "INKP", "TKIM", "SMGR", "INTP"],
    "Energy": ["ADRO", "PTBA", "ITMG", "PGAS", "AKRA", "MEDC", "BUMI", "HRUM", "INDY"],
    "Technology": ["GOTO", "BUKA", "EMTK", "DCII", "MTDL"],
    "Healthcare": ["MIKA", "HEAL", "SILO", "KLBF", "SAME"],
    "Infrastructures": ["TLKM", "ISAT", "EXCL", "JSMR", "TBIG", "TOWR", "PGAS"],
    "Properties & Real Estate": ["BSDE", "CTRA", "PWON", "SMRA", "ASRI", "PANI"],
    "Industrials": ["ASII", "UNTR", "HEXA"],
    "Transportation & Logistic": ["BIRD", "ASSA", "TMAS", "SMDR"]
}

# Variable Global Cache (in-memory)
CACHED_SECTOR_MAP = {}

# Path to JSON cache file
CACHE_FILE_PATH = Path(__file__).parent.parent / "data" / "scraping-stock-wiki.json"

def load_from_json_cache():
    """Load sector map from JSON file if exists"""
    try:
        if CACHE_FILE_PATH.exists() and CACHE_FILE_PATH.stat().st_size > 0:
            with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data and isinstance(data, dict):
                    print(f"✅ Loaded {sum(len(v) for v in data.values())} stocks from JSON cache")
                    return data
    except Exception as e:
        print(f"⚠️ Error loading JSON cache: {e}")
    return None

def save_to_json_cache(sector_map):
    """Save sector map to JSON file"""
    try:
        # Ensure directory exists
        CACHE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CACHE_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(sector_map, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {sum(len(v) for v in sector_map.values())} stocks to JSON cache")
        return True
    except Exception as e:
        print(f"⚠️ Error saving to JSON cache: {e}")
        return False

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

def load_idx_sectors_from_wiki():
    """
    Load IDX sector data with caching strategy:
    1. Check in-memory cache
    2. Check JSON file cache
    3. Scrape from Wikipedia and save to JSON
    4. Fallback to hardcoded backup
    """
    global CACHED_SECTOR_MAP
    
    # 1. Check in-memory cache first (fastest)
    if CACHED_SECTOR_MAP:
        return CACHED_SECTOR_MAP
    
    # 2. Try to load from JSON cache
    json_data = load_from_json_cache()
    if json_data:
        CACHED_SECTOR_MAP = json_data
        return json_data
    
    # 3. JSON cache not found or empty - scrape from Wikipedia
    print("📡 JSON cache empty, scraping from Wikipedia...")
    scraped_data = scrape_from_wikipedia()
    
    if scraped_data:
        # Save to JSON for next time
        save_to_json_cache(scraped_data)
        CACHED_SECTOR_MAP = scraped_data
        return scraped_data
    
    # 4. Scraping failed - use hardcoded backup
    print("⚠️ Scraping failed. Using hardcoded backup data.")
    CACHED_SECTOR_MAP = TOP_CAPS_MAP
    return TOP_CAPS_MAP

def get_competitors(sector: str, current_stock: str):
    """Get competitor stocks in the same sector"""
    sector_map = load_idx_sectors_from_wiki()
    
    # Find candidates in the same sector
    candidates = []
    
    # Try exact match first
    if sector in sector_map:
        candidates = sector_map[sector]
    else:
        # Fuzzy match if not found
        for key, stocks in sector_map.items():
            # Match first word (e.g., 'Energy' matches 'Energy & Mineral')
            if sector.split()[0] in key or key.split()[0] in sector:
                candidates.extend(stocks)
                break
    
    # Fallback: use Financials as default
    if not candidates:
        candidates = TOP_CAPS_MAP.get("Financials", [])

    # Filter out current stock
    competitors = [s for s in candidates if s != current_stock]
    
    # Quality filter: prioritize stocks in TOP_CAPS_MAP
    priority_competitors = []
    other_competitors = []
    
    # Flatten TOP_CAPS_MAP for quick lookup
    all_top_caps = [item for sublist in TOP_CAPS_MAP.values() for item in sublist]
    
    for comp in competitors:
        if comp in all_top_caps:
            priority_competitors.append(comp)
        else:
            other_competitors.append(comp)
            
    # Combine: priority first, then others
    final_list = priority_competitors + other_competitors
    
    # Return top 4
    return final_list[:4]