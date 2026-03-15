"""
Data Models untuk News dari TradingView API
"""

from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class NewsProvider:
    """Model untuk provider berita"""
    id: str
    name: str
    logo_id: str
    
    @property
    def credibility_score(self) -> float:
        """
        Skor kredibilitas berdasarkan provider
        Reuters, Dow Jones = high credibility
        """
        high_credibility = ['reuters', 'dow-jones', 'bloomberg']
        medium_credibility = ['trading-economics', 'tradingview']
        
        if self.id in high_credibility:
            return 1.0
        elif self.id in medium_credibility:
            return 0.7
        else:
            return 0.5


@dataclass
class RelatedSymbol:
    """Model untuk simbol yang terkait dengan berita"""
    symbol: str
    logoid: str
    
    @property
    def exchange(self) -> str:
        """Extract exchange dari symbol (e.g., TVC:GOLD -> TVC)"""
        return self.symbol.split(':')[0] if ':' in self.symbol else ''
    
    @property
    def ticker(self) -> str:
        """Extract ticker dari symbol (e.g., TVC:GOLD -> GOLD)"""
        return self.symbol.split(':')[1] if ':' in self.symbol else self.symbol


@dataclass
class NewsItem:
    """Model untuk single news item dari TradingView"""
    id: str
    title: str
    published: int  # Unix timestamp
    urgency: int
    story_path: str
    provider: NewsProvider
    related_symbols: List[RelatedSymbol] = field(default_factory=list)
    link: Optional[str] = None
    permission: Optional[str] = None
    is_flash: bool = False
    
    # Sentiment analysis results (akan diisi setelah analisis)
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_confidence: Optional[float] = None
    
    @property
    def published_datetime(self) -> datetime:
        """Convert Unix timestamp ke datetime"""
        return datetime.fromtimestamp(self.published)
    
    @property
    def published_str(self) -> str:
        """Format datetime ke string yang readable"""
        return self.published_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def is_high_priority(self) -> bool:
        """Apakah berita ini high priority?"""
        return self.urgency == 1 or self.is_flash
    
    @property
    def importance_score(self) -> float:
        """
        Skor kepentingan berita (0.0 - 1.0)
        Berdasarkan: urgency, is_flash, provider credibility
        """
        base_score = 0.5
        
        # Urgency contribution
        if self.urgency == 1:
            base_score += 0.2
        
        # Flash news contribution
        if self.is_flash:
            base_score += 0.2
        
        # Provider credibility contribution
        base_score += self.provider.credibility_score * 0.1
        
        return min(1.0, base_score)
    
    def matches_symbol(self, target_symbol: str) -> bool:
        """Check apakah berita ini relevan dengan symbol tertentu"""
        target_symbol = target_symbol.upper()
        for sym in self.related_symbols:
            if target_symbol in sym.symbol.upper() or target_symbol in sym.ticker.upper():
                return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert ke dictionary untuk JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'published': self.published,
            'published_str': self.published_str,
            'urgency': self.urgency,
            'is_flash': self.is_flash,
            'is_high_priority': self.is_high_priority,
            'importance_score': self.importance_score,
            'link': self.link,
            'provider': {
                'id': self.provider.id,
                'name': self.provider.name,
                'credibility': self.provider.credibility_score
            },
            'related_symbols': [
                {'symbol': s.symbol, 'ticker': s.ticker, 'exchange': s.exchange}
                for s in self.related_symbols
            ],
            'sentiment': {
                'label': self.sentiment,
                'score': self.sentiment_score,
                'confidence': self.sentiment_confidence
            } if self.sentiment else None
        }
    
    @classmethod
    def from_api_response(cls, data: Dict) -> 'NewsItem':
        """
        Create NewsItem dari raw API response
        
        Args:
            data: Dictionary dari TradingView API
        
        Returns:
            NewsItem instance
        """
        provider_data = data.get('provider', {})
        provider = NewsProvider(
            id=provider_data.get('id', ''),
            name=provider_data.get('name', ''),
            logo_id=provider_data.get('logo_id', '')
        )
        
        symbols_data = data.get('relatedSymbols', [])
        symbols = [
            RelatedSymbol(
                symbol=s.get('symbol', ''),
                logoid=s.get('logoid', '')
            )
            for s in symbols_data
        ]
        
        return cls(
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


@dataclass
class NewsCollection:
    """Collection of news items dengan utility methods"""
    items: List[NewsItem] = field(default_factory=list)
    
    def add(self, item: NewsItem):
        """Add news item ke collection"""
        self.items.append(item)
    
    def filter_by_symbol(self, symbol: str) -> 'NewsCollection':
        """Filter news berdasarkan symbol"""
        filtered = [item for item in self.items if item.matches_symbol(symbol)]
        return NewsCollection(items=filtered)
    
    def filter_by_sentiment(self, sentiment: str) -> 'NewsCollection':
        """Filter news berdasarkan sentiment"""
        filtered = [item for item in self.items if item.sentiment == sentiment]
        return NewsCollection(items=filtered)
    
    def filter_high_priority(self) -> 'NewsCollection':
        """Filter hanya high priority news"""
        filtered = [item for item in self.items if item.is_high_priority]
        return NewsCollection(items=filtered)
    
    def sort_by_time(self, reverse=True) -> 'NewsCollection':
        """Sort by published time (newest first by default)"""
        sorted_items = sorted(self.items, key=lambda x: x.published, reverse=reverse)
        return NewsCollection(items=sorted_items)
    
    def get_sentiment_summary(self) -> Dict:
        """Get summary of sentiments"""
        total = len(self.items)
        if total == 0:
            return {
                'total': 0,
                'bullish': 0,
                'bullish_pct': 0.0,
                'bearish': 0,
                'bearish_pct': 0.0,
                'neutral': 0,
                'neutral_pct': 0.0,
                'avg_score': 0.0
            }
        
        bullish = sum(1 for item in self.items if item.sentiment == 'BULLISH')
        bearish = sum(1 for item in self.items if item.sentiment == 'BEARISH')
        neutral = sum(1 for item in self.items if item.sentiment == 'NEUTRAL')
        
        return {
            'total': total,
            'bullish': bullish,
            'bullish_pct': round(bullish / total * 100, 1),
            'bearish': bearish,
            'bearish_pct': round(bearish / total * 100, 1),
            'neutral': neutral,
            'neutral_pct': round(neutral / total * 100, 1),
            'avg_score': round(sum(item.sentiment_score or 0 for item in self.items) / total, 2)
        }
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
