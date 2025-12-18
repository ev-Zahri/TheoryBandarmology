import yfinance as yf
import pandas as pd
import numpy as np

def calculate_advanced_technical(stock_list: list):
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
            # --- 0. Persiapan Data (KODE LAMA ANDA TETAP SAMA) ---
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

            # Pastikan tipe data float
            open_price = df['Open'].astype(float) # Butuh ini untuk Price Action
            high = df['High'].astype(float)
            low = df['Low'].astype(float)
            close = df['Close'].astype(float)
            volume = df['Volume'].astype(float)

            # --- 1. ADVANCED: ICHIMOKU KINKO HYO ---
            period9_high = high.rolling(window=9).max()
            period9_low = low.rolling(window=9).min()
            tenkan_sen = (period9_high + period9_low) / 2

            period26_high = high.rolling(window=26).max()
            period26_low = low.rolling(window=26).min()
            kijun_sen = (period26_high + period26_low) / 2

            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

            period52_high = high.rolling(window=52).max()
            period52_low = low.rolling(window=52).min()
            senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

            last_close = close.iloc[-1]
            last_span_a = senkou_span_a.iloc[-1]
            last_span_b = senkou_span_b.iloc[-1]
            
            ichimoku_status = "Neutral"
            if last_close > last_span_a and last_close > last_span_b:
                ichimoku_status = "STRONG BULLISH (Above Cloud)"
            elif last_close < last_span_a and last_close < last_span_b:
                ichimoku_status = "STRONG BEARISH (Below Cloud)"
            else:
                ichimoku_status = "Consolidation (Inside Cloud)"

            # --- 2. ADVANCED: STOCHASTIC RSI ---
            rsi_period = 14
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            stoch_period = 14
            min_rsi = rsi.rolling(window=stoch_period).min()
            max_rsi = rsi.rolling(window=stoch_period).max()
            stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
            
            current_stoch = round(stoch_rsi.iloc[-1], 2)
            
            momentum_signal = "Hold"
            if current_stoch < 0.2: momentum_signal = "Oversold (Golden Cross Potential)"
            elif current_stoch > 0.8: momentum_signal = "Overbought (Death Cross Potential)"

            # --- 3. ADVANCED: OBV TREND ---
            obv_change = np.where(close > close.shift(1), volume, 
                         np.where(close < close.shift(1), -volume, 0))
            obv = pd.Series(obv_change).cumsum()
            
            obv_slope = obv.iloc[-1] - obv.iloc[-5]
            price_slope = close.iloc[-1] - close.iloc[-5]
            
            divergence_status = "Sync"
            if price_slope > 0 and obv_slope < 0:
                divergence_status = "BEARISH DIVERGENCE (Price Up, Vol Down)"
            elif price_slope < 0 and obv_slope > 0:
                divergence_status = "BULLISH DIVERGENCE (Price Down, Vol Up)"

            # --- 4. INSTITUTIONAL: ANCHORED VWAP (Rolling 20 Days) ---
            # Menentukan apakah Institusi sedang untung atau rugi bulan ini
            vwap_period = 20
            typical_price = (high + low + close) / 3
            # Rumus VWAP: Sum(Price*Vol) / Sum(Vol)
            rolling_pv = (typical_price * volume).rolling(window=vwap_period).sum()
            rolling_vol = volume.rolling(window=vwap_period).sum()
            vwap = rolling_pv / rolling_vol
            
            curr_vwap = vwap.iloc[-1]
            
            vwap_status = "Bearish Control"
            if last_close > curr_vwap:
                vwap_status = "Bullish Control (Inst. Buying)"

            # --- 5. PRICE ACTION: CANDLESTICK PATTERN ---
            # Menggunakan logika matematika candle
            last_o = open_price.iloc[-1]
            last_c = close.iloc[-1]
            last_h = high.iloc[-1]
            last_l = low.iloc[-1]
            
            prev_o = open_price.iloc[-2]
            prev_c = close.iloc[-2]
            
            body = abs(last_c - last_o)
            upper_wick = last_h - max(last_c, last_o)
            lower_wick = min(last_c, last_o) - last_l
            
            pa_signal = "Neutral"
            
            # Deteksi Hammer (Reversal Bullish)
            if (lower_wick > 2 * body) and (upper_wick < body):
                pa_signal = "Hammer (Potential Reversal)"
            
            # Deteksi Bullish Engulfing (Kuat)
            if (prev_c < prev_o) and (last_c > last_o) and (last_c > prev_o) and (last_o < prev_c):
                pa_signal = "Bullish Engulfing (Strong Buy)"

            # --- FINAL RESULT ---
            results.append({
                "stock": stock,
                "price": int(last_close),
                "ichimoku_status": ichimoku_status,
                "stoch_rsi": current_stoch,
                "momentum_signal": momentum_signal,
                "obv_divergence": divergence_status,
                "vwap_price": int(curr_vwap),
                "vwap_status": vwap_status,
                "candle_pattern": pa_signal
            })

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            continue

    return results