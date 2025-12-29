"""
Service Commodity & Forex News Analysis
========================================

Main exports untuk news analysis system.

Usage:
    from api.service_comm_forex import CompleteNewsAnalyzer
    
    analyzer = CompleteNewsAnalyzer()
    collection = analyzer.analyze_from_tradingview(symbol="XAUUSD", limit=20)
    sentiment = analyzer.get_market_sentiment()
"""

# Main analyzer (recommended)
from .complete_news_analyzer import CompleteNewsAnalyzer

# Core components (jika perlu akses langsung)
from .tradingview_news_fetcher import TradingViewNewsFetcher
from .enhanced_sentiment import EnhancedSentimentAnalyzer
from .news_model import NewsItem, NewsCollection, NewsProvider, RelatedSymbol

__all__ = [
    'CompleteNewsAnalyzer',
    'TradingViewNewsFetcher',
    'EnhancedSentimentAnalyzer',
    'NewsItem',
    'NewsCollection',
    'NewsProvider',
    'RelatedSymbol',
]

__version__ = '2.0.0'
