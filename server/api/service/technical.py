import yfinance as yf
import pandas as pd
import numpy as np

def calculate_advanced_technical(stock_list: list):
    results = []
    tickers = [f"{s}.JK" for s in stock_list]
    
    if not tickers:
        return []

    # Kita butuh data cukup panjang (1 tahun) untuk Ichimoku (52 periode)
    try:
        data = yf.download(tickers, period="1y", group_by='ticker', progress=False)
    except Exception as e:
        print(f"Error fetching yfinance: {e}")
        return []

    for stock in stock_list:
        try:
            # 0. Persiapan Data
            if len(stock_list) > 1:
                # Multiple stocks: data is multi-indexed
                ticker_key = f"{stock}.JK"
                if ticker_key not in data.columns.get_level_values(0):
                    continue
                df = data[ticker_key].copy()
            else:
                # Single stock: yfinance returns MultiIndex columns
                # Need to flatten by selecting the ticker column
                df = data.copy()
                # If columns are MultiIndex, flatten them
                if isinstance(df.columns, pd.MultiIndex):
                    # Take the second level (price data)
                    df.columns = df.columns.get_level_values(1)
            
            # Clean data
            df = df.dropna()
            if df.empty: 
                continue

            # Pastikan tipe data float
            high = df['High'].astype(float)
            low = df['Low'].astype(float)
            close = df['Close'].astype(float)
            volume = df['Volume'].astype(float)

            # --- 1. ADVANCED: ICHIMOKU KINKO HYO (The Cloud) ---
            # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
            period9_high = high.rolling(window=9).max()
            period9_low = low.rolling(window=9).min()
            tenkan_sen = (period9_high + period9_low) / 2

            # Kijun-sen (Base Line): (26-period high + 26-period low)/2
            period26_high = high.rolling(window=26).max()
            period26_low = low.rolling(window=26).min()
            kijun_sen = (period26_high + period26_low) / 2

            # Senkou Span A (Leading Span A): (Tenkan + Kijun)/2
            # Shifted future 26 periods (tapi untuk analisa skrg, kita lihat nilai historical)
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

            # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
            period52_high = high.rolling(window=52).max()
            period52_low = low.rolling(window=52).min()
            senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

            # Ambil nilai terakhir yang valid
            last_close = close.iloc[-1]
            last_span_a = senkou_span_a.iloc[-1]
            last_span_b = senkou_span_b.iloc[-1]
            
            # Ichimoku Status
            ichimoku_status = "Neutral"
            if last_close > last_span_a and last_close > last_span_b:
                ichimoku_status = "STRONG BULLISH (Above Cloud)"
            elif last_close < last_span_a and last_close < last_span_b:
                ichimoku_status = "STRONG BEARISH (Below Cloud)"
            else:
                ichimoku_status = "Consolidation (Inside Cloud)"

            # --- 2. ADVANCED: STOCHASTIC RSI (Fast Momentum) ---
            # Lebih sensitif daripada RSI biasa
            rsi_period = 14
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate StochRSI
            stoch_period = 14
            min_rsi = rsi.rolling(window=stoch_period).min()
            max_rsi = rsi.rolling(window=stoch_period).max()
            stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
            
            current_stoch = round(stoch_rsi.iloc[-1], 2) # Range 0 - 1
            
            momentum_signal = "Hold"
            if current_stoch < 0.2: momentum_signal = "Oversold (Golden Cross Potential)"
            elif current_stoch > 0.8: momentum_signal = "Overbought (Death Cross Potential)"

            # --- 3. ADVANCED: OBV TREND (Money Flow) ---
            # Mendeteksi apakah kenaikan harga didukung volume
            # Rumus manual OBV
            obv_change = np.where(close > close.shift(1), volume, 
                         np.where(close < close.shift(1), -volume, 0))
            obv = pd.Series(obv_change).cumsum()
            
            # Cek Tren OBV 5 hari terakhir (Slope)
            obv_slope = obv.iloc[-1] - obv.iloc[-5]
            price_slope = close.iloc[-1] - close.iloc[-5]
            
            divergence_status = "Sync"
            if price_slope > 0 and obv_slope < 0:
                divergence_status = "BEARISH DIVERGENCE (Price Up, Vol Down)" # Bahaya
            elif price_slope < 0 and obv_slope > 0:
                divergence_status = "BULLISH DIVERGENCE (Price Down, Vol Up)" # Potensi Rebound

            results.append({
                "stock": stock,
                "price": int(last_close),
                "ichimoku_status": ichimoku_status,
                "stoch_rsi": current_stoch,
                "momentum_signal": momentum_signal,
                "obv_divergence": divergence_status
            })

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            continue

    return results