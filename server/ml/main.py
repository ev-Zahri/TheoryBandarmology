from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/analyze")
async def analyze_data(data: BrokerData):
    # 1. Parsing JSON dari data.raw_json
    # 2. Proses Pandas & Yfinance
    # 3. Return hasil list of objects
    return {"message": "Data berhasil di analisa", "data": result}
