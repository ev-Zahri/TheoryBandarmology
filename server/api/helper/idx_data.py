import pandas as pd
import ssl

# --- BACKUP MANUAL (Jika Scraping Gagal) ---
# Kita tetap simpan Top Caps agar competitor landscape relevan (Bluechip vs Bluechip)
# Karena di Wikipedia semua saham dicampur (BBCA dicampur Bank Mini)
TOP_CAPS_MAP = {
    "Financials": ["BBCA", "BBRI", "BMRI", "BBNI", "ARTO", "BRIS", "BBTN", "MEGA"],
    "Consumer Non-Cyclicals": ["ICBP", "INDF", "MYOR", "UNVR", "GGRM", "HMSP", "KLBF", "SIDO", "CPIN", "JPFA"],
    "Basic Materials": ["MDKA", "ANTM", "INCO", "TINS", "BRMS", "MBMA", "INKP", "TKIM", "SMGR", "INTP"],
    "Energy": ["ADRO", "PTBA", "ITMG", "PGAS", "AKRA", "MEDC", "BUMI", "HRUM", "INDY"],
    "Technology": ["GOTO", "BUKA", "EMTK", "DCII", "MTDL"],
    "Healthcare": ["MIKA", "HEAL", "SILO", "KLBF", "SAME"],
    "Infrastructures": ["TLKM", "ISAT", "EXCL", "JSMR", "TBIG", "TOWR", "PGAS"],
    "Properties & Real Estate": ["BSDE", "CTRA", "PWON", "SMRA", "ASRI", "PANI"],
    "Industrials": ["ASII", "UNTR", "HEXA"],
    "Transportation & Logistic": ["BIRD", "ASSA", "TMAS", "SMDR"]
}

# Variable Global Cache
CACHED_SECTOR_MAP = {}

def load_idx_sectors_from_wiki():
    """
    Mengambil 900+ Saham & Sektornya dari Wikipedia secara otomatis.
    """
    global CACHED_SECTOR_MAP
    
    # Jika sudah ada di memori, return saja (biar gak lemot request terus)
    if CACHED_SECTOR_MAP:
        return CACHED_SECTOR_MAP
    
    url = "https://id.wikipedia.org/wiki/Daftar_perusahaan_yang_tercatat_di_Bursa_Efek_Indonesia"
    
    try:
        # Bypass SSL verification error yang kadang muncul di Python
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Pandas ajaib: Baca semua tabel di URL tersebut
        dfs = pd.read_html(url)
        
        # Biasanya tabel utama ada di urutan ke-0 atau ke-1
        # Kita cari tabel yang punya kolom 'Kode' dan 'Sektor'
        target_df = None
        for df in dfs:
            if 'Kode' in df.columns and 'Sektor' in df.columns:
                target_df = df
                break
        
        if target_df is None:
            print("⚠️ Gagal menemukan tabel saham di Wikipedia. Menggunakan Backup.")
            CACHED_SECTOR_MAP = TOP_CAPS_MAP
            return TOP_CAPS_MAP
            
        # Proses Dataframe ke Dictionary
        # Format: {'Energy': ['ADRO', 'PTBA', ...], 'Financials': [...]}
        new_map = {}
        
        for index, row in target_df.iterrows():
            ticker = str(row['Kode']).strip()
            # Wikipedia kadang nulis sektor dengan bahasa Indonesia/Inggris campur
            # Kita ambil raw-nya saja
            sector_raw = str(row['Sektor']).strip()
            
            # Mapping nama sektor Wiki ke Standar kita (Opsional, agar rapi)
            # Contoh: "Keuangan" -> "Financials"
            # Tapi untuk sekarang biarkan raw agar lengkap
            
            if sector_raw not in new_map:
                new_map[sector_raw] = []
            
            new_map[sector_raw].append(ticker)
            
        print(f"✅ Sukses load {len(target_df)} saham dari Wikipedia!")
        CACHED_SECTOR_MAP = new_map
        return new_map

    except Exception as e:
        print(f"⚠️ Error Scraping Wikipedia: {e}. Menggunakan Data Backup.")
        CACHED_SECTOR_MAP = TOP_CAPS_MAP
        return TOP_CAPS_MAP

def get_competitors(sector: str, current_stock: str):
    # 1. Load Data (Otomatis cek Wiki atau Cache)
    sector_map = load_idx_sectors_from_wiki()
    
    # 2. Cari kandidat di sektor yang sama
    # Kita coba cari key yang mirip (Case insensitive search) karena nama sektor yfinance vs wiki beda
    # yfinance: "Financial Services" | Wiki: "Keuangan" atau "Financials"
    
    candidates = []
    
    # Coba match persis dulu (dari Backup Manual)
    if sector in sector_map:
        candidates = sector_map[sector]
    else:
        # Jika tidak ketemu, coba cari dari seluruh map yang ada di Wiki
        # Ini logika 'fuzzy' sederhana
        for key, stocks in sector_map.items():
            # Jika kata pertama cocok (misal 'Energy' cocok dengan 'Energy & Mineral')
            if sector.split()[0] in key or key.split()[0] in sector:
                candidates.extend(stocks)
                break # Ambil satu kategori terdekat saja
    
    # Fallback: Jika masih kosong, pakai Backup Manual 'Financials' sebagai default/random
    if not candidates:
        candidates = TOP_CAPS_MAP.get("Financials", [])

    # 3. Filter saham diri sendiri
    competitors = [s for s in candidates if s != current_stock]
    
    # 4. Filter Quality (PENTING):
    # Masalah Wikipedia adalah dia mencampur saham Gocap dengan Bluechip.
    # Kita harus memprioritaskan saham yang ada di list TOP_CAPS_MAP jika ada.
    
    priority_competitors = []
    other_competitors = []
    
    # Flatten list top caps untuk pengecekan cepat
    all_top_caps = [item for sublist in TOP_CAPS_MAP.values() for item in sublist]
    
    for comp in competitors:
        if comp in all_top_caps:
            priority_competitors.append(comp)
        else:
            other_competitors.append(comp)
            
    # Gabungkan: Prioritas dulu, baru sisanya
    final_list = priority_competitors + other_competitors
    
    # Ambil 4 teratas
    return final_list[:4]