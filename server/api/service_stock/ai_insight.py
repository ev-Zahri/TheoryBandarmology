import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY belum di-set di file .env")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
def generate_insight(stock_code, bandar_data, tech_data, quant_data, fund_data):
    if not api_key:
        return "Error: API Key Gemini belum dikonfigurasi. Silakan cek file .env Anda."
    
    # buat konstruksi prompt
    prompt = f"""Bertindaklah sebagai Senior Equity Analyst profesional untuk Pasar Saham Indonesia (IHSG).
    Tugasmu adalah membuat 'Executive Summary' singkat, padat, dan actionable berdasarkan data berikut untuk saham {stock_code}.
    
    DATA ANALISIS (Dihitung oleh Sistem):
    
    1. BANDARMOLOGY (Aliran Dana):
    - Total Value Transaksi Broker Top: {bandar_data.get('value_bn', 0)} Milyar Rupiah
    - Status Akumulasi: {bandar_data.get('status', 'Netral')}
    - Average Harga Bandar: {bandar_data.get('broker_avg', 0)}
    - Asing (Foreign Flow): {bandar_data.get('foreign_status', 'Netral')}
    
    2. TEKNIKAL & PRICE ACTION:
    - Tren Jangka Pendek: {tech_data.get('candle_pattern', '-')}
    - Status VWAP (Institusi): {tech_data.get('vwap_status', '-')}
    - Indikator Momentum (StochRSI): {tech_data.get('momentum_signal', '-')}
    - Ichimoku Cloud: {tech_data.get('ichimoku_status', '-')}
    
    3. QUANTITATIVE (Statistik):
    - Z-Score (Kewajaran Harga): {quant_data.get('z_score', 0)} ({quant_data.get('z_status', '-')})
    - Volatilitas (Squeeze): {quant_data.get('volatility_status', '-')}
    - Pivot Support S1: {quant_data.get('algo_s1', 0)}
    
    4. FUNDAMENTAL (Kesehatan):
    - Status: {fund_data.get('summary', {}).get('status', '-')}
    - Catatan: {', '.join(fund_data.get('summary', {}).get('flags', []))}
    
    INSTRUKSI OUTPUT:
    Buatlah analisis naratif dalam Bahasa Indonesia yang profesional dengan format Markdown.
    Strukturnya harus:
    
    ### ⚡ Insight Utama
    (Satu kalimat kesimpulan apakah saham ini menarik dibeli sekarang atau tidak).
    
    ### 🔍 Analisis Mendalam
    - **Bandarmology:** Jelaskan apa yang dilakukan Big Money/Asing. Apakah mereka akumulasi atau distribusi? Apakah harga sekarang jauh dari harga rata-rata mereka?
    - **Teknikal & Quant:** Jelaskan kondisi tren, momentum, dan apakah harga "Murah" atau "Mahal" secara statistik (Z-Score). Sebutkan support terdekat.
    - **Fundamental:** Sekilas tentang keamanan berinvestasi di saham ini.
    
    ### 🎯 Strategi Trading
    - **Action:** (BUY / WAIT / SELL)
    - **Alasan:** (Poin singkat kenapa)
    - **Area Beli Ideal:** (Saran harga berdasarkan Pivot S1 atau Avg Bandar)
    
    Gunakan gaya bahasa yang objektif, tidak bertele-tele, dan fokus pada profitabilitas.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Maaf, AI sedang sibuk atau terjadi kesalahan koneksi: {str(e)}"