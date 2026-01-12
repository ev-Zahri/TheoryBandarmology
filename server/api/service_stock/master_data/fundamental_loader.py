"""
Master Data Loader for Fundamental Stock Data
Loads from JSON cache with fallback to yfinance
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any

# Path to fundamental data JSON
FUNDAMENTAL_DATA_FILE = Path(__file__).parent.parent.parent / "data" / "stock_fundamental_data.json"

# Cache TTL: 7 days for fundamental data
CACHE_TTL_DAYS = 7


def load_fundamental_data() -> Dict[str, Any]:
    """Load fundamental data from JSON file"""
    if not FUNDAMENTAL_DATA_FILE.exists():
        return {
            'last_updated': None,
            'stocks': {}
        }
    
    try:
        with open(FUNDAMENTAL_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fundamental data: {e}")
        return {
            'last_updated': None,
            'stocks': {}
        }


def save_fundamental_data(data: Dict[str, Any]):
    """Save fundamental data to JSON file"""
    try:
        FUNDAMENTAL_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        data['last_updated'] = datetime.now().isoformat()
        
        with open(FUNDAMENTAL_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Fundamental data saved: {len(data.get('stocks', {}))} stocks")
    except Exception as e:
        print(f"Error saving fundamental data: {e}")


def get_stock_fundamental_data(stock_code: str) -> Optional[Dict[str, Any]]:
    """
    Get fundamental data for a single stock
    Returns None if not found
    """
    data = load_fundamental_data()
    return data.get('stocks', {}).get(stock_code)


def get_sector(stock_code: str) -> str:
    """Get sector for a stock"""
    stock_data = get_stock_fundamental_data(stock_code)
    if stock_data:
        return stock_data.get('sector', 'Unknown')
    return 'Unknown'


def get_financial_ratios(stock_code: str) -> Dict[str, Optional[float]]:
    """Get financial ratios for a stock"""
    stock_data = get_stock_fundamental_data(stock_code)
    
    if not stock_data:
        return {}
    
    return {
        'pe_ratio': stock_data.get('pe_ratio'),
        'pb_ratio': stock_data.get('pb_ratio'),
        'ps_ratio': stock_data.get('ps_ratio'),
        'roe': stock_data.get('roe'),
        'roa': stock_data.get('roa'),
        'debt_to_equity': stock_data.get('debt_to_equity'),
        'current_ratio': stock_data.get('current_ratio'),
        'dividend_yield': stock_data.get('dividend_yield')
    }


def get_company_profile(stock_code: str) -> Dict[str, Any]:
    """Get company profile for a stock"""
    stock_data = get_stock_fundamental_data(stock_code)
    
    if not stock_data:
        return {}
    
    return {
        'company_name': stock_data.get('company_name', stock_code),
        'sector': stock_data.get('sector', 'Unknown'),
        'industry': stock_data.get('industry', 'Unknown'),
        'market_cap': stock_data.get('market_cap'),
        'employees': stock_data.get('employees'),
        'website': stock_data.get('website'),
        'description': stock_data.get('description', '')
    }


def is_data_stale(days: int = CACHE_TTL_DAYS) -> bool:
    """Check if fundamental data is stale"""
    data = load_fundamental_data()
    
    if not data.get('last_updated'):
        return True
    
    try:
        last_updated = datetime.fromisoformat(data['last_updated'])
        age = datetime.now() - last_updated
        return age > timedelta(days=days)
    except:
        return True


def get_data_age() -> Optional[str]:
    """Get human-readable age of fundamental data"""
    data = load_fundamental_data()
    
    if not data.get('last_updated'):
        return None
    
    try:
        last_updated = datetime.fromisoformat(data['last_updated'])
        age = datetime.now() - last_updated
        
        if age.days > 0:
            return f"{age.days} day{'s' if age.days > 1 else ''} ago"
        else:
            hours = age.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
    except:
        return None


def get_stats() -> Dict[str, Any]:
    """Get statistics about fundamental data"""
    data = load_fundamental_data()
    
    return {
        'total_stocks': len(data.get('stocks', {})),
        'last_updated': data.get('last_updated'),
        'age': get_data_age(),
        'is_stale': is_data_stale()
    }


def get_all_sectors() -> List[str]:
    """Get list of all unique sectors"""
    data = load_fundamental_data()
    sectors = set()
    
    for stock_data in data.get('stocks', {}).values():
        sector = stock_data.get('sector')
        if sector and sector != 'Unknown':
            sectors.add(sector)
    
    return sorted(list(sectors))
