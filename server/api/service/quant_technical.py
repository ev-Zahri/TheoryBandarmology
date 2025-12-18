import yfinance as yf
import pandas as pd
import numpy as np

def calculate_quant_metrics(stock_list: list):
    results = []
    tickers = [f"{s}.JK" for s in stock_list]
    
    if not tickers:
        return []

    try:
        data = yf.download(tickers, period="1y", group_by='ticker', progress=False)
    except Exception as e:
        print(f"Error fetching yfinance: {e}")
        return []

    for stock in stock_list:
        try:
            # --- 0. Data Preparation (KODE LAMA ANDA TETAP SAMA) ---
            if len(stock_list) > 1:
                ticker_key = f"{stock}.JK"
                if ticker_key not in data.columns.get_level_values(0):
                    continue
                df = data[ticker_key].copy()
            else:
                df = data.copy()
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(1)
            
            df = df.dropna()
            if df.empty: 
                continue

            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            df['Close'] = df['Close'].astype(float)
            df['Open'] = df['Open'].astype(float)

            # --- 1. QUANT: Z-SCORE ---
            period = 20
            df['mean'] = df['Close'].rolling(window=period).mean()
            df['std'] = df['Close'].rolling(window=period).std()
            
            # Handle std 0 agar tidak error division
            df['z_score'] = np.where(df['std'] == 0, 0, (df['Close'] - df['mean']) / df['std'])
            current_z = round(float(df['z_score'].iloc[-1]), 2)
            
            z_status = "Normal"
            if current_z > 2.0: z_status = "Statistically Expensive (Sell Zone)"
            elif current_z > 1.0: z_status = "Slightly Expensive"
            elif current_z < -2.0: z_status = "Statistically Cheap (Buy Zone)"
            elif current_z < -1.0: z_status = "Slightly Cheap"

            # --- 2. QUANT: ATR / Volatility ---
            df['prev_close'] = df['Close'].shift(1)
            df['tr1'] = df['High'] - df['Low']
            df['tr2'] = abs(df['High'] - df['prev_close'])
            df['tr3'] = abs(df['Low'] - df['prev_close'])
            df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
            
            df['atr'] = df['tr'].rolling(window=14).mean()
            
            current_atr = 0
            if not pd.isna(df['atr'].iloc[-1]):
                current_atr = round(float(df['atr'].iloc[-1]), 0)

            # --- 3. ALGORITHMIC S/R (Pivot Points) ---
            last_row = df.iloc[-1]
            high = float(last_row['High'])
            low = float(last_row['Low'])
            close = float(last_row['Close'])
            
            pivot = (high + low + close) / 3
            r1 = (2 * pivot) - low
            s1 = (2 * pivot) - high
            
            posisi = "Inside Range"
            if close > r1: posisi = "Breakout Resistance"
            elif close < s1: posisi = "Breakdown Support"

            # --- 4. QUANT: TTM SQUEEZE DETECTION ---
            # Deteksi ketika Bollinger Bands masuk ke dalam Keltner Channel
            # Ini tanda harga 'diam' sebelum meledak besar.
            
            # Bollinger Bands (20, 2.0)
            sma20 = df['Close'].rolling(window=20).mean()
            std20 = df['Close'].rolling(window=20).std()
            bb_upper = sma20 + (2.0 * std20)
            bb_lower = sma20 - (2.0 * std20)
            
            # Keltner Channels (20, 1.5 ATR) - Kita pakai ATR 1.5 untuk filter lebih ketat
            # Kita pakai ATR yang sudah dihitung di atas, tapi rolling 20
            df['atr20'] = df['tr'].rolling(window=20).mean()
            kc_upper = sma20 + (1.5 * df['atr20'])
            kc_lower = sma20 - (1.5 * df['atr20'])
            
            # Cek kondisi Squeeze hari ini
            # Squeeze terjadi jika BB Upper < KC Upper DAN BB Lower > KC Lower
            is_squeeze = (bb_upper.iloc[-1] < kc_upper.iloc[-1]) and (bb_lower.iloc[-1] > kc_lower.iloc[-1])
            
            squeeze_status = "Normal Volatility"
            if is_squeeze:
                squeeze_status = "⚠️ SQUEEZE (Ready to Explode)"

            # --- FINAL RESULT ---
            results.append({
                "stock": stock,
                "last_price": int(close),
                "z_score": current_z,
                "z_status": z_status,
                "volatility_atr": int(current_atr),
                "algo_support_s1": int(s1),
                "algo_resistance_r1": int(r1),
                "technical_bias": posisi,
                # Field Baru Ditambahkan:
                "volatility_status": squeeze_status
            })

        except Exception as e:
            print(f"Error processing {stock}: {str(e)}")
            continue

    return results