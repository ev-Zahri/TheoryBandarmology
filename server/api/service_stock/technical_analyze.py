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
            
            # Handle division by zero by replacing 0 with very small number
            loss_safe = loss.replace(0, 1e-10)
            rs = gain / loss_safe
            rsi = 100 - (100 / (1 + rs))
            
            stoch_period = 14
            min_rsi = rsi.rolling(window=stoch_period).min()
            max_rsi = rsi.rolling(window=stoch_period).max()
            
            # Calculate StochRSI with safe division
            rsi_range = max_rsi - min_rsi
            rsi_range_safe = rsi_range.replace(0, 1e-10)  # Avoid division by zero
            stoch_rsi = (rsi - min_rsi) / rsi_range_safe
            
            # Get current value and handle NaN/inf
            current_stoch = stoch_rsi.iloc[-1]
            if pd.isna(current_stoch) or np.isinf(current_stoch):
                current_stoch = 0.5  # Default to neutral if calculation fails
            else:
                # Clamp to 0-1 range
                current_stoch = max(0.0, min(1.0, float(current_stoch)))
                current_stoch = round(current_stoch, 2)
            
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
                vwap_status = "Bullish Control"

            # --- 5. PRICE ACTION: CANDLESTICK PATTERN ---
            # Menggunakan logika matematika candle
            # Ambil data 3 hari terakhir untuk pola multi-candle
            # c0 = Hari Ini, c1 = Kemarin, c2 = 2 hari lalu
            c0_O, c0_H, c0_L, c0_C = open_price.iloc[-1], high.iloc[-1], low.iloc[-1], close.iloc[-1]
            c1_O, c1_H, c1_L, c1_C = open_price.iloc[-2], high.iloc[-2], low.iloc[-2], close.iloc[-2]
            c2_O, c2_H, c2_L, c2_C = open_price.iloc[-3], high.iloc[-3], low.iloc[-3], close.iloc[-3]

            # Helper Variables (Body, Wicks)
            def get_candle_props(o, h, l, c):
                body = abs(c - o)
                upper_wick = h - max(c, o)
                lower_wick = min(c, o) - l
                total_range = h - l
                avg_range = total_range if total_range > 0 else 1 
                is_bullish = c > o
                return body, upper_wick, lower_wick, total_range, is_bullish

            body0, u_wick0, l_wick0, range0, bull0 = get_candle_props(c0_O, c0_H, c0_L, c0_C)
            body1, u_wick1, l_wick1, range1, bull1 = get_candle_props(c1_O, c1_H, c1_L, c1_C)
            
            patterns = []

            # --- SINGLE CANDLE PATTERNS ---
            # 1. DOJI (Body sangat kecil) Syarat: Body kurang dari 10% total range
            if body0 <= (range0 * 0.1):
                patterns.append("Doji (Indecision)")

            # 2. MARUBOZU (Body sangat besar, tanpa ekor/ekor kecil) Syarat: Body > 90% range
            elif body0 >= (range0 * 0.9):
                patterns.append("Marubozu (Strong Momentum)")

            # 3. HAMMER / HANGING MAN Syarat: Ekor bawah panjang (2x body), ekor atas kecil
            if (l_wick0 >= 2 * body0) and (u_wick0 <= body0 * 0.5):
                if c0_C < close.iloc[-10]: 
                    patterns.append("Hammer (Bullish Reversal)")
                else: 
                    patterns.append("Hanging Man (Bearish Warning)")
            
            # 4. INVERTED HAMMER / SHOOTING STAR Syarat: Ekor atas panjang (2x body), ekor bawah kecil
            if (u_wick0 >= 2 * body0) and (l_wick0 <= body0 * 0.5):
                if c0_C < close.iloc[-10]:
                    patterns.append("Inverted Hammer (Potential Reversal)")
                else:
                    patterns.append("Shooting Star (Bearish Reversal)")
            
            # 5. SPINNING TOP Syarat: Body kecil, ekor atas & bawah mirip
            if (body0 < range0 * 0.3) and (abs(u_wick0 - l_wick0) < range0 * 0.1):
                patterns.append("Spinning Top (Neutral)")

            # --- DUAL CANDLE PATTERNS ---
            # 6. ENGULFING (Memakan candle sebelumnya)
            if (body0 > body1) and (bull0 != bull1):
                if bull0 and (c0_C > c1_O) and (c0_O < c1_C):
                    patterns.append("Bullish Engulfing (Strong Buy)")
                elif not bull0 and (c0_C < c1_O) and (c0_O > c1_C):
                    patterns.append("Bearish Engulfing (Strong Sell)")

            # 7. HARAMI (Ibu hamil - Candle hari ini kecil di dalam body kemarin)
            if (body0 < body1) and (c0_H < c1_H) and (c0_L > c1_L):
                if bull0: patterns.append("Bullish Harami")
                else: patterns.append("Bearish Harami")

            # --- TRIPLE CANDLE PATTERNS ---
            # 8. MORNING STAR (Reversal Naik: Besar Merah -> Kecil -> Besar Hijau)
            if (not bull1) and (bull0) and (abs(c1_C - c1_O) < range1 * 0.3): 
                pass

            candle_signal = ", ".join(patterns) if patterns else "No Major Pattern"

            # --- 6. PRICE ACTION: MACD ---
            # MACD Line: 12 EMA - 26 EMA
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            
            # Signal Line: 9 EMA dari MACD Line
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            
            # Histogram
            macd_hist = macd_line - signal_line
            
            # Status MACD
            last_macd = macd_line.iloc[-1]
            last_signal = signal_line.iloc[-1]
            last_hist = macd_hist.iloc[-1]
            prev_hist = macd_hist.iloc[-2]
            
            macd_status = "Neutral"
            if last_hist > 0 and prev_hist < 0:
                macd_status = "GOLDEN CROSS (Buy Signal)"
            elif last_hist < 0 and prev_hist > 0:
                macd_status = "DEAD CROSS (Sell Signal)"
            elif last_macd > last_signal:
                macd_status = "Bullish Trend"
            elif last_macd < last_signal:
                macd_status = "Bearish Trend"
            
            results.append({
                "stock": stock,
                "price": int(last_close),
                "ichimoku_status": ichimoku_status,
                "stoch_rsi": current_stoch,
                "momentum_signal": momentum_signal,
                "obv_divergence": divergence_status,
                "vwap_price": int(curr_vwap),
                "vwap_status": vwap_status,
                "candlestick_pattern": candle_signal,
                "candle_shape": "Bullish" if bull0 else "Bearish",
                "macd_status": macd_status,
            })

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            continue

    return results