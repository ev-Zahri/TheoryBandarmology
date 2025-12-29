"""
Complete News Analysis System
Fetch dari TradingView API + Analyze sentiment dengan konten lengkap
"""

import json
from datetime import datetime
from typing import Optional, Dict, List

from .tradingview_news_fetcher import TradingViewNewsFetcher
from .enhanced_sentiment import EnhancedSentimentAnalyzer
from .news_model import NewsItem, NewsCollection, NewsProvider, RelatedSymbol


class CompleteNewsAnalyzer:
    """
    Complete analyzer: Fetch dari TradingView + Analyze sentiment
    """
    
    def __init__(self):
        self.fetcher = TradingViewNewsFetcher()
        self.sentiment_analyzer = EnhancedSentimentAnalyzer()
        self.news_collection = NewsCollection()
    
    def analyze_from_tradingview(
        self,
        symbol: str = "XAUUSD",
        limit: int = 20,
        type: str = "forex",
        fetch_delay: float = 0.5
    ) -> NewsCollection:
        """
        Fetch berita dari TradingView dan analyze sentiment
        
        Args:
            symbol: Symbol untuk filter (e.g., 'XAUUSD' for forex, 'GOLD' for commodity)
            limit: Jumlah berita maksimal
            type: 'forex' atau 'commodity'
            fetch_delay: Delay antar request (seconds)
        
        Returns:
            NewsCollection dengan sentiment analysis
        """
        print("\n" + "=" * 80)
        print(f"📰 COMPLETE NEWS ANALYSIS: {symbol}")
        print("=" * 80)
        
        # Fetch news dengan konten lengkap
        news_data = self.fetcher.fetch_news_with_content(
            symbol=symbol,
            limit=limit,
            type=type,
            delay=fetch_delay
        )
        
        if not news_data:
            print("❌ No news data fetched")
            return self.news_collection
        
        # Process dan analyze setiap berita
        print(f"\n📊 Analyzing sentiment for {len(news_data)} news items...\n")
        
        for i, item_data in enumerate(news_data, 1):
            # Create NewsItem
            news_item = self._create_news_item(item_data)
            
            # Get content untuk analysis
            content = item_data.get('full_content', '')
            
            # Analyze sentiment dari konten lengkap
            if content:
                sentiment_result = self.sentiment_analyzer.analyze(content)
                news_item.sentiment = sentiment_result['sentiment']
                news_item.sentiment_score = sentiment_result['score']
                news_item.sentiment_confidence = sentiment_result['confidence']
                
                print(f"[{i}/{len(news_data)}] {news_item.title[:60]}")
                print(f"  → {news_item.sentiment} (score: {news_item.sentiment_score}, conf: {news_item.sentiment_confidence})")
            else:
                print(f"[{i}/{len(news_data)}] ⚠️  No content: {news_item.title[:60]}")
            
            # Add to collection
            self.news_collection.add(news_item)
        
        print(f"\n✅ Analysis complete! {len(self.news_collection)} news items processed")
        return self.news_collection
    
    def _create_news_item(self, data: Dict) -> NewsItem:
        """
        Create NewsItem dari TradingView API response
        
        Args:
            data: Raw data dari API
        
        Returns:
            NewsItem object
        """
        # Provider
        provider_data = data.get('provider', {})
        provider = NewsProvider(
            id=provider_data.get('id', ''),
            name=provider_data.get('name', ''),
            logo_id=provider_data.get('logo_id', '')
        )
        
        # Related symbols
        symbols_data = data.get('relatedSymbols', [])
        symbols = [
            RelatedSymbol(
                symbol=s.get('symbol', ''),
                logoid=s.get('logoid', '')
            )
            for s in symbols_data
        ]
        
        # Create NewsItem
        return NewsItem(
            id=data.get('id', ''),
            title=data.get('title', ''),
            published=data.get('published', 0),
            urgency=data.get('urgency', 2),
            story_path=data.get('storyPath', ''),
            provider=provider,
            related_symbols=symbols,
            link=data.get('link'),
            permission=data.get('permission'),
            is_flash=data.get('is_flash', False)
        )
    
    def get_market_sentiment(self, symbol: Optional[str] = None) -> Dict:
        """
        Get overall market sentiment
        
        Args:
            symbol: Filter by specific symbol
        
        Returns:
            Dictionary dengan sentiment summary
        """
        collection = self.news_collection
        
        if symbol:
            collection = collection.filter_by_symbol(symbol)
        
        summary = collection.get_sentiment_summary()
        
        # Calculate weighted sentiment
        weighted_scores = []
        for item in collection.items:
            if item.sentiment_score is not None and item.sentiment_confidence is not None:
                weight = item.importance_score * item.sentiment_confidence
                weighted_scores.append(item.sentiment_score * weight)
        
        weighted_avg = sum(weighted_scores) / len(weighted_scores) if weighted_scores else 0
        
        # Determine overall sentiment
        if weighted_avg > 0.3:
            overall = 'BULLISH'
        elif weighted_avg < -0.3:
            overall = 'BEARISH'
        else:
            overall = 'NEUTRAL'
        
        return {
            'overall_sentiment': overall,
            'weighted_score': round(weighted_avg, 2),
            'news_count': summary['total'],
            'breakdown': {
                'bullish': summary['bullish'],
                'bearish': summary['bearish'],
                'neutral': summary['neutral']
            },
            'percentages': {
                'bullish': summary['bullish_pct'],
                'bearish': summary['bearish_pct'],
                'neutral': summary['neutral_pct']
            }
        }
    
    def get_top_news(self, limit: int = 10, high_priority_only: bool = False) -> List[NewsItem]:
        """
        Get top news items
        
        Args:
            limit: Maximum number of items
            high_priority_only: Only high priority news
        
        Returns:
            List of NewsItem
        """
        collection = self.news_collection
        
        if high_priority_only:
            collection = collection.filter_high_priority()
        
        collection = collection.sort_by_time(reverse=True)
        return collection.items[:limit]
    
    def export_results(self, filepath: str):
        """
        Export hasil analisis ke JSON file
        
        Args:
            filepath: Output file path
        """
        market_sentiment = self.get_market_sentiment()
        
        output = {
            'analyzed_at': datetime.now().isoformat(),
            'total_news': len(self.news_collection),
            'market_sentiment': market_sentiment,
            'news_items': [item.to_dict() for item in self.news_collection.items]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results exported to {filepath}")


if __name__ == "__main__":
    # Main demo
    analyzer = CompleteNewsAnalyzer()
    
    print("\n" + "=" * 80)
    print("COMPLETE NEWS ANALYSIS DEMO")
    print("=" * 80)
    
    # Analyze news dari TradingView
    collection = analyzer.analyze_from_tradingview(
        symbol="XAUUSD",
        type="forex",
        limit=10,  # Ambil 10 berita terbaru
        fetch_delay=1.0  # 1 detik delay antar request
    )
    
    # Show market sentiment
    print("\n" + "=" * 80)
    print("📊 MARKET SENTIMENT SUMMARY")
    print("=" * 80)
    
    sentiment = analyzer.get_market_sentiment()
    print(json.dumps(sentiment, indent=2))
    
    # Show top 5 news
    print("\n" + "=" * 80)
    print("🔥 TOP 5 RECENT NEWS")
    print("=" * 80)
    
    top_news = analyzer.get_top_news(limit=5)
    for i, news in enumerate(top_news, 1):
        print(f"\n{i}. [{news.published_str}] {news.provider.name}")
        print(f"   {news.title}")
        print(f"   Sentiment: {news.sentiment} (score: {news.sentiment_score}, confidence: {news.sentiment_confidence})")
        print(f"   Priority: {'🔴 HIGH' if news.is_high_priority else '🟢 Normal'}")
        print(f"   Importance: {news.importance_score:.2f}")
    
    # Export results
    print("\n" + "=" * 80)
    print("💾 EXPORTING RESULTS")
    print("=" * 80)
    
    analyzer.export_results(
        'd:/Code Programs/Tech Stack/TheoryBandarmology/server/api/data/comm_forex/analyzed_news.json'
    )
    
    print("\n✅ Analysis complete!")
