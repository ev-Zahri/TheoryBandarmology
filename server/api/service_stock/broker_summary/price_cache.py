"""
Price Cache Manager for Indonesian Stocks
Caches stock prices with 15-minute TTL to avoid yfinance rate limiting
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
from api.helper.idx_data import load_idx_sectors_from_wiki
import time


# Cache file path
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'stock_prices_cache.json')

# Cache TTL: 15 minutes
CACHE_TTL_MINUTES = 15

# Known delisted/suspended stocks to skip (updated periodically)
DELISTED_STOCKS = {
    'NCKL', 'MTMH', 'ZONE', 'MAIN', 'CRAB', 'BIMA', 'KBLM', 'SQMI',
    'PNSE', 'TRAM', 'WOMF', 'KARW', 'SRTG', 'CPGT', 'KOBX', 'MITI',
    # Add more as discovered
}


def normalize_stock_code(stock_code: str) -> str:
    """
    Normalize stock code by removing special suffixes.
    
    Examples:
        BBCA-W -> BBCA (warrant)
        BRPTBQCF6A -> BRPT (rights issue)
        BBCA -> BBCA (normal stock)
    
    Args:
        stock_code: Raw stock code from broker data
        
    Returns:
        Normalized base stock code
    """
    if not stock_code:
        return stock_code
    
    # Remove warrant suffix (-W)
    if stock_code.endswith('-W'):
        return stock_code[:-2]
    
    # Remove rights/special suffixes (usually 4+ chars, mix of letters/numbers)
    # Pattern: Base stock (4 chars) + Suffix (6+ chars with numbers)
    # Example: BRPT (4) + BQCF6A (6) = BRPTBQCF6A
    
    # If length > 4 and contains numbers, likely has suffix
    if len(stock_code) > 4:
        # Try to extract base code (usually first 4 chars)
        # Check if it's a valid pattern (letters only for base)
        base = stock_code[:4]
        suffix = stock_code[4:]
        
        # If suffix contains numbers or special chars, it's likely a special code
        if any(c.isdigit() for c in suffix) or any(c in 'QWXYZ' for c in suffix):
            return base
    
    return stock_code


def get_idx_stock_list() -> List[str]:
    """
    Get list of all Indonesian stock codes from Wikipedia.
    Uses the existing idx_data.py scraper to get 900+ stocks.
    Filters out known delisted stocks.
    """
    try:
        # Load sector map from Wikipedia (with caching)
        sector_map = load_idx_sectors_from_wiki()
        
        # Extract all stock codes from all sectors
        all_stocks = []
        for sector, stocks in sector_map.items():
            all_stocks.extend(stocks)
        
        # Remove duplicates
        unique_stocks = list(set(all_stocks))
        
        # Filter out delisted stocks
        active_stocks = [s for s in unique_stocks if s not in DELISTED_STOCKS]
        
        delisted_count = len(unique_stocks) - len(active_stocks)
        if delisted_count > 0:
            print(f"Filtered out {delisted_count} delisted stocks")
        
        print(f"Loaded {len(active_stocks)} active stocks from IDX (Wikipedia)")
        return active_stocks
    
    except Exception as e:
        print(f"Error loading IDX stocks from Wikipedia: {e}")
        print("Falling back to minimal stock list...")
        
        # Minimal fallback list
        return [
            'BBCA', 'BBRI', 'BMRI', 'BBNI', 'TLKM', 'ASII', 'UNVR', 'ICBP', 
            'GGRM', 'HMSP', 'INDF', 'KLBF', 'ADRO', 'ANTM', 'INCO', 'PTBA'
        ]


def load_cache() -> Optional[Dict]:
    """Load price cache from JSON file"""
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        
        # Check if cache is still valid (within TTL)
        last_updated = datetime.fromisoformat(cache.get('last_updated', ''))
        now = datetime.now()
        
        if now - last_updated > timedelta(minutes=CACHE_TTL_MINUTES):
            print(f"Cache expired (last updated: {last_updated})")
            return None
        
        print(f"Cache loaded ({len(cache.get('prices', {}))} stocks, age: {(now - last_updated).seconds // 60} minutes)")
        return cache
    
    except Exception as e:
        print(f"Error loading cache: {e}")
        return None


def save_cache(prices: Dict[str, Optional[float]]):
    """Save price cache to JSON file"""
    try:
        cache = {
            'last_updated': datetime.now().isoformat(),
            'ttl_minutes': CACHE_TTL_MINUTES,
            'total_stocks': len(prices),
            'prices': prices
        }
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
        
        print(f"Cache saved: {len(prices)} stocks")
    
    except Exception as e:
        print(f"Error saving cache: {e}")


def fetch_single_price(stock_code: str, retry_count: int = 0) -> Optional[float]:
    """
    Fetch single stock price with retry logic and delisted stock handling.
    Normalizes stock code to handle warrants and rights issues.
    """
    # Normalize stock code (remove -W, rights suffixes, etc.)
    normalized_code = normalize_stock_code(stock_code)
    
    # Skip known delisted stocks
    if normalized_code in DELISTED_STOCKS:
        return None
    
    try:
        ticker_symbol = f"{normalized_code}.JK"
        stock = yf.Ticker(ticker_symbol)
        
        # Try to get current price
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        if current_price:
            return float(current_price)
        
        # Fallback: try history
        hist = stock.history(period='1d')
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        
        return None
    
    except Exception as e:
        error_msg = str(e)
        
        # Check if stock is delisted
        if 'delisted' in error_msg.lower() or 'not found' in error_msg.lower():
            # Add to delisted list and skip silently
            DELISTED_STOCKS.add(normalized_code)
            return None
        
        # Handle rate limiting
        if 'Too Many Requests' in error_msg and retry_count < 3:
            wait_time = (2 ** retry_count) * 5  # 5s, 10s, 20s
            print(f"Rate limited on {normalized_code}, retrying in {wait_time}s...")
            time.sleep(wait_time)
            return fetch_single_price(stock_code, retry_count + 1)
        
        # Only print error for non-delisted issues
        if 'delisted' not in error_msg.lower() and 'not found' not in error_msg.lower():
            print(f"Error fetching {normalized_code}: {e}")
        
        return None


def fetch_all_prices(stock_codes: List[str], max_workers: int = 5) -> Dict[str, Optional[float]]:
    """
    Fetch prices for all stocks with rate limiting protection
    Uses smaller max_workers to avoid rate limiting
    """
    prices = {}
    total = len(stock_codes)
    completed = 0
    
    print(f"Fetching prices for {total} stocks (max {max_workers} concurrent)...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_stock = {
            executor.submit(fetch_single_price, code): code 
            for code in stock_codes
        }
        
        for future in as_completed(future_to_stock):
            stock_code = future_to_stock[future]
            try:
                price = future.result()
                prices[stock_code] = price
                completed += 1
                
                if completed % 50 == 0:
                    print(f"Progress: {completed}/{total} stocks fetched")
            
            except Exception as e:
                print(f"Error processing {stock_code}: {e}")
                prices[stock_code] = None
    
    successful = sum(1 for p in prices.values() if p is not None)
    print(f"Completed: {successful}/{total} prices fetched successfully")
    
    return prices


def get_price(stock_code: str, force_refresh: bool = False) -> Optional[float]:
    """
    Get stock price from cache or fetch if needed
    
    Args:
        stock_code: Stock ticker code
        force_refresh: Force refresh from API even if cache exists
        
    Returns:
        Current stock price or None
    """
    # Skip delisted stocks
    if stock_code in DELISTED_STOCKS:
        return None
    
    # Load cache
    if not force_refresh:
        cache = load_cache()
        if cache and stock_code in cache.get('prices', {}):
            return cache['prices'][stock_code]
    
    # Cache miss or expired - fetch individual stock
    print(f"Fetching {stock_code} from API...")
    price = fetch_single_price(stock_code)
    
    # Update cache with new price
    cache = load_cache()
    if cache and cache.get('prices'):
        cache['prices'][stock_code] = price
    else:
        cache = {
            'prices': {stock_code: price},
            'last_updated': datetime.now().isoformat(),
            'ttl_minutes': CACHE_TTL_MINUTES
        }
    
    save_cache(cache['prices'])
    
    return price


def refresh_cache(stock_codes: Optional[List[str]] = None) -> Dict[str, Optional[float]]:
    """
    Refresh price cache for all or specific stocks
    
    Args:
        stock_codes: List of stock codes to refresh, or None for all IDX stocks
        
    Returns:
        Dictionary of stock prices
    """
    if stock_codes is None:
        stock_codes = get_idx_stock_list()
    
    print(f"Refreshing cache for {len(stock_codes)} stocks...")
    prices = fetch_all_prices(stock_codes, max_workers=5)
    save_cache(prices)
    
    return prices


def get_multiple_prices(stock_codes: List[str]) -> Dict[str, Optional[float]]:
    """
    Get prices for multiple stocks using incremental caching.
    Only fetches prices for stocks not in cache or if cache is expired.
    
    Args:
        stock_codes: List of stock codes from broker data
        
    Returns:
        Dictionary mapping stock codes to prices
    """
    # Load existing cache
    cache = load_cache()
    
    prices = {}
    missing_stocks = []
    
    # Check which stocks are in valid cache
    if cache and cache.get('prices'):
        cached_prices = cache['prices']
        
        for code in stock_codes:
            # Skip delisted stocks
            if code in DELISTED_STOCKS:
                prices[code] = None
                continue
            
            # Use cached price if available
            if code in cached_prices:
                prices[code] = cached_prices[code]
            else:
                missing_stocks.append(code)
    else:
        # No valid cache, need to fetch all
        missing_stocks = [s for s in stock_codes if s not in DELISTED_STOCKS]
    
    # Fetch only missing stocks
    if missing_stocks:
        print(f"Cache miss for {len(missing_stocks)} stocks, fetching from API...")
        new_prices = fetch_all_prices(missing_stocks, max_workers=5)
        
        # Merge with existing prices
        prices.update(new_prices)
        
        # Update cache with new prices
        if cache and cache.get('prices'):
            cache['prices'].update(new_prices)
        else:
            cache = {'prices': new_prices}
        
        cache['last_updated'] = datetime.now().isoformat()
        cache['ttl_minutes'] = CACHE_TTL_MINUTES
        save_cache(cache.get('prices', {}))
    else:
        print(f"All {len(stock_codes)} stocks found in cache (age: {get_cache_age(cache)} minutes)")
    
    return prices


def get_cache_age(cache: Optional[Dict]) -> int:
    """Get cache age in minutes"""
    if not cache or 'last_updated' not in cache:
        return 999
    
    try:
        last_updated = datetime.fromisoformat(cache['last_updated'])
        age = (datetime.now() - last_updated).seconds // 60
        return age
    except:
        return 999
