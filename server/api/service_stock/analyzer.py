import json
import pandas as pd
import yfinance as yf
import math
import numpy as np
from ..helper.safe_float import safe_float
from ..helper.safe_int import safe_int

def process_broker_data(raw_json_str: str):
    try:
        # 1. Parse JSON
        parsed_data = json.loads(raw_json_str)
        
        # 2. Ekstrak Metadata
        broker_data = parsed_data.get("data", {})
        broker_info = {
            "broker_code": broker_data.get("broker_code", "UNKNOWN"),
            "broker_name": broker_data.get("broker_name", "Unknown Broker"),
            "date_start": broker_data.get("from", ""),
            "date_end": broker_data.get("to", "")
        }
        
        # 3. Validasi & Ekstrak Item
        try:
            items = broker_data["broker_summary"]["brokers_buy"]
        except KeyError:
            return {"error": "Struktur JSON salah. Pastikan copy JSON dari Network Tab 'broker/summary' di Stockbit.", "status_code": 400}
        
        if not items:
            return {"error": "Tidak ada data pembelian (Net Buy) pada periode ini.", "status_code": 404}

        # 4. Pandas Processing
        df = pd.DataFrame(items)
        
        # Konversi Tipe Data
        df["Stock"] = df["netbs_stock_code"]
        df["AvgPrice"] = df["netbs_buy_avg_price"].apply(lambda x: safe_float(x))
        df["TotalValue"] = df["bval"].apply(lambda x: safe_float(x))
        df["TotalLot"] = df["blot"].apply(lambda x: safe_int(x)) # Stockbit kadang string
        
        # Bersihkan data: Hapus yang value 0 atau AvgPrice 0
        df = df[(df["TotalValue"] > 0) & (df["AvgPrice"] > 0)].copy()

        # Filter: Hanya saham valid (Max 4 huruf, hindari Warrant -W)
        # Regex: Hanya huruf A-Z, panjang 4 digit. Tapi simple len <= 4 juga oke untuk MVP.
        df = df[df["Stock"].str.len() <= 4]
        
        if df.empty:
            return {"error": "Tidak ada saham valid setelah filter.", "status_code": 404}

        # 5. Hitung 'Weight' (Alokasi Dana Broker)
        # Ini fitur penting: Berapa persen uang broker lari ke saham ini?
        total_portfolio_value = df["TotalValue"].sum()
        df["Weight"] = (df["TotalValue"] / total_portfolio_value) * 100

        # 6. Fetch Harga YFinance
        stock_list = df["Stock"].unique().tolist()
        tickers_jk = [f"{ticker}.JK" for ticker in stock_list]
        
        current_prices = {}
        
        if stock_list:
            try:
                # Download batch agar cepat
                market_data = yf.download(tickers_jk, period="1d", progress=False)["Close"]
                
                # Handling jika data cuma 1 baris (Series) atau Tabel (DataFrame)
                if not market_data.empty:
                    last_prices = market_data.iloc[-1] # Ambil baris terakhir (Latest Close/Live)
                    
                    if len(stock_list) == 1:
                        # Case cuma 1 saham
                        code = stock_list[0]
                        current_prices[code] = safe_float(last_prices.item())
                    else:
                        # Case banyak saham
                        for ticker in tickers_jk:
                            clean_code = ticker.replace(".JK", "")
                            try:
                                # Handle jika ticker tidak ada di YFinance (return NaN)
                                price = last_prices[ticker]
                                current_prices[clean_code] = safe_float(price)
                            except:
                                current_prices[clean_code] = 0
            except Exception as e:
                print(f"YFinance Error: {e}") 
                # Lanjut saja, harga nanti jadi 0

        # 7. Final Logic Loop (Classification)
        result_list = []
        
        # Statistik Ringkasan
        stats_win = 0
        stats_loss = 0
        stats_potential_pnl = 0

        for index, row in df.iterrows():
            stock = row["Stock"]
            avg_price = row["AvgPrice"]
            curr_price = current_prices.get(stock, 0)
            
            # Hitung % Perubahan
            diff_pct = 0
            floating_pnl = 0 # Rupiah
            
            if curr_price > 0:
                diff_pct = ((curr_price - avg_price) / avg_price) * 100
                # Hitung Estimasi Cuan/Rugi Rupiah (Lot * 100 lembar * Selisih Harga)
                floating_pnl = (curr_price - avg_price) * row["TotalLot"] * 100
            
            # Update Global Stats
            stats_potential_pnl += floating_pnl
            if diff_pct > 0.5: stats_win += 1
            elif diff_pct < -0.5: stats_loss += 1

            # Klasifikasi Status (Lebih Detail)
            # Toleransi BEP di angka 0.5% (Karena fee beli+jual biasanya 0.4%-0.5%)
            status = "NEUTRAL" # BEP
            status_color = "gray" # Untuk frontend hint
            
            if diff_pct >= 5.0:
                status = "BIG PROFIT"
                status_color = "green"
            elif diff_pct > 0.5:
                status = "PROFIT"
                status_color = "green"
            elif diff_pct <= -5.0:
                status = "DEEP LOSS" # Nyangkut parah
                status_color = "red"
            elif diff_pct < -0.5:
                status = "LOSS"
                status_color = "red"

            result_list.append({
                "stock": stock,
                "broker_avg": round(avg_price, 0),
                "current_price": round(curr_price, 0),
                "value_bn": round(row["TotalValue"] / 1_000_000_000, 2), # Dalam Milyar (Billion)
                "value_raw": row["TotalValue"],
                "lot": int(row["TotalLot"]),
                "weight_pct": round(row["Weight"], 1), # % Alokasi
                "diff_pct": round(diff_pct, 2),
                "floating_pnl": round(floating_pnl, 0), # Estimasi Rupiah
                "status": status,
                "status_color": status_color
            })

        # 8. Sorting
        # Sort utama berdasarkan Value (Uang yang dipertaruhkan)
        result_list = sorted(result_list, key=lambda x: x["value_raw"], reverse=True)

        # 9. Return Final Structure
        return {
            "status": "success",
            "broker_info": broker_info,
            "summary": {
                "total_value": total_portfolio_value,
                "total_stocks": len(result_list),
                "win_vs_loss": f"{stats_win} - {stats_loss}",
                "potential_pnl_total": stats_potential_pnl
            },
            "data": result_list
        }

    except json.JSONDecodeError:
        return {"error": "Format JSON tidak valid.", "status_code": 400}
    except Exception as e:
        # Print error log di terminal server untuk debugging
        import traceback
        traceback.print_exc() 
        return {"error": f"Server Error: {str(e)}", "status_code": 500}