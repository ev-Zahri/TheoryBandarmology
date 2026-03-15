# 📡 API Documentation - Forex & Commodity News

## Base URL
```
http://localhost:8000
```

---

## 🔹 Endpoints

### 1. Get News List (Raw Data)

**Endpoint**: `GET /v1/{symbol}/get-news`

**Description**: Mengambil seluruh berita dari TradingView dengan konten lengkap (tanpa analisis sentiment)

**Parameters**:
- `symbol` (path, required): Symbol untuk filter berita
  - Forex: `XAUUSD`, `EURUSD`, `GBPUSD`, dll
  - Commodity: `GOLD`, `SILVER`, `OIL`, dll
- `limit` (query, optional): Jumlah berita maksimal (default: 20)
- `type` (query, optional): Tipe symbol - `forex` atau `commodity` (default: `forex`)

**Example Request**:
```bash
# Forex
GET http://localhost:8000/v1/XAUUSD/get-news?limit=10&type=forex

# Commodity
GET http://localhost:8000/v1/GOLD/get-news?limit=10&type=commodity
```

**Example Response**:
```json
{
  "message": "Daftar berita berhasil diambil",
  "symbol": "XAUUSD",
  "type": "forex",
  "total_items": 10,
  "data": [
    {
      "id": "DJN_DN20251228000898:0",
      "title": "Gold Climbs Above $4,500/oz for First Time",
      "published": 1735372800,
      "urgency": 1,
      "permission": "headline",
      "relatedSymbols": [
        {
          "symbol": "FX:XAUUSD",
          "logoid": "metal/gold"
        }
      ],
      "storyPath": "/news/...",
      "provider": {
        "id": "dow-jones",
        "name": "Dow Jones Newswires",
        "logo_id": "dow-jones-newswires"
      },
      "full_content": "Gold prices climbed to a record high above $4,500 per ounce...",
      "detail": {
        "short_description": "...",
        "ast_description": {...}
      }
    }
  ],
  "status_code": 200
}
```

---

### 2. Get News Sentiment Analysis

**Endpoint**: `GET /v1/{symbol}/news-sentiment`

**Description**: Menganalisa sentiment berita dari TradingView dengan market sentiment summary

**Parameters**:
- `symbol` (path, required): Symbol untuk filter berita
- `limit` (query, optional): Jumlah berita maksimal (default: 20)
- `type` (query, optional): Tipe symbol - `forex` atau `commodity` (default: `forex`)

**Example Request**:
```bash
# Forex
GET http://localhost:8000/v1/XAUUSD/news-sentiment?limit=20&type=forex

# Commodity
GET http://localhost:8000/v1/GOLD/news-sentiment?limit=20&type=commodity
```

**Example Response**:
```json
{
  "message": "Data sentimen berita berhasil diambil",
  "symbol": "XAUUSD",
  "type": "forex",
  "market_sentiment": {
    "overall_sentiment": "BULLISH",
    "weighted_score": 0.52,
    "news_count": 20,
    "breakdown": {
      "bullish": 13,
      "bearish": 4,
      "neutral": 3
    },
    "percentages": {
      "bullish": 65.0,
      "bearish": 20.0,
      "neutral": 15.0
    }
  },
  "top_news": [
    {
      "id": "DJN_DN20251228000898:0",
      "title": "Gold Climbs Above $4,500/oz for First Time",
      "published": "2025-12-28 15:30:00",
      "sentiment": "BULLISH",
      "sentiment_score": 0.8,
      "sentiment_confidence": 0.9,
      "importance_score": 0.85,
      "is_high_priority": true,
      "provider": "Dow Jones Newswires",
      "urgency": 1
    }
  ],
  "status_code": 200
}
```

---

## 📊 Response Fields Explanation

### Market Sentiment
- `overall_sentiment`: Overall market sentiment (`BULLISH`, `BEARISH`, `NEUTRAL`)
- `weighted_score`: Weighted average score (-1.0 to 1.0)
- `news_count`: Total number of news analyzed
- `breakdown`: Count by sentiment type
- `percentages`: Percentage by sentiment type

### News Item
- `id`: Unique news ID
- `title`: News headline
- `published`: Published timestamp (Unix or formatted string)
- `sentiment`: Sentiment label (`BULLISH`, `BEARISH`, `NEUTRAL`)
- `sentiment_score`: Sentiment score (-1.0 to 1.0)
- `sentiment_confidence`: Confidence level (0.0 to 1.0)
- `importance_score`: Calculated importance (0.0 to 1.0)
- `is_high_priority`: High priority flag (urgency 1)
- `provider`: News provider name
- `urgency`: Urgency level (1 = high, 2 = normal, 3 = low)

---

## 🚀 Usage Examples

### JavaScript (Fetch API)
```javascript
// Get news list
const getNews = async (symbol, limit = 20, type = 'forex') => {
  const response = await fetch(
    `http://localhost:8000/v1/${symbol}/get-news?limit=${limit}&type=${type}`
  );
  const data = await response.json();
  return data;
};

// Get sentiment analysis
const getSentiment = async (symbol, limit = 20, type = 'forex') => {
  const response = await fetch(
    `http://localhost:8000/v1/${symbol}/news-sentiment?limit=${limit}&type=${type}`
  );
  const data = await response.json();
  return data;
};

// Usage
const newsData = await getNews('XAUUSD', 10, 'forex');
const sentimentData = await getSentiment('XAUUSD', 20, 'forex');

console.log('Market Sentiment:', sentimentData.market_sentiment.overall_sentiment);
console.log('Weighted Score:', sentimentData.market_sentiment.weighted_score);
```

### Python (Requests)
```python
import requests

BASE_URL = "http://localhost:8000"

# Get news list
def get_news(symbol, limit=20, type='forex'):
    response = requests.get(
        f"{BASE_URL}/v1/{symbol}/get-news",
        params={'limit': limit, 'type': type}
    )
    return response.json()

# Get sentiment analysis
def get_sentiment(symbol, limit=20, type='forex'):
    response = requests.get(
        f"{BASE_URL}/v1/{symbol}/news-sentiment",
        params={'limit': limit, 'type': type}
    )
    return response.json()

# Usage
news_data = get_news('XAUUSD', limit=10, type='forex')
sentiment_data = get_sentiment('XAUUSD', limit=20, type='forex')

print('Market Sentiment:', sentiment_data['market_sentiment']['overall_sentiment'])
print('Weighted Score:', sentiment_data['market_sentiment']['weighted_score'])
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "Simbol tidak boleh kosong"
}
```

### 404 Not Found
```json
{
  "detail": "Daftar berita tidak ditemukan untuk simbol XAUUSD"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Server error: Connection timeout"
}
```

---

## 💡 Best Practices

1. **Rate Limiting**: Jangan request terlalu sering (min 1 detik antar request)
2. **Caching**: Cache hasil untuk beberapa menit untuk mengurangi load
3. **Error Handling**: Always handle errors dengan try-catch
4. **Limit**: Gunakan limit yang reasonable (10-20 untuk real-time, 50-100 untuk batch)
5. **Type Parameter**: Pastikan gunakan type yang benar (`forex` atau `commodity`)

---

## 📝 Symbol Examples

### Forex
- `XAUUSD` - Gold vs USD
- `EURUSD` - Euro vs USD
- `GBPUSD` - Pound vs USD
- `USDJPY` - USD vs Yen

### Commodity
- `GOLD` - Gold
- `SILVER` - Silver
- `OIL` - Crude Oil
- `NATGAS` - Natural Gas

---

**Last Updated**: 2025-12-29  
**API Version**: 1.0.0
