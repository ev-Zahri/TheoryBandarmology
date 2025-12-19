import yfinance as yf

def get_company_profile(stock_code: str):
    ticker_code = f"{stock_code}.JK"
    ticker = yf.Ticker(ticker_code)
    
    try:
        info = ticker.info
    except Exception as e:
        return {"error": f"Gagal mengambil data profil: {str(e)}"}

    # --- 1. BUSINESS MODEL & IDENTITY ---
    # Mengambil deskripsi bisnis
    summary = info.get('longBusinessSummary', 'Deskripsi tidak tersedia.')
    sector = info.get('sector', 'Unknown')
    industry = info.get('industry', 'Unknown')
    website = info.get('website', '#')
    employees = info.get('fullTimeEmployees', 0)
    founded = info.get('firstTradeDateEpochUtc', None) 
    
    # --- 2. MANAGEMENT TEAM (Directors) ---
    # YFinance biasanya mengembalikan list officers
    officers_raw = info.get('companyOfficers', [])
    management_team = []
    
    # Ambil max 6 orang penting
    for officer in officers_raw[:6]:
        name = officer.get('name', 'Unknown')
        title = officer.get('title', 'Position Unknown')
        
        # Trik: Gunakan UI Avatars untuk generate foto placeholder yang keren
        safe_name = name.replace(" ", "+")
        photo_url = f"https://ui-avatars.com/api/?name={safe_name}&background=0D8ABC&color=fff&size=128"
        
        management_team.append({
            "name": name,
            "position": title,
            "photo_url": photo_url
        })

    # --- 3. SHAREHOLDER STRUCTURE (Kepemilikan) ---
    # Data yfinance: heldPercentInsiders & heldPercentInstitutions
    pct_insider = info.get('heldPercentInsiders', 0)
    pct_institution = info.get('heldPercentInstitutions', 0)
    
    # Konversi ke persen
    if pct_insider < 1.0: pct_insider *= 100
    if pct_institution < 1.0: pct_institution *= 100
    
    # Hitung Masyarakat (Public)
    pct_public = 100 - (pct_insider + pct_institution)
    if pct_public < 0: pct_public = 0 

    shareholders = [
        {"name": "Institutions (Big Money)", "percent": round(pct_institution, 2), "color": "#3b82f6"}, # Blue
        {"name": "Insiders (Pemilik/Manajemen)", "percent": round(pct_insider, 2), "color": "#22c55e"}, # Green
        {"name": "Public (Masyarakat)", "percent": round(pct_public, 2), "color": "#94a3b8"} # Gray
    ]
    
    # Sorting biar yang terbesar di atas
    shareholders = sorted(shareholders, key=lambda x: x['percent'], reverse=True)

    # --- 4. DATA TAMBAHAN (Timeline/History) ---
    # Karena tidak ada timeline spesifik, kita return tahun IPO/Berdiri jika ada
    info.get('governanceEpochDate')
    
    return {
        "status": "success",
        "identity": {
            "name": info.get('longName', stock_code),
            "symbol": stock_code,
            "sector": sector,
            "industry": industry,
            "website": website,
            "employees": employees,
            "description": summary
        },
        "business_model": {
            "revenue_stream_desc": f"Perusahaan ini beroperasi di sektor {sector}, industri {industry}.",
            "key_activities": summary
        },
        "management": management_team,
        "shareholders": shareholders,
        "history": {
            "founded_summary": f"Data historis spesifik tidak tersedia via API publik, namun perusahaan ini terdaftar aktif di sektor {sector}."
        }
    }