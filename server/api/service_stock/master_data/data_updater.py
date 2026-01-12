"""
Data Updater for Master Stock Data
Fetches data from yfinance with anti-rate-limiting strategy
"""

import yfinance as yf
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

from api.helper.idx_data import load_idx_sectors_from_wiki
from api.service_stock.master_data.technical_loader import load_technical_data, save_technical_data
from api.service_stock.master_data.fundamental_loader import load_fundamental_data, save_fundamental_data


# Known delisted/suspended stocks to skip
DELISTED_STOCKS = {
    'SQMI', 'TRAM', 'WOMF', 'CPGT', 'MITI', 'MFIN', 'APOL', 'ATPK', 
    'BAEK', 'BBNP', 'BRAU', 'CKRA', 'DAJK', 'DAVO', 'GMCW', 'GREN', 
    'INVS', 'ITTG', 'LAMI', 'MASA', 'NAGA', 'SAIP', 'SCBD', 'SIAP', 
    'SOBI', 'SQBB', 'SQBI', 'STUP', 'TKGA', 'TMPI', 'TRUB', 'UMKM', 
    'UNTX', 'FORZ', 'FREN', 'HDTX', 'JKSW', 'KPAL', 'KPAS', 'KRAH', 
    'MAMI', 'MYRX', 'NIPS', 'PRAS', 
}


def normalize_stock_code(stock_code: str) -> str:
    """Normalize stock code (remove -W, rights suffixes)"""
    if not stock_code:
        return stock_code
    
    # Remove warrant suffix
    if stock_code.endswith('-W'):
        return stock_code[:-2]
    
    # Remove rights/special suffixes
    if len(stock_code) > 4:
        base = stock_code[:4]
        suffix = stock_code[4:]
        
        if any(c.isdigit() for c in suffix) or any(c in 'QWXYZ' for c in suffix):
            return base
    
    return stock_code


def clean_stock_code(stock_code: str) -> str:
    """
    Clean stock code by removing prefixes like 'BEI: ', whitespace, etc.
    """
    if not stock_code:
        return stock_code
    
    # Remove common prefixes
    prefixes_to_remove = ['BEI: ', 'BEI:', 'IDX: ', 'IDX:']
    for prefix in prefixes_to_remove:
        if stock_code.startswith(prefix):
            stock_code = stock_code[len(prefix):]
    
    # Strip whitespace
    stock_code = stock_code.strip()
    
    # Remove empty strings
    if not stock_code or stock_code == '':
        return None
    
    return stock_code


def get_all_stock_codes() -> List[str]:
    """
    Get all stock codes from multiple sources:
    1. Wikipedia (primary source)
    2. Existing cache (stocks we've seen before)
    3. Can be extended with broker data
    """
    all_stocks = set()
    
    # Source 1: Wikipedia
    try:
        sector_map = load_idx_sectors_from_wiki()
        for stocks in sector_map.values():
            # Clean each stock code
            cleaned_stocks = [clean_stock_code(s) for s in stocks]
            # Filter out None values
            cleaned_stocks = [s for s in cleaned_stocks if s]
            all_stocks.update(cleaned_stocks)
        print(f"Loaded {len(all_stocks)} stocks from Wikipedia")
    except Exception as e:
        print(f"Error loading from Wikipedia: {e}")
    
    # Source 2: Existing cache (stocks not in Wikipedia)
    try:
        technical_data = load_technical_data()
        cached_stocks = set(technical_data.get('stocks', {}).keys())
        new_from_cache = cached_stocks - all_stocks
        if new_from_cache:
            print(f"Found {len(new_from_cache)} additional stocks from cache")
            all_stocks.update(new_from_cache)
    except Exception as e:
        print(f"Error loading from cache: {e}")
    
    # Filter out delisted stocks and empty strings
    active_stocks = [s for s in all_stocks if s and s not in DELISTED_STOCKS]
    
    print(f"Total active stocks: {len(active_stocks)}")
    return sorted(list(active_stocks))


def fetch_technical_data_single(stock_code: str) -> Optional[Dict[str, Any]]:
    """Fetch technical data for a single stock"""
    normalized_code = normalize_stock_code(stock_code)
    
    if normalized_code in DELISTED_STOCKS:
        return None
    
    try:
        ticker = yf.Ticker(f"{normalized_code}.JK")
        info = ticker.info
        hist = ticker.history(period='1mo')
        
        # Check if stock has data
        if not info or info.get('regularMarketPrice') is None:
            return None
        
        # Calculate technical indicators
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        
        data = {
            'stock_code': stock_code,  # Original code
            'normalized_code': normalized_code,
            'current_price': current_price,
            'previous_close': info.get('previousClose'),
            'open': info.get('open'),
            'day_high': info.get('dayHigh'),
            'day_low': info.get('dayLow'),
            'volume': info.get('volume'),
            'avg_volume': info.get('averageVolume'),
            '52w_high': info.get('fiftyTwoWeekHigh'),
            '52w_low': info.get('fiftyTwoWeekLow'),
            'beta': info.get('beta'),
            'last_updated': datetime.now().isoformat()
        }
        
        # Add moving averages if history available
        if not hist.empty and len(hist) >= 50:
            data['moving_avg_50'] = hist['Close'].tail(50).mean()
            if len(hist) >= 200:
                data['moving_avg_200'] = hist['Close'].tail(200).mean()
        
        return data
    
    except Exception as e:
        error_msg = str(e)
        if 'delisted' in error_msg.lower() or 'not found' in error_msg.lower():
            DELISTED_STOCKS.add(normalized_code)
        return None


def fetch_fundamental_data_single(stock_code: str) -> Optional[Dict[str, Any]]:
    """Fetch fundamental data for a single stock"""
    normalized_code = normalize_stock_code(stock_code)
    
    if normalized_code in DELISTED_STOCKS:
        return None
    
    try:
        ticker = yf.Ticker(f"{normalized_code}.JK")
        info = ticker.info
        
        # Check if stock has data
        if not info or info.get('regularMarketPrice') is None:
            return None
        
        data = {
            'stock_code': stock_code,  # Original code
            'normalized_code': normalized_code,
            'company_name': info.get('longName', stock_code),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'market_cap': info.get('marketCap'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'pe_ratio': info.get('trailingPE'),
            'pb_ratio': info.get('priceToBook'),
            'ps_ratio': info.get('priceToSalesTrailing12Months'),
            'peg_ratio': info.get('pegRatio'),
            'roe': info.get('returnOnEquity'),
            'roa': info.get('returnOnAssets'),
            'debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'quick_ratio': info.get('quickRatio'),
            'dividend_yield': info.get('dividendYield'),
            'payout_ratio': info.get('payoutRatio'),
            'profit_margin': info.get('profitMargins'),
            'operating_margin': info.get('operatingMargins'),
            'book_value': info.get('bookValue'),
            'eps': info.get('trailingEps'),
            'website': info.get('website'),
            'employees': info.get('fullTimeEmployees'),
            'description': info.get('longBusinessSummary', ''),
            'last_updated': datetime.now().isoformat()
        }
        
        return data
    
    except Exception as e:
        error_msg = str(e)
        if 'delisted' in error_msg.lower() or 'not found' in error_msg.lower():
            DELISTED_STOCKS.add(normalized_code)
        return None


def update_technical_data_batch(
    stock_codes: List[str],
    batch_size: int = 300,
    delay_between_batches: int = 30,
    max_workers: int = 5,
    progress_callback=None
) -> Dict[str, Any]:
    """
    Update technical data with anti-rate-limiting strategy
    
    Args:
        stock_codes: List of stock codes to update
        batch_size: Number of stocks per batch
        delay_between_batches: Seconds to wait between batches
        max_workers: Max concurrent requests per batch
        progress_callback: Optional callback function(current, total, status)
        
    Returns:
        Updated technical data dictionary
    """
    # Load existing data
    data = load_technical_data()
    if 'stocks' not in data:
        data['stocks'] = {}
    
    total_stocks = len(stock_codes)
    processed = 0
    successful = 0
    failed = 0
    
    print(f"\n=== Starting Technical Data Update ===", flush=True)
    print(f"Total stocks: {total_stocks}", flush=True)
    print(f"Batch size: {batch_size}", flush=True)
    print(f"Delay between batches: {delay_between_batches}s", flush=True)
    print(f"Max workers per batch: {max_workers}\n", flush=True)
    
    # Report initial progress
    if progress_callback:
        progress_callback(0, total_stocks, "starting", successful, failed)
    
    # Process in batches
    for i in range(0, total_stocks, batch_size):
        batch = stock_codes[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_stocks + batch_size - 1) // batch_size
        
        print(f"Batch {batch_num}/{total_batches}: Processing {len(batch)} stocks...", flush=True)
        
        # Report batch start
        if progress_callback:
            progress_callback(processed, total_stocks, f"processing_batch_{batch_num}", successful, failed)
        
        # Fetch batch concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fetch_technical_data_single, code): code for code in batch}
            
            for future in as_completed(futures):
                stock_code = futures[future]
                try:
                    result = future.result()
                    if result:
                        data['stocks'][stock_code] = result
                        successful += 1
                    else:
                        failed += 1
                    processed += 1
                except Exception as e:
                    print(f"  Error processing {stock_code}: {e}", flush=True)
                    failed += 1
                    processed += 1
        
        print(f"  Progress: {processed}/{total_stocks} ({successful} successful, {failed} failed)", flush=True)
        
        # Save intermediate results
        save_technical_data(data)
        
        # Report progress after batch
        if progress_callback:
            progress_callback(processed, total_stocks, "batch_complete", successful, failed)
        
        # Delay before next batch (except for last batch)
        if i + batch_size < total_stocks:
            print(f"  Waiting {delay_between_batches}s before next batch...\n", flush=True)
            if progress_callback:
                progress_callback(processed, total_stocks, "waiting", successful, failed)
            time.sleep(delay_between_batches)
    
    print(f"\n=== Technical Data Update Complete ===", flush=True)
    print(f"Total: {processed} stocks", flush=True)
    print(f"Successful: {successful}", flush=True)
    print(f"Failed: {failed}", flush=True)
    print(f"Success rate: {(successful/processed*100):.1f}%\n", flush=True)
    
    # Report completion
    if progress_callback:
        progress_callback(processed, total_stocks, "complete", successful, failed)
    
    return data


def update_fundamental_data_batch(
    stock_codes: List[str],
    batch_size: int = 50,
    delay_between_batches: int = 60,
    max_workers: int = 5,
    progress_callback=None
) -> Dict[str, Any]:
    """
    Update fundamental data with anti-rate-limiting strategy
    Similar to technical update but for fundamental data
    """
    # Load existing data
    data = load_fundamental_data()
    if 'stocks' not in data:
        data['stocks'] = {}
    
    total_stocks = len(stock_codes)
    processed = 0
    successful = 0
    failed = 0
    
    print(f"\n=== Starting Fundamental Data Update ===", flush=True)
    print(f"Total stocks: {total_stocks}", flush=True)
    print(f"Batch size: {batch_size}", flush=True)
    print(f"Delay between batches: {delay_between_batches}s", flush=True)
    print(f"Max workers per batch: {max_workers}\n", flush=True)
    
    # Report initial progress
    if progress_callback:
        progress_callback(0, total_stocks, "starting", successful, failed)
    
    # Process in batches
    for i in range(0, total_stocks, batch_size):
        batch = stock_codes[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_stocks + batch_size - 1) // batch_size
        
        print(f"Batch {batch_num}/{total_batches}: Processing {len(batch)} stocks...", flush=True)
        
        if progress_callback:
            progress_callback(processed, total_stocks, f"processing_batch_{batch_num}", successful, failed)
        
        # Fetch batch concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fetch_fundamental_data_single, code): code for code in batch}
            
            for future in as_completed(futures):
                stock_code = futures[future]
                try:
                    result = future.result()
                    if result:
                        data['stocks'][stock_code] = result
                        successful += 1
                    else:
                        failed += 1
                    processed += 1
                except Exception as e:
                    print(f"  Error processing {stock_code}: {e}", flush=True)
                    failed += 1
                    processed += 1
        
        print(f"  Progress: {processed}/{total_stocks} ({successful} successful, {failed} failed)", flush=True)
        
        # Save intermediate results
        save_fundamental_data(data)
        
        if progress_callback:
            progress_callback(processed, total_stocks, "batch_complete", successful, failed)
        
        # Delay before next batch (except for last batch)
        if i + batch_size < total_stocks:
            print(f"  Waiting {delay_between_batches}s before next batch...\n", flush=True)
            if progress_callback:
                progress_callback(processed, total_stocks, "waiting", successful, failed)
            time.sleep(delay_between_batches)
    
    print(f"\n=== Fundamental Data Update Complete ===", flush=True)
    print(f"Total: {processed} stocks", flush=True)
    print(f"Successful: {successful}", flush=True)
    print(f"Failed: {failed}", flush=True)
    print(f"Success rate: {(successful/processed*100):.1f}%\n", flush=True)
    
    if progress_callback:
        progress_callback(processed, total_stocks, "complete", successful, failed)
    
    return data


def add_stocks_from_broker_data(stock_codes: List[str]):
    """
    Add new stocks discovered from broker data to master data
    This ensures stocks not in Wikipedia are still tracked
    """
    existing_technical = load_technical_data()
    existing_fundamental = load_fundamental_data()
    
    new_stocks = []
    for code in stock_codes:
        if code not in existing_technical.get('stocks', {}) and code not in existing_fundamental.get('stocks', {}):
            new_stocks.append(code)
    
    if new_stocks:
        print(f"Found {len(new_stocks)} new stocks from broker data")
        # Update both technical and fundamental for new stocks
        update_technical_data_batch(new_stocks, batch_size=10, delay_between_batches=30)
        update_fundamental_data_batch(new_stocks, batch_size=10, delay_between_batches=30)
