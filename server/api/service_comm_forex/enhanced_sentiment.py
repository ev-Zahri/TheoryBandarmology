"""
Enhanced Sentiment Analysis untuk Forex & Commodity News
Menggunakan keyword-based analysis dengan scoring yang lebih detail
"""

class EnhancedSentimentAnalyzer:
    def __init__(self):
        # Kata-kata bullish dengan bobot berbeda
        self.bullish_strong = [
            'surge', 'soar', 'rocket', 'rally', 'boom', 'breakout', 
            'record high', 'all-time high', 'fresh record', 'new high',
            'strong gains', 'sharp rise', 'significant increase'
        ]
        
        self.bullish_moderate = [
            'rise', 'gain', 'higher', 'up', 'climb', 'advance', 'increase',
            'bullish', 'positive', 'growth', 'demand', 'strength', 'support',
            'upward', 'momentum', 'recovery', 'rebound'
        ]
        
        # Kata-kata bearish dengan bobot berbeda
        self.bearish_strong = [
            'crash', 'plunge', 'collapse', 'tumble', 'slump', 'plummet',
            'sharp decline', 'significant drop', 'heavy losses', 'sell-off'
        ]
        
        self.bearish_moderate = [
            'fall', 'drop', 'lower', 'down', 'decline', 'decrease', 'slip',
            'bearish', 'negative', 'weak', 'weakness', 'pressure', 'concern',
            'downward', 'retreat', 'pullback', 'correction'
        ]
        
        # Kata-kata netral/stabilitas
        self.neutral_words = [
            'steady', 'stable', 'flat', 'unchanged', 'consolidate',
            'sideways', 'range-bound', 'mixed', 'await', 'hold'
        ]
        
        # Kata-kata yang mengindikasikan ketidakpastian
        self.uncertainty_words = [
            'may', 'might', 'could', 'uncertain', 'unclear', 'mixed signals',
            'volatility', 'volatile', 'fluctuate'
        ]
        
        # Negation words - membalik sentiment
        self.negation_words = ['not', 'no', 'never', 'without', 'lack']
    
    def analyze(self, text):
        """
        Menganalisis sentiment dari teks berita
        
        Returns:
            dict: {
                'sentiment': 'BULLISH' | 'BEARISH' | 'NEUTRAL',
                'score': float (-1.0 to 1.0),
                'confidence': float (0.0 to 1.0),
                'keywords': list of matched keywords
            }
        """
        if not text:
            return self._create_result('NEUTRAL', 0.0, 0.0, [])
        
        text_lower = text.lower()
        words = text_lower.split()
        
        score = 0.0
        matched_keywords = []
        
        # Check for negation context
        has_negation = any(neg in words for neg in self.negation_words)
        
        # Score bullish strong (weight: 3)
        for word in self.bullish_strong:
            if word in text_lower:
                weight = -3 if has_negation else 3
                score += weight
                matched_keywords.append(f"+++ {word}")
        
        # Score bullish moderate (weight: 1)
        for word in self.bullish_moderate:
            if word in text_lower:
                weight = -1 if has_negation else 1
                score += weight
                matched_keywords.append(f"+ {word}")
        
        # Score bearish strong (weight: -3)
        for word in self.bearish_strong:
            if word in text_lower:
                weight = 3 if has_negation else -3
                score += weight
                matched_keywords.append(f"--- {word}")
        
        # Score bearish moderate (weight: -1)
        for word in self.bearish_moderate:
            if word in text_lower:
                weight = 1 if has_negation else -1
                score += weight
                matched_keywords.append(f"- {word}")
        
        # Check neutral words
        neutral_count = sum(1 for word in self.neutral_words if word in text_lower)
        if neutral_count > 0:
            matched_keywords.append(f"= neutral ({neutral_count})")
        
        # Check uncertainty
        uncertainty_count = sum(1 for word in self.uncertainty_words if word in text_lower)
        
        # Normalize score to -1.0 to 1.0 range
        normalized_score = max(-1.0, min(1.0, score / 10.0))
        
        # Calculate confidence based on number of keywords and uncertainty
        keyword_strength = min(1.0, len(matched_keywords) / 5.0)
        uncertainty_penalty = uncertainty_count * 0.1
        confidence = max(0.0, min(1.0, keyword_strength - uncertainty_penalty))
        
        # Determine sentiment
        if abs(normalized_score) < 0.2 or neutral_count >= 2:
            sentiment = 'NEUTRAL'
        elif normalized_score > 0:
            sentiment = 'BULLISH'
        else:
            sentiment = 'BEARISH'
        
        return self._create_result(sentiment, normalized_score, confidence, matched_keywords)
    
    def _create_result(self, sentiment, score, confidence, keywords):
        """Helper untuk membuat result dictionary"""
        return {
            'sentiment': sentiment,
            'score': round(score, 2),
            'confidence': round(confidence, 2),
            'keywords': keywords
        }
    
    def get_sentiment_label(self, score):
        """Konversi score ke label yang lebih deskriptif"""
        if score >= 0.6:
            return 'VERY BULLISH'
        elif score >= 0.2:
            return 'BULLISH'
        elif score <= -0.6:
            return 'VERY BEARISH'
        elif score <= -0.2:
            return 'BEARISH'
        else:
            return 'NEUTRAL'


# Fungsi helper untuk backward compatibility
def analyze_sentiment(text):
    """Simple function untuk compatibility dengan kode lama"""
    analyzer = EnhancedSentimentAnalyzer()
    result = analyzer.analyze(text)
    return result['sentiment']


if __name__ == "__main__":
    # Testing
    analyzer = EnhancedSentimentAnalyzer()
    
    test_cases = [
        "Gold Climbs Above $4,500/oz for First Time Amid Rising Geopolitical Tensions",
        "Gold Pulls Back Slightly",
        "Comex Gold Settles 0.05% Lower at $4480.60",
        "Safe-haven gold ventures beyond $4,500/oz for the first time",
        "Gold steady as investors focus on US rate policy next year",
        "Gold prices not showing significant growth despite demand"
    ]
    
    print("=== Enhanced Sentiment Analysis Test ===\n")
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']} (score: {result['score']}, confidence: {result['confidence']})")
        print(f"Keywords: {', '.join(result['keywords'])}")
        print()
