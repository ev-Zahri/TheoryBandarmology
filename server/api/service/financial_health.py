import yfinance as yf
import pandas as pd
from datetime import datetime
from ..helper.get_safe_info import get_safe_info


def analyze_financial_health(stock_list: list):
    results = []
    # Tambahkan .JK
    
    for stock in stock_list:
        try:
            ticker_obj = yf.Ticker(f"{stock}.JK")
            # Fetch info (ini memakan waktu network)
            info = ticker_obj.info
            
            # 1. VALUATION (Murah/Mahal)
            pe_ratio = get_safe_info(info, 'trailingPE', 0)
            pb_ratio = get_safe_info(info, 'priceToBook', 0)
            market_cap = get_safe_info(info, 'marketCap', 0)
            market_cap_t = round(market_cap / 1_000_000_000_000, 2) # Triliun
            
            # 2. PROFITABILITY (Kemampuan Cetak Laba)
            roe = get_safe_info(info, 'returnOnEquity', 0) * 100
            npm = get_safe_info(info, 'profitMargins', 0) * 100 # Net Profit Margin
            
            # 3. SOLVENCY (Kesehatan Hutang) - SANGAT PENTING
            der = get_safe_info(info, 'debtToEquity', 0) # Debt to Equity Ratio
            # Di yfinance DER biasanya skala 0-100+, kadang 0-1. Kita asumsikan >100 itu hutang > equity
            
            # 4. GROWTH (Pertumbuhan)
            rev_growth = get_safe_info(info, 'revenueGrowth', 0) * 100
            earnings_growth = get_safe_info(info, 'earningsGrowth', 0) * 100

            # 5. DIVIDEND
            div_yield = get_safe_info(info, 'dividendYield', 0) * 100

            # --- SCORING & DIAGNOSA ---
            health_label = "Neutral"
            score = 0
            flags = [] # Catatan merah/hijau

            # Cek Utang (Safety First)
            if der > 200: # Utang 2x Modal
                flags.append("⚠️ High Debt")
                score -= 2
            elif der < 50:
                flags.append("✅ Low Debt")
                score += 1
            
            # Cek Profitabilitas
            if roe > 15: 
                flags.append("✅ High ROE")
                score += 1
            elif roe < 0:
                flags.append("❌ Loss Making")
                score -= 2
            
            # Cek Valuasi
            if 0 < pe_ratio < 10:
                flags.append("💎 Undervalued (PER<10)")
                score += 1
            elif pe_ratio > 40:
                flags.append("⚠️ Overvalued")
                score -= 1

            # Kesimpulan Kesehatan
            if score >= 2: health_label = "HEALTHY / STRONG"
            elif score <= -2: health_label = "RISKY / WEAK"
            else: health_label = "MODERATE"

            results.append({
                "stock": stock,
                "market_cap_t": market_cap_t,
                "valuation": {
                    "per": round(pe_ratio, 2),
                    "pbv": round(pb_ratio, 2),
                    "div_yield": round(div_yield, 2)
                },
                "health": {
                    "roe": round(roe, 2),
                    "npm": round(npm, 2),
                    "der": round(der, 2), # Hutang
                    "rev_growth": round(rev_growth, 2)
                },
                "summary": {
                    "status": health_label,
                    "flags": flags
                }
            })

        except Exception as e:
            print(f"Error Financial {stock}: {e}")
            continue
            
    return results