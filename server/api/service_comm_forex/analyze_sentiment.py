
def analyze_sentiment(text):
    positive_words = ['record', 'higher', 'bullish', 'demand', 'growth', 'rise']
    negative_words = ['drop', 'fall', 'bearish', 'weak', 'lower', 'plunge']
    
    text = text.lower()
    score = 0
    for word in positive_words:
        if word in text: score += 1
    for word in negative_words:
        if word in text: score -= 1
        
    status = "NEUTRAL"
    if score > 0: status = "BULLISH"
    if score < 0: status = "BEARISH"
    
    return status