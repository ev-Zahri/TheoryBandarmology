import cot_reports as cot
import pandas as pd
import os
import re
from datetime import datetime

def get_full_cot_analysis(start_date, end_date, export_csv=True):
    dt_start = pd.to_datetime(start_date)
    dt_end = pd.to_datetime(end_date)
    years_to_fetch = list(range(dt_start.year, dt_end.year + 1))
    
    all_frames = []
    for year in years_to_fetch:
        print(f"[LOG] Fetching data year {year}...")
        try:
            df = cot.cot_year(year, 'legacy_fut')
            if df is not None: all_frames.append(df)
        except Exception as e: print(f"[ERR] {year}: {e}")

    if not all_frames: return None

    df_raw = pd.concat(all_frames, ignore_index=True)
    # Normalisasi: lowercase + ganti semua karakter non-alphanumeric dengan underscore
    df_raw.columns = [re.sub(r'[^a-z0-9]+', '_', str(c).strip().lower()).strip('_') for c in df_raw.columns]

    # Filter instrumen USD INDEX:
    # - Pre-2022 : "U.S. DOLLAR INDEX - ICE FUTURES U.S."
    # - Post-2022: "USD INDEX - ICE FUTURES U.S."
    market_col = next((c for c in df_raw.columns if 'market' in c and 'exchange' in c), None)
    if market_col is None:
        print("[ERR] Kolom market/exchange tidak ditemukan.")
        return None
    usd_mask = df_raw[market_col].str.contains(
        r"(?:USD INDEX|U\.S\. DOLLAR INDEX).*ICE FUTURES U\.S\.",
        na=False, case=False, regex=True
    )
    usd_df = df_raw[usd_mask].copy()

    if usd_df.empty:
        print("[ERR] Tidak ada data USD INDEX ditemukan. Cek nama instrumen di data.")
        print(f"[INFO] Contoh nama instrumen: {df_raw[market_col].unique()[:5]}")
        return None

    print(f"[INFO] {len(usd_df)} baris data USD INDEX ditemukan.")

    # --- MAPPING KOLOM LENGKAP (ALL POSITIONS, CHANGES, PERCENT OF OPEN INTEREST) ---
    columns_to_extract = {
        # Dasar
        'as_of_date_in_form_yymmdd': 'Date',
        'open_interest_all': 'OI_All',

        # Non-Commercial (Speculators)
        'noncommercial_positions_long_all': 'NonComm_Long',
        'noncommercial_positions_short_all': 'NonComm_Short',
        'noncommercial_positions_spreading_all': 'NonComm_Spreading',

        # Commercial (Hedgers)
        'commercial_positions_long_all': 'Comm_Long',
        'commercial_positions_short_all': 'Comm_Short',

        # Total Reportable
        'total_reportable_positions_long_all': 'Total_Rept_Long',
        'total_reportable_positions_short_all': 'Total_Rept_Short',

        # Non-Reportable (Small Traders)
        'nonreportable_positions_long_all': 'NonRept_Long',
        'nonreportable_positions_short_all': 'NonRept_Short',

        # --- CHANGES (Perubahan dari Minggu Lalu) ---
        'change_in_open_interest_all': 'Change_OI',
        'change_in_noncommercial_long_all': 'Change_NonComm_Long',
        'change_in_noncommercial_short_all': 'Change_NonComm_Short',
        'change_in_noncommercial_spreading_all': 'Change_NonComm_Spreading',
        'change_in_commercial_long_all': 'Change_Comm_Long',
        'change_in_commercial_short_all': 'Change_Comm_Short',
        'change_in_total_reportable_long_all': 'Change_Total_Rept_Long',
        'change_in_total_reportable_short_all': 'Change_Total_Rept_Short',
        'change_in_nonreportable_long_all': 'Change_NonRept_Long',
        'change_in_nonreportable_short_all': 'Change_NonRept_Short',

        # --- PERCENT OF OPEN INTEREST ---
        'of_oi_noncommercial_long_all': 'Pct_NonComm_Long',
        'of_oi_noncommercial_short_all': 'Pct_NonComm_Short',
        'of_oi_commercial_long_all': 'Pct_Comm_Long',
        'of_oi_commercial_short_all': 'Pct_Comm_Short',
    }


    # Ekstraksi dan Rename (hanya kolom yang ada di data)
    available_cols = {k: v for k, v in columns_to_extract.items() if k in usd_df.columns}
    print(f"[INFO] Kolom berhasil dicocokkan: {list(available_cols.values())}")
    final_df = usd_df[list(available_cols.keys())].rename(columns=available_cols)

    # Parsing & Calculations
    final_df['Date'] = pd.to_datetime(final_df['Date'], format='%y%m%d')

    # Pastikan semua kolom posisi adalah numerik
    numeric_cols = [c for c in final_df.columns if c != 'Date']
    final_df[numeric_cols] = final_df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Analisis: Net Positions (aman jika kolom tidak ada)
    if 'NonComm_Long' in final_df.columns and 'NonComm_Short' in final_df.columns:
        final_df['Net_NonComm'] = final_df['NonComm_Long'] - final_df['NonComm_Short']
    if 'Comm_Long' in final_df.columns and 'Comm_Short' in final_df.columns:
        final_df['Net_Comm'] = final_df['Comm_Long'] - final_df['Comm_Short']
    if 'NonRept_Long' in final_df.columns and 'NonRept_Short' in final_df.columns:
        final_df['Net_NonRept'] = final_df['NonRept_Long'] - final_df['NonRept_Short']


    final_df = final_df.sort_values('Date', ascending=False) # Terbaru di atas
    
    # Filter tanggal sesuai input
    final_df = final_df[(final_df['Date'] >= dt_start) & (final_df['Date'] <= dt_end)]

    if export_csv:
        path = f"./cot_data/COT_USD_INDEX_{dt_start.year}_{dt_end.year}.csv"
        final_df.to_csv(path, index=False)
        print(f"[SUCCESS] Full data exported to: {path}")

    return final_df

# --- RUN ---
full_data = get_full_cot_analysis('2010-01-01', '2020-12-31')
print(full_data.head())