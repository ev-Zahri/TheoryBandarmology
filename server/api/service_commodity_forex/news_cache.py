"""
News Cache Manager
Manages caching of news data to avoid redundant API calls
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import threading


class NewsCache:
    """
    Thread-safe cache for news data with TTL (Time To Live)
    """
    
    def __init__(self, ttl_minutes: int = 15):
        """
        Args:
            ttl_minutes: Cache time-to-live in minutes (default: 15 minutes)
        """
        self.cache: Dict[str, Dict] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
        self.lock = threading.Lock()
    
    def _get_cache_key(self, symbol: str, type: str, limit: int) -> str:
        """Generate cache key from parameters"""
        return f"{symbol}:{type}:{limit}"
    
    def get(self, symbol: str, type: str, limit: int) -> Optional[List[Dict]]:
        """
        Get cached news data if available and not expired
        
        Args:
            symbol: Symbol (e.g., 'XAUUSD')
            type: Type ('forex' or 'commodity')
            limit: Number of items
        
        Returns:
            Cached news data or None if not found/expired
        """
        with self.lock:
            key = self._get_cache_key(symbol, type, limit)
            
            if key not in self.cache:
                return None
            
            cached_data = self.cache[key]
            cached_time = cached_data['timestamp']
            
            # Check if cache is expired
            if datetime.now() - cached_time > self.ttl:
                # Remove expired cache
                del self.cache[key]
                return None
            
            print(f"✅ Cache HIT for {symbol} ({type})")
            return cached_data['data']
    
    def set(self, symbol: str, type: str, limit: int, data: List[Dict]):
        """
        Store news data in cache
        
        Args:
            symbol: Symbol
            type: Type
            limit: Number of items
            data: News data to cache
        """
        with self.lock:
            key = self._get_cache_key(symbol, type, limit)
            self.cache[key] = {
                'data': data,
                'timestamp': datetime.now()
            }
            print(f"💾 Cached {len(data)} news items for {symbol} ({type})")
    
    def invalidate(self, symbol: str = None, type: str = None):
        """
        Invalidate cache for specific symbol/type or all
        
        Args:
            symbol: Symbol to invalidate (None = all)
            type: Type to invalidate (None = all)
        """
        with self.lock:
            if symbol is None and type is None:
                # Clear all cache
                self.cache.clear()
                print("🗑️  Cleared all cache")
            else:
                # Clear specific cache entries
                keys_to_remove = []
                for key in self.cache.keys():
                    parts = key.split(':')
                    if (symbol is None or parts[0] == symbol) and \
                       (type is None or parts[1] == type):
                        keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    del self.cache[key]
                
                if keys_to_remove:
                    print(f"🗑️  Invalidated {len(keys_to_remove)} cache entries")
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            total_entries = len(self.cache)
            total_items = sum(len(v['data']) for v in self.cache.values())
            
            return {
                'total_entries': total_entries,
                'total_items': total_items,
                'ttl_minutes': self.ttl.total_seconds() / 60
            }


# Global cache instance
news_cache = NewsCache(ttl_minutes=15)  # 15 minutes TTL
