import yfinance as yf
from api.helper.idx_data import get_competitors
from api.service_stock.master_data import get_company_profile as get_cached_profile, get_stock_fundamental_data

def get_company_profile(stock_code: str):
    """
    Get company profile with master data integration.
    Uses cached data first, falls back to yfinance if not available.
    """
    # Try to get from master data cache first
    cached_data = get_stock_fundamental_data(stock_code)
    
    # If we have cached data, use it for basic info
    if cached_data:
        sector = cached_data.get('sector', 'Unknown')
        industry = cached_data.get('industry', 'Unknown')
        company_name = cached_data.get('company_name', stock_code)
        website = cached_data.get('website', '#')
        employees = cached_data.get('employees', 0)
        description = cached_data.get('description', 'Deskripsi tidak tersedia.')
        
        # For detailed data (management, dividends), still need yfinance
        ticker_code = f"{stock_code}.JK"
        ticker = yf.Ticker(ticker_code)
        
        try:
            info = ticker.info
        except Exception as e:
            # If yfinance fails, use cached data only
            info = {}
    else:
        # No cached data, use yfinance entirely
        ticker_code = f"{stock_code}.JK"
        ticker = yf.Ticker(ticker_code)
        
        try:
            info = ticker.info
        except Exception as e:
            return {"error": f"Gagal mengambil data profil: {str(e)}"}
        
        # Extract from yfinance
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        company_name = info.get('longName', stock_code)
        website = info.get('website', '#')
        employees = info.get('fullTimeEmployees', 0)
        description = info.get('longBusinessSummary', 'Deskripsi tidak tersedia.')

    # --- 1. BUSINESS MODEL & IDENTITY ---
    founded = info.get('firstTradeDateEpochUtc', None) if info else None
    
    # --- 2. MANAGEMENT TEAM (Directors) ---
    officers_raw = info.get('companyOfficers', []) if info else []
    management_team = []
    
    for officer in officers_raw[:6]:
        name = officer.get('name', 'Unknown')
        title = officer.get('title', 'Position Unknown')
        safe_name = name.replace(" ", "+")
        photo_url = f"https://ui-avatars.com/api/?name={safe_name}&background=0D8ABC&color=fff&size=128"
        
        management_team.append({
            "name": name,
            "position": title,
            "photo_url": photo_url
        })

    # --- 3. SHAREHOLDER STRUCTURE ---
    pct_insider = info.get('heldPercentInsiders', 0) if info else 0
    pct_institution = info.get('heldPercentInstitutions', 0) if info else 0
    
    if pct_insider < 1.0: pct_insider *= 100
    if pct_institution < 1.0: pct_institution *= 100
    
    pct_public = 100 - (pct_insider + pct_institution)
    if pct_public < 0: pct_public = 0 

    shareholders = [
        {"name": "Institutions (Big Money)", "percent": round(pct_institution, 2), "color": "#3b82f6"},
        {"name": "Insiders (Pemilik/Manajemen)", "percent": round(pct_insider, 2), "color": "#22c55e"},
        {"name": "Public (Masyarakat)", "percent": round(pct_public, 2), "color": "#94a3b8"}
    ]
    
    shareholders = sorted(shareholders, key=lambda x: x['percent'], reverse=True)

    # --- 4. DATA TAMBAHAN ---
    ipo = info.get('governanceEpochDate') if info else None

    # --- 5. COMPETITORS ---
    competitors = get_competitors(sector, stock_code)
    competitors_data = []
    for comp in competitors:
        competitors_data.append({
            "ticker": comp,
            "name": f"Competitor {comp}",
            "sector": sector
        })

    # --- 6. DIVIDEND ---
    dividends_data = []
    try:
        if ticker:
            divs = ticker.dividends
            if not divs.empty:
                recent_divs = divs.sort_index(ascending=False).head(5)
                for date, value in recent_divs.items():
                    dividends_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "amount": value,
                        "year": date.year
                    })
    except Exception as e:
        print(f"⚠️ Error mengambil data dividen: {e}")
        pass
    
    return {
        "status": "success",
        "data_source": "master_data" if cached_data else "yfinance",
        "identity": {
            "name": company_name,
            "symbol": stock_code,
            "sector": sector,
            "industry": industry,
            "website": website,
            "employees": employees,
            "description": description,
            "address": f"{info.get('address1', '') if info else ''}, {info.get('city', '') if info else ''}",
            "ipo": ipo,
        },
        "business_model": {
            "revenue_stream_desc": f"Perusahaan ini beroperasi di sektor {sector}, industri {industry}.",
            "key_activities": description
        },
        "management": management_team,
        "shareholders": shareholders,
        "competitors": competitors_data,
        "dividends": dividends_data,
        "history": {
            "founded_summary": f"Data historis spesifik tidak tersedia via API publik, namun perusahaan ini terdaftar aktif di sektor {sector}."
        }
    }