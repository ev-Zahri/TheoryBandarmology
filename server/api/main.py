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
from api.service_stock.master_data import (
    get_technical_stats,
    get_fundamental_stats,
    update_technical_data_batch,
    update_fundamental_data_batch,
    get_all_stock_codes,
    add_stocks_from_broker_data
)
from api.service_stock.accumulation import (
    detect_accumulation,
    get_all_accumulating_stocks,
    get_broker_accumulation,
    save_accumulation_data,
    load_accumulation_data
)
from typing import Dict, List
import json
from datetime import datetime

app = FastAPI()

# In-memory progress tracker
reload_progress = {
    "technical": {
        "is_running": False,
        "current": 0,
        "total": 0,
        "status": "idle",
        "successful": 0,
        "failed": 0,
        "started_at": None,
        "completed_at": None
    },
    "fundamental": {
        "is_running": False,
        "current": 0,
        "total": 0,
        "status": "idle",
        "successful": 0,
        "failed": 0,
        "started_at": None,
        "completed_at": None
    }
}

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
        
        # NEW: Detect accumulation patterns
        accumulation_results = detect_accumulation(json_data)
        save_accumulation_data(accumulation_results)
        
        return {
            "message": "File broker summary berhasil diproses",
            "data": result,
            "accumulation": {
                "total_brokers": accumulation_results['total_brokers'],
                "brokers": {
                    broker_code: {
                        'total_transactions': broker_data['total_transactions'],
                        'accumulating_stocks_count': broker_data['accumulating_stocks_count']
                    }
                    for broker_code, broker_data in accumulation_results['brokers'].items()
                }
            },
            "status_code": 200
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


# ==================== ACCUMULATION APIs ====================

@app.get("/v1/accumulation/stocks")
async def get_accumulating_stocks():
    """
    Get all accumulating stocks across all brokers
    """
    try:
        data = load_accumulation_data()
        all_stocks = get_all_accumulating_stocks(data)
        
        return {
            "message": "Accumulating stocks retrieved successfully",
            "total_stocks": len(all_stocks),
            "last_updated": data.get('last_updated'),
            "stocks": all_stocks,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving accumulating stocks: {str(e)}"
        )


@app.get("/v1/accumulation/broker/{broker_code}")
async def get_broker_accumulating_stocks(broker_code: str):
    """
    Get accumulating stocks for specific broker
    """
    try:
        data = load_accumulation_data()
        broker_data = get_broker_accumulation(data, broker_code)
        
        if not broker_data:
            raise HTTPException(
                status_code=404,
                detail=f"No accumulation data found for broker: {broker_code}"
            )
        
        return {
            "message": f"Accumulating stocks for {broker_code} retrieved successfully",
            "broker_code": broker_code,
            "data": broker_data,
            "status_code": 200
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving broker accumulation: {str(e)}"
        )


@app.get("/v1/accumulation/summary")
async def get_accumulation_summary():
    """
    Get summary of accumulation data
    """
    try:
        data = load_accumulation_data()
        
        summary = {
            "last_updated": data.get('last_updated'),
            "total_brokers": data.get('total_brokers', 0),
            "brokers": []
        }
        
        for broker_code, broker_data in data.get('brokers', {}).items():
            summary['brokers'].append({
                "broker_code": broker_code,
                "total_transactions": broker_data.get('total_transactions', 0),
                "total_stocks_analyzed": broker_data.get('total_stocks_analyzed', 0),
                "accumulating_stocks_count": broker_data.get('accumulating_stocks_count', 0)
            })
        
        return {
            "message": "Accumulation summary retrieved successfully",
            "data": summary,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving accumulation summary: {str(e)}"
        )


# ==================== MASTER DATA ENDPOINTS ====================

@app.get("/v1/master-data/stats")
async def get_master_data_stats():
    """
    Get statistics about master data (technical and fundamental)
    """
    try:
        technical_stats = get_technical_stats()
        fundamental_stats = get_fundamental_stats()
        
        return {
            "technical": technical_stats,
            "fundamental": fundamental_stats,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting stats: {str(e)}"
        )


@app.post("/v1/master-data/reload/technical")
async def reload_technical_data(
    batch_size: int = 300,
    delay: int = 30,
    max_workers: int = 5
):
    """
    Manually reload technical data from yfinance
    
    Args:
        batch_size: Number of stocks per batch (default: 300)
        delay: Seconds between batches (default: 30)
        max_workers: Concurrent requests per batch (default: 5)
    """
    try:
        # Check if already running
        if reload_progress["technical"]["is_running"]:
            return {
                "message": "Technical data reload already in progress",
                "progress": reload_progress["technical"],
                "status_code": 409  # Conflict
            }
        
        stock_codes = get_all_stock_codes()
        
        # Initialize progress
        reload_progress["technical"] = {
            "is_running": True,
            "current": 0,
            "total": len(stock_codes),
            "status": "starting",
            "successful": 0,
            "failed": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Progress callback function
        def progress_callback(current, total, status, successful, failed):
            reload_progress["technical"].update({
                "current": current,
                "total": total,
                "status": status,
                "successful": successful,
                "failed": failed
            })
            if status == "complete":
                reload_progress["technical"]["is_running"] = False
                reload_progress["technical"]["completed_at"] = datetime.now().isoformat()
        
        # Run update in background (non-blocking)
        import threading
        
        def update_task():
            try:
                update_technical_data_batch(
                    stock_codes,
                    batch_size=batch_size,
                    delay_between_batches=delay,
                    max_workers=max_workers,
                    progress_callback=progress_callback
                )
            except Exception as e:
                print(f"Error in background task: {e}")
                reload_progress["technical"]["is_running"] = False
                reload_progress["technical"]["status"] = f"error: {str(e)}"
        
        thread = threading.Thread(target=update_task, daemon=True)
        thread.start()
        
        return {
            "message": "Technical data reload started",
            "total_stocks": len(stock_codes),
            "estimated_time_minutes": (len(stock_codes) // batch_size) * (delay // 60),
            "status_code": 202  # Accepted
        }
    except Exception as e:
        reload_progress["technical"]["is_running"] = False
        raise HTTPException(
            status_code=500,
            detail=f"Error starting reload: {str(e)}"
        )


@app.get("/v1/master-data/reload/progress")
async def get_reload_progress():
    """
    Get current progress of reload operations
    """
    return {
        "technical": reload_progress["technical"],
        "fundamental": reload_progress["fundamental"],
        "status_code": 200
    }


@app.post("/v1/master-data/reload/fundamental")
async def reload_fundamental_data(
    batch_size: int = 50,
    delay: int = 60,
    max_workers: int = 5
):
    """
    Manually reload fundamental data from yfinance
    
    Args:
        batch_size: Number of stocks per batch (default: 50)
        delay: Seconds between batches (default: 60)
        max_workers: Concurrent requests per batch (default: 5)
    """
    try:
        # Check if already running
        if reload_progress["fundamental"]["is_running"]:
            return {
                "message": "Fundamental data reload already in progress",
                "progress": reload_progress["fundamental"],
                "status_code": 409  # Conflict
            }
        
        stock_codes = get_all_stock_codes()
        
        # Initialize progress
        reload_progress["fundamental"] = {
            "is_running": True,
            "current": 0,
            "total": len(stock_codes),
            "status": "starting",
            "successful": 0,
            "failed": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Progress callback function
        def progress_callback(current, total, status, successful, failed):
            reload_progress["fundamental"].update({
                "current": current,
                "total": total,
                "status": status,
                "successful": successful,
                "failed": failed
            })
            if status == "complete":
                reload_progress["fundamental"]["is_running"] = False
                reload_progress["fundamental"]["completed_at"] = datetime.now().isoformat()
        
        # Run update in background (non-blocking)
        import threading
        
        def update_task():
            try:
                update_fundamental_data_batch(
                    stock_codes,
                    batch_size=batch_size,
                    delay_between_batches=delay,
                    max_workers=max_workers,
                    progress_callback=progress_callback
                )
            except Exception as e:
                print(f"Error in background task: {e}")
                reload_progress["fundamental"]["is_running"] = False
                reload_progress["fundamental"]["status"] = f"error: {str(e)}"
        
        thread = threading.Thread(target=update_task, daemon=True)
        thread.start()
        
        return {
            "message": "Fundamental data reload started",
            "total_stocks": len(stock_codes),
            "estimated_time_minutes": (len(stock_codes) // batch_size) * (delay // 60),
            "status_code": 202  # Accepted
        }
    except Exception as e:
        reload_progress["fundamental"]["is_running"] = False
        raise HTTPException(
            status_code=500,
            detail=f"Error starting reload: {str(e)}"
        )


@app.post("/v1/master-data/discover-stocks")
async def discover_stocks_from_broker(stock_codes: List[str]):
    """
    Add new stocks discovered from broker data to master data
    
    Args:
        stock_codes: List of stock codes from broker data
    """
    try:
        add_stocks_from_broker_data(stock_codes)
        
        return {
            "message": "Stock discovery completed",
            "stocks_processed": len(stock_codes),
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error discovering stocks: {str(e)}"
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