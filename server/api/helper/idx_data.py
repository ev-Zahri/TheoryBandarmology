import json
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import requests

# --- BACKUP MANUAL (Jika Scraping dan JSON Cache Gagal) ---
TOP_CAPS_MAP: Dict[str, List[str]] = {
    "Financials": ["BBCA", "BBRI", "BMRI", "BBNI", "ARTO", "BRIS", "BBTN", "MEGA"],
    "Consumer Non-Cyclicals": ["ICBP", "INDF", "MYOR", "UNVR", "GGRM", "HMSP", "KLBF", "SIDO", "CPIN", "JPFA"],
    "Basic Materials": ["MDKA", "ANTM", "INCO", "TINS", "BRMS", "MBMA", "INKP", "TKIM", "SMGR", "INTP"],
    "Energy": ["ADRO", "PTBA", "ITMG", "PGAS", "AKRA", "MEDC", "BUMI", "HRUM", "INDY"],
    "Technology": ["GOTO", "BUKA", "EMTK", "DCII", "MTDL"],
    "Healthcare": ["MIKA", "HEAL", "SILO", "KLBF", "SAME"],
    "Infrastructures": ["TLKM", "ISAT", "EXCL", "JSMR", "TBIG", "TOWR", "PGAS"],
    "Properties & Real Estate": ["BSDE", "CTRA", "PWON", "SMRA", "ASRI", "PANI"],
    "Industrials": ["ASII", "UNTR", "HEXA"],
    "Transportation & Logistic": ["BIRD", "ASSA", "TMAS", "SMDR"],
}

# Variable Global Cache (in-memory)
CACHED_SECTOR_MAP: Dict[str, List[str]] = {}

# Path to JSON cache file
CACHE_FILE_PATH = Path(__file__).parent.parent / "data" / "scraping-stock-wiki.json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def load_from_json_cache() -> Optional[Dict[str, List[str]]]:
    """Load sector map from JSON cache file if it exists and has content."""
    try:
        if CACHE_FILE_PATH.exists() and CACHE_FILE_PATH.stat().st_size > 0:
            with CACHE_FILE_PATH.open("r", encoding="utf-8") as cache_file:
                data = json.load(cache_file)
            if data and isinstance(data, dict):
                print(f"Loaded {sum(len(v) for v in data.values())} tickers from JSON cache")
                # Ensure list conversion in case the JSON deserialized tuples/sets
                return {str(key): list(value) for key, value in data.items()}
    except Exception as exc:
        print(f"Error loading JSON cache: {exc}")
    return None


def save_to_json_cache(sector_map: Dict[str, List[str]]) -> bool:
    """Persist sector map to JSON for reuse."""
    try:
        CACHE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CACHE_FILE_PATH.open("w", encoding="utf-8") as cache_file:
            json.dump(sector_map, cache_file, ensure_ascii=False, indent=2)
        print(f"Saved {sum(len(v) for v in sector_map.values())} tickers to JSON cache")
        return True
    except Exception as exc:
        print(f"Error saving to JSON cache: {exc}")
        return False


def fetch_wikipedia_html() -> Optional[str]:
    """Fetch raw HTML from Wikipedia with a dedicated request."""
    try:
        response = requests.get(
            "https://id.wikipedia.org/wiki/Daftar_perusahaan_yang_tercatat_di_Bursa_Efek_Indonesia",
            headers={"User-Agent": USER_AGENT},
            timeout=15,
            verify=False,  # Match previous permissive SSL behavior
        )
        response.raise_for_status()
        return response.text
    except Exception as exc:
        print(f"Error fetching Wikipedia page: {exc}")
        return None


def scrape_from_wikipedia() -> Optional[Dict[str, List[str]]]:
    """Scrape stock data from Wikipedia."""
    html = fetch_wikipedia_html()
    if not html:
        return None

    try:
        dfs = pd.read_html(html, header=0)

        target_df = None
        for df in dfs:
            if "Kode" in df.columns and "Sektor" in df.columns:
                target_df = df
                break

        if target_df is None:
            print("Gagal menemukan tabel saham di Wikipedia")
            return None

        new_map: Dict[str, List[str]] = {}
        for _, row in target_df.iterrows():
            ticker = str(row["Kode"]).strip()
            sector_raw = str(row["Sektor"]).strip()

            new_map.setdefault(sector_raw, []).append(ticker)

        print(f"Scraped {len(target_df)} stocks from Wikipedia")
        return new_map

    except Exception as exc:
        print(f"Error scraping Wikipedia: {exc}")
        return None


def load_idx_sectors_from_wiki() -> Dict[str, List[str]]:
    """
    Load IDX sector data with caching strategy:
    1. Check in-memory cache
    2. Check JSON file cache
    3. Scrape from Wikipedia and save to JSON
    4. Fallback to hardcoded backup
    """
    global CACHED_SECTOR_MAP

    if CACHED_SECTOR_MAP:
        return CACHED_SECTOR_MAP

    json_data = load_from_json_cache()
    if json_data:
        CACHED_SECTOR_MAP = json_data
        return json_data

    print("JSON cache empty, scraping from Wikipedia...")
    scraped_data = scrape_from_wikipedia()

    if scraped_data:
        save_to_json_cache(scraped_data)
        CACHED_SECTOR_MAP = scraped_data
        return scraped_data

    print("Scraping failed. Using hardcoded backup data.")
    CACHED_SECTOR_MAP = TOP_CAPS_MAP
    return TOP_CAPS_MAP


def get_competitors(sector: str, current_stock: str) -> List[str]:
    """Get competitor stocks in the same sector."""
    sector_map = load_idx_sectors_from_wiki()

    normalized_sector = sector.lower()
    candidates: List[str] = []

    if sector in sector_map:
        candidates = sector_map[sector]
    else:
        for key, stocks in sector_map.items():
            if normalized_sector.split()[0] in key.lower().split()[0] or key.lower().split()[0] in normalized_sector:
                candidates.extend(stocks)
                break

    if not candidates:
        candidates = TOP_CAPS_MAP.get("Financials", [])

    competitors = [s for s in candidates if s != current_stock]

    all_top_caps = {item for sublist in TOP_CAPS_MAP.values() for item in sublist}
    priority_competitors = [comp for comp in competitors if comp in all_top_caps]
    other_competitors = [comp for comp in competitors if comp not in all_top_caps]

    final_list = priority_competitors + other_competitors
    return final_list[:4]
