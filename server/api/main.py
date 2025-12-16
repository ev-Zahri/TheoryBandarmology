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

# Endpoint untuk analisis data
@app.post("/analyze")
async def analyze_data(data: BrokerData):
    # data yang sudah diimport terus di analisa terus di kategorikan

    #  return berupa data yang sudah dianalisa oleh machine learning
    return {"message": "Data berhasil di analisa", "data": result}

# Endpoint untuk Import recent data broker summary
@app.post("/import-recent-data")
async def import_recent_data(data: BrokerData):
    # 1. Parsing JSON dari data.raw_json
    return {"message": "Data berhasil di import"}


