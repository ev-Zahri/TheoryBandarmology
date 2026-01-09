from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.service_stock.analyzer import process_broker_data
from api.service_stock.technical_analyze import calculate_advanced_technical
from api.service_stock.quant_technical import calculate_quant_metrics
from api.service_stock.financial_health import analyze_financial_health
from api.service_stock.news_narrative import analyze_news_narrative
from api.service_stock.company_profile import get_company_profile
from api.service_comm_forex.complete_news_analyzer import CompleteNewsAnalyzer
from api.service_comm_forex.tradingview_news_fetcher import TradingViewNewsFetcher
from api.service_comm_forex.news_cache import news_cache
from api.service_stock.broker_summary.broker_summary import parse_xhr_response, validate_json_structure
from typing import Dict, List
import json

app = FastAPI()

origin = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for stock analysis
class StockAnalysisRequest(BaseModel):
    stocks: List[str]

# Endpoint untuk analisis data broker - menerima JSON langsung
@app.post("/v1/stock/analyze")
async def analyze_data(request: Request):
    try:
        body = await request.json()
        
        if not body:
            raise HTTPException(status_code=400, detail="JSON tidak boleh kosong.")
        
        raw_json_str = json.dumps(body)
        result = process_broker_data(raw_json_str)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])

        return {
            "message": "Data berhasil di analisis", 
            "data": result,
            "status_code": 200
        }
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON tidak valid: {str(e)}")

@app.post('/v1/stock/analyze/technical')
async def analyze_technical(request: StockAnalysisRequest):
    try: 
        if not request.stocks:
            raise HTTPException(status_code=400, detail="List saham tidak boleh kosong")
        
        data = calculate_advanced_technical(request.stocks)

        if not data:
            raise HTTPException(status_code=404, detail="Data teknikal tidak ditemukan untuk saham tersebut")

        print(f"Response technical {data}")

        return {
            "message": "Analisis teknikal berhasil", 
            "data": data,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Endpoint untuk analisis kuantitatif (Z-Score, ATR, Pivot Points)
@app.post('/v1/stock/analyze/quant')
async def analyze_quant(request: StockAnalysisRequest):
    try: 
        if not request.stocks:
            raise HTTPException(status_code=400, detail="List saham tidak boleh kosong")
        
        data = calculate_quant_metrics(request.stocks)

        if not data:
            raise HTTPException(status_code=404, detail="Data kuantitatif tidak ditemukan untuk saham tersebut")

        return {
            "message": "Analisis kuantitatif berhasil", 
            "data": data,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post('/v1/stock/analyze/fundamental')
async def get_financial(request: StockAnalysisRequest):
    try:
        if not request.stocks:
            raise HTTPException(status_code=400, detail="List saham tidak boleh kosong")
        
        data = analyze_financial_health(request.stocks)

        if not data:
            raise HTTPException(status_code=400, detail="Data kesehatan finansial tidak ditemukan untuk saham tersebut")
        
        return {
            "message": "Analisis kuantitatif berhasil", 
            "data": data,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post('/v1/stock/analyze/news')
async def analyze_news(request: StockAnalysisRequest):
    try:
        if not request.stocks:
            raise HTTPException(status_code=400, detail="List saham tidak boleh kosong")
        
        data = analyze_news_narrative(request.stocks)

        if not data:
            raise HTTPException(status_code=404, detail="Data narasi berita tidak ditemukan untuk saham tersebut")
        
        return {
            "message": "Analisis narasi berita berhasil", 
            "data": data,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get('/v1/stock/company-profile/{stock_code}')
def get_insight(stock_code: str):
    try:
        if not stock_code:
            raise HTTPException(status_code=400, detail="Kode saham tidak boleh kosong")
        
        data = get_company_profile(stock_code)
        if not data:
            raise HTTPException(status_code=404, detail="Data profil tidak ditemukan untuk saham tersebut")
        
        return {
            "message": "Profil Perusahaan berhasil diambil", 
            "data": data,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Endpoint untuk Import recent data broker summary
@app.post("/v1/stock/import-recent-data")
async def import_recent_data(request: Request):
    body = await request.json()
    return {"message": "Data berhasil di import"}


# Endpoint untuk upload broker summary file (XHR intercepted data)
@app.post("/v1/stock/broker-summary/upload")
async def upload_broker_summary(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400, 
                detail="File harus berformat JSON (.json)"
            )
        
        # Read file content
        content = await file.read()
        
        # Validate file size (max 10MB)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Ukuran file terlalu besar. Maksimal 10MB"
            )
        
        # Parse JSON
        try:
            json_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"File JSON tidak valid: {str(e)}"
            )
        
        # Validate structure
        if not validate_json_structure(json_data):
            raise HTTPException(
                status_code=400,
                detail="Struktur JSON tidak sesuai. Pastikan file berisi data XHR dari Stockbit broker summary."
            )
        
        # Process data
        result = parse_xhr_response(json_data)
        
        return {
            "message": "File broker summary berhasil diproses",
            "data": result,
            "status_code": 200
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


# =============== API untuk FOREX dan COMMODITY ====================
@app.get("/v1/{symbol}/get-news")
async def get_all_news(symbol: str, limit: int = 20, type: str = "forex"):
    try:
        if not symbol:
            raise HTTPException(status_code=400, detail="Simbol tidak boleh kosong")
        
        # Check cache first
        cached_news = news_cache.get(symbol, type, limit)
        if cached_news:
            return {
                "message": "Daftar berita berhasil diambil (from cache)", 
                "symbol": symbol,
                "type": type,
                "total_items": len(cached_news),
                "data": cached_news,
                "cached": True,
                "status_code": 200
            }
        
        # Cache miss - fetch from TradingView
        fetcher = TradingViewNewsFetcher()
        news_data = fetcher.fetch_news_with_content(
            symbol=symbol,
            limit=limit,
            type=type,
            delay=0.5
        )
        
        if not news_data:
            raise HTTPException(status_code=404, detail=f"Daftar berita tidak ditemukan untuk simbol {symbol}")
        
        # Store in cache
        news_cache.set(symbol, type, limit, news_data)
        
        return {
            "message": "Daftar berita berhasil diambil", 
            "symbol": symbol,
            "type": type,
            "total_items": len(news_data),
            "data": news_data,
            "cached": False,
            "status_code": 200
        }
    except HTTPException:
        raise HTTPException(status_code=400, detail="Terjadi kesalahan pada server") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/v1/{symbol}/news-sentiment")
async def get_news_sentiment(symbol: str, limit: int = 20, type: str = "forex"):
    try:
        if not symbol:
            raise HTTPException(status_code=400, detail="Simbol tidak boleh kosong")
        
        # Try to get news from cache first
        cached_news = news_cache.get(symbol, type, limit)
        
        if cached_news:
            print(f"✅ Using cached news for sentiment analysis: {symbol}")
            # Analyze sentiment from cached news
            analyzer = CompleteNewsAnalyzer()
            
            # Process cached news directly (skip fetching)
            from api.service_comm_forex.news_model import NewsItem, NewsProvider, RelatedSymbol
            
            for item_data in cached_news:
                # Create NewsItem from cached data
                provider_data = item_data.get('provider', {})
                provider = NewsProvider(
                    id=provider_data.get('id', ''),
                    name=provider_data.get('name', ''),
                    logo_id=provider_data.get('logo_id', '')
                )
                
                symbols_data = item_data.get('relatedSymbols', [])
                symbols = [
                    RelatedSymbol(
                        symbol=s.get('symbol', ''),
                        logoid=s.get('logoid', '')
                    )
                    for s in symbols_data
                ]
                
                news_item = NewsItem(
                    id=item_data.get('id', ''),
                    title=item_data.get('title', ''),
                    published=item_data.get('published', 0),
                    urgency=item_data.get('urgency', 2),
                    story_path=item_data.get('storyPath', ''),
                    provider=provider,
                    related_symbols=symbols,
                    link=item_data.get('link'),
                    permission=item_data.get('permission'),
                    is_flash=item_data.get('is_flash', False)
                )
                
                # Analyze sentiment from cached full_content
                content = item_data.get('full_content', '')
                if content:
                    sentiment_result = analyzer.sentiment_analyzer.analyze(content)
                    news_item.sentiment = sentiment_result['sentiment']
                    news_item.sentiment_score = sentiment_result['score']
                    news_item.sentiment_confidence = sentiment_result['confidence']
                
                analyzer.news_collection.add(news_item)
        else:
            # No cache - fetch and analyze (fallback)
            print(f"⚠️  Cache miss - fetching and analyzing: {symbol}")
            analyzer = CompleteNewsAnalyzer()
            collection = analyzer.analyze_from_tradingview(
                symbol=symbol,
                limit=limit,
                type=type,
                fetch_delay=0.5
            )
        
        if len(analyzer.news_collection) == 0:
            raise HTTPException(status_code=404, detail=f"Data sentimen berita tidak ditemukan untuk simbol {symbol}")
        
        market_sentiment = analyzer.get_market_sentiment()
        top_news = analyzer.get_top_news(limit=10)
        
        return {
            "message": "Data sentimen berita berhasil diambil", 
            "symbol": symbol,
            "type": type,
            "used_cache": cached_news is not None,
            "market_sentiment": market_sentiment,
            "top_news": [
                {
                    "id": news.id,
                    "title": news.title,
                    "published": news.published_str,
                    "sentiment": news.sentiment,
                    "sentiment_score": news.sentiment_score,
                    "sentiment_confidence": news.sentiment_confidence,
                    "importance_score": news.importance_score,
                    "is_high_priority": news.is_high_priority,
                    "provider": news.provider.name,
                    "urgency": news.urgency
                }
                for news in top_news
            ],
            "status_code": 200
        }
    except HTTPException:
        raise HTTPException(status_code=400, detail="Terjadi kesalahan pada server")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# Cache management endpoints
@app.post("/v1/cache/invalidate")
async def invalidate_cache(symbol: str = None, type: str = None):
    """Invalidate cache for specific symbol/type or all"""
    try:
        news_cache.invalidate(symbol, type)
        return {
            "message": "Cache invalidated successfully",
            "symbol": symbol,
            "type": type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/v1/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = news_cache.get_stats()
        return {
            "message": "Cache stats retrieved",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")