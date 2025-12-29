"""
TradingView News Fetcher - Fetch news dengan konten lengkap dari TradingView API
Menggunakan endpoint news-mediator untuk mendapatkan detail berita
"""

import requests
import json
from typing import Optional, Dict, List
from datetime import datetime
import time


class TradingViewNewsFetcher:
    """
    Fetcher untuk mengambil berita dari TradingView dengan konten lengkap
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.tradingview.com/',
            'Origin': 'https://www.tradingview.com'
        })
        
        # API endpoints
        self.news_list_url = "https://news-mediator.tradingview.com/public/view/v1/symbol"
        self.news_detail_url = "https://news-mediator.tradingview.com/public/news/v1/story"
    
    def _format_symbol(self, symbol: str, type: str = "forex") -> str:
        """
        Format symbol untuk TradingView
        
        Args:
            symbol: Symbol mentah (e.g., 'GOLD', 'XAUUSD')
            type: 'forex' atau 'commodity'
        
        Returns:
            Formatted symbol (e.g., 'FX:XAUUSD', 'TVC:GOLD')
        """
        symbol = symbol.upper()
        
        # Jika sudah ada prefix, return as is
        if ':' in symbol:
            return symbol
        
        # Format berdasarkan type
        if type == "forex":
            return f"FX:{symbol}"
        elif type == "commodity":
            return f"TVC:{symbol}"
        else:
            return symbol
    
    def fetch_news_list(self, symbol: str = "XAUUSD", limit: int = 50, type: str = "forex") -> List[Dict]:
        """
        Fetch daftar berita untuk symbol tertentu
        
        Args:
            symbol: Symbol untuk filter berita (e.g., 'GOLD', 'XAUUSD')
            limit: Jumlah maksimal berita yang diambil
            type: 'forex' atau 'commodity'
        
        Returns:
            List of news items (basic info)
        """
        try:
            # Format symbol
            formatted_symbol = self._format_symbol(symbol, type)
            
            # Params menggunakan format yang benar
            params = [
                ('filter', 'lang:en'),
                ('filter', f'symbol:{formatted_symbol}'),
                ('client', 'web'),
                ('streaming', 'false'),  # Non-streaming untuk get list
                ('user_prostatus', 'non_pro')
            ]
            
            response = self.session.get(
                self.news_list_url,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                return items[:limit]
            else:
                print(f"Error fetching news list: {response.status_code}")
                print(f"URL: {response.url}")
                return []
        
        except Exception as e:
            print(f"Error in fetch_news_list: {e}")
            return []
    
    def fetch_news_detail(self, news_id: str) -> Optional[Dict]:
        """
        Fetch detail berita lengkap termasuk konten
        
        Args:
            news_id: ID berita (e.g., 'moneycontrol:4fac10f29094b:0')
        
        Returns:
            Dictionary dengan detail berita lengkap atau None jika gagal
        """
        try:
            params = {
                'id': news_id,
                'lang': 'en',
                'user_prostatus': 'non_pro'
            }
            
            response = self.session.get(
                self.news_detail_url,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching detail for {news_id}: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"Error in fetch_news_detail for {news_id}: {e}")
            return None
    
    def extract_content_from_detail(self, detail: Dict) -> str:
        """
        Extract konten text dari detail response
        
        Args:
            detail: Detail response dari API
        
        Returns:
            String konten berita
        """
        # Try short_description first
        content = detail.get('short_description', '')
        
        # Try to extract from ast_description (lebih lengkap)
        ast_desc = detail.get('ast_description', {})
        if ast_desc and ast_desc.get('type') == 'root':
            children = ast_desc.get('children', [])
            paragraphs = []
            
            for child in children:
                if child.get('type') == 'p':
                    # Extract text from paragraph
                    p_children = child.get('children', [])
                    for text in p_children:
                        if isinstance(text, str):
                            paragraphs.append(text)
            
            if paragraphs:
                content = ' '.join(paragraphs)
        
        return content
    
    def fetch_news_with_content(
        self, 
        symbol: str = "XAUUSD", 
        limit: int = 20,
        type: str = "forex",
        delay: float = 0.5
    ) -> List[Dict]:
        """
        Fetch berita dengan konten lengkap
        
        Args:
            symbol: Symbol untuk filter
            limit: Jumlah berita maksimal
            type: 'forex' atau 'commodity'
            delay: Delay antar request detail (seconds)
        
        Returns:
            List of news items dengan konten lengkap
        """
        print(f"\n🔍 Fetching news for {symbol}...")
        
        # Step 1: Get news list
        news_list = self.fetch_news_list(symbol, limit, type)
        print(f"Found {len(news_list)} news items")
        
        # Step 2: Fetch detail untuk setiap berita
        news_with_content = []
        
        for i, news_item in enumerate(news_list, 1):
            news_id = news_item.get('id')
            title = news_item.get('title', '')
            
            print(f"[{i}/{len(news_list)}] Fetching: {title[:60]}...")
            
            # Fetch detail
            detail = self.fetch_news_detail(news_id)
            
            if detail:
                # Extract content
                content = self.extract_content_from_detail(detail)
                
                # Combine basic info + content
                news_item['full_content'] = content
                news_item['detail'] = detail
                
                news_with_content.append(news_item)
                print(f"  ✅ Got {len(content)} chars")
            else:
                print(f"  ❌ Failed to fetch detail")
            
            # Delay to avoid rate limiting
            if i < len(news_list):
                time.sleep(delay)
        
        print(f"\n✅ Successfully fetched {len(news_with_content)} news with content")
        return news_with_content
    
    def save_to_file(self, news_data: List[Dict], filepath: str):
        """
        Save news data ke JSON file
        
        Args:
            news_data: List of news items
            filepath: Output file path
        """
        output = {
            'fetched_at': datetime.now().isoformat(),
            'total_items': len(news_data),
            'items': news_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to {filepath}")


if __name__ == "__main__":
    # Test fetcher
    fetcher = TradingViewNewsFetcher()
    
    print("=" * 80)
    print("TRADINGVIEW NEWS FETCHER TEST")
    print("=" * 80)
    
    # Test 1: Fetch news list
    print("\n--- Test 1: Fetch News List ---")
    news_list = fetcher.fetch_news_list(symbol="XAUUSD", limit=5, type="forex")
    print(f"Got {len(news_list)} news items")
    
    if news_list:
        print("\nFirst news item:")
        first = news_list[0]
        print(f"  ID: {first.get('id')}")
        print(f"  Title: {first.get('title')}")
        print(f"  Published: {datetime.fromtimestamp(first.get('published', 0))}")
    
    # Test 2: Fetch detail
    if news_list:
        print("\n--- Test 2: Fetch News Detail ---")
        news_id = news_list[0].get('id')
        detail = fetcher.fetch_news_detail(news_id)
        
        if detail:
            print(f"✅ Got detail for {news_id}")
            content = fetcher.extract_content_from_detail(detail)
            print(f"Content length: {len(content)} chars")
            print(f"\nContent preview:\n{content[:300]}...")
    
    # Test 3: Fetch with content (only 3 items for demo)
    print("\n--- Test 3: Fetch News with Full Content ---")
    response = input("\nFetch 3 news with full content? (y/n): ").lower()
    
    if response == 'y':
        news_with_content = fetcher.fetch_news_with_content(
            symbol="XAUUSD",
            limit=3,
            type="forex",
            delay=1.0
        )
        
        # Save to file
        fetcher.save_to_file(
            news_with_content,
            'd:/Code Programs/Tech Stack/TheoryBandarmology/server/api/data/comm_forex/fetched_news.json'
        )
