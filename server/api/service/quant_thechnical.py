import yfinance as yf
import pandas as pd
import numpy as np

def calculate_quant_metrics(stock_list: list):
    results = []
    # Tambahkan suffix .JK untuk pasar Indonesia
    tickers = [f"{s}.JK" for s in stock_list]
    
    if not tickers:
        return []

    try:
        # Download data 1 tahun untuk perhitungan statistik
        data = yf.download(tickers, period="1y", group_by='ticker', progress=False)
    except Exception as e:
        print(f"Error fetching yfinance: {e}")
        return []

    for stock in stock_list:
        try:
            # --- 0. Data Preparation ---
            # Handling yfinance multi-index
            if len(stock_list) > 1:
                df = data[f"{stock}.JK"].copy()
            else:
                df = data.copy()
            
            # Drop NaN dan pastikan kolom numerik
            df.dropna(inplace=True)
            if df.empty: continue

            # Pastikan kolom High, Low, Close tipe datanya float
            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            df['Close'] = df['Close'].astype(float)
            df['Open'] = df['Open'].astype(float)

            # --- 1. QUANT: Z-SCORE (Manual Calculation) ---
            # Konsep: Seberapa menyimpang harga dari rata-rata 20 hari?
            period = 20
            df['mean'] = df['Close'].rolling(window=period).mean()
            df['std'] = df['Close'].rolling(window=period).std()
            
            # Rumus Z-Score: (Harga - Mean) / Standar Deviasi
            # Menangani pembagian dengan nol
            df['z_score'] = np.where(df['std'] == 0, 0, (df['Close'] - df['mean']) / df['std'])
            
            current_z = round(float(df['z_score'].iloc[-1]), 2)
            
            z_status = "Normal"
            if current_z > 2.0: z_status = "Statistically Expensive (Sell Zone)"
            elif current_z > 1.0: z_status = "Slightly Expensive"
            elif current_z < -2.0: z_status = "Statistically Cheap (Buy Zone)"
            elif current_z < -1.0: z_status = "Slightly Cheap"

            # --- 2. QUANT: ATR / Volatility (Manual Calculation) ---
            # True Range = Max(High-Low, Abs(High-PrevClose), Abs(Low-PrevClose))
            df['prev_close'] = df['Close'].shift(1)
            df['tr1'] = df['High'] - df['Low']
            df['tr2'] = abs(df['High'] - df['prev_close'])
            df['tr3'] = abs(df['Low'] - df['prev_close'])
            
            # Ambil nilai max dari ketiga TR tersebut per baris
            df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
            
            # Average True Range (ATR) 14 Hari
            df['atr'] = df['tr'].rolling(window=14).mean()
            
            # Handle jika data kurang dari 14 hari
            current_atr = 0
            if not pd.isna(df['atr'].iloc[-1]):
                current_atr = round(float(df['atr'].iloc[-1]), 0)

            # --- 3. ALGORITHMIC S/R (Pivot Points Standard) ---
            # Pivot Points dihitung berdasarkan data HARI SEBELUMNYA (Latest Close)
            last_row = df.iloc[-1]
            high = float(last_row['High'])
            low = float(last_row['Low'])
            close = float(last_row['Close'])
            
            pivot = (high + low + close) / 3
            r1 = (2 * pivot) - low
            s1 = (2 * pivot) - high
            
            # Bias Teknikal
            posisi = "Inside Range"
            if close > r1: posisi = "Breakout Resistance"
            elif close < s1: posisi = "Breakdown Support"

            # Simpan hasil
            results.append({
                "stock": stock,
                "last_price": int(close),
                "z_score": current_z,
                "z_status": z_status,
                "volatility_atr": int(current_atr),
                "algo_support_s1": int(s1),
                "algo_resistance_r1": int(r1),
                "technical_bias": posisi
            })

        except Exception as e:
            # Skip saham error agar tidak mematikan seluruh proses
            print(f"Error processing {stock}: {str(e)}")
            continue

    return results