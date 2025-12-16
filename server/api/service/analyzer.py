import json
import pandas as pd
import yfinance as yf
import math

def safe_float(value, default=0):
    """Safely convert value to float, handling NaN and Infinity"""
    if value is None:
        return default
    try:
        val = float(value)
        if math.isnan(val) or math.isinf(val):
            return default
        return val
    except (ValueError, TypeError):
        return default

def safe_round(value, decimals=0, default=0):
    """Safely round a value, handling NaN and Infinity"""
    val = safe_float(value, default)
    return round(val, decimals)

# fungsi untuk mengolah raw json dari stockbit menjadi data matang
def process_broker_data(raw_json_str: str):
    try:
        # Parse JSON
        parsed_data = json.loads(raw_json_str)
        
        # Ekstrak metadata broker
        broker_info = {
            "broker_code": parsed_data.get("data", {}).get("broker_code", ""),
            "broker_name": parsed_data.get("data", {}).get("broker_name", ""),
            "from_date": parsed_data.get("data", {}).get("from", ""),
            "to_date": parsed_data.get("data", {}).get("to", "")
        }
        
        try:
            items = parsed_data["data"]["broker_summary"]["brokers_buy"]
        except KeyError as e:
            return {"error": "Struktur JSON tidak valid. Pastikan copy dari Network Tab Stockbit dengan benar.", "status_code": 400}
        
        if not items:
            return {"error": "Tidak ada data pembelian broker ditemukan.", "status_code": 404}

        df = pd.DataFrame(items)
        
        # Filter hanya kolom yang dibutuhkan
        df["Stock"] = df["netbs_stock_code"]
        df["AvgPrice"] = pd.to_numeric(df["netbs_buy_avg_price"], errors="coerce")
        df["TotalValue"] = pd.to_numeric(df["bval"], errors="coerce")
        df["TotalLot"] = pd.to_numeric(df["blot"], errors="coerce")
        df["Type"] = df.get("type", "Unknown")

        df_clean = df[["Stock", "AvgPrice", "TotalValue", "TotalLot", "Type"]].copy()
        
        # Filter stock yang valid (tidak mengandung suffix warrant/right issue, panjang ticker <= 4)
        df_clean = df_clean[df_clean["Stock"].str.len() <= 4]

        if df_clean.empty:
            return {"error": "Tidak ada saham valid ditemukan setelah filter.", "status_code": 404}

        # Ambil harga pasar saat ini
        stock_list = df_clean["Stock"].unique().tolist()
        tickers_jk = [f"{ticker}.JK" for ticker in stock_list]

        # Download harga dengan thread true agar cepat
        current_price = {}
        try:
            market_data = yf.download(tickers_jk, period="1d", progress=False)["Close"]
            
            if market_data is not None and not market_data.empty:
                if len(stock_list) == 1:  # Jika hanya 1 stock
                    try:
                        val = safe_float(market_data.iloc[-1].item())
                        current_price[stock_list[0]] = val
                    except:
                        current_price[stock_list[0]] = 0
                else:  # Jika lebih dari 1 stock
                    last_row = market_data.iloc[-1]
                    for ticker in tickers_jk:
                        stock_code = ticker.replace('.JK', '')
                        try: 
                            current_price[stock_code] = safe_float(last_row[ticker].item())
                        except: 
                            current_price[stock_code] = 0
        except Exception as e:
            # Jika gagal fetch, set semua ke 0
            for stock in stock_list:
                current_price[stock] = 0

        # Hitung logika bandarmologi (profit dan loss)
        result = []
        for index, row in df_clean.iterrows():
            stock = row["Stock"]
            avg_price = safe_float(row["AvgPrice"])
            total_value = safe_float(row["TotalValue"])
            total_lot = safe_float(row["TotalLot"])
            curr = safe_float(current_price.get(stock, 0))
            
            # Skip jika avg_price tidak valid
            if avg_price <= 0:
                continue
            
            # hitung presentase gain/loss
            if avg_price > 0 and curr > 0:
                diff_pct = ((curr - avg_price) / avg_price) * 100
            else:
                diff_pct = 0

            # definisi status
            status = "NEUTRAL"
            if diff_pct > 0: status = "PROFIT"
            elif diff_pct < 0: status = "LOSS"

            result.append({
                "stock": stock,
                "broker_avg": safe_round(avg_price),
                "current_price": safe_round(curr),
                "value": safe_round(total_value),
                "lot": safe_round(total_lot),
                "diff_pct": safe_round(diff_pct, 2),
                "status": status,
                "type": row["Type"] if isinstance(row["Type"], str) else "Unknown"
            })
        
        # sorting result berdasarkan value (descending)
        result = sorted(result, key=lambda x: x["value"], reverse=True)

        return {
            "broker_info": broker_info,
            "stocks": result,
            "total_stocks": len(result)
        }

    except json.JSONDecodeError as e:
        return {"error": f"JSON tidak valid: {str(e)}", "status_code": 400}
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}", "status_code": 500}