from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from service.analyzer import process_broker_data

app = FastAPI()

origin = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrokerData(BaseModel):
    raw_json: str

# Endpoint untuk analisis data
@app.post("/analyze")
async def analyze_data(data: BrokerData):
    # Validasi input kosong
    if not data.raw_json:
        raise HTTPException(status_code=400, detail="JSON tidak boleh kosong.")

    # call fungsi analyzer
    result = process_broker_data(data.raw_json)
    
    #  Cek jika ada error logika
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # return result
    return {"message": "Data berhasil di analisis", "data": result, "status_code": 200}

# Endpoint untuk Import recent data broker summary
@app.post("/import-recent-data")
async def import_recent_data(data: BrokerData):
    # 1. Parsing JSON dari data.raw_json
    return {"message": "Data berhasil di import"}


