from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.service.analyzer import process_broker_data
from api.service.technical_analyze import calculate_advanced_technical
from api.service.quant_technical import calculate_quant_metrics
from api.service.financial_health import analyze_financial_health
from api.service.news_narrative import analyze_news_narrative
from api.service.company_profile import get_company_profile
from typing import Any, Dict, List
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
@app.post("/v1/analyze")
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

@app.post('/v1/analyze/technical')
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
@app.post('/v1/analyze/quant')
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


@app.post('/v1/analyze/fundamental')
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

@app.post('/v1/analyze/news')
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

@app.get('/v1/company-profile/{stock_code}')
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
@app.post("/v1/import-recent-data")
async def import_recent_data(request: Request):
    body = await request.json()
    return {"message": "Data berhasil di import"}
