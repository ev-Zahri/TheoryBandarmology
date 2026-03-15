import cot_reports as cot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_cot_data_robust(year=2024):
    print(f"[LOG] Mencoba mengambil data tahun {year}...")
    
    try:
        # Mengambil data menggunakan library
        df = cot.cot_year(year, 'legacy_fut')
        
        if df is None or df.empty:
            print("[ERROR] DataFrame kosong.")
            return None

        # --- STRATEGI DEFENSIF: Normalisasi Kolom ---
        # Kita buat mapping: { 'nama_kolom_asli': 'nama_kolom_bersih' }
        original_cols = df.columns.tolist()
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Cari kolom market name secara dinamis
        market_col = None
        for col in df.columns:
            if 'market' in col and 'exchange' in col:
                market_col = col
                break
        
        if not market_col:
            print(f"[DEBUG] Kolom tersedia: {df.columns.tolist()}")
            print("[ERROR] Kolom Market/Exchange tidak ditemukan.")
            return None

        print(f"[LOG] Menggunakan kolom: '{market_col}' untuk identifikasi instrumen.")

        # --- FILTERING ---
        # Cari baris yang mengandung "U.S. DOLLAR INDEX"
        usd_mask = df[market_col].str.contains("U.S. DOLLAR INDEX", na=False, case=False)
        usd_df = df[usd_mask].copy()

        if usd_df.empty:
            print("[ERROR] Data USD INDEX tidak ditemukan dalam file.")
            return None

        # --- MAPPING DATA PENTING ---
        # Mencari kolom tanggal dan posisi secara dinamis
        date_col = [c for c in df.columns if 'date' in c and 'form' in c][0]
        long_col = [c for c in df.columns if 'noncomm' in c and 'long' in c and 'all' in c][0]
        short_col = [c for c in df.columns if 'noncomm' in c and 'short' in c and 'all' in c][0]

        # Buat dataframe hasil yang bersih
        result = pd.DataFrame({
            'Date': pd.to_datetime(usd_df[date_col], format='%y%m%d'),
            'Long': pd.to_numeric(usd_df[long_col]),
            'Short': pd.to_numeric(usd_df[short_col])
        })
        
        result['Net_Position'] = result['Long'] - result['Short']
        result = result.sort_values('Date')

        print(f"[SUCCESS] Berhasil memproses {len(result)} data poin.")
        return result

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan kritis: {e}")
        return None

# --- RUN ---
df_final = get_cot_data_robust(2024)

if df_final is not None:
    plt.figure(figsize=(12, 6))
    sns.set_style("darkgrid")
    
    # Area chart: Hijau jika Net > 0, Merah jika Net < 0
    plt.fill_between(df_final['Date'], df_final['Net_Position'], 
                     where=(df_final['Net_Position'] >= 0), color='g', alpha=0.3)
    plt.fill_between(df_final['Date'], df_final['Net_Position'], 
                     where=(df_final['Net_Position'] < 0), color='r', alpha=0.3)
    
    sns.lineplot(data=df_final, x='Date', y='Net_Position', color='black', linewidth=1.5)
    
    plt.axhline(0, color='black', linestyle='--')
    plt.title('USD Index (DXY) Net Speculative Position - 2024', fontsize=14)
    plt.ylabel('Net Contracts')
    plt.tight_layout()
    plt.show()