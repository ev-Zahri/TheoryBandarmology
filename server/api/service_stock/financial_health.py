import yfinance as yf
import pandas as pd
from datetime import datetime
from ..helper.get_safe_info import get_safe_info
from api.service_stock.master_data import get_financial_ratios, get_stock_fundamental_data


def analyze_financial_health(stock_list: list):
    """
    Analyze financial health with master data integration.
    Uses cached fundamental data when available, falls back to yfinance.
    """
    results = []
    
    for stock in stock_list:
        try:
            # Try to get from master data first
            cached_ratios = get_financial_ratios(stock)
            cached_fundamental = get_stock_fundamental_data(stock)
            
            # If we have cached data, use it
            if cached_ratios and cached_fundamental:
                pe_ratio = cached_ratios.get('pe_ratio', 0) or 0
                pb_ratio = cached_ratios.get('pb_ratio', 0) or 0
                roe = (cached_ratios.get('roe', 0) or 0) * 100
                npm = (cached_fundamental.get('profit_margin', 0) or 0) * 100
                der = cached_ratios.get('debt_to_equity', 0) or 0
                div_yield = (cached_ratios.get('dividend_yield', 0) or 0) * 100
                market_cap = cached_fundamental.get('market_cap', 0) or 0
                market_cap_t = round(market_cap / 1_000_000_000_000, 2)
                
                # Growth data might not be in cache, try yfinance
                try:
                    ticker_obj = yf.Ticker(f"{stock}.JK")
                    info = ticker_obj.info
                    rev_growth = get_safe_info(info, 'revenueGrowth', 0) * 100
                    earnings_growth = get_safe_info(info, 'earningsGrowth', 0) * 100
                except:
                    rev_growth = 0
                    earnings_growth = 0
            else:
                # Fallback to yfinance entirely
                ticker_obj = yf.Ticker(f"{stock}.JK")
                info = ticker_obj.info
                
                pe_ratio = get_safe_info(info, 'trailingPE', 0)
                pb_ratio = get_safe_info(info, 'priceToBook', 0)
                market_cap = get_safe_info(info, 'marketCap', 0)
                market_cap_t = round(market_cap / 1_000_000_000_000, 2)
                
                roe = get_safe_info(info, 'returnOnEquity', 0) * 100
                npm = get_safe_info(info, 'profitMargins', 0) * 100
                
                der = get_safe_info(info, 'debtToEquity', 0)
                
                rev_growth = get_safe_info(info, 'revenueGrowth', 0) * 100
                earnings_growth = get_safe_info(info, 'earningsGrowth', 0) * 100
                
                div_yield = get_safe_info(info, 'dividendYield', 0) * 100

            # --- SCORING & DIAGNOSA ---
            health_label = "Neutral"
            score = 0
            flags = []

            # Cek Utang (Safety First)
            if der > 200:
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
                    "der": round(der, 2),
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