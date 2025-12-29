"""
Example: Perbandingan Analisis Judul vs Konten Lengkap
Menunjukkan perbedaan akurasi antara kedua metode
"""

import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service_comm_forex.news_analyzer import NewsAnalyzer
from service_comm_forex.news_model import NewsItem


def compare_analysis_methods():
    """
    Membandingkan hasil analisis dari judul saja vs konten lengkap
    """
    
    sample_file = 'd:/Code Programs/Tech Stack/TheoryBandarmology/server/api/data/sample.json'
    
    print("=" * 80)
    print("PERBANDINGAN: Analisis Judul vs Konten Lengkap")
    print("=" * 80)
    
    # ========== METHOD 1: Title Only (Cepat) ==========
    print("\n\n🚀 METHOD 1: QUICK ANALYSIS (Title Only)")
    print("-" * 80)
    
    analyzer_quick = NewsAnalyzer(fetch_content=False)
    collection_quick = analyzer_quick.load_from_file(sample_file)
    
    # Ambil 5 berita pertama untuk Gold
    quick_news = collection_quick.filter_by_symbol('GOLD').sort_by_time(reverse=True).items[:5]
    
    print(f"\nAnalyzed {len(quick_news)} news items (Title Only):\n")
    for i, news in enumerate(quick_news, 1):
        print(f"{i}. {news.title}")
        print(f"   Sentiment: {news.sentiment} (score: {news.sentiment_score}, confidence: {news.sentiment_confidence})")
        print()
    
    quick_sentiment = analyzer_quick.get_market_sentiment(symbol='GOLD', hours=24)
    print("\n📊 Market Sentiment Summary (Title Only):")
    print(json.dumps(quick_sentiment, indent=2))
    
    
    # ========== METHOD 2: Full Content (Akurat tapi Lambat) ==========
    print("\n\n" + "=" * 80)
    print("🔍 METHOD 2: DEEP ANALYSIS (Full Content)")
    print("-" * 80)
    print("\n⚠️  Note: Ini akan fetch konten lengkap dari setiap berita")
    print("⏱️  Proses akan lebih lambat tapi lebih akurat\n")
    
    # Tanya user apakah mau lanjut
    response = input("Lanjutkan dengan deep analysis? (y/n): ").lower()
    
    if response != 'y':
        print("\n❌ Deep analysis dibatalkan")
        return
    
    analyzer_deep = NewsAnalyzer(fetch_content=True)
    
    # Load dan analyze dengan konten lengkap (hanya 5 berita untuk demo)
    with open(sample_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ambil hanya 5 berita pertama untuk demo
    limited_data = {
        'items': data['items'][:5]
    }
    
    collection_deep = analyzer_deep.process_api_response(limited_data, deep_analysis=True)
    
    deep_news = collection_deep.items
    
    print(f"\n\nAnalyzed {len(deep_news)} news items (Full Content):\n")
    for i, news in enumerate(deep_news, 1):
        print(f"{i}. {news.title}")
        print(f"   Sentiment: {news.sentiment} (score: {news.sentiment_score}, confidence: {news.sentiment_confidence})")
        
        # Show content preview if available
        if news.id in analyzer_deep.content_cache:
            content = analyzer_deep.content_cache[news.id]
            print(f"   Content preview: {content[:150]}...")
        print()
    
    deep_sentiment = analyzer_deep.get_market_sentiment()
    print("\n📊 Market Sentiment Summary (Full Content):")
    print(json.dumps(deep_sentiment, indent=2))
    
    
    # ========== COMPARISON ==========
    print("\n\n" + "=" * 80)
    print("📈 COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"\nTitle Only Analysis:")
    print(f"  Overall Sentiment: {quick_sentiment['overall_sentiment']}")
    print(f"  Weighted Score: {quick_sentiment['weighted_score']}")
    print(f"  Bullish: {quick_sentiment['percentages']['bullish']}%")
    print(f"  Bearish: {quick_sentiment['percentages']['bearish']}%")
    print(f"  Neutral: {quick_sentiment['percentages']['neutral']}%")
    
    print(f"\nFull Content Analysis:")
    print(f"  Overall Sentiment: {deep_sentiment['overall_sentiment']}")
    print(f"  Weighted Score: {deep_sentiment['weighted_score']}")
    print(f"  Bullish: {deep_sentiment['percentages']['bullish']}%")
    print(f"  Bearish: {deep_sentiment['percentages']['bearish']}%")
    print(f"  Neutral: {deep_sentiment['percentages']['neutral']}%")
    
    print("\n" + "=" * 80)
    print("💡 KESIMPULAN:")
    print("=" * 80)
    print("""
1. TITLE ONLY (Quick):
   ✅ Sangat cepat (instant)
   ✅ Tidak perlu network request
   ❌ Kurang akurat (hanya dari headline)
   ❌ Bisa misleading jika judul clickbait
   
2. FULL CONTENT (Deep):
   ✅ Lebih akurat (analisis konten lengkap)
   ✅ Menangkap nuansa yang tidak ada di judul
   ❌ Lebih lambat (perlu fetch setiap artikel)
   ❌ Bisa kena rate limiting jika terlalu banyak
   
REKOMENDASI:
- Gunakan TITLE ONLY untuk monitoring real-time
- Gunakan FULL CONTENT untuk analisis mendalam sebelum trading decision
- Kombinasi: Quick scan dulu, lalu deep analysis untuk berita penting saja
    """)


def demo_hybrid_approach():
    """
    Demo pendekatan hybrid: Quick scan + selective deep analysis
    """
    
    print("\n\n" + "=" * 80)
    print("🎯 HYBRID APPROACH DEMO")
    print("=" * 80)
    print("\nStrategi: Quick scan semua berita, deep analysis untuk high priority saja\n")
    
    sample_file = 'd:/Code Programs/Tech Stack/TheoryBandarmology/server/api/data/sample.json'
    
    # Step 1: Quick scan semua berita
    print("Step 1: Quick scan all news...")
    analyzer = NewsAnalyzer(fetch_content=False)
    collection = analyzer.load_from_file(sample_file)
    
    # Filter high priority news
    high_priority = collection.filter_high_priority().filter_by_symbol('GOLD')
    
    print(f"Found {len(high_priority)} high priority news for GOLD")
    
    # Step 2: Deep analysis untuk high priority saja
    if len(high_priority) > 0:
        print(f"\nStep 2: Deep analysis for {min(3, len(high_priority))} high priority news...")
        
        analyzer_deep = NewsAnalyzer(fetch_content=True)
        
        # Ambil 3 berita high priority pertama
        priority_items = high_priority.items[:3]
        
        for news in priority_items:
            print(f"\n🔴 HIGH PRIORITY: {news.title}")
            
            # Fetch content
            content = analyzer_deep.content_fetcher.fetch_content(news)
            
            if content:
                # Re-analyze dengan konten lengkap
                sentiment_result = analyzer_deep.sentiment_analyzer.analyze(content)
                
                print(f"   Title-based: {news.sentiment} (score: {news.sentiment_score})")
                print(f"   Content-based: {sentiment_result['sentiment']} (score: {sentiment_result['score']})")
                
                if news.sentiment != sentiment_result['sentiment']:
                    print(f"   ⚠️  SENTIMENT CHANGED! Title vs Content berbeda")
            else:
                print(f"   ❌ Could not fetch content")
    
    print("\n✅ Hybrid analysis complete!")


if __name__ == "__main__":
    # Run comparison
    compare_analysis_methods()
    
    # Optional: Run hybrid demo
    print("\n\n")
    response = input("Jalankan Hybrid Approach Demo? (y/n): ").lower()
    if response == 'y':
        demo_hybrid_approach()
