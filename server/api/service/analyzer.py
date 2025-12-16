import json
import pandas as pd
import yfinance as yf

# fungsi untuk mengolah raw json dari stockbit menjadi data matang
def process_broker_data(raw_json_str: str):
    try:
        # Parse JSON
        parsed_data = json.loads(raw_json_str)
        try:
            items = parsed_data["data"]["broker_summary"]["broker_buy"]
        except KeyError as e:
            # fallback jika struktur json tidak valid
            return {"error": "Struktur JSON tidak valid. Pastikan copy dari Network Tab Stockbit dengan benar.", "status_code": 400}
        
        if not items:
            return {"error": "Tidak ada data pembelian broker ditemukan.", "status_code": 404}

        df = pd.DataFrame(items)
        df["Stock"] = df["netbs_stock_code"]
        df["AvgPrice"] = pd.numeric(df["netbs_buy_avg_price"], errors="coerce")
        df["TotalValue"] = pd.numeric(df["bval"], errors="coerce")

        df_clean = df[["Stock", "AvgPrice", "TotalValue"]].copy()

        #  Ambil harga pasar saat ini
        stock_list = df_clean["Stock"].unique().tolist()
        tickers_jk = [f"{ticker}.JK" for ticker in stock_list]

        # Download harga dengan thread true agar cepat
        market_data = yf.download(tickers_jk, period="1d", progress=False)["Close"]

        # Handling format yfinance
        current_price = {}
        if len(stock_list) == 1:  # Jika hanya 1 stock
            val = market_data.iloc[-1].item()
            current_price[stock_list[0]] = val
        else:  # Jika lebih dari 1 stock
            last_row = market_data.iloc[-1]
            for ticker in tickers_jk:
                stock_code = ticker.replace('.JK', '')
                try: 
                    current_price[stock_code] = last_row[ticker].item()
                except KeyError: 
                    current_price[stock_code] = 0

        # Hitung logika bandarmologi (profit dan loss)
        result = []
        for index, row in df_clean.iterrows():
            stock = row["Stock"]
            avg_price = row["AvgPrice"]
            curr = current_price.get(stock, 0)
            
            # hitung presentase gain/loss
            if avg > 0 and curr > 0:
                diff_pct = ((curr - avg) / avg) * 100
            else:
                diff_pct = 0

            # definisi status
            status = "NEUTRAL"
            if diff_pct > 0: status = "BUY"
            elif diff_pct < 0: status = "SELL"

            result.append({
                "stock": stock,
                "broker_avg": round(avg, 0),
                "current_price": round(curr, 0),
                "value": row["TotalValue"],
                "diff_pct": round(diff_pct, 2),
                "status": status
            })
        
        # sorting result berdasarkan value
        result = sorted(result, key=lambda x: x["value"], reverse=True)

        return {"message": "Data berhasil di analisis", "data": result, "status_code": 200}