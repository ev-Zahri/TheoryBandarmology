"""
Master Data Loader for Technical Stock Data
Loads from JSON cache with fallback to yfinance
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
import time

# Path to technical data JSON
TECHNICAL_DATA_FILE = Path(__file__).parent.parent.parent / "data" / "stock_technical_data.json"

# Cache TTL: 24 hours for technical data
CACHE_TTL_HOURS = 24


def load_technical_data() -> Dict[str, Any]:
    """Load technical data from JSON file"""
    if not TECHNICAL_DATA_FILE.exists():
        return {
            'last_updated': None,
            'stocks': {}
        }
    
    try:
        with open(TECHNICAL_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading technical data: {e}")
        return {
            'last_updated': None,
            'stocks': {}
        }


def save_technical_data(data: Dict[str, Any]):
    """Save technical data to JSON file"""
    try:
        TECHNICAL_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        data['last_updated'] = datetime.now().isoformat()
        
        with open(TECHNICAL_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Technical data saved: {len(data.get('stocks', {}))} stocks")
    except Exception as e:
        print(f"Error saving technical data: {e}")


def get_stock_technical_data(stock_code: str) -> Optional[Dict[str, Any]]:
    """
    Get technical data for a single stock
    Returns None if not found
    """
    data = load_technical_data()
    return data.get('stocks', {}).get(stock_code)


def get_current_price(stock_code: str) -> Optional[float]:
    """Get current price for a stock"""
    stock_data = get_stock_technical_data(stock_code)
    if stock_data:
        return stock_data.get('current_price')
    return None


def get_multiple_prices(stock_codes: List[str]) -> Dict[str, Optional[float]]:
    """
    Get prices for multiple stocks from technical JSON
    
    Args:
        stock_codes: List of stock codes
        
    Returns:
        Dictionary mapping stock codes to prices
    """
    data = load_technical_data()
    prices = {}
    
    for code in stock_codes:
        stock_data = data.get('stocks', {}).get(code)
        if stock_data:
            prices[code] = stock_data.get('current_price')
        else:
            prices[code] = None
    
    return prices


def is_data_stale(hours: int = CACHE_TTL_HOURS) -> bool:
    """Check if technical data is stale"""
    data = load_technical_data()
    
    if not data.get('last_updated'):
        return True
    
    try:
        last_updated = datetime.fromisoformat(data['last_updated'])
        age = datetime.now() - last_updated
        return age > timedelta(hours=hours)
    except:
        return True


def get_data_age() -> Optional[str]:
    """Get human-readable age of technical data"""
    data = load_technical_data()
    
    if not data.get('last_updated'):
        return None
    
    try:
        last_updated = datetime.fromisoformat(data['last_updated'])
        age = datetime.now() - last_updated
        
        if age.days > 0:
            return f"{age.days} day{'s' if age.days > 1 else ''} ago"
        elif age.seconds > 3600:
            hours = age.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = age.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    except:
        return None


def get_stats() -> Dict[str, Any]:
    """Get statistics about technical data"""
    data = load_technical_data()
    
    return {
        'total_stocks': len(data.get('stocks', {})),
        'last_updated': data.get('last_updated'),
        'age': get_data_age(),
        'is_stale': is_data_stale()
    }
