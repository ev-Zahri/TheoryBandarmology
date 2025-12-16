from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.service.analyzer import process_broker_data
from typing import Any, Dict
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

# Endpoint untuk analisis data - menerima JSON langsung
@app.post("/v1/analyze")
async def analyze_data(request: Request):
    try:
        # Ambil body JSON langsung
        body = await request.json()
        
        if not body:
            raise HTTPException(status_code=400, detail="JSON tidak boleh kosong.")
        
        # Convert dict ke string untuk processor
        raw_json_str = json.dumps(body)
        
        # call fungsi analyzer
        result = process_broker_data(raw_json_str)
        
        # Cek jika ada error logika
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=result.get("status_code", 400), detail=result["error"])
        
        # return result
        return {
            "message": "Data berhasil di analisis", 
            "data": result,
            "status_code": 200
        }
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON tidak valid: {str(e)}")

# Endpoint untuk Import recent data broker summary
@app.post("/v1/import-recent-data")
async def import_recent_data(request: Request):
    body = await request.json()
    return {"message": "Data berhasil di import"}
