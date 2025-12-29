# 📁 Struktur Folder & File Guide

## ✅ File yang DIPERLUKAN (Core System)

### 1. **complete_news_analyzer.py** ⭐ MAIN
**Purpose**: Main analyzer yang menggabungkan fetching + sentiment analysis  
**Usage**: `from api.service_comm_forex import CompleteNewsAnalyzer`  
**Dependencies**: tradingview_news_fetcher, enhanced_sentiment, news_model

### 2. **tradingview_news_fetcher.py** 🔧 CORE
**Purpose**: Fetch berita dari TradingView API dengan konten lengkap  
**API Endpoints**:
- `news-mediator.tradingview.com/public/view/v1/symbol` - List berita
- `news-mediator.tradingview.com/public/news/v1/story` - Detail berita

### 3. **enhanced_sentiment.py** 🧠 CORE
**Purpose**: Advanced sentiment analysis dengan weighted scoring  
**Features**:
- Weighted keywords (strong/moderate)
- Negation handling
- Confidence scoring

### 4. **news_model.py** 📊 CORE
**Purpose**: Data models (NewsItem, NewsCollection, dll)  
**Classes**:
- `NewsItem` - Single news item
- `NewsCollection` - Collection dengan filtering
- `NewsProvider` - Provider info
- `RelatedSymbol` - Symbol info

### 5. **__init__.py** 📦 EXPORT
**Purpose**: Clean exports untuk package  
**Exports**: CompleteNewsAnalyzer, TradingViewNewsFetcher, dll

---

## ⚠️ File yang DEPRECATED (Bisa Dihapus)

### ❌ **analyze_sentiment.py**
**Reason**: Digantikan oleh `enhanced_sentiment.py`  
**Status**: Legacy, simple keyword matching  
**Action**: Bisa dihapus setelah migrasi

### ❌ **news_analyzer.py**
**Reason**: Digantikan oleh `complete_news_analyzer.py`  
**Status**: Old approach (scraping-based)  
**Action**: Bisa dihapus

### ❌ **news_content_fetcher.py**
**Reason**: Digantikan oleh `tradingview_news_fetcher.py`  
**Status**: HTML scraping approach (tidak reliable)  
**Action**: Bisa dihapus

### ⚠️ **news_narrative.py**
**Reason**: Streaming approach (berbeda use case)  
**Status**: Bisa dipertahankan untuk real-time monitoring  
**Action**: Keep jika butuh streaming, hapus jika tidak

---

## 📚 File Dokumentasi

### ✅ **README.md**
**Purpose**: Main documentation  
**Content**: Usage guide, API reference, examples  
**Status**: Keep & update

### ✅ **STRUCTURE.md** (file ini)
**Purpose**: Struktur folder & file guide  
**Status**: Keep

---

## 🗂️ Struktur Folder Recommended

```
service_comm_forex/
├── __init__.py                      ✅ Package exports
├── complete_news_analyzer.py        ✅ Main analyzer
├── tradingview_news_fetcher.py      ✅ API fetcher
├── enhanced_sentiment.py            ✅ Sentiment analyzer
├── news_model.py                    ✅ Data models
├── README.md                        ✅ Documentation
├── STRUCTURE.md                     ✅ This file
│
├── news_narrative.py                ⚠️  Optional (streaming)
│
└── [DEPRECATED - Bisa Dihapus]
    ├── analyze_sentiment.py         ❌ Old sentiment
    ├── news_analyzer.py             ❌ Old analyzer
    └── news_content_fetcher.py      ❌ Old fetcher
```

---

## 🚀 Migration Guide

### Dari Old System ke New System:

**Old (analyze_sentiment.py):**
```python
from analyze_sentiment import analyze_sentiment
sentiment = analyze_sentiment(title)  # Simple
```

**New (enhanced_sentiment.py):**
```python
from api.service_comm_forex import EnhancedSentimentAnalyzer
analyzer = EnhancedSentimentAnalyzer()
result = analyzer.analyze(content)  # Advanced
# result = {'sentiment': 'BULLISH', 'score': 0.8, 'confidence': 0.9}
```

**Old (news_analyzer.py):**
```python
from news_analyzer import NewsAnalyzer
analyzer = NewsAnalyzer(fetch_content=True)  # Scraping
```

**New (complete_news_analyzer.py):**
```python
from api.service_comm_forex import CompleteNewsAnalyzer
analyzer = CompleteNewsAnalyzer()
collection = analyzer.analyze_from_tradingview(symbol="XAUUSD")  # API
```

---

## 🧹 Cleanup Steps

1. **Backup dulu** (jika perlu):
   ```bash
   mkdir deprecated
   mv analyze_sentiment.py deprecated/
   mv news_analyzer.py deprecated/
   mv news_content_fetcher.py deprecated/
   ```

2. **Update imports** di file lain:
   - Ganti `from analyze_sentiment import` → `from .enhanced_sentiment import`
   - Ganti `from news_analyzer import` → `from .complete_news_analyzer import`

3. **Test** setelah cleanup:
   ```bash
   python -m api.service_comm_forex.complete_news_analyzer
   ```

4. **Hapus deprecated** jika semua berjalan OK:
   ```bash
   rm deprecated/*
   ```

---

## 📝 Summary

**Keep (5 files):**
1. ✅ `complete_news_analyzer.py`
2. ✅ `tradingview_news_fetcher.py`
3. ✅ `enhanced_sentiment.py`
4. ✅ `news_model.py`
5. ✅ `__init__.py`

**Optional (1 file):**
6. ⚠️ `news_narrative.py` (jika butuh streaming)

**Delete (3 files):**
7. ❌ `analyze_sentiment.py`
8. ❌ `news_analyzer.py`
9. ❌ `news_content_fetcher.py`

**Total: 5-6 core files** (dari 10 files sebelumnya)

---

**Last Updated**: 2025-12-29  
**Version**: 2.0.0
