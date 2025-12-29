import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime
from ..helper.get_safe_info import get_safe_info

def analyze_news_narrative(stock_list: list):
    results = []
    
    for stock in stock_list:
        try:
            # Query spesifik ke Google News Indonesia
            rss_url = f"https://news.google.com/rss/search?q={stock}+saham+indonesia+when:7d&hl=id-ID&gl=ID&ceid=ID:id"
            feed = feedparser.parse(rss_url)
            
            news_items = []
            sentiment_score = 0
            
            # Keyword Mapping
            keywords = {
                "positive": ['laba', 'naik', 'melonjak', 'dividen', 'akuisisi', 'ekspansi', 'rekor', 'buyback', 'positif'],
                "negative": ['rugi', 'turun', 'anjlok', 'gugat', 'pkpu', 'utang', 'denda', 'suspend', 'negatif', 'koreksi'],
                "corporate_action": ['rups', 'dividen', 'right issue', 'stock split', 'merger', 'ipo']
            }

            # Ambil max 5 berita terakhir
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link
                pub_date = entry.published[:16] # Ambil tanggal saja
                
                title_lower = title.lower()
                
                # Deteksi Sentimen
                item_sentiment = "Neutral"
                if any(w in title_lower for w in keywords["positive"]):
                    item_sentiment = "Positive"
                    sentiment_score += 1
                elif any(w in title_lower for w in keywords["negative"]):
                    item_sentiment = "Negative"
                    sentiment_score -= 1
                
                # Deteksi Kategori
                category = "General"
                if any(w in title_lower for w in keywords["corporate_action"]):
                    category = "📢 Corp Action"
                elif "laba" in title_lower or "kuartal" in title_lower:
                    category = "💰 Earnings"
                
                news_items.append({
                    "title": title,
                    "link": link,
                    "date": pub_date,
                    "sentiment": item_sentiment,
                    "category": category
                })
            
            # Kesimpulan Narasi
            narrative_mood = "Neutral"
            if sentiment_score >= 2: narrative_mood = "Bullish Optimism"
            elif sentiment_score <= -2: narrative_mood = "Bearish Pessimism"

            results.append({
                "stock": stock,
                "news_count": len(news_items),
                "narrative_mood": narrative_mood,
                "headlines": news_items
            })
            
        except Exception as e:
            print(f"Error News {stock}: {e}")
            continue

    return results